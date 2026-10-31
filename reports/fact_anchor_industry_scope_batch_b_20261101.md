# Fact Anchor 기술사 공통원리 적합성 검토 — Batch B (2026-11-01)

## 대상과 판정 범위

- 검토 기준: `codex/essay-boundary-calibration-20261028`, 원천 Registry `grading/evidence/approved_fact_registry.json` 1,520건. 이번 **추가 검토 38개 Fact ID**. Batch A 기존 20개와 중복 없음.
- 인용된 표준·공식 기술자료의 **접근 가능한 부분과 수학적/공학적 관계**를 검토했다. 공개되지 않은 표준 Annex 또는 제품 매뉴얼 전체를 읽었다고 주장하지 않는다.
- 사용자 원칙: *일반적으로 산업계에서 인정되는 원리, 공개 표준의 적용 범위, 재현 가능한 물리식*을 기술사 **필수 채점 Fact**로 우선 인정한다. 제품의 포트 수·튜빙 인치·특정 튜닝 코드·실험 수치는 제품문맥 사실일 수 있으나 범용 필수 답안에서 제거한다.
- `GENERAL_KEEP` = 일반원리 채점 후보, `STANDARD_SCOPE_KEEP` = 표준의 명시된 적용범위에서만 채점 후보, `HOLD_ANNEX_DETAIL` = 부속서 문구 미재확인으로 보류, `REMOVE_GENERIC_CORE` = 제품 고유 세부를 일반 채점 Fact에서 제외 권고, `GENERALIZE_PRODUCT_CASE` = 일반원리로 치환하고 제품 사례는 보조 설명으로 이동 권고.
- 총계: GENERAL_KEEP 24 · STANDARD_SCOPE_KEEP 2 · HOLD_ANNEX_DETAIL 2 · REMOVE_GENERIC_CORE 5 · GENERALIZE_PRODUCT_CASE 5. **이 표는 Registry 승인 변경·삭제 완료 수가 아니다.** `verified`/source hash를 재승격하지 않고 score를 변경하지 않았다.

## Fact ID별 독립 판정

