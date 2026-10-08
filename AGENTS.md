# AGENTS.md - Non-Negotiable Rules & Repo Layout

These apply to every phase. The agent must reread AGENTS.md at the start of every session.

## A. Honesty and data integrity
- Never fabricate, estimate or hard-code metrics, probabilities, SHAP values, FPS or latency. If something was not measured, say 'not measured'.
- Never invent clinical reference ranges. Use null when unsure; use widely known approximate ranges only with a source note in features.yaml.
- Never mark a step done if it is a stub, a TODO, or runs only on mock data. Mock data must be labeled MOCK in code and removed before Phase 14.
- Demo patients must be real rows from the public dataset (shown by index, no identifiers) with their real model outputs.

## B. ML correctness
- No target leakage: LAD, LCX, RCA, Cath and the overall CAD target column are never features. A unit test must fail loudly if they appear.
- Fit imputers, scalers, encoders, SMOTE and feature selection only on training folds (use sklearn or imblearn Pipelines).
- Tune hyperparameters only in an inner loop. Report scores only from outer folds or out-of-fold predictions.
- Fixed seed (42) everywhere. A single command (make train) must reproduce all artifacts from raw data.
- Report accuracy, precision, recall, F1, ROC-AUC, plus PR-AUC, balanced accuracy, MCC and Brier score, as mean and std over repeated stratified folds.
- SHAP must be computed on the uncalibrated base model. State the output space (log-odds) on every SHAP chart. Never label SHAP bars as percentages.

## C. Product and safety wording
- Never write 'diagnosis', 'blockage found', 'plaque detected here', or call probability 'confidence'. Use 'model-predicted probability of significant LAD stenosis'.
- Risk bands (for example Low below 0.35, Moderate 0.35 to 0.65, High above 0.65) are display thresholds chosen by the team and must be described that way, not as clinical cutoffs.
- Disclaimer banner is sticky at the top of the main screen, repeated in footer, README, model card and report.
- No LLM may generate explanations. Plain-language text is built from templates over real SHAP values.

## D. Engineering discipline
- Edit files in place. Do not regenerate whole files for small changes. Do not refactor outside the current phase.
- Do not add unplanned features. If you see a good idea, write it in DECISIONS.md under 'Ideas', and continue.
- Do not change the API contract (API_CONTRACT.md) without updating both backend and frontend and logging the change.
- Pin dependencies after a working install (pip freeze, package-lock). Do not upgrade packages mid-project without a reason in DECISIONS.md.
- Never commit secrets, .env files, node_modules or virtual environments.
- Keep terminal output short (use head, tail, -q). Never print whole dataframes. This saves tokens.
- If the same error persists after 3 attempts: stop, write the blocker and what was tried in PROGRESS.md, choose the simpler alternative, and continue.

## Repository Layout
cardiovision/
  AGENTS.md PROGRESS.md DECISIONS.md API_CONTRACT.md ATTRIBUTIONS.md README.md
  Makefile docker-compose.yml Dockerfile requirements.txt
  config/
    features.yaml (groups, labels, types, ranges, normal ranges, defaults - generated from real data)
    models.yaml (model registry + small hyperparameter grids)
    anatomy.yaml (vessel -> mesh node name, camera presets, risk bands, palettes)
  data/raw/ data/processed/
  ml/
    preprocessing/ (audit.py, schema.py, build.py) training/ (cv.py, registry.py, train.py)
    evaluation/ (metrics.py, plots.py) explainability/ (shap_engine.py, text.py)
    inference/ (predict.py) artifacts/ (models/, figures/, *.json, model_card.md)
  backend/app/ (main.py, routers/, schemas/, services/)
  frontend/ (src/components, src/scenes, src/store, src/services, public/models, public/demo_cache.json)
  scripts/ (verify_phase.py, pick_demo_patients.py, export_demo_cache.py)
  tests/ docs/ (report.md, report.pdf, video_script.md, screenshots/, figures/)
