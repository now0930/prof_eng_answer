# 제어밸브의 가스·증기 사이징, 팽창계수 및 초크 유동

## 1. Topic 정보

- Topic ID: `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`
- Question Type: `CALC_DESIGN`
- Supported Secondary Type: `PRINCIPLE_INTERPRETATION`
- Supported Tertiary Type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection Importance: `CORE_MUST_PREPARE`
- 주 자료: Control Valve Handbook 제5장, Control Valve Primer 제5장

## 2. 출제 의도

가스·증기 제어밸브는 압축성 유동을 고려해 sizing해야 한다.

좋은 답안은 Cv 식만 나열하지 않는다.

먼저 flow basis를 정의한다.

Pressure와 temperature를 absolute basis로 변환한다.

Gas property를 선정한다.

Pressure-drop ratio와 choked limit를 비교한다.

Expansion factor를 계산한다.

Required capacity와 selected trim travel을 반복 검증한다.

## 3. 적용 대상

이 Topic은 다음 유체를 대상으로 한다.

- Single-phase gas
- Single-phase vapor
- Saturated steam
- Superheated steam

다음 condition은 별도 검토가 필요하다.

- Wet steam
- Two-phase gas-liquid flow
- Condensing vapor
- Solid-containing gas
- Cryogenic flashing service

## 4. Flow Basis

압축성 유체의 flow basis는 반드시 명시한다.

### 4.1 Standard 또는 Normal Volumetric Flow

Base pressure와 base temperature에서 환산한 부피유량이다.

다음을 함께 기록한다.

- Standard 또는 normal 정의
- Base pressure
- Base temperature
- Dry 또는 wet basis
- Gas composition

### 4.2 Actual Volumetric Flow

Valve inlet 또는 지정 operating condition에서의 실제 부피유량이다.

Pressure와 temperature가 변하면 actual volume도 변한다.

### 4.3 Mass Flow

시간당 질량으로 나타낸다.

Standard volume와 같은 숫자로 취급하지 않는다.

## 5. Absolute Pressure와 Temperature

Pressure-drop ratio는 absolute pressure를 사용한다.

\[
x
=
\frac{P_1-P_2}{P_1}
\]

- \(P_1\): inlet absolute pressure
- \(P_2\): outlet absolute pressure
- \(x\): dimensionless pressure-drop ratio

Gauge pressure는 absolute pressure로 변환한다.

\[
P_{\mathrm{abs}}
=
P_{\mathrm{gauge}}
+
P_{\mathrm{atmospheric}}
\]

Upstream temperature도 absolute temperature로 사용한다.

- SI: K
- US customary: °R

Celsius 또는 Fahrenheit 숫자를 그대로 gas equation에 넣지 않는다.

## 6. Gas Properties

다음 property를 확인한다.

- Molecular weight \(M\)
- Gas specific gravity \(G_g\)
- Inlet density \(\rho_1\)
- Specific heat ratio \(\gamma\) 또는 \(k\)
- Compressibility factor \(Z_1\)
- Steam enthalpy·density·quality
- Gas composition

선택한 equation이 요구하는 property set만 사용한다.

\(M\), \(G_g\), \(\rho_1\)를 서로 같은 변수로 취급하지 않는다.

## 7. Compressibility Factor

\(Z_1\)은 inlet condition의 real-gas behavior를 보정한다.

\[
Z_1
=
\frac{P_1 v_1}
{R T_1}
\]

Ideal gas에 가까우면 1에 접근한다.

그러나 모든 gas와 pressure에서 1이라고 단정하지 않는다.

Gas composition, pressure와 temperature에 맞는 property source를 사용한다.

## 8. Specific Heat Ratio와 \(F_\gamma\)

Specific heat ratio는 다음과 같다.

\[
\gamma
=
\frac{C_p}{C_v}
\]

Common IEC·ISA notation에서는 다음 factor를 사용할 수 있다.

\[
F_\gamma
=
\frac{\gamma}{1.4}
\]

\(F_\gamma\)는 choked pressure ratio와 expansion factor에 영향을 준다.

정확한 notation은 적용 standard edition을 확인한다.

## 9. Valve Pressure-Drop-Ratio Factor

### 9.1 \(x_T\)

\(x_T\)는 bare valve의 choked-flow pressure-ratio 특성을 나타낸다.

다음에 따라 달라질 수 있다.

