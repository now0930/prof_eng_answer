# Routh-Hurwitz 안정도 판별과 제어기 이득 범위 Topic Sheet

## 1. 문서 목적

이 문서는 다음 Topic Pack을 만들기 위한 사람 검토용 요구사항 문서이다.

- Topic ID: `routh_hurwitz_stability_criterion_gain_range`
- 주제명: Routh-Hurwitz 안정도 판별과 제어기 이득 범위
- 대표 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 중요도: `CORE_MUST_PREPARE`
- 적용 분야: 산업계측제어기술사 제어공학 답안
- 작성 순서: Markdown 요구사항 확정 후 ChatGPT가 JSON을 직접 작성
- 금지사항: Gemini 또는 다른 LLM이 Topic Pack JSON을 직접 생성하지 않음

이 문서를 기준으로 다음 파일을 작성한다.

1. `README.md`
2. `fact_anchor.json`
3. `logic_check.json`
4. `model_answer.json`
5. `topic_importance.json`

JSON은 기존 스키마와 validator를 확인한 뒤 ChatGPT가 직접 작성한다.

---

## 2. Topic Pack 설계 목적

Routh-Hurwitz 판별법은 특성방정식의 근을 직접 계산하지 않고도 우반평면 극점의 수와 안정 여부를 판단하는 대수적 안정도 판별법이다.

직전 Topic Pack인 피드백 시스템 주제에서 다음 관계를 다뤘다.

- 루프 전달함수: `L(s)=G(s)H(s)`
- 폐루프 특성방정식: `1+L(s)=0`
- 폐루프 안정성은 특성방정식의 모든 근이 좌반평면에 존재하는지로 판단

이번 Topic Pack은 이 특성방정식을 실제 다항식으로 전개한 뒤 다음을 판단하는 단계까지 확장한다.

- 우반평면 극점 개수
- 점근안정 여부
- 허수축 근 존재 여부
- 제어기 이득 `K`의 안정 범위
- 상대안정도 조건
- 특수한 Routh 배열 처리
- 판별법의 적용 한계

핵심 연결 구조는 다음과 같다.

`폐루프 특성방정식 → Routh 배열 → 첫 열 부호 변화 → 우반평면 극점 수 → 안정 이득 범위`

---

## 3. 대표 문제

### 3.1 기본 설명형

Routh-Hurwitz 안정도 판별법의 원리와 판별 절차를 설명하시오.

### 3.2 계산형

다음 특성방정식에 대하여 Routh 배열을 작성하고 안정 여부를 판별하시오.

### 3.3 이득 범위형

폐루프 특성방정식에 포함된 제어기 이득 `K`의 안정 범위를 Routh-Hurwitz 판별법으로 구하시오.

### 3.4 특수 경우형

Routh 배열 작성 중 첫 열의 원소가 0이 되는 경우와 한 행 전체가 0이 되는 경우의 처리 방법을 설명하시오.

### 3.5 상대안정도형

모든 폐루프 극점의 실수부가 `-α`보다 작도록 하는 조건을 Routh-Hurwitz 판별법으로 구하시오.

---

## 4. 문제 유형

주요 문제 유형은 `CALC_DESIGN`으로 한다.

이유는 다음과 같다.

- 특성다항식으로부터 배열을 직접 구성해야 한다.
- 첫 열 조건을 부등식으로 변환해야 한다.
- 제어기 이득 범위를 계산해야 한다.
- 경계값에서 허수축 근 또는 중복근을 별도로 판단해야 한다.
- 상대안정도 문제에서는 변수 치환과 재전개가 필요하다.

보조적으로 다음 성격도 포함한다.

- `PRINCIPLE_INTERPRETATION`: 판별 원리와 부호 변화 의미
- `PROCEDURE`: Routh 배열 작성 절차
- `COMPARE_SELECTION`: 직접 근 계산, Nyquist, Root Locus와의 적용 차이

대표 `question_type` 값은 `CALC_DESIGN`으로 고정한다.

---

## 5. 난이도와 중요도

### 5.1 난이도

`THEORY_CORE`

Routh-Hurwitz 판별법은 다음 주제를 연결하는 핵심 제어이론이다.

