# Topic Pack·Fact Anchor·Logic Check 원자성 점검 및 보완 계획

점검일: 2026-10-05
대상 revision: `8a203c4` 및 현재 worktree source
상태: inventory 구조 점검 완료, 의미 보완은 미실시

## 1. 판정 기준

- **Topic Pack:** 독립적으로 출제될 수 있는 문제군과 지식 소유 경계 하나를 소유한다.
  하나의 공식 출제기준 대항목에 Pack 하나만 둔다는 뜻은 아니다. 연결된 하위 요구가
  하나의 통합 답안과 판정 경계를 공유하면 같은 Pack에 둘 수 있다.
- **Fact Anchor:** 답안에서 독립적으로 참·거짓 또는 충족 여부를 판단할 수 있는 정답
  주장 하나를 표현한다. 조건·단위·예외는 주장의 유효범위를 한정할 때 유지한다.
- **Logic Check:** 독립적으로 식별할 수 있는 오답 주장 또는 오개념 하나를 표현한다.
  여러 표현 패턴은 같은 오개념의 표기·표현 변형일 때 한 rule에 둘 수 있다.

한 레코드의 두 절이 서로 다른 정오 판정을 받을 수 있다면 분리 후보이다. 문장 길이,
접속사, Anchor 개수만으로 위반을 확정하지 않는다. Topic 분리는 실제 문제군, 독립
답안, routing 영향 및 전후 회귀 결과가 있어야 한다.

## 2. 점검 범위와 방법

전체 `rubrics/topic_packs/`의 85개 Pack, 2,061개 Fact Anchor 및 Logic Check source를
읽어 구조·참조·질문계약·표현 형태를 집계했다. 다음 기존 도구를 사용했다.

- `scripts/audit_topic_pack_atomicity.py`
- `scripts/rubric_manager.py validate-topic-packs`
- `scripts/rubric_manager.py validate-generated-rubrics`
- `scripts/validate_topic_pack_quality.py`

이번 검토는 코드로 전수 inventory scan을 했지만, 2,061개 Anchor와 모든 Logic rule의
기술 의미를 전문가가 일일이 승인한 전수 검토는 아니다. 정량 경고는 조사 우선순위다.
구조 gate가 통과했다는 사실은 각 Fact/오답 규칙의 원자성이 이미 보증됐다는 의미가
아니다.

## 3. 결과 요약

| 검사 | 결과 | 해석 |
|---|---:|---|
| Pack / Fact Anchor | 85 / 2,061 | 현재 대상 inventory |
| Topic Pack atomicity audit | 차단 오류 0, 경고 38 | schema/소유권 오류는 없으나 구조 검토 후보가 남음 |
| Source validator | 통과 | 필수 schema와 cross-reference 유효 |
| Generated validator | 통과 | source projection이 generated bank와 구조적으로 일치 |
| Topic quality validator | 오류 0, 경고 28 | 원자성 의미 검증은 포함하지 않음 |
| Logic `fatal_conditions` | 문자열 550, 객체 493 (총 1,043) | 같은 의미가 두 데이터 형태에 분산. 원자성 자체를 증명하지 않음 |
| Logic `major_checks` | 문자열 60, 객체 447 (총 507) | 동일하게 이질적 표현이 남아 있음 |

Logic 수량은 unique misconception 수가 아니다. 같은 개념이 profile, deterministic
check 또는 generated mirror에 중복 표현될 수 있다. 이를 서로 독립된 오류 규칙 개수로
해석하지 않는다.

## 4. 확인된 원자성 위반 및 구체적인 보완

아래는 자동 경고가 아니라 내용을 직접 확인한 우선 수정 후보이다.

