# 계측 프로젝트 관리: 기본설계, 원가·일정, 설계문서, 조달·시공 및 인수

## 1. Topic metadata

- `topic_id`: `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`
- `official_criterion`: `IC-2027-W-4-4`
- `question_type`: `IMPLEMENTATION_EVALUATION`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `NORMAL`
- `historical_frequency_used`: `false`
- `semantic_execution`: `LLM_ONLY`

## 2. STEP 0 ownership conclusion

기존 `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`는 URS·FRS·FDS·SDS, logic/HMI, FAT·SAT·commissioning 등 software-specific ownership이 강했다.

STEP 0 explicit comparison 결과:

- software-specific signal: 10
- instrumentation-wide signal: 0
- narrow project duplicate blocker: 0
- proposed routing alias collision: 0

따라서 신규 Topic은 software project와 별도로 instrumentation-wide project management를 소유한다.

## 3. Project lifecycle

`Requirements / Feasibility → Basic Design → Detailed Design → Procurement → Fabrication / Vendor Review → Construction → Mechanical Completion / Precommissioning → Acceptance / Handover → Closeout`

각 단계는 입력·산출물·승인기준을 갖는다.

## 4. Scope and Design Basis

Scope에는 다음이 포함된다.

- Included / excluded scope
- Battery limit
- Discipline / vendor interface
- Existing facility tie-in
- Responsibility
- Acceptance boundary

Basic Design 입력은 다음을 포함한다.

- Process condition
- PFD / P&ID
- Control Philosophy
- Safety / hazardous area / environment
- Power / communication
- Reliability requirement
- Applicable standard and specification

## 5. WBS / Schedule / Progress / Risk

WBS는 Scope를 work package로 분해하여 deliverable, responsibility, cost와 schedule을 연결한다.

Schedule은 milestone과 dependency, critical path, long-lead item, vendor data, construction/site window를 연결한다.

Progress는 객관적 milestone과 완료증거로 측정한다.
계획 대비 실적과 forecast를 비교한다.

Risk Register는 cause, probability, consequence, owner, mitigation, residual risk와 action due date를 관리한다.

## 6. Cost Estimate / Cost Control

Estimate는 다음 basis를 기록한다.

- Scope
- Quantity
- Unit rate
- Instrument / panel / cable / JB / bulk material
- Engineering / inspection / construction / vendor service
- Assumption / exclusion
- Contingency

Cost Control은 다음을 구분한다.

- Budget Baseline
- Commitment
- Actual Cost
- Remaining Commitment
- Estimate to Complete
- Final Forecast
- Change Impact

현재 Actual이 Budget보다 작다는 사실만으로 최종 예산준수를 판단하지 않는다.

## 7. Document Control

문서는 다음 정보를 통제한다.

- Document number
- Title / discipline
- Revision
- Status
- Review / approval
- Transmittal
- Superseded copy

MDR 또는 동등한 register로 예정·실제 발행일, 책임자와 dependency를 관리한다.

## 8. Instrumentation engineering deliverables

핵심 deliverable:

- Instrument Index
- Instrument Datasheet
- I/O List
- Loop Diagram
- Hook-up Drawing
- Cable Schedule
- Junction Box Schedule
- Termination / Wiring information
- MTO / BOQ

Instrument Index는 Tag 기반 master register다.
I/O List는 field-control system interface까지만 소유한다.

URS·FRS·FDS·SDS, logic/HMI, software FAT/SAT 상세는 기존 software project Topic으로 handoff한다.

## 9. Procurement and Vendor

`Requisition → RFQ → Technical / Commercial Evaluation → Clarification → PO → Vendor Document Review → Inspection / Release`

Vendor document 승인 결과는 project datasheet, loop, cable/JB와 master register에 반영한다.

Vendor shop inspection과 software FAT의 상세 ownership은 구분한다.

## 10. Construction / QA/QC / Completion

시공 전 다음 readiness를 확인한다.

- AFC drawing
- Material
- Access
- Power / piping
- Support / cable route / JB
- Discipline interface

ITP 또는 동등한 계획으로 hold/witness point, inspection, acceptance criterion과 quality record를 관리한다.

Mechanical Completion은 설치완료와 동일하지 않다.
검사·시험·문서상태와 punch closeout evidence를 포함한다.

## 11. Acceptance / Handover

Project Acceptance는 다음 evidence를 기준으로 한다.

