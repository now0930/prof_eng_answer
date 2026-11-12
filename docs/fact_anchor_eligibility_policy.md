# Topic Pack / Fact Anchor engineering evidence and scoring eligibility policy

**2026-11-04 current operational checkpoint:** Topic Pack source에는 Fact Anchor
2,092개가 있으며, 실행용 overlay가 539개를 일반 채점 참조에서 차단하고
1,553개는 차단하지 않는다. 이전 checkpoint의 차단 436개에 1,656건 제안
검토에서 새로 차단한 보류 22개와 일반 채점 제외 81개가 더해진 값이다.
기존 엄격 판정 415건은 유지했고, 신규 supported/scope-supported 후보
1,135건은 비공개 staging에 두었으며 **이번 제안으로 운영 승인한 Fact는
0건**이다. 제안 보류 25건 중 나머지 3건은 기존 SIL/Nyquist 채점 계약과
충돌해 기존 상태를 유지한 채 별도 검토한다. 차단되지 않은 Anchor를
독립적으로 검증된 Fact로 해석하지 않는다. 상세 사항은
[운영 배포 기록](../reports/fact_anchor_1656_operational_deployment_20261104.md)을
참조한다. 아래의 이전 날짜별 수치는 감사 이력이며, 이 업데이트는
채점 적격성 기준을 완화하지 않는다.

## 학습 자료에서 발견한 Topic Pack 후보의 채택 기준 (2026-11-11)

- 원문에서 확인한 물리 법칙, 독립 기술 자료 또는 적용 가능한 공식 표준으로 뒷받침되는 명확하고 정확한 공학적 주장만 Topic Pack에 채택한다. 주장별로 출처 위치, 적용 대상·운전 조건·가정, 결론을 확인한다. 식은 변수의 의미와 적용 범위를 명시하고, 표준은 확인한 판과 적용 범위를 적는다.
- 개인 답안, 복습 글 및 AI 보완 답안은 후보 발굴에 활용한다. 기술 근거가 부족하거나 문구에 여러 해석이 가능하면 검토 대기로 둔다. 특정 판·설치 구성에 한정된 세부값은 적용 조건과 함께 참고로 관리한다.
- 기존 Anchor의 주장과 소유 Topic을 먼저 확인한다. 이미 다루는 원리는 기존 항목을 재사용하고, 실제 공백이나 불명확한 문구만 변경 후보로 기록한다. 승인과 source-hash, 검증 및 릴리스 절차를 거쳐 반영한다.
- 학습자별 오개념의 근거와 교정 이력은 [학습 루프 정책](answer_review_loop_policy.md)에 따라 비공개 DB에 기록한다.

## Canonical facts vs private derivation/correction records (2026-11-11 clarification)

- The Topic Pack/Fact Anchor is the **short, accurate, generalizable end result**: one well-bounded engineering proposition with indispensable assumptions, units, scope and evidence. It is not a notebook for an individual learner's mistaken beliefs or step-by-step derivations. Brevity never justifies removing a condition needed for correctness.
- Store the learner-specific *route to that proposition* in a **private learning DB**: original problem/attempt and evidence span, misconception versus omission versus ambiguity, corrected physical reasoning and derivation, checked source locator, applicable conditions, self-check and review history. Every such record remains `score_effect: none`.
- Any general Fact discovered while correcting a learner stays a **private candidate** until personal context is removed, the existing canonical owner/duplicates are checked, independent evidence supports the exact conditional statement, and the **existing** approval/source-hash/validation/release workflow is followed. No automatic promotion, scoring requirement or additional mandatory approval gate is created.
- **Existing behavior is retained:** pre-attempt study-answer display on an explicit `/review` request and the established AI reviewer approval workflow are unchanged. This is a documentation boundary, not evidence that a new private DB schema has already been deployed.

## Latest inventory/report checkpoint — 2026-11-01

This paragraph is a **status pointer, not a change to evidence-admission policy**. The current work branch contains **89 Topic Pack fact_anchor files / 2,092 Anchor rows**, and the 2026-10-30 Registry snapshot is **1,520 records** (including the 1,290-ID recheck Queue). The latest **report-only** 1,290-ID adjudication is **862 KEEP_BOUNDED candidates; 275 general-scoring exclusions; one scoped-only entry; 80 revisions; 50 insufficient-source holds; 11 standard-scoped holds; 11 vendor-scoped holds**, after reconciling the 159-ID original-source ledger. Detailed sources and exact-ID action list are at [the 2,092-Anchor inventory](../reports/fact_anchor_full_inventory_2092_status_20261101.md), [1,290-ID review reconciliation](../reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv), and [152 open corrective/hold cases](../reports/fact_anchor_1290_open_actions_152_20261101.csv).

