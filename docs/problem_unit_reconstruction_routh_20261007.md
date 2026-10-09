# Routh-Hurwitz Pack 문제 단위 및 요구별 coverage 검토

검토일: 2026-10-07
대상: `routh_hurwitz_stability_criterion_gain_range`
자동 primary disposition: disconnected question families / boundary review
상태: source JSON·README·Topic Sheet를 요구범위 기준으로 보완; human technical review 전

## 판단

5개 question patterns의 자동 clustering은 원리·계산 2개, K/상대안정도 2개, 특수행 1개로
세 family를 분리했다. 그러나 이들은 **같은 Routh-Hurwitz 계산기법을 특성다항식에 적용하는
문제 변형**이다. 독립 이론 영역을 부당하게 한 Pack에 결합한 것이라기보다, 하나의 Routh
problem unit 안에 질문별 계산범위가 서로 다른 구조로 판단한다. 즉시 분리하지 않는다.

## 발견한 연결 문제

- 14개 Anchor 중 original patterns가 union으로 요구한 것은 11개(79%)였다.
- 모든 8개 recommended outline에 `anchor_refs`가 비어 있었다.
- `positive_coefficients_not_sufficient`는 안정판정 원리의 중심 조건인데 pattern 1·2에서
  요구되지 않았다.
- `routh_does_not_return_exact_pole_locations`는 원리설명의 중요한 경계인데 pattern 1에
  연결되지 않았다.
- `time_delay_requires_approximation_or_frequency_method`는 광범위한 한계 지식이다. 단순
  계산 문제에서 필수요구로 처리되면 과잉평가가 될 수 있다.
- 전역 `high_score_points`, `common_missing_points`, `topic_importance`, logic `major_checks`가
  특수행/K 경계/상대안정도/시간지연/현장여유를 모든 문제에 요구하는 문구로 읽힐 수 있었다.

## 보완 내용

- Pattern 1에 양의 계수 필요조건의 한계와 Routh가 정확한 pole locations를 주지 않는 점을
  연결했다. Pattern 2에 양의 계수 조건의 한계를 연결했다.
- 8개 outline section에 Anchor refs를 전부 채웠다.
- 시간지연 fact를 `optional`로 두고, 타 조건은 해당 문제에서 요구하거나 계산상 실제 발생할
  때만 필수라고 high-score, common-missing, topic-importance, Logic major guidance에 한정했다.
- 대표 Topic Sheet/README에 하나의 기법 단위와 다섯 질문별 coverage contract를 기록했다.
- Fatal IDs, deterministic scoring, A/B/C/D/E contract, Question Type, aliases/router, pattern
  문장, score weights는 바꾸지 않았다. Fatal은 계속 학생이 오개념을 실제 정답으로 주장한
  경우에만 적용한다.

Pattern-to-anchor union은 11/14(79%)에서 13/14(93%)로 올랐다. 남은 미참조 anchor는
시간지연의 적용경계로, 문제에서 해당 한계를 물을 때에만 평가하는 선택 지식이다. 이는
문제 coverage의 자동 증명이 아니라 질문 demand와 anchor 범위를 정렬한 결과다.

## 검증 상태

다음 scoped schema/quality/release 검증이 필요하다. 전체 release gate는 다른 managed draft의
승인상태 때문에 별도로 막혀 있다. Routh fact의 기술 원문 판·쪽 및 수식 대조는 이 검토에서
수행하지 않았으며, 외부 승인/출제 빈도를 주장하지 않는다.
