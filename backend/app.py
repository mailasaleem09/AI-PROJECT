from flask import Flask, jsonify, request
from flask_cors import CORS
from database import mongo
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/disease_prediction_db"
mongo.init_app(app)

from routes import api
app.register_blueprint(api, url_prefix='/api')

@app.before_request
def log_request_info():
    print(f"\n[REQUEST] {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.get_data(as_text=True)}")


@app.route('/')
def home():
    return jsonify({"message": "Disease Prediction API is running"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" STARTING BACKEND SERVER")
    print("="*50)
    print(" * Backend URL: http://127.0.0.1:5000")
    print(" * Frontend Proxy Target: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
