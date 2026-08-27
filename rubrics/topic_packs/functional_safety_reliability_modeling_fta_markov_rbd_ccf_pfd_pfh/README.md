# 기능안전 신뢰도 모델링: FTA·Markov·RBD·CCF·PFDavg·PFH

## Topic ID

`functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`

## 목적

SIS/SIF의 정량적 신뢰도 모델링 방법을 설명하고, 모델 선택과 계산 가정을 구분하는 답안을 평가한다.

핵심 범위는 다음과 같다.

- Reliability Block Diagram(RBD)
- Fault Tree Analysis(FTA)
- Markov Model
- Common Cause Failure(CCF)와 β-factor
- Proof Test Interval과 Proof Test Coverage
- Diagnostic Coverage와 위험고장 분류
- Voting Architecture
- 저수요 모드의 PFDavg
- 고수요·연속수요 모드의 PFH
- Sensor·Logic Solver·Final Element의 전체 SIF 정량화

## 대표 문제

1. 기능안전 시스템의 신뢰도 모델링 기법인 RBD, FTA, Markov Model을 비교하고 적용 방법을 설명하시오.
2. SIS의 PFDavg 또는 PFH 산정 시 CCF, Proof Test, Diagnostic Coverage와 Voting Architecture를 설명하시오.
3. 1oo1, 1oo2, 2oo3 구조의 신뢰도 특성과 정량 평가 시 고려사항을 설명하시오.
4. Target SIL과 Achieved SIL을 구분하고 정량 신뢰도 모델의 가정과 한계를 설명하시오.

## 핵심 정답 기준

- RBD는 성공경로 또는 기능 가용 구조를 중심으로 직렬·병렬 조합을 표현한다.
- FTA는 Top Event에서 원인 고장으로 전개하는 논리 모델이다.
- Markov Model은 상태전이와 복구·진단·시험에 따른 시간 의존 거동을 표현한다.
- 세 모델은 목적과 가정이 다르므로 동일 기법으로 취급하지 않는다.
- 저수요 모드에서는 일반적으로 PFDavg를 사용한다.
- 고수요 또는 연속수요 모드에서는 일반적으로 PFH를 사용한다.
- PFDavg와 PFH의 적용은 SIF의 demand mode와 표준 정의에 연결해야 한다.
- Voting Architecture는 HFT, 안전성, 가용성, Spurious Trip 사이의 trade-off를 가진다.
- CCF를 무시하면 중복구조의 신뢰도를 과대평가한다.
- Proof Test Interval이 길거나 Coverage가 낮으면 검출되지 않은 위험고장의 평균 노출시간이 증가한다.
- Achieved SIL은 Sensor, Logic Solver, Final Element와 지원기능의 전체 SIF를 평가해야 한다.
- 정량 계산은 고장률, 독립성, CCF, 진단, 수리시간, 시험주기와 Coverage 가정을 명시해야 한다.
- 정량 하드웨어 무결성과 체계적 무결성은 서로 대체되지 않는다.

## 정답으로 인정할 표현

- RBD를 “성공경로 중심 모델”, FTA를 “Top Event 원인전개 모델”로 설명한 표현
- Markov Model을 상태전이와 시간 의존성, 복구·시험 상태를 포함하는 모델로 설명한 표현
- PFDavg를 저수요 demand mode의 평균 요구시 실패확률로 설명한 표현
- PFH를 고수요·연속수요에서 시간당 위험고장 빈도 지표로 설명한 표현
- β-factor를 중복 채널의 공통원인 고장 기여분을 분리하는 단순화 모델로 설명한 표현
- Proof Test와 Diagnostic Coverage가 검출 가능한 위험고장 범위와 노출시간에 영향을 준다고 설명한 표현
- 구성요소별 PFD 기여도를 합산하되 독립성과 근사 가정을 명시한 표현

## 핵심 fatal 오류

