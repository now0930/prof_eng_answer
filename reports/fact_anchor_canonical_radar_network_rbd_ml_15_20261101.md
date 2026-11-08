# Canonical technical source audit — Radar, Industrial Networks, FTA/RBD, ML and PID (2026-11-01)

Reviewer GPT-6 AI (2026-11-01). Exact original canonical `rubrics/topic_packs/` statements individually read and compared to the cited publisher/official technical materials. Fifteen claims `KEEP_BOUNDED`, subject to the limitations listed. This is claim-level technical review, NOT a blanket approval for deterministic grading; do not copy optional device features as universal law.

PDF provenance: TI slide 8 and NASA p11 were **visually inspected** with PDF screenshot. FieldComm HART original document and Modbus Organization original document were checked from indexed PDF text, **visual screenshot failed (HTTP 403 and 404 respectively)**; original URLs and text section are recorded, and independent visual verification cannot be claimed.

## 1. radar_fmcw_sweep_slope_definition

- Topic / Anchor: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` / `radar_fmcw_linear_frequency_sweep`
- Original claim: FMCW 레이더는 시간에 따라 주파수가 선형적으로 변하는 처프를 연속 송신하며 스윕 기울기는 S=Δf/T_s로 정의할 수 있다.
- Original publisher: Texas Instruments, mmWave Radar for Automotive and Industrial Applications (2017), page 8 visually reviewed
- Source URL: https://www.ti.com/content/dam/videos/external-videos/en-us/2/3816841626001/5675916489001.mp4/subassets/Mmwave_webinar_Dec2017.pdf
- Evidence section: Slide 4 (chirp frequency ramp), Slide 8 (B/Tc)
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Linear chirp slope S=B/Ts; non-linear sweeps require calibrated actual f(t), and repeated sawtooth transmitter is one common implementation.

## 2. radar_fmcw_beat_frequency_to_distance_relation

- Topic / Anchor: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` / `radar_fmcw_beat_frequency_distance`
- Original claim: 정지표면과 이상적인 선형 처프에서 스윕 기울기 S=B/T_s, 비트주파수 f_b=Sτ이며 거리는 D=v_g·f_b/(2S)=v_g·f_b·T_s/(2B)이다. 실제 계기는 스윕 비선형, 신호처리와 기체공간 전파속도 영향을 함께 고려한다.
- Original publisher: Texas Instruments, mmWave Radar for Automotive and Industrial Applications (2017), page 8 visually reviewed
- Source URL: https://www.ti.com/content/dam/videos/external-videos/en-us/2/3816841626001/5675916489001.mp4/subassets/Mmwave_webinar_Dec2017.pdf
- Evidence section: Slide 8: fb=(2R/c)(B/Tc) and td=2R/c
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Stationary target and linear chirp, neglect Doppler: D=v_g f_b/(2S); medium propagation speed, calibration, sweep nonlinearity alter actual range.

## 3. fmcw_range_resolution_accuracy_and_fft_bin_distinction

- Topic / Anchor: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` / `radar_bandwidth_range_resolution`
- Original claim: FMCW의 이상적 거리 분해능은 ΔR≈v_g/(2B)이다. 이는 두 인접 반사면을 분리하는 능력이며 단일 표면의 측정 정확도, 반복성 또는 FFT bin 간격과 동일하지 않다. 정확도는 S/N비, 주파수·위상 추정, 보간, 스윕 선형성, 교정과 설치조건의 영향을 함께 받는다.
- Original publisher: Texas Instruments Radar Academy 2.10 Terminology: Range Resolution
- Source URL: https://dev.ti.com/tirex/explore/content/radar_academy_2_10_00_2/_build/radar_academy_2_10_00_2/source/introduction/terminology.html
- Evidence section: Terminology Range Resolution Δr=c/(2B) and single target IF f=slope 2d/c
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Range resolution separates targets; accuracy/repeatability and FFT bin spacing are not automatically equal to Δr, depend on bandwidth, estimator interpolation, SNR and calibration.

## 4. hart_multidrop_shares_pair_with_digital_values_unique_addresses_and_fixed_loop_current

- Topic / Anchor: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` / `sw07_hart_multidrop`
- Original claim: HART multidrop 구성은 여러 장치의 디지털 통신을 한 쌍에 연결할 수 있지만 loop current 운용방식, 주소, polling, 전원과 사용 목적을 점대점 구성과 구분해야 한다.
- Original publisher: FieldComm Group, HART Communication Application Guide Rev.7.1 (27 September 2013), p42–44 indexed original text; screenshot 403
- Source URL: https://www.fieldcommgroup.org/sites/default/files/imce_files/technology/documents/HART_ApplicationGuide_r7.1.pdf
- Evidence section: HART Multi-drop Networks p42 and Configuring Devices p44
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Multidrop field instruments share wire pair; each configured address, current commonly fixed at 4mA in conventional noncontroller multidrop and data fully digital; exceptional HART field-controller configurations may retain analog outputs.

