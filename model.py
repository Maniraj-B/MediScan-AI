import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

class DiseaseModel:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.model = None
        self.features = None
        self.label_encoder = LabelEncoder()
        self.load_and_train()

    def create_synthetic_dataset(self):
        """Generate comprehensive synthetic dataset for demo"""
        # 8 symptoms, 6 diseases
        symptoms = ['fever', 'cough', 'fatigue', 'headache', 'nausea', 
                   'sore_throat', 'runny_nose', 'body_ache']
        diseases = ['Influenza', 'Common Cold', 'COVID-19', 'Migraine', 
                   'Gastroenteritis', 'Allergies']
        
        # Disease-symptom mapping (probability patterns)
        patterns = {
            'Influenza': [0.9, 0.8, 0.9, 0.5, 0.3, 0.4, 0.3, 0.8],
            'Common Cold': [0.3, 0.7, 0.4, 0.3, 0.1, 0.8, 0.9, 0.3],
            'COVID-19': [0.8, 0.7, 0.8, 0.4, 0.2, 0.6, 0.3, 0.7],
            'Migraine': [0.1, 0.1, 0.6, 0.9, 0.5, 0.1, 0.1, 0.4],
            'Gastroenteritis': [0.5, 0.1, 0.7, 0.4, 0.9, 0.1, 0.1, 0.5],
            'Allergies': [0.1, 0.3, 0.4, 0.4, 0.1, 0.7, 0.8, 0.2]
        }
        
        # Generate 1000 samples per disease
        data = []
        for disease, probs in patterns.items():
            for _ in range(1000):
                row = [1 if np.random.random() < prob else 0 for prob in probs]
                row.append(disease)
                data.append(row)
        
        # Add some noise/mixed cases
        for _ in range(500):
            random_disease = np.random.choice(diseases)
            probs = patterns[random_disease]
            row = [1 if np.random.random() < prob + np.random.normal(0, 0.1) else 0 for prob in probs]
            row = [min(1, max(0, x)) for x in row]  # Keep binary
            row.append(random_disease)
            data.append(row)
        
        df = pd.DataFrame(data, columns=symptoms + ['diseases'])
        
        # Save to dataset path
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
        df.to_csv(self.dataset_path, index=False)
        print(f"✅ Synthetic dataset created with {len(df)} samples")
        return df

    def load_and_train(self):
        try:
            # Load or create dataset
            if not os.path.exists(self.dataset_path):
                df = self.create_synthetic_dataset()
            else:
                df = pd.read_csv(self.dataset_path)
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Check target column
            if 'diseases' not in df.columns:
                raise ValueError("Dataset must contain 'diseases' column")
            
            # Separate features and target
            y = df['diseases']
            X = df.drop('diseases', axis=1)
            
            # Store feature names
            self.features = list(X.columns)
            
            # Encode target labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=150,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            self.model.fit(X, y_encoded)
            
            print(f"✅ Model trained successfully on {len(X)} samples")
            print(f"   Features: {self.features}")
            print(f"   Diseases: {list(self.label_encoder.classes_)}")
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            raise

    def predict(self, input_dict):
        try:
            # Create full feature vector
            input_data = [input_dict.get(col, 0) for col in self.features]
            
            # Prediction
            prediction_encoded = self.model.predict([input_data])[0]
            prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
            
            # Probability distribution
            probabilities = self.model.predict_proba([input_data])[0]
            confidence = max(probabilities) * 100
            
            # Get all disease probabilities
            prob_dist = {
                disease: round(prob * 100, 1) 
                for disease, prob in zip(self.label_encoder.classes_, probabilities)
            }
            
            return {
                "prediction": prediction,
                "confidence": round(confidence, 2),
                "prob_dist": prob_dist
            }
            
        except Exception as e:
            return {
                "error": str(e)
            }

    def get_feature_list(self):
        return self.features if self.features else ['fever', 'cough', 'fatigue', 'headache', 'nausea']