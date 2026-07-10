# Nyquist 안정도 판별과 이득·위상여유 Topic Pack 요구사항

이 문서는 산업계측제어기술사 답안 채점 시스템에서
Nyquist 안정도 판별과 이득·위상여유 주제를 평가하기 위한
requirements-first 설계 계약이다.

이 문서를 먼저 확정한 뒤 다음 순서로 작업한다.

1. Topic Pack source JSON 직접 작성
2. source validator와 품질 validator 실행
3. generated Rubric Bank 재생성
4. generated contract 검증
5. Logic Check 실제 LLM smoke 검증
6. release validation과 Rubric Audit

---

## 1. 문서 목적

이 Topic Pack은 연속시간 선형 시불변 폐루프 시스템의 안정성을
Nyquist 안정도 판별법으로 설명하고 계산하는 답안을 평가한다.

평가 대상은 단순한 Nyquist plot 모양 암기가 아니다.
다음 논리 연결을 정확히 설명해야 한다.

- 폐루프 특성방정식과 루프 전달함수의 관계
- 개루프 우반평면 극점 수 $P$
- $-1+j0$ 임계점에 대한 순선회수 $N$
- 폐루프 우반평면 극점 수 $Z$
- $P$, $N$, $Z$ 관계를 이용한 폐루프 안정 판정
- gain margin과 phase margin의 정의 및 해석
- 시간지연, 불안정 개루프, 복수 교차주파수의 처리
- 수학적 안정성과 현장 강인성의 차이

이 문서는 source JSON의 정답 범위, fatal 조건,
모범 답안 구성과 출력 계약을 고정한다.

---

## 2. Topic Pack 식별정보

- 제목: `Nyquist 안정도 판별과 이득·위상여유`
- topic_id: `nyquist_stability_criterion_gain_phase_margin`
- question_type: `CALC_DESIGN`
- difficulty: `THEORY_CORE`
- selection_importance: `CORE_MUST_PREPARE`
- subject: 산업계측제어
- 기본 제어구조: 표준 음의 피드백
- 평가 방식: Fact Anchor + Model Answer + LLM-only Logic Check
- deterministic fatal checks: 비활성화
- LLM candidate rules: 빈 배열
- candidate evidence: key-term semantic fallback 사용
- 권장 Fact Anchor 수: 14개
- 권장 모범 답안 outline: 8개
- fatal condition 수: 8개

---

## 3. 출제 의도

Nyquist 안정도 판별은 다음 역량을 동시에 평가하는
제어이론 핵심 주제이다.

1. 개루프 전달함수와 폐루프 특성방정식을 연결하는 능력
2. 복소함수의 argument principle을 제어 안정성에 적용하는 능력
3. 개루프 불안정 극점을 포함한 시스템을 판별하는 능력
4. 주파수응답과 폐루프 안정성을 연결하는 능력
5. gain margin과 phase margin을 현장 강인성으로 해석하는 능력
6. 시간지연과 비최소위상 특성이 안정여유에 미치는 영향을 판단하는 능력
7. Routh-Hurwitz 결과와 Nyquist 결과를 교차 검증하는 능력

기술사 답안은 정의만 나열해서는 부족하다.
반드시 식, 판정 절차, 계산 예제, 경계조건과 현장 해석을 연결해야 한다.

---

## 4. 학습 목표

답안 작성자는 다음 항목을 설명할 수 있어야 한다.

- 표준 음의 피드백에서 폐루프 특성방정식이
  $1+L(s)=0$임을 설명한다.
- Nyquist contour와 $L(s)$ 평면 사상의 의미를 설명한다.
- $P$, $N$, $Z$를 명확히 정의한다.
- 선택한 선회 방향 convention을 먼저 선언한다.
- $N_{cw}=Z-P$ 관계를 일관되게 적용한다.
- 폐루프 안정 조건 $Z=0$을 판정한다.
- 허수축 위 개루프 극점의 contour 우회 필요성을 설명한다.
- gain crossover와 phase crossover를 구분한다.
- gain margin과 phase margin을 올바른 주파수에서 계산한다.
- 복수 crossover에서 단일 margin 숫자만으로 결론 내리지 않는다.
- 시간지연 $e^{-sT}$의 위상효과를 설명한다.
- 수학적 안정 경계와 실무 운전영역을 구분한다.

