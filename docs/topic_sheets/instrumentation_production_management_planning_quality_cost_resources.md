# 계측·제어 생산관리: 생산계획, 능력·일정, 품질·원가, 자원 및 성과관리

## 1. Topic metadata

- `topic_id`: `instrumentation_production_management_planning_quality_cost_resources`
- `official_criterion`: `IC-2027-W-4-5`
- `question_type`: `IMPLEMENTATION_EVALUATION`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `NORMAL`
- `historical_frequency_used`: `false`
- `semantic_execution`: `LLM_ONLY`

## 2. STEP 0 ownership conclusion

STEP 0에서 기존 `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` Topic을 직접 비교했다.

결과:

- MES/data-system signal: 8
- production-management direct signal: 0
- narrow production duplicate blocker: 0
- proposed routing alias collision: 0

따라서 신규 Topic은 데이터 플랫폼이 아니라 **생산운영 의사결정과 관리체계**를 독립 소유한다.

인접 Topic handoff는 다음 ID로 고정한다.

- O&M 관리: `control_system_operations_maintenance_calibration_inspection_spares_kpi`
- 프로젝트 관리: `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`

## 3. Production Management flow

`Demand / Order → Planning Horizon → Capacity / Schedule → Material / Manpower / Equipment → Quality / Cost → KPI → Daily Review / PDCA`

## 4. Planning / Takt / Capacity

Takt Time 대표관계:

`Takt Time = Available Production Time / Customer Demand`

Cycle Time은 실제 공정 처리시간 또는 unit discharge interval이다.

Takt와 Cycle Time을 비교해 수요충족 가능성을 판단한다.

Capacity는 nameplate가 아니라 available time, actual cycle/rate, planned downtime과 resource constraint를 반영한다.

Line throughput은 bottleneck과 blocking/starvation에 제한될 수 있다.

## 5. Scheduling / Changeover / WIP

단기일정은 finite-capacity 관점으로 작성한다.

- Equipment availability
- Manpower / Skill
- Material availability
- Tooling
- Precedence
- Due date
- Changeover

Changeover가 크면 sequence와 batch size가 중요하다.
큰 batch는 setup loss를 줄일 수 있지만 WIP·lead time·inventory를 증가시킬 수 있다.

## 6. Resource Planning

### Material

BOM, production plan, inventory, lead time과 lot/alternative condition을 연결한다.

### Manpower

표준작업량, shift, skill matrix, 휴무·교육·자격을 반영한다.

### Equipment

생산계획에는 available time과 capability를 반영한다.
maintenance strategy와 MTBF/MTTR은 Topic 2로 handoff한다.

## 7. Quality Management

품질요구를 CTQ·specification·control item·inspection·reaction plan으로 전개한다.

주요 KPI:

- FPY
- Yield
- Scrap
- Rework

불량 발생 시 lot·time·equipment·process·material을 추적하여 containment한다.

MES genealogy는 근거 data를 제공할 수 있지만 생산판정과 격리의 책임을 자동으로 대체하지 않는다.

## 8. Production Cost

생산원가는 목적에 따라 다음을 포함할 수 있다.

- Direct Material
- Direct Labor
- Manufacturing Overhead
- Energy / Utility
- Consumables
- Scrap / Rework loss

Standard/Plan Cost와 Actual Cost를 비교해 variance를 material, labor, yield, energy, downtime 원인으로 분해한다.

Project estimate/budget control은 Topic 3로 handoff한다.

## 9. KPI

### OEE

대표식:

`OEE = Availability × Performance × Quality`

각 요소의 시간·속도·양품 기준을 같은 planned-production context에서 정의한다.

OEE 하나만으로 납기·원가·안전·수요대응을 모두 평가하지 않는다.

### Flow / Delivery KPI

- Throughput
- Cycle Time
- Lead Time
- WIP
- Schedule Adherence
- On-Time Completion / Delivery

각 지표는 공정경계·due date·freeze point와 분모를 명확히 정의한다.

## 10. MES / ERP / Historian boundary

ERP는 주문·계획·자재·원가와 기업자원 데이터를 제공한다.
MES는 작업지시·현장실적·품질·자원·Genealogy를 연결한다.
Historian은 시계열 운영데이터를 보존한다.

하지만 실제 production capacity, sequence, priority, quality, cost, resource trade-off는 Production Management가 소유한다.

## 11. Daily Management / PDCA

Shift 또는 일일 단위로 다음을 review한다.

