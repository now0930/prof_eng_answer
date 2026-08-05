# 스마트 포지셔너 진단, 밸브 시그니처 및 예지보전

## Topic ID

`smart_positioner_diagnostics_valve_signature_predictive_maintenance`

## Question type

Primary: `DIAGNOSIS_ACTION`

Supported secondary: `IMPLEMENTATION_EVALUATION`

Supported tertiary: `PRINCIPLE_INTERPRETATION`

## 핵심 범위

- Smart-positioner diagnostic data chain
- Online monitoring과 offline diagnostic test
- Static valve signature와 dynamic operating signature
- Comparable as-left baseline과 operating context
- Travel error·hysteresis·actuator-pressure band
- Conditional friction proxy와 process-force confounding
- Supply·I/P·relay·air-consumption·feedback-sensor health
- Cycle·accumulated travel·stroke-time trend
- Residual·percentage·rate-of-change trend
- Alarm persistence·deadband·confidence·data quality
- Multi-evidence failure isolation
- Time-based·condition-based·predictive maintenance
- Detect→verify→diagnose→prioritize→plan→repair→as-left
- HART·Fieldbus·asset-management integration
- As-found·as-left와 work-order feedback

## Logic Check 정책

- Fact Anchor: 44
- Fatal misconception: 24
- Major conditional claim: 12
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Physical force·friction sizing: Topic 1
- Deadband·stiction·hysteresis·response 시험과 tuning: Topic 3
- Positioner·I/P·booster·accessory 원리와 calibration: Topic 11
- Seat leakage·packing·fugitive emissions: Topic 13
- SIS·ESD·PST와 proof-test credit: Topic 15
- Full valve-package lifecycle: Topic 16

## Source

- `docs/topic_sheets/smart_positioner_diagnostics_valve_signature_predictive_maintenance.md`
- Control Valve Handbook smart positioner, diagnostic data and valve-signature sections
- Control Valve Primer valve-positioner diagnostics and maintenance sections
- Topic 1, Topic 3, Topic 10 and Topic 11 source packs
- `gemini_script/20260805_topic12_smart_positioner_diagnostics_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
