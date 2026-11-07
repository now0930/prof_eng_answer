# 4–20 mA analog loop: 3 remaining exact-ID primary-source checks (2026-11-01)

Reviewer GPT-6, existing branch `codex/essay-boundary-calibration-20261028`. Compared exact original Topic Pack `rubrics/topic_packs/analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting/fact_anchor.json`, no modification to canonical registry. Sources inspected as manufacturer original HTML, not PDF-derived claims.

Primary sources:
- NI, *4-20 mA Current Loop Fundamentals, System Design, and Setup*, 2025-02-03, §§Current Loop Components / Designing a Current Loop System: https://www.ni.com/en/shop/data-acquisition/fundamentals--system-design--and-setup-for-the-4-to-20-ma-curren.html
- Analog Devices, *PIXI MAX11300 4-20mA Current Control Loop Transmitter*, §§Load Resistor / Power Supply: https://www.analog.com/en/resources/technical-articles/pixi-max11300-420ma-current-control-loop-transmitter.html
- NI, *Sinking and Sourcing with C Series Digital I/O Hardware*, notes analog-module current source/sink and NI-9266 current output: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019LBbSAM (indexed publisher text; no claim of entire original page reviewed beyond excerpt)
- Analog Devices, *CN0289 Flexible Loop-Powered Pressure Sensor Transmitter* schematic/testing: https://wiki.analog.com/resources/eval/user-guides/circuits-from-the-lab/cn0289

| Exact fact ID | Decision | Original statement vs evidence and limits |
|---|---|---|
| `four_to_twenty_milliamp_repair_requires_end_to_end_reverification` | `REVISE_REQUIRED` | Functional signal re-check after repair is sound, but exact 4/12/20 mA, 0/50/100%, complete end-to-end alarm and **trip direction** tests in *every repaired analog loop* are not universal. Many loops are not associated with a trip, and test points depend on equipment commissioning/safety procedures. Replace with a scope-specific post-repair input→engineering scaling→applicable alarm/safety actions verification with applicable test points and records. |
| `acl_resistor_voltage_measurement` | `KEEP_BOUNDED` | Ohm's law `I=V/R` across known shunt; NI and ADI first-party examples of resistive current-to-voltage conversion (e.g. 250Ω 4–20mA gives 1–5V). Only for the actual shunt and correct circuit, with electrical safety and common-mode limits. |
| `four_twenty_ma_source_sink_match_and_polarity` | `KEEP_BOUNDED` | Current-loop sourcing/sinking, active/passive power architecture and polarity must match the receiver and transmitter. A second incompatible powered output *can* overdrive a device, but damage is not inevitable; depends on current limits, isolation/protection, card construction. |

3 previously PENDING exact IDs → 2 keep, 1 revision hold; expected: 299 PENDING, 617 KEEP_BOUNDED, 52 REVISE_REQUIRED, 32 insufficient, 7 standards scope, 7 vendor scope, 275 screening excluded, 1 legacy scope. Unresolved scoring holds 345 (=299+32+7+7), revision holds 52; original 276 screening exclusions unchanged. No release/pass or managed Topic Pack / Registry regeneration represented. PR #17 remains draft and unmerged.
