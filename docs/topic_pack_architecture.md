# Topic Pack Architecture

이 문서는 `prof_eng_answer`의 Topic Pack 구조, source of truth, generated runtime bank, 현재 inventory와 Software Topic 범위를 설명한다.

실제 작성 절차는 `topic_pack_workflow.md`, JSON 작성 기준은 `rubric_authoring_guide.md`를 함께 본다.

## 1. 현재 상태

현재 generated manifest 기준:

| 항목 | 현재 상태 |
|---|---:|
| Topic Pack | 52 |
| Generated bank | 6 |
| Software Topic | 13 |
| 기본 Rubric Bank mode | `generated` |

Topic 개수의 authoritative source는 다음 파일이다.

```text
rubrics/generated/topic_pack_manifest.generated.json
```

Runtime bank 선택의 authoritative source는 `rubric_bank_paths.py`다.

Manifest 내부의 설명성 metadata 문자열보다 실제 `RUBRIC_BANK_MODE`와 runtime path resolver를 우선한다.

## 2. Source와 generated의 경계

### Topic Pack source

```text
rubrics/topic_packs/<topic_id>/
├── README.md
├── fact_anchor.json
├── logic_check.json
├── model_answer.json
└── topic_importance.json
```

일부 authoring 도구가 상태 metadata 파일을 추가할 수 있지만, runtime projection의 핵심 source는 위 네 JSON과 topic identity다.

### Topic Sheet

```text
docs/topic_sheets/<topic_id>.md
```

Topic Sheet는 runtime Rubric이 아니다. 요구사항, 정답 Fact, fatal/warn, false positive, expected question, field judgement와 Topic boundary를 사람이 검토하기 위한 구조화 Markdown이다.

### Generated bank

```text
rubrics/generated/
├── fact_anchors.generated.json
├── logic_check_profiles.generated.json
├── logic_checks.generated.json
├── model_answers.generated.json
├── topic_importance.generated.json
└── topic_pack_manifest.generated.json
```

Generated bank는 build output이다. 직접 수정하지 않는다.

## 3. 각 source 파일의 책임

| 파일 | 책임 |
|---|---|
| `README.md` | 사람이 이해하는 Topic 목적, 범위, 검토 메모 |
| `fact_anchor.json` | 정답 coverage를 구성하는 atomic Fact |
| `model_answer.json` | 고득점 답안 구조, expected question과 field connection |
| `logic_check.json` | 정답과 직접 충돌하는 오류, safe case와 verifier profile source |
| `topic_importance.json` | difficulty, selection importance, high-band 조건 |
| Topic Sheet | JSON authoring 전 요구사항·경계 검토 |

## 4. Runtime load

기본 mode:

```text
RUBRIC_BANK_MODE=generated
```

`rubric_bank_paths.py`가 다음 generated path를 선택한다.

- Fact Anchor
- Model Answer
- Topic Importance
- Logic Check
- Logic Check Profile
- Topic Pack Manifest

Legacy bank는 비교·호환 목적으로 남아 있지만, 현재 Topic coverage 개수를 legacy Model Answer/Fact JSON의 item count로 설명하지 않는다.

## 5. 문서 탐색용 영역 분류

아래 분류는 문서 탐색용이다. Runtime difficulty 또는 Question Type 분류가 아니다.

| 영역 | Topic 수 |
|---|---:|
| Software / OT / Industrial AI | 13 |
| Control Valve / Final Control Element | 16 |
| Control Theory | 12 |
| Instrumentation / Sensor | 11 |
| 합계 | 52 |

## 6. Software Topic Pack: SW-01~SW-13

| SW | Topic ID | 핵심 범위 |
|---|---|---|
| SW-01 | `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | PLC·DCS·SCADA·Remote I/O 구조, 이중화, 가용성·신뢰성 |
| SW-02 | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | Sequence, Interlock, Permissive, Trip, 상태전이, Fail-safe |
| SW-03 | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | HMI/SCADA, Alarm, Setpoint, SOE, 운전자 정보관리 |
| SW-04 | `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 제어 Software Lifecycle, V-model, 추적성, V&V |
| SW-05 | `sis_sil_safety_software_independence_systematic_failure_verification_validation` | SIS/SIL Software, 독립성, systematic failure, V&V |
| SW-06 | `configuration_change_release_backup_rollback_migration_obsolescence_management` | 형상·변경·Release, Backup/Rollback, Migration, Obsolescence |
| SW-07 | `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 산업 유·무선통신, Fieldbus/Ethernet, 상호운용성, 선정 |
| SW-08 | `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | 실시간성, Determinism, 시간동기, Fault recovery, Resilience |
| SW-09 | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | OT Cybersecurity, Defense-in-depth, Allowlisting, Supply chain, Incident response |
| SW-10 | `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 프로젝트 문서, FAT/SAT, 시운전, 성능시험, 인수 |
| SW-11 | `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | Historian, MES, IT/OT integration, 데이터 품질, 실시간 처리 |
| SW-12 | `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | Industrial AI/ML, 이상진단, 예지보전, Model lifecycle |
| SW-13 | `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | Physical AI, Robot, Sensor fusion, Digital Twin, 자율제조와 안전제어 |

