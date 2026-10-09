# SIS/SIL 안전 소프트웨어 Topic Pack 문제 단위 보충 감사

## 범위와 판정

대상은 `sis_sil_safety_software_independence_systematic_failure_verification_validation`이다. 이번 작업은 기존 자동 screen의 40건 상세검토를 대체하거나 Topic Pack을 승인하는 작업이 아니라, 문제별 의도와 채점 범위가 일치하는지 확인한 별도 보충 감사다. 따라서 공식 진행 카운터 `29/40`은 변경하지 않는다.

## 확인한 구조

- 대표 패턴 15개: 긍정형 10개, 경계 오분류 방지형 3개, 인접 V-Model/SIL 회귀 패턴 2개.
- 문제 예시 10개는 긍정형 10개에 대응한다. Topic Sheet의 부정형 8개는 별도 routing 경계 사례이며 대표 패턴 수와 동일한 목록이 아니다.
- 원천 Anchor는 34개이고, logic profile의 실제 fatal 조건은 18개다. 기존 README/Sheet의 31/16 표기는 원천 데이터와 맞지 않아 수정했다.
- 10개 대표 문제에 동일한 일반 intent가 반복되어, 문항 요구와 피드백 연결을 판별하기 어려웠다.
- 고득점·누락 및 importance 조건은 패턴별 적용범위가 드러나지 않아, 인접 질문에서 요구하지 않은 주제를 감점/가점할 여지가 있었다.

## 변경

- 각 대표 패턴의 intent를 해당 질문의 지식·판단 요구에 맞게 구체화했다. 세 경계 패턴은 Boundary guard임을 명시했다.
- 고득점, 누락 및 중요도 조건에 적용 패턴을 명시하고, Pattern 12(MISRA 지침과 동적 단위시험의 구분)의 긍정·누락 평가 조건을 보강했다.
- pattern 문장, required Anchor 연결, Question Type, routing 권한, alias, fatal 처리 및 logic-check 실행 권한은 변경하지 않았다.
- README와 Topic Sheet의 원천 요약 개수를 실제 JSON 기준으로 맞추고 패턴 그룹 구성을 설명했다.

## 검증

- `tests/test_sis_sil_pattern_scope.py`: 3/3 PASS.
- `scripts/test_sis_sil_safety_software_topic.py`: 16/16 PASS.
- topic-pack schema validation: PASS (87 packs, 2,068 anchors).
- quality validation: PASS (0 errors, 0 warnings).
- atomicity audit: PASS (0 errors, 0 warnings).
- scoped release: PASS. 검증 중 생성되는 projection은 사전 snapshot으로 복구했고, LLM smoke는 실행하지 않았다.
- 변경 파일 `git diff --check`: PASS.

이 결과는 구조와 계약 검증이며 안전 표준 조항이나 기술 내용의 전문가 승인을 의미하지 않는다. 향후 사람/LLM 내용 검토가 필요한 사실 주장은 별도 검토 대상으로 남긴다.

## 다음 후보

Screen inventory에서 큰 Anchor 집합 경계 재검토 후보로 표시된 `smart_positioner_diagnostics_valve_signature_predictive_maintenance`를 다음 보충 감사 후보로 둔다. 이는 topic routing 또는 승인 상태 변경을 뜻하지 않는다.
