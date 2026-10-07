# 기존 Topic Pack Problem-unit 적합성 1차 감사

점검일: 2026-10-06
기준: `docs/topic_pack_workflow.md` §4 Problem-unit / coverage 계약

## 1. 판정 범위와 현재 지위

대상은 `rubrics/generated/topic_pack_manifest.generated.json`에 있는 기존 82개다.
다만 manifest의 `runtime_status`는
`generated_candidate_not_yet_runtime_default`이므로 이 82개를 운영 runtime이 이미
사용 중이라고 부르지 않는다. Source directory에는 Chapter 20 신규 초안 3개가 더
있지만 이들은 이번 82개 집계에서 제외했다.

기존 Pack의 질문 패턴은 확인된 기출이 아니라 관련 지식으로 작성한 예상 문제다.
공식 출제기준 문서와의 PRIMARY/SECONDARY 표도 내부 후보 정렬이지 공식 분류·승인이
아니다. 따라서 이번 감사는 `기출 여부`가 아니라 다음을 판단한다.

1. 대표 예상 문제가 출제 가능한 구체적 요구(대상·동사·조건)를 갖는가?
2. Pack 안의 expected patterns가 같은 문제의 변형인지, 독립된 문제들인지?
3. 그 대표 문제를 완결 답안으로 풀도록 연결 지식과 Anchor가 충분하고 추적 가능한가?

## 2. 전수 screen 결과

| 지표 | 결과 | 의미 |
|---|---:|---|
| manifest 대상 Pack | 82 | 기준 inventory |
| Fact Anchor | 2,037 | 원자성·coverage 검토 대상 |
| `expected_question_patterns` | 717 | Pack당 평균 8.7개, 중앙값 10개 |
| 패턴이 정확히 10개인 Pack | 43 | 표준 템플릿 질문 개수가 문제 단위 경계를 증명하지 않음 |
| 분리된 질문-Anchor family 경고 | 21 Pack | 각 Pack의 패턴이 서로 단절된 복수 묶음일 가능성 |
| Anchor 40개 이상 경고 | 10 Pack | 지식 범위·소유권 재검토 신호이지 자동 분리 지시가 아님 |
| Alias 충돌 경고 | 4 Pack | Problem-unit 분리보다 Router owner 검토가 우선 |
| 위 원자성 경고가 하나 이상인 Pack | 30 Pack | 82개 중 우선 의미 검토 대상 |
| 패턴이 한 번도 참조하지 않는 Fact Anchor가 있는 Pack | 51 Pack | 불필요 지식 또는 예상 문제/coverage 연결 누락 후보 |
| 패턴-Anchor union 참조율 90% 미만 | 18 Pack | 연결 누락/범위 초과 여부 확인 후보 |
| 패턴-Anchor union 참조율 85% 미만 | 7 Pack | 우선 coverage 확인 후보 |

CSV의 단일 triage 결과는 경계 재검토 28개, coverage 연결 재검토 10개, alias 경계
재검토 2개, 구조 경고 없는 잠정 유지 42개다. 단일 triage는 우선 처리 신호이므로,
다른 축의 중첩 경고·낮은 참조율은 CSV 지표와 아래 coverage 목록에서 함께 본다.

평균 94.2% 참조율은 한 Anchor가 질문에 적어도 한 번 연결되는 비율일 뿐이다.
각 문제의 모든 요구가 충족된다는 뜻은 아니다. 반대로 미참조 Anchor도 바로 삭제할
대상이 아니다. 이는 “다른 대표 문제를 추가할지 / 지식을 handoff할지 / 범위 밖으로
둘지” 검토할 신호다.

기계 screen의 Pack별 질문 수, Anchor 수, 참조율, 경고와 임시 disposition은
[`topic_pack_problem_unit_screen_20261006.csv`](topic_pack_problem_unit_screen_20261006.csv)에
기록했다. `잠정 유지 후보`는 자동 경고가 없다는 뜻이며 내용 승인 또는 충분성 확인이
아니다. 82개 전체 목록은 내부 후보 정렬표인
[`topic_pack_classification.md`](topic_pack_classification.md)에서 확인할 수 있다.

## 3. 우선 수정 후보 선정

아래 5개를 **1차 Problem-unit 재구성 후보**로 선정한다. 선정은 Pack 경계·문제 문장·
요구-지식 coverage를 정리하자는 뜻이다. 기존 A/B/C/D/E 채점 계약, deterministic
scoring, Question Type, fatal 처리, Router authority를 바꾸거나 Pack을 지금 분할·삭제한
것은 아니다.

