# Memory Optimization Plan

The goal is to reduce RAM usage and ensure that resources (heavy models and large images) are freed as soon as they are no longer needed.

## Proposed Changes

### [Engine Layer]
#### [MODIFY] [base.py](file:///home/jc/Videos/ai_ocr/ocr_engines/base.py)
- Add an optional `cleanup()` method to the `OCREngine` base class.

#### [MODIFY] [nanonets.py](file:///home/jc/Videos/ai_ocr/ocr_engines/nanonets.py)
#### [MODIFY] [easy.py](file:///home/jc/Videos/ai_ocr/ocr_engines/easy.py)
#### [MODIFY] [tesseract.py](file:///home/jc/Videos/ai_ocr/ocr_engines/tesseract.py)
- **Implement `cleanup()`**: Explicitly delete heavy objects (like `self.llm` or `self.reader`) and call `gc.collect()`.
- **Optimize PDF processing**: Modify `extract_text` or `_process_pdf` to process pages one by one instead of loading all pages into a list simultaneously. This prevents RAM spikes proportional to PDF length.

### [Application Layer]
#### [MODIFY] [main.py](file:///home/jc/Videos/ai_ocr/main.py)
- Ensure the engine is cleaned up after use using a `try...finally` block.
- Add an optional `--cleanup` flag (enabled by default) to trigger resource release.

## Verification Plan

### Manual Verification
1. **Monitor RAM Usage**:
   - Run `main.py` on a multi-page PDF with `nanonets` or `easyocr`.
   - Observe peak RAM usage.
   - Run again with the optimized code and observe if peak RAM is lower (due to page-by-page processing) and if RAM is freed after completion (if monitored within a script wrap).
   - Note: In a standard CLI run, the OS will always free RAM on exit. To truly verify "freeing RAM", I will add a temporary check inside `main.py` that prints memory usage before and after `cleanup()`.

2. **Functional Test**: Ensure OCR still works correctly for both single images and PDFs.
