# 제어밸브의 공력·수력 소음, 소음 예측 및 저소음 트림

## 1. Topic 정보

- Topic ID: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Supported Secondary Type: `CALC_DESIGN`
- Supported Tertiary Type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection Importance: `CORE_MUST_PREPARE`

## 2. 출제 의도

Control valve noise는 유체역학, 음향학과 valve sizing을 연결해야 한다.

좋은 답안은 소음이 크다는 현상과 저소음 트림만 나열하지 않는다.

다음 순서로 설명한다.

1. Process-flow noise와 accessory noise
2. Sound power와 sound pressure
3. dB·dBA와 spectrum
4. Aerodynamic·hydrodynamic mechanism
5. Internal source와 external radiation
6. Low-noise trim과 path treatment
7. Operating-case matrix
8. Field measurement와 verification

## 3. Noise Source 분류

### 3.1 Process-Flow Noise

- Aerodynamic noise
- Liquid turbulence noise
- Cavitation noise
- Flashing noise

### 3.2 Accessory Noise

- Actuator exhaust
- Positioner exhaust
- Booster exhaust
- Solenoid exhaust

Accessory 구조 상세는 Topic 11에서 검토한다.

## 4. Source·Path·Receiver

Noise control hierarchy는 다음과 같다.

\[
\text{Source}
\rightarrow
\text{Path}
\rightarrow
\text{Receiver}
\]

Source treatment는 acoustic power generation을 줄인다.

Path treatment는 acoustic transmission과 radiation을 줄인다.

Receiver protection은 작업자 노출을 줄인다.

같은 reduction을 중복 적용하지 않는다.

## 5. Sound Power Level

Sound power는 source가 방출하는 acoustic energy rate이다.

\[
L_W
=
10
\log_{10}
\left(
\frac{W}{W_0}
\right)
\]

- \(W\): acoustic power
- \(W_0\): reference power
- \(L_W\): sound power level

Sound power는 source property에 가깝다.

## 6. Sound Pressure Level

Sound pressure는 observation point의 pressure fluctuation이다.

\[
L_p
=
20
\log_{10}
\left(
\frac{p_{\mathrm{rms}}}{p_0}
\right)
\]

Sound pressure level은 다음에 영향을 받는다.

- Distance
- Directivity
- Reflection
- Pipe radiation
- Enclosure
- Background noise
- Measurement location

## 7. Sound Power와 Sound Pressure 비교

| 구분 | Sound Power | Sound Pressure |
|---|---|---|
| 물리량 | Acoustic energy rate | Local pressure fluctuation |
| 대표식 | \(10\log_{10}\) | \(20\log_{10}\) |
| 위치 영향 | Source property 중심 | Observation point 영향 |
| 주요 조건 | Source mechanism | Distance·environment |
| 직접 등치 | 불가 | 불가 |

Sound power와 sound pressure를 같은 숫자로 취급하지 않는다.

## 8. dB Logarithmic Addition

Independent source level은 산술합하지 않는다.

\[
L_{\mathrm{total}}
=
10
\log_{10}
\left[
\sum_i10^{L_i/10}
\right]
\]

동일한 독립 source 두 개는 약 3 dB 증가한다.

\[
10\log_{10}(2)
=
3.01\ \mathrm{dB}
\]

Acoustic pressure amplitude 두 배는 약 6 dB 증가한다.

\[
20\log_{10}(2)
=
6.02\ \mathrm{dB}
\]

두 현상을 혼동하지 않는다.

## 9. Overall Level과 Frequency Spectrum

Overall level은 frequency energy를 하나의 값으로 합산한다.

Spectrum은 frequency별 distribution을 나타낸다.

다음을 구분한다.

- Overall dB
- Octave-band level
- One-third-octave level
- Peak frequency
- Broadband noise
- Tonal noise

같은 overall level이라도 spectrum이 다를 수 있다.

## 10. A-Weighting과 dBA

A-weighting은 사람 청감의 frequency sensitivity를 근사한다.

\[
L_A
=
10
\log_{10}
\left[
\sum_i10^{(L_i+A_i)/10}
\right]
\]

dBA는 unweighted dB와 동일하지 않다.

Band별 correction을 적용한 뒤 logarithmic sum을 수행한다.

## 11. Aerodynamic Noise

Gas가 valve restriction을 통과하면 high-velocity turbulent jet가 형성된다.

다음 mechanism이 발생할 수 있다.

