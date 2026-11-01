# Independent canonical-to-primary checks — 24 anchors (2026-11-01)

This batch directly retrieved and read each canonical `rubrics/topic_packs/<topic_id>/fact_anchor.json` statement. The named propositions were compared to publisher HTML text, engineering equations and specific technical sections. These `KEEP_BOUNDED` judgments are scoped to the original claims with explicit assumptions; they are not blanket product guarantees, legal standards, or a passing score release test.

Publisher sources: NI, Rheonics, Advantech, Omron, Rockwell Automation, MathWorks, Pepperl+Fuchs and exida. All links below are to the primary publisher's *HTML*, and not a claim of page-image PDF review.

## 1. acl_current_loop_principle

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_current_loop_principle`
- **Actual source statement:** 4–20 mA 루프는 직렬 경로의 동일 전류를 측정변수에 대응시켜 원거리로 전송하는 아날로그 신호 방식이다.
- **Source original:** https://www.ni.com/en/shop/data-acquisition/fundamentals--system-design--and-setup-for-the-4-to-20-ma-curren.html
- **Source section/locator:** Current Loop Components, Fig.2
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Series loop uses common 4-20mA current as analogue measurement signal; ensure supply and scaling.

## 2. acl_live_zero_fault_discrimination

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_live_zero_fault_discrimination`
- **Actual source statement:** 4 mA live zero는 정상 0% 공정값과 0 mA 근방의 단선·전원 상실을 구분하고 2선식 기기의 동작 전력을 제공한다.
- **Source original:** https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P8ZUSA0
- **Source section/locator:** Advantages of 4-20mA, two numbered explanations
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Live zero 4mA represents 0% and is distinct from near-zero loop fault; 0mA cannot distinguish all possible failure causes.

## 3. acl_two_wire_loop_powered

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_two_wire_loop_powered`
- **Actual source statement:** 2선식 transmitter는 전원과 신호가 한 쌍을 공유하며 외부 loop supply에서 공급된 전류로 기기를 구동하고 측정값을 전송한다.
- **Source original:** https://www.ni.com/en/shop/data-acquisition/fundamentals--system-design--and-setup-for-the-4-to-20-ma-curren.html
- **Source section/locator:** Current Loop Components and loop-power explanation
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Typical two-wire device draws operating power from shared signal loop; external supply and burden remain necessary.

## 4. acl_active_source_output

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_active_source_output`
- **Actual source statement:** Active 또는 sourcing 출력은 transmitter가 신호 루프에 전원과 전류를 공급하는 형식으로, passive input 또는 적합한 부하와 결선한다.
- **Source original:** https://support.rheonics.com/en/support/solutions/articles/81000297457
- **Source section/locator:** Active analog output and sinking PLC input section
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** A self-powered 4-wire active current output drives passive loop load; do not equate every active signal with 2-wire loop-power.

