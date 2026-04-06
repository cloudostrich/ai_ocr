# ocr_engines/nanonets.py
import os
import gc
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler # Generic handler, usually works for Qwen2-VL if configured
from .base import OCREngine

# mungert_Nanonets-OCR2-3B-q4_0.gguf, Nanonets-OCR2-3B-q8_0.mmproj
# mungert_Nanonets-OCR2-1.5B-exp-q4_0.gguf , Nanonets-OCR2-1.5B-exp.mmproj-Q8_0.gguf
# Nanonets-OCR2-1.5B-exp.i1-Q4_K_M.gguf
class NanonetsOCR(OCREngine):
    def __init__(self):
        # 1. PATHS
        # Use absolute path to ensure reliability
        base_path = os.path.abspath("models/nanonets")
        model_path = os.path.join(base_path, "Nanonets-OCR2-1.5B-exp.i1-Q4_K_M.gguf")
        # Filename from directory listing
        mmproj_path = os.path.join(base_path, "Nanonets-OCR2-1.5B-exp.mmproj-Q8_0.gguf")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        if not os.path.exists(mmproj_path):
            raise FileNotFoundError(f"Vision adapter not found at {mmproj_path}")

        # 2. Setup the Vision Handler
        self.chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)

        # 3. Load the Model
        print(f"Loading Nanonets GGUF from {model_path}...")
        self.llm = Llama(
            model_path=model_path,
            chat_handler=self.chat_handler,
            n_ctx=4096,
            n_gpu_layers=0, # CPU only
            verbose=False # Set to false to reduce noise unless debugging
        )

    def extract_text(self, image_path: str) -> str:
        if image_path.lower().endswith('.pdf'):
            from pdf2image import convert_from_path
            
            # Process PDF page by page to save RAM
            print(f"Processing PDF: {image_path}")
            
            # Use generator/iterator if possible, or just open and process one by one
            # pdf2image.convert_from_path returns a list, which is RAM heavy.
            # However, we can use the 'last_page' and 'first_page' params to loop.
            from pdf2image import pdfinfo_from_path
            info = pdfinfo_from_path(image_path)
            total_pages = info["Pages"]
            
            full_text = ""
            for page_num in range(1, total_pages + 1):
                print(f"Processing Page {page_num}/{total_pages}...")
                
                # Load only ONE page at a time
                images = convert_from_path(image_path, first_page=page_num, last_page=page_num)
                if not images:
                    continue
                image = images[0]
                
                # Save temp file for the LLM to read
                temp_path = f"temp_nanonets_page_{page_num}.png"
                image.save(temp_path)
                
                page_text = self._process_image(temp_path)
                full_text += f"\n--- Page {page_num} ---\n{page_text}"
                
                # Immediate cleanup of page objects
                del image
                del images
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                gc.collect()
                
            return full_text
        else:
            return self._process_image(image_path)

    def _process_image(self, image_path: str) -> str:
        image_url = f"file://{os.path.abspath(image_path)}"
        response = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image perfectly. Do not summarize. Return only the text found."},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=1024,
            temperature=0.1
        )
        return response["choices"][0]["message"]["content"]
    
    def cleanup(self):
        """Free memory used by the Llama model."""
        if hasattr(self, 'llm'):
            print("Cleaning up Nanonets resources...")
            # llama-cpp-python models can be heavy; deleting them helps
            del self.llm
            if hasattr(self, 'chat_handler'):
                del self.chat_handler
            gc.collect()
