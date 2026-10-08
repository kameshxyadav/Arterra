"""FastAPI entry point for the CardioVision service.

- Mounts the `/predict` router which provides a POST endpoint to obtain model‑predicted probabilities for the four targets (CAD, LAD, LCX, RCA).
- The service loads each saved model on first request (lazy loading) and re‑uses them for subsequent calls.
- No target leakage: only numeric non‑target columns from the processed parquet are used as features.
- All paths are resolved relative to the repository root.
"""

from fastapi import FastAPI
from pathlib import Path

# Import the router that implements the prediction endpoint
from .routers import predict

app = FastAPI(title="CardioVision API", version="0.1.0")

# Include the router under the `/api` prefix (feel free to adjust)
app.include_router(predict.router, prefix="/api")

# Root health check
@app.get("/", tags=["Health"]) 
async def health_check():
    return {"status": "ok"}