---

## 5. 적용 범위

이 Topic Pack은 다음 문제에 적용한다.

- Nyquist 안정도 판별법의 원리 설명
- Nyquist contour와 Nyquist plot 작성 절차
- $P$, $N$, $Z$ 관계를 이용한 폐루프 안정성 판정
- 주어진 $L(s)$의 안정 이득 $K$ 범위 계산
- gain margin과 phase margin 계산
- Bode plot과 Nyquist plot의 안정여유 연결
- 시간지연이 포함된 시스템의 안정성 해석
- 개루프 우반평면 극점이 있는 시스템의 Nyquist 판정
- 허수축 위 극점을 포함한 시스템의 수정 Nyquist contour
- Routh-Hurwitz 결과와 Nyquist 결과의 교차 검증
- 운전점 변화와 모델 불확실성을 고려한 안정여유 평가

---

## 6. 비적용 범위

다음 항목은 이 Topic Pack의 직접 평가 범위가 아니다.

- 이산시간 시스템의 전체 Jury 안정도 판별
- $z$ 평면 단위원에 대한 discrete Nyquist 전체 유도
- MIMO 시스템의 generalized Nyquist criterion 전체 증명
- $\mu$-analysis와 structured singular value의 상세 계산
- describing function을 이용한 비선형 limit cycle 계산
- root locus 전체 작도법
- Nichols chart 전체 설계 절차
- 상태공간 Lyapunov 안정도 증명
- 확률적 강인제어 설계

다만 답안이 적용 한계를 설명하기 위해 위 방법을 보조적으로
언급하는 것은 허용한다.

---

## 7. 선수 지식

답안 작성에는 다음 지식이 필요하다.

- 전달함수와 극점·영점
- 표준 음의 피드백
- 폐루프 특성방정식
- 복소평면과 복소수의 크기·위상
- 주파수응답 $L(j\omega)$
- Bode plot
- Routh-Hurwitz 안정도 판별
- 우반평면, 좌반평면과 허수축의 안정성 의미
- gain crossover frequency
- phase crossover frequency
- 시간지연의 Laplace 표현 $e^{-sT}$

선수 지식이 부족한 답안은 계산식을 제시하더라도
판정 근거가 불완전할 수 있다.

---

## 8. 핵심 용어와 기호

### 8.1 기본 기호

- $L(s)$: loop transfer function
- $G(s)$: forward-path transfer function
- $H(s)$: feedback transfer function
- $L(s)=G(s)H(s)$
- $F(s)=1+L(s)$
- $P$: $L(s)$의 열린 우반평면 극점 수
- $Z$: $F(s)=1+L(s)$의 열린 우반평면 영점 수
- $N_{cw}$: $L(s)$ Nyquist plot의 $-1+j0$에 대한
  순시계방향 선회수
- $\omega_{gc}$: gain crossover frequency
- $\omega_{pc}$: phase crossover frequency
- $GM$: gain margin
- $PM$: phase margin

### 8.2 안정성 의미

$Z$는 폐루프 특성방정식의 우반평면 근 개수와 같다.

- $Z=0$: 우반평면 폐루프 극점 없음
- $Z>0$: 폐루프 불안정
- 허수축 폐루프 극점 존재: 점근안정이 아니므로 별도 경계 검증 필요

---

## 9. 폐루프 특성방정식과 Nyquist 판별 대상

표준 음의 피드백에서 폐루프 전달함수는

$T(s)=G(s)/[1+G(s)H(s)]$

이고 loop transfer function을

$L(s)=G(s)H(s)$

로 두면 폐루프 특성방정식은

$1+L(s)=0$

이다.

