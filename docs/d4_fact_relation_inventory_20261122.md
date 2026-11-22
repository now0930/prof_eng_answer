# D4-WRONG-15: 26개 Fact의 연구용 관계 범위

승인 Registry Fact를 이용한 구성요소 비교 후보와 미지원 대상을 기록합니다. 모든 비교는 연구용이며 `source_match_proven=false`, `score_admission=DISABLED`, `score_effect=none`입니다. 명시된 관계의 부정 여부는 모델 제안이고 원문 span 일치만으로 의미가 입증되지 않습니다. `PARTIAL`은 프로파일이 실제 답안의 의미를 검증한다는 뜻이 아닙니다.

실제 제공된 55개 Claim의 고유 Fact ID 26건을 확인했습니다. 기존 5개와 신규 10개는 원 Registry relation·condition에 한정된 PARTIAL, 11개는 HOLD입니다. 새 프로파일은 자연어 추출이나 기술적 정답 라벨을 자동으로 만들지 않습니다.

| Fact ID | 상태 | 근거·미완료 사유 |
|---|---|---|
| `final_element_safe_action_process_dependent` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `fisher_585c_fail_close_spring_must_provide_required_seat_force` | HOLD | 제조사·모델별 스프링과 seat force 조건 및 힘 평형 검토 필요 |
| `fisher_actuator_sizing_sums_loads_for_service_case` | HOLD | 공급 압력 및 적용 하중별 부호·제원 검토 필요 |
| `fisher_balanced_trim_reduces_static_unbalance_not_all_loads` | HOLD | 정적 불평형의 제한 효과와 다른 하중 구분 필요 |
| `fisher_unbalance_force_pressure_area_equations` | HOLD | 트림 형상별 힘·면적·단위 관계 검토 필요 |
| `friction_force_opposes_relative_or_impending_motion` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `linear_spring_force_changes_with_preload_and_displacement` | HOLD | 선형 모델·방향·예압의 수치 및 단위 검토 필요 |
| `rtd_four_wire_kelvin_measurement` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `rtd_three_wire_bridge_compensation_assumptions` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `second_order_critical_damping_response` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `second_order_damping_target_is_application_tradeoff` | HOLD | 응답 목표·적용 조건은 보편 단일값이 아님 |
| `second_order_overdamped_response` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `second_order_pole_response_relationship` | HOLD | 복소극·실근 경계와 수식 적용 범위 검토 필요 |
| `second_order_underdamped_response` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `sil_achieved_sil_verification` | HOLD | 전체 SIF 정량·구조 검증 범위가 복합적임 |
| `sil_demand_mode_metric_selection` | HOLD | 요구 모드별 지표 및 적용 조건 구분 필요 |
| `sil_sis_sif_scope` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `sw04_integration_test_verifies_software_interfaces` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `sw04_system_test_checks_system_requirements_in_intended_environment` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `sw04_unit_test_verifies_isolated_software_units` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `thermocouple_extension_compensating_wire_polarity` | HOLD | 보상도선 종류·극성·온도 범위·접점 구배 검토 필요 |
| `thermocouple_law_of_intermediate_metals` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `thermocouple_measures_temperature_difference` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `thermocouple_reference_junction_compensation` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `v_model_design_test_mapping` | PARTIAL | Registry 관계·조건에 한정; 의미/극성 근거 독립 검증 필요 |
| `valmet_control_valve_breakaway_friction_decreases_after_motion_starts` | HOLD | 제조사 모형과 비교 조건에서만 성립하는 한정 관계 |
