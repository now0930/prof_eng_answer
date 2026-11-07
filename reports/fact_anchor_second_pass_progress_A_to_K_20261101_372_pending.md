# Fact Anchor independent original-source audit — 372 PENDING, 2026-11-01

Original Queue = **1,290 exact distinct Fact IDs**; at start of this review turn 477 still lacked claim-by-claim primary-source disposition. **105 newly compared** with original publisher documents, university theory, physics and official engineering resources. Current PENDING **372**, total audit dispositions **918**. **A non-PENDING disposition is not automatically a certified universal scoring reference.**

## De-duplicated A–K first-source ownership

| First appearance Batch | Distinct IDs | Audited disposition | Independently PENDING |
|---|---:|---:|---:|
| A | 20 | 13 | 7 |
| B | 56 | 46 | 10 |
| C | 41 | 21 | 20 |
| D | 82 | 60 | 22 |
| E | 81 | 70 | 11 |
| F | 123 | 54 | 69 |
| G | 92 | 67 | 25 |
| H | 116 | 116 | 0 |
| I | 130 | 79 | 51 |
| J | 294 | 241 | 53 |
| K | 255 | 151 | 104 |
| **TOTAL** | **1,290** | **918** | **372** |

## All verdict totals (exact current CSV)

- `PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW`: **372**
- `EXCLUDE_FROM_GENERAL_SCORING_ONLY`: **275**
- `KEEP_BOUNDED`: **556**
- `REVISE_REQUIRED`: **46**
- `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE`: **29**
- `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD`: **4**
- `KEEP_AS_SCOPED_ONLY_NOT_GENERAL_SCORING`: **1**
- `SOURCE_CHECKED_SCOPED_STANDARD_HOLD`: **7**

Separate executable source-hold manifest contains **412** exact (topic,anchor,fact) pairs: 372 never independently reviewed, 29 insufficient primary-source scope, 7 source-confirmed specific standards/Annex, 4 vendor/model specific applications. Existing screening exclusion overlay **276** and independent revision overlay **46** distinct, not summable as certified claims.

## New original claim comparisons in this turn (105)

- 유량계 원리: **10** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_flow_20261101_v2.md)
- 공정제어 구조: **10** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_architecture_20261101_v2.md)
- PID: **6** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_pid_20261101_v2.md)
- 진상·지상 보상기: **9** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_lead_lag_20261101_v2.md)
- 광학·iToF·삼각측량: **15** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_optical_20261101_v2.md)
- 압전센서: **8** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_piezo_20261101_v2.md)
- LVDT/RVDT: **7** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_lvdt_20261101_v2.md)
- 레이더·GWR 레벨: **13** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_radar_20261101_v2.md)
- 상태피드백 추종·관측기: **7** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_state_tracking_20261101_v2.md)
- 제어밸브 본체·액추에이터: **11** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_control_valve_types_20261101_v2.md)
- 회전속도·엔코더·타코미터: **9** exact Fact IDs — [evidence matrix](fact_anchor_independent_review_speed_rotation_20261101_v2.md)

Reviewer scope: every verdict based on exact original Topic Pack statement compared with author/publisher text, model assumptions and field applicability. Qualified physical facts can be KEEP_BOUNDED; extended vendor-only examples, missing theorem hypotheses, arbitrary mandatory checklists, compound unsupported assumptions become source-scope holds or revision required. Some PDF original materials gave extracted text but screenshot attempts failed (including AMETEK Model 706); the individual report says so. Do not treat unviewable PDF image pages as visually checked.

## Release and code boundaries

The current branch is **NOT** a completed approved source/Registry/Topic Pack release. Original Pack definitions, Registry legacy status, generated answer/score views and A/B/C deterministic contracts were NOT changed in this evidence pass. The GitHub draft PR [#17](https://github.com/now0930/prof_eng_answer/pull/17) stays unmerged. Focused hold-overlay regression tests must match all 1,290 audit IDs and 412 source-hold keys; the full release currently has outstanding canonical-grading regressions and **must not be declared green or bypassed**. The remaining 372 PENDING need real individual original-source verification, and 46 source-revision cases need managed canonical corrections and release validation.