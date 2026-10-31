# Fact Anchor 제어이론/수식 기술 검토 — Batch E (2026-11-01)

## 입력과 분류

- 브랜치 `codex/essay-boundary-calibration-20261028`; 현행 Queue의 Routh, Nyquist, Bode, Root Locus, Lead/Lag, State Space, LQR **82개 원문 Fact ID 개별 점검**.
- 분류: CONDITIONED_CORE 12; CORE_EQUATION 63; ENGINEERING_JUDGMENT 6; SUPPLEMENT_ONLY 1. Batch A/기존 최초 판정에서 언급된 5개를 재검토하였으므로 보수적으로 신규 77개로 계산.
- `CORE_EQUATION`: 명시된 수학 모델·조건에 따른 일반 물리/대수 관계; `CONDITIONED_CORE`: 근사·수치·모드 조건이 성립해야 함; `ENGINEERING_JUDGMENT`: 성능·현장 적용 판단이므로 단일 정답 수치나 필수 체크리스트로 강제 금지; `SUPPLEMENT_ONLY`: 일반 시험의 필수 채점 지식이 아닌 설계 휴리스틱.
- 모델/수치점검은 독립 외부문서로 완전 인증했다는 의미가 아님. 실제 종속성·특이점·구간을 다루는 원식은 MathWorks·MIT·대학 강의 자료와 교차 점검. 수식 소급 조건은 Registry 원문/conditions 필드가 계속 적용된다.

## 원문 ID별 기술/채점 판정

