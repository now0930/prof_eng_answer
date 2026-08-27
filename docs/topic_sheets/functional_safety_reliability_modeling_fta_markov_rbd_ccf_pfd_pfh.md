# Topic Sheet — 기능안전 신뢰도 모델링

## 1. Topic metadata

- topic_id: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`
- title_ko: 기능안전 신뢰도 모델링: FTA·Markov·RBD·CCF·PFDavg·PFH
- question_type: `PRINCIPLE_INTERPRETATION`
- difficulty: `THEORY_CORE`
- selection_importance: `HIGH`
- source_basis:
  - The Safety Critical Systems Overview & Chapter 1
  - The Safety Critical System Chapter 2
  - The Safety Critical Systems Chapter 3
  - The Safety Critical Systems Chapter 4
  - The Safety Critical System Chapter 5
  - IEC 61508/IEC 61511의 기능안전 수명주기 및 정량 하드웨어 무결성 개념
- ownership:
  - 일반 정량 신뢰도 모델링과 계산 가정
  - FTA·RBD·Markov의 비교
  - CCF·Proof Test·Diagnostics·Voting의 정량 영향
  - PFDavg·PFH의 demand mode별 적용

## 2. Core correct facts

1. RBD는 시스템이 성공하기 위한 기능경로를 직렬·병렬 블록으로 표현하는 성공논리 모델이다.
2. 직렬 성공경로는 구성요소 하나의 실패가 기능실패로 이어지며, 병렬 성공경로는 요구된 성공조건을 만족하는 대체경로를 가진다.
3. FTA는 정의된 Top Event에서 시작하여 AND/OR Gate로 원인 고장조합을 하향 전개하는 실패논리 모델이다.
4. Minimal Cut Set은 Top Event를 발생시키는 최소 기본사건 조합이다.
5. Markov Model은 정상·위험고장·진단검출·수리·시험·degraded 상태 사이의 전이를 시간 의존적으로 표현한다.
6. Markov Model은 상태와 전이 수가 증가하면 계산과 검증 복잡도가 급격히 증가한다.
7. RBD, FTA와 Markov Model은 표현 관점과 가정이 다르며 하나를 다른 하나와 동일하게 취급하지 않는다.
8. 저수요 SIF의 정량 목표는 일반적으로 PFDavg로 표현한다.
9. 고수요 또는 연속수요 SIF의 정량 목표는 일반적으로 PFH로 표현한다.
10. PFDavg와 PFH의 선택은 demand mode 정의에 근거해야 한다.
11. 단순 저수요 1oo1 근사에서 검출되지 않은 일정 위험고장률과 완전 Proof Test를 가정하면 PFDavg는 고장률과 시험주기에 비례한다.
12. 위 근사는 일정 고장률, 독립성, 시험 복구, 수리와 진단 조건을 명시해야 하며 모든 구조에 그대로 적용하지 않는다.
13. RRF는 정의된 조건에서 위험 감소 요구를 나타내며 저수요 모드에서는 PFDavg의 역수 관계로 설명할 수 있다.
14. 1oo1, 1oo2, 2oo2, 2oo3 등 Voting Architecture는 요구 성공조건에 따라 위험고장과 Spurious Trip 특성이 달라진다.
15. Voting 구조와 HFT는 SIL 달성의 한 요소이며 단독으로 SIL을 보장하지 않는다.
16. CCF는 중복 채널을 동시에 무력화하여 독립고장 가정의 이점을 감소시킨다.
17. β-factor 모델은 전체 위험고장률 중 공통원인 기여분을 단순화해 분리하는 대표 모델이다.
18. 물리적 분리, 독립 전원·배관·환경, 다양성, 독립 교정·정비 절차는 CCF 저감 근거가 될 수 있다.
19. Diagnostic Coverage는 위험고장 중 자동 진단으로 검출되는 비율과 관련되며 Proof Test Coverage와 동일하지 않다.
20. Proof Test는 Online Diagnostics가 검출하지 못한 잠복 위험고장을 발견하기 위해 수행한다.
21. Proof Test Interval이 길어지면 잠복 위험고장의 평균 노출시간이 증가할 수 있다.
22. Partial Proof Test 또는 PST는 전체 위험고장모드를 검출하지 못하므로 Coverage와 잔여고장을 명시해야 한다.
23. 전체 SIF의 정량 평가는 Sensor, Logic Solver, Final Element와 필요한 Utility·Interface의 기여를 포함한다.
24. 개별 구성요소 인증은 전체 SIF의 Achieved SIL을 자동 결정하지 않는다.
25. 정량 하드웨어 무결성 계산은 체계적 무결성, 소프트웨어 V&V, 형상관리와 독립성 증거를 대체하지 않는다.
26. 계산 결과에는 고장률 출처, 운전환경, 시험주기, 수리시간, 진단, CCF, Bypass와 모델 근사조건을 함께 제시해야 한다.

## 3. Acceptable answer expressions

- “RBD는 성공경로, FTA는 실패원인 전개, Markov는 상태전이 모델이다.”
- “PFDavg는 저수요 요구시 실패확률의 평균값이며 PFH는 고수요·연속수요의 시간기반 지표다.”
- “β-factor는 중복채널의 공통원인 고장 부분을 분리한다.”
- “Proof Test Interval과 Coverage가 잠복 위험고장의 노출시간과 PFDavg에 영향을 준다.”
- “2oo3는 안전성과 가용성 사이의 trade-off가 있으며 CCF와 degraded voting을 평가해야 한다.”
- “전체 SIF는 Sensor–Logic Solver–Final Element의 연속 기능으로 평가한다.”
- 용어와 수식을 다르게 표현하더라도 조건과 물리적 의미가 맞으면 인정한다.

## 4. Fatal wrong claims

1. `[pfdavg_all_demand_modes]` PFDavg는 저수요·고수요·연속수요에 구분 없이 같은 방식으로 적용한다.
   - correction: demand mode에 따라 PFDavg 또는 PFH를 구분한다.
2. `[pfdavg_equals_pfh]` PFDavg와 PFH는 단위만 바꾸면 같은 값이다.
   - correction: 서로 다른 성능지표이며 정의와 적용 모드가 다르다.
3. `[voting_guarantees_sil]` 2oo3 또는 HFT 구조만 채택하면 SIL이 자동 보장된다.
   - correction: CCF, 진단, 시험, 전체 SIF와 systematic capability를 평가한다.
4. `[ccf_irrelevant_to_redundancy]` 중복구조에서는 CCF를 무시해도 결과가 변하지 않는다.
   - correction: CCF는 중복 이점을 크게 감소시킬 수 있다.
5. `[proof_test_removes_systematic_faults]` Proof Test가 소프트웨어와 사양의 체계적 오류를 정량적으로 제거한다.
   - correction: Proof Test는 정의된 위험고장 검출범위를 다루며 체계적 무결성은 별도 수명주기 증거가 필요하다.
6. `[pst_proves_total_sis]` PST만 통과하면 전체 Final Element와 전체 SIS의 PFDavg가 입증된다.
   - correction: PST Coverage 밖의 고장과 Sensor·Logic·전체 Final Element 경계를 포함한다.
7. `[fta_rbd_markov_identical]` FTA, RBD, Markov Model은 목적과 가정이 동일한 같은 기법이다.
   - correction: 성공논리, 실패논리, 상태전이라는 모델 관점이 다르다.
8. `[component_certificate_proves_sif]` SIL 인증기기 하나가 전체 SIF의 SIL을 결정한다.
   - correction: 전체 기능경계와 구조·정량·체계적 증거를 평가한다.
9. `[quantitative_hardware_proves_systematic_integrity]` PFDavg 또는 PFH 계산만으로 소프트웨어와 체계적 무결성까지 입증된다.
   - correction: 정량 하드웨어 무결성과 체계적 무결성은 상호 보완적이다.

## 5. Warn-level weak claims

- demand mode를 명시하지 않은 PFDavg/PFH 설명
- 계산식만 있고 기호, 단위, 가정 설명이 없음
- Voting 구조를 나열했으나 HFT·Spurious Trip·degraded mode 비교가 없음
- CCF를 언급했으나 독립성 확보 방법과 연결하지 않음
- Proof Test Interval만 언급하고 Coverage·Diagnostics를 구분하지 않음
- Sensor, Logic Solver 또는 Final Element 중 하나만 계산하고 전체 SIF처럼 결론냄
- 모델 결과의 데이터 출처와 불확실성 설명이 없음
- FTA, RBD, Markov의 장단점과 적용조건 비교가 없음

## 6. False positive cautions

- 정답을 설명하기 위한 부정문과 반박문은 fatal로 처리하지 않는다.
- “2oo3만으로 SIL이 보장되지 않는다”는 정답이다.
- “PFDavg는 고수요 모드 지표가 아니다”는 정답이다.
- 여러 모델을 비교하기 위해 한 문장에 병기한 것을 동일 모델 주장으로 보지 않는다.
- 교육 목적의 단순화 계산에서 가정을 명시했다면 실제 전체 모델과 다르다는 이유만으로 fatal 처리하지 않는다.
- β-factor 이외의 CCF 모델을 사용한 답안을 허용한다.
- 수식 OCR 오류는 주변 설명과 단위, 결론을 함께 확인한다.
- 표나 그림의 위치만으로 오답을 확정하지 않는다.

## 7. Regex candidate patterns

결정론적 keyword penalty는 기본 비활성으로 유지한다.

문맥 검증 후보:

- `PFDavg.*(모든|전체).*(수요|demand)`
- `(2oo3|HFT).*(자동|무조건).*(SIL|무결성).*(보장|달성)`
- `(CCF|공통원인).*(무시|영향.*없)`
- `(PST|partial stroke).*(전체 SIS|전체 SIF).*(입증|보장)`
- `(FTA|RBD|Markov).*(동일|같은 기법|완전히 대체)`
- `(인증기기|certified component).*(전체 SIF|전체 SIS).*(SIL).*(결정|보장)`

위 패턴은 candidate extraction에만 사용한다. Fatal 판정은 정답 주장과의 충돌을 문맥으로 검증한다.

## 8. fact_anchor.json generation guidance

- 20개 이상 atomic anchor로 분리한다.
- 정의, 모델 비교, demand mode, PFDavg/PFH, CCF, 진단, Proof Test, Voting, 전체 SIF 경계를 포함한다.
- 각 anchor는 `anchor_id`, `statement`, `expected`, `keywords`, `required`, `weight`를 유지한다.
- 오답 regex와 감점 정책은 넣지 않는다.
- source_basis는 이 Topic Sheet를 가리킨다.

## 9. logic_check.json generation guidance

- `schema_version`, `topic_id`, `title`, `deterministic_checks`, `llm_profile`, `revision_notes` 구조를 유지한다.
- broad deterministic penalty는 비활성으로 둔다.
- Fatal wrong claim 9개를 `llm_profile.fatal_conditions`에 correction과 함께 넣는다.
- `truth_schema`, `safe_conditions`, candidate extraction key terms를 충분히 작성한다.
- 부정형 정답과 비교문을 false positive로 보호한다.
- P0 오답 4개는 반드시 명시한다.
  - PFDavg all demand modes
  - Voting/HFT alone guarantees SIL
  - PST alone proves total SIS
  - FTA/RBD/Markov are interchangeable

## 10. model_answer.json generation guidance

권장 전개:

1. 기능안전 정량 신뢰도 평가의 목적과 범위
2. RBD·FTA·Markov의 정의와 비교
3. 고장모드와 입력변수 λDU, λDD, DC, β, T1, MTTR
4. Voting Architecture와 CCF
5. 저수요 PFDavg와 고수요·연속수요 PFH
6. Proof Test·Diagnostics·Repair·Bypass의 영향
7. Sensor–Logic Solver–Final Element 전체 SIF 계산
8. 가정, 한계, 데이터 검증과 수명주기 관리
9. 결론

고득점 요소:

- 모델별 목적·가정·장단점 비교
- demand mode와 지표의 정확한 연결
- 수식의 조건과 물리적 의미
- CCF와 독립성 저감대책
- 시험·진단·수리·degraded mode 반영
- 정량 하드웨어와 체계적 무결성 경계
- 현장 데이터와 SRS·Proof Test 절차 연결

## 11. topic_importance.json generation guidance

- difficulty: `THEORY_CORE`
- selection_importance: `HIGH`
- question_type: `PRINCIPLE_INTERPRETATION`
- high-band unlock:
  - 세 모델의 차이를 정확히 구분
  - demand mode별 PFDavg/PFH 구분
  - CCF, Proof Test, Diagnostics와 Voting을 연결
  - 전체 SIF 경계와 계산 가정을 명시
  - 정량 하드웨어와 체계적 무결성을 구분
  - fatal logic error 없음

## 12. Human review checklist

- [ ] 신규 Topic이 기존 HAZOP/LOPA, HIPPS, Final Element, SW-05와 중복되지 않는가?
- [ ] RBD, FTA, Markov의 정의와 적용 경계가 정확한가?
- [ ] PFDavg와 PFH의 demand mode 구분이 정확한가?
- [ ] 단순 근사식을 일반 공식처럼 과장하지 않았는가?
- [ ] CCF, β-factor, Diagnostic Coverage와 Proof Test Coverage를 구분했는가?
- [ ] Voting/HFT만으로 SIL을 보장하지 않는다는 방어가 명시됐는가?
- [ ] PST의 검출범위와 전체 SIS 경계를 구분했는가?
- [ ] 정량 하드웨어와 체계적 무결성 경계를 명시했는가?
- [ ] fatal과 단순 누락을 구분했는가?
- [ ] false positive caution이 충분한가?
- [ ] 표·수식·다이어그램을 claim 중심으로 평가하는가?
- [ ] source JSON 생성 전 사람이 본 Topic Sheet를 승인했는가?