| 순위 | Topic Pack | 판정 근거 | 재구성 방향 |
|---:|---|---|---|
| 1 | `control_valve_positioner_ip_converter_booster_accessories_calibration` | 40 Anchor와 10개 질문 패턴이 전통 포지셔너 작동원리, I/P, 부스터·부속기기, split-range, 교정, 고장진단을 각각 묻는다. 별도 Smart Positioner Pack도 있어 경계가 특히 중요하다. | 사용자가 지정한 전통적 포지셔너의 구조·동작을 중심 Problem Unit으로 삼고, 독립 문제로 보이는 accessory/calibration/diagnosis 요구는 기존 owner와 비교해 분리·handoff 후보로 정리한다. Smart 진단은 기존 Smart Positioner 소유로 둔다. |
| 2 | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` | 28 Anchor, 10 패턴, 9개 disconnected family. DP 구성·Wet/Dry leg·밀도 보상·Remote Seal·계면·설치오차·Radar/GWR 비교가 한 Pack에 공존한다. | DP 레벨 핵심 문제와 별도 계산/설치/비교 문제를 가른다. Radar/GWR와 Chapter 20의 Sight Glass·Float·Bubbler 초안 간 handoff를 명확히 한다. |
| 3 | `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | 35 Anchor, 10 패턴, 3개 disconnected family(7/2/1). Hardware lifecycle, panel/부품 설계, 생산검증·시험이 한 묶음이다. | “Hardware lifecycle 종합문제”가 실제 대표 unit인지 검토하고, 독립적인 설계·생산검증 요구를 분리 후보로 기록한다. |
| 4 | `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 34 Anchor, 10 패턴, 3개 disconnected family(1/8/1). 프로젝트 Scope/Cost, 문서체계, FAT/SAT·시운전·인수가 섞이고 프로젝트관리·SW V-Model Pack과 경계가 겹친다. | 프로젝트관리, 설계문서/추적성, 현장시험·인수 중 하나의 출제 가능 종합문제인지 검토하고 owner/handoff를 분명히 한다. |
| 5 | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | 31 Anchor, 10 패턴, 5개 disconnected family(3/3/2/1/1). HMI 설계, Alarm lifecycle, Setpoint/Trip/Interlock, SOE·권한관리가 독립 요구일 수 있다. | 운전자 정보/HMI와 Alarm·Trip 관리 등 서로 다른 답안 축을 식별하고 대표 문제 및 owner를 정리한다. |

### 2차 후보

첫 배치 이후 다음을 순서대로 본다. 이들은 후보이지 자동 분할 결론이 아니다.

- **커뮤니케이션 경계:** `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`, `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- **계측/설치 범위:** `instrumentation_installation_wiring_impulse_tubing_inspection_codes`, `instrumentation_power_grounding_shielding_ups_ground_loop_emc`, `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- **다기술·응용 묶음:** `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`, `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`, `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`, `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`, `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`, `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`
- **대형 Control Valve 묶음:** `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`, `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`, `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`, `final_control_element_sil_sis_esd_valve_partial_stroke_test`, `configuration_change_release_backup_rollback_migration_obsolescence_management`, `smart_positioner_diagnostics_valve_signature_predictive_maintenance`, `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`

그 외의 경고 대상도 CSV의 근거를 유지하며 후속 검토한다. 경고가 없는 나머지는
**현재 우선순위가 낮은 잠정 유지군**으로 분류했을 뿐, 충분성·출제 가능성을 승인한
것은 아니다.

## 4. Coverage 연결 재검토 우선 목록

다음 참조율은 `expected_question_patterns`의 required anchor ID union과 Pack Anchor ID의
비율이다. 실제 문제 요구 coverage를 자동 입증하지 않는다.

| Topic Pack | 참조율 | 우선 확인 |
|---|---:|---|
| `pid_controller_tuning_sequence_gain_effects` | 60% | PID 정의·식·P/I/D 기능 Anchor가 문제 패턴에서 왜 빠졌는지 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 71% | Radar/GWR Anchor 혼입 여부, 미참조 원리의 별도 Problem Unit 여부 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 79% | 안정성 이론의 경계 주장과 개별 계산문제 coverage 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 79% | 불확도·설치 응답·signal conditioning 요구의 필요성 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 81% | 개시빈도·proof test·SRS lifecycle 요구의 연결 또는 다른 owner handoff 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 81% | RBD/FTA/Markov 및 PFD/PFH 대표 문제별 coverage 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 85% | 설치, 배선, 도압관, 법규/검사 요구별 패턴 소유성 확인 |

## 5. 진행 순서와 안전 경계

1. 전통 포지셔너 Pack의 대표 문제와 요구-지식-Anchor coverage, 기존 10개 패턴의
   disposition을 별도 검토서에 정리했다:
   [`problem_unit_reconstruction_positioner_20261006.md`](problem_unit_reconstruction_positioner_20261006.md).
2. 이 검토에서는 기존 source JSON, generated bank, runtime routing은 변경하지 않았다.
   현재 문제는 40개 Anchor를 지닌 accessory·calibration·diagnosis까지 한 owner로 묶고
   있으며, 중심 문제는 사용자가 지정한 전통 포지셔너 구조·작동원리로 좁히는 방향이다.
3. 2순위 차압식 레벨 측정 Pack도 별도 검토서에 A–E 다섯 Problem Unit 후보, 현재 10개
   패턴 배치, 신규 Chapter 20 지식의 연결과 source 검증 공백을 기록했다:
   [`problem_unit_reconstruction_dp_level_20261006.md`](problem_unit_reconstruction_dp_level_20261006.md).
   현 작업트리에서 바뀐 DP Pack 파일은 덮어쓰거나 되돌리지 않았다.
4. 3–5순위 후보도 기존 10개 패턴을 문제 요구별로 묶고 독립 후보를 가른 검토서를
   만들었다: [`problem_unit_reconstruction_candidates_3to5_20261006.md`](problem_unit_reconstruction_candidates_3to5_20261006.md).
   세 Pack의 source와 routing은 변경하지 않았다.
5. 2차 후보의 첫 배치(통신 2, 설치/접지 2, 압력 계측 1)도 별도 감사했다:
   [`problem_unit_audit_second_wave_comms_install_pressure_20261006.md`](problem_unit_audit_second_wave_comms_install_pressure_20261006.md).
   atomicity 선택 실행은 오류 0·경고 7이며, 연결 패턴과 이미 명시된 SW-07/SW-08 및
   installation/design ownership을 문제 단위 기준으로 정리했다.
6. 의미상 Pack 분할/이동이 필요해지면 새 owner와 기존 routing·학습 View 참조를 확인하고,
   managed workflow 및 focused/full validation 후에도 사람의 source 검토 전에는
   approval/promote를 기록하지 않는다.
7. 전체 82개 구조 감사에서 자동 경고가 없었던 군도 content/출제 가능성 검토 완료로
   오해하지 않도록 `provisional`로 유지한다. 기존 score contract, deterministic scoring,
   Question Type, Router authority, fatal handling, golden/release gates는 변경하지 않는다.

## 6. 변경 및 검증 상태

- 이번 작업: 82개 전수 구조 screen, 1차 후보 5개 전체 상세 감사, 2차 후보 첫 배치 5개
  Problem Unit·coverage·기존 패턴 경계 제안 문서화
- 포지셔너 Pack README와 Topic Sheet를 중심 Problem Unit/coverage 및 독립 후보를 명시하도록 수정
- 채점/라우팅 JSON, generated bank와 topic_id: 변경 없음 (기존 패턴 및 consumer contract 보존)
- 채점·Router 계약: 변경 없음
- 관련 source release validator: 포지셔너 Pack PASS, 사용자 변경이 진행 중이던 차압 레벨 Pack PASS
- 전체 `validate_topic_pack_release.py --all`: **승격 전 Gate에서 중단**. 기존 Chapter 20 draft
  3개에 현재 사람 승인·reviewer·승인 hash가 없어, managed workflow가 generated promotion을
  차단했다. draft 3개는 이 요청 범위 밖의 기존 사용자 변경이며 승인 상태를 위조하지 않았다.
- 포지셔너 Router/semantic focused suite: 29 PASS; 포지셔너 topic release validator: PASS
- 포지셔너 전체 focused script: 39 PASS, 1 FAIL. 유일 실패는 기존 82-entry generated
  manifest와 worktree의 85 source directory(Chapter 20 draft 3개 추가)가 일치하지 않아서다.
  topic-specific source/generation quality validator는 통과했고, 해당 불일치는 새 변경 이전부터
  존재한 inventory integration 상태로 남겼다.
- 문서 상대링크/`git diff --check`: PASS; Chapter 20 boundary test: 3 PASS (저장소 루트 PYTHONPATH 지정)
- 기존 전체 regression: 실행하지 않음 (machine-consumed grading/router JSON 미변경)
- 다음 작업: 포지셔너 Pack의 10개 machine patterns를 별도 Problem Unit/owner로 이관할 때의
  consumer·router migration을 설계한 뒤, 2차 후보 중 보안·다기술 묶음을 계속 감사
