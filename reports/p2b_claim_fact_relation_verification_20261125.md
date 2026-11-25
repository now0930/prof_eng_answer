# P2-B — Claim–Fact 관계 검증: 정적 감사 및 실행 준비 (2026-11-25)

**부분 완료; 실제 Python 실행 대기.** Baseline main `45c7d146e4673e885005c04535e65dc9b9d7c8a5`, tree `d06a43d7b36323b587e52086c495f12dcc8e9442`. P2-A `ecad9992ccf45814b5d92a5a5421292b420793d7`. 신규 score_admission=DISABLED, score_effect=none. P1-C 8건 미적용.

## 1. 최신 main inventory 실측

89개 `logic_check.json`을 고정 main에서 6개 읽기 배치(15/15/15/15/15/14)로 모두 파싱하고 Git tree blob SHA와 일치 확인. 16 Topic에 machine_contract 존재, 73 없음. 113 machine facts, 72 positive requirement rules + 6 violation_only. 16개 Topic의 정본 fact_anchor/logic_check/model_answer, Registry 및 네 exclusion 파일을 대조하고 78개 (owner, requirement) 고유 행을 기록했다. Local Python loader/validator는 아직 실행하지 않았다.

| Inventory batch | 전체 규칙 | 긍정 규칙 | exact owner+anchor | 제외 통과 | 승인 verified Registry + explicit pattern 연결 |
|---|---:|---:|---:|---:|---:|
| [1](p2b_relation_inventory_20261125/batch_1.json) |16|16|12|12|9|
| [2](p2b_relation_inventory_20261125/batch_2.json) |21|21|19|17|14|
| [3](p2b_relation_inventory_20261125/batch_3.json) |17|11|7|2|2|
| [4](p2b_relation_inventory_20261125/batch_4.json) |6|6|5|5|2|
| [5](p2b_relation_inventory_20261125/batch_5.json) |16|16|11|9|9|
| [6](p2b_relation_inventory_20261125/batch_6.json) |2|2|0|0|0|
| Total |78|72|54|45|36|

18 positive rules have no exact owner Anchor, nine exact matches excluded, nine unexcluded lack explicit Registry link (3 flow, 3 software, 3 weir). Registry link requires approved + verified and explicit legacy_anchor_id, not same-string assumption; exclusion compares owner+Anchor and Registry fact_id. 36 are structural candidates, not full semantic equivalence or new scoring admission. Denominator 2,096 from P1-A inventory; 45/2,096=2.15%, 36/2,096=1.72%. The 89 logic files' count reverified; not another 2,096-fact technical audit.

## 2. Semantic review and selected cases

[36 individual decisions and 111 synthetic inputs](p2b_relation_cases_20261125.json): selected scoped subrelation 6, related subrelation not sampled 23, hold mapping 7. Selection is a deliberately bounded, nonrandom sample. Each selected requirement has existing explicit question pattern, exact Anchor owner, approved/verified Registry legacy link, no overlay exclusion, and a specific existing Machine Fact. Scope is a subrelation, not proof of every component of an Anchor or a minimum-match requirement. Registry has no polarity field; polarity comes from existing Machine Fact. No ontology or rule added.

| Selected requirement | Machine Fact | Scope |
|---|---|---|
| flow_volumetric_rate_area_integral | volumetric_flow_from_area_average_velocity | mean normal velocity and defined cross section |
| flow_mass_rate_density_relation | mass_flow_density_volume_relation | uniform density; separate integral and nonidentity fact |
| sw04_verification_definition | verification_checks_specification | defined work-product specification |
| ipgse_pe_signal_reference_boundary | emc_pe_distinct_reference | functional distinction, not mandatory electrical isolation |
| mcdc_one_hundred_percent_limit | mcdc_does_not_guarantee_total_sil | full MC/DC alone cannot assure overall SIL |
| hazop_lopa_required_rrf | required_rrf_uses_residual_tolerable_ratio | same scenario endpoint and time basis |

