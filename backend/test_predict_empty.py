import requests
import json

url = 'http://127.0.0.1:5000/api/predict'

# Payload with mix of valid numbers and empty strings, simulating a partially filled form
payload = {
    "user_id": "test_user_id", # This should be handled gracefully now too
    "symptoms": {
        "glucose": 100, 
        "cholesterol": "", # Empty string!
        "hemoglobin": 13, 
        "platelets": "", # Empty string!
        "white_blood_cells": 6000, 
        # ... other fields missing entirely
    }
}

try:
    print("Sending prediction request with EMPTY fields...")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
