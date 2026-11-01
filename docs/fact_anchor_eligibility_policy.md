# Topic Pack / Fact Anchor engineering evidence and scoring eligibility policy

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
