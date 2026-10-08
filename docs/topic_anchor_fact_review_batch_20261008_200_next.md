# Topic Pack Fact Anchor 감사 — 다음 200개

- 감사일: 2026-10-08
- 범위: 아래 7개 Topic Pack에서 지정한 200개 Anchor
- 판정: 오류 확정 0, 사실관계 확인 138, 적용 맥락·표준 프로파일 확인 필요 62
- 수정: 없음. 명백한 기술 오류는 발견하지 못했다. 기존 작업 트리에 미커밋 변경이 다수 있어 원본 Pack 파일은 수정하지 않았다.
- 해석: `맥락확인`은 틀렸다는 뜻이 아니라, 문장이 권고·설계 선택·프로파일 종속 사실이어서 적용 설비/표준/벤더 조건을 확인해야 한다는 뜻이다.

## 범위 및 판정 기록

`사실확인`은 일반 기술 원리와 기본 정의에 대해 출처 대조 시 반증을 찾지 못한 항목이다. `맥락확인`은 구체적 설비·운전조건·규격 프로파일에 따라 구현이 달라지거나, 표준의 강제요건이 아닌 설계 권고를 포함하는 항목이다. 개별 표준의 완전한 규범 적합성 판정은 표준 원문 및 프로젝트 적용판을 확인하지 않고 확정하지 않았다.

| Topic ID | 이번 감사 범위 | 총 Anchor | 사실확인 | 맥락확인 |
|---|---:|---:|---:|---:|
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 21–30 | 10 | 8 | 2 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | 1–30 | 30 | 20 | 10 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | 1–29 | 29 | 20 | 9 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | 1–40 | 40 | 31 | 9 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 1–40 | 40 | 27 | 13 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | 1–30 | 30 | 20 | 10 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | 1–21 | 21 | 12 | 9 |
| **합계** |  | **200** | **138** | **62** |

### 맥락 확인이 남은 Anchor

- AI/ML: `calibration_and_uncertainty`, `mlops_lifecycle`
- Physical AI/robot: `physical_ai_definition`, `industrial_robot_architecture`, `collaborative_robot_application`, `digital_twin_definition`, `digital_twin_fidelity`, `digital_twin_synchronization`, `safety_envelope`, `supervisory_control_human_override`, `operational_design_domain_validation`, `runtime_monitoring_change_control`
- IIoT: `iiot_layered_architecture_device_edge_platform_cloud`, `iiot_edge_gateway_functions`, `iiot_aas_open_model_optional`, `iiot_digital_thread_definition`, `iiot_digital_thread_traceability_links`, `iiot_digital_twin_handoff`, `iiot_edge_device_onboarding_identity`, `iiot_security_zero_trust_least_privilege`, `iiot_availability_resilience_rto_rpo`
- 실시간 네트워크: `sw08_scheduling`, `sw08_tsn_toolbox`, `sw08_ptp_clock_architecture`, `sw08_timestamping_accuracy`, `sw08_mrp`, `sw08_dlr`, `sw08_fallback_local_control`, `sw08_graceful_degradation`, `sw08_measurement_acceptance`
- 통신 방식: `sw07_foundation_fieldbus`, `sw07_foundation_fieldbus_function_blocks`, `sw07_profibus_pa`, `sw07_modbus_tcp`, `sw07_ethernetip_cip`, `sw07_profinet`, `sw07_opcua`, `sw07_wirelesshart`, `sw07_isa10011a`, `sw07_device_profile`, `sw07_device_description`, `sw07_conformance_vs_interoperability`, `sw07_commissioning_workflow`
- Historian/MES: `historian_time_series_role`, `mes_execution_role`, `isa95_hierarchy_interface`, `source_timestamp_event_time`, `time_sync_alignment`, `data_completeness_metric`, `timeliness_latency_metric`, `streaming_event_processing`, `compression_deadband_tradeoff`, `batch_genealogy`
- HMI/Alarm: `sw03_high_performance_hmi`, `sw03_display_hierarchy`, `sw03_color_context_navigation`, `sw03_alarm_philosophy`, `sw03_alarm_rationalization`, `sw03_alarm_priority`, `sw03_alarm_deadband`, `sw03_alarm_delay`, `sw03_alarm_shelving`

그 외 범위 내 Anchor는 `사실확인`으로 판정했다. 적용 맥락이 없는 절대적 보장으로 읽히지 않도록 원문이 이미 “일반적으로”, “할 수 있다”, “요구에 따라”, “검증해야 한다” 등 조건부 표현을 둔 사실을 확인했다. 특히 TSN/PTP/PRP·HSR, HART/WirelessHART, EtherCAT/PROFINET, OPC UA, ISA-95, ISA-18/101 및 디지털 트윈 표준은 기능 자체와 특정 구현의 보장을 구분했다.

## 주요 대조 근거