Nyquist 안정도 판별은 $L(s)$ 자체의 극점 위치만으로
폐루프 안정성을 직접 단정하지 않는다.

복소함수

$F(s)=1+L(s)$

의 우반평면 영점 수를 argument principle로 계산한다.
$F(s)$의 영점은 폐루프 특성방정식의 근이므로
그 우반평면 영점 수가 $Z$이다.

---

## 10. Nyquist contour 요구사항

Nyquist contour는 일반적으로 열린 우반평면 전체를 둘러싸는
폐곡선으로 구성한다.

포함 요소는 다음과 같다.

1. 허수축의 음의 무한대에서 양의 무한대까지의 경로
2. 무한 반원의 폐곡선
3. 허수축 위 극점이 있으면 해당 극점을 피하는 작은 우회 경로
4. contour orientation의 명시

유리 proper 전달함수에서 무한 반원 사상은 종종 원점으로 수렴하지만,
상대차수와 전달함수 형태를 확인하지 않고 자동으로 생략하면 안 된다.

contour 위에 $L(s)$의 극점이 존재하면 argument principle을
그 상태로 직접 적용할 수 없다.

---

## 11. Nyquist mapping과 실계수 대칭성

Nyquist plot은 Nyquist contour 위의 모든 $s$를
복소함수 $L(s)$에 대입하여 $L$ 평면에 사상한 궤적이다.

실계수 전달함수에서는

$L(-j\omega)=L(j\omega)^*$

이므로 음의 주파수 궤적은 양의 주파수 궤적의
실수축 대칭이다.

따라서 계산은 보통 $\omega=0^+$에서 $\infty$까지 수행하고,
대칭성을 이용해 전체 궤적을 완성할 수 있다.

그러나 허수축 극점 우회 사상과 무한 반원 사상은
양의 주파수 궤적만으로 자동 대체되지 않으므로 별도로 검토한다.

---

## 12. 개루프 우반평면 극점 수 P

$P$는 loop transfer function $L(s)$의 열린 우반평면 극점 수이다.

다음 원칙을 적용한다.

- 중복극점은 중복도를 포함해 센다.
- 허수축 위 극점은 열린 우반평면 극점 $P$에 포함하지 않는다.
- 허수축 위 극점은 contour 우회 대상으로 별도 처리한다.
- 극점·영점 상쇄를 임의로 수행하지 않는다.
- 불안정 pole-zero cancellation은 내부 안정성을 숨길 수 있다.
- $P$를 계산하지 않고 선회수만 보는 것은 불완전한 판정이다.

Nyquist 판정 전에 반드시 $P$를 먼저 고정해야 한다.

---

## 13. P, N, Z 관계와 안정 판정

이 문서의 기본 convention은 다음과 같다.

- Nyquist contour는 열린 우반평면을 시계방향으로 둘러싼다.
- $N_{cw}$는 $-1+j0$에 대한 순시계방향 선회수를 양수로 정의한다.

이때 argument principle에 의해

$N_{cw}=Z-P$

이다.

따라서

$Z=P+N_{cw}$

이다.

폐루프 점근안정을 위해서는 열린 우반평면 폐루프 극점이 없어야 하므로

$Z=0$

이어야 한다.

따라서 필요한 선회수는

$N_{cw}=-P$

이다.

즉, $P$개의 개루프 우반평면 극점이 있으면
$-1$점을 순반시계방향으로 $P$회 선회해야 폐루프 안정이 가능하다.

---

## 14. 선회 방향 convention 관리

교재와 소프트웨어에 따라 선회 방향의 부호 정의가 다를 수 있다.

반시계방향 선회를 양수로 정의한 경우

$N_{ccw}=P-Z$

를 사용할 수 있다.

두 식은 서로 모순이 아니다.

$N_{ccw}=-N_{cw}$

관계로 동일한 결과를 나타낸다.

채점에서는 다음을 확인한다.

