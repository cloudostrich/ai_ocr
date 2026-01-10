import sys
import os
import time

print("--- DIAGNOSTIC START ---")

# 1. Check Python Environment
print(f"[1] Python Executable: {sys.executable}")
print(f"[1] Working Directory: {os.getcwd()}")

# 2. Check for Poppler (System Tool)
print("[2] Checking for Poppler system tools...")
from shutil import which
if which("pdftoppm") is None:
    print("❌ ERROR: 'pdftoppm' tool not found!")
    print("   SOLUTION: Run 'sudo pacman -S poppler' in your terminal.")
    sys.exit(1)
else:
    print(f"✅ Poppler found at: {which('pdftoppm')}")

# 3. Check PDF2Image Library
print("[3] Testing PDF to Image conversion...")
try:
    from pdf2image import convert_from_path
    # Create a dummy PDF path or check if specific file exists
    target_pdf = "samples/ProfitandLosJuly2024rev.pdf"
    
    if not os.path.exists(target_pdf):
        print(f"❌ ERROR: File not found at {target_pdf}")
        sys.exit(1)
        
    print(f"   Converting {target_pdf} (This may take 10-20 seconds)...")
    start_t = time.time()
    
    # Try converting just the FIRST page to be fast
    pages = convert_from_path(target_pdf, dpi=200, first_page=1, last_page=1)
    
    print(f"✅ Conversion successful! Time: {time.time() - start_t:.2f}s")
    print(f"   Created {len(pages)} image object(s).")

except Exception as e:
    print(f"❌ PDF CONVERSION FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Check EasyOCR
print("[4] Testing EasyOCR initialization...")
try:
    import easyocr
    import numpy as np
    
    # Use your custom path if you set one, otherwise default
    model_dir = "models/easyocr" if os.path.exists("models/easyocr") else None
    print(f"   Loading EasyOCR (Model dir: {model_dir})...")
    
    reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir, verbose=True)
    
    print("   Running OCR on the converted PDF page...")
    # Convert PIL image to numpy for EasyOCR
    image_np = np.array(pages[0])
    
    results = reader.readtext(image_np, detail=0)
    print("✅ OCR Success! First few words found:")
    print("   " + " ".join(results[:10]) + "...")

except Exception as e:
    print(f"❌ OCR FAILED: {e}")
    import traceback
    traceback.print_exc()

print("--- DIAGNOSTIC END ---")