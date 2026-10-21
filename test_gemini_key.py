import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Testing API key: {api_key[:15]}...")

# Test with REST API
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [{
        "parts": [{
            "text": "Say OK"
        }]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✓ SUCCESS! Gemini API is working!")
        print(f"Response: {result['candidates'][0]['content']['parts'][0]['text']}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {str(e)}")
