# 저항·정전용량·인덕턴스형 센서의 물성·기하 변환 원리

## Topic ID

`passive_sensor_resistive_capacitive_inductive_transduction`

## 분류

- 문제 유형: `PRINCIPLE`
- 난이도: `FIELD_APPLICATION`
- 선택 중요도: `NORMAL`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화

## 대표 문제

저항형, 정전용량형, 인덕턴스형 센서에서 재료 물성과 기하학적
변형이 R, C, L을 변화시키고 전압·전류 신호로 검출되는 원리를
설명하시오.

## 통합 변환 사슬

    측정량
    -> 기계적 변형 또는 재료 물성 변화
    -> Delta R, Delta C, Delta L
    -> 외부 여기와 신호조절
    -> 전압, 전류, 임피던스, 위상, 주파수

수동형 파라미터 센서는 일반적으로 외부 여기가 필요하다.

## Young's modulus

    sigma_m = F / A_m
    epsilon_m = Delta l / l
    E = sigma_m / epsilon_m

Young's modulus는 전기적 물성이 아니라 힘과 압력을 기하학적
변형으로 바꾸는 기계적 물성이다.

## 저항형 센서

    R = rho l / A
    R = l / (kappa A)

    Delta R / R
    =
    Delta rho / rho
    + Delta l / l
    - Delta A / A

핵심 물성은 도전율 `kappa` 또는 비저항 `rho`이며, 길이와 단면적은
기하학적 변수다.

스트레인 게이지는 Gauge factor와 Wheatstone bridge를 이용한다.

## 정전용량형 센서

    C = epsilon A / d

    Delta C / C
    =
    Delta epsilon / epsilon
    + Delta A / A
    - Delta d / d

핵심 물성은 유전율 `epsilon`이며, 전극면적과 간격은 기하학적
변수다.

    q = C V

    i = C dV/dt + V dC/dt

AC bridge, charge amplifier, oscillator 또는 CDC로 검출할 수 있다.

## 인덕턴스형 센서

    R_m = l_m / (mu A)
    L = N^2 / R_m

    L approximately mu N^2 A / l_m

핵심 물성은 투자율 `mu`이며, 자속면적, 자기회로 길이와 공극은
기하학적 변수다.

와전류 센서에서는 대상체의 도전율, 투자율, 두께, 주파수와 거리가
코일 복소 임피던스를 변화시킨다.

## 세 물성의 대응

- 저항 `R` ↔ 도전율 `kappa`
- 정전용량 `C` ↔ 유전율 `epsilon`
- 인덕턴스 `L` ↔ 투자율 `mu`

도전율, 유전율과 투자율은 서로 다른 물리량이다.

## Source 구성

- `fact_anchor.json`: 14개 핵심 사실과 8개 Fatal 오개념
- `logic_check.json`: LLM truth schema와 fatal condition
- `model_answer.json`: 8개 권장 답안 구조
- `topic_importance.json`: 8개 고득점 해제조건
- `README.md`: Topic Pack 안내

## 핵심 채점 원칙

- 물성, 기하와 신호조절의 역할을 구분한다.
- Young's modulus를 기계적 변형의 연결요소로 설명한다.
- R, C, L의 기본식과 변화율을 인과관계로 설명한다.
- 수동센서의 외부 여기 필요성을 설명한다.
- 감도와 범위·선형성·잡음의 상충관계를 설명한다.
- 교정, 불확도, 환경과 동적응답을 포함해 검증한다.
