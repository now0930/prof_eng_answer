# 제어밸브의 Authority·Rangeability·Installed Gain 및 공정 성능

## 1. Topic 정보

- Topic ID: `control_valve_authority_rangeability_gain_installed_performance`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Supported Secondary Type: `CALC_DESIGN`
- Difficulty: `THEORY_CORE`
- Selection Importance: `CORE_MUST_PREPARE`
- 주 자료: Control Valve Handbook 제2장

## 2. 출제 의도

제어밸브의 성능은 고유 특성만으로 결정되지 않는다.

밸브는 배관계와 제어루프에 설치된다.

유량이 변하면 밸브와 배관의 차압 분배가 달라진다.

그 결과 installed characteristic와 installed gain이 변한다.

좋은 답안은 Authority, rangeability, installed gain과 process gain을 하나의 흐름으로 연결한다.

## 3. Valve Authority

### 3.1 물리적 의미

Valve Authority는 정의한 운전점에서 시스템의 가변 차압 중 밸브가 담당하는 비율이다.

밸브가 유량 변화에 영향을 줄 수 있는 상대적 여유를 나타낸다.

### 3.2 단순 직렬계의 식

단순한 직렬 배관계의 설계점에서는 다음과 같이 표현할 수 있다.

\[
a_v =
\frac{\Delta P_{v,d}}
{\Delta P_{v,d}+\Delta P_{s,d}}
\]

- \(\Delta P_{v,d}\): 설계 유량의 밸브 차압
- \(\Delta P_{s,d}\): 밸브를 제외한 가변 시스템 저항의 설계점 차압

이 식을 적용하기 전에 시스템 경계를 정의해야 한다.

Static head, pump curve, bypass와 parallel branch가 있으면 가용 차압의 변화를 별도로 검토한다.

### 3.3 낮은 Authority의 영향

Authority가 낮으면 밸브 차압의 비중이 작다.

유량 변화에 따라 배관 마찰손실의 비중이 크게 달라진다.

밸브 travel과 실제 유량의 관계가 고유 특성에서 왜곡된다.

Installed gain의 변화도 커질 수 있다.

특정 Authority 숫자를 모든 계통의 합격 기준으로 사용하지 않는다.

## 4. Pressure-drop redistribution

배관 마찰손실은 일반적으로 유량에 따라 증가한다.

최대 유량에서는 배관 손실이 커질 수 있다.

밸브에 남는 차압은 감소할 수 있다.

낮은 유량에서는 배관 손실이 작아진다.

밸브 차압은 증가할 수 있다.

따라서 밸브 차압을 항상 일정하다고 가정하면 installed performance를 잘못 예측할 수 있다.

## 5. Oversizing과 Installed Performance

Oversized valve는 요구 유량을 낮은 travel에서 처리한다.

정상 운전 개도가 너무 낮아질 수 있다.

Travel의 작은 변화가 큰 유량 변화를 만들 수 있다.

Deadband와 resolution의 상대적 영향도 커질 수 있다.

동일 유량에서 밸브 저항이 지나치게 작으면 밸브 차압과 Authority가 낮아질 수 있다.

개선 방법은 다음과 같다.

- Valve size 재검토
- Reduced-capacity trim 적용
- Trim \(C_v\) 재선정
- Characteristic 재검토
- System pressure allocation 검토
- Minimum·normal·maximum 운전점 재검증

정량 required \(C_v\) 계산은 별도 Topic에서 다룬다.

## 6. Inherent Gain과 Installed Gain

### 6.1 Inherent valve gain

밸브 차압을 일정하게 유지한 시험조건에서 travel 대비 유량 변화의 기울기이다.

\[
K_{v,\mathrm{inh}} =
\frac{d(q/q_r)}
{d(x/x_r)}
\bigg|_{\Delta P_v=\mathrm{constant}}
\]

고유 특성의 국부 기울기를 의미한다.

### 6.2 Installed valve gain

실제 계통에서 travel 대비 실제 유량 변화의 국부 기울기이다.

\[
K_{v,\mathrm{inst}} =
\frac{d(q/q_r)}
{d(x/x_r)}
\bigg|_{\mathrm{installed\ system}}
\]

밸브 차압과 system resistance가 변하므로 운전점에 따라 달라진다.

### 6.3 비교

