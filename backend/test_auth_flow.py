
import unittest
import json
import shutil
import os
from app import app
from database import mongo

class TestAuthFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Clean up database once before all tests
        if os.path.exists("./.mongita_db"):
            shutil.rmtree("./.mongita_db")

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_register(self):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(payload),
                               content_type='application/json')
        print(f"\nRegister Response: {response.data}")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("User created", data["message"])

    def test_02_login_success(self):
        payload = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.app.post('/api/auth/login',
                               data=json.dumps(payload),
                               content_type='application/json')
        print(f"\nLogin Success Response: {response.data}")
        self.assertEqual(response.status_code, 200)

    def test_03_login_fail(self):
        payload = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = self.app.post('/api/auth/login',
                               data=json.dumps(payload),
                               content_type='application/json')
        print(f"\nLogin Fail Response: {response.data}")
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
