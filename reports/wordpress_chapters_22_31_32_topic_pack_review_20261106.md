# WordPress Chapters 22, 31, 32 — Topic Pack source review (2026-11-06)

## Scope and provenance

The five WordPress posts below are source references, not automatic scoring authority. The public blog text was checked against the existing Topic ownership; only general, explicitly question-scoped principles were proposed as new Fact Anchors. No private OCR database, answer, session, or credential is included. Existing `wp-post:9774` source hash was preserved because the newer post revision has not been re-synchronized into the private source database.

| Post | Source locator | Topic Pack | Decision |
| --- | --- | --- | --- |
| [9774, Chapter 22-1](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-22-1/) | Flow measurement / open-channel sections | `flow_measurement_meter_principles_velocity_selection`, `open_channel_weir_flume_head_discharge_submergence_selection` | Already linked to the previously approved Topic Packs; no duplicate Fact and no silent source-hash replacement. |
| [9782, Chapter 22-2](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-22-2/) | §22.7–22.11, especially §22.9 change-of-quantity | `flow_measurement_meter_principles_velocity_selection` | Add Master source reference and one conditional net-flow conservation Fact. Coriolis/thermal are already represented; niche equipment details remain learning context. |
| [9789, Chapter 31](https://now0930.pe.kr/wordpress/lessions-in-industrial-instrumentation-chapter-31/) | §31.4 relation, §31.6 dynamic feedforward, §31.7.1 limit/selector | `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | Add Master source reference and three question-scoped Facts. Preserve existing ratio, feedforward, and override Facts. |
| [9814, Chapter 32.1](https://now0930.pe.kr/wordpress/chapter32-1-process-safety-20261031/) | Hazardous-area classification and protection | `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | Add Master source reference and explanation only. Do not promote MIE/MESG/MICR numerical values or edition-scoped protection requirements into general scoring Facts. |
| [9839, Chapter 32.2–32.6](https://now0930.pe.kr/wordpress/chapter32-probability-reliability-sis-20261103/) | Failure rate, reliability, PFD, SIF boundary | `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`, `sil_target_determination_risk_reduction_and_lifecycle` | Add Master source references and clarify existing assumptions. Do not duplicate existing λ/MTTR/PFD/SIF scoring Facts or conflate production availability with SIF dangerous failure probability. |

## Candidate Fact review

| Anchor | Primary technical cross-check | Condition and ownership |
| --- | --- | --- |
| `flow_inventory_change_net_balance` | [Kuphaldt, Lessons in Industrial Instrumentation, §22.9](https://www.ibiblio.org/kuphaldt/socratic/sinst/book/liii_3v00.pdf); [author-hosted chapter](https://control.com/textbook/continuous-fluid-flow-measurement/change-of-quantity-flow-measurement/) | Conservation gives **net** flow from inventory change; an individual stream is not identified when several streams coexist. Required only for explicit change-of-quantity questions. |
| `relation_control_offset_setpoint` | [Kuphaldt, §31.4](https://control.com/textbook/basic-process-control-strategies/relation-control/) | Offset/difference setpoint, distinguished from multiplication/ratio. Required only when relation or relation-vs-ratio is asked. |
| `feedforward_dynamic_compensation_timing` | [Kuphaldt, §31.6](https://control.com/textbook/basic-process-control-strategies/feedforward-with-dynamic-compensation/) | Disturbance and manipulated paths have different dynamics; compensation must be causal/realizable. Required only when dynamic feedforward is asked. |
| `limit_control_bound_signal` | [Kuphaldt, §31.7.1](https://control.com/textbook/basic-process-control-strategies/limit-selector-and-override-controls/) | Bound a specified signal; do not confuse with choosing among measured PVs or controller COs. Required only for explicit limit/selector questions. |

The Master's new references remain `verification_status: unverified` because a post link is not a full private-source hash/OCR synchronization. This does not override the separate, source-grounded review of the four narrowly bounded scoring statements above.

## AI technical reviewer

Review method: delegated AI review, not human approval. Reviewer was launched with the configured `gpt-6-luna` model override; its agent-visible model label was "GPT-6 / Codex" and no finer deployed model ID was exposed. The independent reviewer compared the WordPress sections and the original author's book with the exact source JSON/README diff.

- Initial review approved the three process-control statements but held the inventory-flow statement because `dm/dt=Σm_in−Σm_out` did not distinguish inventory mass from stream mass-flow rates and omitted the volumetric-balance assumptions.
- The flow expected statement now uses `dM/dt=Σṁ_in−Σṁ_out` and separately bounds `dV/dt=ΣQ_in−ΣQ_out` to appropriate inventory and density/stream-accounting conditions.
- Relation-control explanation now explicitly requires compatible PV/SP units; the Limit comparison question was narrowed to Override so it does not silently require an unmodeled measurement-selector Fact.
- **Final technical decision: all four new Anchors approved as source-supported, conditional Facts.** No approval is claimed for the held hazardous-area numerical/edition-specific details or the full private WordPress/OCR source database.

## Validation record

- `python3 scripts/rubric_manager.py validate-topic-packs`: PASS, 89 packs / 2,096 anchors.
- `python3 -m pytest -q tests/test_master_topic_pack_schema.py tests/test_master_topic_pack_projections.py tests/test_master_topic_pack_integration.py`: PASS, 14 tests.
- `python3 scripts/rubric_manager.py validate-all`: PASS before generated rebuild.
- Final generated, full pytest and release-gate results are recorded separately in `reports/wordpress_chapters_22_31_32_release_20261106.md` so this approval report remains immutable after its hash is recorded.
- The initial managed-Pack reapproval command exposed a workflow defect: its preapproval phase ran the generated pipeline before updating the source hash, causing a stale-hash failure. The controller was changed to validate only source schema and quality before approval; the postapproval full release validation remains mandatory and unchanged.