- Plan vs Actual
- Production quantity
- Quality
- Downtime
- Manpower
- Material shortage
- WIP
- Cost / loss
- Key abnormality

각 이슈는 owner·action·due date로 관리한다.
개선 후 Safety·Quality·Delivery·Cost를 함께 재검증한다.

## 12. Required Fact Anchors

총 `28`개 Anchor를 `fact_anchor.json` 정본으로 사용한다.

1. `production_management_objective_scope` — 생산관리는 고객·수요 요구를 안전·품질·납기·원가 목표와 생산능력·인력·자재·설비 제약에 맞춰 실행 가능한 생산계획으로 변환하고, 실적과 편차를 피드백하여 지속적으로 조정하는 운영관리 체계다.
2. `production_demand_order_plan_translation` — 생산계획은 수요·주문, 재고정책, 납기, 제품 Mix와 우선순위를 입력으로 받아 기간별 생산량과 품목구성을 정하며, 수요 변동과 공급 제약에 따라 rolling 방식으로 재계획할 수 있어야 한다.
3. `production_horizon_master_detailed_schedule` — 생산계획은 장·중기 자원계획, Master Production Schedule과 단기 상세일정처럼 시간 Horizon을 구분하고, 상위 계획의 생산량·납기 목표를 하위 작업순서와 작업지시로 점진적으로 구체화해야 한다.
4. `production_takt_cycle_time_boundary` — Takt Time은 일반적으로 가용 생산시간을 고객 요구수량으로 나눈 수요 기준 속도이고, Cycle Time은 실제 공정 또는 설비가 한 단위를 처리하는 데 걸리는 시간 또는 단위 배출간격이므로 서로 구분하여 비교해야 한다.
5. `production_capacity_available_time_rate` — 생산능력은 가용시간, 설비·인력 수, 표준 Cycle Time 또는 처리율, 계획정지와 현실적 효율을 기준으로 산정하며, 이론능력과 실제 유효능력을 구분해 병목과 납기 가능성을 판단해야 한다.
6. `production_bottleneck_throughput_constraint` — 연속된 공정의 지속 가능한 Throughput은 일반적으로 가장 제약이 큰 Bottleneck의 유효능력과 차단·기아·buffer 상태에 의해 제한되므로, 비병목 설비의 국부 효율만 높여도 전체 생산량이 같은 비율로 증가하는 것은 아니다.
7. `production_line_balancing_workload` — 라인 밸런싱은 작업요소와 표준시간을 작업장·설비에 배분하여 Takt 요구를 만족시키면서 공정 간 유휴·과부하와 병목을 줄이는 활동이며, precedence와 작업자·설비 제약을 함께 고려해야 한다.
8. `production_finite_capacity_schedule_dispatch` — 단기 생산일정은 설비·인력·금형·치공구·자재의 실제 가용성과 changeover, 선후관계, due date를 반영하는 finite-capacity 관점으로 작성하고, 현장 dispatching rule은 상위 납기·우선순위와 모순되지 않게 운영해야 한다.
9. `production_changeover_sequence_batch_tradeoff` — 다품종 생산에서는 Changeover 시간과 순서의존성을 고려해 제품 Sequence와 Batch Size를 정해야 하며, 큰 Batch는 setup 손실을 줄일 수 있지만 WIP·Lead Time·재고와 수요변동 대응성을 악화시킬 수 있다.
10. `production_wip_flow_lead_time` — WIP는 공정 사이의 완충과 변동 흡수에 필요할 수 있지만 과도하면 흐름을 가리고 Lead Time과 재고비용을 증가시키므로, Throughput·Cycle Time·buffer 용량과 함께 관리해야 한다.
11. `production_material_requirement_availability` — 자재관리는 BOM·생산계획·재고·Lead Time과 lot/대체품 조건을 이용해 소요량과 필요시점을 계산하고, 결품·과잉재고를 줄이도록 발주·공급·라인투입을 동기화해야 한다.
12. `production_manpower_skill_shift` — 인력계획은 생산량과 공정별 표준작업량, Shift, Skill Matrix, 휴무·교육·교대 제약을 반영해 필요한 인원과 배치를 정하고, 단순 인원수뿐 아니라 자격·숙련도와 다기능성을 함께 관리해야 한다.
13. `production_equipment_resource_availability` — 생산설비 자원계획은 생산에 실제 사용할 수 있는 설비의 가용시간, capability, tooling과 계획정지 정보를 반영하되, 고장정비 전략·MTBF·MTTR·예방정비 KPI 자체의 관리는 O&M Topic으로 handoff한다.
14. `production_quality_plan_ctq_spec` — 품질관리는 고객·제품 요구를 CTQ와 공정·검사 기준으로 전개하고, 공정단계별 specification·control item·sampling/inspection·reaction plan을 정의하여 생산계획과 동일한 제품·revision 기준으로 운영해야 한다.
15. `production_fpy_yield_scrap_rework` — 생산품질 KPI는 FPY, Yield, Scrap, Rework 등으로 불량과 손실을 구분할 수 있으며, 분모·재작업 포함여부·검사단계 정의를 일관되게 해야 제품·라인 간 비교가 의미 있다.
16. `production_process_quality_feedback` — 공정 품질은 검사결과와 공정변수의 trend·이상·관리한계 등을 이용해 이상을 조기에 검출하고, 이상 시 생산격리·조건확인·원인분석·복구·재발방지로 연결해야 하며 단순 검사수치 저장으로 끝나지 않아야 한다.
17. `production_defect_containment_traceability` — 불량 발생 시 영향 Lot·시간·설비·공정·자재를 추적해 의심범위를 격리하고, 선별·재작업·폐기와 원인·조치를 기록해야 하며 Traceability는 MES/Historian의 genealogy data를 활용할 수 있지만 생산판정과 containment 책임을 대체하지 않는다.
18. `production_cost_structure` — 생산원가는 목적과 회계정책에 따라 직접재료비, 직접노무비, 제조간접비와 에너지·소모품·불량·재작업 등으로 구성할 수 있으며, 어떤 비용을 단위원가에 포함하는지 기준을 일관되게 정의해야 한다.
19. `production_standard_actual_cost_variance` — 원가관리는 표준 또는 계획 원가와 Actual Cost를 비교하여 material usage·price, labor efficiency, scrap/rework, energy, downtime 등 variance의 원인을 분해하고 생산조건·계획·품질 개선으로 환류해야 한다.
20. `production_unit_cost_volume_yield` — 단위원가는 총 생산비용을 적절한 양품 생산량으로 나누는 방식 등으로 관리할 수 있으며, 생산량·Yield·Scrap·가동손실 변화가 분모와 비용구조에 미치는 영향을 함께 봐야 한다.
21. `production_energy_consumables_cost` — 에너지·Utility·소모품 사용량은 생산량, 제품 Mix, 설비상태와 운전조건에 따라 변하므로 단위제품당 사용량과 peak·idle loss를 함께 추적하여 원가와 효율개선에 반영할 수 있다.
22. `production_oee_apq_formula_boundary` — OEE는 통상 Availability×Performance×Quality의 곱으로 표현하며, 각 요소의 시간·속도·양품 기준을 동일한 planned production context에서 정의해야 하고, OEE 하나만으로 납기·원가·안전·수요대응을 모두 대표할 수는 없다.
23. `production_throughput_cycle_lead_wip_kpi` — Throughput, Cycle Time, Lead Time과 WIP는 서로 다른 흐름 KPI이므로 동일한 것으로 취급하지 않고, 공정경계와 측정시점을 정의하여 병목·대기·재공의 원인을 분석해야 한다.
24. `production_schedule_adherence_delivery_kpi` — 생산계획 준수율, Schedule Adherence, On-Time Completion/Delivery 등 납기 KPI는 계획 freeze 기준, due time, 완료판정과 분모를 정의하고, 긴급순서변경·결품·품질hold 같은 원인을 구분해 개선에 사용해야 한다.
25. `production_mes_data_handoff` — MES·Historian은 작업지시, 실적, 품질, 상태, genealogy와 시계열 데이터를 수집·전달하는 실행·정보 계층으로 활용할 수 있지만, 어떤 생산량·우선순위·capacity·quality·cost·resource 목표를 선택할지는 생산관리 의사결정이 소유한다.
26. `production_erp_mes_role_boundary` — ERP는 주문·수요·자재·원가·기업자원을 상위 수준에서 관리하고 MES는 제조실행과 현장실적을 연결할 수 있으며, 생산관리는 두 계층의 정보를 이용해 실제 capacity·sequence·quality·resource 제약을 반영한 실행계획을 조정한다.
27. `production_daily_management_visual_control` — Daily Production Management는 계획 대비 생산량, 품질, downtime, manpower, material shortage, WIP와 주요 이상을 짧은 주기로 review하고, owner·조치·due date를 명확히 하여 다음 Shift와 계획에 반영해야 한다.
28. `production_pdca_tradeoff_improvement` — 생산관리 개선은 Plan-Do-Check-Act 관점에서 수요·capacity·schedule·quality·cost·resource·KPI의 편차와 원인을 검토하고, 병목·작업방법·sequence·batch·자원배치·품질조건을 변경한 뒤 안전·품질·납기·원가 효과를 함께 재검증해야 한다.

