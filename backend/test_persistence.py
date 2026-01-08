
import unittest
import os
import shutil
from app import app
from database import mongo
from models import User

class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Clean up any existing DB for test isolation if needed
        # But here we WANT to test persistence, so we might need a multi-step test
        # or we just assume the env is clean.
        # Let's delete the local db folder if it exists to start fresh
        if os.path.exists("./.mongita_db"):
            shutil.rmtree("./.mongita_db")
            
    def test_persistence(self):
        # 1. Create a user
        with app.app_context():
            print("Creating user...")
            mongo.db.users.insert_one({"email": "persist@test.com", "name": "Persist"})
            count1 = mongo.db.users.count_documents({})
            self.assertEqual(count1, 1)
            
        # 2. Simulate "Restart" by re-initializing the client 
        # (MongitaClientDisk reloads from disk on init)
        # However, `mongo.cx` is already initialized in `app`. 
        # We need to forcefully close/re-open or just create a new client pointing to the same path.
        
        print("Simulating restart...")
        from mongita import MongitaClientDisk
        new_client = MongitaClientDisk(host="./.mongita_db")
        new_db = new_client['disease_prediction_db']
        
        count2 = new_db.users.count_documents({})
        print(f"Count after restart: {count2}")
        self.assertEqual(count2, 1)

if __name__ == '__main__':
    unittest.main()
