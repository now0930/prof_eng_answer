# 2차 시스템 주파수응답과 공진주파수 Topic Sheet

## 1. Topic metadata

- topic_id: second_order_system_resonance_frequency_response
- question_type: PRINCIPLE_INTERPRETATION
- representative_question: 표준 2차 시스템의 주파수응답과 공진주파수를 설명하시오.
- aliases:
  - 2차 시스템 주파수응답
  - 2차계 주파수응답
  - 공진주파수
  - resonance frequency
  - resonant peak
  - second order system frequency response
  - damping ratio resonance
  - ωr
  - Mr
  - bandwidth
  - Bode plot
  - frequency response

## 2. Core correct facts

- 표준 2차 시스템 전달함수는 `G(s)=Kωn²/(s²+2ζωn s+ωn²)`로 표현할 수 있다.
- 주파수응답은 `s=jω`를 대입하여 해석한다.
- 정규화 주파수비는 `r=ω/ωn`이다.
- 정규화 magnitude는 `|G(jω)|/K = 1/sqrt((1-r²)²+(2ζr)²)`로 표현할 수 있다.
- 공진 peak는 감쇠비가 충분히 작을 때만 발생한다.
- 공진주파수는 `ωr=ωn√(1-2ζ²)`이다.
- 공진주파수 존재 조건은 `0≤ζ<1/√2`이다.
- `ζ≥1/√2`이면 magnitude가 단조 감소하여 뚜렷한 공진 peak가 없다.
- resonant peak는 `Mr=1/(2ζ√(1-ζ²))`로 표현할 수 있다.
- 유한한 resonant peak는 보통 `0<ζ<1/√2`에서 다룬다.
- 감쇠비가 증가하면 resonant peak는 감소한다.
- 감쇠비가 작을수록 공진 peak가 커지고 특정 주파수 대역에서 진동과 노이즈 증폭 위험이 커진다.
- `ωd=ωn√(1-ζ²)`는 시간응답의 감쇠진동수이다.
- `ωr=ωn√(1-2ζ²)`는 주파수응답의 공진주파수이다.
- 따라서 `ωd`와 `ωr`는 다른 개념이다.
- 시간응답 overshoot 조건은 일반적으로 `0<ζ<1`이다.
- 주파수응답 resonance peak 조건은 `0<ζ<1/√2`이다.
- overshoot와 resonance는 관련은 있지만 동일한 조건으로 판단하면 안 된다.
- `ωr≈ωn`은 감쇠비가 매우 작을 때의 근사로는 허용된다.
- resonance frequency와 natural frequency는 항상 같은 것이 아니다.
- 현장에서는 기계 진동, 구조물 공진, 센서 동특성, 노이즈 증폭, 제어루프 bandwidth, PID 튜닝과 연결된다.

## 3. Acceptable answer expressions

### Formula expressions

- `G(s)=Kωn²/(s²+2ζωn s+ωn²)`
- `s=jω`
- `r=ω/ωn`
- `|G(jω)|/K = 1/sqrt((1-r²)²+(2ζr)²)`
- `ωr=ωn√(1-2ζ²)`
- `0≤ζ<1/√2`
- `ζ<0.707`
- `Mr=1/(2ζ√(1-ζ²))`
- `ωd=ωn√(1-ζ²)`

### Natural-language expressions

- 감쇠비가 `1/√2`보다 작을 때 공진 peak가 존재한다.
- 감쇠비가 증가하면 공진 peak가 낮아진다.
- `ζ≥1/√2`에서는 뚜렷한 공진 peak가 없다.
- 공진주파수는 자연주파수보다 낮아질 수 있다.
- 감쇠가 매우 작으면 `ωr`는 `ωn`에 가까워진다.
- 시간응답의 감쇠진동수와 주파수응답의 공진주파수는 다르다.
- overshoot 조건과 resonance 조건은 다르다.
- Bode magnitude plot에서 감쇠비가 작을수록 peak가 크게 나타난다.
- 현장에서는 특정 주파수에서 진동이나 노이즈가 증폭될 수 있으므로 공진을 회피해야 한다.

## 4. Fatal wrong claims

### id: resonance_at_zeta_one

