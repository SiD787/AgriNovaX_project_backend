"""
AgriNovaX API - FastAPI backend for crop recommendation system.
Entry point: python backend/main.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
import sys

# Add the backend directory to the Python path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prediction_engine import PredictionEngine
from logic_layer import (
    classify_soil_health,
    match_parameters,
    build_suitability_table,
    calculate_confidence,
    assess_risk,
    generate_crop_reasons,
)
from economics import calculate_economics
from soil_engine import analyze_soil
from voice_generator import generate_voice_script, get_supported_languages
from weather_service import get_weather_data, geocode_location
from crop_data import CROP_DISPLAY_NAMES, MULTI_CROPPING
from chat_engine import chat as chat_with_ai

# Initialize FastAPI
_app = FastAPI(
    title="AgriNovaX API",
    description="AI-powered agricultural advisory system for Indian farmers",
    version="1.0.0",
)

# CORS middleware
_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model (lazy-loaded for serverless cold starts)
prediction_engine = None

def get_prediction_engine():
    global prediction_engine
    if prediction_engine is None:
        try:
            prediction_engine = PredictionEngine()
            print("[OK] ML Model loaded successfully")
        except Exception as e:
            print(f"[WARN] Model not loaded: {e}")
            print("   Run 'python backend/train_model.py' first to train the model.")
    return prediction_engine


# Request/Response models
class PredictRequest(BaseModel):
    N: float = Field(..., ge=0, le=200, description="Nitrogen content (kg/ha)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus content (kg/ha)")
    K: float = Field(..., ge=0, le=200, description="Potassium content (kg/ha)")
    temperature: float = Field(..., ge=-10, le=55, description="Temperature in °C")
    humidity: float = Field(..., ge=0, le=100, description="Humidity in %")
    ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    rainfall: float = Field(..., ge=0, le=500, description="Rainfall in mm")
    land_area: Optional[float] = Field(1.0, ge=0.1, le=1000, description="Land area in acres")
    budget: Optional[float] = Field(None, ge=0, description="Budget in INR")
    language: Optional[str] = Field("en", description="Language code (en, hi, mr, ta, te, kn, bn)")
    location: Optional[str] = Field(None, description="Location name for weather data")
    moisture: Optional[float] = Field(None, description="Soil moisture %")
    conductivity: Optional[float] = Field(None, description="Soil conductivity (dS/m)") 


@_app.get("/")
async def root():
    return {
        "message": "AgriNovaX API is running! 🚀",
        "frontend_url": "http://localhost:5173",
        "docs_url": "http://localhost:8000/docs"
    }


@_app.get("/health")
async def health_check():
    engine = get_prediction_engine()
    return {
        "status": "healthy",
        "model_loaded": engine is not None,
        "version": "1.0.0"
    }


@_app.get("/languages")
async def languages():
    return {"languages": get_supported_languages()}


@_app.post("/predict")
async def predict(request: PredictRequest):
    """Main prediction endpoint - returns full crop advisory."""
    
    engine = get_prediction_engine()
    if engine is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Run train_model.py first.")
    
    # 1. ML Prediction
    prediction = engine.predict(
        N=request.N,
        P=request.P,
        K=request.K,
        temperature=request.temperature,
        humidity=request.humidity,
        ph=request.ph,
        rainfall=request.rainfall,
    )
    
    best_crop = prediction["best_crop"]
    model_confidence = prediction["confidence"]
    
    # 2. Soil Health Classification
    soil_health = classify_soil_health(request.N, request.P, request.K)
    
    # 3. Parameter Matching
    parameter_table = match_parameters(
        best_crop, request.N, request.P, request.K,
        request.temperature, request.humidity, request.ph, request.rainfall
    )
    
    # 4. Suitability Table
    suitability = build_suitability_table(best_crop, parameter_table)
    
    # 5. Blended Confidence
    confidence = calculate_confidence(model_confidence, parameter_table)
    
    # 6. Risk Assessment
    risk_level = assess_risk(parameter_table)
    
    # 7. Crop Reasons
    reasons = generate_crop_reasons(best_crop, parameter_table, suitability)
    
    # 8. Economics
    land_area = request.land_area or 1.0
    economics = calculate_economics(best_crop, land_area)
    
    # 9. Soil Improvement
    soil_analysis = analyze_soil(best_crop, request.N, request.P, request.K, request.ph)
    
    # 10. Voice Script
    voice = generate_voice_script(
        language=request.language or "en",
        soil_health=soil_health,
        crop=best_crop,
        confidence=confidence,
        risk_level=risk_level,
        profit_summary=economics["summary"],
        soil_tips=soil_analysis["soil_tips"],
    )
    
    # 11. Weather (optional)
    weather = None
    if request.location:
        geo = await geocode_location(request.location)
        weather = await get_weather_data(geo["latitude"], geo["longitude"])
        if weather:
            weather["location"] = geo
    
    # 12. Multi-cropping suggestions
    companion_crops = MULTI_CROPPING.get(best_crop, [])
    multi_cropping = [
        {"crop": c, "display_name": CROP_DISPLAY_NAMES.get(c, c.title())}
        for c in companion_crops[:4]
    ]
    
    # Build response
    response = {
        "status": "success",
        "soil_health": {
            **soil_health,
            "confidence_score": confidence,
            "risk_level": risk_level,
        },
        "recommendation": {
            "crop": best_crop,
            "display_name": CROP_DISPLAY_NAMES.get(best_crop, best_crop.title()),
            "confidence": confidence,
            "model_confidence": model_confidence,
            "reasons": reasons,
        },
        "alternatives": prediction["alternatives"],
        "parameter_table": parameter_table,
        "suitability": suitability,
        "economics": economics,
        "soil_improvement": soil_analysis,
        "voice": voice,
        "weather": weather,
        "multi_cropping": multi_cropping,
        "input_summary": {
            "N": request.N,
            "P": request.P,
            "K": request.K,
            "temperature": request.temperature,
            "humidity": request.humidity,
            "ph": request.ph,
            "rainfall": request.rainfall,
            "land_area": land_area,
            "location": request.location,
            "language": request.language,
        }
    }
    
    return response


@_app.get("/weather/{location}")
async def weather(location: str):
    """Standalone weather endpoint."""
    geo = await geocode_location(location)
    weather_data = await get_weather_data(geo["latitude"], geo["longitude"])
    weather_data["location"] = geo
    return weather_data


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's question")
    language: str = Field("en", description="Language code (en, hi, mr)")


@_app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Conversational AI assistant for farming Q&A."""
    result = chat_with_ai(
        question=request.message,
        lang=request.language,
    )
    return result


# ── Vercel ASGI Middleware ──────────────────────────────────
# Vercel rewrites /api/health → backend/main.py but the ASGI path
# remains /api/health. This middleware strips the /api prefix so
# FastAPI's routes (registered as /health, /predict, etc.) match.
class _StripApiPrefix:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            path = scope.get("path", "")
            if path.startswith("/api"):
                scope["path"] = path[4:] or "/"
        await self.app(scope, receive, send)

# Export the wrapped app — Vercel picks up the `app` variable
app = _StripApiPrefix(_app)


# ── Local Development ──────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("[AgriNovaX] Starting API on http://localhost:8000")
    uvicorn.run(_app, host="0.0.0.0", port=8000, reload=False)
