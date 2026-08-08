# Topic Pack 공식 출제기준 분류

## 1. 목적

이 문서는 현재 52개 Topic Pack을 산업계측제어기술사
2027.01.01~2030.12.31 필기 공식 출제기준의 33개 세부항목에 매핑한다.

공식 출제기준은 `docs/exam_scope/industrial_instrumentation_control_2027_2030_criteria.md`를
단일 기준으로 사용한다.

이 문서는 분류 관계만 정의한다. 출제기준별 coverage 수준은 아직 판정하지 않는다.

## 2. 분류 계약

- 각 Topic Pack은 정확히 하나의 `PRIMARY` 공식 세부항목을 가진다.
- `SECONDARY`는 해당 Topic이 실질적으로 함께 다루는 공식 세부항목이며 0개 이상일 수 있다.
- `PRIMARY`는 Topic의 핵심 출제의도와 직접 지식소유 범위를 기준으로 결정한다.
- `SECONDARY`는 단순 키워드 중복이 아니라 Topic 내용이 실제 답안 근거를 제공할 때만 부여한다.
- `HIGH`는 공식 세부항목과 Topic 범위가 직접 대응하는 경우다.
- `MEDIUM`은 공식 기준이 넓거나 Topic이 여러 공식 항목의 경계에 놓여 추가 검토가 필요한 경우다.
- 내부 `IC-2027-W-*` ID는 관리용 ID이며 한국산업인력공단의 공식 식별자가 아니다.
- 이 분류는 Question Type과 독립된 축이다.

Stage 2B-2 semantic mapping review SHA-256: `b61c51218f66c520eef4c6949fe62dfab960cfab783cca52274b4d1cccac9017`

## 3. 분류 현황

| 항목 | 수량 |
|---|---:|
| Topic Pack | 52 |
| 공식 세부항목 | 33 |
| HIGH confidence | 40 |
| MEDIUM confidence | 12 |
| PRIMARY owner가 있는 공식 세부항목 | 22 |
| PRIMARY owner가 없는 공식 세부항목 | 11 |

PRIMARY owner가 없다는 사실만으로 coverage 부족을 의미하지 않는다.
SECONDARY 관계와 Topic의 실제 내용까지 역집계한 뒤 별도 단계에서 coverage를 판정한다.

## 4. Topic Pack별 공식 기준 매핑

