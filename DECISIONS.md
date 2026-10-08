# Architecture & Design Decisions Log

## Phase 0: Bootstrap & Initial Decisions
- **Target mapping**: CAD overall target, LAD, LCX, RCA binary targets to be determined in Phase 1 audit.
- **Leakage prevention**: Explicit guard against inclusion of LAD, LCX, RCA, Cath or overall target in feature matrices.
- **3D Visualization**: Procedural/lightweight tube geometry for LAD, LCX, RCA node mapping over heart surface mesh.
- **Risk Bands**: Low (<0.35), Moderate (0.35 - 0.65), High (>0.65) defined in `config/anatomy.yaml`.
- **Random Seed**: Fixed to 42 across all random processes.

## Ideas
- (Future ideas to consider without scope creep)
