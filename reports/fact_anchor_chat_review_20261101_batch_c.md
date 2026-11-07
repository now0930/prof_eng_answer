# Fact Anchor 기술사 적합성·통합 후보 — Batch C (2026-11-01)

## 판정 범위

- 브랜치 `codex/essay-boundary-calibration-20261028`. 현행 Registry/Queue 중 Balanced Trim 29건과 PLC Sequence/Interlock 14건, 총 **43건**을 물리 원리·표준 범위와 비교했다. 이 중 이전 Batch A의 2건(`balance_seal_resistance_is_actuator_load`, `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff`)은 재검토이므로 **새로 검토한 고유 Fact ID는 41건**.
- 결과: SUPPLEMENT_CONDITIONAL 5; CORE_PHYSICS 5; MODEL_EXAMPLE 7; CORE_CONDITIONAL 15; CONSOLIDATE_CANDIDATE 6; CORE_SUPPORTED 5.
- `CORE_PHYSICS`: 물리 관계 확인, `CORE_SUPPORTED`: 공통 안전·논리 원리, `CORE_CONDITIONAL`: 적용 조건 필수, `MODEL_EXAMPLE`: 제조사·설계별 사실/구체 명령은 일반 답안의 필수 Fact 아님, `SUPPLEMENT_CONDITIONAL`: 실무 상세로 유용하지만 일반 시험의 필수답안으로 강제 불가, `CONSOLIDATE_CANDIDATE`: 서로 겹치는 내용, **현재 삭제 확정 아님**.
- 동일 의미 중복 Anchor는 **배점 중복을 방지**하기 위해 Topic Pack 질문 요구축·Logic·Gold Answer 및 코드의 참조관계 확인 후 정식 CLI/회귀 검증을 거쳐 통합하는 것이 적합. 제품 고유 근거가 있다고 업계 공통 원리로 승격하지 않는다.

## Fact ID별 판정

