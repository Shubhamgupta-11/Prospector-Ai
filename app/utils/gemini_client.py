"""Simple Gemini API client using REST API"""
import requests
import os
import logging
import time

logger = logging.getLogger(__name__)


class GeminiClient:
    """Simple client for Google Gemini API using REST"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = "gemini-3.8-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def generate_content(self, prompt: str, max_retries: int = 3) -> str:
        """Generate content using Gemini with retry logic"""
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['candidates'][0]['content']['parts'][0]['text']
                
                elif response.status_code == 503:
                    # Service unavailable - retry with exponential backoff
                    wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                    logger.warning(f"Gemini API 503 error (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                    last_error = f"Service temporarily unavailable (high demand)"
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                
                elif response.status_code == 429:
                    # Rate limit - retry with longer backoff
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    logger.warning(f"Gemini API rate limit (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                    last_error = f"Rate limit exceeded"
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                
                else:
                    # Other error - log and raise
                    error_msg = f"Gemini API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
            except requests.exceptions.Timeout:
                logger.warning(f"Gemini API timeout (attempt {attempt + 1}/{max_retries})")
                last_error = "Request timed out"
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise Exception("Gemini API request timed out after retries")
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Gemini API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                last_error = str(e)
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise Exception(f"Gemini API request failed: {str(e)}")
        
        # All retries exhausted
        raise Exception(f"Gemini API unavailable after {max_retries} attempts: {last_error}")