| # | Topic Pack | PRIMARY | SECONDARY | Confidence | 근거 |
|---:|---|---|---|:---:|---|
| 1 | `balanced_trim_unbalanced_trim_structure_sealing_applications` | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | HIGH | Balanced/Unbalanced trim의 압력경계·유효면적·밀봉 구조는 제어밸브의 작동원리·기능이 중심이다. |
| 2 | `bode_frequency_response_stability_margin_bandwidth` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-2` 제어시스템의 보상요소 | HIGH | Bode 주파수응답, 안정여유, 대역폭이 중심이고 lead/lag/PID 보상기 설계는 보조 범위다. |
| 3 | `configuration_change_release_backup_rollback_migration_obsolescence_management` | `IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | `IC-2027-W-4-6` 제어시스템의 운영 및 관리<br>`IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | HIGH | 운영 단계의 형상·변경·Release·Backup·Migration·Obsolescence를 수명주기 관리로 직접 다룬다. |
| 4 | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `IC-2027-W-3-6` 제어논리 설계 및 논리도 작성 | `IC-2027-W-4-3` 안전, 방재 등 재난대비 목적의 계측제어시스템 설계<br>`IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | HIGH | Sequence·Interlock·Permissive·Trip·상태전이·Cause & Effect가 제어논리 설계의 직접 범위다. |
| 5 | `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등) | `IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증<br>`IC-2027-W-4-9` 계측제어설비 설치 및 기술기준 | MEDIUM | Scope·Schedule·Cost·문서·FAT/SAT·인수의 프로젝트 실행 흐름이 중심이며 SW 검증과 설치/시운전은 보조다. |
| 6 | `control_valve_authority_rangeability_gain_installed_performance` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | HIGH | Valve authority·installed gain·rangeability는 공정 유체계와 밸브의 압력강하 재분배를 포함한 유체제어 설계 주제다. |
| 7 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | HIGH | 액체 압력분포·Pvc·증기압·초크·캐비테이션/플래싱을 유체제어 설계 관점에서 다룬다. |
| 8 | `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | HIGH | 고유/설치 유량특성과 Linear·Equal Percentage·Quick Opening은 제어밸브의 고유 기능과 동작특성이 중심이다. |
| 9 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능<br>`IC-2027-W-4-6` 제어시스템의 운영 및 관리 | MEDIUM | Deadband·stiction·응답시간의 최종제어요소 동특성이 중심이고 positioner/actuator 및 진단·운영은 보조다. |
| 10 | `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | HIGH | 불평형력·마찰력에 필요한 actuator thrust/torque와 fail-safe 선정이 핵심 설계 결과다. |
| 11 | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | HIGH | 압축성 유체의 유량·압력비·초크 조건과 Cv 산정은 유체제어 설계가 중심이다. |
| 12 | `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | HIGH | 공력·수력 소음의 유동 메커니즘과 저소음 trim 설계가 유체제어 설계 범위에 직접 해당한다. |
| 13 | `control_valve_positioner_ip_converter_booster_accessories_calibration` | `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-4-6` 제어시스템의 운영 및 관리 | MEDIUM | Positioner·I/P·booster가 actuator 구동계의 command-to-travel chain을 구성하며 교정·운영은 보조다. |
| 14 | `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | HIGH | Seat leakage·shutoff·packing·sealing은 제어밸브 trim/밀봉 기능이 중심이다. |
| 15 | `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | MEDIUM | 공정 P/T/Q/유체조건을 기반으로 valve package를 선정하는 통합 유체제어 설계가 중심이며 lifecycle은 보조다. |
| 16 | `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-4-6` 제어시스템의 운영 및 관리 | HIGH | 고·저유량, 온도, 입자·slurry에 따른 valve geometry/material 대책은 가혹 유체제어 설계가 중심이다. |
| 17 | `control_valve_sizing_cv_kv_reynolds_liquid_selection` | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | HIGH | Cv·Kv, Reynolds 보정, 운전점별 required coefficient와 sizing은 유체제어 설계의 직접 범위다. |
| 18 | `control_valve_types_globe_rotary_body_actuator_selection` | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능 | MEDIUM | Globe/rotary body·trim 형식 비교가 주축이고 actuator 종류와 matching을 함께 다룬다. |
| 19 | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | 차압식 레벨 측정원리·선정과 밀도/설치/도압관 오차를 함께 다룬다. |
| 20 | `feedback_system_closed_loop_sensitivity_steady_state_error` | `IC-2027-W-1-1` 제어시스템의 전달함수 | `IC-2027-W-1-3` 제어시스템의 응답특성<br>`IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | MEDIUM | 폐루프 전달함수·특성방정식·S/T가 기본 구조이며 정상상태 오차와 loop 설계가 이어진다. |
| 21 | `final_control_element_sil_sis_esd_valve_partial_stroke_test` | `IC-2027-W-4-3` 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능<br>`IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | HIGH | SIF final element·safe state·PFD/PFH·proof test는 안전 목적 계측제어시스템 설계가 중심이다. |
| 22 | `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소 | `IC-2027-W-3-3` 제어기기 및 시스템의 통신방식<br>`IC-2027-W-4-6` 제어시스템의 운영 및 관리 | MEDIUM | Historian·MES·ERP·Edge/Gateway의 IT/OT 계층 통합 구조가 제어시스템 설계요소에 가장 가깝다. |
| 23 | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소<br>`IC-2027-W-3-6` 제어논리 설계 및 논리도 작성 | MEDIUM | Alarm·SOE·setpoint·operator authority를 운전정보 관리로 다루므로 운영·관리가 중심이다. |
| 24 | `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | `IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | HIGH | 산업 AI/ML·이상탐지·예지보전은 공식 신기술 항목에 직접 해당하며 model lifecycle은 보조다. |
| 25 | `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `IC-2027-W-3-3` 제어기기 및 시스템의 통신방식 | `IC-2027-W-4-1` 가용도(availability), 신뢰도(reliability)<br>`IC-2027-W-2-7` 계측제어기기에 관한 유·무선 통신, 규약 | HIGH | Latency·jitter·determinism·PTP·redundancy를 시스템 통신방식의 실시간 성능 관점에서 다룬다. |
| 26 | `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `IC-2027-W-2-7` 계측제어기기에 관한 유·무선 통신, 규약 | `IC-2027-W-3-3` 제어기기 및 시스템의 통신방식 | HIGH | 유·무선, Fieldbus, Ethernet, protocol/profile과 상호운용성 선정은 계측제어기기 통신·규약에 직접 해당한다. |
| 27 | `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | `IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | `IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | HIGH | 요구사항부터 구현·V&V·RTM·HIL·회귀시험까지 제어 SW 개발·검증 자체를 다룬다. |
| 28 | `lead_lag_compensator_phase_margin_steady_state_error` | `IC-2027-W-1-2` 제어시스템의 보상요소 | `IC-2027-W-1-3` 제어시스템의 응답특성 | HIGH | Lead/Lag 전달함수와 위상·이득 보상 설계는 제어시스템 보상요소에 직접 해당한다. |
| 29 | `lqr_optimal_state_feedback_riccati_weighting_design` | `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | `IC-2027-W-1-2` 제어시스템의 보상요소<br>`IC-2027-W-1-3` 제어시스템의 응답특성 | MEDIUM | LQR은 상태피드백 제어기 설계 주제이며 공식 고전 보상요소보다 제어설계 항목에 우선 배치했다. |
| 30 | `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | LVDT/RVDT의 변위·각도 측정원리와 센서 선정·오차가 중심이다. |
| 31 | `nyquist_stability_criterion_gain_phase_margin` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-1` 제어시스템의 전달함수 | HIGH | Nyquist 안정판별과 GM/PM은 제어시스템 안정·주파수 응답특성 분석이 중심이다. |
| 32 | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | `IC-2027-W-4-7` 제어기기 및 시스템의 사이버 보안 및 대책 | `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | HIGH | OT cyber threat·segmentation·allowlisting·supply chain·incident response가 공식 사이버보안 항목과 직접 일치한다. |
| 33 | `passive_sensor_resistive_capacitive_inductive_transduction` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | 저항·정전용량·인덕턴스형 센서의 변환원리와 선정·교정 특성이 중심이다. |
| 34 | `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소<br>`IC-2027-W-4-3` 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | HIGH | Physical AI·robot·sensor fusion·digital twin·자율제조는 공식 신기술 예시와 직접 대응한다. |
| 35 | `pid_controller_tuning_sequence_gain_effects` | `IC-2027-W-3-5` PI, PID 등 제어 및 Parameter 설정 | `IC-2027-W-1-3` 제어시스템의 응답특성<br>`IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | HIGH | P/I/D 동작과 parameter tuning 순서·게인 영향이 공식 PI/PID parameter 설정 항목에 직접 해당한다. |
| 36 | `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | 압전 센서·전하증폭기·힘/압력/가속도 측정원리와 적용·오차가 중심이다. |
| 37 | `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소 | `IC-2027-W-4-1` 가용도(availability), 신뢰도(reliability)<br>`IC-2027-W-4-6` 제어시스템의 운영 및 관리 | HIGH | PLC·DCS·SCADA·PC·Remote I/O 구조와 redundancy 설계가 공식 제어시스템 설계요소에 직접 해당한다. |
| 38 | `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준<br>`IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | Radar FMCW/pulse 비접촉 거리·레벨 측정원리와 false echo·설치오차가 중심이다. |
| 39 | `root_locus_stability_gain_design` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-1` 제어시스템의 전달함수 | HIGH | 이득 변화에 따른 폐루프 극점·안정성·과도응답 해석이 응답특성의 중심이다. |
| 40 | `routh_hurwitz_stability_criterion_gain_range` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-1` 제어시스템의 전달함수 | HIGH | 특성방정식으로 안정성·이득범위를 판정하므로 제어시스템 응답/안정 특성이 중심이다. |
| 41 | `rtd_temperature_sensor_principle_pt100_wiring_compensation` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | RTD/Pt100의 측정원리·배선보상·선정·오차가 센서/계측기 범위에 직접 해당한다. |
| 42 | `second_order_lag_response_by_damping_ratio` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-1` 제어시스템의 전달함수 | HIGH | 감쇠비와 극점 위치·과도응답의 관계를 직접 다루는 전형적인 응답특성 주제다. |
| 43 | `second_order_system_resonance_frequency_response` | `IC-2027-W-1-3` 제어시스템의 응답특성 | `IC-2027-W-1-1` 제어시스템의 전달함수 | HIGH | 2차계 주파수응답·공진주파수·bandwidth가 제어시스템 응답특성에 직접 해당한다. |
| 44 | `sis_sil_safety_software_independence_systematic_failure_verification_validation` | `IC-2027-W-4-3` 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | `IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증<br>`IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | HIGH | SIS/SIF/SIL·안전 SW 독립성·systematic failure·V&V를 안전 목적 시스템 설계로 통합한다. |
| 45 | `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능<br>`IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능<br>`IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | HIGH | Online/offline 진단·valve signature·예지보전은 제어시스템 운영·유지관리 목적이 중심이다. |
| 46 | `state_feedback_reference_tracking_prefilter_integral_action` | `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | `IC-2027-W-1-2` 제어시스템의 보상요소<br>`IC-2027-W-1-3` 제어시스템의 응답특성 | MEDIUM | 상태피드백 기준추종·prefilter·적분상태 확대는 feedback 제어설계가 중심이며 보상/응답 이론이 보조다. |
| 47 | `state_space_controllability_observability_pole_placement` | `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | `IC-2027-W-1-1` 제어시스템의 전달함수<br>`IC-2027-W-1-2` 제어시스템의 보상요소 | MEDIUM | 상태공간·가제어/가관측·상태피드백 극점배치는 현대 제어설계에 가장 가깝다. |
| 48 | `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | Strain gauge/load cell의 변환원리·bridge·보상·오차사슬은 센서·계측기 항목이 중심이다. |
| 49 | `temperature_measurement_error_heat_transfer` | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | HIGH | 전도·대류·복사·담금깊이 등 측정오차 원인과 저감대책이 Topic의 직접 출제의도다. |
| 50 | `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | NTC/PTC 온도센서의 저항-온도 특성·측정회로·선형화·오차가 중심이다. |
| 51 | `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | MEDIUM | README·Fact·Model evidence가 Seebeck·기준접점·CJC·보상도선의 열전대 원리를 일관되게 지지한다. 2026-08-08 source repair와 generated semantic/idempotence audit에서 RTD positive ownership contamination 0건을 확인했으며, RTD 관련 문자열은 rejected/low-score 경계 표현으로만 유지한다. |
| 52 | `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준<br>`IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | HIGH | 초음파 TOF 비접촉 거리·레벨 측정과 온도보상·반사/설치오차가 공식 비접촉 측정 항목에 직접 해당한다. |