**2026-11-02 local synchronization:** the original-source audit and executable hold manifests now match the latest reconciliation by exact Fact/Topic/Anchor ID: 80 revision, 184 source-or-promotion and 276 original general-scoring exclusions, **540 blocked in total**. The 184 include 112 `KEEP_BOUNDED` candidates still awaiting canonical promotion, so this synchronization does not release them. Registry and Topic Pack wording were not approved or changed. `validate-all` and the Topic Pack integration gate passed, but the full Release Gate failed on existing canonical grading regressions (the clean branch baseline failed the same 7 assertions and 8 errors). Thus no release/deployment or unblocking is claimed. See [synchronization report](../reports/fact_anchor_1290_operational_reconciliation_20261102.md). The dated checkpoints **below** are preserved as history.


Effective: 2026-11-01. This policy is a user-directed persistent authoring,
verification and general-grading reference contract. It applies to new and
updated Topic Packs, Fact records, generated learning/grading views and repairs.

## Core scoring reference: stringent admission rule

A Fact Anchor is eligible as a **general technical-exam core scoring reference**
only when it states a materially useful, independently falsifiable engineering
fact supported by an **identified primary standard, official engineering
documentation, established physical principle or reproducible calculation**.
The evidence record must identify title, issuing authority, edition/version,
specific clause/page/formula/section, URL when available, access date,
claim-to-evidence mapping, applicable conditions and any counterexample.
A plausible citation, a previously populated `verification_status`, a vendor
example, a schema/hash check, LLM consensus, or a Chat screening label is
**not an independent fact check**. Do not auto-certify the remaining Queue.

A core statement should be broadly applicable in industrial instrumentation,
control, safety, maintenance or systems engineering. Retain indispensable
units, physical assumptions and conditions. Do not collapse condition-dependent
standards into unconditional laws. When a wording is partly correct, replace it
with the smallest broadly supported engineering proposition and cite it
individually; do not silently promote a narrowed statement.

## Mandatory exclusion from general scoring reference

- `noncore_detail`: niche procedure, arbitrary example, vendor or model
  feature, very detailed application case, unsupported blanket expectation
  or peripheral item.
- `scoped_standard_or_jurisdiction`: jurisdictional regulations, edition-
  specific normative obligations or specialized design procedures whose
  universal applicability is not established. Keep as context for a question
  explicitly scoped to that regulation/standard, **not** as a general
  mandatory grading requirement.
- `duplicate_scoring_requirement`: redundant demand already represented
  by a better canonical fact. Preserve just one grading owner and
  cross-reference alternatives rather than double-counting.
- `overgeneralization_or_correction_required`: inaccurate, over-broad or
  unresolved claims. Do not score them as a correct Fact before evidence-backed
  repair and renewed review.

The four reasons are scored **ineligible**, independent of whether the
underlying claim is literally true in a limited context. Mark uncertainty
as pending/hold; do not infer falsehood from noncore or scoped classification.
Avoid deleting technical source history or weakening independently verified
fatal correctness checks unrelated to the excluded grading requirement.

## Current snapshot and implementation

- Queue: 1,290 Fact IDs, *not* yet independently verified end-to-end.
- Screening-based general-scoring exclusion: 276 unique Fact IDs and 276
  unique `(topic_id, anchor_id)` pairs; 190 noncore, 66 scoped,
  17 duplicate and 3 corrective.
- Canonical review evidence: `reports/fact_anchor_chat_ledger_20261101.csv`
  and `reports/fact_anchor_scoring_scope_candidates_20261101.md`.
- Executable exclusion overlay:
  `grading/evidence/fact_anchor_scoring_exclusions_20261101.json` and
  `grading/evidence/fact_anchor_scoring_exclusions.py`.
- The overlay filters eligible Anchor reference extraction, new question
  contract resolution, answer-claim matching and reviewed Fact score
  projection. This is a *reference exclusion*, not mass deletion of the
  Registry, source Topic Pack or generated banks.

For every remaining Fact, record: stable Fact ID, original statement,
relationship, official evidence and locator, conditions/limitations,
contradictions, reviewer identification/method, decision
(`KEEP`, `REVISE`, `DELETE`, `HOLD`), reviewed revision and exact
effects on Master Topic Pack, Model Answer, Logic Check, tests and generated
views. A decision without adequate independent source evidence is `HOLD`.

