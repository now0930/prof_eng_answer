# HAZOP·LOPA·독립보호계층을 이용한 목표 SIL 결정 및 SIF 할당

## 1. Topic metadata

- Topic ID: `hazop_lopa_ipl_risk_reduction_sil_target_allocation`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Source authoring: `docs/topic_pack_workflow.md`의 직접 authoring 절차

## 2. Scope and ownership

본 Topic은 HAZOP에서 도출한 원인–결과를 LOPA scenario로 정규화하고, initiating event frequency, conditional modifier와 적격 IPL의 PFD를 이용해 residual frequency를 계산한 후 target RRF·PFDavg·SIL을 정하고 SIF/SRS로 인계하는 과정만 소유한다.

다음은 인접 Topic으로 넘긴다.

- 일반 SIS/SIL software lifecycle과 verification/validation
- Final element의 상세 PST·proof-test 계산
- Relief device sizing과 flare system
- HAZOP facilitation 전체 절차

## 3. Core correct facts

1. HAZOP은 deviation, cause, consequence와 safeguard를 식별하지만 SIL을 직접 정하지 않는다.
2. LOPA는 명확한 initiating event와 consequence endpoint를 갖는 scenario 단위 분석이다.
3. Initiating event frequency는 적용 경계와 자료 근거를 가져야 한다.
4. Conditional modifier와 IPL PFD는 역할이 다르며 중복 반영하지 않는다.
5. IPL은 independence, specificity, dependability, auditability를 충족해야 한다.
6. 공유 Sensor·Logic·Final Element·전원·절차는 common cause와 double counting 관점에서 검토한다.
7. Residual frequency는 initiating frequency × modifier × credited IPL PFD로 산정한다.
8. Residual frequency와 tolerable frequency의 비로 추가 RRF 요구를 판단한다.
9. Low-demand 근사에서 PFDavg_target ≤ 1/RRF_required 관계를 사용한다.
10. Target SIL은 요구사항이고 achieved SIL은 설계검증 결과다.
11. LOPA 결과는 전체 SIF 경계와 SRS 요구로 인계한다.
12. 변경 시 MOC와 revalidation으로 LOPA와 SRS를 갱신한다.

## 4. Acceptable expressions

- IPL: 독립보호계층, independent protection layer
- Residual frequency: 보호계층 적용 후 scenario frequency
- RRF: risk reduction factor, 위험감소계수
- PFDavg: 평균 요구시고장확률
- Target SIL: 요구 SIL, 목표 SIL
- Achieved SIL: 검증된 SIL, 달성 SIL

## 5. Fatal wrong claims

- HAZOP risk ranking만으로 SIL이 자동 결정된다.
- 종속된 보호기능도 각각 독립 IPL로 곱할 수 있다.
- 계획된 safeguard는 설치 전부터 credit할 수 있다.
- RRF가 커질수록 허용 PFDavg도 커진다.
- Target SIL과 achieved SIL은 동일하다.
- 인증 부품 하나가 전체 SIF SIL을 보장한다.

## 6. Warn-level weak claims

- Initiating event frequency의 근거가 없다.
- Conditional modifier의 적용조건이 없다.
- Alarm/operator action의 response time과 절차가 없다.
- SIF 경계 또는 process safety time이 없다.
- Proof test, bypass와 MOC 요구가 없다.

## 7. False positive cautions

- “독립적이지 않다”라는 문구가 dependency 위험을 지적하는 올바른 설명일 수 있다.
- “SIL이 필요 없다”는 문구는 RRF_required ≤ 1인 특정 scenario에서 조건부로 옳을 수 있다.
- PFDavg 수치범위는 low-demand mode임을 명시한 경우에만 동일 기준으로 평가한다.
- BPCS credit을 무조건 금지하는 것이 아니라 initiating cause와의 독립성을 확인해야 한다.

## 8. Expected question patterns

1. HAZOP 결과를 LOPA scenario로 전환하고 목표 SIL을 결정하는 절차를 설명하시오.
2. LOPA 계산절차와 residual frequency 및 RRF 산정방법을 설명하시오.
3. IPL 인정조건과 double counting 방지방안을 설명하시오.
4. BPCS와 Alarm·Operator Action의 IPL 인정조건을 설명하시오.
5. RRF, PFDavg와 SIL의 관계를 설명하시오.
6. Target SIL과 achieved SIL을 비교하시오.
7. LOPA 결과의 SIF/SRS 할당방법을 설명하시오.
8. LOPA 변경관리와 revalidation 방안을 설명하시오.

## 9. Fact Anchor guidance

Fact Anchor는 정의, 계산관계, 적용조건, IPL 적격성, target/achieved 구분과 SRS handoff를 atomic statement로 분리한다. 표준 Clause 번호나 회사 고유 risk criterion은 일반 Fact로 고정하지 않는다.

## 10. Model Answer guidance

답안은 HAZOP → scenario → frequency/modifier → IPL qualification → residual risk → RRF/PFDavg/SIL → SIF/SRS → MOC 순서로 전개한다.

## 11. Logic Check guidance

Fatal 판정은 문맥상 명백한 correctness error에만 적용한다. 단순 키워드 또는 부정어만으로 cap을 적용하지 않는다.

## 12. Topic Importance guidance

계산식뿐 아니라 독립성 판단과 수명주기 handoff가 고득점 unlock 조건이다. Difficulty는 점수를 직접 부여하지 않는다.

## 13. Cross-topic handoff

- 일반 기능안전 Lifecycle: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- Final element 진단·PST: `final_control_element_sil_sis_esd_valve_partial_stroke_test`
- 본 Topic은 위 Topic의 세부 설계를 재소유하지 않는다.

## 14. Human review checklist

- [ ] Scenario의 initiating event와 consequence endpoint가 명확한가
- [ ] Modifier와 IPL을 중복 적용하지 않았는가
- [ ] IPL independence와 common cause를 검토했는가
- [ ] RRF와 PFDavg 관계가 올바른가
- [ ] Target SIL과 achieved SIL을 구분했는가
- [ ] SIF 경계와 SRS handoff가 있는가
- [ ] MOC와 revalidation이 있는가
- [ ] Generated bank를 직접 수정하지 않았는가
