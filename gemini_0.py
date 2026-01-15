from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY=AIzaSyB9pzcIfD6BoBlhBLR-ko5qDNYW_z36CHE`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)