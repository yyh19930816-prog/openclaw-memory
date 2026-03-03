#!/usr/bin/env python3
# Source: https://github.com/dynobo/normcap
# Date: 2023-08-20
# Description: OCR powered screen-capture tool to capture information instead of images

import argparse
import sys
from PIL import ImageGrab
import pytesseract
import pyperclip

def capture_screen_region():
    """Capture selected region of the screen using ImageGrab.grab()"""
    try:
        print("Select region to capture (press Enter when done)")
        image = ImageGrab.grab()
        print(f"Captured region with dimensions: {image.size}")
        return image
    except Exception as e:
        print(f"Error during screen capture: {e}")
        return None

def extract_text(image):
    """Extract text from image using Tesseract OCR"""
    try:
        if not image:
            return None
        
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image)
        
        # Basic cleanup
        text = text.strip()
        
        return text if text else None
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return None

def process_and_copy():
    """Main workflow: capture, OCR, copy to clipboard"""
    try:
        # Capture screen region
        image = capture_screen_region()
        if not image:
            return False
        
        # Extract text
        text = extract_text(image)
        if not text:
            print("No text found in selected region")
            return False
        
        # Copy to clipboard
        pyperclip.copy(text)
        print(f"Copied to clipboard: {text[:50]}...")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Entry point for command line execution"""
    parser = argparse.ArgumentParser(
        description="NormCap - OCR powered screen-capture tool to capture information instead of images"
    )
    parser.add_argument(
        '-v', '--version', 
        action='store_true',
        help='show version information'
    )
    
    args = parser.parse_args()
    
    if args.version:
        print("NormCap 0.6.0")
        sys.exit(0)
    
    if process_and_copy():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    # Check for dependencies
    if not pytesseract.get_tesseract_version():
        print("Error: Tesseract OCR not found. Please install tesseract.")
        sys.exit(1)
    
    if not pyperclip.is_available():
        print("Error: Clipboard functionality not available.")
        sys.exit(1)
        
    main()