# 산업계측제어기술사 2027~2030 공식 출제기준 Topic Pack Coverage

## 1. 목적

이 문서는 산업계측제어기술사 2027~2030 필기 공식 출제기준 33개 세부항목에 대해
현재 52개 Topic Pack의 실제 의미 범위를 기준으로 coverage 수준을 평가한다.

공식 기준과 Topic Pack 분류는 다음 문서를 기준으로 한다.

- `docs/exam_scope/industrial_instrumentation_control_2027_2030_criteria.md`
- `docs/topic_pack_classification.md`

## 2. 판정 원칙

- `COVERED`: 현재 Topic Pack 집합이 해당 공식 criterion의 핵심 범위를 독립 답안 수준으로 실질적으로 설명할 수 있다.
- `PARTIAL`: 관련 Topic은 있으나 공식 criterion의 일부 핵심 범위가 빠져 있거나 다른 Topic의 부수 범위로만 존재한다.
- `GAP`: 현재 Topic Pack 집합에 해당 criterion의 실질적 답안 근거가 없다.
- Topic 개수 또는 PRIMARY Topic 보유 여부만으로 자동 판정하지 않는다.
- PRIMARY와 SECONDARY Topic의 README, Fact, Model evidence를 공식 criterion의 의미 범위와 비교한다.
- 내부 `IC-2027-W-*` ID는 repository 관리용 ID이며 한국산업인력공단의 공식 식별자가 아니다.
- Coverage는 Question Type과 독립된 축이다.

Stage 3B semantic coverage review SHA-256: `59c670736c94f98d57cd8e0fb2c63537112b46cbdd0cfdf723525bfe344dc27f`

## 3. 전체 현황

| 판정 | 수량 | 비율 |
|---|---:|---:|
| COVERED | 16 | 48.5% |
| PARTIAL | 8 | 24.2% |
| GAP | 9 | 27.3% |
| 합계 | 33 | 100.0% |

- HIGH confidence: 30
- MEDIUM confidence: 3

## 4. 공식 세부항목 Coverage Matrix