## 5. 공식 세부항목별 ownership index

이 표는 분류 관계의 역색인이다. 아직 coverage 판정표가 아니다.

| 공식 세부항목 | PRIMARY Topic | SECONDARY Topic |
|---|---|---|
| `IC-2027-W-1-1` 제어시스템의 전달함수 | `feedback_system_closed_loop_sensitivity_steady_state_error` | `nyquist_stability_criterion_gain_phase_margin`<br>`root_locus_stability_gain_design`<br>`routh_hurwitz_stability_criterion_gain_range`<br>`second_order_lag_response_by_damping_ratio`<br>`second_order_system_resonance_frequency_response`<br>`state_space_controllability_observability_pole_placement` |
| `IC-2027-W-1-2` 제어시스템의 보상요소 | `lead_lag_compensator_phase_margin_steady_state_error` | `bode_frequency_response_stability_margin_bandwidth`<br>`lqr_optimal_state_feedback_riccati_weighting_design`<br>`state_feedback_reference_tracking_prefilter_integral_action`<br>`state_space_controllability_observability_pole_placement` |
| `IC-2027-W-1-3` 제어시스템의 응답특성 | `bode_frequency_response_stability_margin_bandwidth`<br>`nyquist_stability_criterion_gain_phase_margin`<br>`root_locus_stability_gain_design`<br>`routh_hurwitz_stability_criterion_gain_range`<br>`second_order_lag_response_by_damping_ratio`<br>`second_order_system_resonance_frequency_response` | `feedback_system_closed_loop_sensitivity_steady_state_error`<br>`lead_lag_compensator_phase_margin_steady_state_error`<br>`lqr_optimal_state_feedback_riccati_weighting_design`<br>`pid_controller_tuning_sequence_gain_effects`<br>`state_feedback_reference_tracking_prefilter_integral_action` |
| `IC-2027-W-1-4` 전자기기의 오차 발생요인과 대책 | — | — |
| `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`<br>`lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`<br>`passive_sensor_resistive_capacitive_inductive_transduction`<br>`piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`<br>`rtd_temperature_sensor_principle_pt100_wiring_compensation`<br>`strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`<br>`thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`<br>`thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`<br>`temperature_measurement_error_heat_transfer`<br>`ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` |
| `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`<br>`ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | — |
| `IC-2027-W-2-3` 측정 시 오차발생 원인과 대책 | `temperature_measurement_error_heat_transfer` | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`<br>`lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`<br>`passive_sensor_resistive_capacitive_inductive_transduction`<br>`piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`<br>`radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`<br>`rtd_temperature_sensor_principle_pt100_wiring_compensation`<br>`strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`<br>`thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`<br>`thermocouple_temperature_sensor_seebeck_reference_junction_compensation`<br>`ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` |
| `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능 | `balanced_trim_unbalanced_trim_structure_sealing_applications`<br>`control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`<br>`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`<br>`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`<br>`control_valve_types_globe_rotary_body_actuator_selection` | `control_valve_authority_rangeability_gain_installed_performance`<br>`control_valve_cavitation_flashing_choked_flow_damage_prevention`<br>`control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`<br>`control_valve_gas_sizing_choked_flow_critical_pressure_ratio`<br>`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`<br>`control_valve_positioner_ip_converter_booster_accessories_calibration`<br>`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`<br>`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`<br>`control_valve_sizing_cv_kv_reynolds_liquid_selection`<br>`smart_positioner_diagnostics_valve_signature_predictive_maintenance` |
| `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능 | `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`<br>`control_valve_positioner_ip_converter_booster_accessories_calibration` | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`<br>`control_valve_types_globe_rotary_body_actuator_selection`<br>`final_control_element_sil_sis_esd_valve_partial_stroke_test`<br>`smart_positioner_diagnostics_valve_signature_predictive_maintenance` |
| `IC-2027-W-2-6` 계측제어기기의 전원 및 접지방식 | — | — |
| `IC-2027-W-2-7` 계측제어기기에 관한 유·무선 통신, 규약 | `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` |
| `IC-2027-W-2-8` 계측제어기기 및 시스템 설계 규정 | — | — |
| `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | `control_valve_authority_rangeability_gain_installed_performance`<br>`control_valve_cavitation_flashing_choked_flow_damage_prevention`<br>`control_valve_gas_sizing_choked_flow_critical_pressure_ratio`<br>`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`<br>`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`<br>`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`<br>`control_valve_sizing_cv_kv_reynolds_liquid_selection` | `balanced_trim_unbalanced_trim_structure_sealing_applications`<br>`control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`<br>`control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` |
| `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소 | `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`<br>`plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`<br>`physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` |
| `IC-2027-W-3-3` 제어기기 및 시스템의 통신방식 | `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`<br>`industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` |
| `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | `lqr_optimal_state_feedback_riccati_weighting_design`<br>`state_feedback_reference_tracking_prefilter_integral_action`<br>`state_space_controllability_observability_pole_placement` | `control_valve_authority_rangeability_gain_installed_performance`<br>`feedback_system_closed_loop_sensitivity_steady_state_error`<br>`pid_controller_tuning_sequence_gain_effects` |
| `IC-2027-W-3-5` PI, PID 등 제어 및 Parameter 설정 | `pid_controller_tuning_sequence_gain_effects` | — |
| `IC-2027-W-3-6` 제어논리 설계 및 논리도 작성 | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` |
| `IC-2027-W-3-7` 공정제어 계측(P&ID) 설계 | — | — |
| `IC-2027-W-3-8` 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | `configuration_change_release_backup_rollback_migration_obsolescence_management`<br>`control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`<br>`control_software_project_engineering_documents_fat_sat_commissioning_acceptance`<br>`sis_sil_safety_software_independence_systematic_failure_verification_validation` |
| `IC-2027-W-3-9` 계측제어시스템의 하드웨어 개발, 생산 및 검증 | — | — |
| `IC-2027-W-3-10` 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등) | — | — |
| `IC-2027-W-4-1` 가용도(availability), 신뢰도(reliability) | — | `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`<br>`plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` |
| `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책 | — | — |
| `IC-2027-W-4-3` 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | `final_control_element_sil_sis_esd_valve_partial_stroke_test`<br>`sis_sil_safety_software_independence_systematic_failure_verification_validation` | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`<br>`physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` |
| `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등) | `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | — |
| `IC-2027-W-4-5` 생산관리(원가, 인력, 수행일정 등) | — | — |
| `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`<br>`smart_positioner_diagnostics_valve_signature_predictive_maintenance` | `configuration_change_release_backup_rollback_migration_obsolescence_management`<br>`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`<br>`control_valve_positioner_ip_converter_booster_accessories_calibration`<br>`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`<br>`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`<br>`historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`<br>`ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`<br>`plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` |
| `IC-2027-W-4-7` 제어기기 및 시스템의 사이버 보안 및 대책 | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | — |
| `IC-2027-W-4-8` 제어기기 및 시스템의 수명주기 관리방법 | `configuration_change_release_backup_rollback_migration_obsolescence_management` | `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`<br>`final_control_element_sil_sis_esd_valve_partial_stroke_test`<br>`industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`<br>`instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`<br>`sis_sil_safety_software_independence_systematic_failure_verification_validation`<br>`smart_positioner_diagnostics_valve_signature_predictive_maintenance` |
| `IC-2027-W-4-9` 계측제어설비 설치 및 기술기준 | — | `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` |
| `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle`<br>`physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | — |
| `IC-2027-W-5-2` 계측제어 관련 동향 | — | — |

