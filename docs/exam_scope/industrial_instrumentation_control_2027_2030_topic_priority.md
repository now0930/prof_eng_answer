# 산업계측제어기술사 2027~2030 Topic Pack 우선순위 Roadmap

## 1. 목적

이 문서는 공식 필기 세부항목 중 현재 Coverage가 `GAP` 또는 `PARTIAL`인 17개 영역을
현재 Topic Pack 구조와 공식 출제기준에 맞추어 보완하기 위한 개발 우선순위를 정의한다.

기준 Coverage 문서:

- `docs/exam_scope/industrial_instrumentation_control_2027_2030_topic_pack_coverage.md`

Stage 4B semantic priority review SHA-256: `87268861f9aa7af6cc9de9482cbf911d551ded36dd1adb4042e580fd43abffec`

## 2. Historical evidence 사용 경계

- Historical evidence quality: **LIMITED_USE_QUALITATIVELY**
- Actual-exam-like source count: **0**
- Trend-like source count: **1**
- Historical frequency score authorized: **false**

Repository에서 실제 회차별 기출 원문을 충분히 확보하지 못했으므로
이번 우선순위에는 기출 빈도 숫자를 사용하지 않는다.
즉 아래 점수는 출제확률이 아니라 Topic Pack 개발 순서를 위한 semantic planning score다.

## 3. 우선순위 판정 축

- Coverage urgency: `GAP=5`, `PARTIAL=3`
- 기술사 답안 핵심성: 1~5
- 복수 criterion 보완 효과: 1~5
- 기존 Topic과의 ownership 명확성: 1~5
- Historical frequency: **미채점**
- 최대 20점

## 4. 17개 미충족 criterion 우선순위

| Rank | ID | Coverage | Urgency | Core | Leverage | Ownership | Score |
|---:|---|:---:|---:|---:|---:|---:|---:|
| 1 | `IC-2027-W-2-6` 계측제어기기의 전원 및 접지방식 | GAP | 5 | 5 | 5 | 5 | **20** |
| 2 | `IC-2027-W-3-7` 공정제어 계측(P&ID) 설계 | GAP | 5 | 5 | 5 | 5 | **20** |
| 3 | `IC-2027-W-2-8` 계측제어기기 및 시스템 설계 규정 | GAP | 5 | 4 | 5 | 5 | **19** |
| 4 | `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책 | GAP | 5 | 5 | 4 | 5 | **19** |
| 5 | `IC-2027-W-3-10` 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등) | GAP | 5 | 4 | 4 | 5 | **18** |
| 6 | `IC-2027-W-3-9` 계측제어시스템의 하드웨어 개발, 생산 및 검증 | GAP | 5 | 4 | 4 | 5 | **18** |
| 7 | `IC-2027-W-1-4` 전자기기의 오차 발생요인과 대책 | GAP | 5 | 4 | 3 | 5 | **17** |
| 8 | `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | PARTIAL | 3 | 5 | 5 | 4 | **17** |
| 9 | `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계 | PARTIAL | 3 | 5 | 5 | 4 | **17** |
| 10 | `IC-2027-W-4-9` 계측제어설비 설치 및 기술기준 | PARTIAL | 3 | 5 | 5 | 4 | **17** |
| 11 | `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | PARTIAL | 3 | 5 | 4 | 3 | **15** |
| 12 | `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | PARTIAL | 3 | 4 | 2 | 5 | **14** |
| 13 | `IC-2027-W-4-5` 생산관리(원가, 인력, 수행일정 등) | GAP | 5 | 2 | 2 | 5 | **14** |
| 14 | `IC-2027-W-4-6` 제어시스템의 운영 및 관리 | PARTIAL | 3 | 4 | 4 | 3 | **14** |
| 15 | `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등) | PARTIAL | 3 | 4 | 3 | 3 | **13** |
| 16 | `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | PARTIAL | 3 | 3 | 3 | 3 | **12** |
| 17 | `IC-2027-W-5-2` 계측제어 관련 동향 | GAP | 5 | 2 | 2 | 2 | **11** |

## 5. Criterion별 판단 근거

### 1. `IC-2027-W-2-6` 계측제어기기의 전원 및 접지방식

- Coverage: **GAP**
- Semantic priority score: **20/20**
- 판단: 전원·접지는 계측 오차, EMC, 설치 품질과 직접 연결되고 현재 독립 Topic이 전혀 없다.
- 잔여범위: AC/DC 전원계통, UPS/DC system, grounding/bonding, signal ground, shield, ground loop, EMC 관점의 신규 Topic이 필요하다.

### 2. `IC-2027-W-3-7` 공정제어 계측(P&ID) 설계

- Coverage: **GAP**
- Semantic priority score: **20/20**
- 판단: P&ID는 계장 설계의 공통 언어이며 설계·시공·시운전·운영 문서를 연결한다.
- 잔여범위: P&ID 및 공정배관계장도 작성·검토 전용 Topic이 필요하다.

### 3. `IC-2027-W-2-8` 계측제어기기 및 시스템 설계 규정

- Coverage: **GAP**
- Semantic priority score: **19/20**
- 판단: 설계기준·표준·specification은 프로젝트/설치 기준을 지배하는 상위 설계축이다.
- 잔여범위: 설계기준, applicable code/standard hierarchy, design basis, specification 작성·검토·deviation 관리 Topic이 필요하다.

### 4. `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책

