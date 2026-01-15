import csv
import json
import time
from datetime import datetime
from google import genai
from google.genai import types

# Start timing
start_time = time.time()

# Read the bank statement PDF
with open('samples/bs_aug_2024.pdf', 'rb') as f:
    pdf_bytes = f.read()

# Prompt to extract structured transaction data
prompt = """
Analyze this bank statement PDF and extract all transactions.
For each transaction, extract the following details:
1. transaction_date - the date the transaction occurred
2. value_date - the value date of the transaction
3. description - description of the transaction
4. type - either "withdrawal" or "deposit"
5. amount - the transaction amount (as a number, without currency symbols)

Return the data as a JSON array with objects containing these exact keys:
{
  "transactions": [
    {
      "transaction_date": "YYYY-MM-DD",
      "value_date": "YYYY-MM-DD", 
      "description": "...",
      "type": "withdrawal" or "deposit",
      "amount": 123.45
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
json_filename = f"output_json/bank_stmt_{timestamp}.json"
csv_filename = f"output_csv/bank_stmt_{timestamp}.csv"

# Write JSON output
with open(json_filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Extracted {len(data.get('transactions', []))} transactions")
print(f"JSON saved to: {json_filename}")

# Write CSV output based on template format
# Headers: Transaction Date,Value date,Description,Transaction Type,Amount,dr/cr,Accounting Entries,,cr/dr,user to input
csv_headers = [
    'Transaction Date',
    'Value date',
    'Description',
    'Transaction Type',
    'Amount',
    'dr/cr',
    'Accounting Entries',
    'cr/dr',
    'user to input'
]

with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

    for txn in data.get('transactions', []):
        txn_type = txn.get('type', '')

        # Determine dr/cr and cr/dr based on transaction type
        if txn_type == 'withdrawal':
            transaction_type = 'withdrawals'
            dr_cr = 'cr'
            cr_dr = 'dr'
        else:  # deposit
            transaction_type = 'Deposits'
            dr_cr = 'dr'
            cr_dr = 'cr'

        row = [
            txn.get('transaction_date', ''),  # Transaction Date
            txn.get('value_date', ''),        # Value date
            txn.get('description', ''),       # Description
            transaction_type,                  # Transaction Type
            txn.get('amount', ''),            # Amount
            dr_cr,                            # dr/cr
            'bank',                           # Accounting Entries
            cr_dr,                            # cr/dr
            ''                                # user to input (blank)
        ]
        writer.writerow(row)

print(f"CSV saved to: {csv_filename}")

# Print elapsed time
elapsed_time = time.time() - start_time
print(f"\nTotal time: {elapsed_time:.2f} seconds")
