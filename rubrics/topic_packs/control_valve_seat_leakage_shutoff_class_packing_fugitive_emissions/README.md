# 제어밸브 시트 누설, 차단 등급, 패킹 및 비산배출

## Topic ID

`control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `DIAGNOSIS_ACTION`

Supported tertiary: `IMPLEMENTATION_EVALUATION`

## 핵심 범위

- Internal through-seat leakage와 external atmospheric leakage
- Shutoff class와 complete test-condition contract
- Shop test와 field operating leakage 경계
- Soft seat·metal seat trade-off
- Single·double seat와 balanced-trim leakage path
- Seat load·contact stress·pressure direction
- Gas·liquid와 volumetric·mass·bubble leakage basis
- Absolute pressure·temperature reference conversion
- Seat damage·contamination·thermal distortion·misalignment
- Stem·shaft packing과 leakage-friction trade-off
- Live-loaded·low-emission packing과 bellows seal
- Fugitive-emission screening·quantification
- Concentration와 mass-emission rate
- As-found·as-left, detection limit와 uncertainty
- Specification→test→installation→maintenance workflow

## Logic Check 정책

- Fact Anchor: 48
- Fatal misconception: 24
- Major conditional claim: 12
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator thrust·seat-load sizing: Topic 1
- Packing friction·stiction·dynamic response: Topic 3
- Cavitation·flashing damage physics: Topic 8
- Balanced trim·balance-seal mechanics: Topic 10
- Positioner·I/P calibration: Topic 11
- Valve signature·predictive diagnostics: Topic 12
- Severe-service package design: Topic 14
- SIS·ESD·PST·proof-test credit: Topic 15
- Full valve-package lifecycle: Topic 16

## Source

- `docs/topic_sheets/control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions.md`
- Control Valve Handbook seat leakage, packing and emissions sections
- Control Valve Primer seat sealing and field-maintenance sections
- Topic 1, Topic 3, Topic 8, Topic 10, Topic 11 and Topic 12 source packs
- `gemini_script/20260805_topic13_seat_leakage_packing_emissions_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
