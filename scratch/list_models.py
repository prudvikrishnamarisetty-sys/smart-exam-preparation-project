import os, sys
sys.path.append('c:/backup smart exam project/smart examination project')
from dotenv import load_dotenv
load_dotenv('c:/backup smart exam project/smart examination project/.env')
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
with open('scratch/models.txt', 'w') as f:
    for m in client.models.list():
        f.write(m.name + '\n')