## 6. 경계 검토가 필요한 MEDIUM confidence Topic

### `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`

- PRIMARY: `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등)
- SECONDARY: `IC-2027-W-3-8`, `IC-2027-W-4-9`
- 판단 근거: Scope·Schedule·Cost·문서·FAT/SAT·인수의 프로젝트 실행 흐름이 중심이며 SW 검증과 설치/시운전은 보조다.

### `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`

- PRIMARY: `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능
- SECONDARY: `IC-2027-W-2-5`, `IC-2027-W-4-6`
- 판단 근거: Deadband·stiction·응답시간의 최종제어요소 동특성이 중심이고 positioner/actuator 및 진단·운영은 보조다.

### `control_valve_positioner_ip_converter_booster_accessories_calibration`

- PRIMARY: `IC-2027-W-2-5` 구동기(공압, 모터 등)의 작동원리 및 기능
- SECONDARY: `IC-2027-W-2-4`, `IC-2027-W-4-6`
- 판단 근거: Positioner·I/P·booster가 actuator 구동계의 command-to-travel chain을 구성하며 교정·운영은 보조다.

### `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

- PRIMARY: `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소
- SECONDARY: `IC-2027-W-2-4`, `IC-2027-W-4-8`
- 판단 근거: 공정 P/T/Q/유체조건을 기반으로 valve package를 선정하는 통합 유체제어 설계가 중심이며 lifecycle은 보조다.

### `control_valve_types_globe_rotary_body_actuator_selection`

- PRIMARY: `IC-2027-W-2-4` 제어밸브의 작동원리 및 기능
- SECONDARY: `IC-2027-W-2-5`
- 판단 근거: Globe/rotary body·trim 형식 비교가 주축이고 actuator 종류와 matching을 함께 다룬다.

### `feedback_system_closed_loop_sensitivity_steady_state_error`

- PRIMARY: `IC-2027-W-1-1` 제어시스템의 전달함수
- SECONDARY: `IC-2027-W-1-3`, `IC-2027-W-3-4`
- 판단 근거: 폐루프 전달함수·특성방정식·S/T가 기본 구조이며 정상상태 오차와 loop 설계가 이어진다.

### `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`

- PRIMARY: `IC-2027-W-3-2` 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소
- SECONDARY: `IC-2027-W-3-3`, `IC-2027-W-4-6`
- 판단 근거: Historian·MES·ERP·Edge/Gateway의 IT/OT 계층 통합 구조가 제어시스템 설계요소에 가장 가깝다.

### `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`

- PRIMARY: `IC-2027-W-4-6` 제어시스템의 운영 및 관리
- SECONDARY: `IC-2027-W-3-2`, `IC-2027-W-3-6`
- 판단 근거: Alarm·SOE·setpoint·operator authority를 운전정보 관리로 다루므로 운영·관리가 중심이다.

### `lqr_optimal_state_feedback_riccati_weighting_design`

- PRIMARY: `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계
- SECONDARY: `IC-2027-W-1-2`, `IC-2027-W-1-3`
- 판단 근거: LQR은 상태피드백 제어기 설계 주제이며 공식 고전 보상요소보다 제어설계 항목에 우선 배치했다.