## 13. Fatal Wrong Claims

총 `14`개 Fatal contract를 사용한다.

1. `production_fatal_max_output_only` — 생산관리는 생산량을 최대화하는 활동이므로 품질·납기·원가·안전과 자원제약은 부차적이다.
   - Correction: 생산관리는 수요를 안전·품질·납기·원가 목표와 capacity·resource 제약에 맞춰 실행 가능한 계획으로 최적화해야 한다.
2. `production_fatal_takt_equals_cycle` — Takt Time과 Cycle Time은 같은 개념이며 항상 같은 산식으로 계산된다.
   - Correction: Takt Time은 수요 기준 생산속도이고 Cycle Time은 실제 공정의 처리시간 또는 배출간격이므로 구분해야 한다.
3. `production_fatal_nameplate_equals_capacity` — 설비 정격속도와 근무시간만 곱하면 계획정지·인력·자재·효율과 관계없이 실제 생산능력을 정확히 알 수 있다.
   - Correction: 실제 유효능력은 가용시간, 실제 cycle/rate, 계획정지와 자원·운영 제약을 반영해 산정해야 한다.
4. `production_fatal_local_oee_guarantees_throughput` — 각 설비 OEE를 높이면 병목과 buffer 상태에 관계없이 line throughput이 같은 비율로 반드시 증가한다.
   - Correction: 시스템 throughput은 병목의 유효능력과 blocking·starvation·flow에 제한되므로 국부 OEE 향상과 전체생산량은 구분해야 한다.
