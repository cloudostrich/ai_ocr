import pytesseract
from .base import OCREngine

class TesseractOCR(OCREngine):
    def extract_text(self, image_path: str) -> str:
        if image_path.lower().endswith('.pdf'):
            from pdf2image import convert_from_path
            images = convert_from_path(image_path)
            text = ""
            for i, image in enumerate(images):
                text += f"--- Page {i+1} ---\n"
                text += pytesseract.image_to_string(image) + "\n"
            return text
        else:
            return pytesseract.image_to_string(image_path)
