import requests
import json

try:
    print("Testing /api/stats endpoint...")
    response = requests.get('http://127.0.0.1:5000/api/stats')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