- Scope completion
- Performance / quality requirement
- Punch status
- Required document and certificate
- Training
- Initial spare
- As-Built
- Contract acceptance criteria

Handover Dossier는 실제 설치상태를 재현할 수 있어야 한다.

인수 이후 maintenance strategy, calibration interval, CMMS와 KPI는 Topic 2 O&M management로 handoff한다.

## 12. Required Fact Anchors

총 `28`개 Anchor를 `fact_anchor.json` 정본으로 사용한다.

1. `project_lifecycle_stage_gate` — 계측 프로젝트는 요구·타당성 검토에서 시작해 기본설계, 상세설계, 조달, 제작·검사, 시공, 완성·시운전 지원, 인수·종결로 이어지는 lifecycle로 관리하며 각 단계는 승인된 입력·산출물과 다음 단계 진입기준을 가져야 한다.
2. `project_scope_boundary_interface` — 프로젝트 Scope는 포함·제외범위, battery limit와 discipline 간 interface, owner·EPC·vendor의 책임, 기존설비 tie-in과 최종 acceptance boundary를 명확히 하여 누락·중복과 scope creep을 방지해야 한다.
3. `project_design_basis_requirements` — Basic Design의 출발점은 공정조건, PFD·P&ID, Control Philosophy, 위험·안전 요구, 환경·방폭·재질·전원·통신·신뢰성 요구와 적용 규격을 Design Basis로 정리하고 변경기준을 통제하는 것이다.
4. `project_wbs_responsibility_raci` — WBS는 프로젝트 Scope를 관리 가능한 work package로 분해하고 각 package에 산출물·책임·일정·비용을 연결하며, discipline·owner·vendor 간 승인·검토·실행 책임은 RACI 또는 동등한 책임체계로 명확히 해야 한다.
5. `project_schedule_milestone_dependency_critical_path` — 프로젝트 일정은 engineering, procurement, vendor data, fabrication, construction, completion과 handover의 dependency를 반영해 milestone과 critical path를 관리하고, 장기납기 품목과 site window가 전체 일정에 미치는 영향을 추적해야 한다.
6. `project_progress_measurement_forecast` — 진도는 문서 발행, 승인, 발주, 제작, 납품, 설치, 검사완료 같은 객관적 milestone과 가중치 기준으로 측정하고, 계획 대비 실적과 forecast를 비교해 지연원인·잔여작업·완료예정일을 갱신해야 한다.
7. `project_cost_estimate_basis_quantity_rate_contingency` — 계측 프로젝트 Cost Estimate는 scope와 estimate basis를 명시하고 기기·패널·케이블·JB·자재 수량, 단가, engineering·inspection·construction·vendor service 비용과 합리적 contingency를 근거로 산정하며 assumption과 제외항목을 기록해야 한다.
8. `project_cost_baseline_commitment_actual_forecast` — Cost Control은 승인 Budget Baseline을 기준으로 commitment, actual cost, remaining commitment와 Estimate to Complete를 추적하고, 단순한 집행액뿐 아니라 최종 예상비용과 change impact를 비교해야 한다.
9. `project_risk_register_mitigation` — 프로젝트 Risk Register는 기술·interface·schedule·cost·supply·construction·safety 위험의 원인, 발생가능성, 영향, owner와 mitigation을 기록하고 정기 review하여 residual risk와 action due date를 추적해야 한다.
10. `project_change_control_scope_cost_schedule` — Design·Scope·Vendor·Site 조건의 변경은 요청, 영향분석, 승인, baseline 갱신과 실행·검증으로 관리하며 영향분석에는 기술, 안전, cost, schedule, document, procurement와 acceptance 영향이 포함되어야 한다.
11. `project_document_control_revision_transmittal` — 설계문서는 문서번호·제목·discipline·revision·status를 통제하고 review/approval, transmittal, superseded document 회수와 최신본 배포를 관리하여 현장과 vendor가 동일한 승인본을 사용하도록 해야 한다.
12. `project_master_deliverable_register` — Master Deliverable Register 또는 동등한 문서목록은 계측 discipline의 모든 산출물, 예정·실제 발행일, revision, review status, 책임자와 관련 procurement/construction dependency를 연결해 문서진도와 누락을 관리해야 한다.
13. `instrument_index_master_tag_register` — Instrument Index는 Tag, service, instrument type, P&ID reference, location, process connection, datasheet와 I/O·loop·cable 등 관련문서 link를 관리하는 계측 master register이며 변경 시 연관 산출물 정합성을 확인해야 한다.
14. `instrument_datasheet_process_mechanical_interface` — Instrument Datasheet는 process condition과 measurement range, accuracy·response 요구, 재질·접속·방폭·환경·전원·통신·accessory 요구를 구매 가능한 technical specification으로 변환하고 vendor data와 최종 as-built 값을 반영해야 한다.
15. `instrument_document_set_loop_hookup_cable_jb` — 계측 상세설계 문서군은 Loop Diagram, Hook-up Drawing, Cable Schedule, Junction Box Schedule, termination/wiring 정보 등으로 구성되며 각 문서는 Tag·I/O·cable core·terminal·installation detail이 서로 일치해야 한다.
16. `io_list_software_project_handoff` — I/O List는 field instrument와 control system 사이의 signal type, range, unit, channel·cabinet allocation 등 interface를 정의하되, software의 URS·FRS·FDS·SDS와 logic/HMI 상세설계는 기존 control software project Topic으로 handoff해야 한다.
17. `instrument_quantity_mto_boq` — 계측 MTO·BOQ는 Instrument Index와 layout·hook-up·cable routing 등 승인된 설계에서 기기, cable, gland, tray, JB, tubing·fitting, support 등 수량을 산출하고 revision 변경이 cost·procurement에 반영되도록 추적해야 한다.
18. `procurement_requisition_rfq_tbe_po` — 계측 조달은 Material/Technical Requisition, RFQ, Vendor Bid의 technical·commercial evaluation, clarification, 구매조건 확정과 PO로 이어지며 기술요구, 수량, inspection, document, delivery와 warranty 요구를 일관되게 전달해야 한다.
19. `vendor_document_review_integration` — Vendor Document Review는 certified drawing, datasheet, calculation, wiring, terminal, protocol, manual과 certificate 등을 검토하여 project requirement와 interface 적합성을 확인하고, 승인 결과를 관련 design document에 반영해야 한다.
20. `vendor_inspection_acceptance_handoff` — 제작품의 vendor inspection과 shop acceptance는 계약된 검사·성능·문서 기준으로 수행하고 nonconformance와 punch를 종결한 뒤 release해야 하며, software 기능의 상세 FAT/SAT 절차는 기존 control software project Topic으로 handoff한다.
21. `construction_installation_readiness` — 현장 계측시공은 approved-for-construction 도면·자재·작업공간·전원·배관·support·cable route·JB와 discipline interface의 readiness를 확인하고 설치순서와 access·maintainability를 고려해 수행해야 한다.
22. `construction_qa_qc_itp_hold_witness` — 계측 시공 QA/QC는 ITP 또는 동등한 검사계획으로 inspection point, hold/witness point, 책임·기록과 acceptance criterion을 정의하고 설치검사, continuity/insulation, tubing leak 등 적용 가능한 검사항목의 evidence를 남겨야 한다.
23. `mechanical_completion_punch_systemization` — Mechanical Completion은 system/subsystem별 설치완료와 검사·시험·문서상태를 확인해 완료증적을 만들고, 미완료·결함은 punch classification, owner, due date와 closeout evidence로 추적해야 한다.
24. `precommissioning_loop_readiness_handoff` — 계측 Precommissioning은 전원·배선·tubing, instrument calibration status, loop continuity와 I/O interface readiness를 확인하여 commissioning 가능한 상태를 만들며, control software의 detailed loop test·SAT·site integration 절차는 기존 software project Topic으로 handoff한다.
25. `project_acceptance_criteria_evidence` — Project Acceptance는 Scope 완료, 성능·품질 기준 충족, punch 상태, required document·certificate·training·spare·as-built 제출 등 계약상 acceptance criteria와 evidence를 기준으로 판단해야 하며 단순 가동 성공만으로 대체할 수 없다.
26. `asbuilt_handover_document_dossier` — Handover Dossier는 최종 As-Built drawing, Instrument Index·datasheet·loop·cable/JB 문서, vendor manual·certificate, calibration/inspection record, punch closeout와 configuration reference를 포함해 운영조직이 실제 설치상태를 재현할 수 있도록 인계해야 한다.
27. `operations_maintenance_handover_boundary` — 프로젝트 종료 시 초기 예비품, maintenance recommendation, warranty, vendor contact, training과 asset data를 운영조직에 인계하되, 인수 이후의 예방정비·검교정주기·CMMS·KPI 운영은 control_system_operations_maintenance_calibration_inspection_spares_kpi Topic으로 handoff한다.
28. `project_closeout_lessons_learned` — Project Closeout은 최종 cost·schedule·scope와 change, claim, NCR·punch, outstanding obligation을 정리하고 lessons learned와 actual quantity·vendor performance·estimate accuracy를 다음 프로젝트의 design basis·estimate·schedule risk에 환류해야 한다.