## Promotion and regression safeguards

Never edit `rubrics/generated` by hand. For content changes, review source
and run the repository's managed workflow, reviewer record, source hash,
focused unit/regression tests, `validate-all` and full release validation.
Prove exclusion both when an Anchor is question-owned explicitly and when
it is automatically inferred. Confirm that canonical requirements unrelated
to exclusions, A/B/C/D/E authority, fatal logic, question ownership, and
score ceilings are preserved. Report exact observed test results; no CI or
runtime PASS claim without an actual run. Work on the existing work branch,
not `main`, until integration gates pass.


## Independent primary-source revision holds — 2026-11-01

In addition to the original 276 general-scoring exclusions, the running
independent primary-source audit may classify previously eligible entries as
`REVISE_REQUIRED`. These do **not** become accepted grading references until
the precise original Fact wording, Topic Pack source, evidence mapping and
regenerated outputs are repaired and release validation passes.

The separate data file
`grading/evidence/fact_anchor_independent_revision_holds_20261101.json`
is an executable **temporary scoring hold** for the 43 entries currently
marked `REVISE_REQUIRED` in the independent verification audit. It is
not merged into the original 276 screening exclusions and does not denote
a scientifically false statement. Core reference extraction checks both
overlays. The corresponding hold can be removed only after independent
source-grounded correction and regression evidence; never infer a pass
from the legacy Registry's `verified` status.

Source checks are incomplete for the rest of the Queue; existing score
behavior outside those 276+40 is not proof of independent re-verification.
These changes have not been runtime-tested or release-gated within the
GitHub-only review session. A CI green status must be observed before
claiming operational validation.

## Current independent source review state (2026-11-01, H07)

Source-audit 1,290 unique Fact IDs: 563 unreviewed, 393 KEEP_BOUNDED,
7 SOURCE_CHECKED_SCOPED_STANDARD_HOLD, 8 HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE,
43 REVISE_REQUIRED, 275 EXCLUDE_FROM_GENERAL_SCORING_ONLY and 1
KEEP_AS_SCOPED_ONLY_NOT_GENERAL_SCORING. The original 276 scoring
exclusions and 43 revision-hold overlay entries remain unchanged.

The unresolved-source scoring overlay contains 578 unique held pairs,
consisting of 563 pending, 8 insufficient evidence and 7 independently
verified within a standard's limited scope but **not eligible as generic**.
These held entries may not become required general grading references.

Batch H has 125 reviewed source IDs, none remaining PENDING, but its
explicit HOLD and scoped statuses are **not equivalent to verified facts**.
Source verification for the remaining A–G/I–K items continues.
Details: `reports/fact_anchor_independent_review_batch_H_06_20261101.md`
and `reports/fact_anchor_independent_review_batch_H_07_20261101.md`.

This documentation and scoring snapshot neither repairs all canonical
Topic Packs/Registry nor passes the known failing full Release Gate.
Do not merge the work branch or dilute protected grading criteria.

## State-space original-source review update (2026-11-01)

Eleven generic continuous-time LTI state-space/observability/control theory facts were checked independently against original ASU, MIT and Technion sources. All require stated linear-model and rank assumptions; no generic claim of actuator saturation immunity or zero steady-state tracking error is made. The unique source-audit pending count is now **552**, the conditional technical KEEP_BOUNDED count **404**. Seven standard-specific scope holds, eight insufficient-direct-source holds, 43 repair-required holds and the pre-existing exclusion overlay remain intact. The unresolved scoring manifest holds **567** unique Fact/Anchor keys. Details: `reports/fact_anchor_independent_review_state_space_20261101.md`. Full release validation is still blocked by canonical grading regressions; do not deploy.

## Thermocouple NIST and OEM original-source checks (2026-11-01)

Eleven exact thermocouple Fact IDs independently checked, bound to ITS-90, CJC, materials, calibration procedure, signal-chain and sensor installation conditions; see `reports/fact_anchor_independent_review_thermocouple_20261101.md`. Current audit: **541 PENDING**, **415 KEEP_BOUNDED**, 7 source-scoped standard holds, 8 inadequate-direct-source holds, 43 corrective, 275 original screening exclusions and 1 original scoped-only. The executable unresolved-source overlay contains **556** holds. Do not interpret generic conditional KEEP as completed original canonical Topic Pack/Registry approval or actual release gate pass.

## Ultrasonic primary-source fact review (2026-11-01)

