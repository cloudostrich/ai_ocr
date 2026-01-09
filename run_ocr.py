import argparse
import sys
import os
from ocr_engines.tesseract import TesseractOCR

def main():
    parser = argparse.ArgumentParser(description="Run OCR on a specific file.")
    parser.add_argument("filename", help="Path to the file to process (image or PDF).")
    parser.add_argument("--engine", choices=['tesseract', 'paddle', 'nanonets'], default='tesseract', help="OCR engine to use (default: tesseract)")
    args = parser.parse_args()

    filepath = args.filename
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Processing: {filepath} using {args.engine} engine")
    
    engine = None
    if args.engine == 'tesseract':
        engine = TesseractOCR()
    elif args.engine == 'paddle':
        from ocr_engines.paddle import PaddleOCREngine
        engine = PaddleOCREngine()
    elif args.engine == 'nanonets':
        from ocr_engines.nanonets import NanonetsOCR
        engine = NanonetsOCR()
        
    try:
        text = engine.extract_text(filepath)
        print("\n--- OCR Result ---\n")
        print(text)
        print("\n------------------\n")
    except Exception as e:
        print(f"Error during OCR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
