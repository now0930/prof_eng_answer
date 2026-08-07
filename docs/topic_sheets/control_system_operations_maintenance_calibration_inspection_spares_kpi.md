# 계측제어시스템 운영·유지보수, 검교정·점검, 예비품 및 KPI 관리

## 1. Topic metadata

- `topic_id`: `control_system_operations_maintenance_calibration_inspection_spares_kpi`
- `official_criterion`: `IC-2027-W-4-6`
- `question_type`: `IMPLEMENTATION_EVALUATION`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `NORMAL`
- `historical_frequency_used`: `false`
- `semantic_execution`: `LLM_ONLY`
- `deterministic_checks.enabled`: `false`
- `candidate_extraction.rules`: `[]`

## 2. Coverage purpose

이 Topic은 계측제어시스템을 설치·인수한 뒤 실제 운전기간 동안 수행하는 **운영·유지보수 관리 프로그램**을 소유한다.

핵심은 개별 장비의 수리기술이 아니라 다음 폐루프다.

`Asset Register → Criticality → Maintenance Strategy → Calibration/Inspection → Work Order/History → Spares → KPI → RCA/Review → Policy Improvement`

## 3. Scope boundary

### 3.1 In scope

- Asset register와 system boundary
- Corrective / Preventive / CBM / Predictive Maintenance
- Criticality·risk 기반 maintenance planning
- Work Order·failure code·maintenance history·RCA
- Calibration program·interval·As-Found·As-Left·OOT
- Reference standard·traceability
- Routine inspection·functional test·loop check
- Defect priority·deferred maintenance
- Critical spare·min/max·reorder point·lead time
- Preservation·shelf-life·obsolescence
- MTBF·MTTR·Availability
- PM compliance·schedule compliance·backlog
- CMMS/EAM data quality
- Roles·competence·permit·LOTO·restoration
- Configuration/back-up change handoff
- PDCA·lifecycle cost optimization

### 3.2 Out of scope / handoff

