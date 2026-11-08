# Canonical Fact Anchor to original publisher comparisons — 2026-11-01

This batch individually retrieved 13 **canonical source** `fact_anchor.json` statements from the existing topic branch and compared them against specific official published references. **No blanket source endorsement.** KEEP_BOUNDED means only a stated bounded proposition remains eligible for further scoring admission; REVISE_REQUIRED means the current canonical sentence must be rewritten before relying on it as a universal fact.

No Topic Pack JSON or generated grading bank was altered. Formal approval/release tests were not run in this connector-only review.

### Individual source and technical decisions

#### 1. sw02_sensor_voting_tradeoff_is_architecture_specific

- **Canonical topic/anchor:** `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` / `sw02_voting_logic`
- **Original canonical statement:** Voting logic은 N개 입력 중 M개 이상이 Trip 조건일 때 동작하는 M-out-of-N 구조이며, 채널 독립성·공통원인·진단·불일치 처리와 함께 설계해야 한다.
- **Publisher's original document:** https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/safebk-rm003_-en-p.pdf
- **Locator:** Process Safebook 1 p.161, 20 Definitions, 2oo3 / Architecture
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** M-out-of-N trip voting (including 2oo3) is meaningful with chosen channel independence/failure architecture; no universal SIL, common-cause, or diagnostic credit inferred.

#### 2. linearized_control_loop_gain_is_cascade_product

- **Canonical topic/anchor:** `control_valve_authority_rangeability_gain_installed_performance` / `loop_gain_component_product`
- **Original canonical statement:** 루프의 정적 민감도는 controller, actuator·positioner, installed valve, process와 measurement gain의 결합으로 해석할 수 있다.
- **Publisher's original document:** https://www.mathworks.com/help/control/ref/inputoutputmodel.series.html
- **Locator:** Description: SISO series interconnection equals transfer-function product
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Local linearized SISO open-loop component gains multiply at a specified operating point; nonlinearity, feedback and saturation require separate treatment.

#### 3. fixed_speed_stable_centrifugal_pump_head_falls_with_flow

- **Canonical topic/anchor:** `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` / `control_valve_pump_curve_installed_characteristic_effect`
- **Original canonical statement:** Centrifugal pump가 공급하는 head는 일반적으로 flow 증가와 함께 감소하므로 pump curve가 운전점별 available pressure와 valve differential pressure에 영향을 준다.
- **Publisher's original document:** https://www.grundfos.com/solutions/learn/ecademy/all-courses/the-basic-pump-curve-course/what-is-a-pump-curve-
- **Locator:** What is a pump curve: QH relation
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Typical stable centrifugal-pump Q-H curve for constant-speed operation; not a theorem for every impeller, region, speed, series arrangement or control strategy.

#### 4. gas_equation_n_constant_depends_on_units_and_flow_form

- **Canonical topic/anchor:** `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `unit_constant_equation_dependency`
- **Original canonical statement:** N 상수는 flow basis, pressure·temperature unit, molecular-weight·density representation과 equation form에 따라 선택한다.
- **Publisher's original document:** https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_02.pdf
- **Locator:** Valve Sizing (Standardized Method), Table 3-2 Equation Constants / example N6, N7, N9
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Published N numerical conversion factors depend on chosen equation and measurement units/flow basis, not intrinsic fluid properties. PDF text checked; full PDF screenshot unavailable.

#### 5. position_error_convention_and_negative_feedback

- **Canonical topic/anchor:** `control_valve_positioner_ip_converter_booster_accessories_calibration` / `position_error_negative_feedback`
- **Original canonical statement:** Position error는 e=r-y이며 positioner output은 error magnitude를 줄이는 negative-feedback 방향이어야 한다.
- **Publisher's original document:** https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners
- **Locator:** What Is a Valve Positioner? Feedback of stem/shaft position
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** e=r-y is a chosen sign convention for reference minus measured travel; actuator action must be wired/calibrated so feedback reduces error, not assumed for all direct/reverse configurations.

#### 6. split_range_segments_calibrated_to_intended_travel

- **Canonical topic/anchor:** `control_valve_positioner_ip_converter_booster_accessories_calibration` / `split_range_local_mapping`
- **Original canonical statement:** Split-range 각 segment는 own local current range로 normalization하고 gap·overlap·action을 확인한다.
- **Publisher's original document:** https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200149x012.pdf
- **Locator:** Fisher 3610J/3620J Instruction Manual p.28 Table 8, verified page screenshot (zero-based 27)
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Each participating valve's own input subrange maps to rated travel; gap/overlap/direct/reverse settings are design-specific, not a fixed 4-12/12-20 standard.

#### 7. control_valve_required_capacity_maps_through_selected_characteristic_to_travel

- **Canonical topic/anchor:** `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `selected_characteristic_travel_mapping`
- **Original canonical statement:** Required coefficient를 selected trim의 inherent characteristic와 rated coefficient에 대응시켜 operating travel을 추정한다.
- **Publisher's original document:** https://www.emerson.com/is/content/emerson/ko/final-control/flow-controls/documents/d101881x012.pdf
- **Locator:** Emerson Control Valve Handbook 6e, ch.5 5.4.1–5.4.2; ch.1 Rated and Relative Cv definitions
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Required Cv can be matched to a manufacturer's Cv-vs-travel characteristic only under stated differential pressure and fluid sizing assumptions; installed pressure-drop variation may change operating travel. Indexed PDF text; screenshot failed for size.

#### 8. rack_pinion_actuator_rotary_output_application_and_sizing

