# PR #46 Registry 검토 및 승인 대상 문장

기준 `c8f21e8ece3e71b51394d8c75b25e70d8173a4fd`. 기존 Registry 행은 [승인 Registry](../grading/evidence/approved_fact_registry.json)의 정확한 Fact ID로 추적한다. 아래 다섯 문장은 2026-11-25 기술 검토를 마친 승인 권고 문안이다. 실제 승인은 대기 중이다. 승인 시 이 문서의 커밋과 정확한 Fact ID·문장을 참조하여 기존 절차에서 검토자·근거·승인 이력을 기록한다. 레거시 Topic Pack 관리 및 기존 승격 절차는 [Topic Pack workflow](../docs/topic_pack_workflow.md)와 [Fact Anchor eligibility](../docs/fact_anchor_eligibility_policy.md)를 따른다.

## 기술 검토 승인 권고 5건

### 1. encoder_frequency_limit_selection

- Registry ID `encoder_speed_and_decode_rate_must_fit_frequency_limits`. 기존 문구는 다음과 같다.

  > For an incremental encoder with N_eff decoded counts per revolution at n rpm, the count-event rate is f=n·N_eff/60 counts/s. Encoder output electronics and the receiving counter/input each have finite frequency or pulse-width limits; the selected maximum speed and decode mode must remain within both applicable limits. Increasing decoded counts/revolution increases event rate at the same shaft speed.

- **승인 대상 문장**

  증분형 엔코더가 `n` rpm으로 회전하고 PPR이 채널의 회전당 신호 주기 수를 뜻할 때, 채널 출력 주파수는 `n·PPR/60` Hz이고 수신기의 유효 계수율은 `n·N_eff/60` count/s이다. 최대 회전속도와 선택한 복호 모드에서 엔코더 출력 한계, 수신기 입력 주파수·펄스폭 한계, 사양에 명시된 내부 계수 처리 한계를 각각 확인한다.
- PPR의 제조사 정의와 `N_eff`의 복호 기준을 확인한다. 복호 모드는 수신기의 이벤트율 및 허용 입력 사양에 영향을 줄 수 있다. 특정 모듈의 수치 한계는 해당 모델에만 적용한다. [Rockwell 1746-UM002B, Counting relationship 및 Input Frequency](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1746-um002_-en-p.pdf)

### 2. gear_tooth_speed_equation

- Registry ID `rotation_speed_tooth_event_frequency_relation`. 기존 문구는 다음과 같다.

  > If there are Z effective target events per revolution and each event produces one counted pulse, pulse frequency f in hertz and rotational speed n in rpm satisfy n = 60f/Z. Z must reflect the actual counted events per revolution, including edge multiplication or missing-tooth patterns as applicable.

- **승인 대상 문장**

  한 회전 또는 정수 회전에서 측정한 이벤트 평균 주파수가 `f` Hz이고 회전당 유효 이벤트 수가 `Z`이면 평균 회전속도는 `60f/Z` rpm이다. 결손치를 포함한 두 검출 에지 사이의 구간 평균 회전속도는 실제 회전각을 경과 시간으로 나누어 환산한다.