- 답안이 사용하는 선회 방향을 명시했는가
- 부호 convention을 처음부터 끝까지 일관되게 적용했는가
- 최종적으로 계산한 $Z$가 물리적 폐루프 안정성과 일치하는가

방향 명칭만 다르더라도 정의와 계산이 일관되면 정상 답안이다.

---

## 15. 개루프 안정 시스템 P=0의 특수형

$P=0$이면

$N_{cw}=Z$

이다.

폐루프 안정 조건 $Z=0$을 만족하려면

$N_{cw}=0$

이어야 한다.

즉, $P=0$인 표준 음의 피드백 시스템에서는
Nyquist plot이 $-1+j0$을 순선회하지 않아야 한다.

그러나 다음 사항도 확인해야 한다.

- 궤적이 정확히 $-1$점을 통과하는가
- 허수축 폐루프 극점이 발생하는가
- gain 또는 phase crossover가 복수로 존재하는가
- 단순한 그림 해상도 때문에 접촉을 놓치지 않았는가

“선회하지 않는다”와 “$-1$점을 통과한다”는 같은 의미가 아니다.

---

## 16. 허수축 위 개루프 극점 처리

$L(s)$가 $s=0$ 또는 $s=j\omega_0$에 극점을 가지면
기본 contour가 극점을 통과하므로 argument principle을
그대로 적용할 수 없다.

다음 절차를 사용한다.

1. 극점 주변을 작은 반원으로 우회한다.
2. 우회 방향과 contour 내부 포함 여부를 명시한다.
3. 작은 반원의 $L(s)$ 평면 사상을 계산하거나 극한으로 판단한다.
4. 우회 사상을 포함하여 전체 $-1$점 선회수를 계산한다.
5. 경계극점과 폐루프 허수축 극점을 구분한다.

원점 적분기를 포함한 시스템은 이 절차를 자주 요구한다.

---

## 17. 이득 K 변화와 Nyquist 궤적

$L(s)=K L_0(s)$이고 $K>0$이면
$K$ 변화는 Nyquist 궤적의 반지름 방향 scaling으로 해석할 수 있다.

- 위상은 $L_0(j\omega)$와 동일하다.
- 크기는 $K$배가 된다.
- 임계이득은 궤적이 $-1$점을 통과하는 조건에서 구한다.
- 임계이득 경계는 일반적으로 점근안정 범위에 포함하지 않는다.
- 경계에서는 허수축 폐루프 극점 가능성을 확인한다.

$K<0$ 또는 복소이득은 단순 양의 반지름 scaling으로 해석하면 안 된다.

---

## 18. Gain margin 정의

phase crossover frequency는

$\angle L(j\omega_{pc})=-180^\circ$

를 만족하는 주파수이다.
위상은 선택한 unwrap convention과 등가각을 고려한다.

선형 gain margin은

$GM=1/|L(j\omega_{pc})|$

이다.

dB 표현은

$GM_{dB}=-20\log_{10}|L(j\omega_{pc})|$

이다.

해석은 다음과 같다.

- $GM>1$: 해당 crossover 기준으로 추가 이득 증가 여유가 있음
- $GM=1$: 임계경계
- $GM<1$: 해당 crossover 기준으로 이미 불안정 측에 있을 수 있음

개루프 불안정 시스템이나 복수 crossover에서는
고전적 단일 GM만으로 폐루프 안정성을 단정하지 않는다.

---

## 19. Phase margin 정의

gain crossover frequency는

$|L(j\omega_{gc})|=1$

을 만족하는 주파수이다.

표준 음의 피드백에서 phase margin은

$PM=180^\circ+\angle L(j\omega_{gc})$

이다.

위상은 연속적으로 unwrap한 값을 사용해야 한다.

해석은 다음과 같다.

- 양의 PM은 일반적으로 추가 위상지연 여유를 의미한다.
- $PM=0^\circ$는 임계경계 후보이다.
- 음의 PM은 해당 crossover 기준 불안정 가능성을 나타낸다.
- PM은 감쇠비와 연관될 수 있지만 일반 시스템에서 일대일 관계는 아니다.
- 시간지연, 비최소위상 영점과 복수 crossover가 있으면 Nyquist 전체 궤적을 확인한다.

