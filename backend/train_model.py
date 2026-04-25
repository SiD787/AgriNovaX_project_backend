"""
Model Training Script - Trains a Random Forest classifier on the crop recommendation dataset.
Run: python train_model.py
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def clean_dataset(df):
    """Clean and preprocess the dataset."""
    # Remove any rows where label column has non-crop values (header duplicates, etc.)
    # Drop rows with any NaN after conversion
    numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Convert to numeric, coercing errors
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows with NaN
    df = df.dropna()
    
    # Remove any duplicate header rows that might have leaked in
    df = df[df['label'] != 'label']
    
    # Strip whitespace from label
    df['label'] = df['label'].str.strip().str.lower()
    
    # Remove rows where label is empty
    df = df[df['label'] != '']
    
    return df.reset_index(drop=True)

def train_model():
    """Train the crop recommendation model."""
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Load dataset
    data_path = os.path.join('data', 'dataset.csv')
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Raw dataset shape: {df.shape}")
    
    # Clean data
    df = clean_dataset(df)
    print(f"Cleaned dataset shape: {df.shape}")
    print(f"Crops found: {df['label'].nunique()} - {sorted(df['label'].unique())}")
    
    # Features and target
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[features].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['label'])
    
    print(f"\nFeatures: {features}")
    print(f"Samples: {len(X)}")
    print(f"Classes: {len(label_encoder.classes_)}")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Train Random Forest
    print("\nTraining Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*60}")
    print(f"MODEL ACCURACY: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"{'='*60}")
    
    print("\nClassification Report:")
    target_names = label_encoder.classes_
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    # Feature importance
    print("\nFeature Importance:")
    for feat, imp in sorted(zip(features, model.feature_importances_), key=lambda x: -x[1]):
        print(f"  {feat:15s}: {imp:.4f}")
    
    # Save model, scaler, and label encoder
    joblib.dump(model, os.path.join('models', 'crop_model.joblib'))
    joblib.dump(scaler, os.path.join('models', 'scaler.joblib'))
    joblib.dump(label_encoder, os.path.join('models', 'label_encoder.joblib'))
    joblib.dump(features, os.path.join('models', 'features.joblib'))
    
    print(f"\nModel saved to models/crop_model.joblib")
    print(f"Scaler saved to models/scaler.joblib")
    print(f"Label encoder saved to models/label_encoder.joblib")
    print(f"Features list saved to models/features.joblib")
    
    return model, scaler, label_encoder

if __name__ == "__main__":
    train_model()
