# S7 answer-derived Claim shadow (research only)

This isolated module explores answer-visible surface cues for five Registry Facts. Stage A accepts only the answer string and emits surface text, polarity cue, evidence span and an explicit review-only status. It does not read Registry or Machine Contract data. Stage B receives that output separately; it currently returns `NOT_ESTABLISHED` for semantic identity because no independently reviewed alias mapping is available. Missing, quoted or negated evidence is never converted into credit.

The supported probes are deadband direction reversal, approved configuration baseline, effective unbalanced area, V-Model stage mapping, and Nyquist contour/mapping. This is a narrow lexical pilot, not a general natural-language parser. Conditions are not inferred or extracted; the output says `NOT_EXTRACTED`. Independent accuracy remains `NOT_ESTABLISHED`.

`score_admission=DISABLED` and `score_effect=none` are fixed. The module is not imported by the operational grading path. Author-draft challenges are development examples only and do not provide independent truth labels.
