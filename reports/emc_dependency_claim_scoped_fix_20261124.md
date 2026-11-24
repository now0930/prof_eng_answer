# EMC depends_on: exclusion-first convergence and rollback of non-scoring patch

Date: 2026-11-24. Owner: Issue #42, Draft PR #43. Source baseline: `main@30b13262ad3899919edae7cb72be3ddeca677f18`.

## Decision

**The requested positive-score behavior was invalid because of the existing exclusion policy.** `grading/evidence/fact_anchor_scoring_exclusions_20261101.json` excludes `(instrumentation_power_grounding_shielding_ups_ground_loop_emc, ipgse_shield_termination_frequency)` with reason `noncore_detail`. `grading/scoring/deterministic_requirement_evaluator.py` intentionally omits an excluded positive requirement unless an independently detected invariant has violated that same requirement.

The earlier PR #43 added a global `depends_on` predicate alias, narrowed an EMC concept alias, and changed its negation behavior. The original structural gap did exist at the extraction layer, but there is **no established actual positive-scoring defect to fix** for this excluded requirement. The earlier 7 focused failures arose from assuming the excluded requirement must appear as SATISFIED or WRONG; that was the wrong oracle. Reverting all three production-source changes is the minimal, lowest-risk resolution.

### The exception that must remain

The Machine Contract binds `EMC_SHIELD_ONE_END_UNIVERSAL` to `ipgse_shield_termination_frequency` with fatal classification. The deterministic evaluator must still emit `WRONG` and fatal on an **independently detected** violation. Do not confuse an explicit global invariant with negative claims heuristically extracted from a noncore excluded statement.

### New test-only boundary

The focused test file `tests/test_emc_dependency_claim_regression.py` now verifies the actual repository evaluation policy:
- A positive answer, a direct exact positive claim, negative statement, quoted statement, hypothesis, and frequency-only mention do not cause the excluded requirement to appear or earn positive score.
- A direct negative machine claim without an independent invariant does not invent `WRONG`.
- An independently supplied real invariant `EMC_SHIELD_ONE_END_UNIVERSAL` still yields `WRONG`, fatal and blocks full credit.
- No duplicate credit; no upstream LLM authority.

**A missing requirement row is intentional: do not coerce it to UNKNOWN/MISSING/WRONG or synthesize SATISFIED.** This test-only change does not grant approval, score admission or release of any Fact.

## Verification gates

Codex earlier executed PR #43's pre-rollback original focused suite: **18 passed, 7 failed**. This result belongs to `6e30e01350d8f751d566d30a0a62dd3a4485a503`, NOT this corrected commit.

This corrected test-only revision must still run:
```bash
python3 -B -m pytest -q tests/test_emc_dependency_claim_regression.py tests/test_canonical_claim_extractor.py tests/test_deterministic_requirement_evaluator.py
python3 -B scripts/release_candidate.py validate
```
The test-only branch remains **NOT_VALIDATED / Draft / UNMERGED** until actual same-SHA focused and full gates pass. No GitHub Actions run or passed count may be invented. If a test fails, inspect whether it assumes a wrong admission policy before changing any production logic.

## Convergence and next WIP

- **Cause of BLOCKED:** invalid test expectation for an intentionally excluded Requirement.
- **Resolution type:** NO_PRODUCTION_CHANGE; preserve score exclusion and independent fatal.
- **Remaining extractor issues:** Korean double negation and hypotheticals have been observed in non-scoring extraction; they do **not** justify broad production changes absent a reproducible defect in an admitted scoring path.
- **Next eligible issue:** after this policy-protection test passes, investigate encoder frequency vs decoder count rate only if its specific requirement is actually admitted to scoring.
- PR #41 validated SHA remains untouched. 119 HOLD, D4, A–C deterministic authority, all canonical Fact/Registry and score policy stay unchanged.
