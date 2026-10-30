# 잔여 Fact 일반 원리 재검토 — 첫 배치 20건 (2026-10-30)

검토자: Codex (AI 자체 검토, 사람 승인 아님). 입력: [첫 배치 목록](remaining_fact_recheck_first_batch_20261030.csv), Registry SHA-256 `918a0b0c594929ab34068630311a54005df0dd9152ee36ac0d670022f3f450de`. 이 판정은 **일반 원리와 주장 범위의 1차 검토**다. 모든 인용문서의 해당 절을 독립적으로 완독했다는 뜻이 아니며, `GENERAL_PRINCIPLE_CONSISTENT`도 source-grounded 최종 `verified` 재승인이 아니다. 기존 운영 Fact 상태·점수는 변경하지 않는다.

| 번호 | Fact ID | 1차 판정 | 일반 원리/범위 판단 |
| ---: | --- | --- | --- |
| 1 | `four_to_twenty_milliamp_repair_requires_end_to_end_reverification` | GENERAL_PRINCIPLE_CONSISTENT | 수리 후 출력·입력 스케일·경보 경로를 설치 루프에서 확인하는 것은 타당한 실무 방식. 저·중·고 3점과 기록 방식은 모든 설비의 법적 의무로 일반화하지 않음. |
| 2 | `balance_seal_resistance_is_actuator_load` | GENERAL_PRINCIPLE_CONSISTENT | 해당 balance/bore seal 구조의 마찰·저항은 actuator 요구력에 영향을 줄 수 있음. seal 없는 밸브나 임의 구조로 확대하지 않음. |
| 3 | `multiple_and_absent_stability_crossings` | GENERAL_PRINCIPLE_CONSISTENT | 고전적 gain/phase margin은 해당 교차점의 정의와 탐색 주파수 범위에 의존. 교차점이 여러 개인 경우 하나만 전제하지 않는다는 취지는 타당함. 단, `infinite`와 `unavailable` 표기는 계산 도구·정의에 따라 구분. |
| 4 | `dod_sd22_dmsms_resolution_categories_and_complexity` | SOURCE_SCOPE_CHECK | DoD SD-22 Table 9의 단종 대응 분류 예시로는 타당. 모든 OT 설비의 필수 옵션 목록이 아님. 해당 taxonomy의 세부 범위만 인용. |
| 5 | `chl_production_configuration_baseline_contents` | SOURCE_SCOPE_CHECK | NASA의 product baseline 정의와 부합하는 설명. 모든 프로젝트의 BOM 필드 또는 단일 문서 형식을 정하는 보편 규칙으로 사용하지 않음. |
| 6 | `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff` | GENERAL_PRINCIPLE_CONSISTENT | 입력 필터가 짧은 pulse를 놓치거나 응답을 지연할 수 있다는 trade-off는 타당. Hysteresis는 임계값 왕복 chatter에 적용되는 별도 방법이며 모든 접점에 묶어 요구하지 않음. |
| 7 | `asset_maintenance_risk_prioritization_considers_likelihood_consequence_and_defined_criteria` | GENERAL_PRINCIPLE_CONSISTENT | 가능성·결과와 조직별 기준을 고려하는 원리는 타당. ISO 문서의 공개 설명만으로 개별 조항·가중치까지 확정하지 않음. |
| 8 | `control_range_is_declared_installed_gain_acceptance_interval` | SOURCE_SCOPE_CHECK | installed gain의 허용 구간은 선언된 기준으로 평가할 수 있음. 0.5~2.0은 Fisher Sourcebook 사례이며 보편 합격선으로 승격하지 않음. |
| 9 | `anti_cavitation_trim_does_not_prevent_application_defined_flashing` | GENERAL_PRINCIPLE_CONSISTENT | downstream 압력이 증기압 아래인 지속 기화 조건을 내부 trim만으로 제거할 수 없다는 원리와 부합. 각 운전점의 압력·온도와 설계 경계를 확인해야 함. |
| 10 | `control_valve_installed_characteristic_field_validation_scope` | GENERAL_PRINCIPLE_CONSISTENT | 실제 설치 특성은 밸브·계통 ΔP와 유량의 관계를 포함하므로 stroke-only 시험만으로 증명되지 않음. 전 유량곡선 현장시험은 보편 의무가 아님. |
| 11 | `control_valve_stiction_static_friction_can_cause_stick_jump_motion` | GENERAL_PRINCIPLE_CONSISTENT | 정지마찰에 따른 멈춤·갑작스러운 움직임은 가능한 양상. 모든 지연/급격한 움직임을 stiction으로 단정하지 않는 현 문구가 적절함. |
| 12 | `control_valve_guide_function_and_transverse_load_wear_relevance` | SOURCE_SCOPE_CHECK | guide 기능과 특정 실험에서 측정된 횡하중은 구별해야 함. 단일 globe-valve 실험을 모든 밸브의 마찰 증가식으로 일반화하지 않음. |
| 13 | `gas_equation_n_constant_depends_on_units_and_flow_form` | GENERAL_PRINCIPLE_CONSISTENT | 경험적/규격상 sizing 식의 숫자 상수는 단위계·식 형태에 의존한다는 차원 관계가 타당함. 특정 N값은 식·유량 기준을 함께 제시해야 함. |
| 14 | `control_valve_external_spl_depends_on_observation_and_environment` | GENERAL_PRINCIPLE_CONSISTENT | 외부 SPL은 관측 위치·방향·반사 환경에 의존하며 음향 power level과 구별됨. 고정 감쇠값을 주장하지 않음. |
| 15 | `conventional_4_20_ma_to_3_15_psi_linear_range_endpoints` | GENERAL_PRINCIPLE_CONSISTENT | 선형 사상 `P=3+12(I−4)/16`에서 4·12·20 mA → 3·9·15 psig가 정확함. split-range·역동작에는 적용하지 않음. |
| 16 | `epa_method_21_type_ii_ambient_background_comparison` | SOURCE_SCOPE_CHECK | EPA Method 21 Type II §8.3.2의 지역 배경 VOC 측정·25 cm 하한에 한정하면 맞음. seat leakage 시험 일반 규칙으로 확대하지 않음. |
| 17 | `emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff` | SOURCE_SCOPE_CHECK | Emerson Handbook의 body-material 선정 설명으로만 사용. 모든 부품·모든 유체의 보편 재질 체크리스트로 승격하지 않음. |
| 18 | `cryogenic_control_valve_extension_bonnet_protects_packing_from_cold_zone` | NARROW_OR_CORRECT | 확실한 일반 원리는 extended bonnet이 **packing 부위를** 극저온 유체로부터 열적으로 분리하는 것. 현재 문장의 ‘packing과 actuator’를 함께 보호한다고 읽힐 수 있어, actuator 보호 여부는 구체적 구조·열해석에 따른다고 좁히는 편이 안전함. |
| 19 | `control_valve_min_normal_max_flow_are_evaluated_separately` | GENERAL_PRINCIPLE_CONSISTENT | 설계 입력이 minimum/normal/maximum으로 주어진 경우 각 운전점의 required coefficient를 따로 산정하는 원리는 타당. 모든 프로젝트가 반드시 그 세 점만 요구한다는 뜻은 아님. |
| 20 | `cage_guides_plug_and_enables_flow_characterization` | SOURCE_SCOPE_CHECK | 문구가 Fisher/Emerson 특정 cage 구조로 범위를 한정한 점이 중요함. 입자 허용성과 trim 기능은 제품별 검토 사항이지 cage-guided 전체의 보편 성질이 아님. |

