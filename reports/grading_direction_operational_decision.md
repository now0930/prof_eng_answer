# D/E qualitative shadow operational decision — 2026-10-20

## Decision

- Existing deterministic `/grade` and `regrade_to_telegram.py`: **GO**. They remain
  the only authority for A/B/C/D/E and the final 25-point score.
- Qualitative D/E LLM proposal: **SHADOW ONLY**, `score_effect=none`.
- Qualitative D/E as final-score authority: **NO-GO**. Do not switch Telegram
  totals or treat an invalid proposal as zero.

This is a bounded deployment decision, not an assertion that the shadow
evaluator has met its original completion criteria.

## Evidence

- 25/25 reviewed calibration cases construct deterministic A/B/C and scoped
  D/E input. This is an input-availability check, not expert agreement.
- A provider-free run gives `UNEVALUATED`, no D/E values and no provider calls.
- Local `gemma4:e4b` initial three-run trial: 0/3 structurally valid; two
  JSON parsing failures and one score-range failure.
- Local `qwen3.5:9b` initial three-run trial: 0/3 structurally valid; empty
  or invalid JSON. Turning off model thinking and constraining JSON resolved
  the output-shape issue but exposed invented literal quotations.
- A quote-only repair was limited to unique exact answer substrings. It never
  accepts paraphrased or ambiguous model text.
- Program-created evidence IDs removed free-form model quotations. The same
  qwen case still failed 2/2 because it reused a positive evidence ID; the
  duplicate-credit guard was not relaxed. The gemma evidence-ID trial failed
  2/2 due to truncated model output.
- No independently reviewed D1–E2 scores exist for the 25-case worklist.
  Current expert labels cover demand/finding/total ranges only.

These failures are observed on one calibration case and are not extrapolated
to model accuracy across all topics. No numerical quality acceptance threshold
was invented to make the result pass.

Release verification after the final code changes: `PROMOTE_GENERATED=0
scripts/validate_release.sh` exited 0, `rubric_manager.py validate-all`
reported `ALL VALID`, and 23 focused pytest cases passed. The separate opt-in
10-run P0 grading reproducibility gate was not invoked; it is not evidence for
or against D/E qualitative accuracy.

## Operating boundary

The existing Telegram regrade command remains available:

```bash
cd /home/now0930/hermes
bash workspace/prof_eng_answer/scripts/run_telegram_regrade.sh \
  session <SESSION_ID> --dry-run --no-source-text
```

Remove `--dry-run` only when the user intends a Telegram send. Regrade creates
a new `regrade_*` session and does not mutate the original. D/E Shadow results,
if run separately, are not sent as a grade.

## Deployment and smoke result

The bounded shadow/code changes were committed as `e28c3ff` on
`codex/fact-grounded-grading-plan`, pushed, fast-forwarded into the clean
Hermes operating checkout, and the existing bot container was restarted.
In-container D/E contract tests passed 16/16. A dry-run regrade of the private
temperature-comparison source session passed 1/1 with final 14.5/25,
`provider_calls=0`, and no Telegram send. It created a separate private
`regrade_*` session; the original source was not overwritten. The bot remained
running after the test. This proves the legacy deterministic regrade can be
invoked now; it does not promote qualitative D/E to score authority.

To reconsider qualitative D/E authority, first obtain independent expert
D1–E2 labels, establish a pre-declared acceptance criterion, demonstrate
repeatable valid proposals on the selected set, reconcile the existing WRONG
ceiling, and rerun the full release gate. Do not bypass any of these gates by
changing labels or accepting malformed model output.
