# Stage 8 — Scoring Safety and Generated Bank Release Report

Date: 2026-11-12<br>
Repository: `/home/now0930/hermes/workspace/prof_eng_answer`<br>
Branch: `codex/topic-pack-evidence-policy-20261111`<br>
Starting and ending HEAD: `8827219d1356da9b055cf8c9f5777c01a465dc52`

## Executive result

- #19 was narrowed to machinery emergency-stop reset scope and removed from generic positive scoring requirements. Its engineering explanation remains available in the Topic Pack.
- #51 was narrowed to the existing COMAH assessment evidence scope. Its existing approved Fact identity and Topic scoring owner were retained; no new Fact was approved.
- No new Fatal Rule, Score Group, weight, or scoring authority was added. The existing SIS MOC relation and certificate-interval Fatal invariant remain in force.
- Official Topic Pack release validation promoted all six Generated Bank files. Final freshness comparison found zero stale files and zero leaf differences.
- Full offline pytest: **1,622 passed, 0 failed, 1 skipped**. Non-promote Release Gate: **exit 0**.
- No operational deployment, Bot restart, commit, or push was performed.

## Scope and preserved work

At start, branch and HEAD matched the requested baseline. The worktree already contained staged, unstaged, and untracked user changes from earlier stages. These were left in place; no reset, clean, blanket staging, or restoration was performed. The initial file/hash inventory is recorded in `/tmp/stage8_baseline_hashes.json` and the pre-promotion backup manifests under `/tmp/stage8_pre_*_20261112/`.

The Stage 5–7 edits, including #24 `flashing_classification` and `approve-topic --approval-only`, were preserved. Existing promotion IDs and scoring contracts were not replaced. The final `git diff --check` completed without errors.

## #19 — `sw02_trip_latch_reset`

### Evidence and scope

