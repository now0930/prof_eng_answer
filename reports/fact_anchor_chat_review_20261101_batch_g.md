# Fact Anchor 액체/기체 제어밸브 Sizing — Batch G (2026-11-01)

## 범위·기준

- 작업 브랜치 `codex/essay-boundary-calibration-20261028`의 Queue에 있는 Cavitation/Flashing 33, Gas Sizing 33, Cv/Kv/Reynolds Liquid 29, **총 95개 Fact ID**를 기술사 공통원리·조건부 공인식·제품 고유 사례로 구분.
- 판정 집계: CORE_CONDITIONAL 20; CORE_PHYSICS 17; STANDARD_FORMULA 26; DUPLICATE_CANDIDATE 8; CORE_SUPPORTED 15; SUPPLEMENT_ONLY 6; CORRECT_REQUIRED 2; HOLD_SPECIFIC_STANDARD 1.
- `CORE_PHYSICS`/`CORE_SUPPORTED`는 물리 및 단위·유량 특성의 일반 사실. `CORE_CONDITIONAL`는 지정 운전·유체·형상 조건이 충족되어야 함. `STANDARD_FORMULA`는 IEC 60534/ISA 75의 해당 단상·유동영역 식에 한해서 유지하고 **모든 밸브의 필수 숫자 암기 항목으로 강제 금지**. `SUPPLEMENT_ONLY`/`DUPLICATE_CANDIDATE`는 채점 Core에서 분리·통합 권고. `HOLD_SPECIFIC_STANDARD`는 조항 전문 미확인.

## 개별 판정