- 폐루프 특성방정식
- 극점과 안정성
- PID 및 제어기 이득
- Root Locus
- Nyquist 안정도 판별
- Gain Margin과 Phase Margin
- 상대안정도
- 고차 시스템 설계

### 5.2 선택 중요도

`CORE_MUST_PREPARE`

이 주제는 계산 절차뿐 아니라 다음 오개념을 구분할 수 있어야 한다.

- 필요조건과 충분조건
- 우반평면 극점과 좌반평면 극점
- 첫 열의 0과 한 행 전체 0
- 경계 안정과 점근 안정
- 다항식과 시간지연 시스템
- 안정 이득 범위의 열린 경계와 닫힌 경계

---

## 6. 적용 범위

다음 내용을 Topic Pack 범위에 포함한다.

1. 연속시간 선형 시불변 시스템
2. 실수 계수를 갖는 특성다항식
3. Routh 배열 구성
4. 첫 열 부호 변화와 우반평면 근 개수
5. 점근안정 조건
6. 필요조건과 충분조건 구분
7. 첫 열 선두 원소가 0인 경우
8. 한 행 전체가 0인 경우
9. 보조다항식과 도함수 행
10. 허수축 근과 대칭근
11. 이득 `K`의 안정 범위
12. 경계값 검증
13. 상대안정도와 축 이동
14. 적용 한계와 다른 안정도 기법과의 연결

다음 내용은 핵심 범위에서 제외하되 확장 설명은 허용한다.

- Jury 안정도 판별법
- Schur-Cohn 판별법
- 이산시간 안정도 판별
- 완전한 Nyquist contour 유도
- Root Locus 작도 전체 절차
- Lyapunov 안정도 증명
- 비선형 시스템의 전역 안정성
- 무한차원 시스템의 엄밀한 안정성 증명

---

## 7. 기본 수학 모델

일반적인 폐루프 특성다항식을 다음과 같이 둔다.

\[
P(s)=a_n s^n+a_{n-1}s^{n-1}+\cdots+a_1s+a_0
\]

단, 다음 조건을 기본 전제로 한다.

- `a_n ≠ 0`
- 계수는 실수
- 차수는 유한
- 공통 인수가 있으면 먼저 정리
- 특성방정식은 `P(s)=0`

연속시간 시스템이 점근안정하려면 모든 근이 다음 조건을 만족해야 한다.

\[
\operatorname{Re}(s_i)<0
\]

즉, 모든 폐루프 극점이 복소 `s` 평면의 열린 좌반평면에 있어야 한다.

---

## 8. Routh-Hurwitz 판별의 핵심 원리

Routh 배열의 첫 번째 열에서 발생하는 부호 변화 횟수는 특성다항식이 갖는 우반평면 근의 개수와 같다.

중복근은 중복도를 포함하여 계산한다.

따라서 다음 조건이 모두 성립하면 점근안정으로 판단할 수 있다.

1. 첫 열에 부호 변화가 없다.
2. 첫 열에 0이 없다.
3. 한 행 전체가 0이 되는 특수 경우가 없다.
4. 허수축 근이 없다.
5. 모든 근이 열린 좌반평면에 있다.

단순히 첫 열의 부호 변화가 없다는 사실만 보고 허수축 근 존재 가능성을 무시하면 안 된다.

---

## 9. 계수 조건의 의미

안정 다항식의 모든 계수가 같은 부호를 갖는 것은 일반적으로 필요한 조건이다.

통상 최고차항 계수를 양수로 정규화하면 모든 계수가 양수여야 한다.

그러나 다음 명제는 성립하지 않는다.

> 모든 계수가 양수이면 시스템은 반드시 안정하다.

계수가 모두 양수인 것은 필요조건일 수 있지만 일반적인 고차 다항식에서 충분조건은 아니다.

따라서 계수 부호 확인은 초기 screening으로만 사용하고 최종 판정은 Routh 배열의 첫 열 조건으로 수행한다.

계수 중 0이 있거나 부호가 섞여 있으면 안정 가능성을 우선 의심할 수 있지만, 정확한 우반평면 근 개수는 Routh 배열을 통해 확인한다.

---

