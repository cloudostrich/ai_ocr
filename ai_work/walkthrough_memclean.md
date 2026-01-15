# Memory Optimization Walkthrough

I have implemented significant memory management improvements to the OCR project to address the high RAM usage reported.

## Key Changes

### 1. Explicit Model Cleanup
Large AI models like Nanonets and EasyOCR are now explicitly deleted and cleaned up after use. 
- Added a `cleanup()` method to the `OCREngine` base class.
- Modified `main.py` to use a `try...finally` block, ensuring `engine.cleanup()` is called even if an error occurs during processing.

### 2. Efficient PDF Processing
Previously, the code would load all pages of a PDF into RAM simultaneously as images before starting OCR. This created RAM spikes proportional to the document length.
- Updated all engines (`tesseract`, `nanonets`, `easy`) to process PDFs **page-by-page**.
- Each page is loaded, OCRed, and then immediately freed from memory before the next page is processed.

## Modified Files

### Engine Layer
- [base.py](file:///home/jc/Videos/ai_ocr/ocr_engines/base.py): Added `cleanup()` method.
- [nanonets.py](file:///home/jc/Videos/ai_ocr/ocr_engines/nanonets.py): Implemented model deletion and page-by-page processing.
- [easy.py](file:///home/jc/Videos/ai_ocr/ocr_engines/easy.py): Implemented model deletion and page-by-page processing.
- [tesseract.py](file:///home/jc/Videos/ai_ocr/ocr_engines/tesseract.py): Implemented page-by-page processing.

### Application Layer
- [main.py](file:///home/jc/Videos/ai_ocr/main.py): Added resource management logic and a `⏱️ Processing time` display.

## Troubleshooting

### Import Error: `pdf_info` not found
Fixed by using `pdfinfo_from_path` instead of `pdf_info` in the current environment.

### High RAM Usage from IDE (Pyrefly Extension)
The **Pyrefly** extension (Python type checker) can consume **3-4 GB of RAM** when Python files are open.

**To disable Pyrefly:**
1. Open Extensions panel (`Ctrl+Shift+X`)
2. Search for **"Pyrefly"**
3. Click **"Disable"**

> [!TIP]
> To run without clearing OCR engine resources (e.g., for speed in batch scripts), use the `--no-cleanup` flag, though this is not recommended for high-memory models like Nanonets.
