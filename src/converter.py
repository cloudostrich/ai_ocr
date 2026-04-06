# import pytesseract
from PIL import Image
# import re
# import os
from os import path
from argparse import ArgumentParser

parser = ArgumentParser(description='Convert TIFF to PNG/PDF')
parser.add_argument('tiff_path', type=str, help='Path to the TIFF file')
parser.add_argument('output_format', type=str, choices=['png', 'pdf'], help='Output format (png or pdf)')
args = parser.parse_args()


def convert_tiff_to_png(tiff_path):
    """
    Converts a TIFF to PNG. 
    Handles multi-page TIFFs by saving only the first page 
    (or generic logic to save all).
    """
    try:
        with Image.open(tiff_path) as img:
            # Convert to RGB (removes alpha channel quirks if any)
            rgb_img = img.convert('RGB')
            
            # Create new filename
            base_name = path.splitext(tiff_path)[0]
            png_path = f"{base_name}.png"
            
            # Save as PNG
            rgb_img.save(png_path, "PNG", quality=95)
            print(f"Converted: {png_path}")
            return png_path
            
    except Exception as e:
        print(f"Error converting {tiff_path}: {e}")
        return None

def tiff_to_pdf(tiff_path, pdf_path):
    """Converts a TIFF image to a PDF file."""
    image = Image.open(tiff_path)
    # Convert to RGB if necessary to ensure PDF compatibility
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(pdf_path, "PDF", resolution=100.0)
    print(f"Successfully converted {tiff_path} to {pdf_path}")

# --- Execution ---
# file_name = "samples/delivery_note_tiff/300bw DO.tif" # Ensure this file is in your folder
try:
    # Step 1: Convert to PDF
    tiff_to_pdf(file_name, "output_document.pdf")
    
    # Step 2: Extract Data
    # extract_invoice_data(file_name)
    
except Exception as e:
    print(f"Error: {e}")

def main():
    if args.output_format == 'png':
        convert_tiff_to_png(args.tiff_path)
    elif args.output_format == 'pdf':
        tiff_to_pdf(args.tiff_path, args.output_format)

if __name__ == '__main__':
    main()
    