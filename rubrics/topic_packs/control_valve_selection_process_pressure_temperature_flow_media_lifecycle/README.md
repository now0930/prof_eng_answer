# 공정 압력·온도·유량·유체 및 수명주기를 고려한 제어밸브 선정 절차

## Topic ID

`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `IMPLEMENTATION_EVALUATION`

Supported tertiary: `PROCEDURE`

## 핵심 범위

- Governing document와 requirement traceability
- Minimum·normal·maximum·startup·shutdown·upset operating case
- Pressure·temperature·flow·phase·composition·property envelope
- Control·shutoff·leakage·fail action·response·safety requirement
- Topic 1~15 specialist result hand-off와 cross-check
- Body·trim·characteristic·material·actuator·accessory package selection
- Datasheet·requisition·vendor bid·deviation·guarantee
- ITP·FAT·SAT·commissioning·installed-performance acceptance
- Reliability·availability·maintainability·spares·obsolescence
- Energy·downtime·lifecycle cost·field feedback·MOC·revalidation

## Logic Check 정책

- Fact Anchor: 52
- Fatal misconception: 26
- Major conditional claim: 14
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Topic 1~15가 actuator, characteristic, dynamic response, body taxonomy,
  authority, liquid·gas sizing, cavitation·flashing, noise, trim,
  accessories, diagnostics, leakage, severe service 및 SIS final element의
  전문 물리와 계산을 소유한다.
- Topic 16은 각 결과의 입력·가정·margin·limitation·evidence를 인수하여
  통합 package 선정, procurement, acceptance와 lifecycle closure를 소유한다.

## Source

- `docs/topic_sheets/control_valve_selection_process_pressure_temperature_flow_media_lifecycle.md`
- Approved Process Design Basis, PFD, P&ID, control narrative and SRS
- Project datasheet, requisition, vendor bid, deviation register and ITP
- FAT, SAT, commissioning, as-built and field-failure records
- Adjacent Topic 1~15 Source Packs
- `gemini_script/20260806_topic16_control_valve_selection_process_lifecycle_requirements.md`

Source JSON authored. Generated-bank build와 focused regression은 별도 단계에서 수행한다.
