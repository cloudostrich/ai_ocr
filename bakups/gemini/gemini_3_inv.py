import csv
import json
import time
from datetime import datetime
from google import genai
from google.genai import types

# Start timing
start_time = time.time()

# Read the invoices PDF
with open('samples/invoices.pdf', 'rb') as f:
    pdf_bytes = f.read()

# Prompt to extract structured invoice data
prompt = """
Analyze this PDF containing invoices and extract data from each invoice.
For each invoice, extract the following details:
1. supplier_name - the name of the supplier (e.g., "Monopole", "Wine Clique", etc.)
2. date - the invoice date (format: DD/MM/YYYY)
3. amount - the total amount (as a number, without currency symbols)
4. payment_terms - the payment terms (e.g., "30 days", "Net 30", etc.)

Return the data as a JSON array with objects containing these exact keys:
{
  "invoices": [
    {
      "supplier_name": "...",
      "date": "DD/MM/YYYY",
      "amount": 123.45,
      "payment_terms": "...",
      "invoice_number": "..."
    }
  ]
}

Only return valid JSON, no additional text or markdown formatting.
"""

# Call Gemini API
client = genai.Client()
response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[
        types.Part.from_bytes(
            data=pdf_bytes,
            mime_type='application/pdf',
        ),
        prompt
    ]
)

# Parse the response
if response.text is None:
    print("No response from Gemini")
    exit(1)
response_text = response.text.strip()

# Remove markdown code block if present
if response_text.startswith('```'):
    lines = response_text.split('\n')
    # Remove first line (```json) and last line (```)
    response_text = '\n'.join(lines[1:-1])

# Parse JSON
try:
    data = json.loads(response_text)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}")
    print(f"Raw response:\n{response.text}")
    exit(1)

# Generate output filenames with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
json_filename = f"output_json/invoices_{timestamp}.json"
csv_filename = f"output_csv/invoices_{timestamp}.csv"

# Write JSON output
with open(json_filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Extracted {len(data.get('invoices', []))} invoices")
print(f"JSON saved to: {json_filename}")

# Write CSV output
csv_headers = [
    'Name of supplier',
    'Date',
    'Amount',
    'Payment terms',
    'Invoice number'
]

with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

    for inv in data.get('invoices', []):
        row = [
            inv.get('supplier_name', ''),
            inv.get('date', ''),
            inv.get('amount', ''),
            inv.get('payment_terms', ''),
            inv.get('invoice_number', '')
        ]
        writer.writerow(row)

print(f"CSV saved to: {csv_filename}")

# Print elapsed time
elapsed_time = time.time() - start_time
print(f"\nTotal time: {elapsed_time:.2f} seconds")
