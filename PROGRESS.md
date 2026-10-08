# PROGRESS (update after every step; keep under ~150 lines)

STATE
  current_phase: 0
  current_step: P0.6
  last_green_phase: -1
  last_commit: None
  updated: 2026-10-08
  half_done: "Repo structure, AGENTS.md, PROGRESS.md, DECISIONS.md, API_CONTRACT.md created"
  next_command: "python scripts/verify_phase.py 0"

## FACTS DISCOVERED (copy real values here)
  rows: null | n_features_after_exclusion: null | cad_target_col: null | vessel_cols: LAD,LCX,RCA
  class_balance: CAD null | LAD null | LCX null | RCA null
  selected_models: CAD=null | LAD=null | LCX=null | RCA=null | thresholds file: ml/artifacts/thresholds.json

## PHASE LOG
| Phase | Status (todo/doing/green) | Gate result (1 line) | Git tag |
|-------|---------------------------|----------------------|---------|
| 0     | doing                     | pending              | -       |
| 1     | todo                      | -                    | -       |
| 2     | todo                      | -                    | -       |
| 3     | todo                      | -                    | -       |
| 4     | todo                      | -                    | -       |
| 5     | todo                      | -                    | -       |
| 6     | todo                      | -                    | -       |
| 7     | todo                      | -                    | -       |
| 8     | todo                      | -                    | -       |
| 9     | todo                      | -                    | -       |
| 10    | todo                      | -                    | -       |
| 11    | todo                      | -                    | -       |
| 12    | todo                      | -                    | -       |
| 13    | todo                      | -                    | -       |
| 14    | todo                      | -                    | -       |

## BLOCKERS / OPEN PROBLEMS
None

## NEXT 3 ACTIONS
1. Complete P0 steps and verify phase 0 with `python scripts/verify_phase.py 0`.
2. Git commit and tag `phase-0-done`.
3. Stop and report Phase 0 completion.
