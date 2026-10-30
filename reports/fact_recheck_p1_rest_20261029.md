# P1 Facts 재검증 결과 — CSV 41–138

판정은 등록 Fact와 Anchor를 보고, 계산 항목은 식을 직접 재유도한 범위다. 공개 출처 본문을 아직 직접 열지 않은 항목은 근거가 등록돼 있어도 HOLD로 남긴다. 이 기록은 승인 상태/등록부를 변경하지 않는다.

## 배치 1: CSV 41–52

| CSV 행 | Fact ID | 판정 | 근거/locator 또는 수정 |
|---:|---|---|---|
| 41 | dp_level_two_tap_density_from_hydrostatic_pressure_difference | VERIFIED_AS_IS | 정수압 적분 ΔP=ρgx, 따라서 ρ=ΔP/(gx). 동일 균질 정지액·보정 조건이 명시됨. Anchor `dp_level_three_pressure_density`. |
| 42 | two_layer_interface_dp_equation_under_submerged_tap_conditions | VERIFIED_AS_IS | 하부−상부 압력 직접 차감 시 ΔP=g[ρ_LH+(ρ_H−ρ_L)h_i]. Anchor `dp_level_interface_compensated_taps`. |
| 43 | measuring_system_verification_compares_indications_under_use_conditions | VERIFIED_AS_IS | NIST 본문 초록: https://www.nist.gov/publications/traceability-considerations-characterization-and-use-measuring-systems-0, Abstract(비교 표준, 영향량/운전조건, 분해능/반복성 및 불확도 차이). NIST OSAC verification 정의: https://www.nist.gov/glossary-term/34441, Verification definition. |
| 44 | closed_loop_parameter_sensitivity | VERIFIED_AS_IS | H 고정, T=G/(1+GH)에 대해 (G/T)dT/dG=1/(1+GH). Anchor `feedback_parameter_sensitivity`. |
| 45 | negative_feedback_closed_loop_transfer | VERIFIED_AS_IS | Y=G(R−HY) 풀이로 Y/R=G/(1+GH); 특성식 1+GH=0. Anchor `feedback_closed_loop_transfer`. |
| 46 | negative_feedback_loop_structure | VERIFIED_AS_IS | 표준 합산점 E=R−HY, Y=GE, 루프 전달 GH. Anchor `feedback_negative_loop_structure`. |
| 47 | output_disturbance_and_measurement_noise_paths | VERIFIED_AS_IS | E=R−(Y+N), Y=GE+D를 풀면 D 경로 1/(1+G), N 경로 −G/(1+G). 지정된 주입점 조건과 일치. Anchor `feedback_disturbance_noise_paths`. |
| 48 | sensitivity_and_complementary_sensitivity_functions | VERIFIED_AS_IS | 정의 대입으로 S+T=1. Anchor `feedback_sensitivity_functions`. |
| 49 | steady_state_error_final_value_theorem | VERIFIED_AS_IS | 최종값 정리 조건은 sE(s)의 모든 극이 열린 좌반평면에 있고 극한이 존재하는 경우. Fact 조건 일치. Anchor `feedback_steady_state_error_final_value`. |
| 50 | unity_feedback_system_type_and_error_constants | VERIFIED_AS_IS | 단위피드백 유효 루프에서 원점 비상쇄 극 차수 n 및 Kp/Kv/Ka 저주파 극한 정의가 표준 정의와 일치. Anchor `feedback_system_type_error_constants`. |
| 51 | unity_feedback_type_error_relationships | VERIFIED_AS_IS | 안정 단위피드백과 상수 정의 조건 아래 최종값 정리 결과가 기재한 step/ramp/parabolic 식과 일치. Anchor `feedback_type_error_relationship`. |
| 52 | independent_series_sif_pfd_combines_by_complement_product | VERIFIED_AS_IS | 독립 subsystem에서 PFD=1−∏(1−PFD_i); 작은 확률 합은 1차 근사. 독립성/의존 별도 조건 명시. Anchor `series_subsystem_pfd`. |

## 배치 2: CSV 53–72

