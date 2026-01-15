# ocr_engines/ocrflux.py

import gc
import os
import base64
from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path
from .base import OCREngine

# Default model path relative to project root
DEFAULT_MODEL_PATH = "models/ocrflux/ocrflux-3b-q4_k_m.gguf"


class OCRFluxEngine(OCREngine):
    """
    OCRFlux OCR Engine using llama-cpp-python for GGUF model inference.
    OCRFlux is a multimodal vision-language model designed for OCR tasks.
    """

    def __init__(self, model_path: str = None):
        print("Loading OCRFlux model...")
        
        # Determine model path
        if model_path is None:
            # Get the project root directory (parent of ocr_engines)
            project_root = Path(__file__).parent.parent
            model_path = project_root / DEFAULT_MODEL_PATH
        
        self.model_path = str(model_path)
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at: {self.model_path}")
        
        # Import llama-cpp-python
        try:
            from llama_cpp import Llama
            from llama_cpp.llama_chat_format import Llava15ChatHandler
        except ImportError:
            raise ImportError(
                "llama-cpp-python is required for OCRFlux. "
                "Install with: pip install llama-cpp-python"
            )
        
        # Initialize the model with vision capabilities
        # n_ctx is set to handle image tokens + text
        # n_gpu_layers=0 for CPU inference (can be adjusted for GPU)
        print(f"Loading model from: {self.model_path}")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=4096,
            n_gpu_layers=0,  # Set to -1 for full GPU offload if available
            verbose=False
        )
        print("OCRFlux model loaded successfully!")

    def extract_text(self, file_path: str) -> str:
        """Extract text from image or PDF file."""
        if file_path.lower().endswith('.pdf'):
            return self._process_pdf(file_path)
        else:
            return self._process_image(file_path)

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode an image file to base64 string."""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def _process_image(self, image_path: str) -> str:
        """Process a single image and extract text using OCRFlux."""
        try:
            # Read and encode the image
            image_base64 = self._encode_image_to_base64(image_path)
            
            # Create the prompt for OCR
            prompt = """<|im_start|>system
You are an OCR assistant. Extract all text from the provided image accurately, preserving the original layout and structure as much as possible.<|im_end|>
<|im_start|>user
<image>
Please perform OCR on this image and output all the text you can see.<|im_end|>
<|im_start|>assistant
"""
            
            # Generate response
            response = self.llm(
                prompt,
                max_tokens=2048,
                temperature=0.1,
                stop=["<|im_end|>"]
            )
            
            extracted_text = response["choices"][0]["text"].strip()
            return extracted_text
            
        except Exception as e:
            print(f"Error processing image with OCRFlux: {e}")
            return ""

    def _process_pdf(self, pdf_path: str) -> str:
        """Convert PDF to images and OCR each page."""
        print(f"Processing PDF: {pdf_path}")
        
        info = pdfinfo_from_path(pdf_path)
        total_pages = info["Pages"]
        full_text = []
        
        # Create a temp directory for images
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(1, total_pages + 1):
                print(f"  - OCRing page {i}/{total_pages}...")
                
                # Convert one page at a time
                pages = convert_from_path(
                    pdf_path, 
                    dpi=300, 
                    fmt="jpeg", 
                    first_page=i, 
                    last_page=i
                )
                
                if not pages:
                    continue
                
                # Save page image temporarily
                temp_image_path = os.path.join(temp_dir, f"page_{i}.jpg")
                pages[0].save(temp_image_path, "JPEG")
                
                # Process the image
                page_text = self._process_image(temp_image_path)
                full_text.append(page_text)
                
                # Cleanup
                del pages
                gc.collect()
        
        return "\n\n".join(full_text)

    def cleanup(self):
        """Free memory used by the OCRFlux model."""
        if hasattr(self, 'llm'):
            print("Cleaning up OCRFlux resources...")
            del self.llm
            gc.collect()
