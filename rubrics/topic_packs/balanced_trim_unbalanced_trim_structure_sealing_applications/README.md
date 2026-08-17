# Balanced·Unbalanced Trim의 구조, 밀봉 및 적용

## Topic ID

`balanced_trim_unbalanced_trim_structure_sealing_applications`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `PRINCIPLE_INTERPRETATION`

Supported tertiary: `STRUCTURE`

## 핵심 범위

- Trim pressure boundary와 구조
- Unbalanced effective area와 `Fu = ΔP·Au`
- Balanced residual area와 `Fr = ΔP·Ar`
- Force sign convention
- Balance hole·passage와 pressure communication
- Cage-guided balanced plug
- Balance seal·seat seal 구분
- Balance-seal friction과 breakaway
- Balance leakage·seat leakage 구분
- Pressure equalization transient
- Passage plugging과 dynamic imbalance
- Clean·dirty·high-temperature·cryogenic application
- Operating-case force matrix
- Vendor cutaway·force table·seal-limit crosscheck

## Logic Check 정책

- Fact Anchor: 36
- Fatal misconception: 20
- Major conditional claim: 9
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator thrust와 fail-safe spring sizing: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- Deadband·stiction·hysteresis diagnosis: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`
- General body·cage·guide selection: `control_valve_types_globe_rotary_body_actuator_selection`
- Low-noise·multi-stage trim: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`
- Seat leakage class·packing·fugitive emissions: `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`
- Severe-service material·hardfacing: `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`
- Full valve-package workflow: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`
- 본 Topic은 balance hole·pressure communication·balance seal·residual force와 적용조건을 소유한다.
- Balance seal·seat·cage의 물리적 분해점검, 교체와 재조립 절차는 향후 Valve Maintenance 전문 Topic으로 hand-off할 계획이며, 현재는 active routing 대상으로 사용하지 않는다.

## Source

- `docs/topic_sheets/balanced_trim_unbalanced_trim_structure_sealing_applications.md`
- Control Valve Handbook trim, cage-guided plug and pressure-balanced construction sections
- Control Valve Primer balanced and unbalanced trim sections
- `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`, `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`, `control_valve_types_globe_rotary_body_actuator_selection` 및 `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` source packs
- Vendor cutaway, force table, balance-seal temperature·pressure limit와 flow direction을 함께 확인한다.
- `gemini_script/20260804_topic10_balanced_unbalanced_trim_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
