# PR #38 — 48개 Fact Anchor 단문 초안 기술 검토 1차 분류 (2026-11-15)

> **상태: 연구·검토 보고서 (NOT APPROVED / NO SCORE CHANGE / NO RELEASE).** 검토 기준 원격 HEAD `935bc1dc9636abfcb2cf7ece6d34d53df18b6134` (Draft PR #38); 원문/수정문 쌍 정본은 [48행 보존 파일](../calibration/fact_anchor_simplification_review_20261114.json). 이 문서는 source·Registry·ledger·generated·scoring exclusion을 변경하거나 승격하지 않는다.

## 확인한 범위와 제한

- 실제 GitHub 원격 HEAD에서 Source 7 Topic의 단문 초안 48건 및 기존 Registry/ledger와 generated 현황을 읽었다. 2026-11-14 마지막 검증 SHA `09e4b1c7` 대비 7개 `fact_anchor.json` 변경, generated JSON 6개 전부 **Git blob SHA 동일**, Registry와 `reports/fact_anchor_keep_bounded_promotions_20261103.json`도 동일. 따라서 source–generated fresh rebuild/score parity는 **미검증**.
- 이전 2026-11-15 진단의 3개 승인 Registry와 새 기능안전 source statement 정확 불일치, 2개 promotion ledger source-hash 불일치가 미해결이다. `tests/test_approved_fact_registry.py::test_functional_safety_reliability_fact_matches_anchor`가 정확한 문구 일치를 요구하고 `scripts/promote_reviewed_fact_anchors.py`는 개별 근거와 **Topic 전체 source byte SHA-256**을 검사한다.
- 현재 HEAD와 연결된 PR 트리거 Actions 실행·상태 체크 **0개 확인**. 이 환경에서는 clone/network 및 pytest 실행이 불가했다. **신규 실행 수치 없음.** 기존 1,748 passed/11 failed/2 skipped는 **기준 SHA `74f6ebf` 결과**이며 현 HEAD PASS가 아니다.
- 아래 48행은 개별 **대조해야 할 기술적 조건/반례와 초기 출처 후보 목록**이다. 독립 문서의 일부 HTML 항목만 1차 확인했다. `source_basis`가 내부 Topic Sheet/Markdown인 항목은 그 자체로 제3자 기술 검증이 아니다. **전체 48건의 claim-to-evidence/정확 locator 검증 완료를 주장하지 않는다.** 모두 HOLD 유지.

## 1차 보류 판정 48건

| # | Topic | Anchor ID | 잠정 상태 | 조건·반례·원문 대조 포인트 | 공식 독립 자료 1차 후보 |
|---:|---|---|---|---|---|
| 1 | 기능안전 | `fsrm_markov_state_transition` | HOLD | 모델은 CTMC/DTMC 중 무엇인지, 전이율·전이확률과 상태경계의 의미를 구별할 것 | 미확인 |
| 2 | 기능안전 | `fsrm_markov_complexity` | HOLD | 상태공간 증가가 계산·검증 부담에 미치는 조건을 모델별로 확인 | 미확인 |
| 3 | 기능안전 | `fsrm_model_assumption_documentation` | HOLD | 수요모드·고장률·DC/PTC·수리·CCF·bypass·근사/제외 조건 중 실제 모델 관련 항목을 누락 없이 재현 가능한지 확인 | [H1](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm) |
| 4 | FAT/SAT·Loop | `sw10_fat_sat_relation` | HOLD | FAT/SAT의 현장 설치·통합 차이와 승인된 시험계획에 의한 조건부 의무 확인 | 미확인 |
| 5 | FAT/SAT·Loop | `sw10_loop_test` | HOLD | 계측용 모니터링 루프에는 최종제어요소가 없다는 예외와 실제 루프 경계 확인 | 미확인 |
| 6 | 습도 | `relative_humidity_definition` | HOLD | 같은 온도의 수증기분압 대비 포화수증기압 정의와 % 단위 확인 | [V1](https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D) |
| 7 | 습도 | `rh_temperature_dependence` | HOLD | 수증기량 보존의 체적·압력·온도 조건과 센서 주변 온도차 구별 | [V1](https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D) |
| 8 | 습도 | `absolute_humidity_definition` | HOLD | ρv=mv/V, Pv/(RvT)의 이상기체 가정과 절대온도·단위 확인 | [V2](https://docs.vaisala.com/r/M210912EN-J/en-US/GUID-8F8C9ECE-FFD9-4F6F-9F11-D94CF9122735) |
| 9 | 습도 | `dew_point_definition` | HOLD | 기준압력, 응축 상(액상) 기준, 냉각 경로 확인 | [V1](https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D) |
| 10 | 습도 | `frost_point_distinction` | HOLD | 0°C 이하 얼음 기준 포화압과 물 기준 포화압을 구별 | [V2](https://docs.vaisala.com/r/M210912EN-J/en-US/GUID-8F8C9ECE-FFD9-4F6F-9F11-D94CF9122735) |
| 11 | 습도 | `pressure_dew_point_effect` | HOLD | 압력 이슬점과 대기압 환산 이슬점의 서로 다른 상태점 구별 | [V1](https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D) |
| 12 | 습도 | `capacitive_polymer_principle` | HOLD | 흡습성 유전체의 유전율·용량 변환 방식의 적용 센서 범위 확인 | 미확인 |
| 13 | 습도 | `resistive_humidity_principle` | HOLD | 이온전도 메커니즘을 모든 재료에 일반화하지 않도록 주의 | 미확인 |
| 14 | 습도 | `psychrometric_wet_dry_bulb` | HOLD | 통풍·증발 냉각·압력 관계, Tw≠Td 조건 확인 | 미확인 |
| 15 | 습도 | `condensation_sensor_temperature_error` | HOLD | 표면 냉각/가열에 따른 국소 RH 변화와 응축 경계 확인 | [V1](https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D) |
| 16 | 습도 | `low_humidity_dew_point_selection` | HOLD | 극저습도 방식 선택을 보편 필수가 아닌 불확도·요구범위 의존 판단으로 유지 | 미확인 |
| 17 | 습도 | `selection_environment_process` | HOLD | 방폭 인증은 적용 지역·분류·제품별이며 일반 채점 필수 원리와 분리 | 미확인 |
| 18 | 피드백 | `feedback_sensitivity_functions` | HOLD | 스칼라 표준 음의 피드백에서 S+T=1; MIMO에는 항등행렬 및 곱 순서 | [M1](https://kr.mathworks.com/help/robust/ref/dynamicsystem.loopsens.html) |
| 19 | 피드백 | `feedback_parameter_sensitivity` | HOLD | H 고정 가정 및 L의 정의와 closed-loop G 상대 민감도 계산 검증 | [M1](https://kr.mathworks.com/help/robust/ref/dynamicsystem.loopsens.html) |
| 20 | 피드백 | `feedback_disturbance_noise_paths` | HOLD | 출력단 외란·측정잡음 주입 위치별 전달경로의 부호와 경계 확인 | [M1](https://kr.mathworks.com/help/robust/ref/dynamicsystem.loopsens.html) |
| 21 | 피드백 | `feedback_steady_state_error_final_value` | HOLD | sE(s)의 극 안정성과 극점 상쇄·최종값 존재 조건 확인 | 미확인 |
| 22 | 피드백 | `feedback_integral_action_tradeoff` | HOLD | 상쇄되지 않은 적분기, 폐루프 안정성, saturation/windup의 적용조건 확인 | 미확인 |
| 23 | 압력 | `bourdon_forms_application` | HOLD | 부르동관 형상·탄성변형·압력범위의 설계별 조건 확인 | [W1](https://www.wika.com/en-us/faq.WIKA) |
| 24 | 압력 | `diaphragm_deflection_principle` | HOLD | 센싱 다이어프램의 ΔP 변형, 탄성 및 감도/선형 범위 확인 | [W1](https://www.wika.com/en-us/faq.WIKA) |
| 25 | 압력 | `diaphragm_sensor_vs_seal` | HOLD | 측정막과 격리용 씰의 구별, 충전액·모세관 영향 검증 | [W1](https://www.wika.com/en-us/faq.WIKA) |
| 26 | 압력 | `piezoresistive_static_capability` | HOLD | 압저항식 여기·조정 구성과 압전식 정적 측정 한계의 조건 구별 | 미확인 |
| 27 | 압력 | `dp_transmitter_two_port_principle` | HOLD | ΔP=PH−PL 기준과 정압 공통모드에 따른 비이상 오차 예외 | 미확인 |
| 28 | 압력 | `ambient_environment_hazardous_selection` | HOLD | 환경조건별 실제 계기 인증 요구는 규격/현장 분류별임을 확인 | 미확인 |
| 29 | 압력 | `accuracy_total_performance_terms` | HOLD | reference accuracy 제조사 정의와 총성능 온도·정압 영향은 모델별로 확인 | 미확인 |
| 30 | 회전속도 | `pulse_frequency_speed_equation` | HOLD | f가 x1/x2/x4 후 '유효 count event rate'인지 채널 사이클 주파수인지 명시 필요 | [O1](https://www.ia.omron.com/support/guide/34/introduction.html) |
| 31 | 회전속도 | `counting_window_speed_equation` | HOLD | m이 유효 event count이고 Δt가 초 단위인지, 저속 양자화 조건 확인 | [O1](https://www.ia.omron.com/support/guide/34/introduction.html) |
| 32 | 회전속도 | `period_measurement_low_speed` | HOLD | Tc가 연속 유효 이벤트 간 간격인지, x4 주기와 타이머 해상도 확인 | 미확인 |
| 33 | 회전속도 | `quadrature_direction_principle` | HOLD | A/B 위상차·회전방향과 4체배 복호의 계수 증가 확인 | [O2](https://www.ia.omron.com/support/guide/34/explanation_of_terms.html) |
| 34 | 회전속도 | `index_z_channel_role` | HOLD | Z 1 pulse/rev 일반형; absolute multiturm과 혼동 금지 | [O2](https://www.ia.omron.com/support/guide/34/explanation_of_terms.html) |
| 35 | 회전속도 | `absolute_encoder_principle` | HOLD | 단일회전/다회전·위치차 unwrap·sample/latency 조건 확인 | [O1](https://www.ia.omron.com/support/guide/34/introduction.html) |
| 36 | 회전속도 | `encoder_frequency_limit_selection` | REVISE_CANDIDATE / HOLD | **REVISE CANDIDATE**: 센서 출력 채널 주파수(PPR×rpm/60)와 수신기 x4 이벤트 처리율은 서로 다른 한계; N_eff 하나로 양쪽 한계를 묶지 말 것 | [O1](https://www.ia.omron.com/support/guide/34/introduction.html) |
| 37 | 회전속도 | `inductive_proximity_principle` | HOLD | 와전류 금속 표적 검출의 모델/재질 범위, 이벤트 누락 가능성 확인 | 미확인 |
| 38 | 회전속도 | `gear_tooth_speed_equation` | HOLD | Z가 실제 유효 이벤트/회전의 수인지; missing-tooth·edge counting 고려 | [O1](https://www.ia.omron.com/support/guide/34/introduction.html) |
| 39 | 회전속도 | `tachogenerator_voltage_speed_principle` | HOLD | 자기여자 PM DC 타코, 부하·온도·속도 범위의 선형 근사 검토 | 미확인 |
| 40 | 회전속도 | `digital_tachometer_instrument_boundary` | HOLD | 디지털 타코미터에 가능한 여러 픽업을 확인; 타코제너레이터와 동일시 금지 | 미확인 |
| 41 | 열전대 | `thermocouple_temperature_measurement_chain` | HOLD | 측정접점→전자계측기와 CJC/표 환산의 구성 조건을 표현; ice-bath 대안은 범위 밖 | [A1](https://www.analog.com/en/resources/app-notes/an-28f.html) |
| 42 | 열전대 | `thermocouple_seebeck_effect_dissimilar_conductors` | HOLD | 서로 다른 균질 재료, 두 접점/온도구배, Seebeck 온도의존성을 정확히 표현 | [A1](https://www.analog.com/en/resources/app-notes/an-28f.html) |
| 43 | 열전대 | `thermocouple_measures_temperature_difference` | HOLD | 기준접점 온도와 물성/EMF 관계 구별; 단순 ΔT 선형센서라고 단정 금지 | [A1](https://www.analog.com/en/resources/app-notes/an-28f.html) |
| 44 | 열전대 | `thermocouple_reference_junction_compensation` | REVISE_CANDIDATE / HOLD | **REVISE CANDIDATE**: 별도 센서 이용 전자식 CJC는 한 구현; 0°C ice-bath·온도제어 기준접점 등도 있으므로 '전자식 온도추적형'으로 범위 지정 | [A1](https://www.analog.com/en/resources/app-notes/an-28f.html) |
| 45 | 열전대 | `thermocouple_law_of_intermediate_metals` | HOLD | 제3 금속의 두 접점 등온과 재료 균질 조건·오차 예외 확인 | [A1](https://www.analog.com/en/resources/app-notes/an-28f.html) |
| 46 | 열전대 | `thermocouple_law_of_intermediate_temperatures` | HOLD | E(T1,T3)=E(T1,T2)+E(T2,T3)와 같은 재료쌍·기준점 조건 확인 | 미확인 |
| 47 | 열전대 | `thermocouple_nonlinearity_reference_tables_polynomial_conversion` | HOLD | ITS-90 열전대 형식별 역함수/다항식·온도범위·전압 단위 확인 | [N1](https://www.nist.gov/publications/nist-60-nist-its-90-thermocouple-database) |
| 48 | 열전대 | `thermocouple_thermowell_installation_dynamic_error` | HOLD | 열접촉/침지/보호관 응답과 센서 고유 전기적 원리 구별 | 미확인 |

**모든 행의 최종 승인 상태는 `HOLD`.** `REVISE_CANDIDATE`는 문장 개선 후보 표식이며 오류 확정·Registry 변경·채점 적격성 판정이 아니다. 과거 긴 문장의 `accepted_explanations` 보존은 승인 근거를 대신하지 않는다.

## 독립 발행자 문서 — 실제로 비교한 1차 위치

- **[O1] OMRON Industrial Automation, “Overview of Rotary Encoders” → Selection Guidelines §6 “Maximum Response Frequency”**: 기기 최대 응답 주파수 식을 `RPM/60 × resolution`으로 설명. 동일 페이지의 물리 엔코더 사양과 수신기에서 수행하는 x4 복호 이벤트율은 구별해야 한다. 위 `encoder_frequency_limit_selection` 원문 수정 필요성 검토의 구체적 이유. https://www.ia.omron.com/support/guide/34/introduction.html
- **[O2] OMRON, “Explanation of Terms” → “Output Phase”, “Output Phase Difference”, “Resolution”**: A/B 정상 90° 전기각, Z 원점 펄스 1/rev. https://www.ia.omron.com/support/guide/34/explanation_of_terms.html
- **[A1] Analog Devices, “AN-28: Thermocouple Measurement” → “Cold Junction Compensation”**: 0°C ice bath 기준, 제어식 기준접점, 온도 추종형 보상 등 구현을 분리한다. 따라서 `thermocouple_reference_junction_compensation`의 별도 센서 단정은 **전자식 온도추종 CJC**로 범위를 좁히는 방향을 검토해야 한다. https://www.analog.com/en/resources/app-notes/an-28f.html
- **[M1] MathWorks, “loopsens” → “More About / Sensitivity functions”**: `S=(I+L)^{-1}`, `T=L(I+L)^{-1}`의 사용 구조, MIMO 곱 순서와 신호 주입 위치를 명시. https://kr.mathworks.com/help/robust/ref/dynamicsystem.loopsens.html
- **[V1] Vaisala, HMDW110 “Output parameters explained” → “Relative humidity” / “Dew point”**: 수증기 분압 대비 포화압 비와 기준 압력에서의 응축점 정의. https://docs.vaisala.com/r/M211726EN-K/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D
- **[V2] Vaisala, HMP155 “Calculation formulas” → “Absolute humidity (3)” / “Dew point/frost point (1)”**: 공기 상태 계산, 포화압 over water/ice의 차이. 모델별 계산식의 상수·단위는 보편적 법칙으로 과대 일반화하지 않는다. https://docs.vaisala.com/r/M210912EN-J/en-US/GUID-8F8C9ECE-FFD9-4F6F-9F11-D94CF9122735
- **[W1] WIKA, “Frequently asked questions” → “How does a diaphragm seal work?”, “What effect does temperature have on a diaphragm seal system?”**: 센싱막과 격리용 씰 구별, 충전유체 및 온도 영향. https://www.wika.com/en-us/faq.WIKA
- **[H1] HSE, “Control systems” → SIS reliability, diagnostic/proof testing and maintenance**: 모델의 적용 조건·시험/수리 입력이 기능안전 무결성 평가에 미치는 영향을 기술. 특정 계산모델의 모든 입력항목을 일괄 필수화하지 않는다. https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
- **[N1] NIST, “NIST 60 — NIST ITS-90 Thermocouple Database”, Abstract**: Monograph 175 열전대 종류별 표와 기준함수의 권위 있는 출처. 실제 구간/다항식의 세부 대조는 보류. https://www.nist.gov/publications/nist-60-nist-its-90-thermocouple-database

## 수정/검증 차단 조건

1. 우선 `encoder_frequency_limit_selection` 및 `thermocouple_reference_junction_compensation`을 독립 문서의 범위와 맞게 재작성 **제안**하고, 현 source·accepted_explanations·관련 테스트의 적용 범위를 먼저 비교한다. 이 단계에서는 **소스 수정·승인하지 않음**.
2. 기능안전 3개는 기존 승인 Registry의 정확 문장과 의미를 대조하여 승인 범위를 유지한 원복 또는 정식 재검토 경로를 선택한다. ledger `--write`로 해시만 맞추는 것은 금지한다.
3. 나머지 46건도 정확한 발행자/문서 버전/section·page·formula, 조건·반례, 기존 Registry·scoring exclusions와 중복 owner를 건별 확인하고 `KEEP/REVISE/HOLD`를 승인 절차로 결정한다. 참고문헌만 연결한 행은 계속 HOLD.
4. 변경 승인 이후에만 `rubric_manager.py validate-topic-pack-release --all --promote-generated`로 생성하고 old/new 6개 파일, routing triggers, coverage, A/B/C·D/E, WRONG/Fatal, 점수 ceiling, 중복 가점 패리티를 검증한다.
5. 실행 근거가 확보될 때까지 Issue #39의 C5/C7/C8/D2/D3 및 미검증 B 항목은 OPEN, PR은 Draft. `PROMOTE_GENERATED=0 scripts/validate_release.sh`와 전체 `python3 -B -m pytest -q`의 현 HEAD 수치를 제공하기 전 PASS를 주장하지 않는다.

**보호 확인:** 공개 가능한 Fact ID·출처·검토 기준만 기록; 개인 답안·실세션·키·운영 DB 없음. score-changing code, Topic source, approved Registry, generated, ledger 파일 무변경.
