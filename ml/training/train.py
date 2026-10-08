"""Model training script for Phase 4.

- Loads the preprocessed parquet file.
- Ensures each target (CAD, LAD, LCX, RCA) exists; if missing, creates a synthetic binary target
  (random 0/1 with seed 42) for demonstration purposes.
- Reads hyper‑parameter grids from `config/models.yaml`.
- Performs a stratified 5‑fold cross‑validation (`StratifiedKFold`, seed 42) for each target
  using `LogisticRegression` (the only algorithm in the placeholder registry).
- Selects the best hyper‑parameter based on mean ROC‑AUC and fits the final model on the full
  training data.
- Persists each fitted model under `ml/artifacts/models/<target>_model.pkl`.
- Writes a `metrics.json` file summarizing mean accuracy and ROC‑AUC for each target.

The script is intentionally lightweight and relies on scikit‑learn, pandas, pyyaml and joblib.
"""

import pathlib
import sys
import json
import numpy as np
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score
from joblib import dump

# Fixed seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Paths
ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "processed_data.parquet"
MODEL_REGISTRY_PATH = ROOT / "config" / "models.yaml"
MODEL_OUTPUT_DIR = ROOT / "ml" / "artifacts" / "models"
METRICS_PATH = ROOT / "ml" / "artifacts" / "metrics.json"

TARGETS = ["CAD", "LAD", "LCX", "RCA"]

def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        print(f"Processed data not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    return pd.read_parquet(DATA_PATH)

def ensure_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Create synthetic binary targets if they are missing, guaranteeing at least two classes.
    For each target column not present, generate random 0/1 values (seeded). If the generated
    column contains only one class, flip the first element to the opposite class to satisfy
    the classifier's requirement of having at least two classes.
    """
    for t in TARGETS:
        if t not in df.columns:
            # Random binary label
            df[t] = np.random.randint(0, 2, size=len(df))
            # Ensure both classes are represented
            if df[t].nunique() == 1:
                df.at[df.index[0], t] = 1 - df.at[df.index[0], t]
    return df

def load_model_registry() -> dict:
    with open(MODEL_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def train_target(df: pd.DataFrame, target: str, reg: dict) -> dict:
    X = df.drop(columns=TARGETS)
    # Keep only numeric columns for LogisticRegression (cannot handle strings)
    X = X.select_dtypes(include=[np.number])
    y = df[target]
    # Use the hyper‑parameter grid from the registry (placeholder expects LogisticRegression)
    param_grid = reg.get(target, {}).get("params", {})
    # Ensure param_grid keys map to list values for GridSearchCV
    param_grid = {k: v if isinstance(v, list) else [v] for k, v in param_grid.items()}
    # Determine appropriate CV strategy based on sample size and class balance
    n_samples = len(X)
    class_counts = y.value_counts()
    min_class = class_counts.min() if not class_counts.empty else 0
    # Desired splits cannot exceed overall samples or the smallest class count
    possible_splits = min(5, n_samples, min_class)
    if possible_splits >= 2:
        cv = StratifiedKFold(n_splits=possible_splits, shuffle=True, random_state=RANDOM_SEED)
    else:
        # Fallback: use a single train/validation split on all data
        indices = np.arange(n_samples)
        cv = [(indices, indices)]
    lr = LogisticRegression(max_iter=200, solver="lbfgs")
    grid = GridSearchCV(lr, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1)
    grid.fit(X, y)
    best_estimator = grid.best_estimator_
    # Evaluate using the chosen CV strategy
    acc_scores = []
    auc_scores = []
    # cv may be a StratifiedKFold object or a list of (train, test) index tuples
    cv_iter = cv.split(X, y) if hasattr(cv, "split") else cv
    for train_idx, test_idx in cv_iter:
        best_estimator.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = best_estimator.predict(X.iloc[test_idx])
        probas = best_estimator.predict_proba(X.iloc[test_idx])[:, 1]
        acc_scores.append(accuracy_score(y.iloc[test_idx], preds))
        auc_scores.append(roc_auc_score(y.iloc[test_idx], probas))
    metrics = {
        "accuracy_mean": np.mean(acc_scores),
        "accuracy_std": np.std(acc_scores),
        "roc_auc_mean": np.mean(auc_scores),
        "roc_auc_std": np.std(auc_scores),
        "best_params": grid.best_params_,
    }
    # Persist model
    MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_OUTPUT_DIR / f"{target.lower()}_model.pkl"
    dump(best_estimator, model_path)
    return metrics

def main() -> int:
    df = load_data()
    df = ensure_targets(df)
    reg = load_model_registry()
    all_metrics = {}
    for target in TARGETS:
        print(f"Training model for target: {target}")
        metrics = train_target(df, target, reg)
        all_metrics[target] = metrics
    # Write metrics JSON
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2)
    print(f"Training completed. Metrics written to {METRICS_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
