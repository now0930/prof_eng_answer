# HAZOP·LOPA·독립보호계층을 이용한 목표 SIL 결정 및 SIF 할당

## Topic ID

`hazop_lopa_ipl_risk_reduction_sil_target_allocation`

## 목적

HAZOP에서 식별한 원인–결과를 LOPA scenario로 정규화하고, 적격 IPL의 위험감소를 반영하여 목표 RRF·PFDavg·SIL을 결정한 뒤 SIF와 SRS로 인계하는 판단을 채점한다.

## 대표 문제

1. HAZOP 결과를 LOPA scenario로 전환하고 목표 SIL을 결정하는 절차를 설명하시오.
2. IPL 인정조건과 double counting 방지방안을 설명하시오.
3. RRF, PFDavg, target SIL과 achieved SIL의 관계를 설명하시오.
4. LOPA 결과를 SIF와 SRS에 할당하는 방법을 설명하시오.

## Topic boundary

이 Topic이 소유하는 범위:

- HAZOP deviation에서 LOPA 원인–결과 scenario로의 전환
- Initiating event frequency와 conditional modifier
- IPL 적격성, 독립성, 공통원인과 이중계산
- Residual frequency, tolerable frequency, RRF와 PFDavg
- Target SIL 결정과 SIF/SRS 할당
- 다중 scenario, MOC와 revalidation

인접 Topic으로 넘기는 범위:

- SIL verification의 상세 하드웨어 구조제약과 software lifecycle 일반론
- SIF final element의 PST, 진단과 proof-test 계산 상세
- Relief valve sizing과 flare/vent system 설계
- HAZOP 회의 운영기법 전반과 위험행렬 일반론

## 핵심 정답

- HAZOP은 hazard identification이고 LOPA는 scenario별 risk reduction gap 평가다.
- 독립성·특정성·신뢰성·감사가능성이 입증된 IPL만 credit한다.
- Residual frequency를 tolerable event frequency와 비교하여 RRF_required를 구한다.
- Low-demand 조건에서 PFDavg_target과 SIL band를 연결한다.
- Target SIL과 achieved SIL을 분리한다.
- LOPA 결과를 전체 SIF 경계와 검증 가능한 SRS 요구로 인계한다.

## Fatal 오류

- Consequence severity 또는 HAZOP ranking만으로 SIL 자동 지정
- 종속 보호기능의 PFD 중복 곱셈
- 미구현 recommendation의 IPL credit
- RRF–PFDavg 관계 역전
- Target SIL을 achieved SIL로 간주
- Component certificate만으로 전체 SIF SIL 결정

## 검토 상태

- Topic Sheet: 직접 작성
- Source JSON: 직접 작성
- Generated bank: 변경하지 않음
- Commit/Push: 수행하지 않음

## Scope and adjacent Topic ownership

- This Topic Pack owns HAZOP deviation analysis, LOPA initiating-event and
  IPL crediting, IPL independence and no-double-counting checks, risk-gap
  context, and target SIL allocation.
- Demand-mode selection is explicit: low-demand uses PFDavg, while
  high-demand or continuous mode uses PFH. Detailed FTA, Markov, RBD, CCF,
  proof-test, voting, diagnostic-coverage, PFDavg, and PFH derivations belong
  to `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`.
- Partial-stroke-test procedures and detailed final-element diagnostics remain
  in the HIPPS or final-element Topic Packs; PST is only an adjacent example
  here.
- SIL means Safety Integrity Level (안전 무결성 수준). Safety Instrument Level
  is incorrect; SIS separately means Safety Instrumented System.
