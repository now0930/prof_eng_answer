# Nine remaining Fact Anchor holds: next-action triage

Date: 2026-11-04. Branch: `codex/essay-boundary-calibration-20261028`.

This is a **repair plan, not an approval or scoring promotion**. The nine IDs
remain blocked by `fact_anchor_unresolved_source_holds_20261101.json`. Do not
change the 437-block overlay or the 103-entry promotion ledger on the strength
of this triage. Existing Registry `verified` labels do not override the hold.

| Fact ID | Decision for next patch | Required proof before any promotion |
|---|---|---|
| `control_valve_vena_contracta_is_minimum_flow_area` | Repair ID/claim identity. The Topic Anchor currently discusses minimum pressure; minimum flow area and minimum pressure are related but not interchangeable. | Preserve stable-ID migration history; verify the revised canonical statement and its question-specific need. |
| `control_valve_guide_function_and_transverse_load_wear_relevance` | Keep as bounded context, not an automatic core requirement in every friction diagnosis. | Add question-scope selection regression; compare the previously reviewed 17.0 and 14.5 replays without altering score thresholds. |
| `dp_level_radar_gwr_measurement_principle_comparison` | Split DP/radar/GWR physical principles from product-specific density/accuracy claims. | Primary documentation per principle; ensure no three-way comparison is required by an unrelated DP-level question. |
| `emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff` | Retain as vendor example/noncore, not a general mandatory Fact. | A separate broadly applicable material-selection proposition, if needed, must have its own ID and independent evidence. |
| `force_balance_null_position_error_detection` | Narrow to the documented force-balance architecture. | Confirm whether null detection is a property of the specified instrument, not all force-balance devices. |
| `lower_temperature_reduces_water_vapor_pressure_at_fixed_composition` | Correct canonical wording to water (or separately source another specified liquid), compare at unchanged absolute pressure and composition, and avoid promising cavitation/flashing elimination. | IAPWS water saturation-pressure relation; question-specific prevention relevance. |
| `pneumatic_force_balance_transmitter_chain` | Scope the flapper-nozzle/relay chain to that transmitter architecture. | Primary architecture drawing and a test that generic force balance does not demand this chain. |
| `srs_lifecycle_handoff_process_independently_verified` | Separate SRS handoff from independent verification; do not infer independence from handoff alone. | An applicable lifecycle standard clause or official guidance with exact scope and role. |
| `temperature_sensor_thermal_resistance_model` | State quasi-steady heat balance; treat radiation as nonlinear unless a local linearization is declared. | Primary heat-transfer/temperature-measurement source and a transient-vs-steady boundary test. |

For the water claim, the [IAPWS water/steam FAQ](https://iapws.org/faqs/faq1)
tabulates increasing saturation pressure from 0.00317 MPa at 25 °C to
0.1014 MPa at 100 °C. This directly supports the *water* temperature trend,
not a universal valve-damage-prevention guarantee. The
[IAPWS industrial formulation](https://www.iapws.org/relguide/IF97-Rev.html)
identifies its saturation-curve scope. For the sensor claim, the
[NIST thermocouple study](https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote1603.pdf)
describes the reading as a steady-state convection/radiation balance; it does
not justify an unrestricted linear thermal-resistance network for radiation.

Next safe implementation unit: revise one canonical Topic source and its
reviewed Fact mapping at a time; record source/locator and reviewer method;
run managed Topic approval, generated freshness, focused regressions,
`validate-all`, and the full non-promote Release Gate. Keep each ID blocked
until all of those pass. No score threshold, fatal rule or deterministic
authority change is proposed.
