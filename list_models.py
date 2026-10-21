import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        print("Available Gemini models:")
        for model in result.get('models', []):
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"  - {model['name']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Exception: {str(e)}")
