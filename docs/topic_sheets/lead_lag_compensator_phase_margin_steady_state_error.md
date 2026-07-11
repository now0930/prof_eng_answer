# 진상·지상 보상기의 위상여유·정상상태 오차 설계

## 1. Topic Pack 기본정보

- Topic ID: `lead_lag_compensator_phase_margin_steady_state_error`
- 한글 제목: `진상·지상 보상기의 위상여유·정상상태 오차 설계`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 문항 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 키워드 채점: 비활성화
- 권장 답안 분량: 기술사 답안지 약 3쪽
- 선행 Topic:
  - `feedback_system_closed_loop_sensitivity_steady_state_error`
  - `root_locus_stability_gain_design`
  - `bode_frequency_response_stability_margin_bandwidth`
  - `nyquist_stability_criterion_gain_phase_margin`

## 2. Topic 선정 이유

진상·지상 보상기는 제어대상 자체를 변경하지 않고 제어기의 극점과 영점을 추가하여
폐루프 시스템의 안정도, 과도응답, 정상상태 정확도를 개선하는 고전제어의 핵심 설계기법이다.

기존 Topic Pack은 다음 내용을 이미 다룬다.

1. 피드백 시스템의 민감도와 정상상태 오차
2. 근궤적을 이용한 안정도와 이득 설계
3. Bode 선도를 이용한 위상여유·이득여유·대역폭 해석
4. Nyquist 판별을 이용한 폐루프 안정도 검증

본 Topic Pack은 이들 해석 결과를 실제 보상기 파라미터 설계로 연결한다.

진상보상기는 양의 위상을 추가하여 위상여유와 응답속도를 개선하는 데 사용하며,
지상보상기는 저주파 루프이득을 높여 정상상태 오차를 줄이면서 교차주파수 변화를 제한하는 데 사용한다.

다만 보상기는 모든 성능을 동시에 개선하지 않는다.
대역폭, 노이즈 민감도, 제어입력, 강인성, 정상상태 오차 사이의 상충관계를 함께 설명해야 한다.

## 3. 대표 출제문제

> 진상보상기와 지상보상기의 전달함수, 주파수응답 특성 및 설계 절차를 설명하고,
> 위상여유와 정상상태 오차 개선을 위한 진상·지상 보상기 설계 시 고려사항을 논하시오.

계산·설계형 변형 문제는 다음을 포함할 수 있다.

- 목표 위상여유를 만족하는 진상보상기 설계
- 정상상태 오차상수를 만족하는 지상보상기 설계
- 목표 교차주파수에서 보상기 이득과 극점·영점 계산
- 진상·지상 결합보상기의 순차 설계
- 보상 전후 Bode 선도와 시간응답 비교
- 구현 시 포화·노이즈·이산화 영향을 고려한 파라미터 보정

## 4. 표준 설계 모델

단위피드백 시스템의 개루프 전달함수를 다음과 같이 둔다.

\[
L(s)=C(s)G(s)
\]

폐루프 전달함수는 다음과 같다.

\[
T(s)=\frac{L(s)}{1+L(s)}
\]

오차 전달함수는 다음과 같다.

\[
\frac{E(s)}{R(s)}=\frac{1}{1+L(s)}=S(s)
\]

여기서 보상기 \(C(s)\)는 plant \(G(s)\)와 구분해야 한다.

### 4.1 진상보상기 표준형

\[
C_{lead}(s)
=K_c\frac{1+Ts}{1+\alpha Ts},
\qquad 0<\alpha<1
\]

영점과 극점은 다음과 같다.

\[
z=-\frac{1}{T},
\qquad
p=-\frac{1}{\alpha T}
\]

따라서 진상보상기에서는 극점이 영점보다 원점에서 더 멀리 위치한다.

최대 위상진상은 다음과 같다.

\[
\phi_{max}
=\sin^{-1}\left(
\frac{1-\alpha}{1+\alpha}
\right)
\]

최대 위상진상 주파수는 다음과 같다.

\[
\omega_m
=\frac{1}{T\sqrt{\alpha}}
\]

해당 주파수에서의 크기는 다음과 같다.

\[
\left|C_{lead}(j\omega_m)\right|
=\frac{K_c}{\sqrt{\alpha}}
\]

### 4.2 지상보상기 표준형

\[
C_{lag}(s)
=K_c\frac{1+Ts}{1+\beta Ts},
\qquad \beta>1
\]

영점과 극점은 다음과 같다.

\[
z=-\frac{1}{T},
\qquad
p=-\frac{1}{\beta T}
\]

따라서 지상보상기에서는 극점이 영점보다 원점에 더 가깝다.

지상보상기는 저주파와 고주파의 상대 이득을 조정하여
정상상태 오차 개선에 필요한 저주파 루프이득을 확보한다.

