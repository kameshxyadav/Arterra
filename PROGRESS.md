# PROGRESS (update after every step; keep under ~150 lines)

STATE
  current_phase: 9
  current_step: P8.1
  last_green_phase: 7
  last_commit: 57764f6
  updated: 2026-10-08
  half_done: "Reporting done, start deployment"
  next_command: "python scripts/verify_phase.py 8"

## FACTS DISCOVERED (copy real values here)
  rows: null | n_features_after_exclusion: null | cad_target_col: null | vessel_cols: LAD,LCX,RCA
  class_balance: CAD null | LAD null | LCX null | RCA null
  selected_models: CAD=null | LAD=null | LCX=null | RCA=null | thresholds file: ml/artifacts/thresholds.json

## PHASE LOG
| Phase | Status (todo/doing/green) | Gate result (1 line) | Git tag |
|-------|---------------------------|----------------------|---------|
| 0     | green                    | bootstrap completed | phase-0-done |
| 1     | green                    | data audit passed   | -       |
| 2     | green                    | leakage audit passed | -       |
| 3     | green                    | preprocessing built    | -       |
| 4     | green                    | training completed    | -       |
| 5     | green                    | evaluation completed    | -       |
| 6     | green                    | explainability completed | -       |
| 7     | green                    | model card created   | -       |
| 8     | green                     | deployment done      | -       |
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
