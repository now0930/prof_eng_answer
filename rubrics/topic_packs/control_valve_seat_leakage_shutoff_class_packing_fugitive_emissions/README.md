# 제어밸브 시트 누설, 차단 등급, 패킹 및 비산배출

## Topic ID

`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `DIAGNOSIS_ACTION`

Supported tertiary: `IMPLEMENTATION_EVALUATION`

## 핵심 범위

- Internal through-seat leakage와 external atmospheric leakage
- Shutoff class와 complete test-condition contract
- Shop test와 field operating leakage 경계
- Soft seat·metal seat trade-off
- Single·double seat와 balanced-trim leakage path
- Seat load·contact stress·pressure direction
- Gas·liquid와 volumetric·mass·bubble leakage basis
- Absolute pressure·temperature reference conversion
- Seat damage·contamination·thermal distortion·misalignment
- Stem·shaft packing과 leakage-friction trade-off
- Live-loaded·low-emission packing과 bellows seal
- Fugitive-emission screening·quantification
- Concentration와 mass-emission rate
- As-found·as-left, detection limit와 uncertainty
- Specification→test→installation→maintenance workflow

## Logic Check 정책

- Fact Anchor: 48
- Fatal misconception: 24
- Major conditional claim: 12
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator thrust·seat-load sizing: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- Packing friction·stiction·dynamic response: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`
- Cavitation·flashing damage physics: `control_valve_cavitation_flashing_choked_flow_damage_prevention`
- Balanced trim·balance-seal mechanics: `balanced_trim_unbalanced_trim_structure_sealing_applications`
- Positioner·I/P calibration: `control_valve_positioner_ip_converter_booster_accessories_calibration`
- Valve signature·predictive diagnostics: `smart_positioner_diagnostics_valve_signature_predictive_maintenance`
- Severe-service package design: `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`
- SIS·ESD·PST·proof-test credit: `final_control_element_sil_sis_esd_valve_partial_stroke_test`
- Full valve-package lifecycle: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`
- 본 Topic은 leakage class, test condition, acceptance와 packing·fugitive-emission 성능 판정을 소유한다.
- Lapping, packing 교체, 분해·재조립과 수리 후 복원 절차는 향후 Valve Maintenance 전문 Topic으로 hand-off할 계획이다.
- 개별 산업표준의 판본·시험장치·인증·approval 상세는 향후 Valve Standards·Approvals 전문 Topic으로 hand-off할 계획이다.
- 아직 생성되지 않은 두 전문 Topic은 active routing alias나 cross-topic ID로 사용하지 않는다.

## Source

- `docs/topic_sheets/control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions.md`
- Control Valve Handbook seat leakage, packing and emissions sections
- Control Valve Primer seat sealing and field-maintenance sections
- `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`, `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`, `control_valve_cavitation_flashing_choked_flow_damage_prevention`, `balanced_trim_unbalanced_trim_structure_sealing_applications`, `control_valve_positioner_ip_converter_booster_accessories_calibration` 및 `smart_positioner_diagnostics_valve_signature_predictive_maintenance` source packs
- Leakage class는 class 명칭만이 아니라 fluid, pressure, temperature, direction, seat load, test duration과 측정방법을 함께 확인한다.
- `gemini_script/20260805_topic13_seat_leakage_packing_emissions_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