---

## 20. 복수 crossover 처리

시스템에 따라 $\omega_{gc}$ 또는 $\omega_{pc}$가
여러 개 존재할 수 있다.

이 경우 다음 원칙을 적용한다.

1. 모든 gain crossover를 찾는다.
2. 각 gain crossover의 phase margin을 계산한다.
3. 모든 phase crossover를 찾는다.
4. 각 phase crossover의 gain margin을 계산한다.
5. 불안정 경계에 가장 가까운 crossover를 확인한다.
6. 최종 판단은 Nyquist의 순선회수와 함께 수행한다.

단순히 가장 낮은 주파수 crossover 하나만 사용하면
고주파 불안정 위험을 놓칠 수 있다.

---

## 21. 시간지연의 영향

순수 시간지연은

$e^{-sT}$

로 표현한다.

주파수축에서

$|e^{-j\omega T}|=1$

이고

$\angle e^{-j\omega T}=-\omega T$

이다.

따라서 시간지연은 이상적인 경우 크기응답을 변화시키지 않지만
주파수가 증가할수록 위상지연을 선형적으로 증가시킨다.

그 결과 다음 현상이 발생할 수 있다.

- phase margin 감소
- gain crossover에서의 위상 악화
- 임계이득 감소
- 폐루프 진동 증가
- 불안정 발생

Nyquist 방법은 초월함수 $e^{-sT}$를 주파수응답 형태로
직접 다룰 수 있다는 점에서 Routh-Hurwitz보다 유리하다.

---

## 22. 개루프 불안정과 비최소위상 시스템

개루프 우반평면 극점이 있으면 $P>0$이다.

이 경우 “$-1$점을 선회하지 않으면 안정”이라는
$P=0$ 특수형을 적용하면 안 된다.

폐루프 안정에는

$N_{cw}=-P$

가 필요하다.

우반평면 영점은 $P$에는 포함되지 않지만
다음 특성을 유발할 수 있다.

- 추가 위상지연
- inverse response
- achievable bandwidth 제한
- 안정여유와 응답성능의 trade-off 악화

비최소위상 시스템은 양의 GM과 PM 숫자만으로
충분한 강인성을 보장한다고 단정하지 않는다.

---

## 23. 현장 강인성 및 설계 판단

수학적으로 안정한 제어기 이득 전체가
현장에서 안전한 운전영역은 아니다.

다음 요소를 함께 검토한다.

- 공정 운전점 변화
- 플랜트 파라미터 불확실성
- 센서와 actuator의 동특성
- 통신 및 계산 지연
- 샘플링과 zero-order hold
- actuator saturation
- rate limit
- 센서 잡음
- 미모델 고주파 모드
- 비최소위상 영점
- dead time 변화
- 유지보수 후 모델 편차

현장 적용 이득은 Nyquist 임계경계에서 충분한 거리를 두어야 한다.

검증 방법은 다음을 포함한다.

- 전체 운전점 Bode/Nyquist 분석
- 최소 GM과 PM 확인
- pole calculation 교차 검증
- step response와 disturbance response
- saturation 포함 simulation
- 지연 변화 sensitivity test
- 현장 단계별 gain 적용

---

## 24. 대표 계산 예제 1: Routh와 Nyquist 교차 검증

다음 loop transfer function을 사용한다.

$L(s)=K/[s(s+1)(s+2)]$

표준 음의 피드백 폐루프 특성방정식은

$1+L(s)=0$

이므로

$s(s+1)(s+2)+K=0$

이고 정리하면

$s^3+3s^2+2s+K=0$

이다.

Routh-Hurwitz 결과는

$0<K<6$

에서 점근안정이다.

Nyquist의 phase crossover 조건은

$-90^\circ-\tan^{-1}(\omega)-\tan^{-1}(\omega/2)
=-180^\circ$

이다.

따라서

