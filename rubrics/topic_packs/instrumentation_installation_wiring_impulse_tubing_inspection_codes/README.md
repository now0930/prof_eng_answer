# 계측설비 설치·배선·도압배관·시공검사 및 기술기준

## Topic ID

`instrumentation_installation_wiring_impulse_tubing_inspection_codes`

## Criterion

`IC-2027-W-4-9`

## Question type

Primary: `IMPLEMENTATION_EVALUATION`

Supported secondary: `DIAGNOSIS_ACTION`

Supported tertiary: `PRINCIPLE_INTERPRETATION`

## Difficulty

`FIELD_APPLICATION`

## 핵심 범위

- Applicable regulation / project specification / approved drawing / vendor instruction 확인
- Instrument location, orientation, accessibility, maintenance clearance
- Enclosure, cable gland, unused entry sealing과 environmental integrity
- Cable tray / conduit routing과 mechanical protection
- Power·VFD와 instrumentation cable segregation의 현장 구현
- Bend radius / pulling tension / terminal / ferrule / lug / core identification
- Spare core 처리
- 승인된 grounding/shield termination의 physical implementation
- Intrinsic-safety / hazardous-area wiring segregation의 field execution
- Pressure / DP impulse tubing routing, slope, support, fitting, drain/vent
- Gas / liquid / steam service 차이
- DP high/low path의 hydrostatic·thermal bias 억제
- Root valve / manifold / drain / vent와 hook-up drawing 일치
- Installation inspection, punch, reinspection, closure evidence
- As-built reconciliation

## 핵심 답안 흐름

`승인기준 확인 → 현장 설치 → 배선·도압배관 품질 → 검사·Punch → As-built reconciliation`

## 중요한 경계

- FAT 합격은 field installation quality의 대체 evidence가 아니다.
- Impulse line slope는 모든 service에 동일하지 않다.
- Shield/grounding philosophy는 설치자가 임의 변경하지 않는다.
- 사용하지 않는 cable entry는 승인된 방식으로 닫아 enclosure integrity를 유지한다.
- Sensitive electronics가 연결된 회로에 임의의 동일 시험전압을 적용하지 않는다.
- Code/spec/drawing 충돌은 formal clarification/deviation으로 해결한다.

## Ownership boundary

- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - 전원·grounding topology·shield philosophy·EMC mitigation 설계
  - 본 Topic은 승인된 wiring/grounding/shield drawing의 **물리적 구현·검사**를 소유
- `instrumentation_system_design_basis_codes_standards_specification_deviation_management`
  - 적용 법규/표준 edition·Design Basis·specification·deviation의 상위 governance
  - 본 Topic은 승인된 기준의 **field implementation**을 소유
- `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
  - P&ID/loop/control narrative 설계
  - 본 Topic은 승인도서와 hook-up/termination document의 **현장 구현**을 소유
- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
  - 위험장소 분류·Ex/IS equipment selection
  - 본 Topic은 승인된 Ex/IS **installation condition**을 보존
- `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
  - FAT/SAT/commissioning 전체 acceptance
  - 본 Topic은 **field installation inspection과 punch/as-built evidence**를 소유

## Logic Check 정책

- Fact Anchor: 33
- Fatal misconception: 9
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Deterministic direct checks: disabled
- Direct score application: disabled
- Direct D/E effect: none

## Code/Standard policy

특정 법규·표준 edition과 project specification의 채택은 프로젝트·관할 authority에 따라 달라질 수 있다. 따라서 source pack은 특정 edition 번호를 고정하지 않고 **적용 기준 확인 → 승인도서 구현 → inspection evidence**의 원칙을 평가한다.

## Historical frequency

Historical frequency는 근거가 없으므로 사용하지 않는다.

## Source

- `docs/topic_sheets/instrumentation_installation_wiring_impulse_tubing_inspection_codes.md`
- Repository exam-scope criterion `IC-2027-W-4-9`
- Instrumentation field installation, wiring, impulse tubing, inspection and technical-code compliance fundamentals

Source JSON authored by ChatGPT. Generated rebuild, classification/release registration, focused regression and commit are later steps.
