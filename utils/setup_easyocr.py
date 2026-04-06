import easyocr
import os

# 1. Define your custom model folder relative to this script
# Using abspath ensures it works regardless of how you call the script
project_root = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(project_root, "models", "easyocr")

# 2. Create the directory if it doesn't exist
if not os.path.exists(model_dir):
    os.makedirs(model_dir)
    print(f"Created directory: {model_dir}")

print(f"Downloading EasyOCR models to: {model_dir} ...")

# 3. Initialize the Reader
# 'model_storage_directory' tells it where to look/save.
# 'download_enabled=True' allows it to fetch files if missing.
reader = easyocr.Reader(
    ['en'],                        # Language list (English)
    gpu=False,                     # CPU only (MacBook)
    model_storage_directory=model_dir, 
    download_enabled=True,
    verbose=True                   # Show progress bars
)

print("\n✅ Setup Complete! Models are safely stored in 'models/easyocr/'.")