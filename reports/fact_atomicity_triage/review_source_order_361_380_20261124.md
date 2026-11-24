# 457-candidate atomicity review — source-ledger indices 361–380 (2026-11-24)

> REVIEW_EVIDENCE_ONLY / NOT_APPROVED / score_effect=none / score_admission=DISABLED.

## Identity and sequence caveat

- Based on `reports/fact_atomicity_triage/batch_01.json` ... `batch_07.json` in their documented concatenation order (78+92+64+42+82+48+51 = 457).
- Under **that explicit order**, indices 361–380 are the 20 entries in source `batch_06.json` rows 3–22. The immutable source item content, Topic ID, Anchor ID, and source blob SHA are recorded in the accompanying JSON.
- The user-reported 17/18 technical-review sequence (feedback/safety/humidity/HIL/EMC then manufacturing/Lead-Lag/LQR/LVDT) **does not coincide** with this concatenated canonical queue order (indices 321–360 are predominantly OT cybersecurity, robotics and pressure). The earlier 360 decisions/identities were not found as row-level review files in the GitHub branch inspection. This report **must not be added to the claimed 360 as 20 new unique decisions** until earlier reviewer ID ledgers are reconciled.
- Source `main@119b6de0a4955c75ba00f2bb07ba7e40c0a5685e`. No canonical Fact, approval, scoring, Registry, generated data, D4, Issue #39, or 119 HOLD changes.
- Primary/official manufacturer and engineering documents were consulted via publicly available web pages and indexed extracts. Full PDF illustration-level verification was not established for every source; source links are locators, **not standard-compliance certifications**.

## Proposed decisions — **not authoritative status changes**

**20 rows = KEEP 15, REVISE 5, HOLD 0.** “KEEP” means current physical claim appears defensible within the specified scope, **not** full source approval or scoring eligibility.

