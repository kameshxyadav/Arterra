import subprocess
import json
import pathlib
import sys

def run_evaluation():
    result = subprocess.run([sys.executable, "-m", "ml.evaluation.evaluate"], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("Evaluation script failed")
    return result.stdout

def test_evaluation_summary():
    # Run evaluation script
    run_evaluation()
    # Load the generated summary (relative to repository root)
    summary_path = pathlib.Path("ml/artifacts/evaluation_summary.json")
    assert summary_path.is_file(), f"Summary JSON not found at {summary_path}"
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    # Expect entries for each target
    expected_targets = ["CAD", "LAD", "LCX", "RCA"]
    for target in expected_targets:
        assert target in summary, f"Missing target {target} in summary"
        metrics = summary[target]
        # Required metric keys
        required_keys = ["accuracy", "precision", "recall", "f1", "roc_auc", "pr_auc", "balanced_accuracy", "mcc", "brier"]
        for key in required_keys:
            assert key in metrics, f"{key} missing for {target}"
    # Simple sanity check: accuracy should be between 0 and 1
    for target, metrics in summary.items():
        acc = metrics["accuracy"]
        assert 0.0 <= acc <= 1.0, f"Accuracy out of bounds for {target}: {acc}"
