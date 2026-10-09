# Topic Pack 문제 단위 재정리 — 전체 진행 현황

> 이 문서는 source 검토 당시의 이력이다. Stage 8/9의 과거 실패·미수행 상태와 82개 목록은 현재 상태가 아니다. 86개 운영 Pack의 최신 구조·View 감사 결과는 [전체 내용·View 연결 감사](topic_pack_content_completion_20261007.md)를 따른다.

갱신: 2026-10-07
기준 inventory: 2026-10-06 감사 manifest 82개
목적: 각 Pack을 출제 가능한 하나의 독립 문제 단위로 보고, 질문 요구-지식-Anchor-answer outline의 충분성과 경계를 정리한다. 기출·공식 출제분류라고 추정하지 않는다.

## 현재 진행 수

| 작업 단위 | 전체 | 완료/검토 | 잔여 | 판정 |
|---|---:|---:|---:|---|
| 기존 Pack 자동 구조·coverage screen | 82 | 82 | 0 | 완료. 자동 screen은 사람의 의미 검토나 내용 승인이 아님 |
| 주 구조/원자성 우선 상세검토 | 30 | 30 | 0 | PASS. 자동 경고 중 일부는 독립 문항군/owner 확인 필요로 보존 |
| 별도 coverage 연결 재검토군 | 10 | 10 | 0 | coverage triage 완료; 패턴별 적용범위 마지막 후보까지 검토 |
| 전체 우선 상세검토 신호 | 40 | 40 | 0 | **100% source-level screen/audit 완료**. 내용 승인·통합·release 승격은 별도 단계 |

80여 개를 동일한 수준으로 모두 재작성하는 계획이 아니다. 82개는 전수 screen이 끝났고,
후속은 구조 경고 30개와 primary coverage triage 10개를 먼저 의미 검토한다. 여기서도
자동 경고가 중첩되는 보조지표는 별도로 보고, 같은 Pack을 두 번 완료 수에 더하지 않는다.

## 상세 검토 완료 40건

