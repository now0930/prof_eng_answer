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

## Unresolved independent-source claims (fail-closed quarantine, 2026-11-01)

A separate executable snapshot, `grading/evidence/fact_anchor_unresolved_source_holds_20261101.json`,
holds **590** unreviewed claim IDs and **5** insufficient-direct-source-scope
claim IDs (595 distinct non-overlapping Fact/Anchor pairs). These do not receive
general scoring credit or carry verified status from this review. The original
276 scoring exclusions and 43 primary-source revision holds remain unchanged.
Unresolved / held is not equivalent to physically false, deletion, or reviewed.

`tests/test_fact_anchor_unresolved_source_holds.py` must verify exact ID-level
membership against the independent audit and disjointness. An individual
hold may only be removed after exact original technical source/edition/locator
and conditions are documented, affected Topic Pack/Registry sources updated by
the managed workflow if necessary, and focused + full release gates passed.

**This overlay is a temporary safety constraint, not independent verification
completion or a release certification**. Prior to use in deployed grading,
full regression and generated-bank freshness must be observed.