14 exact generic acoustic-physics and pulse-echo measurement Fact IDs newly checked against Pepperl+Fuchs and Endress+Hauser original publisher technical documents; see `reports/fact_anchor_independent_review_ultrasonic_20261101.md`. Source-audit PENDING **527**, KEEP_BOUNDED **429**, 8 insufficient, 7 source-checked standard-scoped, 43 revision, 275 excluded, one legacy scoped. Executable unresolved-source holds **542**. Release Gate and Registry/Topic Pack canonical promotion remain incomplete.

## Thermistor independent NTC/PTC technical review (2026-11-01)

13 exact Fact IDs compared to TDK and Analog Devices first-party source texts: 10 bounded physical/measurement facts retained; 3 universalized claims (fault-action requirement, PTC global monotonicity, unspecified polymer mechanism) marked insufficient-scope HOLD, **not** certified false. The source-audit counts are PENDING **514**, KEEP_BOUNDED **439**, 11 insufficient and 7 standard-scoped holds. The executable scoring hold manifest carries **532** pairs (514+11+7). See `reports/fact_anchor_independent_review_thermistor_20261101.md`. No Registry/Topic Pack approval or Release Gate completion.

## NI/HBK bridge and strain-gauge independent review (2026-11-01)

Twelve exact ID claims reviewed in `reports/fact_anchor_independent_review_strain_gauge_20261101.md`: ten scoped physics/measurement claims kept; one conditional mandatory fault-diagnostic claim held; **one half-bridge / quarter-bridge Type II classification error marked REVISE_REQUIRED** pending canonical correction. Cumulative original-source pending 502; KEEP_BOUNDED 449; REVISE_REQUIRED 44; source-insufficient 12; IEC-scoped 7, previously excluded 275 and legacy scoped-only one. Source-hold manifest 521, independent revision overlay 44; original screening exclusion overlay 276 unchanged. Current full Release Gate remains blocked; do not merge or deploy.

## Industrial pressure and DP independent original-source review (2026-11-01)

Thirteen exact ID source-pending facts individually compared with WIKA and Emerson official measurement resources, original Rosemount 3051S Wireless impulse-line manual (printed p.35) and 2051 TPE formula (p.68); source screenshots checked. Twelve conditional physics/measurement facts retained and one prescriptive lifecycle-procurement claim held for insufficient mandatory scope; report `reports/fact_anchor_independent_review_pressure_20261101.md`. Current independent original-source PENDING **489**, KEEP_BOUNDED **461**, 13 insufficient, 7 standard-scoped, 44 revision, 275 excluded, 1 legacy scoped. Executable unresolved-source manifest **509**. Full Release Gate remains an independent blocker, and no canonical Topic Pack/Registry approval has been performed.

## Humidity original-source physics vs manufacturer examples (2026-11-01)

Twelve exact humidity Fact IDs individually compared with Vaisala, Rotronic, TI and Michell original technical materials. Eight bounded general physical/measurement facts kept, three manufacturer/model-specific claims recorded as `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` (explicitly NOT generally scoreable), one unsupported universal procurement lifecycle mandate held. The TI SRHR-233C original source PDF figure was screenshot-verified at printed page 2-45. Michell original Optidew maintenance PDF text was checked but browser screenshot timed out (not treated as visually verified). See `reports/fact_anchor_independent_review_humidity_20261101.md`. Cumulative PENDING **477**, KEEP_BOUNDED **469**, insufficient source **14**, standard-scoped **7**, vendor-scoped **3**, revision **44**, screening exclusion **275**, legacy scoped **1**. Generic scoring source manifest **501**. This is not managed Topic Pack/Registry approval or Release Gate PASS.

## 2026-11-01 flow / industrial architecture / PID / lead-lag independent-source review

35 formerly-PENDING exact Fact Anchors individually compared with published first-party Emerson, E+H, OMEGA, Brooks, MathWorks, Yokogawa and TI technical sources. 31 engineering propositions accepted only in their explicit physics/configuration assumptions and 4 long universal procedure/selection mandates flagged `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE`; their falsehood is **not** asserted. Evidence reports: `reports/fact_anchor_independent_review_flow_20261101_v2.md`, `...architecture_20261101_v2.md`, `...pid_20261101_v2.md`, `...lead_lag_20261101_v2.md`. Current PENDING **442**, KEEP_BOUNDED **500**, insufficient HOLD **18**, revised **44**, excluded **275**, standards scoped **7**, vendor scoped **3**, existing scoped **1**. Executable source-hold list **470** =442+18+7+3; 44 revision holds and 276 earlier exclusions unchanged. This is evidence review, NOT a Topic Pack source-hash approval or full Release Gate PASS.