1. `control_valve_positioner_ip_converter_booster_accessories_calibration` — 중심 문제 단위 및 10 pattern owner 검토
2. `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` — DP 문제군/분리 후보 검토
3. `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` — lifecycle/design/production verification 경계 검토
4. `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` — 문서/현장시험/인수 경계 검토
5. `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` — HMI/alarm/SOE/Trip ownership 검토
6. `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience` — 실시간 네트워크 문제군 검토
7. `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` — fieldbus/ethernet/무선 문제군 검토
8. `instrumentation_installation_wiring_impulse_tubing_inspection_codes` — 종합 field-installation workflow 판정; cable·impulse tubing·검사 세 family를 하위 패턴으로 연결하고 pattern별 평가범위를 명시
9. `instrumentation_power_grounding_shielding_ups_ground_loop_emc` — 전원·접지·차폐·EMC 경계 검토
10. `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` — 압력계측 원리·선정·오차 문제군 검토
11. `pid_controller_tuning_sequence_gain_effects` — coverage 60%에서 70%로 추적 보완; 미요구 PI/PD 배경을 필수 고득점 내용에서 분리
12. `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` — GWR 고유 4 Anchor가 기존 14 pattern에 연결되지 않는 scope/owner gap을 확인하고 managed GWR draft 생성
13. `routh_hurwitz_stability_criterion_gain_range` — 5 patterns의 공통 계산기법 problem unit은 유지; 질문별 optional/required Anchor·outline 추적 보완
14. `rtd_temperature_sensor_principle_pt100_wiring_compensation` — required-anchor union 71.4%; 3개 문제 패턴 경계를 정리하고 측정전류·자기발열 패턴에서 미요구 진단내용을 필수에서 제외
15. `sil_target_determination_risk_reduction_and_lifecycle` — required-anchor union 87.5%; SIL 결정·계산·방법비교·성능검증 4패턴의 누락 요구 보완 및 공통 채점문구 범위화
16. `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` — required-anchor union 84.6%; RBD 직렬·병렬 연결 보완, mode 설명과 무관한 근사식 필수요건 및 전역 공통채점 범위 축소
17. `bode_frequency_response_stability_margin_bandwidth` — 초기 required-anchor union 12/14(85.7%, screen 반올림 86%); crossover 차이 설명에 PM·GM 수치 계산까지 묶인 과잉요구를 해제하고, 원리·작도 패턴의 위상기여 누락과 outline의 Anchor 연결 공백을 보완
18. `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` — 초기 required-anchor union 24/28(85.7%, screen 반올림 86%); 10개 질문의 Anchor 연결은 목적에 맞아 유지하고, 전역 high-score/common-missing 및 importance unlock을 해당 패턴에서만 적용하도록 범위를 명시
19. `state_feedback_reference_tracking_prefilter_integral_action` — 초기 required-anchor union 12/14(85.7%, screen 반올림 86%); 극점배치·추종 구분을 개념/추종 패턴에, 강인성·노이즈 이득 trade-off를 검증 패턴에 추가하고 고득점·누락 기준을 질문별로 범위화
20. `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` — 13 patterns/33 anchors; explicit MC/DC hybrid pattern 12의 per-pattern anchor gap을 보완하고 outline을 33/33 연결, high-score/common-missing과 importance unlock을 pattern-scoped로 정리
21. `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` — 10개 대표 질문의 required Anchor union 25/27(92.6%); 원리 문항에 interference 연결, sensing 비교에서 불필요한 framework Anchor 제거, 고득점·누락·importance 기준을 패턴별로 한정하고 내부 planning tag를 공식 출제분류로 오인하지 않게 문서화
22. `configuration_change_release_backup_rollback_migration_obsolescence_management` — 11개 예상문항을 모두 직접 질문형으로 맞추고 39/40 Anchor required union, 40/40 outline 연결; 고득점·누락·major·importance 조건을 패턴별로 한정. 40 Anchor/11문항의 넓은 family boundary는 Router를 건드리지 않고 Stage 6 owner 검토에 이월
23. `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` — 10개 직접 질문형 패턴과 38/38 required Anchor union을 확인. 음향 기초(P1), 다중 소음원 계산(P2), 소음원리·저감·운전/측정(P3–P10) 3 family가 확인되어 불필요한 required Anchor 연결은 만들지 않고, scoring 범위와 topic 분리는 Stage 6 owner 검토에 이월
24. `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` — 10개 pattern의 required Anchor와 outline이 각각 48/48 연결됨을 확인. seat/class, 측정·환산, 원인진단, packing/emission 및 workflow의 내용을 pattern별 high-score/missing/importance 조건으로 제한; 48-anchor owner 분리 여부는 Stage 6에 이월
25. `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` — 12개 question intent를 각 demand에 맞게 수정하고, 재질/sealing 문항의 actuator-load Anchor 오연결을 온도·열과도 Anchor로 교정. High-score/common-missing/importance 적용범위를 pattern별로 제한하고 통합 절차 Pack owner는 유지
26. `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles` — 10개 intent를 문제별로 구체화하고 required Anchor union을 43/48에서 48/48로 보완. High-score/common-missing/importance를 해당 pattern에 한정; severe-service 응용 Pack으로 유지하고 48-Anchor ownership warning을 Stage 6에 이월
27. `final_control_element_sil_sis_esd_valve_partial_stroke_test` — 10개 intent를 개별 demand로 수정하고 두 orphan Anchor를 관련 pattern에 연결해 48/48 union 완성. PFD 계산과 PST/proof-test program 등 겹치는 범위를 구분하고 고득점·누락·중요도 조건을 pattern-scope화. Focused test는 57개 중 55 PASS, generated parity/manifest의 기존 두 이슈는 후속 integration에 이월
28. `lead_lag_compensator_phase_margin_steady_state_error` — 5개 question intent/example을 분명히 하고 전역 채점·중요도 기준을 패턴별로 적용. 14/14 Anchor union 유지. lead/lag generic alias의 Root Locus 중복과 3개 disconnected problem family는 routing을 손대지 않고 owner audit 대상으로 기록
29. `lqr_optimal_state_feedback_riccati_weighting_design` — 5개 문항 family를 분리해 고득점·누락·importance 기준을 pattern-scoped로 한정. Q/R 비교에 공통 배율 Anchor를 연결해 required union 14/14, outline 14/14 완성. 기준입력·LQI 이웃 Pack 및 4개 disconnected family 경고는 owner audit에 이월
30. `passive_sensor_resistive_capacitive_inductive_transduction` — strain gauge와 충돌한 alias를 제거하고 Gauge-factor Anchor를 optional 처리, 13/14 required·14/14 outline; 별도 검증 PASS
31. `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` — Sensor Fusion·State Estimation 문항을 Physical AI closed loop에 연결하고 30/30 union 완성
32. `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` — 11개 문항의 독립 요구군을 유지하며 누락 equipment/piping representation을 P2에 연결, 24/24 union
33. `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` — 14개 문항의 독립 요구군을 유지하고 20/20 Anchor 연결·feedback scope 보완
34. `root_locus_stability_gain_design` — 5개 intent/example을 정리하고 departure/arrival angle 누락 Anchor를 연결, 14/14 union·outline; lead/lag alias collision은 owner review로 이월
35. `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` — 12개 intent/example과 pattern-scoped 평가범위를 정리하고 33/33 union 확인; 6개 독립 question-family warning은 의도된 분리 신호로 보존
36. `smart_positioner_diagnostics_valve_signature_predictive_maintenance` — 10개 pattern의 high-score/missing/importance scope를 명시하고 44/44 union; large-inventory 경고는 owner review로 보존
37. `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` — 10개 문항 범위와 scoring scope를 명시하고 22/22 union; 4개 연결 component는 임의 결합하지 않고 owner review 신호로 기록
38. `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` — 13개 문항의 고득점·누락·importance scope를 한정하고 14/14 union; 독립 질문군 경고는 유지
39. `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization` — 세 intent 누락을 채우고 operating-range Anchor를 P1에 연결, 14/14 union; 잘못된 RTD 설명을 정정
40. `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` — 10개 intent와 40/40 Anchor union, pattern별 평가범위 보완; 8개 연결 component 및 large-inventory 경고는 Stage 6 owner review로 이월