### `state_feedback_reference_tracking_prefilter_integral_action`

- PRIMARY: `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계
- SECONDARY: `IC-2027-W-1-2`, `IC-2027-W-1-3`
- 판단 근거: 상태피드백 기준추종·prefilter·적분상태 확대는 feedback 제어설계가 중심이며 보상/응답 이론이 보조다.

### `state_space_controllability_observability_pole_placement`

- PRIMARY: `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계
- SECONDARY: `IC-2027-W-1-1`, `IC-2027-W-1-2`
- 판단 근거: 상태공간·가제어/가관측·상태피드백 극점배치는 현대 제어설계에 가장 가깝다.

### `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`

- PRIMARY: `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준
- SECONDARY: `IC-2027-W-2-3`
- 판단 근거: README·Fact·Model evidence가 Seebeck·기준접점·CJC·보상도선의 열전대 원리를 일관되게 지지한다. 2026-08-08 source repair와 generated semantic/idempotence audit에서 RTD positive ownership contamination 0건을 확인했으며, RTD 관련 문자열은 rejected/low-score 경계 표현으로만 유지한다.

## 7. PRIMARY owner가 없는 공식 세부항목

다음 항목은 현재 52개 Topic Pack 중 PRIMARY owner가 없는 항목이다.
이 목록은 coverage 부족 판정이 아니다.

- `IC-2027-W-1-4` 전자기기의 오차 발생요인과 대책
- `IC-2027-W-2-6` 계측제어기기의 전원 및 접지방식
- `IC-2027-W-2-8` 계측제어기기 및 시스템 설계 규정
- `IC-2027-W-3-7` 공정제어 계측(P&ID) 설계
- `IC-2027-W-3-9` 계측제어시스템의 하드웨어 개발, 생산 및 검증
- `IC-2027-W-3-10` 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등)
- `IC-2027-W-4-1` 가용도(availability), 신뢰도(reliability)
- `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책
- `IC-2027-W-4-5` 생산관리(원가, 인력, 수행일정 등)
- `IC-2027-W-4-9` 계측제어설비 설치 및 기술기준
- `IC-2027-W-5-2` 계측제어 관련 동향

## 8. Source 정합성 점검 결과

- `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`:
  Stage 2B-1에서 확인된 mixed TC+RTD source anomaly는 2026-08-08 source repair로 해소했다.
  Fact title/safe expressions, Logic display metadata, Model legacy fields, Topic Importance note를 Thermocouple ownership에 맞게 정리했다.
  generated 6개 bank에서 RTD positive ownership contamination 0건과 semantic idempotence를 확인했다.
  `IC-2027-W-2-1` PRIMARY / `IC-2027-W-2-3` SECONDARY 매핑과 기존 MEDIUM mapping confidence는 재분류하지 않는다.

## 9. 변경 경계

이 문서는 다음을 변경하지 않는다.

- 기존 Topic Pack source JSON
- generated rubric bank
- Question Type
- Router 및 채점 Python
- 점수·cap 정책

다음 단계에서는 이 분류 문서를 read-only로 재감사한다.
그 이후에만 commit 여부를 결정한다.