## 10. Routh 배열 구성 원칙

다항식이 다음과 같다고 한다.

\[
P(s)=a_n s^n+a_{n-1}s^{n-1}+\cdots+a_0
\]

첫 번째 행에는 다음 계수를 배치한다.

\[
a_n,\ a_{n-2},\ a_{n-4},\ldots
\]

두 번째 행에는 다음 계수를 배치한다.

\[
a_{n-1},\ a_{n-3},\ a_{n-5},\ldots
\]

이후 행은 바로 위 두 행의 원소로 계산한다.

부호 convention은 교재에 따라 식의 분자 부호를 다르게 표현할 수 있다.

중요한 것은 다음과 같다.

- 하나의 convention을 배열 전체에서 일관되게 사용
- 첫 열 부호 변화 결과가 동일해야 함
- 식을 외우기보다 행렬식 또는 교차곱 구조를 이해
- 계산 과정에서 0으로 나누는 경우를 별도로 처리

표준적인 한 표현은 다음과 같다.

\[
b_1=
\frac{
a_{n-1}a_{n-2}-a_n a_{n-3}
}{
a_{n-1}
}
\]

\[
b_2=
\frac{
a_{n-1}a_{n-4}-a_n a_{n-5}
}{
a_{n-1}
}
\]

다음 행의 첫 원소는 같은 방식으로 계산한다.

\[
c_1=
\frac{
b_1a_{n-3}-a_{n-1}b_2
}{
b_1
}
\]

배열 계산식의 형태보다 첫 열 부호와 특수 상황 처리가 더 중요하다.

---

## 11. 안정 판정

최고차항 계수를 양수로 정규화한 경우 점근안정을 위한 Routh 조건은 일반적으로 다음과 같이 정리한다.

- 첫 열 모든 원소가 존재
- 첫 열 모든 원소가 0이 아님
- 첫 열 모든 원소가 같은 부호
- 한 행 전체가 0이 아님
- 허수축 근이 없음

첫 열 부호 변화 횟수가 `m`이면 우반평면 근이 `m`개 존재한다.

예를 들어 첫 열이 다음과 같다고 한다.

\[
+,\ +,\ -,\ -,\ +
\]

부호 변화는 다음 두 번이다.

- `+ → -`
- `- → +`

따라서 우반평면 근은 2개이다.

Routh 판별은 우반평면 근의 개수를 알려주지만 일반적으로 각 근의 정확한 수치 위치를 직접 제공하지 않는다.

---

## 12. 첫 열의 선두 원소가 0인 경우

Routh 배열을 작성하는 도중 어떤 행의 첫 번째 원소만 0이고 그 행의 나머지 원소가 모두 0은 아닌 경우가 있다.

이 경우 다음 절차를 적용한다.

1. 해당 첫 원소를 작은 양수 `ε`로 대체한다.
2. 배열 계산을 계속한다.
3. `ε → 0+` 극한에서 첫 열 부호를 판단한다.
4. 부호 변화 횟수를 계산한다.

여기서 `ε`는 임의의 유한 숫자로 고정하여 사용하는 것이 아니다.

반드시 양의 작은 값으로 두고 극한의 부호를 해석해야 한다.

`ε` 처리의 목적은 배열 계산을 계속할 수 있도록 0으로 나누는 문제를 회피하는 것이다.

이 경우를 한 행 전체가 0인 경우와 혼동하면 안 된다.

---

## 13. 한 행 전체가 0인 경우

Routh 배열에서 한 행 전체가 0이 되는 경우가 있다.

이는 근이 원점에 대해 대칭적으로 존재하는 구조를 나타낼 수 있다.

예시는 다음과 같다.

- 허수축 위의 켤레근
- 실수축에 대한 대칭근
- 원점 대칭 근
- 짝수 다항식 또는 홀수 다항식에 관련된 대칭 구조

처리 절차는 다음과 같다.

1. 0행의 바로 위 행 계수로 보조다항식 `A(s)`를 구성한다.
2. `A(s)`를 `s`에 대해 미분한다.
3. `dA(s)/ds`의 계수를 0행에 대입한다.
4. Routh 배열 계산을 계속한다.
5. 보조다항식의 근을 별도로 검토한다.