| Fact ID | 판정 | 독립성·적용 조건/채점 적합성 |
|---|---|---|
| `balanced_trim_pressure_equalization_has_finite_transient` | `SUPPLEMENT_CONDITIONAL` | 유한 통로저항·유체 컴플라이언스가 있으면 과도 압력평형 지연이 가능하지만 시간상수·크기는 개별 형상에 좌우. 일반 답안 필수로 요구할 필요 낮음 |
| `balanced_trim_breakaway_running_friction_are_distinct` | `CORE_PHYSICS` | 정지마찰과 운동마찰은 개념상 다른 물리량; 보편적인 배율 없음 |
| `balanced_trim_balance_hole_blockage_impairs_pressure_communication` | `MODEL_EXAMPLE` | Fisher HP/HPA의 균압구멍 막힘은 제품 구성 사례. 일반 원리는 압력소통 통로 폐색 가능성 |
| `cage_guided_balanced_trim_functions` | `MODEL_EXAMPLE` | Cage 지지·유량특성 형성·Balance Seal 구성은 해당 타입별 기능; 공통 밸브 필수 부품목록이 아님 |
| `control_valve_effective_unbalance_area_definition` | `CORE_PHYSICS` | 축방향 압력 합력에 대응하는 실효 면적을 정의; Seat nominal area와 항상 일치하지 않음 |
| `balanced_trim_force_reduction_area_ratio` | `CORE_CONDITIONAL` | 같은 ΔP·정적 기준이라면 힘 비=실효 면적 비; 다른 압력조건에서는 성립하지 않음 |
| `control_valve_pressure_force_direction_is_construction_specific` | `CORE_PHYSICS` | 축 방향 부호·압력작용면에 따라 열림/닫힘 힘이 바뀜 |
| `balanced_plug_seal_is_secondary_pressure_boundary` | `MODEL_EXAMPLE` | Cage형 Balanced Trim에 한정되는 내부 밀봉 경계, 제품 구조 예시 |
| `plug_to_cage_and_seat_leakage_paths_are_distinct` | `CORE_CONDITIONAL` | 둘 다 존재하는 설계에서 Seat 누설과 Balance Seal 누설 경로가 별개 |
| `balance_seal_resistance_is_actuator_load` | `CORE_CONDITIONAL` | Balance Seal이 있는 설계에 한해 마찰/저항을 Actuator 요구력에 포함 |
| `balanced_trim_pressure_communication_path` | `CONSOLIDATE_CANDIDATE` | 동일 팩의 balance_passage_equalizes_plug_pressure 및 residual_unbalance_area와 논리 중복; 구조 사례로 통합 검토 |
| `balance_passage_equalizes_plug_pressure` | `CORE_CONDITIONAL` | 해당 균압 통로가 막히지 않고 설계대로 연결된 경우 압력 평형과 정적 불평형력 감소 |
| `balanced_trim_unbalance_force_equation` | `CORE_PHYSICS` | 정압력 차×유효 투영면적 F=ΔP·A; 단위 일치 확인 |
| `balanced_trim_residual_unbalance_area` | `CORE_PHYSICS` | 실제 균압 트림의 잔류 면적과 압력력은 0으로 보장되지 않음 |
| `control_valve_unbalance_area_not_always_seat_area` | `CONSOLIDATE_CANDIDATE` | effective_unbalance_area_definition과 주제·평가기준 중복 가능; nominal seat와 분리한다는 핵심만 유지 |
| `ideal_full_balance_is_not_universal_actual_state` | `CONSOLIDATE_CANDIDATE` | residual_unbalance_area와 실질 내용 중복; 이상 모델·실제 모델 구분은 기존 Core 문장에 포함 가능 |
| `balanced_globe_trim_seat_and_balance_seal_boundaries` | `CORE_CONDITIONAL` | 특정 Cage-guided 타입의 Plug-Seat와 Plug-Cage Seal 서로 다른 경계; 전 밸브의 공통구조로 확대 금지 |
| `control_valve_pressure_force_sign_depends_on_loaded_areas_and_axis` | `CONSOLIDATE_CANDIDATE` | pressure_force_direction_is_construction_specific와 대체로 중복; 축 기준과 유효면적 조건만 Core에 유지 |
| `balanced_trim_seal_leakage_is_separate_internal_path` | `CONSOLIDATE_CANDIDATE` | plug_to_cage_and_seat_leakage_paths_are_distinct와 내용 중복 가능; 고유 leakage class는 참고 |
| `sliding_stem_actuator_force_includes_seat_load_unbalance_and_friction` | `CORE_CONDITIONAL` | 정압력력·Seat Load·Packing Friction·추가 하중은 별도 힘 항목; 선정 모델에 따라 크기 산정 |
| `balanced_trim_extreme_temperature_seal_checks_are_model_specific` | `SUPPLEMENT_CONDITIONAL` | 소재의 압력·온도 범위 확인은 일반 원리. 고온·극저온별 개별 씰 구조는 제조사 확인 |
| `balanced_trim_selection_should_be_reconciled_with_vendor_force_and_seal_data` | `SUPPLEMENT_CONDITIONAL` | 장치 선정 검증의 실무 가이드. 내부 형상·압력구분·허용 차압표는 모델별 정보 |
| `balanced_trim_force_advantage_is_case_specific_in_high_dp_or_large_valves` | `CORE_CONDITIONAL` | 균압 트림이 힘을 감소시킬 수 있으나 Actuator 소형화나 안전성 자동 보장은 없음 |
| `balanced_trim_elastomer_seal_compatibility_and_failure_modes_are_condition_specific` | `SUPPLEMENT_CONDITIONAL` | 엘라스토머 존재 시 팽윤·압출·마찰 등은 적용 가능성이 있지만 모든 실패모드 체크리스트 암기는 부적절 |
| `balanced_trim_particulate_blockage_risk_is_passage_and_model_specific` | `SUPPLEMENT_CONDITIONAL` | 입자·유로 개구의 폐색/마모 위험은 일반 원리; Fisher strainer·dirty-service 절차는 사례 |
| `balanced_trim_defined_case_force_review_is_configuration_specific` | `CORE_CONDITIONAL` | 최소·정상·최대 등을 실제 정의된 운전점에 대해 해석; 동일 세 조건을 모든 설비에 강제하지 않음 |
| `sw02_manual_control_does_not_remove_hazard_preventing_protection` | `CORE_SUPPORTED` | 수동운전이라도 위험방지 Interlock을 자동으로 무효화할 수 없음; 승인된 Override는 별도 절차 |
| `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff` | `CORE_SUPPORTED` | Filter·Debounce는 짧은 펄스 제거와 검출 지연 상충, Hysteresis는 다른 임계값 원리 |
| `sw02_fail_safe_action_is_application_defined_safe_state` | `CORE_SUPPORTED` | 정의한 안전상태는 Hazard별로 다름; Fail-Closed·탈여자는 보편적 정답 아님 |
| `sw02_state_transition_is_deterministic_function_when_all_state_inputs_are_defined` | `CORE_CONDITIONAL` | 결정론적 상태전이 함수는 설계 명세의 성질; IEC 61131-3 SFC 자체가 자동 보장하지 않음 |
| `sw02_sequence_steps_transitions_actions_and_fault_timing` | `CORE_CONDITIONAL` | Step/Transition/Action 일반원리, Timeout은 설계 선택으로 취급 |
| `sw02_permissive_is_a_condition_for_authorized_start` | `CORE_SUPPORTED` | Permissive는 허용 조건으로서 특정 운전의 실행을 개방함; 모든 경우 AND 식으로 한정하지 않음 |
| `sw02_interlock_changes_or_inhibits_control_action` | `CORE_SUPPORTED` | Interlock은 단순 경보와 구별되는 조작 억제/보호 작용; 구체 동작은 사양 정의 |
| `sw02_trip_response_preempts_sequence_in_documented_safety_example` | `MODEL_EXAMPLE` | Siemens Safety Matrix 특유 Trip Reset 순서·Ack 정책은 보편적 필수 정답이 아님 |
| `sw02_step_completion_uses_device_feedback_and_timeout` | `CORE_CONDITIONAL` | 동작 완료 Feedback와 Timeout 판단은 산업 공통 설계 패턴, Rockwell 구체 구현은 사례 |
| `sw02_sfc_action_lifecycle_and_output_retention` | `MODEL_EXAMPLE` | Siemens SFC/ Rockwell P_SEQ 출력 유지·Action qualifier 차이는 제품 구현; 통일된 무조건 규칙 아님 |
| `sw02_sensor_voting_tradeoff_is_architecture_specific` | `CORE_CONDITIONAL` | 1oo2/2oo3 투표는 오동작 Trip과 위험시 Trip 실패 간 상충, 기능별 정량평가 필요 |
| `sw02_first_out_simultaneous_scan_behavior_is_vendor_specific` | `MODEL_EXAMPLE` | Rockwell PINTLK의 동시 scan first-out 표시는 제품 고유 동작; 물리적 고장 순서를 보장하지 않음 |
| `sw02_sfc_transition_is_boolean_condition_enabling_next_step` | `CORE_CONDITIONAL` | Boolean Transition은 SFC의 널리 쓰이는 개념; 제조사 Scan/우선순위 세부는 독립 |
| `sw02_bypassability_is_configured_and_selected_with_role_controls_in_plantpax` | `MODEL_EXAMPLE` | Rockwell PlantPAx Engineering/Maintenance 역할 및 Bypass 조건은 제조사 고유, 보편 필수 Fact 아님 |
| `balanced_trim_assessment_uses_residual_unbalance_area_seat_load_and_application` | `CONSOLIDATE_CANDIDATE` | 불평형 면적·Seat Load·마찰 합산을 재서술; Core force equation과 actuator force 통합 검토 |
| `control_valve_packing_friction_is_a_scoped_deadband_contributor` | `CORE_CONDITIONAL` | Packing 마찰은 Deadband 기여 가능; 시스템 지연·진동의 단독 원인으로 단정 금지 |
| `balanced_and_noise_attenuation_trim_are_distinct_coexisting_functions` | `CORE_CONDITIONAL` | 압력 불평형력 감소와 다단 감압 저소음은 서로 다른 설계 목표이며 병용 가능 |

