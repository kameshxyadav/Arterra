"""
Correlation and AUC sanity check script for feature matrix vs targets.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from ml.preprocessing.build import load_xy, get_preprocessor

for target in ["CAD", "LAD", "LCX", "RCA"]:
    X, y = load_xy(target)
    prep = get_preprocessor(scaled=True)
    X_trans = prep.fit_transform(X)
    
    aucs = []
    for col_idx in range(X_trans.shape[1]):
        feature_vec = X_trans[:, col_idx]
        if np.std(feature_vec) == 0:
            continue
        try:
            auc = roc_auc_score(y, feature_vec)
            if auc < 0.5:
                auc = 1.0 - auc
            aucs.append((auc, col_idx))
        except Exception:
            pass
            
    aucs.sort(reverse=True)
    top_auc = aucs[0][0] if aucs else 0.0
    print(f"Target {target:5s} | Max single-feature AUC: {top_auc:.4f}")
    if top_auc > 0.95:
        print(f"WARNING: Exceptionally high single-feature AUC for target {target}!")
