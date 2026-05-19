import os, sys
sys.path.append('c:/backup smart exam project/smart examination project')
from dotenv import load_dotenv
load_dotenv('c:/backup smart exam project/smart examination project/.env')
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
try:
    print('2.0:', client.models.generate_content(model='gemini-2.0-flash', contents='hi').text)
except Exception as e:
    print('2.0 Error:', e)

try:
    print('1.5:', client.models.generate_content(model='gemini-1.5-flash', contents='hi').text)
except Exception as e:
    print('1.5 Error:', e)
