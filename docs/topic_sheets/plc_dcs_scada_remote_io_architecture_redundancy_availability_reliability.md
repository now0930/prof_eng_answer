# Topic Sheet: PLC·DCS·SCADA·PC 기반 및 Remote I/O 제어시스템의 구조·이중화·가용도·신뢰도

## 1. 출제범위 위치

- L0: 산업계측제어 소프트웨어
- L1: 제어 플랫폼과 운전논리
- L2: PLC·DCS·SCADA·PC 기반 및 Remote I/O 제어시스템의 구조·이중화·가용도·신뢰도
- L3: PLC/DCS/SCADA 비교, Remote I/O, 이중화, RAM, Bumpless Transfer, SPOF·CCF, 유지보수·시험

## 2. 출제 의도

본 Topic은 제어시스템 구성요소를 단순 나열하는 문제가 아니다. 공정 요구와 장애영향을 기준으로 플랫폼을 선정하고, End-to-End 제어경로의 단일고장점을 식별하며, 고장검출·상태동기화·절체·성능저하 운전·복구를 하나의 수명주기로 설명하는 능력을 평가한다.

## 3. 필수 답안 요소

### 3.1 플랫폼과 계층구조

- PLC: 고속 논리·시퀀스·기계제어
- DCS: 연속공정·분산제어·통합운전·고가용성
- SCADA: 광역 감시·데이터 수집·원격운전
- PC 기반 제어: 유연성·확장성과 실시간성·OS·패치 위험
- Remote I/O: 배선절감·분산설치와 통신·공통전원 장애영향

### 3.2 이중화와 절체

- CPU·전원·I/O·서버·통신망의 계층별 이중화
- Active/Standby와 Heartbeat·Watchdog·자가진단
- 프로그램·내부상태·PID 적분상태·Sequence·Setpoint·출력 동기화
- Bumpless Transfer
- 오절체 위험과 공정 허용시간을 고려한 Failover 기준
- Degraded Mode·Local Control·Fallback
- 복구·재동기화·계획된 원복

### 3.3 RAM과 고장분석

- Reliability, Maintainability, Availability 구분
- MTBF와 MTTR
- `A = MTBF / (MTBF + MTTR)`의 적용조건
- 직렬·병렬 신뢰도와 독립고장 가정
- Single Point of Failure
- Common Cause Failure
- 독립성·다양성·물리적 분리

### 3.4 운영과 수용기준

- 온라인 유지보수
- 정기 절체시험과 복구훈련
- 예비품·장애기록·절차 표준화
- 고장검출시간·절체시간·출력변동·데이터손실·복구시간
- 공정중단 결과·정비능력·생애주기비용에 따른 선정

## 4. 권장 답안 순서

1. 공정 요구와 고가용도 목적
2. 플랫폼 및 계층구조
3. 이중화 대상과 Active/Standby 구조
4. 고장검출·상태동기화·Bumpless Transfer
5. Degraded Mode·Local Control·복구
6. RAM 정량평가
7. SPOF·CCF 및 저감대책
8. 유지보수·시험·수용기준·선정 Trade-off

## 5. 치명적 오개념

- 이중화만 하면 Common Cause Failure가 제거된다는 주장
- 상태동기화 없이 Bumpless Transfer가 가능하다는 주장
- Remote I/O 통신상실에도 모든 기능이 항상 정상이라는 주장
- Reliability와 Availability가 동일하다는 주장
- MTBF만으로 Availability가 결정된다는 주장
- CPU 이중화만으로 End-to-End 단일고장점이 제거된다는 주장
- 복구 후 검증 없이 즉시 원복해야 한다는 주장

## 6. Topic 경계

- SW-03은 Alarm·Setpoint·Trip·SOE·화면·운전권한의 상세 관리를 담당하고, SW-01은 HMI·SCADA 서버의 아키텍처와 이중화 역할만 담당한다.
- SW-05는 SIS·SIL 안전무결성과 체계적 고장을 담당하고, SW-01은 일반 제어시스템의 가용도·고장허용·공통원인고장을 담당한다.
- SW-07은 프로토콜·매체·토폴로지·상호운용성 선정을 담당하고, SW-01은 통신망을 이중화 아키텍처 구성요소로 다룬다.
- SW-08은 Latency·Jitter·결정성·시간동기화·복구시간을 담당하고, SW-01은 시스템 수준의 네트워크 이중화 목적과 절체결과를 담당한다.
- SW-09는 Zone·Conduit·DMZ·Firewall·Allowlisting·공급망 보안을 담당하며 SW-01은 가용도와 복구 관점의 최소 보안 고려만 포함한다.
- SW-10은 설계문서·FAT·SAT·시운전·인수 절차를 담당하고, SW-01은 기술적 구조와 수용기준을 담당한다.
- SW-11은 Historian·MES·ERP·IT/OT 데이터 통합과 데이터 품질을 담당하고, SW-01은 SCADA·서버·통신의 제어 아키텍처를 담당한다.
- SW-12는 진단데이터 기반 이상탐지·예지보전·AI 모델을 담당하고, SW-01은 제어플랫폼의 구조와 신뢰성을 담당한다.