| Fact ID | 권고 | 물리/적용 조건 및 중복/수정 사유 |
|---|---|---|
| `liquid_sizing_crosscheck_reuses_same_process_and_equation_basis` | `CORE_CONDITIONAL` | 교차 검산은 동일 운전조건·단위·보정계수 이용 |
| `liquid_valve_phase_change_pressures_are_absolute` | `CORE_PHYSICS` | P1/P2/Pv/Pc는 적용 온도·절대압 기준을 일치 |
| `liquid_valve_vapor_pressure_is_temperature_specific` | `CORE_PHYSICS` | 증기압은 온도의 함수; 동일 유체라도 운전 온도 달라지면 재계산 |
| `liquid_valve_pc_is_thermodynamic_critical_pressure` | `STANDARD_FORMULA` | Pc와 FL 기호의 정의가 다름. 실제 IEC/Fisher 방정식 문맥 |
| `control_valve_vena_contracta_is_minimum_flow_area` | `CORE_PHYSICS` | Vena contracta는 축소 유동의 최소 제트 단면 |
| `sub_vapor_pressure_at_vena_contracta_forms_vapor` | `CORE_PHYSICS` | 국소 정압이 증기압보다 낮으면 기포가 형성될 수 있음 |
| `control_valve_pressure_recovers_after_vena_contracta` | `CORE_PHYSICS` | 축소부 하류 일부 압력 회복과 비가역 손실을 구별 |
| `liquid_valve_choked_flow_is_limited_maximum_capacity` | `CORE_PHYSICS` | Choking은 유량 한계이지 유량 0이 아님 |
| `cavitation_requires_vapor_formation_and_pressure_recovery` | `CORE_PHYSICS` | Cavitation의 국소 기화 및 후속 압력회복·붕괴 과정 |
| `flashing_persists_when_outlet_pressure_below_vapor_pressure` | `CORE_PHYSICS` | P2<Pv에서 하류 증기상이 지속되는 Flashing 원리 |
| `cavitation_and_flashing_share_local_vapor_formation` | `CORE_PHYSICS` | 두 현상 모두 국소 기화를 공유하나 하류 기포 지속 여부가 다름 |
| `fisher_fl_is_rated_liquid_pressure_recovery_factor` | `STANDARD_FORMULA` | FL는 밸브별 pressure recovery 지표, 유체의 고유 물성으로 오인 금지 |
| `liquid_critical_pressure_ratio_factor_ff_depends_on_pv_pc` | `STANDARD_FORMULA` | FF=0.96−0.28√(Pv/Pc)의 단상 유체·적용 모델 한정 |
| `bare_valve_liquid_choked_pressure_drop_limit` | `STANDARD_FORMULA` | ΔPmax=FL²(P1−FF·Pv)는 특정 IEC sizing 모델·무부착 Fitting 조건 |
| `fp_corrects_attached_piping_fitting_effect` | `STANDARD_FORMULA` | FP는 직접 연결된 reducer·fitting 보정, 임의 원거리 배관손실 보정이 아님 |
| `flp_combines_valve_and_attached_fitting_recovery` | `STANDARD_FORMULA` | FLP의 의미 및 FP와 결합되는 범위를 함께 확인 |
| `fitting_adjusted_liquid_choked_pressure_drop_limit` | `STANDARD_FORMULA` | (FLP/FP)²(P1−FF·Pv) 조건부 식; Fitting 없는 식과 혼용 금지 |
| `liquid_sizing_uses_actual_or_choked_limit_whichever_is_lower` | `STANDARD_FORMULA` | ΔPsizing은 실제·허용 Choked Drop 중 작은 값 |
| `liquid_choked_flow_remains_finite_nonzero_capacity` | `DUPLICATE_CANDIDATE` | liquid_valve_choked_flow_is_limited_maximum_capacity와 사실상 동일 원리 |
| `persistent_flashing_can_erode_downstream_valve_surfaces` | `CORE_CONDITIONAL` | Flashing 유동의 침식은 조건부, 모든 Flashing이 동일 손상률은 아님 |
| `choked_flow_vaporization_and_damage_are_distinct_assessments` | `CORE_SUPPORTED` | Choked 유량·기화 발생·손상 정도는 별개 척도 |
| `raising_downstream_pressure_can_raise_vena_pressure_conditionally` | `CORE_CONDITIONAL` | Backpressure 조절이 도움이 되는 것은 특정 운전점/유체/밸브 기하에서 |
| `multistage_trim_can_limit_per_stage_pressure_drop_conditionally` | `CORE_CONDITIONAL` | 다단 Trim의 단계별 감압은 적용조건에서 기화를 제한할 수 있음 |
| `higher_fl_lower_recovery_may_reduce_cavitation_susceptibility` | `CORE_CONDITIONAL` | 높은 FL이 저회복과 관련된 비교를 보장하는 것은 동일 비교조건에서 |
| `anti_cavitation_trim_does_not_prevent_application_defined_flashing` | `CORE_PHYSICS` | Flashing 조건 P2<Pv는 Trim 자체로 없앨 수 없음 |
| `cavitation_trim_effectiveness_can_change_with_travel_and_geometry` | `SUPPLEMENT_ONLY` | Trim Travel 변화에 따른 Stage 유동특성은 제품별 상세 |
| `lower_temperature_reduces_water_vapor_pressure_at_fixed_composition` | `CORE_PHYSICS` | 물 포화증기압은 통상 온도 상승 시 증가, 온도 저하시 감소; 상평형 적용 |
| `liquid_valve_phase_change_pressure_variables` | `DUPLICATE_CANDIDATE` | 이미 개별 P1/P2/Pv/Pc/FL/FF Fact와 중복, 별도 가점 최소화 |
| `lower_liquid_recovery_factor_increases_cavitation_susceptibility` | `DUPLICATE_CANDIDATE` | higher_fl_lower_recovery...의 반대 표현; 동일 비교 원리로 묶기 |
| `backpressure_reduces_vena_contracta_cavitation_risk_conditionally` | `DUPLICATE_CANDIDATE` | raising_downstream_pressure...와 동일 현상, 별도 필수 가점 금지 |
| `cavitation_onset_and_damage_coefficients_are_valve_specific` | `SUPPLEMENT_ONLY` | Fisher Ki/Kc는 제조사 특정 선정법에서의 상세 계수 |
| `control_valve_phase_change_service_case_scope` | `CORE_CONDITIONAL` | 적용 설계운전점 기준; 최소/정상/최대 3가지 무조건 강제 금지 |
| `control_valve_flashing_damage_mitigation_is_application_specific` | `SUPPLEMENT_ONLY` | 유로 형상·내식/내마모 선정은 프로젝트별; 특정 Trim 구조를 보편화 금지 |
| `control_valve_liquid_sizing_vendor_result_independent_crosscheck` | `CORE_CONDITIONAL` | Vendor Cv/Sizing 결과를 동일 입력·단위·적용식으로 검산; 모든 상세 변수의 필수 암기 요구 금지 |
| `gas_sizing_flow_bases_and_equation_forms_are_distinct` | `CORE_SUPPORTED` | 질량·표준체적 유량 기준을 혼동하지 않음 |
| `gas_standard_volume_basis_has_explicit_reference_conditions` | `CORE_SUPPORTED` | Standard와 Normal 기준 온도·압력을 반드시 명시, 60°F/14.7 psia는 사례 |
| `gas_sizing_uses_absolute_pressure_and_temperature` | `CORE_PHYSICS` | 절대 압력·절대 온도 입력 필요 |
| `gas_pressure_drop_ratio_uses_upstream_absolute_pressure` | `STANDARD_FORMULA` | x=(P1−P2)/P1, 절대 P1 기준 무차원 |
| `gas_specific_heat_factor_is_gamma_over_1_4` | `STANDARD_FORMULA` | Fγ=γ/1.4는 해당 제어밸브 sizing 규약 |
| `gas_attached_fittings_modify_fp_and_choked_ratio_factor` | `STANDARD_FORMULA` | Fitting 존재시 FP·xTP를 밸브 단독 xT와 구별 |
| `gas_choked_limit_caps_sizing_ratio_and_expansion_factor` | `STANDARD_FORMULA` | Xchoked와 Expansion Y의 적용 단상/유동범위 조건 확인 |
| `gas_expansion_factor_accounts_for_compressible_expansion` | `STANDARD_FORMULA` | Y는 기체 팽창 효과, 표준모델 Choke에서 2/3 |
| `gas_choking_limits_flow_increase_from_further_downstream_reduction` | `CORE_PHYSICS` | Choked는 고정 상류조건에서 하류압 저하에 대한 유량 한계 |
| `gas_equation_n_constant_depends_on_units_and_flow_form` | `CORE_SUPPORTED` | N 상수는 단위·유량형태에 의존 |
| `gas_required_cv_iteration_uses_selected_product_xt` | `SUPPLEMENT_ONLY` | 특정 Trim xT를 사용한 제조사 반복 sizing 세부 절차 |
| `control_valve_cv_us_unit_reference_definition` | `CORE_SUPPORTED` | Cv는 60°F 물·1psi·US gpm 기준의 표준 Capacity |
| `control_valve_required_cv_inverse_sqrt_pressure_drop` | `CORE_CONDITIONAL` | 같은 유량·밀도, 비초크 난류식 내에서 Cv∝1/√ΔP |
| `control_valve_sizing_pressure_drop_operating_point_boundary` | `CORE_PHYSICS` | 정의된 운전점 실제 Valve 차압과 계통 Available 차압 구별 |
| `control_valve_basic_liquid_flow_coefficient_relation` | `CORE_PHYSICS` | 비초크 난류 단상 Q∝Cv√(ΔP/SG) |
| `control_valve_basic_liquid_equation_applicability_boundary` | `CORE_SUPPORTED` | 고점도·Cavitation·Flashing·Choked·비뉴턴/2상 유동 조건은 추가식 |
| `control_valve_gas_sizing_uses_absolute_upstream_temperature` | `DUPLICATE_CANDIDATE` | gas_sizing_uses_absolute_pressure_and_temperature와 중복 |
| `control_valve_gas_pressure_drop_ratio_increases_as_downstream_pressure_falls` | `DUPLICATE_CANDIDATE` | gas_pressure_drop_ratio...의 x식에서 바로 도출 |
| `control_valve_gas_choked_flow_is_a_nonzero_limiting_flow_condition` | `DUPLICATE_CANDIDATE` | gas_choking_limits_flow...와 동일 원리 |
| `control_valve_gas_choked_flow_does_not_increase_with_further_downstream_pressure_reduction` | `DUPLICATE_CANDIDATE` | gas_choking_limits_flow...와 동일 원리 |
| `control_valve_xt_is_bare_valve_choked_pressure_drop_ratio_parameter` | `STANDARD_FORMULA` | xT 제품/Travel별 공칭 계수; 모든 Trim 동일 수치 아님 |
| `control_valve_xtp_adjusts_choked_pressure_drop_ratio_for_attached_fittings` | `STANDARD_FORMULA` | xTP는 부착 Fitting 포함 보정 |
| `control_valve_gas_sizing_no_attached_fittings_sets_fp_one_and_xtp_equal_xt` | `STANDARD_FORMULA` | Fitting 미부착 조건 FP=1,xTP=xT |
| `control_valve_gas_choked_pressure_ratio_limit_uses_specific_heat_factor_and_xt` | `STANDARD_FORMULA` | xchoked=FγxT 또는 FγxTP 적용조건 |
| `control_valve_gas_sizing_y_expansion_factor_subcritical_relation` | `STANDARD_FORMULA` | Y=1−x/(3FγxT) 계열의 유효 범위에서만 |
| `control_valve_gas_sizing_y_bounds_are_one_to_two_thirds_at_choke` | `STANDARD_FORMULA` | 해당 Expansion Model에서 Y∈[2/3,1] |
| `control_valve_gas_subcritical_flow_rises_while_expansion_factor_falls_with_x` | `CORE_CONDITIONAL` | 일반 Subcritical Flow 사례. 물성·압력 등 조건 유지 시 |
| `control_valve_gas_standard_volume_equation_structure_uses_selected_gas_property_basis` | `STANDARD_FORMULA` | 표준 체적식의 T,Z,M/SG, 유량 기준 일치 |
| `control_valve_gas_mass_flow_density_equation_structure` | `STANDARD_FORMULA` | 질량유량식은 ρ1와 P1 및 x에 대한 지정식 사용 |
| `control_valve_gas_sizing_selects_property_input_by_equation_form` | `CORE_SUPPORTED` | ρ/M/SG 등은 선택 Sizing Form에 맞춰 적용 |
| `control_valve_compressible_sizing_scope_single_phase` | `CORE_CONDITIONAL` | 2상/다상 Steam·Gas에 단상 식 무조건 적용 금지 |
| `gas_sizing_xt_is_product_and_travel_specific` | `CORE_CONDITIONAL` | xT는 Valve·Trim·Travel·Flow 방향 등에 의존 |
| `gas_required_coefficient_differs_from_published_rated_capacity` | `CORE_SUPPORTED` | Required와 Rated Coefficient를 구별 |
| `gas_sizing_checks_defined_minimum_normal_maximum_cases` | `CORE_CONDITIONAL` | 프로젝트 설계 운전점 범위, 정확히 세 상태 의무 아님 |
| `gas_sizing_separates_single_phase_steam_from_wet_steam_case` | `CORE_CONDITIONAL` | Wet steam 2상은 단상 압축성 모델과 구분 |
| `gas_sizing_result_can_be_independently_reproduced_from_documented_inputs` | `CORE_CONDITIONAL` | 재현 가능한 입력/물성/제품계수·단위로 Vendor Sizing 대조 |
| `gas_sizing_outputs_feed_aerodynamic_noise_review` | `SUPPLEMENT_ONLY` | Gas Sizing과 Noise Calculation의 관계는 실무 주제, 특정 Noise 식 필수 아님 |
| `fail_open_gas_valve_flow_uses_credible_case_pressures_and_choke_check` | `CORE_CONDITIONAL` | Fail-open 시 동시 발생 가능한 압력·밸브 상태로 최대 유량 위험 검토 |
| `control_valve_cv_is_flow_capacity_not_travel_or_line_size` | `CORE_SUPPORTED` | Cv는 유량 용량계수, Travel/Line size와 동일 개념 아님 |
| `control_valve_cv_kv_conversion_is_approximate_unit_conversion` | `CORE_PHYSICS` | Kv≈0.865Cv, 정의된 기준수온·단위에서 환산 |
| `control_valve_sizing_equation_requires_consistent_units` | `CORE_SUPPORTED` | Cv/Kv 단위, 비중·ΔP·유량 일치 |
| `control_valve_fp_accounts_for_directly_attached_fittings` | `STANDARD_FORMULA` | Fp는 직접 부착 Fitting 보정 |
| `control_valve_fp_depends_on_valve_and_attached_geometry` | `CORE_CONDITIONAL` | Fp는 제조사·Trim/관경·부착 Geometry에 의존 |
| `iec_liquid_sizing_scope_excludes_complex_nonnewtonian_and_slurry_services` | `CORE_CONDITIONAL` | 비뉴턴/Slurry/다상에 IEC 단상 난류식 무조건 확대 금지 |
| `control_valve_nonturbulent_trigger_high_viscosity_low_flow_or_low_dp` | `CORE_PHYSICS` | 점도·유량·형상에 따라 Re 감소와 비난류 보정 필요 |
| `control_valve_selection_fr_below_one_increases_required_cv` | `STANDARD_FORMULA` | FR<1이면 동일 유량에 필요한 Cv가 증가, 유효 보정범위 확인 |
| `control_valve_fr_depends_on_reynolds_and_valve_style_inputs` | `STANDARD_FORMULA` | FR는 Re·밸브 스타일별 정의; 보편상수 아님 |
| `control_valve_selection_repeats_after_selected_style_fl_update` | `SUPPLEMENT_ONLY` | 선정/계수 반복 수렴 절차는 방법/모델별 |
| `control_valve_required_and_rated_coefficients_are_distinct` | `CORE_SUPPORTED` | 요구 Cv와 Rated Cv의 구분 |
| `control_valve_body_size_and_trim_capacity_are_not_identical` | `CORE_SUPPORTED` | Body Size 같아도 Trim 용량 다를 수 있음 |
| `control_valve_min_normal_max_flow_are_evaluated_separately` | `CORRECT_REQUIRED` | 원문 ‘세 상태를 각각 계산해야 한다’는 무조건 의무로 확대되므로 적용 운전점이 지정된 경우로 수정 |
| `control_valve_required_capacity_maps_through_selected_characteristic_to_travel` | `CORE_CONDITIONAL` | 요구 Cv를 Trim 고유특성과 Travel에 대응, Installed ΔP의 변화를 별도 고려 |
| `control_valve_oversizing_can_reduce_low_flow_control_performance` | `CORE_CONDITIONAL` | 과대용량에 의한 저 개도·Gain/Resolution 문제는 조건부 |
| `kv_reference_definition_is_water_flow_at_one_bar_with_source_specific_temperature` | `CORE_SUPPORTED` | Kv는 규정된 기준 수온·물, 1bar 차압, m³/h 유량 |
| `liquid_valve_sizing_requires_process_fluid_and_operating_case_inputs` | `CORRECT_REQUIRED` | 필요한 입력 종류는 설계 운전점/액체 유동영역별. 모든 상황에 Pv,Pc,점도를 동시에 필수 강제 금지 |
| `control_valve_reynolds_equation_uses_style_and_passage_modifiers` | `STANDARD_FORMULA` | Valve Reynolds에는 기종별 형상계수 포함 |
| `control_valve_undersized_capacity_may_fail_maximum_flow_case` | `CORE_SUPPORTED` | 선정 계수 부족 시 요구 유량 실패 가능 |
| `liquid_sizing_screens_cavitation_flashing_and_choked_flow_with_pressure_data` | `CORE_CONDITIONAL` | 위험 조건/영역에서 Vapor Pressure·Choking 검토 필요 |
| `normal_control_valve_travel_target_is_application_specific` | `CORE_SUPPORTED` | 보편적인 정상 Travel 20–80% 같은 고정 합격구간 없음 |
| `control_valve_reynolds_correction_uses_separate_reduced_trim_relation` | `HOLD_SPECIFIC_STANDARD` | IEC 60534-2-1 Annex A.7·A.8의 0.016 절차는 유료 규격 조항 직접 대조 전 보류; 일반 기술사 필수 암기 아님 |
| `control_valve_sizing_uses_valve_specific_reynolds_equation` | `STANDARD_FORMULA` | IEC Valve Reynolds 공식의 geometry 요소·영역을 적용. 일반 배관 Reynolds로 대체 금지 |

