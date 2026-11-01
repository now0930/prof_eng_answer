# Source review: valve sizing and ADC principles — 2026-11-01

Six entries are marked KEEP_BOUNDED in the independent verification audit. These conclusions are strictly limited to the propositions stated in the fact IDs; they do not certify all Topic Pack prose.

| Fact ID | Official source | Technical boundary |
|---|---|---|
| liquid_valve_phase_change_pressures_are_absolute | Emerson Control Valve Handbook 6th ed., ch. 5, section 5.6 terminology; https://www.emerson.kr/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf | P1, P2, Pv, Pc are defined as absolute pressure in phase-change calculations; differential pressure remains a difference. |
| liquid_valve_vapor_pressure_is_temperature_specific | Emerson Control Valve Handbook 6th ed., ch. 5, section 5.6; same URL | Pv defined for liquid at inlet/flowing temperature; not a universal constant independent of composition and temperature. |
| gas_sizing_uses_absolute_pressure_and_temperature | Emerson Control Valve Handbook 6th ed., ch. 5, sections 5.6 and 5.10; same URL | P1 and P2 absolute static pressures; T1 absolute upstream temperature. Specific equation still requires appropriate compressibility and choked-flow checks. |
| gas_standard_volume_basis_has_explicit_reference_conditions | Emerson Control Valve Handbook 6th ed., ch. 5, section 5.6 note; same URL | Handbook defines its standard basis as 15.5 °C (60 °F) and 14.7 psia (101.3 kPa). Other standards can use other reference bases; no globally unique standard volume basis may be inferred. |
| control_valve_required_cv_inverse_sqrt_pressure_drop | Emerson, Valve Sizing Calculations (Traditional Method), https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_11.pdf | Cv=Q sqrt(G/ΔP) for fixed flow, density and ordinary nonchoked liquid sizing; fails as a universal claim under viscosity correction, fittings effects, cavitation or flashing. |
| eem_adc_resolution_accuracy_distinction | NI, Resolution vs Accuracy of ADC, https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q0000019k2PCAQ&l=en-US | Resolution is smallest distinguishable digital count change; accuracy concerns agreement with actual input; more bits do not guarantee higher accuracy. |

Method note: Accessible official web text was compared. Attempts to screenshot the large Emerson PDF failed due to the source size, so screenshot/image confirmation was **not** completed; avoid describing this batch as a page-image inspection. The exact complete Topic Pack original text and every existing citation were not individually inspected. Verdicts remain bounded to the named propositions and must not justify broad automatic scoring rules.
