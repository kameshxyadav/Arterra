import subprocess
import sys
import pathlib
import json


def test_training():
    """Run the training script and verify that model files and metrics are created."""
    root = pathlib.Path(__file__).resolve().parents[2]
    # Execute training script
    result = subprocess.run([sys.executable, '-m', 'ml.training.train'], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, f"Training script failed: {result.stderr}\n{result.stdout}"
    # Verify model files exist
    models_dir = root / 'ml' / 'artifacts' / 'models'
    for tgt in ['cad', 'lad', 'lcx', 'rca']:
        model_path = models_dir / f"{tgt}_model.pkl"
        assert model_path.exists(), f"Model file missing: {model_path}"
    # Verify metrics JSON exists and contains entries for each target
    metrics_path = root / 'ml' / 'artifacts' / 'metrics.json'
    assert metrics_path.exists(), f"Metrics file missing: {metrics_path}"
    with open(metrics_path, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    for tgt in ['CAD', 'LAD', 'LCX', 'RCA']:
        assert tgt in metrics, f"Metrics missing for {tgt}"
        # Basic sanity checks on metric keys
        for key in ['accuracy_mean', 'roc_auc_mean', 'best_params']:
            assert key in metrics[tgt], f"{key} missing in metrics for {tgt}"
