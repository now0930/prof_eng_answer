# Nyquist 안정도 판별과 이득·위상여유

## Topic Pack 식별정보

- topic_id: `nyquist_stability_criterion_gain_phase_margin`
- question_type: `CALC_DESIGN`
- difficulty: `THEORY_CORE`
- selection_importance: `CORE_MUST_PREPARE`
- 평가 방식: Fact Anchor + Model Answer + LLM-only Logic Check

## 목적

이 Topic Pack은 Nyquist contour와 argument principle을 이용하여
폐루프 안정성을 판정하고, gain margin과 phase margin을
현장 강인성에 연결하는 답안을 평가한다.

단순한 Nyquist plot 모양 암기가 아니라 다음 연결을 요구한다.

- 표준 음의 피드백의 특성방정식 `1+L(s)=0`
- 개루프 우반평면 극점 수 `P`
- `-1+j0` 임계점의 순선회수 `N`
- 폐루프 우반평면 극점 수 `Z`
- 선택한 선회 방향 convention
- gain·phase crossover와 GM·PM
- 허수축 극점, 시간지연과 복수 crossover
- 수학적 안정경계와 현장 운전여유

## 핵심 판정 convention

이 Topic Pack은 우반평면 Nyquist contour를 시계방향으로 돌고,
`-1`점의 순시계방향 선회수를 양수로 정의한다.

따라서 다음 식을 사용한다.

- `N_cw = Z - P`
- `Z = P + N_cw`
- 폐루프 점근안정 조건: `Z = 0`
- 필요한 선회수: `N_cw = -P`

반시계방향 양수 convention을 명확히 정의하고
끝까지 일관되게 사용한 답안도 정상으로 인정한다.

## 파일 구성

- `fact_anchor.json`: 14개 핵심 Fact Anchor와 8개 fatal 오개념
- `logic_check.json`: deterministic 비활성 LLM 검증 profile
- `model_answer.json`: 8개 section의 계산·설계형 모범 답안
- `topic_importance.json`: 난이도와 문항 선택 중요도
- `README.md`: Topic Pack 운영 설명

## 대표 계산

`L(s)=K/[s(s+1)(s+2)]`에서 phase crossover는
`ω_pc=√2`이고 임계이득은 `K_cr=6`이다.

따라서 점근안정 범위는 `0<K<6`이며
Routh-Hurwitz 결과와 일치한다.

## Logic Check 정책

- deterministic checks: disabled
- candidate extraction rules: empty
- key-term semantic fallback: enabled by common runtime
- fatal confidence threshold: `0.75`
- fatal recommended ceiling: `10.0`
- 필수 출력: `verdict`, `confidence`, `reason`, `checks`, `findings`

LLM은 candidate evidence의 실제 주장과 전체 문맥을 확인한다.
오개념 인용 후 명확히 반박한 문장은 fatal로 판정하지 않는다.