SW 번호는 학습·문서화용 mapping이다. Runtime key는 `topic_id`다.

## 7. Control Valve / Final Control Element 16개

- `balanced_trim_unbalanced_trim_structure_sealing_applications`
- `control_valve_authority_rangeability_gain_installed_performance`
- `control_valve_cavitation_flashing_choked_flow_damage_prevention`
- `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`
- `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`
- `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`
- `control_valve_positioner_ip_converter_booster_accessories_calibration`
- `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`
- `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`
- `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`
- `control_valve_sizing_cv_kv_reynolds_liquid_selection`
- `control_valve_types_globe_rotary_body_actuator_selection`
- `final_control_element_sil_sis_esd_valve_partial_stroke_test`
- `smart_positioner_diagnostics_valve_signature_predictive_maintenance`

## 8. Control Theory 12개

- `bode_frequency_response_stability_margin_bandwidth`
- `feedback_system_closed_loop_sensitivity_steady_state_error`
- `lead_lag_compensator_phase_margin_steady_state_error`
- `lqr_optimal_state_feedback_riccati_weighting_design`
- `nyquist_stability_criterion_gain_phase_margin`
- `pid_controller_tuning_sequence_gain_effects`
- `root_locus_stability_gain_design`
- `routh_hurwitz_stability_criterion_gain_range`
- `second_order_lag_response_by_damping_ratio`
- `second_order_system_resonance_frequency_response`
- `state_feedback_reference_tracking_prefilter_integral_action`
- `state_space_controllability_observability_pole_placement`

## 9. Instrumentation / Sensor 11개

- `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`
- `passive_sensor_resistive_capacitive_inductive_transduction`
- `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`
- `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
- `rtd_temperature_sensor_principle_pt100_wiring_compensation`
- `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`
- `temperature_measurement_error_heat_transfer`
- `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`
- `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`

## 10. Topic boundary와 ownership

Topic이 늘어날수록 개별 Fact 정확성보다 boundary 관리가 중요해진다.

새 Topic은 다음을 명시한다.

- 이 Topic이 직접 소유하는 핵심 요구
- 인접 Topic으로 handoff할 내용
- broad alias로 가져오면 안 되는 표현
- expected question pattern
- cross-topic dependency
- false positive 주의사항

예를 들어 Software 영역에서는 Lifecycle, 변경관리, Cybersecurity, Safety Software의 ownership을 섞지 않는다.

Control Valve에서는 특성, authority/rangeability, sizing, actuator force, severe service, diagnostics를 한 Topic의 broad alias로 합치지 않는다.

## 11. Generated rebuild 원칙

Source authoring 중에는 generated bank를 반복 수정하지 않는다.

권장:

```text
Topic source 작성
  → focused validation
  → topic 단위 commit
  → 다음 topic
  → lane / batch 의미 감사
  → integration 단계
  → generated bank 6개 rebuild
  → release validation
```

Generated rebuild commit은 대규모 line diff가 발생할 수 있다. 이는 JSON projection과 정렬·직렬화에 따른 build artifact 특성일 수 있으므로 source와 manifest coverage 검증을 함께 본다.

## 12. Validation

Topic source 단계:

```text
py_compile
  → topic focused tests
  → schema / quality validation
  → git diff --check
```

Integration 단계:

```text
read-only cross-topic audit
  → generated rebuild
  → validate-all
  → release coverage gate
  → PROMOTE_GENERATED=0 release validation
  → clean checkout / CI
```

Container smoke는 runtime 차이가 실제로 관련될 때만 수행한다.

## 13. Hermetic regression

Committed test는 다음을 지킨다.

- 개발자 로컬 `data/sessions/...`를 fixture로 사용하지 않는다.
- 재현이 필요한 session input은 `scripts/fixtures/`에 의미가 드러나는 이름으로 저장한다.
- 개인 session ID를 테스트 source의 영구 계약으로 사용하지 않는다.
- clean checkout에서도 focused test와 release validation이 동일하게 통과해야 한다.

## 14. Source of truth 우선순위

1. 현재 commit의 runtime code
2. Topic Pack source JSON
3. generated manifest와 generated bank
4. focused regression / release validation
5. 현재 문서
6. archive와 과거 commit 기록

문서와 runtime이 충돌하면 위 순서로 재검증한다.
