import pytesseract
import gc
from pdf2image import convert_from_path, pdfinfo_from_path
from .base import OCREngine

class TesseractOCR(OCREngine):
    def extract_text(self, image_path: str) -> str:
        if image_path.lower().endswith('.pdf'):
            print(f"Processing PDF: {image_path}")
            
            info = pdfinfo_from_path(image_path)
            total_pages = info["Pages"]
            text = ""
            
            for i in range(1, total_pages + 1):
                print(f"  - OCRing page {i}/{total_pages}...")
                
                # Load only ONE page at a time
                images = convert_from_path(image_path, first_page=i, last_page=i)
                if not images:
                    continue
                
                image = images[0]
                text += f"--- Page {i} ---\n"
                text += pytesseract.image_to_string(image) + "\n"
                
                # Cleanup
                del image
                del images
                gc.collect()
                
            return text
        else:
            return pytesseract.image_to_string(image_path)
    
    def cleanup(self):
        """Tesseract is an external process, but we call gc for safety."""
        gc.collect()
