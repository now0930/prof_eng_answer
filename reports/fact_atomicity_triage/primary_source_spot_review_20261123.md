# P1/P2 priority primary-source cross-check — 2026-11-23

**Scope:** non-scoring engineering fact review, selected from the 457-item multi-sentence queue. **Not a 457-item technical approval.**
**Canonical reference:** main `30b13262ad3899919edae7cb72be3ddeca677f18`.
**Status:** REVIEW_EVIDENCE_ONLY / NOT_APPROVED / score_effect=none / score_admission=DISABLED.

## External independent source locators consulted

1. OSHA, [29 CFR §1910.119(l)(1)-(5)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119), official HTML, Management of Change. §(l)(1) specifies covered process changes and replacement-in-kind exception; §(l)(2) identifies prechange review topics; §§(l)(3)-(5) address training and updating the relevant information/procedures.
2. UK HSE, [Control systems — safety-related systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), HTML, sections *Actuators and signal conversion*, *Utilities*, *Proof testing*, *System integrity*. Safety-function dependencies and the limitations of partial-stroke exercising are discussed.
3. IEC webstore, [IEC 61511-1:2016+A1:2017](https://webstore.iec.ch/en/publication/61289), standard scope summary only; not a substitute for full edition-specific clause access.
4. OMRON, [3G3MV PLC Board User's Manual I01E-EN-01](https://files.omron.eu/downloads/latest/manual/en/i01e_3g3mv_plc_board_users_manual_en.pdf), Appendix B, printed pp. 80-81. The documented example explicitly distinguishes pulse frequency input limit from quadrature x4 count resolution; extraction readable, PDF screenshot unavailable in this review.
5. NIST, [SP 250-35: Calibration of Thermocouples and Thermocouple Materials](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication250-35.pdf), §2.6.3 *Law of Intermediate Temperatures*. Extracted text supports EMF additivity; PDF screenshot unavailable in this review.
6. Emerson/Rosemount, [DP Level — Technical Note 00840-1400-4801 Rev BB](https://www.emerson.kr/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-3051s-ers-77758.pdf), §§2.2–2.4. Describes wet/dry leg error mechanisms and why balanced capillaries do not eliminate all temperature error; PDF screenshot unavailable in this review.
7. MIT OCW/Open Learning, [System Functions and Laplace Transform](https://openlearninglibrary.mit.edu/courses/course-v1%3AOCW%2B18.031%2B2019_Spring/courseware/week6/lec10/), Black feedback relation; webpage extraction preview, direct page reopening unavailable here.

## Named Anchor technical review

| Source Topic suffix / Anchor ID | Distinct facts / scope judgment | Evidence match | Decision for current cycle |
| --- | --- | --- | --- |
| `configuration_change_... / sw06_moc_trigger_and_scope` | Scope must be limited to OSHA-covered processes; replacement-in-kind excluded. Normative MOC requirements and OT NIST guidance are two independent claims. | OSHA §(l)(1)-(5) supports the covered-process MOC portion; NIST part not independently checked in this cycle. | **PARTIAL_PRIMARY_SOURCE_SUPPORT / HOLD**. Retain unchanged, separate OSHA vs NIST units on any later proposal. |
| `configuration_change_... / sw06_impact_analysis_multidisciplinary` | OSHA enumerated review requirements vs suggested multidisciplinary/OT examples must not be conflated as uniform mandatory checklist. | OSHA §(l)(2) supports only the process-specific subset. | **PARTIAL_PRIMARY_SOURCE_SUPPORT / HOLD**. |
| `configuration_change_... / sw06_change_implementation_plan` | Generic plan contents vs OSHA §(l) obligations vs NIST OT recommendations are independent bounded propositions. | OSHA §(l)(2)-(5) supports its limited norm; other components not checked. | **PARTIAL_PRIMARY_SOURCE_SUPPORT / HOLD**. |
| `final_control_element_... / final_element_role_in_sif` | Final element and necessary pilot valve/actuator/utility participation depends on actual safety function boundary. | HSE *Actuators* and *Utilities* support the general boundary. | **PRELIMINARY_SUPPORT_WITH_SCOPE**, no canonical approval. |
| `final_control_element_... / utility_supply_and_shared_dependencies` | Shared utilities and independence may influence safety integrity; avoid treating all utilities as universally included. | HSE *System integrity* and *Utilities*. | **PRELIMINARY_SUPPORT_WITH_SCOPE**, no canonical approval. |
| `final_control_element_... / safe_state_process_hazard_basis` | Process safe state is hazard/SRS dependent; cannot decree fail-open/fail-closed universally. | HSE safety-function/hazard discussion; IEC 61511 publisher scope supports achieving/maintaining safe state, not every SRS-specific detail. | **PARTIAL_PRIMARY_SOURCE_SUPPORT / HOLD**. |
| `final_control_element_... / pst_not_full_proof_test` | HSE distinguishes in-service partial stroke exercising from full proof testing, which must address previously unrevealed failure modes. | HSE *Actuators* and *Proof testing*. | **PRELIMINARY_SUPPORT_WITH_SCOPE**, no canonical approval. |
| `final_control_element_... / full_stroke_proof_test_scope` | Scope, conditions at demand and end-to-end coverage must be tailored to safety function and safe procedure. | HSE *Proof testing*, includes end-to-end and expected-trip conditions. | **PRELIMINARY_SUPPORT_WITH_SCOPE**, no canonical approval. |
| `speed_rotation_... / encoder_frequency_limit_selection` | Old canonical statement can conflate per-channel PPR input pulse frequency and x1/x2/x4 decoded internal count rate if it uses N_eff for an input-frequency limit. | OMRON Appendix B pp. 80–81 explicitly distinguishes real pulse limit vs quadrature counts. | **REVISE_CANDIDATE / HOLD**. PR #38 had a separate precision-correction candidate, but that branch was closed; do not copy/approve automatically. |
| `speed_rotation_... / pulse_frequency_speed_equation` | Formula n=60f/N_eff is correct only when f counts the same effective events as N_eff. A channel physical pulse frequency uses corresponding PPR instead. | Engineering consistency plus OMRON counter examples; PDF visual verification pending. | **CONDITION_REVIEW_REQUIRED / HOLD**. |
| `thermocouple_... / thermocouple_law_of_intermediate_temperatures` | Thermoelectric EMF additivity under calibrated homogeneous material/reference conditions. | NIST SP250-35 §2.6.3 extracted text. | **TEXTUAL_SOURCE_SUPPORT, VISUAL_REVIEW_PENDING / HOLD**. |
| `thermocouple_... / thermocouple_law_of_intermediate_metals` | Inserted third-metal junctions must be isothermal to avoid additional net emf in the idealized law. | ASTM [Reference Junctions](https://store.astm.org/stp46143s.html) official metadata/summary; full underlying clause not checked. | **LIMITED_PRIMARY_SOURCE_SUPPORT / HOLD**. |
| `differential_pressure_level_... / dp_level_dry_leg_condensation_error` | Dry-leg condensation changes LP reference head and may bias DP/level. | Emerson Rosemount note §2.2 extracted text. | **TEXTUAL_SOURCE_SUPPORT, VISUAL_REVIEW_PENDING / HOLD**. |
| `differential_pressure_level_... / dp_level_capillary_length_symmetry` | Symmetric capillaries cannot eliminate all temperature-induced head error. | Emerson note §2.4 extracted text. | **TEXTUAL_SOURCE_SUPPORT, VISUAL_REVIEW_PENDING / HOLD**. |
| `bode_frequency_... / open_loop_closed_loop_roles` | Negative feedback yields G/(1+GH) from reference to output; only H=1 permits L/(1+L). Gain/phase margin from loop and bandwidth from applicable closed-loop response. | MIT control/Black formula source plus direct symbolic derivation; page access partial. | **PRELIMINARY_SUPPORT_WITH_SCOPE**, no canonical approval. |

## Review policy

This report records **15 named, individually interpreted technical observations**, spanning 6 high-risk Topic families, without asserting that the whole Anchor statement was source-verified for each row. The same Anchor can need further clause/published edition/scope inspection even where a subclaim is supported. No reviewer authorization, Fact Registry change, Claim admission, or score change is implied.

The remaining **442** items have per-ID triage snapshots in `batch_01.json`–`batch_07.json` but **have not received independent source-level technical checks in this cycle**. The 457-item independent verification requirement is therefore **NOT_COMPLETE**, despite 100% traceable inventory and structural triage.

PDF screenshot attempts returned cache-miss errors; this limitation is recorded rather than converting search-text evidence into a full visually checked technical approval.
