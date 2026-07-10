# Bode 선도에 의한 안정여유·대역폭 해석과 주파수응답 설계

## 0. 문서 목적

이 문서는 다음 Topic Pack을 작성하기 위한 사람 검토용 요구사항 원본이다.

- Topic ID: `bode_frequency_response_stability_margin_bandwidth`
- 한글 제목: `Bode 선도에 의한 안정여유·대역폭 해석과 주파수응답 설계`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- Logic Check 방식: `LLM_ONLY`
- 결정론 검사: 비활성화
- candidate extraction rule: 빈 배열
- Fact Anchor 목표 수: 14
- fatal misconception 목표 수: 8
- Model Answer 권장 전개 수: 8
- high-band unlock condition 목표 수: 8

이 문서는 Bode 선도의 단순 작도법만 다루지 않는다.

다음 내용을 하나의 논리 구조로 연결해야 한다.

1. 개루프 주파수응답
2. 크기선도와 위상선도의 구성
3. 이득교차주파수와 위상교차주파수
4. 위상여유와 이득여유
5. 폐루프 대역폭
6. 안정여유와 시간응답의 관계
7. 시간지연과 비최소위상 특성
8. 다중 교차점과 고전적 안정여유의 한계
9. 보상기 설계
10. 현장 검증과 운전 제약

---

## 1. 출제 의도

기술사 답안에서는 Bode 선도를 단순히 주파수에 따른 크기와 위상 그래프로 설명하는 것만으로 부족하다.

고득점 답안은 다음 질문에 답해야 한다.

- 어떤 전달함수의 Bode 선도를 사용하는가?
- 개루프 전달함수와 폐루프 전달함수의 역할은 무엇인가?
- 각 극점과 영점은 기울기와 위상에 어떤 영향을 주는가?
- 이득교차주파수와 위상교차주파수는 어떻게 다른가?
- 위상여유와 이득여유는 어디에서 계산하는가?
- 이득여유의 배수 표현과 dB 표현은 어떻게 변환하는가?
- 폐루프 대역폭은 어떤 기준으로 정의하는가?
- 대역폭과 개루프 이득교차주파수는 언제 유사하고 언제 달라지는가?
- 시간지연과 비최소위상 영점은 안정여유에 어떤 영향을 주는가?
- 다중 교차점이 존재할 때 단일 PM·GM 값만으로 판단해도 되는가?
- 보상기를 적용할 때 응답속도, 안정여유, 잡음과 포화 사이의 trade-off는 무엇인가?
- 실제 설비에서는 모델 오차와 운전점 변화를 어떻게 검증하는가?

---

## 2. 적용 전제와 부호 규약

### 2.1 기본 피드백 구조

기본 설명은 음의 피드백 시스템을 전제로 한다.

개루프 전달함수는 다음과 같이 정의한다.

\[
L(s)=G(s)H(s)
\]

폐루프 기준입력 전달함수는 다음과 같다.

\[
T(s)=\frac{L(s)}{1+L(s)}
\]

감도함수는 다음과 같다.

\[
S(s)=\frac{1}{1+L(s)}
\]

따라서 다음 관계가 성립한다.

\[
S(s)+T(s)=1
\]

폐루프 특성방정식은 다음과 같다.

\[
1+L(s)=0
\]

양의 피드백 구조에서는 특성방정식과 안정 판정 기준이 달라질 수 있으므로, 본 Topic Pack의 기본 수식을 그대로 적용해서는 안 된다.

### 2.2 주파수 단위

기본 각주파수 단위는 `rad/s`이다.

주파수 \(f\)와 각주파수 \(\omega\)의 관계는 다음과 같다.

\[
\omega=2\pi f
\]

\[
f=\frac{\omega}{2\pi}
\]

답안에서 Hz와 rad/s를 혼용할 경우 반드시 변환 관계를 명시해야 한다.

### 2.3 위상 표현

위상은 연속적인 해석을 위해 unwrap된 위상을 기준으로 판단할 수 있다.

표시 범위가 \(-180^\circ\)에서 \(180^\circ\)로 접히는 그래프에서는 위상교차점과 다중 교차점을 잘못 판정할 수 있다.

### 2.4 이득의 부호

고전적 PM·GM 설명은 일반적으로 양의 스칼라 이득과 음의 피드백을 전제로 한다.

음의 이득 또는 피드백 부호 변경은 추가적인 \(180^\circ\) 위상 변화를 유발하므로 별도 해석이 필요하다.

---

## 3. 필수 용어

다음 용어를 일관되게 사용한다.

- 개루프 전달함수: `open-loop transfer function`
- 루프 전달함수: `loop transfer function`
- 폐루프 전달함수: `closed-loop transfer function`
- 크기선도: `magnitude plot`
- 위상선도: `phase plot`
- 절점주파수: `corner frequency`, `break frequency`
- 이득교차주파수: `gain crossover frequency`
- 위상교차주파수: `phase crossover frequency`
- 위상여유: `phase margin`
- 이득여유: `gain margin`
- 대역폭: `bandwidth`
- 공진피크: `resonant peak`
- 감도함수: `sensitivity function`
- 상보감도함수: `complementary sensitivity function`
- 비최소위상 영점: `non-minimum-phase zero`
- 시간지연: `time delay`, `dead time`
- 위상 펼침: `phase unwrap`
- 강인성: `robustness`
- 교차주파수: `crossover frequency`

---

## 4. 필수 수식

