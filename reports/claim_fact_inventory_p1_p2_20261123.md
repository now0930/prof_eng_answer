# P1–P2 Fact Anchor / Canonical Claim audit — initial checkpoint (2026-11-23)

> **Status: AUDIT_ONLY / NOT_RELEASED.** Owner: Issue #40. D4 research is closed
> (`NO_GO_OPERATIONAL_ADMISSION`); Issue #39 B7 remains OPEN, 119 HOLD. Do not
> reopen D4, admit Claim–Fact evidence to scores, or merge/deploy this branch.

## Baselines and measured inventory

- Canonical base: `main@30b13262ad3899919edae7cb72be3ddeca677f18`.
- GitHub API read-only enumeration of all `rubrics/topic_packs/*/fact_anchor.json`:
  **89 Topic files, 2,096 Anchor rows**. All 89 files were parsed. No Anchor
  identity was missing, and no within-Topic exact `statement` duplicates
  were observed in the initial seven-batch read.
- **457** `statement` values were flagged as *multiple-sentence review
  candidates* by a punctuation-plus-whitespace heuristic. This **does not**
  prove 457 multi-claim violations or technical errors. Actual atomicity,
  omissions and source validity need per-Fact technical review.
- The new `scripts/audit_fact_anchor_claim_inventory.py` reproduces these
  counts from a checkout and adds ID-only cross-Topic exact-text duplicates,
  condition-cue counts and optional machine-contract ontology-ID diagnostics.
  Its full actual checkout output and cross-Topic counts remain **NOT_RUN**
  until executed at the candidate SHA. It does not inspect or alter private
  answers or generate score-bearing facts.
- Work branch begins from **main**, not the closed/unmerged D4 branch.

## Optional Machine Contract structural read — complete source inspection

All 89 Topic `logic_check.json` files were examined from the same main
baseline. Exactly **16** Topic machine contracts contain **113** machine
Facts. An additional exact structural comparison against all corresponding
Fact Anchor IDs and the global ontology gave:

- Same-named machine Fact ID and human-readable Anchor ID: **0 / 113**.
  This is **two independent ID namespaces by design**, not 113 missing
  or broken joins. An explicit evidence-backed mapping, if required, must
  not be constructed from guessed name equality.
- Machine-contract Topic owner mismatch: **0**.
- Undefined condition identifier: **0**.
- Ontology predicate resolution uses both `canonical_predicates.json`
  **and** `relations.json`. Subject/object term resolution includes
  `engineering_concepts.json`, `quantities.json` **and**
  `dimensions.json`.
- With all those namespaces considered, **one** predicate identifier is
  not found: `depends_on` in the EMC shield-termination machine Fact
  `emc_shield_termination_depends_on_conditions`. This is an **ontology
  mapping review candidate**, not an erroneous technical Fact or authority
  to substitute a guessed predicate.
- The `has_dimension` relation and objects `dimensionless` /
  `inverse_time` are valid in the corresponding ontology namespaces.
  Omitting those namespaces creates false missing-ID alarms.

The new audit script records zero or more review-only gaps; it does not
change contracts or grade answers. Actual invocation of that script at
the new PR SHA and full repository tests remain **NOT_RUN**.

## 457-candidate identity-locked triage batches — 2026-11-23

The **complete ID inventory** of the punctuation-based 457 cases has been
recorded in `reports/fact_atomicity_triage/batch_01.json` to `batch_07.json`.
The actual seven batch files were read back from GitHub and reconciled:

| Batch | Topic files | Candidate rows |
| --- | ---: | ---: |
| 01 | 13 | 78 |
| 02 | 13 | 92 |
| 03 | 13 | 64 |
| 04 | 13 | 42 |
| 05 | 13 | 82 |
| 06 | 13 | 48 |
| 07 | 11 | 51 |
| **Total** | **89** | **457** |

All 457 `(topic_id, anchor_id)` pairs are **unique**. The candidates occupy
**58 Topic** families; 31 Topic Pack files had no multi-sentence candidate.
Heuristic cue counts (not disjoint and **not technical defect counts**):

- applicability/condition cue: **220**
- numeric/formula/standard-string cue: **254**
- generalization or exception cue: **164**
- normative source-basis text cue: **153**
- vendor source-basis text cue: **75**
- Topic-boundary cue: **11**

Each row retains canonical statement, provenance text and exact source-file
Git blob SHA. This is **per-row structural traceability**, not per-row
technical source verification: all 457 rows remain
`HOLD_INDEPENDENT_TECHNICAL_SOURCE_CHECK` and
`KEEP_CURRENT_CANONICAL_UNCHANGED`. A source_basis citation name is not
evidence that the cited source was read and reconciled.

`tests/test_fact_atomicity_triage_integrity.py` now checks the frozen 89
sources, each source blob, the 457 distinct IDs, original source/metadata
identity and no scoring admission. The new test has **not been executed on
the full candidate repository** because that checkout/test runner is not
available here. The earlier isolated synthetic 8-passed result is a
different test scope.

A separate [priority source-review report](fact_atomicity_triage/primary_source_spot_review_20261123.md)
records source-by-source interpretation for **15 selected** cases. It flags
the legacy encoder input-frequency/decoded-count conflation as a revision
candidate, and carefully distinguishes partially corroborated standards,
manufacturer-specific assumptions and PDF text extraction where screenshots
were unavailable. **None** of these 15 has been approved for a new canonical
or scoring change.

Consequently **442 candidates have no independent source-level review in
this cycle**. The requested independent technical verification of all 457
remains **NOT_COMPLETE**, even though identity tracking is complete.

## Release / validation blocker

