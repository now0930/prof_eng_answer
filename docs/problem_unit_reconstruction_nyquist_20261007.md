# Nyquist Topic Pack 문제 단위 감사

작성일: 2026-10-07
대상: `nyquist_stability_criterion_gain_phase_margin`

## 판정

Nyquist 안정도 판별·이득범위·특수조건·안정여유의 5개 질문 패턴을 하나의 주파수응답 안정도 문제영역으로 유지한다. 자동 원자성 경고는 없지만, 기존 global 평가기준을 각 패턴에서 전부 요구하지 않도록 범위를 제한했다.

## 보완 내용

- 대표 원리·판별 패턴에 `stable_open_loop_special_case`를 추가해 P=0 특수형이 14개 Anchor required union에 빠져 있던 공백을 채웠다.
- 이득 K 안정범위 문항에서 현장 강인성 Anchor를 필수 요구에서 빼고, 개루프/폐루프 RHP 극점 개수로 안정구간을 계산하도록 정렬했다. 현장 검증은 해당 문항이 직접 요구하는 강인성 질문에 한정한다.
- 8개 답안 outline의 intent가 모든 section에서 동일했던 오류를 수정하고 section별 anchor_refs를 작성했다. 이제 14개 Anchor 모두 outline에서 추적된다.
- `high_score_points`, `common_missing_points`, importance unlock을 5개 question pattern 범위로 제한했다.
- 기존 common-missing 항목 중 “Nyquist 궤적 첫 두 행 계수 배치”는 Nyquist 질문 요구와 맞지 않고 Routh 표 개념을 혼입하므로 제거했다. Routh는 K 안정범위 문항의 선택적 교차검증으로만 남겼다.
- Question Type, 8개 Fatal 계약, Router/alias, deterministic scoring 및 점수계약은 변경하지 않았다.

## 검증

- Schema validation: PASS; 전체 source inventory 87 Pack / 2,067 Anchor 확인.
- Topic quality (`--require-logic-check`): PASS, errors 0, warnings 0.
- Atomicity audit: PASS, warnings 0.
- 5 patterns / 5 examples 일치.
- Required-anchor union: 14/14; outline Anchor refs: 14/14; foreign/unresolved refs 0.
- 전용 Router/Routh 경계 회귀 `scripts/test_nyquist_routh_routing_boundary.py`: 3/3 PASS.
- Scoped release: PASS; generated pipeline PASS, smoke SKIPPED. generated outputs는 사전 snapshot으로 복원.
- `git diff --check`: PASS.

## 집계 범위

inventory screen에서 이 Pack은 자동 경고 없는 `잠정 유지 후보`였다. 요청에 따른 추가 의미/구조 감사이며, 기존 30개 구조경고와 10개 coverage candidate로 정의한 40건 집계에는 포함되지 않으므로 그 진행 카운터는 변경하지 않는다.