근거 문서: `topic_pack_problem_unit_audit_20261006.md`,
`problem_unit_reconstruction_lead_lag_20261007.md`,
`problem_unit_reconstruction_final_element_sil_20261007.md`,
`problem_unit_reconstruction_severe_service_20261007.md`,
`problem_unit_reconstruction_valve_selection_20261007.md`,
`problem_unit_reconstruction_seat_leakage_20261007.md`,
`problem_unit_reconstruction_control_valve_noise_20261007.md`,
`problem_unit_reconstruction_positioner_20261006.md`,
`problem_unit_reconstruction_dp_level_20261006.md`,
`problem_unit_reconstruction_candidates_3to5_20261006.md`,
`problem_unit_audit_second_wave_comms_install_pressure_20261006.md`,
`problem_unit_reconstruction_pid_tuning_20261007.md`,
`problem_unit_reconstruction_radar_gwr_20261007.md`,
`problem_unit_reconstruction_routh_20261007.md`,
`problem_unit_reconstruction_rtd_20261007.md`,
`problem_unit_reconstruction_sil_target_20261007.md` 및 연결된 Topic Sheet.
`problem_unit_reconstruction_fsrm_20261007.md` 및 후속 설치 검토서 `problem_unit_reconstruction_installation_20261007.md`도 상세판정 근거에 포함.
`problem_unit_reconstruction_lqr_20261007.md`도 상세판정 근거에 포함.
이번 잔여 마감 근거: `problem_unit_reconstruction_passive_sensor_rcl_20261007.md`, `problem_unit_reconstruction_physical_ai_20261007.md`, `problem_unit_reconstruction_pid_piping_instrumentation_diagram_20261007.md`, `problem_unit_reconstruction_piezoelectric_20261007.md`, `problem_unit_reconstruction_root_locus_20261007.md`, `problem_unit_reconstruction_mcdc_structural_coverage_20261007.md`, `problem_unit_reconstruction_smart_positioner_20261007.md`, `problem_unit_reconstruction_speed_strain_thermistor_20261007.md`, `problem_unit_reconstruction_ot_cybersecurity_20261007.md`.
수동형 R·C·L과 Physical AI는 과거 별도 보충 작업으로 작성됐으나 각각 cross-topic alias/disconnected-family 우선 후보임을 재대조해 이번 40/40 마감 목록에 병합했다. 근거는 `problem_unit_reconstruction_passive_sensor_rcl_20261007.md`와 `problem_unit_reconstruction_physical_ai_20261007.md`다. LVDT/RVDT, Nyquist 및 광학·레이저는 screen상 잠정 유지 후보에 대한 별도 보충 검토이며 primary 30/coverage 10 카운터에는 포함하지 않는다. 원천 수정만 완료한 Pack의 generated projection은 integration 단계에서 일괄 검증·승격한다.

