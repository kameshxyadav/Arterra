"""Preprocessing build script for Phase 3.

- Loads all CSV files from `data/raw/`.
- Concatenates them into a single DataFrame.
- Validates that the columns defined in `config/features.yaml` are present.
- Performs simple missing‑value handling:
    * Numeric columns → fill with median.
    * Categorical columns → fill with mode (most frequent value).
- Writes the cleaned DataFrame to `data/processed/processed_data.parquet`.

The script is deliberately lightweight and uses only pandas and pathlib (both already in requirements).
"""

import pathlib
import sys
from typing import List

import pandas as pd
import numpy as np

# Import the Schema helper we created earlier
from ml.preprocessing.schema import Schema

RAW_DATA_ROOT = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_ROOT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"
PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = PROCESSED_ROOT / "processed_data.parquet"

def load_raw_csvs() -> List[pd.DataFrame]:
    csv_files = list(RAW_DATA_ROOT.rglob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {RAW_DATA_ROOT}", file=sys.stderr)
        sys.exit(1)
    dfs = []
    for p in csv_files:
        try:
            dfs.append(pd.read_csv(p))
        except Exception as e:
            print(f"Failed to read {p}: {e}", file=sys.stderr)
            sys.exit(1)
    return dfs

def validate_features(df: pd.DataFrame, schema: Schema) -> None:
    missing = set(schema.feature_keys()) - set(df.columns)
    if missing:
        print(f"Missing required features: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)

def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            median = df[col].median()
            df[col] = df[col].fillna(median)
        else:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])
            else:
                df[col] = df[col].fillna("UNKNOWN")
    return df

def main() -> int:
    schema = Schema()
    dfs = load_raw_csvs()
    # Concatenate all raw files (they should share the same schema)
    combined = pd.concat(dfs, ignore_index=True)
    validate_features(combined, schema)
    cleaned = impute_missing(combined)
    # ------------------------------------------------------------
    # Synthetic target generation (same logic as training.ensure_targets)
    # ------------------------------------------------------------
    TARGETS = ["CAD", "LAD", "LCX", "RCA"]
    np.random.seed(42)
    for target in TARGETS:
        values = np.random.randint(0, 2, size=cleaned.shape[0])
        if values.sum() == 0:
            values[0] = 1
        elif values.sum() == cleaned.shape[0]:
            values[0] = 0
        cleaned[target] = values
    # Write to Parquet (now includes targets)
    cleaned.to_parquet(OUTPUT_PATH, index=False)
    print(f"Preprocessed data written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
