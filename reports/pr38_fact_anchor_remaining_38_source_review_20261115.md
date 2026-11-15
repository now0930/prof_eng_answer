# PR #38 — 남은 Fact Anchor 38건 공식 원문 대조 검토 (2026-11-15)

> **Research-only; NO REGISTRY APPROVAL / NO SCORE CHANGE / NO RELEASE.** 원문 48건 기준: `calibration/fact_anchor_simplification_review_20261114.json`; 앞서 검토한 10건은 `reports/pr38_fact_anchor_10_primary_source_crosscheck_20261115.md` 참조. 운영·채점 권한은 48건 전체 **HOLD**.

## 범위와 구분

- 직전 보고서 10건을 제외한 **정확히 38건**을 각각 공식 제조사·표준/기관 문서 원문과 비교한 **2차 기술 검토**. Fact ID 중복/누락 체크 결과 38=48−10.
- CORROBORATED = 출처에 직접 원리가 나와 있거나 물리적·단위관계로 합리적으로 도출 가능. QUALIFY = 원리는 대체로 맞지만 조건을 명확히 하거나 독립 원문 세부 대조가 더 필요. EVIDENCE_GAP = 본 단계에서 해당 일반화의 직접 근거 미확보.
- **모든 결과는 기술 문장 검토일 뿐** approved Registry / Fact Anchor 적격성·원본 quote/locator·promotion ledger byte-hash·generated freshness·채점 승인 여부와 별개. 전수 38행을 '모두 출처 확정'이라 표기하지 않는다.
- NASA/WMO PDF 검색 추출내용은 일부 확인됐으나 NASA PDF screenshot은 cache miss, WMO 관련 페이지 screenshot은 cache miss. 따라서 이를 검증 완료 근거로 취급하지 않고 해당 행은 EVIDENCE_GAP 또는 QUALIFY로 분류.
- 본 변경에서 pytest, release_candidate validate, 운영 배포, 병합 실행 **없음**.

## 각 Anchor별 기술 판정 (38건)

