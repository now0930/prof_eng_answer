# 제어밸브의 캐비테이션·플래싱·액체 초크 유동 및 손상 방지

## 1. Topic 정보

- Topic ID: `control_valve_cavitation_flashing_choked_flow_damage_prevention`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Supported Secondary Type: `COMPARE_SELECTION`
- Supported Tertiary Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Selection Importance: `CORE_MUST_PREPARE`

## 2. 출제 의도

Liquid control valve의 cavitation과 flashing은 pressure profile을 이해해야 구분할 수 있다.

좋은 답안은 현상명과 대책만 나열하지 않는다.

다음 순서로 설명한다.

1. \(P_1\rightarrow P_{vc}\rightarrow P_2\) pressure profile
2. Operating-temperature vapor pressure \(P_v\)
3. Thermodynamic critical pressure \(P_c\)
4. \(F_F\), \(F_L\), \(F_P\), \(F_{LP}\)
5. Liquid choked pressure-drop limit
6. Cavitation과 flashing classification
7. Damage mechanism
8. Prevention과 mitigation
9. Vendor crosscheck

## 3. 적용 대상

이 Topic은 다음 service를 대상으로 한다.

- Single-phase liquid entering the valve
- Water
- Hydrocarbon liquid
- Solvent
- Chemical liquid
- Hot condensate
- Pump-discharge letdown
- High-pressure liquid letdown

다음 condition은 별도 검토가 필요하다.

- Inlet two-phase flow
- Slurry
- Non-Newtonian liquid
- Cryogenic flashing
- Reactive decomposition
- Solid-containing erosive service

## 4. Pressure Profile

Valve restriction을 통과하면 flow area가 감소한다.

Velocity가 증가한다.

Static pressure가 감소한다.

Minimum pressure는 vena contracta 부근에서 형성된다.

\[
P_1
\rightarrow
P_{vc}
\rightarrow
P_2
\]

- \(P_1\): valve inlet pressure
- \(P_{vc}\): vena-contracta pressure
- \(P_2\): valve outlet pressure

Vena contracta 이후 flow area가 증가한다.

일부 velocity head가 static pressure로 회복된다.

보통 \(P_{vc}<P_2<P_1\)이다.

Pressure recovery 크기는 valve style과 trim에 따라 달라진다.

## 5. Absolute Pressure

다음 pressure는 absolute pressure로 사용한다.

- \(P_1\)
- \(P_2\)
- \(P_{vc}\)
- \(P_v\)
- \(P_c\)

Gauge pressure는 absolute pressure로 변환한다.

\[
P_{\mathrm{abs}}
=
P_{\mathrm{gauge}}
+
P_{\mathrm{atmospheric}}
\]

모든 pressure는 동일 unit을 사용한다.

## 6. Vapor Pressure

\(P_v\)는 operating temperature에서 liquid와 vapor가 평형을 이루는 pressure이다.

Temperature가 증가하면 일반적으로 \(P_v\)도 증가한다.

따라서 다음을 확인한다.

- Liquid composition
- Operating temperature
- Minimum·normal·maximum temperature
- Startup·shutdown temperature
- Vapor-pressure source

상온 property를 고온 service에 그대로 사용하지 않는다.

## 7. Thermodynamic Critical Pressure

\(P_c\)는 liquid-vapor phase boundary가 사라지는 critical point의 pressure이다.

\(P_c\)는 valve coefficient가 아니다.

\(P_v/P_c\) ratio는 \(F_F\) 계산에 사용될 수 있다.

## 8. Liquid Critical-Pressure-Ratio Factor

Common relation은 다음과 같다.

\[
F_F
=
0.96
-
0.28
\sqrt{
\frac{P_v}{P_c}
}
\]

정확한 notation과 적용범위는 standard edition을 확인한다.

\(P_v\)와 \(P_c\)는 absolute pressure와 동일 unit을 사용한다.

\(P_v/P_c\)가 증가하면 \(F_F\)는 감소한다.

## 9. Pressure-Recovery Factor

### 9.1 \(F_L\)

\(F_L\)은 bare valve의 pressure-recovery factor이다.

