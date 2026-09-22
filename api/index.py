from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Find the project root
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "expense_classifier.pkl"

# Load the trained ML model
model = joblib.load(MODEL_PATH)


# Create FastAPI application
app = FastAPI(
    title="SmartSpend AI API",
    description="AI-powered personal expense analysis backend",
    version="1.0.0",
)


# Allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------

class Expense(BaseModel):
    merchant: str
    description: str
    amount: float


class PredictionRequest(BaseModel):
    merchant: str
    description: str


# -----------------------------
# API Routes
# -----------------------------

@app.get("/api")
def home():
    return {
        "message": "SmartSpend AI API is running",
        "status": "online",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/api/expense")
def add_expense(expense: Expense):
    return {
        "message": "Expense received",
        "expense": expense.model_dump(),
    }


@app.post("/api/predict")
def predict_category(data: PredictionRequest):
    text = f"{data.merchant} {data.description}"

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = float(max(probabilities))

    return {
        "category": prediction,
        "confidence": round(confidence * 100, 2),
    }
