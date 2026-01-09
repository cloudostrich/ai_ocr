from llama_cpp import Llama

llm = Llama(
    model_path="zoo/Llama-3.2-3B-Instruct-Q5_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=0,
    verbose=False  # <--- CHANGED THIS TO FALSE
)

# I also cleaned up the prompt tags because the library handles them automatically now
messages = [
    {"role": "user", "content": "Write a funny haiku about Linux."}
]

output = llm.create_chat_completion(
    messages=messages,
    max_tokens=100
)

print("-" * 30)
print(output['choices'][0]['message']['content'])