다음에 따라 달라질 수 있다.

- Valve style
- Trim geometry
- Flow direction
- Travel
- Manufacturer test data

### 9.2 방향

높은 \(F_L\)은 pressure recovery가 작다는 의미이다.

낮은 \(F_L\)은 pressure recovery가 크다는 의미이다.

낮은 \(F_L\)일수록 \(P_{vc}\)가 더 낮아질 수 있다.

따라서 cavitation susceptibility가 증가할 수 있다.

### 9.3 Universal value 금지

\(F_L\)을 valve type별 하나의 고정값으로 일반화하지 않는다.

Selected travel의 manufacturer data를 확인한다.

## 10. Attached Fittings

Reducer 또는 expander가 valve에 직접 연결되면 assembly behavior가 달라진다.

### 10.1 \(F_P\)

\(F_P\)는 attached fittings가 capacity에 미치는 영향을 보정한다.

### 10.2 \(F_{LP}\)

\(F_{LP}\)는 valve와 fittings의 combined pressure-recovery factor이다.

No-fitting reference에서는 적용 method가 허용할 때 다음과 같이 둘 수 있다.

\[
F_P=1
\]

\[
F_{LP}=F_L
\]

Fitting이 있으면 \(F_{LP}=F_L\)이라고 자동 가정하지 않는다.

## 11. Liquid Choked Pressure-Drop Limit

### 11.1 Bare Valve

Common structure는 다음과 같다.

\[
\Delta P_{\mathrm{choked}}
=
F_L^2
(
P_1-F_FP_v
)
\]

### 11.2 Fitting-Adjusted Assembly

Common structure는 다음과 같다.

\[
\Delta P_{\mathrm{choked}}
=
\left(
\frac{F_{LP}}{F_P}
\right)^2
(
P_1-F_FP_v
)
\]

Exact units와 notation은 적용 standard를 확인한다.

## 12. Effective Sizing Pressure Drop

Actual pressure drop은 다음과 같다.

\[
\Delta P_{\mathrm{actual}}
=
P_1-P_2
\]

Sizing에는 다음 값을 사용한다.

\[
\Delta P_{\mathrm{sizing}}
=
\min
(
\Delta P_{\mathrm{actual}},
\Delta P_{\mathrm{choked}}
)
\]

Subcritical이면 actual pressure drop을 사용한다.

Choked이면 limit value를 사용한다.

큰 값을 사용하면 안 된다.

## 13. Vena-Contracta Pressure

Common no-fitting interpretation은 다음과 같다.

\[
P_{vc}
\approx
P_1
-
\frac{
\Delta P_{\mathrm{actual}}
}{
F_L^2
}
\]

이 식은 direction과 pressure-recovery 해석에 사용한다.

Installed local pressure의 universal exact prediction으로 사용하지 않는다.

Attached fittings가 있으면 \(F_{LP}\), \(F_P\)와 manufacturer method를 사용한다.

## 14. Vapor Formation

Vapor formation은 다음 조건에서 시작될 수 있다.

\[
P_{vc}<P_v
\]

\(P_{vc}\)가 vapor pressure보다 낮아지면 liquid 일부가 vapor bubble로 변한다.

이 조건만으로 cavitation과 flashing을 구분할 수는 없다.

\(P_2\)를 추가로 확인한다.

## 15. Cavitation

Cavitation의 기본 조건은 다음과 같다.

\[
P_{vc}<P_v
\]

\[
P_2>P_v
\]

Vena contracta에서 bubble이 생성된다.

Downstream에서 pressure가 vapor pressure보다 높게 회복된다.

Bubble이 collapse한다.

Collapse는 다음 현상을 만들 수 있다.

- Microjet
- Local shock pressure
- Pitting
- Vibration
- Noise
- Trim erosion
- Body damage

Cavitation 발생과 severe damage는 동일하지 않다.

Exposure time, intensity, material과 geometry가 damage severity에 영향을 준다.

## 16. Flashing

Flashing의 기본 조건은 다음과 같다.

\[
P_{vc}<P_v
\]

