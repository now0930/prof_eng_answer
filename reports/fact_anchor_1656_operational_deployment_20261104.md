# Fact Anchor 1,656 review checkpoint: operational deployment

Date: 2026-11-04 (Asia/Seoul). Branch:
`codex/essay-boundary-calibration-20261028`. Deployed code commit:
`78cf0249f8e0d9faa411af43ade06f951e8b84a8`.

## What is and is not complete

The 1,656-row proposal package passed identity and hash checks against the
current Topic Pack sources. Its candidate data is staged privately, with **0
new Fact approvals**. Existing strict-verdict rows (415) were not rewritten;
the 1,135 new supported/scope-supported proposals have not had individual
source, question-scope and duplicate-credit admission completed. Of the 25
proposed holds, 22 new runtime holds are active and three previously promoted
SIL/Nyquist requirements remain live pending a protected-contract review.
All 81 proposed non-scoring/routing rows are now blocked. Current total:
2,092 Topic Pack Anchors, 539 scoring-blocked, 1,553 non-blocked. A
non-blocked Anchor is not proof of independent fact verification.

**The requested 1,656/1,656 technical verification and final promotion is
not complete.** The validation gate proves software consistency only; it
cannot turn proposal labels into source-grounded technical approvals.

## Verification and deployment

- The development branch passed `python3 scripts/rubric_manager.py
  validate-all`, full `PROMOTE_GENERATED=0 scripts/validate_release.sh`, and
  `python3 -m pytest -q` (1,461 passed, 1 skipped, 1 warning) before deployment.
- The Docker Compose service mounts a separate checkout. That checkout was
  clean except for one untracked private WordPress DB; the DB was checksum-
  backed up outside the checkout and its checksum was unchanged after the
  branch switch. There were no exact ignored-file collisions with the target
  branch. The checkout was switched from its older `main` to the verified
  branch at `78cf024` without reset or deletion.
- `prof_eng_answer_bot` was restarted. Its `python -u bot.py` process remained
  running at post-restart check.
- The first deterministic-only smoke run under the **production** environment
  failed its zero-provider-call assertion because `QUALITATIVE_DE_MODE=argon`
  legitimately attempted one D/E provider call. Re-running the deterministic
  smoke with `QUALITATIVE_DE_MODE=off` passed: deterministic marker, fatal
  detection, no external verdict authority, persisted result.
- A separate synthetic, non-private temperature-sensor answer under the
  actual production setting returned a final score of 8.25/25, provider-call
  count 1, `de_status=APPLIED`, and `llm_verdict_authority=0`. This confirms
  execution, **not** score-quality calibration or a Telegram end-to-end test.

## Documentation and grading recheck (same date)

- README, architecture, Fact eligibility, roadmap and runbook now distinguish
  the 539 blocked / 1,553 non-blocked operational counts from technical
  verification. The deterministic-only smoke explicitly disables optional
  D/E assistance during its own test, then restores the prior setting.
- The deterministic-only production-entrypoint smoke passed with zero provider
  calls, fatal detection and persisted result. `validate-all` passed, and the
  full pytest run passed (1,461 passed, 1 skipped, 1 pre-existing warning).
  The full non-promoting Release Gate also passed; its separate opt-in P0
  ten-run reproducibility check was skipped by the gate configuration.
- A separate public synthetic thermocouple/RTD answer produced 14.34/25 on
  the deterministic-primary entrypoint and routed to the thermocouple Topic.
  The test injected a non-network provider stub; its reported
  `provider_calls=1` is an attempted optional call, not proof that an
  external model evaluated the answer. This is an execution smoke, not an
  expert score-calibration result or a Telegram end-to-end test.

## Next technical work

Individually adjudicate the 1,135 new proposed Fact statements and their
question/duplicate-credit ownership, plus the three existing SIL/Nyquist
contract conflicts. Do not promote candidates merely to reach a count. Keep
source hashes and previous strict verdicts, then rerun focused grading
regressions and release validation for every bounded promotion batch.
