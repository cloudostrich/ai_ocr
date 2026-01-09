import llama_cpp

# Get the system info string and decode it from bytes to text
sys_info = llama_cpp.llama_print_system_info()
print(sys_info.decode('utf-8'))
