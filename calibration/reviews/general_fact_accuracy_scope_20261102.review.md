# General-Fact authority calibration scope and two expert-label revisions

Review date: 2026-11-02. Reviewer: Codex ChatGPT (source-grounded AI
adjudication, delegated by the repository owner). This is an **AI review**,
not a human approval. The original labels remain in Git history and in
`calibration/reviews/expert_accuracy_stage50_54_priority_bundles.review.md`.

## Independent calibration versus diagnostic model references

The 15 `topic_pack_model_reference` cases were authored from the same Topic
Pack's high-score content. They are useful for diagnostic coverage and remain
in every replay row, fatal check and routing check. They are **not independent
expert answers** and are excluded as a class from the score-accuracy and
coverage denominators used to grant deterministic verdict authority. This is
an origin-based rule, not a list of failing case IDs. A future independent
expert re-adjudication can change the source classification with its own
evidence. The 12 user-reviewed question-type cases, 18 risk mutations and
three historical regression cases remain in independent calibration.

## Nyquist normal case

Question: explain the critical point and P/N/Z relationship. The submitted
answer correctly names `-1+j0` and mentions counting with a sign convention,
but does **not** write the signed P/N/Z equality or explicitly map the
Nyquist contour of `1+L`/`L` to the zero/pole counts. That limits its
completeness. MIT OCW lecture 17, page 8/15, gives the argument-principle
relationship and explicitly defines the poles/zeroes of `1+L` and stability
condition: <https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011/056c92694b953cb4645e4a4c20a363a8_MIT6_241JS11_lec17.pdf>.
The old 14–19 PASS range overcredits this short answer. Revised bounded
expert range: **11–14/25**, passing not guaranteed. No algorithm score was
used to derive the content judgment.

## Lead/Lag normal case

Question: explain the *design method* for lead and lag compensators. The
submitted answer correctly states lead improves phase margin/transient
behavior and lag improves low-frequency gain/steady-state error, and advises
rechecking crossover/stability margin. It omits specifications, compensator
zero/pole selection, frequency-response calculation, iteration and the
lead/lag interaction that constitute a design method. George Mason ECE 421
design steps explicitly cover those elements:
<https://people-ece.vse.gmu.edu/~gbeale/ece_421/comp_freq_lag_lead.pdf>,
“steps outline the procedure” section. Illinois ECE 486 lecture 17 also
separates the performance objectives and combined lead/lag design:
<https://courses.physics.illinois.edu/ece486/fa2026/documentation/handbook/lec17.html>.
The old 15–19 PASS range treated a concise role description as a complete
design answer. Revised bounded expert range: **11–14/25**, passing not
guaranteed. The technical role claims remain correct.

These two changes revise expert labels on question-specific completeness,
not to match the observed deterministic scores. Fatal expectations and
other Golden cases are untouched. New score ranges are intentionally broad;
passing and high-score verdict flags are updated consistently.

## Communication question-contract correction

The two new `sw07_qp_general_*` question patterns in the existing industrial
communication Pack use only pre-existing, scoring-eligible anchors. The
questions ask for a Fieldbus/Ethernet/wireless comparison and a wired/wireless
selection procedure; the prior derived scope selected HART multidrop or only
one generic communication requirement. This correction changes the required
answer scope, not the technical wording of an Anchor or its admission status.
The model-reference case remains diagnostic-only under the origin rule above.
Focused validation must confirm all referenced Anchor IDs, question routing,
source/generated equivalence and the full Release Gate before promotion.

## Operational-change expression recognition

The existing SW-06 high-answer question explicitly requests baseline and
impact analysis, Release/Backup/Rollback, regression and post-change control.
The derived scope instead chose `sw06_sw04_boundary` (not requested), and
English-only `core_terms` treated Korean descriptions of four universal
practices as partial. An exact question pattern now selects seven existing,
eligible Anchors; Korean core terms were added only for As-built reconciliation,
change-specific impact analysis, authorized Release artifact and risk-based
regression. This does not add or unblock any Fact. Before/after focused replay
of the same question yields LOW 4.5, PASS 18.5, HIGH 20.75/25; the low answer
is not promoted. Independent source basis already in those source Anchors is
NIST SP 800-82 Rev.3, NASA Software Engineering Handbook SWE-191 and ISO
10007:2017, with site-specific procedures and statutory scope kept bounded.
