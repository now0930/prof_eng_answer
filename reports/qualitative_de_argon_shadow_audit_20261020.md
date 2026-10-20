# D/E Argon shadow exploratory audit — 2026-10-20

## Boundary

Only three publicly tracked, reviewed calibration fixtures were sent to the
Google Gemini API with the user's explicit approval. No private answer session,
WordPress database or Telegram message was sent. `gemini-4-argon` was used via
the Interactions API. This was an exploratory shadow test, not a release of D/E
score authority. The final 25-point grade, A/B/C, `WRONG` and fatal policies
were unchanged. Raw answers and credentials are not included here.

## Observations

| Public case ID | Purpose | Valid runs | D proposals | E proposals | Within-case dispersion |
| --- | --- | ---: | --- | --- | --- |
| `qtype_qg-cs-high-01` | high-quality comparison | 2/2 | 6, 6 | 2, 2 | 0 |
| `qtype_qg-cs-low-01` | low-quality comparison | 2/2 | 2, 2 | 0, 0 | 0 |
| `mcdc_vmodel_sil_issue1` | answer with verified technical errors | 2/2 | 3, 3 | 0, 0 | 0 |

All six proposals passed literal-quote, Topic-scope, positive-evidence and
non-duplication validation. The model separated the high- and low-quality
cases and did not grant E credit to the error case. This does **not** establish
agreement with an independent expert D/E label. On one additional inspection
of the error case, positive D1–D3 reasons were tied to partial, literal answer
excerpts; E1–E2 were zero. That is a narrow reason audit, not a proof that the
proposed points are the only defensible expert scores.

Earlier local `qwen3.5:9b` and `glm-4.7-flash` trials remained `UNEVALUATED`
because they reused an evidence ID for multiple positive criteria. Increasing
Ollama context size fixed premature truncation but did not justify relaxing
the duplicate-credit guard. The Argon prompt excludes short bare headings
from evidence options and requires each reason to be supported by its selected
excerpt.

## Decision and next evidence

**Shadow evaluation: technically callable and provisionally promising.**
**Final-score authority: NO-GO.** Three cases, two repetitions each and one
manual reason inspection are insufficient to establish cross-topic accuracy,
calibration or acceptable failure rate. Before score promotion, compare a
pre-declared broader sample against independently reviewed D1–E2 labels,
including wrong-answer and terse-answer edge cases, and define the exact
fallback and final-score ceiling policy. Do not treat structural validity or
zero within-case dispersion as semantic truth.

## Subsequent operational decision

After this exploratory report, the user authorized bounded use of Argon D/E
in the final grade and ongoing operational review. The adapter is opt-in;
accepted D/E proposals stay under deterministic requirement ceilings, while
A/B/C, fatal findings and verdict policy are unchanged. Provider or validation
failure falls back to deterministic D/E. This operational choice does not
retroactively turn the six shadow runs into independent expert labels. Score
disputes and provider failures should be recorded in private quality check
sheets, then reviewed against expert criteria before prompt or policy changes.
