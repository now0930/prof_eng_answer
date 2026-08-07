# 산업 IoT·스마트공장: Device–Edge–Cloud 아키텍처, 상호운용성 및 Digital Thread

- Topic ID: `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`
- Official criterion: `IC-2027-W-5-1`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency used: `false`

## Scope

이 Topic은 **IIoT·Smart Factory platform architecture와 Digital Thread lifecycle**를 소유한다.

핵심 흐름은 다음과 같다.

`Asset / Device → Edge / Gateway → Data / Platform → Application / Enterprise / Cloud → Lifecycle Digital Thread`

주요 설계축은 workload placement, offline/degraded operation, semantic interoperability, information/asset model, device fleet lifecycle, security, scalability, availability와 brownfield migration이다.

## Ownership boundary

- `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`
  - Historian·MES·ERP·ISA-95
  - Timestamp·quality code·compression·retention
  - Data governance·genealogy·industrial streaming
- `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
  - Fieldbus·Industrial Ethernet·Wireless
  - Protocol/device profile/gateway 상세 선정
  - Physical/network interoperability test
- `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
  - Digital Twin fidelity·state synchronization
  - Simulation·sensor fusion·autonomous manufacturing
- `instrumentation_production_management_planning_quality_cost_resources`
  - Production planning/capacity/quality/cost/resource decision
- 본 Topic
  - Device–Edge–Platform–Cloud architecture
  - Workload placement·offline resilience
  - Semantic platform·asset model
  - Digital Thread lifecycle continuity
  - Device/Edge fleet operation

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