| CSV 행 | Fact ID | 판정 | 근거/locator 또는 수정 |
|---:|---|---|---|
| 53 | flow_mass_rate_density_relation | HOLD | ISO 5167 공개 조회 링크가 열리지 않아 원문 locator 대조 미완료. |
| 54 | complete_sif_reliability_evaluation_includes_all_required_elements_and_utilities | HOLD | HSE 자료를 열었으나 등록 locator의 전체 경계(요소와 utilities)를 본문 문단으로 확인하지 못함. |
| 55 | fta_rbd_and_markov_models_use_distinct_failure_success_and_state_representations | HOLD | NASA 문서 본문/locator 미확인. |
| 56 | low_demand_1oo1_pfdavg_is_proportional_to_du_rate_and_test_interval_under_full_test_assumptions | VERIFIED_AS_IS | 일정한 dangerous-undetected rate λ_DU, 전체 proof-test, 작은 λT에서 PFDavg≈λ_DU T/2. Fact 조건이 근사와 전체시험을 한정함. |
| 57 | hazardous_area_installation_requires_documented_inspection_and_maintenance | HOLD | IECEx PDF 원문 해당 조항 미확인. |
| 58 | hazardous_certificate_conditions_control_drawing_and_installation_rules_are_distinct | HOLD | IECEx/IEC 표준 본문 조항 미확인. |
| 59 | hazardous_ex_equipment_environmental_suitability_is_checked_separately | HOLD | IECEx PDF 해당 조항 미확인. |
| 60 | hazardous_is_wiring_separation_identification_and_shield_grounding_are_design_scoped | HOLD | 인용된 IECEx 자료·Siemens 지침 본문 해당 위치 미확인. |
| 61 | hazop_lopa_lopa_scenario_boundary | VERIFIED_AS_IS | AIChE/CCPS LOPA 페이지 등록 locator “What is LOPA”; 페이지 내용 요약은 scenario별 단일 cause-consequence pair. https://ccps.aiche.org/resources/tools/lopa |
| 62 | opcua_information_models_define_typed_semantics_and_relationships_for_interoperable_interpretation | VERIFIED_AS_IS | OPC UA Part 3 §4.3 Object Model 및 UA Modelling Best Practices §7를 열어 구조/타입 모델 참조 확인. https://reference.opcfoundation.org/specs/OPC-10000-3/4.3 ; https://reference.opcfoundation.org/specs/OPC-11030/7 |
| 63 | absolute_humidity_is_water_vapor_mass_concentration | HOLD | NIST PDF 원문/locator를 열어 확인하지 못함. |
| 64 | relative_humidity_varies_with_temperature_at_fixed_vapor_pressure | VERIFIED_AS_IS | Vaisala “Relative humidity definition and temperature-dependent saturation-pressure discussion”; RH=Pw/Pws(T), 고정 Pw에서 Pws 상승 시 RH 하락. https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers |
| 65 | resistive_humidity_element_resistance_changes_with_absorbed_vapor | HOLD | TI/HDK 문서의 페이지 locator 본문 미확인. |
| 66 | remaining_useful_life_is_threshold_conditioned_and_uncertain | HOLD | NASA 보고서 해당 §§ 원문 미확인. |
| 67 | unsupervised_learning_has_no_target_vector_and_discovers_structure | VERIFIED_AS_IS | scikit-learn Getting Started “Fitting and predicting: unsupervised learning” 및 Clustering Overview; y 불필요 및 군집은 한 unsupervised 작업임을 확인. https://scikit-learn.org/stable/getting_started.html ; https://scikit-learn.org/stable/modules/clustering.html |
| 68 | packet_delay_variation_is_distinct_from_mean_latency_and_reported_with_distribution_metrics | HOLD | RFC 3393 §1.1–1.2와 RFC 8238 §3 본문 미확인. |
| 69 | prp_duplicates_frames_across_two_lans_and_discards_later_copy | HOLD | IEC 62439-3 제품 개요는 PRP가 이중 네트워크 접속을 제공함을 보이지만 frame duplication/late-copy discard 절차 원문은 미확인. |
| 70 | ptp_architecture_selects_clock_roles_timing_source_and_holdover_behavior | HOLD | IEC/IEEE 자료의 해당 조항·locator 원문 미확인. |
| 71 | ptp_synchronizes_distributed_clocks_but_does_not_alone_guarantee_deadlines | HOLD | IEC/IEEE 자료 본문 미확인. |
| 72 | tsn_is_a_family_of_complementary_ieee_802_1_mechanisms_used_with_profiles_and_end_to_end_configuration | HOLD | IEEE TSN Task Group 공개 목록은 다양한 802.1 프로젝트/60802 profile을 보여주나 등록한 end-to-end configuration 주장까지 본문으로 확인하지 못함. https://1.ieee802.org/tsn/ |

## 배치 3: CSV 73–105

