# CardioVision - Cardiovascular Risk Visualization and Prediction

Decision support and educational prototype for predicting overall CAD status and individual coronary artery stenosis (LAD, LCX, RCA), with 3D interactive heart visualization and SHAP explainability.

> **Disclaimer**: Decision support / educational prototype. Not a medical diagnosis and not a substitute for formal diagnostic imaging or clinical judgment.

## Quickstart

```bash
make setup
make train
make api
make web
```

## Structure
- `config/`: System configuration (features, models, anatomy).
- `ml/`: Preprocessing, training, evaluation, SHAP explainability, and inference pipeline.
- `backend/`: FastAPI REST backend.
- `frontend/`: React + Three.js 3D viewer & clinical dashboard.
- `docs/`: Documentation, figures, and video script.
