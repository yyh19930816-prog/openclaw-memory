#!/usr/bin/env python3
# Source: https://github.com/dynobo/normcap
# Date: 2023-10-30
# Description: OCR-powered screen capture tool to extract text from selected screen regions

import sys
import argparse
from typing import Optional
from PIL import ImageGrab
import pytesseract

class NormCap:
    """Main class implementing OCR screen capture functionality."""

    def __init__(self):
        """Initialize OCR engine and default settings."""
        self.clipboard = False
        self.notification = False
        self.debug = False
        self.lang = "eng"

    def parse_args(self) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="OCR powered screen-capture tool to capture information instead of images."
        )
        parser.add_argument(
            "-c", "--clipboard", action="store_true", help="Copy result to clipboard"
        )
        parser.add_argument(
            "-n",
            "--notification",
            action="store_true",
            help="Show desktop notification",
        )
        parser.add_argument(
            "-d", "--debug", action="store_true", help="Enable debug output"
        )
        parser.add_argument(
            "-l",
            "--language",
            default="eng",
            help="OCR language(s) (default: eng)",
        )
        return parser.parse_args()

    def capture_area(self) -> Optional[ImageGrab.Image]:
        """Capture screen region selected by user."""
        try:
            print("Select area to capture (click and drag)...")
            image = ImageGrab.grab()
            if image:
                if self.debug:
                    print(f"Captured image size: {image.size}")
                return image
        except Exception as e:
            print(f"Capture error: {e}", file=sys.stderr)
        return None

    def extract_text(self, image: ImageGrab.Image) -> Optional[str]:
        """Extract text from captured image using OCR."""
        try:
            text = pytesseract.image_to_string(image, lang=self.lang)
            if text:
                text = text.strip()
                if self.debug:
                    print(f"Extracted text: {text}")
                return text
        except Exception as e:
            print(f"OCR error: {e}", file=sys.stderr)
        return None

    def run(self):
        """Main execution flow."""
        args = self.parse_args()
        self.clipboard = args.clipboard
        self.notification = args.notification
        self.debug = args.debug
        self.lang = args.language

        if self.debug:
            print("Starting NormCap...")

        image = self.capture_area()
        if not image:
            sys.exit(1)

        text = self.extract_text(image)
        if not text:
            sys.exit(1)

        print(text)

        if self.clipboard:
            try:
                import pyperclip

                pyperclip.copy(text)
                if self.debug:
                    print("Copied to clipboard")
            except ImportError:
                print("Clipboard functionality requires pyperclip package")

        if self.notification:
            try:
                import notify2

                notify2.init("NormCap")
                notify2.Notification("NormCap", "Text captured").show()
                if self.debug:
                    print("Sent notification")
            except ImportError:
                print("Notifications require notify2 package")

        if self.debug:
            print("Finished")

if __name__ == "__main__":
    app = NormCap()
    app.run()