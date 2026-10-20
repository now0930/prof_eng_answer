# D/E qualitative shadow contract

`GRADING_DIRECTION_CONTRACT.md` governs this experimental, score-neutral path.
It does not replace the currently deployed D/E or the final 25-point grade.

## Inputs and authority

`grading.qualitative.de_shadow.evaluate_qualitative_de(question, answer,
abc_result, topic_context, llm_call=None, model_metadata=None)` accepts an
already completed deterministic A/B/C breakdown, requirement rows with literal
answer spans, routed Topic IDs and optional verified Fact excerpts. The LLM
receives these as context; answer text is untrusted data. The LLM response is a
proposal, never an authority over A/B/C, `WRONG`, fatal findings or total score.

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

## Transition rule

Current deterministic D/E and `bot.format_result` are unchanged. A future
qualitative-authority mode must treat failed D/E evaluation as `UNEVALUATED`,
must not manufacture a final 25-point score, and must reconcile the existing
`WRONG` pass ceiling before switching live scoring. This is intentionally not
implemented in the shadow phase.