보조다항식의 차수는 그 행에 대응하는 차수로 구성한다.

한 행 전체가 0이라는 사실만으로 즉시 불안정이라고 단정하지 않는다.

다만 허수축 근이 존재하면 점근안정은 아니다.

허수축에 단순근이 있고 우반평면 근이 없다면 임계안정 또는 한계안정 가능성을 검토한다.

허수축에 중복근이 존재하면 응답이 발산할 수 있으므로 안정으로 분류하면 안 된다.

---

## 14. 허수축 근과 안정성 분류

연속시간 시스템의 안정성은 다음과 같이 구분한다.

### 14.1 점근안정

모든 극점이 열린 좌반평면에 존재한다.

\[
\operatorname{Re}(s_i)<0
\]

### 14.2 임계안정 또는 한계안정

- 우반평면 극점이 없음
- 허수축에 단순근이 존재
- 나머지 극점은 좌반평면에 존재

이 경우 지속진동이 나타날 수 있다.

### 14.3 불안정

다음 중 하나가 존재하면 불안정이다.

- 우반평면 극점
- 허수축 중복극점
- 원점 중복극점
- 시간에 따라 발산하는 모드

따라서 Routh 배열에서 부호 변화가 없더라도 한 행 전체가 0이면 점근안정 여부를 별도로 확인해야 한다.

---

## 15. 제어기 이득 K의 안정 범위

특성다항식 계수에 제어기 이득 `K`가 포함된 경우 다음 절차로 안정 범위를 구한다.

1. 폐루프 특성방정식을 구한다.
2. 특성다항식을 `s`의 내림차순으로 정리한다.
3. Routh 배열을 작성한다.
4. 첫 열 원소를 `K`의 식으로 나타낸다.
5. 첫 열 모든 원소가 같은 부호가 되도록 부등식을 세운다.
6. 모든 부등식의 교집합을 구한다.
7. 경계값을 특성방정식 또는 보조다항식으로 별도 검증한다.

최고차항을 양수로 정규화했다면 일반적으로 첫 열에 대해 다음과 같은 엄격 부등식을 적용한다.

\[
r_i(K)>0
\]

안정 범위의 경계에서는 다음 현상이 발생할 수 있다.

- 허수축 근
- 원점 근
- 중복근
- 차수 저하
- 분모 계수 소거

그러므로 경계값을 자동으로 안정 범위에 포함하면 안 된다.

점근안정 범위는 보통 열린 구간으로 표현된다.

경계값을 포함할 수 있는지는 해당 근을 직접 검증한 뒤 별도로 결정한다.

---

## 16. 상대안정도

모든 극점이 단순히 좌반평면에 존재하는 것보다 더 왼쪽에 위치하도록 요구할 수 있다.

예를 들어 모든 극점이 다음 조건을 만족해야 한다고 한다.

\[
\operatorname{Re}(s)<-\alpha
\]

단, `α>0`이다.

다음 치환을 사용한다.

\[
z=s+\alpha
\]

즉,

\[
s=z-\alpha
\]

원래 특성다항식 `P(s)`에 `s=z-α`를 대입하여 다음 변환 다항식을 만든다.

\[
P(z-\alpha)
\]

이 변환 다항식이 `z` 평면에서 안정하도록 Routh 판별을 수행하면 원래 극점이 `s` 평면에서 `Re(s)<-α`를 만족하는지 판단할 수 있다.

치환 방향을 반대로 적용하면 상대안정도 영역을 잘못 판정할 수 있다.

---

## 17. 시간지연과 비다항식 시스템

Routh-Hurwitz 판별법은 유한차수 다항식에 직접 적용한다.

다음과 같은 순수 시간지연 항을 포함한 특성방정식은 초월방정식이다.

\[
e^{-Ls}
\]

따라서 시간지연 항을 포함한 원래 특성방정식에 Routh 배열을 직접 적용하면 안 된다.

필요한 경우 다음 방법을 검토한다.

- Padé approximation 후 근사 다항식에 적용
- Nyquist 안정도 판별
- 주파수응답 해석
- 시간지연 안정성 전용 기법
- 수치적 근 계산