$\omega_{pc}=\sqrt{2}$

이다.

이 주파수에서 분모 크기는

$\omega\sqrt{1+\omega^2}\sqrt{4+\omega^2}=6$

이므로

$|L(j\omega_{pc})|=K/6$

이다.

임계조건 $|L|=1$에서

$K_{cr}=6$

이다.

따라서 Nyquist 결과도

$0<K<6$

이며 Routh 결과와 일치한다.

$K=6$은 점근안정 범위에 포함하지 않고
허수축 극점을 별도 확인한다.

---

## 25. 대표 계산 예제 2: 개루프 우반평면 극점

다음 loop transfer function을 고려한다.

$L(s)=K/[(s-1)(s+2)]$

개루프 극점은

$s=1,\ -2$

이므로

$P=1$

이다.

폐루프 특성방정식은

$(s-1)(s+2)+K=0$

즉,

$s^2+s+(K-2)=0$

이다.

2차 다항식의 점근안정 조건은

$K>2$

이다.

Nyquist 관점에서 폐루프 안정은 $Z=0$이므로

$N_{cw}=-P=-1$

이 필요하다.

즉, $-1$점을 순반시계방향으로 한 번 선회해야 한다.

이 예제는 개루프 불안정 시스템에서
무선회가 폐루프 안정을 의미하지 않음을 보여준다.

---

## 26. 대표 계산 예제 3: 시간지연

다음 시스템을 고려한다.

$L(s)=K e^{-sT}/[s(s+1)]$

시간지연 항의 크기는 1이므로

$|L(j\omega)|=K/[\omega\sqrt{1+\omega^2}]$

이다.

그러나 위상은

$\angle L(j\omega)
=-90^\circ-\tan^{-1}(\omega)-\omega T\cdot180^\circ/\pi$

이다.

$T$가 증가하면 모든 양의 주파수에서 추가 위상지연이 증가한다.

따라서 다음 경향이 발생한다.

- phase crossover가 낮아질 수 있음
- phase margin 감소
- 허용 가능한 $K$ 감소
- Nyquist 궤적이 $-1$점에 가까워짐
- 폐루프 진동 또는 불안정 가능성 증가

Padé 근사를 사용해 다항식으로 변환할 수도 있지만
근사 차수와 가짜 pole-zero 영향이 있으므로
원래 지연 주파수응답과 교차 검증한다.

---

## 27. 특수 상황과 오판 방지

다음 상황은 별도 주의가 필요하다.

### 27.1 $-1$점 통과

Nyquist plot이 $-1$점을 통과하면
폐루프 특성방정식이 허수축 근을 가질 가능성이 있다.
점근안정으로 포함하지 않고 임계안정 또는 불안정을 별도 판정한다.

### 27.2 pole-zero cancellation

우반평면 pole-zero cancellation은 외부 전달함수에서 사라져 보여도
내부 불안정 모드를 숨길 수 있다.

### 27.3 improper transfer function

상대차수가 음수인 improper 모델은
일반적인 무한 반원 사상 가정을 그대로 사용할 수 없다.

### 27.4 복수 선회

궤적이 $-1$점을 여러 번 선회하면
방향과 횟수를 대수적으로 합산한다.

### 27.5 plot 해상도

수치 plot의 주파수 grid가 거칠면
작은 loop, 접촉, 복수 crossover를 놓칠 수 있다.

### 27.6 안정여유 숫자의 한계

GM과 PM은 유용한 지표지만
모든 불확실성에 대한 절대적 강인성 보증은 아니다.

---

## 28. Fact Anchor 계약

Fact Anchor는 최소 14개를 작성한다.

1. `closed_loop_characteristic_equation`
   - 표준 음의 피드백 특성방정식은 $1+L(s)=0$이다.

2. `nyquist_contour_and_mapping`
   - 열린 우반평면 Nyquist contour를 $L(s)$ 평면으로 사상한다.

3. `argument_principle_pnz_relation`
   - 시계방향 양수 convention에서 $N_{cw}=Z-P$이다.

