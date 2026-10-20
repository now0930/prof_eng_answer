# Grading direction contract — D/E qualitative shadow

Status: development/shadow; not an authorization to change live grades. Baseline: 2026-10-20.

## Purpose and authority

The 25-point rubric remains A 3, B 6, C 8, D 6, E 2. A/B/C and the
`SATISFIED`/`PARTIAL`/`WRONG`/`MISSING` requirement decisions belong to the
deterministic engine, approved Master Topic Pack and Engineering Ontology.
The LLM may propose only D1–D3 and E1–E2 qualitative evidence and at most
three interview questions. The program validates the proposal. An LLM cannot
change A/B/C, a verified error, a fatal finding, a Topic Pack, or a final total.

## Scope

Allowed now: read-only baseline audit; separate shadow evaluator and private
shadow persistence; direction guards, tests, and non-scoring learning/diagnosis
projection. Preserve legacy D/E scoring and production outputs for comparison.

Forbidden now: modifying generated banks or Topic Packs, silently changing
score ceilings, replacing production D/E or Telegram totals, treating a model
proposal as verified semantic truth, publishing answers/sessions/credentials,
or creating a final 25-point score when D/E is `UNEVALUATED` in a future
qualitative-authority mode. An unresolved proposal is not a zero-point score.

## Failure and uncertainty

For a provider failure, malformed JSON, bad quote/span, wrong-topic evidence,
contradiction with deterministic `WRONG`, duplicate positive credit, or uncertain
meaning, the shadow result is `UNEVALUATED` with reason codes. Existing live
deterministic scores are unchanged. Static checks prove only shape and literal
provenance, not the truth of a technical interpretation.

## Release and transition

Any production D/E switch needs an independently reviewed expert benchmark,
repeatability study, explicit acceptance criteria, a ceiling-policy decision,
full release regression and a separate deployment decision. Until then the
shadow has `score_effect=none`, no Telegram score mutation and no automatic
promotion of interview questions to Master facts.
