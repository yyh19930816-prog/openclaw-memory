#!/usr/bin/env python3
# Source: https://github.com/dynobo/normcap
# Date: 2023-04-25
# Description: OCR powered screen capture tool to extract text from screen regions

import sys
import io
from typing import Optional

import pyperclip
from PIL import Image, ImageGrab
from pytesseract import pytesseract


class NormCap:
    """
    Main application class implementing OCR screen capture functionality.
    
    Features:
    - Select screen region to capture
    - Extract text using Tesseract OCR
    - Copy extracted text to clipboard
    """
    
    def __init__(self):
        """Initialize Tesseract OCR path and check dependencies"""
        # Default Tesseract path - adjust based on your system
        self.tesseract_cmd = 'tesseract'
        
        # Alternative paths for different OS
        if sys.platform == 'win32':
            self.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        elif sys.platform == 'darwin':
            self.tesseract_cmd = '/usr/local/bin/tesseract'
            
        pytesseract.tesseract_cmd = self.tesseract_cmd
    
    def capture_screen(self) -> Optional[Image.Image]:
        """
        Capture screen region using default system screenshot tool.
        
        Returns:
            PIL.Image.Image: Captured image or None if canceled
        """
        try:
            return ImageGrab.grab()
        except Exception as e:
            print(f"Screen capture failed: {e}")
            return None
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image: PIL Image containing text
            
        Returns:
            Extracted text as string
        """
        try:
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"OCR failed: {e}")
            return ""
    
    def copy_to_clipboard(self, text: str) -> bool:
        """
        Copy text to system clipboard.
        
        Args:
            text: String to copy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Clipboard copy failed: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        print("Select region to capture (click and drag)...")
        image = self.capture_screen()
        
        if not image:
            print("Capture canceled")
            return False
            
        print("Processing image...")
        text = self.extract_text(image)
        
        if not text.strip():
            print("No text detected!")
            return False
            
        print("Copying to clipboard...")
        text = text.strip()
        success = self.copy_to_clipboard(text)
        
        if success:
            print(f"Copied:\n{text}")
            return True
        return False


if __name__ == "__main__":
    app = NormCap()
    sys.exit(0 if app.run() else 1)