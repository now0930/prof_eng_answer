# 제어밸브의 Cv·Kv, 액체 사이징, Reynolds 보정 및 선정

## 1. Topic 정보

- Topic ID: `control_valve_sizing_cv_kv_reynolds_liquid_selection`
- Question Type: `CALC_DESIGN`
- Supported Secondary Type: `COMPARE_SELECTION`
- Supported Tertiary Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection Importance: `CORE_MUST_PREPARE`
- 주 자료: Control Valve Handbook 제5장, Control Valve Primer 제5장

## 2. 출제 의도

Cv와 Kv는 제어밸브의 유량 용량을 나타낸다.

두 계수의 차이는 단위계와 기준조건이다.

좋은 답안은 정의만 나열하지 않는다.

공정자료를 이용하여 required coefficient를 계산한다.

Piping geometry와 Reynolds correction을 검토한다.

Minimum, normal과 maximum 조건에서 selected trim을 확인한다.

마지막으로 service limitation과 vendor result를 검증한다.

## 3. Cv와 Kv

### 3.1 Cv

Cv는 valve geometry와 유동 손실을 포함한 flow-capacity coefficient이다.

일반적인 미국 단위 정의에서는 다음 조건을 사용한다.

- 기준 유체: 60°F 물
- 밸브 차압: 1 psi
- 유량 단위: US gpm

Cv는 valve opening 또는 line size가 아니다.

### 3.2 Kv

Kv는 metric 단위계의 flow-capacity coefficient이다.

일반적인 정의에서는 다음 조건을 사용한다.

- 기준 유체: 지정된 기준상태의 물
- 밸브 차압: 1 bar
- 유량 단위: \(m^3/h\)

정확한 reference water temperature wording은 적용 표준과 manufacturer 문서를 확인한다.

### 3.3 변환

통상 다음 관계를 사용한다.

\[
K_v\approx0.865C_v
\]

\[
C_v\approx1.156K_v
\]

계수만 변환하고 flow와 pressure 단위를 혼용하면 안 된다.

Project calculation, vendor catalog와 purchase specification의 단위계를 일치시킨다.

## 4. 비초크 액체 기본식

### 4.1 Cv 식

단상·비압축성·비초크·난류 액체에서는 다음 식을 사용할 수 있다.

\[
Q_{\mathrm{US}}
=
C_v
\sqrt{
\frac{\Delta P_{\mathrm{psi}}}{SG}
}
\]

Required Cv는 다음과 같다.

\[
C_{v,\mathrm{req}}
=
Q_{\mathrm{US}}
\sqrt{
\frac{SG}{\Delta P_{\mathrm{psi}}}
}
\]

### 4.2 Kv 식

Metric 단위에서는 다음과 같이 표현할 수 있다.

\[
Q_{\mathrm{SI}}
=
K_v
\sqrt{
\frac{\Delta P_{\mathrm{bar}}}{SG}
}
\]

Required Kv는 다음과 같다.

\[
K_{v,\mathrm{req}}
=
Q_{\mathrm{SI}}
\sqrt{
\frac{SG}{\Delta P_{\mathrm{bar}}}
}
\]

### 4.3 물리적 방향

동일한 coefficient와 SG에서 pressure drop이 4배이면 유량은 2배가 된다.

동일 유량에서 SG가 증가하면 required coefficient도 증가한다.

동일 유량에서 valve pressure drop이 증가하면 required coefficient는 감소한다.

Pressure drop에 선형 비례한다고 설명하면 안 된다.

## 5. 기본식의 적용조건

기본식은 다음 조건을 전제로 한다.

- Liquid
- Single phase
- Approximately incompressible
- Non-choked
- Sufficiently turbulent
- Newtonian 또는 standard correlation이 유효한 유체
- 식과 일치하는 단위계

다음 조건에서는 추가 검토가 필요하다.

- Cavitation
- Flashing
- Liquid choked flow
- Two-phase flow
- Slurry
- Non-Newtonian fluid
- Polymer
- High viscosity
- Extremely small flow coefficient

## 6. Sizing 입력자료

다음 자료를 수집한다.

- Minimum flow
- Normal flow
- Maximum flow
- Inlet pressure \(P_1\)
- Outlet pressure \(P_2\)
- Valve pressure drop \(\Delta P\)
- Temperature
- Density 또는 specific gravity
- Vapor pressure
- Critical pressure
- Dynamic 또는 kinematic viscosity
- Pipe size
- Valve nominal size 후보
- Reducer·expander와 부착 fitting
- Required characteristic
- Vendor trim capacity data