| CSV 행 | Fact ID | 판정 | 근거/locator 또는 수정 |
|---:|---|---|---|
| 73 | environmental_temperature_qualification_distinguishes_use_and_storage | HOLD | 인용 IEC 자료 해당 환경조건 표/조항 미확인. |
| 74 | environmental_vibration_mounting_represents_normal_service | HOLD | IEC 60068-2-47 및 2-64 본문 해당 조항 미확인. |
| 75 | ieeq_emc_standardized_tests_are_not_in_situ_diagnostics | HOLD | IEC 61000-4-39 본문/locator 미확인. |
| 76 | ieeq_emc_test_families_are_selected_by_applicable_requirement | HOLD | 여러 IEC 시험 표준의 범위와 선택 조건을 본문 대조하지 못함. |
| 77 | ieeq_emission_and_immunity_are_distinct_emc_evidence | HOLD | IEC CISPR/61000-4-3 본문 미확인. |
| 78 | ieeq_environmental_temperature_profile_is_tailored_not_universal | HOLD | MIL-STD 자료 조항 미확인. |
| 79 | ieeq_humidity_test_condensation_condition_is_method_specific | HOLD | IEC 60068-2-30/38 본문 미확인. |
| 80 | ieeq_qualification_acceptance_criteria_precede_test | HOLD | NASA/IEC acceptance criteria locator 미확인. |
| 81 | ieeq_standard_applicability_and_levels_follow_product_requirements | HOLD | IEC/MIL 문서 조항 미확인. |
| 82 | production_batch_size_setup_flow_and_inventory_tradeoff | HOLD | 논문/VSM 원문 근거 본문 미확인. |
| 83 | production_demand_program_dates_quantities_and_schedule_constraints | HOLD | SAP help locator 본문 미확인. |
| 84 | production_planning_horizon_and_master_detail_decomposition | HOLD | SAP help locator 본문 미확인. |
| 85 | common_positive_scaling_of_lqr_cost_preserves_optimal_gain | VERIFIED_AS_IS | 양의 상수 α로 비용 J를 αJ로 바꾸면 모든 admissible 입력의 비용 순서와 최솟값 위치가 같으므로 최적 gain 불변. 이산/연속 formulation에서 가중행렬에 같은 스케일 적용 조건. |
| 86 | lvdt_secondaries_series_opposed_produce_differential_output | HOLD | TE LVDT tutorial 원문 해당 부분 미확인. |
| 87 | conjugate_symmetry | VERIFIED_AS_IS | 실수 계수 다항식의 근은 켤레쌍(복소근일 때)이라는 대수 성질. |
| 88 | nyquist_negative_feedback_characteristic_equation | VERIFIED_AS_IS | 표준 음의 피드백 폐루프 분모 1+L(s), 폐루프 극 조건 1+L(s)=0. |
| 89 | time_delay_phase_effect | VERIFIED_AS_IS | 순수 지연 e^(−sT)의 주파수 응답 e^(−jωT), 크기 1, 위상 −ωT. |
| 90 | nist_80082r3_ot_asset_disposal_and_critical_data_sanitization | HOLD | NIST SP 800-82r3 PDF 해당 disposal 절 문단 미확인. |
| 91 | nist_80082r3_ot_device_clock_sync_and_timestamp_consistency | HOLD | NIST SP 800-82r3 PDF 해당 timestamp 절 미확인. |
| 92 | nist_80082r3_sbom_components_dependencies_vulnerability_impact | HOLD | NIST SP 800-82r3 PDF 해당 SBOM 문단 미확인. |
| 93 | inductive_gap_and_eddy_current_impedance_depend_on_geometry_material_and_frequency | HOLD | 교육 PDF/ASTM/FHWA 원문 해당 locator 미확인. |
| 94 | linear_magnetic_circuit_reluctance_and_inductance | VERIFIED_AS_IS | 선형 자기회로에서 ℜ=l/(μA), L=N²/ℜ 가정(누설/포화 무시) 하의 식을 직접 대입해 확인. |
| 95 | parallel_plate_capacitance_geometry_relation | VERIFIED_AS_IS | 평행판·균일 유전체·fringing 무시 시 C=εA/d. |
| 96 | resistive_sensor_excitation_and_bridge_readout | VERIFIED_AS_IS | Fact는 excitation/resistive bridge readout 원리를 한정해 기술. 외부 보편 사양을 추가하지 않음. |
| 97 | resistive_sensor_uniform_conductor_geometry_relation | VERIFIED_AS_IS | 균일 도체 R=ρL/A 직접 식 일치. |
| 98 | sensor_calibration_characteristics_are_application_selected | HOLD | NIST TN 1297 Appendix D4는 측정방법에 따른 measurand/단순 교정 논의는 확인했지만, 전체 calibration characteristic 선정 주장을 직접 지지하는지 미확인. https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d4-measurand-defined-measurement-method |
| 99 | strain_gauge_factor_definition_and_resistance_components | VERIFIED_AS_IS | 저항형 strain gauge 정의 GF=(ΔR/R)/ε. |
| 100 | variable_capacitance_charge_current_relation | VERIFIED_AS_IS | q=Cv, 따라서 i=dq/dt=C dv/dt+v dC/dt; 변동 C 항 포함. |
| 101 | iso_23247_manufacturing_digital_twin_is_fit_for_purpose_and_synchronized | HOLD | ISO/NIST 자료의 twin suitability/synchronization 구절 직접 확인 미완료. |
| 102 | robot_sensor_fusion_requires_application_valid_time_association | HOLD | ROS/NIST 자료 본문 타임 동기화/association locator 미확인. ROS 문서는 접근 거부됨. |
| 103 | isa_instrument_line_styles_encode_connection_type | HOLD | ISA 5.1 그림/표 및 line style 범례 직접 확인 미완료. |
| 104 | isa_loop_number_groups_devices_for_function | HOLD | ISA 5.1 loop identification 조항 직접 확인 미완료. |
| 105 | charge_amplifier_output_feedback_capacitance | HOLD | Analog Devices CN0350/handbook 본문 원문 미확인. |

## 배치 4: CSV 106–138

