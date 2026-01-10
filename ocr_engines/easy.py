# ocr_engines/easyocr_engine.py

import easyocr
import numpy as np
from pdf2image import convert_from_path
from .base import OCREngine

class EasyOCREngine(OCREngine):
    def __init__(self):
        print("Loading EasyOCR model...")
        # gpu=False is mandatory for your Mac
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, file_path: str) -> str:
        # 1. Check if it is a PDF
        if file_path.lower().endswith('.pdf'):
            return self._process_pdf(file_path)
        else:
            return self._process_image(file_path)

    def _process_image(self, image_input) -> str:
        """Helper to process a single image (path or numpy array)"""
        try:
            # detail=0 returns just the list of strings
            result_list = self.reader.readtext(image_input, detail=0)
            return " ".join(result_list)
        except Exception as e:
            print(f"Error processing image: {e}")
            return ""

    def _process_pdf(self, pdf_path: str) -> str:
        """Converts PDF to images and OCRs each page"""
        print(f"Processing PDF: {pdf_path}")
        full_text = []
        
        # Convert PDF to list of images (RAM heavy, but usually okay for small docs)
        # fmt="jpeg" is faster and uses less RAM than default ppm
        pages = convert_from_path(pdf_path, dpi=300, fmt="jpeg")

        for i, page in enumerate(pages):
            print(f"  - OCRing page {i+1}/{len(pages)}...")
            
            # Convert PIL image to numpy array for EasyOCR
            page_np = np.array(page)
            
            # Extract text from this page
            page_text = self._process_image(page_np)
            full_text.append(page_text)

        return "\n\n".join(full_text)