극점과 영점을 교차주파수보다 충분히 낮은 영역에 배치하면
목표 교차주파수 부근의 위상 손실을 제한할 수 있다.

## 5. Fact Anchor 계약

### A01 — `lead_lag_design_objective`

보상기는 plant 자체가 아니라 제어기 전달함수에 극점과 영점을 추가하여
루프 전달함수의 크기와 위상을 변경한다.

설계 목표는 단순 안정화가 아니라 다음 성능의 균형이다.

- 폐루프 안정도
- 위상여유와 이득여유
- 대역폭과 응답속도
- 정상상태 오차
- 제어입력 크기
- 측정노이즈 민감도
- 모델 불확실성에 대한 강인성

### A02 — `lead_lag_lead_pole_zero_geometry`

진상보상기의 표준형에서 \(0<\alpha<1\)이다.

\[
C_{lead}(s)
=K_c\frac{1+Ts}{1+\alpha Ts}
\]

진상보상기의 극점은 영점보다 원점에서 더 멀리 위치한다.

\[
|p|>|z|
\]

이 극점·영점 배치가 관심 주파수 구간에 양의 위상을 추가한다.

### A03 — `lead_lag_lead_maximum_phase_relation`

진상보상기의 최대 위상진상은 \(\alpha\)로 결정된다.

\[
\phi_{max}
=\sin^{-1}\left(
\frac{1-\alpha}{1+\alpha}
\right)
\]

따라서 필요한 최대 위상진상으로부터 다음과 같이 \(\alpha\)를 정할 수 있다.

\[
\alpha
=\frac{1-\sin\phi_{max}}
{1+\sin\phi_{max}}
\]

### A04 — `lead_lag_lead_center_frequency_magnitude`

최대 위상진상이 발생하는 중심주파수는 다음과 같다.

\[
\omega_m
=\frac{1}{T\sqrt{\alpha}}
\]

해당 주파수에서 진상보상기의 크기 증가는 다음과 같다.

\[
\left|
\frac{1+j\omega_mT}
{1+j\omega_m\alpha T}
\right|
=\frac{1}{\sqrt{\alpha}}
\]

따라서 진상보상기는 위상만 추가하는 요소가 아니며
교차주파수도 이동시킨다.

### A05 — `lead_lag_lead_phase_margin_design_sequence`

진상보상기 설계는 일반적으로 다음 순서로 수행한다.

1. 보상 전 루프의 위상여유와 교차주파수를 계산한다.
2. 목표 위상여유와 추가 안전여유를 고려해 필요한 위상진상을 정한다.
3. 필요한 위상진상으로부터 \(\alpha\)를 계산한다.
4. 새로운 교차주파수 후보를 선정한다.
5. \(\omega_m\)을 목표 교차주파수 부근에 배치하여 \(T\)를 정한다.
6. 크기 조건을 만족하도록 \(K_c\)를 조정한다.
7. 보상 후 안정여유와 시간응답을 재검증한다.

### A06 — `lead_lag_lead_bandwidth_noise_effort_tradeoff`

진상보상기는 일반적으로 위상여유와 대역폭을 증가시키고 응답을 빠르게 할 수 있다.

그러나 고주파 이득이 커지면 다음 문제가 발생할 수 있다.

- 측정노이즈 증폭
- 제어입력 증가
- 액추에이터 포화
- 미모델링 고주파 동특성 자극
- 디지털 구현 시 샘플링 제약 증가

따라서 대역폭 증가는 무조건적인 성능 향상이 아니다.

### A07 — `lead_lag_lag_pole_zero_geometry`

지상보상기의 표준형에서 \(\beta>1\)이다.

\[
C_{lag}(s)
=K_c\frac{1+Ts}{1+\beta Ts}
\]

지상보상기의 극점은 영점보다 원점에 더 가깝다.

\[
|p|<|z|
\]

이 배치는 저주파 루프이득과 고주파 루프이득의 비를 조정한다.

### A08 — `lead_lag_lag_steady_state_error_improvement`

정상상태 오차는 시스템 형과 저주파 오차상수에 의해 결정된다.

지상보상기는 저주파 루프이득을 증가시켜
위치·속도·가속도 오차상수를 개선할 수 있다.

다만 적분기를 추가하지 않는 일반적인 지상보상기는
시스템 형을 자동으로 증가시키지 않는다.

따라서 정상상태 오차가 반드시 0이 되는 것은 아니다.

### A09 — `lead_lag_lag_crossover_phase_loss`

지상보상기의 극점과 영점은 목표 교차주파수보다 충분히 낮게 배치하여
교차주파수 부근의 추가 위상지연을 제한한다.

그러나 지상보상기는 항상 음의 위상을 발생시키므로
위상여유가 완전히 보존된다고 가정해서는 안 된다.

설계 후 실제 위상여유를 다시 계산해야 한다.

