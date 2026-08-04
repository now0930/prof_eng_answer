# Balanced·Unbalanced Trim의 구조, 밀봉 및 적용

## 1. Topic 정보

- Topic ID: `balanced_trim_unbalanced_trim_structure_sealing_applications`
- Question Type: `COMPARE_SELECTION`
- Supported Secondary Type: `PRINCIPLE_INTERPRETATION`
- Supported Tertiary Type: `STRUCTURE`
- Difficulty: `FIELD_APPLICATION`
- Selection Importance: `CORE_MUST_PREPARE`

## 2. 출제 의도

Balanced·unbalanced trim 문제는 구조와 force를 연결해야 한다.

좋은 답안은 balanced trim은 작은 actuator를 사용한다는 결론만 제시하지 않는다.

다음 순서로 설명한다.

1. Body·plug·cage·seat와 pressure boundary
2. Effective unbalanced area
3. Unbalanced pressure force
4. Balance hole과 pressure communication
5. Residual effective area와 residual force
6. Balance seal loading·friction·leakage
7. Service별 적용과 제한
8. Topic 1·3·4·9·13·14·16 hand-off
9. Vendor force table과 maintenance 검증

## 3. Unbalanced Trim

Unbalanced trim은 differential pressure의 net effect가 plug에 크게 상쇄되지 않는다.

기본 force magnitude는 다음과 같다.

\[
F_u
=
\Delta P
A_u
\]

- \(F_u\): unbalanced pressure force
- \(\Delta P\): relevant differential pressure
- \(A_u\): effective unbalanced area

Unbalanced trim은 구조가 단순할 수 있다.

Balance seal friction이 작거나 없을 수 있다.

그러나 pressure force가 커질 수 있다.

## 4. Effective Unbalanced Area

Effective unbalanced area는 pressure field가 net axial force를 만드는 equivalent area이다.

다음과 항상 같지 않다.

- Nominal seat area
- Plug diameter area
- Stem area
- Cage diameter area
- Balance-seal diameter area

Manufacturer effective-area table을 우선 확인한다.

## 5. Force Direction

Positive stem direction을 먼저 정의한다.

Signed force는 다음처럼 표현할 수 있다.

\[
\vec{F}_u
=
s
\Delta P
A_u
\]

\(s\)는 actual pressure geometry로 결정한다.

Flow-to-open·flow-to-close label만으로 sign을 고정하지 않는다.

## 6. Balanced Trim

Balanced trim은 plug 양측 또는 balance chamber 사이에 pressure-communication path를 제공한다.

대표 구조는 다음과 같다.

- Balance hole
- Balance passage
- Hollow plug
- Cage-guided balanced plug
- Piston ring
- Seal ring
- Pressure-balanced seal
- Pilot-balanced construction

## 7. Balance Hole과 Passage

Balance hole은 pressure를 plug 반대편 chamber에 전달한다.

목적은 net pressure force를 줄이는 것이다.

다음 영향을 검토한다.

- Hole diameter
- Hole count
- Passage length
- Fluid viscosity
- Particulate
- Fouling
- Erosion
- Travel
- Pressure transient

Balance hole이 있다고 즉시 완전 평형이 되는 것은 아니다.

## 8. Residual Pressure Force

Balanced trim에도 residual force가 남을 수 있다.

\[
F_r
=
\Delta P
A_r
\]

- \(F_r\): residual pressure force
- \(A_r\): residual effective unbalanced area

Balanced trim은 일반적으로 \(A_r<A_u\)가 되도록 설계된다.

\(A_r=0\)은 ideal full-balance model이다.

## 9. Force Reduction Ratio

동일 \(\Delta P\)와 static basis에서 다음을 사용할 수 있다.

\[
R_F
=
\frac{|F_r|}{|F_u|}
=
\frac{A_r}{A_u}
\]

\[
\eta_F
=
1
-
R_F
\]

이 값은 pressure-force reduction이다.

Total actuator-thrust reduction과 항상 같지는 않다.

다음 항이 추가되기 때문이다.

- Seat load
- Packing friction
- Balance-seal friction
- Spring force
- Margin

## 10. Cage-Guided Balanced Plug

Cage-guided balanced plug는 다음 기능을 결합할 수 있다.

- Guiding
- Pressure chamber
- Seal support
- Flow-area definition
- Trim retention

Cage-guided라는 이유만으로 balanced trim이라고 단정하지 않는다.

