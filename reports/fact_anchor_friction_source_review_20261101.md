# Control valve friction source review (2026-11-01)

Source: Emerson, Control Valve Handbook 6th ed., Chapter 1 friction definitions and Chapter 2 sections 2.1.1 / 2.1.3.5.
https://www.emerson.kr/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf

All five are KEEP_BOUNDED, not blanket certifications:
- balanced_trim_breakaway_running_friction_are_distinct: static breakaway friction versus dynamic running friction; no universal numerical force relation.
- control_valve_packing_friction_is_a_scoped_deadband_contributor: packing friction is one possible deadband source, not necessarily sole cause.
- control_valve_stiction_static_friction_can_cause_stick_jump_motion: stick-slip may occur, not in every actuator/loop.
- rotary_valve_actuator_connection_backlash_is_lost_motion_and_design_specific: linkage play can cause lost motion; magnitude and significance depend on construction.
- static_friction_is_force_threshold_to_start_stationary_fce_motion: motion initiation requires overcoming opposing static friction, depending on loading and configuration.

Scope: official PDF indexed text checked; image screenshot was attempted and failed due to 17 MB download limit. Full Topic Pack wording was not independently read. Do not generalize the above judgments beyond named propositions.