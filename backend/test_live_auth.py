
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_live_registration():
    print(f"Testing Live Server at {BASE_URL}")
    email = f"live_test_{int(time.time())}@test.com"
    payload = {
        "name": "Live Tester",
        "email": email,
        "password": "password123"
    }
    
    try:
        # 1. Register
        print(f"Registering {email}...")
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
        print(f"Register Status: {resp.status_code}")
        print(f"Register Response: {resp.text}")
        
        if resp.status_code != 201:
            print("FAILED: Registration failed")
            return

        # 2. Login
        print(f"Logging in...")
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        print(f"Login Status: {resp.status_code}")
        print(f"Login Response: {resp.text}")
        
        if resp.status_code == 200:
            print("SUCCESS: Live Login working!")
        else:
            print("FAILED: Live Login failed")
            
    except Exception as e:
        print(f"CRITICAL ERROR: Could not connect to server. Is it running? {e}")

if __name__ == "__main__":
    test_live_registration()
