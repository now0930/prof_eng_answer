# 제어 Hardware Lifecycle·Panel Architecture·부품선정·생산검증

## 1. Topic identity

- Topic ID: `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`
- Criterion: `IC-2027-W-3-9`
- Lane: `SOFTWARE_LLM_LANE_A`
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Historical frequency: 사용하지 않음

## 2. 출제 의도

이 Topic은 제어반 부품을 나열하는 문제가 아니다.

Hardware를 반복 생산 가능한 engineering product로 만들기 위해 다음 lifecycle을 설명해야 한다.

`Requirement → Architecture/Interface → Component Selection → Design Verification → Manufacturability/Production Control → Production Verification → Configuration/Release`

핵심은 requirement traceability, 설계 margin, design verification와 production variation의 분리, configuration evidence이다.

## 3. Hardware requirement

Hardware requirement는 system requirement에서 hardware 책임을 분리한다.

주요 항목:

- Power input / consumption
- Analog / digital I/O
- Communication
- Electrical interface
- Isolation
- Performance
- Environment
- Reliability
- Maintainability
- Safety / application constraint
- Mechanical / enclosure interface
- Diagnostic / fault behavior

각 requirement는 architecture와 verification evidence까지 추적한다.

## 4. Panel / Product Architecture

Hardware architecture는 기능을 block으로 partitioning한다.

예:

- Power input / protection
- Power conversion / distribution
- Controller / processor
- Analog I/O
- Digital I/O
- Signal conditioning
- Communication
- Isolation
- Terminal / connector
- Enclosure / thermal

Partitioning의 목적은 interface를 명확히 하고 fault propagation, maintainability와 verification boundary를 관리하는 것이다.

## 5. Interface definition

각 interface는 다음을 정의한다.

- Signal type / range
- Electrical level
- Source / load capability
- Isolation
- Connector / terminal
- Communication physical layer
- Fault state
- 필요 시 timing / update condition

암묵적인 interface assumption은 prototype에서는 동작해도 양산 또는 현장 연결에서 문제를 만들 수 있다.

## 6. Power budget와 protection

Power budget은 nominal load만 계산하지 않는다.

- Normal load
- Peak / startup load
- Supply tolerance
- Conversion loss
- Protection device
- Future/design margin
- Branch capability

Power protection은 applicable requirement에 따라 overcurrent, short, reverse polarity, over/undervoltage, surge/transient 등의 위험을 다룬다.

Protection 자체가 정상전압강하나 nuisance trip을 만들지 않는지도 검토한다.

## 7. Component selection

Component selection은 nominal rating 비교만으로 끝나지 않는다.

다음을 통합하여 평가한다.

- Voltage / current / power rating
- Temperature / environment
- Derating
- Tolerance / accuracy requirement
- Interface compatibility
- Lifecycle / availability
- Second source 가능성
- Maintainability / replaceability
- Quality grade
- Safety / application requirement

### Derating

Derating은 component stress를 rating 한계에서 떨어뜨려 reliability margin을 확보하는 방법이다.

모든 component에 동일한 percentage를 적용하는 것이 아니다. Component type, manufacturer data와 applicable requirement에 따라 기준을 정한다.

## 8. Thermal과 physical layout

Thermal design은 다음을 고려한다.

- Component dissipation
- Power conversion loss
- Enclosure heat accumulation
- Ambient condition
- Airflow / cooling path
- Hotspot

Physical panel layout은 thermal만 보는 것이 아니다.

- Power/noise source와 sensitive I/O 배치
- Maintenance clearance
- Terminal access
- Cable entry
- Replaceability
- Functional partition

을 함께 고려한다.

## 9. I/O / Communication hardware

I/O module은 다음을 확인한다.

- Signal type / range
- Input loading
- Output drive
- Isolation
- Accuracy / resolution requirement
- Update requirement
- Diagnostics
- Fault state

Communication hardware는 protocol 논리와 구분하여 physical layer, media/connector, isolation, compatibility, port/recovery requirement를 확인한다.

## 10. Design Review

Design review는 문서 확인만 하는 행위가 아니다.

다음 설계 risk를 단계별로 확인한다.

- Requirement traceability
- Architecture / interface consistency
- Schematic
- BOM
- Layout
- Power margin
- Thermal margin
- Failure risk
- Testability
- Manufacturability
- Maintainability

Open action은 owner와 closure evidence를 남긴다.

## 11. Verification과 Validation

Verification:

`설계가 specified requirement대로 구현되었는가?`

Validation:

`최종 intended use와 상위 운용요구에 적합한가?`

두 개념은 연관되지만 동일하지 않다.

Hardware Topic에서는 requirement별 design verification evidence가 핵심이다.

## 12. Verification Plan

각 requirement에 대해 다음을 사전에 정의한다.

- Verification method
  - Analysis
  - Inspection
  - Test
  - Demonstration
- DUT configuration
- Test condition
- Acceptance criterion
- Evidence owner

시험결과를 본 뒤 기준을 맞추는 방식은 verification 신뢰성을 떨어뜨린다.

## 13. Prototype / Design Verification

Prototype은 architecture와 design margin을 검증하는 중요한 단계이다.

확인 예:

- Power
- I/O
- Interface
- Protection
- Fault response
- Thermal behavior
- Diagnostic path
- Requirement-specific function

