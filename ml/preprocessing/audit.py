"""Data audit script for Phase 1.

This script scans the `data/raw/` directory for CSV files, loads each with pandas, and
produces a JSON audit summary saved to `ml/artifacts/data_audit.json`.
The JSON contains for each file:
- `row_count`
- `col_count`
- `columns` (list of column names)
- `missing_percent_per_column` (percentage of missing values per column)
- `numeric_summary` (mean, std, min, max for numeric columns)

The script is deliberately lightweight and uses only the standard libraries plus
pandas (already in `requirements.txt`). It exits with code 0 on success and prints a short
message. Errors are printed to stdout and cause a non‑zero exit code.
"""

import json
import pathlib
import sys
from typing import Dict, Any

import pandas as pd

DATA_ROOT = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw"
OUTPUT_PATH = pathlib.Path(__file__).resolve().parents[1] / "artifacts" / "data_audit.json"

def audit_file(csv_path: pathlib.Path) -> Dict[str, Any]:
    df = pd.read_csv(csv_path)
    row_count, col_count = df.shape
    columns = list(df.columns)
    # Missing percentages per column
    missing = (df.isna().sum() / len(df) * 100).round(2).to_dict()
    # Numeric summary for numeric columns only
    numeric = df.select_dtypes(include=["number"]).agg(["mean", "std", "min", "max"]).round(2).to_dict()
    return {
        "file": str(csv_path.relative_to(DATA_ROOT.parent)),
        "row_count": row_count,
        "col_count": col_count,
        "columns": columns,
        "missing_percent_per_column": missing,
        "numeric_summary": numeric,
    }

def main() -> int:
    if not DATA_ROOT.exists():
        print(f"Data root {DATA_ROOT} does not exist", file=sys.stderr)
        return 1
    csv_files = list(DATA_ROOT.rglob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {DATA_ROOT}", file=sys.stderr)
        return 1
    audit_results = [audit_file(p) for p in csv_files]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)
    print(f"Audit completed: {len(audit_results)} file(s) written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
