import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# Try to import BalancedRandomForest, fallback to standard if not installed
try:
    from imblearn.ensemble import BalancedRandomForestClassifier
    HAS_IMBLEARN = True
except ImportError:
    HAS_IMBLEARN = False

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = [
            "Glucose","Cholesterol","Hemoglobin","Platelets","White Blood Cells",
            "Red Blood Cells","Hematocrit","Mean Corpuscular Volume","Mean Corpuscular Hemoglobin",
            "Mean Corpuscular Hemoglobin Concentration","Insulin","BMI","Systolic Blood Pressure",
            "Diastolic Blood Pressure","Triglycerides","HbA1c","LDL Cholesterol","HDL Cholesterol",
            "ALT","AST","Heart Rate","Creatinine","Troponin","C-reactive Protein"
        ]
        self.feature_means = {} # Store means for imputation
        # Classes will be determined from dataset
        self.classes = []
        self.accuracy = 0.0 # Will be calculated from test set
        
        self.train_model()

    def train_model(self):
        # Check for CSV files
        train_path = os.path.join(os.path.dirname(__file__), "Blood_sample_dataset_balanced.csv")
        test_path = os.path.join(os.path.dirname(__file__), "blood_samples_dataset_test.csv")
        
        if os.path.exists(train_path):
            print("Loading real dataset...")
            self._train_real_model(train_path, test_path)
        else:
            print("Dataset not found. Training dummy model (24 features)...")
            self._train_dummy_model()

    def _train_real_model(self, train_path, test_path):
        try:
            df_train = pd.read_csv(train_path)
            
            # Handle missing values broadly
            for col in df_train.columns:
                if df_train[col].dtype == "object":
                    df_train[col] = df_train[col].fillna(df_train[col].mode()[0])
                else:
                    df_train[col] = df_train[col].fillna(df_train[col].mean())
            
            # Clean column names
            df_train.columns = [c.strip() for c in df_train.columns]
            
            X_train = df_train[self.feature_names]
            y_train = df_train["Disease"]
            
            # Store means for prediction time imputation
            self.feature_means = X_train.mean().to_dict()
            print("Feature means calculated for imputing missing values.")

            # Apply SMOTE to balance classes if imblearn is available
            try:
                from imblearn.over_sampling import SMOTE
                smote = SMOTE(random_state=42)
                X_res, y_res = smote.fit_resample(X_train, y_train)
                X_train, y_train = X_res, y_res
                print("SMOTE applied: training set balanced.")
            except Exception as e:
                print(f"SMOTE not applied: {e}")
            
            # Encode labels
            y_train_encoded = self.label_encoder.fit_transform(y_train)
            self.classes = self.label_encoder.classes_
            
            # Scaler
            X_train_scaled = self.scaler.fit_transform(X_train)
            
            # Model
            if HAS_IMBLEARN:
                self.model = BalancedRandomForestClassifier(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_leaf=8,
                    min_samples_split=12,
                    max_features="sqrt",
                    warm_start=True,
                    random_state=42,
                    n_jobs=-1
                )
            else:
                self.model = RandomForestClassifier(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_leaf=8,
                    min_samples_split=12,
                    max_features="sqrt",
                    class_weight='balanced',
                    random_state=42,
                    n_jobs=-1
                )
                
            self.model.fit(X_train_scaled, y_train_encoded)
            print("Real model trained successfully.")

            # Calculate Accuracy if test file exists
            if os.path.exists(test_path):
                df_test = pd.read_csv(test_path)
                # Clean and fill
                for col in df_test.columns:
                    if df_test[col].dtype == "object":
                        df_test[col] = df_test[col].fillna(df_test[col].mode()[0])
                    else:
                        df_test[col] = df_test[col].fillna(df_test[col].mean())
                df_test.columns = [c.strip() for c in df_test.columns]
                
                X_test = df_test[self.feature_names]
                y_test = df_test["Disease"]
                
                X_test_scaled = self.scaler.transform(X_test)
                y_test_encoded = self.label_encoder.transform(y_test)
                
                predictions = self.model.predict(X_test_scaled)
                self.accuracy = accuracy_score(y_test_encoded, predictions)
                print(f"Model Accuracy: {self.accuracy * 100:.2f}%")
            else:
                self.accuracy = 0.0
            
        except Exception as e:
            print(f"Error training real model: {e}")
            self._train_dummy_model()

    def _train_dummy_model(self):
        # Generate random data for 24 features (Scale 0-1000 to mimic real values)
        dummy_classes = ["Healthy", "Diabetes", "Anemia", "Thalasse", "Thromboc"]
        X_dummy = np.random.rand(100, 24) * 1000
        y_dummy = np.random.randint(0, len(dummy_classes), 100)
        
        self.classes = dummy_classes
        self.label_encoder.fit(self.classes)
        
        self.scaler.fit(X_dummy)
        
        self.feature_means = {f: 500.0 for f in self.feature_names} # Dummy means
        
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.model.fit(X_dummy, y_dummy)

    def predict(self, input_data):
        # Expect input_data to be a list or dict of 24 features
        # If dict, ensure order
        
        if not self.model:
            self.train_model()
            
        features = []
        if isinstance(input_data, dict):
            # Map dict keys to feature list order, filling MEAN if missing
            for name in self.feature_names:
                # Keys might match exactly or need normalization? 
                # Assuming frontend sends matching keys or we normalize.
                
                # Normalize name: Lower case, replace spaces AND HYPHENS with underscores
                normalized_name = name.lower().replace(" ", "_").replace("-", "_")
                # Try original, normalized, and underscore-to-space variants
                alt_name = name.replace("_", " ")
                val = input_data.get(name) or input_data.get(normalized_name) or input_data.get(alt_name)
                
                # Get mean for this feature
                default_val = self.feature_means.get(name, 0.0)
                
                if val is None or val == "":
                     features.append(default_val)
                else:
                    try:
                        features.append(float(val))
                    except (ValueError, TypeError):
                        features.append(default_val)
                        
        elif isinstance(input_data, list):
            if len(input_data) != 24:
                # This fallback is riskier with list, filling 0s might be bad
                # But lists are less likely to be used directly by frontend
                features = input_data[:24] + [0]*(24-len(input_data))
            else:
                features = input_data
        
        # Scale
        features_scaled = self.scaler.transform([features])
        
        # Predict
        pred_idx = self.model.predict(features_scaled)[0]
        pred_class = self.classes[pred_idx]
        
        return pred_class

predictor = DiseasePredictor()
