# Instrumentation Installation Topic Pack 문제 단위·coverage 재검토

일자: 2026-10-07
대상: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
기초 감사: `docs/topic_pack_problem_unit_screen_20261006.csv`의 3 disconnected families 경고

## 판정: 종합 field-installation work package로 유지

세 anchor-disconnected family 경고만으로 Pack을 세 개로 나누지 않았다. 실제로 출제 가능한
종합 질문은 승인기준·도면에서 시작해 계기 설치, cable/termination 및 impulse line 시공,
검사·punch closure·as-built 인수까지 설명하게 할 수 있다. 이것은 세 하위 기술을 단순 병렬
나열하는 것이 아니라 하나의 현장 설치·인수 lifecycle을 완성하는 문제다.

따라서 대표 종합 Pattern 1의 필수 anchor를 workflow 연결에 충분하도록 보강했다. 그 결과
선택 실행 `audit_topic_pack_atomicity.py --topic-id ...`에서 기존 `DISCONNECTED_QUESTION_FAMILIES`
경고가 사라지고 decision PASS / warning 0이 됐다. 이는 의미상 문제 단위 판정의 보조 증거일
뿐이며 자동 통과 자체가 분할 불필요를 증명하는 것은 아니다.

## 패턴별 필수범위

| Pattern | 문항 축 | 필수 범위 원칙 |
|---:|---|---|
| 1 | 설치·배선·도압관 시공과 검사 절차 | 승인기준, 도면, cable·terminal, impulse line·service slope, 검사·전기시험 경계, as-built 흐름 |
| 2–3 | cable tray/gland/terminal 및 power/VFD segregation | cable workmanship 또는 승인 설계의 현장 구현만 요구 |
| 4–6 | impulse tubing, service별 slope, DP high/low 설치오차 | 문항의 service·측정 구조에 해당하는 routing, hydrostatic/thermal error, fitting/support만 요구 |
| 7, 10 | 시공검사·punch·as-built, FAT 후 현장검사 | inspection closure evidence와 FAT/field evidence 경계 |
| 8 | 기술기준·승인문서 충돌 | 기준 hierarchy 및 정식 clarification/deviation |
| 9 | IS/위험장소 cable 설치 | 기존 승인 classification·gland·segregation 보존. 장비 선정과 장소 분류는 인접 owner |

33개 anchor 중 required-anchor union은 28개(84.8%)로 유지됐다. 나머지 다섯 anchor는
접근성/환경보호, spare core, P&ID와 grounding/EMC 설계 boundary 세부사항이다. 해당 문항이
요구하거나 답안의 기술 주장과 직접 관련될 때 보조 평가하며 무관한 답안의 공통 누락 감점으로
쓰지 않는다.

## 수정 사항

- Pattern 1에 승인도면 구현, cable routing/terminal, 공통 impulse routing/service slope,
  검사·continuity test와 as-built anchor를 추가해 질문문과 답안 요구를 맞췄다.
- 전역 `high_score_points`와 `common_missing_points`를 패턴별 적용 조건으로 다시 썼다.
  Cable-only 답안에 impulse-line 전체 요건을 요구하지 않는다.
- Fact Anchor 33개, fatal IDs, routing aliases, Question Type, deterministic scoring, output
  contract, adjacent Topic authority는 변경하지 않았다.
- `logic_check.json` deterministic topic aliases empty 품질 경고는 이번 수정 전부터 있던
  warning으로 보이며 비활성 deterministic checks나 routing contract를 추측해 수정하지 않았다.

## 검증 결과 및 한계

- Source schema PASS, focused topic regression PASS, power/grounding boundary regression PASS,
  environmental/EMC adjacent regression PASS.
- Atomicity audit: decision PASS, error 0, warning 0.
- Scoped generated-pipeline release PASS. Quality report는 error 0, warning 1(위 기존 empty alias).
  생성 rubric은 사전 snapshot으로 복원했다.
- Runtime grader의 새 hard pattern-scope enforcement는 만들지 않았다. 기존 grader/Router 계약을
  유지하고 Topic Pack source와 문서에 요구 범위를 명시했다.