Cutaway를 확인한다.

## 11. Balance Seal

Balance seal은 balance chamber의 pressure boundary를 형성한다.

대표 형태는 다음과 같다.

- Piston ring
- PTFE seal
- Graphite seal
- Metal seal
- Composite seal

Balance seal은 seat seal과 다르다.

## 12. Balance Seal Loading

Seal loading은 다음에 영향을 받는다.

- Differential pressure
- Preload
- Geometry
- Temperature
- Thermal expansion
- Wear
- Swelling
- Extrusion
- Manufacturing tolerance

Exact limit는 manufacturer data를 확인한다.

## 13. Balance-Seal Friction

Balance-seal friction은 motion을 반대한다.

\[
F_{bs}v
\le
0
\]

단순 magnitude model은 다음과 같다.

\[
|F_{bs}|
\approx
\mu_{bs}
N_{bs}
\]

이 식은 조건부 model이다.

\(\mu_{bs}\)와 \(N_{bs}\)를 universal constant로 사용하지 않는다.

## 14. Breakaway와 Running Friction

Motion 시작 시 breakaway friction이 발생할 수 있다.

운동 중에는 running friction이 발생한다.

조건부로 다음 관계가 나타날 수 있다.

\[
F_{breakaway}
\ge
F_{running}
\]

Fixed ratio로 일반화하지 않는다.

Deadband·stiction 진단은 Topic 3과 연결한다.

## 15. Balance-Seal Leakage

Balance-seal leakage는 pressure chamber 사이의 internal leakage이다.

다음에 영향을 줄 수 있다.

- Pressure balancing
- Residual force
- Dynamic response
- Internal recirculation
- Wear

Seat leakage와 구분한다.

## 16. Seat Leakage

Seat leakage는 closed seat boundary를 통과하는 leakage이다.

Balance-seal leakage와 다음이 다르다.

| 구분 | Balance-seal leakage | Seat leakage |
|---|---|---|
| 위치 | Balance chamber 사이 | Closed seat boundary |
| 기능 | Pressure balancing 영향 | Shutoff performance |
| Rating | Internal design basis | Leakage class basis |
| 주요 영향 | Residual force·response | Process isolation |
| 상세 Topic | Topic 10 | Topic 13 |

Balanced trim이라고 특정 leakage class가 자동 보장되지 않는다.

## 17. Pressure Equalization Transient

Rapid stroke에서 balance chamber pressure가 즉시 steady state에 도달하지 않을 수 있다.

다음에 의존한다.

- Chamber volume
- Passage conductance
- Fluid compressibility
- Viscosity
- Leakage
- Plug velocity
- Pressure step
- Fouling

## 18. Passage Plugging

Dirty·particulate service에서 balance passage가 막힐 수 있다.

결과는 다음과 같다.

- Residual force 증가
- Pressure lag
- Stick-slip
- Actuator overload
- Seat-load variation
- Travel instability

Allowable particle size는 vendor 기준을 확인한다.

## 19. Flow-to-Open·Flow-to-Close

Flow-to-open은 process pressure force가 opening direction을 돕는 구성이다.

Flow-to-close는 closing direction을 돕는 구성이다.

실제 판정에는 다음이 필요하다.

- Upstream pressure
- Downstream pressure
- Plug orientation
- Seat orientation
- Stem direction
- Balance chamber
- Passage
- Travel

Label만으로 force sign을 결정하지 않는다.

## 20. Actuator Input 분리

Conceptual actuator input은 다음과 같다.

\[
F_{input}
=
F_{pressure}
+
F_{seat}
+
F_{packing}
+
F_{balance\ seal}
+
F_{spring}
+
F_{margin}
\]

각 항의 sign과 operating case를 구분한다.

정량 actuator sizing과 fail-safe spring은 Topic 1이 소유한다.

## 21. Topic 1 Handoff

Topic 10에서 다음을 제공한다.

- \(A_u\)
- \(A_r\)
- Pressure-force direction
- Balance-seal friction
- Seat-load requirement
- Pressure cases

Topic 1은 required thrust와 spring을 산정한다.

## 22. Topic 3 Handoff

Topic 3이 소유하는 범위는 다음과 같다.

- Deadband
- Stiction
- Hysteresis
- Stick-slip
- Response time
- Positioner compensation

## 23. Topic 4 Handoff

Topic 4가 소유하는 범위는 다음과 같다.

