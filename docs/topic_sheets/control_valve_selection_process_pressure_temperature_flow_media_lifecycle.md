# 공정 압력·온도·유량·유체 및 수명주기를 고려한 제어밸브 선정 절차

`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

## 1. 핵심 정의

제어밸브 선정은 Cv 하나를 계산하거나 body type 하나를 고르는 작업이 아니다.
공정 요구조건을 완전하게 수집하고 전문 분석 결과를 통합하여 package를 결정하는 절차이다.
결정 결과는 datasheet, vendor evaluation, FAT·SAT, commissioning 및 수명주기 자료로 검증한다.

Topic 16은 통합 선정 프로세스를 소유한다.
Topic 1~15는 개별 물리와 전문 계산을 소유한다.

## 2. 전체 선정 흐름

1. Governing document와 tag·service boundary를 확정한다.
2. Minimum·normal·maximum·transient operating case matrix를 작성한다.
3. Pressure·temperature·flow·phase·composition 및 property basis를 검증한다.
4. Control·shutoff·leakage·fail action·response·safety 요구를 정의한다.
5. Topic 1~15의 sizing·damage·dynamics·safety 결과를 교차검증한다.
6. Body·trim·characteristic·material·actuator·accessory package를 비교한다.
7. Datasheet·requisition·vendor bid·deviation을 통제한다.
8. ITP·FAT·SAT·commissioning으로 성능을 인수한다.
9. Reliability·spares·lifecycle cost·field feedback·MOC를 폐루프로 관리한다.

## 3. Operating Case와 Process Data

| 구분 | 확인 항목 | 선정 영향 |
|---|---|---|
| 운전 case | minimum, normal, maximum, startup, shutdown, upset, cleaning | governing Cv, ΔP, travel, temperature와 load 결정 |
| 압력 | reference, 위치, static head, line loss, design pressure | sizing, class, actuator load, choking 영향 |
| 온도 | normal, transient, heat soak, ambient, tracing | material, clearance, packing, actuator·accessory 영향 |
| 유량 | mass·volume, standard·actual, uncertainty | capacity, turndown, velocity와 energy 영향 |
| 유체 | phase, composition, density, viscosity, vapor pressure | equation, cavitation, corrosion와 sealing 영향 |
| 입자·오염 | size, shape, concentration, fouling, cleaning | body·trim geometry, material과 maintenance 영향 |

## 4. 기능 요구조건

- Control objective와 required response
- Installed turndown, authority, gain과 travel distribution
- Shutoff differential pressure와 required leakage
- Fail-open, fail-close 또는 fail-in-place
- Loss of air, power, signal과 stored energy
- Noise, vibration, emissions, hazardous area와 regulatory requirement
- SIS·ESD 적용 시 safe state, PFDavg·PFH, response와 proof-test requirement

## 5. Topic 1~15 결과 통합

- **Topic 1** `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`: Actuator force, friction, spring sizing and fail-safe mechanics
- **Topic 2** `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`: Inherent and installed flow-characteristic theory
- **Topic 3** `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`: Deadband, stiction and dynamic-response testing
- **Topic 4** `control_valve_types_globe_rotary_body_actuator_selection`: Valve-body and actuator taxonomy
- **Topic 5** `control_valve_authority_rangeability_gain_installed_performance`: Authority, installed gain, rangeability and turndown
- **Topic 6** `control_valve_sizing_cv_kv_reynolds_liquid_selection`: Liquid Cv, Kv, Reynolds and piping-factor calculation
- **Topic 7** `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`: Gas sizing, expansion factor and choked pressure ratio
- **Topic 8** `control_valve_cavitation_flashing_choked_flow_damage_prevention`: Cavitation, flashing and liquid choking physics
- **Topic 9** `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`: Aerodynamic and hydrodynamic noise prediction
- **Topic 10** `balanced_trim_unbalanced_trim_structure_sealing_applications`: Balanced and unbalanced trim structure and seal mechanics
- **Topic 11** `control_valve_positioner_ip_converter_booster_accessories_calibration`: Positioner, I/P, booster and accessory calibration
- **Topic 12** `smart_positioner_diagnostics_valve_signature_predictive_maintenance`: Valve signature and predictive-diagnostics detail
- **Topic 13** `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`: Seat leakage, shutoff class, packing and fugitive emissions
- **Topic 14** `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`: High-low flow, temperature, cryogenic and particle severe service
- **Topic 15** `final_control_element_sil_sis_esd_valve_partial_stroke_test`: SIF final-element architecture, PFDavg, PST and proof-test verification

통합 시에는 결과값만 받지 않는다.
입력 case, units, assumption, correction, margin, limitation, reviewer와 evidence를 함께 확인한다.

## 6. Package 선정 Matrix

| Package 요소 | 주요 기준 | 대표 위험 |
|---|---|---|
| Body·flow path | capacity, recovery, solids, piping, access | oversizing, erosion, plugging, removal 불가 |
| Trim·characteristic | installed gain, travel, damage, stability | hunting, low-travel control, wear |
| Material·sealing | composition, temperature, corrosion, leakage | corrosion, galling, external release |
| Actuator | worst-case load, minimum supply, fail action, speed | fail-to-move, slow trip, insufficient shutoff |
| Accessories | response, capacity, diagnostics, hazardous area | interaction failure, restriction, false feedback |
| Installation | orientation, piping load, support, drain·vent, access | vibration, trapped fluid, maintenance delay |

Mandatory requirement를 만족하지 못한 후보는 weighted score로 보상하지 않는다.
Uncertainty와 contingency는 분리하고 double margin을 방지한다.

## 7. Datasheet와 Vendor Evaluation

- 동일 datasheet revision과 case basis로 vendor bid를 비교한다.
- Vendor sizing의 inputs, units, correction, warnings와 proprietary coefficient를 확인한다.
- Deviation은 requirement ID, impact, risk, owner와 approval로 관리한다.
- Guaranteed capacity, leakage, response, material, noise, delivery와 support를 구분한다.
- Purchase 이후 model, material, firmware, setpoint와 drawing 변경을 configuration control한다.

## 8. FAT·SAT·Commissioning

- FAT: pressure boundary, leakage, stroke, fail action, accessories, response와 documents
- SAT: actual wiring, air supply, logic, interlock, command와 feedback
- Commissioning: actual process에서 travel, oscillation, response, noise, cavitation과 control objective
- As-built: final datasheet, drawing, configuration, calibration, records, spares와 maintenance instruction

FAT는 SAT와 commissioning을 대체하지 않는다.

## 9. Reliability와 Lifecycle

- Availability는 MTBF와 MTTR뿐 아니라 bypass와 online repair 가능성을 포함한다.
- Spare는 installed population 비율이 아니라 criticality, lead time와 interchangeability로 정한다.
- Lifecycle cost는 purchase, energy, maintenance, downtime, service life와 disposal을 포함한다.
- Field failure, diagnostics, as-found·as-left와 vendor notice를 MOC와 revalidation에 반영한다.

## 10. Screening Formula

### `capacity_utilization`

- 식: \(U_C = C_{v,\mathrm{required}}/C_{v,\mathrm{rated}}\)
- 적용: Rated capacity가 양수일 때 required capacity가 catalog·selected capacity에서 차지하는 비율이다.
- 회귀 예: `capacity_utilization(80, 100)=0.8`

### `capacity_margin`

- 식: \(M_C = (C_{v,\mathrm{rated}}-C_{v,\mathrm{required}})/C_{v,\mathrm{required}}\)
- 적용: Required capacity가 양수일 때 capacity 여유를 required 기준으로 표현한다.
- 회귀 예: `capacity_margin(100, 80)=0.25`

### `installed_range_requirement`

- 식: \(R_{\mathrm{req}} = Q_{\max,\mathrm{req}}/Q_{\min,\mathrm{req}}\)
- 적용: Required minimum flow가 양수일 때 필요한 installed flow range를 계산한다.
- 회귀 예: `installed_range_requirement(100, 5)=20`

### `range_margin`

- 식: \(M_R = (R_{\mathrm{available}}-R_{\mathrm{required}})/R_{\mathrm{required}}\)
- 적용: Required range가 양수일 때 available range의 상대 여유를 평가한다.
- 회귀 예: `range_margin(30, 20)=0.5`

### `valve_authority_handoff`

- 식: \(a = \Delta P_v/(\Delta P_v+\Delta P_{\mathrm{other}})\)
- 적용: Topic 5 hand-off 식이며 두 압력손실 합이 양수인 동일 operating case에서 적용한다.
- 회귀 예: `valve_authority(40, 60)=0.4`

### `hydraulic_energy_loss_power`

- 식: \(P_{\mathrm{loss}} = \Delta P\,Q\)
- 적용: 압력차와 actual volumetric flow를 일관된 SI 단위로 사용할 때 W 단위 hydraulic power loss를 계산한다.
- 회귀 예: `hydraulic_power(200000, 0.01)=2000`

### `availability`

- 식: \(A = MTBF/(MTBF+MTTR)\)
- 적용: Repairable steady-state approximation에서 MTBF가 양수이고 MTTR이 음수가 아닐 때 적용한다.
- 회귀 예: `availability(990, 10)=0.99`

### `expected_downtime_cost`

- 식: \(C_D = f\,t_D\,c_D\)
- 적용: 분석기간 내 failure frequency, mean downtime 및 downtime cost rate의 곱이다.
- 회귀 예: `downtime_cost(2, 5, 1000)=10000`

### `discounted_lifecycle_cost`

- 식: \(LCC = \sum_{t=0}^{N} C_t/(1+r)^t\)
- 적용: 기간별 현금흐름과 discount rate의 시점·통화·실질 또는 명목 기준을 일치시킨다.
- 회귀 예: `discounted_cost([1000,110],0.1)=1100`

### `weighted_selection_score`

- 식: \(S = \sum_i w_i s_i\)
- 적용: Mandatory gate 통과 후 정규화된 non-negative weight의 합이 1일 때 후보 비교에 사용한다.
- 회귀 예: `weighted_score([0.6,0.4],[80,90])=84`

### `requirement_coverage`

- 식: \(C_R = N_{\mathrm{verified}}/N_{\mathrm{applicable}}\)
- 적용: Applicable requirement 수가 양수이고 verified 수가 범위 내일 때 적용한다.
- 회귀 예: `requirement_coverage(45,50)=0.9`

### `deviation_closure_rate`

- 식: \(C_D = N_{\mathrm{closed}}/N_{\mathrm{total}}\)
- 적용: Total technical deviation 수가 양수이고 closed 수가 범위 내일 때 적용한다.
- 회귀 예: `deviation_closure_rate(18,20)=0.9`

## 11. 실무 답안 작성 순서

1. 선정 목적, tag·service boundary, governing document와 requirement register를 정의한다.
2. Minimum·normal·maximum·transient case와 pressure·temperature·flow·phase·composition envelope를 정리한다.
3. Control, shutoff, leakage, fail action, response, safety, environmental 및 regulatory requirement를 정의한다.
4. Topic 1~15의 sizing, characteristic, dynamics, damage, leakage, severe-service 및 SIS 결과를 교차검증한다.
5. Body, trim, characteristic, flow direction, material, actuator, accessory와 installation을 trade-off한다.
6. Datasheet, requisition, vendor bid, sizing assumption, deviation, guarantees와 configuration을 통제한다.
7. ITP, material traceability, FAT, SAT, loop check, commissioning 및 installed-performance acceptance를 수행한다.
8. Reliability, availability, maintainability, spares, obsolescence, energy, downtime 및 lifecycle cost를 평가한다.
9. As-built baseline, field failure, diagnostics, as-found·as-left, MOC와 periodic revalidation을 폐루프로 관리한다.

## 12. 고득점 기준

- Operating case completeness와 data reference를 먼저 제시한다.
- Topic 1~15의 결과를 계산값 나열이 아니라 decision hand-off로 연결한다.
- Body·trim·material·actuator·accessory를 하나의 package로 비교한다.
- Vendor deviation과 acceptance evidence를 포함한다.
- Reliability, maintainability, energy, downtime와 field feedback까지 연결한다.

## 13. 대표 오답

- 오답: 정상 유량 한 점만 맞으면 모든 운전조건에서 적합한 밸브다.
  - 교정: Minimum·normal·maximum·startup·shutdown·upset 등 governing case matrix를 검증해야 한다.
- 오답: Vendor가 선정한 뒤 datasheet를 작성해도 선정 품질에는 영향이 없다.
  - 교정: Datasheet는 vendor 비교 전 요구조건과 case basis를 고정하는 핵심 입력 문서다.
- 오답: Vendor sizing software 결과는 독립 검토 없이 승인할 수 있다.
  - 교정: 입력·units·correction·warning·assumption과 guarantee basis를 독립 검토한다.
- 오답: 배관 line size와 동일한 밸브 size를 선택하면 된다.
  - 교정: Valve size는 required Cv, controllability, velocity, noise, reducer 영향과 installation을 종합하여 정한다.
- 오답: Cv가 클수록 capacity margin이 커져 항상 안전하다.
  - 교정: Oversizing은 저 travel, gain 증가, hunting 및 shutoff·response 문제를 만들 수 있다.
- 오답: 모든 계산에 margin을 많이 더할수록 더 좋은 선정이다.
  - 교정: Uncertainty와 contingency를 분리하고 double margin 및 operability 손실을 방지한다.
- 오답: Catalog rangeability가 required Qmax/Qmin보다 크면 installed turndown이 보장된다.
  - 교정: Installed characteristic, authority, gain, minimum controllable flow와 travel distribution을 검증한다.
- 오답: Equal-percentage 또는 linear라는 이름만으로 제어성이 결정된다.
  - 교정: System pressure distribution과 installed characteristic이 실제 제어성을 결정한다.
- 오답: Normal operating pressure만으로 body class를 선정한다.
  - 교정: Design pressure·temperature envelope, material group, transient와 applicable code를 사용한다.
- 오답: 유체 이름만 같으면 재질도 동일하게 선정할 수 있다.
  - 교정: Composition, concentration, temperature, velocity, contaminants와 cleaning chemical을 확인한다.
- 오답: Liquid와 gas는 같은 sizing 식과 동일 correction을 적용한다.
  - 교정: Phase별 equation, compressibility, expansion, vapor pressure 및 choking domain을 구분한다.
- 오답: Inlet이 liquid이면 valve 내부의 flashing 또는 two-phase 가능성은 무시할 수 있다.
  - 교정: Pressure·temperature path와 phase-change consequence를 검증한다.

## 14. Key Tags

control valve selection, process design basis, operating case matrix, datasheet, vendor bid evaluation, valve body trim actuator package, FAT SAT commissioning, lifecycle cost, reliability maintainability, MOC revalidation
