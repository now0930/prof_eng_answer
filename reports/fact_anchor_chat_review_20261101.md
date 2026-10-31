# Fact Anchor Chat 기술 검토 — 2026-11-01 (Batch A)

## 기준, 권한과 한계
- GitHub 기준선: `b8c6eba1aff51fc4203955a859b844574f487a4b`.
- 원본: `reports/fact_verification_progress_20261030.md`, `remaining_fact_current_queue_20261030.csv`, `grading/evidence/approved_fact_registry.json`.
- 원본 Registry 1,520건, 현행 미검토 Queue 1,290건(기존 첫 배치 20건 포함). 최초 1,272건 재검토 스냅샷의 제거 2·유지 5·미확인 1,265 기록은 **수정하지 않는다**.
- **AI 기술 검토**이며 사람 승인, 표준 전체 열람, Registry `verified` 갱신 또는 채점/생성물 갱신이 아니다. `score_effect=none`은 Topic Pack Core/Logic의 영향이 없다는 뜻이 아니다.
- `GENERAL_VERIFIED`: 출처의 명시적 범위 또는 재현 가능한 식을 대조한 항목. `SCOPE_KEEP`: 특정 제도·제품 범위에서 사실이며 보편 정답으로 사용 금지. `NARROW_OR_CORRECT`: 기술적으로 지나치게 단정적인 문구 수정 필요. `HOLD`: 추가 근거 또는 적용범위 검증 필요.
- 이 Batch는 **기존 첫 배치 20건의 독립적인 후속 검토 기록**이다. 출처 본문을 새로 대조하지 못한 행은 선행 보고서 판단에 근거한 `PRELIMINARY`로 기록해 새 근거 검증으로 계산하지 않는다.

## 첫 배치 20건 — 기존 판정의 채점 경계 재검토

| # | Fact ID | 권고 | 근거 및 확인 범위 |
|---:|---|---|---|
| 1 | `four_to_twenty_milliamp_repair_requires_end_to_end_reverification` | HOLD / 문구 축소 | 루프 복구 후 저·중·고 3점 + 경보 시험이 모든 설비의 일률적 의무임을 확정하지 않음. 기기/현장 시험계획 우선; Emerson Rosemount 8750W §6.8, Rockwell 엔지니어링 스케일링 자료는 제품 사례. |
| 2 | `balance_seal_resistance_is_actuator_load` | SCOPE_KEEP | Fisher HP/HPA Bore Seal과 착좌 저항의 관계. 해당 제품의 설계/구동력 산정에 한정. |
| 3 | `multiple_and_absent_stability_crossings` | GENERAL_VERIFIED | 여러 gain/phase crossing은 단일 경계로 축약 불가. crossing 부재에서 `Inf`와 `undefined`는 계산 도구 정의와 분석 범위에 따라 구분. MathWorks `margin` 설명. |
| 4 | `dod_sd22_dmsms_resolution_categories_and_complexity` | SCOPE_KEEP | DoD SD-22 Table 9의 단종 대응 분류. 산업 공통 필수 선택목록이 아님. |
| 5 | `chl_production_configuration_baseline_contents` | SCOPE_KEEP | NASA Product Baseline 정의. 모든 BOM 필드·서류 양식의 보편 의무 아님. |
| 6 | `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff` | GENERAL_VERIFIED | 입력 필터는 채터링 억제와 펄스 누락·지연의 상충관계. Hysteresis는 별도의 임계값 원리. Siemens S7-1200 디지털 입력 필터 자료. |
| 7 | `asset_maintenance_risk_prioritization_considers_likelihood_consequence_and_defined_criteria` | SCOPE_KEEP | ISO 31000의 가능성·결과 개념 및 ISO 55001의 자산 의사결정. 전 산업 동일 가중치 없음. |
| 8 | `control_range_is_declared_installed_gain_acceptance_interval` | SCOPE_KEEP | Fisher Sourcebook의 정규화 installed gain 0.5~2.0은 해당 책 기준이지 규격상 보편 합격선 아님. |
| 9 | `anti_cavitation_trim_does_not_prevent_application_defined_flashing` | GENERAL_VERIFIED | 하류압력 < 증기압 조건에서 지속 기화가 가능한 이상 Trim만으로 영구 기화를 없앨 수 없음. 운전점·유체·압력 확인. |
| 10 | `control_valve_installed_characteristic_field_validation_scope` | GENERAL_VERIFIED | 설치유량 특성은 계통 압력강하까지 포함. Stroke-only 시험과 설치유량특성 검증을 동일시하지 않음. |
| 11 | `control_valve_stiction_static_friction_can_cause_stick_jump_motion` | GENERAL_VERIFIED | Stiction은 지연 후 점프를 설명할 수 있으나 모든 움직임 문제의 유일 원인은 아님. |
| 12 | `control_valve_guide_function_and_transverse_load_wear_relevance` | SCOPE_KEEP | Ferrari의 2-inch globe-valve 실험 범위만 인정. 범용 마찰·변형 증가식 도출 금지. |
| 13 | `gas_equation_n_constant_depends_on_units_and_flow_form` | GENERAL_VERIFIED | 기체 sizing 수치상수는 식 형태·유량 기준·단위계에 의존. 적용 식과 상수 반드시 짝지음. |
| 14 | `control_valve_external_spl_depends_on_observation_and_environment` | GENERAL_VERIFIED | 외부 음압레벨은 관측 위치·환경에 의존. 음향파워레벨과 구별. |
| 15 | `conventional_4_20_ma_to_3_15_psi_linear_range_endpoints` | GENERAL_VERIFIED | 선형 보간 `P(psig)=3+12(I-4)/16`; 4/12/20 mA→3/9/15 psig. Split/역동작 제외. |
| 16 | `epa_method_21_type_ii_ambient_background_comparison` | SCOPE_KEEP | EPA Method 21 §8.3.2의 VOC 배경농도 측정·25 cm 제약. Seat Leakage 공통 규칙 아님. |
| 17 | `emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff` | SCOPE_KEEP | Emerson Handbook의 body material 선택 예시. 모든 부품·매질에 보편 동일 목록 적용 금지. |
| 18 | `cryogenic_control_valve_extension_bonnet_protects_packing_from_cold_zone` | NARROW_OR_CORRECT | 확실한 일반 원리는 packing/packing box의 저온 분리. Actuator 전체의 보호·vapor space 유무는 설계와 방향에 따름. |
| 19 | `control_valve_min_normal_max_flow_are_evaluated_separately` | NARROW_OR_CORRECT | 해당 프로젝트 설계조건에 최소·정상·최대 유량이 정의된 경우 개별 sizing. 모든 프로젝트에 정확히 3운전점을 강제하지 않음. |
| 20 | `cage_guides_plug_and_enables_flow_characterization` | SCOPE_KEEP | Fisher/Emerson cage 구조의 기능 설명. 이물·슬러리 허용성은 제품별로 확인. |

