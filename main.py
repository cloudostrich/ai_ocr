"""
Imports are moved to inside the function to avoid errors if dependencies are missing
from ocr_engines.tesseract import TesseractOCR
from ocr_engines.paddle import PaddleOCREngine
from ocr_engines.nanonets import NanonetsOCR
from ocr_engines.easy import EasyOCREngine

Sample files:
BalanceSheetJuly2024rev.pdf  document.jpg  july2024.pdf  ProfitandLosJuly2024rev.pdf
"""
import argparse
import sys
import os

def get_ocr_engine(engine_type):
    if engine_type == "tesseract":
        from ocr_engines.tesseract import TesseractOCR
        return TesseractOCR()
    # elif engine_type == "paddle":
    #     from ocr_engines.paddle import PaddleOCREngine
    #     return PaddleOCREngine()
    elif engine_type == "nanonets":
        from ocr_engines.nanonets import NanonetsOCR
        return NanonetsOCR()
    elif engine_type in ["easy", "easyocr"]:
        from ocr_engines.easy import EasyOCREngine
        return EasyOCREngine()
    else:
        raise ValueError("Unknown engine")

def main():
    parser = argparse.ArgumentParser(description="Run OCR on a specific file.")
    parser.add_argument("filename", help="Path to the file to process (image or PDF).")
    parser.add_argument("--engine", choices=['tesseract', 'easy', 'nanonets'], default='tesseract', help="OCR engine to use (default: tesseract)")
    args = parser.parse_args()

    filepath = args.filename
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Processing: {filepath} using {args.engine} engine")
    
    engine = None
    if args.engine == 'tesseract':
        engine = get_ocr_engine("tesseract")
    elif args.engine == 'easy':
        engine = get_ocr_engine("easy")
    elif args.engine == 'nanonets':
        engine = get_ocr_engine("nanonets")
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




# --- Your Agent Logic ---