Padé approximation을 사용하면 근사 차수에 따라 인공 극점과 영점이 생길 수 있으므로 근사 오차를 명시해야 한다.

---

## 18. 적용 한계

Routh-Hurwitz 판별법의 장점은 다음과 같다.

- 근을 직접 계산하지 않고 안정 여부 판단
- 우반평면 근 개수 계산
- 파라미터와 이득 안정 범위 도출
- 고차 다항식의 대수적 판별
- 계산 절차가 구조적임

한계는 다음과 같다.

- 정확한 극점 위치를 직접 제공하지 않음
- 감쇠비와 고유진동수를 직접 제공하지 않음
- 안정여유의 크기를 직접 제공하지 않음
- 시간지연 초월함수에 직접 적용할 수 없음
- 계수 불확실성과 강인안정성을 직접 보장하지 않음
- 고차 배열은 수치 오차에 민감할 수 있음
- 비선형 시스템의 전역 안정성을 보장하지 않음

따라서 실제 설계에서는 다음과 함께 사용한다.

- Root Locus
- Bode plot
- Nyquist plot
- Gain Margin
- Phase Margin
- 극점 수치 계산
- 시간응답 simulation
- 파라미터 민감도 검토
- Monte Carlo 검증
- 실제 설비 step test

---

## 19. 현장 적용 관점

Routh-Hurwitz 판별법을 현장 제어기에 적용할 때는 다음을 고려한다.

### 19.1 모델 유효성

- 선형화 운전점
- 공정 gain 변화
- 시정수 변화
- dead time
- 밸브 비선형
- sensor filtering
- sampling period
- actuator saturation

### 19.2 안정 범위와 운전 범위

수학적으로 안정한 `K` 범위가 곧바로 현장에서 사용 가능한 범위를 의미하지 않는다.

안정 범위 내부에서도 다음 문제가 발생할 수 있다.

- 낮은 감쇠비
- 과도한 overshoot
- 느린 settling
- actuator saturation
- valve hunting
- sensor noise 증폭
- 충분하지 않은 phase margin
- 운전점 변화에 따른 불안정

따라서 설계 이득은 안정 경계에서 충분히 떨어진 영역을 선택해야 한다.

### 19.3 검증 절차

1. nominal model로 Routh 안정 범위 계산
2. 최소·정상·최대 운전조건 모델 검토
3. 극점 위치 계산
4. Bode 또는 Nyquist 안정여유 확인
5. step response와 disturbance response 확인
6. 포화 및 anti-windup 조건 확인
7. simulation 또는 digital twin 검증
8. 제한된 현장 시험
9. trend monitoring
10. 최종 tuning 확정

---

## 20. Fact Anchor 설계 요구사항

`fact_anchor.json`에는 최소 12개의 anchor를 둔다.

추천 anchor는 다음과 같다.

### Anchor 1. 안정성의 극점 조건

모든 폐루프 극점이 열린 좌반평면에 있어야 점근안정이다.

### Anchor 2. Routh 첫 열의 의미

첫 열 부호 변화 수는 우반평면 근 개수와 같다.

### Anchor 3. 계수 양수 조건의 한계

모든 계수가 양수인 것은 일반적으로 필요조건이지 충분조건이 아니다.

### Anchor 4. 첫 두 행 구성

첫 행과 둘째 행은 특성다항식 계수를 한 항씩 건너 배치한다.

### Anchor 5. 일반 행 계산

이전 두 행을 이용한 교차곱 구조로 다음 행을 계산한다.

### Anchor 6. 첫 열 원소 0 처리

첫 열 원소만 0이면 양의 `ε`로 대체하고 `ε→0+`에서 부호를 판단한다.

### Anchor 7. 한 행 전체 0 처리

바로 위 행으로 보조다항식을 만들고 그 도함수 계수로 0행을 대체한다.

### Anchor 8. 허수축 근

한 행 전체 0은 대칭근과 허수축 근 가능성을 나타내며 점근안정을 별도로 확인해야 한다.

### Anchor 9. 이득 안정 범위

첫 열 부등식의 교집합으로 `K` 범위를 구하고 경계값을 별도 검증한다.

