from ocr_engines.tesseract import TesseractOCR
from ocr_engines.paddle import PaddleOCREngine
# from ocr_engines.nanonets import NanonetsOCR

def get_ocr_engine(engine_type):
    if engine_type == "tesseract":
        return TesseractOCR()
    elif engine_type == "paddle":
        return PaddleOCREngine()
    elif engine_type == "nanonets":
        # return NanonetsOCR()
        pass
    else:
        raise ValueError("Unknown engine")

# --- Your Agent Logic ---
selected_engine = "paddle"  # Change this string to switch versions!
ocr = get_ocr_engine(selected_engine)

text = ocr.extract_text("document.jpg")
print(f"Agent sees: {text}")

# Pass 'text' to llama-cpp-python...