- wrong claim: `ζ=1`을 공진 조건 또는 공진 peak 발생 조건으로 설명한다.
- why fatal: `ζ=1`은 시간응답의 임계감쇠 조건이며, 주파수응답에서 공진 peak 발생 조건이 아니다.
- examples:
  - `ζ=1에서 공진이 발생한다.`
  - `임계감쇠가 공진 조건이다.`
  - `ζ=1일 때 공진주파수가 정의된다.`
- expected cap: 10.0

### id: omega_r_as_damped_natural_frequency

- wrong claim: `ωr=ωn√(1-ζ²)`를 공진주파수로 정의한다.
- why fatal: `ωn√(1-ζ²)`는 시간응답의 감쇠진동수 `ωd`이고, 공진주파수 `ωr`는 `ωn√(1-2ζ²)`이다.
- examples:
  - `공진주파수는 ωn√(1-ζ²)이다.`
  - `ωr=ωd=ωn√(1-ζ²)`
  - `감쇠진동수와 공진주파수는 같다.`
- expected cap: 10.0

### id: resonance_for_all_damping_ratios

- wrong claim: 모든 감쇠비에서 공진 peak 또는 공진주파수가 존재한다고 설명한다.
- why fatal: 공진 peak와 `ωr`는 `ζ<1/√2` 조건에서만 정의된다.
- examples:
  - `모든 2차계에는 공진주파수가 있다.`
  - `감쇠비와 관계없이 공진 peak가 존재한다.`
  - `ζ≥1/√2에서도 공진 peak가 발생한다.`
- expected cap: 10.0

### id: zeta_one_over_sqrt_two_as_critical_damping

- wrong claim: `ζ=1/√2` 또는 `ζ≈0.707`을 임계감쇠로 설명한다.
- why fatal: `ζ=1/√2`는 공진 peak가 사라지는 경계 조건이고, 임계감쇠는 `ζ=1`이다.
- examples:
  - `ζ=0.707은 임계감쇠이다.`
  - `ζ=1/√2에서 중근이 된다.`
  - `ζ=1/√2가 critical damping이다.`
- expected cap: 10.0

### id: omega_r_always_equals_omega_n

- wrong claim: 공진주파수 `ωr`가 자연주파수 `ωn`과 항상 같다고 설명한다.
- why fatal: `ωr=ωn√(1-2ζ²)`이므로 감쇠가 있으면 일반적으로 `ωr<ωn`이다. `ωr≈ωn`은 감쇠가 매우 작은 경우의 근사일 뿐이다.
- examples:
  - `공진주파수는 항상 자연주파수와 같다.`
  - `ωr=ωn은 모든 2차계에서 성립한다.`
- expected cap: 10.0

### id: overshoot_condition_as_resonance_condition

- wrong claim: 시간응답 overshoot 조건 `0<ζ<1`을 주파수응답 resonance 조건으로 그대로 설명한다.
- why fatal: overshoot 조건과 resonant peak 조건은 다르며, resonance peak 조건은 `0<ζ<1/√2`이다.
- examples:
  - `0<ζ<1이면 공진 peak가 존재한다.`
  - `부족감쇠이면 항상 공진이 발생한다.`
  - `overshoot가 있으면 반드시 resonant peak가 있다.`
- expected cap: 10.0

## 5. Warn-level weak claims

### id: missing_resonance_existence_condition

- weak claim: `ωr=ωn√(1-2ζ²)` 공식은 썼지만 `ζ<1/√2` 존재 조건을 누락한다.
- why weak: 공식의 적용 범위를 설명하지 않아 주파수응답 해석이 불완전하다.
- scoring impact: major 또는 minor

### id: missing_magnitude_response_formula

- weak claim: 공진주파수만 설명하고 magnitude 식 또는 주파수비 `r=ω/ωn`를 설명하지 않는다.
- why weak: 주파수응답에서 공진 peak가 어떻게 도출되는지 설명이 부족하다.
- scoring impact: minor

### id: weak_time_frequency_distinction

- weak claim: 시간응답과 주파수응답의 차이를 구분하지 않는다.
- why weak: `ωd`, `ωr`, overshoot, resonance의 개념 혼동 위험이 크다.
- scoring impact: major

### id: missing_field_application

- weak claim: 기계 진동, 센서 노이즈, bandwidth, 제어루프 튜닝 등 현장 적용을 설명하지 않는다.
- why weak: 기술사 답안의 D/E 영역 설득력이 낮아진다.
- scoring impact: minor

## 6. False positive cautions

