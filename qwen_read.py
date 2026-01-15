import base64
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

def process_bank_statement():
    model_path = "./models/qwen2-vl/Qwen2-VL-7B-Instruct-Q4_K_M.gguf"
    mmproj_path = "./models/qwen2-vl/mmproj-Qwen2-VL-7B-Instruct-f16.gguf"
    
    # Path to your PDF converted to an image (Qwen reads images, not raw PDFs directly)
    # You might need to convert PDF -> JPG first using 'pdftoppm' or similar
    image_path = "bank_statement_page1.jpg" 

    # 1. Setup the Vision Handler
    # Note: We use the generic Llava handler which often works for Qwen in newer versions
    # If this fails, ensure you have the latest llama-cpp-python: pip install -U llama-cpp-python
    chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)

    # 2. Initialize Model (CPU Mode for Linux compatibility)
    print("Loading model... this may take a moment on CPU.")
    llm = Llama(
        model_path=model_path,
        chat_handler=chat_handler,
        n_ctx=4096,           # Large context for dense text
        n_gpu_layers=0,       # Set to 0 for CPU. Increase if you have Vulkan drivers.
        verbose=False
    )

    # 3. Prepare Image
    # Qwen needs the image passed as a data URI string
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    data_uri = f"data:image/jpeg;base64,{img_base64}"

    # 4. The Prompt
    # Qwen2-VL is smart. We ask it to look at the columns specifically.
    prompt_msg = [
        {"role": "system", "content": "You are a specialized financial OCR assistant."},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": data_uri}},
            {"type": "text", "text": """
            Analyze this bank statement. 
            Focus on the table structure. 
            There are distinct columns for 'Withdrawal' and 'Deposit' which might be far apart.
            
            Extract all transactions into a JSON list.
            JSON Format: [{"date": "...", "description": "...", "type": "withdrawal/deposit", "amount": 0.00}]
            """}
        ]}
    ]

    print("Reading document...")
    response = llm.create_chat_completion(messages=prompt_msg, temperature=0.1)
    
    print("\n--- Result ---")
    print(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    # Helper to ensure you have an image to test
    if not os.path.exists("bank_statement_page1.jpg"):
        print("Alert: Please convert your PDF page to 'bank_statement_page1.jpg' first.")
        print("Tip: Use 'pdftoppm -jpeg -f 1 -l 1 bank_stmt.pdf bank_statement_page1'")
    else:
        process_bank_statement()