4. `critical_point_minus_one`
   - Nyquist 안정 판정 임계점은 $-1+j0$이다.

5. `open_loop_rhp_poles_count`
   - $P$는 $L(s)$의 열린 우반평면 극점 수이다.

6. `closed_loop_rhp_poles_count`
   - $Z$는 $1+L(s)$의 열린 우반평면 영점 수이다.

7. `stable_open_loop_special_case`
   - $P=0$인 폐루프 안정 시스템은 $-1$점 순선회가 0이어야 한다.

8. `imaginary_axis_pole_indentation`
   - 허수축 위 개루프 극점은 contour 우회가 필요하다.

9. `conjugate_symmetry`
   - 실계수 전달함수는 양·음 주파수 궤적이 실수축 대칭이다.

10. `gain_margin_definition`
    - GM은 phase crossover에서 계산한다.

11. `phase_margin_definition`
    - PM은 gain crossover에서 계산한다.

12. `multiple_crossover_interpretation`
    - 복수 crossover는 모두 평가하고 Nyquist 선회수와 결합한다.

13. `time_delay_phase_effect`
    - 순수 지연은 크기는 1이지만 위상을 $-\omega T$만큼 지연시킨다.

14. `field_robustness_validation`
    - 현장 이득은 임계경계에서 여유를 두고 지연·불확실성을 검증한다.

각 anchor는 다음 필드를 가져야 한다.

- id
- statement
- core_terms
- accepted_explanations
- rejected_explanations
- grading_notes
- source_basis

---

## 29. Model Answer 계약

Model Answer의 question_type은 `CALC_DESIGN`으로 고정한다.

권장 outline은 정확히 8개 section으로 구성한다.

1. 문제 배경과 Nyquist 판별 목적
2. 폐루프 특성방정식과 $L(s)$ 정의
3. Nyquist contour와 mapping 절차
4. $P$, $N$, $Z$ 정의와 안정 조건
5. 이득 $K$ 및 임계조건 계산
6. GM과 PM 계산 및 복수 crossover 처리
7. 시간지연·개루프 불안정·허수축 극점 특수조건
8. 현장 강인성 검증과 결론

모범 답안은 다음 요소를 포함한다.

- 핵심 수식
- 계산 순서
- 선회 방향 convention
- 최소 하나의 안정 범위 예제
- 최소 하나의 개루프 불안정 예제
- 시간지연의 위상효과
- Routh 또는 pole calculation과의 교차 검증
- 현장 적용 여유

키워드만 나열하는 답안은 고득점 모범 답안으로 인정하지 않는다.

---

## 30. Logic Check 계약

Logic Check는 LLM-only 방식으로 구성한다.

### 30.1 deterministic 설정

- enabled: false
- fatal_checks: 빈 배열
- major_checks: 빈 배열
- question_type_checks: 빈 배열
- score_effect: none

deterministic regex가 fatal 결론을 직접 내리지 않는다.

### 30.2 candidate extraction

- max_candidates: 20
- nearby_window: 2
- key_terms: Nyquist, $-1$, 선회, 우반평면, gain margin,
  phase margin, crossover, 시간지연 등
- rules: 빈 배열

rules가 비어 있으므로 공통 key-term semantic fallback이
답안의 관련 문맥을 candidate evidence로 추출해야 한다.

candidate extraction은 오답을 결정하지 않는다.
최종 semantic verdict는 LLM이 수행한다.

### 30.3 출력 계약

LLM 출력은 JSON object만 허용한다.

필수 필드는 다음과 같다.

- `verdict`
- `confidence`
- `reason`
- `checks`
- `findings`

verdict 허용값은 다음과 같다.

- pass
- warn
- fatal

fatal confidence threshold는 0.75로 한다.

fatal 판정 시 권장 ceiling은 10.0점으로 한다.

LLM 호출 실패, JSON parse 실패 또는 필수 필드 오류는
fatal cap을 만들지 않고 안전한 warn diagnostic으로 처리한다.