The approved source supports a machinery emergency-stop rule: reset of the emergency stop must not itself restart machinery; normal start controls are used separately. This is not evidence that every process Trip, SIS, PLC sequence, or non-safety automatic recovery sequence must require a manual reset edge. The source scope was checked against official HSE material: [EIS28: The use of work equipment](https://www.hse.gov.uk/pubns/eis28.pdf) and [PUWER guidance](https://www.hse.gov.uk/pubns/priced/puwer.pdf).

### Changes

- Bounded the Canonical Anchor statement and accepted explanations to machinery emergency-stop reset, with separate normal starting; general process Trip recovery follows the specific Trip function and sequence design.
- Updated Logic Check conditions so a missing latch/reset edge is an error only when the question explicitly requires that behavior. Generic process Trip and non-safety automatic sequence omissions are not treated as faults.
- Removed the Anchor from generic model-answer required-anchor scopes and made its use conditional on the question actually requiring it.
- Kept the Anchor and its explanatory value; no scoring exclusion overlay was needed because the generic question contracts no longer require it.

### Deterministic scoring A/B

The harness exercised actual question-scope selection and the production Fact Anchor adapter. Before the change, generic cases produced PARTIAL or MISSING for manual reset, cause-removal reset, an allowed non-safety automatic recovery, and a correct distinction between emergency stop and general Trip; an answer omitting the reset edge was SATISFIED. After the change all five cases reported `NOT_IN_SCORING_SCOPE` for this Anchor in generic patterns. Thus the generic scoring path no longer penalizes omission or grants unearned credit for this non-demanded detail. A specifically scoped emergency-stop question can still use the bounded Fact.

No Fatal Rule was introduced or changed.

## #51 — `operations_moc_revalidation`

### Evidence and approval boundary

The prior Canonical wording extended beyond the existing approved Registry statement by appearing to require broad trend, as-found, bypass, demand, and spurious-trip records universally. The relevant official source is [HSE COMAH C&I assessment guidance](https://www.hse.gov.uk/comah/sragtech/discguidciindex.htm), which describes evidence in a COMAH assessment context, including routine and SIS-specific maintenance, proof-test frequency/basis, and SIS modification procedure/records. It does not establish a universal record list for every jurisdiction and SIS.

### Changes and contract effects

- Narrowed the Canonical statement, accepted explanations, Logic Check, and model-answer guidance to the bounded evidence and context supported by the existing reviewed source.
- Retained the existing Fact ID, Topic scoring owner, score contract, and promotion identity. The production projection now recognizes bounded evidence; an answer relying only on the former broad universal record list does not satisfy that bounded Fact.
- Preserved the independent machine-contract MOC relation and the Fatal rule `fatal_certificate_interval_as_operating_minimum`.
- Repaired the existing promotion review through the official promotion builder pathway, pointing to `reports/topic_pack_stage8_moc_scope_review_20261112.md`. All **104/104** existing promotion IDs remain. The changed pin records reflect the revised statement/source hashes and review report; no synthetic approval was created.
- No new formal managed Topic approval or new Fact approval was recorded. Technical source review and release promotion are not represented as human review. The deployed AI reviewer model identifier was not available, so none is claimed.

### Deterministic scoring A/B

The production scoring harness returned `SATISFIED` for bounded COMAH evidence and `MISSING` where that evidence was omitted or replaced solely by an overgeneralized universal-record claim. The separate MOC relation still returns SATISFIED for a correct relation, WRONG for its contradiction, and MISSING when required by the question. The existing certificate interval Fatal is still emitted when its invariant is violated.

## Generated Bank promotion

Before official promotion, all six generated files were stale. The command below was run after the Canonical and promotion-review changes and exited **0**:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated
```

The command reported release validation PASS for 89 Topics and 2,096 Anchors. It promoted only repository Generated Bank outputs; it did not deploy runtime files. The final freshness comparison reported all six files `stale=False` with `leaf_diffs=0`.

| Generated file | Final SHA-256 |
|---|---|
| `fact_anchors.generated.json` | `e3eaab1555e3b85c1175e644d8be728ee0321c961bed095a6d0f1a3e4482df5b` |
| `model_answers.generated.json` | `b37229a7ed70ef115b6be51060fe2c28be638bf9a46006d60b328eade00ac305` |
| `topic_importance.generated.json` | `27b7b54dc373c3520d07ff1c8cfde833ab031101ef8301849319c9254b3c07e3` |
| `logic_checks.generated.json` | `d7708f074e11192b82ebc6a56a692006527a5c0fc8b6427c04bf4149b75af203` |
| `logic_check_profiles.generated.json` | `63b4ac4c3b8f558c1244431860cd4d5f00e7db24c278041cb21e3d6315df2722` |
| `topic_pack_manifest.generated.json` | `ec83aabc699722569514cd74b837e75b540f8cc0187b912e08cfc9cecaa871ea` |

Backups were retained under `/tmp/stage8_pre_promote_20261112`, `/tmp/stage8_pre_final_promote_20261112`, and `/tmp/stage8_pre_gatefix_promote_20261112`. No restore was needed.

## Validation results

| Check | Result |
|---|---|
| Official `validate-topic-pack-release --all --promote-generated` | PASS, exit 0 |
| Topic Pack content audit | PASS: 89 Topics, 89 Masters, 767 questions, 2,096 Anchors |
| Master Topic Pack validation | PASS: 89 |
| `rubric_manager.py validate-all` | PASS |
| Promotion pin check | PASS: 104/104 existing IDs |
| Generated freshness comparison | PASS: 6/6 fresh, 0 leaf differences |
| Focused control-sequence Topic regression | PASS: 27 tests |
| Focused confirmed-anchor correction regression | PASS: 3 tests |
| Full offline pytest, `python3 -B -m pytest -q` | **1,622 passed, 0 failed, 1 skipped**, exit 0 |
| Non-promote Release Gate | **exit 0** |
| `git diff --check` | PASS |

The non-promote Gate command was:

```bash
PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 RUN_GRADING_REPRODUCIBILITY=0 bash scripts/validate_release.sh
```

It exited **0**. The dedicated exact 10-run grading reproducibility gate remained opt-in and was skipped by the script as configured; the Gate did run deterministic production smoke and host regression checks. The full pytest run included the two new scoring-scope regressions, increasing the Stage 7 baseline from 1,620 to 1,622 passed tests.

## Final Git and operational state

- Branch unchanged: `codex/topic-pack-evidence-policy-20261111`
- HEAD unchanged: `8827219d1356da9b055cf8c9f5777c01a465dc52`
- Existing staged/unstaged/untracked work preserved. The final worktree includes the intended Stage 8 Topic Pack, promotion review, six Generated Bank, regression test, and report changes alongside prior-stage work.
- Commit: not performed
- Push: not performed
- Operational deployment / Bot restart: not performed
- New officially approved Facts: 0

No personal learner answers, attempt records, or private session data were included in this report.