각 자료의 정상조건과 최악조건을 구분한다.

Pressure의 gauge 또는 absolute 표기와 단위를 확인한다.

## 7. Sizing Pressure Drop

Sizing pressure drop은 정의한 운전점에서 valve inlet과 outlet의 pressure 차이다.

\[
\Delta P_v=P_1-P_2
\]

System 전체 differential을 valve pressure drop으로 그대로 사용하면 안 된다.

Pump head, static head, line loss와 다른 equipment loss를 제외하고 valve에 실제 배분되는 차압을 확인한다.

Minimum, normal과 maximum flow에서 \(\Delta P_v\)가 다를 수 있다.

## 8. Required와 Rated Coefficient

### 8.1 Required coefficient

공정 flow, pressure drop와 density를 만족하기 위해 필요한 Cv 또는 Kv이다.

### 8.2 Rated coefficient

Selected valve와 trim이 full rated position에서 제공하는 catalog capacity이다.

### 8.3 구분

Required value와 rated value는 동일하지 않다.

Selected rated capacity는 required capacity 이상이어야 한다.

그러나 지나치게 큰 rated value는 oversizing을 만들 수 있다.

Body size와 rated trim capacity도 동일하지 않다.

Reduced-capacity trim을 사용할 수 있다.

## 9. Minimum·Normal·Maximum 조건

### 9.1 Minimum flow

- Required coefficient가 너무 작아 small-flow 영역에 들어가는지 확인한다.
- Reynolds correction 필요성을 확인한다.
- Selected travel이 deadband와 resolution보다 충분한지 확인한다.
- Minimum controllable flow와 seat leakage를 구분한다.

### 9.2 Normal flow

- Required coefficient와 selected trim curve를 비교한다.
- Normal operating travel을 확인한다.
- Normal travel의 적정 범위는 project와 valve type에 따라 설정한다.
- 특정 opening band를 보편 규격으로 사용하지 않는다.

### 9.3 Maximum flow

- Required maximum coefficient를 계산한다.
- Selected trim이 maximum flow를 확보하는지 확인한다.
- High travel에서 control margin이 남는지 확인한다.
- Pressure drop와 cavitation·choked possibility를 확인한다.

## 10. Characteristic와 Operating Travel

Selected trim의 inherent characteristic를 사용하여 required coefficient에 대응하는 travel을 추정한다.

Linear, equal-percentage와 quick-opening 형상의 상세 비교는 Topic 2가 소유한다.

Topic 6에서는 다음을 확인한다.

- Minimum flow의 usable travel
- Normal flow의 controllable travel
- Maximum flow의 capacity margin
- Selected trim의 rated Cv 또는 Kv
- Required turndown과 actual travel span

Travel mapping은 manufacturer curve 또는 verified characteristic data를 사용한다.

## 11. Piping Geometry Factor

### 11.1 의미

밸브에 reducer, expander, elbow 또는 tee가 직접 연결되면 assembly pressure loss가 달라진다.

이를 \(F_P\)로 보정할 수 있다.

### 11.2 일반 관계

\[
q
=
N_1F_PC
\sqrt{
\frac{\Delta P}{\rho_r}
}
\]

\(F_P<1\)이면 effective capacity가 bare valve보다 작다.

동일 flow를 확보하려면 required coefficient가 증가한다.

\[
C_{\mathrm{corrected}}
=
\frac{C_{\mathrm{basic}}}{F_P}
\]

### 11.3 주의사항

\(F_P\)는 다음에 따라 달라질 수 있다.

- Valve size
- Pipe size
- Reducer와 expander geometry
- Fitting type
- Selected valve coefficient
- Valve style

부착 fitting이 없으면 일반적으로 \(F_P=1\)이다.

모든 installation에서 \(F_P\)를 무시하거나 항상 적용한다고 일반화하지 않는다.

## 12. Viscosity와 Valve Reynolds Number

고점도 또는 저유량에서는 viscous force의 영향이 커진다.

Small trim에서는 characteristic dimension이 작아진다.

Valve 내부 flow가 laminar 또는 transitional 영역에 들어갈 수 있다.

