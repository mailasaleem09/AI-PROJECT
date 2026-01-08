
import pandas as pd
import os

# Load the training dataset
train_path = os.path.join("backend", "Blood_sample_dataset_balanced.csv")
df = pd.read_csv(train_path)

print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())

# Check class distribution
if 'Disease' in df.columns:
    print("\n=== Disease Distribution ===")
    disease_counts = df['Disease'].value_counts()
    print(disease_counts)
    print(f"\nTotal samples: {len(df)}")
    print(f"Number of classes: {len(disease_counts)}")
    
    # Check for class imbalance
    print("\n=== Class Percentages ===")
    percentages = (disease_counts / len(df) * 100).round(2)
    for disease, pct in percentages.items():
        print(f"{disease}: {pct}%")
else:
    print("\nWARNING: 'Disease' column not found!")
    print("Available columns:", df.columns.tolist())