The repository's `.github/workflows/validation.yml` supports
`workflow_dispatch` only. The currently available GitHub integration can
read files, commits and Actions runs, but does **not** provide an action
to dispatch a new workflow run. This environment also cannot clone the
repository from GitHub (DNS resolution unavailable). Therefore the candidate
SHA's full `release_candidate.py validate` cannot honestly be marked
executed or PASS.

**Mandatory gate still open:** run the manual validation workflow on
`audit/claim-fact-inventory-20261123` at its final SHA, inspect the
passed/failed/skipped counts and generated/source consistency, then record
the exact run URL and SHA. No automatic workflow trigger was introduced.

## Historical pending sentence proposals (not admission)

At closed D4 SHA `5a49a7daf042fc4749b9ae137c9af054ff68afae`,
`calibration/fact_anchor_simplification_review_20261114.json` records
48 candidates across seven Topics as
`PENDING_TECHNICAL_REVIEW / CANDIDATE_ONLY_NOT_APPLIED / score_effect:none`.
A read-only comparison found 29 source statements matching its
`previous_statement`, 18 registered reviewed wording exceptions and one
documented encoder precision correction. None of the 48 source statements
exactly matches its proposed `simplified_statement`.

That historical result is separate from the 89-Topic **main** inventory.
It is not a blanket return to the old texts, a reason to merge PR #38 or
approval of the 48 proposed short sentences.

## Structural priority and technical-condition triage

The initial punctuation-heuristic hotspots include:

| Topic | Flagged / Total | Initial action |
| --- | ---: | --- |
| Final control element / SIL / SIS | 42 / 48 | Review proof-test and dangerous-failure assumptions |
| OT cybersecurity defense-in-depth | 39 / 40 | Separate independently testable controls from descriptions |
| DP level, wet/dry leg and remote seal | 27 / 28 | Protect fluid density, elevation, and installation assumptions |
| Configuration / change / release | 23 / 40 | Separate change-control requirements from examples |
| Speed / encoder / tachometer | 22 / 22 | Keep PPR, decoded count rate and receiver frequency distinct |
| Control-valve positioner and accessories | 21 / 40 | Avoid combining independent checks in one mandatory Fact |

**Example review boundaries from existing main source:**

1. Relative humidity definition: preserve same-temperature saturation reference
   and the meaning of `P_w/P_ws(T)`; shortening is not independent proof.
2. Encoder frequency selection: per-channel `PPR` frequency and
   decoded `N_eff` count rate can differ; do not generalize an x4 decoder
   to the physical channel frequency.
3. Thermocouple intermediate-metal law: equal temperature at the two
   added-metal junctions is essential to the stated ideal result.
4. Flow `mass_flow_density_volume_relation`: an example optional machine
   contract explicitly includes `uniform_density`. Source Anchor ownership
   and question scope must be checked before a mapping is claimed.

These are **triage risks**, not per-Fact independent technical approvals.
Actual source locators, formula dimensions, counterexamples and reviewer
provenance must accompany any eventual wording change. A source `source_basis`
pointer alone is not a verification.

## P2 existing ownership — no new Claim schema

| Existing layer | Owns | Does **not** own |
| --- | --- | --- |
| Topic `fact_anchor.json` | Human-readable bounded technical fact, Fact ID and original source evidence | Per-answer score or inferred meaning |
| `logic_check.json.machine_contract.facts` | Optional `fact_id`, `subject`, `predicate`, `object`, `polarity`, `conditions` | Automatic Fact approval; mandatory coverage for all Topics |
| Global `grading_ontology/` | Common predicate, quantity, concept and unit IDs / aliases | Topic-specific required Question scope |
| `canonical_grading_evidence.py` | Answer claim `source_span`, context, qualifiers and evidence-only normalization | `SATISFIED`, `WRONG`, Fatal, score or verdict |
| Question `required_anchor_ids`, `pass_required_anchor_ids` | The explicit question's required coverage | Global truth or Fact promotion |
| Deterministic requirement evaluator | Verified evidence-to-requirement state and score authority | Model-proposed new canonical truth |

**Audit diagnostics never imply approval.** A machine Fact ID that is different from a human-readable Anchor ID is normal
and **not** an error. A predicate missing from both defined predicate
namespaces or a term missing from all applicable namespaces is a *review
gap* only. The D4 119 HOLD remain untouched.
Do not auto-create aliases or infer missing conditions. Preserve
`UNKNOWN/ABSTAIN` and the existing A/B/C deterministic, D/E constrained
proposal, Fatal/WRONG/ceiling and 25-point contracts.

## Reproduction commands (new branch checkout)

```bash
python3 scripts/audit_fact_anchor_claim_inventory.py --summary-only
python3 -B -m pytest -q tests/test_fact_anchor_claim_inventory.py
python3 scripts/rubric_manager.py validate-all
python3 -B scripts/release_candidate.py validate
```

The synthetic focused test uses no external API, real student answer or
production DB. The original GitHub workflow is **manual-only
(`workflow_dispatch`)**: pushing code or opening a draft PR does not
itself establish a Release Validation PASS. Record precise candidate HEAD,
passed/failed/skipped/quarantine and mismatch diagnostics **after** the
workflow is explicitly executed.

## Completion boundaries

- **Measured:** all 89 main Fact source files and 2,096 Anchors; 457
  punctuation-based review candidates.
- **Implemented:** read-only audit and synthetic fail-closed regression
  tests in this separate branch.
- **Not established:** full per-Anchor scientific equivalence; independent
  source-locator validation; zero semantic cross-Topic duplication; complete
  machine-contract alignment; full repository offline pytest at branch SHA;
  approval/merge/deployment.
- **Prohibited:** modifications to canonical Fact sources, Registry,
  Topic bank/generated files, scoring exclusions, 119 HOLD, production
  bot/DB, previous PR #38 or closed D4 decision.