| # | fact_id | verdict | 기술사 채점 기준과 범위 | source key |
|---:|---|---|---|---|
| 1 | `hazop_lopa_ipl_definition` | `GENERAL_KEEP` | 독립·기능성·검증가능성은 일반적인 IPL 인정 요건 | CCPS |
| 2 | `hazop_lopa_ipl_independence` | `GENERAL_KEEP` | 원인사건/다른 IPL과 독립성 확보 | CCPS |
| 3 | `hazop_lopa_lopa_frequency_equation` | `GENERAL_KEEP` | 빈도×적용 조건부 확률×독립 IPL PFD; 독립성·시나리오 기준 명시 | CCPS |
| 4 | `hazop_lopa_required_rrf` | `GENERAL_KEEP` | 동일 결과·시간단위에서 잔여빈도/허용빈도의 무차원 비 | CCPS+DERIVATION |
| 5 | `hazop_lopa_pfdavg_rrf_relation` | `GENERAL_KEEP` | 저요구·독립 SIF 가정에서 PFDavg 목표≤1/RRF; 등식은 정의된 할당만 | HSE+DERIVATION |
| 6 | `hazop_lopa_sil_band_mapping` | `STANDARD_SCOPE_KEEP` | SIL1~3 저요구 PFDavg 구간을 IEC 61508/61511의 해당 모드에 한정 | IEC61508 |
| 7 | `hazop_lopa_target_vs_achieved_sil` | `GENERAL_KEEP` | LOPA 목표 할당과 SIF 설계·수명주기 실증은 별개의 검증 | HSE |
| 8 | `hazop_lopa_sif_allocation_boundary` | `GENERAL_KEEP` | Sensor/Logic/Final Element의 SIF 안전기능 경계와 안전상태·시간 설정 | HSE |
| 9 | `hazop_lopa_bpcs_ipl_credit` | `GENERAL_KEEP` | 원인 제공 BPCS의 동일 기능을 자동으로 독립 IPL로 중복계상 금지 | CCPS |
| 10 | `hazop_lopa_alarm_operator_ipl` | `GENERAL_KEEP` | 경보/운전원 대응은 독립성·기능·가용시간·절차·감사 가능성 확보 때만 | CCPS |
| 11 | `hazop_lopa_no_double_counting` | `GENERAL_KEEP` | 공유 센서·전원 등 종속 계층의 PFD를 독립 계층처럼 중복 곱하지 않음 | CCPS |
| 12 | `hazop_lopa_common_cause_dependency` | `GENERAL_KEEP` | 공통원인·공유자원은 독립 가정 이전에 반영 | CCPS |
| 13 | `hazop_lopa_enabling_and_conditional_modifiers` | `GENERAL_KEEP` | 시나리오에 실제 적용되는 조건부 확률만 사용; 모든 시나리오에 고정 항목 강제 금지 | CCPS |
| 14 | `hazop_lopa_hazop_role` | `GENERAL_KEEP` | HAZOP은 이탈·원인·결과·보호수단 분석이고 자체로 SIL 산출은 아님 | HSE+CCPS |
| 15 | `hazop_lopa_ipl_specificity` | `GENERAL_KEEP` | IPL은 특정 원인-결과 시나리오를 저감하는 기능이어야 함 | CCPS |
| 16 | `hazop_lopa_ipl_dependability_auditability` | `GENERAL_KEEP` | 독립성 이외에 성능·시험/정비·감사 가능성이 필요 | CCPS |
| 17 | `hazop_lopa_consequence_without_credited_protection` | `GENERAL_KEEP` | 보호계층 효과를 결과와 PFD에 이중 반영하는 순환 계산 금지 | CCPS+DERIVATION |
| 18 | `rtd_pt100_reference_resistance_alpha_standard` | `GENERAL_KEEP` | IEC 60751형 Pt100의 R(0°C)=100Ω, α≈0.00385/°C; 고유형별 값과 구분 | NI-RTD |
| 19 | `rtd_callendar_van_dusen_characteristic` | `GENERAL_KEEP` | 0°C 위·아래 C 항의 유무 및 계수·온도범위 조건을 명시 | NI-RTD |
| 20 | `thermocouple_reference_junction_compensation` | `GENERAL_KEEP` | 냉접점 온도를 측정해 등가 열기전력으로 보상; 단자 온도구배는 오차 | NI-CJC |
| 21 | `thermocouple_law_of_intermediate_temperatures` | `GENERAL_KEEP` | 동일 열전대·동일 기준에서 E(T1,T3)=E(T1,T2)+E(T2,T3) | NIST |
| 22 | `thermocouple_nonlinearity_reference_tables_polynomial_conversion` | `GENERAL_KEEP` | 열전대 종류별 NIST ITS-90 기준함수·표, 유효 온도범위 준수 | NIST-M175 |
| 23 | `thermocouple_measures_temperature_difference` | `GENERAL_KEEP` | 측정/기준접점 열기전력 관계와 기준접점 온도 필요성 | NI-CJC |
| 24 | `thermocouple_seebeck_effect_dissimilar_conductors` | `GENERAL_KEEP` | Seebeck 계수·온도의존성이 있는 열기전력; 종류별 비선형 | NIST-M175 |
| 25 | `iec62382_loop_check_exercises_individual_and_combined_loop_components` | `GENERAL_KEEP` | IEC 62382 §6.2.4: 전체 루프 구성요소 동작을 하나의 기능시험에서 확인 | IEC62382 |
| 26 | `iec62382_end_to_end_loop_check_is_not_sis_validation` | `STANDARD_SCOPE_KEEP` | IEC 62382 §5.2에서 SIS validation 제외; 안전기능은 IEC 61511 검증 별도 | IEC62382 |
| 27 | `iec62382_control_stroke_intermediate_points_and_hysteresis_checks` | `HOLD_ANNEX_DETAIL` | Annex A.4의 25/50/75% 구체 예시는 공개된 본문 확인 범위에서 재대조되지 않음. 보편 필수 시험점 인증 금지 | IEC62382 |
| 28 | `iec62382_actuator_failure_simulation_verifies_configured_reaction` | `HOLD_ANNEX_DETAIL` | Annex A.4 예시 항목은 본문 추가 대조 필요. 설계된 fail action 확인 자체는 타당 | IEC62382 |
| 29 | `fisher_2625_volume_booster_one_to_one_pressure_following` | `REMOVE_GENERIC_CORE` | 2625의 1:1 압력비는 제품 사양; Booster의 공압 유량·응답 기능으로 일반화 | EMERSON2625 |
| 30 | `fisher_3582_supply_medium_debris_and_connection_leak_controls` | `GENERALIZE_PRODUCT_CASE` | 청정 공급공기·누설 점검 원리는 유지; Fisher 3582 모델별 필터·점검 절차는 채점 제외 | REGISTRY_VENDOR |
| 31 | `actuator_bench_set_is_spring_adjustment_not_positioner_signal_travel_calibration` | `GENERALIZE_PRODUCT_CASE` | Bench set(스프링 초기압축)과 포지셔너 신호/Travel 교정의 구분은 유지; Fisher 657 설정값 암기 제외 | REGISTRY_VENDOR |
| 32 | `fisher_handbook_reports_direction_specific_valve_response_time` | `REMOVE_GENERIC_CORE` | Valve A Td 0.25/0.50s, T63 0.34/0.74s는 특정 시험 예시; 방향별 응답 특성만 유지 | REGISTRY_VENDOR |
| 33 | `dvc6200_sis_relay_capacity_and_tubing_requirements_are_variant_specific` | `REMOVE_GENERIC_CORE` | DVC6200 모델별 3/8 in 및 High-Cv 릴레이 연결 규격은 일반 정답 아님; 유량·압력손실·충전시간 인과로 교체 | EMERSON-DVC |
| 34 | `dvc6200_sis_tuning_response_adjustment_is_assembly_specific` | `REMOVE_GENERIC_CORE` | DVC6200 C~M 튜닝셋 암기 금지; 응답속도·안정성·Overshoot의 상충관계로 교체 | EMERSON-DVC |
| 35 | `fisher_vbl_booster_bypass_separates_large_and_small_signal_operation` | `GENERALIZE_PRODUCT_CASE` | 큰 입력·작은 입력과 바이패스의 기능 원리는 유지 가능; VBL 고유 조정 절차는 보편 의무 아님 | REGISTRY_VENDOR |
| 36 | `fisher_multiport_selector_well_test_routing_scope` | `REMOVE_GENERIC_CORE` | 8 inlet/1 test/7 production 등 특정 제품 port 수는 범용 제어밸브 구조·선정 지식이 아님 | REGISTRY_VENDOR |
| 37 | `fisher_v500_eccentric_plug_cam_action_and_erosive_service_scope` | `GENERALIZE_PRODUCT_CASE` | 편심 회전으로 seat 접촉·마찰을 줄이는 원리는 유지; V500 제품의 유체 적합성을 보편화하지 않음 | REGISTRY_VENDOR |
| 38 | `fisher_positioner_feedback_and_actuator_linkage_lost_motion_are_distinct` | `GENERALIZE_PRODUCT_CASE` | Positioner feedback과 기계적 backlash 구분은 유지; 3660/1052 링크 세부형상 암기 제외 | REGISTRY_VENDOR |

