# Canonical verification — SFC and P&ID, 2026-11-01

Five pending canonical Fact Anchor source claims were read from rubrics/topic_packs and compared with primary official publications. Verdict: KEEP_BOUNDED in all five cases. No source or generated bank changes; no release gate was run.

## 1. sw02_state_transition_is_deterministic_function_when_all_state_inputs_are_defined

Canonical topic: control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe

Canonical anchor: sw02_state_transition_model

Canonical original statement: 상태전이는 현재 상태와 명령, Permissive, Interlock, Trip, 설비 피드백 및 시간조건을 입력으로 다음 상태를 결정하는 함수로 표현할 수 있으며, 동일 입력에서 결정론적 결과가 나와야 한다.

Primary publisher: https://www.plcopen.org/standards/logic/iec-61131-3/faqs/

Locator: PLCopen IEC 61131-3 FAQ, Sequential Function Chart; supplement: https://infosys.beckhoff.com/content/1033/tcplccontrol/925269003.html

Verdict: KEEP_BOUNDED

Boundaries: A fully specified current state, sampled inputs, evaluation and transition priority can define one next state. This does not imply unconstrained asynchronous plant events are deterministic without observation model.

## 2. instrument_tag_identity_is_cross_referenced_in_project_documents

Canonical topic: pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative

Canonical anchor: pid_instrument_index_io_relation

Canonical original statement: P&ID의 instrument tag는 Instrument Index, I/O List, datasheet 등과 상호 추적 가능해야 하며 tag 누락·중복·service 불일치는 설계 검토 항목이다.

Primary publisher: https://www.isa.org/intech-home/2022/april-2022/features/improving-project-documentation-and-change-managem

Locator: ISA InTech 2022, Instrument Index and project documentation/change management

Verdict: KEEP_BOUNDED

Boundaries: Maintain consistent tag identities where P&ID, index, wiring/I-O list and datasheet actually apply; the source does not require an identical document set for every instrument.

## 3. p_and_id_valves_have_distinct_functions_not_all_are_control_valves

Canonical topic: pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative

Canonical anchor: valve_function_distinction

Canonical original statement: P&ID의 밸브 기호는 isolation, check, control, relief 등 기능이 서로 다르므로 모든 밸브를 제어밸브로 해석하지 않고 기호·tag·legend를 함께 확인한다.

Primary publisher: https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5

Locator: ISA5 identification and symbols; supplementary Emerson functional valve categories at https://www.emerson.com/en/final-control/catalog/products-and-software/valves

Verdict: KEEP_BOUNDED

Boundaries: Isolation, check, relief and modulating control are distinct service functions. Interpretation must use symbol/legend/tag and project context; no blanket classification from generic valve symbol.

## 4. control_narrative_complements_pid_with_operating_logic_description

Canonical topic: pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative

Canonical anchor: pid_control_narrative_relation

Canonical original statement: Control narrative는 제어 목적, 정상·비정상 동작, mode, setpoint·override·shutdown 철학을 문장으로 보완하며 P&ID의 기호 연결만으로 모든 운전 의도를 대체하지 않는다.

Primary publisher: https://blog.isa.org/best-practices-and-standards-control-narratives

Locator: ISA blog, Best Practices and Standards for Control Narratives; instrument/function descriptions and operational logic

Verdict: KEEP_BOUNDED

Boundaries: Narrative complements diagram with sequence, modes, setpoints, abnormal actions and interlocks where design requires; not a fixed mandatory list in every industry/project.

## 5. pid_is_process_safety_information_for_hazard_analysis_and_operations

Canonical topic: pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative

Canonical anchor: pid_lifecycle_use

Canonical original statement: P&ID는 설계검토뿐 아니라 위험검토, 시공, commissioning, 운전, 정비, troubleshooting 및 변경관리에서 공통 기준문서로 활용되므로 최신성과 문서 간 일치성이 중요하다.

Primary publisher: https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119

Locator: OSHA 29 CFR 1910.119(d)(3)(i)(B) P&IDs as process safety information, (e)(3) PHA, (l) management of change; supported as example of lifecycle use

Verdict: KEEP_BOUNDED

Boundaries: P&ID supports design, hazard review, operations, maintenance and change management as good engineering practice; OSHA PSM legal applicability is US-jurisdiction and facility scoped, not universal duty.

## WIP correction to prior report

The canonical production_throughput_cycle_lead_wip_kpi claim itself already distinguishes WIP, throughput, cycle time and lead time and demands explicit process boundaries. Source-comparison wording had conflated an external terminology caveat with a defect requiring correction of this original claim. Under the existing statement and its declared scope, verdict is KEEP_BOUNDED. Cycle-time denominators and measurement meanings must still be stated for exam answers. This replaces the previous REVISE_REQUIRED verdict in the prior 13-item report.

Limits: this is claim-to-publisher comparison, not all texts in the Topic Pack. Legal scope from OSHA cannot be imposed on facilities outside its actual coverage. Manufacturer or vendor-specific rules do not become general scoring requirements.