## 5. acl_passive_sink_output

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_passive_sink_output`
- **Actual source statement:** Passive 또는 sinking 출력은 신호 루프의 외부 전원을 받아 전류를 조절하는 형식으로, powered input 또는 별도 loop supply와 결선한다.
- **Source original:** https://www.advantech.com/ko-kr/support/details/faq?id=1-HIIV-473
- **Source section/locator:** FAQ ANALOG: current AO sinking needs supply in series
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Sinking current output modulates current drawn from separate loop power; interface polarity/wiring is model-specific.

## 6. acl_compliance_voltage_load_budget

- **Canonical topic/anchor:** `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_compliance_voltage_load_budget`
- **Actual source statement:** 루프는 공급전압이 transmitter의 최소 동작전압과 cable·barrier·indicator·input resistance의 최대 전압강하를 감당하는 compliance/load budget을 만족해야 한다.
- **Source original:** https://www.ni.com/en/shop/data-acquisition/fundamentals--system-design--and-setup-for-the-4-to-20-ma-curren.html
- **Source section/locator:** Power requirements: minimum transmitter voltage, shunt and two-wire resistance
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Use maximum loop current for voltage burden; sensor minimum voltage plus cable/shunt/barrier/input drops must fit supply.

## 7. encoder_feedback_selection_by_required_motion_information

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `selection_direction_position_resolution`
- **Actual source statement:** 속도만 필요한지, 회전방향·relative position·absolute position까지 필요한지에 따라 one-channel pulse, quadrature incremental 또는 absolute encoder를 구분한다. 필요한 angular resolution과 control bandwidth도 함께 선정한다.
- **Source original:** https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- **Source section/locator:** Output Phase, Resolution, Absolute Code, CW definitions
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Direction/relative increments need appropriate multi-phase output; absolute address requires absolute encoding. Required bandwidth is application-defined.

## 8. encoder_pulse_interface_noise_and_receiver_compatibility

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `electrical_interface_noise_error`
- **Actual source statement:** Pulse speed signal은 output type, supply level, cable length, shielding, grounding, common-mode noise와 receiver threshold의 영향을 받는다. Differential line driver나 proper termination이 필요한 경우 controller interface까지 포함해 검토한다.
- **Source original:** https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- **Source section/locator:** Output Circuit: open collector, voltage output, RS-422 line driver and receiver
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Signal interface/receiver must match outputs and electrical thresholds. RS-422 differential helps noise rejection; grounding specifics are application-dependent.

## 9. encoder_resolution_terms_require_definition_and_decode_mode

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `encoder_resolution_ppr_cpr_definition`
- **Actual source statement:** Encoder resolution은 PPR, CPR 또는 bit 수로 표현될 수 있지만 제조사와 controller가 PPR/CPR를 정의하는 방식이 다를 수 있다. 따라서 catalog의 cycle/pulse 정의와 controller의 edge-decoding mode를 확인해 N_eff를 확정해야 한다.
- **Source original:** https://www.rockwellautomation.com/en-gb/docs/studio-5000-logix-designer/38-03/contents-ditamap/module-information/encoder-mode---1794-vhsc.html
- **Source section/locator:** Encoder X1, X2, X4 pulse-multiplication mode descriptions
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Effective counts/revolution must match manufacturer pulse resolution and receiver edge decode; PPR/CPR naming is not uniformly applied.

## 10. encoder_speed_and_decode_rate_must_fit_frequency_limits

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `encoder_frequency_limit_selection`
- **Actual source statement:** Encoder와 receiving counter/PLC에는 최대 output/input frequency가 있으므로 최고 회전속도와 N_eff의 곱이 허용 주파수를 넘지 않도록 선정한다. 해상도를 높이면 동일 속도에서 pulse frequency도 증가한다.
- **Source original:** https://www.ia.omron.com/products/family/487/specification.html
- **Source section/locator:** E6B2-C resolution and maximum response frequency specification
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Pulse frequency grows with rpm and pulses/rev; separately respect sensor output maximum frequency and receiver count/edge limits.

## 11. quadrature_phase_order_encodes_direction

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `quadrature_direction_principle`
- **Actual source statement:** Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다. x1/x2/x4 decoding에 따라 유효 count/rev가 달라질 수 있다.
- **Source original:** https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- **Source section/locator:** Output Phase Difference approximately 90°; CW A normally leads B
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Relative order of A/B edges determines direction under stated view and invert conventions; x1/x2/x4 varies counts.

## 12. shaft_rpm_to_angular_velocity_and_encoder_counts_require_defined_scaling

- **Canonical topic/anchor:** `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `speed_angular_frequency_relation`
- **Actual source statement:** 회전속도는 회전수, 각속도 또는 pulse frequency로 표현할 수 있다. 회전속도 n[rpm]과 각속도 ω[rad/s]의 관계는 ω = 2πn/60이며, pulse 방식에서는 1회전당 유효 count 수를 확인해야 한다.
- **Source original:** https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- **Source section/locator:** Resolution: pulses per shaft revolution; mathematical derivation of units
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** ω[rad/s]=2πn[rpm]/60. Encoder frequency conversion also requires effective count/revolution and receiver mode.

## 13. state_feedback_pole_placement_is_not_tracking_specification

