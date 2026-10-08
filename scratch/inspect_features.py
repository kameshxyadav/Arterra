import os
import json
import pandas as pd
import numpy as np

# Load dataset
data_file = os.path.join("data", "raw", "z_alizadeh_sani_extension.xlsx")
df = pd.read_excel(data_file)

# Basic audit info
shape = list(df.shape)
missing_counts = df.isnull().sum().to_dict()
duplicates = int(df.duplicated().sum())

dtypes = {col: str(df[col].dtype) for col in df.columns}

# Targets and Leakage Columns
target_cols = ["LAD", "LCX", "RCA", "Cath"]
leakage_cols = ["LAD", "LCX", "RCA", "Cath"]
feature_cols = [col for col in df.columns if col not in target_cols]

# Split numeric vs categorical
numeric_cols = []
categorical_cols = []

for col in feature_cols:
    if pd.api.types.is_numeric_dtype(df[col]):
        numeric_cols.append(col)
    else:
        # Check if binary / categorical strings
        categorical_cols.append(col)

print(f"Shape: {shape}")
print(f"Numeric features ({len(numeric_cols)}): {numeric_cols}")
print(f"Categorical features ({len(categorical_cols)}): {categorical_cols}")

# Target class balances
class_balances = {}
for t in target_cols:
    class_balances[t] = df[t].value_counts().to_dict()
print("Class balances:", class_balances)
