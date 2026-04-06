import os
import base64
import json
from pdf2image import convert_from_path
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

# --- CONFIGURATION ---
MODEL_PATH = "models/qwen2-vl/Qwen2-VL-7B-Instruct-Q4_K_M.gguf"
MMPROJ_PATH = "models/qwen2-vl/mmproj-Qwen2-VL-7B-Instruct-f16.gguf"
PDF_FILE = "samples/bank_stmt.pdf"

def convert_pdf_to_image(pdf_path):
    """
    Converts the first page of a PDF to a temporary JPG image.
    Returns the path to the generated image.
    """
    print(f" Converting Page 1 of {pdf_path} to image...")
    try:
        # Convert only the first page (fmt="jpeg")
        images = convert_from_path(pdf_path, first_page=1, last_page=1, fmt="jpeg")
        
        if not images:
            raise ValueError("No images generated from PDF.")
            
        # Save to a temp file
        temp_img_path = "temp_page1.jpg"
        images[0].save(temp_img_path, "JPEG")
        return temp_img_path
        
    except Exception as e:
        print(f" Error converting PDF: {e}")
        return None

def process_bank_statement():
    # 1. Convert PDF to Image
    image_path = convert_pdf_to_image(PDF_FILE)
    if not image_path:
        return

    # 2. Setup Qwen2-VL Handler
    # Note: We use the generic Llava handler which works for most GGUF vision models
    chat_handler = Llava15ChatHandler(clip_model_path=MMPROJ_PATH)

    # 3. Load Model
    print(" Loading Qwen2-VL model... (This runs on CPU/System RAM)")
    llm = Llama(
        model_path=MODEL_PATH,
        chat_handler=chat_handler,
        n_ctx=4096,          # Large context for dense statements
        n_gpu_layers=0,      # 0 = CPU. (Metal is not available on Linux)
        verbose=False
    )

    # 4. Prepare Image for the Model
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f"data:image/jpeg;base64,{img_base64}"

    # 5. Define the Prompt
    # We explicitly ask for JSON and column logic
    prompt_msg = [
        {"role": "system", "content": "You are a financial data extraction assistant."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": data_uri}},
            {"type": "text", "text": """
            Extract the transaction table from this bank statement into a JSON list.
            
            Rules:
            1. Columns: Date, Description, Type (Withdrawal or Deposit), Amount.
            2. Logic: The 'Withdrawal' column is distinct from 'Deposit'. 
               - If a number is in the left numeric column -> Withdrawal.
               - If a number is in the right numeric column -> Deposit.
            3. Ignore headers and Chinese characters.
            4. Output valid JSON only.
            """}
        ]}
    ]

    # 6. Run Inference
    print(" Reading document...")
    response = llm.create_chat_completion(
        messages=prompt_msg,
        temperature=0.1, # Low temp for factual accuracy
        max_tokens=2048
    )

    # 7. Output
    print("\n" + "="*30)
    result = response["choices"][0]["message"]["content"]
    print(result)
    
    # Clean up temp file
    if os.path.exists(image_path):
        os.remove(image_path)

if __name__ == "__main__":
    if not os.path.exists(PDF_FILE):
        print(f"Error: {PDF_FILE} not found. Please place your PDF in this folder.")
    else:
        process_bank_statement()