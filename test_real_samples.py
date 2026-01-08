
import sys
import os
import pandas as pd
sys.path.append(os.getcwd())

from backend.ml_model import predictor

# Load actual samples from the dataset
train_path = os.path.join("backend", "Blood_sample_dataset_balanced.csv")
df = pd.read_csv(train_path)

print("Testing with ACTUAL dataset samples...\n")

# Get one sample from each disease class
for disease in df['Disease'].unique():
    sample = df[df['Disease'] == disease].iloc[0]
    
    # Convert to dict format that frontend would send
    input_dict = {}
    for feature in predictor.feature_names:
        # Normalize feature name to match dataset columns
        if feature in sample.index:
            input_dict[feature.lower().replace(" ", "_").replace("-", "_")] = str(sample[feature])
    
    prediction = predictor.predict(input_dict)
    print(f"Actual: {disease:15} -> Predicted: {prediction}")
    
print("\n" + "="*50)
print("If predictions don't match actual, the model has issues.")
