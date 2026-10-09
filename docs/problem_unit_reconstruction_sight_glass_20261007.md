# Sight Glass Level Topic Pack 문제 단위 감사

검토일: 2026-10-07
대상: `sight_glass_level_gauge_communicating_vessels_interface`
상태: `draft / human_review_required` 유지

## 판정 및 보완

두 문제 단위는 연통·상별 연결 원리와 유리관 지시불량·고온고압 적용으로 구분된다. 기존 Pack은 5개 Anchor가 patterns와 outline에 연결돼 있었으나 intent/example은 없었다. 또한 모든 high-score 조건이 공통이어서 유리관 질문에서 직접 요구되지 않는 자기식 게이지 부자·챔버 구조를 필수처럼 요구했다.

- 2개 대표문항 각각에 intent와 example을 추가했다.
- 5개 Anchor의 pattern/outline 추적을 회귀 테스트로 고정했다.
- pattern별 high-score, common-missing 및 importance 기준을 제한했다.
- 자기식 지시부/부자 설명은 문항이 직접 비교를 요구할 때만 평가하고, 누락 자체는 감점하지 않는다.
- Fact Anchor 기술문장, Question Type, logic-check 정책은 변경하지 않았다.
- 기존 초안 상태와 reviewer metadata를 승인·검증완료로 승격하지 않았다.

## 검증

- Focused pattern-scope regression: 4/4 PASS.
- Schema/global-anchor validation: PASS (87 packs, 2,068 anchors).
- Quality: PASS, 0 errors, 0 warnings.
- Atomicity: PASS, 0 errors, 0 warnings.
- Scoped release: PASS; generated output restored to its pre-validation snapshot; LLM smoke skipped.
- Topic status remains `draft / human_review_required`; source hash is intentionally not synced and approval/review metadata is untouched.

구조 검증은 수두·계면 연결에 대한 기술 정확성이나 사람의 최종 승인을 대신하지 않는다.
