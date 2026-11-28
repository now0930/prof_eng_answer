# P2-B Claim–Fact 관계 검증 결과

## 판정

**P2-B: `PARTIAL_OR_UNRESOLVED` — 완료 게이트 미통과. P2-C는 시작하지 않았다.**

Python에서 구조화 Claim 64건과 자연어 Claim 47건, 총 111건을 모두 실행했고 `EXECUTION_ERROR=0`이었다. 두 재현 결함은 제한적으로 수정했다. 그러나 RRF 적용조건이 Machine Fact에 구조화되어 있지 않아 구조화 입력 2건이 SUPPORT 관계로 통과하며, 자연어 관계 기대 20건은 `RECOGNITION_UNCERTAIN`에 머문다. 사례 라벨은 개발 준비 자료이며 독립 전문가가 검증한 정답이 아니므로 정확도·Precision·Recall은 `NOT_ESTABLISHED`다.

## 기준과 입력

- 기준 main: `45c7d146e4673e885005c04535e65dc9b9d7c8a5`
- 코드 및 집중시험 SHA: `5718f21239e97435359fabe006a177b560695ff1`
- 입력: `reports/p2b_relation_cases_20261125.json`
- 입력 SHA-256: `bf75899e302c5cb9736332fe230a914d0cd0d57d09c8d59e6328910267e60ee9`
- 결과: `reports/p2b_relation_results_20261125.json`
- 결과 SHA-256: `b9193c5a2e88d3219684e3c197101290b74bdcf9400be9e86dce94a6b9c9c52a`
- 건별 원인 및 처분: `reports/p2b_relation_mismatch_analysis_20261125.json` (111건)
- 회귀 및 Gate 증거: `reports/p2b_relation_regression_results_20261125.json`
- 실행: `python3 -B reports/run_p2b_relation_diagnostic_20261125.py --output reports/p2b_relation_results_20261125.json`

기준 Python 결과는 수정 전 SHA `50f16a15af5ed947130326d540b93baaa49cee51774bc0143ae4e674bd35e5d2`에서 실행해 보존했다. 결과 파일은 덮어쓰지 않고 별도 경로로 만들었다. 구조화/자연어 결과 및 confusion 표는 결과 JSON에 각각 제공한다.

## 실제 Python 결과 비교

| 집합 | 건수 | 수정 전 일치 | 수정 후 일치 | 수정 전 불일치 | 수정 후 불일치 | 수정 후 실행 오류 |
|---|---:|---:|---:|---:|---:|---:|
| 구조화 관계 | 64 | 50 | 56 | 14 | 8 | 0 |
| 자연어 관계 | 47 | 26 | 27 | 21 | 20 | 0 |
| 합계 | 111 | 76 | 83 | 35 | 28 | 0 |

관측 상태 분포:

| 집합/시점 | CONFIRMED_RELATION | CONFIRMED_CONTRADICTION | RECOGNITION_UNCERTAIN | INVALID_EVIDENCE |
|---|---:|---:|---:|---:|
| 구조화 전 | 20 | 12 | 26 | 6 |
| 구조화 후 | 14 | 12 | 32 | 6 |
| 자연어 전 | 6 | 2 | 39 | 0 |
| 자연어 후 | 5 | 2 | 40 | 0 |

이 일치율과 상태 분포는 개발 fixture와 기존 evaluator의 비교 결과다. 독립 의미 정확도를 나타내지 않는다. 구조화 6개 잘못된 span은 `INVALID_EVIDENCE`로 거부됐다.

## 수정한 결함

1. **Topic 소유권 누출:** 구조화 Claim에 명시된 `qualifiers.owner_topic_id`가 비교 계약의 Topic과 다르면 해당 Topic 계약에서 Claim을 제외하도록 했다. owner 정보가 없는 기존 Claim 형식의 동작은 보존했다. 대상 `other_owner` 6건에서 잘못된 Claim 연결이 제거됐다.
2. **미해결 span의 오인정 위험:** 자연어 추출에서 미해결 span이 관련 Fact에 걸쳐 있으면 그 Fact의 audit 확인을 막는다. 단, 후속 동일 Fact에 명시적 `corrected` 주장이 존재하면 그 정정 Claim을 평가한다.
3. **실행/테스트 방어:** 진단 runner는 지원된 연구용 소스 변경만 허용하고, 모든 사례를 순회해 `EXECUTION_ERROR`를 세며 하나라도 있으면 비정상 종료한다.

추가한 회귀 시험은 타 Topic의 명시 owner Claim 차단, unresolved contradictory span의 fail-closed 처리, 후속 정정 주장 우선, 독립 재현 사례를 확인한다. 최종 focused suite는 **17 passed**다.

## 남은 불일치 및 원인