### A10 — `lead_lag_lag_gain_ratio_error_constant`

정상상태 오차상수를 \(\beta\)배 개선하려면
저주파 루프이득이 목표 비율만큼 증가하도록 설계한다.

이때 단순히 전체 이득만 높이면 교차주파수와 안정여유가 크게 변할 수 있으므로,
지상 극점·영점을 이용해 저주파 이득 개선과 교차주파수 보존을 분리한다.

### A11 — `lead_lag_combined_design`

진상·지상 결합보상기는 다음 두 목표를 함께 만족시키기 위해 사용한다.

- 진상부: 위상여유, 대역폭, 과도응답 개선
- 지상부: 저주파 이득, 정상상태 오차 개선

일반적으로 목표 교차주파수와 안정여유를 먼저 설계한 뒤
정상상태 정확도를 보완하지만,
plant 특성과 요구조건에 따라 반복 설계가 필요하다.

두 보상기의 효과는 독립적이지 않으므로 최종 결합 루프를 다시 검증해야 한다.

### A12 — `lead_lag_root_locus_frequency_consistency`

진상·지상 보상기의 효과는 Bode 선도와 근궤적에서 일관되게 설명할 수 있다.

진상보상기는 근궤적을 원하는 감쇠비와 고유진동수 영역으로 이동시키는 데 사용할 수 있다.

지상보상기는 정상상태 오차 개선을 위해 저주파 이득을 증가시키면서
지배극 위치 변화를 제한하도록 설계할 수 있다.

주파수영역 설계와 근궤적 설계는 서로 다른 물리현상을 의미하는 것이 아니라
동일한 폐루프 특성을 다른 관점에서 평가한다.

### A13 — `lead_lag_plant_robustness_limits`

다음 특성은 보상 가능한 성능을 제한한다.

- 우반평면 영점
- 시간지연
- 불안정극
- 낮은 주파수의 공진모드
- 미모델링 동특성
- 센서 및 액추에이터 대역폭
- 큰 파라미터 불확실성

진상·지상 보상기를 추가했다고 해서
모든 plant를 원하는 성능으로 만들 수 있는 것은 아니다.

### A14 — `lead_lag_implementation_validation`

최종 설계는 다음 항목을 함께 검증해야 한다.

1. 폐루프 극점과 안정도
2. 이득여유와 위상여유
3. 교차주파수와 대역폭
4. 계단응답의 상승시간·오버슈트·정착시간
5. 정상상태 오차
6. 민감도 함수와 상보민감도 함수
7. 제어입력과 액추에이터 포화
8. 고주파 노이즈 증폭
9. 모델 불확실성과 시간지연
10. 연속 보상기의 이산화 오차

## 6. Fatal Wrong Claim 계약

### F01 — `lead_lag_fatal_lead_pole_zero_reversed`

잘못된 주장:

> 진상보상기의 극점은 영점보다 원점에 더 가깝다.

교정:

진상보상기에서는 극점이 영점보다 원점에서 더 멀다.

\[
|p|>|z|
\]

극점이 원점에 더 가까운 구조는 지상보상기의 전형적인 배치다.

### F02 — `lead_lag_fatal_lead_only_changes_phase`

잘못된 주장:

> 진상보상기는 크기에는 영향을 주지 않고 위상만 증가시킨다.

교정:

진상보상기는 관심 주파수에서 양의 위상과 함께 크기도 증가시키므로
이득교차주파수와 대역폭을 변화시킨다.

### F03 — `lead_lag_fatal_lead_always_reduces_bandwidth`

잘못된 주장:

> 진상보상기는 항상 대역폭을 감소시킨다.

교정:

진상보상기는 일반적으로 교차주파수와 대역폭을 증가시키는 방향으로 작용한다.
다만 plant와 이득 설정에 따라 최종 결과를 계산해야 한다.

### F04 — `lead_lag_fatal_lag_always_improves_phase_margin`

잘못된 주장:

> 지상보상기는 위상여유를 항상 증가시킨다.

교정:

지상보상기는 음의 위상을 추가한다.
극점과 영점을 낮은 주파수에 배치하여 위상 손실을 작게 만들 수는 있지만
위상여유 증가가 자동으로 보장되지는 않는다.

### F05 — `lead_lag_fatal_lag_guarantees_zero_error`

잘못된 주장:

> 지상보상기를 추가하면 모든 입력에 대한 정상상태 오차가 0이 된다.

교정:

지상보상기는 저주파 이득과 오차상수를 개선하지만
시스템 형과 입력 종류에 따라 정상상태 오차가 남을 수 있다.

### F06 — `lead_lag_fatal_margins_guarantee_robustness`

잘못된 주장:

> 양의 이득여유와 위상여유만 확보하면 모든 불확실성과 시간지연에 강인하다.