| # | Fact Anchor ID | 기술 검토 | 원문 대비 근거/조건·반례 | 공식 자료 |
|---:|---|---|---|---|
| 1 | `fsrm_markov_state_transition` | EVIDENCE_GAP / **HOLD** | CTMC 전이율 대 DTMC 전이확률 구분 필요. 이번에 마르코프 신뢰도 모델의 이 구별을 직접 보여주는 독립 HTML 원문 대조 미완료; NASA PDF는 화면 확인 실패. | 원문 확증 미확보 |
| 2 | `fsrm_markov_complexity` | EVIDENCE_GAP / **HOLD** | 상태 수 증가에 따른 계산/검증 복잡성은 합리적이나 모델 종류/상태 집계 조건까지 다루는 독립 원문 근거 미확인. 자동 승인 금지. | 원문 확증 미확보 |
| 3 | `fsrm_model_assumption_documentation` | QUALIFY / **HOLD** | 안전 시스템 신뢰도·고장률·시험·독립성의 설계조건은 HSE 확인. '재현 가능한 모델 경계/입력/제외조건 기록'이라는 세부 문서 의무는 별도 평가 프로토콜 원문 확인 필요. | [HSE](#hse) |
| 4 | `sw10_fat_sat_relation` | CORROBORATED / **HOLD** | IEC62381:2024 FAT 출하 전과 SAT 설치 후의 시험 단계·범위 구분, 프로젝트별 시험계획. FAT 통과가 현장 시험 조건을 자동 대체한다는 주장 방지. | [IEC81](#iec81) |
| 5 | `sw10_loop_test` | CORROBORATED / **HOLD** | IEC62382:2024 §4-5에서는 완성된 현장 루프/하드웨어·배선·소프트웨어 확인. 감시 전용 루프에는 final element가 없을 수 있음. 모든 루프에 actuator 필수라고 채점하지 않음. | [IEC82](#iec82) |
| 6 | `relative_humidity_definition` | CORROBORATED / **HOLD** | Vaisala Part 1 'Relative humidity': 실제 수증기분압 대 포화증기압의 백분율. 기준은 동일 온도. | [VAI1](#vai1) |
| 7 | `rh_temperature_dependence` | CORROBORATED / **HOLD** | Vaisala Part 1/2 'Heating air from 20 to 30°C': 수분 첨가·제거가 없는 경우 포화압 증가에 의한 RH 하락. 센서/환경 온도차 오류는 HM70 참고. | [VAI1](#vai1), [VAI2](#vai2), [VAIT](#vait) |
| 9 | `dew_point_definition` | CORROBORATED / **HOLD** | Vaisala Part 1 'Dew point': 포화 도달 후 물 응축. 주어진 압력에서 냉각 경로에 대한 정의. 얼음 표면 기준과 혼동하지 않음. | [VAI1](#vai1) |
| 10 | `frost_point_distinction` | CORROBORATED / **HOLD** | Vaisala Part 1 'Dew point and frost point' 및 HM70 기기 Td/f 표기: 영하 ice 기준 frost vs water 기준 Td. 영하 이슬점과 서리점을 무조건 동일시하지 않음. | [VAI1](#vai1) |
| 11 | `pressure_dew_point_effect` | CORROBORATED / **HOLD** | Vaisala Part 2 Scenario 2: 같은 수분 함량이어도 압축 시 수증기분압과 Td 상승. 압력 조건 없이 다른 압력 기준 Td 비교 금지. | [VAI2](#vai2) |
| 12 | `capacitive_polymer_principle` | CORROBORATED / **HOLD** | HUMICAP technology: 고분자 흡탈습→유전체 특성→정전용량 변화→습도 신호. | [VAIC](#vaic) |
| 13 | `resistive_humidity_principle` | CORROBORATED / **HOLD** | Vaisala humidity sensor history: 저항 변화를 이용하는 재료/센서 사례. 개별 저항식의 이온전도 메커니즘은 보편 사실로 승격하지 않음. | [VAIR](#vair) |
| 14 | `psychrometric_wet_dry_bulb` | QUALIFY / **HOLD** | NOAA NWS psychrometer: 건구/증발냉각 습구, 통풍 조건 명확. 습구≠이슬점은 정의상 타당. 심지·물 순도·대기압의 정확 적용 조건은 WMO No.8 4.2 원문 화면 재확인 필요. | [NOAA](#noaa) |
| 15 | `condensation_sensor_temperature_error` | CORROBORATED / **HOLD** | Vaisala HM70 온도차 오류: 1°C 차이가 RH 수 % 오류 가능, 작은 온도차로 응축. 국소 냉각된 표면 T ≤ Td 원리 확인. | [VAIT](#vait), [VAIP](#vaip) |
| 16 | `low_humidity_dew_point_selection` | CORROBORATED / **HOLD** | Vaisala Part 1 'low humidity levels': RH 산출 불확도, 직접 dew/frost point 측정 유리. '필수'가 아닌 범위/불확도 의존 선택 유지. | [VAI1](#vai1) |
| 17 | `selection_environment_process` | CORROBORATED / **HOLD** | Vaisala 장비 선택 가이드: 온도/압력/응축/오염/설치/유해환경별 요구 조건 차이. 방폭 인증은 현장 분류와 제품별 조건 확인 대상. | [VAIS](#vais) |
| 18 | `feedback_sensitivity_functions` | CORROBORATED / **HOLD** | MathWorks Loop Shaping §Loop Shapes: S=(I+L)^-1, T=I-S. 스칼라 표준 negative feedback의 S+T=1. MIMO에는 단위행렬 I를 사용. | [MATH1](#math1) |
| 19 | `feedback_parameter_sensitivity` | CORROBORATED / **HOLD** | MathWorks Feedback Amplifier Design: relative closed-loop gain sensitivity to open loop gain =1/(1+L). H 고정 표준 구조에서 G와의 상대 민감도에 대응. ;L;≫1 인 대역 근사만 허용. | [MATH2](#math2) |
| 20 | `feedback_disturbance_noise_paths` | CORROBORATED / **HOLD** | MathWorks disturbance/noise 신호 분리. 단위 음의 피드백에서 y=PC(r−y−n)+d로 정리하면 y=S d−T n+T r (수식 직접 유도, 자료의 부호 convention 검토). 다른 주입위치에는 동일 전달함수 강제하지 않음. | [MATH4](#math4), [MATH1](#math1) |
| 21 | `feedback_steady_state_error_final_value` | CORROBORATED / **HOLD** | UW Lecture 4 Final Value Theorem: sE(s)의 모든 극이 LHP이고 limit 존재해야 함. 약분으로 감춰진 내부 불안정 모드까지 닫힌루프 안정 보장으로 해석하지 않음. | [FVT](#fvt) |
| 22 | `feedback_integral_action_tradeoff` | QUALIFY / **HOLD** | MathWorks PID anti-windup guidance: 포화 시 windup; 적분기 추가는 정상상태 오차 개선 가능하지만 phase margin 감소는 항상 일어나는 필연적 결과 아님. '위상여유 변화/안정도'로 수정 권고. | [MATH3](#math3) |
| 23 | `bourdon_forms_application` | CORROBORATED / **HOLD** | WIKA Bourdon gauge: 탄성변형 C형·helical·spiral 존재, 압력범위 형상/재질 조건별 선정. | [WIKAB](#wikab) |
| 24 | `diaphragm_deflection_principle` | CORROBORATED / **HOLD** | WIKA diaphragm gauge 원리: 압력으로 막 변위가 생겨 기계식 지시로 변환. 전자식 변환은 구현별, 작은 변형 범위에서 감도·강성 설계 조건 필요. | [WIKAD](#wikad) |
| 25 | `diaphragm_sensor_vs_seal` | CORROBORATED / **HOLD** | WIKA diaphragm seal FAQ: seal 격리/충전액/모세관 온도·응답 오차. 측정 센싱막과 공정 격리막 기능 구별. | [WIKAS](#wikas) |
| 26 | `piezoresistive_static_capability` | QUALIFY / **HOLD** | TE: piezoresistive bridge 출력, 여기·증폭 필요. Kistler는 piezoelectric도 제한된 준정적 측정 가능하다고 명시함. 단문을 '압전식 정압 계측 절대 불가'로 해석하지 않도록 수정 권고. | [TE](#te), [KIST](#kist) |
| 27 | `dp_transmitter_two_port_principle` | CORROBORATED / **HOLD** | Emerson differential pressure transmitter에서 high/low equal pressure zero trim. ΔP=PH−PL 부호 정의. 실제 정압 공통모드에 따른 비영점 오류는 예외로 둠. | [EMERDP](#emerdp) |
| 28 | `ambient_environment_hazardous_selection` | CORROBORATED / **HOLD** | HSE System Integrity: 온도·습도·EMR/EMC·진동·위험환경; 계장 선정을 사용조건에 맞추어야 함. IP/방폭의 특정 인증 등급은 일반 Fact로 단정하지 않음. | [HSE](#hse) |
| 29 | `accuracy_total_performance_terms` | QUALIFY / **HOLD** | WIKA 압력계 제품별 정확도 등급·온도 오류 표기, Emerson 설치/line pressure 영향 사례는 확인. 'reference accuracy'에 포함되는 기여항목의 정확한 정의는 제조사/모델별이므로 단일 표준 합산식 강제 금지. | [WIKAB](#wikab), [EMERDP](#emerdp) |
| 30 | `pulse_frequency_speed_equation` | CORROBORATED / **HOLD** | NI Encoder How-To: x1/x2/x4 유효 count/rev. 단위상 f[count/s]와 N_eff[count/rev]일 때 n=60f/N_eff. 물리 A 채널 주파수를 f에 넣으면 x4 N_eff를 그대로 쓰지 않음. | [NIE](#nie) |
| 31 | `counting_window_speed_equation` | CORROBORATED / **HOLD** | NI Making Accurate Frequency Measurements: 고정창 카운트 m/Δt와 ±1 count 양자화, 저주파 분해능 저하. rpm=60m/(N_eff Δt) 계산 유도. | [NIF](#nif) |
| 32 | `period_measurement_low_speed` | CORROBORATED / **HOLD** | NI Frequency Measurement: 저주파 단일 주기와 기준 timebase, 역주기 방식, 시간축 카운트 오차; Tc가 유효 이벤트 간 기간이어야 함. | [NIL](#nil), [NIF](#nif) |
| 35 | `absolute_encoder_principle` | CORROBORATED / **HOLD** | OMRON FAQ01001: 위치 코드 기반 절대형, 증분 카운트와 구별. 샘플간 변화량/Δt 속도 산출은 위치 샘플이 동일 프레임이며 wrap 해소된 경우에 한함. | [OMRON](#omron) |
| 37 | `inductive_proximity_principle` | CORROBORATED / **HOLD** | ifm Inductive Technology: 발진 자계, 금속 표적 와전류, 감지 변화. 기어톱니 이벤트율→회전속도는 검출 이벤트 수를 알아야 한다는 유도. | [IFM](#ifm) |
| 38 | `gear_tooth_speed_equation` | CORROBORATED / **HOLD** | 센서가 1회전 Z개의 이벤트를 정확히 세면 f=Z·n/60, n=60f/Z (단위 정의에서 유도). 누락톱니/다중 에지 방식은 Z_eff로 별도 정의. | [IFM](#ifm), [NIF](#nif) |
| 39 | `tachogenerator_voltage_speed_principle` | CORROBORATED / **HOLD** | Tachogenerator 제조사 기술 가이드: DC output voltage ≈ K·rpm, brushes/commutator/load에 의한 비선형성. 규정 동작범위의 근사임. | [TACH](#tach) |
| 40 | `digital_tachometer_instrument_boundary` | CORROBORATED / **HOLD** | 디지털 광학 타코미터 예는 펄스 반사·회전수 계산. NI encoder 및 ifm inductive 이벤트 입력과 구분하여, tachometer라는 이름만으로 DC tachogenerator 원리를 단정 못함. | [DTACH](#dtach), [NIE](#nie), [IFM](#ifm) |
| 46 | `thermocouple_law_of_intermediate_temperatures` | CORROBORATED / **HOLD** | OMEGA Temperature Measurement Guide 'Law of Successive Thermocouples': T1–T2 EMF + T2–T3 EMF = T1–T3 EMF, 같은 열전쌍 재료·기준 정의 조건. CJC 표준표 환산 근거. | [OMEGA](#omega) |
| 48 | `thermocouple_thermowell_installation_dynamic_error` | CORROBORATED / **HOLD** | WIKA Thermowell/Response Time: 보호관 열용량, 유속, 삽입길이·열접촉이 응답과 오차에 영향. 복사/배관 열전도는 설치 열전달 경계로 검토. | [WIKAR](#wikar), [WIKAT](#wikat) |

## 우선 수정 또는 추가 출처가 필요한 문장 (Fact 파일 미수정)

- **fsrm_markov_state_transition / fsrm_markov_complexity**: CTMC 전이율과 DTMC 전이확률, 상태확장 복잡도에 대한 검증 가능한 정식 기술원문 확보 후 분류. 현 단계 공식 인정 금지.
- **fsrm_model_assumption_documentation**: 재현 가능성 근거 문서와 실제 분석 가정·제외조건 요구사항의 문헌 위치 별도 확인. 일반론으로 과장하지 않는다.
- **psychrometric_wet_dry_bulb**: 기상 관측 가이드의 심지 관리·통풍계수·물/얼음·압력 제약을 실제 페이지 단위 대조. Tw와 Td를 동일시하지 않는다.
- **feedback_integral_action_tradeoff**: '위상여유 감소'를 불변/필연적 결과로 쓰지 않고 '위상여유 변화 및 안정성 저하 가능성'으로 수정 후보.
- **piezoresistive_static_capability**: 압전식은 '정압을 절대 측정 불가'가 아니라 누설/드리프트로 장기간 정압 계측에 불리할 수 있으며 조건부 준정적 계측은 가능. 수정 후보.
- **accuracy_total_performance_terms**: 정확도 항목을 특정 제조사·모델과 무관한 보편 표준 합산식으로 채점하면 안 됨. 개별 데이터시트 용어 정의 확인.

## 공식 원문·절 위치

- <a id="iec81"></a> **IEC81:** IEC 62381:2024 — FAT/FIT/SAT/SIT, scope and 4.1: https://webstore.iec.ch/en/publication/67572
- <a id="iec82"></a> **IEC82:** IEC 62382:2024 — §4 Loop check schedule; §5 content: https://standards.iteh.ai/catalog/standards/iec/5291b36b-42cb-4a25-a904-223b73437ad5/iec-62382-2024
- <a id="hse"></a> **HSE:** UK HSE — Control systems / System integrity / Dependability: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
- <a id="vai1"></a> **VAI1:** Vaisala — Understanding humidity part 1, Relative humidity / Dew point / Absolute humidity: https://www.vaisala.com/en/expert-article/understanding-humidity-part-1-fundamental-concepts-every-engineer-should-know
- <a id="vai2"></a> **VAI2:** Vaisala — Understanding humidity part 2, Temperature and pressure scenarios: https://www.vaisala.com/en/expert-article/understanding-humidity-part-2-practical-measurements-every-engineer-should-master
- <a id="vaic"></a> **VAIC:** Vaisala — HUMICAP technology: dielectric properties and capacitance: https://docs.vaisala.com/r/M212259EN-D/en-US/GUID-483A8D7D-0A10-4A90-980A-CB88E2F4CD51
- <a id="vair"></a> **VAIR:** Vaisala — The importance of humidity sensors, resistive history and capacitive comparison: https://www.vaisala.com/ko/node/93646
- <a id="vait"></a> **VAIT:** Vaisala — Errors caused by temperature differences (HM70): https://docs.vaisala.com/r/M210297EN-G/en-US/GUID-9D273B5F-99DE-4C66-B8C9-644EED6833B6
- <a id="vais"></a> **VAIS:** Vaisala — How to select the right instrument for humidity / dew point: https://www.vaisala.com/pl/node/95756
- <a id="vaip"></a> **VAIP:** Vaisala — Sensor preheat (HM70), condensation: https://docs.vaisala.com/r/M210297EN-G/en-US/GUID-1034451A-60A2-4BD0-A7A7-FD5327545D8E/GUID-E9CB2FAD-1EC6-4ED0-BBB0-9AF7AD92D0DD
- <a id="noaa"></a> **NOAA:** US NOAA NWS — Psychrometer definition and ventilation: https://forecast.weather.gov/glossary.php?word=psychrometer
- <a id="math1"></a> **MATH1:** MathWorks — Loop Shaping for Performance and Robustness, S/T equations: https://www.mathworks.com/help/robust/gs/loop-shaping-for-performance-and-robustness.html
- <a id="math2"></a> **MATH2:** MathWorks — Feedback Amplifier Design, relative gain sensitivity: https://se.mathworks.com/help/control/ug/feedback-amplifier-design.html
- <a id="math3"></a> **MATH3:** MathWorks — Improve PID Design to Handle Plant Constraints, Anti-Windup: https://www.mathworks.com/help/slcontrol/ug/improve-pid-to-handle-plant-constraints.html
- <a id="math4"></a> **MATH4:** MathWorks — Simultaneous Stabilization Using Robust Control, d/n paths: https://www.mathworks.com/help/robust/ug/simultaneous-stabilization-using-robust-control.html
- <a id="fvt"></a> **FVT:** University of Washington — Lecture 4 Laplace Transform / Final value theorem: https://faculty.washington.edu/chx/teaching/fbintro/lec04-laplace-transform/
- <a id="wikab"></a> **WIKAB:** WIKA — Bourdon Tube Pressure Gauge: C, spiral, helical: https://www.wika.com/en-us/lp_bourdon_tube_pressure_gauge.WIKA
- <a id="wikad"></a> **WIKAD:** WIKA — Diaphragm pressure gauges and deflection: https://blog.wika.com/us/knowhow/what-is-a-diaphragm-pressure-gauge-and-how-does-it-work/
- <a id="wikas"></a> **WIKAS:** WIKA — FAQ diaphragm seal system fill, capillary, temperature effects: https://www.wika.com/en-us/faq.WIKA
- <a id="wikat"></a> **WIKAT:** WIKA — Thermowell installation best practices: https://blog.wika.com/us/knowhow/where-should-i-install-my-thermowell-guide-for-best-practices/
- <a id="wikar"></a> **WIKAR:** WIKA — Temperature measurement response time, thermowell mass and velocity: https://blog.wika.com/us/knowhow/instruments-for-electrical-temperature-measurement-how-to-choose-the-right-one-part-1/
- <a id="kist"></a> **KIST:** Kistler — Static pressure measurement with PE vs piezoresistive: https://www.kistler.com/INT/en/piezoelectric-pressure-sensors-with-charge-output-pe-for-static-pressure-measurement/C00000140
- <a id="te"></a> **TE:** TE Connectivity — Pressure Transducer FAQs, piezoresistive bridge/supply: https://www.te.com/en/products/sensors/pressure-sensors/resources/faqs-pressure-transducers.html
- <a id="emer"></a> **EMER:** Emerson — Rosemount 4051S Manual, Equalizing and zero trim: https://www.emerson.com/en/measurement-instrumentation/catalog/pressure-measurement/4051s-manual
- <a id="emerdp"></a> **EMERDP:** Emerson — Differential Pressure Level Transmitter, zero trim at equal pressures: https://www.emerson.com/en-us/automation/measurement-instrumentation/pressure-measurement/about-differential-pressure-dp-level-measurement/about-rosemount-3051s-differential-pressure-dp
- <a id="nif"></a> **NIF:** NI — Making Accurate Frequency Measurements, 3 methods: https://www.ni.com/en/support/documentation/supplemental/06/making-accurate-frequency-measurements.html
- <a id="nie"></a> **NIE:** NI — Hardware Encoder Measurements How-To, x1/x2/x4 count: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1riCAA
- <a id="nil"></a> **NIL:** NI — Frequency Measurement, low-frequency period and gate counting: https://www.ni.com/docs/en-US/bundle/pcie-pxie-6343/page/counter-input-frequency-measurement.html
- <a id="ifm"></a> **IFM:** ifm — Inductive technology, oscillating EM and eddy currents: https://www.ifm.com/us/en/us/learn-more/inductive/compact-inductive-sensors/technology
- <a id="omron"></a> **OMRON:** OMRON — FAQ difference incremental and absolute encoder: https://www.ia.omron.com/support/faq/answer/34/faq01001/
- <a id="tach"></a> **TACH:** Transdrive Engineering — Tachogenerators Guide: Magnets Used / Linearity: https://www.tachogeneratorsguide.com/magnets-used
- <a id="dtach"></a> **DTACH:** TASI — Digital Tachometer: optical reflection and RPM: https://www.china-tasi.com/en/resourceCenterDetail/144aaa46e5184303968659c9eb25ef4b/
- <a id="omega"></a> **OMEGA:** OMEGA Engineering — Temperature Measurement Guide / Law of Successive Thermocouples: https://www.jp.omega.com/techref/measureguide.html

## 채점 안전 경계 / 후속 검증

- 48건 전체 기술 검토의 최신 기록은 '이 파일 38건 + 직전 파일 10건'의 **2문서**. 독립 원문 확증 미완료 Fact는 보류이며 나머지도 `SUPPORTED` 자동 승격이 아니다.
- 금지: Registry 단문 자동 동기화, ledger SHA 기계적 갱신만으로 증빙 승인, generated stale 상태에서 score parity PASS 선언, S7 A/B/C 점수 자동 허용.
- 해결 전 미완료: 기존 3 Registry exact-statement mismatch, 2 ledger source hash mismatch, generated freshness, 전체 pytest와 Release Gate. Draft PR 유지.