## 순차 작업 계획

| 단계 | 작업 | 상태 |
|---|---|---|
| 1 | 기준 inventory/82개 자동 screen과 판정 기준 확정 | PASS |
| 2 | 상위 구조 후보 1–5의 개별 문제 단위·owner 검토 | PASS (문서 검토; machine migration 일부 미수행) |
| 3 | 2차 후보 첫 배치 5개 상세 검토 | PASS (문서 검토) |
| 4 | coverage-only 후보 10개 중 낮은 coverage부터 대조 | PASS (10/10; source-level 검토 완료) |
| 5 | 선택 후보 source Pack·Topic Sheet를 문제 요구 기준으로 보완 | PASS (40개 screen/audit 대상의 source-level 검토 완료; 일부 reviewer draft는 미승격) |
| 6 | 중복 owner/Router, Grading·Training·Diagnosis View 영향 분석 | PASS WITH RETAINED WARNINGS (32 atomicity warnings; two generic lead/lag alias collisions preserved by routing-authority contract) |
| 7 | approved inventory / draft inventory와 generated manifest 간 계약 정리 | PASS (87 source = 82 active/generated + 5 draft; no draft promoted) |
| 8 | 영향있는 targeted tests, full regression/release validation | FAIL/REVIEW (selected scoped releases PASS; full non-promote suite has 1 deterministic requirement-count mismatch) |
| 9 | 커밋/push | NOT DONE; unrelated pre-existing worktree changes prevent a safe isolated commit; Stage 8 gate is not green |

## 현재 초안·검증 상태

- 새 `control_valve_pneumatic_accessories_function_application`은 9개 신규 고유 Fact Anchor를
  가진 managed `draft / human_review_required` 상태다. 기존 Positioner owner/routing은 아직
  그대로이며 이관·중복운영을 활성화하지 않았다.
- Topic Pack directories에는 기존 Chapter 20 drafts 3개와 새 공압 부속기기/GWR 초안 2개가 있다.
  전체 release `--all`은 이 다섯 팩의 사람 검토/승인 메타데이터가 없어 승격을 차단한다.
- 현재 `validate_topic_packs.py` 전체: 87 packs / 2,068 anchors PASS.
- 현재 전체 quality validator: 87 packs, errors 0 / warnings 28. Full atomicity: errors 0 / warnings 32이며 20 disconnected question-family, 10 large-inventory, 2 alias collision 경고는 별도 owner 검토 근거와 함께 유지한다.
- 이번 잔여 6 Pack의 scoped release validation은 모두 PASS했고 generated snapshot을 복원했다. 전체 `PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh`는 150개 테스트 중 1개 실패했다: `tests.test_mcdc_cross_topic_canonical_promotion`의 expected raw requirement count 13, actual 15. 이 작업은 deterministic scorer/Fact Anchor/fatal contract를 바꾸지 않았으므로 assertion을 우회하거나 점수 contract를 수정하지 않았다.
- Accessory, PID, GWR 각각의 scoped schema/quality/release validation PASS; 각 release 검증이
  임시 생성한 generated banks는 사전 snapshot으로 복원됐고 `rubrics/generated/` 변경은 없다.
- Routh scoped schema/quality/release validation PASS; Nyquist/Routh routing boundary 3 tests PASS.
  생성 bank는 release validator가 사전 snapshot으로 복원했다.
- RTD는 3개 expected pattern의 required-anchor union을 10/14로 재산정했다. 측정전류·
  자기발열·선정 패턴에 진단 anchor를 요구하던 과잉범위를 해제했고, global high-score /
  common-missing 조건에 pattern scope를 명시했다. Source schema, quality, generated-pipeline
  scoped release PASS; 상세 판정은 `problem_unit_reconstruction_rtd_20261007.md` 참조.
