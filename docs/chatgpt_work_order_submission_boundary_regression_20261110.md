# 작업 완료 보고 — 입력 경계 및 pytest 복구

## 범위와 안전성

`/grade`의 문제/답안 분리와 이번 전체 pytest에서 확인된 일곱 실패를 처리했다. 점수, A/B/C/D/E, Fatal, Fact의 승인·채점 적격성은 변경하지 않았다. 개인 답안, 세션 원문, 자격증명 및 운영 DB는 출력·복사·커밋하지 않았다. 사용자가 수정한 `docs/README.md`와 `docs/chatgpt_server_latest_main_deployment_checklist_20261109.md`는 보존했다.

브랜치 `fix/telegram-grade-numbered-question-20261110`, 기준 HEAD `ed72eaf007610d7af3e0d0822b1b57f864940480`에서 작업했다. 모든 변경은 아직 미커밋이다.

## `/grade` 입력 경계

- `문제:`, `문제 1.`, `[문제]`, `답안:`, `답안`, `[답안]` 표지를 처리하고 명시 경계를 우선한다.
- 표지가 불완전한 경우 번호형 답안 제목 등 문서 구조로 경계를 추론하며, 여러 줄 문항을 지원한다.
- 질문과 답안이 비거나 겹치는 등 경계가 불명확하면 원문을 보존하고 채점·라우팅하지 않으며 사용자에게 형식 안내를 제공한다.
- Router에는 분리된 질문만, 답안 평가는 분리된 답안만 전달한다. `P₁` 같은 기술 문자는 보존한다.
- 경계, 원문 줄 범위, 신뢰도 및 상태를 추적한다.

관련 입력 정규화기·Telegram 연결 회귀 테스트: **52 passed**. 이후 전체 pytest도 통과했다.

## 전체 pytest 실패 일곱 건의 처리

1. 승인된 한국어 Anchor를 테스트가 낡은 영문 문자열로만 검사하던 네 테스트를 의미·기술 요건을 확인하도록 맞췄다. 한국어 원문과 조건은 유지했다.
2. 감사 재현에서 최신 원본과 이전 검토 CSV의 역할이 혼재했다. 2026-11-02 원본 스냅샷과 완료된 검토 기록은 보존하고, 현재 문장으로는 별도 2026-11-10 검토 CSV를 생성했다. 검증기는 명시적 source snapshot을 입력받아 해당 시점의 불변 필드를 비교한다.
3. canonical promotion ledger는 공식 `promote_reviewed_fact_anchors.py --write` 생성 절차로 갱신했다. 5개 `topic_source_sha256`가 갱신됐고, 각 승격 Fact의 `statement_sha256`, Fact ID 및 승격/채점 판정은 바뀌지 않았다.
4. 일곱 항목을 모두 통과시킨 뒤 `calibration/pytest_quarantine.json`의 제외 목록을 비웠다. 실패 기록은 resolved history로 남겼으며, 실패를 skip/quarantine으로 숨기지 않았다.

2026-11-02 완료 검토의 원문·결론을 현재 Topic Pack 내용으로 덮어쓰지 않았다. 신규 11-10 검토 패킷은 새 문장 검토용이며 승인/승격을 뜻하지 않는다.

## 검증 결과

- 전체 명령: `python3 -B -m pytest -q`
- 결과: **1608 passed, 2 skipped, 0 failed, 경고 없음 (339.32초)**
- 기존 입력 경계·정규화기·결정론 채점 관련 집중 검사: **52 passed**
- Fact Anchor reconciliation 및 관련 구조 테스트: **43 passed**
- Python 컴파일 검사는 작업 중 통과했다.
- `test_private_master_to_review`는 공개 checkout에 없는 비공개 WordPress bundle을 요구하므로 명시적 `pytest.skip`으로 바꿨다. 비공개 fixture가 있을 때의 통합 검증은 그대로 수행하며, 없으면 사유가 분명한 skip으로 처리한다. 단독 실행도 같은 사유를 `SKIP`으로 표시한다.

## 미실행 사항

- 운영 서버 pull, 컨테이너 재시작, 배포: 미수행
- Git commit/push: 미수행
- GitHub Actions: 미실행
- Accuracy Gate / Qualification / 유료 LLM 호출: 미실행

따라서 이 검증은 개발 checkout의 pytest 결과이며, 운영 반영 또는 배포 승인을 의미하지 않는다.
