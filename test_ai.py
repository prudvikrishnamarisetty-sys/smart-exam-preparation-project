import os
import sys
from dotenv import load_dotenv
load_dotenv(".env")

# Configure console output to handle UTF-8 symbols
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

key = os.environ.get("GEMINI_API_KEY")
print("Key length:", len(key) if key else 0)

try:
    from google import genai
    client = genai.Client(api_key=key)
    # Using gemini-2.5-flash as it is supported on this API key's quota
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello!"
    )
    print("Success:", response.text)
except Exception as e:
    print("Error:", str(e))