### Anchor 10. 경계값

점근안정 범위의 경계는 허수축 근 또는 원점 근을 가질 수 있어 자동으로 포함하지 않는다.

### Anchor 11. 상대안정도 치환

`Re(s)<-α`를 확인하려면 `s=z-α`를 대입한 다항식에 Routh 판별을 수행한다.

### Anchor 12. 적용 한계

시간지연 초월함수에는 직접 적용할 수 없으며 근사 또는 주파수영역 기법이 필요하다.

추가 anchor로 다음을 허용한다.

- 중복 허수축 근의 불안정성
- Routh 판별은 정확한 근 위치를 제공하지 않음
- 현장 이득 선정은 안정 경계에서 여유를 둬야 함
- 계수 정규화와 부호 convention
- 수치 오차와 symbolic calculation 검증

---

## 21. Model Answer 설계 요구사항

`model_answer.json`의 outline은 8개 항목을 권장한다.

1. 안정도 판별 목적과 특성방정식
2. Routh 배열의 첫 두 행 구성
3. 일반 행 계산과 첫 열 의미
4. 안정 조건과 필요조건·충분조건 구분
5. 첫 열 0과 `ε` 처리
6. 한 행 전체 0과 보조다항식 처리
7. 이득 `K` 범위와 상대안정도 계산
8. 현장 적용, 한계와 다른 안정도 기법 연계

고득점 요소에는 다음이 포함되어야 한다.

- 특성방정식을 정확히 구성
- 첫 열 부호 변화와 우반평면 근 수 연결
- 양의 계수 조건을 충분조건으로 오해하지 않음
- 두 특수 경우를 구분
- 경계값을 별도 검증
- 상대안정도 치환 방향을 정확히 적용
- 시간지연에 직접 적용하지 않음
- 현장 안정여유와 모델 불확실성을 고려

---

## 22. Logic Check 설계 원칙

이번 Topic Pack의 Logic Check는 LLM profile 방식으로 구성한다.

### 22.1 결정론적 정규표현식 검사

사용하지 않는다.

다음 필드는 비활성 또는 빈 배열로 둔다.

- `deterministic_checks.enabled=false`
- deterministic fatal checks: `[]`
- deterministic major checks: `[]`
- deterministic question type rules: `[]`
- candidate extraction rules: `[]`
- fact anchor regex patterns: `[]`

정규표현식으로 수식 표기와 문맥을 직접 판정하지 않는다.

### 22.2 LLM 검증 목적

LLM은 답안에서 각 fatal condition을 개별적으로 검토한다.

단순 키워드 존재 여부가 아니라 다음을 판단한다.

- 실제 주장인지
- 오답을 인용한 것인지
- 오답을 수정하는 문맥인지
- 조건부 가정인지
- 최종 결론이 무엇인지
- 계산 결과와 설명이 일치하는지

---

## 23. Fatal 오개념

LLM profile에는 다음 8개 fatal condition을 둔다.

### 23.1 `routh_sign_changes_left_half_plane`

잘못된 주장:

첫 열 부호 변화 수가 좌반평면 극점 수라고 설명한다.

정확한 원칙:

첫 열 부호 변화 수는 우반평면 극점 수이다.

### 23.2 `positive_coefficients_always_stable`

잘못된 주장:

특성다항식의 모든 계수가 양수이면 항상 안정이라고 단정한다.

정확한 원칙:

양의 계수는 일반적으로 필요조건이며 고차 다항식의 충분조건이 아니다.

### 23.3 `zero_leading_element_same_as_zero_row`

잘못된 주장:

첫 열 원소만 0인 경우와 한 행 전체가 0인 경우를 같은 방법으로 처리한다.

정확한 원칙:

첫 열 원소만 0이면 `ε` 처리하고, 한 행 전체가 0이면 보조다항식과 도함수를 사용한다.

### 23.4 `zero_row_immediately_unstable`

잘못된 주장:

한 행 전체가 0이면 추가 분석 없이 즉시 불안정이라고 판정한다.

정확한 원칙:

보조다항식으로 대칭근과 허수축 근을 분석한 뒤 안정성 종류를 판정해야 한다.