- PFDavg를 모든 demand mode에 동일하게 적용한다고 단정
- PFH와 PFDavg를 같은 물리량 또는 단순 단위변환 관계로 설명
- 2oo3 또는 HFT만 적용하면 SIL이 자동 보장된다고 설명
- CCF가 중복구조의 정량 결과에 영향을 주지 않는다고 설명
- Proof Test가 체계적 소프트웨어 오류까지 정량적으로 제거한다고 설명
- Partial Stroke Test만으로 전체 Final Element 또는 전체 SIS의 PFDavg가 입증된다고 설명
- FTA, RBD, Markov Model을 목적·가정이 동일한 상호대체 모델로 설명
- 개별 SIL 인증기기 하나로 전체 SIF의 Achieved SIL이 결정된다고 설명
- 정량 하드웨어 계산만으로 체계적 무결성까지 입증된다고 설명

## Warn 수준의 부족한 표현

- PFDavg 또는 PFH 수식만 쓰고 demand mode를 구분하지 않음
- Voting 구조만 나열하고 안전성·가용성·오동작 trade-off를 설명하지 않음
- β-factor만 언급하고 독립성·공통환경·공통시험 절차를 연결하지 않음
- Proof Test Interval은 제시하지만 Coverage와 검출되지 않은 위험고장을 설명하지 않음
- 구성요소 고장률을 제시하지만 Sensor–Logic–Final Element의 전체 SIF 경계를 설명하지 않음
- 계산 결과만 쓰고 가정, 근사조건과 불확실성을 제시하지 않음

## False positive 주의사항

- “PFDavg는 고수요 모드 지표가 아니다”와 같은 부정형 정답을 오답으로 잡지 않는다.
- “2oo3만으로 SIL이 보장되는 것은 아니다”와 같은 반박 문장을 fatal로 잡지 않는다.
- FTA, RBD, Markov를 비교하기 위해 같은 문장에 병기한 것을 동일 기법 주장으로 해석하지 않는다.
- 단순화 계산에서 독립고장 가정을 명시한 경우, CCF를 무조건 누락 오류로 처리하지 않고 적용범위를 확인한다.
- 표·수식·블록도는 배치 자체가 아니라 주변 설명에서 읽히는 claim을 평가한다.
- β-factor 이외의 CCF 모델을 사용한 답안을 오답으로 처리하지 않는다.

## 표와 다이어그램 처리 메모

다음 표현을 claim evidence로 인정한다.

- RBD의 직렬·병렬 성공경로
- FTA의 AND/OR Gate와 Top Event 전개
- Markov State Transition Diagram
- 1oo1·1oo2·2oo3 Voting 표
- λDU, λDD, DC, T1, MTTR, β를 표시한 계산식
- Sensor·Logic Solver·Final Element의 PFD 기여도 표

도식만 있고 의미 설명이 없으면 fatal이 아니라 coverage 부족으로 평가한다.

## 현장 적용 판단 기준

- SRS의 demand mode와 Target SIL 확인
- Failure Rate Data의 출처와 적용 조건 확인
- Independent Failure와 CCF 분리
- Diagnostic Coverage와 Proof Test Coverage 구분
- Proof Test Interval, Repair Time, Bypass Time 반영
- Degraded Voting과 Maintenance Override 반영
- Sensor·Logic Solver·Final Element 및 Utility의 전체 경계 확인
- 계산 모델 검증과 실제 시험·운영 데이터 피드백

## 인접 Topic 경계

- `hazop_lopa_ipl_risk_reduction_sil_target_allocation`
  - 위험분석, RRF와 Target SIL 할당을 주로 담당한다.
- `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture`
  - HIPPS 적용 사례와 과압보호 구조를 담당한다.
- `final_control_element_sil_sis_esd_valve_partial_stroke_test`
  - Final Element와 PST 적용을 담당한다.
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`
  - 체계적 고장, 소프트웨어 검증, 독립성과 기능안전 관리 경계를 담당한다.
- `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis`
  - 소프트웨어 구조적 커버리지와 MC/DC를 담당한다.

본 Topic은 위 사례를 포괄하는 일반 정량 신뢰도 모델링을 담당하며, 위험 할당이나 소프트웨어 수명주기를 대체하지 않는다.

## 검토 메모

- 신규 Topic 후보 C의 semantic ownership 판정 결과에 따라 생성한다.
- A·B·D 기존 Topic 보강은 이 Topic과 분리하여 후속 commit에서 수행한다.
- generated bank는 source JSON 검토와 focused validation 전에는 갱신하지 않는다.
