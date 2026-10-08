import sys
import pathlib

R = pathlib.Path(__file__).resolve().parents[1]
REQ = {
    0: ["AGENTS.md", "PROGRESS.md", "DECISIONS.md", "API_CONTRACT.md", "Makefile", "config/anatomy.yaml"],
    1: ["data/raw", "ml/artifacts/data_audit.json", "config/features.yaml"],
    2: ["ml/preprocessing/schema.py", "tests/test_leakage.py"],
    3: ["ml/artifacts/cv_baseline.json"],
    4: ["ml/artifacts/final_cv.json", "ml/artifacts/thresholds.json"],
    5: ["ml/artifacts/metrics.json", "ml/artifacts/model_card.md", "ml/artifacts/leakage_audit.json"],
    6: ["ml/artifacts/shap_global.json", "tests/test_explain.py"],
    7: ["backend/app/main.py", "tests/test_api.py", "ml/artifacts/demo_patients.json"],
    8: ["frontend/package.json", "frontend/src"],
    9: ["frontend/src/scenes", "docs/screenshots"],
    10: ["docs/screenshots/integration_flow.png"],
    11: ["frontend/public/demo_cache.json"],
    12: ["README.md", "Dockerfile", "docker-compose.yml", "ATTRIBUTIONS.md"],
    13: ["docs/report.pdf", "docs/video_script.md"],
    14: ["docs/SUBMISSION_CHECKLIST.md"],
}

arg = sys.argv[1] if len(sys.argv) > 1 else "--all"
all_pass = True
for p in (sorted(REQ) if arg == "--all" else [int(arg)]):
    miss = [f for f in REQ[p] if not (R / f).exists()]
    if miss:
        all_pass = False
    print(f"phase {p}: {'PASS' if not miss else 'FAIL missing ' + str(miss)}")

if not all_pass:
    sys.exit(1)