5. `production_fatal_infinite_capacity_schedule` — 생산일정은 설비·인력·자재 가용성과 changeover를 확인하지 않고 주문순서대로 작성해도 실행 가능하다.
   - Correction: 단기 일정은 finite capacity와 실제 resource availability, precedence, changeover와 due date를 반영해야 한다.
6. `production_fatal_large_batch_always_best` — Changeover가 있는 공정에서는 Batch Size가 클수록 WIP·Lead Time·재고와 관계없이 항상 최적이다.
   - Correction: Batch Size는 setup 손실과 WIP·Lead Time·inventory·수요변동 대응성의 trade-off로 결정해야 한다.
7. `production_fatal_more_wip_always_better` — WIP를 늘릴수록 설비 starvation이 줄어들기 때문에 lead time과 생산성은 항상 동시에 좋아진다.
   - Correction: WIP는 변동 흡수에 도움을 줄 수 있지만 과도하면 lead time과 재고비용을 증가시키므로 flow 관점에서 적정 수준을 관리해야 한다.
8. `production_fatal_quality_final_inspection_only` — 최종검사에서 합격 여부만 확인하면 생산 중 CTQ, 공정관리항목과 reaction plan은 필요 없다.
   - Correction: 품질은 CTQ와 공정 control item·inspection·reaction plan을 공정단계에 전개하고 이상 시 즉시 containment·조치해야 한다.
9. `production_fatal_fpy_equals_final_yield` — FPY와 최종 Yield는 재작업 여부와 검사단계에 관계없이 항상 같은 값이다.
   - Correction: FPY는 first-pass 성과이고 최종 Yield는 재작업·검사경계에 따라 달라질 수 있으므로 정의와 분모를 구분해야 한다.
10. `production_fatal_material_cost_only` — 생산원가는 원재료비만 의미하므로 노무·간접비·에너지·불량·재작업 손실은 원가관리 대상이 아니다.
   - Correction: 생산원가는 목적에 따라 재료·노무·간접비와 에너지·불량·재작업 등 관련 비용항목을 정의해 관리해야 한다.
11. `production_fatal_oee_proves_all_performance` — OEE가 높으면 납기·원가·수요대응·안전·품질이 모두 자동으로 최적화됐다고 판단할 수 있다.
   - Correction: OEE는 Availability·Performance·Quality 기반의 설비효율 지표이며 납기·원가·안전·수요대응은 별도 KPI와 함께 평가해야 한다.