| ID | 공식 세부항목 | Coverage | Confidence | PRIMARY | SECONDARY |
|---|---|:---:|:---:|---:|---:|
| `IC-2027-W-1-1` | 제어시스템의 전달함수 | **COVERED** | MEDIUM | 1 | 6 |
| `IC-2027-W-1-2` | 제어시스템의 보상요소 | **COVERED** | HIGH | 1 | 4 |
| `IC-2027-W-1-3` | 제어시스템의 응답특성 | **COVERED** | HIGH | 6 | 5 |
| `IC-2027-W-1-4` | 전자기기의 오차 발생요인과 대책 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-2-1` | 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | **PARTIAL** | HIGH | 8 | 3 |
| `IC-2027-W-2-2` | 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | **PARTIAL** | HIGH | 2 | 0 |
| `IC-2027-W-2-3` | 측정 시 오차발생 원인과 대책 | **COVERED** | HIGH | 1 | 10 |
| `IC-2027-W-2-4` | 제어밸브의 작동원리 및 기능 | **COVERED** | HIGH | 5 | 10 |
| `IC-2027-W-2-5` | 구동기(공압, 모터 등)의 작동원리 및 기능 | **COVERED** | HIGH | 2 | 4 |
| `IC-2027-W-2-6` | 계측제어기기의 전원 및 접지방식 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-2-7` | 계측제어기기에 관한 유·무선 통신, 규약 | **COVERED** | HIGH | 1 | 1 |
| `IC-2027-W-2-8` | 계측제어기기 및 시스템 설계 규정 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-3-1` | 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | **PARTIAL** | HIGH | 7 | 3 |
| `IC-2027-W-3-2` | 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소 | **COVERED** | HIGH | 2 | 2 |
| `IC-2027-W-3-3` | 제어기기 및 시스템의 통신방식 | **COVERED** | HIGH | 1 | 2 |
| `IC-2027-W-3-4` | 단일루프 제어 및 다중루프 제어설계 | **PARTIAL** | HIGH | 3 | 3 |
| `IC-2027-W-3-5` | PI, PID 등 제어 및 Parameter 설정 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-3-6` | 제어논리 설계 및 논리도 작성 | **COVERED** | HIGH | 1 | 1 |
| `IC-2027-W-3-7` | 공정제어 계측(P&ID) 설계 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-3-8` | 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | **COVERED** | HIGH | 1 | 4 |
| `IC-2027-W-3-9` | 계측제어시스템의 하드웨어 개발, 생산 및 검증 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-3-10` | 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등) | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-4-1` | 가용도(availability), 신뢰도(reliability) | **COVERED** | HIGH | 0 | 2 |
| `IC-2027-W-4-2` | 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책 | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-4-3` | 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | **COVERED** | HIGH | 2 | 2 |
| `IC-2027-W-4-4` | 프로젝트 관리(원가, 인력, 수행일정 등) | **PARTIAL** | HIGH | 1 | 0 |
| `IC-2027-W-4-5` | 생산관리(원가, 인력, 수행일정 등) | **GAP** | HIGH | 0 | 0 |
| `IC-2027-W-4-6` | 제어시스템의 운영 및 관리 | **PARTIAL** | MEDIUM | 2 | 8 |
| `IC-2027-W-4-7` | 제어기기 및 시스템의 사이버 보안 및 대책 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-4-8` | 제어기기 및 시스템의 수명주기 관리방법 | **COVERED** | HIGH | 1 | 6 |
| `IC-2027-W-4-9` | 계측제어설비 설치 및 기술기준 | **PARTIAL** | HIGH | 0 | 1 |
| `IC-2027-W-5-1` | 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | **PARTIAL** | MEDIUM | 2 | 0 |
| `IC-2027-W-5-2` | 계측제어 관련 동향 | **GAP** | HIGH | 0 | 0 |

## 5. PARTIAL 상세

PARTIAL 항목은 기존 Topic을 폐기하거나 중복 생성하지 않고 잔여범위만 보강해야 한다.

### `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`, `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`, `passive_sensor_resistive_capacitive_inductive_transduction`, `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`, `rtd_temperature_sensor_principle_pt100_wiring_compensation`, `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`, `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`, `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- 관련 SECONDARY Topic: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`, `temperature_measurement_error_heat_transfer`, `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- 판정 근거: RTD, thermistor, thermocouple, LVDT/RVDT, strain/load cell, piezo, DP level, passive transduction 등 다수 센서 원리와 선정 근거가 있다.
- 잔여범위: 공식 예시의 압력·습도·속도 등 주요 측정량을 독립적으로 포괄하지 못한다. 특히 일반 압력계측, 습도, 속도/회전 계측 범위가 비어 있다.

### `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`, `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- 관련 SECONDARY Topic: 없음
- 판정 근거: Ultrasonic TOF와 Radar FMCW/Pulse의 비접촉 거리·레벨 측정원리와 보상·오차는 직접 다룬다.
- 잔여범위: 공식 예시의 광학식 비접촉 측정과 광센서/레이저 기반 원리·알고리즘이 없다.

### `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: `control_valve_authority_rangeability_gain_installed_performance`, `control_valve_cavitation_flashing_choked_flow_damage_prevention`, `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`, `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`, `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`, `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`, `control_valve_sizing_cv_kv_reynolds_liquid_selection`
- 관련 SECONDARY Topic: `balanced_trim_unbalanced_trim_structure_sealing_applications`, `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`, `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- 판정 근거: Cv/Kv, gas/liquid sizing, cavitation/flashing, authority, installed gain, severe service 등 밸브 중심의 유체제어 설계 evidence는 매우 강하다.
- 잔여범위: 공식 항목은 온도·압력·유량·수위 제어의 기본요소와 전체 loop 설계를 요구한다. 현재는 최종제어요소에 편중되어 process dynamics, transmitter-controller-valve loop 및 각 변수별 제어전략이 부족하다.

### `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: `lqr_optimal_state_feedback_riccati_weighting_design`, `state_feedback_reference_tracking_prefilter_integral_action`, `state_space_controllability_observability_pole_placement`
- 관련 SECONDARY Topic: `control_valve_authority_rangeability_gain_installed_performance`, `feedback_system_closed_loop_sensitivity_steady_state_error`, `pid_controller_tuning_sequence_gain_effects`
- 판정 근거: 상태공간, 상태피드백, LQR과 일반 feedback/PID evidence는 풍부하다.
- 잔여범위: 공정제어에서 말하는 single-loop와 cascade, ratio, feedforward, override/selective, split-range 같은 전형적 다중루프 제어구조의 설계 Topic이 없다.

