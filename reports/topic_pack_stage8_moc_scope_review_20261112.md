# Stage 8 — `operations_moc_revalidation` Source Scope Review

- Date: 2026-11-12
- Topic: `sil_target_determination_risk_reduction_and_lifecycle`
- Anchor: `operations_moc_revalidation`
- Existing Registry Fact: `sis_operational_maintenance_modification_records_and_review`
- Review type: source-scope reconciliation for an existing approved/verified Registry Fact; no new Fact approval or human-review claim.
- Reviewer identity: Codex GPT-6 agent; exact deployment model ID is not exposed by this runtime.

## Approved source scope

The existing Registry Fact describes the process-industry SIS evidence expected in HSE's COMAH safety-report assessment context: arrangements for routine and SIS-specific maintenance, proof-test frequency and its basis, and a procedure for SIS modification. It explicitly does not establish that every trend field listed in the prior Canonical Anchor is a universal mandatory record item.

The primary source is HSE's [Discipline guidance for assessment of C&I issues in COMAH reports](https://www.hse.gov.uk/comah/sragtech/discguidciindex.htm):

- Criteria 5.2.4.3/5.2.4.4 identify maintenance and operation evidence, including routine maintenance arrangements, SIS-specific maintenance, proof-test frequency and how it was derived.
- Criterion 5.2.5.1 addresses SIS modification and asks for a modification procedure and a representative example.
- The guidance frames these as evidence for COMAH safety-report assessment against BS IEC 61511 or an equivalent standard. It does not prescribe a universal list of every operating trend field for all jurisdictions or all SIS applications.

The current Anchor is broader than that approved source scope. In particular, mandatory logging of proof-test completion, as-found failures, bypass time, demands, spurious trips, component/settings changes, and revalidation of every listed change cannot be inferred as one universal checklist from this source.

## Reconciled Canonical statement

> HSE COMAH 안전보고서 평가에서는 공정산업 SIS의 정기정비 체계, SIS별 정비 조치, proof-test 주기와 산정 근거, SIS 변경 절차의 대표 증거를 제시하도록 요구한다. 이 지침은 모든 산업·관할에서 모든 trend field를 보편적으로 의무 기록하라는 뜻이 아니다.

This statement is limited to the cited assessment context and to the evidence named by the Registry Fact. Other event or trend records remain dependent on the applicable risk analysis, design basis, operating procedure, and jurisdiction.

## Disposition and contract impact

| Fact ID | Canonical statement | Source review disposition | Evidence and boundary |
|---|---|---|---|
| `sis_operational_maintenance_modification_records_and_review` | HSE COMAH 안전보고서 평가에서는 공정산업 SIS의 정기정비 체계, SIS별 정비 조치, proof-test 주기와 산정 근거, SIS 변경 절차의 대표 증거를 제시하도록 요구한다. 이 지침은 모든 산업·관할에서 모든 trend field를 보편적으로 의무 기록하라는 뜻이 아니다. | `KEEP_BOUNDED` | HSE COMAH C&I assessment guidance, Criteria 5.2.4.3/5.2.4.4 and 5.2.5.1; no universal trend-field checklist. |

The existing Registry approval, verification status, Fact ID, Topic owner, Score Group, Weight, and deterministic Fatal Rule are unchanged. No new Fact ID, Fact approval, scoring owner, or score weight is created. The legacy promotion record is regenerated through `scripts/promote_reviewed_fact_anchors.py` so its statement hash and source hash match the narrowed Canonical source and this review report.

No Topic managed approval was recorded: this legacy Topic has no `topic_status.json`. No human review is claimed.