- `ζ=1`을 시간응답의 임계감쇠로 설명하는 것은 정상이다.
- `ζ=1`을 공진 조건으로 설명할 때만 fatal이다.
- `ωd=ωn√(1-ζ²)`를 시간응답의 감쇠진동수로 설명하는 것은 정상이다.
- `ωd`를 공진주파수라고 부르거나 `ωr`와 동일시할 때만 fatal이다.
- `ωr≈ωn`은 감쇠비가 매우 작을 때의 근사 설명이면 허용 가능하다.
- `ζ≈0.707`을 공진 peak가 사라지는 경계 조건으로 설명하면 정상이다.
- `ζ≈0.707`을 임계감쇠 또는 중근 조건으로 설명하면 오류이다.
- overshoot와 resonance의 관련성을 언급하는 것은 정상이다.
- overshoot 조건 `0<ζ<1`과 resonance 조건 `0<ζ<1/√2`를 동일시하면 오류이다.
- Bode plot 그림만 있고 설명이 모호한 경우에는 그림 위치만으로 fatal 처리하지 않는다.

## 7. Regex candidate patterns

### id: resonance_at_zeta_one

- `ζ\s*=\s*1.{0,60}공진`
- `zeta\s*=\s*1.{0,60}resonan`
- `임계\s*감쇠.{0,60}공진`
- `critical\s*damp.{0,60}resonan`

### id: omega_r_as_damped_natural_frequency

- `ωr\s*=\s*ωn\s*(?:√|sqrt)\s*\(?\s*1\s*-\s*ζ\s*(?:\^|²|2)`
- `omega\s*r.{0,40}omega\s*n.{0,40}sqrt.{0,20}1\s*-\s*zeta`
- `공진\s*주파수.{0,80}ωn\s*(?:√|sqrt)\s*\(?\s*1\s*-\s*ζ`
- `ωd.{0,40}ωr.{0,40}(?:같|동일)`
- `감쇠\s*진동수.{0,60}공진\s*주파수.{0,40}(?:같|동일)`

### id: resonance_for_all_damping_ratios

- `모든\s*감쇠비.{0,60}공진`
- `감쇠비.{0,40}관계\s*없이.{0,40}공진`
- `all\s*damping\s*ratio.{0,60}resonan`
- `ζ\s*>=?\s*1\s*/?\s*√?\s*2.{0,60}공진`
- `ζ\s*≥\s*1\s*/\s*√2.{0,60}공진`

### id: zeta_one_over_sqrt_two_as_critical_damping

- `ζ\s*=\s*1\s*/\s*√2.{0,60}임계\s*감쇠`
- `ζ\s*≈\s*0\.707.{0,60}임계\s*감쇠`
- `0\.707.{0,60}critical\s*damp`
- `1\s*/\s*sqrt\s*\(?2\)?.{0,60}critical\s*damp`
- `ζ\s*=\s*1\s*/\s*√2.{0,60}중근`

### id: omega_r_always_equals_omega_n

- `ωr\s*=\s*ωn.{0,40}(?:항상|언제나|always)`
- `공진\s*주파수.{0,60}자연\s*주파수.{0,40}(?:같|동일)`
- `resonance\s*frequency.{0,60}natural\s*frequency.{0,40}(?:same|equal)`
- `ωr.{0,40}ωn.{0,40}always`

### id: overshoot_condition_as_resonance_condition

- `0\s*<\s*ζ\s*<\s*1.{0,60}공진`
- `부족\s*감쇠.{0,60}항상.{0,40}공진`
- `underdamped.{0,60}always.{0,40}resonan`
- `overshoot.{0,60}반드시.{0,40}공진`
- `오버\s*슈트.{0,60}공진\s*peak.{0,40}조건`

## 8. fact_anchor.json generation guidance

fact_anchor.json은 다음 anchor를 포함해야 한다.

- 표준 2차 전달함수와 주파수응답 대입 `s=jω`
- 정규화 주파수비 `r=ω/ωn`
- magnitude response 식
- 공진주파수 `ωr=ωn√(1-2ζ²)`
- 공진 peak 존재 조건 `ζ<1/√2`
- resonant peak `Mr`
- 감쇠비 증가에 따른 peak 감소
- `ωn`, `ωd`, `ωr`의 구분
- 시간응답 overshoot 조건과 주파수응답 resonance 조건의 차이
- 현장 적용: 기계 진동, 노이즈 증폭, bandwidth, 제어루프 튜닝

