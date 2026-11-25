# Fact Anchor Registry and Canonical Approval Application — 2026-11-25

The repository owner explicitly approved the exact 17 proposed Registry statements in `reports/fact_anchor_registry_approval_bundle_17.md` and the eight corresponding canonical source updates. This record documents application of that approval; it does not claim a new independent technical review.

## Registry updates

- Updated exactly 17 existing Registry rows by `legacy_anchor_id` and `fact_id` from the approved bundle.
- Incremented each row revision from 1 to 2.
- Preserved relation tuples/conditions, source references and source hashes, verification references, `review_status`, `verification_status`, `score_effect`, and the registry-wide approval record.
- No entry was added to or removed from the scoring promotion ledger. No scoring exclusion was changed.

| Anchor ID | Registry Fact ID | Revision | Excluded from scoring |
|---|---|---:|---:|
| `digital_twin_definition` | `iso_23247_manufacturing_digital_twin_is_fit_for_purpose_and_synchronized` | 1 → 2 | false |
| `dp_level_hydrostatic_pressure_principle` | `dp_level_hydrostatic_pressure_principle` | 1 → 2 | false |
| `dp_level_wet_leg_zero_elevation` | `dp_level_wet_leg_zero_elevation` | 1 → 2 | true |
| `encoder_frequency_limit_selection` | `encoder_speed_and_decode_rate_must_fit_frequency_limits` | 1 → 2 | false |
| `gear_tooth_speed_equation` | `rotation_speed_tooth_event_frequency_relation` | 1 → 2 | false |
| `half_bridge_sensitivity_compensation` | `half_bridge_sensitivity_compensation` | 1 → 2 | true |
| `hazard_scenario_boundary` | `sil_hazard_scenario_boundary` | 1 → 2 | true |
| `imperfect_test_residual_risk` | `partial_testing_leaves_unrevealed_failure_modes_for_full_proof_test` | 1 → 2 | false |
| `incremental_encoder_principle` | `incremental_encoder_reports_displacement_relative_to_reference` | 1 → 2 | false |
| `manifold_isolation_sequence` | `rosemount_2051_three_valve_zero_check_isolation_side_sequence` | 1 → 2 | true |
| `om_asset_register_system_boundary` | `iso14224_equipment_id_function_location_and_reliability_taxonomy` | 1 → 2 | true |
| `production_schedule_adherence_delivery_kpi` | `production_schedule_kpi_defines_freeze_period_and_completion_basis` | 1 → 2 | true |
| `pst_not_full_proof_test` | `partial_stroke_exercise_is_not_full_proof_test` | 1 → 2 | true |
| `resistive_sensor_ac_measurement` | `some_resistive_humidity_sensors_require_ac_excitation` | 1 → 2 | false |
| `sw09_software_firmware_integrity` | `nist_80082r3_ot_software_firmware_authenticity_checks` | 1 → 2 | true |
| `thermocouple_measures_temperature_difference` | `thermocouple_measures_temperature_difference` | 1 → 2 | false |
| `tolerable_risk_alarp` | `sil_tolerable_risk_alarp` | 1 → 2 | true |

## Canonical source updates

Exactly eight source anchors were updated from the approved proposal sentence. For each, `statement` and exact duplicate canonical fields (`claim`, `description`, or an accepted explanation only when equal to the previous statement) were aligned; non-identical alternatives and rejected explanations were retained.

| Anchor ID | Topic ID | Updated fields |
|---|---|---|
| `dp_level_hydrostatic_pressure_principle` | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` | statement, claim, description |
| `dp_level_wet_leg_zero_elevation` | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` | statement, claim, description |
| `hazard_scenario_boundary` | `sil_target_determination_risk_reduction_and_lifecycle` | statement, claim, description, accepted_explanations[0] |
| `manifold_isolation_sequence` | `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation` | statement |
| `om_asset_register_system_boundary` | `control_system_operations_maintenance_calibration_inspection_spares_kpi` | statement |
| `production_schedule_adherence_delivery_kpi` | `instrumentation_production_management_planning_quality_cost_resources` | statement, claim, description |
| `sw09_software_firmware_integrity` | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | statement, claim |
| `tolerable_risk_alarp` | `sil_target_determination_risk_reduction_and_lifecycle` | statement, claim, accepted_explanations[0] |

## Consistency and validation adjustments

- The managed Rosemount manifold Topic Pack approval hash was refreshed with `rubric_manager.py approve-topic --reviewer now0930 --review-method human --approval-only`, following the owner's explicit approval; no generated promotion was performed by that command.
- The NIST OT software/firmware item had a matching `core_facts` and `logic_check.llm_profile.truth_schema` copy. Both source-side copies were aligned to the approved anchor statement; scoring authority and logic rules were not changed.
- Two regression expectations that asserted superseded wording were updated to assert the approved schedule-KPI and Rosemount-scoped statements.
- The 80-row revision-review export was refreshed from the approved Registry/source values by its official exporter; all rows remain `UNREVIEWED`.
- The canonical promotion ledger builder refreshed only topic-level source hashes for already-listed entries; its 104 Fact-ID membership, all statement hashes, and promotion decisions remained unchanged.
- Protected 143-answer replay: 143/143 output rows byte-identical to baseline SHA-256 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`; observed score/status/routing differences: 0.

## Explicitly unchanged

- `deenergized_energized_test_condition` and `partial_stroke_test_risk_controls` remain unapplied.
- Five reference-only items and two removal candidates remain unchanged.
- 119 HOLD, D4, exclusion overlay, A–E scoring authority and weights remain unchanged.
- Natural-language relation recognition and `grounded_attempt` remain separate work.
- The current 80-item undecided revision-review export was regenerated by its official exporter to reflect the newly approved registry/source text; all 80 remain `UNREVIEWED`, with no new verdict or proposal. Historical 2026-11-02 snapshot was not changed.
- Generated outputs were not edited by hand; they were rebuilt through `rubric_manager.py build-generated-rubrics`.
