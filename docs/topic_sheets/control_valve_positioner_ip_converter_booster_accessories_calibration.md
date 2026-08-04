# 제어밸브 포지셔너·I/P 변환기·부스터·부속기기 및 교정


## 1. Topic 정보

- Topic ID: `control_valve_positioner_ip_converter_booster_accessories_calibration`
- Primary: `PRINCIPLE_INTERPRETATION`
- Secondary: `STRUCTURE`
- Tertiary: `PROCEDURE`
- Difficulty: `FIELD_APPLICATION`
- Importance: `CORE_MUST_PREPARE`

## 2. 핵심 Signal Chain

4–20 mA → I/P → pneumatic signal → positioner → actuator → travel → feedback
Positioner는 command와 actual travel을 비교한다.
I/P는 current를 pneumatic pressure로 변환한다.

## 3. Positioner

Positioner는 local travel-feedback controller이다.
$$e=r-y$$
Output correction은 |e|를 줄이는 negative-feedback 방향이어야 한다.
Pneumatic type은 nozzle-flapper, force balance, relay와 feedback cam을 사용할 수 있다.

## 4. I/P Converter

I/P converter는 current-to-pressure transducer이다.
Travel을 직접 측정하지 않는다.
$$x=\frac{I-I_{min}}{I_{max}-I_{min}}$$
$$P=P_{min}+x(P_{max}-P_{min})$$

## 5. Conventional Mapping

| Current | Pressure |
|---:|---:|
| 4 mA | 3 psi |
| 12 mA | 9 psi |
| 20 mA | 15 psi |

## 6. Direct·Reverse Action

Direct normalized mapping: y=x
Reverse normalized mapping: y=1-x
Positioner action, actuator action과 fail action을 분리한다.

## 7. Feedback Linkage

Lever, pivot, cam, link length, backlash와 full-travel alignment를 확인한다.

## 8. Zero·Span Calibration

1. Supply와 action을 확인한다.
2. Lower input에서 zero를 맞춘다.
3. Upper input에서 span을 맞춘다.
4. Lower endpoint를 재확인한다.
5. Intermediate point를 확인한다.

## 9. Multipoint Verification

0·25·50·75·100% upstroke와 downstroke를 모두 측정한다.

## 10. Calibration Error

$$E_{FS}=100\frac{y_{meas}-y_{cmd}}{y_{max}-y_{min}}$$
Tolerance는 site·vendor basis를 확인한다.

## 11. Hysteresis

$$H=y_{up}-y_{down}$$
Deadband·stiction·hunting 상세는 Topic 3이 소유한다.

## 12. Split Range

$$x_s=\frac{I-I_{s,min}}{I_{s,max}-I_{s,min}}$$
각 segment의 own range, gap, overlap와 fail action을 확인한다.

## 13. Volume Booster

Booster는 pilot pressure를 추종하며 큰 fill·vent flow를 제공한다.
$$P_{out}\approx P_{pilot}$$
Pressure amplifier가 아니다.
Bypass와 hunting tuning은 Topic 3으로 hand-off한다.

## 14. Filter Regulator

Supply air를 여과하고 pressure를 조절한다.

## 15. Lock-Up Relay

조건부로 actuator chamber pressure를 hold한다.
항상 fail-close를 의미하지 않는다.

## 16. Quick Exhaust

Actuator chamber를 local exhaust로 빠르게 vent한다.
Booster와 다른 장치이다.

## 17. Solenoid Valve

Electrical command에 따라 pneumatic path를 switching한다.
SIS·ESD architecture는 Topic 15가 소유한다.

## 18. Volume Tank

Pneumatic energy를 저장한다.
Supply interruption 대응과 response tradeoff를 함께 검토한다.

## 19. Bench Set과 Calibration

Bench set은 actuator spring force range이다.
Positioner calibration은 command와 travel relation을 맞춘다.
같은 작업이 아니다.

## 20. Loop Test

DCS command, current, I/P pressure, positioner output, chamber pressure, travel과 fail action을 교차 확인한다.

## 21. Failure Response

Loss of signal, air, power, solenoid, I/P, positioner, booster와 lock-up failure를 각각 확인한다.

## 22. As-Found·As-Left

조정 전·후 current, pressure, travel, hysteresis, supply와 acceptance를 기록한다.

## 23. Topic 경계

- Topic 1: thrust, bench force와 spring sizing
- Topic 3: deadband, stiction, hunting와 response
- Topic 4: actuator type과 general structure
- Topic 10: balanced trim과 balance-seal friction
- Topic 12: smart diagnostics와 valve signature
- Topic 15: SIS·ESD·PST
- Topic 16: full package workflow

## 24. 대표 오답

- Positioner와 I/P는 같은 장치이다.
- I/P가 actual travel을 측정한다.
- Positioner는 open-loop device이다.
- Direct action은 항상 fail-open이다.
- 4 mA는 0 psi이다.
- Booster는 steady-state pressure amplifier이다.
- Quick exhaust와 booster는 같다.
- Lock-up은 항상 fail-close이다.
- Bench set과 calibration은 같다.
- Upstroke만 확인하면 된다.

## 25. 고득점 답안 기준

1. 전체 signal chain을 제시한다.
2. Positioner와 I/P를 구분한다.
3. Negative feedback와 error를 설명한다.
4. Current-pressure mapping을 계산한다.
5. Direct·reverse action과 fail action을 분리한다.
6. Multipoint up·down calibration을 설명한다.
7. Split-range local mapping을 설명한다.
8. Booster와 accessory 기능을 구분한다.
9. Failure response와 loop test를 포함한다.
10. Topic 1·3·4·10·12·15·16 경계를 명시한다.