### 4.1 Bode 크기

\[
M_{\mathrm{dB}}(\omega)
=
20\log_{10}|L(j\omega)|
\]

전력비가 아니라 전달함수의 진폭비를 다루므로 일반적으로 \(20\log_{10}\)을 사용한다.

### 4.2 이득교차주파수

\[
|L(j\omega_{gc})|=1
\]

동일한 dB 표현은 다음과 같다.

\[
20\log_{10}|L(j\omega_{gc})|=0\ \mathrm{dB}
\]

### 4.3 위상여유

\[
PM
=
180^\circ+\angle L(j\omega_{gc})
\]

여기서 \(\angle L(j\omega_{gc})\)는 일반적으로 음의 위상값이다.

예를 들어 다음과 같다.

\[
\angle L(j\omega_{gc})=-135^\circ
\]

이면,

\[
PM=180^\circ-135^\circ=45^\circ
\]

이다.

### 4.4 위상교차주파수

\[
\angle L(j\omega_{pc})=-180^\circ
\]

보다 일반적으로 위상은 다음 조건을 만족하는 교차점을 포함할 수 있다.

\[
\angle L(j\omega)=-(2k+1)180^\circ
\]

다중 교차점이 존재하면 모든 관련 교차점을 확인해야 한다.

### 4.5 이득여유

선형 배수 표현은 다음과 같다.

\[
GM
=
\frac{1}{|L(j\omega_{pc})|}
\]

dB 표현은 다음과 같다.

\[
GM_{\mathrm{dB}}
=
20\log_{10}(GM)
\]

따라서 다음과 같이 쓸 수 있다.

\[
GM_{\mathrm{dB}}
=
-20\log_{10}|L(j\omega_{pc})|
\]

예를 들어 위상교차주파수에서 루프 크기가 \(-10\ \mathrm{dB}\)이면 이득여유는 \(+10\ \mathrm{dB}\)이다.

### 4.6 폐루프 대역폭

일반적인 저역통과형 폐루프 시스템에서는 저주파 이득을 기준으로 다음 조건을 만족하는 주파수를 대역폭으로 정의한다.

\[
|T(j\omega_{BW})|
=
\frac{|T(0)|}{\sqrt{2}}
\]

dB 상대값으로는 다음과 같다.

\[
20\log_{10}
\left(
\frac{|T(j\omega_{BW})|}{|T(0)|}
\right)
=
-3.0103\ \mathrm{dB}
\]

대역폭은 절대적인 \(0\ \mathrm{dB}\) 기준이 아니라 저주파 폐루프 이득에 대한 상대값으로 정의해야 한다.

### 4.7 시간지연

시간지연 요소는 다음과 같다.

\[
e^{-s\tau}
\]

주파수응답의 크기는 다음과 같다.

\[
|e^{-j\omega\tau}|=1
\]

위상은 다음과 같다.

\[
\angle e^{-j\omega\tau}
=
-\omega\tau\ \mathrm{rad}
\]

degree 표현은 다음과 같다.

\[
\angle e^{-j\omega\tau}
=
-\omega\tau\frac{180^\circ}{\pi}
\]

시간지연은 크기선도를 직접 바꾸지 않지만 위상지연을 증가시켜 PM과 안정성을 악화시킬 수 있다.

---

## 5. Bode 선도 구성 규칙

### 5.1 상수 이득

양의 상수 이득 \(K\)는 크기선도를 다음만큼 평행 이동시킨다.

\[
20\log_{10}K
\]

양의 \(K\)는 위상선도를 변경하지 않는다.

### 5.2 원점 극점

\[
\frac{1}{s}
\]

는 다음 특성을 갖는다.

- 크기 기울기: \(-20\ \mathrm{dB/dec}\)
- 위상: \(-90^\circ\)

원점 극점이 \(n\)개이면 다음과 같다.

- 크기 기울기: \(-20n\ \mathrm{dB/dec}\)
- 위상: \(-90n^\circ\)

### 5.3 원점 영점

\[
s
\]

는 다음 특성을 갖는다.

- 크기 기울기: \(+20\ \mathrm{dB/dec}\)
- 위상: \(+90^\circ\)

### 5.4 1차 좌반평면 영점

\[
1+\frac{s}{\omega_z}
\]

는 절점 이후 크기 기울기에 \(+20\ \mathrm{dB/dec}\)를 추가한다.

위상은 근사적으로 다음 구간에서 변한다.

- \(0.1\omega_z\) 이하: 약 \(0^\circ\)
- \(\omega_z\): 약 \(+45^\circ\)
- \(10\omega_z\) 이상: 약 \(+90^\circ\)

### 5.5 1차 좌반평면 극점

\[
\frac{1}{1+s/\omega_p}
\]

는 절점 이후 크기 기울기에 \(-20\ \mathrm{dB/dec}\)를 추가한다.

위상은 근사적으로 다음 구간에서 변한다.

- \(0.1\omega_p\) 이하: 약 \(0^\circ\)
- \(\omega_p\): 약 \(-45^\circ\)
- \(10\omega_p\) 이상: 약 \(-90^\circ\)

### 5.6 우반평면 영점

우반평면 영점은 대응하는 좌반평면 영점과 크기응답이 같을 수 있지만 위상 기여 방향은 반대이다.

따라서 비최소위상 영점은 크기선도만 보면 식별하기 어렵고, 추가 위상지연과 성능 한계를 유발한다.

