# Encoder frequency Anchor — reproduced scoring overcredit / bounded patch

## Fixed facts & scoring impact

- Owner: [Issue #42](https://github.com/now0930/prof_eng_answer/issues/42#issuecomment-7128118796).
- Exact reproduction base: `main@30b13262ad3899919edae7cb72be3ddeca677f18`.
- Requirement `encoder_frequency_limit_selection` is `importance=core` and part of an explicit 2-question scope. It is **not** in the four inspected exclusion/HOLD lists; this is not a claim of independent source approval.
- Actual Python `grade_deterministically` on the base SHA: `canonical: SATISFIED, B=4, C=6, total=12`; `opposite: SATISFIED, 4, 6, 12`; `mention: SATISFIED, 4, 8, 13.5`; `correct: PARTIAL, 3, 4, 9.75`. These scores are *whole-answer* and differences are not attributable to this Anchor alone.
- Root cause: `fact_anchor_evidence_adapter.py` grants `SATISFIED` from two of three core keywords, or token coverage, without asserting a relation or rejecting explicit contradiction. `calculate_deterministic_score` treats those rows as correctness/coverage evidence.
- Runtime production mode is **unobserved**; the base reproduction is a direct call, not proof of harm to operational grades.

## Proposed one-Anchor safeguard

Only the `speed_rotation_measurement_encoder_proximity_tachometer_selection_error/encoder_frequency_limit_selection` row is guarded: require explicit (a) device/counter maximum frequency selection/limit and (b) resolution-up → output-rate-up assertion for full `SATISFIED`. One supported relation earns at most `PARTIAL`. Denial, mere term lists and unsupported relations cannot earn full credit. If only mentions/contradictions are present, `MISSING` has **no answer evidence span** so it cannot spuriously receive partial B credit in the generic score engine. No new `WRONG`, `fatal`, `ceiling`, Hold status, grading weight or threshold is introduced.

This is a **bounded lexical relation safeguard**, not a general natural-language understanding engine. Contradictory, corrected, negated, hypothetical, symbol-only, multi-sentence or unfamiliar paraphrases may require further cases; do not generalize its result to 457 candidates. Correctness of the original physical `n×N_eff` claim versus manufacturer channel-Hz and decoded count-rate limits still requires independent source review. The **base source text and Fact approval are not changed** by this patch.

## Tests and release gate

Added `tests/test_encoder_frequency_admission_regression.py` for four unmodified replay answers, runtime direct grader path, isolated single-Anchor score contribution, alternate positive phrasing, negative/listing/quote/hypothetical cases and routing scope.

**NOT_RUN on this proposed SHA** — there is no executable remote Python runner in the connector. In a clean Codex worktree:
```bash
python3 -B -m pytest -q tests/test_encoder_frequency_admission_regression.py tests/test_deterministic_primary_grader.py tests/test_speed_rotation_measurement_encoder_proximity_tachometer_selection_error_topic_pack.py
# Only after focused pass
python3 -B scripts/release_candidate.py validate
```
Preserve exact SHA, exit codes, passed/failed/skipped, B/C grades and independent negative cases; if a new failure occurs, fix **this one scoped condition** only. Keep PR Draft and do not merge/deploy/promote Fact until release gate and semantic review are satisfactory. Preserve existing 119 HOLD, D4 and prior validated PR SHA.
