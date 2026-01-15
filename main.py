"""
Imports are moved to inside the function to avoid errors if dependencies are missing
from ocr_engines.tesseract import TesseractOCR
from ocr_engines.paddle import PaddleOCREngine
from ocr_engines.nanonets import NanonetsOCR
from ocr_engines.easy import EasyOCREngine
from ocr_engines.ocrflux import OCRFluxEngine

Sample files:
BalanceSheetJuly2024rev.pdf  document.jpg  july2024.pdf  ProfitandLosJuly2024rev.pdf
"""
import argparse
import sys
import os
import time
import json
from datetime import datetime

def save_results(filepath, engine_name, text, elapsed_time):
    """Save OCR results to a JSON file in ./outputs directory."""
    # Create outputs directory if it doesn't exist
    outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Generate output filename based on input filename and timestamp
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{base_name}_{timestamp}.json"
    output_path = os.path.join(outputs_dir, output_filename)
    
    # Prepare result data
    result = {
        "source_file": os.path.abspath(filepath),
        "engine": engine_name,
        "timestamp": datetime.now().isoformat(),
        "processing_time_seconds": round(elapsed_time, 2),
        "text": text
    }
    
    # Write JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    return output_path

def get_ocr_engine(engine_type):
    if engine_type == "tesseract":
        from ocr_engines.tesseract import TesseractOCR
        return TesseractOCR()
    # elif engine_type == "paddle":
    #     from ocr_engines.paddle import PaddleOCREngine
    #     return PaddleOCREngine()
    elif engine_type == "nanonets":
        from ocr_engines.nanonets import NanonetsOCR
        return NanonetsOCR()
    elif engine_type in ["easy", "easyocr"]:
        from ocr_engines.easy import EasyOCREngine
        return EasyOCREngine()
    elif engine_type == "ocrflux":
        from ocr_engines.ocrflux import OCRFluxEngine
        return OCRFluxEngine()
    else:
        raise ValueError("Unknown engine")

def format_elapsed_time(elapsed_seconds):
    """Format elapsed time in a human-readable way."""
    if elapsed_seconds < 60:
        return f"{elapsed_seconds:.2f} seconds"
    else:
        minutes = int(elapsed_seconds // 60)
        seconds = elapsed_seconds % 60
        return f"{minutes} minute(s) {seconds:.2f} seconds"

def main():
    parser = argparse.ArgumentParser(description="Run OCR on a specific file.")
    parser.add_argument("filename", help="Path to the file to process (image or PDF).")
    parser.add_argument("--engine", choices=['tesseract', 'easy', 'nanonets', 'ocrflux'], default='tesseract', help="OCR engine to use (default: tesseract)")
    parser.add_argument("--no-cleanup", action="store_true", help="Do not cleanup engine resources after run (not recommended)")
    args = parser.parse_args()

    filepath = args.filename
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Processing: {filepath} using {args.engine} engine")
    
    # Start timing
    start_time = time.time()
    
    engine = None
    try:
        # Initialize engine
        if args.engine == 'tesseract':
            engine = get_ocr_engine("tesseract")
        elif args.engine == 'easy':
            engine = get_ocr_engine("easy")
        elif args.engine == 'nanonets':
            engine = get_ocr_engine("nanonets")
        elif args.engine == 'ocrflux':
            engine = get_ocr_engine("ocrflux")
            
        # Run OCR
        text = engine.extract_text(filepath)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        print("\n--- OCR Result ---\n")
        print(text)
        print("\n------------------\n")
        print(f"⏱️  Processing time: {format_elapsed_time(elapsed_time)}")
        
        # Save results to file
        output_path = save_results(filepath, args.engine, text, elapsed_time)
        print(f"📄 Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during OCR: {e}")
        sys.exit(1)
    finally:
        if engine and not args.no_cleanup:
            engine.cleanup()
            # Explicitly delete the engine object to help GC
            del engine
            import gc
            gc.collect()
            print("✨ Resources cleaned up.")

if __name__ == "__main__":
    main()




# --- Your Agent Logic ---



