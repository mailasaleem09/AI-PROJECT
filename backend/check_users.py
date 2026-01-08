from app import app
from database import mongo

with app.app_context():
    user_count = mongo.db.users.count_documents({})
    print(f"Total Users in DB: {user_count}")
    
    if user_count > 0:
        users = list(mongo.db.users.find({}, {"_id": 0, "email": 1, "name": 1}))
        print("Users found:", users)
    else:
        print("No users found. Database is likely empty.")