- SIL 목표 결정은 네 pattern의 required-anchor union을 14/16으로 재산정했다. 핵심 SIL
  결정문항에 시나리오·허용위험·IPL·잔여빈도·SIL band·proof test가 연결되지 않은 공백과,
  질문 유형을 가리지 않는 global high-score/common-missing 범위를 보완했다. Scoped schema,
  quality, generated-pipeline release PASS; SIL relation/requirement/operation/routing 관련 8개
  unit test와 MCDC SIL·SIS LOPA 과대채점 회귀 2개 PASS. 생성 rubric은 사전 snapshot으로 복원.
- FTA/Markov/RBD는 8개 pattern의 required-anchor union을 22/26으로 재산정했다. RBD 기본
  직렬·병렬 연결을 비교 문제에 추가하고 PFDavg/PFH 구분 문제의 불필요한 근사식 requirement를
  제거했다. 고득점·누락 평가를 pattern별로 제한했다. Scoped schema/quality/generated-pipeline
  release PASS; FSRM machine-contract/risk Golden, global risk coverage, deterministic-shadow,
  adjacent SIL routing test 19개 PASS. 생성 rubric은 사전 snapshot으로 복원.
- Bode는 crossover 차이 설명 pattern에서 PM·GM 수치 계산 requirement를 제거하고, 원리·작도
  pattern에 위상 기여 Anchor를 연결했다. 8개 outline에 Anchor 참조를 부여하고 고득점·누락
  기준과 중요도 unlock 조건을 대표 질문별로 범위화했다. 필수 Anchor union 초기 12/14
  (85.7%, 86% screen)에서 13/14 (92.9%)로 개선되며, 미연결 `margin_transient_response_approximation`은
  현재 대표 질문에 시간응답 설명을 직접 요구하는 pattern이 없어 선택 지식으로 유지했다. 이는
  source contract와 문서의 명료화이며 grader runtime이 패턴별 점수 게이팅을 한다는 주장은 아니다.
- 제어논리 SW-02는 10개 대표 질문과 28개 Anchor 중 24개 required union 연결(85.7%)을 확인했다.
  나머지 4개는 SW-03/SW-05 ownership 경계와 Entry/Exit 상세처럼 메타 또는 선택 지식이라
  억지로 필수화하지 않았다. 대표 질문별 required anchors는 유지하되 16개 high-score와 14개
  common-missing, 중요도 unlock 조건을 pattern-scoped로 고쳤다. Outline은 기존대로 28개 전체
  Anchor를 연결한다. Focused SW-02 regression 27 tests, source schema/quality (0 warning),
  atomicity (0 warning), scoped generated release 모두 PASS; runtime 점수 게이팅 변경은 없다.
- 상태피드백 추종은 5개 패턴과 14개 Anchor를 대조했다. 기존 미연결이던 극점 배치와
  정상상태 추종의 구분은 패턴 1의 질문 의도에, 강인성·노이즈 이득 trade-off는 검증항목을 묻는
  패턴 5에 직접 부합하므로 required anchors에 각각 연결했다. 이에 14/14 required union으로
  완성했다. `high_score_points`, `common_missing_points`, importance unlock과 Topic Sheet를
  5개 패턴별로 명시해 `N_r` 유도·integral augmentation·observer 검증을 모든 답안에 동시에
  요구하지 않게 했다. Runtime scoring은 변경하지 않았다.
- SW-04는 13개 question pattern, 33개 Anchor, 29/33 required union(87.9%)을 확인했다.
  Pattern 12는 질문문에 MC/DC를 명시하지만 required list에 MC/DC ownership 및 V-Model이 SIL을
  보장하지 않는 경계 Anchor가 없어 해당 패턴에만 추가했다. 8개 outline의 Anchor trace도 기존
  32/33에서 33/33으로 연결했다. 전역 high-score/common-missing 및 9개 unlock 조건을 pattern별로
  한정하고 stale README 수량(31 anchors/10 patterns)을 수정했다. Pattern 13의 `routing_exclusive`
  차단조건과 기존 Router/Golden은 유지했다. 13번의 일반 SIL 검증 범위를 안전 lifecycle로
  확대하지 않았다. Focused regression, 2개 overgrading fixture, source schema/quality/atomicity와
  scoped release 검증 결과는 별도 audit note에 기록한다.
