# LQR Topic Pack 문제 단위 감사

작성일: 2026-10-07
대상: `lqr_optimal_state_feedback_riccati_weighting_design`

## 판정

LQR 설계라는 일관된 핵심 문제영역 안에 5개 질문 family가 있다: 비용함수·CARE 설계절차, Q/R 가중치, 해 존재조건, 극점 배치·기준입력 추종 비교, CARE/DARE 및 실장 검증. 현재 Topic ID와 상위 routing은 유지한다. 단일 질문을 가장한 채 모든 가족의 상세 지식을 각 답안에 요구하지 않도록 각 질문별 required Anchor와 평가 문구를 제한했다.

Pattern 4는 기존 `state_feedback_reference_tracking_prefilter_integral_action`과 기준입력·LQI 범위가 인접한다. 이 Pack에서는 LQR 대 극점배치 및 LQR에서 LQI로의 확장이라는 비교 관점만 유지하고, 독립 owner/routing 변경은 하지 않았다. Stage 6의 cross-topic ownership 검토 대상이다.

## 수정

- Q/R 영향 패턴에 공통 배율 불변성 Anchor `state_lqr_common_scaling_invariance`를 추가했다. 질문의 가중치 비교에 직접 관련하며, 이에 따라 14/14 Anchors가 대표 질문 required union에 연결됐다.
- `high_score_points` 14개와 `common_missing_points` 8개를 pattern-scoped로 재작성했다. 비용함수·CARE, Q/R 튜닝, 존재조건, 추종 비교, 실장검증의 요구를 상호 무관한 문항에 전파하지 않는다.
- 중요도 unlock 조건을 10개 문항 범위형 조건으로 교체했다. 일반화 교차항 N, 비영점 평형점/LQI 세부조건은 질문이 해당 범위를 명시한 경우에만 평가하도록 했다.
- README에 5개 plausible question pattern과 문항별 요구 범위 원칙을 명시했다.
- Topic ID, Question Type, routing aliases, fatal IDs, machine contract, deterministic scoring과 score contract는 변경하지 않았다.

## 경계·잔여 주의사항

- Atomicity audit는 `DISCONNECTED_QUESTION_FAMILIES` 1건(4 components: 2/1/1/1)을 계속 보고한다. 네 family가 실제로 별도 질문으로 성립하므로 허위 지식 연결을 추가하지 않았다. 이 경고 자체는 구조상 관측 신호이며 릴리스 오류가 아니다.
- 문항 4는 기존 상태피드백 추종 Pack과 이웃한다. 점수나 routing을 바꾸지 않고, owner 중복 여부만 전체 cross-topic audit에 이월한다.
- 해당 Pack 전용 회귀 테스트는 `tests/`, `scripts/` 최상위에서 발견하지 못했다. 범용 schema/quality/release 검사로 source contract를 검증했다.

## 검증

- Topic Pack schema validation: PASS.
- Topic Pack quality validation (`--require-logic-check`): PASS, errors 0, warnings 0.
- Atomicity audit: PASS, warning 1 (`DISCONNECTED_QUESTION_FAMILIES`).
- Coverage consistency: 5 patterns / 14 Anchors; required union 14/14, outline union 14/14.
- Scoped release (`--require-logic-check`): PASS; generated pipeline PASS, smoke SKIPPED. Release validator가 사전 snapshot의 generated outputs를 복원했다.
- `git diff --check`: PASS.
- generated output files는 source 변경으로 남겨두지 않았다.

## 근거·해석 범위

이는 저장소의 Topic Pack 작성계약과 현재 source files를 기준으로 한 구조 감사다. 공식 출제분류나 기출문항을 확인했다는 뜻이 아니며, 실제 내용의 기술적 최종 승인을 대신하지 않는다.