- 실제 감지 이벤트와 계수 모드가 `Z`에 반영돼야 한다. 국부 계산에서 각도를 rad로 쓰면 rpm은 `60Δθ/(2πΔt)`이다. 결손치 각간격에 대한 일반화는 예시 휠 형상과 각속도 정의를 결합한 운동학적 도출이다. [MathWorks, Internal Combustion Engine Ignition Control, toothed-wheel description](https://blogs.mathworks.com/simulink/2018/11/07/internal-combustion-engine-ignition-control-example-part-1/)

### 3. incremental_encoder_principle

- Registry ID `incremental_encoder_reports_displacement_relative_to_reference`. 기존 문구는 다음과 같다.

  > An incremental encoder represents shaft movement as pulses/count transitions relative to a reference; an external counter/controller accumulates those transitions to obtain relative position and can derive speed from pulse timing. Unless the accumulated count is retained through power loss or re-established by a reference/homing procedure, an incremental output alone does not identify the shaft's absolute position after restart.

- **승인 대상 문장**

  증분형 엔코더의 펄스를 기준 위치부터 누적하면 상대 변위를 구할 수 있다. 전원 차단 동안 계측하지 못한 이동은 저장 계수값으로 복원할 수 없으며, 위치를 복구하려면 계수의 연속성을 확인하거나 원점 복귀 등으로 기준을 다시 확립해야 한다.
- 계수의 연속성에는 전원 차단 중 미계측 이동이 없고 저장값이 무결한 경우가 포함된다. 특정 드라이브의 복전 동작은 일반 법칙으로 승격하지 않는다. [Rockwell Sensor Technology and Application Basics, Incremental Encoders](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/c117-rm001_-en-p.pdf) · [Rockwell Kinetix 300, Homing Methods](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/2097-um001_-en-p.pdf)

### 4. thermocouple_measures_temperature_difference

- Registry ID `thermocouple_measures_temperature_difference`. 기존 문구는 다음과 같다.

  > 열전대 전압은 측정접점과 기준접점의 온도차에 대응하므로, 절대 측정접점 온도를 구하려면 기준접점 온도를 알아야 한다.

- **승인 대상 문장**

  균질한 열전대 재료쌍과 지정 극성에서 측정접점과 기준접점의 온도를 각각 `T_m`, `T_r`로 하면, 순 열기전력은 해당 형식의 기준함수 차 `E(T_m) − E(T_r)`이다. 기준접점 온도가 고정된 경우 해당 형식의 유효 범위에서 온도차로 전압 변화를 설명할 수 있다.
- 형식별 기준함수는 기준접점 조건과 유효 온도범위를 따른다. 두 온도를 같은 크기로 이동했을 때 온도차가 같아도 전압은 일반적으로 달라질 수 있다. [NIST Monograph 175, 형식별 기준함수와 0 °C 기준접점](https://www.nist.gov/publications/temperature-electromotive-force-reference-functions-and-tables-letter-designated) · [NBS Handbook 121, Law of intermediate temperatures](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook121.pdf)

### 5. imperfect_test_residual_risk

- Registry ID `partial_testing_leaves_unrevealed_failure_modes_for_full_proof_test`. 기존 문구는 다음과 같다.

  > Imperfect proof test 후에도 검출되지 않는 dangerous failure가 남는다. Residual failure rate와 untested failure modes를 명시하고 다음 full test까지의 risk contribution을 평가한다.

- **승인 대상 문장**

  부분시험에서 드러나지 않는 위험고장은 해당 시험의 주기로 제거된 것으로 계산할 수 없다. 각 잔여 고장모드에 대해 실제 검출 후 복구할 수 있는 시험 또는 해당 모드를 제거하는 교체까지의 노출을 모델에 반영한다. 그런 조치가 정의되지 않은 운용구간에는 해당 모드의 위험 기여를 계속 반영한다.
- 완전시험 주기는 그 시험이 해당 고장을 드러내고 복구가 이뤄지는 경우에 적용한다. 시험 명칭만으로 검출률이나 복구를 가정할 수 없다. [HSE OG54 Appendix 1, §§35–43](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf) · [HSE OG54 Appendix 3, partial proof example](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf)

## 나머지 6건

| Anchor | 검토 결과 |
|---|---|
| `absolute_humidity_definition` | `absolute_humidity_is_water_vapor_mass_concentration` 유지. 습공기 체적당 수증기 질량 정의가 일치한다. 이상기체식 적용 조건과 상대습도 설명은 별도다. |
| `counting_window_speed_equation` | `encoder_fixed_window_count_to_rpm_equation` 유지. 고정 계수창과 유효 회전당 계수에서 1계수에 해당하는 절대 RPM 간격이 일정하다. 같은 간격을 저속에서 읽은 값으로 나누면 상대 비중이 증가한다. |
| `fail_action_vs_safe_state` | `final_element_safe_action_process_dependent` 및 `deenergize_trip_requires_application_safe_action_check`를 출처 참조에 사용 가능. 두 Fact의 소유권과 현재 Anchor ID를 유지한다. |
| `redundancy_independence_boundary` | 동일 소유 Topic의 `shared_dependencies_and_environment_affect_independence`를 우선 참조. 다른 소유 Topic의 `common_cause_failures_reduce_redundancy_benefit_under_independence_assumption`은 교차 근거로 사용 가능. |
| `sw04_hil` | 레거시 정본 관리 유지. 기존 Topic에 V&V 관련 Registry 행이 있으나 실제 하드웨어와 실시간 모의 플랜트의 연결에 대한 동일 관계는 확인되지 않았다. |
| `response_time_process_safety_time` | 전체 SIF 응답시간과 문서에 할당된 최종요소 시간의 구분은 아래 근거로 정리했다. 조건을 PR #46의 정본과 대응 설명에 명시했다. 현재 Registry에는 직접 대응하는 행이 없으며 별도 등록을 승인하지 않았다. |

Vaisala는 절대습도 정의와 상태변수 관계를 제시한다. NI는 일정 게이트 동안 이벤트를 세는 원리를 설명한다. [Vaisala, Absolute humidity calculation](https://docs.vaisala.com/r/M211244EN-E/en-US/GUID-6454B70E-2FB0-437D-8D3E-0DA8A5AD35D2) · [NI, Choosing a Counter Frequency Measurement Method](https://www.ni.com/en/support/documentation/supplemental/21/choosing-a-counter-frequency-measurement-method0.html)

HSE는 고장 시 장치 동작과 보호 기능의 설계 맥락 및 공통원인 예방을 설명한다. Siemens는 가상 시운전에서 실제 자동화 장비를 쓰는 HIL과 모의 제어기를 쓰는 SiL을 구분한다. [HSE, Control systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm) · [Siemens SIMIT](https://www.siemens.com/en-us/products/simit/)

### PST 근거 및 범위

exida의 SIF SRS 안내서 Chapter 8은 전체 SIF 응답시간을 PST 이내로 명시한다. ISA-TR84.00.06 §2.2.1은 감지에서 최종요소 동작 후 공정 응답까지를 전체 응답시간 검토 범위의 예로 제시한다. Emerson의 1061 안전 매뉴얼 General Requirements는 시스템 응답시간과 최종요소 서브시스템의 응답시간을 구분한다. Yokogawa SRS 안내는 공정 안전 시간과 응답시간을 요구사항에 포함한다. [exida User Guide, Chapter 8](https://www.exida.com/pub/exSILentiaUserGuide.pdf) · [ISA 기술보고서 §2.2.1](https://webstore.ansi.org/preview-pages/ISA/preview_ISA%2BTR84.00.06-2009.pdf) · [Emerson D104499X012, General Requirements](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/actuators/documents/FCV-OSI-SIL-Safety-Manual-for-Fisher-1061-Actuator-D104499X012-EN.pdf) · [Yokogawa SRS 안내](https://www.yokogawa.com/eu/solutions/products-and-services/consulting/functional-safety-consultancy-services/safety-requirement-specification-srs/)

이 근거에서 도출한 적용 문장은 다음과 같다. 전체 SIF는 해당 위험 시나리오의 PST를 넘기기 전에 요구 안전상태에 도달해야 한다. 최종요소 응답시간이 해당 SIF의 SRS나 추적 가능한 설계 시간 예산에 따로 할당된 경우 그 할당값을 별도로 검증한다. 이 조건부 설계 해석은 근거 검토를 마쳤다. 모든 SRS가 구성요소별 고정 배분값을 직접 기재해야 한다는 주장과 신규 Registry 등록은 보류한다. [Arborion SRS 설계 사례, Process Safety Time 절](https://www.arborionglobal.com/services/functional-safety-engineering/functional-safety-lifecycle/phase-3-safety-requirements-specification)
