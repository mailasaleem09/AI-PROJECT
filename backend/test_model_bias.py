
import unittest
from ml_model import predictor
import logging

class TestModelBias(unittest.TestCase):
    def test_diabetes_prediction(self):
        # High Glucose, High HbA1c => Should be Diabetes
        # Backend expects keys to match logic: name.lower().replace(" ", "_")
        
        # Mapping check: "Glucose" -> "glucose"
        # "HbA1c" -> "hba1c"
        
        input_data = {
            "glucose": "200", # High
            "hba1c": "9.0",   # High
            "cholesterol": "200",
            # Leave others empty to test mean imputation or provide nominals
        }
        
        print("\n--- Testing Diabetes Inputs ---")
        pred = predictor.predict(input_data)
        print(f"Input: High Glucose/HbA1c -> Prediction: {pred}")
        
    def test_anemia_prediction(self):
        # Low Hemoglobin => Anemia
        input_data = {
            "hemoglobin": "8.0", # Low (Male normal 13-17)
            # others
        }
        print("\n--- Testing Anemia Inputs ---")
        pred = predictor.predict(input_data)
        print(f"Input: Low Hemoglobin -> Prediction: {pred}")

    def test_mapping_debug(self):
        # Specifically test the C-Reactive Protein mapping
        # Frontend sends: c_reactive_protein
        # Backend expects: C-reactive Protein -> c-reactive_protein (wait, my manual trace was hyphen vs underscore)
        
        input_data = {
             "c_reactive_protein": "100" 
        }
        
        # We need to peek into the predictor's feature extraction logic logic 
        # But we can't easily without modifying it.
        # Instead, verify if providing ONLY this key changes the result compared to empty.
        
        res1 = predictor.predict({})
        res2 = predictor.predict(input_data)
        print(f"\n--- Mapping Test ---")
        print(f"Empty Input Results: {res1}")
        print(f"C-Reactive Input Results: {res2}")
        
        if res1 == res2:
            print("WARNING: C-Reactive Protein might not be mapped correctly (or model ignores it)")

if __name__ == '__main__':
    unittest.main()
