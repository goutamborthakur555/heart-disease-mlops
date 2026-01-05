from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

# Load model
model = joblib.load("models/best_model.pkl")

class PatientData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: float
    thal: float

@app.post("/predict")
def predict(data: PatientData):
    # Convert input to DataFrame
    input_data = pd.DataFrame([data.dict()])
    
    # Predict
    prediction = model.predict(input_data)
    confidence = model.predict_proba(input_data).max()
    
    return {
        "heart_disease_prediction": int(prediction[0]),
        "confidence": float(confidence)
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

from prometheus_fastapi_instrumentator import Instrumentator

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# Add basic logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response