| 수준 | 현재 레코드 | 문제 | 보완 방향 |
|---|---|---|---|
| P0 Fact | `second_order_lag_response_by_damping_ratio / so2_zero_negative_damping` | 하나의 Anchor가 `ζ=0`의 임계 안정·지속진동과 `ζ<0`의 불안정·발산을 함께 주장한다. 각각 독립 질문·판정이 가능하다. | `ζ=0` 지속진동/임계안정 Anchor와 `ζ<0` 우반평면/불안정 Anchor로 분리하고 질문계약, Logic 참조, generated bank를 갱신한다. |
| P0 Fact | `hazop_lopa_ipl_risk_reduction_sil_target_allocation / hazop_lopa_required_rrf` | 한 569자 statement 안에 RRF 정의와 1 이하 해석, 저·고 demand의 PFDavg/PFH 선택, SIL 약어 정의까지 들어 있다. 서로 다른 평가 주장이다. | RRF 정의·해석, demand mode별 integrity metric, SIL 용어 정의를 별도 Anchor로 분리한다. 각 주장의 출처·조건을 유지한다. |
| P0 Logic | `second_order_lag_response_by_damping_ratio / llm_profile.fatal_conditions`의 표 분류 규칙 | 한 문자열이 부족감쇠, 임계감쇠, 과감쇠의 세 잘못된 구간 대응을 한 rule로 묶는다. 각 오답 표기는 독립 검출·수정 가능하다. | 세 개의 misconception rule로 나누거나, 각각을 가리키는 개별 claim ID와 동일 severity를 부여한다. 표 전체가 잘못된 경우의 통합 회귀도 별도로 유지한다. |

`so2_pole_response_relationship` 및 복합 경계·요약형 Anchor들은 추가 검토가 필요하지만,
복수 용어가 나온다는 사실만으로 분리 위반으로 단정하지 않는다. 관계의 정의·조건·
해석이 하나의 주장인지, 서로 독립 채점 가능한 claim들의 묶음인지 사람 검토로 판정한다.

## 5. Topic Pack 경계 조사 후보

기존 audit은 `required_anchor_ids` 교집합으로 질문 패턴 그래프를 만들고, 3개 이상의
분리 component가 있으면 경고한다. 이는 같은 주제의 서로 다른 세부 질문도 분리하므로
아래 목록은 모두 **검토 후보**이며 분리 지시가 아니다.

### 복수 신호가 겹쳐 우선 조사할 Pack

| Topic Pack | Anchor 수 | 질문 component | 다음 조사 |
|---|---:|---:|---|
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 40 | 9 | 사이버 방어, 공급망, 사고대응 질문이 같은 독립 출제 문제군인지 대조 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | 40 | 6 | 실시간성, 시간동기, 복구·resilience가 하나의 네트워크 문제군인지 대조 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 40 | 6 | 매체/프로토콜 비교와 상호운용성·선정 문제가 답안 경계를 공유하는지 대조 |

### 질문군 연결성 경고 24개

다음은 질문 패턴이 Anchor를 공유하지 않는 component가 3개 이상인 Pack이다.
숫자는 component별 패턴 수이며, 독립 문제군 개수로 확정된 값은 아니다.

| Topic Pack | Component별 패턴 수 |
|---|---|
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | 7, 2, 1 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 1, 8, 1 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 1, 7, 2 |
| `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` | 1, 1, 1, 1, 1, 1, 1, 1 |
| `flow_measurement_meter_principles_velocity_selection` | 10, 1, 1 |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | 5, 1, 1 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | 3, 3, 2, 1, 1 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | 1, 5, 1, 1, 1, 1 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 2, 1, 1, 3, 2, 1 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 4, 3, 3 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 7, 2, 1 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 3, 1, 1 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 2, 1, 1, 1 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 1, 1, 1, 1, 1, 1, 1, 1, 2 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | 8, 1, 1 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 4, 5, 1, 1 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 2, 7, 2, 3 |
| `power_electronics_converters_motor_drive_control` | 5, 1, 1 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 1, 8, 1 |
| `routh_hurwitz_stability_criterion_gain_range` | 2, 2, 1 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 6, 1, 1, 2, 1, 1 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 5, 1, 3, 1 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 10, 1, 1, 1 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 1, 1, 1 |

