# EMC dependency Claim — bounded defect fix review (2026-11-24)

- Owner: [Issue #42](https://github.com/now0930/prof_eng_answer/issues/42), first of three WIP defects.
- Source baseline: `main@30b13262ad3899919edae7cb72be3ddeca677f18`.
- Scope: exactly one Machine Contract requirement, `ipgse_shield_termination_frequency`; all other grading policies unchanged.
- Authority: **DRAFT / NOT_RELEASED / NOT_ADMITTED**. Do not merge, deploy or change D4/119 HOLD. This report does not claim that the new branch passed the repository's pytest or Release Gate.

## Proven source-path gap

The existing Machine Contract fact `emc_shield_termination_depends_on_conditions` requires `(emc_shield,depends_on,emc_frequency_bonding,positive)`. Its only requirement is `ipgse_shield_termination_frequency` with minimum 1 match.

The actual `grading/evidence/canonical_claim_extractor.py` loads aliases from `grading_ontology/canonical_predicates.json` and returns no relation when `predicates.get(predicate_id, [])` has no match. The base ontology lacks `depends_on`. This proves the required **exact relation cannot be emitted by this deterministic grammar path**. It does **not** by itself prove the downstream production grade wrongly scored a real answer; such a run has not been performed.

Simply substituting `qualified_by` is *unsafe*: its alias `조건` is literally contained in the concept alias `주파수·본딩 조건`. A mention-only sentence could therefore falsely match. Likewise the original concept alias `주파수` could satisfy a composite frequency-and-bonding object without bonding evidence. The existing negative grammar does not recognize `-지 않다`, potentially accepting `달라지지 않는다` or `결정되지 않는다` as positive after a naïve predicate fix.

## Narrow proposed changes (only in isolated draft branch)

1. Add **`depends_on`** with explicit dependence phrases (not generic `조건`/`따라`) to the existing canonical predicate ontology, preserving the Machine Fact ID and its current contract.
2. Remove the overly generic `주파수` alias solely from `emc_frequency_bonding`; retain its two combined frequency+bonding aliases.
3. Recognize Korean `-지 않다` negative surface grammar **only for `depends_on`** within the existing `_polarity()`; do not change global predicate handling, scoring, or machine contract.
4. Add a focused `unittest` set in `tests/test_emc_dependency_claim_regression.py` exercising the actual extractor → canonical evidence → deterministic evaluator, not hardcoded answer scoring.

## Test matrix and gate

| Synthetic answer / condition | Expected target state after patch | Original issue addressed |
| --- | --- | --- |
| `차폐 케이블은 주파수·본딩 조건에 따라 달라진다.` | SATISFIED | Missing predicate |
| `... 달라지지 않는다.` | WRONG | Negative must not get positive credit |
| `... 결정되지 않는다.` | WRONG | Negative must not get positive credit |
| `... 조건이라는 용어를 정리한다.` | not SATISFIED | Mention is not dependency |
| `차폐 케이블과 주파수·본딩 조건을 함께 표시한다.` | not SATISFIED | Mere co-occurrence must not credit |
| `차폐 케이블은 주파수에 따라 달라진다.` | not SATISFIED | Bonding condition absent |
| Quoted positive claim, without endorsement | not SATISFIED | Quotation may not receive credit |
| Same answer under another Topic owner | no EMC dependency claim | Cross-topic exclusion |
| Empty answer vs positive answer | only target requirement changes | No unintended scoring spread |
| Repeat identical answer | deterministic same result | Stability |

**Source support for engineering scope (not blanket grounding rule):** [NI Field Wiring and Noise Considerations for Analog Signals](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), grounding/shield coupling and the hazards of both-end ground currents; [Analog Devices EMI/RFI and Shielding Concepts MT-095](https://www.analog.com/media/en/training-seminars/tutorials/MT-095.pdf), frequency-dependent termination considerations. These support dependency on installation and noise regime rather than an unconditional one-end or both-end rule.

### Release requirements

- Run `python3 -B -m pytest -q tests/test_emc_dependency_claim_regression.py tests/test_canonical_claim_extractor.py tests/test_deterministic_requirement_evaluator.py` on the exact new SHA.
- Run `python3 -B scripts/release_candidate.py validate`, preserving total passed/failed/skipped, exit code, and SHA. Run `python3 -B scripts/rubric_manager.py validate-all` if supported by current CLI.
- Any regression failure must be fixed **only** in this bounded branch and rerun on the new SHA.
- Inspect independent positive/negative synthetic answers in the actual grading path and confirm no unexpected credit or WRONG; missing and unresolved must fail closed.
- This branch only becomes eligible for code review when focused and full Release gates pass. Production score admission, canonical Fact promotion, main merge, deployment, bot restart, or D4 reopening are prohibited.

## Evidence granularity

The bounded local Python grammar check reproduced the missing alias path, a naïve `qualified_by` mention-only false-positive risk and `-지 않다` negation risk. That grammar check is **not** equivalent to executing the full repository. The new focused repository tests are committed but **NOT_RUN** until a real runner executes them at the new branch SHA.
