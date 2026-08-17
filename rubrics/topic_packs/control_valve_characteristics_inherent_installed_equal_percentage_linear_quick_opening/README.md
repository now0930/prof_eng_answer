# 제어밸브 고유·설치 유량특성과 Linear·Equal Percentage·Quick Opening

## Topic metadata

- Topic ID: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- Question type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Roadmap priority: `★★★★★`
- Grading mode: `LLM_ONLY`
- Deterministic checks: disabled

## Scope

제어밸브의 기준 유량특성과 실제 system에서 나타나는 설치 유량특성을 구분하고,
Linear, Equal Percentage 및 Quick Opening의 곡선과 선정기준을 평가한다.

- normalized valve travel과 relative flow coefficient
- Inherent Flow Characteristic
- Installed Flow Characteristic
- Linear Characteristic
- Equal Percentage Characteristic
- Quick Opening Characteristic
- valve differential pressure와 actual flow
- pressure-drop redistribution
- system resistance
- pump curve와 static head
- conditional application mapping
- manufacturer curve와 commissioning verification

## Boundary

- Actuator force, friction와 fail-safe spring: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- Valve authority, rangeability와 quantitative installed gain: `control_valve_authority_rangeability_gain_installed_performance`
- Cv·Kv와 liquid sizing: `control_valve_sizing_cv_kv_reynolds_liquid_selection`
- Cavitation, flashing와 choked liquid flow: `control_valve_cavitation_flashing_choked_flow_damage_prevention`
- Balanced·unbalanced trim 상세: `balanced_trim_unbalanced_trim_structure_sealing_applications`
- Stiction, deadband와 hysteresis 상세: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`
- 전체 package 선정과 lifecycle hand-off: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

## Source basis and hand-off

- `docs/topic_sheets/control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening.md`
- Control Valve Handbook의 inherent·installed characteristic 및 system pressure-distribution 설명
- Control Valve Primer의 linear·equal-percentage·quick-opening 적용 설명
- Authority·installed gain의 정량 평가는 `control_valve_authority_rangeability_gain_installed_performance` 결과를 인수한다.
- Catalog characteristic 명칭만으로 선정하지 않고 pump curve, static head, system resistance와 commissioning 결과를 교차검증한다.

## Source inventory

- Fact Anchors: 22
- Fatal misconception contracts: 12
- Major conditional-error contracts: 3
- Rich question patterns: 10
- Recommended Outline sections: 7

## Grading policy

Logic Check는 Topic 신뢰도와 B/C 진단에 사용한다.

Fatal 오류가 확인되면 Topic trust를 `limited`로 본다.

Verified correctness 오류의 canonical owner는 C이며 같은 오류를 B와 C에서 중복 감점하지 않는다.

Logic Check 결과는 D/E 점수에 직접 반영하지 않는다.