## 13. Fatal Wrong Claims

총 `14`개 Fatal contract를 사용한다.

1. `project_fatal_scope_is_equipment_list_only` — 프로젝트 Scope는 계측기 목록만 정하면 충분하며 discipline interface, battery limit와 acceptance boundary는 정의할 필요가 없다.
   - Correction: Scope는 포함·제외범위, interface, battery limit, 책임과 acceptance boundary까지 정의해야 한다.
2. `project_fatal_design_without_basis` — Vendor catalog와 과거 프로젝트 자료가 있으면 공정조건, P&ID와 Design Basis 없이 계측 기본설계를 진행해도 된다.
   - Correction: Basic Design은 승인된 공정조건, P&ID, Control Philosophy, 안전·환경·규격 요구를 Design Basis로 확정한 뒤 진행해야 한다.
3. `project_fatal_no_dependency_schedule` — 프로젝트 일정은 각 작업의 목표일만 정하면 되며 dependency, critical path와 long-lead item은 관리할 필요가 없다.
   - Correction: 일정은 작업간 dependency와 milestone, critical path, 장기납기와 site window를 반영해 관리해야 한다.
4. `project_fatal_actual_cost_below_budget_means_safe` — 현재 Actual Cost가 Budget보다 작으면 남은 commitment와 변경에 관계없이 프로젝트는 최종적으로 예산 내라고 판단할 수 있다.
   - Correction: Cost Control은 actual뿐 아니라 commitment, ETC와 change impact를 포함한 최종 forecast를 봐야 한다.
