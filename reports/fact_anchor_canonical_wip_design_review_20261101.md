# Canonical WIP and P&ID documentation source comparisons — 2026-11-01

Both reviewed exact canonical anchor statements and published professional association sources. KEEP_BOUNDED is not a legal mandate, broad license to grade every document type, or Topic Pack-wide certification.

## 1. production_wip_buffer_and_flow_time_relationship_is_contextual

- Canonical Topic / Anchor: instrumentation_production_management_planning_quality_cost_resources / production_wip_flow_lead_time
- Original statement: WIP는 공정 사이의 완충과 변동 흡수에 필요할 수 있지만 과도하면 흐름을 가리고 Lead Time과 재고비용을 증가시키므로, Throughput·Cycle Time·buffer 용량과 함께 관리해야 한다.
- Original source: https://asq.org/quality-resources/articles/quality-quandaries-reducing-work-in-process-at-an-emergency-assistance-center?id=a4fb71c4fe28487993dd523850f4600a
- Locator: ASQ Quality Engineering, 2013, abstract; supplementary ASQ Six Sigma Forum Magazine 2005 https://asq.org/quality-resources/articles/applying-littles-law-and-the-theory-of-constraints?id=d4a9dd6c735049a39a87421d7ab6217e
- Verdict: KEEP_BOUNDED
- Conditions: WIP buffers variability but excessive WIP can increase lead time, delay visibility and inventory cost; Little's Law applies under stable long-run throughput/flow and consistent system boundaries, not universal instantaneous monotonic effect.

## 2. configuration_review_checks_documented_design_against_physical_configuration

- Canonical Topic / Anchor: pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative / design_review_cross_document_consistency
- Original statement: P&ID 설계검토는 PFD, equipment datasheet, Line List, Instrument Index, I/O List, Cause & Effect, control narrative 등 관련 문서와 tag·service·연결·fail action의 정합성을 교차 확인한다.
- Original source: https://www.isa.org/intech-home/2022/april-2022/features/improving-project-documentation-and-change-managem
- Locator: ISA InTech April 2022, Project documentation requirements; supplemental https://www.isa.org/products/instrumentation-and-control-systems-documentat-1
- Verdict: KEEP_BOUNDED
- Conditions: Review consistency of tag numbers, service functions and cross-references among applicable PFD/P&ID, datasheets, instrument index, I/O lists, logic and related controlled project records. Not all listed documents are universally mandatory for every project; actual physical configuration must be confirmed by as-built/site checks.


No source Topic Pack or generated rubric modified. No release gate executed. Two results are claim-scoped evidence only.