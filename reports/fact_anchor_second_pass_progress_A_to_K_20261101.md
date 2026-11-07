# Fact Anchor second pass — A–K progress and release boundaries (2026-11-01)

Audit state recorded on branch `codex/essay-boundary-calibration-20261028` after five source-review waves in Batch H this turn (11+6+4+4+3 = 28 exact Fact IDs). Reviewer GPT-6, AI original-publisher claim comparison; not human review or release approval.

## Whole current Queue

- 1,290 unique Fact IDs exactly, of which **590** remain `PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW` and **700** have a non-PENDING documented audit disposition.
- KEEP_BOUNDED 376, REVISE_REQUIRED 43, EXCLUDE_FROM_GENERAL_SCORING_ONLY 275, HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE 5, KEEP_AS_SCOPED_ONLY_NOT_GENERAL_SCORING 1.
- **Non-PENDING does NOT mean verified for universal general scoring, nor released to runtime**: excluded items may be only scoped/non-core; 43 require source repair; holds remain uncertain. Existing exclusion overlay 276 and independent revision-hold overlay 43 stay active.

## De-duplicated A–K ownership-by-first-occurrence

The first source report containing an ID owns its row in this counting table; repeated later reviews are excluded only from statistics, never discarded from evidence. This avoids double-counting IDs (Batch H source document itself has 125 IDs, including 9 already in prior batches).

| First appearance | Unique Queue IDs | Documented audit disposition | Independent source comparison still pending |
|---|---:|---:|---:|
| A | 20 | 13 | 7 |
| B | 56 | 30 | 26 |
| C | 41 | 21 | 20 |
| D | 82 | 60 | 22 |
| E | 81 | 50 | 31 |
| F | 123 | 54 | 69 |
| G | 92 | 67 | 25 |
| H | 116 | 94 | 22 |
| I | 130 | 79 | 51 |
| J | 294 | 115 | 179 |
| K | 255 | 117 | 138 |
| **TOTAL** | **1290** | **700** | **590** |

## Batch H full-source membership (125, including repeated IDs)

- `EXCLUDE_FROM_GENERAL_SCORING_ONLY`: 48
- `KEEP_BOUNDED`: 47
- `PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW`: 27
- `REVISE_REQUIRED`: 3

Batch H still PENDING: 27. Actual final Batch H closure requires independent source checks or explicit unresolved hold for all relevant claims **and** managed source/score impact with real tests; it has not been declared complete.

## Reconciliation evidence this turn

- [H 01: 11 source comparisons](fact_anchor_second_pass_H_source_reconciliation_20261101.md)
- [H 02: 6 source comparisons](fact_anchor_second_pass_H_source_reconciliation_02_20261101.md)
- [H 03: 4 valve-trim comparisons](fact_anchor_second_pass_H_valve_trim_checks_03_20261101.md)
- [H 04: 4 packing/emission comparisons](fact_anchor_second_pass_H_packing_emissions_04_20261101.md)
- [H 05: 3 positioner/sizing/leakage comparisons](fact_anchor_second_pass_H_positioner_leakage_sizing_05_20261101.md)
- [Authoritative updated CSV](fact_anchor_independent_verification_audit_20261101.csv)

## Release gate and honesty

- **Source/Registry/Topic Pack changes:** none this turn. Newly source-reviewed `KEEP_BOUNDED` does not license unverified scoring references or unconditionally promote a changed fact.
- **Automated tests, managed generated build, approve-topic, source-hash validation, validate-all, full release gate:** not run; no test pass claim. This Chat GitHub connector can commit tracked texts but cannot execute the user's remote checkout and managed CLI; a repository clone attempt from this execution environment failed DNS resolution to github.com.
- Do not delete vendor examples simply because they are noncore; reference exclusion is distinct from physical falsehood. Do not silently change original Grading/Topic IDs, scoring authority, A/B/C, fatal caps, generated files or `main`.
- To finish the requested four-phase work, remaining 590 pending IDs require exact first-party statement/section verification; repair/revise/remove where source-grounded, run focused regressions and full release gate, and commit source changes only after gates. Explicitly mark paid-standard Annex clauses as HOLD unless original text is available.
