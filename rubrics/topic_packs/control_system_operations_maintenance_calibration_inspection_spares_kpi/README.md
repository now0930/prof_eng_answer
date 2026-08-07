# 계측제어시스템 운영·유지보수, 검교정·점검, 예비품 및 KPI 관리

- Topic ID: `control_system_operations_maintenance_calibration_inspection_spares_kpi`
- Official criterion: `IC-2027-W-4-6`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency used: `false`

## Scope

이 Topic은 계측제어시스템의 **운영·유지보수 관리체계**를 다룬다.

핵심 범위는 다음과 같다.

1. Asset register·system boundary·criticality
2. Corrective·Preventive·Condition-Based·Predictive Maintenance
3. Work Order·maintenance history·failure code·RCA
4. Calibration program·interval·As-Found/As-Left·OOT·traceability
5. Routine inspection·functional test·loop check·defect closeout
6. Critical spare·stock policy·preservation·obsolescence
7. MTBF·MTTR·Availability·PM Compliance·Backlog
8. CMMS/EAM data quality·roles·permit·configuration handoff
9. KPI와 failure history를 이용한 PDCA·lifecycle cost 개선

## Boundary

- 개별 센서·변환기의 물리적 교정원리와 회로오차는 해당 sensor Topic이 소유한다.
- Smart positioner의 valve signature·diagnostic algorithm은 `smart_positioner_diagnostics_valve_signature_predictive_maintenance`가 소유한다.
- Software/configuration의 MOC·backup·rollback·migration 상세는 `configuration_change_release_backup_rollback_migration_obsolescence_management`가 소유한다.
- FAT·SAT·Commissioning·Acceptance는 `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`가 소유한다.
- 이 Topic은 **운영단계의 O&M program과 governance**를 소유한다.

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