- General body type
- General plug type
- General cage type
- Guide
- Bonnet
- Actuator type

Topic 10은 balanced pressure path와 seal 구조를 소유한다.

## 24. Topic 9 Boundary

Topic 9가 소유하는 범위는 다음과 같다.

- Aerodynamic noise
- Hydrodynamic noise
- Low-noise trim
- Multi-stage pressure-drop distribution
- Pipe acoustic treatment

Balanced trim은 low-noise trim과 동일하지 않다.

## 25. Topic 13 Boundary

Topic 13이 소유하는 범위는 다음과 같다.

- Seat leakage class
- Shutoff class
- Packing
- Fugitive emissions
- Stem seal

Topic 10은 balance seal과 internal balance leakage를 소유한다.

## 26. Topic 14 Boundary

Topic 14가 소유하는 범위는 다음과 같다.

- Hardfacing
- Erosion-resistant material
- Severe-service construction
- Material lifecycle 상세

## 27. Clean High-ΔP Service

Balanced trim은 다음 조건에서 유리할 수 있다.

- Clean fluid
- High differential pressure
- Large valve size
- Limited actuator thrust
- Stable maintenance environment

다음을 함께 검토한다.

- Seat leakage
- Seal friction
- Temperature
- Fluid compatibility
- Spare parts
- Lifecycle cost

## 28. Dirty·Slurry·Particulate Service

다음을 검토한다.

- Passage plugging
- Seal scratching
- Abrasive wear
- Particle trapping
- Flushability
- Upstream filtration
- Disassembly
- Spare availability

Unbalanced trim이 단순성과 contamination tolerance에서 유리할 수 있다.

Universal selection은 아니다.

## 29. High-Temperature Service

다음을 검토한다.

- Seal temperature limit
- Thermal expansion
- Creep
- Relaxation
- Graphite oxidation
- Metal-seal leakage
- Friction change
- Cycle life

## 30. Cryogenic Service

다음을 검토한다.

- Material contraction
- Seal embrittlement
- Clearance change
- Leakage
- Ice formation
- Thermal gradient
- Startup transient

## 31. Fluid Compatibility

다음을 확인한다.

- Swelling
- Hardening
- Softening
- Extraction
- Extrusion
- Permeation
- Corrosion
- Lubricity
- Pressure
- Temperature

## 32. Operating Case Matrix

### Minimum

- Low travel
- Seal friction dominance
- Chamber communication
- Control stability

### Normal

- Normal differential pressure
- Residual force
- Seal loading
- Leakage requirement

### Maximum

- Maximum differential pressure
- Maximum residual force
- Actuator input
- Cavitation·noise boundary

### Startup·Shutdown

- Full upstream pressure
- Low downstream pressure
- Thermal transient
- Reverse pressure
- Rapid stroke
- Bypass condition

## 33. Maintenance

Balanced trim은 추가 parts를 가질 수 있다.

다음을 검토한다.

- Seal replacement
- Piston-ring inspection
- Balance-hole cleaning
- Cage wear
- Plug scoring
- Special tools
- Assembly orientation
- Pressure test
- Leakage test
- Spare-part lead time

## 34. Vendor Crosscheck

다음을 확인한다.

- Cutaway
- Pressure arrows
- Balance diameter
- Effective unbalanced area
- Residual force table
- Seal material
- Seal pressure limit
- Seal temperature limit
- Flow direction
- Seat leakage class
- Actuator thrust table
- Maintenance manual

## 35. 선정 절차

1. Body와 trim pressure boundary를 확인한다.
2. Upstream·downstream pressure path를 표시한다.
3. Unbalanced 또는 balanced construction을 판정한다.
4. Effective unbalanced area를 확인한다.
5. \(F_u=\Delta P A_u\)를 계산한다.
6. Balanced trim이면 balance hole과 chamber를 확인한다.
7. Residual area \(A_r\)를 확인한다.
8. \(F_r=\Delta P A_r\)를 계산한다.
9. Force direction과 sign convention을 정한다.
10. Balance seal type과 loading을 확인한다.
11. Balance-seal friction을 확인한다.
12. Balance leakage와 seat leakage를 구분한다.
13. Pressure equalization transient를 검토한다.
14. Dirty service의 passage plugging을 검토한다.
15. High-temperature·cryogenic seal limit를 확인한다.
16. Minimum·normal·maximum 및 startup·shutdown case를 계산한다.
17. Topic 1로 actuator inputs를 hand-off한다.
18. Topic 3·4·9·13·14 경계를 확인한다.
19. Vendor cutaway와 force table을 교차 검증한다.
20. Maintenance와 lifecycle cost를 비교한다.