- 장비별 sensor calibration 원리 → 각 sensor Topic
- Valve signature와 smart positioner predictive diagnostics → `smart_positioner_diagnostics_valve_signature_predictive_maintenance`
- Software/configuration MOC·release·backup·rollback·migration → `configuration_change_release_backup_rollback_migration_obsolescence_management`
- Project FAT·SAT·Commissioning·Acceptance → `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- PLC/DCS redundancy architecture 자체 → `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability`

## 4. O&M management chain

### 4.1 기준정보

Asset register와 Tag를 정비·교정·예비품·KPI 데이터의 공통 key로 사용한다.
System boundary와 자산의 기능·중요도를 먼저 정의한다.

### 4.2 정비전략

- Corrective Maintenance: 고장 후 복구
- Preventive Maintenance: 시간·사용량 기준
- Condition-Based Maintenance: 상태 threshold·trend 기준
- Predictive Maintenance: 데이터 분석·모델 기반 미래 고장위험 추정

어느 하나를 모든 자산에 일괄 적용하지 않는다.
Criticality, consequence, failure behavior와 비용으로 전략을 조합한다.

### 4.3 Work management

`Request → Priority → Permit/Isolation → Execute → Test → Restore → Closeout`

작업종결 시 failure mode, 원인, 조치, 부품, 시간, as-found/as-left를 이력화한다.
반복·중대 고장은 Bad Actor와 RCA로 연결한다.

## 5. Calibration management

Calibration은 adjustment와 동일하지 않다.
요구 정확도·허용오차와 reference standard를 기준으로 비교·판정·기록하고 필요 시 조정한다.

교정주기는 다음을 근거로 조정한다.

- criticality
- drift·as-found history
- operating environment
- usage
- manufacturer recommendation
- legal/quality requirement

As-Found OOT가 발생하면 As-Left 복구만으로 끝내지 않고 영향기간과 관련 공정·품질 데이터의 유효성을 평가한다.

## 6. Inspection management

- Routine Inspection: 외관, 환경, 전원, wiring, grounding, tubing, leakage 등
- Functional Test: 기능 수행 여부 확인
- Loop Check: sensor-input-controller-output 경로 확인
- Alarm/Interlock Test: 설정된 보호·운전기능 검증

Finding은 priority와 due date를 정하고 Work Order·retest·closeout으로 닫는다.
Deferred Maintenance는 risk assessment와 temporary safeguard를 포함한다.

## 7. Spare parts management

Critical Spare는 단가가 아니라 다음으로 판단한다.

- failure consequence
- lead time
- repairability
- substitutability
- commonality
- obsolescence

재고는 min/max 또는 reorder point와 같은 정책으로 관리한다.
전자계장 spare는 shelf-life, storage condition, firmware/license, periodic functional check도 관리한다.

단종부품 대체는 compatibility 확인 후 MOC와 기능시험으로 handoff한다.

## 8. KPI

### 8.1 MTBF

대표적인 데이터 관계:

`MTBF = Operating Time / Number of Failures`

고장 정의와 시간경계를 고정해야 비교가 의미 있다.

### 8.2 MTTR

대표적인 데이터 관계:

`MTTR = Total Restoration Time / Number of Repairs`

조직별로 diagnosis, repair, test, restoration과 waiting time의 포함경계를 명시한다.

### 8.3 Availability

단순 수리 가능 2상태 모델의 고유가용도:

`A_i = MTBF / (MTBF + MTTR)`

실제 Operational Availability는 planned maintenance, logistics delay, administrative delay 등 추가 downtime 정의를 포함할 수 있다.

### 8.4 Process KPI

- PM Compliance
- Schedule Compliance
- Maintenance Backlog
- Emergency Maintenance Ratio
- Repeat Failure / Bad Actor
- OOT rate
- Spare stockout / service level

단일 KPI 최적화를 피하고 reliability·cost·safety·production impact를 균형평가한다.

## 9. Data and governance

CMMS/EAM 또는 동등한 시스템에서는 다음 데이터를 표준화한다.

- Asset ID
- Work type
- Failure code
- Start/end time
- Downtime
- Cause/action
- Used spare
- Test/result

정비 전후 configuration·backup·setpoint·logic 변화도 확인한다.
변경이 있으면 configuration management로 handoff한다.

## 10. Continuous improvement

정기 review에서 다음을 함께 본다.

- KPI trend
- repeated failure
- calibration OOT
- inspection finding
- deferred maintenance
- spare stockout
- obsolescence
- RCA result

결과는 maintenance strategy, interval, spare level, design, training과 lifecycle cost 개선에 환류한다.

## 11. Required Fact Anchors

총 `26`개 Anchor를 `fact_anchor.json`의 정본으로 사용한다.

1. `om_asset_register_system_boundary` — 계측제어시스템 운영·유지보수는 자산대장과 시스템 경계를 먼저 확정하고 Tag, 위치, 기능, 제조사·모델, firmware·software, 중요도, 예비품 및 문서 연결정보를 기준정보로 관리해야 한다.
2. `maintenance_strategy_corrective_preventive_condition_predictive` — 정비전략은 고장 후 수리하는 Corrective Maintenance, 시간·사용량 기반 Preventive Maintenance, 상태지표 기반 Condition-Based Maintenance, 데이터 모델을 활용하는 Predictive Maintenance를 자산 특성과 위험에 따라 조합한다.
3. `maintenance_criticality_risk_prioritization` — 정비 우선순위와 자원배분은 고장확률만이 아니라 안전·환경·생산·품질·규제·복구시간·대체 가능성 등의 고장영향을 함께 반영한 중요도·위험도 평가로 결정해야 한다.
4. `maintenance_plan_task_interval_basis` — 정비계획은 자산별 작업내용, 주기 또는 상태기준, 책임자, 필요 공구·예비품, 안전조치, 정지창과 완료기준을 정의하며, 주기는 제조사 권고·법규·고장이력·환경·criticality와 상태추세를 근거로 조정한다.
5. `work_order_history_closed_loop` — 정비 작업은 Work Order 또는 동등한 작업지시로 요청·우선순위·허가·수행·시험·복구·종결을 추적하고, 고장모드·원인·조치·사용부품·소요시간·as-found/as-left 결과를 이력으로 남겨 다음 계획에 환류해야 한다.
6. `failure_coding_rca_bad_actor_feedback` — 반복고장과 중대한 장애는 일관된 failure code와 원인분류를 사용해 Bad Actor를 식별하고, 필요 시 RCA를 수행하여 설계개선·주기조정·운전조건·교육·예비품 전략으로 환류한다.
7. `calibration_program_traceability` — 검교정 프로그램은 측정기능의 요구 정확도·허용오차, 교정방법, 기준기, 추적성, 환경조건, 주기, 기록 및 합격기준을 정의하여 측정결과의 신뢰성을 유지해야 한다.
8. `calibration_interval_risk_history` — 교정주기는 모든 계측기에 동일하게 적용하지 않고 측정 중요도, 안정성, drift 이력, 사용빈도, 환경, 제조사 권고, 법규 및 as-found 결과를 근거로 단축·유지·연장한다.
9. `calibration_as_found_as_left_oot` — 교정에서는 조정 전 As-Found 값과 조정·교정 후 As-Left 값을 구분해 기록하고, 허용오차를 벗어난 Out-of-Tolerance가 발견되면 영향기간과 관련 공정·품질 데이터의 유효성을 평가해야 한다.
10. `calibration_reference_standard_control` — 교정용 기준기는 피교정기의 요구 불확도와 허용오차에 적합한 성능을 가져야 하며, 유효한 교정상태·식별·환경조건·보관·사용이력과 상위표준에 대한 추적성을 관리해야 한다.
11. `inspection_program_routine_functional_loop` — 점검 프로그램은 외관·전원·배선·접지·배관·누설·환경상태 같은 Routine Inspection과 기능시험, Loop Check, 인터록·알람 시험 등 기능검증을 목적과 위험에 따라 구분해 계획한다.
12. `inspection_findings_defect_priority_closeout` — 점검에서 발견된 결함은 안전·생산·품질 영향과 열화속도에 따라 우선순위를 정하고, 즉시조치·계획정비·운전제한·임시대책을 결정한 뒤 Work Order와 재시험으로 종결을 확인해야 한다.
13. `deferred_maintenance_risk_control` — 정비 또는 점검을 계획일에 수행하지 못해 Deferred Maintenance가 발생하면 단순 연기가 아니라 위험평가, 임시보호조치, 승인, 새로운 기한과 추적책임을 명확히 해야 한다.
14. `spares_criticality_classification` — 예비품은 사용빈도보다 자산 criticality, 고장 시 생산·안전 영향, 조달 Lead Time, 수리 가능성, 대체 가능성, 단종위험을 고려해 Critical Spare와 일반 Spare를 분류한다.
15. `spares_stock_policy_reorder_leadtime` — 예비품 재고수준은 예상수요, 고장률, Lead Time, 최소 주문량, 수리 turnaround, 공용화 가능성, 서비스 수준과 재고비용을 고려해 min/max, reorder point 또는 동등한 보충정책으로 관리한다.
16. `spares_preservation_shelf_life_rotation` — 보유 예비품은 단순 수량뿐 아니라 보관환경, 방습·방진, 배터리·전해콘덴서 등 shelf-life, 정기 기능확인, firmware·license 상태와 선입선출·rotation을 관리해야 실제 고장 시 사용 가능하다.
17. `spares_obsolescence_substitution_moc` — 단종·노후화 부품은 Last-Time Buy, 호환 대체품, repair service, redesign과 migration 대안을 검토하되, 대체품 적용은 I/O·통신·전원·기능·안전·환경·software/firmware 호환성을 확인하고 변경관리와 시험을 거쳐야 한다.
18. `kpi_mtbf_definition_boundary` — MTBF는 수리 가능한 자산에서 운전시간을 해당 기간의 고장횟수로 나눈 평균 고장간 운전시간의 대표 지표이며, 고장 정의와 관찰기간·운전시간 경계를 일관되게 해야 비교가 의미 있다.
19. `kpi_mttr_definition_boundary` — MTTR은 고장 후 복구에 소요되는 평균시간을 나타내며 조직의 정의에 따라 진단·수리·시험·복구 승인 시간을 포함할 수 있으므로 시작·종료 기준과 대기시간 포함 여부를 명확히 해야 한다.
20. `kpi_intrinsic_availability_equation` — 단순한 수리 가능 2상태 모델에서 고유가용도는 A_i=MTBF/(MTBF+MTTR)로 표현할 수 있지만, 실제 운영가용도에는 예방정비·물류대기·행정지연·계획정지 등 추가 시간요소가 포함될 수 있어 지표 정의를 구분해야 한다.
21. `kpi_pm_compliance_backlog_schedule` — 유지보수 관리 KPI는 MTBF·MTTR·가용도 외에도 PM Compliance, Schedule Compliance, Maintenance Backlog, 긴급정비 비율 등을 사용할 수 있으며, 각 지표는 목표·분모·제외조건과 데이터 수집규칙을 먼저 정의해야 한다.
22. `kpi_gaming_single_metric_tradeoff` — 단일 KPI를 목표로 최적화하면 고장 미등록, 정비 조기종결, 과잉 예방정비 같은 왜곡이 생길 수 있으므로 신뢰성·복구성·비용·안전·생산영향을 균형 있게 보고 원자료와 정의를 감사해야 한다.
23. `maintenance_data_quality_cmms_taxonomy` — CMMS/EAM 또는 동등한 관리체계의 유지보수 데이터는 자산ID, failure code, 작업유형, 시작·종료시간, downtime, 사용부품, 원인·조치 등을 표준 taxonomy로 기록해야 KPI와 RCA가 재현 가능하다.
24. `maintenance_roles_competence_permit_restoration` — 정비 작업은 운전·정비·계측·전기·안전·협력사 간 역할과 승인권한을 정의하고, 필요한 역량·교육, 작업허가·격리·LOTO, bypass 관리와 작업 후 기능확인·복구승인을 포함해야 한다.
25. `maintenance_configuration_backup_change_handoff` — 제어시스템 정비 전후에는 현재 configuration과 backup, setpoint·logic·firmware·network 설정의 변경 여부를 확인하고, 변경이 발생하면 승인된 변경관리와 as-built 문서 갱신으로 handoff해야 한다.
26. `om_continuous_improvement_pdca_lifecycle_cost` — 운영·유지보수 체계는 KPI, 고장이력, 교정 OOT, 점검결함, 예비품 소진, RCA 결과를 정기 review하여 정비전략·주기·재고·설계·교육을 개선하고, 신뢰성·가용도뿐 아니라 lifecycle cost와 생산·안전효과를 함께 평가하는 폐루프로 운영한다.

## 12. Fatal Wrong Claims

총 `14`개 Fatal contract를 사용한다.

1. `om_fatal_run_to_failure_for_all` — 모든 계측제어 자산은 고장 후 수리하는 Run-to-Failure가 항상 가장 경제적이므로 criticality나 예방정비를 고려할 필요가 없다.
   - Correction: 정비전략은 자산 criticality, 고장영향, 상태와 비용을 기준으로 Corrective·Preventive·CBM·Predictive를 조합해야 한다.
2. `om_fatal_price_only_criticality` — 정비 우선순위와 Critical Spare 여부는 장비 단가만으로 결정하면 된다.
   - Correction: 안전·생산·품질 영향, 고장확률, 복구시간, 대체 가능성, lead time과 단종위험을 포함한 criticality/risk가 기준이 되어야 한다.
3. `om_fatal_calibration_equals_adjustment` — 교정은 계측기의 zero와 span을 조정하는 작업과 완전히 동일하다.
   - Correction: Calibration은 기준과 비교하여 오차와 적합성을 확인·기록하는 활동이며 조정은 필요 시 별도 수행될 수 있다.
4. `om_fatal_fixed_calibration_interval` — 모든 계측기는 설비조건과 이력에 관계없이 동일한 고정주기로 교정해야 하며 as-found 결과로 주기를 조정하면 안 된다.
   - Correction: 교정주기는 중요도, drift 이력, 환경, 법규, 제조사 권고와 as-found 결과에 따라 위험기반으로 조정할 수 있다.
5. `om_fatal_ignore_as_found_oot` — 교정 후 As-Left가 허용범위에 들어오면 이전 As-Found OOT와 과거 공정·품질 데이터 영향은 검토할 필요가 없다.
   - Correction: As-Found OOT는 영향기간과 관련 측정결과의 유효성에 대한 영향평가가 필요하다.
6. `om_fatal_visual_inspection_equals_function_test` — 외관점검이 정상인 계측 Loop는 기능시험이나 Loop Check 없이도 기능이 정상이라고 확정할 수 있다.
   - Correction: 외관·환경 점검과 기능시험·Loop Check·알람/인터록 검증은 목적이 다르므로 필요한 검증을 별도로 수행해야 한다.
7. `om_fatal_more_pm_always_better` — 예방정비 횟수를 늘릴수록 설비 신뢰성은 항상 향상되므로 정비주기는 가능한 한 짧게 해야 한다.
   - Correction: 과잉정비는 비용·인적오류·초기고장을 늘릴 수 있어 고장이력, 상태와 risk를 근거로 적정 주기를 정해야 한다.
8. `om_fatal_low_usage_zero_spares` — 사용빈도가 낮은 예비품은 lead time이나 고장영향과 관계없이 재고를 0으로 유지하는 것이 항상 최적이다.
   - Correction: Critical spare 재고는 수요빈도뿐 아니라 고장영향, lead time, 대체·수리 가능성, 단종위험과 재고비용을 함께 고려해야 한다.
9. `om_fatal_inventory_count_only` — 창고에 예비품 수량만 확보되어 있으면 shelf-life, 보관환경, firmware나 기능상태는 관리하지 않아도 된다.
   - Correction: 예비품은 보관환경, shelf-life, 기능확인, firmware/license와 호환상태까지 관리해야 실제 사용 가능성을 확보할 수 있다.
10. `om_fatal_uncontrolled_substitution` — 단종부품은 part number나 외형이 비슷한 대체품으로 시험이나 변경관리 없이 즉시 교체해도 된다.
   - Correction: 대체품은 전원·I/O·통신·기능·안전·환경·software/firmware 호환성을 검증하고 승인된 변경관리와 시험을 거쳐야 한다.
11. `om_fatal_mtbf_alone_proves_availability` — MTBF가 증가하면 MTTR과 정지형태를 보지 않아도 실제 운영가용도가 반드시 같은 비율로 좋아진다.
   - Correction: 가용도는 고장간격뿐 아니라 복구시간과 계획정지·물류대기 등 정의된 downtime 구조에 영향을 받으므로 MTBF 단독으로 판단할 수 없다.
12. `om_fatal_availability_formula_universal` — A=MTBF/(MTBF+MTTR)은 계획정지, 물류대기, 행정지연을 포함한 모든 가용도 정의에 조건 없이 적용되는 범용식이다.
   - Correction: MTBF/(MTBF+MTTR)은 단순 수리 가능 2상태 모델의 고유가용도 대표식이며 운영가용도는 추가 downtime 요소와 정의를 포함할 수 있다.
13. `om_fatal_mttr_hands_on_only_universal` — MTTR은 모든 조직에서 공구를 사용하는 순수 수리시간만 뜻하므로 시작·종료와 대기시간의 정의가 필요 없다.
   - Correction: MTTR은 조직의 복구 프로세스 정의에 따라 진단·수리·시험·복구시간 범위가 달라질 수 있으므로 시간경계를 명시해야 한다.
14. `om_fatal_single_kpi_optimization` — 유지보수 성과는 MTBF 같은 단일 KPI 하나만 최대화하면 안전·비용·생산 영향과 관계없이 최적이라고 판단할 수 있다.
   - Correction: KPI는 정의와 원자료를 감사하고 MTBF·MTTR·가용도·PM compliance·backlog·비용·안전 등 균형된 지표와 실제 결과를 함께 평가해야 한다.

## 13. Routing aliases

- `control system operations maintenance management`
- `instrumentation operations maintenance program`
- `instrumentation maintenance management`
- `control system preventive maintenance program`
- `instrument calibration management program`
- `instrumentation calibration interval management`
- `instrument inspection maintenance program`
- `control system inspection maintenance planning`
- `instrumentation critical spare management`
- `control system spare parts inventory management`
- `maintenance KPI MTBF MTTR availability`
- `instrumentation maintenance KPI management`
- `계측제어 시스템 운영 유지보수 관리`
- `계측제어 예방정비 관리`
- `계측기 검교정 주기 관리`
- `계측제어 점검 정비계획`
- `계측제어 예비품 재고 관리`
- `유지보수 KPI MTBF MTTR 가용도`

## 14. Routing field points

- 계측제어 자산대장·Tag·system boundary·configuration reference 관리
- Corrective·Preventive·Condition-Based·Predictive Maintenance 전략 구분
- Criticality·Risk 기반 정비 우선순위와 자원배분
- 정비 task·interval·window·acceptance criteria 관리
- Work Order·failure code·정비이력·RCA·Bad Actor 폐루프
- 검교정 tolerance·reference standard·traceability·acceptance criteria
- Calibration interval과 drift·as-found 이력 기반 주기 최적화
- As-Found·As-Left·Out-of-Tolerance 영향평가
- Routine Inspection·Functional Test·Loop Check 구분
- Inspection finding·defect priority·retest·closeout
- Deferred Maintenance risk assessment와 승인·추적
- Critical Spare·Lead Time·substitutability·obsolescence 분류
- Min/Max·Reorder Point·Lead Time 기반 예비품 재고정책
- Shelf-life·보관환경·rotation·firmware/license 예비품 보존
- Obsolescence·대체품 compatibility·MOC handoff
- MTBF·MTTR의 정의와 데이터 boundary
- Intrinsic Availability와 Operational Availability의 구분
- PM Compliance·Schedule Compliance·Backlog·Emergency Maintenance KPI
- KPI gaming 방지와 reliability·cost·safety balanced review
- CMMS/EAM data quality·taxonomy·failure history
- 역할·역량·작업허가·LOTO·bypass·복구승인
- 정비 전후 configuration·backup·as-built 변경관리 handoff
- KPI·OOT·결함·spares·RCA 기반 PDCA와 lifecycle cost 최적화

## 15. Expected question patterns

1. 계측제어시스템의 운영 및 유지보수 관리체계를 설명하시오.
   - intent: 자산경계부터 정비전략, 검교정, 점검, 예비품, KPI와 개선폐루프를 설계한다.
   - required anchors: om_asset_register_system_boundary, maintenance_strategy_corrective_preventive_condition_predictive, maintenance_criticality_risk_prioritization, maintenance_plan_task_interval_basis, work_order_history_closed_loop, om_continuous_improvement_pdca_lifecycle_cost
2. 제어시스템 예방정비와 상태기반·예지정비의 적용기준을 설명하시오.
   - intent: 정비전략을 trigger basis와 risk로 구분하고 주기를 최적화한다.
   - required anchors: maintenance_strategy_corrective_preventive_condition_predictive, maintenance_criticality_risk_prioritization, maintenance_plan_task_interval_basis, failure_coding_rca_bad_actor_feedback
3. 계측기 검교정 관리계획과 교정주기 결정기준을 설명하시오.
   - intent: calibration program, interval, as-found/as-left, OOT와 기준기 통제를 설명한다.
   - required anchors: calibration_program_traceability, calibration_interval_risk_history, calibration_as_found_as_left_oot, calibration_reference_standard_control
4. 계측제어 설비의 점검 종류와 결함조치 절차를 설명하시오.
   - intent: routine inspection, functional test, loop check와 finding closeout을 설명한다.
   - required anchors: inspection_program_routine_functional_loop, inspection_findings_defect_priority_closeout, deferred_maintenance_risk_control, work_order_history_closed_loop
5. 계측제어 예비품의 Critical Spare 선정과 재고관리 방법을 설명하시오.
   - intent: criticality, lead time, stock policy, preservation과 obsolescence를 설계한다.
   - required anchors: spares_criticality_classification, spares_stock_policy_reorder_leadtime, spares_preservation_shelf_life_rotation, spares_obsolescence_substitution_moc
6. MTBF, MTTR, Availability의 의미와 유지보수 KPI 적용 시 유의사항을 설명하시오.
   - intent: metric definitions, intrinsic availability equation과 운영 KPI boundary를 설명한다.
   - required anchors: kpi_mtbf_definition_boundary, kpi_mttr_definition_boundary, kpi_intrinsic_availability_equation, kpi_gaming_single_metric_tradeoff
7. 제어시스템 유지보수 KPI 체계를 설계하고 개선에 활용하는 방법을 설명하시오.
   - intent: 결과·프로세스 KPI와 data quality, review feedback loop를 설계한다.
   - required anchors: kpi_mtbf_definition_boundary, kpi_mttr_definition_boundary, kpi_intrinsic_availability_equation, kpi_pm_compliance_backlog_schedule, kpi_gaming_single_metric_tradeoff, maintenance_data_quality_cmms_taxonomy, om_continuous_improvement_pdca_lifecycle_cost
8. 교정 결과 Out-of-Tolerance 발생 시 관리 절차를 설명하시오.
   - intent: as-found, impact period, measurement validity, corrective action과 interval feedback을 설명한다.
   - required anchors: calibration_as_found_as_left_oot, calibration_interval_risk_history, work_order_history_closed_loop, failure_coding_rca_bad_actor_feedback
9. 계측제어시스템 단종 대응과 예비품 수명주기 관리방법을 설명하시오.
   - intent: obsolescence risk, last-time buy, substitution, compatibility와 change handoff를 설명한다.
   - required anchors: spares_criticality_classification, spares_preservation_shelf_life_rotation, spares_obsolescence_substitution_moc, maintenance_configuration_backup_change_handoff
10. 운영 중 정비계획을 생산·안전·비용과 연계하여 최적화하는 방법을 설명하시오.
   - intent: criticality, deferred maintenance, KPI와 lifecycle cost의 trade-off를 평가한다.
   - required anchors: maintenance_criticality_risk_prioritization, maintenance_plan_task_interval_basis, deferred_maintenance_risk_control, kpi_pm_compliance_backlog_schedule, kpi_gaming_single_metric_tradeoff, om_continuous_improvement_pdca_lifecycle_cost

## 16. Semantic review requirements

- Asset register와 criticality를 먼저 정의한다.
- Maintenance strategy를 corrective/preventive/CBM/predictive로 구분한다.
- Calibration과 adjustment를 구분한다.
- As-Found·As-Left·OOT impact assessment를 유지한다.
- Routine inspection과 functional/loop test를 구분한다.
- Spare stock을 consequence·lead time·obsolescence와 연결한다.
- MTBF·MTTR·Availability의 metric boundary를 정의한다.
- `A_i=MTBF/(MTBF+MTTR)`의 적용조건을 유지한다.
- KPI gaming을 방지하고 balanced review를 수행한다.
- Data quality와 taxonomy를 KPI·RCA의 기반으로 본다.
- Historical frequency는 근거가 없어 사용하지 않는다.

## 17. Lane boundary

이 STEP 1에서는 다음 파일만 생성한다.

1. Topic Sheet
2. README.md
3. fact_anchor.json
4. logic_check.json
5. model_answer.json
6. topic_importance.json

다음은 수정하지 않는다.

- `rubrics/generated/**`
- 공용 classification/release 정책
- production Python
- 다른 Topic Pack
- `docs/exam_scope/**`
- focused regression test는 STEP 2에서 별도 작성한다.
