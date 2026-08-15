# HIPPS 과압보호시스템의 구조, Voting Architecture 및 Relief System 비교

## Topic ID

`hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture`

## 목적

HIPPS가 과압원 유입을 차단하는 전체 SIF로 동작하는 원리, 2oo3 Sensor와 조건부 1oo2 Final Element Architecture, Relief System과의 기능·비용·적용조건 차이를 채점한다.

## 대표 문제

1. HIPPS의 정의, 구성과 과압보호 동작원리를 설명하시오.
2. 2oo3 Sensor Voting과 degraded mode를 설명하시오.
3. 직렬 Shutdown Valve의 1oo2 구조와 적용조건을 설명하시오.
4. HIPPS와 Relief System의 장단점 및 선정기준을 비교하시오.

## Topic boundary

이 Topic이 소유하는 범위:

- HIPPS 전체 SIF 경계와 과압원 차단 메커니즘
- Trip setpoint, Process Safety Time과 pressure transient
- 2oo3 Sensor voting, degraded mode와 common cause
- 직렬 Final Element의 조건부 1oo2 구조
- Closure Time, Surge, Seat Leakage와 Fail-safe energy
- Target SIL, PFDavg와 BPCS 독립성
- HIPPS와 Relief System의 비교·대체·병행 선정
- SRS, Proof Test, Bypass, MOC와 Revalidation

인접 Topic으로 넘기는 범위:

- HAZOP·LOPA를 이용한 목표 SIL 산정 자체
- Final Element의 상세 PFDavg·PST 계산
- Relief Valve sizing, API fire case와 flare hydraulic 상세
- SIS software lifecycle 일반론

## 핵심 정답

- HIPPS는 유입을 차단하는 예방형 SIF이고 Relief Device는 배출에 의한 완화수단이다.
- 2oo3와 1oo2는 고정 정답이 아니라 Safe State, SIL, common cause와 availability 조건으로 선정한다.
- 전체 응답시간은 Process Safety Time보다 짧아야 한다.
- 전체 HIPPS PFDavg와 독립성을 검증해야 한다.
- Relief 대체 가능성은 Code와 모든 잔여 과압원을 포함해 판단한다.

## Fatal 오류

- HIPPS와 Relief Valve를 동일시함
- 2oo3가 자동으로 SIL을 보장한다고 단정함
- 직렬 두 Valve를 조건 없이 1oo2로 간주함
- 빠른 폐쇄가 항상 안전하다고 단정함
- HIPPS가 모든 Relief Device를 자동 대체한다고 단정함
- Target SIL과 Achieved SIL을 동일시함

## 관리 원칙

Source 내용과 release 상태는 git history, validator 결과와 SRS 변경관리 기록으로 추적한다.
