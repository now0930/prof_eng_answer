# Fact Anchor 단문화 48건 및 Canonical Claim 계약 — #40 후속 실행 기준

> **P2-B3–B5 후속 체크포인트 (2026-11-25):** [기술 검토](../reports/p2b_technical_review_20261125.md), [완료 게이트](../reports/p2b_completion_gate_20261125.md), [회귀/해시 manifest](../reports/p2b_final_regression_20261125.json). commit `de248511b75176df63d6beb94eebda8112bc04eb` (tree `c640ab1cb35adfd2ee4ca25396e61f0c3b466ce1`), [Actions 45627560177](https://github.com/now0930/prof_eng_answer/actions/runs/45627560177) 성공, 동일 SHA, 1,708 passed/2 skipped, `VALIDATION=PASS`. 기존 111 원본 재생 95/111(기존 B3 역사 기준 83/111), 기술검토 반영 별도 fixture 97/111, 실행 오류 0. 새 개발자 provisional probe 17/36; 관계/모순 기대 19건 보류. RRF 조건 생략과 Claim 조건 근거 불일치는 구분했고 mixed 6건은 기존 contradiction/WRONG 정책 차이로 보존. 143 보호 replay snapshot은 byte-identical 0 변경이나 snapshot에 실행 코드 SHA 메타데이터가 없어 SHA 귀속 제한을 보고서에 명시. 전체 pytest 1,708/2 skipped; validate-all `ALL VALID`; Generated freshness 6/6; Topic Pack Release PASS(89 packs/2,096 anchors, optional smoke SKIPPED); 비승격 `validate_release.sh` exit 0. P2-B는 `PARTIAL_OR_UNRESOLVED`; 자연어 보류와 독립 검토 부재로 정확도 `NOT_ESTABLISHED`, P2-C 진입 차단. `score_admission=DISABLED`, `score_effect=none`; 정본, Registry, 채점 정책과 119 HOLD/D4 불변. PR #49 Draft 유지.

> **P2-B 부분 완료 체크포인트 (2026-11-25, 실제 Python 재생):** [최종 보고서](../reports/p2b_claim_fact_relation_final_20261125.md), [111건 실행 결과](../reports/p2b_relation_results_20261125.json), [건별 불일치 분석](../reports/p2b_relation_mismatch_analysis_20261125.json), [회귀 기록](../reports/p2b_relation_regression_results_20261125.json). 최종 코드/시험 SHA `5718f21239e97435359fabe006a177b560695ff1`. 기준 대비 구조화 64건 50→56 일치, 자연어 47건 26→27 일치, 총 76→83/111; 실행 오류 0. explicit foreign owner 누출 및 unresolved span에서의 오인정 위험을 최소 수정으로 막음. 남은 RRF 2건은 Machine Fact에 동일 시나리오·시간 기준 조건이 없어 SUPPORT 후보 위험으로 HOLD; 자연어 20건은 미인식/불확실 보류; 혼합 Claim의 기존 WRONG 우선 정책은 변경하지 않음. 143개 보호 답안 replay는 0건 변경. 집중 pytest 17 passed, validate-all 및 Generated freshness 통과, Topic Pack Release Gate PASS(선택 smoke SKIPPED), Release Candidate 1,698 passed/2 skipped, VALIDATION=PASS. 독립 전문가 정답 라벨은 없고 정확도는 NOT_ESTABLISHED. P2-B는 PARTIAL_OR_UNRESOLVED이며 P2-C 진입 보류. score_admission=DISABLED, score_effect=none, 기존 정본/Registry/운영 권한 불변. Draft 유지.

> **P2-A 완료 체크포인트 (2026-11-25):** [Canonical Claim 계약 맵](../reports/p2a_canonical_claim_contract_map_20261125.md). 현행 evidence schema, Fact/Registry, Topic Machine Contract, ontology, question scope, evaluator 및 비채점 audit 구현을 직접 대조. 4개 대표 연결 사례(Flow 2, FSRM owner 충돌, feedback machine contract 없음), 4계층 exclusion 539 고유 키 확인. Registry relation에 polarity 없음, ID namespace 분리, 조건 귀속·부정/인용/정정·상충·span·수식/차원 및 불확실 경계 확정. 신규 schema/ontology/채점 권한 변경 0. P2-B는 기존 explicit owner/Anchor/Fact/rule join과 구조화 비교·자연어 추출을 분리 검증. 전체 Machine inventory 재집계 및 runtime/pytest/Actions NOT_RUN. 8개 P1-C 후보 미적용. Draft 유지.

> **P1-C 완료 체크포인트 (2026-11-25):** [최소 변경 검토](../reports/p1c_minimal_anchor_change_review_20261125.md) · [8개 후보 JSON](../reports/p1c_minimal_anchor_change_candidates_20261125.json). 48개 처분 확정: P1-B 40개 pool 중 8개만 변경 준비, 32개 실익 부족 유지, 이전 REJECT 6/HOLD 2 유지. 4 Topic, 기존 Registry 관계·문항 scope·채점 권한 불변, 정확 문장 복제 위치 및 수기 대조 답안 기대 기록. 후보는 소유자 승인 대기/미적용; 신규 승인 0, score_effect=none. 외부 원문 재열람 및 회귀시험·Actions NOT_RUN. 다음 P2-A 비채점 계약 맵; P1-C 적용은 별도 승인·검증. Draft 유지.

> **P1-B 완료 체크포인트 (2026-11-25):** [48건 개별 기술 동등성 검토](../reports/p1b_fact_anchor_simplification_review_20261125.md). 최신 main 고정 기준에서 48/48 canonical–manifest–Registry–P1-A join, 7 Topic, 예상문제 직접 연결 46/48. APPROVE 20 / REVISE 20 / HOLD 2 / REJECT 6 (권고이며 승인·적용 아님). 최신 정본 수정 5개 모두 REJECT하여 보존, 기존 제외 2개 모두 HOLD. 다음 P1-C는 최대 40개 후보에서 변경 실익·조건 보존 및 채점 계약을 별도 검토하고 최소 변경만 준비한다. 원출처 신규 독립 재검증, Python grader/pytest/validate-all 및 신규 SHA Actions NOT_RUN. 기존 P1-A 제외 조인 재사용, 119 HOLD/D4/Registry/채점 권한 불변. PR #49 Draft 유지.

> **P1-A 완료 체크포인트 (2026-11-25):** [최신 inventory 감사 보고서](../reports/p1a_fact_anchor_inventory_20261125.md). main `45c7d146e4673e885005c04535e65dc9b9d7c8a5`의 89개 정본 파일 2,096 Anchor 및 12개 관리형 상태 파일을 직접 대조했다. Generated ID/statement 차이 0, 역사적 457/457 및 후보 48/48 존재, 48개 전부 457에 포함. Registry 1,524행, 정확 연결 정본 1,522개, 4계층 제외 합집합 539개. 후보 48개는 전부 Registry 연결·legacy 소속이며 제외 2, 미등재 46. 후보 기술 동등성 판정/신규 승인/적용은 0, P1-B가 다음 작업이다. [원격 브랜치 정리 완료](https://github.com/now0930/prof_eng_answer/issues/40#issuecomment-7158469781)로 7개 삭제, 5개 유지. 아래 §6은 삭제 직전의 역사적 기록이다. PR #49 Draft / 새 SHA 전체 pytest 및 Actions NOT_RUN / 운영 미배포.

2026-11-25. Owner: [Issue #40](https://github.com/now0930/prof_eng_answer/issues/40). 현재 작업은 **계획/읽기 전용 기준 확인**이며, 단문화 승인이나 score admission이 아니다.

## 1. 완료된 범위와 새 기준선

- main: `45c7d146e4673e885005c04535e65dc9b9d7c8a5`, tree `d06a43d7b36323b587e52086c495f12dcc8e9442`.
- [PR #46](https://github.com/now0930/prof_eng_answer/pull/46), [PR #47](https://github.com/now0930/prof_eng_answer/pull/47) 병합 완료. [#42](https://github.com/now0930/prof_eng_answer/issues/42) CLOSED. 역사적 457건의 기술 검토 및 처리 방향 확정 완료: 유지 418, 정본 수정 30, 채점 영향 보류 2, 참고/삭제 후보 보존 7. Registry 17개 기존 행 revision 2 반영.
- [Actions 45582704118](https://github.com/now0930/prof_eng_answer/actions/runs/45582704118): 동일 main SHA, 1,694 passed / 2 skipped, VALIDATION=PASS. 기존 143답안 byte-identical, Generated 6/6 및 Registry 검증 통과는 종결 보고 기록에 따른다. 운영 배포 NOT_RUN. 이 검증을 이후 변경 SHA에 재사용하지 않는다.
- 457건의 기술 검토를 다시 시작하거나 이미 승인된 기술 내용을 문장 길이만으로 원복하지 않는다. 2,096개 Anchor는 앞선 감사 및 Release의 보고 분모이며, P1-A에서 최신 checkout으로 재집계한다.
- [승인 적용 기록](../reports/fact_anchor_approval_application_20261125.md), [우선 11건 종결](../reports/pr46_fact_anchor_closeout_and_followups.md), [후속 29건](../reports/fact_anchor_followup_29_technical_review.md), [관계 인식 재평가](../reports/pr46_relation_recognition_reassessment.md), [점수 영향 보고](../reports/fact_anchor_scoring_drift_2_23_analysis.md) 및 [초기 감사 스냅샷](../reports/claim_fact_inventory_p1_p2_20261123.md)을 이력으로 보존한다.

## 2. 48개 후보 입력 고정 및 최신 정본 대조

후보 원본은 **main에 존재하지 않는다.** 종료된 D4 브랜치의 불변 SHA `5a49a7daf042fc4749b9ae137c9af054ff68afae`에서 [calibration/fact_anchor_simplification_review_20261114.json](https://github.com/now0930/prof_eng_answer/blob/5a49a7daf042fc4749b9ae137c9af054ff68afae/calibration/fact_anchor_simplification_review_20261114.json)을 읽었다. Git blob SHA `38e90d7300ed8b2c5eda2d995a005bd3c785ea15`, manifest baseline `09e4b1c7347c330b6196be695a4c0ac3a091531d`, 48 unique (topic_id, anchor_id), 7 Topic, PENDING_TECHNICAL_REVIEW / CANDIDATE_ONLY_NOT_APPLIED / applied_anchor_count=0 / score_effect=none. 이 파일을 얻기 위해 D4 branch 전체를 main에 병합하거나 D4 연구를 재개하지 않는다. 필요한 경우 해당 후보 파일만 검토 입력으로 추출하고 원본 hash를 보존한다.

GitHub API로 위 manifest 48행과 최신 main의 해당 7개 정본 파일을 읽어 exact ID 및 statement를 비교했다. 과거 #40의 29/18/1 분류는 역사적 기준선이다. 이번 단순 문자열 대조는 다음과 같다.

| Topic | 후보 | previous_statement 일치 | 양쪽 문장과 다름 | simplified_statement 일치 |
|---|---:|---:|---:|---:|
| Functional safety reliability modeling | 3 | 3 | 0 | 0 |
| Software project engineering / FAT SAT | 2 | 2 | 0 | 0 |
| Humidity measurement | 12 | 11 | 1 | 0 |
| Feedback / sensitivity / steady state error | 5 | 5 | 0 | 0 |
| Pressure measurement | 7 | 7 | 0 | 0 |
| Speed / rotation / encoder | 11 | 8 | 3 | 0 |
| Thermocouple | 8 | 7 | 1 | 0 |
| **Total** | **48** | **43** | **5** | **0** |

ID 미대응 0. 다른 5건: `absolute_humidity_definition`, `counting_window_speed_equation`, `encoder_frequency_limit_selection`, `gear_tooth_speed_equation`, `thermocouple_measures_temperature_difference`. 이미 승인된 최신 정본의 기술적 보완과 후보의 차이를 우선 검토한다. 문자열 일치 여부만으로 승인, 오류, 또는 기술적 동등성을 판정하지 않는다. 이 회차의 48개 기술 동등성 판정은 NOT_RUN, 적용 0, 신규 승인 0.

## 3. P1 — 단문화 후보 감사

| 단계 | 작업 / 산출물 | 완료 조건 |
|---|---|---|
| P1-A | 최신 main의 정본 inventory, owner/ID, managed/legacy, Registry 및 제외 상태, 기존 457 이력과 48 후보의 교집합 | 재현 가능한 정확한 SHA, 중복/누락 확인. 휴리스틱은 오류 판정이 아님 |
| P1-B | 48행마다 최신 statement/previous/simplified, 필수 조건·수식·단위·예외·출처 locator, 요구 문항, 기존 승인과 점수 영향 대조 | APPROVE / REVISE / HOLD / REJECT (권고) 및 이유 48/48; 의미가 같고 변경 실익이 없으면 현 정본 유지 권고 |
| P1-C | 승인된 최소 표현 개선만 별도 후보로 준비 | 1 독립 검증 가능 명제를 지향하되 조건·예외를 잃거나 불필요하게 ID를 분리하지 않음. 실제 적용은 별도 승인 및 해당 workflow/회귀 후 |

5개 최신 변경 행의 경우 과거 simplified 문장을 그대로 복구하지 않는다. P1-A/B는 읽기 전용으로 진행한다. 문장 길이, 동의어 개수, 텍스트 유사도만으로 채점 사실을 변경하지 않는다. WIP 최대 3, 검토 배치 최대 20. 기존 119 HOLD와 D4, 제외 Overlay, Registry 승인/해시, 배점/합격 기준을 보존한다.

## 4. P2 — 기존 Canonical Claim 계약 확정 (비채점)

재사용할 코드 및 데이터:
- `grading/evidence/canonical_claim_extractor.py`: provider-neutral evidence 추출만 담당.
- `grading/evidence/topic_machine_contract.py`: 기존 optional additive contract의 schema/owner/authority/score_effect 검증.
- `grading_ontology/canonical_predicates.json`, `relations.json`, engineering concepts/quantities/dimensions: 기존 식별자 우선.
- `grading/scoring/deterministic_requirement_evaluator.py`, `grading/evidence/fact_anchor_evidence_adapter.py`, 질문별 `required_anchor_ids`: 기존 관계 평가와 범위 선택.
- `scripts/audit_relation_recognition.py`: 운영 채점과 분리된 진단.

| 단계 | 계약 및 검증 |
|---|---|
| P2-A | 기존 subject/predicate/object/conditions/polarity, source span, Topic/Fact owner, provenance 및 질문 scope와의 매핑을 코드/스키마 기준으로 문서화. 수식/단위, 조건 귀속, 부정/인용/정정, 상충/불확실의 경계를 정의. 기존 schema 재사용, 새 schema/ontology 일괄 신설 금지. |
| P2-B | 기존 승인 및 scoring-eligible Fact의 명시적 관계를 합성 정답/오답/조건부/인용/키워드 나열과 대조. Fact/Anchor ID의 별도 namespace를 존중하고 명시적 근거 없이 동일 ID 연결을 가정하지 않음. |
| P2-C | 비채점 비교·진단에서 UNKNOWN/ABSTAIN 및 관계 인식 불확실을 보존. 신규 Claim 경로 score_admission=DISABLED, score_effect=none. 관계 비교의 정확도와 자연어 추출의 정확도를 별도 보고. 운영 권한, 배점, fatal, ceiling, D4 불변. |

앞선 #46 진단: 2,096개 중 직접 연결+제외 통과 45개, 구조화된 정상/반대 6/6씩 비교 가능, 자연어 동등표현 0/6 확인. 이는 당시 진단 범위이지 현재 전체 정확도나 자동 확대 근거가 아니다. 기술 관계 미인정 17건과 문항 기대 범위 3건을 별도 추적. #33은 추출, #34는 문제 요구 정렬, #35는 기술 판정/grounded_attempt, #48은 최종제어요소 문안 2건과 B점수 23건의 보류를 소유한다. #40에서 개별 정규식/키워드 추가 반복, 범용 채점기 리팩터, 전체 Machine Contract 일괄 승격을 하지 않는다.

## 5. 검증 및 종결 조건

- 48개 후보별 근거와 판정, 실제 적용/승인 상태를 구분하고 P2 계약 맵 및 비채점 검증을 기록한다. 추가 전수 사실 재검토는 하지 않는다.
- 변경이 필요한 경우 격리 branch/Draft PR, 공식 builder 및 관리형 source approval 절차. 후보 SHA에서 해당 집중시험, validate-all, Generated freshness, 전체 offline Release Candidate, 143 보호 답안 회귀 및 동일 SHA Actions를 기록한다. 실제 실행하지 않은 시험은 NOT_RUN. 문서만 바뀐 경우 문서 링크/차이 검사와 코드 검증을 구분한다.
- Issue #40은 OPEN 유지. 승인 또는 운영 반영과 감사 종결은 별도. main 병합/배포는 별도 승인. Firecrawl 사용 금지.

## 6. 브랜치 정리 기준 (2026-11-25 읽기 전용)

main 기준 GitHub compare에서 ahead_by=0인 7개, open PR의 head/base가 아님을 확인했다. 삭제 전 현재 원격 SHA와 open PR 의존성을 재검증한다. 현재 연결에는 branch ref 삭제 기능이 없어 아직 삭제하지 않았다.

| 정리 후보 | 확인된 원격 HEAD | main ahead |
|---|---|---:|
| audit/claim-fact-inventory-20261123 | 759cb61685fc12eff6895fa06412e2ccd82d4b93 | 0 |
| audit/wip-abc-integration-20261124 | 119b6de0a4955c75ba00f2bb07ba7e40c0a5685e | 0 |
| fix/emc-claim-dependency-scope-20261124 | 574667bdaddc302c33fb1add9876553159a5cce1 | 0 |
| fix/encoder-frequency-credit-20261124 | 6729ee47ff6ae633275f7f9b3835d5c984def0c0 | 0 |
| fix/fact-anchor-technical-followups-20261125 | d39ca8f4db7d7aa644deb47ca730707a677c61eb | 0 |
| fix/moc-impact-checklist-20261124 | aeba94dbb0d90b8ccfa9021bcce49a2651c0c7c6 | 0 |
| fix/priority-11-anchor-corrections-20261125 | 304833ac07bf666b375d689ae3b9bd2ac094808d | 0 |

보존: main; `audit/fact-atomicity-review-19-20261124` (open Draft #45, ahead 2); `codex/data-reports-inventory-20261113` (ahead 38); `feat/claim-alignment-verification-20261114` (ahead 305, closed/unmerged #38의 역사 및 48건 후보 원본). 고유 커밋의 중복/보존 여부를 별도 확인하지 않고 삭제하지 않는다. 이 문서의 작업 branch도 OPEN 작업 동안 유지한다.
