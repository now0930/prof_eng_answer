# P0 Grading Reproducibility Gate

- Version: `p0_grading_reproducibility_smoke_3run_v1`
- Generated: `2026-07-17T15:11:12.903173+00:00`
- Incident session: `data/sessions/20260717_114330_5960502198`
- Cache bypass: `true`
- Score averaging: `false`
- Ensemble scoring: `false`

## Result

**PASS**

| Criterion | Result | Required | Pass |
|---|---:|---:|:---:|
| Completed runs | 3 | 3 | PASS |
| Question type distinct | 1 | 1 | PASS |
| Contract signature distinct | 1 | 1 | PASS |
| Semantic request hash distinct | 1 | 1 | PASS |
| Total score stddev | 0.0 | ≤ 0.5 | PASS |
| Run errors | 0 | 0 | PASS |

## Runs

| Run | Score | A | B | C | D | E | Question type | Status | Topic | Logic | Semantic hash | Originality hash | Errors |
|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|
| 1 | 8.77 | 1.51 | 2.6 | 2.08 | 2.06 | 0.52 | PRINCIPLE_INTERPRETATION | locked | control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe | warn | 19489e610527 | 661b384925bd |  |
| 2 | 8.77 | 1.51 | 2.6 | 2.08 | 2.06 | 0.52 | PRINCIPLE_INTERPRETATION | locked | control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe | warn | 19489e610527 | 661b384925bd |  |
| 3 | 8.77 | 1.51 | 2.6 | 2.08 | 2.06 | 0.52 | PRINCIPLE_INTERPRETATION | locked | control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe | warn | 19489e610527 | 661b384925bd |  |

## Score statistics

- Scores: `[8.77, 8.77, 8.77]`
- Minimum: `8.77`
- Maximum: `8.77`
- Mean: `8.77`
- Population standard deviation: `0.0`

## Notes

- Each run used a new temporary session directory.
- Existing grade/session cache results were not reused.
- Scores were recorded individually. No averaging or ensemble result was used as a final score.
- The production scoring pipeline and post-pipeline cap reconciliation were both executed.