### 23.5 `no_sign_change_always_asymptotically_stable`

잘못된 주장:

첫 열 부호 변화가 없으면 허수축 근 여부와 관계없이 무조건 점근안정이라고 단정한다.

정확한 원칙:

허수축 근 또는 한 행 전체 0이 존재하면 점근안정을 별도로 확인해야 한다.

### 23.6 `routh_entries_are_pole_locations`

잘못된 주장:

Routh 배열의 원소를 실제 극점 좌표라고 설명한다.

정확한 원칙:

Routh 배열은 우반평면 근 개수와 안정 조건을 제공하지만 일반적으로 정확한 근 위치는 제공하지 않는다.

### 23.7 `gain_boundary_always_included`

잘못된 주장:

첫 열 부등식에서 얻은 `K` 경계값을 검증 없이 안정 범위에 포함한다.

정확한 원칙:

경계값은 허수축 근, 원점 근 또는 차수 저하 가능성을 별도로 검증해야 한다.

### 23.8 `direct_routh_on_time_delay`

잘못된 주장:

`e^{-Ls}`가 포함된 초월 특성방정식에 Routh 배열을 직접 적용한다.

정확한 원칙:

Routh 판별은 유한차수 다항식에 적용하며 시간지연은 근사 또는 다른 안정도 기법이 필요하다.

---

## 24. Safe Context 조건

다음 경우에는 fatal로 판정하지 않는다.

1. 오개념을 인용한 뒤 명확히 반박하는 경우
2. 잘못된 풀이 예시를 설명하는 경우
3. 학생 답안의 오류를 교정하는 경우
4. 가정 또는 반례로 제시한 경우
5. 최종 결론에서 정확한 원칙으로 수정한 경우
6. 교재별 부호 convention 차이를 설명하되 결과를 일관되게 적용한 경우
7. 경계값을 임계안정 후보로 제시하고 별도 검증한 경우
8. Padé approximation을 명시하고 근사 다항식에 Routh 판별을 적용한 경우

LLM은 문장 하나만 분리하여 판정하지 않고 주변 문맥과 최종 결론을 함께 확인한다.

---

## 25. LLM 출력 계약

LLM profile의 최상위 출력 필드는 다음을 요구한다.

- `verdict`
- `confidence`
- `reason`
- `checks`
- `findings`

### 25.1 verdict

허용값 예시:

- `pass`
- `warn`
- `fatal`

### 25.2 confidence

0과 1 사이의 유한한 수치로 처리한다.

문자열 수치가 허용되는지는 기존 verifier contract를 따른다.

### 25.3 reason

전체 판정의 핵심 근거를 간결하게 설명한다.

### 25.4 checks

8개 fatal condition 각각에 대한 개별 판정 결과를 포함한다.

각 check는 최소 다음 의미를 제공해야 한다.

- condition ID
- triggered 여부
- evidence
- explanation
- safe context 적용 여부

### 25.5 findings

실제로 발견된 오류만 포함한다.

finding에는 기존 schema가 요구하는 필드를 사용하며 최소한 다음 의미가 보존되어야 한다.

- severity
- message
- evidence
- correct rule
- condition ID
- confidence

---

## 26. Fatal 판정과 점수 정책

Fatal condition이 실제 주장으로 확인되면 다음을 적용한다.

- `fatal_error_detected=true`
- `mode=fatal`
- `THEORY_CORE` 핵심 이론 오류로 표시
- 권장 ceiling은 기존 점수 정책과 reconciler를 통해 적용
- 현재 점수가 ceiling보다 낮으면 추가 수치 cap을 적용하지 않음
- 현재 점수가 ceiling보다 높을 때만 binding cap 적용
- 단순 누락은 fatal로 처리하지 않음
- LLM 실패 시 fail-open diagnostic을 사용하고 fatal로 단정하지 않음

Logic Check는 A/B/C/D/E 점수를 직접 산정하지 않는다.

Logic Check는 다음 역할만 수행한다.

- 핵심 오개념 확인
- D/E claim trust 판단
- fatal ceiling 후보 제공
- 교정 방향 제공

---

## 27. 누락과 오개념 구분

다음은 일반적으로 누락 또는 부족으로 처리한다.

