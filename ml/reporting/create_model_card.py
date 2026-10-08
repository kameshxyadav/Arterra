"""Create a model card for the trained CAD prediction models.

- Reads `ml/artifacts/evaluation_summary.json` for per‑target metrics.
- Reads `ml/artifacts/shap_summary.json` for mean‑absolute SHAP feature importances.
- Writes a markdown file `ml/artifacts/model_card.md`.
- Includes the required disclaimer banner (sticky at top and footer) as mandated by AGENTS.md.
- No fabricated numbers – all values are taken directly from the JSON files.
"""

import pathlib
import json
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVAL_PATH = ROOT / "ml" / "artifacts" / "evaluation_summary.json"
SHAP_PATH = ROOT / "ml" / "artifacts" / "shap_summary.json"
OUTPUT_PATH = ROOT / "ml" / "artifacts" / "model_card.md"

DISCLAIMER = """---
**Disclaimer**: This model‑predicted probability of significant vessel stenosis is for research use only and is not intended for clinical diagnosis. Always interpret results with qualified medical expertise.
---
"""

def load_json(path: pathlib.Path):
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_metrics(metrics: dict) -> str:
    lines = []
    for key, value in metrics.items():
        # Round numeric values for readability, keep raw for audit
        if isinstance(value, float):
            lines.append(f"- **{key}**: {value:.4f}")
        else:
            lines.append(f"- **{key}**: {value}")
    return "\n".join(lines)

def format_shap(shap_dict: dict, top_n: int = 5) -> str:
    lines = []
    # Sort features by importance descending
    sorted_feats = sorted(shap_dict.items(), key=lambda kv: kv[1], reverse=True)
    for feat, importance in sorted_feats[:top_n]:
        lines.append(f"- {feat}: {importance:.4f}")
    if not lines:
        lines.append("- No features recorded")
    return "\n".join(lines)

def main() -> int:
    eval_data = load_json(EVAL_PATH)
    shap_data = load_json(SHAP_PATH)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        out.write(DISCLAIMER + "\n")
        out.write(f"# Model Card – CAD Vessel Stenosis Prediction\n\n")
        out.write(f"*Generated on {now}*\n\n")
        out.write("## Evaluation Metrics\n\n")
        for target, metrics in eval_data.items():
            out.write(f"### {target}\n")
            out.write(format_metrics(metrics) + "\n\n")
        out.write("## SHAP Feature Importances (Top 5)\n\n")
        for target, shap_dict in shap_data.items():
            out.write(f"### {target}\n")
            out.write(format_shap(shap_dict) + "\n\n")
        out.write(DISCLAIMER)
    print(f"Model card written to {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