- Valve style
- Trim geometry
- Flow direction
- Travel
- Manufacturer test data

하나의 universal value가 아니다.

### 9.2 \(x_{TP}\)

Reducer, expander 또는 fitting이 valve에 직접 연결되면 assembly의 pressure recovery가 달라진다.

이 경우 \(F_P\)와 fitting-adjusted \(x_{TP}\)를 검토한다.

Attached fitting 영향이 없으면 method가 허용하는 범위에서 다음과 같이 둘 수 있다.

\[
F_P=1
\]

\[
x_{TP}=x_T
\]

## 10. Actual Pressure Ratio

\[
x
=
\frac{\Delta P}{P_1}
\]

\[
\Delta P=P_1-P_2
\]

동일 \(P_1\)에서 \(P_2\)가 감소하면 \(x\)가 증가한다.

\(P_2=P_1\)이면 \(x=0\)이다.

일반 positive-pressure valve service에서는 \(0\le x<1\)이다.

## 11. Choked Pressure-Ratio Limit

Bare valve의 common relation은 다음과 같다.

\[
x_{\mathrm{choked}}
=
F_\gamma x_T
\]

Fitting-adjusted assembly에서는 다음과 같이 표현할 수 있다.

\[
x_{\mathrm{choked}}
=
F_\gamma x_{TP}
\]

Sizing에는 actual ratio와 choked limit 중 작은 값을 사용한다.

\[
x_{\mathrm{sizing}}
=
\min
\left(
x,\,
x_{\mathrm{choked}}
\right)
\]

큰 값을 선택하면 안 된다.

## 12. Expansion Factor

### 12.1 의미

Gas는 valve를 통과하면서 pressure가 감소하고 volume이 팽창한다.

Density도 감소한다.

Expansion factor \(Y\)는 이 영향을 보정한다.

### 12.2 Common Relation

Bare valve의 common form은 다음과 같다.

\[
Y
=
1-
\frac{x_{\mathrm{sizing}}}
{3F_\gamma x_T}
\]

Fitting assembly에서는 \(x_T\) 대신 \(x_{TP}\)를 사용할 수 있다.

### 12.3 방향

\(x_{\mathrm{sizing}}\)이 증가하면 \(Y\)는 감소한다.

\(x=0\)이면 \(Y=1\)이다.

Common relation에서 다음 범위를 갖는다.

\[
\frac{2}{3}
\le
Y
\le
1
\]

Choked limit에서는 다음과 같다.

\[
Y=\frac{2}{3}
\]

## 13. Subcritical Flow

Actual pressure ratio가 choked limit보다 작은 상태이다.

\[
x<x_{\mathrm{choked}}
\]

Downstream pressure가 감소하면 \(x\)가 증가한다.

Flow도 증가한다.

그러나 gas expansion 때문에 \(Y\)는 감소한다.

Flow 증가가 liquid square-root relation과 동일하지는 않다.

## 14. Choked Flow

Actual pressure ratio가 choked limit에 도달하거나 초과한 상태이다.

\[
x\ge x_{\mathrm{choked}}
\]

Sizing에는 다음 값을 사용한다.

\[
x_{\mathrm{sizing}}
=
x_{\mathrm{choked}}
\]

Choked flow는 유량 정지가 아니다.

Valve 내부 제한부에서 compressible-flow limit에 도달한 상태이다.

동일 upstream condition과 valve travel에서 downstream pressure를 더 낮춰도 mass flow가 무한히 증가하지 않는다.

Choked 위치를 항상 valve outlet이라고 단정하지 않는다.

## 15. Gas Sizing Equation Structure

### 15.1 Standard Volume Form

일반 구조는 다음과 같다.

\[
q_s
=
N_s F_P C P_1Y
\sqrt{
\frac{x_{\mathrm{sizing}}}
{M T_1 Z_1}
}
\]

Gas-specific-gravity equation에서는 \(M\) 대신 식이 요구하는 \(G_g\) term을 사용한다.

### 15.2 Mass Flow Form

일반 구조는 다음과 같다.

\[
w
=
N_w F_P C Y
\sqrt{
x_{\mathrm{sizing}}P_1\rho_1
}
\]

### 15.3 Unit Constant

\(N_s\)와 \(N_w\)는 다음에 따라 달라진다.

- Flow unit
- Pressure unit
- Temperature unit
- Cv 또는 Kv
- Molecular weight 또는 density representation
- Standard equation edition