1차 집계: GENERAL_PRINCIPLE_CONSISTENT 12, SOURCE_SCOPE_CHECK 7, NARROW_OR_CORRECT 1. **최종 Fact 검증 완료 0건**. 따라서 다음 내용 확인 단계에서는 18번의 문구와 연결 Anchor부터 좁힌 뒤, 4·5·8·12·16·17·20번의 source-specific 범위가 채점 필수 Anchor로 과도하게 승격되지 않았는지 확인한다. 나머지 12건은 각 근거의 실제 위치 확인 후 `GENERAL_VERIFIED` 여부를 판단한다.

직접 대조한 공개 1차 근거: [MathWorks `margin` 설명](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html) (여러 crossing), [DoD SD-22 Table 9](https://www.nasa.gov/wp-content/uploads/2023/06/dmsms-guidebook-sd-22-jan2016-tagged.pdf) (resolution taxonomy), [NASA product baseline 용어](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), [Siemens S7-1200 입력 필터 설명](https://cache.industry.siemens.com/dl/files/829/109814829/att_1120874/v1/s71200_system_manual_en-US_en-US.pdf), [ISO 31000 공개 개요](https://www.iso.org/standard/65694.html), [ISO 55001 공개 개요](https://www.iso.org/standard/83054.html), [Fisher 846 I/P manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-846-current-to-pressure-transducers-en.pdf), [eCFR Method 21 §8.3.2](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-7%20to%20Part%2060), [Emerson 극저온 밸브의 packing 설명](https://www.emerson.com/en/final-control/products/vanessa-series-30000-cryogenic-powered-actuator). 이 목록에 없는 원문 절은 아직 직접 대조하지 않았다.
