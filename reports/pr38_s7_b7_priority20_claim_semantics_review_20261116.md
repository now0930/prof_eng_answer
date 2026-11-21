# PR #38 — S7 B7 우선 20개 Fact의 의미·조건·오인식 반례 검토 (2026-11-16)

> **판정: 20/20 HOLD; 새 Alias 승인 0건.** 이 문서는 위험도가 겹치는 18개 범용 Predicate 후보 + 11개 수식/방향성 위험 후보에서 중복 9건을 제외한 20개를 대상으로 한다. 사전에 사용자 승인된 verified Fact를 새로운 Ontology lexical ID 또는 채점 가능한 relation으로 **자동 승인하는 문서가 아니다**.

## 입력 및 검증 기준

- 실제 근거: [GitHub Actions #43857497079](https://github.com/now0930/prof_eng_answer/actions/runs/43857497079) / 검증 커밋 `ed8713d9121c7d899ebb7e0dafea55b61dc0c545`. 1,811 pytest passed / 2 skipped / 0 failed; S7 `REPRODUCED_BASELINE` 47 graded / 1 expected abstain / 179 missing / `score_admission=DISABLED`.
- `s7-alias-inventory` (ID 14222962043)와 `s7-alias-source-review` (ID 14222787692)의 실제 179 투영 / 119 승인 Registry Fact 원문·verification_refs·relations 비교 입력.
- **원인**: 179/179 `ID_NOT_FOUND`. 실제 parser Ontology에 해당 ID가 없으므로, 기존 동일 ID의 `aliases`만 고치는 작업으로 처리할 수 없음. `is/equals/maps/counts` 등의 너무 넓은 alias는 오인정 위험.
- 원문 대조 범위: 공공 기관·제조사·대학이 공개한 **HTML 원문 직접 교차확인 10/20개**, 일부 PDF는 검색 발췌만, 나머지는 Registry가 보존한 근거 메타데이터만 확인함. **원문 직접 교차확인도 신규 어휘/Claim-Fact 정확도 승인과는 별개.**
- 입력의 `verification_refs`는 기존 Registry Fact의 출처 메타데이터일 뿐이다. 이전 Golden 답안 원문은 열거나 기록하지 않았으며 새 점수 산출은 하지 않음.

## 20개 고유 Topic–Fact 검토 레코드 (Source ID·잠정 표현·반례·판정)

1. **`effective_unbalanced_area`** — Topic: `balanced_trim_unbalanced_trim_structure_sealing_applications`; Registry source Fact: `control_valve_effective_unbalance_area_definition`
   - 검토용 조건부 의미 문구(새 Alias 아님): 등가 순압력 작용 투영면적(실제 밸브 구조·압력장 조건부)
   - 반드시 거부할 오인정 반례: 어떤 구성에서도 공칭 시트 면적과 반드시 같다
   - 원문 대조 범위: Emerson handbook 색인 발췌; 전체 PDF 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

2. **`unbalanced_force_equation`** — Topic: `balanced_trim_unbalanced_trim_structure_sealing_applications`; Registry source Fact: `balanced_trim_unbalance_force_equation`
   - 검토용 조건부 의미 문구(새 Alias 아님): 정적 기준에서 F_u=ΔP×A_u (힘 크기, 일치하는 단위)
   - 반드시 거부할 오인정 반례: F_u=ΔP/A_u, 혹은 부호·유로 방향을 무시한 일반화
   - 원문 대조 범위: Emerson handbook 색인 발췌; 전체 PDF 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

3. **`sw06_baseline_approved_reference`** — Topic: `configuration_change_release_backup_rollback_migration_obsolescence_management`; Registry source Fact: `configuration_baseline_is_approved_point_in_time_reference`
   - 검토용 조건부 의미 문구(새 Alias 아님): 정식 검토·합의된 특정 시점의 형상 기준정보
   - 반드시 거부할 오인정 반례: 최신 파일이면 모두 승인된 베이스라인
   - 원문 대조 범위: NIST SP 800-171r3 03.04.01 HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

4. **`deadband_definition_direction_reversal`** — Topic: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`; Registry source Fact: `control_valve_deadband_is_reversal_input_interval_without_observed_output_change`
   - 검토용 조건부 의미 문구(새 Alias 아님): 입력 방향 반전 후 출력 변화가 관찰되지 않는 입력 범위
   - 반드시 거부할 오인정 반례: 일반 지연시간/필터·분해능만 있어도 기계적 데드밴드로 판단
   - 원문 대조 범위: Registry ISA 근거 메타데이터만 확인; 추가 독립 출처 요구
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

5. **`single_port_globe_throttling_structure`** — Topic: `control_valve_types_globe_rotary_body_actuator_selection`; Registry source Fact: `single_port_globe_uses_one_seat_ring`
   - 검토용 조건부 의미 문구(새 Alias 아님): single-port globe body의 한 개 시트링과 직선 운동 폐쇄부
   - 반드시 거부할 오인정 반례: 모든 globe/balanced/double-port valve를 single port로 분류
   - 원문 대조 범위: Emerson handbook 색인 발췌; 전체 PDF 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

6. **`safe_state_process_hazard_basis`** — Topic: `final_control_element_sil_sis_esd_valve_partial_stroke_test`; Registry source Fact: `final_element_safe_action_process_dependent`
   - 검토용 조건부 의미 문구(새 Alias 아님): 특정 공정 위험·안전요구에 따라 정해지는 보호 동작
   - 반드시 거부할 오인정 반례: 모든 공정에서 fail-close가 안전, 또는 fail-open이 항상 안전
   - 원문 대조 범위: HSE Control systems §Dependence on utilities HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

7. **`hazop_lopa_pfdavg_rrf_relation`** — Topic: `hazop_lopa_ipl_risk_reduction_sil_target_allocation`; Registry source Fact: `hazop_lopa_pfdavg_rrf_relation`
   - 검토용 조건부 의미 문구(새 Alias 아님): 저요구·동일 사건 기준 PFDavg_target≤1/RRF_required
   - 반드시 거부할 오인정 반례: 부등호 반전, 실현된 PFD를 목표 PFD로 오인
   - 원문 대조 범위: Registry 기술근거 메타데이터 + 자체 차원/부등식 검토; 외부 원문 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

8. **`hazop_lopa_required_rrf`** — Topic: `hazop_lopa_ipl_risk_reduction_sil_target_allocation`; Registry source Fact: `hazop_lopa_required_rrf`
   - 검토용 조건부 의미 문구(새 Alias 아님): 동일 사건·시간 기준 RRF_required=F_residual/F_tolerable
   - 반드시 거부할 오인정 반례: 분자·분모 반전, 서로 다른 결과 사건 빈도끼리 나눔
   - 원문 대조 범위: Registry 기술근거 메타데이터 + 자체 비율 검토; 외부 원문 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

9. **`rh_temperature_dependence`** — Topic: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`; Registry source Fact: `relative_humidity_varies_with_temperature_at_fixed_vapor_pressure`
   - 검토용 조건부 의미 문구(새 Alias 아님): 수증기 분압 일정할 때 T↑→포화수증기압↑→RH↓
   - 반드시 거부할 오인정 반례: 압력이 변하거나 수증기 유입/응축해도 무조건 T↑이면 RH↓
   - 원문 대조 범위: Vaisala RH 정의·Pws(T) HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

10. **`sw04_v_model_definition`** — Topic: `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`; Registry source Fact: `v_model_design_test_mapping`
   - 검토용 조건부 의미 문구(새 Alias 아님): 요구·설계 단계와 대응 검증·확인 시험 단계의 추적관계
   - 반드시 거부할 오인정 반례: 단순히 아무 두 공정이 '매핑'되면 V-Model이라고 인정
   - 원문 대조 범위: CMU SEI Using V Models for Testing HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

11. **`argument_principle_pnz_relation`** — Topic: `nyquist_stability_criterion_gain_phase_margin`; Registry source Fact: `argument_principle_pnz_relation`
   - 검토용 조건부 의미 문구(새 Alias 아님): 우반평면 등고선·시계방향 양수 규약 N_cw=Z−P; Z=P+N_cw
   - 반드시 거부할 오인정 반례: 시계방향 양수인데 N_cw=P−Z라고 작성
   - 원문 대조 범위: UW Nyquist Lecture 24 HTML 직접 대조; CCW 양수 N_ccw=P−Z의 부호전환
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

12. **`closed_loop_rhp_poles_count`** — Topic: `nyquist_stability_criterion_gain_phase_margin`; Registry source Fact: `closed_loop_rhp_poles_count`
   - 검토용 조건부 의미 문구(새 Alias 아님): 표준 음의 피드백·비모형화 상쇄 없음에서 Z=#RHP zero(1+L)=#폐루프 불안정 극
   - 반드시 거부할 오인정 반례: Z를 L(s) 자체의 우반평면 영점 수로 대체
   - 원문 대조 범위: UW Nyquist Lecture 24 HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

13. **`nyquist_contour_and_mapping`** — Topic: `nyquist_stability_criterion_gain_phase_margin`; Registry source Fact: `nyquist_contour_and_mapping`
   - 검토용 조건부 의미 문구(새 Alias 아님): RHP를 둘러싼 s-평면 경로를 L(s)로 복소평면에 사상
   - 반드시 거부할 오인정 반례: s-평면 윤곽선 자체와 L(s) Nyquist 궤적을 동일 객체로 주장
   - 원문 대조 범위: UW Nyquist Lecture 24 HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

14. **`open_loop_rhp_poles_count`** — Topic: `nyquist_stability_criterion_gain_phase_margin`; Registry source Fact: `open_loop_rhp_poles_count`
   - 검토용 조건부 의미 문구(새 Alias 아님): 중복도 포함 L(s) 열린 우반평면 극점 수 P
   - 반드시 거부할 오인정 반례: 폐루프 극점 수 또는 좌반평면 극점 수를 P로 사용
   - 원문 대조 범위: UW Nyquist Lecture 24 HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

15. **`radar_pulse_time_of_flight`** — Topic: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`; Registry source Fact: `radar_pulse_round_trip_time_measurement`
   - 검토용 조건부 의미 문구(새 Alias 아님): FMR56/57 pulse-ToF에서 기준점~표면 거리 D=c×t_roundtrip/2
   - 반드시 거부할 오인정 반례: 모든 FMCW와 pulse radar가 동일 방식, 또는 D=ct
   - 원문 대조 범위: Endress+Hauser 기술정보 검색 발췌; 지정 판본 PDF 전체 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

16. **`rtd_four_wire_kelvin_measurement`** — Topic: `rtd_temperature_sensor_principle_pt100_wiring_compensation`; Registry source Fact: `rtd_four_wire_kelvin_measurement`
   - 검토용 조건부 의미 문구(새 Alias 아님): 전류 force 2선·고임피던스 voltage sense 2선으로 lead-drop 오차 축소
   - 반드시 거부할 오인정 반례: 2선식도 동일하게 제거, 또는 실제 리드저항이 0이 됨
   - 원문 대조 범위: NI 4-Wire Resistance Measurements HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

17. **`required_rrf_relation`** — Topic: `sil_target_determination_risk_reduction_and_lifecycle`; Registry source Fact: `sil_required_rrf_relation`
   - 검토용 조건부 의미 문구(새 Alias 아님): F_residual>F_tolerable이며 동일 결과/단위에서 RRF_required=F_residual/F_tolerable
   - 반드시 거부할 오인정 반례: F_tolerable/F_residual 또는 차원이 다른 빈도 비율
   - 원문 대조 범위: HSE 기술근거 메타데이터 + 자체 차원 검토; PDF 원문 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

18. **`residual_frequency_before_sif`** — Topic: `sil_target_determination_risk_reduction_and_lifecycle`; Registry source Fact: `sil_residual_frequency_before_sif`
   - 검토용 조건부 의미 문구(새 Alias 아님): 동일 사건에 기존 독립 IPL PFD·수정인자 × 개시사건 빈도로 SIF 이전 잔여빈도 산출
   - 반드시 거부할 오인정 반례: 비독립 IPL을 각각 100% 인정·같은 방호효과 이중 차감
   - 원문 대조 범위: AIChE RAST 원문 기술근거 메타데이터만; PDF 원문 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

19. **`target_pfd_relation`** — Topic: `sil_target_determination_risk_reduction_and_lifecycle`; Registry source Fact: `sil_target_pfd_relation`
   - 검토용 조건부 의미 문구(새 Alias 아님): 저요구 모드 PFDavg_target≤F_tolerable/F_residual=1/RRF_required
   - 반드시 거부할 오인정 반례: 부등호 반전·기준 사건 불일치·달성 SIL과 목표 설정 동치
   - 원문 대조 범위: HSE 기술근거 메타데이터 + 자체 부등식 검토; PDF 원문 미대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

20. **`thermocouple_measures_temperature_difference`** — Topic: `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`; Registry source Fact: `thermocouple_measures_temperature_difference`
   - 검토용 조건부 의미 문구(새 Alias 아님): 재질 쌍이 정해졌을 때 측정·기준 접점 온도 차에 연관된 기전력
   - 반드시 거부할 오인정 반례: 기준 접점 없이 기전력만으로 절대 접점온도를 직접 알 수 있다
   - 원문 대조 범위: NIST Mercury Thermometer Alternatives: Thermocouple HTML 직접 대조
   - **판정: HOLD** (새 ID 정의·기존 Ontology 충돌·부정/역방향 반례·조건 검증·Gold 독립 라벨 미충족)

## 직접 확인한 외부 HTML 원문 범위 (Fact 주장 근거 참고용)

- NIST SP 800-171 Rev. 3, §03.04.01 baseline configuration: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html
- HSE Control systems, §Dependence on utilities / safe-state actions: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
- Vaisala humidity definition and temperature-dependent saturation pressure: https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers
- CMU SEI Using V Models for Testing, 2013: https://www.sei.cmu.edu/blog/using-v-models-for-testing/
- University of Washington Lecture 24, Nyquist sign convention and argument principle: https://faculty.washington.edu/chx/teaching/fbintro/lec24-nyquist-criterion/
- NI 4-Wire Resistance Measurements, current and high-impedance sensing: https://www.ni.com/docs/en-US/bundle/ni-dmm/page/4-wire-resistance-measurements_2.html
- NIST thermocouple two-temperature reference relation: https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/mercury-thermometer-alternatives/mercury-thermometer-5

**미대조 원문**: Emerson·Endress+Hauser PDF는 검색/색인 발췌만, ISA·AIChE·HSE PDF 등은 Registry 근거 메타데이터만 확인. '대조 완료'로 승격하지 않는다. 원문 인용 대신 검토자 작성의 관계 검증/오인정 반례만 기록함.

## 개별 판정과 다음 게이트

1. **현재 판정: HOLD 20**, ACCEPT 0 / REVISE 0 / REJECT 0. 위 검토용 문구는 human-readable *candidate explanation*, parser가 사용할 수 있는 `aliases` 필드나 승인된 새 Ontology 정의가 아님.
2. **우선 결론**: 수학적/물리적 Fact 자체와 어휘 recognition, relation extraction, conditions checking, answer polarity 판단을 분리해야 함. 'Alias만 보강→EXACT_RELATION 증가→정확도 개선'은 성립하지 않음.
3. **승격 요건**: 각각의 새 Subject/Predicate/Object ID가 기존 Ontology와 중복/충돌하지 않는지, 새 Predicate의 역할·방향성·부등호를 formal semantics로 고정할 수 있는지, 적용 조건을 Claim에서 명시적으로 확인할 수 있는지, 최소 정상·반례 사례를 전문가 판정으로 검증할 것.
4. **다음 순서**: 20개 중 특히 Nyquist 4건, RRF/PFD 5건, V-model 1건, 4-wire RTD 1건의 *negative* claim fixtures를 **score-neutral** 독립 실험으로 만들고 false-positive를 측정. 검증 없는 Alias 자동 추가 금지. 나머지 99건은 차후 별도 ID별 검토.
5. **보호**: score_admission=DISABLED 유지, Original Registry/Topic Pack/Generated·A–E·Fatal/WRONG·Ceiling·합격선·SUPPORTED 상태 변경 금지. PR #38 Draft 유지, main 미병합·운영 미배포·서비스 재시작 없음.

**이번 HEAD 변경은 보고서 1개 추가만이며 코드/채점 관련 변경 없음. 이전 Actions 성공은 `ed8713d`의 실측으로만 명시하고 신규 보고서 HEAD에 대한 pytest를 이미 실행했다고 쓰지 않는다.**