Hold mapping: flow_dp_primary_element_conditions (geometry examples or square-root alone do not cover conversion conditions); hazop_lopa_residual_frequency_after_existing_ipls (missing tolerable-frequency comparison); sw04_v_model_definition (Registry only directly supports development/test correspondence, not both min=2 facts); argument_principle_pnz_relation (sign/convention/formula missing); target_pfd_relation (ratio direction/inequality/low demand missing); required_rrf_relation (inverse target probability is conditional, not general residual/tolerable ratio); operations_moc_revalidation (scoped HSE COMAH maintenance evidence not full universal MOC/revalidation rule). Keep original authorities unchanged.

## 3. Executed independent structured reference checks (NOT repository Python)

64 cases across 6 selected subrelations: exact, explicit opposite, quoted, rejected, corrected, mixed, mention, other owner, unresolved scope, invalid span (60); plus missing/different condition for mass flow and RRF (4). Independent JS policy comparison executed using actual Machine Fact tuples and manually assigned evidence fields; exact span, explicit owner, scope, condition-binding flag, polarity, assertion-context and conflict guards. All 64 matched the prewritten reference expectations: 12 CONFIRMED_RELATION, 6 CONFIRMED_CONTRADICTION, 40 RECOGNITION_UNCERTAIN, 6 INVALID_EVIDENCE. This is a self-consistency check of the reference policy and fixture, not independent empirical accuracy, not a reimplementation of all production evaluation rules, not proof the existing evaluator enforces these guards. No score use. Reference source cases/results retained in JSON.

47 natural-language cases prepared: 21 technical positive subrelation, 6 explicit negative, 20 uncertain. Explicit/alternative wording, opposite, quote, correction, keyword list, mixed, formulas and condition omission where applicable. These are manually designed technical expectations; actual extractor/audit statuses NOT_RUN. In particular the existing strict audit may abstain for valid conditional or formula cases, and the production evaluator may not enforce owner and condition binding like this policy comparator. Do not call either result an empirical accuracy until executed.

## 4. Blocker and reproducible actual test

Work handoff declined; local container `git ls-remote https://github.com/now0930/prof_eng_answer.git HEAD` failed DNS resolution, no checkout. GitHub connector can read/write files but does not provide shell execution or a workflow dispatch action in the available tool set. Existing validation workflow is manual workflow_dispatch only, not triggered by commits. No Firecrawl, no workflow changes. Actual Python evaluator/validator/extractor/audit not executed. No pytest, full validate-all, 143 replay, source hold SHA recomputation or Actions run.

[Standalone diagnostic runner](run_p2b_relation_diagnostic_20261125.py) is prepared but NOT_RUN; not imported by production or pytest. In repository checkout at the P2-B Draft branch:

```bash
git fetch origin
git switch docs/issue40-canonical-claim-next-phase-20261125
git pull --ff-only
python3 -B reports/run_p2b_relation_diagnostic_20261125.py --output /tmp/p2b_relation_results_20261125.json
```

Runner verifies baseline, tracked non-document drift and exact source blob identities (including four overlay files and Registry), calls existing evidence builder/validator and deterministic evaluator on all structured cases, and separately extracts natural claims and invokes existing audit. Output reports actual tuples/spans/unresolved, requirement findings, raw audit reason, confusion counts and exceptions, without projecting scores. It does not override differences with policy assumptions or overwrite prior outputs. The runner itself has not been syntax/runtime tested in this environment; execution errors must be recorded and repaired before interpreting results. Output is a new file outside the repo by default in the example. Review output and commit only diagnostic results after checking scope and source hashes; actual grading changes are forbidden.

## 5. Remaining P2-B completion gate

Run and inspect all 64 structured actual and 47 natural actual cases; identify false confirmation/contradiction, abstention and extraction gap, scope mismatch, condition-binding and mixed evidence discrepancies. If actual runner errors, resolve only diagnostic harness and rerun. Record actual SHA and output hash, distinguish historical #46 results and independent reference test. Only after this may mark P2-B completed and begin P2-C; no automatic code repair, no score admission. 119 HOLD/D4/exclusions/Registry/Generated/ledger/A–E and 143 baseline unchanged. Issue #40 OPEN; PR #49 Draft. P2-B static phase complete, runtime phase pending.