- Coverage: **GAP**
- Semantic priority score: **19/20**
- 판단: 위험장소·방폭·본질안전은 안전성과 기기선정의 독립 핵심영역이다.
- 잔여범위: 방폭/본질안전, hazardous area classification, environmental/process hazard에 따른 계측·제어기기 선정과 대책 Topic이 필요하다.

### 5. `IC-2027-W-3-10` 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등)

- Coverage: **GAP**
- Semantic priority score: **18/20**
- 판단: EMC/EMI·온습도·진동 qualification은 전원/접지 및 하드웨어 V&V와 연결된다.
- 잔여범위: 환경시험 및 EMC/EMI 내성·방출, 온습도·진동 등 qualification Topic이 필요하다.

### 6. `IC-2027-W-3-9` 계측제어시스템의 하드웨어 개발, 생산 및 검증

- Coverage: **GAP**
- Semantic priority score: **18/20**
- 판단: 현재 software lifecycle은 강하지만 hardware lifecycle의 대칭축이 비어 있다.
- 잔여범위: 하드웨어 architecture, component selection, panel design, prototype, production test, verification/validation을 묶는 신규 Topic이 필요하다.

### 7. `IC-2027-W-1-4` 전자기기의 오차 발생요인과 대책

- Coverage: **GAP**
- Semantic priority score: **17/20**
- 판단: 전자기기 오차는 공식 GAP이며 온도·노화·전원·noise·공차를 하나의 error chain으로 정리할 필요가 있다.
- 잔여범위: 전자회로·전자기기 오차원인, 온도·노화·전원·노이즈·부품공차와 대책을 다루는 신규 Topic이 필요하다.

### 8. `IC-2027-W-3-1` 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소

- Coverage: **PARTIAL**
- Semantic priority score: **17/20**
- 판단: 밸브 지식은 강하지만 transmitter-controller-final element 전체 loop와 변수별 전략이 부족하다.
- 잔여범위: 공식 항목은 온도·압력·유량·수위 제어의 기본요소와 전체 loop 설계를 요구한다. 현재는 최종제어요소에 편중되어 process dynamics, transmitter-controller-valve loop 및 각 변수별 제어전략이 부족하다.

### 9. `IC-2027-W-3-4` 단일루프 제어 및 다중루프 제어설계

- Coverage: **PARTIAL**
- Semantic priority score: **17/20**
- 판단: 상태공간 Topic과 별개로 cascade/ratio/feedforward/override/split-range 공정제어 구조가 없다.
- 잔여범위: 공정제어에서 말하는 single-loop와 cascade, ratio, feedforward, override/selective, split-range 같은 전형적 다중루프 제어구조의 설계 Topic이 없다.

### 10. `IC-2027-W-4-9` 계측제어설비 설치 및 기술기준

- Coverage: **PARTIAL**
- Semantic priority score: **17/20**
- 판단: FAT/SAT는 있으나 설치·배선·배관·시공검사·code가 부족하다.
- 잔여범위: 설치 자체의 배선·배관·접지·시공검사와 적용 기술기준/code, 설치 품질관리 범위는 다루지 않는다.

### 11. `IC-2027-W-2-1` 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준

- Coverage: **PARTIAL**
- Semantic priority score: **15/20**
- 판단: 센서군은 이미 넓지만 압력·습도·속도/회전이라는 명시적 공식 예시가 비어 있다.
- 잔여범위: 공식 예시의 압력·습도·속도 등 주요 측정량을 독립적으로 포괄하지 못한다. 특히 일반 압력계측, 습도, 속도/회전 계측 범위가 비어 있다.

