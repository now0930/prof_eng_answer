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

## Planned valve-maintenance hand-off

- 이 Topic은 전사·공장 단위 O&M governance, asset register, criticality, CMMS/EAM, work order, maintenance strategy, calibration·inspection program, spares, KPI, RCA와 lifecycle improvement를 계속 소유한다.
- 제어밸브의 분해점검, trim·packing 교체, lapping, actuator·valve 재조립, pressure·leakage·stroke 시험과 수리 후 복원 절차는 향후 Valve Maintenance 전문 Topic으로 분리할 계획이다.
- 해당 전문 Topic이 실제 source pack으로 추가되기 전에는 이를 active routing alias나 cross-topic ID로 사용하지 않는다.
- 현재 Topic은 물리적 overhaul 절차 자체가 아니라 작업 필요성, 계획, 이력, 품질기록, 예비품과 KPI 관점의 관리 hand-off만 다룬다.

## Semantic policy

- `deterministic_checks.enabled=false`
- `llm_profile.enabled=true`
- `candidate_extraction.rules=[]`
- semantic fatal/major 판단은 C-layer에만 귀속한다.
- generated bank와 공용 release/classification 정책은 이 lane에서 수정하지 않는다.