## 반드시 지켜야 할 기술적 경계

- **Cavitation과 Flashing:** 둘 다 Vena Contracta 국소 기화 가능성. 하류 압력이 증기압을 회복하는 경우 기포 붕괴(Cavitation), 하류 증기상이 지속되는 경우 Flashing. `Choked`는 최대 Capacity 영역이며 유량이 0이라는 뜻이 아니다.
- **액체 Sizing:** 단상/난류/비초크 식과 `FL, FF, FP, FLP, FR`를 요구하는 영역을 구별하고 실제 온도에 해당하는 `Pv`, 절대압 `P1,P2,Pc`를 사용한다. 복잡한 Slurry/비뉴턴·다상유동에는 기본식 무조건 적용하지 않는다.
- **가스 Sizing:** `P1/P2/T1` 절대 기준, `x=ΔP/P1`, 제품별 `xT`와 Fitting 보정 `xTP`, 기체 물성 `γ,Z,M,ρ`, `Y`의 Choked 한계를 같은 공식 안에서 맞춰야 한다. kg/h와 Sm³/h, Nm³/h는 단위/기준 상태가 다르다.
- **제외/수정 후보:** `control_valve_min_normal_max_flow_are_evaluated_separately`는 원문이 보편적으로 '세 조건 필수'라고 되어 있으므로 적용 설계운전점에 한정하는 수정 필요. `control_valve_reynolds_correction_uses_separate_reduced_trim_relation`의 Annex 특정 분기값 0.016을 표준 전문 대조 없이 필수 Fact로 인증하지 않는다.
- **중복 채점:** `gas_choking_limits_flow_increase_from_further_downstream_reduction`와 `control_valve_gas_choked_flow_does_not_increase_with_further_downstream_pressure_reduction` 등의 의미상 중복은 하나의 채점 요구축으로 통합할 후보. 실제 결합·삭제는 테스트 필요.

