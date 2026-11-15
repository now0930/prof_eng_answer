# PR #38 Fact Anchor 단문화 2차 검토 — 2026-11-15

**상태: 검토 기록 전용 / 48건 모두 HOLD / 승인 0건 / 신 HEAD 테스트 실행 0건.** 검토 기준: d81617a7cf270bdfdfdf12079b27e12bba5daba4. 이전 원문·단문 쌍은 [48행 원본 감사](../calibration/fact_anchor_simplification_review_20261114.json) 참조.

## 1. 소스 변경 범위 정정

기준 SHA 09e4b1c7347c330b6196be695a4c0ac3a091531d 대비 7개 Topic의 48개 Anchor 변경 필드를 JSON key 단위로 재대조했다. 48개 statement만 바뀐 것이 **아니며**, 다른 key도 의도적으로 동기화되어 있다.

| Topic | statement | expected | claim | description | accepted_explanations |
|---|---:|---:|---:|---:|---:|
| 기능안전 신뢰도 | 3 | 3 | 3 | 3 | 2 |
| FAT/SAT·Loop | 2 | 0 | 0 | 0 | 2 |
| 습도 | 12 | 0 | 12 | 12 | 12 |
| 피드백 | 5 | 0 | 5 | 5 | 5 |
| 압력 | 7 | 0 | 7 | 7 | 7 |
| 회전속도 | 11 | 0 | 11 | 11 | 11 |
| 열전대 | 8 | 0 | 0 | 0 | 8 |
| **합계** | **48** | **3** | **38** | **38** | **47** |

기능안전 1건은 이전 문장이 이미 accepted_explanations에 포함되어 추가 변경이 없었다. 48개 후보 Anchor 이외의 root 필드, ID, weight 및 다른 Anchor 변경은 없었다. 이는 구조 대조일 뿐 기술적 검증이 아니다.

## 2. Generated 전후 영향

- scripts/build_generated_rubrics.py의 content_version(54~70행)은 builder 코드와 전체 대상 Topic JSON에서 하나의 통합 SHA-256 version을 만든다. 이 version이 **6개 Generated 파일 모두**에 기록된다(811~844행).
- build_fact_anchors(219~263, 335~365행)는 expected를 우선하며, 없으면 statement 등으로 정규화한 다음 그 **전체 문장과 추출 단어**를 triggers에 포함한다. 따라서 단문 48건은 단순 주석 변경이 아닌 잠재적인 routing trigger 변화다.
- 원격 Git tree의 09e4b1c7 대비 7개 Topic source만 변경. 동일 기준의 builder, generated 6개 JSON, approved Fact Registry, promotion ledger는 **각 Git blob이 정확히 동일**하다. 이는 이전 관찰된 Generated freshness 실패와 모순되지 않으며, 어떤 새 HEAD의 runtime PASS를 증명하지 않는다.
- 48개의 이전/신규 문장에서 builder의 어휘 추출 정규식으로 토큰 차이가 발생함을 확인했다. **정적 어휘 후보의 변화량은 실제 routing/score 오차 지표가 아니다.**
- tests/test_fact_anchor_simplification_batch.py는 48개 현재 단문을 명시적으로 기대한다. 승인 불일치를 숨기기 위해 기존 테스트를 약화시키거나 7개 Topic을 무조건 원복하면 새 테스트 계약이 깨진다.

## 3. 독립 원문·정확 locator의 1차 확인

아래는 작성자가 직접 발행한 공식 공개 자료의 부분 주장 근거 확인이다. 원문과 단문의 **전체 기술적 동등성, 채점 적용, 안전한 routing/coverage**를 승인한 결과가 아니며, 모두 최종 HOLD다.