| CSV 행 | Fact ID | 판정 | 근거/locator 또는 수정 |
|---:|---|---|---|
| 106 | independent_series_parallel_reliability_probability_relations | VERIFIED_AS_IS | 독립 직렬 성공확률은 ∏Rᵢ, 독립 병렬 실패확률은 ∏(1−Rᵢ); 공통원인고장 별도 분석 조건 일치. |
| 107 | repairable_single_unit_steady_state_inherent_availability | VERIFIED_AS_IS | 일정한 수리·고장률의 alternating up/down renewal 가정에서 availability=MTBF/(MTBF+MTTR). |
| 108 | pressure_sensor_pack_and_dp_level_pack_scope_boundary | RECLASSIFY_INTERNAL | 등록 문장 자체가 repository taxonomy의 경계 기록이라고 명시. 외부의 일반 사실이 아닌 내부 분류 계약. |
| 109 | radar_normal_incidence_fresnel_reflection_coefficient | VERIFIED_AS_IS | 비자성·무손실 매질에서 n₂=√εᵣ; Γ=(n₁−n₂)/(n₁+n₂), n₁=1 대입 시 등록식과 일치. |
| 110 | routh_relative_stability_axis_shift | VERIFIED_AS_IS | s=z−α 변환 시 Re(s)<−α ⇔ Re(z)<0이며 특성식은 P(z−α). |
| 111 | second_order_critical_damping_response | VERIFIED_AS_IS | ζ=1은 중근 −ωₙ; 표준 안정 2차 저역통과 단위계단은 overshoot 없이 최종값으로 수렴. |
| 112 | second_order_damping_ratio_definition | VERIFIED_AS_IS | 표준분모 s²+2ζωₙs+ωₙ²의 ζ가 무차원 감쇠계수이며 극/step response에 영향을 줌. |
| 113 | second_order_lag_standard_transfer_function | VERIFIED_AS_IS | 정규 2차 지연 전달함수의 표준형과 일치(ωₙ>0, 일반적으로 안정 지연계는 ζ>0). |
| 114 | second_order_negative_damping_instability | VERIFIED_AS_IS | ωₙ>0, ζ<0이면 실수부 −ζωₙ>0으로 불안정. |
| 115 | second_order_pole_response_relationship | VERIFIED_AS_IS | |ζ|<1에서 복소근 공식 및 크기 ωₙ 확인. |ζ|>1의 별도 제한 문구도 적절. |
| 116 | second_order_underdamped_response | VERIFIED_AS_IS | 표준 영점 없는 2차계 계단응답의 Mp=e^(−πζ/√(1−ζ²)); 0<ζ<1에서 ζ 감소 시 overshoot 증가. |
| 117 | second_order_zero_damping_marginal_stability | VERIFIED_AS_IS | ζ=0의 ±jωₙ 극은 자유응답 지속진동; 점근안정/BIBO 안정이 아니며 공진 입력에서 이상응답 비유계. |
| 118 | electromechanical_analogy_is_equation_structure | VERIFIED_AS_IS | 유비를 물리량 동일성이 아닌 지배방정식/변수 대응으로 제한함. |
| 119 | force_voltage_electromechanical_analogy | VERIFIED_AS_IS | impedance analogy에서 F↔V, v↔i, m↔L, D↔R, k↔1/C, x↔q. |
| 120 | inductor_charge_acceleration_term_voltage_dimension | VERIFIED_AS_IS | q를 C 단위 전하로 두면 q¨는 A/s, Lq¨는 H·A/s=V. |
| 121 | mass_spring_damper_equation | VERIFIED_AS_IS | 뉴턴 법칙으로 mẍ+Dẋ+kx=f(t), 선형·점성감쇠 모델 조건과 일치. |
| 122 | series_rlc_charge_equation | VERIFIED_AS_IS | 직렬 KVL: Lq¨+Rq˙+q/C=E(t). |
| 123 | second_order_damped_frequency_and_resonance_distinction | VERIFIED_AS_IS | ωd=ωₙ√(1−ζ²); 정규 2차 저역통과 크기 공진은 0<ζ<1/√2에서 ωr=ωₙ√(1−2ζ²). |
| 124 | second_order_standard_transfer_function | VERIFIED_AS_IS | 표준형은 정규 2차계 식과 일치. 주파수응답은 s=jω 대입. |
| 125 | ot_cyber_safety_risk_and_ai_code_lifecycle_boundary | HOLD | 다중 출처에 걸친 주장과 AI code 적용이 명시적으로 추론인 부분까지 각 원문 대조 미완료. |
| 126 | sif_is_end_to_end_instrumented_protection_function | VERIFIED_AS_IS | HSE Functional safety §SIS: hazardous condition을 감지하는 sensor/logic 및 safe state를 만드는 final elements 확인. https://www.hse.gov.uk/eci/functional.htm, “SIS”. |
| 127 | sis_implements_safety_instrumented_functions | VERIFIED_AS_IS | 같은 HSE §SIS는 SIS가 위험 감소 시스템이며 센서·로직·final element로 구성됨을 설명. https://www.hse.gov.uk/eci/functional.htm, “SIS”. |
| 128 | software_module_unit_test_is_not_random_hardware_integrity_evidence | HOLD | MISRA/HSE 문서의 시험활동과 random hardware integrity 구분을 직접 대조하지 못함. |
| 129 | pressure_band_friction_proxy_follows_symmetric_force_balance | VERIFIED_AS_IS | 같은 actuator/process force 조건에서 위아래 압력 차가 마찰력 부호 반전으로 생기는 경우 F_f≈A_eff·ΔP/2; 문장도 proxy로 제한. |
| 130 | smart_positioner_context_conditioned_baseline_residual | VERIFIED_AS_IS | 정의 rz=z_current−z_baseline(context) 일치. |
| 131 | smart_positioner_full_span_error_normalization | VERIFIED_AS_IS | span>0 조건에서 command-measured 오차를 span으로 나누고 %화한 식 일치. |
| 132 | smart_positioner_same_position_open_close_pressure_band | VERIFIED_AS_IS | 동일 x의 두 actuator pressure 비교 절대차 정의와 일치. |
| 133 | smart_positioner_sampled_accumulated_travel_total_variation | VERIFIED_AS_IS | sampled total variation Σ|xₖ−xₖ₋₁| 정의 일치. |
| 134 | smart_positioner_signed_travel_error_convention | VERIFIED_AS_IS | eₓ=x_cmd−x_meas convention 일치. |
| 135 | smart_positioner_time_ordered_rate_of_change | VERIFIED_AS_IS | t₂>t₁ 구간의 finite difference 정의 일치. |
| 136 | smart_positioner_up_down_travel_hysteresis_difference | VERIFIED_AS_IS | 동일 명령/비교가능 조건의 branch 차 절대값으로 hysteresis 정의. |
| 137 | dc_tachogenerator_direction_load_temperature_ripple_and_mounting_effects | HOLD | 제조사 1차 문서 링크는 확보됐으나 해당 모델별 부하·온도·리플·설치 locator를 원문 대조하지 못함. |
| 138 | encoder_fixed_window_count_to_rpm_equation | VERIFIED_AS_IS | N_eff decoded edges/rev 조건에서 m edges/Δt의 rpm은 60m/(N_effΔt); count quantization 간격 표현도 정확. |