### 5.7 2차 극점과 영점

2차 요소는 감쇠비에 따라 절점 부근의 정확한 크기와 위상응답이 달라진다.

낮은 감쇠비의 2차 극점은 공진피크를 유발할 수 있으므로 단순한 직선 근사만으로 응답 최대값을 판단하면 안 된다.

### 5.8 직선 근사와 정확 응답

점근선 작도는 구조 파악에 유용하지만 다음 경우 정확 응답 계산이 필요하다.

- 절점 부근
- 감쇠비가 낮은 2차 요소
- 서로 가까운 극점과 영점
- pole-zero cancellation 근처
- 다중 crossover
- 시간지연이 큰 시스템
- 안정여유가 작은 시스템

---

## 6. Fact Anchor 요구사항

### A01. 개루프와 폐루프 전달함수의 역할

- PM과 GM은 기본적으로 루프 전달함수 \(L(s)=G(s)H(s)\)의 주파수응답에서 구한다.
- 폐루프 대역폭은 \(T(s)=L(s)/(1+L(s))\)에서 평가한다.
- 개루프와 폐루프의 평가 대상을 혼동하지 않는다.
- 폐루프 안정성은 \(1+L(s)=0\)의 근과 관련된다.

### A02. 로그 주파수축과 dB 표현

- Bode 선도는 로그 주파수축을 사용한다.
- 진폭비는 \(20\log_{10}|L(j\omega)|\)로 변환한다.
- 전달함수 곱은 dB 크기의 합과 위상의 합으로 표현할 수 있다.
- 단위와 기준값을 명확히 표시한다.

### A03. 극점·영점의 크기 기울기

- 1차 좌반평면 영점은 절점 이후 \(+20\ \mathrm{dB/dec}\)를 추가한다.
- 1차 좌반평면 극점은 절점 이후 \(-20\ \mathrm{dB/dec}\)를 추가한다.
- 중복 차수에 따라 기울기 변화가 누적된다.
- 원점 극점과 원점 영점은 전체 주파수 구간에서 기울기에 영향을 준다.

### A04. 위상 기여와 비최소위상 요소

- 좌반평면 영점은 양의 위상을 기여한다.
- 좌반평면 극점은 음의 위상을 기여한다.
- 우반평면 영점은 동일한 크기응답을 가질 수 있지만 반대 방향의 위상을 기여한다.
- magnitude만으로 최소위상과 비최소위상 시스템을 항상 구분할 수는 없다.

### A05. 양의 이득 변경의 영향

- 양의 이득 \(K\) 증가는 크기선도를 \(20\log_{10}K\)만큼 이동시킨다.
- 양의 상수 이득은 위상선도 자체를 바꾸지 않는다.
- 이득 변경은 \(\omega_{gc}\), PM, GM과 폐루프 응답을 변경할 수 있다.
- 이득 증가가 항상 안정성과 강인성을 개선하는 것은 아니다.

### A06. 두 교차주파수의 정의

- \(\omega_{gc}\)는 \(|L(j\omega)|=1\)인 주파수이다.
- \(\omega_{pc}\)는 위상이 \(-180^\circ\) 계열에 도달하는 주파수이다.
- 두 주파수는 서로 다른 조건으로 정의된다.
- 두 주파수가 우연히 같을 수는 있지만 일반적으로 같다고 가정하면 안 된다.

### A07. 위상여유 계산

- 위상여유는 \(\omega_{gc}\)에서 계산한다.
- 부호가 포함된 위상을 사용할 때 \(PM=180^\circ+\angle L(j\omega_{gc})\)이다.
- PM은 추가 위상지연에 대한 고전적 여유를 나타낸다.
- crossover가 여러 개이면 단일 교차점만 임의로 선택하면 안 된다.

### A08. 이득여유 계산

- 이득여유는 \(\omega_{pc}\)에서 계산한다.
- 선형 배수는 \(GM=1/|L(j\omega_{pc})|\)이다.
- dB 값은 \(GM_{\mathrm{dB}}=-20\log_{10}|L(j\omega_{pc})|\)이다.
- 배수와 dB 표현의 부호 및 기준을 일관되게 사용한다.

### A09. 교차점이 없거나 여러 개인 경우

- 0 dB 교차가 없으면 고전적 PM이 정의되지 않을 수 있다.
- \(-180^\circ\) 위상교차가 없으면 고전적 GM이 무한대로 표현될 수 있다.
- 다중 교차점에서는 모든 관련 교차점을 확인한다.
- 개루프 불안정 극점, 다중 crossover 또는 복잡한 위상 궤적에서는 Nyquist 해석을 병행한다.

### A10. 폐루프 대역폭

- 폐루프 대역폭은 일반적으로 \(T(s)\)의 저주파 이득 대비 \(-3\ \mathrm{dB}\) 지점이다.
- \(\omega_{BW}\)와 \(\omega_{gc}\)는 서로 다른 전달함수에서 정의된다.
- 잘 거동하는 단일루프 시스템에서는 두 값이 유사할 수 있으나 항등적으로 같지 않다.
- 공진피크, 비단조 응답 또는 비저역통과 특성에서는 대역폭 정의를 명시해야 한다.

### A11. 안정여유와 시간응답의 관계

