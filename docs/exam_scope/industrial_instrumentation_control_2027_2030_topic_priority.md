# 산업계측제어기술사 2027~2030 Topic Pack 우선순위 Roadmap

## 1. 목적

이 문서는 69개 Topic Pack 기준의 확장 후 상태를 관리한다.
기존 17개 미충족 criterion 보완 계획은 완료 이력으로 전환하고, 현재 남은 공식 coverage와 후속 작업만 우선순위화한다.

기준 Coverage 문서:

- `docs/exam_scope/industrial_instrumentation_control_2027_2030_topic_pack_coverage.md`
- 현재 Coverage: `COVERED 30 / PARTIAL 2 / GAP 1`
- 현재 Topic Pack: `69`

## 2. Historical evidence 사용 경계

- Historical evidence quality: **LIMITED_USE_QUALITATIVELY**
- Actual-exam-like source count: **0**
- Trend-like source count: **1**
- Historical frequency score authorized: **false**

Repository에서 실제 회차별 기출 원문을 충분히 확보하지 못했으므로 우선순위에 기출 빈도 숫자를 사용하지 않는다.
아래 우선순위는 출제확률 예측이 아니라 공식 criterion 잔여범위와 현재 Topic ownership을 기준으로 한 개발 순서다.

## 3. 확장 완료 상태

| 구분 | 수량 | 상태 |
|---|---:|---|
| 기존 frozen roadmap의 계획 Topic | 17 | **COMPLETE** |
| 현재 전체 Topic Pack | 69 | **ACTIVE** |
| 공식 criterion COVERED | 30 | **COVERED** |
| 공식 criterion PARTIAL | 2 | **REMAINING** |
| 공식 criterion GAP | 1 | **REMAINING** |

기존 TIER 1~3의 17개 Topic은 모두 구현·통합·검증·main 반영을 완료했다.
따라서 기존 `NEW_TOPIC` 계획은 더 이상 backlog가 아니다.

## 4. 완료된 TIER 1 — 1차 확장

### 1. `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`

- 대상 criterion: `IC-2027-W-3-1`, `IC-2027-W-3-4`
- 상태: **COMPLETE**

### 2. `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`

- 대상 criterion: `IC-2027-W-3-7`
- 상태: **COMPLETE**

### 3. `instrumentation_power_grounding_shielding_ups_ground_loop_emc`

- 대상 criterion: `IC-2027-W-2-6`
- 상태: **COMPLETE**

### 4. `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

- 대상 criterion: `IC-2027-W-4-2`
- 상태: **COMPLETE**

### 5. `instrumentation_system_design_basis_codes_standards_specification_deviation_management`

- 대상 criterion: `IC-2027-W-2-8`
- 상태: **COMPLETE**

### 6. `instrumentation_installation_wiring_impulse_tubing_inspection_codes`

- 대상 criterion: `IC-2027-W-4-9`
- 상태: **COMPLETE**

### 7. `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

- 대상 criterion: `IC-2027-W-3-10`
- 상태: **COMPLETE**

### 8. `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

- 대상 criterion: `IC-2027-W-3-9`
- 상태: **COMPLETE**

## 5. 완료된 TIER 2 — 센서·오차·운영 보강

### 9. `electronics_error_noise_drift_tolerance_aging_power_mitigation`

- 대상 criterion: `IC-2027-W-1-4`
- 상태: **COMPLETE**

### 10. `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`

- 대상 criterion: `IC-2027-W-2-1`
- 상태: **COMPLETE**

### 11. `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`

- 대상 criterion: `IC-2027-W-2-1`
- 상태: **COMPLETE**

### 12. `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`

- 대상 criterion: `IC-2027-W-2-1`
- 상태: **COMPLETE**

### 13. `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`

- 대상 criterion: `IC-2027-W-2-2`
- 상태: **COMPLETE**

### 14. `control_system_operations_maintenance_calibration_inspection_spares_kpi`

- 대상 criterion: `IC-2027-W-4-6`
- 상태: **COMPLETE**

## 6. 완료된 TIER 3 — 관리·신기술 보강

### 15. `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`

- 대상 criterion: `IC-2027-W-4-4`
- 상태: **COMPLETE**

### 16. `instrumentation_production_management_planning_quality_cost_resources`

- 대상 criterion: `IC-2027-W-4-5`
- 상태: **COMPLETE**

### 17. `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`

- 대상 criterion: `IC-2027-W-5-1`
- 상태: **COMPLETE**

## 7. 현재 잔여 criterion

