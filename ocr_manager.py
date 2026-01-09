import config
import sys

def get_ocr_agent():
    if config.OCR_ENGINE == "tesseract":
        from ocr_engines.tesseract import TesseractOCR
        return TesseractOCR()
        
    elif config.OCR_ENGINE == "paddle":
        # Paddle is lazy-loaded so it doesn't eat RAM unless used
        from ocr_engines.paddle import PaddleOCREngine
        return PaddleOCREngine()
        
    elif config.OCR_ENGINE == "nanonets":
        print("WARNING: Loading Nanonets model. This will use significant RAM.")
        from ocr_engines.nanonets import NanonetsOCR
        return NanonetsOCR()
        
    else:
        raise ValueError(f"Unknown Engine: {config.OCR_ENGINE}")