| 구분 | Inherent gain | Installed gain |
|---|---|---|
| 차압 | 일정하게 유지 | 시스템에 따라 변화 |
| 출력 | 고유 유량 또는 \(C_v\) | 실제 설치 유량 |
| 목적 | Trim 고유 특성 평가 | 실제 공정 민감도 평가 |
| 운전점 영향 | 고유 곡선의 위치에 따라 변화 | 고유 곡선과 차압 분배에 따라 변화 |
| 적용 | 밸브 자체 비교 | 루프 성능과 sizing 검증 |

## 7. Process Gain과 Loop Gain

Process gain은 조작량 변화에 대한 공정변수 변화의 비이다.

유량, 부하와 운전조건에 따라 달라질 수 있다.

정규화한 정적 근사에서는 다음과 같이 해석할 수 있다.

\[
K_{\mathrm{loop}}
\approx
K_c K_a K_{v,\mathrm{inst}} K_p K_m
\]

Loop gain은 valve gain 하나로 결정되지 않는다.

Installed valve gain과 process gain이 서로 보상되면 전체 loop gain 변화를 줄일 수 있다.

한 운전점에서만 controller를 tuning하면 다른 운전점에서 과민하거나 둔감할 수 있다.

## 8. Equal-percentage와 Gain Compensation

Equal-percentage characteristic는 travel이 증가할수록 고유 유량 증가량도 커지는 특성이다.

실제 배관계에서는 유량이 증가할수록 밸브 차압이 줄어들 수 있다.

공정 gain도 운전점에 따라 달라질 수 있다.

이 변화가 적절히 결합되면 installed flow characteristic와 loop gain을 더 균일하게 만들 수 있다.

그러나 모든 공정에서 완전한 보상을 보장하지 않는다.

실제 installed flow curve와 gain curve로 확인해야 한다.

## 9. Control Range

Control range는 정의한 성능 허용 기준 안에서 제어 가능한 운전 범위이다.

다음 조건을 사용할 수 있다.

- Installed gain의 허용 범위
- Loop stability와 response
- 반복 가능한 valve motion
- Measurement resolution
- Minimum controllable flow
- Maximum required flow

특정 gain ratio 또는 숫자를 보편적 국제 기준으로 단정하지 않는다.

## 10. Rangeability

### 10.1 Rated 또는 inherent rangeability

명시된 시험조건에서 최대 제어 가능 유량계수와 최소 제어 가능 유량계수의 비이다.

\[
R_v =
\frac{C_{v,\max,\mathrm{controllable}}}
{C_{v,\min,\mathrm{controllable}}}
\]

Travel ratio가 아니다.

Rated \(C_v\) 하나만으로 정해지는 값도 아니다.

### 10.2 Installed rangeability

실제 계통에서 제어 가능한 최대 유량과 최소 유량의 비이다.

\[
R_{\mathrm{inst}} =
\frac{Q_{\max,\mathrm{controllable}}}
{Q_{\min,\mathrm{controllable}}}
\]

가변 차압, 배관 저항, actuator·valve 성능과 측정 한계의 영향을 받는다.

Catalog rangeability와 같다고 가정하지 않는다.

### 10.3 Process turndown

Process turndown은 공정이 요구하는 최대 운전량과 최소 운전량의 비이다.

밸브의 rated rangeability가 충분해도 installed rangeability가 공정 turndown을 만족하지 못할 수 있다.

## 11. Minimum Controllable Flow

최소 제어 가능 유량은 단순히 seat leakage로 결정되지 않는다.

다음 요소를 함께 검토한다.

- Trim의 최소 안정 유로
- Reynolds number와 유동 상태
- Actuator·valve resolution
- Deadband
- Stiction
- Position feedback
- Measurement range와 noise
- Process disturbance
- 낮은 travel의 installed gain

Seat leakage가 작아도 조절 가능한 최소 유량은 0이 아니다.

Shutoff와 throttling 성능을 구분한다.

## 12. 운전점 검증

### 12.1 Minimum flow

- Travel이 deadband와 resolution보다 충분히 큰지 확인한다.
- Installed gain이 지나치게 크지 않은지 확인한다.
- Leakage와 minimum controllable flow를 구분한다.

### 12.2 Normal flow

- 정상 travel이 지나치게 낮지 않은지 확인한다.
- Valve pressure drop와 Authority를 확인한다.
- Controller tuning의 기준 운전점을 정한다.

### 12.3 Maximum flow