## 2026-11-01 optical ToF/triangulation, piezoelectric, LVDT source review

30 formerly PENDING exact ID anchors independently compared with official OMRON/KEYENCE/Analog Devices/PCB/Piezotech sources and scholarly original papers: 23 bounded physical/procedural statements KEEP_BOUNDED and 7 over-composed or unsupported universal requirements retained as explicit insufficient-direct-source HOLD. Reports: `reports/fact_anchor_independent_review_optical_20261101_v2.md`, `...piezo_20261101_v2.md`, `...lvdt_20261101_v2.md`. Audit: **412 PENDING**, **523 KEEP_BOUNDED**, **25 insufficient-scope HOLD**, 44 revised, 275 excluded, 7 IEC/standard-scoped, 3 vendor-scoped, 1 legacy scoped. Fail-closed scoring source manifest **447** keys (412+25+7+3), original exclusions 276 and revision 44 overlays unchanged. No approval of source Topic Packs or Registry, full Release Gate not green, no `main` merge.

## Free-space radar vs GWR and manufacturer-specific source review (2026-11-01)

13 formerly PENDING exact radar-level anchors were independently compared with original AMETEK Magnetrol, Emerson, Analog Devices, VEGA and Endress+Hauser documents; report `reports/fact_anchor_independent_review_radar_20261101_v2.md`. Nine supported bounded physical principles retained; three overgeneralized/rigid radar diagnostics/extended-target model claims source-insufficient; one original Magnetrol 706 rod/cage example verified as model-specific and held outside general scoring. Audit now **399 PENDING**, **532 KEEP_BOUNDED**, **28 insufficient**, **4 manufacturer-specific**, 7 standard-scoped, 44 revisions, 275 screening excluded, 1 legacy scoped. Executable source-hold manifest **438**, plus independent correction hold 44 and original general exclusion 276, no newly approved Registry/Topic Pack/fatal changes. Full Release Gate not certified.

## Observer/prefilter/internal-model original theorem review (2026-11-01)

Seven exact state-feedback tracking Fact IDs individually compared with University of Michigan, University of Agder, MIT, NPTEL and MathWorks published sources. Five bounded theorem claims retained; **two incomplete conditions** moved to `REVISE_REQUIRED`: detectability does not permit arbitrary placement of every observer mode, and constant-disturbance integral rejection requires a feasible stabilizable regulator/augmented plant. Report `reports/fact_anchor_independent_review_state_tracking_20261101_v2.md`. Source audit PENDING **392**, KEEP_BOUNDED **537**, REVISE_REQUIRED **46**, insufficient scope 28, vendor scoped 4, standard scoped 7, excluded 275, legacy scoped 1. Unresolved-source manifest **431**, separate revision overlay **46**, earlier scoring exclusion overlay 276 unchanged. No managed canonical edits or Release Gate PASS.

## Industrial valve and actuator construction original sources (2026-11-01)

Eleven previously unreviewed source Fact IDs individually compared with original Emerson Fisher Control Valve Handbook 5th edition, Emerson Bettis valve actuators, Rotork electric actuator and 2025 Emerson offset-valve whitepaper, including PDF screenshots. All eleven common mechanisms are conditionally source-confirmed with model-specific limitations on offset geometry, actuator fail action and sanitary application; `reports/fact_anchor_independent_review_control_valve_types_20261101_v2.md`. Current PENDING **381**, KEEP_BOUNDED **548**, REVISE_REQUIRED 46, insufficient 28, standard-scoped 7, vendor-scoped 4, excluded 275, legacy-scoped 1. Executable source hold manifest **420**. No original canonical source hash approvals or full Release Gate pass.

## Speed/encoder/tachometer original-source checks (2026-11-01)

Nine exact originally pending claims compared with OMRON/Pepperl+Fuchs/Analog Devices/Nidec/maxon first-party sources; eight bounded physical sensor facts retained and one unconditional complete speed-selection/dynamic-limits checklist held outside general scoring. Report `reports/fact_anchor_independent_review_speed_rotation_20261101_v2.md`. Current PENDING **372**, KEEP_BOUNDED **556**, insufficient scope **29**, standard-scoped **7**, vendor-scoped **4**, revision 46, excluded 275, legacy scoped 1. Source blocking manifest **412** distinct keys, independent correction overlay 46 and existing screening 276 unchanged. Original Topic Pack/Registry source hash not approved and overall release gate still blocked.
