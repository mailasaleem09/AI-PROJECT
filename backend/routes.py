from flask import Blueprint, request, jsonify
from database import mongo
from models import User, Prediction
from ml_model import predictor, HAS_IMBLEARN
from bson import ObjectId, json_util
import json

api = Blueprint('api', __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    print(f"DEBUG: Register Request: {data}")
    # Check if user exists
    if mongo.db.users.find_one({"email": data['email']}):
        print("DEBUG: User already exists")
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User.create(data['name'], data['email'], data['password'])
    result = mongo.db.users.insert_one(new_user)
    print(f"DEBUG: User created with ID: {result.inserted_id}")
    return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    print(f"DEBUG: Login Request: {data}")
    user = mongo.db.users.find_one({"email": data['email']})
    if user:
        print(f"DEBUG: User found: {user['email']}")
        if user['password'] == data['password']:
            print("DEBUG: Password match")
            return jsonify({"message": "Login successful", "user": parse_json(user)}), 200
        else:
            print("DEBUG: Password mismatch")
    else:
        print("DEBUG: User not found")
        
    return jsonify({"error": "Invalid credentials"}), 401

@api.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print(f"DEBUG: Predict Request Payload: {data}")
    user_id = data.get('user_id')
    input_data = data.get('symptoms')
    
    if not input_data:
        print("DEBUG: No input data provided in payload")
        return jsonify({"error": "No input data provided"}), 400

    print(f"DEBUG: Calling predictor with: {input_data}")
    result = predictor.predict(input_data)
    print(f"DEBUG: Prediction result: {result}")
    
    # Store prediction
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        user_obj_id = None
        
    pred_doc = Prediction.create(user_obj_id, input_data, result)
    mongo.db.predictions.insert_one(pred_doc)
    
    return jsonify({"prediction": result, "recommendation": "Consult a doctor for further advice."}), 200

@api.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    predictions = mongo.db.predictions.find({"user_id": ObjectId(user_id)})
    return jsonify(parse_json(list(predictions))), 200

@api.route('/doctor/predictions', methods=['GET'])
def get_all_predictions():
    # Fetch all predictions
    predictions = list(mongo.db.predictions.find().sort("timestamp", -1))
    
    # Manually join with user data for display
    enriched_predictions = []
    for p in predictions:
        user_id = p.get('user_id')
        user_name = "Anonymous"
        if user_id:
            user = mongo.db.users.find_one({"_id": user_id})
            if user:
                user_name = user.get('name', 'Unknown')
        
        p['patient_name'] = user_name
        enriched_predictions.append(p)

    return jsonify(parse_json(enriched_predictions)), 200

@api.route('/diseases', methods=['GET'])
def get_diseases():
    # Mock data or fetch from DB
    diseases = [
        {"name": "Common Cold", "symptoms": ["Runny nose", "Sore throat"], "treatments": ["Rest", "Fluids"]},
        {"name": "Influenza", "symptoms": ["Fever", "Chills", "Muscle aches"], "treatments": ["Antivirals", "Rest"]},
        {"name": "COVID-19", "symptoms": ["Fever", "Cough", "Loss of taste"], "treatments": ["Isolation", "Supportive care"]}
    ]
    return jsonify(diseases), 200

@api.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "accuracy": predictor.accuracy,
        "model_type": "Balanced Random Forest" if HAS_IMBLEARN else "Random Forest"
    }), 200
