# Topic Pack Fact Anchor 감사 — 최종 68개

- 감사일: 2026-10-08
- 대상: 상태공간 설계, 스트레인게이지·로드셀, 열전달 오차, Thermistor, Thermocouple, 초음파 거리/레벨
- 판정: 원리·정의 확인 36, 설치·부품·성능조건 확인 32, 확정 오류 0, 수정 0
- 조건 확인은 사실오류가 아니라 모델·교정·설치·환경에 맞는 적용값 또는 절차를 확인해야 한다는 뜻이다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `state_space_controllability_observability_pole_placement` | 14–14 | 1 | 0 | 1 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 1–14 | 14 | 9 | 5 |
| `temperature_measurement_error_heat_transfer` | 1–5 | 5 | 2 | 3 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 1–14 | 14 | 8 | 6 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 1–14 | 14 | 7 | 7 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 1–20 | 20 | 10 | 10 |
| **합계** |  | **68** | **36** | **32** |

## 기술 대조 요약

- 상태공간 전달함수·최소 realization, controllability/observability와 PBH 조건, pole placement·observer 및 tracking/integral action 구분을 확인했다. 최종 제어기와 observer pole은 actuator, noise, sampling과 plant model에 맞춰 검증해야 한다.
- Strain gauge의 저항 변화, GF, Wheatstone bridge, quarter/half/full bridge의 감도·온도보상 원리를 대조했다. 브리지 감도는 작은 변형률의 근사 및 구체적인 gauge 배치/type에 의존한다 ([NI strain-gage measurement guide](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html)). Load-cell 설치·온도·크리프·보정은 기계구조와 제조사 성능조건에 종속된다.
- 온도계 설치오차의 열저항, stem conduction, immersion depth와 thermowell의 응답영향을 확인했다. 구체 담금깊이 또는 보호관 sizing은 형상·유속·정확도 요구에서 결정한다.
- Thermistor의 NTC/PTC 동작, 제한 범위 B 식, Steinhart–Hart 보정, 자기발열과 회로/ADC 영향을 대조했다. 계수와 동작범위는 소자별 자료 및 교정으로 확정해야 한다.
- Thermocouple의 Seebeck 원리, 기준접점 보상, intermediate-metal/temperature 법칙, 종류별 table·polynomial 환산, extension/compensating wire 및 접점구조를 확인했다. 적용 온도·분위기·정확도와 재료 조합은 표준 등급 및 제조사 자료를 확인한다. 제3 금속 삽입은 두 접점이 같은 온도일 때 순 열기전력에 영향이 없다는 원리로 설명했다 ([Omega thermocouple reference](https://br.omega.com/omegaFiles/techref/pdf/z019-020.pdf)).
- 초음파 pulse-echo에서 d=ct/2, 공기 음속 온도 의존성, ringdown/dead zone, 반사면·설치·echo 선택의 원리를 확인했다. blanking distance와 compensation은 제품별이며 foam/vapor, 거리·대상물 영향 역시 적용조건에 따른다 ([Emerson Rosemount 3100 reference manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0100-4840.pdf)).

## 보류 또는 범위 주의

- 브리지 회로식의 출력 부호·정확한 계수는 브리지 arm 배치, wiring과 excitation/sense 정의를 고정해야 한다. 원문은 해당 감도계수만 작은 변형률·구성 의존적 조건으로 처리했다.
- 고유한 immersion depth, thermistor coefficient, thermocouple tolerance, ultrasonic blanking distance/response와 특정 transmitter의 calibration 주기는 제품 및 현장자료 없이 일반화하지 않았다.
- 확정 기술 오류는 없어 원문 수정은 하지 않았다.

## 전체 감사 종료 기록

- Topic Pack 원본 인벤토리: 87개 Pack, **2,068 Anchors**.
- 배치 보고서 10개(각 200개)와 최종 보고서(68개)의 등록부가 원본 Topic ID·Anchor ID·순번과 일치한다. 중복 0, 누락 0, ID/순번 불일치 0으로 **2,068/2,068 전체 등록**을 확인했다.
- 앞선 진행 기록의 2,073은 실제 원본보다 5개 큰 분모였다. 종료 집계는 저장소 validator가 확인한 2,068개를 기준으로 한다.
- 등록부 판정 총계: 확인/사실확인 1,321, 조건·맥락·적용조건 확인 747. 조건 확인은 오류 판정이 아니며 현장별 자료가 있어야 확정할 적용사항이다.
- 이번 전체 감사 과정에서 확정된 statement/claim 불일치 3건을 SIS/SIL Pack에서 바로잡았다. 그 외 명백한 기술 오류는 확인되지 않아 원문을 유지했다.
- 전체 schema validation: 87 packs/2,068 anchors PASS. 전체 quality validation: errors 0, warnings 28. 28건은 `logic_check deterministic_checks.topic_aliases empty` 경고이며 Anchor 사실오류 판정과는 별개의 후속 품질 항목이다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `state_space_controllability_observability_pole_placement` | 14 | `implementation_tradeoffs_validation` | 조건 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 1 | `strain_gauge_resistance_change_principle` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 2 | `strain_gauge_factor_definition` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 3 | `strain_poisson_transverse_effect` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 4 | `wheatstone_bridge_balance_output` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 5 | `quarter_bridge_sensitivity_temperature` | 조건 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 6 | `half_bridge_sensitivity_compensation` | 조건 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 7 | `full_bridge_sensitivity_compensation` | 조건 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 8 | `load_cell_force_strain_voltage_chain` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 9 | `load_cell_excitation_ratiometric_output` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 10 | `instrumentation_amplifier_adc_signal_chain` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 11 | `temperature_zero_span_compensation` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 12 | `creep_hysteresis_nonlinearity_repeatability` | 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 13 | `installation_eccentric_load_overload` | 조건 확인 |
| `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` | 14 | `wiring_shield_ground_fault_diagnostics` | 조건 확인 |
| `temperature_measurement_error_heat_transfer` | 1 | `temperature_heat_transfer_error_paths` | 확인 |
| `temperature_measurement_error_heat_transfer` | 2 | `temperature_heat_resistance_model` | 조건 확인 |
| `temperature_measurement_error_heat_transfer` | 3 | `temperature_stem_conduction_immersion_error` | 확인 |
| `temperature_measurement_error_heat_transfer` | 4 | `temperature_installation_selection_conditions` | 조건 확인 |
| `temperature_measurement_error_heat_transfer` | 5 | `temperature_error_reduction_measures` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 1 | `thermistor_temperature_measurement_chain` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 2 | `thermistor_semiconductor_resistance_temperature_principle` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 3 | `thermistor_ntc_negative_temperature_coefficient` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 4 | `thermistor_ntc_beta_equation` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 5 | `thermistor_steinhart_hart_linearization` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 6 | `thermistor_ptc_positive_temperature_coefficient_switching` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 7 | `thermistor_voltage_divider_bridge_current_measurement` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 8 | `thermistor_adc_reference_ratiometric_conversion` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 9 | `thermistor_self_heating_dissipation_constant` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 10 | `thermistor_thermal_time_constant_installation` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 11 | `thermistor_tolerance_interchangeability_calibration` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 12 | `thermistor_operating_range_material_selection_stability` | 조건 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 13 | `thermistor_wiring_contact_moisture_noise_effects` | 확인 |
| `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` | 14 | `thermistor_fault_diagnostics_open_short_range_fail_safe` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 1 | `thermocouple_temperature_measurement_chain` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 2 | `thermocouple_seebeck_effect_dissimilar_conductors` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 3 | `thermocouple_measures_temperature_difference` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 4 | `thermocouple_reference_junction_compensation` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 5 | `thermocouple_law_of_intermediate_metals` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 6 | `thermocouple_law_of_intermediate_temperatures` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 7 | `thermocouple_type_material_range_atmosphere_selection` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 8 | `thermocouple_extension_compensating_wire_polarity` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 9 | `thermocouple_nonlinearity_reference_tables_polynomial_conversion` | 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 10 | `thermocouple_junction_construction_response_isolation` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 11 | `thermocouple_thermowell_installation_dynamic_error` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 12 | `thermocouple_signal_conditioning_noise_grounding` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 13 | `thermocouple_calibration_tolerance_uncertainty_drift` | 조건 확인 |
| `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` | 14 | `thermocouple_fault_diagnostics_open_polarity_cjc_validation` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 1 | `ultrasonic_sensor_system_structure` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 2 | `ultrasonic_piezoelectric_transduction` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 3 | `ultrasonic_pulse_echo_time_of_flight` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 4 | `ultrasonic_round_trip_distance_equation` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 5 | `ultrasonic_sound_speed_medium_dependence` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 6 | `ultrasonic_air_temperature_compensation` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 7 | `ultrasonic_dead_zone_ringdown` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 8 | `ultrasonic_beam_angle_footprint` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 9 | `ultrasonic_target_reflectivity_orientation` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 10 | `ultrasonic_frequency_range_resolution_tradeoff` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 11 | `ultrasonic_attenuation_max_range` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 12 | `ultrasonic_echo_amplitude_validity` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 13 | `ultrasonic_level_measurement_reference` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 14 | `ultrasonic_false_echo_multiple_reflection` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 15 | `ultrasonic_foam_vapor_turbulence_error` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 16 | `ultrasonic_mounting_nozzle_obstruction_error` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 17 | `ultrasonic_sensor_crosstalk` | 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 18 | `ultrasonic_repetition_rate_response_averaging` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 19 | `ultrasonic_calibration_echo_mapping_diagnostics` | 조건 확인 |
| `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error` | 20 | `ultrasonic_application_limits_comparison` | 조건 확인 |
