# PR #38 · 9건 후보의 최종 원본 보존/수정 우선순위 판정 (2026-11-15)

> 사람용 요약: **9건 중 8건은 기존 정본을 유지**하며 새로운 단문화안/수정안 적용을 보류한다. **엔코더 주파수 선정 1건만 정밀 원본 수정을 우선 검토**한다. 이것은 소스·채점 Registry **승인·변경이 아니며**, 실제 전체 pytest 검증 전에는 운영 적용하지 않는다.

## 경계와 기준

- 대상 정본: PR #38 HEAD `5f39ad269998151fcb6055cea81459646649db96`, `calibration/fact_anchor_simplification_review_20261114.json` 48개 후보 중 9개 예외. 9건 원본·후보·근거의 identity 검토는 `reports/pr38_fact_anchor_nine_exception_revision_candidates_20261115.json` 참조.
- Fact Anchor 적격성: `docs/fact_anchor_eligibility_policy.md`, Topic Pack workflow: `docs/topic_pack_workflow.md`. 추정상 위험 표현과 실제로 단정 오류가 있는 문장을 구별했다.
- **KEEP_CANONICAL_NO_CHANGE는 원본 변경 불필요 판단**이지 (1) Registry 승격, (2) 독립적으로 시험에 사용 승인, (3) 새 문장 검증 완료를 의미하지 않는다. 일부 PDF의 필요한 쪽 화면은 캐시 오류로 열람되지 않았다. 모든 단문화 후보는 `PENDING_TECHNICAL_REVIEW`·`score_effect: none` 유지.

## 9건 결정

