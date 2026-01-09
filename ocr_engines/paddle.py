#ocr_engines/paddle.py

import os
# --- FIX FOR PYTHON 3.13 CRASH ---
# PaddleOCR's dependency 'modelscope' has a bug in Python 3.13 where it
# checks an env var that doesn't exist. We set it manually here to fix it.
os.environ.setdefault('HUB_DATASET_ENDPOINT', 'https://modelscope.cn/api/v1/datasets')
# ---------------------------------
from paddleocr import PaddleOCR
from .base import OCREngine

class PaddleOCREngine(OCREngine):
    def __init__(self):
        # use_angle_cls=True helps with rotated text
        # lang='en' keeps it lightweight
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def extract_text(self, image_path: str) -> str:
        if image_path.lower().endswith('.pdf'):
            from pdf2image import convert_from_path
            images = convert_from_path(image_path)
            text = ""
            for i, image in enumerate(images):
                # PaddleOCR expects a file path or numpy array. 
                # convert_from_path returns PIL images.
                # We can pass the PIL image directly to the ocr method if checking documentation, 
                # or save it temporarily, or convert to numpy.
                # PaddleOCR supports ndarray which can be got from np.array(pil_image)
                # Note: pdf2image returns RGB (PIL). PaddleOCR expectation depends on how it's used, 
                # but typically mimics cv2.imread which is BGR.
                import numpy as np
                import cv2
                img_array = np.array(image)
                # Convert to BGR for compatibility with cv2-based models
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                result = self.ocr.ocr(img_array)
                if not result or result[0] is None:
                    continue
                    
                page_text = " ".join([line[1][0] for line in result[0]])
                text += f"--- Page {i+1} ---\n"
                text += page_text + "\n"
            return text
        else:
            result = self.ocr.ocr(image_path)
            if not result or result[0] is None:
                return ""
            # Flatten the list of results to just get the text
            text = " ".join([line[1][0] for line in result[0]])
            return text
