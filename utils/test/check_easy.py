# import easyocr
# print("Initializing EasyOCR... (Downloading models to ~/.EasyOCR/)")
# # gpu=False is mandatory for your MacBook Setup
# reader = easyocr.Reader(['en'], gpu=False) 
# print("EasyOCR is ready!")
import easyocr
import os

# ... inside your class __init__ ...

def __init__(self):
    print("Loading EasyOCR model...")
    
    # Define your custom path
    # (Using absolute path is safer for EasyOCR)
    model_dir = os.path.abspath("models/easyocr")
    
    self.reader = easyocr.Reader(
        ['en'], 
        gpu=False,
        model_storage_directory=model_dir, # <--- Add this line
        download_enabled=True              # Allows it to download there if missing
    )