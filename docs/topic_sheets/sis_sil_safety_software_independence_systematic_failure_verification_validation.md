# SIS·SIL 안전 소프트웨어, 독립성, 체계적 고장 및 검증·확인

## 1. Topic

- SW 번호: `SW-05`
- Topic ID: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- 한글 주제: SIS·SIL 안전 소프트웨어, 독립성, 체계적 고장 및 검증·확인
- 기본 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`

## 2. 범위

이 Topic은 기능안전 요구가 부여된 안전 소프트웨어의 전 수명주기를 다룬다.

포함 범위:

1. SIS, SIF, SIL의 관계
2. Hazard/Risk Analysis에서 SRS로 이어지는 요구사항 흐름
3. Safety Application Program의 설계, 구현, 통합 및 형상 통제
4. Random Hardware Failure와 Systematic Failure의 구분
5. Verification과 Validation의 목적 차이
6. 독립성, 분리, 공통원인고장 및 다양성
7. Safety Manual, 인증 제품, Proven in Use의 증거 한계
8. Tool Qualification과 검증된 Library/Function Block
9. Functional Test, Proof Test 및 Software Validation의 관계
10. 변경, Bypass, Override, Audit 및 Competence 관리

## 3. 제외 범위

- 일반 Sequence, Interlock, Permissive, Trip, First-out 및 Fail-safe 동작 메커니즘 자체
- 일반 제어 소프트웨어의 보편적 SDLC, 일반 단위시험 및 일반 형상관리
- Final Element의 PFD 산정 상세, 밸브 PST 설계, 밸브 진단 및 Proof Test 절차 상세
- SIL 결정용 HAZOP/LOPA 계산 상세
- Cybersecurity 상세
- 공통 Router, Generated Bank 및 Production Python 수정

## 4. 인접 Topic Ownership

### SW-02와의 경계

SW-02가 소유하는 내용:

- Sequence와 State Transition
- Interlock, Permissive, Trip 및 Shutdown 논리
- Cause & Effect, Voting, First-out
- 일반 Bypass/Override의 논리 동작
- Fail-safe 동작과 재시작 메커니즘

SW-05가 소유하는 내용:

- 해당 논리가 SIF로 할당되었을 때의 SRS 추적성
- SIL 요구에 따른 Safety Lifecycle
- Safety Application Program의 체계적 고장 억제
- Verification, Validation 및 독립성
- Bypass/Override의 기능안전 승인, 보상조치, 시간 제한 및 복구 확인

### SW-04와의 경계

SW-04가 소유하는 내용:

- 일반 제어 소프트웨어 개발 수명주기
- 일반 요구사항, 설계, Coding, Test 및 V&V
- 일반 소프트웨어 품질과 유지보수

SW-05가 소유하는 내용:

- 기능안전 요구가 추가된 Software Safety Lifecycle
- SRS의 기능 요구와 무결성 요구
- SIL에 상응하는 체계적 능력과 검증 엄격도
- Safety Tool, Library, 인증 범위, Proven in Use 및 독립성
- Safety Modification에 따른 영향분석, Regression 및 Revalidation

### 기존 Final Element/PST Topic과의 경계

- Final Element/PST Topic은 Sensor–Logic Solver–Final Element 중 Final Element의 위험고장, PST, Proof Test Coverage 및 밸브 성능을 소유한다.
- SW-05는 Safety Application Program, SRS 추적성, Software V&V 및 기능안전 관리체계를 소유한다.
- Proof Test 수치는 SW-05에서 관계만 설명하고 세부 밸브 산정은 기존 Topic으로 넘긴다.

## 5. 대표 문제

> SIS·SIL 안전 소프트웨어에서 Safety Lifecycle, 체계적 고장, 독립성 및 Verification·Validation 방안을 설명하시오.

## 6. 핵심 Fact

1. SIS는 하나 이상의 SIF를 구현하는 계장 시스템이다.
2. SIL은 장치명이나 제품명의 등급이 아니라 Safety Function에 요구되는 Safety Integrity의 이산 수준이다.
3. SIF는 감지부, Logic Solver와 Final Element의 전체 경로 및 관련 지원요소로 해석해야 한다.
4. SRS는 SIF가 무엇을, 언제, 어느 성능과 무결성으로 수행해야 하는지를 명확히 규정한다.
5. Safety Application Program은 일반 운전 논리가 아니라 SRS를 구현하는 안전 관련 소프트웨어 구성요소다.
6. Random Hardware Failure는 시간에 따른 물리적 열화의 확률적 고장이다.
7. Systematic Failure는 특정 조건에서 반복 재현될 수 있는 요구사항, 설계, 소프트웨어, 도구, 설치, 운전 또는 변경 결함이다.
8. 소프트웨어 고장은 일반적으로 단순 고장률 계산만으로 충분히 다룰 수 없으며 수명주기 절차와 검증 증거로 통제한다.
9. Verification은 각 단계 산출물이 이전 단계의 입력 요구를 만족하는지 확인한다.
10. Validation은 통합된 SIS/SIF가 의도된 운전환경에서 SRS를 만족하는지 확인한다.
11. Functional Test는 특정 기능의 입력·논리·출력을 시험하지만 전체 Safety Validation과 동일하지 않다.
12. Proof Test는 운전 중 진단으로 발견되지 않은 위험 고장을 검출하고 기능을 복원하기 위한 주기 시험이다.
13. Proof Test는 Software Validation을 대체하지 않는다.
14. 독립성은 이해충돌과 공통 오류 가능성을 줄이는 조직적·기술적 수단이다.
15. BPCS와 SIS를 논리적으로 분리해도 전원, Sensor, Network, Engineering Tool 또는 유지보수 절차를 공유하면 공통원인이 남을 수 있다.
16. 다양성은 공통원인 가능성을 줄일 수 있으나 복잡성과 새로운 체계적 오류를 증가시킬 수 있다.
17. 인증 제품은 인증 범위, Safety Manual의 가정, 사용조건 및 제한을 만족할 때만 증거로 사용할 수 있다.
18. 인증된 Logic Solver를 사용해도 전체 SIF의 SIL 달성은 자동으로 보장되지 않는다.
19. Proven in Use는 식별된 Version, 동일하거나 대표성 있는 환경, 충분한 운전이력 및 결함기록을 요구한다.
20. Tool Qualification은 Tool 오류가 Safety Software에 미치는 영향과 후속 단계에서 검출될 가능성을 근거로 결정한다.
21. Library와 Function Block은 승인 Version, 검증 범위, Parameter 제한 및 변경이력을 통제해야 한다.
22. 요구사항–설계–Code/Configuration–Test Case–Result 간 양방향 Traceability가 필요하다.
23. Modification은 영향분석, 승인, Regression, 필요한 Revalidation 및 As-built 문서 갱신을 수반한다.
24. Bypass와 Override는 승인, 표시, 시간 제한, 보상조치, 기록 및 독립적 복구 확인이 필요하다.
25. Functional Safety Audit은 수명주기 활동과 관리체계의 수행 여부를 확인한다.
26. Competence는 역할, 교육, 경험, 책임 및 평가 근거로 관리한다.
27. SIL의 정량 목표와 체계적 고장 억제 요구는 서로 대체 관계가 아니다.
28. 정량 계산은 가정, Demand Mode, 진단, Proof Test, Repair, 공통원인 및 종속성을 명시해야 한다.
29. 표준 번호의 세부 Clause, 독립성 수준 및 인증 적용범위는 적용 Edition과 조직 규정으로 verify-first 한다.
30. 기능안전은 Hardware, Software, 사람, 절차 및 운영 증거가 결합된 Lifecycle 성과다.

## 7. 필수 수식·지표

### 저요구 모드 위험감소계수

\[
RRF \approx \frac{1}{PFD_{\mathrm{avg}}}
\]

- `PFDavg`가 적절한 저요구 모드에서 사용하는 관계다.
- Target PFD와 Achieved PFD를 구분한다.

### 단순 1oo1 근사

\[
PFD_{\mathrm{avg}} \approx \frac{\lambda_{DU}T_1}{2}
\]

적용 가정:

- 상수 위험 미검출 고장률
- 완전한 Proof Test
- 시험 간격에 비해 수리시간이 작음
- 저요구 모드
- 공통원인과 종속성 미포함

### 직렬 Subsystem 근사

\[
PFD_{\mathrm{SIF}} \approx PFD_{\mathrm{Sensor}}+
PFD_{\mathrm{Logic}}+PFD_{\mathrm{Final}}
\]

- 작은 확률과 독립성 가정에서만 근사한다.
- 공통원인과 공유자원은 별도 반영한다.

### 요구사항 추적성 지표

\[
C_{\mathrm{trace}}=
\frac{N_{\mathrm{verified\ requirements}}}
{N_{\mathrm{applicable\ SRS\ requirements}}}
\]

- 프로젝트 품질지표다.
- SIL 달성의 단독 증거가 아니다.

### Proof Test Coverage 개념

\[
C_{PT}=
\frac{\text{Proof Test로 검출 가능한 위험고장}}
{\text{전체 고려 대상 위험고장}}
\]

- 분모의 고장집합과 시험 경계를 명시한다.
- PST Coverage, Diagnostic Coverage와 구분한다.

### Generic IEC 61508 Target Bands

저요구 모드 PFDavg:

- SIL 1: \(10^{-2} \le PFD_{\mathrm{avg}} < 10^{-1}\)
- SIL 2: \(10^{-3} \le PFD_{\mathrm{avg}} < 10^{-2}\)
- SIL 3: \(10^{-4} \le PFD_{\mathrm{avg}} < 10^{-3}\)
- SIL 4: \(10^{-5} \le PFD_{\mathrm{avg}} < 10^{-4}\)

고요구·연속 모드 PFH:

- SIL 1: \(10^{-6} \le PFH < 10^{-5}\)
- SIL 2: \(10^{-7} \le PFH < 10^{-6}\)
- SIL 3: \(10^{-8} \le PFH < 10^{-7}\)
- SIL 4: \(10^{-9} \le PFH < 10^{-8}\)

주의:

- Process Sector 적용범위, 채택 Edition 및 조직 기준은 verify-first 한다.
- PFDavg와 PFH를 서로 바꾸어 사용하지 않는다.

## 8. Fatal 오류

1. SIL 인증 제품을 사용하면 전체 SIF가 자동으로 SIL을 만족한다.
2. SIL은 PLC나 Sensor 같은 개별 장치에만 부여되는 제품 등급이다.
3. Safety Application Program의 정확한 동작만 확인하면 Hardware와 운영절차 검토는 필요 없다.
4. Software 고장은 모두 Random Hardware Failure처럼 일정 고장률로 계산할 수 있다.
5. PFDavg와 PFH는 동일한 지표이므로 Demand Mode와 무관하게 바꾸어 쓸 수 있다.
6. Proof Test를 수행하면 Safety Software Validation이 완료된다.
7. Functional Test 몇 건이 통과하면 전체 SRS Validation이 완료된다.
8. BPCS와 SIS가 다른 CPU이면 독립성이 자동 보장된다.
9. Diversity를 적용하면 Common Cause Failure가 제거된다.
10. Safety Manual은 제품 설명서이므로 설계 가정과 제한을 확인할 필요가 없다.
11. 인증된 Library Block은 Version과 Parameter에 관계없이 재검증이 필요 없다.
12. Proven in Use는 현장에서 오래 사용했다는 진술만으로 성립한다.
13. Tool에서 생성한 Code는 Tool 오류 가능성이 없으므로 검증하지 않아도 된다.
14. Bypass와 Override는 운전 편의를 위한 기능이므로 SIL과 무관하다.
15. 변경이 작은 경우 영향분석과 Regression 없이 Online Modification을 적용해도 된다.
16. 감사와 Competence는 문서 행위일 뿐 기능안전 성과와 관계없다.

## 9. Warn 기준

1. SIS, SIF, SIL을 구분하지만 전체 경로 관계가 불명확하다.
2. SRS를 언급하지만 기능 요구와 무결성 요구를 구분하지 않는다.
3. Random/Systematic Failure를 나열하나 통제 방법 차이를 설명하지 않는다.
4. Verification과 Validation을 모두 언급하지만 목적과 시점을 바꾸어 쓴다.
5. 독립성을 조직 분리만으로 설명하고 기술적 공유자원을 누락한다.
6. Safety Manual과 인증서를 언급하지만 범위·가정·제한을 누락한다.
7. Proven in Use를 언급하지만 Version, 환경, 운전시간, 결함기록을 누락한다.
8. Tool Qualification을 언급하지만 Tool 오류 영향과 검출 가능성을 누락한다.
9. Library Validation을 언급하지만 Version/Parameter/변경통제를 누락한다.
10. Proof Test와 Validation을 같은 것으로 단정하지는 않지만 관계가 모호하다.
11. Bypass/Override를 언급하지만 승인·시간 제한·보상조치·복구 확인 중 일부가 없다.
12. PFD 근사식을 제시하지만 독립성, 시험완전성, 수리시간 또는 Demand Mode 가정을 누락한다.

## 10. False Positive 기준

다음 표현은 문맥 확인 없이 오류로 판정하지 않는다.

- “SIL 2 PLC”는 제품의 인증·Systematic Capability 또는 적용 가능 범위를 줄여 부르는 현장 표현일 수 있다.
- “독립 검증”은 반드시 외부기관만을 의미하지 않는다. 요구 SIL, 조직규모, 역할분리 및 적용 표준에 따라 적정 독립성 수준을 판단한다.
- “검증된 Library”는 무조건 재시험 면제를 뜻하지 않는다. 승인 범위 내 재사용을 뜻할 수 있다.
- “Proof Test에서 Logic을 시험한다”는 표현 자체는 맞을 수 있다. 이를 Software Validation과 동일시할 때만 오류다.
- “BPCS와 SIS 분리”는 일반적으로 바람직하지만 모든 공유자원이 제거되었다는 의미는 아니다.
- “Diversity 적용”은 CCF 저감수단일 수 있다. CCF 완전 제거라고 단정할 때 오류다.
- “Certified Product”는 유효한 증거 중 하나다. 전체 SIF 자동 적합으로 확장할 때 오류다.
- PFD 합산식은 작은 확률과 독립성 가정이 명시된 근사식이면 허용한다.
- IEC 61508의 SIL 4 표기는 일반 표준 설명에서 허용한다. Process Sector 적용성은 별도 확인한다.
- Bypass가 필요한 운전상황 자체를 오류로 보지 않는다. 무통제·무승인·무기한 운용을 오류로 본다.

## 11. Model Answer

SIS는 하나 이상의 SIF를 구현하여 공정위험을 허용 가능한 수준으로 낮추는 계장시스템이다. SIL은 개별 PLC나 Sensor의 단순 제품등급이 아니라 SIF에 요구되는 Safety Integrity 수준이다. 따라서 인증된 Logic Solver를 사용하더라도 Sensor, Application Program, Final Element, 공통원인, 시험주기와 운영절차를 포함한 전체 SIF가 요구를 만족해야 한다.

Safety Lifecycle은 Hazard와 Risk 분석, 보호계층 할당, SRS 작성, 설계·구현, 통합, Verification, Validation, 운전·정비, 변경 및 폐기로 연결된다. SRS에는 Trip 조건, 안전상태, 응답시간, Reset, Bypass, 진단, 환경조건과 SIL 등 기능·무결성 요구가 명확히 기록되어야 한다. 각 요구는 설계, Program, Test Case와 Result까지 양방향으로 추적되어야 한다.

Random Hardware Failure는 열화에 따른 확률적 고장이므로 PFDavg나 PFH로 평가한다. 반면 Systematic Failure는 요구 누락, 설계 오류, Software 결함, Tool·Library 오류, 설치·변경 실수처럼 특정 조건에서 반복될 수 있다. 이는 고장률 계산만으로 해결할 수 없으므로 표준화된 개발절차, 검토, 독립 Verification, Validation, 형상관리와 Competence로 억제한다.

Verification은 각 단계 산출물이 입력 요구를 충족하는지 확인하는 활동이다. Validation은 통합된 SIS가 실제 운전조건에서 SRS를 만족하는지 확인하는 활동이다. Functional Test와 Proof Test는 필요한 시험이지만 Safety Software Validation과 동일하지 않다. Proof Test는 운전 중 숨은 위험고장을 발견하고 기능을 복원하는 주기 시험이다.

독립성과 분리는 공통 오류와 이해충돌을 줄이기 위한 수단이다. 그러나 CPU가 다르더라도 Sensor, 전원, Network, Engineering Tool과 유지보수 인력을 공유하면 공통원인이 남는다. Diversity도 공통원인을 줄일 수 있으나 복잡성과 새로운 체계적 오류를 만들 수 있으므로 근거와 검증이 필요하다.

인증 제품, Safety Manual, Proven in Use, Tool Qualification과 검증 Library는 모두 증거다. 다만 인증 범위, Version, 환경, Parameter, 사용 제한과 운전이력을 확인해야 한다. 변경, Bypass와 Override는 영향분석, 승인, 보상조치, 시간 제한, 기록, Regression 및 독립적인 복구 확인으로 관리한다. 최종적으로 기능안전은 Hardware 수치만이 아니라 Software, 사람, 절차 및 전 수명주기의 증거가 결합되어 달성된다.

## 12. Topic Importance

- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- 고득점 해제 조건:
  1. SIS–SIF–SIL 관계를 정확히 설명
  2. SRS부터 Validation까지 Lifecycle 연결
  3. Random/Systematic Failure 구분과 통제수단 연결
  4. Verification/Validation/Functional Test/Proof Test 구분
  5. 독립성·분리·공통원인·다양성의 Trade-off 설명
  6. 인증·Safety Manual·Proven in Use의 한계 설명
  7. Tool/Library/변경/Bypass/Override 통제 제시
  8. PFDavg/PFH 및 근사식의 적용 가정 명시

## 13. Routing Alias

권장 Alias:

1. `SIS safety software lifecycle`
2. `SIF SIL safety application program`
3. `Safety Requirement Specification SRS`
4. `functional safety verification validation`
5. `systematic failure random hardware failure`
6. `safety PLC application program validation`
7. `independence separation common cause diversity`
8. `IEC 61508 software lifecycle`
9. `IEC 61511 SIS application program`
10. `safety manual certified product`
11. `proven in use functional safety`
12. `tool qualification safety software`
13. `validated library function block`
14. `safety bypass override modification audit competence`

Broad Alias 금지:

- `SIS`
- `SIL`
- `Trip`
- `Interlock`
- `PLC`
- `Verification`
- `Validation`
- `Safety`

## 14. Question Examples

Positive:

1. SIS·SIF·SIL의 관계와 Safety Software Lifecycle을 설명하시오.
2. Safety Application Program의 Systematic Failure 억제방안을 설명하시오.
3. SIS에서 Verification과 Validation의 차이를 설명하시오.
4. SRS와 양방향 Traceability의 필요성을 설명하시오.
5. Safety Software의 독립성, 분리, Common Cause와 Diversity를 설명하시오.
6. Certified Product, Safety Manual과 Proven in Use의 적용 한계를 설명하시오.
7. 기능안전 Tool Qualification과 Library Validation 방안을 설명하시오.
8. Safety Software Modification의 영향분석과 Revalidation 절차를 설명하시오.
9. SIS의 Bypass·Override 관리방안을 설명하시오.
10. Functional Test, Proof Test와 Safety Validation의 관계를 설명하시오.

Negative Boundary:

1. 일반 PLC Sequence와 Step Transition 구현방법을 설명하시오. → SW-02
2. Interlock, Permissive, Trip 및 First-out 논리를 설명하시오. → SW-02
3. 일반 제어 Software의 요구분석, Coding 및 Unit Test 절차를 설명하시오. → SW-04
4. 일반 Software V-Model과 Agile 개발을 비교하시오. → SW-04
5. ESD Valve의 PST Coverage와 Proof Test Interval 산정을 설명하시오. → Final Element/PST Topic
6. Control Valve의 Fail-open/Fail-close 선정방법을 설명하시오. → Control Valve Topic
7. Alarm Rationalization과 Alarm Flood 대책을 설명하시오. → Alarm Topic
8. Industrial Ethernet Protocol의 상호운용성을 설명하시오. → SW-07

## 15. Focused Regression

Focused Test는 Generated Bank와 Production Router를 요구하지 않는다.

검증 항목:

1. 허용 Source 6개와 Test 1개의 존재
2. JSON 4개 Parse
3. 모든 Topic ID 일치
4. Anchor 30개 이상
5. Fatal 16개 이상
6. 필수 Anchor ID 존재
7. 필수 Fatal ID 존재
8. SIL 제품 자동충족, Proof Test=Validation 등 과장 오류 존재
9. SW-02/SW-04 Boundary Marker 존재
10. PFDavg, PFH, RRF, 1oo1 근사식 존재
11. Routing Alias가 복합어 중심이며 Broad Alias를 포함하지 않음
12. Positive/Negative Question Corpus 존재
13. Model Answer Outline과 High Score Point 존재
14. Topic Importance 계약 일치
15. Generated/Production/Common Router를 파일 출력 대상으로 사용하지 않음

## 16. 생성 파일

- `docs/topic_sheets/sis_sil_safety_software_independence_systematic_failure_verification_validation.md`
- `rubrics/topic_packs/sis_sil_safety_software_independence_systematic_failure_verification_validation/README.md`
- `rubrics/topic_packs/sis_sil_safety_software_independence_systematic_failure_verification_validation/fact_anchor.json`
- `rubrics/topic_packs/sis_sil_safety_software_independence_systematic_failure_verification_validation/logic_check.json`
- `rubrics/topic_packs/sis_sil_safety_software_independence_systematic_failure_verification_validation/model_answer.json`
- `rubrics/topic_packs/sis_sil_safety_software_independence_systematic_failure_verification_validation/topic_importance.json`
- `scripts/test_sis_sil_safety_software_topic.py`

## 17. Verify-first 항목

다음은 적용 프로젝트의 표준 Edition, 기업 규정과 인증 범위를 확인한 뒤 확정한다.

- IEC 61508/61511의 세부 Clause 번호
- Process Sector에서 허용·요구되는 SIL 범위
- Verification/Assessment의 구체적 독립성 수준
- Tool Classification과 Qualification 절차
- Proven in Use의 최소 운전시간·Demand 수
- 인증서의 Systematic Capability, Hardware Constraint 및 Architecture 조건
- Proof Test Coverage, Diagnostic Coverage와 Beta Factor의 수치
- Online Modification 허용조건


## Source JSON Contract Summary

- Anchor count: 30
- Fatal count: 16
- Major count: 12
- Routing alias count: 14
- Positive question count: 10
- Negative boundary count: 8

## MC/DC 상세 구조적 커버리지 경계

본 Topic은 기능안전 요구, Systematic Capability, 독립성, Tool Qualification 원칙과 Safety V&V의 엄격도를 소유한다.

MC/DC의 조건별 독립 영향 Test Pair, Coverage Gap 종결, Dead·Deactivated Code, Source·Object Code와 Instrumentation 증거의 상세는 `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`로 이관한다.

MC/DC 100%는 Safety Lifecycle의 하나의 검증증거이며 전체 SIF의 SIL을 단독으로 보장하지 않는다.
