"""Prediction router for CardioVision FastAPI service.

- Exposes a POST endpoint `/predict` that accepts a JSON payload with the same feature columns as the processed parquet (numeric only, no target columns).
- Returns a JSON mapping each target (CAD, LAD, LCX, RCA) to the model‑predicted probability (float in [0,1]).
- Uses lazy loading: the first request loads the four joblib model files and caches them in module‑level variables.
- All paths are resolved relative to the repository root (`ROOT`).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import pathlib
from joblib import load

router = APIRouter()

# Paths resolved once at import time
ROOT = pathlib.Path(__file__).resolve().parents[3]
MODEL_DIR = ROOT / "ml" / "artifacts" / "models"
TARGETS = ["CAD", "LAD", "LCX", "RCA"]

# Lazy‑loaded models cache
_models = {}

def _load_model(target: str):
    if target in _models:
        return _models[target]
    model_path = MODEL_DIR / f"{target.lower()}_model.pkl"
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found for {target}: {model_path}")
    model = load(model_path)
    _models[target] = model
    return model

class PredictionRequest(BaseModel):
    """Schema for incoming prediction payload.

    The payload must contain **all** numeric feature columns that were used during training
    (i.e., the columns of `data/processed/processed_data.parquet` *excluding* the target columns).
    For simplicity we accept them as a mapping of column name → value.
    """
    features: dict = Field(..., description="Feature name to numeric value mapping")

@router.post("/predict", summary="Get model‑predicted probabilities for CAD/LAD/LCX/RCA")
async def predict(request: PredictionRequest):
    # Validate that we have a DataFrame‑compatible dict
    if not isinstance(request.features, dict) or not request.features:
        raise HTTPException(status_code=400, detail="'features' must be a non‑empty dict")
    # Convert to single‑row DataFrame
    df = pd.DataFrame([request.features])
    # Ensure all columns are numeric (FastAPI may receive strings)
    try:
        df = df.apply(pd.to_numeric)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Feature values must be numeric: {e}")
    # Compute probabilities for each target
    results = {}
    for target in TARGETS:
        try:
            model = _load_model(target)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        # Predict probability of the positive class
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(df)[:, 1][0]
        else:
            # Fallback: use decision function scaled to [0,1]
            if hasattr(model, "decision_function"):
                score = model.decision_function(df)[0]
                prob = (score - score.min()) / (score.max() - score.min())
            else:
                prob = float(model.predict(df)[0])
        results[target] = float(prob)
    return {"probabilities": results}
