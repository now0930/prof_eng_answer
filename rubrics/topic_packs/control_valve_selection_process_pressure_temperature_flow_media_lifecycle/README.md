# 공정 압력·온도·유량·유체 및 수명주기를 고려한 제어밸브 선정 절차

## Topic ID

`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `IMPLEMENTATION_EVALUATION`

Supported tertiary: `PROCEDURE`

## 핵심 범위

- Governing document와 requirement traceability
- Minimum·normal·maximum·startup·shutdown·upset operating case
- Pressure·temperature·flow·phase·composition·property envelope
- Control·shutoff·leakage·fail action·response·safety requirement
- stable Topic ID–based specialist result hand-off와 cross-check
- Body·trim·characteristic·material·actuator·accessory package selection
- Datasheet·requisition·vendor bid·deviation·guarantee
- ITP·FAT·SAT·commissioning·installed-performance acceptance
- Reliability·availability·maintainability·spares·obsolescence
- Energy·downtime·lifecycle cost·field feedback·MOC·revalidation

## Logic Check 정책

- Fact Anchor: 52
- Fatal misconception: 26
- Major conditional claim: 14
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- specialist Topic Packs가 actuator, characteristic, dynamic response, body taxonomy,
  authority, liquid·gas sizing, cavitation·flashing, noise, trim,
  accessories, diagnostics, leakage, severe service 및 SIS final element의
  전문 물리와 계산을 소유한다.
- Topic 16은 각 결과의 입력·가정·margin·limitation·evidence를 인수하여
  통합 package 선정, procurement, acceptance와 lifecycle closure를 소유한다.

## Stable Topic ID hand-off

전문 결과 hand-off는 숫자 순번이 아니라 stable `topic_id`를 기준으로 한다.

| 전문 영역 | Stable Topic ID |
|---|---|
| Actuator force, friction, spring sizing and fail-safe mechanics | `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` |
| Inherent and installed flow-characteristic theory | `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` |
| Deadband, stiction and dynamic-response testing | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` |
| Valve-body and actuator taxonomy | `control_valve_types_globe_rotary_body_actuator_selection` |
| Authority, installed gain, rangeability and turndown | `control_valve_authority_rangeability_gain_installed_performance` |
| Liquid Cv, Kv, Reynolds and piping-factor calculation | `control_valve_sizing_cv_kv_reynolds_liquid_selection` |
| Gas sizing, expansion factor and choked pressure ratio | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` |
| Cavitation, flashing and liquid choking physics | `control_valve_cavitation_flashing_choked_flow_damage_prevention` |
| Aerodynamic and hydrodynamic noise prediction | `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` |
| Balanced and unbalanced trim structure and seal mechanics | `balanced_trim_unbalanced_trim_structure_sealing_applications` |
| Positioner, I/P, booster and accessory calibration | `control_valve_positioner_ip_converter_booster_accessories_calibration` |
| Valve signature and predictive-diagnostics detail | `smart_positioner_diagnostics_valve_signature_predictive_maintenance` |
| Seat leakage, shutoff class, packing and fugitive emissions | `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` |
| High-low flow, temperature, cryogenic and particle severe service | `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles` |
| SIF final-element architecture, PFDavg, PST and proof-test verification | `final_control_element_sil_sis_esd_valve_partial_stroke_test` |

새 Topic Pack이 추가되어도 기존 hand-off ID를 재번호화하지 않는다. 통합 시 입력 case, units, assumptions, correction, margin, limitation, reviewer와 evidence를 함께 인수한다.

## Source

- `docs/topic_sheets/control_valve_selection_process_pressure_temperature_flow_media_lifecycle.md`
- Approved Process Design Basis, PFD, P&ID, control narrative and SRS
- Project datasheet, requisition, vendor bid, deviation register and ITP
- FAT, SAT, commissioning, as-built and field-failure records
- Adjacent specialist Topic Packs identified by stable Topic ID
- `gemini_script/20260806_topic16_control_valve_selection_process_lifecycle_requirements.md`

Source JSON authored. Generated-bank build와 focused regression은 별도 단계에서 수행한다.
