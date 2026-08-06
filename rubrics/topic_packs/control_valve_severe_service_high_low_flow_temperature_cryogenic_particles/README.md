# 제어밸브 가혹 운전: 고·저유량, 고온·저온·극저온 및 입자성 유체

## Topic ID

`control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`

## Question type

Primary: `COMPARE_SELECTION`

Supported secondary: `IMPLEMENTATION_EVALUATION`

Supported tertiary: `DIAGNOSIS_ACTION`

## 핵심 범위

- Severe-service combined operating envelope
- High-flow local velocity, hydraulic power와 downstream effect
- Low-flow minimum controllable flow와 micro-flow trim
- High-temperature strength, derating, expansion와 heat soak
- Cryogenic toughness, contraction, extended bonnet와 cavity pressure
- Particle·slurry·fibrous·sticky fluid characterization
- Full-port·rotary·angle·eccentric와 cage·multi-hole geometry
- Hardfacing·coating·ceramic와 material compatibility
- Purge·flushing·drain·vent·clean-out
- Multiphase·entrained-gas uncertainty
- Wear·clearance trend, inspection와 spare trim
- Vendor qualification, purchaser acceptance와 lifecycle trade-off

## Logic Check 정책

- Fact Anchor: 48
- Fatal misconception: 24
- Major conditional claim: 12
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator thrust·fail-safe sizing: Topic 1
- Deadband·stiction·response: Topic 3
- General body·actuator taxonomy: Topic 4
- Authority·gain·rangeability: Topic 5
- Liquid sizing: Topic 6
- Gas sizing: Topic 7
- Cavitation·flashing: Topic 8
- Noise prediction·mitigation: Topic 9
- Balanced trim·seal mechanics: Topic 10
- Diagnostics·predictive maintenance: Topic 12
- Seat leakage·packing·emissions: Topic 13
- SIS·ESD·PST: Topic 15
- Full package lifecycle: Topic 16

## Source

- `docs/topic_sheets/control_valve_severe_service_high_low_flow_temperature_cryogenic_particles.md`
- Control Valve Handbook severe-service and special-service sections
- Control Valve Primer material, trim and field-maintenance sections
- Topic 1, 3, 4, 5, 6, 7, 8, 9, 10, 12 and 13 source packs
- `gemini_script/20260805_topic14_severe_service_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