## 5. modbus_tcp_maps_application_pdu_with_device_specific_registers_and_tcp_sessions

- Topic / Anchor: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` / `sw07_modbus_tcp`
- Original claim: Modbus TCP는 Modbus application data를 TCP/IP 네트워크에서 교환하도록 mapping한 방식이며 IP 설계, unit identifier 사용, connection 관리와 register mapping을 별도로 확인해야 한다.
- Original publisher: Modbus Organization, Modbus Messaging on TCP/IP Implementation Guide v1.0b (24 Oct 2006), §§3.1.2–3.1.3 original indexed text; screenshot 404
- Source URL: https://modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b.pdf
- Evidence section: §3.1.2 PDU/MBAP, §3.1.3 Unit Identifier, §4.2 connections
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Modbus application PDU transported via TCP plus 7-byte MBAP header; unit ID especially gateway routing, register semantics depend on device documentation; link/network security not provided by legacy plain TCP protocol.

## 6. classification_regression_and_forecasting_target_types

- Topic / Anchor: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` / `task_type_selection`
- Original claim: Classification은 범주를, Regression은 연속값을, Forecasting은 미래 시계열을 예측하므로 목표변수와 의사결정 방식에 맞게 문제를 정의해야 한다.
- Original publisher: Google Machine Learning Glossary, classification vs regression and concept drift
- Source URL: https://developers.google.com/machine-learning/glossary
- Evidence section: Classification model predicts classes; regression predicts numerical values; forecasting requires future time
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Distinguish categories vs numeric targets and future-time prediction; forecasting can use regression models, so these tasks are not logically disjoint algorithm classes.

## 7. input_distribution_shift_and_concept_shift_are_distinct_under_stated_taxonomy

- Topic / Anchor: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` / `drift_types`
- Original claim: Data Drift는 입력분포 변화, Concept Drift는 입력과 Target 관계 변화이며 운전모드·제품·Sensor·정비정책 변화와 구분해 진단한다.
- Original publisher: Google Machine Learning Glossary, classification vs regression and concept drift
- Source URL: https://developers.google.com/machine-learning/glossary
- Evidence section: Glossary concept drift and nonstationarity entries
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: P(X) change versus P(Y|X) change under stated taxonomy; actual manufacturing faults can mix shifts. Google source directly defines concept drift, generic covariate shift derived by conditional probability.

## 8. time_series_and_group_aware_validation_splits

- Topic / Anchor: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` / `chronological_group_split`
- Original claim: 산업 시계열은 시간순 분할과 설비·Batch·제품 단위 Group 분할을 적용하여 동일 Episode와 미래정보가 Train과 Test에 섞이지 않게 해야 한다.
- Original publisher: scikit-learn 1.9.1 TimeSeriesSplit documentation, Description
- Source URL: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- Evidence section: TimeSeriesSplit Description + scikit-learn GroupKFold (separate official page)
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Temporal splits avoid training on future; groups avoid reusing same equipment/batch/event across train/test. Combine both only when data/experiment require both and enforce correct fold chronology and group boundaries.

## 9. rbd_represents_system_success_logic_through_functional_paths

- Topic / Anchor: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_rbd_success_path`
- Original claim: RBD는 시스템이 성공하기 위한 기능경로를 직렬·병렬 블록으로 표현하는 성공논리 모델이다.
- Original publisher: ReliaSoft, Basics: System Reliability Analysis, RBD and series/parallel
- Source URL: https://help.reliasoft.com/articles/content/basics/system_reliability.htm
- Evidence section: RBD graphical representation, system success/failure based on blocks
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: RBD shows success paths, not necessarily physical wiring. Reliability formula requires dependence assumptions/mission time.

## 10. series_and_parallel_rbd_paths_encode_different_success_conditions

- Topic / Anchor: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_rbd_series_parallel`
- Original claim: 직렬 성공경로는 구성요소 하나의 실패가 기능실패로 이어지며, 병렬 성공경로는 요구된 성공조건을 만족하는 대체경로를 가진다.
- Original publisher: ReliaSoft, Basics: System Reliability Analysis, RBD and series/parallel
- Source URL: https://help.reliasoft.com/articles/content/basics/system_reliability.htm
- Evidence section: Series / parallel configuration discussion
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Series requires every block success; simple parallel needs at least one functional alternate. Independence only required to multiply reliability probabilities, not to draw success logic.

