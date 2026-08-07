# 계측기 환경·EMC/EMI·온도·습도·진동 Qualification 및 검증

## 1. Topic identity

- Topic ID: `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
- Criterion: `IC-2027-W-3-10`
- Lane: `SOFTWARE_LLM_LANE_A`
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Historical frequency: 사용하지 않음

## 2. 출제 의도

이 Topic은 “온도시험, 습도시험, 진동시험을 한다”는 항목 나열 문제가 아니다.

Qualification은 다음 chain으로 평가한다.

`Requirement → Test Plan/Setup → Stress Exposure → Functional Monitoring → Acceptance → Failure Analysis/Corrective Action → Re-test/Report`

핵심은 시험조건의 근거, 실제 사용상태를 대표하는 DUT configuration, 시험 중 기능감시, 합격기준과 failure closure evidence이다.

## 3. EMC와 EMI

EMC는 장비가 전자기 환경에서 요구기능을 수행하면서 주변에 과도한 방해를 주지 않는 적합성 개념이다.

EMI는 실제 기능에 영향을 주는 전자기 interference 현상이다.

따라서 EMC와 EMI를 같은 용어로 취급하지 않는다.

## 4. Emission과 Immunity

### Emission

DUT가 cable, enclosure 또는 power/I/O path를 통해 외부로 발생시키는 electromagnetic disturbance를 평가한다.

### Immunity

외부 electromagnetic disturbance가 DUT에 가해질 때 요구기능을 유지하는지 평가한다.

시험항목은 applicable requirement에 따라 conducted/radiated emission, RF immunity, ESD, EFT/burst, surge 및 전원/자기장 관련 immunity 등에서 선정한다.

모든 DUT에 모든 시험을 동일 test level로 적용하는 것이 원칙은 아니다.

## 5. Qualification requirement와 setup

시험 전에 다음을 정의한다.

- Applicable product / project / regulatory requirement
- DUT hardware / firmware / software revision
- Power supply
- I/O and load condition
- Cable type / length / termination
- Grounding / bonding
- Auxiliary equipment
- Operating mode
- Test severity / duration
- Monitoring point
- Acceptance criteria

시험 severity와 duration은 installation environment와 applicable requirement에서 추적되어야 한다.

## 6. DUT operating mode

시험은 idle 상태만 보는 것이 아니다.

Emission이 큰 상태와 susceptibility가 큰 상태를 포함하여 실제 기능을 대표하는 operating mode를 선정한다.

예:

- Sensor input active
- Analog output varying
- Digital communication active
- Relay / discrete I/O operating
- Controller computation / network traffic active

실제 장비 기능에 맞게 선택한다.

## 7. Pre-test baseline과 시험 중 monitoring

Stress 전에 기능 baseline을 확보한다.

- Output / accuracy
- Communication
- Alarm / status
- Reset history
- Visual condition
- 필요 시 insulation / calibration state

시험 중에는 다음을 감시한다.

- Output deviation
- Intermittent error
- Reset
- Communication loss
- Alarm
- Relay chatter
- Automatic recovery
- Manual intervention 필요 여부

시험 종료 후 전원 on/off만 확인하는 것은 충분하지 않다.

## 8. Acceptance criteria

합격기준은 시험 전에 정한다.

다음을 구분한다.

- 허용 가능한 temporary degradation
- Automatic recovery 허용 여부
- Manual intervention 허용 여부
- Safety / control function interruption 허용 여부
- 시험 후 residual degradation
- Calibration / accuracy shift 허용범위

Result를 본 뒤 acceptance criteria를 변경하면 qualification evidence의 신뢰성이 떨어진다.

## 9. Temperature qualification

Operating과 storage/non-operating temperature requirement를 구분한다.

확인사항:

- DUT self-heating
- Thermal stabilization
- Hot / cold condition
- Temperature gradient
- Operating function
- Post-stress calibration shift

Cycle, dwell, transition rate와 thermal shock 적용 여부는 applicable requirement에서 결정한다.

## 10. Humidity qualification

Humidity는 다음 failure mechanism을 유발할 수 있다.

- Insulation resistance 저하
- Leakage
- Corrosion
- Condensation
- Creepage / short risk
- Sensor / electronics drift

Condensing condition과 non-condensing condition을 동일하게 취급하면 안 된다.

시험 후에는 recovery 상태와 corrosion/insulation evidence를 확인한다. 건조 후 정상복귀했다고 해서 시험 중 temporary failure가 없었던 것으로 처리하지 않는다.

## 11. Vibration qualification

Vibration profile은 실제 환경과 applicable requirement에 따라 sine, resonance search/endurance 또는 random profile 등에서 선정한다.

핵심 setup:

- Axis
- Fixture
- Mounting torque
- DUT orientation
- Cable restraint
- Accelerometer / monitoring location

시험 중에는 다음을 확인한다.

- Intermittent contact
- Connector / terminal looseness
- Output noise
- Relay chatter
- Communication dropout
- Resonance symptom

시험 후에는 crack, fretting, fastener looseness, PCB/support damage와 calibration shift를 검사한다.

## 12. 시험장비와 uncertainty

Qualification evidence를 만드는 chamber, field probe, accelerometer, power analyzer와 functional measurement equipment는 필요한 calibration/verification 상태를 확인한다.

Pass/fail boundary에 가까운 결과는 measurement uncertainty, test equipment tolerance와 setup repeatability를 고려하여 margin을 평가한다.

## 13. Failure 처리

Qualification failure가 발생하면 다음 evidence를 확보한다.

1. Stress type / condition
2. Failure 발생 time
3. DUT operating mode
4. Waveform / log
5. Error code
6. Reset / recovery 상태
7. 재현조건

Root cause는 다음 chain으로 분석한다.

`Stress source → Coupling / Physical mechanism → Affected circuit/function → Symptom`

증상만 보고 filter, shielding, damping material을 임의 추가하는 방식은 부적절하다.

## 14. Corrective action과 Re-test

대책 적용 후에는 변경 영향범위를 평가한다.

실패했던 시험만 재시험할지, 관련 emission/immunity 또는 environmental qualification까지 다시 확인할지는 change impact와 risk를 근거로 결정한다.

Hardware, PCB, enclosure, connector/cable, firmware, filter/bonding 변경 후 이전 qualification pass를 자동 승계하지 않는다.

## 15. Qualification report

Report는 최소 다음 traceability를 갖는다.

- Requirement ID
- DUT serial / configuration / revision
- Firmware / software version
- Test setup
- Test equipment
- Calibration / verification status
- Test condition
- Deviation
- Raw / summary result
- Failure evidence
- Corrective action
- Re-test result
- Final disposition

## 16. Ownership boundary

### Topic 1 — Power / Grounding / Shielding / Field EMC

`instrumentation_power_grounding_shielding_ups_ground_loop_emc`

Plant의 EMI noise, ground loop와 field grounding/shielding 대책은 Topic 1이 소유한다.

Topic 3는 controlled qualification condition과 pass/fail evidence를 소유한다.

### Topic 2 — Physical installation

`instrumentation_installation_wiring_impulse_tubing_inspection_codes`

Cable route, gland, wiring, tubing과 field installation inspection은 Topic 2가 소유한다.

Topic 3는 qualification setup이 representative installation condition을 구현했는지 평가한다.

### Topic 4 — Hardware lifecycle

`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

