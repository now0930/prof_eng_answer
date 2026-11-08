# Fact Anchor second-pass primary-source audit — 477 pending (2026-11-01)

Unique first-appearance attribution across original Batch A–K, separate from raw report row counts. These are **evidence dispositions, not universal claim approvals or final release pass**.

| Batch | Distinct IDs | Non-PENDING dispositions | Original-source still pending |
|---|---:|---:|---:|
| A | 20 | 13 | 7 |
| B | 56 | 46 | 10 |
| C | 41 | 21 | 20 |
| D | 82 | 60 | 22 |
| E | 81 | 61 | 20 |
| F | 123 | 54 | 69 |
| G | 92 | 67 | 25 |
| H | 116 | 116 | 0 |
| I | 130 | 79 | 51 |
| J | 294 | 179 | 115 |
| K | 255 | 117 | 138 |
| **TOTAL** | **1,290** | **813** | **477** |

## Exact audit counts
- `PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW`: 477
- `EXCLUDE_FROM_GENERAL_SCORING_ONLY`: 275
- `KEEP_BOUNDED`: 469
- `REVISE_REQUIRED`: 44
- `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE`: 14
- `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD`: 3
- `KEEP_AS_SCOPED_ONLY_NOT_GENERAL_SCORING`: 1
- `SOURCE_CHECKED_SCOPED_STANDARD_HOLD`: 7

During this conversation, 37 formerly source-pending exact IDs were individually reviewed: 12 strain-gauge/bridge facts (10 bounded keep, 1 primary-source correction, 1 insufficient mandatory scope), 13 pressure/DP facts (12 bounded keep, 1 lifecycle-procurement hold), 12 humidity claims (8 bounded keeps, 3 vendor-scoped non-core original applications, 1 unsupported universal lifecycle scope). Starting independent source-pending 514 → 477.

## Evidence reports
- [Strain-gauge (12)](fact_anchor_independent_review_strain_gauge_20261101.md)
- [Pressure and DP (13)](fact_anchor_independent_review_pressure_20261101.md)
- [Humidity and dew/frost point (12)](fact_anchor_independent_review_humidity_20261101.md)

## Hold and release boundaries
Unresolved-source scoring manifest contains **501 distinct Fact/Anchor keys** = 477 still unreviewed + 14 source-insufficient + 7 IEC/standard-scoped + 3 vendor/application-scoped. **44** independently reviewed revision-required anchors remain in separate correction overlay; **276** original screening exclusions remain unchanged. Standard- and vendor-specific facts must not be treated as mandatory universal engineering certification.
Original source Topic Packs, Registry and approved-generated bank were not changed by these source-audit commits. Release verification for the wider branch is still blocked by previously observed canonical contract regressions. The draft [PR #17](https://github.com/now0930/prof_eng_answer/pull/17) must stay unmerged until source repairs and full Release Gate PASS. Only actual CI results may establish a passing gate.