- PM 증가가 일반적으로 감쇠 증가와 overshoot 감소 경향을 보일 수 있다.
- 대역폭 증가가 일반적으로 응답속도 향상 경향을 보일 수 있다.
- 이러한 관계는 dominant second-order와 유사한 조건에서 사용하는 근사적 설계 지침이다.
- 고차계, 영점, 지연과 비최소위상 특성이 있으면 정확한 일대일 관계가 성립하지 않는다.

### A12. 시간지연과 비최소위상 제한

- 순수 시간지연은 크기 \(1\)과 위상 \(-\omega\tau\)를 갖는다.
- 시간지연은 주파수가 증가할수록 위상여유를 감소시킬 수 있다.
- 우반평면 영점은 추가 위상지연과 역응답 가능성을 유발한다.
- 대역폭을 무리하게 높이면 안정성과 강인성이 악화될 수 있다.

### A13. 감도·강인성·잡음 trade-off

- 저주파에서 큰 루프 이득은 추종오차와 외란 감쇠 개선에 유리할 수 있다.
- 고주파에서 큰 루프 이득은 센서 잡음 전달과 미모델 동특성 영향을 키울 수 있다.
- \(S=1/(1+L)\)와 \(T=L/(1+L)\)를 이용해 성능과 강인성의 trade-off를 설명한다.
- 안정여유는 단순한 안정 여부뿐 아니라 모델 불확실성에 대한 여유로 해석한다.

### A14. 보상기 설계와 현장 검증

- lead 보상은 목표 crossover 부근에서 위상여유와 응답속도를 개선하는 데 사용할 수 있다.
- lag 보상은 저주파 이득과 정상상태 성능을 높이되 crossover 영향을 제한하도록 설계할 수 있다.
- PID는 P·I·D 각 요소의 이득과 위상 영향을 함께 고려한다.
- 현장 적용 전 운전점, 시간지연, 포화, rate limit, deadband, 잡음과 모델 오차를 검증한다.

---

## 7. Truth Schema 요구사항

Logic Check의 `truth_schema`는 다음 14개 anchor와 일대일로 대응해야 한다.

1. `open_loop_closed_loop_roles`
2. `log_frequency_and_decibel`
3. `pole_zero_magnitude_slopes`
4. `phase_contribution_nonminimum_phase`
5. `positive_gain_shift`
6. `gain_phase_crossover_frequencies`
7. `phase_margin_calculation`
8. `gain_margin_calculation`
9. `multiple_or_missing_crossovers`
10. `closed_loop_bandwidth`
11. `margin_transient_response_approximation`
12. `delay_and_nonminimum_phase_limits`
13. `sensitivity_robustness_noise_tradeoff`
14. `compensator_and_field_validation`

각 truth 항목은 단순 키워드가 아니라 다음을 포함해야 한다.

- 무엇을 평가하는가
- 어느 전달함수에서 평가하는가
- 어떤 조건에서 성립하는가
- 어떤 예외가 존재하는가
- 잘못 적용할 경우 어떤 판단 오류가 발생하는가

---

## 8. 치명적 오개념 요구사항

### F01. `margins_from_closed_loop_bode`

잘못된 주장:

- PM과 GM을 폐루프 전달함수 \(T(s)\)의 Bode 선도에서 직접 구한다고 단정한다.

정확한 기준:

- 고전적 PM과 GM은 루프 전달함수 \(L(s)\)에서 구한다.
- 폐루프 \(T(s)\)는 대역폭, 공진과 폐루프 응답 평가에 사용한다.

### F02. `crossover_frequencies_are_same`

잘못된 주장:

- gain crossover frequency와 phase crossover frequency는 동일한 주파수라고 설명한다.

정확한 기준:

- \(\omega_{gc}\)와 \(\omega_{pc}\)는 서로 다른 조건으로 정의된다.
- 특정 시스템에서 우연히 일치할 수 있으나 일반 규칙이 아니다.

### F03. `phase_margin_sign_error`

잘못된 주장:

- 부호가 포함된 음의 위상값에 대해 \(PM=180^\circ-\angle L(j\omega_{gc})\)를 그대로 적용한다.

정확한 기준:

\[
PM=180^\circ+\angle L(j\omega_{gc})
\]

- 위상 lag의 절대값을 별도로 정의했다면 표현이 달라질 수 있으므로 부호 규약을 명시한다.

### F04. `gain_margin_db_sign_error`

잘못된 주장:

- \(GM_{\mathrm{dB}}=20\log_{10}|L(j\omega_{pc})|\)라고 하여 부호를 반대로 계산한다.

정확한 기준:

\[
GM_{\mathrm{dB}}
=
-20\log_{10}|L(j\omega_{pc})|
\]

### F05. `bandwidth_always_equals_gain_crossover`

잘못된 주장:

- 폐루프 대역폭과 개루프 이득교차주파수가 항상 동일하다고 단정한다.

정확한 기준:

- 두 값은 서로 다른 전달함수와 기준으로 정의된다.
- 특정 조건에서 근사적으로 유사할 수 있다.

### F06. `phase_margin_damping_exact_universal`

잘못된 주장:

- PM과 damping ratio 사이에 모든 시스템에 적용되는 정확한 일대일 공식이 있다고 단정한다.

정확한 기준:

- dominant second-order와 유사한 제한 조건에서 근사 관계 또는 설계 경향으로 사용한다.
- 고차 극점, 영점, 지연과 비최소위상 특성에 따라 관계가 달라진다.

### F07. `delay_has_no_stability_effect`

잘못된 주장:

- 순수 시간지연은 크기응답을 바꾸지 않으므로 안정성에도 영향을 주지 않는다고 설명한다.