- 필요한 유량을 확보하는지 확인한다.
- 밸브 travel 여유가 있는지 확인한다.
- 밸브 차압이 너무 작아지지 않는지 확인한다.
- Pump와 system resistance를 함께 검토한다.

## 13. 진단 흐름

1. Minimum·normal·maximum flow와 pressure를 수집한다.
2. 각 운전점의 valve pressure drop를 계산한다.
3. 정의한 시스템 경계로 Authority를 평가한다.
4. Required \(C_v\)와 actual travel을 확인한다.
5. Installed flow curve를 작성한다.
6. Installed gain curve를 계산한다.
7. Process gain과 loop gain 변화를 비교한다.
8. Rated rangeability와 installed rangeability를 구분한다.
9. Process turndown 충족 여부를 확인한다.
10. Resize, reduced trim 또는 system 변경 후 재검증한다.

## 14. 개선 방법

### 14.1 Valve 측 개선

- Valve 또는 trim capacity 재선정
- Reduced-capacity trim 적용
- Characteristic 변경
- Low-flow trim 검토
- Actuator·positioner resolution 개선

### 14.2 System 측 개선

- Pump head와 control valve pressure allocation 재검토
- Bypass와 parallel branch 운전 검토
- 불필요한 restriction 제거 또는 재배치
- 운전 mode별 system curve 작성

### 14.3 Control 측 개선

- 운전범위별 loop gain 확인
- Controller tuning 재검토
- Gain scheduling 또는 mode별 tuning 검토
- Measurement range와 resolution 개선

Controller tuning은 잘못된 valve size와 Authority를 대신하지 않는다.

## 15. 대표 오답

- Authority는 valve opening 비율이다.
- Authority는 시스템 경계 없이 계산할 수 있다.
- 모든 배관계에 동일한 Authority 목표값을 적용한다.
- 낮은 Authority는 installed characteristic에 영향을 주지 않는다.
- 큰 valve일수록 항상 제어가 좋다.
- Installed gain은 inherent gain과 같다.
- Installed gain은 전체 travel에서 일정하다.
- Equal-percentage는 모든 공정에서 loop gain을 완전히 일정하게 만든다.
- Loop gain은 valve gain 하나로 결정된다.
- Rangeability는 travel ratio이다.
- Catalog rangeability와 installed rangeability는 같다.
- Rangeability와 process turndown은 같다.
- Zero leakage이면 minimum controllable flow도 zero이다.
- Controller tuning만으로 oversizing을 해결할 수 있다.
- 설계 유량 한 점만 확인하면 전체 운전범위가 검증된다.

## 16. 고득점 답안 기준

고득점 답안은 다음 순서를 가진다.

1. Valve Authority를 시스템 경계와 함께 정의한다.
2. Pressure-drop redistribution을 설명한다.
3. 낮은 Authority와 oversizing의 영향을 연결한다.
4. Inherent gain과 installed gain을 구분한다.
5. Process gain과 loop gain을 연결한다.
6. Equal-percentage의 보상 원리와 한계를 설명한다.
7. Rated rangeability, installed rangeability와 process turndown을 구분한다.
8. Minimum·normal·maximum 운전점으로 검증한다.
9. Valve·system·control 개선안을 제시한다.
10. Installed flow curve와 gain curve로 결론을 검증한다.

## 17. 인접 Topic 경계

- Unbalanced force와 actuator sizing: Topic 1
- Inherent·installed characteristic 형상: Topic 2
- Deadband·stiction·response time: Topic 3
- Valve body와 actuator 종류: Topic 4
- Cv·Kv와 liquid sizing: Topic 6
- Gas sizing과 choked flow: Topic 7
- Cavitation과 flashing: Topic 8
- Balanced·unbalanced trim: Topic 10
- Positioner와 accessories: Topic 11
- 전체 valve package 선정 workflow: Topic 16

## 18. 작성 원칙

- Authority 식은 시스템 경계와 설계점을 함께 쓴다.
- 특정 Authority 숫자를 보편 기준으로 고정하지 않는다.
- Inherent gain과 installed gain을 구분한다.
- Rangeability와 process turndown을 구분한다.
- Catalog 값보다 installed performance를 우선 검증한다.
- Oversizing을 body size 하나만으로 판단하지 않는다.
- Minimum·normal·maximum 운전점을 모두 평가한다.
- 결론은 installed flow curve와 gain curve로 검증한다.
