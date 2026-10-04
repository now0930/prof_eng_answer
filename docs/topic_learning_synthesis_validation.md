# Topic 학습 구성 Stage 8 검증 결과

검증일: 2026-10-05 (Asia/Seoul). 구현·대표 Topic 검증은 Stage 7까지 완료했다.
Stage 8의 전체 회귀 PASS 조건은 미충족이다. 운영 배포·Master 후보 연결은 하지 않았다.

| 검사 | 결과 |
|---|---|
| 전체 `pytest -q` | 723 passed / 11 failed / 1 warning |
| Stage 3 실패 목록과 비교 | 11개 동일, 신규 실패 0개 |
| non-promote `scripts/validate_release.sh` | exit 0 |
| 실제 WordPress 기반 대표 Topic E2E | 전체 pytest에서 실행·통과 |
| 비공개 종합 자료 Git 추적 | 없음 |
| 운영 Master·canonical 변경 | 없음 |

release 실행 환경:
`PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 RUN_GRADING_REPRODUCIBILITY=0`.
live provider smoke와 opt-in 10회 reproducibility 검사는 실행하지 않았다.
release 스크립트 성공이 전체 pytest 성공을 대신하지 않는다.

## 남은 실패 분류

| 범주 | 수 | 재현 파일 / 증상 |
|---|---:|---|
| 기존 실행 구조와 AST 기대 불일치 | 3 | final_formatter_feedback_boundary: difficulty 호출 없음; generic_feedback_final_projection: attach 호출 수 2; grade_submission_normalizer: finalize/cache 순서 |
| 이전 canonical axis 계약 불일치 | 2 | stage22_canonical_axis_runtime_integration: 기존 prompt marker와 relationship_conflict_summary 기대 |
| 구현 모듈 부재 | 1 | stage23_generic_grading_contract: runtime_grading_provenance 없음 |
| 비공개 historical fixture 부재 | 5 | stage25g3e/g3f/g3g1/g3g: 특정 세션 input.raw.txt 없음 |

warning 1개는 기존 private Master E2E가 bool을 반환하는 pytest 경고다.
위 실패는 이번 변경에서 테스트 제외·기대값 완화·채점 규칙 수정으로 우회하지 않았다.
다음 작업은 기존 실행 계약과 테스트 기대를 대조하고, 누락 fixture를 공개 가능한
합성/익명 fixture로 재현할 수 있는지 조사하는 것이다. 검증 없이 실제 세션을
대체하거나 파일 부재를 PASS로 취급하지 않는다.

## 로그와 전달 상태

- `/tmp/synthesis_stage8_pytest.log`: 전체 pytest 상세 로그
- `/tmp/synthesis_stage8_release.log`: 기존 Golden 포함 release 상세 로그
- `data/topic_learning_authoring/nyquist_stability_criterion_gain_phase_margin/stage4_initial/`:
  비공개 출처 패킷·작성본·검토 메모·candidate

임시 로그와 비공개 자료는 Git에 올리지 않는다. 원격 origin은 로컬 경로 저장소이며
GitHub가 아니다. 이 단계에서는 push하지 않았다. 전체 회귀 실패 해결과 원격
목적지 확인 후 최종 전달을 진행한다.
