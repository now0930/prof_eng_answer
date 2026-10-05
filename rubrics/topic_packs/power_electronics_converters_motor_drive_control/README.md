# 전력전자 변환기와 전동기 구동의 원리 및 적용

## Topic ID

`power_electronics_converters_motor_drive_control`

## State

Approval state and reviewer are recorded in `topic_status.json`. The managed
source is human-reviewed; repository-wide integration and runtime Authority
Gate remain separate.

## Ownership

This Topic owns the power-conversion stages and drive-level application of
power-semiconductor switching: AC-DC rectifiers, DC-DC converters, DC-AC
inverters, AC-AC control, PWM, and the principles used to control induction
motor speed and torque. It connects topology, control objective, waveform,
losses, harmonics, protection, and selection.

It does not own detailed motor electromagnetic design, general PID/state-space
or frequency-response design, or shaft-speed sensor measurement and selection.
See the Topic Sheet for explicit handoffs to the speed-measurement,
instrumentation-power/EMC, hazardous-area, and control-theory Topics.

## Representative questions

- Explain AC-DC, DC-DC, DC-AC, and AC-AC converter functions and applications.
- Compare power semiconductor devices by controllability and converter role.
- Explain phase-controlled rectification and PWM DC-DC output control.
- Compare VSI and CSI inverters and explain PWM performance trade-offs.
- Compare V/f and field-oriented control for induction-motor drives.
- Discuss converter/drive efficiency, harmonics, thermal design, EMC, protection,
  regeneration, and commissioning.

## Approved-fact boundary

Only the basic converter output-direction claims are currently wired into the
additive machine contract. The contract can check these selected claims without
an LLM provider; it does not cover all learning objectives or certify a
provider-free final score for every question in this Topic.

The source blog notes include OCR, copied textbook fragments, and conversational
explanations. They are evidence for candidate coverage, not an authority for
canonical equations or topology-independent claims. In particular, switching
equations, SCR commutation, reverse-recovery notation, inverter power flow,
commutation overlap, and vector-control equations require technical review
against explicit circuit, operating-mode, and modeling assumptions.

## Validation and release

Focused Topic Pack validation and the provider-free contract regression test
must pass. The approval record is bound to the reviewed README and source JSON
hashes. Run `validate-topic-pack-release --all` before commit or push; this
Topic's narrow deterministic contract does not certify the overall service
Authority Gate.