## 기술 내용과 채점 정책 구분

1. CCPS는 LOPA에 대해 initiating event frequency와 독립 IPL의 PFD를 결합하는 원리를 설명하고, 독립성·기능·무결성·신뢰성·감사가능성을 IPL의 핵심 속성으로 둔다. 조건부 modifier는 시나리오마다 필요한 경우에만 적용한다. `PFDavg`는 무차원 확률이며 `PFH`와 혼동하면 안 된다. 위험감소비는 같은 결과와 시간단위를 가진 빈도끼리 나눈 비다.
2. 열전대의 온도 중간법칙과 냉접점 보상, NIST ITS-90 열전대 종류별 함수는 **기본 물리적/계측적 Fact**로 남긴다. Pt100의 100Ω·α≈0.00385/°C와 Callendar–Van Dusen 적용 영역 역시 IEC 60751형 백금 RTD에 한정해 인정한다.
3. IEC 62382:2024 §6.2.4는 개별 루프 구성요소 및 통합 기능을 하나의 loop check에서 확인하도록 한다. §5.2는 SIS validation을 제외한다. 단지 **25/50/75% 또는 actuator fail simulation의 부속서 예시**가 있다는 이유만으로 전 산업 공통 필수 시험항목으로 승격할 수 없다. Annex A.4 원문 상세 재검증 전까지 예시의 정확한 locator는 보류한다.
4. Emerson의 DVC6200 SIS low-bleed/high-Cv 배관 치수는 제품 구성별로 달라 실제 매뉴얼에도 별도 규정돼 있다. Fisher 2625 1:1 ratio 역시 특정 booster 사양이다. 기술사 채점은 **압력/유량 용량, 충전·배기 시간, 안정성, 기계적 유격과 피드백의 차이**를 요구해야 한다.
5. Registry의 `score_effect=none`만 믿지 않는다. 위 제품별 주장 가운데 `pneumatic_supply_tubing_spool_capacity`, `positioner_gain_speed_stability_tradeoff`, `booster_pressure_follower_boundary`, `opening_closing_response_asymmetry`는 실제 Topic Pack에서 `core` 또는 `important`이다. Anchor뿐 아니라 `accepted_explanations`, Model Answer, Logic Check, required_anchor_ids 및 Golden 사례를 묶어 변경할 것.
6. `REMOVE_GENERIC_CORE`는 제품 설명이 사실이 아니라는 뜻이 **아니다**. 해당 사실을 보편적 필수 정답/결정론적 채점 근거에서 제외하고, 제품명·사양이 질문에 명시된 경우에만 제품별 사례로 활용한다는 의미다. 일반원리를 잃지 않도록 대체 Anchor 존재를 확인해야 한다.