\[
P_2\le P_v
\]

Vapor가 downstream까지 지속된다.

핵심은 bubble collapse가 아니다.

핵심은 persistent two-phase high-velocity flow이다.

주요 손상은 다음과 같다.

- Droplet impact
- Two-phase jet erosion
- Outlet erosion
- Downstream pipe erosion
- Vibration
- Capacity limitation

## 17. Cavitation과 Flashing 비교

| 구분 | Cavitation | Flashing |
|---|---|---|
| Vapor formation | \(P_{vc}<P_v\) | \(P_{vc}<P_v\) |
| Outlet pressure | \(P_2>P_v\) | \(P_2\le P_v\) |
| Downstream phase | Liquid로 회복 | Vapor가 지속 |
| 핵심 메커니즘 | Bubble collapse | Persistent two-phase flow |
| 대표 손상 | Pitting·shock erosion | Two-phase erosion |
| 대표 대책 | Pressure-drop staging | Geometry·material·location mitigation |

Anti-cavitation trim은 flashing vapor를 재응축하지 않는다.

## 18. Liquid Choked Flow

다음 조건이면 liquid choked flow이다.

\[
\Delta P_{\mathrm{actual}}
\ge
\Delta P_{\mathrm{choked}}
\]

Downstream pressure를 더 낮춰도 flow capacity 증가가 제한된다.

Liquid choked flow는 zero flow가 아니다.

Liquid choked flow는 다음과 동일하지 않다.

- 반드시 damaging cavitation
- 반드시 flashing
- 완전 차단
- 유량 정지

Cavitation과 flashing 모두 choked condition과 함께 나타날 수 있다.

## 19. Cavitation Development Level

다음 용어가 사용될 수 있다.

- Incipient cavitation
- Developed cavitation
- Constant cavitation
- Choked cavitation
- Damaging cavitation

Threshold와 terminology는 standard와 vendor method에 따라 다를 수 있다.

특정 sigma, \(K_c\) 또는 \(x_{FZ}\)를 universal threshold로 고정하지 않는다.

## 20. Cavitation Damage Mechanism

Bubble collapse는 매우 짧은 시간과 작은 영역에 energy를 집중한다.

다음 손상이 발생할 수 있다.

1. Surface pitting
2. Trim edge erosion
3. Seat leakage 증가
4. Vibration
5. Hydrodynamic noise
6. Stem·guide wear
7. Body wall damage

Damage severity는 다음에 따라 달라진다.

- Pressure differential
- Liquid vapor pressure
- Bubble-collapse location
- Material
- Exposure time
- Flow rate
- Trim geometry

## 21. Flashing Damage Mechanism

Flashing에서는 vapor volume이 downstream에서 증가할 수 있다.

Mixture velocity가 증가할 수 있다.

Persistent two-phase flow는 다음 부위를 침식할 수 있다.

- Valve outlet
- Body wall
- Downstream reducer
- Elbow
- Pipe wall
- Weld area

Bubble collapse가 아니라 two-phase momentum과 droplet impact가 핵심이다.

## 22. Operating Case Matrix

다음 case를 각각 검토한다.

### 22.1 Minimum Flow

- Low travel
- Selected-travel \(F_L\)
- Pressure recovery
- Local instability
- Temperature

### 22.2 Normal Flow

- Normal \(P_1\), \(P_2\)
- Operating \(P_v\)
- Actual·choked pressure drop
- Cavitation·flashing classification
- Noise screening

### 22.3 Maximum Flow

- Maximum \(P_1\)
- Minimum \(P_2\)
- Maximum flow
- Selected-travel \(F_L\)
- Choked condition
- Downstream erosion

### 22.4 Startup·Shutdown

- Temporary pressure reversal
- Pump startup pressure
- Warm-up temperature
- Depressurization
- Bypass operation

## 23. Cavitation Prevention

### 23.1 Downstream Pressure 증가

가능한 process에서는 \(P_2\)를 높인다.

Pressure recovery 후 bubble collapse 가능성을 줄일 수 있다.

Process feasibility를 확인한다.

### 23.2 Temperature 감소