- **Canonical topic/anchor:** `control_valve_types_globe_rotary_body_actuator_selection` / `rack_pinion_rotary_torque_conversion`
- **Original canonical statement:** Rack-and-pinion actuator는 piston의 직선 운동을 회전 torque로 변환하여 ball, butterfly와 plug 등 rotary valve에 주로 결합하며 공기압, 회전각과 torque 곡선을 확인해야 한다.
- **Publisher's original document:** https://www.emerson.com/en/final-control/catalog/products-and-software/actuators/pneumatic-actuators/rack-pinion-actuators
- **Locator:** What is a Rack & Pinion actuator? / Common Applications
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Piston rack converts pneumatic linear force into quarter-turn torque for suitable rotary valves; actual pressure, torque margin, travel stops, failure state and loading depend on model.

#### 9. lopa_scenario_outputs_trace_into_srs_function_and_integrity_requirements

- **Canonical topic/anchor:** `hazop_lopa_ipl_risk_reduction_sil_target_allocation` / `hazop_lopa_srs_handoff`
- **Original canonical statement:** LOPA 결과는 원인·감지변수·trip 조건·safe state·목표 SIL·응답시간·proof test·bypass·reset·운전모드를 포함하는 SRS 입력으로 인계되어야 한다.
- **Publisher's original document:** https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/safebk-rm003_-en-p.pdf
- **Locator:** Process Safebook 1 pp.85–86, sec.10 SRS, page 86 visually verified
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** SRS contains per-SIF safe state, SIL, response, trip points, test intervals, modes, bypasses and resets, etc.; LOPA/PHA must supply appropriate risk allocation, but not every SRS field is itself an output of LOPA.

#### 10. real_time_correctness_is_subject_to_application_timing_constraints_not_zero_latency

- **Canonical topic/anchor:** `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing` / `realtime_fit_for_purpose`
- **Original canonical statement:** 실시간 처리는 지연이 0이라는 뜻이 아니라 업무·제어 목적에 맞는 유한한 Deadline, 지연 예산과 결정성 수준을 만족하는 것이다.
- **Publisher's original document:** https://swehb.nasa.gov/spaces/SWEHBVD/pages/140640605/SRS%2B-%2BSoftware%2BRequirements%2BSpecification
- **Locator:** Performance and Timing Requirements / deadlines
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Real-time correctness is evaluated against a declared finite timing/deadline requirement, not physical zero latency; hard versus soft real-time guarantees still differ.

#### 11. opc_ua_information_integration_is_not_automatic_hard_realtime_fieldbus_replacement

- **Canonical topic/anchor:** `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` / `sw07_opcua_role_boundary`
- **Original canonical statement:** OPC UA는 controller·SCADA·MES·gateway·cloud 사이의 정보통합에 강점이 있지만 모든 현장 I/O bus를 자동 대체하거나 정량적 실시간성을 보장하는 것은 아니다.
- **Publisher's original document:** https://opcconnect.opcfoundation.org/2026/06/field-level-communications-corner-june-2026/
- **Locator:** OPC UA FX C2C released; C2D/remote I/O/motion extensions under preparation and prototyping
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** OPC UA information exchange alone does not guarantee application hard real-time properties, although OPC UA FX over TSN may support field-level deterministic services when profiled and verified. Avoid blanket 'OPC UA cannot be real-time'.

#### 12. impulse_line_slope_and_transmitter_position_are_phase_dependent

- **Canonical topic/anchor:** `instrumentation_installation_wiring_impulse_tubing_inspection_codes` / `iiwic_impulse_slope_service_specific`
- **Original canonical statement:** Impulse line의 slope와 transmitter elevation은 gas, liquid, steam 등 service와 condensate/gas pocket 거동에 따라 달라지므로 모든 service에 동일 방향의 slope를 적용해서는 안 된다.
- **Publisher's original document:** https://web-material3.yokogawa.com/IM01C25B01-01EN_018.pdf
- **Locator:** Yokogawa IM01C25B01-01E 18e, section 5.1.2(2),(3), pp 5-3. Screenshot failed due to source size; manufacturer published text checked.
- **Technical verdict:** KEEP_BOUNDED
- **Validated proposition and limitation:** Gas, liquid and steam require differing elevation/routing to avoid gas or condensate pockets; particular installation design/project standards govern details, including slopes.

#### 13. production_wip_throughput_flow_time_boundary

- **Canonical topic/anchor:** `instrumentation_production_management_planning_quality_cost_resources` / `production_throughput_cycle_lead_wip_kpi`
- **Original canonical statement:** Throughput, Cycle Time, Lead Time과 WIP는 서로 다른 흐름 KPI이므로 동일한 것으로 취급하지 않고, 공정경계와 측정시점을 정의하여 병목·대기·재공의 원인을 분석해야 한다.
- **Publisher's original document:** https://learn.ascm.org/sfc/servlet.shepherd/document/download/069R3000006PlDHIA0?operationContext=S1
- **Locator:** ASCM manufacturing glossary: Little's Law and WIP/throughput/lead time definitions
- **Technical verdict:** KEEP_BOUNDED
- **Correction 2026-11-01:** The canonical sentence already requires boundary definitions; changing the term 'cycle time' across domains is an applicability caveat, not sufficient grounds to reject the original bounded claim. The prior REVISE_REQUIRED classification is superseded by KEEP_BOUNDED.
- **Validated proposition and limitation:** Differentiate WIP (quantity), throughput (units/time), and lead time (time), but 'cycle time' varies across authors: unit operation time, inter-departure time, or total flow/cycle time. Explicit definition/measurement boundary required before general scoring.


All individual verdicts require separate scoring admission and guard checks under docs/fact_anchor_eligibility_policy.md. Current source statements are not silently rewritten. Source page checks distinguish HTML, searchable PDF text, and actually verified PDF screenshots. No claim of full PDF image verification where screenshot failed.