- **혼합 주장 정책 차이:** 구조화 `mixed` 6건은 기존 결정론적 evaluator의 contradiction/`WRONG` 우선 동작을 유지한다. 별도 비채점 참조 정책의 기대는 상충 Claim 전체를 `RECOGNITION_UNCERTAIN`으로 보류하는 것이다. 이를 운영 정책 변경으로 해결하지 않았다. 건별 표에는 정책 차이 6개가 있으며 전체 원인 집계의 정책 차이 9에는 기타 참조 정책 경계도 포함된다.
- **RRF 조건 누락/귀속:** `hazop_lopa_required_rrf/condition_omitted`와 `condition_other` 2건은 선택된 Machine Fact에 동일 시나리오 및 시간 기준의 조건이 구조화되어 있지 않아 evaluator가 관계를 매칭했다. Machine Fact 및 정본을 승인 없이 수정하지 않았다. 이 두 건은 SUPPORT 위험으로 HOLD이며 P2-B 게이트 차단 사유다.
- **자연어 추출 한계:** 기대 관계 또는 모순 20건은 `RECOGNITION_UNCERTAIN`이다. 상세 분류는 mismatch JSON에 있다. 관계 동의 표현, 수식/단위, 조건 귀속 및 추출 범위 한계가 원인이다. 미지원 문장을 무리하게 인정하도록 패턴을 추가하지 않았다.
- **불일치 원인 집계 (28건):** `POLICY_DIFFERENCE=9`, `CONDITION_BINDING=7`, `MACHINE_CONTRACT=2`, `EXTRACTOR=15`. 한 사례에 복수 기여 원인이 있을 수 있으므로 합계는 사례 수와 같지 않다. 사례별 처분을 최종 JSON의 각 행에서 확인할 수 있다.
- **Fixture 상대 위험 수:** 구조화 false-support 후보 8→2, 자연어 1→0으로 줄었다. 자연어에서 기대 관계/모순이 보류된 수는 20으로 변하지 않았다. 이는 fixture 상대 진단이며 실제 FP/FN 정확도가 아니다.

## 보호 회귀 및 전체 Gate

- 기존 비공개 143개 기준 답안 재생: 수정 전/후 143행, 변경 0. SHA-256 양쪽 모두 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`. 답안 원문과 출력은 `/tmp`에 비공개로 보존했고 저장소에 넣지 않았다.
- `python3 -B -m pytest -q tests/test_deterministic_requirement_evaluator.py tests/test_audit_relation_recognition.py`: **17 passed**.
- `python3 -B scripts/rubric_manager.py validate-all`: `ALL VALID`.
- `python3 -B scripts/check_generated_rubrics_freshness.py`: `GENERATED RUBRICS FRESH`, 6 files.
- `python3 -B scripts/rubric_manager.py validate-topic-pack-release --all`: exit 0, `TOPIC PACK RELEASE VALIDATION PASS`; 선택 smoke 단계는 보고서 부재로 `SKIPPED`.
- `PROMOTE_GENERATED=0 bash scripts/validate_release.sh`: exit code 0. 로그의 `VALIDATION=PASS_WITH_QUARANTINE`는 synthetic fail-closed orchestration regression 출력이며 실제 Release Candidate 판정이 아니다.
- 공식 offline Release Candidate (`VALIDATION_LIVE_API=0 QUALITATIVE_DE_MODE=off PROMOTE_GENERATED=0 python3 -B scripts/release_candidate.py validate`): **1,698 passed, 0 failed, 2 skipped; exit 0; `VALIDATION=PASS`**. Manifest: `reports/release_candidates/20261125T115557Z_5718f21239e9_pytest/manifest.json`, candidate commit `5718f21239e97435359fabe006a177b560695ff1`.
- 이 manifest는 C2의 코드/시험 SHA에서 생성됐다. 이후 산출물 전용 커밋이 생기면 해당 최종 SHA에서 Release Candidate와 GitHub Actions를 다시 실행하고 결과를 Issue/PR에 보충한다.

## 불변성

Fact Anchor, 승인 Registry, Ontology, Topic Pack, Generated 결과, 채점 권한/정책은 변경하지 않았다. `119 HOLD`, D4 상태, 기존 제외 정책, `score_admission=DISABLED`, `score_effect=none`, main 미병합 및 운영 미배포 상태를 유지했다. 독립 전문가 라벨은 0건이고 accuracy는 `NOT_ESTABLISHED`다.

## 최종 처분

P2-B는 111건 실제 실행, 최소 fail-closed 수정 및 회귀 검증까지 진행됐지만 완료 기준은 충족하지 못했다. RRF 조건이 Machine Fact에 명시적으로 구조화되고 검토되기 전까지 관계를 안전하게 제한할 수 없으며, 자연어 20건도 확인되지 않았다. 따라서 **P2-B는 부분 완료, P2-C 미착수/차단**이다. 다음으로 필요한 범위는 RRF의 동일 시나리오·시간 조건에 관한 별도 Machine Contract 후보 검토와 자연어 추출 한계에 대한 owner 승인된 검증 설계다. 이 문서는 그러한 변경을 승인하지 않는다.
