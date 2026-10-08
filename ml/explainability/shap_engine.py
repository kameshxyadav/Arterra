"""SHAP explainability script for Phase 6.

- Loads processed data (`data/processed/processed_data.parquet`).
- Loads each trained model (`ml/artifacts/models/<target>_model.pkl`).
- Uses `shap.LinearExplainer` (appropriate for LogisticRegression) to compute SHAP values on the full dataset.
- Computes mean absolute SHAP values per feature (feature importance).
- Writes a JSON file `ml/artifacts/shap_summary.json` with per‑target feature importances.

The script respects all non‑negotiable rules:
* Fixed seed (42) everywhere.
* No target leakage – features exclude all target columns.
* Uses only standard scikit‑learn utilities and `shap` (already in requirements).
* SHAP values are stored in raw log‑odds space, not percentages.
"""

import pathlib
import sys
import json
import numpy as np
import pandas as pd
import shap
from joblib import load

# Fixed seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "processed_data.parquet"
MODEL_DIR = ROOT / "ml" / "artifacts" / "models"
OUTPUT_PATH = ROOT / "ml" / "artifacts" / "shap_summary.json"

TARGETS = ["CAD", "LAD", "LCX", "RCA"]

def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        print(f"Processed data not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    return pd.read_parquet(DATA_PATH)

def load_model(target: str):
    model_path = MODEL_DIR / f"{target.lower()}_model.pkl"
    if not model_path.exists():
        print(f"Model file not found for {target}: {model_path}", file=sys.stderr)
        sys.exit(1)
    return load(model_path)

def compute_shap(model, X: pd.DataFrame) -> np.ndarray:
    # LinearExplainer works with linear models (LogisticRegression)
    explainer = shap.LinearExplainer(model, X, feature_perturbation="interventional")
    shap_values = explainer.shap_values(X)
    # shap_values shape: (n_samples, n_features)
    return shap_values

def main() -> int:
    df = load_data()
    # Ensure feature matrix contains only numeric columns and excludes targets
    X = df.drop(columns=TARGETS).select_dtypes(include=[np.number])
    summary = {}
    for target in TARGETS:
        model = load_model(target)
        shap_vals = compute_shap(model, X)
        # Mean absolute SHAP value per feature (importance)
        mean_abs = np.mean(np.abs(shap_vals), axis=0)
        feature_importance = {
            col: float(val) for col, val in zip(X.columns, mean_abs)
        }
        summary[target] = feature_importance
    # Write JSON summary
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"SHAP summary written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
