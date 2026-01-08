import requests
import json

url = 'http://127.0.0.1:5000/api/predict'

# 24 features sample data
payload = {
    "user_id": "test_user_id",
    "symptoms": {
        "glucose": 100, "cholesterol": 200, "hemoglobin": 13, "platelets": 250000, 
        "white_blood_cells": 6000, "red_blood_cells": 4.5, "hematocrit": 40, 
        "mean_corpuscular_volume": 85, "mean_corpuscular_hemoglobin": 28, 
        "mean_corpuscular_hemoglobin_concentration": 33, "insulin": 10, "bmi": 24, 
        "systolic_blood_pressure": 120, "diastolic_blood_pressure": 80, "triglycerides": 150, 
        "hba1c": 5.5, "ldl_cholesterol": 100, "hdl_cholesterol": 50, "alt": 20, "ast": 25, 
        "heart_rate": 70, "creatinine": 0.9, "troponin": 0.01, "c_reactive_protein": 0.5
    }
}

try:
    print("Sending prediction request...")
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
