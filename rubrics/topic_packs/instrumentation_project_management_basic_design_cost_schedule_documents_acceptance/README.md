# 계측 프로젝트 관리: 기본설계, 원가·일정, 설계문서, 조달·시공 및 인수

- Topic ID: `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`
- Official criterion: `IC-2027-W-4-4`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency used: `false`

## Scope

이 Topic은 **instrumentation-wide project management**를 소유한다.

핵심 흐름은 다음과 같다.

`Scope / Design Basis → WBS / Cost / Schedule → Engineering Deliverables → Procurement / Vendor → Construction / QA → Mechanical Completion → Acceptance / Handover / Closeout`

주요 산출물은 Instrument Index, Instrument Datasheet, Loop Diagram, Hook-up, Cable Schedule, Junction Box Schedule, MTO/BOQ 및 관련 vendor/quality/as-built document다.

## Ownership boundary

- `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
  - URS·FRS·FDS·SDS
  - Logic/HMI software design
  - Software FAT·SAT·Site Integration의 상세 절차
- `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
  - P&ID symbol, tag, loop와 control narrative 자체의 상세 원리
- `control_system_operations_maintenance_calibration_inspection_spares_kpi`
  - 인수 후 Preventive/CBM/Predictive Maintenance
  - Calibration interval·spares·CMMS·MTBF/MTTR/KPI
- 본 Topic
  - Basic Design와 instrumentation deliverables
  - Project cost/schedule/change/document control
  - Procurement/vendor document/inspection
  - Construction QA/QC, Mechanical Completion
  - Project-wide acceptance와 As-Built handover

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