### Anchor 40개 이상 경고 10개

| Topic Pack | Anchor 수 |
|---|---:|
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | 40 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 40 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 48 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 52 |
| `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles` | 48 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 48 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | 40 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 40 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 40 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 44 |

### Alias collision 두 쌍

- `lead_lag_compensator_phase_margin_steady_state_error` ↔
  `root_locus_stability_gain_design`
- `passive_sensor_resistive_capacitive_inductive_transduction` ↔
  `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`

각 표현이 동일한 routing trigger인지, 광범위한 공통 개념인지 살펴본 뒤 alias 소유를
한정한다. 라우터/Golden에서 잘못된 선택이 재현되지 않으면 Pack 경계를 변경하지 않는다.

## 6. 보완 실행 계획

### Phase 1 — 원자성 규약과 무변경 baseline (완료)

1. Pack / Anchor / Logic Check의 단위를 문서에 명시했다.
2. validator, atomicity audit, generated validator를 실행해 기준선 결과를 기록했다.
3. 이 단계에서는 채점 source와 generated bank를 변경하지 않았다.

### 다음 작업 실행 순서

다음 작업자는 아래 순서를 유지한다. 앞 단계 결과가 나오기 전에는 Pack 분할이나
대량 source 수정을 시작하지 않는다.

1. **P0 Fact/Logic 세 사례 의미 재검토:** 이 문서 4절의 세 레코드만 읽고 각 절의
   독립 채점 가능성, 적용 조건, 원 출처, 기존 ID 참조를 정리한다. 권위 있는 출처가
   없거나 문맥이 모자라면 사실을 보충하지 말고 보류한다.
2. **변경 전 영향표 작성:** 해당 anchor/rule ID가 사용되는 `expected_question_patterns`,
   `logic_check.json`, question-demand contract, machine contract, fixtures/tests,
   learning synthesis `grading_links` 및 Feedback resolver를 찾아 영향 목록을 만든다.
   ID 변경은 기존 이력·Master 참조와의 호환 확인 전에는 하지 않는다.
3. **범위 확정과 human review:** 사용자가 승인한 Pack 범위와 수정안을 검토받는다.
   승인된 source hash가 있는 managed Topic은 README/source 변경 후 같은 승인 기록을
   재사용하지 않고 공식 승인 workflow로 재승인한다. unmanaged legacy Pack에
   `topic_status.json`을 임의 추가하지 않는다.
4. **한 Topic씩 구현:** P0 중 한 Topic만 수정하고 관련 질문 계약·오답 규칙·회귀를
   함께 갱신한다. Fact Anchor가 정본이고 generated bank는 validator/generator로
   재생성한다. 다른 Topic으로 묶음 확장하지 않는다.
5. **검증과 결과 기록:** 기존 정상/부분/오답/fatal 입력 및 인접 Topic 경계를 같은
   환경에서 재생하고 primary route, candidate order/score, requirement 상태, 점수,
   fatal, verdict를 전후 비교한다. 차이는 의도·영향·회귀 결과와 함께 기록한다.
6. **Pack boundary review:** P0 Fact/Logic 보정 완료 후 5절의 우선 3개 Pack을
   실제 문제/출처에 대조한다. 나머지 disconnected 경고는 순서대로 한 Pack씩
   검토한다. 후보마다 보완 기록 양식을 작성하고 승인 전에는 source를 바꾸지 않는다.
7. **통합 release:** 개별 결과를 모두 설명한 후 source/generated/release/atomicity
   전체 gate를 수행한다. 이 점검 단계 자체는 commit/push 권한이나 승인으로 간주하지
   않는다.

### Pack·Fact·Logic 검토 기록 양식

각 검토 후보마다 다음 항목을 남긴다. `유지` 결정도 evidence와 함께 기록한다.