교정:

GM과 PM은 중요한 상대안정도 지표지만
모델 불확실성, 구조화 불확실성, 공진, 시간지연,
민감도 피크를 모두 보장하지는 않는다.

### F07 — `lead_lag_fatal_exact_cancellation_always_safe`

잘못된 주장:

> 불안정극이나 느린 극은 보상기 영점으로 정확히 상쇄하면 항상 안전하다.

교정:

모델 오차 때문에 정확한 상쇄는 현실적으로 보장되지 않는다.
특히 불안정극이나 우반평면 영점의 상쇄는 강인성과 내부안정성을 훼손할 수 있다.

### F08 — `lead_lag_fatal_any_specification_achievable`

잘못된 주장:

> 진상·지상 보상기를 사용하면 모든 plant에서 임의의 안정여유,
> 대역폭 및 정상상태 오차 조건을 동시에 만족시킬 수 있다.

교정:

우반평면 영점, 시간지연, 포화, 센서 노이즈,
미모델링 동특성과 물리적 대역폭이 달성 가능한 성능을 제한한다.

## 7. 모범답안 권장 구조

### O01 — `design_problem_and_performance_requirements`

- 보상기의 필요성
- 안정도·과도응답·정상상태 오차 요구조건
- plant와 compensator의 역할 구분

### O02 — `lead_compensator_principle`

- 진상보상기 전달함수
- 극점·영점 위치
- 최대 위상진상과 중심주파수
- Bode 선도 특성

### O03 — `lead_compensator_design_procedure`

- 기존 위상여유 계산
- 필요 위상진상 산정
- \(\alpha\), \(T\), \(K_c\) 결정
- 새로운 교차주파수 검증

### O04 — `lag_compensator_principle`

- 지상보상기 전달함수
- 극점·영점 위치
- 저주파 이득과 정상상태 오차
- 추가 위상지연

### O05 — `lag_compensator_design_procedure`

- 요구 오차상수 결정
- 필요 이득비 \(\beta\) 산정
- 극점·영점의 저주파 배치
- 교차주파수와 위상여유 재검증

### O06 — `lead_lag_combined_design`

- 진상·지상 결합 목적
- 설계 순서
- 반복 설계 필요성
- 상호작용 검증

### O07 — `performance_tradeoffs_and_limitations`

- 대역폭과 노이즈
- 응답속도와 제어입력
- 정상상태 오차와 안정여유
- 시간지연·우반평면 영점·포화 한계

### O08 — `implementation_and_final_validation`

- 연속 보상기의 디지털 구현
- 샘플링주기와 이산화
- anti-windup 및 출력 제한
- Bode·Nyquist·근궤적·시간응답 교차검증

## 8. 고득점 해제 조건

다음 8개 조건을 모두 만족할 때 최상위 점수대를 허용한다.

1. 진상보상기의 극점·영점 위치를 정확히 설명한다.
2. 최대 위상진상과 중심주파수 관계를 제시한다.
3. 진상보상기 설계 절차에서 교차주파수 이동을 반영한다.
4. 지상보상기의 저주파 이득 개선 원리를 설명한다.
5. 지상보상기가 시스템 형을 자동으로 증가시키지 않음을 설명한다.
6. 진상·지상 결합보상기의 설계 상호작용을 설명한다.
7. 대역폭·노이즈·제어입력·정상상태 오차의 상충관계를 제시한다.
8. 보상 후 안정여유·시간응답·민감도·포화를 종합 검증한다.

## 9. Source Topic Pack 구현 계약

생성할 Source Topic Pack은 다음 5개 파일로 구성한다.

- `README.md`
- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

구현 조건은 다음과 같다.

- Fact Anchor: 정확히 14개
- Fatal Wrong Claim: 정확히 8개
- LLM truth schema: 14개 Anchor ID와 일치
- LLM fatal conditions: 8개 Fatal ID와 일치
- deterministic checks: 비활성화
- deterministic rule list: 빈 배열
- candidate extraction rules: 빈 배열
- recommended outline: 정확히 8개
- high-band unlock conditions: 정확히 8개
- question type: `CALC_DESIGN`
- difficulty: `THEORY_CORE`
- selection importance: `CORE_MUST_PREPARE`
- source/generated Topic ID 일치
- Gemini Topic Pack Review: `pass`
- Gemini issues: `0`

## 10. 범위 제외

본 Topic Pack에서 다음 내용은 중심 범위에서 제외한다.

- H∞ 최적제어의 수학적 유도
- LQR 비용함수와 Riccati 방정식
- Kalman filter 설계
- 비선형 보상기 설계
- 적응제어
- 모델예측제어
- 상세한 디지털 필터 구조
- 다변수 decoupling 설계

다만 구현 한계나 확장 방향으로 간단히 언급할 수 있다.