### 수정 후보 — 기존 Topic Pack 실제 Core Anchor 대조
- `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles/extended_bonnet_packing_isolation` (`core`): “Cryogenic extended bonnet은 주로 packing box를 저온 영역과 열적으로 분리하도록 설계한다. actuator 온도 영향, 필요한 길이·방향, 기상/단열 공간은 밸브별 설계·운전조건을 확인한다.” Registry만 아니라 `accepted_explanations` 및 연관 Logic/모범답안 검토 필요.
- 같은 Pack `operating_case_envelope` (`core`): 최소/정상/최대, 시동·정지·세정·이상운전은 **해당 설계기준에 적용되는 경우** 평가. 모든 설비에 고정 7개를 요구하지 않음.
- `control_valve_sizing_cv_kv_reynolds_liquid_selection/minimum_normal_maximum_sizing_points` (`core`): “설계기준에 규정된 각각의 유량·차압·밀도 운전점에 필요한 Cv/Kv를 검토한다. 최소·정상·최대는 대표 예시.”로 조정 권고.
- `configuration_change_release_backup_rollback_migration_obsolescence_management`의 `sw06_data_configuration_transformation_validation`, `sw06_migration_strategy_selection`, `sw06_cutover_freeze_gonogo` (`core`): HHS IT 가이드의 사례 암기가 아닌, 일반적인 데이터 무결성·전환 위험 검토의 원리 중심으로 채점. HHS 문구는 출처 표기한 보조 사례.
- 같은 Pack `sw06_obsolescence_mitigation_options`, `sw06_spare_lifecycle_management` (`important`): DoD SD-22 분류 및 NASA NPR 4100.1F Type I/II는 **기관 고유 사례**, 일반적인 필수 채점열거에서 제외 권고.
- 위의 모든 권고는 source와 generated를 직접 수정하거나 Core 중요도를 무조건 내리라는 뜻이 아니다. 해당 Topic 질문 요구축과 모범답안·Logic Check·Golden fixture를 먼저 대조해야 한다.

### 출처/검증 위치
- [MathWorks margin](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html), crossing 동작.
- [IEC 62382:2024 발행기관 개요](https://webstore.iec.ch/en/publication/67573), loop-check 범위와 프로젝트별 적용.
- [Emerson Fisher Control Valve Handbook 5E](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), cage style/actuator sizing/cryogenic.
- [Emerson Fisher HP/HPA manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf), pressure balance holes 및 Bore Seal.
- [DoD SD-22](https://www.nasa.gov/wp-content/uploads/2023/06/dmsms-guidebook-sd-22-jan2016-tagged.pdf), Table 9.
- [EPA Method 21](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-60/appendix-Appendix%20A-7%20to%20Part%2060), §8.3.2.
- [NASA Product Baseline 용어](https://www.nasa.gov/reference/system-engineering-handbook-appendix/).
- [HHS EPLC Data Conversion Practices Guide](https://www.hhs.gov/sites/default/files/ocio/eplc/EPLC%20Archive%20Documents/30-Data%20Conversion/eplc_data_conversion_practices_guide.pdf), pp.1–3.
- [NIST calibration interval](https://www.nist.gov/calibrations/recommended-calibration-interval).
- 기타 선행 이력: `reports/remaining_fact_recheck_batch01_20261030.md`.

## 변경·회귀 경계
- 현행 registry, Topic Pack, generated, scoring contract는 변경하지 않음. 따라서 승인·delete·promote 기록 없음.
- 보고서 단독 GitHub commit. 로컬 `README.md` 및 `docs/operational_quality_checksheet.md` 미커밋 작업에 접근하지 않음.
- 로컬 집중 pytest, `validate-all`, `validate_release.sh`는 이 Chat의 GitHub 연결만으로 실행 불가. 성공으로 주장하지 않음.
- 운영 checkout `a77d29f`, 컨테이너에는 영향 없음.
