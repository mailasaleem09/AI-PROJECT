from datetime import datetime
from bson import ObjectId

class User:
    @staticmethod
    def create(name, email, password):
        return {
            "name": name,
            "email": email,
            "password": password, # In production, hash this!
            "medical_history": [],
            "created_at": datetime.utcnow()
        }

class Prediction:
    @staticmethod
    def create(user_id, input_data, prediction_result):
        return {
            "user_id": ObjectId(user_id) if user_id else None,
            "input_data": input_data,
            "prediction_result": prediction_result,
            "created_at": datetime.utcnow()
        }

class Disease:
    @staticmethod
    def create(name, symptoms, treatments):
        return {
            "name": name,
            "symptoms": symptoms,
            "treatments": treatments
        }
