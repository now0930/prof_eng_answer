# 산업 IoT·스마트공장: Device–Edge–Cloud 아키텍처, 상호운용성 및 Digital Thread

## 1. Topic metadata

- `topic_id`: `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`
- `official_criterion`: `IC-2027-W-5-1`
- `question_type`: `IMPLEMENTATION_EVALUATION`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `NORMAL`
- `historical_frequency_used`: `false`
- `semantic_execution`: `LLM_ONLY`

## 2. STEP 0 ownership conclusion

STEP 0 narrow audit 결과:

- Existing Topic Pack count: 58
- IIoT/Smart Factory true duplicate blocker: 0
- proposed routing alias collision: 0
- Historian/MES Topic: IIoT/Smart Factory architecture direct signal 0
- Communication Topic: network/protocol selection ownership 중심
- Physical AI Topic: Digital Twin fidelity/synchronization/simulation ownership 중심

따라서 본 Topic은 **IIoT/Smart Factory platform architecture와 Digital Thread lifecycle**를 독립 소유한다.

인접 Topic handoff ID:

- Data integration: `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`
- Communication: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- Digital Twin/Physical AI: `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- Production Management: `instrumentation_production_management_planning_quality_cost_resources`

## 3. Layered Architecture

`Asset / Device / Control → Edge / Gateway → Data / Platform → Application / Enterprise / Cloud`

실시간 제어·Interlock·SIS는 Cloud/WAN dependency와 분리된 OT local control boundary를 유지한다.

## 4. Edge / Cloud Workload Placement

Edge는 다음 기능을 수행할 수 있다.

- Protocol termination / normalization
- Filtering / aggregation
- Buffering
- Local rules / analytics
- Quality / timestamp preservation
- Store-and-forward
- Offline / degraded operation

실행위치는 latency, jitter, bandwidth, compute, security/privacy, cost와 outage requirement를 비교해 결정한다.

## 5. Interoperability and Data Contract

Data Contract:

- Value
- Unit
- Timestamp
- Quality
- Source identity
- Engineering range
- Asset / Context
- Schema version

Connectivity와 Syntactic Interoperability는 Semantic Interoperability와 구분한다.

Information Model은 Asset, Property, Event, Command와 Relationship의 의미를 구조화한다.

## 6. Asset Model / Namespace

동일 Asset을 여러 시스템에서 연결하기 위해 다음을 관리한다.

- Asset hierarchy
- Namespace
- Stable identifier
- Property / relationship
- Schema / model version
- Firmware / configuration / engineering revision

AAS는 표준화된 asset representation의 예시로 사용할 수 있으나 도입 자체가 semantic completeness를 보장하지 않는다.

## 7. Digital Thread

Digital Thread는 동일 Asset의 lifecycle data continuity다.

`Requirement → Engineering → Procurement → Installation → Commissioning → Operation → Maintenance → Change`

Identifier/version을 이용해 P&ID, datasheet, loop/cable document, vendor data, software/configuration, maintenance record와 operational event를 연결한다.

Digital Thread는 Digital Twin과 구분한다.
Digital Twin fidelity/state synchronization/simulation 상세는 Physical AI Topic으로 handoff한다.

## 8. Device / Edge Lifecycle

Device onboarding:

- Asset identity
- Credential / certificate
- Configuration baseline
- Data mapping
- Ownership

Fleet management:

- Inventory / health
- Connectivity
- CPU / memory / storage
- Firmware / software / configuration version
- Certificate expiry
- Remote rollout / rollback

## 9. Security / Availability / Scalability

Security:

- Identity / Authentication / Authorization
- Least privilege
- Network segmentation
- Encryption
- Certificate / key lifecycle
- Audit

Scalability:

- Device / Tag count
- Message rate
- Storage growth
- Retention
- Concurrent consumer
- Multi-site

Availability:

- Redundancy / Failover
- Backup / Restore
- DR
- RTO / RPO

Platform HA가 OT local control과 fail-safe를 대체하지 않는다.

## 10. Observability

End-to-end data path를 다음으로 관찰한다.

- Metrics
- Logs
- Events
- Correlation ID
- 필요 시 Distributed Trace

대상은 message loss, latency, resource saturation, interface error와 fleet health다.

## 11. Brownfield / Value

Smart Factory architecture는 use case/KPI에서 requirement를 역도출한다.

예:

- Traceability
- Downtime reduction
- Quality improvement
- Energy optimization
- Faster changeover
- Remote support

Brownfield에서는 기존 PLC/DCS/SCADA, protocol, vendor tool과 production stop constraint를 고려하여 coexistence, pilot, phased migration와 rollback을 적용한다.

## 12. Required Fact Anchors

총 `29`개 Anchor를 `fact_anchor.json` 정본으로 사용한다.

1. `iiot_smart_factory_scope` — 산업 IoT와 스마트공장은 현장 Asset·Sensor·Controller의 데이터를 Edge·Platform·Cloud와 업무시스템에 연결하여 상태인지, 분석, 최적화와 lifecycle 의사결정을 지원하는 제조 아키텍처이며, 단순 원격접속이나 Cloud 사용 자체와 동일하지 않다.
2. `iiot_layered_architecture_device_edge_platform_cloud` — IIoT 아키텍처는 일반적으로 Device/Control, Edge/Gateway, Data/Platform, Application/Enterprise/Cloud 계층으로 역할을 분리하고, 각 계층의 책임·데이터 계약·보안·가용성 경계를 명시해야 한다.
3. `iiot_ot_control_boundary` — 실시간 제어·Interlock·SIS처럼 결정성·안전성이 요구되는 기능은 통신 단절이나 Cloud 지연에 의존하지 않도록 OT 제어경계를 보존하고, IIoT 분석·최적화 계층은 제어 안정성을 침해하지 않는 방식으로 연계해야 한다.
4. `iiot_protocol_connectivity_handoff` — Fieldbus, Industrial Ethernet, Wireless와 Protocol/Gateway의 물리·통신 특성 및 선정 상세는 industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection Topic이 소유하고, 본 Topic은 그 연결을 이용한 상위 Device–Edge–Platform integration을 소유한다.
5. `iiot_edge_gateway_functions` — Edge/Gateway는 Protocol termination·normalization, buffering, filtering, aggregation, local rule/analytics, quality·timestamp 보존과 Store-and-forward를 수행할 수 있으며, 현장 요구에 따라 중앙 Platform 장애 시 제한된 local operation을 유지하도록 설계할 수 있다.
6. `iiot_workload_placement_latency_bandwidth_cost` — Workload Placement는 latency·jitter·bandwidth, 데이터량, privacy/security, compute resource, 운영비용, 장애 시 요구동작과 중앙집중 관리 필요성을 비교하여 Device·Edge·Cloud 중 실행위치를 결정해야 한다.
7. `iiot_offline_degraded_mode` — Cloud·WAN·Platform 단절을 고려하여 Edge buffer 용량, 데이터 만료·우선순위, local fallback/degraded mode, 재접속 후 backlog 재전송과 state resynchronization을 설계해야 한다.
8. `iiot_data_contract_timestamp_quality_context` — IIoT 데이터 계약은 value뿐 아니라 unit, timestamp, quality, source identity, engineering range, asset/context와 schema version을 포함하여 Edge·Platform·Cloud에서 동일한 의미로 해석되도록 해야 한다.
9. `iiot_historian_mes_data_handoff` — Historian·MES·ERP, timestamp·quality code·compression·retention·data governance와 genealogy의 상세 데이터 관리 원리는 historian_mes_it_ot_integration_industrial_data_quality_realtime_processing Topic이 소유하며, 본 Topic은 해당 데이터 기능을 IIoT platform architecture와 lifecycle continuity 관점에서 사용한다.
10. `iiot_syntactic_semantic_interoperability` — Connectivity와 Syntactic Interoperability는 data transport·format 호환성을 의미할 수 있지만, Semantic Interoperability는 asset, property, unit, quality와 관계의 의미까지 공통으로 해석할 수 있어야 하므로 단순 protocol 연결만으로 달성되지 않는다.
11. `iiot_information_model_asset_relationship` — Information Model은 Asset, component, property, event, command와 관계를 구조화하고 identifier·unit·semantic definition을 연결하여 서로 다른 시스템이 동일한 제조 객체를 일관되게 해석하도록 한다.
12. `iiot_asset_namespace_identifier` — Asset hierarchy·namespace와 globally 또는 조직 내에서 일관된 identifier를 정의하여 동일 자산의 Device, Edge, MES, Historian, Cloud와 engineering 문서 표현을 연결하고 중복·충돌을 방지해야 한다.
13. `iiot_asset_model_version_lifecycle` — Asset Model과 schema는 설비 변경, firmware·configuration, software release와 engineering revision에 따라 version을 관리하고, 생산·분석 결과가 어떤 asset/model version과 연결되는지 추적할 수 있어야 한다.
14. `iiot_aas_open_model_optional` — Asset Administration Shell(AAS) 같은 표준화된 digital representation은 asset identification, submodel과 property/relationship 구조를 이용해 cross-system exchange를 지원할 수 있으나, 특정 표준 하나를 사용했다는 사실만으로 semantic completeness나 interoperability가 자동 보장되는 것은 아니다.
15. `iiot_digital_thread_definition` — Digital Thread는 요구·설계·구매·설치·시운전·운전·정비·변경에 걸친 동일 Asset의 identifier, model, configuration, document와 operational data를 추적 가능하게 연결하는 lifecycle data continuity 개념이다.
16. `iiot_digital_thread_traceability_links` — Digital Thread는 object ID와 version을 기준으로 requirement, P&ID·datasheet·loop/cable document, vendor data, software/configuration, maintenance record와 operational event를 link하여 source와 변경이력을 추적할 수 있어야 한다.
17. `iiot_digital_twin_handoff` — Digital Thread는 lifecycle data continuity와 traceability를 소유하고, 동적 모델의 fidelity·state synchronization·simulation·autonomous control에 초점을 둔 Digital Twin 상세 원리는 physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control Topic으로 handoff한다.
18. `iiot_api_event_interface_contract` — Platform interface는 API, event/message, file/batch 등 사용 방식에 맞춰 schema, version, idempotency, ordering, retry, timeout와 error handling을 정의하여 생산자·소비자 간 계약을 명확히 해야 한다.
19. `iiot_edge_device_onboarding_identity` — Device onboarding은 asset identity 확인, credential/ certificate 발급, configuration baseline, data mapping과 ownership 등록을 포함해야 하며, 임의 연결된 장비가 자동으로 신뢰된 자산이 되어서는 안 된다.
20. `iiot_device_edge_fleet_management` — 대규모 IIoT 운영은 device/edge inventory, health, connectivity, storage·CPU·memory, software/firmware/configuration version, certificate expiry와 alarm을 fleet 관점에서 관찰하고 batch/rolling change를 통제해야 한다.
21. `iiot_remote_update_rollback` — 원격 software/firmware/configuration 배포는 compatibility, signed artifact·integrity, 단계적 rollout, health check와 rollback/recovery 경로를 가져야 하며 실패 시 제어기능의 안전한 상태와 현장 복구 가능성을 보존해야 한다.
22. `iiot_observability_logs_metrics_traces` — IIoT Platform은 device/edge/platform의 metrics, log, event와 필요 시 distributed trace·correlation ID를 이용해 수집지연, message loss, resource saturation, interface error와 end-to-end data path 상태를 관찰할 수 있어야 한다.
23. `iiot_security_zero_trust_least_privilege` — IIoT 보안은 asset identity, authentication, authorization, least privilege, network segmentation, encryption, certificate/key lifecycle와 audit를 계층별로 적용하고 OT availability·safety 요구와 함께 설계해야 한다.
24. `iiot_data_privacy_residency_governance` — Cloud·cross-site 데이터 이용은 산업기밀, 개인정보, 계약·규제 요구와 data residency를 고려하여 수집 최소화, access policy, retention과 export boundary를 정의해야 한다.
25. `iiot_scalability_capacity_multi_site` — Platform scalability는 device/tag/event 수, sampling/message rate, storage growth, retention, concurrent consumer와 multi-site 연결을 기준으로 capacity를 계획하고, scale-out 시 ordering·partition·consistency와 비용 영향을 함께 검토해야 한다.
26. `iiot_availability_resilience_rto_rpo` — IIoT 서비스는 업무 중요도에 따라 redundancy, failover, backup/restore와 disaster recovery를 설계하고 RTO·RPO 또는 동등한 복구목표를 정의하되, OT 제어 안전성은 Platform 가용성과 분리하여 보장해야 한다.
27. `iiot_value_use_case_kpi_architecture` — 스마트공장 아키텍처는 기술도입 자체가 아니라 traceability, downtime reduction, quality improvement, energy optimization, faster changeover, remote support 등 명확한 use case와 KPI를 기준으로 필요한 data·latency·availability·security 수준을 역으로 정의해야 한다.
28. `iiot_incremental_brownfield_migration` — Brownfield 스마트공장 전환은 기존 PLC/DCS/SCADA·protocol·vendor tool·legacy tag와 생산중단 제약을 고려하여 gateway/adapter와 coexistence, pilot, 단계적 migration, rollback를 계획하고 기존 제어기능의 안정성을 보존해야 한다.
29. `iiot_lifecycle_governance_pdca` — IIoT/Smart Factory 운영은 architecture, asset model, interface schema, security policy, device fleet, cost와 KPI를 정기 review하고 변경 영향과 technical debt를 관리하여 lifecycle 동안 표준화·확장성·운영성을 지속 개선해야 한다.

## 13. Fatal Wrong Claims

총 `14`개 Fatal contract를 사용한다.

1. `iiot_fatal_internet_connection_equals_smart_factory` — PLC나 센서를 인터넷 또는 Cloud에 연결하면 그것만으로 스마트공장이 완성된다.
   - Correction: 스마트공장은 현장자산, Edge/Platform, 업무·분석과 lifecycle 의사결정을 역할·데이터·보안 경계로 통합해야 한다.
2. `iiot_fatal_cloud_replaces_ot_control` — Interlock·SIS·실시간 제어를 Cloud로 이전해도 네트워크 단절과 지연에 관계없이 동일한 결정성과 안전성이 자동 보장된다.
   - Correction: 결정성·안전성 요구가 있는 OT 제어는 Cloud/WAN 의존과 분리된 local control boundary를 보존해야 한다.
3. `iiot_fatal_edge_is_protocol_converter_only` — Edge Gateway는 protocol converter일 뿐이므로 buffering, local processing, store-and-forward와 offline mode는 고려할 필요가 없다.
   - Correction: Edge는 통신변환 외에도 buffering, normalization, local analytics와 단절 시 continuity 기능을 수행할 수 있다.
4. `iiot_fatal_all_workloads_cloud` — 모든 IIoT workload는 항상 Cloud에서 실행하는 것이 latency·bandwidth·cost·availability 관점에서 최적이다.
   - Correction: 실행위치는 latency, bandwidth, data volume, privacy, compute, cost와 장애 시 동작 요구를 비교해 Device/Edge/Cloud로 배치해야 한다.
5. `iiot_fatal_protocol_equals_semantic_interop` — OPC UA, MQTT 또는 특정 protocol로 통신이 되면 서로 다른 vendor 시스템 간 semantic interoperability도 자동으로 완전 달성된다.
   - Correction: protocol connectivity와 semantic interoperability는 구분하며 asset/property/unit/quality/relationship 의미를 공통 해석할 수 있어야 한다.
6. `iiot_fatal_tag_name_is_information_model` — Tag naming 규칙만 통일하면 Information Model과 Asset relationship은 별도로 정의할 필요가 없다.
   - Correction: Naming은 식별 규칙이고 Information Model은 asset, property와 관계·semantic definition을 구조화한다.
7. `iiot_fatal_digital_thread_is_cloud_trend` — Digital Thread는 sensor trend 데이터를 Cloud에 저장하는 것과 동일하다.
   - Correction: Digital Thread는 동일 asset의 requirement·engineering·configuration·operation·maintenance 정보를 identifier와 version으로 lifecycle 전반에 연결하는 data continuity다.
8. `iiot_fatal_digital_thread_equals_digital_twin` — Digital Thread와 Digital Twin은 이름만 다른 동일 개념이다.
   - Correction: Digital Thread는 lifecycle traceability를, Digital Twin은 동적 모델의 fidelity·state synchronization·simulation 등 다른 초점을 가진다.
9. `iiot_fatal_offline_auto_recovers` — 통신이 복구되면 누락 데이터와 상태가 자동으로 완전 복원되므로 buffer·ordering·backlog·resynchronization 정책은 불필요하다.
   - Correction: offline buffer, ordering/expiry, backlog replay와 state resynchronization을 명시적으로 설계해야 한다.
10. `iiot_fatal_untrusted_device_auto_onboard` — IP 주소가 할당된 장비는 identity와 credential 검증 없이 trusted IIoT asset으로 자동 등록해도 된다.
   - Correction: Device onboarding은 asset identity, credential/certificate, configuration baseline과 data mapping을 검증해야 한다.
11. `iiot_fatal_mass_update_without_rollback` — 모든 Edge 장비에 firmware를 동시에 배포하면 검증, 단계적 rollout와 rollback은 필요 없다.
   - Correction: 원격배포는 compatibility·integrity 검증, staged rollout, health check와 rollback/recovery를 가져야 한다.
12. `iiot_fatal_cloud_removes_capacity_planning` — Cloud platform을 사용하면 device/tag/message/storage 증가에 대한 capacity planning이 자동으로 해결된다.
   - Correction: Device/tag/message rate, storage growth, consumer, multi-site와 consistency/cost를 기준으로 scalability를 설계해야 한다.
13. `iiot_fatal_platform_ha_replaces_local_safety` — Platform 이중화가 있으면 field control의 local autonomy, fail-safe와 degraded mode는 고려할 필요가 없다.
   - Correction: Platform HA와 OT local control/safe-state 요구는 별도 계층에서 설계해야 한다.
14. `iiot_fatal_adjacent_topics_owned_all` — 본 Topic이 Historian/MES data quality·retention, fieldbus/protocol 상세, Digital Twin fidelity·simulation과 production planning까지 모두 직접 소유한다.
   - Correction: 본 Topic은 IIoT/Smart Factory architecture·Edge/Cloud·semantic platform·Digital Thread lifecycle을 소유하고 인접 상세는 각 기존 Topic으로 handoff해야 한다.

## 14. Routing aliases

- `industrial iot smart factory edge cloud digital thread`
- `iiot smart factory edge cloud architecture`
- `industrial iot edge gateway cloud interoperability`
- `smart factory device edge platform cloud integration`
- `iiot asset model semantic interoperability digital thread`
- `industrial edge computing cloud workload placement`
- `smart manufacturing edge cloud data platform`
- `industrial iot device management edge platform`
- `digital thread asset lifecycle manufacturing data`
- `smart factory information model cross vendor interoperability`
- `산업 IoT 스마트공장 엣지 클라우드 디지털 스레드`
- `IIoT 스마트팩토리 엣지 클라우드 아키텍처`
- `스마트공장 디바이스 엣지 플랫폼 클라우드 연계`
- `산업 IoT 상호운용성 정보모델 디지털 스레드`
- `엣지 컴퓨팅 클라우드 워크로드 배치 제조`
- `스마트 제조 자산모델 수명주기 데이터 연계`
- `IIoT 디바이스 관리 엣지 플랫폼 운영`
- `스마트팩토리 크로스벤더 상호운용 디지털 스레드`

## 15. Routing field points

- IIoT·Smart Factory를 단순 인터넷 연결이 아닌 제조 architecture와 lifecycle decision support로 정의
- Device/Control–Edge/Gateway–Platform–Application/Enterprise/Cloud 계층
- 실시간 제어·Interlock·SIS의 OT local control boundary
- Fieldbus/Ethernet/Wireless/Protocol 상세와 communication Topic handoff
- Edge buffering·filtering·normalization·local analytics·store-and-forward
- Latency·bandwidth·compute·security·cost 기반 Device/Edge/Cloud workload placement
- WAN/Cloud 단절 시 offline/degraded mode·backlog replay·resynchronization
- Value·unit·timestamp·quality·source·context·schema version 데이터 계약
- Historian/MES/ERP data-management 상세와 historian_mes_it_ot_integration_industrial_data_quality_realtime_processing handoff
- Connectivity·syntactic·semantic interoperability의 차이
- Asset·property·event·command·relationship의 Information Model
- Asset hierarchy·namespace·identifier의 cross-system identity
- Asset Model·schema·firmware·configuration·engineering revision version
- Asset Administration Shell(AAS)·Submodel의 선택적 표준화 예시
- Digital Thread의 requirement–engineering–operation–maintenance lifecycle continuity
- Identifier/version 기반 engineering document·vendor data·configuration·event traceability link
- Digital Thread와 Digital Twin fidelity/synchronization/simulation ownership 경계
- API/event interface schema·version·idempotency·ordering·retry
- Device onboarding identity·credential·certificate·configuration baseline
- Device/Edge inventory·health·firmware·certificate expiry fleet management
- Remote update compatibility·integrity·staged rollout·rollback
- Metrics·logs·events·trace·correlation ID 기반 end-to-end observability
- Identity·authentication·authorization·least privilege·segmentation·certificate lifecycle
- Privacy·industrial confidentiality·data residency·retention·export boundary
- Device/tag/message rate·storage growth·consumer·multi-site scalability
- Redundancy·failover·backup/restore·RTO/RPO와 OT local autonomy
- Use case/KPI에서 data·latency·availability·security requirement 역도출
- Brownfield gateway/coexistence/pilot/phased migration/rollback
- Architecture·asset model·schema·security·fleet·cost·KPI lifecycle governance

## 16. Expected question patterns

1. 산업 IoT와 스마트공장의 구성 및 Device–Edge–Cloud 아키텍처를 설명하시오.
   - intent: 계층별 역할과 OT control boundary, data/interface contract를 구조적으로 설명한다.
   - required anchors: iiot_smart_factory_scope, iiot_layered_architecture_device_edge_platform_cloud, iiot_ot_control_boundary, iiot_edge_gateway_functions, iiot_workload_placement_latency_bandwidth_cost
2. Edge Computing과 Cloud Computing의 역할 및 workload 배치 기준을 설명하시오.
   - intent: latency·bandwidth·compute·security·cost·offline requirement로 실행위치를 평가한다.
   - required anchors: iiot_edge_gateway_functions, iiot_workload_placement_latency_bandwidth_cost, iiot_offline_degraded_mode, iiot_scalability_capacity_multi_site
3. IIoT의 상호운용성을 Connectivity, Syntactic, Semantic 관점에서 설명하시오.
   - intent: protocol 연결과 information model 기반 semantic interoperability를 구분한다.
   - required anchors: iiot_protocol_connectivity_handoff, iiot_data_contract_timestamp_quality_context, iiot_syntactic_semantic_interoperability, iiot_information_model_asset_relationship, iiot_asset_namespace_identifier
4. 스마트공장에서 Asset Model과 Namespace 관리방법을 설명하시오.
   - intent: asset identity, model relationship와 lifecycle version을 cross-system 관점에서 설명한다.
   - required anchors: iiot_information_model_asset_relationship, iiot_asset_namespace_identifier, iiot_asset_model_version_lifecycle, iiot_aas_open_model_optional
5. Digital Thread의 개념, 구성요소와 Digital Twin과의 차이를 설명하시오.
   - intent: lifecycle continuity와 traceability link를 동적 twin model과 구분한다.
   - required anchors: iiot_digital_thread_definition, iiot_digital_thread_traceability_links, iiot_digital_twin_handoff, iiot_asset_model_version_lifecycle
6. IIoT Platform의 Device onboarding과 fleet 관리방법을 설명하시오.
   - intent: identity/credential, inventory health, version과 remote update/rollback을 lifecycle로 설명한다.
   - required anchors: iiot_edge_device_onboarding_identity, iiot_device_edge_fleet_management, iiot_remote_update_rollback, iiot_observability_logs_metrics_traces
7. IIoT 시스템의 통신단절 및 Platform 장애 대응방안을 설명하시오.
   - intent: offline buffer, degraded mode, state resync와 HA/DR/local autonomy를 설명한다.
   - required anchors: iiot_offline_degraded_mode, iiot_edge_gateway_functions, iiot_availability_resilience_rto_rpo, iiot_ot_control_boundary
8. 스마트공장 플랫폼의 보안·확장성·가용도 설계기준을 설명하시오.
   - intent: identity/least privilege, residency, scalability와 RTO/RPO를 비기능 요구로 통합한다.
   - required anchors: iiot_security_zero_trust_least_privilege, iiot_data_privacy_residency_governance, iiot_scalability_capacity_multi_site, iiot_availability_resilience_rto_rpo
9. Brownfield 공장에 IIoT/Smart Factory를 단계적으로 적용하는 방안을 설명하시오.
   - intent: 기존 protocol/OT constraint, gateway/coexistence, pilot, migration/rollback과 KPI를 연결한다.
   - required anchors: iiot_protocol_connectivity_handoff, iiot_incremental_brownfield_migration, iiot_value_use_case_kpi_architecture, iiot_lifecycle_governance_pdca
10. Historian/MES, 산업통신, Digital Twin과 IIoT/Smart Factory Topic의 ownership을 구분하시오.
   - intent: data-management, protocol, twin model과 platform architecture/digital thread lifecycle의 경계를 설명한다.
   - required anchors: iiot_protocol_connectivity_handoff, iiot_historian_mes_data_handoff, iiot_digital_twin_handoff, iiot_smart_factory_scope, iiot_digital_thread_definition

## 17. Semantic review requirements

- IIoT를 단순 internet/cloud 연결과 구분한다.
- Device–Edge–Platform–Cloud 계층 책임을 정의한다.
- OT local control boundary를 보존한다.
- Edge workload와 offline/degraded mode를 설명한다.
- Data contract와 semantic interoperability를 구분한다.
- Asset namespace/identifier/model version을 lifecycle로 연결한다.
- Digital Thread와 Digital Twin을 구분한다.
- Device onboarding·fleet management·remote rollback을 설명한다.
- Security·scalability·availability를 non-functional requirement로 설명한다.
- Brownfield migration과 use-case KPI를 연결한다.
- Historian/MES·Communication·Physical AI/Production Topic handoff를 유지한다.
- Historical frequency는 근거가 없어 사용하지 않는다.

## 18. Lane boundary

이 STEP 1에서는 Topic Sheet와 Topic Pack source 5개만 생성한다.
focused regression test는 STEP 2에서 별도 작성한다.

다음은 수정하지 않는다.

- `rubrics/generated/**`
- 공용 classification/release 정책
- production Python
- 다른 Topic Pack
- `docs/exam_scope/**`
