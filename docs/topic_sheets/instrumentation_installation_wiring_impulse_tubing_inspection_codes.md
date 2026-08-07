# 계측설비 설치·배선·도압배관·시공검사 및 기술기준

## 1. Topic identity

- Topic ID: `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
- Criterion: `IC-2027-W-4-9`
- Lane: `SOFTWARE_LLM_LANE_A`
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Historical frequency: 사용하지 않음

## 2. 출제 의도

이 Topic은 cable tray나 impulse tubing 항목을 단순 나열하는 문제가 아니다. 승인된 설계의도가 실제 현장 설치에 정확히 구현되었는지 평가하고, 부적합을 inspection·punch·as-built evidence로 닫을 수 있는지를 평가한다.

핵심 답안 흐름은 다음과 같다.

`승인기준 확인 → 현장 설치 → 배선·도압배관 품질 → 검사·Punch → As-built reconciliation`

## 3. 설치 기준의 출발점

설치 전에 적용 법규·인허가 요구, project Design Basis/specification, approved drawing, hook-up/termination drawing, vendor instruction과 적용 표준을 확인한다.

문서 간 요구사항이 충돌하면 현장 작업자가 임의로 선택하지 않는다. Clarification, technical query 또는 deviation 등 승인된 절차로 기준을 확정한 후 시공한다.

## 4. 기기 위치와 접근성

Instrument의 location, elevation, orientation과 tapping point는 승인도면과 현장 간섭조건을 확인한다.

다음 작업이 가능한 접근성이 필요하다.

- Calibration
- Isolation
- Drain / vent
- Manifold operation
- Terminal inspection
- Maintenance replacement

구조물, piping, hot surface, vibration source와의 간섭도 확인한다.

## 5. Cable route와 mechanical protection

계장 cable은 승인된 tray·conduit·support route를 따른다.

- Sharp edge와 crushing 방지
- Excessive pulling tension 방지
- Minimum bend radius 준수
- Heat source와 water accumulation 위험 회피
- Mechanical damage 위험부 protection
- Cable support와 entry strain 관리

Power, motor/VFD와 low-level instrumentation cable의 segregation은 Topic 1의 EMC 설계를 현장에서 구현하는 사항이다. 설치자가 임의로 separation philosophy를 변경하지 않는다.

## 6. Cable gland와 terminal

Cable gland는 cable OD, armour/shield 구조와 enclosure entry에 적합해야 한다.

Unused entry는 승인된 blanking/sealing 방법으로 닫아 enclosure integrity를 유지한다.

Terminal 작업은 conductor를 손상시키지 않는 stripping length와 승인된 ferrule/lug를 사용한다. Loose strand, 과도한 conductor 노출과 접촉불량을 방지한다.

Cable, core, terminal, JB와 instrument tag는 도면과 일치하도록 양단에서 식별한다.

Spare core는 프로젝트 wiring philosophy에 따라 식별·절연·정리한다.

## 7. Shield와 특별 회로의 설치 경계

Shield의 one-end/both-end/360-degree termination을 선택하는 것은 Topic 1의 grounding/EMC 설계 범위이다.

본 Topic에서는 승인된 shield termination drawing이 실제 gland/JB/panel에서 올바르게 구현되었는지 확인한다.

Intrinsic-safety 또는 hazardous-area 회로는 승인된 segregation, terminal, gland/seal 조건을 보존한다. 회로 분류나 방폭기기 선정 자체는 별도 Topic의 소유이다.

## 8. Impulse tubing 공통 원칙

Impulse tubing은 가능한 짧고 단순한 route로 구성한다.

다음을 확인한다.

- Process service와 material compatibility
- Pressure / temperature rating
- Proper fitting assembly
- Internal cleanliness
- Sufficient support
- Vibration fatigue 방지
- Thermal expansion 허용
- Pocket·high point·low point 관리
- Mechanical damage protection
- Root valve / manifold / drain / vent accessibility

## 9. Service별 slope와 transmitter 위치

Impulse line slope는 모든 service에 동일하지 않다.

### Liquid service

Impulse path가 liquid-filled 상태를 유지하고 trapped gas가 측정오차를 만들지 않도록 routing, venting과 transmitter elevation을 결정한다.

### Gas service

Condensate가 impulse path에 고여 hydrostatic error를 만들지 않도록 condensate의 drain-back 방향과 transmitter elevation을 결정한다.

### Steam service

High-temperature steam이 transmitter에 직접 전달되지 않도록 condensate를 이용한 pressure transmission 철학을 적용한다. DP에서는 high/low 측 hydrostatic head가 불필요하게 달라지지 않도록 구성한다.

따라서 “모든 impulse line은 무조건 위로/아래로 slope한다”는 식의 절대 규칙은 부적절하다.

## 10. DP impulse path

DP transmitter의 high/low side는 두 pressure path의 차이를 측정한다. 따라서 두 impulse path에 불필요한 elevation, temperature 또는 liquid-column 차이가 생기면 측정값에 bias가 추가될 수 있다.

다음을 관리한다.

- Route asymmetry 최소화
- Unwanted pocket 방지
- Similar thermal exposure
- Proper support
- Correct high/low connection
- Manifold / vent / drain arrangement
- Cleanliness와 leak integrity

## 11. Installation inspection

Inspection은 최소 다음 chain을 가진다.

1. 적용도면·자재·tag 확인
2. Location / orientation / accessibility 확인
3. Cable route / gland / termination / identification 확인
4. Impulse tubing / fitting / support / manifold 확인
5. Required continuity 및 승인된 시험 확인
6. Punch 등록
7. Corrective action
8. Reinspection
9. Closure evidence
10. As-built reconciliation

Sensitive electronics가 연결된 회로의 insulation-related test는 기기 허용조건과 승인 절차를 확인한다.

## 12. FAT와 현장검사의 차이

FAT는 panel, software, logic, communication 등 공장단계 acceptance evidence가 될 수 있다.

그러나 FAT는 다음 현장 시공품질을 증명하지 않는다.

- Actual cable route
- Field gland/seal
- Junction-box termination
- Instrument mounting
- Impulse tubing slope
- Manifold / root connection
- Field support
- Punch closure
- As-built condition

따라서 field installation inspection은 별도로 필요하다.

## 13. Ownership boundary

### Topic 1 — Power / grounding / shielding / EMC

`instrumentation_power_grounding_shielding_ups_ground_loop_emc`

Grounding topology, shield termination philosophy와 EMC mitigation 선정은 Topic 1이 소유한다. Topic 2는 그 승인 설계의 physical installation을 소유한다.

### Design Basis / Code governance

`instrumentation_system_design_basis_codes_standards_specification_deviation_management`

적용 법규·표준 edition, Design Basis, project specification과 deviation governance는 이 Topic이 소유한다. Topic 2는 확정된 요구사항의 field implementation을 소유한다.

### P&ID / Loop documents

`pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`

P&ID symbol, tag, loop와 control narrative의 설계는 해당 Topic이 소유한다. Topic 2는 승인도서와 hook-up/termination document를 현장에 구현한다.

### Hazardous area / Ex / IS selection

`hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