| Priority | Criterion | Coverage | 남은 범위 | 처리 방식 |
|---:|---|:---:|---|---|
| 1 | `IC-2027-W-4-2` 위험 환경 제어요소 및 대책 | **PARTIAL** | 방폭·본질안전 외 철도·발전·건축 등 비폭발 위험환경의 fail-safe, environmental/functional hazard, 적용별 제어대책 | STATIC_TOPIC |
| 2 | `IC-2027-W-5-1` 계측제어 관련 신기술 | **PARTIAL** | 양자컴퓨팅 등 기타 emerging technology의 개념·계측제어 적용·한계·성숙도 평가 | STATIC_TOPIC |
| 3 | `IC-2027-W-5-2` 계측제어 관련 동향 | **GAP** | 최신동향·법령·표준의 지속 갱신 | DYNAMIC_REVIEW_LANE |

## 8. STATIC BACKLOG 1 — `IC-2027-W-4-2`

- 현재 확보: hazardous area classification, Zone/EPL/Ex marking, 방폭방식, intrinsic safety entity/barrier/wiring, 계측기기 선정.
- 잔여범위: 철도·발전·건축 등 비폭발 위험환경에서의 fail-safe, 환경/기능 hazard, 전원·통신·제어 상실 시 대책, 적용별 제어요소 선정.
- 기존 Topic을 억지로 확장하지 않고 별도 Topic으로 ownership을 분리한다.
- 추천 Topic ID:
  - `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards`
- 우선순위: **1**
- 완료조건: `IC-2027-W-4-2`의 잔여범위를 직접 소유하고 기존 방폭 Topic과 중복 없이 설명·선정·대책까지 grading 가능해야 한다.

## 9. STATIC BACKLOG 2 — `IC-2027-W-5-1`

- 현재 확보: AI/ML, Physical AI, robot, Digital Twin, IIoT, Smart Factory, Edge/Cloud, interoperability, Digital Thread.
- 잔여범위: 양자컴퓨팅 등 기타 emerging technology의 최소 개념, 계측제어 적용 가능성, 성숙도, 한계, 적용 전제.
- 신기술은 변화가 빠르므로 특정 제품·기업 중심이 아니라 원리·적용·한계·성숙도 평가 프레임을 중심으로 작성한다.
- 추천 Topic ID:
  - `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits`
- 우선순위: **2**
- 완료조건: `IC-2027-W-5-1`의 양자컴퓨팅 및 기타 신기술 잔여축을 보완하되 기존 AI/IIoT Topic과 ownership을 분리해야 한다.

## 10. DYNAMIC BACKLOG — `IC-2027-W-5-2`

- Coverage: **GAP**
- Action: **DYNAMIC_REVIEW_LANE**
- 정적 Topic Pack은 생성하지 않는다.
- 최신동향·법령·표준은 시간이 지나면 stale하므로 rolling review와 source refresh로 관리한다.
- review 시점마다 공식 출제기준, 관련 법령·표준 edition, 계측제어 산업 동향을 확인하고 필요 시 별도 snapshot 문서를 갱신한다.
- static owner가 없는 상태를 의도적으로 유지한다.

## 11. 후속 작업 순서

1. `IC-2027-W-4-2` non-explosion hazardous-environment Topic authoring.
2. `IC-2027-W-5-1` quantum/emerging-technology Topic authoring.
3. `IC-2027-W-5-2` Dynamic Review Lane 운영 규칙 작성.
4. Thermocouple mixed TC+RTD source repair를 별도 commit으로 수행.
5. 위 작업 후 공식 Coverage를 다시 read-only 재감사한다.

새 static Topic은 각각 독립 authoring → focused validation → 개별 commit 순서로 처리한다.
두 static Topic 완료 전에는 coverage를 기계적으로 `COVERED`로 승격하지 않는다.

## 12. Architecture boundary

- Official Category ≠ Topic Pack ≠ Question Type.
- 이번 잔여범위는 지식 coverage 문제이므로 Question Type을 추가하지 않는다.
- `IC-2027-W-5-2`는 static Topic이 아니라 `DYNAMIC_REVIEW_LANE`으로 유지한다.
- Thermocouple Topic의 mixed TC+RTD content 문제는 coverage backlog가 아니라 별도 source repair다.
- 이 Roadmap 갱신 단계에서는 Topic source JSON, generated rubric, production Python을 변경하지 않는다.
- 기존 완료 17 Topic의 source 또는 generated 결과를 재작성하지 않는다.
