# Topic 학습 구성 Stage 8 검증 결과

## 최종 전달 대상과 다음 작업

전달 대상은 `https://github.com/now0930/prof_eng_answer.git`의
`codex/record-master-expansion-deployment-20261005` 브랜치다. workspace의 origin은
로컬 중계 저장소이므로 실제 GitHub URL을 확인한 뒤 명시적으로 push한다.
GitHub에서 확인한 기준 커밋 `fb5f6b7`은 현재 작업의 조상이므로 force push나
main 병합 없이 작업 브랜치를 갱신할 수 있다. 실제 push 결과는 작업 응답에서
원격 SHA 일치 여부와 함께 보고한다.

이번 8단계 완료 범위는 초안 작성·검증·View·격리된 통합 검증이다.
다음 개발 범위는 **검토 결과를 받아 학습 후보를 Master에 연결하는 적용 경로**다.
현재 CLI에는 prepare/build만 있으며 실제 적용 명령은 없다.

1. 검토 결정에 후보 해시·검토자·시각·지식/학습 경로별 상태를 고정한다.
2. 변경된 후보에 이전 승인을 재사용하지 못하도록 검증한다.
3. Master revision·before hash·source hash를 다시 검사하는 미리보기를 제공한다.
4. 별도 명시적 적용으로 학습자료와 Master 참조만 변경하고 실패 시 복구한다.
5. 적용 전후 채점 payload 불변과 복습 표시를 검증한다.

위 적용 기능은 이번에 추가하지 않았다. 실제 인간 검토 기록이 없는 자료에
human_verified 상태를 부여하지 않으며 원문·채점 기준 승격과 구분한다.
운영 재시작과 GitHub main 병합도 이번 전달에 포함하지 않는다.

검증일: 2026-10-05 (Asia/Seoul). 구현·대표 Topic 검증은 Stage 7까지 완료했다.
초기 Stage 8에서는 전체 회귀가 실패했으나 아래 후속 수정으로 pytest가 통과했다.
운영 배포·Master 후보 연결은 하지 않았다.

## 후속 회귀 정리

전체 pytest 재실행: **734 passed / 1 warning**, 실패 0건.
로그: `/tmp/synthesis_final_pytest.log`.

non-promote release 스크립트와 `validate-topic-pack-release --all`도 exit 0이다.
로그: `/tmp/synthesis_final_release.log`, `/tmp/synthesis_final_topic_release.log`.
live smoke와 opt-in 10회 재현성 검사는 실행하지 않았다.

운영 채점 코드는 수정하지 않았다. 변경 근거는 다음과 같다.

- difficulty 처리는 직접 호출에서 compatibility wrapper로 이동해 AST 검증 대상을 변경했다.
- Gemini의 정상·fail-closed 두 경로 모두 `contract.get("primary_lens")`를
  전달하는 현재 question-contract authority를 검사한다.
- cache 검증은 deterministic-primary와 legacy 반환 경로를 각각 확인한다.
  단순 파일 줄 순서로 두 경로를 혼동하지 않도록 했다.
- generic canonical-axis 검증은 compact-secondary 선택을 명시적으로 비활성화한
  테스트 문맥에서 기존 generic 분기를 검사한다. compact 분기는 별도 기존 회귀로 검사한다.
- `runtime_grading_provenance`는 누락이 아니라 `grading/scoring/`로 이동되어 있었다.
  테스트 import를 실제 경로로 수정했다. 아래 초기 진단의 모듈 부재 표현을 정정한다.
- 과거 비공개 세션 의존은 `tests/compact_secondary_fixture.py`의 공개 합성
  reproduction으로 교체했다. 이미 커밋된 stage25g3d OCR 표 구조를 사용하며,
  실제 과거 답안 복구라고 주장하지 않는다. fatal 2건, 단일 호출, 14.5 ceiling,
  관련 HFT 행만 재분류하는 기존 검증을 유지했다. 현재 metadata의
  `multi_topic_ids=[]`도 정확하게 검사한다.

기존 private E2E의 bool 반환 warning 1건은 남아 있으며 실패는 아니다.
전체 테스트를 skip하거나 예상 점수를 변경해서 통과시키지 않았다.

## 초기 검증 기록 (수정 전)

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
