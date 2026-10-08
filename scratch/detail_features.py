import pandas as pd

df = pd.read_excel('data/raw/z_alizadeh_sani_extension.xlsx')
target_cols = ["LAD", "LCX", "RCA", "Cath"]

for col in df.columns:
    if col in target_cols:
        continue
    vals = df[col].unique()
    val_cnt = len(vals)
    dtype = df[col].dtype
    if pd.api.types.is_numeric_dtype(df[col]):
        print(f"NUMERIC: {col:22s} | min={df[col].min():.2f}, max={df[col].max():.2f}, median={df[col].median():.2f}, unique_cnt={val_cnt}")
    else:
        print(f"CATEGORICAL: {col:22s} | unique_vals={vals[:6]}")
