import json
from google import genai
from google.genai import types

from google.genai.errors import ServerError, ClientError
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, retry_if_exception

def is_retryable_error(exception):
    if isinstance(exception, (ServerError, httpx.HTTPError)):
        return True
    if isinstance(exception, ClientError) and exception.code == 429:
        return True
    return False

# Call Gemini API
@retry(
    retry=retry_if_exception(is_retryable_error),
    wait=wait_exponential(multiplier=1, min=10, max=120),
    stop=stop_after_attempt(10)
)
def call_gemini_api(pdf_bytes, prompt, mimtype, api_key):
    """
    Call Gemini API to extract data from PDF. Arguments:
    pdf_bytes: bytes - PDF file in bytes
    prompt: str - Prompt to extract data from PDF
    mimtype: str - MIME type of PDF file
    Returns: dict - Extracted data
    Note: add API key as optional argument
    """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type=mimtype,
            ),
            prompt
        ]
    )
    return response

# Parse the response
def parse_response(response):
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
    return data

def main_gemini(pdf_bytes, prompt, mimtype, api_key=None):
    response = call_gemini_api(pdf_bytes, prompt, mimtype, api_key)
    data = parse_response(response)
    return data