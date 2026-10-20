# D/E qualitative shadow contract

`GRADING_DIRECTION_CONTRACT.md` governs bounded D/E score authority. This
shadow evaluator remains score-neutral by itself; the explicit opt-in adapter
may use a validated proposal to replace D/E in the final 25-point grade.

## Inputs and authority

`grading.qualitative.de_shadow.evaluate_qualitative_de(question, answer,
abc_result, topic_context, llm_call=None, model_metadata=None)` accepts an
already completed deterministic A/B/C breakdown, requirement rows with literal
answer spans, routed Topic IDs and optional verified Fact excerpts. The LLM
receives these as context; answer text is untrusted data. The LLM response is a
proposal, never an authority over A/B/C, `WRONG` or fatal findings. Only
validated D/E proposals can change the deterministically recomputed total.

## Output

Each `criteria` row has `criterion_id`, `score`, `reason`, `topic_id`, `quote`,
`start`, `end`. D1 (technical choice), D2 (grounds and conditions), D3
(alternatives, limitations and trade-offs) each have a 0–2 proposed range.
E1 (specific technical follow-up question) and E2 (answer-grounded ability to
explain it) each have a 0–1 proposed range. Interview questions (up to three)
carry a program-generated stable ID, quoted answer span, Topic ID, question,
reason and expected explanation elements. They remain review candidates, not
Master facts.

The evaluator returns either `SHADOW_VALIDATED` (structurally validated but
`semantic_truth_verified=false`) or `UNEVALUATED` with a reason code.
`score_effect=none` in both cases. No `total_score` is emitted. If unavailable
or invalid, D/E is **not** 0; it is unassessed. `model_metadata`, `input_hash`,
`request_hash`, and provider-call count support repeated evaluation audits
without publishing answer text.

The prompt also includes four **synthetic, topic-neutral scoring examples**
(`grading/qualitative/prompt_examples.py`): a partially supported choice,
a generic conclusion without evidence, a claim already marked `WRONG` by
A/B/C, and a fully supported choice with distinct grounds. The illustrative
0–2/0–1 scores calibrate the scale; they are not model
answers, live Topic facts, or expert labels. Current-question A/B/C and literal
answer evidence take precedence. The example version is included in the hashed
request, so later policy changes remain auditable. No example can authorize an
LLM to change the deterministic result or the final score.

`project_deterministic_shadow_input` forms the shadow scope from the owner
Topic IDs of already established requirement rows. It does **not** pass all
router candidates to D/E: a router candidate unrelated to the question must
not become a qualitative credit source. The current adapter supplies no
additional `verified_facts`; the deterministic requirement judgments and
their cited spans are the only technical-evidence boundary in this run.

For a reviewed calibration case, `scripts/run_qualitative_de_repeatability.py`
rebuilds the deterministic input and repeats the shadow evaluation. Its stdout
contains hashes, status counts, proposed-score dispersion and model metadata,
but no answer or answer quotation. A provider-free dry run intentionally exits
2 with `INCOMPLETE`, not a fabricated zero score. Live Ollama use is opt-in:

```bash
OLLAMA_URL=http://ollama:11434 OLLAMA_MODEL=<installed-model> \
  python3 -B scripts/run_qualitative_de_repeatability.py \
  --case-id qtype_qg-cs-high-01 --provider ollama --runs 3
```

Run this only in an authorized environment for transferring the calibration
question and answer to the selected model. Repeated structural acceptance is
**not** expert agreement; all reports retain `acceptance_status=REVIEW_REQUIRED`.
For approved, publicly tracked calibration fixtures only, Gemini 4 Argon can
be exercised with `--provider argon` and `GEMINI_API_KEY` set in the process
environment. The adapter uses the Interactions API with structured JSON,
medium thinking and a 32,768-token ceiling. It never reads private sessions
or credentials from disk itself. The caller must separately decide which
fixture and credential source are authorized. See
`reports/qualitative_de_argon_shadow_audit_20261020.md` for the first
score-neutral quality observations.
The local Ollama adapter now supplies literal, uniquely located evidence
options and asks the model to select IDs. The program converts IDs back to
exact quotations and offsets before the original validator runs. It rejects
unknown IDs, unrelated Topic IDs, WRONG-overlapping spans, duplicate positive
credit and truncated model output. This has not yet produced a passing live
repeatability result; see `reports/grading_direction_operational_decision.md`.

## Program validation and known limits

The validator rejects score overflow, unapproved Topic IDs, missing or altered
literal quote/spans, positive evidence overlapping `WRONG`, positive evidence
without a deterministic supported Fact span, exact duplicate positive evidence,
malformed schema, and LLM attempts to set a final/ABC score. It does not prove
that a semantically plausible interpretation is technically true or that all
expressions of judgment were recalled; expert D/E labels and repeated live
model runs are required before operational promotion.

The optional `shadow_storage` module writes only to an explicitly supplied
private path with exclusive creation and 0600 permissions. Its learning and
diagnosis projections are `candidate`/score-neutral; they cannot update Master
Topic Packs or review history automatically. These are staging envelopes, **not**
the existing `training_projection.schema.json` or
`diagnosis_projection.schema.json` views; a reviewed adapter is needed before a
trainer or diagnoser consumes them.

## Operational promotion

`QUALITATIVE_DE_MODE=argon` enables the bounded adapter. The default `off`
keeps deterministic D/E. Validated proposals replace only D/E; existing
requirement ceilings, fatal caps and verdict rules still apply. An invalid or
unavailable proposal triggers a disclosed `FALLBACK` to deterministic D/E.
The shadow evaluator's own `score_effect=none` and
`semantic_truth_verified=false` remain accurate: its output is structurally
accepted, not expert-verified. Operational disputes go to the private quality
check sheet for later review.