| Fact ID | 판정 | 기술적 판정 경계 |
|---|---|---|
| `second_order_margin_damping_overshoot_bandwidth_trend` | `CONDITIONED_CORE` | ζ≈PM/100·Overshoot·Bandwidth는 지배2차 근사이며 보편 실험법칙이 아님 |
| `delay_and_nonminimum_phase_design_limits` | `CONDITIONED_CORE` | 지연 위상 −ωτ는 정확; RHP 영점의 위상·대역폭 영향은 모델과 성능 목표 의존 |
| `sensitivity_complementary_sensitivity_tradeoff` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `bode_decibel_and_log_frequency_properties` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `positive_gain_bode_magnitude_phase_effect` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `phase_margin_at_gain_crossover` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `gain_margin_at_phase_crossover` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `multiple_and_absent_stability_crossings` | `CORE_EQUATION` | LTI 주파수응답의 dB·위상·여유 식, 교차점 다중성·운전점 가정 |
| `nyquist_minus_one_critical_point` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `nyquist_contour_and_mapping` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `argument_principle_pnz_relation` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `open_loop_rhp_poles_count` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `stable_open_loop_special_case` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `imaginary_axis_pole_indentation` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `gain_margin_definition` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `phase_margin_definition` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `multiple_crossover_interpretation` | `CORE_EQUATION` | 표준 음의 피드백·기준점 −1·정해진 Nyquist 경로 방향·극점 우회 조건 |
| `routh_asymptotic_stability_open_lhp` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_first_column_sign_changes_rhp_count` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_positive_coefficients_not_sufficient` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_first_two_rows_layout` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_zero_first_column_epsilon_limit` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_all_zero_row_auxiliary_polynomial` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_imaginary_axis_roots_stability_class` | `CONDITIONED_CORE` | 중복/단순 허수축 극과 다른 극의 위치·Jordan 형태를 함께 확인 |
| `routh_gain_range_first_column_inequalities` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_gain_boundary_requires_verification` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `routh_time_delay_requires_approximation_or_frequency_method` | `CONDITIONED_CORE` | 지연을 근사했을 때 근사차수/정확도 및 정확한 Nyquist 판별의 차이 |
| `routh_does_not_return_exact_pole_locations` | `CORE_EQUATION` | 유한차수 실계수 LTI 특성다항식, 정규화·경계 특수행을 명시한 Routh–Hurwitz 관계 |
| `root_locus_closed_loop_pole_gain_relationship` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_definition` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_start_end_points` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_real_axis_segment_rule` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_asymptote_centroid` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_breakaway_breakin_points` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_departure_and_arrival_angles` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_imaginary_axis_crossing` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_gain_from_magnitude_condition` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_angle_condition` | `CORE_EQUATION` | 고정 유리함수 개루프·양의 이득·표준 음의 피드백 근궤적 관계 |
| `root_locus_transient_response_mapping` | `CONDITIONED_CORE` | 2차 우세 극과 ζ·ωn의 관계는 해당 모델 조건에서만 |
| `state_space_transfer_function_and_nonunique_realization` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `root_locus_dominant_pole_design_approximation` | `CONDITIONED_CORE` | 고차 계에서 지배2차 가정과 비우세 극 영향 확인 |
| `state_feedback_changes_closed_loop_matrix_to_a_minus_bk` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `controllability_matrix_full_rank_is_lti_controllability_test` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `observability_matrix_full_rank_is_lti_observability_test` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `luenberger_observer_error_dynamics_are_a_minus_lc` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `transfer_function_poles_are_reachable_observable_modes` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `pbh_controllability_and_continuous_time_stabilizability` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `pbh_observability_and_continuous_time_detectability` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `controllable_pair_permits_arbitrary_state_feedback_pole_assignment` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `ackermann_formula_siso_controllability_and_conditioning_caveat` | `CONDITIONED_CORE` | SISO 가제어성에서 계산 가능하나 수치 조건수 나쁘면 직접 계산은 불안정 |
| `observer_based_feedback_separation_principle_pole_union` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `state_feedback_pole_placement_does_not_set_tracking_dc_gain` | `CORE_EQUATION` | 유한차원 연속시간 LTI의 대수 관계, rank 조건 및 명시된 출력/입력 행렬 |
| `lead_compensator_maximum_phase_and_alpha_relation` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lead_compensator_maximum_phase_frequency_and_gain` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lag_compensator_pole_zero_order_and_low_high_frequency_gain` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lag_compensator_reduces_finite_step_error_without_changing_type` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lag_compensator_phase_loss_requires_crossover_recheck` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lag_compensator_dc_to_high_frequency_gain_ratio` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lead_and_lag_sections_shape_transient_and_steady_state_differently` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `root_locus_and_frequency_response_are_views_of_same_loop_transfer` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `compensator_cascades_with_plant_to_shape_loop_response` | `CORE_EQUATION` | 명시된 Lead/Lag 전달함수와 α,β,T>0의 유한차수 LTI 모델 관계 |
| `lead_design_phase_margin_procedure_requires_iterative_recheck` | `ENGINEERING_JUDGMENT` | 표준 설계 절차 중 하나이며 고정 Step 목록은 필수 암기 조건 아님 |
| `continuous_time_lqr_quadratic_cost_state_and_effort` | `CORE_EQUATION` | 선형 시스템, Q⪰0,R≻0 및 stabilizing Riccati 해의 가정에 따른 수학 관계 |
| `continuous_time_lqr_care_and_stabilizing_solution` | `CORE_EQUATION` | 선형 시스템, Q⪰0,R≻0 및 stabilizing Riccati 해의 가정에 따른 수학 관계 |
| `continuous_time_lqr_gain_and_closed_loop_poles` | `CORE_EQUATION` | 선형 시스템, Q⪰0,R≻0 및 stabilizing Riccati 해의 가정에 따른 수학 관계 |
| `lqr_stabilizing_care_existence_conditions` | `CORE_EQUATION` | Q⪰0,R≻0, Stabilizability 및 Detectability 가정에서 Stabilizing CARE |
| `bryson_rule_is_initial_normalization_heuristic` | `SUPPLEMENT_ONLY` | Bryson Rule의 가중치 초기화는 휴리스틱, 보편 최적 결과나 필수 선정법 아님 |
| `lqr_cost_optimization_indirectly_determines_closed_loop_poles` | `CORE_EQUATION` | CARE 최적 K로 폐루프 극이 결정, 직접 Pole Placement와 구별 |
| `unconstrained_standard_lqr_penalty_does_not_enforce_hard_limits` | `CORE_EQUATION` | 선형 시스템, Q⪰0,R≻0 및 stabilizing Riccati 해의 가정에 따른 수학 관계 |
| `continuous_and_discrete_lqr_use_different_riccati_equations` | `CORE_EQUATION` | 선형 시스템, Q⪰0,R≻0 및 stabilizing Riccati 해의 가정에 따른 수학 관계 |
| `lqr_cost_detectability_is_distinct_from_observer_detectability` | `CORE_EQUATION` | LQR 비용의 (Q½,A) 검출가능성과 상태관측기의 (C,A)를 구분 |
| `lqr_q_state_weight_is_objective_not_monotonic_performance_guarantee` | `CONDITIONED_CORE` | Q 증가는 비용함수 가중치 변화일 뿐 개별 성능지표 단조 개선 보장하지 않음 |
| `lqr_r_weight_penalizes_effort_but_does_not_encode_actuator_limits` | `CONDITIONED_CORE` | R은 입력 비용을 가중하지만 Hard Limit을 제약하지 않음 |
| `lqr_tracking_prefilter_and_lqi_have_distinct_conditions` | `CONDITIONED_CORE` | 적용 가능한 평형점·모델·적분확장 조건 확인 |
| `root_locus_target_outside_uncompensated_locus_requires_controller_dynamics_change` | `CORE_EQUATION` | 고정 개루프에서 스칼라 이득만 조절하면 근궤적 밖의 극점 배치 불가 |
| `nyquist_field_validation_separates_linear_margins_from_nonlinear_constraints` | `ENGINEERING_JUDGMENT` | 선형 여유로 비선형 제약·잡음·포화 안전을 인증하지 않음 |
| `state_space_pole_speed_requires_implementation_tradeoff_checks` | `ENGINEERING_JUDGMENT` | 빠른 극 배치가 곧 좋은 현장 성능이라는 보편 정리 아님 |
| `compensator_design_trades_crossover_margins_low_frequency_gain_and_noise_under_model_uncertainty` | `ENGINEERING_JUDGMENT` | Gain/Bandwidth/잡음/모델오차 상충은 판단 기준, 동일 설계 수치 강제 불가 |
| `lead_compensator_high_frequency_gain_noise_tradeoff` | `CONDITIONED_CORE` | 고주파 증폭 1/α와 잡음 영향은 센서 경로·롤오프에 따라 판단 |
| `routh_gain_interval_requires_robustness_and_feasibility_checks` | `ENGINEERING_JUDGMENT` | 명목상 수학적 안정과 실제 안정여유·제약을 분리 |
| `lead_lag_rhp_zero_and_delay_bandwidth_constraints` | `CONDITIONED_CORE` | RHP 영점·시간 지연의 제약 방향은 타당; 모든 경우 동일 Bandwidth 상한 공식 없음 |
| `lead_lag_validation_checks_follow_requirements_and_model` | `ENGINEERING_JUDGMENT` | Simulink 등 도구·점검항목은 개별 모델/요구사양에 따름 |