### 12. `IC-2027-W-2-2` 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘

- Coverage: **PARTIAL**
- Semantic priority score: **14/20**
- 판단: 초음파/Radar는 있으나 광·laser 비접촉 계측이 빠져 있다.
- 잔여범위: 공식 예시의 광학식 비접촉 측정과 광센서/레이저 기반 원리·알고리즘이 없다.

### 13. `IC-2027-W-4-5` 생산관리(원가, 인력, 수행일정 등)

- Coverage: **GAP**
- Semantic priority score: **14/20**
- 판단: 공식 GAP이지만 기술 핵심성은 상대적으로 낮고 제조관리 관점이 강하다.
- 잔여범위: 계측제어기기/시스템 제조 관점의 생산계획·공정·품질·원가·자원관리 Topic이 필요하다.

### 14. `IC-2027-W-4-6` 제어시스템의 운영 및 관리

- Coverage: **PARTIAL**
- Semantic priority score: **14/20**
- 판단: 운영 evidence는 많지만 유지정비 전략·calibration·inspection·spare/KPI가 분산되어 있다.
- 잔여범위: 공식 범위의 일반적인 자동제어시스템 유지정비·운영 체계, 예방/예지/고장정비 전략, calibration/inspection 계획, spare·work order·maintenance KPI가 하나의 전용 Topic으로 통합되어 있지 않다.

### 15. `IC-2027-W-4-4` 프로젝트 관리(원가, 인력, 수행일정 등)

- Coverage: **PARTIAL**
- Semantic priority score: **13/20**
- 판단: 기존 software project Topic과 중복이 있어 일반화된 instrumentation project scope를 신중히 분리해야 한다.
- 잔여범위: 공식 세부범위의 자동화 기본계획, 현장계기 선정, 공사 설계도서, 운전조작서, 제작공정·생산계획, 제조원가까지는 포괄하지 못한다.

### 16. `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등)

- Coverage: **PARTIAL**
- Semantic priority score: **12/20**
- 판단: AI/Physical AI는 이미 강하므로 IoT/Smart Factory 잔여축 위주 보강이 적절하다.
- 잔여범위: 공식 예시의 IoT와 스마트팩토리 전체 architecture는 부분적으로만 연결되고 양자컴퓨팅 등 기타 신기술 축은 없다. 신기술 항목 특성상 지속 확장도 필요하다.

### 17. `IC-2027-W-5-2` 계측제어 관련 동향

- Coverage: **GAP**
- Semantic priority score: **11/20**
- 판단: 정적 Topic 하나보다 주기적 trend/법령/표준 review lane이 적합하며 stale 위험이 크다.
- 잔여범위: 동향/법령/표준 업데이트를 독립적으로 관리하는 Topic 또는 주기적 review 체계가 필요하다.

## 6. 신규 Topic Pack Roadmap

| 순서 | Tier | 추천 Topic ID | 직접 대상 | Action |
|---:|---|---|---|---|
| 1 | TIER_1 | `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | `IC-2027-W-3-1`, `IC-2027-W-3-4` | NEW_TOPIC |
| 2 | TIER_1 | `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | `IC-2027-W-3-7`, `IC-2027-W-4-4`, `IC-2027-W-4-9` | NEW_TOPIC |
| 3 | TIER_1 | `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | `IC-2027-W-2-6`, `IC-2027-W-3-10`, `IC-2027-W-4-9`, `IC-2027-W-1-4` | NEW_TOPIC |
| 4 | TIER_1 | `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | `IC-2027-W-4-2`, `IC-2027-W-2-8`, `IC-2027-W-4-9` | NEW_TOPIC |
| 5 | TIER_1 | `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | `IC-2027-W-2-8`, `IC-2027-W-4-4`, `IC-2027-W-4-9` | NEW_TOPIC |
| 6 | TIER_1 | `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | `IC-2027-W-4-9`, `IC-2027-W-2-6`, `IC-2027-W-2-8` | NEW_TOPIC |
| 7 | TIER_1 | `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | `IC-2027-W-3-10`, `IC-2027-W-2-6`, `IC-2027-W-1-4` | NEW_TOPIC |
| 8 | TIER_1 | `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `IC-2027-W-3-9`, `IC-2027-W-4-5` | NEW_TOPIC |
| 9 | TIER_2 | `electronics_error_noise_drift_tolerance_aging_power_mitigation` | `IC-2027-W-1-4`, `IC-2027-W-2-6`, `IC-2027-W-3-10` | NEW_TOPIC |
| 10 | TIER_2 | `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | `IC-2027-W-2-1` | NEW_TOPIC |
| 11 | TIER_2 | `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | `IC-2027-W-2-1` | NEW_TOPIC |
| 12 | TIER_2 | `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | `IC-2027-W-2-1` | NEW_TOPIC |
| 13 | TIER_2 | `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | `IC-2027-W-2-2` | NEW_TOPIC |
| 14 | TIER_2 | `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `IC-2027-W-4-6` | NEW_TOPIC |
| 15 | TIER_3 | `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | `IC-2027-W-4-4` | NEW_TOPIC |
| 16 | TIER_3 | `instrumentation_production_management_planning_quality_cost_resources` | `IC-2027-W-4-5`, `IC-2027-W-3-9` | NEW_TOPIC |
| 17 | TIER_3 | `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread` | `IC-2027-W-5-1` | NEW_TOPIC |
| 18 | DYNAMIC_LANE | 정적 Topic 없음 | `IC-2027-W-5-2` | DYNAMIC_REVIEW_LANE |