```text
Topic ID / record ID:
현재 주장 또는 문제군:
출처와 locator:
독립 정오 판정 가능 여부:
함께 두어야 하는 조건·예외:
소유 경계 / 인접 Topic handoff:
문제 예시와 required_anchor_ids:
router 및 deterministic/LLM 판정 영향:
학습 목표·순서·기존 grading_links 영향:
결정: 유지 / Anchor 분리 / Logic rule 분리 / question contract 보완 / Pack 분리 후보 / 보류
근거와 남은 불확실성:
필요한 승인자 및 회귀 fixture:
```

### Phase 2 — 명백한 다중 주장 레코드 보정

1. P0 표의 두 Fact Anchor를 각각 최소 claim으로 나눈다.
2. 해당 anchor ID를 참조하는 질문 계약, logic rule, training/grading link를 전부 찾아
   새 ID에 맞게 재배치한다. 기존 ID를 제거할 때는 연결 참조·저장 결과 호환을 확인한다.
3. 복합 Logic Check를 같은 fatal 의미를 유지하는 독립 rule로 분리하고,
   각각 정답·오답·safe-context Golden fixture를 둔다.
4. 의미 source 변경이므로 human review와 managed topic이면 source-hash 재승인을 거친다.

### Phase 3 — 경고 Pack의 실제 문제 대조

우선 복수 신호가 겹치는 세 Pack을 조사하고, 이어서 24개 disconnected 경고를
실제 기출·예상 문제와 비교한다. Pack별로 아래 결정을 기록한다.

- **유지:** 독립 pattern들이 같은 지식 소유권·통합 답안 문제군을 구성한다.
- **질문 계약 보완:** 같은 Pack이 맞지만 특정 문제의 anchor scope가 넓거나 모호하다.
- **Anchor/Logic 보완:** Pack 경계는 맞고 내부 claim이나 오답 단위만 복합적이다.
- **Pack 분리 후보:** 독립 문제군·답안 구조가 있고 router 오선택 또는 owner 혼선이
  Golden으로 재현된다.

동일 공식 출제기준에 매핑되어 있다는 사실은 Pack을 합치는 근거로 충분하지 않다.
반대로 별도 question pattern이나 component가 있다는 사실만으로 분리하지 않는다.
독립된 질문 의도, 최소 공통 답안 구조, 공통/고유 Anchor 경계와 오라우팅의 재현을
함께 확인한다.

### Phase 4 — Pack 분리·통합은 증거 기반으로 한 개씩

분리 후보는 신규 Topic workflow, 명확한 source ownership, human review와 승인,
질문 routing 회귀, 정상/부분/오답/fatal 점수 비교, 학습 동선·handoff 검토를 거친다.
분리 후 이전과 동일한 입력의 primary topic, 후보 순위, 점수, fatal 여부와 verdict를
기록한다. anchor 수를 줄이기 위한 기계적 분할은 하지 않는다.

### Phase 5 — 린트 및 release Gate 개선

1. Factor-level validator에는 없는 의미 원자성을 정규식으로 완전 판정하려 하지 않는다.
   길이/접속사 규칙은 후보 경고에만 쓴다.
2. question pattern의 anchor ID 존재·중복 및 Logic ID/anchor reference의 무결성을
   자동 검사한다.
3. 복합 claim 후보는 review report로 내고 사람이 resolve한다. 승인 없는 대량 rewrite,
   auto-split, generated-bank 직접 수정은 금지한다.
4. 매 batch마다 source validators, generated rebuild/validation, atomicity audit,
   focused regression, `git diff --check`를 통과시킨다.

## 7. 완료 판정

- P0 Fact 및 Logic 사례가 독립 판정 가능한 항목으로 분리되거나, 병합 유지 근거가 기록됨
- 경고 24개와 anchor 수 10개 Pack 각각 유지/보강/분리 검토 결론이 남음
- 분리한다면 분리 전후 routing·점수·fatal·verdict 변화와 Golden 결과를 설명 가능
- 기존 사람 승인·source hash 및 WordPress 연계의 provenance가 훼손되지 않음
- 전체 generated release gate 및 관련 학습 projection 호환 검증 통과