정확한 기준:

- 시간지연은 \(-\omega\tau\)의 위상지연을 추가한다.
- PM을 감소시키고 폐루프 불안정을 유발할 수 있다.

### F08. `positive_margins_always_guarantee_stability`

잘못된 주장:

- 양의 PM과 GM이 표시되면 개루프 불안정 극점, 다중 crossover, 비최소위상 특성과 관계없이 항상 안정하다고 단정한다.

정확한 기준:

- 고전적 margin의 단순 해석에는 전제가 있다.
- 복잡한 경우 전체 Nyquist 조건, 폐루프 극점 또는 추가적인 강인성 검증이 필요하다.

---

## 9. Fatal Condition 판정 주의사항

LLM은 다음을 직접적인 치명적 오개념과 단순 누락으로 구분해야 한다.

### 9.1 fatal로 판단할 수 있는 경우

- 잘못된 공식을 명시적으로 제시한다.
- 서로 다른 crossover를 같다고 명시한다.
- 개루프와 폐루프의 평가 대상을 반대로 단정한다.
- 시간지연이 안정성에 영향을 주지 않는다고 단정한다.
- 근사 관계를 보편적인 정확식으로 단정한다.
- 복잡한 시스템에서도 양의 margin만으로 안정이 보장된다고 단정한다.

### 9.2 단순 누락으로 판단해야 하는 경우

- bandwidth 설명이 부족하다.
- multiple crossover를 언급하지 않았다.
- phase unwrap을 언급하지 않았다.
- 감도함수를 사용하지 않았다.
- lead와 lag 중 하나만 설명했다.
- 현장 검증 항목이 부족하다.

누락은 감점 요소가 될 수 있지만, 반대 주장이 없는 한 자동 fatal로 처리하지 않는다.

### 9.3 안전한 표현

다음과 같은 조건부 표현은 fatal이 아니다.

- “일반적인 단일 교차 시스템에서는”
- “dominant second-order 근사 조건에서”
- “근사적으로 \(\omega_{BW}\)와 \(\omega_{gc}\)가 유사할 수 있다.”
- “고전적 안정여유 기준으로”
- “개루프 불안정 극점이 없고 단일 crossover라는 조건에서”
- “정확한 안정성은 Nyquist 또는 폐루프 극점으로 확인한다.”

---

## 10. Model Answer 권장 전개

### M01. 배경과 설계 목적

- Bode 선도가 주파수별 크기와 위상을 분리해 표현하는 목적을 설명한다.
- 안정성, 응답속도, 외란 억제와 잡음 영향을 함께 평가할 수 있음을 제시한다.
- 단순 작도가 아니라 안정여유와 폐루프 성능 설계가 목적임을 밝힌다.

### M02. 기본 전달함수와 Bode 구성

- \(L(s)=G(s)H(s)\), \(T(s)=L(s)/(1+L(s))\)를 제시한다.
- 극점·영점별 크기 기울기와 위상 기여를 설명한다.
- 상수 이득, 원점 요소, 1차 요소와 2차 요소를 구분한다.
- 정확 응답과 직선 근사의 차이를 설명한다.

### M03. 이득교차와 위상교차

- \(\omega_{gc}\)와 \(\omega_{pc}\)의 정의를 구분한다.
- 0 dB 교차와 \(-180^\circ\) 교차를 각각 표시한다.
- 교차점 부재 또는 다중 교차 시 처리 원칙을 설명한다.

### M04. 위상여유와 이득여유

- PM과 GM의 계산식을 제시한다.
- GM의 선형 배수와 dB 표현을 변환한다.
- 부호 규약과 위상 unwrap을 설명한다.
- 양의 margin의 의미와 적용 전제를 설명한다.

### M05. 폐루프 대역폭과 시간응답

- \(T(s)\)의 저주파 이득 대비 \(-3\ \mathrm{dB}\) 대역폭을 정의한다.
- \(\omega_{BW}\)와 \(\omega_{gc}\)를 구분한다.
- 대역폭, 상승시간, PM, damping과 overshoot의 관계를 조건부로 설명한다.
- 공진피크와 고차계 영향을 고려한다.

### M06. 특수 조건과 적용 한계

- 시간지연의 위상 영향을 설명한다.
- 우반평면 영점의 비최소위상 특성을 설명한다.
- 다중 crossover와 개루프 불안정 극점의 경우 Nyquist 검증이 필요함을 제시한다.
- 단순 PM·GM 해석의 한계를 설명한다.

### M07. 보상기 설계

- 목표 crossover와 PM을 먼저 설정한다.
- lead 보상으로 위상여유와 대역폭을 조정한다.
- lag 보상으로 저주파 이득과 정상상태 성능을 조정한다.
- PID의 P·I·D 영향을 Bode 관점에서 설명한다.
- 설계 후 실제 \(L(s)\), \(T(s)\), \(S(s)\)를 재검증한다.

### M08. 현장 적용과 결론

- 운전점별 모델을 확인한다.
- 공정 시간지연과 샘플링 지연을 포함한다.
- actuator 포화, rate limit와 deadband를 확인한다.
- 센서 잡음과 고주파 미모델 동특성을 검토한다.
- 목표 margin과 bandwidth에 여유를 두고 단계적으로 적용한다.
- 적용 전후 추종오차, overshoot, 정착시간, 조작량과 안정성을 비교한다.

---

## 11. 고득점 판단 조건

