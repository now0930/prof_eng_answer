# 계측·제어 생산관리: 생산계획, 능력·일정, 품질·원가, 자원 및 성과관리

- Topic ID: `instrumentation_production_management_planning_quality_cost_resources`
- Official criterion: `IC-2027-W-4-5`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency used: `false`

## Scope

이 Topic은 **양산 운영의 Production Management**를 소유한다.

핵심 흐름은 다음과 같다.

`Demand / Order → Production Plan → Capacity / Schedule → Material / Manpower / Equipment → Quality / Cost → KPI → Daily Review / PDCA`

주요 개념은 Takt Time, Cycle Time, effective capacity, bottleneck, finite-capacity scheduling, changeover, batch size, WIP, FPY/Yield/Scrap/Rework, production cost variance, OEE, throughput, lead time, schedule adherence다.

## Ownership boundary

- `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`
  - Historian·MES·ERP·ISA-95
  - Timestamp·quality code·data quality
  - Genealogy·traceability data
  - Data governance·semantic interoperability
- `control_system_operations_maintenance_calibration_inspection_spares_kpi`
  - Corrective/Preventive/CBM/Predictive Maintenance
  - Calibration·inspection·spares
  - MTBF·MTTR·maintenance availability/KPI
- `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`
  - Project estimate/budget/commitment
  - Project milestone/critical path
  - Engineering·procurement·construction·acceptance
- 본 Topic
  - 반복 양산의 production plan/capacity/schedule
  - Production quality/cost/resources
  - OEE/flow/delivery KPI와 production PDCA

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
