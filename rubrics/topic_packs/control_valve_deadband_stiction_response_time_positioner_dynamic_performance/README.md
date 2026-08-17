# 제어밸브의 데드밴드·스틱션·응답시간 및 포지셔너 동특성

## Topic ID

`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`

## Question type

`DIAGNOSIS_ACTION`

보조 문제 형식은 `PRINCIPLE_INTERPRETATION`이다.

## 핵심 범위

- Final Control Element와 공정변동성
- Deadband, Backlash와 Hysteresis
- Static friction, Stiction과 Stick-Slip
- PV cycling과 limit cycle
- Dead time과 Dynamic time
- Small-step, Large-step와 Reversal test
- Step sensitivity
- Positioner feedback와 gain trade-off
- Pneumatic supply, tubing과 relay capacity
- Volume booster와 hunting
- 개선 전후 검증

## 경계

- Actuator thrust, unbalance force와 fail-safe spring sizing: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- Inherent·installed characteristic: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- I/P converter, split range와 detailed bench calibration: `control_valve_positioner_ip_converter_booster_accessories_calibration`
- Valve signature와 predictive maintenance: `smart_positioner_diagnostics_valve_signature_predictive_maintenance`
- Valve authority, rangeability와 quantitative installed gain: `control_valve_authority_rangeability_gain_installed_performance`
- Cv·Kv와 liquid/gas sizing: `control_valve_sizing_cv_kv_reynolds_liquid_selection`, `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`
- Packing·linkage·trim의 물리적 분해점검과 부품 교체는 향후 Valve Maintenance 전문 Topic으로 hand-off할 계획이며, 현재는 active routing 대상으로 사용하지 않는다.

## Logic Check 정책

- Fatal misconception: 14개
- Major conditional claim: 5개
- Deterministic verdict: disabled
- LLM semantic profile: enabled
- Direct score application: disabled
- Direct D/E effect: none

## Source

- `gemini_script/20260803_topic03_deadband_stiction_response_positioner_requirements.md`
- `docs/topic_sheets/control_valve_deadband_stiction_response_time_positioner_dynamic_performance.md`
- Control Valve Handbook의 dynamic performance, deadband, friction과 positioner application 설명
- Control Valve Primer의 valve response, linkage, packing friction과 pneumatic accessory 설명
- 개선안은 small-step·large-step·reversal test와 process trend로 전후 성능을 검증한다.

## 작성 상태

Source JSON authored and source-level validation pending generated-bank build.