숫자만 외워 혼용하지 않는다.

## 16. Required와 Rated Coefficient

### 16.1 Required Coefficient

Process flow, pressure, temperature와 gas properties를 만족하기 위해 필요한 Cv 또는 Kv이다.

### 16.2 Rated Coefficient

Selected valve와 trim이 제공하는 catalog capacity이다.

Required와 rated value를 동일시하지 않는다.

Corrected required value보다 충분한 rated capacity가 필요하다.

그러나 지나치게 큰 trim은 낮은 normal travel을 만들 수 있다.

## 17. Selected Travel과 반복 계산

\(x_T\)는 travel에 따라 달라질 수 있다.

다음 순서를 사용한다.

1. Initial \(x_T\) 또는 \(x_{TP}\)를 선택한다.
2. Actual pressure ratio \(x\)를 계산한다.
3. Choked limit를 계산한다.
4. \(x_{\mathrm{sizing}}\)을 선택한다.
5. \(Y\)를 계산한다.
6. Initial required Cv를 계산한다.
7. Candidate trim과 travel을 선택한다.
8. Selected travel의 \(x_T\) 또는 \(x_{TP}\)를 확인한다.
9. 달라지면 choked limit, \(Y\)와 required Cv를 다시 계산한다.
10. Required Cv, rated Cv와 travel이 self-consistent할 때까지 반복한다.

## 18. Minimum·Normal·Maximum Case

### 18.1 Minimum Flow

- Low travel
- Positioner resolution
- Minimum controllable flow
- Potential condensation
- Property accuracy

### 18.2 Normal Flow

- Required Cv
- Normal travel
- \(x_T\) at selected travel
- Subcritical 또는 choked regime
- Noise screening

### 18.3 Maximum Flow

- Maximum upstream pressure
- Minimum downstream pressure
- Maximum temperature 또는 density case
- Choked possibility
- High travel margin
- Downstream equipment capacity

## 19. Fail-Open Maximum Flow

Fail-open valve는 정상 maximum flow보다 더 큰 credible flow를 만들 수 있다.

다음을 검토한다.

- Maximum credible \(P_1\)
- Minimum credible \(P_2\)
- Maximum available valve travel
- Rated Cv
- \(x_T\) 또는 \(x_{TP}\)
- Choked condition
- Maximum gas mass flow
- Downstream relief and equipment capacity
- Aerodynamic noise

Relief capacity calculation 자체는 process safety design 범위이다.

## 20. Steam과 Vapor

Single-phase saturated steam 또는 superheated steam은 일관된 property data를 사용한다.

다음을 확인한다.

- Pressure basis
- Temperature
- Saturation state
- Superheat
- Density 또는 specific volume
- Molecular weight
- Specific heat ratio
- Compressibility 또는 steam-table property

Wet steam은 liquid droplets를 포함하는 two-phase flow이다.

Single-phase gas equation을 property 검토 없이 그대로 적용하지 않는다.

## 21. Aerodynamic Noise Handoff

Gas choked flow는 aerodynamic noise 가능성을 높일 수 있다.

Topic 7은 다음을 screening한다.

- Pressure ratio
- Choked condition
- Gas mass flow
- Valve outlet velocity
- Downstream pressure
- Pipe size

상세 noise prediction, Mach interaction, acoustic efficiency와 low-noise trim은 Topic 9가 소유한다.

## 22. 선정 절차

1. Gas, vapor 또는 steam service를 정의한다.
2. Flow basis를 확정한다.
3. Standard condition을 기록한다.
4. \(P_1\), \(P_2\)를 absolute pressure로 변환한다.
5. \(T_1\)을 absolute temperature로 변환한다.
6. \(M\), \(G_g\), \(\rho_1\), \(\gamma\), \(Z_1\)을 확인한다.
7. Actual pressure ratio \(x\)를 계산한다.
8. Candidate valve의 \(x_T\)를 확인한다.
9. Attached fitting이 있으면 \(F_P\)와 \(x_{TP}\)를 계산한다.
10. Choked limit를 계산한다.
11. \(x_{\mathrm{sizing}}\)을 선택한다.
12. Expansion factor \(Y\)를 계산한다.
13. Flow basis에 맞는 equation과 \(N\) constant를 선택한다.
14. Required Cv 또는 Kv를 계산한다.
15. Candidate trim과 travel을 확인한다.
16. Selected travel의 \(x_T/x_{TP}\)로 반복 계산한다.
17. Minimum·normal·maximum case를 검증한다.
18. Fail-open maximum flow를 검증한다.
19. Steam phase와 property validity를 확인한다.
20. Aerodynamic noise 검토 필요성을 판단한다.
21. Vendor result를 hand calculation으로 교차검증한다.
22. Selected trim과 service limitation을 문서화한다.