Valve Reynolds number는 이러한 상태를 판단한다.

일반 pipe Reynolds number 식을 그대로 valve에 적용한다고 단정하지 않는다.

Valve style modifier, trim geometry와 pressure recovery factor가 포함될 수 있다.

정확한 식과 threshold는 적용 standard와 vendor method를 확인한다.

## 13. Reynolds Number Factor

### 13.1 의미

\(F_R\)은 비난류 상태에서 effective flow capacity 감소를 보정한다.

충분한 난류에서는 일반적으로 \(F_R=1\)이다.

비난류 조건에서는 \(0<F_R<1\)이 될 수 있다.

### 13.2 보정 방향

\[
C_{\mathrm{corrected}}
=
\frac{C_{\mathrm{turbulent}}}{F_R}
\]

\(F_R<1\)이면 corrected required coefficient가 증가한다.

반대로 감소한다고 설명하면 안 된다.

### 13.3 결정방법

\(F_R\)은 다음의 함수가 될 수 있다.

- Valve Reynolds number
- Valve style
- Trim geometry
- Characteristic flow dimension
- \(F_L\)
- \(F_d\)
- Selected rated coefficient

임의의 고정값으로 사용하지 않는다.

## 14. Reynolds 반복 계산

Corrected coefficient와 valve Reynolds number가 상호 의존할 수 있다.

다음 순서를 사용한다.

1. Turbulent basic equation으로 initial required coefficient를 계산한다.
2. Candidate valve와 trim을 선택한다.
3. Valve style·geometry coefficient를 확인한다.
4. Valve Reynolds number를 계산한다.
5. \(F_R\)을 계산한다.
6. Required coefficient를 \(F_R\)로 보정한다.
7. Corrected value로 candidate trim과 Reynolds number를 다시 계산한다.
8. Coefficient와 \(F_R\) 변화가 허용오차 이내가 될 때까지 반복한다.
9. 최종 corrected required coefficient와 rated trim capacity를 비교한다.

시작값과 convergence tolerance는 사용하는 method에 기록한다.

## 15. Small-Flow Valve

Small-flow trim은 일반 full-size trim과 다른 내부 geometry를 가질 수 있다.

Valve style modifier와 \(F_R\) correlation도 달라질 수 있다.

다음 항목을 확인한다.

- Minimum required Cv 또는 Kv
- Trim orifice와 flow passage
- Plug diameter
- Valve style modifier
- Reynolds correction
- Manufacturing tolerance
- Seat leakage
- Actuator·positioner resolution
- Measurement range

일반 globe valve의 full-size correlation을 small-flow trim에 무조건 적용하지 않는다.

## 16. Oversizing과 Undersizing

### 16.1 Oversizing

Oversizing은 rated coefficient가 required range보다 지나치게 큰 상태이다.

다음 문제가 발생할 수 있다.

- Low normal travel
- Poor resolution
- Deadband와 stiction 영향 확대
- Large local installed gain
- Hunting
- Reduced usable range

Body size 하나만으로 oversizing을 판단하지 않는다.

Trim capacity, required coefficient와 travel을 함께 본다.

### 16.2 Undersizing

Undersizing은 selected capacity가 required maximum condition을 만족하지 못하는 상태이다.

다음 문제가 발생할 수 있다.

- Maximum flow 부족
- Nearly full-open operation
- Excessive valve pressure drop
- Pump energy 증가
- Control margin 부족

## 17. Cavitation·Flashing·Choked Screening

Basic capacity calculation이 끝나도 선정은 완료되지 않는다.

다음을 확인한다.

- Inlet pressure
- Outlet pressure
- Vapor pressure
- Critical pressure
- Valve pressure recovery
- Reducer가 있는 경우 adjusted recovery factor
- Predicted pressure at vena contracta
- Downstream pressure recovery

Cavitation, flashing과 liquid choked criterion의 상세 식과 damage prevention은 Topic 8에서 다룬다.

Topic 6은 screening 결과와 Topic 8 검토 필요 여부를 기록한다.

## 18. 복잡 유체

다음 service에는 별도 method가 필요할 수 있다.

- Two-phase flow
- Slurry
- Non-Newtonian liquid
- Polymer
- Liquid with entrained gas
- Solids-containing fluid
- Cryogenic flashing service

Clean single-phase liquid equation을 그대로 적용하지 않는다.

