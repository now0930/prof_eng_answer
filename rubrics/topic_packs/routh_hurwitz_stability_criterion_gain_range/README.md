# Routh-Hurwitz 안정도 판별과 제어기 이득 범위

## 1. Topic Pack 개요

- Topic ID: `routh_hurwitz_stability_criterion_gain_range`
- 대표 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 중요도: `CORE_MUST_PREPARE`
- Logic Check: LLM profile only
- 결정론적 정규표현식 검사: 사용하지 않음

이 Topic Pack은 폐루프 특성방정식에서 Routh 배열을 작성하고 우반평면 극점 수, 점근안정 여부, 제어기 이득 범위와 상대안정도를 판단하는 계산형 답안을 평가한다.

## 2. 핵심 범위

1. 특성방정식과 열린 좌반평면 극점 조건
2. Routh 배열 첫 두 행과 일반 행 계산
3. 첫 열 부호 변화와 우반평면 근 수
4. 양의 계수 조건의 한계
5. 첫 열 원소 0의 ε 처리
6. 전체 0행과 보조다항식
7. 이득 K 범위와 경계값 검증
8. 상대안정도 축 이동
9. 시간지연과 적용 한계
10. 현장 안정여유와 보완 검증

## 3. Source 파일

- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

## 4. Fatal 오개념

1. `routh_sign_changes_left_half_plane`
2. `positive_coefficients_always_stable`
3. `zero_leading_element_same_as_zero_row`
4. `zero_row_immediately_unstable`
5. `no_sign_change_always_asymptotically_stable`
6. `routh_entries_are_pole_locations`
7. `gain_boundary_always_included`
8. `direct_routh_on_time_delay`

## 5. Logic Check 원칙

- 정규표현식으로 사실 여부를 판정하지 않는다.
- LLM이 8개 fatal condition을 항목별로 검토한다.
- 인용, 반례, 오류 교정과 실제 주장을 구분한다.
- 단순 누락은 fatal로 판정하지 않는다.
- LLM 실패 시 fail-open diagnostic을 사용한다.

## 6. 현장 적용

수학적으로 안정한 이득 범위와 실제 운전 가능한 이득 범위는 다를 수 있다. 운전점 변화, 시간지연, 센서 잡음, 밸브 비선형, 포화와 안정여유를 함께 검토하고 극점 계산, Bode/Nyquist 및 제한된 step test로 검증한다.

## 7. 작성 근거

`docs/topic_sheets/routh_hurwitz_stability_criterion_gain_range.md`의 사람이 검토한 요구사항을 기준으로 ChatGPT가 source JSON을 직접 작성했다. 참조 Topic Pack은 schema 확인에만 사용했으며 주제별 집계·라우팅·평가 내용은 전부 Routh-Hurwitz 기준으로 재작성했다.