표와 다이어그램은 claim을 추출해서 evidence로 인정한다. Bode plot, magnitude curve, pole diagram 자체가 아니라 라벨과 설명이 말하는 내용을 fact evidence로 본다.

## 9. logic_check.json generation guidance

logic_check.json은 다음 deterministic fatal checks를 포함해야 한다.

- `ζ=1`을 공진 조건으로 설명
- `ωr=ωn√(1-ζ²)`를 공진주파수로 설명
- `ωd`와 `ωr`를 동일시
- 모든 감쇠비에서 공진 peak가 존재한다고 설명
- `ζ≥1/√2`에서도 공진 peak가 있다고 설명
- `ζ=1/√2` 또는 `ζ≈0.707`을 임계감쇠 또는 중근 조건으로 설명
- `ωr=ωn`이 항상 성립한다고 설명
- overshoot 조건 `0<ζ<1`을 resonance 조건으로 그대로 사용

warn checks는 다음을 포함한다.

- `ζ<1/√2` 조건 누락
- magnitude 식 또는 주파수비 누락
- 시간응답과 주파수응답 구분 부족
- 현장 적용 부족

safe conditions는 false positive caution을 반영해야 한다.

LLM verifier는 표, Bode plot sketch, ASCII diagram에서 claim을 추출하되, 그림 위치만으로 fatal 판정하지 않아야 한다.

## 10. model_answer.json generation guidance

model_answer.json은 다음 구조를 반영해야 한다.

1. 표준 2차 전달함수 제시
2. `s=jω` 대입과 magnitude response 설명
3. 정규화 주파수비 `r=ω/ωn` 설명
4. 공진주파수 `ωr=ωn√(1-2ζ²)` 도출 또는 제시
5. 공진 peak 존재 조건 `ζ<1/√2` 설명
6. resonant peak와 감쇠비 관계 설명
7. `ωn`, `ωd`, `ωr` 구분
8. overshoot와 resonance 구분
9. Bode plot 또는 magnitude curve 해석
10. 현장 적용: 진동, 노이즈, bandwidth, 제어루프 튜닝

고득점 답안은 공식 암기가 아니라 주파수응답 해석과 현장 설계 판단을 연결해야 한다.

## 11. topic_importance.json generation guidance

이 topic은 제어이론의 핵심 변별 topic이다.

중요도 판단:

- 표준 2차계의 주파수응답 해석 능력을 본다.
- 시간응답과 주파수응답의 개념 구분 능력을 본다.
- 감쇠비가 공진 peak와 bandwidth에 미치는 영향을 설명할 수 있어야 한다.
- 공진 회피, 노이즈 증폭 억제, 제어루프 bandwidth 설계로 연결할 수 있어야 한다.

high-band unlock 조건:

- magnitude response 식과 `r=ω/ωn` 설명
- `ωr=ωn√(1-2ζ²)`와 `ζ<1/√2` 조건
- `ωd`와 `ωr` 구분
- overshoot와 resonance 조건 구분
- 현장 trade-off 설명

fatal cap 정책:

- `ωr`와 `ωd` 혼동
- `ζ=1`을 공진 조건으로 설명
- `ζ=1/√2`를 임계감쇠로 설명
- 모든 감쇠비에서 공진 peak가 있다고 설명
- `ωr=ωn`이 항상 성립한다고 설명

## 12. Human review checklist

- topic_id가 `second_order_system_resonance_frequency_response`로 되어 있는가?
- 시간응답 감쇠비별 분류 topic과 혼동되지 않았는가?
- `ωr=ωn√(1-2ζ²)`가 공진주파수로 명확히 제시되었는가?
- `ζ<1/√2` 존재 조건이 명확한가?
- `ωd=ωn√(1-ζ²)`와 `ωr`가 구분되었는가?
- overshoot 조건과 resonance 조건이 구분되었는가?
- `ζ=1/√2`를 임계감쇠로 잘못 설명하지 않았는가?
- `ωr≈ωn` 근사 설명을 오탐하지 않도록 false positive가 있는가?
- 표와 다이어그램은 claim 중심으로 평가하도록 되어 있는가?
- fatal rule과 warn rule이 구분되어 있는가?
- 현장 적용이 기계 진동, 센서 노이즈, bandwidth, 제어루프 튜닝과 연결되는가?