12. `production_fatal_flow_kpis_interchangeable` — Throughput, Cycle Time, Lead Time과 WIP는 모두 생산속도를 의미하므로 동일한 값처럼 서로 바꿔 사용해도 된다.
   - Correction: 네 지표는 서로 다른 물리·운영 의미를 가지므로 공정경계와 측정시점을 정의하여 구분해야 한다.
13. `production_fatal_mes_automates_management` — MES/Historian을 구축하면 생산량·우선순위·capacity·quality·cost·resource 의사결정이 자동으로 최적화되므로 생산관리 기능은 불필요하다.
   - Correction: MES/Historian은 실행·데이터 계층이고 생산계획·자원배분·품질·원가 trade-off는 별도의 production management 의사결정이 필요하다.
14. `production_fatal_project_or_maintenance_scope_takeover` — 생산관리 Topic이 프로젝트 투자예산·EPC 일정과 설비의 MTBF·MTTR·교정주기·예비품 정책까지 모두 직접 소유한다.
   - Correction: 양산 생산 schedule/cost/resource는 본 Topic이 소유하지만 프로젝트 cost/schedule은 Topic 3, maintenance·calibration·spares·MTBF/MTTR은 Topic 2로 handoff해야 한다.

## 14. Routing aliases

- `instrumentation production management planning quality cost resources`
- `instrumentation production planning capacity quality cost`
- `instrumentation production resource management`
- `production management for instrumentation control systems`
- `manufacturing production planning quality cost resources`
- `production capacity scheduling quality cost kpi`
- `instrumentation manufacturing performance management`
- `production plan capacity manpower material equipment`
- `production quality yield scrap cost resource management`
- `production performance oee throughput cycle time wip`
- `계측 생산관리 계획 품질 원가 자원`
- `계장 생산관리 생산계획 품질 원가`
- `계측 생산능력 일정 품질 비용 관리`
- `생산계획 자원배분 품질 원가 KPI`
- `생산능력 인력 자재 설비 자원관리`
- `생산 수율 불량 원가 생산성 관리`
- `OEE 생산성 수율 재공 생산관리`
- `계측제어 생산 운영 계획 성과관리`

## 15. Routing field points

- 수요·주문·재고정책·제품 Mix를 기간별 생산계획으로 변환
- Planning Horizon·MPS·단기 상세일정·작업지시 계층
- Takt Time과 Cycle Time의 정의·산식·역할 구분
- 가용시간·실제 Cycle Time·효율을 반영한 effective capacity
- Bottleneck·Blocking·Starvation과 line Throughput 제약
- Line Balancing·표준시간·Precedence·Takt
- Finite Capacity Scheduling·Dispatching·Due Date·Changeover
- Sequence-dependent setup·Batch Size·WIP·Lead Time trade-off
- Buffer·WIP·Flow·Lead Time 관리
- BOM·생산계획·재고·Lead Time 기반 material availability
- Shift·Skill Matrix·표준작업량 기반 manpower planning
- Equipment available time·capability·tooling과 O&M handoff
- CTQ·Specification·Control Item·Inspection·Reaction Plan
- FPY·Yield·Scrap·Rework의 metric boundary
- 공정품질 trend·관리한계·containment·corrective action
- Lot·설비·공정·자재 traceability와 defect containment
- 직접재료·노무·제조간접비·에너지·불량·재작업 production cost
- Standard Cost·Actual Cost·Variance analysis
- 양품 생산량·Yield·Scrap 변화와 Unit Cost
- 에너지·Utility·소모품의 specific consumption과 idle loss
- OEE=Availability×Performance×Quality와 적용한계
- Throughput·Cycle Time·Lead Time·WIP의 정의와 경계
- Schedule Adherence·On-Time Completion/Delivery와 원인분류
- MES/Historian execution-data layer와 production decision ownership 경계
- ERP order/resource layer·MES execution layer·production management 연계
- Daily Production Management·shift review·action owner·due date
- PDCA와 bottleneck·sequence·batch·resource allocation 개선
- Safety·Quality·Delivery·Cost 다목적 trade-off 검증

## 16. Expected question patterns

1. 생산관리의 기능과 생산계획·품질·원가·자원관리 체계를 설명하시오.
   - intent: 수요를 실행가능한 plan으로 변환하고 capacity·quality·cost·resource와 KPI를 폐루프로 관리한다.
   - required anchors: production_management_objective_scope, production_demand_order_plan_translation, production_capacity_available_time_rate, production_quality_plan_ctq_spec, production_cost_structure, production_manpower_skill_shift, production_pdca_tradeoff_improvement