## 근거 URL, 실제 확인범위

- **CCPS**: https://ccps.aiche.org/resources/tools/lopa
- **HSE**: https://www.hse.gov.uk/eci/functional.htm
- **IEC61508**: https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTA4LTF7ZWQyLjB9Yi5wZGY
- **NI-RTD**: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1rnCAA
- **NI-CJC**: https://www.ni.com/en/support/documentation/supplemental/17/specifications-explained--c-series-modules.html
- **NIST**: https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nbsir85-3133.pdf
- **NIST-M175**: https://www.nist.gov/publications/temperature-electromotive-force-reference-functions-and-tables-letter-designated
- **IEC62382**: https://standards.iteh.ai/catalog/standards/iec/5291b36b-42cb-4a25-a904-223b73437ad5/iec-62382-2024
- **EMERSON2625**: https://www.emerson.kr/ko/final-control/products/fisher-2625
- **EMERSON-DVC**: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf
- **REGISTRY_VENDOR**: source URL in the unchanged approved_fact_registry.json; product-specific scope only

- 주요 공개 대조: CCPS LOPA 페이지의 IPL 독립성과 빈도 결합 정의, HSE 기능안전 수명주기 개요, NI RTD 표준 곡선 및 CJC 기술자료, NIST ITS-90 자료 개요, IEC 62382:2024 공개 §5.2·§6.2.4, Emerson DVC6200 SIS 공식 매뉴얼의 Relay Connections 표.
- `REGISTRY_VENDOR` 표기는 Registry가 기재한 제조사 원문 링크를 식별한 것이며, 이번 Chat에서 그 원문 전체의 문장과 일치함을 재확인한 의미가 아니다. 따라서 `GENERALIZE_PRODUCT_CASE`는 채점 범위 개선 제안이지 기술 사실의 신규 `verified` 승인 아님.

## 현행 잔여 업무와 안전경계

- 기존 1,272건 스냅샷의 **2 제거·5 대조 유지·1,265 미확인** 수치를 소급 변경하지 않는다. 현행 `remaining_fact_current_queue_20261030.csv`에는 첫 배치 포함 1,290개 미검토 Fact ID가 있고 Batch A(20) + Batch B(38)가 판정 메모 대상으로 다뤄졌지만, **공식 Registry 완료 카운터로 합산하지 않는다**.
- 모든 Registry 행의 `verification_status=verified`는 **기존 승인 이력**으로만 간주한다. 이번 독립 검토 여부를 반영하는 신규 상태가 아니다.
- GitHub에 **검토 문서만 기록**. Registry, Topic Pack, generated bank, scoring, deployment **변경 없음**. GitHub 연결만으로 로컬 `validate-all`, `validate_release.sh`, Golden/pytest를 실행하지 못하므로 실행 성공을 주장하지 않는다.
- 실제 수정은 해당 Pack의 source+model answer+logic와 Registry를 함께 수정하고 source-hash·CLI 생성·focused tests·all release/validate-all을 통과하는 별도 stage에서 반영한다. 사용자 미커밋 README·운영 checksheet를 보존하고 운영 checkout/컨테이너는 건드리지 않는다.