HW architecture, component selection, prototype/production verification 전체 lifecycle은 Topic 4가 소유한다.

Topic 3는 environmental/EMC qualification evidence를 독립 소유한다.

### Topic 5 — Electronic error chain

`electronics_error_noise_drift_tolerance_aging_power_mitigation`

Component-level noise, drift, tolerance, aging, power variation error chain은 Topic 5가 소유한다.

Topic 3는 environmental stress 하 DUT function qualification을 소유한다.

## 17. 고득점 답안 조건

고득점 답안은 다음을 포함한다.

- EMC/EMI와 emission/immunity 구분
- Applicable requirement traceability
- Representative setup와 worst-case operating mode
- Pre-test baseline
- In-test monitoring
- Predefined acceptance criteria
- Temperature/humidity/vibration별 failure mechanism
- Failure evidence와 root-cause chain
- Corrective action / re-test / change impact
- Qualification report traceability
- Topic 1/2/4/5 boundary

## 18. Standard policy

실제 standard edition, severity, dwell time, sweep range, test level과 acceptance class는 제품군, 프로젝트와 관할 요구에 따라 달라질 수 있다.

따라서 이 Topic Pack은 출처 없는 특정 수치를 고정하지 않는다.

Historical frequency는 근거가 없으므로 사용하지 않는다.