## 36. 대표 오답

- Balanced와 unbalanced trim의 구조는 같다.
- Balanced trim은 pressure force가 항상 0이다.
- Nominal seat area는 항상 effective unbalanced area이다.
- Balance hole은 모든 transient에서 즉시 완전 평형을 만든다.
- Balance seal과 seat seal은 같다.
- Balance leakage와 seat leakage는 같다.
- Balanced trim에는 seal friction이 없다.
- Seal friction은 motion을 돕는다.
- Flow-to-open이면 모든 valve에서 actuator thrust가 감소한다.
- Unbalanced trim은 high-\(\Delta P\)에 절대 사용할 수 없다.
- 모든 high-\(\Delta P\)에는 balanced trim이 필수이다.
- Balanced trim은 항상 더 낮은 seat leakage를 보장한다.
- Balanced trim은 cavitation과 noise를 제거한다.
- Balanced trim은 actuator margin이 필요 없다.
- Balance-chamber dynamics는 force에 영향을 주지 않는다.
- Passage plugging은 force에 영향을 주지 않는다.
- 하나의 seal material을 모든 fluid·temperature에 사용한다.
- Balanced trim은 maintenance가 필요 없다.
- Normal operating point만 검토한다.
- Residual force와 seal friction을 actuator input에서 무시한다.

## 37. 고득점 답안 기준

고득점 답안은 다음을 포함한다.

1. Pressure boundary를 cutaway 기준으로 설명한다.
2. Effective unbalanced area와 nominal seat area를 구분한다.
3. \(F_u=\Delta P A_u\)를 설명한다.
4. Force sign convention을 명시한다.
5. Balance hole의 pressure communication을 설명한다.
6. Balanced trim의 residual force를 설명한다.
7. \(F_r=\Delta P A_r\)를 설명한다.
8. Ideal full balance와 actual residual force를 구분한다.
9. Balance seal과 seat seal을 구분한다.
10. Balance-seal friction과 breakaway를 설명한다.
11. Balance leakage와 seat leakage를 구분한다.
12. Dynamic pressure equalization을 설명한다.
13. Passage plugging 위험을 설명한다.
14. Flow-to-open·flow-to-close를 geometry-dependent로 설명한다.
15. Topic 1 actuator-sizing hand-off를 명시한다.
16. Clean·dirty·temperature service를 비교한다.
17. Operating-case matrix를 적용한다.
18. Vendor force table과 maintenance data를 검증한다.

## 38. 인접 Topic 경계

- Actuator force·spring sizing: Topic 1
- Deadband·stiction·response: Topic 3
- Body·cage·guide 일반 구조: Topic 4
- Authority·gain·rangeability: Topic 5
- Liquid sizing: Topic 6
- Gas sizing: Topic 7
- Cavitation·flashing: Topic 8
- Valve noise·low-noise trim: Topic 9
- Positioner·I/P·booster: Topic 11
- Seat leakage·packing·emissions: Topic 13
- Severe-service material: Topic 14
- 전체 valve-package workflow: Topic 16

## 39. 작성 원칙

- Balanced와 unbalanced를 구조·pressure path·force로 비교한다.
- Effective area와 nominal seat area를 분리한다.
- Balanced trim을 zero-force trim으로 설명하지 않는다.
- Balance hole과 chamber pressure path를 설명한다.
- Residual force와 residual area를 설명한다.
- Balance seal과 seat seal을 분리한다.
- Balance leakage와 seat leakage를 분리한다.
- Seal friction은 motion을 반대한다고 설명한다.
- Flow direction은 geometry-dependent로 표현한다.
- Actuator sizing은 Topic 1로 hand-off한다.
- Dynamic friction 진단은 Topic 3과 구분한다.
- General body·cage selection은 Topic 4와 구분한다.
- Low-noise trim은 Topic 9와 구분한다.
- Leakage class와 packing은 Topic 13과 구분한다.
- Material 상세는 Topic 14와 구분한다.
- Clean·dirty·temperature service를 비교한다.
- Operating-case matrix를 적용한다.
- Universal thrust reduction·seal limit·leakage class를 사용하지 않는다.
- Vendor cutaway, force table과 maintenance data를 확인한다.
