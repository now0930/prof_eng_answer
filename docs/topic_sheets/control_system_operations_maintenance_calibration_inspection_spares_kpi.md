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

Critical Spare는 중요 자산을 복구하는 데 해당 부품이 필요한지와 자산 고장 결과를 기준으로 위험판단한다. NASA의 시설 RCM 자료는 안전·환경·임무 영향, redundancy, 높은 수리비나 과도한 spare 조달시간 등을 criticality 요소·예시로 든다. 범주와 가중치는 현장별로 정하며 보편 알고리즘으로 단정하지 않는다.

- safety, environment, operations or mission failure consequence
- credible failure and need to restore the critical asset
- available redundancy or alternative means
- procurement and repair lead time
- site-specific additional factors such as repairability, substitution and obsolescence

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

ISO 14224:2016은 석유·천연가스·석유화학 산업의 신뢰성·정비 데이터에 대해 equipment taxonomy/attributes, failure cause/consequence, maintenance action/resources/consequence/downtime 범주와 표준 형식, 데이터 품질 관리·보증 지침을 제시한다. 이 표준은 CMMS/EAM 제품의 사용을 이름으로 요구하지 않으며, 모든 사업장의 추가 work-order 필드나 KPI·RCA의 분석 재현성을 보증하지 않는다.

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

