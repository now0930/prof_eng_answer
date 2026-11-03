# First canonical promotion batch from the 112 KEEP_BOUNDED holds

Date: 2026-11-03. Branch: `codex/essay-boundary-calibration-20261028`.

The user requested that the 112 source-reviewed candidates be prioritized for
promotion. This **first batch promotes 10, not all 112**. The exact-ID and
current-claim hashes are in
[`fact_anchor_keep_bounded_promotions_20261103.json`](fact_anchor_keep_bounded_promotions_20261103.json).
The source review was performed by GPT-6 on 2026-11-01 and is cited per ID in
the JSON ledger. Codex checked current canonical text, Registry ownership,
approved/verified state, source locator and caveat before changing the scoring
hold. The present user instruction authorizes priority promotion; it is not
represented as a new human technical review. No Topic Pack text, Registry
fact, generated bank, scoring formula, fatal rule or point threshold changed.

| Fact ID | Why it is useful for general scoring | Reviewed boundary |
|---|---|---|
| `availability_readiness_and_time_fraction_measures` | Reliability/repair distinction | Select the defined availability measure; do not equate inherent and operational availability. |
| `bode_decibel_and_log_frequency_properties` | Foundational Bode equation | Amplitude ratio uses 20 log10; sum of factors follows log/phase algebra. |
| `closed_seat_leakage_is_distinct_from_minimum_controllable_flow` | Valve shutoff versus control distinction | Do not infer a minimum controllable flow from leakage alone. |
| `contact_temperature_error_controls_depend_on_immersion_gradients_and_use_conditions` | Temperature-installation error and mitigation | Immersion and flow effects are conditional, not a universal depth or speed rule. |
| `control_valve_cv_is_flow_capacity_not_travel_or_line_size` | Prevents Cv/size/travel conflation | Flow-coefficient definition and units are service-specific. |
| `diagnostic_coverage_and_proof_test_coverage_are_distinct_detection_mechanisms` | Functional-safety evidence distinction | Do not equate automatic diagnostic coverage with proof-test coverage. |
| `force_balance_pressure_area_equilibrium` | Pressure-to-force relation | Static calibrated equilibrium and effective sensing area are assumed. |
| `hazop_lopa_sif_allocation_boundary` | Complete SIF boundary | Sensors, logic and final elements plus functional timing/safe state; component names alone earn only partial credit. |
| `hazop_lopa_target_vs_achieved_sil` | Target versus achieved SIL | LOPA target and actual SIF design verification are separate. |
| `proof_testing_targets_dangerous_failures_not_found_by_online_diagnostics` | Proof-test purpose | Latent dangerous failures are the target; proof test does not replace online diagnostics. |

The prior claim-level source reviews are
[`remaining_23`](fact_anchor_independent_review_remaining_23_20261101.md),
[`control_valve_39`](fact_anchor_independent_review_control_valve_39_20261101.md),
[`safety_20`](fact_anchor_independent_review_safety_20_20261101.md), and
[`remaining_27`](fact_anchor_independent_review_remaining_27_20261101.md).
The Registry holds the authority URL and locator for each promoted Fact.

**Why 102 remain held:** KEEP_BOUNDED is not a blanket general-scoring
approval. Some claims are manufacturer examples, architecture-specific or
would require a narrower canonical statement. For example,
`emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff`
describes one publisher's handbook; `force_balance_null_position_error_detection`
speaks too generally about force bars although its cited instrument is a
specific pneumatic architecture. Neither is unblocked here. Review the
remaining 102 one claim and one Topic Pack boundary at a time.

Post-batch arithmetic: 112 prior promotion holds - 10 promoted = 102 pending;
184 prior source/promotion holds - 10 = 174; total general-scoring blocks
540 - 10 = 530; unblocked Topic Pack Anchors 1,552 + 10 = 1,562.
These are pool counts, not the number of requirements used for any answer.

## Verification at this commit candidate

- Focused policy, reconciliation and HAZOP/Telegram regressions: 26 passed.
- Full pytest: 1,454 passed, 1 skipped, 1 existing warning.
- `rubric_manager.py validate-all`: PASS.
- `rubric_manager.py validate-topic-pack-release --all`: PASS; generated
  snapshot restored, no manual generated edit.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: exit 0 / PASS; optional
  10-run reproducibility gate skipped under its opt-in contract.
- Generated freshness: 2 tests passed.

Remote CI and deployment are separate from these local results.