## Core Fact 병합 제안 (승인 전 변경 금지)

1. **압력 불평형력**: `balanced_trim_unbalance_force_equation` + `control_valve_effective_unbalance_area_definition` + `balanced_trim_residual_unbalance_area`; 하나의 물리 Core와 설계별 조건으로 묶는다. 나머지 `control_valve_unbalance_area_not_always_seat_area`, `ideal_full_balance_is_not_universal_actual_state` 등을 별도 점수로 중복 반영하지 않는다.
2. **Seat/Balance Seal 누설**: `plug_to_cage_and_seat_leakage_paths_are_distinct`에 조건부 원리를 놓고, 제조사 고유 Seal 구조는 해설 참고로 둔다. `balanced_trim_seal_leakage_is_separate_internal_path` 중복 가점 금지.
3. **구동력 산정**: `sliding_stem_actuator_force_includes_seat_load_unbalance_and_friction`를 핵심으로 하며 `balanced_trim_assessment_uses_residual_unbalance_area_seat_load_and_application`은 같은 핵심 기준의 반복 가점을 피한다.
4. **물리 Trip/Interlock**: Fail-safe는 위험평가에서 정의한 안전상태; Rockwell PINTLK 동시 스캔 First-Out·PlantPAx Bypass 역할·Siemens Trip reset 관행은 일반 답안 필수 체크항목에서 제외하는 것이 타당.

## 공식 근거와 한계

- [Emerson/Fisher Control Valve Handbook (발행자)](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valve-handbook): 밸브 구성·Actuator·마찰·유체력 원리 및 모델별 설계 필요성. [Handbook cage-guiding 설명](https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf), §3.6. **제조사 고유 공차·실험결과를 일률 수치로 적용하지 않음**.
- [HSE functional safety](https://www.hse.gov.uk/eci/functional.htm), [HSE Control Systems 보호 Trip/Interlock](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm): 위험기반 안전상태·보호계층·독립성, 일반운전과 보호기능 구분.
- [IEC 61131-3:2025 발행기관 공개 범위](https://webstore.iec.ch/en/publication/68533): ST/LD/FBD 및 SFC 언어 요소의 표준 범위. **특정 어플리케이션의 상태전이 유일성/Timeout/안전성은 표준 존재만으로 인증되지 않음**.
- [Rockwell PINTLK 공개 기술문서](https://www.rockwellautomation.com/en-id/docs/studio-5000-logix-designer/37-00/contents-ditamap/instruction-set/plantpax-instructions/pintlk.html): 동일 Scan 여러 first-out 비트·Bypass 조건을 확인했으나 **그 제품/버전 사례에 한정**.

## 변경 및 검증 경계

- Registry/Pack/Logic/Generated/Score 미변경. 이 문서 자체는 제안/내용 검토 기록이다. 제품 예시·중복 Fact의 최종 삭제는 출제 요구·관련 Anchor·테스트 영향까지 확인해야 한다.
- 로컬 `README.md`, `docs/operational_quality_checksheet.md`와 운영 체크아웃 미접근. `validate-all`, release gate 및 CI 미실행.
