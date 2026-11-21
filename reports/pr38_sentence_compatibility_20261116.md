# Fact sentence / grading reference compatibility

The first implementation is explicitly opt-in for the reviewed relative-humidity definition. Its human-readable `statement` is the concise, independently reviewed first sentence; the previously used full statement remains the scoring reference. This is a representation compatibility adapter, not a new Fact approval or scoring gate. Existing exclusions, reviewer/source-hash rules, A/B/C/D/E authority, weights and fatal policy remain in force.

## Contract

- An opted-in Anchor carries `sentence_compatibility.version=fact_anchor_sentence_compat_v1`, a SHA-256 of the previous statement, and the previous statement in both `expected` and the unchanged first `accepted_explanations` entry. The shorter statement must be its exact initial complete sentence; existing `claim` and `description` aliases, if present, match the short source sentence.
- `grading/evidence/fact_anchor_compatibility.py` creates a scoring-only view of a valid explicit marker. It restores the historical statement for lexical evidence, question scope, cross-topic reference, question-demand evidence, D/E canonical-axis extraction and phase-3 selection. Hybrid/multi-topic scoring context also restores mirrored `core_facts`. The source sentence view remains short and score-neutral.
- The existing generated builder already uses `expected` as its first choice; retaining the previous `expected` preserves the prior generated Topic triggers and aliases. No generated bank is edited manually.
- A marker's hash establishes text consistency, **not** reviewer identity, source verification, eligibility or automatic `SUPPORTED` promotion. An unmarked Anchor retains its prior behavior. The runtime ignores malformed markers rather than suppressing an axis or granting credit; the existing Topic Pack validator rejects malformed opt-in metadata before promotion. Held/excluded Facts are not released.

## Initial reviewed Anchor and limitations

`humidity_measurement_capacitive_resistive_dew_point_selection_compensation / relative_humidity_definition`: reviewer `gpt-6-luna`, AI method, original and exact short sentence with source locators in `pr38_humidity_token_neutral_review_20261116.md`. Its accepted explanations and scoring reference are unchanged. The separate temperature-dependence Anchor remains. All other 47 candidates remain unapplied; the encoder frequency precision correction is separate.

Focused tests compare legacy vs opt-in axis IDs/text, lexical evidence/status/spans, derived question scope, cross-topic reference, question-demand assets, generated triggers/aliases, phase-3 selection and hybrid/multi-topic source projection. They also test that independent axes stay separate, invalid metadata does not suppress them, and no opt-in changes unmarked Anchors. These examples do not prove every possible input or external LLM result identical. Full offline pytest, Topic integration, generated freshness and release results must be recorded from actual runs; no deployment is implied.