- Routh 배열 계산식 일부 누락
- 상대안정도 설명 누락
- 현장 적용 설명 부족
- 수치 예제 부족
- 다른 안정도 기법과 비교 부족
- Padé approximation 한계 누락
- 경계값 검증 절차를 간단히만 언급
- 수치 오차 검증 누락

다음은 fatal 후보이다.

- 우반평면과 좌반평면 의미 반전
- 양의 계수를 안정 충분조건으로 단정
- 특수 경우 처리법 반전
- 허수축 근을 점근안정으로 판정
- Routh 원소를 극점 위치로 해석
- 경계값을 검증 없이 안정으로 포함
- 시간지연 초월함수에 직접 적용

---

## 28. 채점 관점

고득점 답안은 다음 흐름을 갖는다.

1. 특성방정식과 안정성 정의
2. Routh 배열 구성 원리
3. 첫 열 부호 변화의 의미
4. 일반 안정 조건
5. 첫 열 원소 0 처리
6. 한 행 전체 0 처리
7. `K` 안정 범위 계산
8. 경계값 검증
9. 상대안정도
10. 현장 적용과 한계

단순히 표를 작성하고 `K` 범위만 제시한 답안은 절차 설명과 해석이 부족할 수 있다.

반대로 설명만 하고 실제 첫 열 부등식과 안정 범위를 구하지 않은 답안은 `CALC_DESIGN` 요구 충족도가 낮다.

---

## 29. 현장 연결 키워드

다음 키워드를 자연스럽게 연결한다.

- characteristic equation
- closed-loop pole
- Routh array
- Routh table
- first-column sign change
- right-half-plane pole
- asymptotic stability
- marginal stability
- imaginary-axis pole
- auxiliary polynomial
- epsilon method
- gain range
- controller gain
- relative stability
- shifted axis
- phase margin
- gain margin
- time delay
- Padé approximation
- model uncertainty
- operating point
- actuator saturation
- robust stability
- commissioning
- step test

키워드 나열만으로 고득점으로 판정하지 않는다.

---

## 30. Topic Pack 생성 시 점검사항

JSON 생성 전에 다음을 확인한다.

1. 기존 Topic Pack schema
2. 기존 Topic Pack validator
3. 기존 quality validator
4. generated pipeline builder
5. generated/runtime audit
6. Topic ID 관계
7. question type 허용값
8. topic importance scope
9. LLM profile 출력 계약
10. Logic Check evaluator의 profile-only 처리

JSON 생성 후 다음을 확인한다.

1. source Topic Pack validation
2. Topic Pack quality validation
3. generated pipeline rebuild
4. generated rubric validation
5. topic routing smoke
6. mocked Logic Check fatal/pass regression
7. 실제 LLM profile 최소 smoke
8. Release Validation
9. Rubric Audit
10. 작업 트리와 staged 상태

---

## 31. 완료 기준

다음 조건을 모두 만족해야 Topic Pack 작성이 완료된 것으로 본다.

- 요구사항 Markdown이 사람 검토 가능한 수준으로 완성됨
- Fact Anchor가 핵심 수학 원칙을 포함함
- Model Answer가 계산 절차와 해석을 모두 포함함
- 8개 fatal condition이 개별적으로 정의됨
- safe context가 정의됨
- 결정론적 regex 검사가 비활성화됨
- LLM output contract가 명확함
- source와 generated validator가 통과함
- topic routing이 기존 토픽과 충돌하지 않음
- 실제 LLM profile 경로가 최소 1회 검증됨
- Release Validation과 Rubric Audit이 통과함
- 임시 report와 synthetic session이 정리됨
- 커밋 전 staged 상태가 비어 있음

---

## 32. 다음 작업

이 문서 검토가 끝난 뒤 다음 순서로 진행한다.

1. 기존 Topic Pack schema와 유사 Topic Pack 확인
2. ChatGPT가 5개 source 파일을 직접 작성
3. source validation
4. generated rubric rebuild
5. generated validation
6. focused host tests
7. 필요한 경우 최소 container LLM smoke
8. Release Validation과 Rubric Audit
9. 독립 커밋 생성
10. origin/main push