5. `project_fatal_change_without_impact_approval` — 현장이나 Vendor의 변경은 공기단축 목적이면 cost·schedule·document 영향평가와 승인 없이 바로 적용해도 된다.
   - Correction: 변경은 기술·안전·cost·schedule·document·procurement·acceptance 영향분석과 승인, baseline 갱신을 거쳐야 한다.
6. `project_fatal_uncontrolled_document_revision` — 현장 작업자는 파일명이나 최신 이메일만 확인하면 되므로 문서 revision·status·transmittal을 통제할 필요가 없다.
   - Correction: 설계문서는 승인상태, revision, transmittal과 superseded document 회수를 통제해야 한다.
7. `project_fatal_instrument_index_independent` — Instrument Index, P&ID, datasheet, loop와 cable 문서는 독립 문서이므로 Tag와 interface 정합성을 서로 확인할 필요가 없다.
   - Correction: 계측 master data와 연관 설계문서는 Tag·signal·terminal·cable·service 기준으로 상호 정합성을 유지해야 한다.
8. `project_fatal_lowest_bid_without_technical_review` — 계측 구매는 최저가 Vendor를 선정하면 되므로 technical compliance, delivery, inspection와 document requirement 평가는 필요 없다.
   - Correction: 조달은 기술적합성, interface, 납기, 검사·문서·보증 요구와 commercial 조건을 함께 평가해야 한다.
9. `project_fatal_vendor_document_not_integrated` — Vendor drawing과 datasheet가 승인되면 project loop, cable, datasheet와 관련문서에는 변경을 반영하지 않아도 된다.
   - Correction: 승인된 Vendor data는 관련 project design document와 master register에 반영되어야 한다.
10. `project_fatal_install_before_afc_readiness` — 자재가 현장에 도착하면 AFC 도면, interface readiness와 inspection plan이 없어도 설치를 시작하는 것이 일정상 유리하다.
   - Correction: 계측시공은 승인도면, 자재, site/interface readiness와 QA/QC 기준을 확인한 후 수행해야 한다.
11. `project_fatal_mechanical_completion_equals_installed` — 계측기가 물리적으로 설치되어 있으면 검사기록과 punch 상태에 관계없이 Mechanical Completion으로 판정한다.
   - Correction: Mechanical Completion은 설치뿐 아니라 요구 검사·시험·문서상태와 punch 관리 evidence를 확인해야 한다.