- **Canonical topic/anchor:** `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_design_objective`
- **Actual source statement:** 상태피드백 극점배치는 적절한 가제어성·안정화 가능성 조건에서 폐루프 pole을 정하는 절차이지, 그 자체로 기준입력의 크기 보정이나 정상상태 추종오차 제거를 보장하지 않는다. 추종·외란응답·입력제약은 설계 요구로 별도 정의하고, 필요에 따라 reference prefilter, 적분상태 확장 및 구현 제약을 검토한다.
- **Source original:** https://www.mathworks.com/help/control/getstart/pole-placement.html
- **Source section/locator:** State Feedback Gain Selection: closed loop A-BK and poles
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Pole placement sets feedback dynamics of linear model, not reference scaling, disturbance elimination or hard bounds.

## 14. state_reference_prefilter_does_not_cancel_independent_disturbance

- **Canonical topic/anchor:** `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_disturbance_reference_performance`
- **Actual source statement:** 기준입력 추종과 외란 제거는 신호의 입력 위치와 모델에 따라 구분해야 하며, 프리필터만으로 plant 입력 또는 출력 외란을 제거할 수 없다.
- **Source original:** https://www.mathworks.com/help/control/ug/single-loop-feedbackprefilter-compensator-design.html
- **Source section/locator:** Design Overview: PID rejects output disturbance; reference filter tunes tracking
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** An input reference prefilter by itself cannot cancel unknown independent input/output disturbance. Measured disturbance feedforward is a different architecture.

## 15. integrator_augmentation_requires_augmented_stabilizability

- **Canonical topic/anchor:** `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_augmented_controllability_stabilizability`
- **Actual source statement:** 원래 시스템이 가제어하더라도 적분 확대시스템이 자동으로 가제어하지는 않으며, 임의 극점 배치에는 확대시스템의 가제어성, 안정화에는 최소한 안정화 가능성이 필요하다.
- **Source original:** https://www.mathworks.com/help/control/ref/ss.lqi.html
- **Source section/locator:** LQI Limits and augmented integrator state; direct counterexample A=0,B=1,C=0,D=0
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Controllable (A,B) need not yield controllable augmented tracking integrator; need augmented control/stabilization feasibility for requested design.

## 16. integral_state_tracking_saturation_requires_antiwindup_validation

- **Canonical topic/anchor:** `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_saturation_anti_windup`
- **Actual source statement:** 액추에이터 포화 중 적분오차가 계속 누적되면 windup이 발생하므로 conditional integration, clamping 또는 back-calculation 등의 anti-windup을 적용하고 포화 응답을 별도로 검증한다.
- **Source original:** https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html
- **Source section/locator:** Anti-windup examples: back-calculation and clamping
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Actuator saturation can make feedback integrator wind up; apply and validate antiwindup tailored to actuator and loop.

## 17. state_space_pole_speed_requires_implementation_tradeoff_checks

- **Canonical topic/anchor:** `state_space_controllability_observability_pole_placement` / `implementation_tradeoffs_validation`
- **Actual source statement:** 빠른 controller·observer pole은 응답속도를 높일 수 있지만 control effort, 포화, 잡음, peaking, sampling 및 모델 오차 민감도를 키울 수 있으므로 단계적 검증이 필요하다.
- **Source original:** https://www.mathworks.com/help/control/getstart/pole-placement.html
- **Source section/locator:** Caution: weakly controllable/observable poles, high gain and perturbations
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Aggressively moved poles may increase gain and model sensitivity. Validate effort, sampling, saturation and observer noise separately.

## 18. ultrasonic_air_temperature_changes_uncompensated_range

- **Canonical topic/anchor:** `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` / `ultrasonic_air_temperature_compensation`
- **Actual source statement:** 공기 중 음속의 온도 의존성을 보상하지 않으면 비행시간을 거리로 환산할 때 측정오차가 발생한다.
- **Source original:** https://blog.pepperl-fuchs.com/en/2018/ultrasonic-sensor-faq-external-influences-on-sensor-operation/
- **Source section/locator:** Question 3: air temperature changes sound speed around 0.17%/degree
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Uncompensated acoustic time-of-flight yields apparent range errors; correction needs actual medium conditions.

## 19. ultrasonic_nearby_sensor_crosstalk_risk

- **Canonical topic/anchor:** `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` / `ultrasonic_sensor_crosstalk`
- **Actual source statement:** 인접 초음파 센서가 동시에 송신하면 다른 센서의 펄스를 자신의 에코로 인식하는 크로스토크가 발생할 수 있다.
- **Source original:** https://blog.pepperl-fuchs.com/en/2019/ultrasonic-sensor-faq-synchronization-and-common-mode/
- **Source section/locator:** FAQ Question 5: sequential multiplex to avoid cross talk
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Nearby unsynchronized sonars can cross-talk; staggered trigger timing reduces it but can increase response time.

