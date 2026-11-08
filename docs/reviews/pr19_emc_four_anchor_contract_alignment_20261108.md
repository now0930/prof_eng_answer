# PR #19 — EMC positive Fact Anchor machine-contract alignment (review only)

## Purpose and authorization

This correction addresses four mismatches in `logic_check.json` where the required canonical fact tested a *different engineering assertion* from the named Fact Anchor. It does **not** promote any scoring exclusion, change any Golden range, or change the nine fatal/major invariant bindings.

The current positive-scoring holds remain in force for:

- `ipgse_scope_chain`
- `ipgse_emi_coupling_paths`
- `ipgse_power_quality_scope`
- `ipgse_final_verification`
- `ipgse_diagnostic_workflow`

## Before / after

| Held anchor | Previous unrelated fact | New fact relation(s) | Minimum required |
| --- | --- | --- | --- |
| `ipgse_scope_chain` | PE `distinct_from` signal reference | interference source `distinct_from` coupling path; coupling path `distinct_from` victim | 2 of 2 |
| `ipgse_emi_coupling_paths` | shield `depends_on` frequency/bonding | named coupling modes `diagnoses` source-path-victim | 1 of 1 |
| `ipgse_power_quality_scope` | UPS `does_not_guarantee` EMC immunity | power quality `measured_by` power events | 1 of 1 |
| `ipgse_final_verification` | shield `depends_on` frequency/bonding | corrective action `verifies` repeat conditions; corrective action `validates` before/after evidence | 2 of 2 |

The positive assertions remain narrower than the full prose of each anchor. A fact triple being detected is **evidence of that relationship only**, not certification that the entire anchor text was proved. In particular, the final-verification contract does not yet independently prove accuracy or resolution specification compliance.

The new `diagnoses` canonical predicate is additive, with narrow aliases (`진단`, `원인 분석`, `diagnose`). Other existing predicate definitions are unchanged.

## Controlled evidence cases

`tests/test_emc_four_anchor_contract_alignment.py` checks positive, off-topic, wrong, and explicit-negation contexts. It also asserts the five scoring holds remain enabled. The parser is a deterministic evidence extractor; it must not grant positive points to an unrelated PE, shield-termination, or UPS answer merely because it mentions the word `EMC`.

## Expected follow-up and release blocking

1. Execute the new test and the existing grading/EMC tests on the user's server.
2. Repeat `tmp/pr19_emc_real_answers_audit.py` and `tmp/pr19_emc_contract_diagnostics.py`. Inspect the real canonical matches and lexical fallback separately.
3. Keep the source model answer's 13–19 Golden unchanged; if its shadow score remains below 13, do not force the score by adding generic keywords or changing thresholds.
4. Before lifting any hold, verify individual anchors against their source and test positive/negative evidence independent of the held model answer.
5. `ipgse_diagnostic_workflow` is untouched and still held.

This is a **contract identity repair**, not an approval to score the held positive facts or a PR-READY decision.