다음 8개 조건을 모두 `high_band_unlock_conditions`에 반영한다.

1. 개루프 \(L(s)\)와 폐루프 \(T(s)\)의 평가 목적을 정확히 구분한다.
2. 극점·영점별 크기 기울기와 위상 기여를 합성한다.
3. \(\omega_{gc}\), \(\omega_{pc}\), PM과 GM을 정확히 정의하고 계산한다.
4. GM의 배수와 dB 표현을 일관된 부호로 변환한다.
5. 폐루프 \(-3\ \mathrm{dB}\) bandwidth와 개루프 crossover의 근사 관계 및 한계를 설명한다.
6. 안정여유를 damping, overshoot와 응답속도에 조건부로 연결한다.
7. 시간지연, 비최소위상 영점, 다중 crossover와 phase unwrap의 영향을 검증한다.
8. lead·lag·PID 보상과 현장 운전점, 포화, 잡음 및 모델 오차를 함께 검토한다.

---

## 12. 문제 예시

Model Answer의 `expected_question_patterns`에는 다음 유형을 포함한다.

1. Bode 선도의 원리와 작성 방법을 설명하고 안정여유를 구하시오.
2. 주어진 개루프 전달함수의 Bode 선도에서 위상여유와 이득여유를 계산하시오.
3. 이득교차주파수와 위상교차주파수의 차이를 설명하시오.
4. 폐루프 대역폭과 개루프 이득교차주파수의 관계를 설명하시오.
5. Bode 선도를 이용하여 목표 위상여유를 만족하는 제어기 이득을 설계하시오.
6. lead 또는 lag 보상기를 이용한 주파수응답 설계 절차를 설명하시오.
7. 시간지연이 위상여유와 폐루프 안정성에 미치는 영향을 설명하시오.
8. 다중 crossover가 있는 시스템에서 고전적 PM·GM 판정의 한계를 설명하시오.

---

## 13. Routing Alias 요구사항

다음 표현을 routing alias 후보로 사용한다.

- Bode
- Bode plot
- Bode diagram
- 보드선도
- 보드 선도
- 주파수응답
- frequency response
- magnitude plot
- phase plot
- 이득교차주파수
- gain crossover frequency
- phase crossover frequency
- 위상교차주파수
- 위상여유
- phase margin
- 이득여유
- gain margin
- 안정여유
- stability margin
- 대역폭
- bandwidth
- 0 dB crossover
- -180 degree crossover
- lead compensation
- lag compensation
- phase lead
- phase lag

일반 단어인 다음 표현만으로 강한 routing을 수행하지 않는다.

- 안정성
- 응답
- 이득
- 위상
- 주파수
- 제어기
- 설계
- 여유
- 속도

---

## 14. Routing Field Point 요구사항

다음 의미 연결점을 포함한다.

- 개루프 크기선도에서 0 dB 교차를 확인한다.
- 개루프 위상선도에서 \(-180^\circ\) 교차를 확인한다.
- PM과 GM을 계산한다.
- 배수와 dB 이득여유를 변환한다.
- 폐루프 \(-3\ \mathrm{dB}\) 대역폭을 확인한다.
- 안정여유와 overshoot 및 damping의 관계를 조건부로 설명한다.
- 시간지연의 \(-\omega\tau\) 위상을 반영한다.
- 비최소위상 영점의 위상 손실을 확인한다.
- multiple crossover와 phase unwrap을 검토한다.
- lead·lag·PID 보상기를 적용한다.
- 저주파 외란 억제와 고주파 잡음의 trade-off를 검토한다.
- 운전점, 포화와 모델 오차를 확인한다.

---

## 15. Source Topic Pack 작성 계약

### 15.1 README.md

다음을 명시한다.

- Topic 목적
- 이론 범위
- 14개 Fact Anchor
- 8개 fatal misconception
- LLM-only 판단 정책
- 개루프와 폐루프 구분
- 교차주파수 구분
- bandwidth 정의
- 특수 조건
- 검증 명령
- 복사 오염 방지 원칙

### 15.2 fact_anchor.json

다음 필드를 기존 최신 Topic Pack schema에 맞춰 작성한다.

- `schema_version`
- `topic_id`
- `title_ko`
- `anchors`
- `core_facts`
- `fatal_wrong_claims`
- `safe_expressions`
- `regex_patterns`
- `revision_notes`

계약:

- anchors: 정확히 14개
- fatal_wrong_claims: 정확히 8개
- 모든 anchor ID는 본 문서 A01~A14와 대응
- 모든 fatal ID는 본 문서 F01~F08과 대응
- 다른 Topic Pack의 고유 수식이나 용어를 남기지 않음

### 15.3 logic_check.json

계약:

- deterministic check 비활성화
- deterministic fatal check 빈 배열
- deterministic major check 빈 배열
- candidate rules 빈 배열
- key terms는 Bode 전용 표현으로 구성
- truth_schema 정확히 14개
- fatal_conditions 정확히 8개
- false positive caution 포함
- safe condition 포함
- LLM-only source policy 명시

### 15.4 model_answer.json

계약:

- `question_type`: `CALC_DESIGN`
- recommended outline: 정확히 8개
- high-score point: 정확히 8개
- expected question pattern: 최소 5개
- common missing point: 최소 8개
- routing alias와 field point를 구분
- Bode 전용 내용만 사용
- 현장 적용 항목 포함

### 15.5 topic_importance.json

계약:

- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `question_type`: `CALC_DESIGN`
- high-band unlock condition: 정확히 8개
- note는 Bode 주파수응답 설계 내용으로 작성
- revision note에 다른 Topic 이름을 잘못 남기지 않음

---

## 16. Logic Check LLM 판정 계약

### 16.1 입력 범위

LLM은 다음 내용을 함께 검토한다.

- 문제
- 사용자 답안
- 선택된 Topic ID
- truth schema
- fatal conditions
- safe expressions
- false-positive cautions

### 16.2 출력 원칙

- 직접적인 반대 주장만 fatal 후보로 판정한다.
- 단순 누락은 fatal로 판정하지 않는다.
- 수식의 부호와 평가 주파수를 함께 확인한다.
- 개루프와 폐루프 전달함수를 구분한다.
- 조건부 근사 표현을 허용한다.
- 복수 교차점과 특수 조건을 고려한다.
- 근거 문장을 답안에서 직접 연결한다.
- 자신 없는 경우 과도한 fatal 판정을 하지 않는다.

### 16.3 candidate extraction

- deterministic candidate rule은 사용하지 않는다.
- candidate rule은 빈 배열로 유지한다.
- key term fallback은 routing 보조 용도로만 사용한다.
- 단일 일반 단어만으로 Topic을 확정하지 않는다.
- Bode, margin, crossover, bandwidth 등 복수 신호를 함께 사용한다.

---

## 17. 다른 Topic과의 경계

### 17.1 Nyquist Topic과의 경계

Bode Topic은 PM, GM, crossover와 bandwidth를 중심으로 한다.

Nyquist Topic의 다음 요소를 중심 내용으로 복사하지 않는다.

- contour mapping
- encirclement count
- Nyquist 경로의 방향
- 원점을 우회하는 contour
- \(N\), \(Z\), \(P\) 계수식

단, 복잡한 crossover에서 Nyquist 검증이 필요하다는 적용 한계는 언급할 수 있다.

### 17.2 Routh-Hurwitz Topic과의 경계

Bode Topic은 주파수응답 기반 해석이다.

다음 내용을 중심으로 전개하지 않는다.

- Routh 배열
- 첫 열 부호변화
- 영행
- 0 선두항 처리
- 계수의 부호 조건

### 17.3 근궤적 Topic과의 경계

Bode Topic은 주파수축에서 크기와 위상을 해석한다.

다음 근궤적 작도 규칙을 복사하지 않는다.

- 실수축 구간 판정
- 점근선 중심
- 점근선 각도
- 이탈점과 진입점
- 출발각과 도착각

### 17.4 2차 시스템 주파수응답 Topic과의 경계

공진주파수와 공진피크를 설명할 수 있으나, 본 Topic의 중심은 다음이다.

- loop transfer function
- crossover
- PM과 GM
- closed-loop bandwidth
- 보상기 설계
- robustness

PM과 damping ratio의 관계를 모든 시스템에 적용되는 정확식으로 만들지 않는다.

### 17.5 PID Topic과의 경계

PID 각 항의 일반적인 시간응답 효과보다 다음을 중심으로 한다.

- 주파수별 이득과 위상 기여
- crossover 이동
- PM 변화
- bandwidth 변화
- 고주파 잡음과 미분필터
- 저주파 적분 이득
- 보상 전후 margin 비교

---

## 18. Cross-topic 복사 오염 방지 검사

Source Pack과 generated bank에서 다음 잘못된 잔여 문구를 검사한다.

- Bode Topic에 Routh 배열 설명이 남아 있지 않은가?
- Bode Topic에 Nyquist 선회 횟수 계산이 남아 있지 않은가?
- Bode Topic에 근궤적 실축 홀수 규칙이 남아 있지 않은가?
- Bode Topic에 이탈점 계산이 남아 있지 않은가?
- Bode Topic에 PM과 damping ratio의 보편적 정확식이 남아 있지 않은가?
- revision note에 Routh, Nyquist 또는 root-locus 내용을 재작성했다고 잘못 기록하지 않았는가?
- title과 Topic ID가 모든 source/generated 파일에서 일치하는가?
- high-band 조건이 Bode 전용 내용인가?
- fatal condition이 Bode 전용 오개념인가?

---

## 19. 현장 적용 요구사항

다음 항목을 model answer와 field point에 반영한다.

### 19.1 운전점

- 공정 이득과 시정수는 운전점에 따라 달라질 수 있다.
- 단일 운전점 모델만으로 margin을 확정하지 않는다.
- 최소·정상·최대 부하 조건을 비교한다.

### 19.2 시간지연

- 계측 지연
- 통신 지연
- 계산 지연
- 샘플링과 zero-order hold
- actuator 응답지연
- 공정 dead time

을 검토한다.

### 19.3 비선형성

- 포화
- rate limit
- deadband
- hysteresis
- stiction

은 선형 Bode 해석만으로 충분히 표현되지 않을 수 있다.

### 19.4 잡음과 필터

- 대역폭 증가는 고주파 센서 잡음 영향을 키울 수 있다.
- 미분 동작은 고주파 잡음을 증폭할 수 있다.
- derivative filter와 measurement filter의 위상지연을 함께 검토한다.

### 19.5 모델 불확실성

- 고주파 미모델 모드
- 공진 모드
- parameter variation
- delay uncertainty
- sensor/actuator dynamics

를 검토한다.

### 19.6 단계적 적용

