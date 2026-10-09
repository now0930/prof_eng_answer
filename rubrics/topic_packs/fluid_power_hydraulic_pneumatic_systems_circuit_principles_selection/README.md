# 유공압 시스템·유압회로의 원리와 구성요소 선정

## Topic ID

`fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection`

## State

Approval state and reviewer are recorded in `topic_status.json`. The managed
source is human-reviewed; repository-wide integration and runtime Authority
Gate remain separate.

## Ownership

This Topic owns general industrial fluid-power fundamentals: hydraulic and
pneumatic system components, circuit functions, working-fluid distinctions,
basic actuators, auxiliaries, and application trade-offs. It includes
electrohydraulic servo/proportional valve operation only at the fluid-power
stage level.

It does not own process control-valve body/actuator selection, process-valve
sizing, valve positioner calibration, general control theory, or instrument
measurement. These boundaries and named handoffs are in the Topic Sheet.

## Evidence quality

The local source cluster contains five substantive technical summaries, one
exam prompt, one symbol-only post with no stored body, and one empty post. The
lecture notes contain OCR and simplified or condition-dependent equations;
they are coverage evidence rather than unquestioned authority. Pressure
ratings, Reynolds thresholds, component performance comparisons, and
manufacturer-specific servo-valve structures are not asserted as universal
facts.

## Grading scope

The source rubric covers system architecture, component roles, hydraulic/
pneumatic contrasts, circuit interpretation, and field constraints. The
additive provider-free machine contract is deliberately narrow: it checks only
that hydraulic systems use liquid working fluid and pneumatic systems use
gas. It cannot grade every equation, circuit, or application choice and does
not establish the overall service Authority Gate.

## Validation and release

Focused source validation and the provider-free routing/contract regression
test must pass. The approval record is bound to the reviewed README and source
JSON hashes. Run `validate-topic-pack-release --all` before commit or push.
