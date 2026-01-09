from llama_cpp import Llama
import sys

try:
    print("✅ Success! llama-cpp-python imported successfully.")
    print(f"Python version: {sys.version.split()[0]}")
except ImportError:
    print("❌ Error: Could not import llama_cpp.")
