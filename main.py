import time
from datetime import datetime
from argparse import ArgumentParser
import pandas as pd
import src.prompts as prm
from pathlib import Path
from PIL import Image
from io import BytesIO
import src.gemini_api as gapi



# Parse command line arguments
def parse_argv():
    parser = ArgumentParser(description='Extract structured data from sample files')
    parser.add_argument('sample_path', type=str, help='Path to the sample file')
    parser.add_argument('filetype', type=str, help='1 of bs, inv, dn')
    args = parser.parse_args()
    stem = Path(args.sample_path).stem
    ext = Path(args.sample_path).suffix
    return args, stem, ext

# check for tif/tiff files
def grab_pdf_bytes(args, ext):
    if ext == '.tif' or ext == '.tiff':
        # convert tif to pdf
        with Image.open(args.sample_path) as img:
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            pdf_bytes = img_byte_arr.getvalue()
            print("tif/tiff converted to PNG successfully...")
    else:
        # Read the bank statement PDF
        with open(args.sample_path, 'rb') as f:
            pdf_bytes = f.read()
    return pdf_bytes

# Grab relevant prompt and mimtype
def grab_prompt_and_mimtype(args):
    if args.filetype == 'bs':
        prompt = prm.prompt_bs
        mimtype = 'application/pdf'
    elif args.filetype == 'inv':
        prompt = prm.prompt_inv
        mimtype = 'application/pdf'
    elif args.filetype == 'dn':
        prompt = prm.prompt_dn
        mimtype = 'image/png'
    else:
        print(f"Invalid file type: {args.filetype}")
        exit(1)
    return prompt, mimtype

def main():
    # Start timing
    start_time = time.time()
    
    # Parse command line arguments
    args, stem, ext = parse_argv()
    
    # Grab PDF bytes
    pdf_bytes = grab_pdf_bytes(args, ext)
    
    # Grab prompt and mimtype
    prompt, mimtype = grab_prompt_and_mimtype(args)
    
    # Call Gemini API
    data = gapi.main_gemini(pdf_bytes, prompt, mimtype, api_key="AIzaSyB9pzcIfD6BoBlhBLR-ko5qDNYW_z36CHE")

    # Convert to DataFrame
    df = pd.DataFrame(data["data"])
    # print(df)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        print(df)   
    
    # End timing
    elapsed_time = time.time() - start_time
    print(f"\nTotal time: {elapsed_time:.2f} seconds")
    return df, stem

if __name__ == "__main__":
    df, stem = main()
    # print(data)
    df.to_csv(f'{stem}.csv', index=False)