- Turbulent mixing
- Jet interaction
- Expansion
- Shock cell
- Downstream pipe interaction

High pressure ratio와 choked regime은 strong aerodynamic noise와 연계될 수 있다.

Choked flow는 zero flow가 아니다.

## 12. Topic 7 Handoff

Topic 7에서 다음을 인계한다.

- \(P_1\)
- \(P_2\)
- \(T_1\)
- Molecular weight
- Specific heat ratio
- Compressibility factor
- \(F_\gamma\)
- \(x_T\)
- \(x_{TP}\)
- Expansion factor \(Y\)
- Mass flow
- Selected travel
- Downstream pipe size

Topic 9는 gas capacity sizing을 반복하지 않는다.

## 13. Gas Outlet Velocity와 Mach Number

Noise risk는 다음과 연계된다.

- Outlet density
- Mass flow
- Flow area
- Sonic velocity
- Outlet velocity
- Mach number
- Pipe diameter
- Expansion condition

특정 Mach number를 universal limit로 고정하지 않는다.

## 14. Hydrodynamic Noise

### 14.1 Liquid Turbulence

Single-phase turbulence는 broadband pressure fluctuation을 만든다.

### 14.2 Cavitation

\[
P_{vc}<P_v
\]

\[
P_2>P_v
\]

Bubble collapse는 impulsive pressure와 broadband noise를 만든다.

### 14.3 Flashing

\[
P_{vc}<P_v
\]

\[
P_2\le P_v
\]

Persistent two-phase flow와 droplet impact가 noise와 vibration을 만든다.

Cavitation과 flashing의 mechanism을 동일하게 설명하지 않는다.

## 15. Topic 8 Handoff

Topic 8에서 다음을 인계한다.

- \(P_1\)
- \(P_2\)
- \(P_{vc}\)
- \(P_v\)
- \(P_c\)
- \(F_F\)
- \(F_L\)
- \(F_P\)
- \(F_{LP}\)
- Liquid choked limit
- Cavitation regime
- Flashing regime
- Selected travel
- Downstream geometry

Topic 9는 phase-change classification을 반복하지 않는다.

## 16. Acoustic Transmission

Noise prediction은 다음 과정을 구분한다.

\[
\text{Fluid mechanical energy}
\rightarrow
\text{Acoustic power}
\rightarrow
\text{Internal propagation}
\rightarrow
\text{Pipe transmission}
\rightarrow
\text{External radiation}
\rightarrow
\text{Measured SPL}
\]

Source level과 external SPL을 같은 값으로 사용하지 않는다.

## 17. Pipe Transmission Loss

Transmission loss는 다음에 의존한다.

- Pipe diameter
- Wall thickness
- Schedule
- Material
- Frequency
- Fluid
- Insulation
- Support
- Enclosure

Pipe transmission loss를 universal constant로 사용하지 않는다.

## 18. Distance Correction

Free-field point-source approximation은 다음과 같다.

\[
L_{p,2}
=
L_{p,1}
-
20
\log_{10}
\left(
\frac{r_2}{r_1}
\right)
\]

Distance가 두 배가 되면 약 6 dB 감소한다.

다음 조건에서는 직접 적용하지 않는다.

- Distributed pipe source
- Strong reflection
- Enclosure
- Near field
- Different directivity

## 19. Aerodynamic Prediction Input

- Gas property
- \(P_1\), \(P_2\)
- Inlet temperature
- Mass flow
- Valve coefficient
- Selected travel
- \(x_T\), \(x_{TP}\)
- Choked regime
- Outlet velocity
- Mach number
- Pipe diameter
- Pipe wall thickness
- Observation point

적용 IEC 60534-8-3 edition을 확인한다.

## 20. Hydrodynamic Prediction Input

- Liquid density
- Vapor pressure
- Critical pressure
- \(P_1\), \(P_2\)
- Flow rate
- Valve coefficient
- Selected travel
- \(F_L\), \(F_P\), \(F_{LP}\)
- Cavitation regime
- Flashing regime
- Pipe geometry
- Observation point

적용 IEC 60534-8-4 edition을 확인한다.

## 21. Multi-Hole·Multi-Path Trim

하나의 큰 jet를 여러 작은 jet로 분할한다.

다음 효과를 기대할 수 있다.

- Energy distribution
- Jet length reduction
- Characteristic scale reduction
- Peak-frequency shift
- Reduced individual jet strength

Downstream jet recombination을 검토한다.

## 22. Multi-Stage Trim

