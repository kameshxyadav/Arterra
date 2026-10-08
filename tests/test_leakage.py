import json
import pathlib

def test_no_leakage():
    """Ensure no prohibited columns appear in any raw CSV file."""
    audit_path = pathlib.Path(__file__).resolve().parents[2] / "ml" / "artifacts" / "leakage_audit.json"
    with open(audit_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        leakage = entry.get("leakage_columns", [])
        assert not leakage, f"Leakage columns found in {entry.get('file')}: {leakage}"