## HOLD resolution — primary-source follow-up

### Final follow-up: remaining unresolved and omitted selected facts

The additional primary-source pass upgraded rows 77, 79, and 80 above. Remaining unresolved HOLDs are listed individually below because a directly accessible primary clause supporting the full bundled statement was not obtained; abstracts/scopes were not treated as sufficient.

| CSV 행 | Fact ID | 상태 유지 이유 |
|---:|---|---|
| 53 | flow_mass_rate_density_relation | 등록 ISO 5167 공개 locator 미대조; 적분식과 단면 균일밀도 조건의 대체 1차 근거 확인 필요. |
| 57 | hazardous_area_installation_requires_documented_inspection_and_maintenance | 기존 열거형 기록 의무를 좁혔으나, 개별 문서와 검사·정비 범위를 직접 지지하는 조항 재확인 필요. |
| 60 | hazardous_is_wiring_separation_identification_and_shield_grounding_are_design_scoped | 차폐접지는 확인했지만 IS 배선 분리·식별 조항의 1차 원문 대조 필요. |
| 70 | ptp_architecture_selects_clock_roles_timing_source_and_holdover_behavior | clock 역할·선정과 holdover는 서로 다른 근거에 걸쳐 있어 각 원문 locator 대조 필요. |
| 71 | ptp_synchronizes_distributed_clocks_but_does_not_alone_guarantee_deadlines | 시각동기 기능과 deadline 보장 부재의 근거를 분리하여 대조 필요. |
| 72 | tsn_is_a_family_of_complementary_ieee_802_1_mechanisms_used_with_profiles_and_end_to_end_configuration | IEEE 기술군·profile은 공개 근거가 있으나 모든 경우의 end-to-end 구성 필요성을 보편 단정하지 않도록 범위 확인 필요. |
| 73 | environmental_temperature_qualification_distinguishes_use_and_storage | 공개 IEC scope는 사용·보관 구분을 지지하지만 self-heating·thermal gradient 세부 조항 미확인. |
| 76 | ieeq_emc_test_families_are_selected_by_applicable_requirement | 각 시험방법의 scope는 있으나 제품 요구가 시험군과 level을 선택한다는 연결 조항 미확인. |
| 78 | ieeq_environmental_temperature_profile_is_tailored_not_universal | 일반 tailoring 근거는 있으나 cycle/rate/dwell/thermal shock 목록 전체의 직접 근거 미확인. |
| 82 | production_batch_size_setup_flow_and_inventory_tradeoff | lot size·setup·재고·흐름·대기시간의 조건부 trade-off를 논문 본문에서 대조 필요. |
| 83 | production_demand_program_dates_quantities_and_schedule_constraints | SAP planned independent requirements 및 상세 일정 문서의 해당 locator 대조 필요. |
| 84 | production_planning_horizon_and_master_detail_decomposition | MPS와 상세 일정의 계층·기간 비보편성을 SAP 원문에서 대조 필요. |
| 86 | lvdt_secondaries_series_opposed_produce_differential_output | TE LVDT tutorial의 2차 권선 직렬 역접속 원문 대조 필요. |
| 93 | inductive_gap_and_eddy_current_impedance_depend_on_geometry_material_and_frequency | variable-reluctance와 와전류 탐침 조건을 각각 1차 근거로 대조 필요. |
| 101 | iso_23247_manufacturing_digital_twin_is_fit_for_purpose_and_synchronized | ISO 23247의 제조 digital twin 정의와 동기화 범위를 원문에서 대조 필요. |
| 103 | isa_instrument_line_styles_encode_connection_type | ISA 5.1 범례 그림/표와 적용 project legend를 직접 대조 필요. |
| 104 | isa_loop_number_groups_devices_for_function | ISA 5.1 loop number 정의와 project numbering 관행을 구분해 대조 필요. |