Temperature를 낮추면 \(P_v\)가 감소한다.

Cavitation margin을 늘릴 수 있다.

Cooling cost와 process requirement를 확인한다.

### 23.3 Total Pressure Drop 감소

Valve across pressure drop을 줄인다.

Pump head, line loss와 downstream equipment 조건을 함께 검토한다.

### 23.4 Pressure-Drop Staging

Pressure drop을 여러 stage로 나눈다.

각 stage의 local pressure가 vapor pressure 아래로 과도하게 떨어지는 것을 방지한다.

적용 예는 다음과 같다.

- Multi-stage trim
- Multi-hole cage
- Series restriction
- Two valves in series
- Downstream restriction device

### 23.5 Higher \(F_L\) Trim

Higher \(F_L\)의 low-recovery trim을 사용한다.

Vena-contracta pressure 저하를 줄일 수 있다.

Selected travel의 \(F_L\)을 확인한다.

## 24. Flashing Damage Mitigation

Flashing은 downstream pressure가 vapor pressure보다 낮아 지속되는 phase change이다.

Anti-cavitation trim만으로 제거할 수 없는 경우가 많다.

다음을 검토한다.

- Valve를 downstream vessel에 가깝게 설치
- Outlet flow path를 직선화
- Downstream pipe size 확대
- Sudden impingement 회피
- Erosion path 예측
- Body geometry 검토
- Trim·body material 검토
- Replaceable liner 검토
- Downstream elbow 거리 확보

Material 상세는 Topic 14에서 검토한다.

## 25. Hydrodynamic Noise Handoff

Cavitation과 flashing은 hydrodynamic noise와 vibration을 만들 수 있다.

Topic 8은 다음을 screening한다.

- Cavitation classification
- Choked condition
- Flow rate
- Pressure differential
- Valve style
- Downstream pipe

상세 noise prediction, sound pressure level과 low-noise trim은 Topic 9가 소유한다.

## 26. Vendor Crosscheck

Vendor result에서 다음을 확인한다.

- \(P_1\), \(P_2\) absolute basis
- Operating temperature
- \(P_v\)
- \(P_c\)
- \(F_F\)
- \(F_L\)
- \(F_P\)
- \(F_{LP}\)
- Selected travel
- Actual pressure drop
- Choked pressure-drop limit
- Cavitation·flashing regime
- Noise warning
- Material recommendation
- Minimum·normal·maximum case

Hand calculation과 input sheet로 교차 검증한다.

## 27. 선정 절차

1. Liquid composition을 정의한다.
2. Minimum·normal·maximum flow를 정의한다.
3. Startup·shutdown case를 정의한다.
4. \(P_1\), \(P_2\)를 absolute pressure로 변환한다.
5. Operating temperature의 \(P_v\)를 확인한다.
6. \(P_c\)를 확인한다.
7. \(F_F\)를 계산한다.
8. Candidate valve의 selected-travel \(F_L\)을 확인한다.
9. Attached fittings가 있으면 \(F_P\)와 \(F_{LP}\)를 계산한다.
10. Actual pressure drop을 계산한다.
11. Liquid choked pressure-drop limit를 계산한다.
12. Effective sizing pressure drop을 선택한다.
13. \(P_{vc}\)와 \(P_v\)를 비교한다.
14. \(P_2\)와 \(P_v\)를 비교한다.
15. Cavitation·flashing을 분류한다.
16. Choked 여부를 분리해 판정한다.
17. Damage mechanism을 판정한다.
18. Process modification 가능성을 검토한다.
19. Higher \(F_L\)과 pressure-drop staging을 검토한다.
20. Flashing service geometry를 검토한다.
21. Noise 검토 필요성을 판단한다.
22. Material 상세를 Topic 14로 hand-off한다.
23. Vendor result를 hand calculation으로 확인한다.
24. Selected trim과 limitation을 문서화한다.

## 28. 대표 오답

