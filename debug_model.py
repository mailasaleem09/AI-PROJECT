
import sys
import os
# Add current dir to path to import backend modules
sys.path.append(os.getcwd())

from backend.ml_model import predictor

print("Predictor loaded.")
print(f"Model Accuracy (pre-computed): {predictor.accuracy}")

# TestCase 1: Diabetes (High Glucose)
# Note: Feature names must be exact or normalized match
input_diabetes = {
    "glucose": "250", 
    "hba1c": "9.0",
    # Others will be mean-filled
}
pred_diabetes = predictor.predict(input_diabetes)
print(f"Diabetes Input -> {pred_diabetes}")

# TestCase 2: Anemia (Low Hemoglobin)
input_anemia = {
    "hemoglobin": "5.0",
}
pred_anemia = predictor.predict(input_anemia)
print(f"Anemia Input -> {pred_anemia}")

# TestCase 3: C-Reactive Protein (Mapping check)
# Frontend sends "c_reactive_protein"
# Backend expects "C-reactive Protein" -> normalized "c_reactive_protein"
input_crp = {
    "c_reactive_protein": "20.0" # High CRP indicates inflammation/infection
}
pred_crp = predictor.predict(input_crp)
print(f"CRP Input -> {pred_crp}")
