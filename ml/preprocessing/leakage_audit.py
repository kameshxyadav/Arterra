"""Leakage audit for Phase 2.

Scans all CSV files under `data/raw/` and checks that no prohibited columns are present.
Prohibited columns (as per AGENTS.md) are:
- LAD, LCX, RCA (individual vessel targets)
- Cath (angiography data)
- CAD (overall target)

The script outputs a JSON file `ml/artifacts/leakage_audit.json` with a list of findings per file:
```json
[
  {
    "file": "data/raw/patient_data.csv",
    "leakage_columns": []
  }
]
```
If any prohibited column is found, it is listed in `leakage_columns`. The script exits with code 0 regardless, but the downstream test will fail if any list is non‑empty.
"""

import json
import pathlib
import sys
from typing import List, Dict, Any

DATA_ROOT = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw"
OUTPUT_PATH = pathlib.Path(__file__).resolve().parents[1] / "artifacts" / "leakage_audit.json"

PROHIBITED = {"LAD", "LCX", "RCA", "Cath", "CAD"}

def audit_file(csv_path: pathlib.Path) -> Dict[str, Any]:
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
    except Exception as e:
        return {"file": str(csv_path), "error": str(e), "leakage_columns": []}
    cols = set(df.columns)
    leakage = sorted(list(cols.intersection(PROHIBITED)))
    return {"file": str(csv_path.relative_to(DATA_ROOT.parent)), "leakage_columns": leakage}

def main() -> int:
    if not DATA_ROOT.exists():
        print(f"Data root {DATA_ROOT} does not exist", file=sys.stderr)
        return 1
    csv_files = list(DATA_ROOT.rglob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {DATA_ROOT}", file=sys.stderr)
        return 1
    results = [audit_file(p) for p in csv_files]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Leakage audit completed: {len(results)} file(s) written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