## 7. TIER 1 — 1차 확장

### 1. `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`

- 공정제어 Loop Architecture와 단일·다중루프 제어
- 대상 criterion: `IC-2027-W-3-1`, `IC-2027-W-3-4`
- 이유: 하나의 Topic으로 두 PARTIAL을 동시에 직접 보완한다. 기존 상태공간/PID/밸브 Topic과 역할 경계도 명확하다.

### 2. `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`

- P&ID 계기기호·Tag·Loop·Control Narrative 설계
- 대상 criterion: `IC-2027-W-3-7`, `IC-2027-W-4-4`, `IC-2027-W-4-9`
- 이유: 현재 완전 GAP이며 프로젝트 설계도서와 설치/시운전까지 연결되는 공통 문서축이다.

### 3. `instrumentation_power_grounding_shielding_ups_ground_loop_emc`

- 계측 전원·접지·Shield·Ground Loop·UPS/DC System
- 대상 criterion: `IC-2027-W-2-6`, `IC-2027-W-3-10`, `IC-2027-W-4-9`, `IC-2027-W-1-4`
- 이유: 공식 GAP을 직접 닫고 EMC·설치·오차와 연결되는 높은 재사용성을 가진다.

### 4. `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

- 위험장소 분류·방폭·본질안전 및 계측기기 선정
- 대상 criterion: `IC-2027-W-4-2`, `IC-2027-W-2-8`, `IC-2027-W-4-9`
- 이유: 안전·기기선정·설치 code를 묶는 독립 기술영역이며 현재 관련 Topic이 없다.

### 5. `instrumentation_system_design_basis_codes_standards_specification_deviation_management`

- 계측제어 Design Basis·Code/Standard·Specification·Deviation 관리
- 대상 criterion: `IC-2027-W-2-8`, `IC-2027-W-4-4`, `IC-2027-W-4-9`
- 이유: 설계 규정 GAP을 직접 소유하고 프로젝트·설치 기준의 상위 reference 역할을 한다.

### 6. `instrumentation_installation_wiring_impulse_tubing_inspection_codes`

- 계측설비 설치·배선·도압배관·시공검사 및 기술기준
- 대상 criterion: `IC-2027-W-4-9`, `IC-2027-W-2-6`, `IC-2027-W-2-8`
- 이유: 현재 FAT/SAT 위주의 evidence를 실제 설치 품질·시공검사·code까지 확장한다.

### 7. `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

- 환경시험·EMC/EMI·온습도·진동 Qualification
- 대상 criterion: `IC-2027-W-3-10`, `IC-2027-W-2-6`, `IC-2027-W-1-4`
- 이유: 환경 검증 GAP을 직접 닫고 전원/접지·전자기기 오차와 연계된다.

### 8. `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

- 제어 Hardware Lifecycle·Panel Architecture·생산·V&V
- 대상 criterion: `IC-2027-W-3-9`, `IC-2027-W-4-5`
- 이유: software lifecycle의 대칭축인 hardware 개발·생산·검증 GAP을 채운다.


## 8. TIER 2 — 센서·오차·운영 보강

### 9. `electronics_error_noise_drift_tolerance_aging_power_mitigation`