| Fact Anchor ID | 결정 | 기존 원본/수정안 비교 및 판단 | 1차 근거·정확 locator |
|---|---|---|---|
| `fsrm_markov_state_transition` | **원본 유지** | 기존 원본이 상태·전이확률/전이율 및 경계별 상태정의를 조건부로 이미 정확히 제시. CTMC/DTMC 구별은 설명 자료로 유익하지만 기존 일반 명제를 대체할 근거는 아님. | [공식 출처](https://www.mathworks.com/help/econ/discrete-time-markov-chains.html) — MathWorks, Discrete-Time Markov Chains, 'What Are Discrete-Time Markov Chains?'; ECSS-Q-HB-30-02A **draft** v0.4.5 §9.4.3.4. |
| `fsrm_markov_complexity` | **원본 유지** | 원본은 '상태공간이 커지면 부담이 증가할 수 있다'고 한정하므로 과대단정 없음. 기존 2문장을 한 문장으로 축약할 채점상 필요가 확인되지 않음. | [공식 출처](https://handbook.reliability.space/en/latest/system/handbook/reliability_prediction/methods.html) — ECSS-Q-HB-30-02A **draft** v0.4.5 §9.4.3.4: n개 이진 상태의 최대 2^n 조합 및 복잡성. |
| `fsrm_model_assumption_documentation` | **원본 유지** | 원본이 실제 적용된 입력을 기록하고 관련 없는 항목은 무조건 계산요소로 요구하지 않도록 이미 제한. 새 짧은 표현으로 교체하면 진단·시험·CCF 등 주요 점검 항목이 사라짐. | [공식 출처](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf) — UK HSE, Appendix 1 'PFD Calculations' 1–8 및 Figure 1. IEC 61511 특정 의무 조항은 이번 검토에서 본문 확인 안 됨. |
| `psychrometric_wet_dry_bulb` | **원본 유지** | WMO 건습구 계산에는 건습구 온도와 기압·통풍·심지 상태가 작용하며 원본이 이미 이를 포함. 변경안은 새 기술 주장 없이 표현만 재배열. | [공식 출처](https://amc.namem.gov.mn/wp-content/uploads/WMO/1.%208_I-2023_en.pdf) — WMO-No.8 (2023) Vol I Ch4 §§4.3.1.1–4.3.1.8 (PDF text 확인, screenshot 불가). |
| `feedback_integral_action_tradeoff` | **원본 유지** | 원본은 위상여유 감소를 '유발할 수 있다'고 표현하므로 항상 감소한다고 단정한 것이 아님. 포화와 windup 우려도 타당하며 원본 수정 필요성 불충분. | [공식 출처](https://www.mathworks.com/help/control/ug/assessing-gain-and-phase-margins.html) — MathWorks, 'Assessing Gain and Phase Margins', 'Gain and Phase Margins'; 'Improve PID Design to Handle Plant Constraints', 'How Constraints Affect PID Performance'. |
| `piezoresistive_static_capability` | **원본 유지** | 원본은 압전식 정압 측정이 '어렵다'고 했지 불가능하다고 하지 않음. Kistler의 제한적 정압 가능성과 양립. 원본에 오류가 있다는 지난 암시는 과도한 진단. | [공식 출처](https://www.kistler.com/CH/en/piezoelectric-pressure-sensors-with-charge-output-pe-for-static-pressure-measurement/C00000140) — Kistler, 'Is it possible to measure static pressures...?' / 'Measuring small and large static pressures over a long period'. |
| `accuracy_total_performance_terms` | **원본 유지** | 원본에 이미 '제조사 정의가 다를 수 있다'는 조건이 존재하고 실제 성능을 온도·정압·설치·안정성으로 평가한다고 함. 일반 공학적 선정 지침으로 유지하되 특정 모델 합산식을 모든 기기에 적용하지 않음. | [공식 출처](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-00813-0100-4801.pdf) — Emerson Rosemount 3051S Series Product Data Sheet Rev UW, Apr 2026, 'Transmitter total performance', p.139. |
| `encoder_frequency_limit_selection` | **원본 정밀 수정 검토** | 기존 원본도 RPM×N_eff를 Hz 사양과 바로 비교하는 것처럼 읽혀 /60 단위변환과 물리 채널 PPR 대 복호 후 N_eff를 혼동할 위험. 소스 실제 정정은 승인·source hash·생성물·전체 pytest 절차에서만 수행. | [공식 출처](https://www.ia.omron.com/support/guide/34/introduction.html) — OMRON, 'Selection Guidelines [6] Maximum Response Frequency'; NI, 'Hardware Encoder Measurements How-To Guide' X1/X2/X4; Rockwell 1769-UM006 high-speed counter 'Chapter 2 Module Operation — Input Frequency'. |
| `thermocouple_reference_junction_compensation` | **원본 유지** | 기존 원본에 0°C 유지법 외 보상법도 있다고 명시했고 전자식 별도 센서는 '일반적으로'라고 한정됨. 짧은 후보가 전자식 CJC만을 유일한 보상법으로 오해시킬 수 있으므로 원본 보존. | [공식 출처](https://www.analog.com/en/resources/app-notes/an-28f.html) — Analog Devices AN-28 'Cold Junction Compensation', Fig.5 ice bath, Fig.6 Peltier constant reference, Fig.7 tracking compensation; Appendix A. |

## 유일한 원본 정밀 수정 후보: encoder_frequency_limit_selection

**현 원본 위험:** '최고 회전속도와 N_eff의 곱이 허용 주파수를 넘지 않도록'은 ① 회전속도가 rpm이면 /60이 필요한 점, ② 물리 출력 주기와 디코딩 후 count-rate가 다른 점을 불명확하게 만든다. 이는 '기존 canonical이 전부 틀렸다'가 아니라 수식·사양의 경계를 명확히 할 필요다.

**대체 제안 (미적용)**

> 증분형 엔코더의 최고회전속도 n_max[rpm]와 **채널 출력 주기수** PPR[cycle/rev]로 계산한 최대 채널 주파수는 f_ch=n_max×PPR/60[Hz]이다. 엔코더 자체의 최대 출력 응답 주파수와 수신기의 해당 복호모드별 허용 **입력 신호 주파수**를 비교한다. 수신기에 별도의 디코딩 후 계수 이벤트 처리율 한계가 규정되어 있다면, x1/x2/x4의 유효 이벤트율도 따로 확인한다.

**단위 예시:** n_max=3,000 rpm, PPR=2,000 cycle/rev이면 f_ch=100,000 Hz. 유효 x4 계수율은 400,000 count/s. 수신기가 'x4 quadrature input 250 kHz'라고 사양화한 경우 이것이 채널 입력 주파수인지, 내부 계수율인지 **그 제품 설명서의 정의로 판독**해야 한다. x4 입력 250 kHz를 무작정 400 kcount/s와 비교해서 불합격시키면 오류일 수 있다.

**검증할 부가 조건:** 입력 Filter 주파수, A/B 상차 및 위상 간격, 최대 속도·PPR 구분, quadrature x4 jitter/noise, 반례 `f_ch`를 `N_eff`로 이중 4배 계산한 경우, counter의 실제 계수속도 spec. [OMRON Selection Guidelines [6]](https://www.ia.omron.com/support/guide/34/introduction.html), [NI Hardware Encoder How-To](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1riCAA), [Rockwell 1769-UM006 Chapter 2](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1769-um006_-en-p.pdf).

## 다음 실행 작업(별도 검증 환경에서, **아직 미실행**)

1. 실제 branch HEAD와 기존 `source_basis`, 승인 Registry, promotion ledger의 encoder 항목 및 exclude overlay 여부 확인. 원본 Facts의 statement/expected/claim/description/accepted_explanations에 동일 과대주장이 존재하는지 살펴 수정 범위를 결정. 승인 증거 및 exact Fact ID를 특정하지 못하면 Registry의 승인문구는 변경하지 않는다.
2. `rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json`의 **해당 anchor 1개만** 조건을 유지하며 수정. 다른 47건 보류 원본 및 단문화 후보 적용 금지. Anchor ID, Topic ID, grading weights, fatal/ceiling/WRONG/exclusions, other Topic data 불변.
3. 원문 단위 반례 및 PPR와 N_eff·x1/x2/x4 간 관계 focused test 보강. 현행 `tests/test_fact_anchor_simplification_batch.py`, `tests/test_fact_anchor_sentence_sync_audit.py`는 **48건 source==previous**를 요구하므로, 승인된 encoder 변경에 한해 manifest/테스트를 정책대로 동기화하거나 신규 manifest를 도입해야 한다. 단순 테스트 삭제·xfailed·quarantine 금지.
4. 기존 승인·source hash·ledger 계약대로 채점용 Registry와 source의 일치 여부를 **개별 원문 검토**. 원문 SHA만 바꿔 무심사 승격하지 않는다. `rubrics/generated/` 직접 편집 금지.
5. 검증 환경에서 `python3 -B -m pytest -q tests/test_fact_anchor_simplification_batch.py tests/test_fact_anchor_sentence_sync_audit.py tests/test_approved_fact_registry.py`와 `python3 scripts/rubric_manager.py validate-topic-pack-release --all` 수행. 정식 관리 경로로 생성물을 빌드/승격한 후 `python3 -B scripts/release_candidate.py validate`로 **전체 pytest 결과(pass/fail/skip)** 확보. 실제 실패가 있다면 원인별로 해결; 기존 점수·Golden parity 확인.
6. 모든 게이트 확인 전 Draft PR 유지, Issue #39 체크박스 보류, main merge 및 bot deploy/restart 금지.

## 이번 검토로 완료한 것과 남은 것

- 완료: 기존 9개 원본/수정안 구분, 8개 원본 유지 결정, 1개 source precision 수정 후보 확정, 조건/출처 locator 명시. 48개 전체 단문화 후보는 여전히 미적용이다.
- 미완료: canonical encoder 수정, Registry/ledger 적용, generated rebuild, GitHub Actions workflow_dispatch, 전체 pytest와 Release Gate. **PASS/APPROVED/DEPLOYED 0건**.

## 출처 범위 주의

- `fsrm_markov_state_transition`: 이산시간 전이확률과 연속시간 전이율을 혼동하지 않음. Draft를 확정 ECSS 표준으로 서술 금지.
- `fsrm_markov_complexity`: 2^n은 모든 조합을 유지한 이진 상태 모형의 최대 규모이며 항상 실제 모델 상태 개수가 아님.
- `fsrm_model_assumption_documentation`: PDF 원본 screen cache miss; 목록의 모든 항목이 보편 필수라는 식의 의무화 금지.
- `psychrometric_wet_dry_bulb`: 센서 심지의 물/얼음과 psychrometric coefficient를 구별. PDF 시각 검증 미완료; 새 채점 의무 신설 금지.
- `feedback_integral_action_tradeoff`: 적분 추가만으로 안정성·오차 제거 보장 안 됨. 위상여유는 크로스오버, 이득 및 설계에 따라 달라짐.
- `piezoresistive_static_capability`: 전하 출력 PE는 drift 크기/허용 오차/시간에 따라 정적 또는 준정적 응용 가능. 정압 가능성을 보편 무제한으로 단정 금지.
- `accuracy_total_performance_terms`: 모델 3051S 성능 조합은 이 회사 정의. PDF p0 화면만 확인, p139 screenshot cache miss; 독립 범용 표준 인증으로 해석 금지.
- `encoder_frequency_limit_selection`: x4 모드의 내부 count event-rate와 허용 external input frequency는 단위 Hz가 같아도 서로 다른 사양. Rockwell 모델 수치는 일반 정답 기준으로 쓰지 않음.
- `thermocouple_reference_junction_compensation`: 동온도 기준접점이 실제 0°C라면 온도추적 보상 계산 센서를 반드시 설치해야 한다는 뜻이 아님. 채점기 필수요소 추가 금지.
