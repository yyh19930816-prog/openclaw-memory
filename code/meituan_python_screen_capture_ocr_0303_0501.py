#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NormCap - OCR powered screen-capture tool
Source: https://github.com/dynobo/normcap
Created: 2023-11-15
Description: Captures screen regions using OCR to extract text instead of images
"""

import argparse
import sys
import tempfile
from pathlib import Path

try:
    import pytesseract
    from PIL import ImageGrab, Image
    import pyperclip
except ImportError as e:
    print(f"Error: Required packages not found. Install with:\n"
          f"pip install pytesseract pillow pyperclip")
    sys.exit(1)


class NormCap:
    """Main application class for NormCap OCR screen capture."""

    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="normcap_"))
        self.output_file = self.temp_dir / "capture.png"

    def capture_region(self):
        """
        Captures a region of the screen selected by the user.
        
        Returns:
            Image: PIL Image object of the captured region
        """
        print("Select region to capture...")
        try:
            # On Linux may need to use alternative capture method
            return ImageGrab.grab()
        except Exception as e:
            print(f"Capture failed: {e}")
            return None

    def extract_text(self, image):
        """
        Extracts text from captured image using Tesseract OCR.
        
        Args:
            image (Image): PIL Image to process
            
        Returns:
            str: Extracted text or empty string if failed
        """
        if not image:
            return ""
            
        try:
            # Save temporary image for OCR processing
            image.save(self.output_file)
            
            # Configure Tesseract (language can be parameterized)
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                str(self.output_file),
                config=custom_config
            )
            return text.strip()
        except Exception as e:
            print(f"OCR failed: {e}")
            return ""

    def copy_to_clipboard(self, text):
        """
        Copies extracted text to system clipboard.
        
        Args:
            text (str): Text to copy
        """
        if text:
            pyperclip.copy(text)
            print("Text copied to clipboard!")
        else:
            print("No text was extracted.")

    def run(self):
        """Main execution flow: capture -> OCR -> clipboard."""
        parser = argparse.ArgumentParser(
            description="NormCap - OCR powered screen capture tool"
        )
        parser.parse_args()
        
        image = self.capture_region()
        if image:
            text = self.extract_text(image)
            self.copy_to_clipboard(text)


def main():
    """Entry point for NormCap application."""
    try:
        NormCap().run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()