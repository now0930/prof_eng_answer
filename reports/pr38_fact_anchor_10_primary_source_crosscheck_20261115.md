# PR #38 — Fact Anchor 원문 대조 2차: 선별 10건 (2026-11-15)

> 검토 전용. TECHNICALLY_CORROBORATED는 기술 근거 부합을 뜻하며 Fact Registry 승인·채점 적격성·배포를 의미하지 않는다. 전체 48건 운영 HOLD 유지.

## 검토 근거 및 판정

| Anchor ID | 결과 | 공식 근거의 정확한 위치 |
|---|---|---|
| absolute_humidity_definition | 원리 부합 / HOLD. 단위체적당 수증기 질량, 이상기체 근사, 절대온도(K) 필요 | Vaisala HMT130/TMT130 User Guide, Absolute humidity calculation: a=C·Pw/(T+273.15), 여기서 T는 °C |
| quadrature_direction_principle | 원리 부합 / HOLD. A/B 90° 전기각, 선행 채널과 방향, x2/x4 복호 | OMRON Rotary Encoders, Explanation of Terms: Output Phase Difference, CW; Introduction: Features |
| index_z_channel_role | 원리 부합 / HOLD. Z 채널 일반적 1회전당 1회, 단독 다회전 절대위치 불가 | OMRON Explanation of Terms: Output Phase; FAQ00946 |
| thermocouple_measures_temperature_difference | 원리 부합 / HOLD. 측정 및 기준접점 온도 모두 필요 | Analog Devices, Cold Junction Compensation in Thermocouple Guide: Introduction |
| thermocouple_reference_junction_compensation | **REVISE_REQUIRED / HOLD**. 별도 온도센서 기반 보상은 구현 사례이지 보상 개념의 유일한 방식은 아님. 0°C 기준접점도 가능 | Analog Devices, Basics of Thermocouples: Measuring Cold Junction Temperature; AN-28: Cold Junction Compensation |
| thermocouple_law_of_intermediate_metals | 원리 부합 / HOLD. 제3 금속 두 접속부 등온이 필요 | Analog Devices AN-274: LAW OF INTERMEDIATE METALS, Fig 1c |
| thermocouple_nonlinearity_reference_tables_polynomial_conversion | 원리 부합 / HOLD. 형식별 ITS-90 비선형 EMF-온도 관계·표/다항식 | NIST Monograph 175, NIST 60 ITS-90 Thermocouple Database |
| encoder_frequency_limit_selection | **REVISE_REQUIRED / HOLD**. 엔코더 채널 주파수와 수신기 x4 계수 이벤트 처리율 구별 | OMRON Introduction: Selection Guidelines [6] Maximum Response Frequency; Features: 4-multiplier |
| thermocouple_seebeck_effect_dissimilar_conductors | 원리 부합 / HOLD. 재료별 기전력 및 비선형성 | Analog Devices AN-28 Figures 3,4; NIST Monograph 175 |
| thermocouple_temperature_measurement_chain | 원리 부합 / HOLD. EMF 측정, 기준접점 처리, 종류별 온도 환산; 실제 0°C 기준접점은 전자식 보상 불필요 | Analog Devices Cold Junction Compensation Guide: Introduction; NIST Monograph 175 |

## 수정 제안 (Fact 파일 및 Registry에는 반영하지 않음)

**encoder_frequency_limit_selection**

엔코더 선정 시 최대 회전속도와 채널당 PPR로 출력 채널 주파수 f_channel=n_max·PPR/60을 확인한다. 수신 카운터·PLC는 x1/x2/x4 복호에 따른 유효 계수 이벤트율과 입력 신호 주파수 사양을 각각 검토한다. 단, PPR 정의는 해당 엔코더 데이터시트에 따른다.

**thermocouple_reference_junction_compensation**

열전대 기준접점 온도 영향은 알려진 기준온도(예: 0°C)를 유지하거나 전자식 냉접점 보상에서 기준접점 온도를 센서로 측정해 해당 기전력을 보정하여 처리한다. 전자식 보상에서는 센서 위치와 단자 온도구배가 오차원이 된다.

## 공식 문서 URL

- Vaisala Absolute humidity: https://docs.vaisala.com/r/M211280EN-E/en-US/GUID-6454B70E-2FB0-437D-8D3E-0DA8A5AD35D2
- OMRON Introduction: https://www.ia.omron.com/support/guide/34/introduction.html
- OMRON Explanation of Terms: https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- OMRON Z FAQ: https://www.ia.omron.com/support/faq/answer/34/faq00946/
- ADI Cold Junction Guide: https://www.analog.com/en/resources/technical-articles/cold-junction-compensation-in-thermocouple-guide.html
- ADI Basics: https://www.analog.com/en/resources/design-notes/2022/07/16/12/19/the-basics-of-thermocouples.html
- ADI AN-28: https://www.analog.com/en/resources/app-notes/an-28f.html
- ADI AN-274: https://www.analog.com/media/en/technical-documentation/application-notes/an-274.pdf
- NIST Monograph 175: https://www.nist.gov/publications/temperature-electromotive-force-reference-functions-and-tables-letter-designated
- NIST 60: https://www.nist.gov/publications/nist-60-nist-its-90-thermocouple-database

## 안전 경계 및 미완료

- 정확히 위 10건만 공식자료와 대조: 8건 원리 부합, 2건 수정 필요. 48건 전수 완료 아님.
- 기술적 부합은 기존 Registry statement exact-match, 원문 quote/locator 대조, Ledger source byte SHA, generated freshness 또는 최종 채점 승인과 별개.
- 원격 GitHub 내용을 읽었으나 pytest와 release_candidate.py validate는 **실행하지 않았음**. 해당 SHA의 PASS를 선언하지 않는다.
- Topic Pack, Registry, generated, 채점 코드와 운영 서비스, PR draft/merge 상태는 변경하지 않는다.
