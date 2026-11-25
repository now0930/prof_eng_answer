# PR #46 / #47 통합 정합성 및 검증 계획

## 현재 원격 관계

검토 시점의 원격 상태:

| 항목 | 값 |
|---|---|
| main | `119b6de0a4955c75ba00f2bb07ba7e40c0a5685e` |
| PR #46 head | `304833ac07bf666b375d689ae3b9bd2ac094808d` |
| PR #47 head | `243562b351fc567bf3cd687b3da65d454c699557` |
| PR #46 | OPEN, Draft, base `main` |
| PR #47 | OPEN, Draft, base PR #46 branch `fix/priority-11-anchor-corrections-20261125` |

PR #47은 PR #46의 작업 브랜치에 의존한다. 두 PR은 독립 병합 후보가 아니며, 승인 후에는 선행 #46의 검토·병합 절차를 먼저 마친 다음 #47의 base와 최종 diff를 재확인해야 한다. 이번 문서 작성에서는 두 PR, main, 승인 원장 및 운영 데이터를 변경하지 않는다.

## 변경 파일 중복과 정합성 위험

`main..PR #46` 변경 33개와 `PR #46..PR #47` 변경 28개의 경로를 비교했을 때 15개 경로가 중복된다.

- Generated 6개: `fact_anchors`, `logic_check_profiles`, `logic_checks`, `model_answers`, `topic_importance`, `topic_pack_manifest`
- PR #47에서 후속 변경된 두 Topic의 원본: PST partial-stroke Topic의 Topic Sheet, `fact_anchor.json`, `logic_check.json`; humidity Topic `fact_anchor.json`
- PR #46에서 이미 수정한 두 Topic의 후속 원본: encoder Topic `fact_anchor.json`; thermocouple Topic의 `fact_anchor.json`, `logic_check.json`, `model_answer.json`

따라서 단순 파일 복사나 개별 Generated 파일 병합은 금지한다. 두 PR의 원본 정본이 승인될 때만 의존 브랜치의 최종 트리에서 공식 Builder를 한 번 실행하고, 모든 Generated 파일을 fresh rebuild와 비교한다. 검증은 최종 통합 후보의 정확한 SHA에서 다시 수행한다.

## 승인 후 적용 순서

1. 사용자는 17개 Registry 제안과 참고/삭제 후보를 항목별로 승인·수정·거절한다. 이 문서는 승인이 아니다.
2. PR #46의 승인된 변경만 공식 workflow와 검증 도구로 처리한다. 기존 review/promotion ledger 및 source hash는 수동 편집하지 않는다.
3. PR #46의 Draft/필수 CI/정본 및 Generated 검증이 완료된 뒤 기존 의존관계를 유지하여 #46을 선행 처리한다.
4. PR #47을 최신 #46 결과 위에서 재비교한다. squash 또는 base 변경으로 커밋 ancestry가 달라졌다면 force push 없이 정상 rebase/새 커밋으로 재정렬하고 모든 충돌을 검토한다.
5. #47에서 승인된 후속 원본만 공식 승인 절차로 반영하고 Generated 6개를 다시 생성한다.
6. 최종 통합 후보 SHA에서 집중시험, registry/eligibility 검증, Generated freshness, `validate-all`, 전체 오프라인 pytest, 비승격 `validate_release.sh`, Release Candidate 검증을 수행한다.
7. 동일 최종 SHA에 대한 수동 GitHub Actions 결과를 확인한다. 이전 SHA의 PASS는 재사용하지 않는다.
8. 모든 필수 조건이 충족된 뒤에도 별도 병합 승인이 없으면 Draft 및 미병합 상태를 유지한다. 운영 배포는 이번 범위 밖이다.

## 실제 실행 근거

기존 PR #47 HEAD `243562b351fc567bf3cd687b3da65d454c699557`에서 이미 보고된 검증은 해당 과거 SHA에 한정된다: focused 445 passed, Topic 전용 57 passed, 전체 pytest 1,694 passed/0 failed/2 skipped, Generated 6/6 fresh, `validate-all` ALL VALID, Actions [run 45542801906](https://github.com/now0930/prof_eng_answer/actions/runs/45542801906) 성공.

이 통합 문서 묶음의 첫 커밋 `81e8bb51230f323d6fbc0dadd831a4131b544805`에서는 다음을 새로 실행했다.

- 집중 회귀: 436 passed.
- `python3 -B scripts/release_candidate.py validate`: exit 0; 전체 pytest 1,694 passed, 0 failed, 2 skipped; `VALIDATION=PASS`; manifest `reports/release_candidates/20261125T044758Z_81e8bb51230f_pytest/manifest.json`.
- `python3 -B scripts/check_generated_rubrics_freshness.py`: 6 files fresh.
- `python3 -B scripts/rubric_manager.py validate-all`: `ALL VALID`.
- `PROMOTE_GENERATED=0 bash scripts/validate_release.sh`: exit 0; release test coverage 154/154, missing 0. 스크립트 내부 fail-closed 회귀 fixture는 의도적으로 `PASS_WITH_QUARANTINE` 및 bad-answer sentinel을 출력해 그 시뮬레이션을 검사하며, 이는 실제 Release Candidate `VALIDATION=PASS`와 별개다.
- 143개 보호된 기존 답안 재생: 비공개 fixture 사용, 143행; 기준 결과와 byte-for-byte 동일, 결과 SHA-256 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`.
- Registry 파일은 1,524행이며, 모든 행의 현재 상태는 `review_status=approved`, `verification_status=verified`, `score_effect=none`; 해당 필드 및 Registry 파일은 수정하지 않았다. 위의 기존 승인 상태는 신규 17개 문안을 승인하지 않는다.

이 보고서 뒤에 문서만 추가해 새 커밋을 만들면 새 SHA에서 Release Candidate와 수동 Actions를 다시 실행해야 한다. 과거 SHA의 결과를 새 SHA의 CI PASS로 간주하지 않는다.

## 불변 조건

- 457개 검토 이력과 기존 143개 답안 입력을 보존한다.
- 119 HOLD, D4, scoring exclusion overlay 및 A~E 채점 권한을 유지한다.
- 승인 전에는 Registry, Promotion Ledger, 승인 hash, Topic Pack 정본, Generated를 이 보고서 작업으로 변경하지 않는다.
- 채점 영향 보류 2건은 계속 보류하고, 참고용 5건/삭제 후보 2건은 실제로 이동·삭제하지 않는다.
- Registry 승인과 독립 전문가 정확도 검증을 서로 대체하지 않는다.
- PR #46/#47 모두 Draft, 미병합 상태이며 main/production은 변경하지 않는다.
