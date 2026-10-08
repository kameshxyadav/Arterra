"""Evaluation script for Phase 5.

- Loads processed data from `data/processed/processed_data.parquet`.
- Loads each trained model (`ml/artifacts/models/<target>_model.pkl`).
- Computes a full suite of metrics for every target (CAD, LAD, LCX, RCA):
    * accuracy, precision, recall, F1, ROC‑AUC, PR‑AUC, balanced accuracy,
      Matthews correlation coefficient (MCC), Brier score.
- Writes a JSON report `ml/artifacts/evaluation_summary.json` with the per‑target metrics.

The script follows the non‑negotiable rules: fixed seed (42), no target leakage (features
exclude all target columns), and uses only standard scikit‑learn utilities.
"""

import pathlib
import sys
import json
import numpy as np
import pandas as pd
from joblib import load
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    balanced_accuracy_score,
    matthews_corrcoef,
    brier_score_loss,
)

# Fixed seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "processed_data.parquet"
MODEL_DIR = ROOT / "ml" / "artifacts" / "models"
OUTPUT_PATH = ROOT / "ml" / "artifacts" / "evaluation_summary.json"

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

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> dict:
    # Guard against single‑class cases for metrics that require both classes
    pos_label = 1
    # Accuracy always defined
    accuracy = accuracy_score(y_true, y_pred)
    # Precision/Recall/F1 – use zero_division=0 to avoid errors when a class is absent
    precision = precision_score(y_true, y_pred, zero_division=0, pos_label=pos_label)
    recall = recall_score(y_true, y_pred, zero_division=0, pos_label=pos_label)
    f1 = f1_score(y_true, y_pred, zero_division=0, pos_label=pos_label)
    # ROC‑AUC – if only one class present, set to nan
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = float("nan")
    # PR‑AUC (average_precision)
    try:
        pr_auc = average_precision_score(y_true, y_prob)
    except ValueError:
        pr_auc = float("nan")
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    mcc = matthews_corrcoef(y_true, y_pred)
    # Brier score – requires probability of the positive class
    brier = brier_score_loss(y_true, y_prob)
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "balanced_accuracy": bal_acc,
        "mcc": mcc,
        "brier": brier,
    }

def main() -> int:
    df = load_data()
    # Ensure we only use numeric features (no strings) and exclude target columns
    X = df.drop(columns=TARGETS).select_dtypes(include=[np.number])
    summary = {}
    for target in TARGETS:
        y = df[target].values
        model = load_model(target)
        # Predict probabilities for the positive class
        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X)[:, 1]
        else:
            # Fallback to decision function scaled to [0,1]
            if hasattr(model, "decision_function"):
                scores = model.decision_function(X)
                probas = (scores - scores.min()) / (scores.max() - scores.min())
            else:
                probas = model.predict(X)
        preds = (probas >= 0.5).astype(int)
        summary[target] = compute_metrics(y, preds, probas)
    # Write JSON summary
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Evaluation summary written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