- 계측설비 설치 Pack은 기존 구조 우선검토 #8의 후속으로 세 disconnected pattern family를
  하나의 타당한 field-installation workflow에 연결했다. Pattern 1 범위를 보강해 atomicity
  audit PASS/warnings 0, pattern-scoped score/missing 기준 적용. Dedicated installation,
  power/grounding boundary, environmental adjacent tests PASS; scoped release PASS. 기존 empty
  deterministic topic aliases 품질경고 1건은 변경하지 않았다. 이 Pack은 기존 #8에 포함되어
  이번 40건 중복 집계 방지를 위해 완료 수를 변경하지 않음.
- Positioner 전용 Router/semantic 테스트는 PASS; 기존 focused script는 generated manifest
  82개와 현재 source directories 87개의 일치 assertion에서 FAIL한다. 초안 5개를 포함할지
  운영 기준 inventory만 비교할지 검사 계약을 바로잡아야 한다. 테스트 자체는 우회·변경하지
  않았다.
- PID 수정은 expected question 문구, 점수 가중치, fatal IDs, Question Type, routing,
  deterministic scoring을 변경하지 않았다. 새 내용은 pattern/outline Anchor 연결과
  필수/선택 배경 경계를 명시했다.
- 아직 commit 또는 push하지 않았다. Full release gate가 통과하지 않고 worktree에 사용자의
  다른 미커밋 수정도 있어 unrelated content를 함께 확정하지 않는다.
- SW-06은 focused regression 42 tests와 source/scoped release 검증을 수행한다. 상세내용, 40-Anchor warning 및 source 판본상태는 `problem_unit_reconstruction_sw06_20261007.md`에 기록한다.
- 제어밸브 통합 선정 Pack의 source/schema/quality/scoped release는 PASS했으나, 기존 focused regression 65개 중 63개만 PASS했다. 실패 1건은 known 87-source/82-manifest inventory mismatch이고, 나머지 1건은 source 변경 후 generated importance가 사전 snapshot에 남은 parity mismatch다. 이를 숨기거나 우회하지 않았으며, generated projection integration에서 재빌드 후 다시 검증해야 한다. 상세 판정은 `problem_unit_reconstruction_valve_selection_20261007.md`.

## 다음 작업

source-level 우선 상세검토 40/40을 마쳤다(주 구조/원자성 30/30, coverage triage 10/10). 이 수치는 문제 단위·Anchor·평가기준을 읽고 조정한 비율이지 내용의 기술적 승인이나 generated bank 승격을 뜻하지 않는다. Stage 6–7 inventory/owner 계약을 완료했으며, 다음은 Stage 8 회귀 실패 원인의 검토다. Full release regression이 green이 아니므로 promote·commit·push는 보류한다.

보충 감사를 포함한 구조·coverage triage 40개는 모두 source-level 검토됐다. 이전에 별도 보충 기록으로만 관리하던 Passive Sensor, Physical AI, P&ID, Piezoelectric, Root Locus는 본래 screen backlog의 30건 안에 있었으므로 이번에 정식 완료 목록에 병합했다. 별도 non-inventory 감사(예: LVDT/RVDT, Nyquist, Optical)는 중복 집계하지 않는다. Stage 6 audit은 32개 경고를 오류 없이 판정했고 2개 generic alias collision은 기존 routing 권한 보존을 위해 남겼다. Stage 7은 source 87=active/generated 82+draft 5 inventory 계약을 확인했다. GWR와 공압 액세서리 등 다섯 managed draft는 사람 검토/승인 전이므로 승격하지 않는다. Stage 8 전체 비승격 회귀는 기존 MC/DC cross-topic canonical promotion 테스트에서 `raw_requirement_count` 기대값 13과 관측값 15가 달라 실패했다. MC/DC scoring/Golden 계약을 임의 변경하지 않고 원인 검토 단계에 둔다.

**원칙:** Topic Pack 내용은 더 좋은 자동 coverage 수치를 만들기 위해 무작정 채우지 않는다.
대표 질문이 실제로 요구하는 fact를 필수로 연결하고, 배경 사실은 선택으로 표시한다. 사람의
검토가 필요한 source는 승인 상태로 가장하지 않는다.
