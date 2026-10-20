# D/E shadow validation review — 2026-10-20

## Phase and Gate status

| Phase | Result | Evidence |
|---|---|---|
| 0 baseline audit | PASS | `reports/grading_direction_baseline_audit.md`; two private sessions' numeric scores reproduced without copying answer text |
| 1 direction contract | PASS for scope | `GRADING_DIRECTION_CONTRACT.md`, `scripts/check_grading_direction.py` |
| 2 independent shadow | PASS for structure | `grading/qualitative/`; production score owner and Topic Packs untouched |
| 3 synthetic contract tests | PASS for tested invariants | `tests/test_qualitative_de_shadow.py`, cross-Topic and checksheet regressions; no real-model quality claim |
| 3 repeated live LLM evaluation | REVIEW_REQUIRED | Local Ollama trials were run; all tested proposals were rejected by structural or evidence gates. See `grading_direction_operational_decision.md` |
| 3 expert D/E agreement | REVIEW_REQUIRED | 48 existing expert cases have demand, finding and total-range labels but no D1–E2 expert labels; a deterministic 25-case worklist and blank label contract are now available |
| 4 operating switch | NOT_STARTED | No expert D/E acceptance criterion, ceiling-policy decision, or authorized deployment |

## Six-case comparison coverage

Synthetic tests cover a bounded technical choice/grounds/alternative/follow-up
proposal, generic conclusion without verified technical span, verified wrong
claim, fabricated quote, duplicate positive evidence, technical paraphrase and
unsupported model output. These tests prove rejection/serialization behavior
only. They do not measure a real model's sensitivity to a deleted conclusion,
an enriched decision, or a paraphrase; those require independent model runs and
expert labels.

The A/B/C authority audit found that the pre-existing cross-Topic LLM path
could promote `PARTIAL` to `SATISFIED`. It now records only score-neutral
suggestions. A provider response may be present, but requirement statuses,
A/B/C components and total remain the same as the provider-free run. The
private temperature answer was checked read-only: both paths retain 14.5 and
the same 6/4/1/0 requirement summary. The quality checksheet recognizes a
diagnostic-only provider call without falsely reporting score ownership.

## Ceiling policy review

The regraded temperature answer has `A+B+C+D+E = 15.431818`, but one `WRONG`
requirement makes `pass_evidence_eligible=false`; the existing 14.5 ceiling
therefore yields 14.5. This ceiling remains untouched. Whether a future
qualitative D/E proposal may change the raw sum while the ceiling holds must
be decided and tested separately; the shadow never applies its proposed D/E.

## Direction audit

G0 repository/user changes protected: PASS. G1 initial purpose: PASS. G2 A/B/C
authority: PASS after the cross-Topic score-neutral correction and runtime
invariance regression. G3 LLM limited to D/E proposal: PASS for implemented
module; existing cross-Topic technical suggestions are also score-neutral.
G4 quote/error/duplicate gates: PASS for literal checks; semantic correctness
REVIEW_REQUIRED. G5 final/ceiling
unchanged: PASS in shadow, operational policy REVIEW_REQUIRED. G6 expert and
repeated live evaluation: REVIEW_REQUIRED. G7 regression: PASS —
`PROMOTE_GENERATED=0 scripts/validate_release.sh` exited 0 on 2026-10-20,
`python3 scripts/rubric_manager.py validate-all` reported `ALL VALID`, and
the new D/E shadow, benchmark and literal-evidence focused pytest run passed
23 cases after the scoped-input and repeatability additions. The dedicated
10-run P0 reproducibility gate was opt-in and skipped. G8 training/diagnosis
candidate staging and Master immutability:
PASS for the score-neutral interface; existing View consumption REVIEW_REQUIRED.

No failing gate was bypassed. The unresolved expert and provider checks prevent
claiming that the new D/E assessment is ready for operational scoring.

## Repeatability input and scope check

The shadow input adapter uses the Topic owners of deterministic requirement
rows, not all preliminary router candidates. On the temperature comparison
fixture, this excludes the unrelated second-order lag candidate while retaining
the thermocouple and RTD owners. A three-run synthetic provider test shows that
varying D1 suggestions are reported as a range, never silently converted to a
final grade. A two-run provider-free calibration dry run returned
`INCOMPLETE`, two `provider_not_configured` reasons, zero provider calls and
no D/E values. The provider-free exit code 2 is expected and is **not** a live
repeatability result. The 25-case worklist includes reviewed demand labels,
not independent expert D/E scores; model-answer and risk-mutation sources must
be interpreted as separate case strata during later expert comparison.

All 25 selected cases were also passed through the existing deterministic
grader and scoped-input adapter without an LLM call: 25/25 produced a D/E
shadow-ready input, five per question type. This confirms input construction,
not whether the deterministic requirement judgments or eventual D/E proposals
agree with an expert.

The sandboxed development environment does not expose model settings. An
approved connection to the existing host-local Ollama allowed
bounded live trials on one calibration case. None passed the full validator;
details are recorded in `grading_direction_operational_decision.md`.
Independently reviewed D1–E2 labels and a passing repeatability study are
still required before G6 can move beyond `REVIEW_REQUIRED`.

## Expert D/E worklist prepared

`scripts/prepare_qualitative_de_benchmark.py` selects 25 reviewed cases, five
per canonical question type, while rotating available source kinds. Its manifest
contains case IDs, source references and question/answer hashes, **not** copied
answer text. The blank label sheet has D1–D3/E1–E2 fields but is deliberately
invalid as expert truth until an identified reviewer records scores, reasons,
literal evidence spans and review time. To prepare local files:

```bash
python3 -B scripts/prepare_qualitative_de_benchmark.py \
  --manifest /tmp/qualitative_de_benchmark_manifest.json \
  --blank-labels /tmp/qualitative_de_benchmark_labels.json
```

After independent expert review, validate the completed sheet with
`--validate-labels /path/to/completed_labels.json`. A valid schema only proves
provenance and evidence location; it does not itself establish the quality of
the expert judgment. Keep completed sheets and any answer excerpts out of a
public commit. Provider repeatability and score-ceiling policy remain separate
unmet gates.