| Queue | Anchor ID | Proposed verdict | Technical scope and reason | Independent source locator |
|---:|---|---|---|---|
| 361 | `bourdon_forms_application` | KEEP | C/spiral/helical 구성과 압력 범위의 형상 의존 관계가 제조사 설명에 부합. 특정 압력 수치를 보편화하지 않음. | [1](https://www.wika.com/en-us/lp_bourdon_tube_pressure_gauge.WIKA), [2](https://blog.wika.com/us/knowhow/what-is-a-diaphragm-pressure-gauge-and-how-does-it-work/) |
| 362 | `diaphragm_deflection_principle` | KEEP | 압력차에 따른 탄성 다이어프램 변위와 저압 감도는 일반적 원리. 재질/두께별 과압 허용치 일반화 금지. | [1](https://blog.wika.com/us/knowhow/what-is-a-diaphragm-pressure-gauge-and-how-does-it-work/) |
| 363 | `diaphragm_sensor_vs_seal` | KEEP | 측정 다이어프램과 유체 격리용 seal 기능이 다르고 seal+capillary+fill fluid의 추가 오차가 존재. | [1](https://blog.wika.com/us/knowhow/what-is-a-diaphragm-pressure-gauge-and-how-does-it-work/), [2](https://www-prod.isa.org/web/acom/article/tip-14-capillary-seal-pitfalls) |
| 364 | `piezoresistive_static_capability` | KEEP | Piezoresistive는 정압/장기 모니터링 가능, 일반 piezoelectric charge-output은 누설로 장기 정압에 불리. 일부 piezoelectric의 준정적 측정 예외 유지. | [1](https://www.kistler.com/INT/en/piezoelectric-pressure-sensors-with-charge-output-pe-for-static-pressure-measurement/C00000140), [2](https://www.pcb.com/resources/technical-information/introduction-to-pressure-sensors) |
| 365 | `dp_transmitter_two_port_principle` | KEEP | 고압/저압 포트 차압 계측과 동일 포트압의 이상적 영차압 원리. 실제 zero offset과 설치오차 구분. | [1](https://www.wika.com/en-in/106d.WIKA), [2](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00813-0105-4001.pdf) |
| 366 | `ambient_environment_hazardous_selection` | KEEP | 환경/보호/설치 조건을 선정 입력으로 취급하는 설계 체크리스트. 방폭 인증의 세부 규정 판단이나 전 장비 공통 의무값을 생성하지 않음. | [1](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00813-0105-4001.pdf) |
| 367 | `accuracy_total_performance_terms` | REVISE | reference accuracy의 제조사 정의와 total performance 평가 항목이 별도 검증 가능 명제. 단일 필수 Fact로 결합하기보다 용어정의와 적용성능을 분리. | [1](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00813-0105-4001.pdf), [2](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/marketing/products/dp-flow/documents/doc-rosemount-00805-0100-1041.pdf) |
| 368 | `zero_span_drift_calibration` | REVISE | span shift(측정 전달특성 gain 변화)와 re-ranging(설정 LRV/URV 변경)을 혼동할 수 있음. zero trim, sensor trim, re-ranging, 교정의 역할 구별 필요. | [1](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/marketing/products/dp-flow/documents/doc-rosemount-00805-0100-1041.pdf), [2](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051-00813-0105-4001.pdf) |
| 369 | `cascade_secondary_faster` | KEEP | secondary는 primary 대비 충분히 빠른 것이 전제; 임의의 3:1 등 단일 속도비를 보편적 절대 규칙으로 승격하지 않음. | [1](https://controlguru.com/an-implementation-recipe-for-cascade-control/) |
| 370 | `cascade_disturbance_condition` | KEEP | secondary PV가 외란에 대한 조기 관측 신호이며 secondary loop가 제어능력을 갖출 때 유리. | [1](https://controlguru.com/cascade-disturbance-rejection-in-the-jacketed-stirred-reactor/), [2](https://controlguru.com/an-implementation-recipe-for-cascade-control/) |
| 371 | `feedforward_principle` | KEEP | 선형 중첩 y=G_u u+G_d d에서 G_ff=-G_d/G_u는 이상적 소거를 표현. 구현 시 인과성, 안정성, 지연, 불확실성 범위가 필수. | [1](https://www.mathworks.com/help/pdf_doc/control/control_ug.pdf) |
| 372 | `split_range_control` | REVISE | split-range는 하나의 제어출력을 둘 이상의 요소에 분배하지만 실제 배분 특성에는 overlap/deadband도 있을 수 있으므로 항상 상호배타적인 출력구간이라고 한정하지 않음. | [1](https://cache.industry.siemens.com/dl/files/808/36209808/att_77975/v1/s7jal71b_en-US.pdf) |
| 373 | `loop_interaction_coordination` | KEEP | actuator 공유, 포화, 모드/신호 방향/loop coupling은 조정 요인. MIMO/LQR/MPC는 이 Fact의 채점 범위 밖이라는 Topic 메타 경계. | [1](https://www.mathworks.com/help/pdf_doc/control/control_ug.pdf), [2](https://cache.industry.siemens.com/dl/files/808/36209808/att_77975/v1/s7jal71b_en-US.pdf) |
| 374 | `feedforward_dynamic_compensation_timing` | KEEP | 두 전달 경로의 동적/지연 차이를 조정하며 지연이 뒤늦은 관측을 보상할 수는 없음. 모든 외란을 완전 상쇄한다고 주장하지 않음. | [1](https://www.mathworks.com/help/pdf_doc/control/control_ug.pdf) |
| 375 | `field_implementation_validation` | KEEP | Siemens PID_Compact 기능 매뉴얼 11/2024 p.90-92: V3에서 active integral limiting, automatic/manual and output limit 동작 명시. 구현 예시로만 유지. | [1](https://support.industry.siemens.com/cs/attachments/108210036/s71500_pid_control_function_manual_en-US_en-US.pdf?download=true) |
| 376 | `radar_pulse_distance_equation` | KEEP | pulse time-of-flight D=v_g tau/2 관계 성립; 이상 공기에서 c 근사. 고압증기 등에서는 gas-phase dielectric 영향 경고; GWR 자료의 구체 수치를 free-space 장치에 직접 전용하지 않음. | [1](https://www.emerson.com/en/measurement-instrumentation/industries/power/level-measurement-in-steam-drums), [2](https://www.us.endress.com/en/endress-hauser-group/Case-studies-application-notes/frequency-antenna-selection-effects) |
| 377 | `radar_fmcw_beat_frequency_distance` | KEEP | 정지 표면/선형 chirp, Doppler 무시 시 f_b=S tau와 D=v_g f_b/(2S) 도출. 계기별 chirp 추정·캘리브레이션은 별도. | [1](https://www.analog.com/en/resources/technical-articles/how-to-build-a-24-ghz-fmcw-radar-system.html) |
| 378 | `radar_bandwidth_range_resolution` | REVISE | ideal ΔR=v_g/(2B)는 타깃 분리능. FFT range-bin spacing은 관측 시간/FFT 길이에 따라 달라지고 full sweep no-padding에서는 수치가 일치할 수도 있어 '항상 다른 값'으로 단정 금지. | [1](https://www.analog.com/en/resources/technical-articles/how-to-build-a-24-ghz-fmcw-radar-system.html), [2](https://www.analog.com/en/resources/glossary/frequency_bin.html) |
| 379 | `radar_frequency_antenna_tradeoff` | KEEP | 동일 개구에서 carrier-frequency 증가는 빔 집속에 유리. range resolution은 변조 bandwidth에 좌우되며 단독 accuracy 향상 보장하지 않음. | [1](https://www.us.endress.com/en/endress-hauser-group/Case-studies-application-notes/frequency-antenna-selection-effects), [2](https://www.vega.com/en-ca/company/blog/2020/radar-sensors-with-strong-focusing-ensure-more-precise-values-in-continuous-level-measurement) |
| 380 | `radar_mounting_nozzle_obstruction_error` | REVISE | 긴/좁은 노즐 및 장애물/부적절한 정렬은 '오차를 일으킬 수 있음'으로 한정; 표면 성상에 따라 수직/경사 타깃 정렬과 제조사 액세서리 조건 확인. | [1](https://www.ch.endress.com/en/field-instruments-overview/level-measurement/Radar-Micropilot-FMR67), [2](https://www.us.endress.com/en/endress-hauser-group/Case-studies-application-notes/frequency-antenna-selection-effects) |

## Five wording revisions (proposals only)

### 367. `accuracy_total_performance_terms`

**Current source:** 압력계기의 reference accuracy는 linearity, hysteresis, repeatability 등의 일부 또는 조합일 수 있고 제조사 정의가 다를 수 있다. 실제 성능은 온도·static pressure·installation·stability 영향까지 포함한 total performance 관점으로 평가한다.

**Recommended wording (not applied):** [분리 권고] (1) Reference accuracy에 포함되는 linearity·hysteresis·repeatability 항목과 합성 방식은 제조사 사양서 정의를 따른다. (2) 실제 적용 성능을 평가할 때는 reference accuracy 외에 ambient temperature, static pressure, long-term stability, installation 영향을 사용조건과 모델 사양에 따라 검토한다.

**Reason:** reference accuracy의 제조사 정의와 total performance 평가 항목이 별도 검증 가능 명제. 단일 필수 Fact로 결합하기보다 용어정의와 적용성능을 분리.

### 368. `zero_span_drift_calibration`

**Current source:** Zero shift는 입력 0 또는 LRV 부근의 offset 변화이고 span shift는 sensitivity 또는 URV-LRV 관계의 변화다. 설치·온도·line pressure 영향이 있으면 제조사 절차에 따라 zero trim, sensor trim 또는 calibration을 구분해 수행한다.

**Recommended wording (not applied):** Zero shift는 기준 입력(예: LRV)에서의 출력 오프셋 변화이고, span shift는 고정된 설정 범위에서 입력-출력 기울기 또는 감도의 변화이다. 설정 LRV/URV 변경(re-ranging)은 span drift와 구분하며, 설치·온도·정압 영향에 대한 zero trim, sensor trim, calibration은 제조사 절차에 따라 선택한다.

**Reason:** span shift(측정 전달특성 gain 변화)와 re-ranging(설정 LRV/URV 변경)을 혼동할 수 있음. zero trim, sensor trim, re-ranging, 교정의 역할 구별 필요.

### 372. `split_range_control`

**Current source:** Split-range 제어는 하나의 controller output 범위를 둘 이상의 최종제어요소에 분할하여 각 요소가 서로 다른 출력구간에서 작동하도록 하는 구조이다. 예를 들어 heating과 cooling valve를 하나의 temperature controller가 서로 다른 범위에서 구동할 수 있다.

**Recommended wording (not applied):** Split-range 제어는 하나의 controller output을 둘 이상의 최종제어요소에 구간별로 매핑하는 구조이다. 예를 들어 하나의 온도 조절기가 heating/cooling valve를 구동할 수 있고, 배분 특성에는 설계 목적에 따라 분리 구간, 중첩 구간 또는 deadband가 포함될 수 있다.

**Reason:** split-range는 하나의 제어출력을 둘 이상의 요소에 분배하지만 실제 배분 특성에는 overlap/deadband도 있을 수 있으므로 항상 상호배타적인 출력구간이라고 한정하지 않음.

### 378. `radar_bandwidth_range_resolution`

**Current source:** FMCW의 이상적 거리 분해능은 ΔR≈v_g/(2B)이다. 이는 두 인접 반사면을 분리하는 능력이며 단일 표면의 측정 정확도, 반복성 또는 FFT bin 간격과 동일하지 않다. 정확도는 S/N비, 주파수·위상 추정, 보간, 스윕 선형성, 교정과 설치조건의 영향을 함께 받는다.

**Recommended wording (not applied):** 정지 표적과 이상적인 FMCW 선형 chirp에서 두 표적의 거리 분해능은 대략 ΔR≈v_g/(2B)이다. 단일 표면의 거리 추정 정확도와 구별해야 하며 FFT bin 간격은 FFT 크기·관측 구간·zero padding에 따라 달라진다. 전체 chirp 구간을 zero-padding 없이 분석하면 수치적으로 ΔR과 일치할 수 있으나 zero-padding만으로 실제 분해능이 개선되지는 않는다.

**Reason:** ideal ΔR=v_g/(2B)는 타깃 분리능. FFT range-bin spacing은 관측 시간/FFT 길이에 따라 달라지고 full sweep no-padding에서는 수치가 일치할 수도 있어 '항상 다른 값'으로 단정 금지.

### 380. `radar_mounting_nozzle_obstruction_error`

**Current source:** 긴 노즐, 작은 노즐직경, 안테나 매몰, 빔 경로 장애물 및 측정면을 향하지 않은 부적절한 정렬은 측정오차를 유발한다. 액체에서는 일반적으로 안테나 축을 액면에 수직으로 정렬하고, 분체에서는 경사진 표면을 향하도록 제조사 지침과 정렬장치에 따라 의도적으로 기울일 수 있다.

**Recommended wording (not applied):** 긴/좁은 노즐, 안테나 매몰, 반사 장애물 또는 부적절한 정렬은 설치조건에 따라 거짓 반사나 신호감쇠 및 측정오차를 일으킬 수 있다. 액체/분체의 표면 형상과 계기 모델별 제조사 설치지침을 확인하여 안테나 위치와 정렬을 결정한다.

**Reason:** 긴/좁은 노즐 및 장애물/부적절한 정렬은 '오차를 일으킬 수 있음'으로 한정; 표면 성상에 따라 수직/경사 타깃 정렬과 제조사 액세서리 조건 확인.


## Method, limitations, and release boundary

- Cross-check aimed at generally accepted engineering principles, bounded conditions, equation units, manufacturer-specific claims and whether two sentences introduce a second independently gradable obligation.
- FMCW derived units: `S=B/T_s` (Hz/s); `f_b=S*(2D/v_g)` (Hz); `D=v_g*f_b/(2S)` (m); `ΔR≈v_g/(2B)` (m). The expressions assume linear chirp, stationary target and negligible Doppler.
- Siemens PDF: `PID control Function Manual, 11/2024`, heading `PID_Compact as of V2` and `PID parameters V3`, printed pp. 90–92; search-index text reviewed, visual screenshot unavailable.
- No Python scoring reproduction, full repository test or Release Gate executed for this report. No canonical statement modification. All original audit HOLD and admission controls remain unchanged.
- Follow-up required: obtain/restore prior review's 360 **exact IDs plus versioned verdict ledger**, run a set-difference check against these 20 IDs, then recalculate cumulative progress; independently verify the five revisions before any Topic Pack or grading effect.