## 11. fault_tree_analysis_decomposes_defined_top_event_with_boolean_logic

- Topic / Anchor: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_fta_top_event`
- Original claim: FTA는 정의된 Top Event에서 시작하여 AND/OR Gate로 원인 고장조합을 하향 전개하는 실패논리 모델이다.
- Original publisher: NASA/TM–20240013806 (Oct 2024), §5.4 Fault Tree Analysis p11, PDF page index 22 visually reviewed
- Source URL: https://ntrs.nasa.gov/api/citations/20240013806/downloads/TM_Survey_MOC.pdf
- Evidence section: §5.4 FTA, page11 screenshot index22
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Specified top failure decomposes using AND/OR basic events; probabilistic evaluation requires accounting for dependencies/common cause and does not justify arbitrary multiplication of dependent event probabilities.

## 12. reliability_is_time_bounded_probability_under_conditions

- Topic / Anchor: `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` / `sw01_reliability_definition`
- Original claim: Reliability는 정해진 조건과 기간 동안 요구기능을 고장 없이 수행할 확률이며 시간구간을 포함하는 개념이다.
- Original publisher: ReliaSoft, Basics: System Reliability Analysis, RBD and series/parallel
- Source URL: https://help.reliasoft.com/articles/content/basics/system_reliability.htm
- Evidence section: Basic System Reliability Analysis R(t), individual component reliability
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Reliability is probability of successful function over declared mission time, conditions and failure criterion. Distinct from steady state availability/repairability.

## 13. low_demand_risk_reduction_factor_is_inverse_of_pfdavg_under_defined_sif_metric

- Topic / Anchor: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_rrf_relationship`
- Original claim: RRF는 정의된 조건에서 위험 감소 요구를 나타내며 저수요 모드에서는 PFDavg의 역수 관계로 설명할 수 있다.
- Original publisher: exida, RRF and PFDavg low-demand relationship
- Source URL: https://www.exida.com/Blog/how-does-mission-time-proof-test-interval-and-proof-test-coverage-impact-pfdavg
- Evidence section: RRF=1/PFDavg for low demand SIF
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Simplified low-demand RRF=1/PFDavg if safe failure/protection modeled per demand; not PFH, not independent multiple SIF risk without scenario aggregation.

## 14. pid_ideal_s_domain_equation

- Topic / Anchor: `pid_controller_tuning_sequence_gain_effects` / `pid_s_domain_formula`
- Original claim: 라플라스 영역에서 이상적인 PID 제어기는 Gc(s)=Kp+Ki/s+Kd s 형태로 표현할 수 있다.
- Original publisher: MathWorks, PID Controller in parallel form R2026b
- Source URL: https://www.mathworks.com/help/control/ref/pid.html
- Evidence section: Continuous-time parallel-form C=Kp+Ki/s+Kd*s/(Tf*s+1), Tf=0 limiting case
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: Ideal continuous-time PID has Kp+Ki/s+Kd*s; physically realizable derivative often filtered, discrete controller differs.

## 15. industrial_process_response_time_spans_input_detection_to_output_action

- Topic / Anchor: `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` / `sw08_response_time_definition`
- Original claim: Response time은 입력 변화 또는 사건 발생부터 필요한 출력 또는 조치가 완료될 때까지의 end-to-end 시간으로 센싱, 연산, 통신, 출력 갱신과 장치동작을 포함한다.
- Original publisher: Rockwell Automation, GuardLogix 5580 System Reaction Time, official HTML
- Source URL: https://www.rockwellautomation.com/en-il/docs/technical/logix5000/_online/1756-rm012/guardlogix-5580-and-compact-guardlogix-5580-safety/reaction-times/system-reaction-time.html
- Evidence section: System reaction time sensor+logic+actuator and safety task components
- Verdict: **KEEP_BOUNDED**
- Technical conditions and evidence limitation: End-to-end includes sensor reaction, input, controller task, communication/output and actuator; actual bound and final completion definition depend on target control function.


No tests executed, no grading or source Topic Pack mutation, no generated file changes; no source hash/release workflow was asserted. A score-admission procedure must separately enforce excluded and revision-hold overlays.