- Gauge pressure를 \(P_v\), \(P_c\) 식에 그대로 사용한다.
- Vapor pressure는 temperature와 무관하다.
- \(P_c=P_v\)이다.
- 낮은 \(F_L\)은 pressure recovery가 작다.
- \(F_L\)은 모든 valve와 travel에서 같다.
- Fitting이 있어도 항상 \(F_{LP}=F_L\)이다.
- Actual과 choked pressure drop 중 큰 값을 사용한다.
- Liquid choked flow는 유량이 0이다.
- Choked 이후 \(P_2\)를 낮추면 flow가 계속 비례 증가한다.
- \(P_2\le P_v\)이면 cavitation이라고만 판정한다.
- Flashing은 bubble collapse 현상이다.
- Cavitation과 flashing은 동일하다.
- 모든 cavitation은 즉시 severe damage를 만든다.
- Liquid choked flow는 항상 damaging cavitation이다.
- Flashing vapor는 반드시 downstream에서 collapse한다.
- Anti-cavitation trim은 flashing vapor를 재응축한다.
- Valve size만 키우면 모든 문제가 해결된다.
- Hard material만 사용하면 pressure profile 검토가 필요 없다.
- Gas \(x_T\), \(F_\gamma\), \(Y\) 식을 liquid에 사용한다.
- Normal operating point 한 점만 검토한다.

## 29. 고득점 답안 기준

고득점 답안은 다음 순서를 가진다.

1. \(P_1\rightarrow P_{vc}\rightarrow P_2\) pressure profile을 설명한다.
2. \(P_v\)와 \(P_c\)를 absolute pressure로 정의한다.
3. \(F_F\), \(F_L\), \(F_P\), \(F_{LP}\)를 구분한다.
4. Actual과 choked pressure drop 중 작은 값을 사용한다.
5. \(P_{vc}<P_v\)로 vapor formation을 판정한다.
6. \(P_2>P_v\)와 \(P_2\le P_v\)로 cavitation·flashing을 구분한다.
7. Liquid choked flow를 zero flow와 구분한다.
8. Cavitation·flashing damage mechanism을 구분한다.
9. Choked, vapor formation과 damage severity를 분리한다.
10. Minimum·normal·maximum과 startup·shutdown을 검토한다.
11. Process modification과 pressure-drop staging을 설명한다.
12. Higher \(F_L\) trim의 원리를 설명한다.
13. Flashing geometry mitigation을 설명한다.
14. Anti-cavitation trim이 flashing cure가 아님을 설명한다.
15. Topic 9·14 경계를 설명한다.
16. Vendor result를 hand calculation으로 교차 검증한다.

## 30. 인접 Topic 경계

- Actuator force와 fail-safe: Topic 1
- Characteristic 형상: Topic 2
- Deadband·stiction·response: Topic 3
- Body·actuator 종류: Topic 4
- Authority·rangeability·gain: Topic 5
- Non-choked liquid Cv·Kv와 Reynolds: Topic 6
- Gas·steam choked sizing: Topic 7
- Hydrodynamic·aerodynamic noise: Topic 9
- Balanced·unbalanced trim: Topic 10
- Severe-service material: Topic 14
- 전체 valve-package workflow: Topic 16

## 31. 작성 원칙

- Pressure를 absolute basis로 통일한다.
- \(P_v\)를 operating temperature에서 확인한다.
- \(P_c\)와 \(P_v\)를 구분한다.
- \(F_L\)의 pressure-recovery 방향을 지킨다.
- Fitting이 있으면 \(F_P\)와 \(F_{LP}\)를 검토한다.
- Actual과 choked pressure drop 중 작은 값을 사용한다.
- Cavitation과 flashing을 \(P_2/P_v\) 관계로 구분한다.
- Choked flow를 zero flow로 설명하지 않는다.
- Choked, vapor formation과 damage를 동일시하지 않는다.
- Anti-cavitation과 flashing mitigation을 구분한다.
- Universal \(F_L\), sigma, \(K_c\), \(x_{FZ}\)를 사용하지 않는다.
- Selected travel의 recovery factor를 확인한다.
- Startup·shutdown을 포함한다.
- Noise와 material 상세를 인접 Topic으로 분리한다.
- Vendor software 결과를 hand calculation으로 확인한다.
