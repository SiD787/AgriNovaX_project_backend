"""
Prediction Engine - Loads the trained model and generates crop predictions.
"""

import os
import numpy as np
import joblib


class PredictionEngine:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.model = joblib.load(os.path.join(models_dir, 'crop_model.joblib'))
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
        self.label_encoder = joblib.load(os.path.join(models_dir, 'label_encoder.joblib'))
        self.features = joblib.load(os.path.join(models_dir, 'features.joblib'))

    def predict(self, N, P, K, temperature, humidity, ph, rainfall):
        """
        Predict the best crop given soil and weather parameters.
        
        Returns:
            dict with best_crop, confidence, alternatives (top 3), all_probabilities
        """
        # Prepare input
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        input_scaled = self.scaler.transform(input_data)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(input_scaled)[0]
        
        # Sort by probability
        sorted_indices = np.argsort(probabilities)[::-1]
        
        # Best crop
        best_idx = sorted_indices[0]
        best_crop = self.label_encoder.classes_[best_idx]
        best_confidence = float(probabilities[best_idx])
        
        # Top alternatives (exclude best)
        alternatives = []
        for idx in sorted_indices[1:4]:
            crop_name = self.label_encoder.classes_[idx]
            confidence = float(probabilities[idx])
            if confidence > 0.01:  # Only include if > 1% confidence
                alternatives.append({
                    "crop": crop_name,
                    "confidence": round(confidence * 100, 1)
                })
        
        # All probabilities for reference
        all_probs = {}
        for i, crop in enumerate(self.label_encoder.classes_):
            all_probs[crop] = round(float(probabilities[i]) * 100, 2)
        
        return {
            "best_crop": best_crop,
            "confidence": round(best_confidence * 100, 1),
            "alternatives": alternatives,
            "all_probabilities": all_probs
        }
