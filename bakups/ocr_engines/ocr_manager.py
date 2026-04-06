import config
import sys

def get_ocr_agent():
    if config.OCR_ENGINE == "tesseract":
        from ocr_engines.tesseract import TesseractOCR
        return TesseractOCR()
        
    elif config.OCR_ENGINE == "nanonets":
        print("WARNING: Loading Nanonets model. This will use significant RAM.")
        from ocr_engines.nanonets import NanonetsOCR
        return NanonetsOCR()

    elif config.OCR_ENGINE in ["easy", "easyocr"]:
        from ocr_engines.easy import EasyOCREngine
        return EasyOCREngine()
        
    else:
        raise ValueError(f"Unknown Engine: {config.OCR_ENGINE}")
