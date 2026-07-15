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

## Lead-lag 설계 적용조건

- 지상보상기의 저주파·고주파 상대 이득비는 β이다. 목표 교차주파수 부근의 이득을 기존 수준으로 유지하도록 K_c를 선택한 경우 저주파 루프이득과 해당 정적 오차상수를 약 β배 높일 수 있다. 실제 개선비는 K_c, 기존 루프이득, 시스템 형과 입력 종류를 함께 계산하여 확인한다.
- 진상보상기는 양의 위상뿐 아니라 크기응답도 변화시키므로 새 이득교차주파수와 위상여유를 보상 후 개루프에서 다시 계산해야 한다.
- 위상여유와 감쇠비·오버슈트의 관계는 안정한 최소위상 단일루프에서 지배적 2차계 근사가 유효할 때 사용하는 설계 경향이며 일반적인 등식으로 단정하지 않는다.
- 보상기 설계 후에는 센서 잡음, 제어입력, 액추에이터 포화와 rate limit, 샘플링·이산화, 시간지연 및 모델 불확실성을 시간영역과 주파수영역에서 함께 검증한다.
- Fatal의 직접 점수 영향은 B/C에 한정한다. D/E는 직접 감점하지 않고 관련 claim trust만 제한한다.

## Fact verification references

- MIT OpenCourseWare 16.30 Topic 4: Control design using Bode plots
- MathWorks `Bode Diagram Design`
- MathWorks loop-shaping and robust-control guidance
- MathWorks Control System Designer
- MathWorks PID anti-windup guidance
