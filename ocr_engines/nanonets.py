# ocr_engines/nanonets.py
import os
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler # Generic handler, usually works for Qwen2-VL if configured

class NanonetsOCR:
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
            verbose=True
        )

    def extract_text(self, image_path: str) -> str:
        if image_path.lower().endswith('.pdf'):
            from pdf2image import convert_from_path
            # Limit to 1st page for now to save time/memory during testing, or iterate all
            # For this engine, it's very slow, so maybe we should iterate but warn?
            # Let's iterate all.
            images = convert_from_path(image_path)
            full_text = ""
            for i, image in enumerate(images):
                # Save temp file for the LLM to read
                temp_path = f"temp_nanonets_page_{i}.png"
                image.save(temp_path)
                
                print(f"Processing Page {i+1}...")
                page_text = self._process_image(temp_path)
                full_text += f"\n--- Page {i+1} ---\n{page_text}"
                
                # Cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)
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
    
"""
# Fallback method inside extract_text
import subprocess
cmd = [
    "./venv/bin/llama-qwen2vl-cli", # Or wherever your compiled binary is
    "-m", model_path,
    "--mmproj", mmproj_path,
    "--image", image_path,
    "-p", "Extract text..."
]
result = subprocess.run(cmd, capture_output=True, text=True)
return result.stdout
"""
