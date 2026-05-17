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
        
        # Sorted list of all crops
        sorted_crops = []
        for idx in sorted_indices:
            crop_name = self.label_encoder.classes_[idx]
            confidence = float(probabilities[idx])
            sorted_crops.append({
                "crop": crop_name,
                "confidence": round(confidence * 100, 1)
            })
            
        best_crop = sorted_crops[0]["crop"]
        best_confidence = sorted_crops[0]["confidence"]
        
        # All probabilities for reference
        all_probs = {}
        for i, crop in enumerate(self.label_encoder.classes_):
            all_probs[crop] = round(float(probabilities[i]) * 100, 2)
        
        return {
            "best_crop": best_crop,
            "confidence": best_confidence,
            "sorted_crops": sorted_crops,
            "all_probabilities": all_probs
        }