그러나 prototype pass는 production readiness가 아니다.

Prototype은 production variation과 manufacturing process capability를 충분히 대표하지 않을 수 있다.

## 14. DFM / DFA

양산 전에 manufacturability와 assembly variation을 검토한다.

- Component orientation
- Assembly sequence
- Tool access
- Mistake proofing
- Inspection access
- Repetitive work variation
- Repair / rework

목표는 “조립 가능”이 아니라 “반복적으로 동일 품질로 생산 가능”이다.

## 15. BOM / Configuration

다음을 configuration baseline으로 관리한다.

- BOM
- Schematic
- Drawing
- PCB / panel revision
- Approved component/source
- Firmware dependency
- Manufacturing instruction
- Test configuration

생산 unit이 어느 revision으로 만들어졌는지 trace할 수 있어야 한다.

## 16. Production Control

Production control에는 다음이 포함된다.

- Incoming material identity / source 확인
- Controlled work instruction
- Process condition
- Tool status
- Required inspection
- Label / traceability
- Nonconformance handling

Crimp, torque, soldering, connector mating 등 품질에 영향을 주는 공정은 작업방법과 검사방법이 관리되어야 한다.

## 17. Production Verification

Production test의 목적은 design verification 전체를 반복하는 것이 아니다.

주요 목적은 제조변동, 오조립, 부품불량을 unit 수준에서 검출하는 것이다.

따라서 critical path에 대한 test coverage를 설계한다.

EOL/final production test의 예:

- Power-up
- Supply current
- I/O channels
- Communication ports
- Diagnostics
- Alarm
- Protection path
- 필요 시 calibration-related checks

Test result는 unit와 연결하여 추적한다.

## 18. Test Fixture

Production test fixture와 test software도 production quality를 만드는 측정시스템이다.

다음을 관리한다.

- Version
- Calibration / verification
- Known-good / reference check
- Change control

Fixture 문제를 DUT defect로 오판하거나 DUT defect를 놓치지 않게 해야 한다.

## 19. Nonconformance와 Rework

Production failure는 다음 chain으로 닫는다.

`Detect → Contain → Classify → Disposition → Rework → Reinspection/Retest → Closure`

임의 repair 후 정상 unit로 출하하지 않는다.

## 20. Change Impact와 Re-verification

다음 변경은 verification evidence에 영향을 줄 수 있다.

- Component substitution
- PCB/layout
- Panel wiring architecture
- Power design
- Connector
- Enclosure
- Manufacturing process

Impact assessment 결과에 따라 필요한 design verification, environmental requalification 또는 production test update 범위를 결정한다.

## 21. Release Gate

Hardware release 전에 다음을 확인한다.

- Open design action 없음
- Requirement verification gap 없음
- Unresolved critical nonconformance 없음
- Approved BOM/source
- Production-test coverage 완료
- Configuration baseline 완료
- Evidence package 완료

## 22. Ownership boundary

### Topic 1 — Power / Grounding / EMC mechanism

`instrumentation_power_grounding_shielding_ups_ground_loop_emc`

Grounding topology, shielding, ground loop와 EMC mechanism은 Topic 1이 소유한다.

Topic 4는 해당 requirement를 hardware architecture와 DV에 반영한다.

### Topic 2 — Field installation

`instrumentation_installation_wiring_impulse_tubing_inspection_codes`

Field cable/gland/wiring/tubing installation은 Topic 2가 소유한다.

Topic 4는 panel/product 내부 hardware implementation과 manufacturing을 소유한다.

### Topic 3 — Environmental / EMC Qualification

`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

온도·습도·진동·EMC qualification 상세 시험은 Topic 3가 소유한다.

Topic 4는 qualification requirement/result를 hardware lifecycle release gate에 연결한다.

### Topic 5 — Electronics error chain

`electronics_error_noise_drift_tolerance_aging_power_mitigation`

Noise, drift, tolerance, aging, power variation의 detailed component-level error mechanism은 Topic 5가 소유한다.

Topic 4는 requirement 수준의 accuracy/tolerance margin과 component selection을 소유한다.

### Software lifecycle

`instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`

Software V-model은 해당 Topic이 소유한다.

Topic 4는 hardware lifecycle을 소유한다.

### FAT / SAT / Commissioning

`control_software_project_engineering_documents_fat_sat_commissioning_acceptance`

Project FAT/SAT/commissioning acceptance는 해당 Topic이 소유한다.

Topic 4는 hardware design verification와 production verification을 소유한다.

## 23. 고득점 답안 조건

고득점 답안은 다음을 포함한다.

- Requirement traceability
- Architecture / interface
- Component selection / derating
- Power / thermal margin
- Verification vs validation
- Prototype ≠ production readiness
- DFM / DFA
- Configuration baseline
- Production test coverage
- Fixture/test software control
- Nonconformance / retest
- Change impact / release gate
- Adjacent Topic ownership boundary

## 24. Fixed-number policy

Specific derating percentage, design margin, production test limit와 standard edition은 component type, manufacturer data와 applicable project/product requirement에 따라 달라질 수 있다.

따라서 이 Topic Pack은 출처 없는 특정 수치를 고정하지 않는다.

Historical frequency는 근거가 없으므로 사용하지 않는다.
