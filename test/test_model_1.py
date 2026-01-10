from llama_cpp import Llama

llm = Llama(
    model_path="models/nanonets/Nanonets-OCR2-1.5B-exp.i1-Q4_K_M.gguf",
    n_ctx=2048,        
    n_threads=4,       
    n_gpu_layers=0,    
    verbose=True       
)

output = llm(
    "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWrite a funny haiku about Linux.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    max_tokens=100,
    stop=["<|eot_id|>"],
    echo=False
)

print(output['choices'][0]['text'])
