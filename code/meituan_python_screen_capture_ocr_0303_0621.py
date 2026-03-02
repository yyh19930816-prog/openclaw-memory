#!/usr/bin/env python3
# Source: https://github.com/dynobo/normcap
# Date: 2023-08-21
# Description: OCR powered screen-capture tool to capture information instead of images

import sys
import platform
from pathlib import Path
from typing import Optional, Tuple

try:
    import mss
    import pytesseract
    import pyperclip
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required package - {e.name}")
    print("Install with: pip install mss pytesseract pillow pyperclip")
    sys.exit(1)


class NormCap:
    """Main class implementing OCR screen capture functionality."""

    def __init__(self):
        self.tesseract_cmd = self._get_tesseract_path()
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

    def _get_tesseract_path(self) -> Path:
        """Get path to Tesseract OCR executable based on platform."""
        if platform.system() == "Windows":
            return Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
        elif platform.system() == "Darwin":  # macOS
            return Path("/usr/local/bin/tesseract")
        else:  # Linux
            return Path("/usr/bin/tesseract")

    def capture_screen(self) -> Optional[Image.Image]:
        """Capture screen region using mouse selection."""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                print("Select region to capture (drag mouse)...")
                
                # Get selection coordinates from mouse
                from Xlib.display import Display
                display = Display()
                screen = display.screen()
                root = screen.root
                
                # Wait for mouse button press
                print("Click and drag to select region...")
                start_event = root.query_pointer()._data
                end_event = None
                
                # Wait for mouse button release
                while not end_event or end_event["mask"] & 0x100:  # Button1 mask
                    end_event = root.query_pointer()._data
                
                # Calculate selection rectangle
                x1, y1 = start_event["root_x"], start_event["root_y"]
                x2, y2 = end_event["root_x"], end_event["root_y"]
                left, top = min(x1, x2), min(y1, y2)
                width, height = abs(x2 - x1), abs(y2 - y1)
                
                # Capture selected region
                region = {"top": top, "left": left, "width": width, "height": height}
                sct_img = sct.grab(region)
                return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    def extract_text(self, image: Image.Image) -> Optional[str]:
        """Extract text from image using Tesseract OCR."""
        try:
            return pytesseract.image_to_string(image).strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return None

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard."""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Clipboard Error: {e}")
            return False

    def run(self) -> None:
        """Main execution flow: capture -> OCR -> copy to clipboard."""
        print("NormCap - OCR Screen Capture Tool")
        
        image = self.capture_screen()
        if not image:
            print("Failed to capture screen region")
            return
            
        text = self.extract_text(image)
        if not text:
            print("No text extracted from selection")
            return
            
        if self.copy_to_clipboard(text):
            print(f"Copied to clipboard: {text[:50]}...")
        else:
            print("Failed to copy to clipboard")


if __name__