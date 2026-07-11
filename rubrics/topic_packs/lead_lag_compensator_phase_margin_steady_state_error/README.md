# 진상·지상 보상기의 위상여유·정상상태 오차 설계

## Topic ID

`lead_lag_compensator_phase_margin_steady_state_error`

## 분류

- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화

## 대표 문제

진상보상기와 지상보상기의 전달함수, 주파수응답 특성과 설계 절차를
설명하고 위상여유와 정상상태 오차 개선을 위한 고려사항을 논하시오.

## 진상보상기

    C_lead(s) = Kc(1 + Ts) / (1 + αTs),  0 < α < 1

- 영점: `-1/T`
- 극점: `-1/(αT)`
- 위치 관계: `|p| > |z|`
- 최대 위상진상: `φmax = sin^-1((1-α)/(1+α))`
- 중심주파수: `ωm = 1/(T√α)`

## 지상보상기

    C_lag(s) = Kc(1 + Ts) / (1 + βTs),  β > 1

- 영점: `-1/T`
- 극점: `-1/(βT)`
- 위치 관계: `|p| < |z|`
- 저주파 이득: `Kc`
- 고주파 이득: `Kc/β`

## Source 구성

- `fact_anchor.json`: 14개 핵심 사실과 8개 Fatal 오개념
- `logic_check.json`: LLM truth schema와 fatal condition
- `model_answer.json`: 8개 권장 답안 구조
- `topic_importance.json`: 8개 고득점 해제 조건
- `README.md`: Topic Pack 안내

## 핵심 채점 원칙

- 극점·영점 위치나 위상·오차 원리를 반대로 단정하면 Fatal 후보로 본다.
- 단순 공식 누락은 즉시 Fatal로 처리하지 않는다.
- 진상 설계에서는 교차주파수 이동을 반영한다.
- 지상 설계에서는 저주파 이득 개선과 시스템 형 증가를 구분한다.
- 보상 후 주파수응답·시간응답·정상상태 오차·노이즈·포화를 검증한다.