| Anchor ID | 발행자/원문 locator | 1차 명제 대조 · 제한 |
|---|---|---|
| fsrm_markov_complexity | NASA NTRS, [NASA-CR-188288 Abstract](https://ntrs.nasa.gov/citations/19940028356) | 상태공간 증가에 따른 메모리/CPU 부담의 모델 의존성을 지지. PDF 원문 screenshot 실패로 시각 확인 미완료 |
| fsrm_markov_state_transition | NASA NTRS, [Non-homogeneous Markov model Abstract](https://ntrs.nasa.gov/citations/19900039580) | 시간·상태 의존 전이율은 특정 모델 확장 사항이며 모든 모델 필수조건 아님 |
| fsrm_model_assumption_documentation | HSE, [Proof Testing Requirements Appendix 1](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf), PFD Calculations 2~8; [Appendix 2](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf), Auditing 6~7 | 실제 고장자료·시험주기·수리시간·모델 가정을 명시하는 취지. PDF 텍스트만 확인, 화면 screenshot 실패로 **시각 원문 최종 확인 보류** |
| sw10_fat_sat_relation | Siemens, [Virtual commissioning](https://blog.siemens.com/2022/03/reduce-cost-time-and-risk-with-a-virtual-simulation-environment/), FAT/SAT | 구별되는 시험단계임은 지지. '두 시험 모두 필수'는 승인 프로젝트 시험계획에 종속 |
| sw10_loop_test | Emerson, [Rosemount 3144S Manual](https://www.emerson.com/en/measurement-instrumentation/catalog/temperature-measurement/3144s-manual), 2.6 Loop Test | 배선·출력·recorders 검증 사례. 모든 모니터링 Loop에 최종 제어요소가 있다는 해석 금지 |
| relative_humidity_definition | Vaisala, [HM40 Parameters](https://docs.vaisala.com/r/M211088EN-D/en-US/GUID-F1EB60A0-9D47-4257-B24D-142DAE551AFA?contentId=1jWtV0_40n8awBaQvQP5vw), Relative humidity | 같은 온도의 실제 수증기 분압/포화수증기압 비 |
| absolute_humidity_definition | Vaisala, [HMP155 Calculation formulas](https://docs.vaisala.com/r/M210912EN-J/en-US/GUID-8F8C9ECE-FFD9-4F6F-9F11-D94CF9122735), Equation (3) | 수증기 분압과 온도의 이상기체 관계; 온도 K 및 단위 변환 필요 |
| dew_point_definition | Vaisala, HM40 Parameters, Dewpoint | 현 압력에서 물 응축이 시작되는 온도; 서리점 구분 |
| frost_point_distinction | Vaisala, HMP155 Calculation formulas, Eq. (5~8) | 물/얼음 포화압 구별 |
| psychrometric_wet_dry_bulb | Vaisala, HM40 Parameters, Wet bulb | 증발냉각 정의만 확인, 통풍·심지·압력의 식 검증 미완료 |
| feedback_sensitivity_functions | MathWorks, [Loop Shaping](https://kr.mathworks.com/help/robust/gs/loop-shaping-for-performance-and-robustness.html), S and T equations | S=(I+L)^-1, T=L(I+L)^-1, S+T=I; S+T=1은 SISO |
| diaphragm_sensor_vs_seal | WIKA, [FAQ](https://www.wika.com/en-us/faq.WIKA), diaphragm seal fill fluid and temperature questions | 격리용 seal의 충전액·모세관 및 온도 오차와 감지용 막 구분 |
| quadrature_direction_principle | OMRON, [Encoder Terms](https://www.ia.omron.com/support/guide/34/explanation_of_terms.html), Output Phase Difference | A/B 정상 90° 전기각. x4 수신 처리율은 별도 검증 |
| index_z_channel_role | OMRON, Encoder Terms, Output Phase | Z 기준 신호 1회/회전. Z 단독으로 다회전 absolute position 불가 |
| encoder_frequency_limit_selection | OMRON, [Encoder Selection](https://www.ia.omron.com/support/guide/34/introduction.html), Selection Guidelines [6] Maximum Response Frequency | **REVISE_CANDIDATE**: 출력 channel 주파수와 수신기 x4 계수 이벤트율을 한 한계로 묶으면 안 됨 |
| thermocouple_reference_junction_compensation | Analog Devices, [AN-28](https://www.analog.com/en/resources/app-notes/an-28f.html), Cold Junction Compensation, Figs 5~7 | **REVISE_CANDIDATE**: 별도 온도센서 추종은 한 CJC 구성; ice bath/제어식 기준접점은 별도 구성 |
| thermocouple_nonlinearity_reference_tables_polynomial_conversion | NIST, [NIST 60 ITS-90 Thermocouple Database](https://www.nist.gov/publications/nist-60-nist-its-90-thermocouple-database), Abstract | 열전대 유형별 표준 기준 함수 존재 확인; 온도범위·다항식 계수 개별 대조는 보류 |

위 **17건**은 특정 원문 항목에 대한 부분 근거 대조만 완료했다. 전체 48개 원문/수정문 검토 목록과 미확인 조건은 [1차 보고서](pr38_fact_anchor_48_technical_triage_20261115.md)에 보존되어 있다.

## 4. 기존 사실 수정 후보 — 현재 원천에 미적용

**encoder_frequency_limit_selection**

증분형 엔코더의 출력 채널 주파수는 회전속도와 회전당 출력 펄스 수로 산정해 센서의 정격과 비교하고, 수신기의 x1/x2/x4 계수 이벤트 처리율은 별도로 검증한다.

예: PPR=1000, 3000 rpm이라면 출력 A 채널 주파수는 50 kHz, x4 수신 이벤트는 초당 200,000회다. 각각 다른 처리 한계다.

**thermocouple_reference_junction_compensation**

온도추종형 전자식 열전대 냉접점 보상에서는 기준접점의 온도를 별도 센서로 측정하고 열전대 종류별 보상 기전력을 적용해 측정접점 온도로 환산한다.

이 항목은 ice bath 등 모든 기준접점 구현을 설명하지 않는다. 단자·온도센서 등온성은 원문에서 설명/조건으로 유지하는 방향을 검토한다.

## 5. Release 및 Fact 승인 보류 경계

현 원격 HEAD에서 pytest, Topic 통합 검증, Generated rebuild, Release Validation **신규 실행 없음**. 이 환경은 GitHub Connector로 리포지토리를 읽을 수 있으나 독립 shell container에서는 github.com DNS가 해석되지 않아 clone할 수 없다. 독립적으로 검증되지 않은 문장 승격·registry 수정을 하지 않았으며 승인 ledger를 해시만 맞춰 재작성하지 않았다. 테스트 격리/약화, scoring exclusion 삭제, main merge, 운영 bot 수정·배포·재시작도 없음.

기능안전 Registry/Topic statement 불일치 3건, ledger source-hash 2건, Generated freshness 2건과 routing·coverage·점수·WRONG/Fatal/중복 가점의 동등성은 **실행 근거를 갖춘 해소가 아님**. C5/C7/C8/D2/D3 체크박스를 계속 OPEN으로 유지한다.