## 20. sil_required_rrf_relation

- **Canonical topic/anchor:** `sil_target_determination_risk_reduction_and_lifecycle` / `required_rrf_relation`
- **Actual source statement:** 잔여 사건빈도 F_residual이 허용 사건빈도 F_tolerable보다 크면 SIF가 제공해야 할 최소 위험감소율은 RRF_required = F_residual / F_tolerable이다.
- **Source original:** https://www.exida.com/Blog/how-does-mission-time-proof-test-interval-and-proof-test-coverage-impact-pfdavg
- **Source section/locator:** RRF=1/PFDavg plus required ratio from event-frequency balance
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** For defined low-demand SIF and properly allocated scenario, required additional risk reduction is Fresidual/Ftolerable when >1; both frequencies same units.

## 21. sil_target_pfd_relation

- **Canonical topic/anchor:** `sil_target_determination_risk_reduction_and_lifecycle` / `target_pfd_relation`
- **Actual source statement:** 저요구 모드에서 목표 평균 요구고장확률은 PFDavg_target <= 1 / RRF_required = F_tolerable / F_residual로 정한다. 빈도끼리의 비이므로 무차원이며 허용빈도와 기초빈도를 곱하지 않는다.
- **Source original:** https://www.exida.com/Blog/how-does-mission-time-proof-test-interval-and-proof-test-coverage-impact-pfdavg
- **Source section/locator:** Low-demand RRF/PFDavg inverse relationship
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** PFDavg target <= Ftolerable/Fresidual (when residual risk exceeds acceptable); excludes high-demand PFH substitution and unsupported IPL assumptions.

## 22. root_locus_target_outside_uncompensated_locus_requires_controller_dynamics_change

- **Canonical topic/anchor:** `root_locus_stability_gain_design` / `compensator_design_application`
- **Actual source statement:** 목표점이 기존 근궤적 위에 없으면 lead, lag, lead-lag 또는 PID로 근궤적을 변경하고 현장 제약을 검증한다.
- **Source original:** https://www.mathworks.com/help/control/ug/root-locus-design.html
- **Source section/locator:** Increase Gain and Add Poles/Zeros compensator design example
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Varying scalar gain alone moves poles along the unchanged locus; off-locus poles require different open-loop dynamics or other control architecture.

## 23. mcdc_unique_cause_pair_holds_other_conditions_fixed

- **Canonical topic/anchor:** `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_unique_cause`
- **Actual source statement:** Unique-cause MC/DC는 대상 조건만 변경하고 다른 모든 조건을 고정한 두 Test Case로 독립 영향을 입증하는 방식이다.
- **Source original:** https://www.mathworks.com/help/polyspace_test/ref/modifiedconditiondecisioncoveragemcdc.html
- **Source section/locator:** Description: change only condition under test while other conditions unchanged
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** Unique-cause MC/DC demonstrates decision flip caused by one condition, holding others fixed; masking variants have different assumptions.

## 24. mcdc_full_coverage_is_not_complete_requirements_or_sil_evidence

- **Canonical topic/anchor:** `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_one_hundred_percent_limit`
- **Actual source statement:** 100% MC/DC는 구현된 복합 Decision의 구조가 규정된 수준으로 실행되었음을 보일 뿐 요구사항의 완전성, 알고리즘 타당성, Timing 안전성과 전체 SIL 달성을 단독으로 보장하지 않는다.
- **Source original:** https://www.mathworks.com/help/matlab-test/ug/types-of-code-coverage-for-matlab-source-code.html
- **Source section/locator:** Modified Condition/Decision Coverage structural metric
- **Verdict:** KEEP_BOUNDED
- **Engineering validity conditions:** 100% MC/DC proves structural independent effects only, not requirements completeness, algorithm correctness, overall functional safety or SIL.


No canonical JSON or generated grading bank has been edited or reapproved. No full release validation or runtime scoring regression was run. A conditional keep in the audit does not override the separate exclusion and revision-hold overlays or the need for eligibility admission.