# D4-WRONG-22 delegated blind AI technical review

The owner delegated technical review to ChatGPT. A fresh-context reviewer was launched with the explicit `gpt-6.2-astra` model override and `high` reasoning; the reviewer could not independently self-query the runtime model. The review role was `DELEGATED_CHATGPT_TECHNICAL_EXPERT`, method `ai`, not human. The reviewer received only the blind packet and source materials, without prior candidate outcomes or the private mapping.

Before unblinding, an independent validation checked the 23 unique IDs, original answer and question hashes, exact evidence offsets and text, allowed judgments, declared AI role and requested model, timestamp, source metadata, rationales and mode 0600. The fixed private review SHA-256 is `944d4479f046da4857f163489f4a0c868283ac3b4a8d67fdc98b5d34b48d3bf5`. The reviewer's self-identification could not independently confirm the configured model. No private answer, source span or mapping is included here.

The delegated AI judgments were SUPPORT 13, CONTRADICT 5, UNRESOLVED 5; separately, conditions/scope were SATISFIED 7, OMITTED 11, MISMATCH 5, UNRESOLVED 0. Twelve relation reviews cite directly read Fisher or NBS official documents; eleven use independent derivation checks with no externally cited original source. Source/document provenance and a judgment are not an independent human validation of semantic correctness.

For the six existing directional candidates only, the delegated AI reference produced: existing SUPPORT → AI SUPPORT 3, CONTRADICT 0, UNRESOLVED 0; existing CONTRADICT → AI CONTRADICT 3, SUPPORT 0, UNRESOLVED 0. Under the predeclared conditional definitions, false SUPPORT is 0/3 (0%) and false CONTRADICT is 0/3 (0%). These are small, selected, AI-reference comparisons; they are not population accuracy, independently human-verified false-positive rates, or evidence for production admission.

The 17 previously scope-held relations, excluded from those denominators, received AI relation labels SUPPORT 10, CONTRADICT 2 and UNRESOLVED 5. Their paired scopes were SUPPORT/OMITTED 6, SUPPORT/SATISFIED 4, CONTRADICT/MISMATCH 2, UNRESOLVED/OMITTED 5. Semantic direction and scope are distinct dimensions.

The 23 relations belong to seven answers, represented without forcing mixed answers into a single label: one [UNRESOLVED], one [SUPPORT], one [CONTRADICT, CONTRADICT, CONTRADICT], two [SUPPORT, SUPPORT, SUPPORT, SUPPORT, UNRESOLVED], one [CONTRADICT, CONTRADICT, UNRESOLVED, UNRESOLVED], and one [SUPPORT, SUPPORT, SUPPORT, SUPPORT]. A potential common cause for three relations remains unconfirmed; no cause-deduplicated metric is calculated.

Registry, Topic Pack, Goldens, production scoring and approvals are unchanged. 119 HOLD, B7 OPEN, `score_admission=DISABLED`, `score_effect=none`, and PR Draft remain. The review is AI-delegated and not an independent human expert validation; external private storage remains outstanding.