- 전자기기 오차·Noise·Drift·Tolerance·Aging 및 대책
- 대상 criterion: `IC-2027-W-1-4`, `IC-2027-W-2-6`, `IC-2027-W-3-10`
- 이유: 1-4를 직접 소유하면서 전원/EMC와 중복하지 않도록 회로·부품 error chain에 집중한다.

### 10. `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`

- 압력계측 Sensor 원리·선정·오차
- 대상 criterion: `IC-2027-W-2-1`
- 이유: 공식 예시에 직접 포함되고 기존 DP level/압전 동압 Topic과 구분되는 일반 압력계측 공백을 메운다.

### 11. `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`

- 속도·회전수 계측 Encoder·Proximity·Tachometer
- 대상 criterion: `IC-2027-W-2-1`
- 이유: 공식 예시 중 현재 독립 coverage가 없는 속도/회전 계측을 보강한다.

### 12. `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`

- 습도·노점 계측 원리·선정·보상
- 대상 criterion: `IC-2027-W-2-1`
- 이유: 공식 예시의 습도 측정 공백을 직접 닫는다.

### 13. `optical_laser_photoelectric_noncontact_measurement_tof_triangulation`

- 광·Laser·Photoelectric 비접촉 측정과 TOF/Triangulation
- 대상 criterion: `IC-2027-W-2-2`
- 이유: 초음파/Radar와 겹치지 않으면서 공식 문구의 '광' 측정 공백을 직접 보강한다.

### 14. `control_system_operations_maintenance_calibration_inspection_spares_kpi`

- 제어시스템 운영·유지정비·Calibration·Inspection·Spare·KPI
- 대상 criterion: `IC-2027-W-4-6`
- 이유: 분산된 운영 evidence를 유지정비 management lifecycle로 통합한다.


## 9. TIER 3 — 관리·신기술 보강

### 15. `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance`

- 계측제어 프로젝트 관리·기본설계·원가·일정·설계도서
- 대상 criterion: `IC-2027-W-4-4`
- 이유: 기존 software project Topic을 무리하게 확장하지 않고 일반 계측제어 project scope를 독립시킨다.

### 16. `instrumentation_production_management_planning_quality_cost_resources`

- 계측제어 생산관리·공정·품질·원가·자원
- 대상 criterion: `IC-2027-W-4-5`, `IC-2027-W-3-9`
- 이유: 공식 GAP이지만 기술설계 Topic보다 우선도는 낮다. 제조·생산관리 문제에 독립 대응한다.

### 17. `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`

- Industrial IoT·Smart Factory·Edge/Cloud·Interoperability
- 대상 criterion: `IC-2027-W-5-1`
- 이유: 기존 AI/Physical AI가 이미 강하므로 신기술의 IoT/Smart Factory architecture 잔여축만 보강한다.

## 10. Dynamic lane — 최신동향

- 대상 criterion: `IC-2027-W-5-2`
- Action: **DYNAMIC_REVIEW_LANE**
- 이유: 정적 Topic Pack은 빠르게 stale해진다. 주기적 source refresh와 review workflow가 더 적합하다.

`IC-2027-W-5-2`는 일반적인 정적 Topic Pack 한 개로 고정하지 않는다.
최신동향·법령·표준은 시간이 지나면 stale해지므로 rolling review와 source refresh를 별도 운영하는 편이 적절하다.

## 11. 1차 확장 효과

TIER 1은 8개 신규 Topic으로 다음 큰 공백을 우선 닫는 것을 목표로 한다.

- 공정제어 전체 loop 및 다중루프 구조
- P&ID
- 전원·접지
- 위험장소·방폭·본질안전
- 설계기준·표준·Specification
- 설치·배선·도압배관·시공검사
- 환경·EMC/EMI Qualification
- Hardware lifecycle·생산·V&V

TIER 1 완료 후 Coverage를 다시 계산한 뒤 TIER 2를 착수한다.
즉 18개 후보를 한 번에 생성하지 않는다.

## 12. Architecture boundary

- 이번 gap은 지식범위 문제이므로 Question Type을 추가하지 않는다.
- Thermocouple Topic의 RTD 혼합-content 문제는 별도 source repair로 유지한다.
- 신규 Topic source JSON은 이 문서 작성 단계에서 생성하지 않는다.
- 각 Topic은 이후 독립 authoring → focused validation → 개별 commit 순서로 처리한다.