- simulation
- software-in-the-loop
- hardware-in-the-loop
- 제한된 운전조건 시험
- 단계별 gain 적용
- fallback parameter 확보

순으로 적용할 수 있다.

---

## 20. 답안 평가 기준

### 20.1 기본 점수 요소

- Bode 선도의 정의
- 크기와 위상 표현
- 극점·영점 기여
- crossover 정의
- PM과 GM 계산
- bandwidth 정의

### 20.2 중간 점수 요소

- GM의 배수/dB 변환
- 개루프와 폐루프 구분
- margin과 시간응답의 조건부 관계
- 시간지연 영향
- 보상기 적용

### 20.3 고득점 요소

- multiple crossover
- phase unwrap
- 개루프 불안정 극점에 대한 한계
- 비최소위상 영점
- sensitivity와 complementary sensitivity
- robustness와 noise trade-off
- 현장 운전점과 비선형성
- 단계적 검증과 적용 전후 성능 비교

---

## 21. 작성 금지 사항

다음 방식으로 작성하지 않는다.

- 정의만 나열하고 수식이 없음
- 수식만 나열하고 평가 대상이 없음
- PM과 GM의 평가 주파수를 바꿈
- 개루프 margin과 폐루프 bandwidth를 혼동함
- dB 부호를 확인하지 않음
- Hz와 rad/s를 혼용함
- PM과 damping ratio를 보편적인 정확식으로 단정함
- 시간지연의 위상 효과를 누락함
- 양의 margin만으로 모든 시스템의 안정성을 보장함
- 보상기의 장점만 쓰고 trade-off를 누락함
- 현장 모델 오차와 포화를 무시함
- 다른 Topic Pack의 revision note를 복사함

---

## 22. 검증 시나리오

### 22.1 정상 답안

다음 내용을 정확히 포함하는 답안은 fatal finding이 없어야 한다.

- \(L(s)\)와 \(T(s)\) 구분
- \(\omega_{gc}\)와 \(\omega_{pc}\) 구분
- PM과 GM 공식
- 폐루프 bandwidth
- 시간지연 위상
- 조건부 margin 해석
- 보상기와 현장 검증

### 22.2 치명적 오개념 답안

각 fatal misconception을 하나씩 명시한 답안에서 해당 fatal ID가 검출되어야 한다.

한 답안에 모든 오개념을 넣지 않고, 오개념별 독립 회귀 테스트를 우선한다.

### 22.3 안전한 조건부 답안

다음 표현은 fatal로 검출되지 않아야 한다.

- “일반적인 단일 crossover 조건에서”
- “근사적으로 bandwidth와 gain crossover가 유사할 수 있다.”
- “dominant second-order 조건에서 PM과 damping이 관련된다.”
- “정확한 안정성은 Nyquist와 폐루프 극점으로 검증한다.”

### 22.4 단순 누락 답안

다음 누락은 품질 감점이 될 수 있지만 fatal이 아니어야 한다.

- sensitivity 함수 누락
- multiple crossover 누락
- phase unwrap 누락
- 현장 적용 누락

---

## 23. 최종 인수 기준

Source Topic Pack 작성 후 다음 조건을 모두 만족해야 한다.

### 23.1 파일

- 요구사항 시트 1개
- README 1개
- fact_anchor.json 1개
- logic_check.json 1개
- model_answer.json 1개
- topic_importance.json 1개

### 23.2 구조

- Fact Anchor 14개
- Truth Schema 14개
- Fatal Condition 8개
- Model Answer 권장 전개 8개
- High-band Unlock Condition 8개
- deterministic checks 비활성화
- candidate rules 빈 배열

### 23.3 의미

- PM과 GM은 개루프 \(L(s)\)에서 계산
- bandwidth는 폐루프 \(T(s)\)에서 계산
- crossover 2종 구분
- GM dB 부호 정확
- 시간지연 위상 정확
- PM-damping 관계를 조건부로 표현
- multiple crossover와 특수 조건 반영
- 다른 Topic 내용 오염 없음

### 23.4 Repository

- source validator PASS
- generated build PASS
- generated validator PASS
- quality validator PASS
- routing smoke PASS
- semantic review PASS
- release validator PASS
- Rubric Audit PASS
- 생성 보고서 정리
- 의도한 파일만 변경
- staging 전까지 staging empty 유지

---

## 24. 작성 순서

오류를 최소화하기 위해 다음 순서를 고정한다.

1. 본 요구사항 시트 작성 및 검증
2. source Topic Pack 5개 파일 작성
3. source schema와 의미 계약 검증
4. generated bank 생성
5. source/generated 일치 검증
6. host 기반 비LLM 회귀
7. container 기반 LLM smoke 1회
8. semantic review
9. release validation
10. Rubric Audit
11. 검증 보고서 정리
12. 정확한 파일만 staging
13. staged semantic contract 검증
14. commit 및 push

---

## 25. Revision Notes

- Bode 주파수응답 전용 요구사항으로 신규 작성함.
- Nyquist, Routh-Hurwitz, 근궤적 및 2차계 Topic과의 경계를 명시함.
- PM·GM의 평가 대상과 폐루프 bandwidth를 분리함.
- 시간지연, 비최소위상 영점, 다중 crossover와 phase unwrap을 포함함.
- deterministic regex에 의존하지 않고 LLM-only 의미 판정을 사용하도록 설계함.
- source 작성 전에 14개 anchor와 8개 fatal condition을 고정함.