## 23. 대표 오답

- Gauge pressure를 pressure ratio에 그대로 사용한다.
- \(x=\Delta P/P_2\)이다.
- Standard volume와 actual volume는 항상 같다.
- Celsius 숫자를 \(T_1\)에 그대로 사용한다.
- 모든 gas에서 \(Z_1=1\)이다.
- 모든 gas에서 \(F_\gamma=1\)이다.
- \(x_T\)는 모든 valve에서 같다.
- \(x_T\)는 travel과 무관하다.
- Fitting이 있어도 \(x_{TP}=x_T\)이다.
- Actual \(x\)와 choked limit 중 큰 값을 사용한다.
- Pressure ratio가 증가하면 \(Y\)도 증가한다.
- Choked 이후 \(Y\)를 2/3보다 계속 낮춘다.
- Choked flow는 유량이 0이다.
- Choked 이후 downstream pressure를 낮추면 flow가 계속 비례 증가한다.
- Gas에 liquid Cv equation을 그대로 사용한다.
- Gas capacity는 \(P_1\)과 무관하다.
- Required Cv와 rated Cv는 같은 값이다.
- Normal flow 한 점만 계산하면 된다.
- Wet steam에 dry-gas equation을 그대로 적용한다.

## 24. 고득점 답안 기준

고득점 답안은 다음 순서를 가진다.

1. Flow basis와 standard condition을 구분한다.
2. Pressure와 temperature를 absolute basis로 변환한다.
3. Gas properties를 정의한다.
4. \(x=\Delta P/P_1\)을 계산한다.
5. \(F_\gamma\)와 \(x_T/x_{TP}\)를 확인한다.
6. Actual ratio와 choked limit 중 작은 값을 선택한다.
7. \(Y\)의 감소 방향과 2/3 lower bound를 설명한다.
8. Flow basis에 맞는 gas equation을 선택한다.
9. Units와 \(N\) constant를 일치시킨다.
10. Required와 rated coefficient를 구분한다.
11. Selected travel의 \(x_T\)로 반복 계산한다.
12. Minimum·normal·maximum case를 검증한다.
13. Fail-open maximum flow를 검증한다.
14. Steam phase와 property validity를 확인한다.
15. Noise screening과 Topic 9 hand-off를 설명한다.
16. Vendor result를 hand calculation으로 교차 검증한다.

## 25. 인접 Topic 경계

- Actuator force와 fail-safe: Topic 1
- Characteristic 형상: Topic 2
- Deadband·stiction·response: Topic 3
- Valve body·actuator 종류: Topic 4
- Authority·rangeability·installed gain: Topic 5
- Liquid Cv·Kv와 Reynolds correction: Topic 6
- Liquid cavitation·flashing·choked: Topic 8
- Aerodynamic noise와 low-noise trim: Topic 9
- Balanced·unbalanced trim: Topic 10
- Severe-service material: Topic 14
- 전체 package workflow: Topic 16

## 26. 작성 원칙

- Flow basis를 먼저 정의한다.
- Gauge pressure를 pressure ratio에 사용하지 않는다.
- Celsius·Fahrenheit 숫자를 \(T_1\)로 직접 사용하지 않는다.
- \(x\)와 choked limit 중 작은 값을 사용한다.
- \(Y\)의 감소 방향을 지킨다.
- Choked flow를 zero flow로 설명하지 않는다.
- Standard-volume·actual-volume·mass-flow equation을 혼용하지 않는다.
- Exact \(N\) constant는 units와 함께 사용한다.
- \(x_T\)를 universal constant로 취급하지 않는다.
- Attached fitting이 있으면 \(F_P\)와 \(x_{TP}\)를 검토한다.
- Selected travel에서 \(x_T\)가 바뀌면 반복 계산한다.
- Wet steam은 별도 two-phase 검토를 수행한다.
- Topic 8 liquid choked와 Topic 9 aerodynamic noise를 분리한다.
- Vendor software 결과를 input sheet와 hand calculation으로 확인한다.