---

## 31. Fatal condition 계약

다음 8개 ID를 정확히 한 번씩 source 요구사항에 정의한다.

1. `nyquist_encircles_origin_instead_of_minus_one`
   - 답안이 Nyquist 안정 판정의 임계점을
     $-1+j0$가 아니라 원점이라고 실제 정답으로 주장한다.

2. `nyquist_ignores_open_loop_rhp_poles`
   - 답안이 $P$를 계산하지 않아도 선회수만으로
     모든 폐루프 안정성을 판정할 수 있다고 주장한다.

3. `nyquist_no_encirclement_always_stable`
   - 답안이 개루프 우반평면 극점 수와 무관하게
     $-1$점 무선회이면 항상 폐루프 안정이라고 주장한다.

4. `nyquist_sign_convention_reversed_without_definition`
   - 답안이 선회 방향 부호를 정의하지 않고
     $P$, $N$, $Z$ 관계를 반대로 적용하여 최종 안정성을 오판한다.

5. `imaginary_axis_pole_used_without_indentation`
   - 답안이 contour 위 개루프 극점을 우회하지 않고
     일반 argument principle을 그대로 적용한다.

6. `gain_margin_measured_at_gain_crossover`
   - 답안이 gain margin을 phase crossover가 아니라
     gain crossover에서 계산한다고 주장한다.

7. `phase_margin_measured_at_phase_crossover`
   - 답안이 phase margin을 gain crossover가 아니라
     phase crossover에서 계산한다고 주장한다.

8. `time_delay_changes_magnitude_only`
   - 답안이 순수 시간지연은 위상에는 영향이 없고
     크기응답만 변화시킨다고 주장한다.

오답 문장을 인용한 뒤 명확히 반박하는 문맥은 fatal이 아니다.

단순 누락, 짧은 설명, convention 표기 부족은
최종 안정성 오판이 없다면 major 또는 minor로 처리한다.

---

## 32. 완료 조건과 검증 기준

Topic Pack 완료 조건은 다음과 같다.

### 32.1 Requirements Sheet

- 번호 heading이 1부터 32까지 정확히 존재한다.
- 14개 Fact Anchor ID가 모두 존재한다.
- 8개 fatal ID가 각각 정확히 한 번 존재한다.
- question_type이 `CALC_DESIGN`이다.
- difficulty가 `THEORY_CORE`이다.
- selection_importance가 `CORE_MUST_PREPARE`이다.
- deterministic fatal check가 비활성화되어 있다.
- candidate rules가 빈 배열로 정의되어 있다.
- output 필드 5개가 모두 정의되어 있다.
- 문서 끝에 newline이 존재한다.
- trailing whitespace와 tab이 없다.

### 32.2 Source Topic Pack

다음 5개 파일을 작성한다.

- README.md
- fact_anchor.json
- logic_check.json
- model_answer.json
- topic_importance.json

source validator와 quality validator를 모두 통과해야 한다.

### 32.3 Generated Rubric Bank

다음 generated 파일에 topic이 정확히 한 번 반영되어야 한다.

- fact_anchors.generated.json
- logic_check_profiles.generated.json
- logic_checks.generated.json
- model_answers.generated.json
- topic_importance.generated.json
- topic_pack_manifest.generated.json

### 32.4 Logic Check runtime

다음을 확인한다.

- generated LLM profile 로드
- 8개 fatal condition 로드
- key-term fallback candidate 생성
- 명백한 Nyquist 오개념의 실제 LLM fatal 판정
- fatal confidence threshold 적용
- recommended ceiling 10.0
- LLM 실패 시 안전한 warn fallback

### 32.5 Release validation

다음을 모두 통과해야 한다.

- Python compile
- Topic Pack validation
- generated pipeline validation
- Topic Pack quality validation
- focused Logic Check regression
- score-flow guard regression
- output formatter regression
- 최종 Rubric Audit
- git diff whitespace validation
- 정확한 changeset 검증