1. `om_asset_register_system_boundary` — ISO 14224 범위에서 장비 식별번호는 기능과 물리적 위치를 식별하며, 신뢰성·정비 데이터에는 taxonomy와 관련 장비속성이 포함된다. 이는 모든 계측자산의 보편적 CMMS 필드 목록을 정하지 않는다.
2. `maintenance_strategy_corrective_preventive_condition_predictive` — Corrective는 고장 검출 후 복구, Preventive는 열화·고장확률 저감, CBM은 물리적 상태 평가 기반 예방정비, Predictive는 이력 데이터와 알려진 미래 운전변수로 추정·계산한 미래 상태 예측에 기반한다. 이 표준 용어 정의만으로 자산별 전략·주기를 정할 수 없다.
3. `maintenance_criticality_risk_prioritization` — 위험기반 정비 우선순위에는 가능성뿐 아니라 결과·영향을 고려하고, 자산관리 의사결정 기준은 조직 목표·적용범위에 맞게 정의한다. 표준은 보편적인 계측자산 영향요소 목록이나 가중치를 정하지 않는다.
4. `maintenance_plan_task_interval_basis` — ISO 14224:2016은 정비계획을 유지보수에 필요한 활동·절차·자원·기간을 포함하는 구조화·문서화된 작업 집합으로 정의한다. 이 정의만으로 사업장별 작업·주기·안전조치·정지창을 보편적으로 정하지 않는다.
5. `work_order_history_closed_loop` — ISO 14224 범위의 고장자료는 원인·결과, 정비자료는 조치·사용자원·정비결과·downtime을 다루며, 표준화 형식은 신뢰성·정비 데이터의 교환·분석을 돕는다. 현장 Work Order workflow와 추가 필드는 사업장 정의 사항이다.
6. `failure_coding_rca_bad_actor_feedback` — ISO 14224:2016의 적용 산업에서 failure cause/consequence 범주와 표준 형식, failure mode의 분석 활용을 설명한다. Bad Actor 기준·RCA 실행·개선 환류 방식은 표준이 규정하지 않으므로 사업장별로 정한다.
7. `calibration_program_traceability` — 추적성은 불확도를 기여하는 문서화된 교정 사슬로 측정결과를 기준에 연결하는 특성이며, 용도적합성과 동일하지 않다. 재교정 주기는 정확도 요구·외부 요구·기기 안정성·환경·이력을 고려하며 NIST는 보편 주기를 정하지 않는다.
8. `calibration_interval_risk_history` — 교정주기는 모든 계측기에 동일하게 적용하지 않고 측정 중요도, 안정성, drift 이력, 사용빈도, 환경, 제조사 권고, 법규 및 as-found 결과를 근거로 단축·유지·연장한다.
9. `calibration_as_found_as_left_oot` — 교정에서는 조정 전 As-Found 값과 조정·교정 후 As-Left 값을 구분해 기록하고, 허용오차를 벗어난 Out-of-Tolerance가 발견되면 영향기간과 관련 공정·품질 데이터의 유효성을 평가해야 한다.
10. `calibration_reference_standard_control` — 교정용 기준기는 피교정기의 요구 불확도와 허용오차에 적합한 성능을 가져야 하며, 유효한 교정상태·식별·환경조건·보관·사용이력과 상위표준에 대한 추적성을 관리해야 한다.
11. `inspection_program_routine_functional_loop` — 점검 프로그램은 외관·전원·배선·접지·배관·누설·환경상태 같은 Routine Inspection과 기능시험, Loop Check, 인터록·알람 시험 등 기능검증을 목적과 위험에 따라 구분해 계획한다.
12. `inspection_findings_defect_priority_closeout` — OSHA PSM 적용 공정의 기계적 건전성 대상 설비에서 허용한계 초과 결함은 추가 사용 전 또는 안전 확보 조치하에 시정해야 한다. 이를 보편적인 위험 우선순위·Work Order·재시험 규정으로 확대하지 않는다.
13. `deferred_maintenance_risk_control` — HSE offshore functional-safety 지침의 SIS deferral 절차, 검토·승인 역할, 위험평가·모니터링, 연기기간·누적위험 고려 권고를 해당 적용범위로 설명한다. 이를 모든 정비의 법적 보편요건으로 확대하지 않는다.
14. `spares_criticality_classification` — Critical Spare는 중요 자산 복구 필요성, 고장 결과, redundancy와 procurement/repair lead time을 고려해 자산별로 분류한다. 범주·가중치와 추가요인은 현장별이며, 사용빈도·가격 단독 기준이나 보편 알고리즘으로 단정하지 않는다.
15. `spares_stock_policy_reorder_leadtime` — 예비품 재고수준은 예상수요, 고장률, Lead Time, 최소 주문량, 수리 turnaround, 공용화 가능성, 서비스 수준과 재고비용을 고려해 min/max, reorder point 또는 동등한 보충정책으로 관리한다.
16. `spares_preservation_shelf_life_rotation` — 보유 예비품은 단순 수량뿐 아니라 보관환경, 방습·방진, 배터리·전해콘덴서 등 shelf-life, 정기 기능확인, firmware·license 상태와 선입선출·rotation을 관리해야 실제 고장 시 사용 가능하다.
17. `spares_obsolescence_substitution_moc` — 단종·노후화 부품은 Last-Time Buy, 호환 대체품, repair service, redesign과 migration 대안을 검토하되, 대체품 적용은 I/O·통신·전원·기능·안전·환경·software/firmware 호환성을 확인하고 변경관리와 시험을 거쳐야 한다.
18. `kpi_mtbf_definition_boundary` — MTBF는 수리 가능한 자산에서 운전시간을 해당 기간의 고장횟수로 나눈 평균 고장간 운전시간의 대표 지표이며, 고장 정의와 관찰기간·운전시간 경계를 일관되게 해야 비교가 의미 있다.
19. `kpi_mttr_definition_boundary` — ISO 14224/ISO/TR 12489에서 MTTR 수리시간과 MTTRes 전체 복구시간을 구분하고, fault-detection 및 return-to-service 경계를 명시한다. 약어 MTTR을 두 뜻으로 혼용하지 않는다.
20. `kpi_intrinsic_availability_equation` — 단순한 수리 가능 2상태 모델에서 고유가용도는 A_i=MTBF/(MTBF+MTTR)로 표현할 수 있지만, 실제 운영가용도에는 예방정비·물류대기·행정지연·계획정지 등 추가 시간요소가 포함될 수 있어 지표 정의를 구분해야 한다.
21. `kpi_pm_compliance_backlog_schedule` — 유지보수 관리 KPI는 MTBF·MTTR·가용도 외에도 PM Compliance, Schedule Compliance, Maintenance Backlog, 긴급정비 비율 등을 사용할 수 있으며, 각 지표는 목표·분모·제외조건과 데이터 수집규칙을 먼저 정의해야 한다.
22. `kpi_gaming_single_metric_tradeoff` — 성과지표는 목표와 연계되고 명확한 정의를 가져야 하며, 지표 집합은 핵심 우선순위를 균형 있게 포함해야 한다. 단일 성과지표에 과도하게 의존하거나 이를 보상·자원배분과 연결하면 목표와 어긋난 행동 및 지표 조작 유인이 생길 수 있다. GAO의 일반 지침이며 정비 KPI의 특정 사례나 보편 산식은 아니다.
23. `maintenance_data_quality_cmms_taxonomy` — ISO 14224:2016의 신뢰성·정비 데이터 범주, 표준 형식 및 데이터 품질 지침을 해당 산업 범위에서 설명하고, CMMS/EAM 선택 또는 KPI·RCA 분석 보증과 구분한다.
24. `maintenance_roles_competence_permit_restoration` — OSHA 29 CFR 1910.147 적용범위의 위험에너지 관리·교육·정기점검·격리확인·안전한 해제/재가동과 1910.119 적용 공정의 안전작업·교육·협력사 통제를 설명한다. 이를 보편적인 작업허가·SIS bypass 승인·기능시험 의무로 확대하지 않는다.
25. `maintenance_configuration_backup_change_handoff` — NIST SP 800-82 Rev.3은 OT 구성 변경의 배포 전 기록·시험·승인과 변경 추적을, SP 1339(2026)는 backup의 변경관리 연계·정기 생성·시험·복구연습 검토를 권고한다. 변경통제 범위와 backup 대상·주기는 시스템별로 정하며, 모든 정비작업에 같은 전후 baseline/backup 점검을 보편 규칙으로 두지 않는다.
26. `om_continuous_improvement_pdca_lifecycle_cost` — ISO 55001:2024 자산관리시스템 개선 및 비용·위험·성과 균형, ISO 55000:2024의 자산수명주기 가치 원칙을 설명하되, 특정 KPI/OOT/예비품 input·review 주기·조치를 보편 절차로 확대하지 않는다.

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