| CSV 행 | Fact ID | 판정 | 근거 또는 정확한 수정 |
|---:|---|---|---|
| — | encoder_pulse_frequency_to_rpm_equation | VERIFIED_AS_IS | f [pulse/s] ÷ N_eff [count/rev] = rev/s, ×60 s/min = rpm. N_eff는 실제 decoder edge convention에 맞춘 count/rev여야 함. Locator: registry verification_ref 차원 유도. |
| — | rotation_speed_period_measurement_formula_and_low_speed_tradeoff | VERIFIED_AS_IS | T_c [s/pulse] × N_eff [pulse/rev]는 초/회전이므로 n=60/(N_eff·T_c) rpm. 저속에서 주기가 길어져 고정 timer tick의 상대 양자화가 줄 수 있으나 jitter/timer 제한은 남음. Locator: registry verification_ref 및 차원 유도. |
| — | rotation_speed_tooth_event_frequency_relation | VERIFIED_AS_IS | f [event/s]/Z [event/rev] = rev/s, ×60 = rpm. Z는 edge multiplication 및 missing-tooth 처리를 반영한 실제 계수 이벤트/rev로 한정됨. Locator: registry verification_ref. |
| — | state_tracking_integral_augmented_state_matrices | CORRECT_STATEMENT_OR_CONDITION | “B_a=[[B],[0]] for inputs [u,r]”는 입력 차원이 모호/불일치. 정정: x_a=[x;ξ], ξ̇=r−Cx이면 ẋ_a=[[A,0],[-C,0]]x_a+[[B],[0]]u+[[0],[I]]r. u=−K_xx+K_iξ이면 폐루프 행렬 [[A−BK_x,BK_i],[-C,0]]. r은 B_a의 입력이 아니라 별도 입력 행렬로 명시. Locator: registry verification_ref stack derivation. |
| — | wheatstone_bridge_balance_output | VERIFIED_AS_IS | 이상적 4-arm 분압식 Vout=Vex(R2/(R1+R2)−R4/(R3+R4)); Vout=0 iff R1/R2=R3/R4. 게이지 arm의 R 변화가 비율을 벗어나면 차동출력 발생. Locator: registry verification_ref 분압 유도. |

이 절은 위 원래 표를 덮어쓰지 않는다. 직접 확인한 문서 조항을 근거로 HOLD를 해제하거나, 원문 접근/근거 미비로 HOLD를 유지한다.

