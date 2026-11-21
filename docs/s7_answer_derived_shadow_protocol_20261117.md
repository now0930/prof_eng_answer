# S7 answer-derived Claim shadow (research only)

This isolated module explores answer-visible surface cues for five Registry Facts. Stage A accepts only the answer string and emits surface text, polarity cue, evidence span and an explicit review-only status. It does not read Registry or Machine Contract data. Stage B receives that output separately; it currently returns `NOT_ESTABLISHED` for semantic identity because no independently reviewed alias mapping is available. Missing, quoted or negated evidence is never converted into credit.

The supported probes are deadband direction reversal, approved configuration baseline, effective unbalanced area, V-Model stage mapping, and Nyquist contour/mapping. This is a narrow lexical pilot, not a general natural-language parser. Conditions are not inferred or extracted; the output says `NOT_EXTRACTED`. Independent accuracy remains `NOT_ESTABLISHED`.

`score_admission=DISABLED` and `score_effect=none` are fixed. The module is not imported by the operational grading path. Author-draft challenges are development examples only and do not provide independent truth labels.

## 2026-11-17 correction

The first pilot treated a pair of topic words as a relation and carried a Fact-specific hint in Stage A. The correction removes that hint and records only subject, relation, object, and their exact answer spans for supported syntax. A deadband statement saying there is no output change remains a positive definition; a statement denying a link to input reversal is held. The initial Nyquist test failed because the pattern expected the object after the relation although the Korean sentence says “우반평면을 둘러싸고”. A second failure came from expecting one triple where the sentence describes both the s-plane contour and the L(s) mapping. They are now separate answer-derived surface Claims. The mapping is still a bounded phrase probe, not proof of the full Nyquist criterion or Registry semantic equivalence.