## 반드시 보존할 오류방지 조건

1. **Routh:** 계수 전부 양수는 충분조건이 아니다. 0행/첫열 0과 허수축 근·차수저하를 직접 검사. 지연 `e^{-Ls}`는 다항식 Routh로 직접 해결되지 않는다.
2. **Nyquist:** `N=P-Z` vs `N=Z-P`는 영상/경로의 시계·반시계 부호 정의에 따라 달라짐. 기준점 −1, 개루프 RHP 극 `P`와 전체 폐루프 불안정극 `Z`를 혼동 금지. 단일 crossover만으로 전체 winding 보증 불가.
3. **2차계 근사:** `ζ≈PM/100`, PM과 Over/Undershoot는 제한적 모델 근사. 시간지연·RHP 영점·고차 모드를 배제한 무조건 법칙으로 Fact 승격하지 않는다.
4. **Lead/Lag:** 같은 보상기 전달함수에서 극·영점 순서, 최대 위상 및 주파수와 고주파 노이즈 상충을 검증. Lag는 원점 적분기를 추가하지 않으므로 일반적으로 system type을 바꾸지 않는다.
5. **State Space:** 단순 전달함수만으로 비가제어·비가관측 내부모드의 안정성을 확인할 수 없다. Pole Placement는 가제어성 조건을 요구하며 Pre-filter는 적분 추종과 동일하지 않다.
6. **LQR:** CARE/DARE는 다르다. `u^TRu`는 입력의 크기를 벌점화할 뿐 입력 포화 제한을 강제하지 않는다. Bryson Rule은 초기 튜닝 경험칙이지 최적 결과의 정리가 아니다.

## 권위 자료 (본문 또는 공개 기술 설명)

- [MIT Electronic Feedback Systems, Routh criterion 자료](https://ocw.mit.edu/courses/res-6-010-electronic-feedback-systems-spring-2013/): 계수부호/첫열 부호변화 및 특수행.
- [MathWorks margin/allmargin, 교차점·여유](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html), [Stability Analysis](https://www.mathworks.com/help/control/stability-margins.html).
- [MathWorks Root Locus](https://www.mathworks.com/help/control/ref/dynamicsystem.rlocus.html), [Pole Placement](https://www.mathworks.com/help/control/getstart/pole-placement.html).
- [MathWorks LQR](https://www.mathworks.com/help/control/ref/lti.lqr.html), [CARE stabilizing solution](https://www.mathworks.com/help/control/ref/icare.html).
- [Washington University Nyquist sign convention](https://faculty.washington.edu/chx/teaching/fbintro/lec24-nyquist-criterion/), [Root locus angle condition](https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/).

## 보고서 효력

- 기존 `verified`, `score_effect`, Topic Pack, Logic, 모범답안, generated 변경하지 않음. 신규 Fact 재승인으로 카운트하지 않음.
- 실제 코어 수정/Anchor 삭제 시 해당 질문의 채점 요구와 테스트를 로컬에서 검증 후 CLI 생성·회귀 테스트 필요. 이 보고서 커밋만으로 release 게이트를 통과했다고 주장하지 않음.