Vendor와 process specialist의 verified method를 사용한다.

## 19. 선정 절차

1. Project unit basis를 확정한다.
2. Cv 또는 Kv 기준을 선택한다.
3. Minimum·normal·maximum process data를 수집한다.
4. 각 운전점의 valve pressure drop를 결정한다.
5. Basic required coefficient를 계산한다.
6. Piping geometry factor 적용 여부를 검토한다.
7. Viscosity와 valve Reynolds number를 검토한다.
8. 필요하면 \(F_R\) correction을 반복 계산한다.
9. Corrected required coefficient를 구한다.
10. Candidate body와 trim rated capacity를 선택한다.
11. Characteristic curve에서 operating travel을 확인한다.
12. Oversizing과 undersizing을 검토한다.
13. Cavitation·flashing·choked possibility를 screening한다.
14. Complex fluid 적용 한계를 확인한다.
15. Vendor sizing sheet와 hand calculation을 교차 검증한다.
16. Selected trim, travel과 service limitation을 문서화한다.

## 20. 대표 오답

- Cv는 valve opening percentage이다.
- Cv와 Kv 숫자는 항상 같다.
- Cv가 Kv보다 더 정확하다.
- Liquid flow는 pressure drop에 선형 비례한다.
- SG가 증가하면 required Cv가 감소한다.
- Basic liquid equation은 cavitation과 flashing에도 그대로 적용한다.
- Required Cv와 rated Cv는 같은 값이다.
- Body size가 같으면 trim capacity도 같다.
- Normal flow 한 점만 계산하면 된다.
- Reducer와 expander는 sizing에 영향을 주지 않는다.
- \(F_P<1\)이면 required Cv가 감소한다.
- Viscosity는 Cv 계산에 영향을 주지 않는다.
- \(F_R<1\)이면 required Cv가 감소한다.
- \(F_R\)은 임의 상수로 선택한다.
- Reynolds correction은 반복 계산이 필요 없다.
- Catalog Cv가 크면 operating travel 검토가 필요 없다.
- Slurry에 clean-liquid equation을 그대로 적용한다.

## 21. 고득점 답안 기준

고득점 답안은 다음 순서를 가진다.

1. Cv와 Kv의 정의와 단위를 구분한다.
2. Conversion relation과 unit consistency를 제시한다.
3. Basic liquid equation과 적용조건을 쓴다.
4. Flow, pressure, density와 viscosity 자료를 정리한다.
5. Minimum·normal·maximum condition을 각각 계산한다.
6. Required와 rated coefficient를 구분한다.
7. Body size와 trim capacity를 구분한다.
8. \(F_P\)를 검토한다.
9. Valve Reynolds와 \(F_R\)을 조건부로 적용한다.
10. 필요하면 반복 계산한다.
11. Operating travel과 over·under sizing을 검증한다.
12. Cavitation·flashing·choked possibility를 screening한다.
13. Vendor 결과를 hand calculation으로 교차 검증한다.
14. Selected trim과 service limitation으로 결론을 정리한다.

## 22. 인접 Topic 경계

- Unbalanced force와 actuator sizing: Topic 1
- Characteristic 형상: Topic 2
- Deadband·stiction·response: Topic 3
- Valve body·actuator 종류: Topic 4
- Authority·rangeability·installed gain: Topic 5
- Gas sizing과 gas choked flow: Topic 7
- Cavitation·flashing·liquid choked 상세: Topic 8
- Noise prediction: Topic 9
- Balanced·unbalanced trim: Topic 10
- Severe service: Topic 14
- 전체 package workflow: Topic 16

## 23. 작성 원칙

- Definition과 calculation unit을 함께 쓴다.
- Cv와 Kv 중 하나가 우수하다고 설명하지 않는다.
- Square-root relation을 지킨다.
- Density direction을 반대로 쓰지 않는다.
- Formula applicability를 명시한다.
- Minimum·normal·maximum condition을 모두 계산한다.
- Required와 rated coefficient를 구분한다.
- Body size와 trim capacity를 구분한다.
- \(F_P\)와 \(F_R\) 보정 방향을 지킨다.
- Reynolds correction을 조건부로 적용한다.
- 특정 opening 또는 margin 숫자를 보편 기준으로 고정하지 않는다.
- 결론은 selected trim, operating travel과 service limitation으로 검증한다.
