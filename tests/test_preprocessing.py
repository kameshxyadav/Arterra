import pathlib
import subprocess
import sys
import json

def test_preprocessing_build():
    """Run the preprocessing build script and verify output parquet exists and contains required features."""
    # Run the build script
    result = subprocess.run([sys.executable, '-m', 'ml.preprocessing.build'], cwd=pathlib.Path(__file__).resolve().parents[2], capture_output=True, text=True)
    assert result.returncode == 0, f"Build script failed: {result.stderr}\n{result.stdout}"
    # Verify parquet file created
    parquet_path = pathlib.Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'processed_data.parquet'
    assert parquet_path.exists(), f"Processed parquet not found at {parquet_path}"
    # Load parquet and check that at least one row exists and required columns are present
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    assert not df.empty, "Processed DataFrame is empty"
    # Load schema to get expected columns
    from ml.preprocessing.schema import Schema
    schema = Schema()
    missing = set(schema.feature_keys()) - set(df.columns)
    assert not missing, f"Missing columns after preprocessing: {missing}"
