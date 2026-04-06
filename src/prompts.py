
# Prompt to extract structured transaction data
"""
Original BS prompt:
1. transaction_date - the date the transaction occurred
2. value_date - the value date of the transaction
3. description - description of the transaction
4. type - either "withdrawal" or "deposit"
5. amount - the transaction amount (as a number, without currency symbols)

"""
# Bank Statement Prompt
prompt_bs = """
Analyze this bank statement PDF and extract all transactions. For this document, ignore all handwritten text.
For each transaction, extract the following details:
1. Payee-Line 1 : 1st line of each item under Description
2. Payee-Line 2 : 2nd line of each item under Description
3. Payee-Line 3 : 3rd line of each item under Description
4. Payee-Line 4 : 4th line of each item under Description
5. Payment Date : Transaction Date, the date the transaction occurred
6. Purchase # : Invoice no of the bill pay to this organization. Deduced from one of the lines under Description.
7. Supplier# : name of who the coy/person pay to.. singtel, SP, supplier name? Deduced from one of the lines under Description.
8. Amount Applied : the transaction amount (as a number, without currency symbols). 
9. Memo : what type of payment is it giro, paynow, TT, bank charges. Deduced from one of the lines under Description.
10. type : either "withdrawal" or "deposit"

Return the data as a JSON array with objects containing these exact keys:
{
  "data": [
    {
      "Payee-Line 1" : "...",
      "Payee-Line 2" : "...",
      "Payee-Line 3" : "...",
      "Payee-Line 4" : "...",
      "Payment Date" : "YYYY-MM-DD",
      "Purchase #" : "...",
      "Supplier#"  : "...",
      "Amount Applied" : 123.45,
      "Memo" : "...",
      "type" : "withdrawal" or "deposit",
    }
  ]
}

Only return valid JSON, no additional text or markdown formatting.
"""

# Invoice Prompt
prompt_inv = """
Analyze this PDF containing invoices and extract data from each invoice.
For each invoice, extract the following details:
1. supplier_name : the name of the supplier (e.g., "Monopole", "Wine Clique", etc.)
2. date : the invoice date (format: DD/MM/YYYY)
3. amount : the total amount (as a number, without currency symbols)
4. payment_terms : the payment terms (e.g., "30 days", "Net 30", etc.)

Return the data as a JSON array with objects containing these exact keys:
{
  "data": [
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

# Delivery Note Prompt
prompt_dn = """
Analyze this PNG delivery note document and extract the following details:
1. person_in_charge : Name of the person in charge
2. company_name : Company name
3. date : Date of the document (format: DD/MM/YYYY)
4. reference_number : Reference number (e.g., Invoice No, P.O. No, D.O. No)
5. total_amount : Total amount (as a number, without currency symbols)

Return the data as a JSON array with objects containing these exact keys:
{
  "data": [
    {
      "person_in_charge": "...",
      "company_name": "...",
      "date": "DD/MM/YYYY",
      "reference_number": "...",
      "total_amount": 123.45
    }
  ]
}

Only return valid JSON, no additional text or markdown formatting.
"total_amount" should be null or 0 if not found.
"""