12. `project_fatal_acceptance_is_single_successful_run` — 설비가 한 번 정상가동하면 계약 acceptance criteria, punch, 문서, certificate와 training 상태에 관계없이 최종 Acceptance가 완료된다.
   - Correction: Project Acceptance는 계약상 성능·품질·문서·punch·교육 등 사전 정의된 criteria와 evidence로 판단해야 한다.
13. `project_fatal_io_list_replaces_software_design` — I/O List가 완성되면 URS·FRS·FDS·SDS, logic/HMI와 software FAT·SAT 상세설계가 모두 대체된다.
   - Correction: I/O List는 field-control system interface 문서이며 software requirement·design·test 상세는 기존 control software project Topic이 별도로 소유한다.
14. `project_fatal_handover_without_asbuilt` — 프로젝트 종료 시 최신 P&ID만 전달하면 실제 설치상태를 재현할 수 있으므로 As-Built loop·cable/JB, vendor, calibration·inspection record는 필요 없다.
   - Correction: Handover는 실제 설치상태를 재현할 수 있는 As-Built 계측문서, vendor data, quality·calibration records와 closeout evidence를 포함해야 한다.

## 14. Routing aliases

- `instrumentation project management basic design`
- `instrumentation project basic engineering`
- `instrumentation project cost schedule control`
- `instrumentation engineering deliverables management`
- `instrumentation project procurement construction handover`
- `instrumentation design basis cost estimate schedule`
- `instrument index datasheet loop cable project`
- `instrumentation material requisition vendor document review`
- `instrumentation construction mechanical completion handover`
- `instrumentation project acceptance dossier`
- `계측 프로젝트 관리 기본설계`
- `계장 프로젝트 기본설계`
- `계측 프로젝트 비용 일정 관리`
- `계장 프로젝트 원가 일정 관리`
- `계측 설계문서 조달 시공 관리`
- `계장 Instrument Index Datasheet 문서관리`
- `계측 프로젝트 Mechanical Completion 인수`
- `계측 프로젝트 As-Built Handover`

## 15. Routing field points

- Project lifecycle와 stage gate의 입력·산출물·승인기준
- Scope·battery limit·discipline interface·tie-in·acceptance boundary
- PFD·P&ID·Control Philosophy·공정조건 기반 Design Basis
- WBS·work package·RACI와 deliverable 책임
- Milestone·dependency·critical path·long-lead item 일정관리
- 객관적 milestone·weighted progress와 completion forecast
- Estimate basis·quantity·unit rate·service·contingency 비용산정
- Budget baseline·commitment·actual·ETC·final forecast 원가통제
- Risk register·risk owner·mitigation·residual risk
- Project change impact의 기술·cost·schedule·document 통합관리
- Document number·revision·status·transmittal·superseded copy 통제
- Master Deliverable Register와 document schedule
- Instrument Index master tag register와 P&ID 정합성
- Instrument Datasheet의 process·mechanical·electrical·communication interface
- Loop Diagram·Hook-up·Cable Schedule·Junction Box Schedule 정합성
- I/O List의 field-control system interface와 software project handoff
- MTO·BOQ·quantity take-off와 procurement/cost 연계
- Material Requisition·RFQ·TBE·Vendor clarification·PO
- Vendor document review와 certified drawing project integration
- Vendor inspection·NCR·punch·shop acceptance와 software FAT handoff
- AFC drawing·material·site/interface readiness와 instrumentation construction
- ITP·hold/witness point·quality record·acceptance criterion
- Mechanical Completion·systemization·punch closeout
- Precommissioning loop readiness와 software SAT/site integration handoff
- Project Acceptance criteria·evidence·document·training·spare
- As-Built instrumentation dossier와 vendor/quality record handover
- O&M training·warranty·initial spare와 Topic 2 maintenance handoff
- Final cost/schedule/vendor performance와 lessons learned feedback

## 16. Expected question patterns

1. 계측 프로젝트의 기본설계부터 인수까지 관리절차를 설명하시오.
   - intent: Design Basis, deliverables, cost/schedule, procurement, construction, completion과 handover를 통합한다.
   - required anchors: project_lifecycle_stage_gate, project_scope_boundary_interface, project_design_basis_requirements, project_schedule_milestone_dependency_critical_path, project_cost_estimate_basis_quantity_rate_contingency, procurement_requisition_rfq_tbe_po, construction_installation_readiness, project_acceptance_criteria_evidence, asbuilt_handover_document_dossier
