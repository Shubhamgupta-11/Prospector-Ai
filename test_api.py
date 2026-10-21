import requests

url = "http://localhost:8000/api/v1/discover"
data = {
    "icp_description": "B2B SaaS companies, 50-200 employees",
    "max_results": 3
}

print("Testing discovery API...")
response = requests.post(url, json=data, timeout=60)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