위험장소 분류와 Ex/IS equipment selection은 해당 Topic이 소유한다. Topic 2는 승인된 installation condition을 보존한다.

### FAT / SAT / Commissioning

`control_software_project_engineering_documents_fat_sat_commissioning_acceptance`

전체 FAT/SAT/commissioning acceptance는 해당 Topic이 소유한다. Topic 2는 field installation inspection, punch와 as-built evidence를 소유한다.

## 14. 고득점 답안 조건

고득점 답안은 다음을 포함한다.

- Applicable document hierarchy
- Field location / accessibility
- Cable route / gland / terminal 품질
- Service-specific impulse tubing
- DP high/low hydrostatic bias
- Inspection / punch / reinspection
- As-built reconciliation
- FAT와 field evidence의 구분
- 인접 Topic과 ownership boundary

## 15. Code/Standard policy

실제 프로젝트의 법규·표준 edition과 project specification은 관할 authority, 산업, client requirement와 계약조건에 따라 달라질 수 있다.

따라서 이 Topic Pack은 특정 edition 번호를 고정하지 않는다. 답안에서는 **적용 기준을 확인하고 승인된 설치 요구를 현장에 구현하며 inspection evidence로 검증하는 원칙**을 중심으로 평가한다.

Historical frequency는 근거가 없으므로 사용하지 않는다.
