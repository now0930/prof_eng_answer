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

Fisher 3570 action 변경은 해당 매뉴얼의 별도 절차다. 밸브 조립체를 service에서 분리하기 전에 임시 공정제어를 확보하고, control valve를 bypass한 뒤 positioner input signal·supply pressure를 차단한다. 변경 후 adjustment procedure로 동작을 확인하고 action label을 갱신한다. 이를 모든 positioner나 manual handwheel의 공통 복귀순서로 일반화하지 않는다.

Fisher 3570은 주문된 travel·input range·action으로 출고된다. 제조사 매뉴얼은 운전조건 변경, 분해·재조립, 또는 valve travel과 요구 input range의 불일치가 있을 때 조정 필요성을 검토하고 명판 범위와 현재 조건을 대조하도록 한다. 모든 ΔP 변화나 startup/shutdown이 자동으로 재교정을 요구한다는 뜻은 아니다.

같은 매뉴얼에서 bias spring은 zero/시작점, range spring은 span/full travel, relay-nozzle 조정은 steady-state output pressure를 정한다. 이는 Fisher 3570의 조정구조이며 다른 positioner의 cam, I/P converter 또는 booster 설정을 대변하지 않는다.

같은 매뉴얼에서 bias spring은 zero/시작점, range spring은 span/full travel, relay-nozzle 조정은 steady-state output pressure를 정한다. 이는 Fisher 3570의 조정구조이며 다른 positioner의 cam, I/P converter 또는 booster 설정을 대변하지 않는다.

Positioner endpoint의 표시 travel과 밸브 nominal travel은 장치별 매뉴얼에 따라 확인한다. Masoneilan SVI II ESD는 full stroke가 nominal valve travel보다 큰 일부 valve에서 표시 100%를 nominal travel에 맞추는 STOP OP 보정을 제공한다. Fisher DVC2000은 Travel Cutoff Low가 seat load 확보에 쓰일 수 있다고 설명하고 해당 모델의 0.5% 설정을 권고한다. 이 설정값을 다른 모델에 일반화하지 않는다.

## 9. Multipoint Verification

IEC 62382:2024 Annex A.4의 control-stroke 예는 full-open·full-close 및 25·50·75% 중간점을 포함한다.
중간점은 증가·감소 방향에서 검사해 hysteresis를 확인한다. 시험점과 acceptance criteria는 project loop plan으로 정한다.

## 10. Calibration Error

$$E_{FS}=100\frac{y_{meas}-y_{cmd}}{y_{max}-y_{min}}$$
Tolerance는 site·vendor basis를 확인한다.

## 11. Hysteresis

$$H=y_{up}-y_{down}$$
IEC 62382:2024 Annex A.4 control-stroke 예는 중간 travel을 증가·감소 방향에서 비교해 hysteresis를 확인한다. Up/down 차이만으로 deadband 또는 stiction 원인을 단정하지 않는다. Deadband·stiction·hunting의 상세 진단은 Topic 3이 소유한다.

## 12. Split Range

$$x_s=\frac{I-I_{s,min}}{I_{s,max}-I_{s,min}}$$
각 segment의 own range, gap, overlap와 fail action을 확인한다.

## 13. Volume Booster

Fisher 2625·2625SST·2625NS는 제조사 자료상 설계 deadband 안에서 입력 pilot pressure와 동일한 출력압력을 내는 1:1 volume booster이다.
$$P_{out}=P_{pilot}\quad\text{within the specified deadband, for these models}$$
이는 해당 제품군의 사양이다. 다른 booster 모델의 압력비는 제조사 자료에서 확인하며, volume booster의 압력비를 보편 명제로 단정하지 않는다.
Booster는 큰 입력변화에서 높은 fill·vent flow를 공급하여 stroke speed를 높일 수 있다.
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

같은 온도·압력대역에서 저장 기체량 변화는 이상기체식 Δn=VΔP/(RT)에 비례한다.
같은 공급 질량유량·부하에서는 더 큰 용적이 저장 공기량과 잠재적 압력지원시간을 늘리지만 충전시간도 늘린다.
실제 유지시간·actuator response는 누설, 부하, 압력대역과 공급·배기 용량에 따라 달라지며 고정된 hold time을 보장하지 않는다.

## 18.1 Tubing·Fitting·Actuator Volume

충전·배기 응답은 actuator 요구 기체량과 positioner·booster·배관 경로의 실제 유량용량에 좌우된다.
제한적 경로는 압력강하와 응답지연을 만들 수 있다. Fisher VBL 매뉴얼은 booster 용량수요에 맞춘 배관과 actuator 연결부 선정을 지시한다.
Tube size, pressure drop과 stroke time은 모델 용량·배관 구성·부하조건으로 산정하며 보편값으로 단정하지 않는다.

## 19. Bench Set과 Calibration

Bench set은 actuator spring force range이다.
Positioner calibration은 command와 travel relation을 맞춘다.
같은 작업이 아니다.

## 20. Loop Test

IEC 62382 loop functional check 목적은 한 시험에서 구성 loop의 개별 및 통합 동작을 확인하는 것이다.
Electropneumatic valve에서는 실제 구성에 따라 DCS command, current, I/P·positioner/actuator pressure, travel·feedback point를 loop plan에 맞춰 확인한다.

## 21. Failure Response

IEC 62382:2024 Annex A.4는 actuator failure simulation(예: air 또는 electrical signal loss) 후 올바른 reaction을 확인하는 예를 든다.
시험 시나리오와 기대 fail position은 실제 loop 설계·acceptance criteria에 따르며 SIS validation을 대신하지 않는다.

## 22. As-Found·As-Left

Calibration 전 as-found 상태와 조정·검증 후 as-left 상태를 구분해 기록한다.
Current, pressure, travel, hysteresis 등 항목과 acceptance 기준은 장치와 적용 절차에 맞춘다.
Fisher DVC6200은 calibration 전에 signature 진단으로 as-found data를 취득할 수 있으며, NIST는 calibration report에 pre/post data를 포함하라고 권고한다.

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
- Fisher 2625·2625SST·2625NS가 제조사 명시 1:1 pressure follower가 아니라 압력비 증폭기라고 설명한다.
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