Total pressure drop을 여러 stage로 분할한다.

각 stage의 pressure ratio와 velocity를 제한한다.

Gas service에서는 shock strength를 줄일 수 있다.

Liquid service에서는 local pressure collapse를 줄일 수 있다.

Stage 수를 universal 값으로 고정하지 않는다.

## 23. Diffuser

Diffuser 또는 orifice plate는 system pressure drop을 분담한다.

Valve pressure ratio를 낮출 수 있다.

다음을 검토한다.

- Required flow
- Pressure loss
- Capacity
- Choked condition
- Diffuser noise
- Erosion
- Blockage
- Maintenance

## 24. Silencer·Insulation·Enclosure

### Silencer

Gas 또는 pipe-borne acoustic energy를 attenuation한다.

Pressure loss를 검토한다.

### Insulation

Pipe external radiation을 줄일 수 있다.

Frequency와 installation에 따라 효과가 달라진다.

### Enclosure

Source와 receiver 사이 radiation path를 차단한다.

Heat, ventilation과 access를 검토한다.

## 25. Valve Size Tradeoff

Larger valve는 동일 flow에서 일부 velocity를 낮출 수 있다.

그러나 다음 문제가 발생할 수 있다.

- Low travel
- Poor rangeability use
- High installed gain
- Seat instability
- Higher cost
- Different pressure recovery

Valve size 확대만으로 항상 소음이 감소한다고 단정하지 않는다.

## 26. Low-Noise Trim Tradeoff

다음을 함께 검토한다.

- Required Cv
- Rated Cv
- Selected travel
- Rangeability
- Passage size
- Stage count
- Plugging
- Particle tolerance
- Erosion
- Maintenance
- Spare parts
- Cost

## 27. Operating Case Matrix

### Minimum

- Low travel
- Trim activation
- Control stability
- Spectrum

### Normal

- Overall level
- Octave spectrum
- External SPL
- Selected travel

### Maximum

- Maximum flow
- Minimum downstream pressure
- Choked regime
- Outlet velocity
- Capacity margin

### Startup·Shutdown

- Bypass
- Blowdown
- Warm-up
- Depressurization
- Emergency condition

## 28. Multiple Sources

Parallel valve와 bypass source를 함께 검토한다.

Independent source는 logarithmic sum을 사용한다.

\[
L_{\mathrm{total}}
=
10
\log_{10}
\sum_i10^{L_i/10}
\]

Coherent interaction 가능성을 확인한다.

## 29. Field Measurement

다음을 기록한다.

- Instrument
- Calibration
- dB or dBA
- Time weighting
- Frequency band
- Distance
- Direction
- Operating condition
- Background noise
- Reflection
- Nearby source
- Pipe support

Prediction point와 measurement point를 일치시킨다.

## 30. Background Correction

Source-on과 source-off level을 비교한다.

Background level이 source level과 가까우면 uncertainty가 증가한다.

적용 correction method를 standard에서 확인한다.

## 31. Prediction과 Measurement 차이

1. Process input 확인
2. Fluid property 확인
3. Valve model 확인
4. Selected travel 확인
5. Flow regime 확인
6. Pipe geometry 확인
7. Transmission loss 확인
8. Observation point 확인
9. Background correction 확인
10. Reflection 확인
11. Multiple source 확인
12. Instrument calibration 확인

## 32. Occupational Limit

Noise limit은 다음에 따라 달라진다.

- Country
- Exposure time
- Company standard
- Continuous or impulsive noise
- Hearing-conservation policy

특정 dBA를 universal limit로 고정하지 않는다.

## 33. 선정 절차

1. Process-flow noise와 accessory noise를 구분한다.
2. Fluid와 operating case를 정의한다.
3. Topic 7 또는 Topic 8의 sizing·regime 결과를 인계한다.
4. Aerodynamic 또는 hydrodynamic mechanism을 판정한다.
5. Sound power와 sound pressure target을 구분한다.
6. Overall level과 octave spectrum을 확인한다.
7. dBA requirement를 확인한다.
8. Pipe geometry와 transmission loss를 입력한다.
9. External SPL observation point를 정의한다.
10. Minimum·normal·maximum과 startup·shutdown을 계산한다.
11. Multi-hole 또는 multi-stage trim을 검토한다.
12. Diffuser의 pressure-drop 분담을 검토한다.
13. Silencer·insulation·enclosure를 검토한다.
14. Cv·rangeability·plugging·maintenance tradeoff를 검토한다.
15. Parallel source를 logarithmic sum으로 결합한다.
16. Vendor prediction을 hand-check한다.
17. Field measurement condition을 정의한다.
18. 적용 occupational limit을 확인한다.
19. Prediction과 measurement를 비교한다.
20. Final mitigation과 limitation을 문서화한다.

