import os
from dotenv import load_dotenv
load_dotenv(".env")
key = os.environ.get("GEMINI_API_KEY")
print("Key length:", len(key) if key else 0)

try:
    from google import genai
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello!"
    )
    print("Success:", response.text)
except Exception as e:
    print("Error:", str(e))