### `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등)

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- 관련 SECONDARY Topic: 없음
- 판정 근거: 제어 SW 프로젝트 Topic이 scope, schedule, cost, feasibility, URS/FRS/FDS/SDS, FAT/SAT, commissioning, acceptance를 다룬다.
- 잔여범위: 공식 세부범위의 자동화 기본계획, 현장계기 선정, 공사 설계도서, 운전조작서, 제작공정·생산계획, 제조원가까지는 포괄하지 못한다.

### `IC-2027-W-4-6` 제어시스템의 운영 및 관리

- 판정: **PARTIAL** (MEDIUM)
- 관련 PRIMARY Topic: `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`, `smart_positioner_diagnostics_valve_signature_predictive_maintenance`
- 관련 SECONDARY Topic: `configuration_change_release_backup_rollback_migration_obsolescence_management`, `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`, `control_valve_positioner_ip_converter_booster_accessories_calibration`, `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`, `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`, `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`, `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`, `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability`
- 판정 근거: Alarm/HMI/SOE 운전정보, valve diagnostics/predictive maintenance, configuration·backup·migration, network/system resilience 등 운영 evidence는 넓다.
- 잔여범위: 공식 범위의 일반적인 자동제어시스템 유지정비·운영 체계, 예방/예지/고장정비 전략, calibration/inspection 계획, spare·work order·maintenance KPI가 하나의 전용 Topic으로 통합되어 있지 않다.

### `IC-2027-W-4-9` 계측제어설비 설치 및 기술기준

- 판정: **PARTIAL** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- 판정 근거: FAT/SAT, loop test, site integration, commissioning, performance test, acceptance, as-built/handover evidence는 존재한다.
- 잔여범위: 설치 자체의 배선·배관·접지·시공검사와 적용 기술기준/code, 설치 품질관리 범위는 다루지 않는다.

### `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등)

- 판정: **PARTIAL** (MEDIUM)
- 관련 PRIMARY Topic: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`, `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- 관련 SECONDARY Topic: 없음
- 판정 근거: 산업 AI/ML, 예지보전, Physical AI, robot, sensor fusion, digital twin, autonomous manufacturing와 safety control은 깊게 다룬다.
- 잔여범위: 공식 예시의 IoT와 스마트팩토리 전체 architecture는 부분적으로만 연결되고 양자컴퓨팅 등 기타 신기술 축은 없다. 신기술 항목 특성상 지속 확장도 필요하다.

## 6. GAP 상세

GAP 항목은 현재 52개 Topic Pack으로 독립 답안 수준의 실질 coverage를 확보하지 못한 영역이다.

### `IC-2027-W-1-4` 전자기기의 오차 발생요인과 대책

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 현재 52개 Topic 중 이 공식 항목에 연결된 PRIMARY/SECONDARY Topic이 없고 전자기기 자체의 오차 발생원인·대책을 독립적으로 다루는 evidence가 없다.
- 신규/보강 필요범위: 전자회로·전자기기 오차원인, 온도·노화·전원·노이즈·부품공차와 대책을 다루는 신규 Topic이 필요하다.

### `IC-2027-W-2-6` 계측제어기기의 전원 및 접지방식

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 계측제어기기 전원 또는 접지방식을 직접 소유하거나 보조하는 Topic이 없다.
- 신규/보강 필요범위: AC/DC 전원계통, UPS/DC system, grounding/bonding, signal ground, shield, ground loop, EMC 관점의 신규 Topic이 필요하다.

