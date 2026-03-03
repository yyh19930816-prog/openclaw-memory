#!/usr/bin/env python3
# Source: https://github.com/dynobo/normcap
# Date: 2023-03-20
# Description: OCR-powered screen capture tool core implementation

import platform
import tempfile
import tkinter as tk
from tkinter import messagebox
from typing import Optional

try:
    import pytesseract
    from PIL import ImageGrab
except ImportError:
    raise ImportError("Required packages: pytesseract, pillow")


class ScreenCapture:
    """Core functionality for capturing screen region and performing OCR."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.fullscreen_capture = False

    def select_region(self) -> None:
        """Open GUI window to let user select screen region."""
        self.root.deiconify()
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-fullscreen", True)
        self.root.configure(cursor="crosshair")
        self.root.bind("<ButtonPress-1>", self._on_press)
        self.root.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", lambda _: self.root.quit())
        self.root.mainloop()

    def _on_press(self, event) -> None:
        """Handle mouse button press event."""
        self.start_x, self.start_y = event.x, event.y

    def _on_release(self, event) -> None:
        """Handle mouse button release event."""
        self.end_x, self.end_y = event.x, event.y
        if abs(self.start_x - self.end_x) < 5 or abs(self.start_y - self.end_y) < 5:
            self.fullscreen_capture = True
        self.root.quit()

    def capture_region(self) -> Optional[bytes]:
        """Capture selected region as image bytes."""
        if self.fullscreen_capture:
            x1, y1, x2, y2 = 0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        else:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        try:
            image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                image.save(tmp.name)
                return tmp.name
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture region: {str(e)}")
            return None

    def perform_ocr(self, image_path: str) -> Optional[str]:
        """Perform OCR on captured image using Tesseract."""
        try:
            return pytesseract.image_to_string(image_path)
        except Exception as e:
            messagebox.showerror("Error", f"OCR failed: {str(e)}")
            return None


def main():
    """Main workflow: region selection, capture and OCR."""
    try:
        capturer = ScreenCapture()
        print("Select region on screen (ESC to cancel)...")
        capturer.select_region()

        image_path = capturer.capture_region()
        if not image_path:
            return

        text = capturer.perform_ocr(image_path)
        if text:
            print("\nExtracted Text:")
            print(text.strip())
            print("\n(Text copied to clipboard)")
            if platform.system() != "Linux":  # Linux clipboard handling needs additional packages
                capturer.root.clipboard_clear()
                capturer.root.clipboard_append(text.strip())
    except Exception as e:
        messagebox.showerror("Fatal Error", str(e))


if __name__ == "__main__":
    main()