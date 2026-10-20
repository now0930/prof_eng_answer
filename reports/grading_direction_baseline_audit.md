# D/E direction baseline audit — 2026-10-20

## Repository and ownership

The operational checkout `/home/now0930/hermes/workspace/prof_eng_answer` is
clean at `af0dc33` on `codex/fact-grounded-grading-plan`, **not** `main`.
The writable development checkout is at the same commit with unrelated user
changes in `README.md` and `docs/operational_quality_checksheet.md`; preserve
both. The locally known GitHub `main` ref is `0bc808f`, two commits behind
this branch. Network freshness of that ref has not been established.

## Current scoring path

`grading_agents.run_agent_pipeline` enters `grade_deterministically` in
deterministic-primary mode. Routing and question contracts select Topic Pack
requirements; canonical claims and engineering invariants produce evidence and
error findings. `calculate_deterministic_score` groups requirements, computes
weighted requirement and correctness ratios, then assigns A/B/C. It currently
also assigns D from fixed judgment cue pairs and E from linkage cues via
`deterministic_score_evidence.evaluate_score_evidence`. These are lexical
proxies, not assessments of the quality of engineering judgment or interview
depth. D/E are capped by the requirement ratio. The score engine owns floors,
ceilings and final total; `bot.format_result` displays the stored grade.
Private session history and review data are downstream of grading, not score
inputs. Topic Packs/approved Fact anchors define technical facts; the ontology
captures canonical claims and engineering constraints.

## Reproduced private-session numbers (no answer text copied)

| Session | A | B | C | D | E | Raw | Final | Ceiling |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `20261019_115928_5960502198` | 3.00 | 2.586207 | 4.00 | 1.25 | 0.862069 | 11.70 | 11.00 | 11.00 |
| `regrade_20261019_130049_5960502198` | 3.00 | 4.363636 | 5.818182 | 1.25 | 1.00 | 15.43 | 14.50 | 14.50 |

For the regrade, the component sum is 15.431818; one `WRONG` requirement
causes `pass_evidence_eligible=false`, so the existing `25 × 0.58 = 14.5`
ceiling reduces the published result. Neither the raw sum nor the cap may be
silently changed during the D/E shadow work.

## Targets, protections, risks

Target: a separate, structured, quote-bound D/E shadow evaluator and private
learning/diagnosis projection. Protect A/B/C, requirement semantics, fatal
detection, existing score and Telegram path, Topic Packs and generated banks.
Risks: an LLM quote can be literal yet semantically wrong; a wrong claim can
be reused as positive D/E evidence; duplicate credit; provider variance;
missing expert labels; and confusing an `UNEVALUATED` shadow with zero or a
new final score. The current branch/main mismatch requires a later integration
decision; it does not authorize an implicit merge or deployment.

## Found and corrected during direction audit

The existing thermocouple/RTD cross-Topic evaluator allowed a quoted LLM
proposal to promote `PARTIAL` to `SATISFIED`. That could indirectly alter B/C
despite a deterministic final score calculator. The current change preserves
the quote only as `score_effect=none` review data; requirement rows, A/B/C and
the final score must be identical with and without an LLM response. This is a
necessary authority-boundary correction, not a new positive scoring rule.