2. 생산계획 수립 시 Takt Time, Cycle Time, 생산능력과 Bottleneck의 관계를 설명하시오.
   - intent: 수요속도와 공정속도, effective capacity와 시스템 제약을 연결한다.
   - required anchors: production_takt_cycle_time_boundary, production_capacity_available_time_rate, production_bottleneck_throughput_constraint, production_line_balancing_workload
3. 다품종 생산의 일정계획과 Changeover·Batch Size·WIP 관리방법을 설명하시오.
   - intent: finite capacity와 setup/sequence, batch, buffer/lead-time trade-off를 설계한다.
   - required anchors: production_finite_capacity_schedule_dispatch, production_changeover_sequence_batch_tradeoff, production_wip_flow_lead_time, production_schedule_adherence_delivery_kpi
4. 생산자원 계획에서 인력·자재·설비를 어떻게 관리하는지 설명하시오.
   - intent: BOM/lead time, skill/shift, available equipment capability를 schedule과 연결한다.
   - required anchors: production_material_requirement_availability, production_manpower_skill_shift, production_equipment_resource_availability, production_finite_capacity_schedule_dispatch
5. 생산품질 관리와 FPY, Yield, Scrap, Rework 지표의 활용방법을 설명하시오.
   - intent: CTQ/control plan, quality KPI boundary, process feedback와 containment를 설명한다.
   - required anchors: production_quality_plan_ctq_spec, production_fpy_yield_scrap_rework, production_process_quality_feedback, production_defect_containment_traceability
6. 생산원가의 구성과 원가절감 관리방법을 설명하시오.
   - intent: cost boundary, standard-actual variance, yield/volume, energy loss를 운영개선과 연결한다.
   - required anchors: production_cost_structure, production_standard_actual_cost_variance, production_unit_cost_volume_yield, production_energy_consumables_cost
7. OEE의 구성과 생산관리 KPI 적용 시 유의사항을 설명하시오.
   - intent: OEE A×P×Q와 flow/delivery KPI를 함께 보고 metric boundary와 한계를 설명한다.
   - required anchors: production_oee_apq_formula_boundary, production_throughput_cycle_lead_wip_kpi, production_schedule_adherence_delivery_kpi, production_pdca_tradeoff_improvement
8. MES·ERP·Historian과 생산관리의 역할 및 정보 흐름을 설명하시오.
   - intent: 데이터/실행 계층과 production decision ownership을 계층적으로 구분한다.
   - required anchors: production_mes_data_handoff, production_erp_mes_role_boundary, production_demand_order_plan_translation, production_defect_containment_traceability
9. 생산계획 대비 실적 편차가 발생할 때 개선 절차를 설명하시오.
   - intent: capacity·material·manpower·quality·cost·bottleneck 원인을 분류하고 daily management와 PDCA로 닫는다.
   - required anchors: production_daily_management_visual_control, production_capacity_available_time_rate, production_material_requirement_availability, production_manpower_skill_shift, production_process_quality_feedback, production_standard_actual_cost_variance, production_pdca_tradeoff_improvement
10. 프로젝트 관리·유지보수 관리·생산관리의 Cost, Schedule, Resource KPI ownership을 구분하시오.
   - intent: 양산 생산 schedule/cost/resource와 project/O&M의 lifecycle boundary를 설명한다.
   - required anchors: production_equipment_resource_availability, production_standard_actual_cost_variance, production_schedule_adherence_delivery_kpi, production_mes_data_handoff, production_pdca_tradeoff_improvement

## 17. Semantic review requirements

- 생산관리 목적을 SQDC와 resource constraint 통합관리로 설명한다.
- Takt Time·Cycle Time·effective capacity를 구분한다.
- Bottleneck과 line throughput을 연결한다.
- Finite capacity와 changeover·batch·WIP를 일정에 반영한다.
- 자재·인력·설비 resource planning을 구분한다.
- CTQ·FPY/Yield·Scrap/Rework·containment를 설명한다.
- Production cost boundary와 variance를 설명한다.
- OEE A×P×Q와 적용한계를 설명한다.
- Throughput·Cycle Time·Lead Time·WIP를 구분한다.
- MES/ERP/Historian data layer와 production decision ownership을 구분한다.
- Project management와 O&M management handoff를 유지한다.
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