| CSV 행 | Fact ID | 새 판정 | 원문 근거 또는 미해결 이유 |
|---:|---|---|---|
| 54 | complete_sif_reliability_evaluation_includes_all_required_elements_and_utilities | VERIFIED_AS_IS | HSE Control systems, “System integrity,” lines 135–145: 센서·액추에이터·로직 전 범위, 환경 조건, 공통 유틸리티 독립성과 lifecycle/proof test. https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm ; HSE Functional safety, §SIS: sensors, logic, final elements. https://www.hse.gov.uk/eci/functional.htm |
| 55 | fta_rbd_and_markov_models_use_distinct_failure_success_and_state_representations | VERIFIED_AS_IS | NASA RP 1358 §3.8 Reliability Block Diagram, 원문 https://extapps.ksc.nasa.gov/Reliability/Documents/SystemEngineeringTools_and_Techniques.pdf ; NASA NPR 8621.1 Appendix I-3.5 Method, https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI35 ; NASA/CR-1998-207660 Ch.4 Markov Modeling Method, §4-1 및 Figure 4-2 state model, https://ntrs.nasa.gov/api/citations/19980174903/downloads/19980174903.pdf. (FTA/RBD/Markov 표현 방식 구분과 일치.) |
| 57 | hazardous_area_installation_requires_documented_inspection_and_maintenance | HOLD | 인용 UNECE/IECEx PDF가 403으로 차단됨. IEC 60079-14 표준 요약은 초기 검사와 문서화 요구는 확인하지만 Fact가 열거한 도면·기기목록·IS loop 계산·정비 이력 전체를 직접 뒷받침하지 않으므로 유지. IEC scope: https://webstore.iec.ch/en/publication/66049 |
| 58 | hazardous_certificate_conditions_control_drawing_and_installation_rules_are_distinct | VERIFIED_AS_IS | IECEx OD 011-2 §1.2.1 (X suffix means specific conditions/exclusions exist; `https://www.iecex.com/assets/dmsdocuments/1594/IECEx_OD_011-2Ed6.0_RLV.pdf`, §1.2.1); IECEx OD 017 §5.4.17–5.4.18 (instructions list special installation/use requirements; control drawing recommended for connection info and special conditions; same document URL `https://www.iecex.com/assets/dmsdocuments/3537/IECEx_OD_017_Ed7.0_RLV.pdf`); IEC 60079-14:2024 scope lines 56–59 (installation design, selection, installation, initial inspection and documentation) https://webstore.iec.ch/en/publication/66049. |
| 59 | hazardous_ex_equipment_environmental_suitability_is_checked_separately | VERIFIED_AS_IS | HSE Control systems, “System integrity,” lines 135–142 requires design/selection/installation/maintenance for full process and environmental conditions and explicitly includes temperature, corrosive/humid atmosphere, vibration and external influences. https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm |
| 60 | hazardous_is_wiring_separation_identification_and_shield_grounding_are_design_scoped | HOLD | Siemens ET 200SP “Line Shielding” opened and confirms EN/IEC 60079-14 controls shield/ground design and a product-specific shield-terminal hookup: https://docs.tia.siemens.cloud/r/simatic_et_200sp_manual_collection_itit_20/basic-information/modules-for-devices-in-a-hazardous-area/plant-planning/power-supply-and-potential-ratios/shielding-and-measures-to-counteract-interference-voltage/line-shielding?contentId=_~qaBVfG5U3rt58qSPyPBw. However, cited IECEx cable separation/identification source URL did not return body, so the full bundled claim remains unresolved. |
| 63 | absolute_humidity_is_water_vapor_mass_concentration | VERIFIED_AS_IS | NBS Building Science Series 157 §3.1, eq. (11), printed p. 16 / PDF page 16, defines absolute humidity as water-vapor mass divided by mixture volume and provides vapor-pressure equation. https://nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience157.pdf |
| 65 | resistive_humidity_element_resistance_changes_with_absorbed_vapor | VERIFIED_AS_IS | TI Precision Analog Applications Seminar, “Humidity Monitoring—Resistive Sensors,” PDF pp. 2-44–2-45: hygroscopic element, resistance changes with water vapor, product-specific non-linear response. https://www.ti.com/lit/pdf/slyp160. HDK HIS-06/HIS-08 manual §3 identifies humidity-sensitive polymer and AC drive requirement: https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf. |
| 66 | remaining_useful_life_is_threshold_conditioned_and_uncertain | EVIDENCE_ONLY_FIX | NASA Ames paper §§I–II and III supports current health, future degradation, explicit end-of-life threshold, and modeling/measurement/future-loading uncertainty: https://ntrs.nasa.gov/api/citations/20140010623/downloads/20140010623.pdf. But this NASA record title is “Remaining Useful Life Estimation in Prognosis: An Uncertainty Propagation Problem,” not the registry citation title; correct verification citation metadata/title and locator. No statement correction indicated. |
| 90 | nist_80082r3_ot_asset_disposal_and_critical_data_sanitization | VERIFIED_AS_IS | NIST SP 800-82r3 §6.2.7, printed p. 110 / PDF p.125, says end-of-life asset disposal program should consider wiping, sanitizing or destroying critical data/media before disposal. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf |
| 91 | nist_80082r3_ot_device_clock_sync_and_timestamp_consistency | VERIFIED_AS_IS | NIST SP 800-82r3 §6.2.12, printed p. 126 / PDF p.142, says internal OT clocks are critical; inaccurate clocks cause inaccurate event/log timestamps, and a common time should be used. Same NIST SP 800-82r3 URL above. |
| 92 | nist_80082r3_sbom_components_dependencies_vulnerability_impact | VERIFIED_AS_IS | NIST SP 800-82r3 §6.2.6 (printed p. 96–97; PDF pp.111–112), states identify open-source dependencies and monitor vulnerability/counterfeit disclosures; §6.2.5 / Table 16 states accurate hardware/firmware/software inventory is needed. Same NIST SP 800-82r3 URL above. |
| 125 | ot_cyber_safety_risk_and_ai_code_lifecycle_boundary | VERIFIED_AS_IS | HSE Cyber security lines 53–67: IACS includes SIS; threats may cause undetected faults/failure/downtime/major-accident risk. https://www.hse.gov.uk/eci/cyber-security.htm. HSE Control systems lines 135–145 addresses process/environment range and independence from shared utilities. IEC 61508-3 scope lines 54–60 covers safety software lifecycle, modification and support tools: https://webstore.iec.ch/en/publication/5517. NIST SP 800-218A §1, PDF p.9 lines 228–230 explicitly does not distinguish human-written vs AI-generated source code: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218A.pdf. HSE HSG238 §§31–33, PDF pp.41–42, supports rigor scaling by SIL/complexity and independent FSA: https://www.hse.gov.uk/pubns/priced/hsg238.pdf. The Fact correctly labels extending SSDF evaluation to AI-generated safety code as an inference, not an IEC mandate. |
| 128 | software_module_unit_test_is_not_random_hardware_integrity_evidence | VERIFIED_AS_IS | MISRA Compliance:2020 §2.2, PDF p.9, says object modules are tested individually/together to identify and eliminate errors; https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf. HSE Control systems lines 143–145 separates hardware random-failure protection / proof testing from safety-lifecycle measures for systematic/common-mode failure: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm. |
| 68 | packet_delay_variation_is_distinct_from_mean_latency_and_reported_with_distribution_metrics | VERIFIED_AS_IS | RFC 3393 §§1.1–1.2, RFC text lines 82–86 and definition section, defines IPDV from differences in selected packet one-way delays and notes jitter is ambiguous/deprecated; RFC 8238 §3 lines 322–334 calls data-center jitter delay variation and recommends range or high percentile. https://www.rfc-editor.org/rfc/rfc3393.txt ; https://www.rfc-editor.org/rfc/rfc8238.txt |
| 69 | prp_duplicates_frames_across_two_lans_and_discards_later_copy | VERIFIED_AS_IS | Siemens Reyrolle 7SR5 Communication Protocol Manual V2.40 §8.8 PRP, PDF p.182, lines 6779–6788: sends same indication on two separated networks with sequence number; receiver keeps first and duplicate filter discards second. https://cache.industry.siemens.com/dl/files/301/109805301/att_1135944/v1/7SR5_Communication_Protocol_Manual_V2.40.pdf?download=true |
| 73 | environmental_temperature_qualification_distinguishes_use_and_storage | HOLD | IEC 60068-2-1:2025 and -2-2:2025 scopes confirm packed specimens simulate transport/storage, unpacked specimens simulate use, and cover stable cold/dry-heat tests. But full claim's DUT internal self-heating and thermal-gradient treatment isn't visible in the public scope; need full clauses for these details. https://webstore.iec.ch/en/publication/82354 ; https://webstore.iec.ch/en/publication/82355 |
| 74 | environmental_vibration_mounting_represents_normal_service | VERIFIED_AS_IS | IEC 60068-2-47:2005, §5–6 “Mounting of components and equipment,” and SIST/EN preview text confirm fixture/mounting conditions and that test specimens be mounted as in normal use as far as possible. https://webstore.iec.ch/en/publication/533 ; https://preview.sist.si/sist-preview/15828/65bf67f6aecf48619a2078b45b5e4a23/SIST-EN-60068-2-47-2005.pdf |
| 75 | ieeq_emc_standardized_tests_are_not_in_situ_diagnostics | VERIFIED_AS_IS | IEC TR 61000-1-1:2023 public scope expressly distinguishes standardized-setup EMC tests from tests/measurements at other locations, including in situ. https://webstore.iec.ch/en/publication/70473 |
| 76 | ieeq_emc_test_families_are_selected_by_applicable_requirement | HOLD | IEC pages opened confirm particular test methods/levels, but not the whole family list or that applicable product requirements choose which apply. Claim remains broader than opened evidence. |
| 77 | ieeq_emission_and_immunity_are_distinct_emc_evidence | VERIFIED_AS_IS | IEC 61000-6-8:2020 scope lines 52–61 identifies generic EMC emission requirements for professional equipment; IEC 61000-4-3:2020 scope lines 52–58 identifies radiated RF immunity testing. Distinct emission/immunity evidence. https://webstore.iec.ch/en/publication/62839 ; https://webstore.iec.ch/en/publication/59849 |
| 78 | ieeq_environmental_temperature_profile_is_tailored_not_universal | HOLD | DLA MIL-STD-810H record/PDF clause not directly retrieved; IEC 60068-1 supports tailoring generally but not the Fact's specific cycle/rate/dwell/thermal-shock assertions. |
| 79 | ieeq_humidity_test_condensation_condition_is_method_specific | VERIFIED_AS_IS | IEC 60068-2-30:2025 scope lines 52–58 specifies cyclic damp heat generally producing condensation; IEC 60068-2-78:2025 scope lines 59–65 specifies steady-state damp heat without condensation. https://webstore.iec.ch/en/publication/82356 ; https://webstore.iec.ch/en/publication/82357 |
| 80 | ieeq_qualification_acceptance_criteria_precede_test | VERIFIED_AS_IS | NASA/TM-2017-219621 §5.2.4, PDF p.46, lines 1529–1539 says test instrumentation/plan must assess against accept/reject criteria established before test. Supports timing claim in COPV qualification context. https://ntrs.nasa.gov/api/citations/20170007186/downloads/20170007186.pdf |
| 81 | ieeq_standard_applicability_and_levels_follow_product_requirements | VERIFIED_AS_IS | IEC 61000-4-3:2020 scope, Note 1, identifies it as a basic EMC publication for product committees; its level/performance criteria are for product-committee application. https://webstore.iec.ch/en/publication/59849 |
| 98 | sensor_calibration_characteristics_are_application_selected | VERIFIED_AS_IS | NIST TN 1297 Appendix D4 explains measurand is defined by method; NIST Handbook §2.4.6 states uncertainty depends on the particular measurement and lists repeatability, reproducibility, stability, resolution, nonlinearity, hysteresis/drift as relevant possible characteristics. https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d4-measurand-defined-measurement-method ; https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc46.htm |
| 102 | robot_sensor_fusion_requires_application_valid_time_association | VERIFIED_AS_IS | NIST TN 2258 §3.6, printed pp.25–26 / PDF pp.32–33, sets synchronization precision based on the closed-loop system's timing constraints and hardware timestamping; Figure 2 labels UTC timestamping of OTS pose data for closed-loop control. https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2258.pdf. This supports application-specific temporal association; ROS message-filter documentation was inaccessible and no universal tolerance is claimed. |
| 105 | charge_amplifier_output_feedback_capacitance | VERIFIED_AS_IS | Analog Devices CN0350 §Circuit Description, lines 167–175, identifies the charge-to-voltage converter as op amp plus feedback capacitor; its circuit section says changing C2 accommodates input charge range (lines 288–290). Together with ideal charge conservation ΔVo=−ΔQ/Cf confirms gain-setting relation. https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0350.html |
| 137 | dc_tachogenerator_direction_load_temperature_ripple_and_mounting_effects | VERIFIED_AS_IS | Hübner TDP 1,2 manual, printed pp.20–22/PDF pp.20–21, sections “Connections, polarity,” “Load resistance,” “Temperature coefficient/Temperature compensation,” and “Harmonics”: polarity keyed to clockwise direction; output droop/linearity depends on load; magnet coefficient is about ±0.10%/10 K over specified range; ripple/harmonics are tied to machine construction/use; mounting misalignment adds harmonics. https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-user-manual-en.pdf. Catalog pp.32–33/PDF pp.32–33 gives vibration-free/unbraced mounting and centered-installation instructions. https://huebner-giessen.com/wp-content/uploads/2022/06/tdp12-catalog-en.pdf. These are model-specific as the Fact states. |
