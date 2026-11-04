# 63-Fact private review package: admission preflight

Date: 2026-11-04. Work branch: `codex/essay-boundary-calibration-20261028`.
Input ZIP SHA-256: `1d51645bdd99ecee61e0022ed24f3db75a1548e4c9f214a5e1ca53280dd37bd9`.
The ZIP and its raw CSV remain outside the public repository. This report
records aggregate findings only; it is **not** a technical approval.

## Identity and current state

- Combined candidate CSV: 63 unique Fact IDs. New 13-item CSV: 13 unique IDs.
- All 63 Fact/Topic/Anchor identities exist and match the current Registry.
  The 63 recorded Topic statement SHA-256 values match the current work branch.
- The ZIP's GitHub `main` reference (`1afe8b52`) matches fetched `origin/main`.
  The active work branch has additional review/hold changes and must not be
  replaced with `main` or the ZIP snapshot.
- **All 63 remain blocked** by current overlays: 25 revision holds, 9
  insufficient-source holds, 3 reviewed-but-not-promoted holds, 19 noncore
  exclusions, 5 scoped exclusions, 2 correction/overgeneralization exclusions.
- The separate nine IDs described as independent/scoped in the work order are
  not members of these 63. All nine are already blocked in current overlays;
  no unblocking is warranted merely because their classification is proposed.

## Evidence and grading-admission gaps in the package itself

- `final_promotion_decision`: `NOT_APPROVED` on all 63 rows.
- Newly checked 13: the ZIP proposes minimal technical statements and source
  locators, but explicitly records zero runtime score changes and no Release
  Gate run. These source reviews still need current-claim, question-scope and
  duplicate-credit integration on this branch.
- Independent `gpt-6-luna` primary-source cross-check of those 13 found
  technical support for all 13 **within their stated source scope**, but
  only 10 look potentially eligible as general-core candidates. Three stay
  held for general scoring: `fisher_bench_set_is_actuator_spring_adjustment_reference`
  (Fisher model-specific bench-set procedure),
  `industrial_wireless_site_survey_rf_environment_and_operational_link_validation`
  (WirelessHART evidence does not cover the linked ISA100.11a question and a
  site survey is not universally required), and
  `pneumatic_force_balance_transmitter_chain` (SAMSON-specific pneumatic
  architecture does not satisfy a generic pneumatic-and-electronic question).
  This independent check is technical review, **not** runtime authorization.
- Prior 50: the ZIP says **not reverified in this pass**. Across the combined
  packet, evidence status is 26 current-round direct review, 12 prior direct
  review not rechecked, 9 prior partial review not rechecked, and 16 not
  source-verified. These labels are not interchangeable with admission.
- `question_contract_check`: `PENDING` on all 63 rows. Existing question
  patterns reference the 13 new IDs syntactically (1–3 patterns each), but
  that does not prove the Anchor is mandatory for the exact question demand.
- `duplicate_score_check`: `PENDING` on 61 rows; two rows explicitly require
  one RTD resistance-measurement credit owner. No blanket 63-item `must`
  promotion can satisfy the single-owner rule.

## Safe decision

Validation on this checkout: `python3 scripts/rubric_manager.py validate-all`
passed. The first `PROMOTE_GENERATED=0 scripts/validate_release.sh` run was
interrupted after several slow host-regression groups; a full retry then
completed with exit code 0, including `TOPIC_CONTENT_AUDIT=PASS` (89 topics,
2,092 anchors). The optional dedicated 10-run reproducibility gate was not
enabled. This is a baseline validation only, **not** promotion approval. No
operational Fact, hold overlay, scoring rule, or generated bank was changed.

Do **not** remove the 63 holds, add 63 required anchors, change A–E scoring,
or assert Release Gate PASS from this ZIP. The work order itself requires
current-source, question-contract and duplicate-credit checks and says
problematic items must not be automatically promoted. The proposed 5
independent-credit exclusions and 4 conditional facts remain blocked while
their exact question-owned contracts are designed; current overlays already
prevent them from general scoring.

Next implementable units: (1) current-source and question-scope review for
the 13 with explicit single-owner regressions; (2) separate evidence work for
the 50, prioritizing the 16 unverified and 9 partial cases; (3) explicit
question-only contracts for the four conditional facts if technically
supported. Promote one bounded batch only after managed Topic generation,
focused correct/incorrect/paraphrase/out-of-scope tests, `validate-all` and
full Release Gate. Keep raw ZIP/CSV and any returned review results private.