2. 계측 프로젝트 Basic Design의 입력자료와 주요 산출물을 설명하시오.
   - intent: Design Basis와 Instrument Index·Datasheet 및 관련 상세설계로 이어지는 구조를 설명한다.
   - required anchors: project_design_basis_requirements, instrument_index_master_tag_register, instrument_datasheet_process_mechanical_interface, instrument_document_set_loop_hookup_cable_jb, io_list_software_project_handoff
3. 계측 프로젝트의 Cost Estimate와 Cost Control 방법을 설명하시오.
   - intent: estimate basis에서 budget baseline, commitment, actual, ETC와 change impact까지 연결한다.
   - required anchors: project_scope_boundary_interface, project_cost_estimate_basis_quantity_rate_contingency, project_cost_baseline_commitment_actual_forecast, instrument_quantity_mto_boq, project_change_control_scope_cost_schedule
4. 계측 프로젝트의 일정 및 진도관리 방법을 설명하시오.
   - intent: WBS, dependency, milestone, critical path와 objective progress/forecast를 설명한다.
   - required anchors: project_wbs_responsibility_raci, project_schedule_milestone_dependency_critical_path, project_progress_measurement_forecast, project_risk_register_mitigation
5. 계측 프로젝트 주요 설계문서의 역할과 상호 정합성 관리방법을 설명하시오.
   - intent: Instrument Index, Datasheet, Loop, Hook-up, Cable/JB와 I/O interface를 연결한다.
   - required anchors: project_document_control_revision_transmittal, project_master_deliverable_register, instrument_index_master_tag_register, instrument_datasheet_process_mechanical_interface, instrument_document_set_loop_hookup_cable_jb, io_list_software_project_handoff
6. 계측기기 구매와 Vendor 문서·검사 관리절차를 설명하시오.
   - intent: Requisition, RFQ/TBE, PO, vendor document review와 inspection/punch를 설명한다.
   - required anchors: procurement_requisition_rfq_tbe_po, vendor_document_review_integration, vendor_inspection_acceptance_handoff, instrument_quantity_mto_boq
7. 계측 시공의 착수조건, QA/QC, Mechanical Completion 절차를 설명하시오.
   - intent: AFC/readiness, ITP, quality evidence, systemization과 punch closeout을 연결한다.
   - required anchors: construction_installation_readiness, construction_qa_qc_itp_hold_witness, mechanical_completion_punch_systemization, precommissioning_loop_readiness_handoff
8. 계측 프로젝트 인수기준과 Handover Dossier의 구성 및 관리방법을 설명하시오.
   - intent: acceptance criteria, as-built, quality/vendor record, training·spare와 운영 handoff를 설명한다.
   - required anchors: project_acceptance_criteria_evidence, asbuilt_handover_document_dossier, operations_maintenance_handover_boundary, project_closeout_lessons_learned
9. 계측 프로젝트 변경이 원가·일정·문서·조달에 미치는 영향과 관리방법을 설명하시오.
   - intent: scope/interface와 baseline을 기준으로 integrated change control을 설명한다.
   - required anchors: project_scope_boundary_interface, project_change_control_scope_cost_schedule, project_cost_baseline_commitment_actual_forecast, project_schedule_milestone_dependency_critical_path, project_document_control_revision_transmittal, project_risk_register_mitigation
10. 계측 프로젝트와 제어 소프트웨어 프로젝트의 설계문서·시험·인수 ownership을 구분하시오.
   - intent: Instrumentation-wide design/procurement/construction과 SW URS/FRS/FDS/SDS/FAT/SAT의 경계를 설명한다.
   - required anchors: instrument_index_master_tag_register, instrument_datasheet_process_mechanical_interface, instrument_document_set_loop_hookup_cable_jb, io_list_software_project_handoff, vendor_inspection_acceptance_handoff, precommissioning_loop_readiness_handoff, project_acceptance_criteria_evidence

## 17. Semantic review requirements

- Scope·interface·acceptance boundary를 정의한다.
- Basic Design을 Design Basis로 시작한다.
- WBS·critical path·long-lead와 객관적 progress를 설명한다.
- Cost estimate와 final forecast를 구분한다.
- Document revision/status/transmittal을 통제한다.
- Instrument Index·Datasheet·Loop·Cable/JB 정합성을 연결한다.
- Procurement와 vendor document integration을 설명한다.
- Construction readiness·ITP·MC·punch를 설명한다.
- Acceptance를 계약기준과 evidence로 설명한다.
- Software project와 post-handover O&M ownership을 침범하지 않는다.
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