## 공개·권위 자료와 확인 한계

- [ISA 75 공식 표준 범위](https://www.isa.org/standards-and-publications/isa-standards/isa-75-standards): ANSI/ISA 75.01.01의 설치조건 액체/기체, 비난류/난류, Fitting 보정 범위 확인.
- [ISA 75.01 담당 위원회](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa75-01).
- [Emerson/Fisher Control Valve Handbook](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valve-handbook): 액체/기체 Cv·Choking·FL/xT 선정의 제조사 기술자료.
- [IEC 60534-2-1:2011 공개 기술 미리보기](https://www.iteh.eu/catalog/standards/sist/a3615b03-2b10-4d43-a04a-8af5c430bb33/sist-en-60534-2-1-2011): 단상 난류·비난류 구분, 압축성 표준식 일부와 조건. **전문 조항이나 최신 개정판까지 확인했다는 주장은 하지 않음**.
- [같은 표준의 압축성 가스 및 액체 차압 한계 공개 Preview](https://www.iteh.us/catalog/standards/clc/fb99dc2d-5586-4a83-89d6-f5df428e8d92/en-60534-2-1-2011): `xchoked`, `Fγ`, `FLP/FP` 및 `FF` 등 공개된 식 범위 확인.

## 효력·회귀 경계

- 이 파일은 Source Fact/Topic Pack/Logic/Generated를 **바꾸지 않은 기술 검토 기록**이다. 기존 `verified`나 Queue 수치에서 자동 제외하지 않는다. 표준의 특정 Annex 문장을 직접 인증하지 않은 항목은 Hold가 유지된다.
- 사용자 미커밋 자료, main, 운영 checkout/컨테이너 불변. 로컬 CLI·pytest·release gate·validate-all 미실행.