## 34. 대표 오답

- Sound power와 sound pressure는 같다.
- dB level을 산술합한다.
- 동일 source 두 개는 6 dB 증가한다.
- Pressure amplitude 두 배는 3 dB 증가한다.
- dBA와 unweighted dB는 같다.
- Overall dB가 같으면 spectrum도 같다.
- Distance는 SPL에 영향을 주지 않는다.
- Aerodynamic noise는 flow와 pressure ratio에 무관하다.
- Choked gas는 flow가 없어 noise가 없다.
- 하나의 Mach limit를 모든 valve에 적용한다.
- Cavitation과 flashing noise는 동일하다.
- Hydrodynamic noise는 cavitation에서만 발생한다.
- Flashing noise는 bubble collapse이다.
- Pipe transmission loss는 필요 없다.
- 모든 insulation은 동일 attenuation을 제공한다.
- Low-noise trim은 noise를 0으로 만든다.
- Valve size를 키우면 항상 조용하다.
- Diffuser는 capacity에 영향을 주지 않는다.
- Source·path·receiver reduction을 무조건 산술합한다.
- Normal case 한 점만 검토한다.
- 하나의 dBA가 모든 project의 법적 limit이다.

## 35. 고득점 답안 기준

고득점 답안은 다음을 포함한다.

1. Process-flow noise와 accessory noise를 구분한다.
2. Source·path·receiver hierarchy를 설명한다.
3. Sound power와 sound pressure를 구분한다.
4. \(10\log\)와 \(20\log\)를 구분한다.
5. Independent source를 logarithmic sum으로 합산한다.
6. Overall level, spectrum과 dBA를 구분한다.
7. Aerodynamic turbulent jet·shock mechanism을 설명한다.
8. Hydrodynamic turbulence·cavitation·flashing을 구분한다.
9. Topic 7·8 upstream input을 명시한다.
10. Pipe transmission loss와 external radiation을 설명한다.
11. Multi-hole jet division을 설명한다.
12. Multi-stage pressure-ratio·velocity control을 설명한다.
13. Diffuser와 path treatment를 구분한다.
14. Valve size와 low-noise trim tradeoff를 설명한다.
15. Operating-case matrix를 적용한다.
16. Field measurement와 background correction을 설명한다.
17. Universal Mach·dBA 기준을 사용하지 않는다.
18. Vendor prediction을 field data로 교차 검증한다.

## 36. 인접 Topic 경계

- Actuator force와 fail-safe: Topic 1
- Deadband·stiction·positioner dynamics: Topic 3
- Body·actuator type: Topic 4
- Authority·rangeability·gain: Topic 5
- Non-choked liquid sizing: Topic 6
- Gas choked capacity: Topic 7
- Cavitation·flashing·liquid choked regime: Topic 8
- Balanced·unbalanced trim: Topic 10
- Positioner·I/P·booster accessory: Topic 11
- Severe-service material: Topic 14
- SIL·SIS·ESD: Topic 15
- 전체 valve-package workflow: Topic 16

## 37. 작성 원칙

- Sound power와 sound pressure를 분리한다.
- dB logarithmic addition을 적용한다.
- Overall level, spectrum과 dBA를 분리한다.
- Aerodynamic·hydrodynamic mechanism을 분리한다.
- Topic 7·8 결과를 upstream input으로 사용한다.
- Source·path·receiver 대책을 분리한다.
- Internal source와 external SPL을 직접 동일시하지 않는다.
- Pipe transmission loss를 검토한다.
- Low-noise trim의 jet·stage 분할 원리를 설명한다.
- Diffuser와 silencer의 역할을 구분한다.
- Valve size와 capacity tradeoff를 검토한다.
- Plugging·erosion·maintenance를 검토한다.
- Minimum·normal·maximum 및 startup·shutdown을 검토한다.
- Parallel source는 logarithmic sum을 사용한다.
- Field measurement condition과 background를 기록한다.
- Universal Mach·dBA·stage 수를 사용하지 않는다.
- 적용 standard edition과 vendor method를 명시한다.
- Prediction을 field data로 교차 검증한다.