### `IC-2027-W-2-8` 계측제어기기 및 시스템 설계 규정

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 제어설계 규정 검토와 기준서 작성 자체를 다루는 Topic이 없다.
- 신규/보강 필요범위: 설계기준, applicable code/standard hierarchy, design basis, specification 작성·검토·deviation 관리 Topic이 필요하다.

### `IC-2027-W-3-7` 공정제어 계측(P&ID) 설계

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: P&ID 작성, 계기기호, tag, loop number, line/interface, control narrative 연계 등을 직접 다루는 Topic이 없다.
- 신규/보강 필요범위: P&ID 및 공정배관계장도 작성·검토 전용 Topic이 필요하다.

### `IC-2027-W-3-9` 계측제어시스템의 하드웨어 개발, 생산 및 검증

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 제어반·전자응용기기·로봇 하드웨어의 개발, 생산, 시험·검증 프로세스를 직접 다루는 Topic이 없다.
- 신규/보강 필요범위: 하드웨어 architecture, component selection, panel design, prototype, production test, verification/validation을 묶는 신규 Topic이 필요하다.

### `IC-2027-W-3-10` 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등)

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 온도·습도·EMI/EMC 등 환경 검증시험의 시험조건, 규격, acceptance와 대책을 다루는 Topic이 없다.
- 신규/보강 필요범위: 환경시험 및 EMC/EMI 내성·방출, 온습도·진동 등 qualification Topic이 필요하다.

### `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 위험장소·산업별 hazardous environment에서 고려해야 할 제어요소와 보호방식을 직접 다루는 Topic이 없다.
- 신규/보강 필요범위: 방폭/본질안전, hazardous area classification, environmental/process hazard에 따른 계측·제어기기 선정과 대책 Topic이 필요하다.

### `IC-2027-W-4-5` 생산관리(원가, 인력, 수행일정 등)

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 생산관리의 원가·인력·일정, 생산계획·공정관리 등을 독립적으로 다루는 Topic이 없다.
- 신규/보강 필요범위: 계측제어기기/시스템 제조 관점의 생산계획·공정·품질·원가·자원관리 Topic이 필요하다.

### `IC-2027-W-5-2` 계측제어 관련 동향

- 판정: **GAP** (HIGH)
- 관련 PRIMARY Topic: 없음
- 관련 SECONDARY Topic: 없음
- 판정 근거: 계측제어 관련 최신 동향, 관련 법령·기술기준 변화 자체를 정기적으로 다루는 Topic이 없다.
- 신규/보강 필요범위: 동향/법령/표준 업데이트를 독립적으로 관리하는 Topic 또는 주기적 review 체계가 필요하다.

## 7. COVERED 해석상 주의점

- `IC-2027-W-4-1` 가용도·신뢰도는 PRIMARY Topic이 없지만,
  PLC/DCS/SCADA architecture와 industrial network resilience의 실제 evidence가
  MTBF, MTTR, availability, redundancy, SPOF, common-cause failure를 충분히 다루므로 COVERED로 판정한다.
- PRIMARY Topic 수가 0이라는 사실만으로 GAP을 의미하지 않는다.
- 반대로 관련 Topic이 존재해도 공식 criterion의 핵심 범위를 다루지 못하면 PARTIAL이다.

## 8. Source 정합성 별도 이슈

- `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`의
  model evidence에는 열전대와 RTD 내용이 혼재하는 정합성 이슈가 확인되어 있다.
- 이 문제는 `IC-2027-W-2-1`의 PARTIAL 판정 원인이 아니다.
- Topic source repair는 coverage 분류 작업과 분리하여 별도 수행한다.

## 9. 다음 단계 경계

이 문서는 coverage 현황을 고정하는 문서다.
신규 Topic Pack의 실제 우선순위는 아직 결정하지 않는다.

다음 단계에서는 GAP 9개와 PARTIAL 8개를 대상으로 다음 요소를 함께 평가한다.

- 공식 출제범위 직접성
- 과거 기출 빈도
- 시험 변별력과 준비 중요도
- 기존 Topic Pack과의 중복도
- 하나의 신규 Topic으로 여러 잔여범위를 함께 보완할 수 있는지 여부

Question Type 변경은 이 coverage 작업에서 수행하지 않는다.