- AI 위험관리: NIST AI RMF는 설계·개발·배포·운영의 위험관리 및 배포 후 모니터링·변경관리를 다룬다. 이 Framework는 자발적 위험관리 프레임워크이며 특정 MLOps 구현을 의무화하지 않는다. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- 제조 디지털 트윈: ISO 23247은 제조 디지털 트윈의 프레임워크를 제공한다. NIST는 제조 디지털 트윈의 검증·확인·불확실성 정량화 및 동기화 중요성을 별도로 다룬다. [ISO 23247-1](https://www.iso.org/standard/75066.html), [NIST Digital Twins](https://www.nist.gov/digital-twins), [NIST credibility considerations](https://www.nist.gov/publications/credibility-consideration-digital-twins-manufacturing)
- ISA-95/MES/ERP: ISA는 ISA-95를 기업 기능과 제조제어 기능 사이의 통합 모델·정보 교환 표준군으로 설명하고, Level 3 제조운영과 Level 4 기업계획의 구분을 제시한다. [ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard)
- OPC UA: OPC Foundation은 정보모델, 메시지·통신 모델과 적합성 모델을 정의하지만 모든 서버가 모든 기능을 제공하는 것은 아니며 Profile/필수기능 확인이 필요하다. [OPC UA Core](https://profiles.opcfoundation.org/document/1), [OPC UA Part 5](https://reference.opcfoundation.org/specs/OPC-10000-5/full)
- 실시간·이중화 통신: IEEE 802.1Qbv는 IEEE 802.1AS 시간에서 유도된 타이밍을 이용한 시간 인식 queue scheduling을 정의한다. IEC 62439-3은 PRP/HSR을 규정하며, 표준이 설명하는 seamless 동작도 정의된 구성·고장조건을 전제로 해석해야 한다. [IEEE 802.1Qbv](https://www.ieee802.org/1/pages/802.1bv.html), [IEC 62439-3](https://webstore.iec.ch/en/publication/64423)
- 산업 프로토콜: FieldComm Group은 HART가 4–20 mA loop에 digital signaling을 얹은 방식에서 발전했고 WirelessHART 네트워크 관리 기능을 정의한다고 설명한다. ODVA는 DLR의 Supervisor 및 Beacon/Announce ring-node 변형을 구분한다. [FieldComm Group HART](https://www.fieldcommgroup.org/technologies), [WirelessHART](https://www.fieldcommgroup.org/technologies/wirelesshart), [ODVA DLR guidance](https://www.odva.org/wp-content/uploads/2020/05/PUB00316R2_Guidelines-for-Using-Device-Level-Ring-DLR-with-EtherNetIP.pdf)
- 산업 Ethernet/장치 기술: PI의 GSDML은 PROFINET 장치의 식별·구조·통신·프로세스 데이터·진단 설명을 다룬다. EtherCAT Technology Group은 sub-device가 프레임 통과 중 데이터를 읽고 삽입하는 on-the-fly 처리를 설명한다. [PI GSDML](https://sea.profibus.com/downloads-and-media/gsdml-gsdx-specification-for-profinet), [EtherCAT Technology Group](https://www.ethercat.org/en/technology.html)
- HMI/Alarm: ISA-101은 제조 HMI의 화면계층·탐색·그래픽/색상·경보 표시 등을 범위에 포함한다. ISA-18 계열은 Alarm lifecycle, philosophy, rationalization, 우선순위 및 성능 모니터링을 다룬다. [ISA-101](https://www.isa.org/standards-and-publications/isa-101-standards), [ISA-18](https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards)
- OT 경계: NIST SP 800-82는 OT의 성능·신뢰성·안전 요구를 고려하며 네트워크 분할·격리 등 보안 대책을 위험에 따라 적용하도록 다룬다. [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)

## Anchor별 등록부

다음 표는 이번 배치의 전 Anchor를 빠짐없이 열거한다. 모든 판정은 위 출처 범위와 해당 Anchor의 조건부 문구를 함께 대조한 결과다.

| Topic ID | Anchor ID | 판정 |
|---|---|---|
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `calibration_and_uncertainty` | 맥락확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `deployment_environment` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `model_version_traceability` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `production_monitoring` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `drift_types` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `retraining_trigger` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `regression_and_champion_challenger` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `explainability_limits` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `human_review_fallback` | 사실확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | `mlops_lifecycle` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `physical_ai_definition` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `industrial_robot_architecture` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `collaborative_robot_application` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `sensor_complementarity` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `timestamp_and_synchronization` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `calibration_coordinate_frame` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `fusion_uncertainty` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `common_cause_and_fault_detection` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `state_estimation` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `localization` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `slam_relation` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `observability_limits` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `world_model` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `digital_twin_definition` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `digital_twin_fidelity` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `digital_twin_synchronization` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `simulation_scenario_coverage` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `synthetic_data_domain_gap` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `robot_planning_hierarchy` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `closed_loop_ai` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `edge_on_device_ai` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `latency_deadline_budget` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `autonomous_manufacturing` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `human_robot_collaboration` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `safety_envelope` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `safe_state_fallback_degraded_mode` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `supervisory_control_human_override` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `functional_safety_separation` | 사실확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `operational_design_domain_validation` | 맥락확인 |
| `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` | `runtime_monitoring_change_control` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_smart_factory_scope` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_layered_architecture_device_edge_platform_cloud` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_ot_control_boundary` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_protocol_connectivity_handoff` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_edge_gateway_functions` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_workload_placement_latency_bandwidth_cost` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_offline_degraded_mode` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_data_contract_timestamp_quality_context` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_historian_mes_data_handoff` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_syntactic_semantic_interoperability` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_information_model_asset_relationship` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_asset_namespace_identifier` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_asset_model_version_lifecycle` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_aas_open_model_optional` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_digital_thread_definition` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_digital_thread_traceability_links` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_digital_twin_handoff` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_api_event_interface_contract` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_edge_device_onboarding_identity` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_device_edge_fleet_management` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_remote_update_rollback` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_observability_logs_metrics_traces` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_security_zero_trust_least_privilege` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_data_privacy_residency_governance` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_scalability_capacity_multi_site` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_availability_resilience_rto_rpo` | 맥락확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_value_use_case_kpi_architecture` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_incremental_brownfield_migration` | 사실확인 |
| `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `iiot_lifecycle_governance_pdca` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_performance_requirements` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_latency_definition` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_jitter_definition` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_cycle_time_definition` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_response_time_definition` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_throughput_distinction` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_determinism_definition` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_worst_case_analysis` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_network_load_headroom` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_priority_qos` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_scheduling` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_tsn_toolbox` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_tsn_qbv` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_tsn_preemption` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_tsn_policing` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_ptp_purpose` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_ptp_clock_architecture` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_timestamping_accuracy` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_sync_not_determinism` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_redundancy_objectives` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_recovery_time_components` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_ring_recovery_general` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_mrp` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_dlr` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_prp` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_hsr` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_seamless_independence` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_packet_loss` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_broadcast_storm` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_multicast_management` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_congestion_buffering` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_failover_state_consistency` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_fallback_local_control` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_graceful_degradation` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_redundancy_health_monitoring` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_failure_domain_independence` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_fault_injection_testing` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_measurement_acceptance` | 맥락확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_sw07_boundary` | 사실확인 |
| `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` | `sw08_sw09_boundary` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_communication_requirements` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_layered_view` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_selection_multicriteria` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_copper_media` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_fiber_media` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_serial_communication` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_rs485_multidrop` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_topology_selection` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_termination_grounding` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_fieldbus_concept` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_hart_overlay` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_hart_multidrop` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_foundation_fieldbus` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_foundation_fieldbus_function_blocks` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_profibus_pa` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_modbus_rtu` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_modbus_tcp` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_ethernetip_cip` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_profinet` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_ethercat` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_opcua` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_opcua_role_boundary` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_wirelesshart` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_isa10011a` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_wireless_site_survey` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_wireless_power_lifecycle` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_gateway_role` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_protocol_conversion` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_device_profile` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_device_description` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_interoperability_levels` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_conformance_vs_interoperability` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_commissioning_workflow` | 맥락확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_addressing_naming` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_diagnostics_maintenance` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_installed_base_transition` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_lifecycle_compatibility` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_vendor_tool_dependency` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_sw08_boundary` | 사실확인 |
| `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | `sw07_sw09_boundary` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `historian_time_series_role` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `historian_not_backup_only` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `mes_execution_role` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `erp_business_role` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `isa95_hierarchy_interface` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `it_ot_layered_integration` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `edge_gateway_role` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `source_timestamp_event_time` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `time_sync_alignment` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `quality_code_semantics` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `bad_uncertain_propagation` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `data_completeness_metric` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `timeliness_latency_metric` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `store_and_forward_recovery` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `streaming_event_processing` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `compression_deadband_tradeoff` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `quality_event_preservation` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `metadata_context_role` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `tag_naming_namespace` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `information_model_semantics` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `master_data_consistency` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `data_governance_ownership` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `retention_lifecycle` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `traceability_audit` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `batch_genealogy` | 맥락확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `acquisition_sampling_semantics` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `event_snapshot_distinction` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `realtime_fit_for_purpose` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `semantic_interoperability` | 사실확인 |
| `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` | `topic_boundary_transport_model` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_scope_operator_information` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_hmi_scada_architecture` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_architecture_redundancy_quality` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_high_performance_hmi` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_display_hierarchy` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_color_context_navigation` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_definition` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_philosophy` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_rationalization` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_priority` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_state_acknowledgement` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_deadband` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_delay` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_shelving` | 맥락확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_suppression` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_flood_chattering` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_performance_kpi` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_setpoint_value_classes` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_setpoint_governance` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_alarm_trip_interlock_boundary` | 사실확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_soe_definition` | 사실확인 |

## 결론

이번 200개에서는 확정적으로 잘못된 사실을 찾지 못해 원본 Anchor를 바꾸지 않았다. 62개 `맥락확인` 항목도 현재 문구가 조건·프로파일 의존성을 대체로 표시하고 있어 즉시 정정 대상으로 보지 않았다. 향후 구체적 플랜트 설계, 적용 규격판 또는 벤더별 호환성 표로 구체화할 때 검토해야 한다. 당시 진행 메모의 분모 2,073은 후속 전수 대조에서 실제 원본 인벤토리와 불일치한 것으로 확인됐다. 전체 완료 집계는 최종 감사 보고서의 2,068개 기준을 따른다.
