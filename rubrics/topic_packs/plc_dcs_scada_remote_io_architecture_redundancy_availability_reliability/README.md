# PLC·DCS·SCADA·PC 기반 및 Remote I/O 제어시스템의 구조·이중화·가용도·신뢰도

## 1. Topic 역할

- 레벨: `L2_CANONICAL_SOFTWARE_TOPIC`
- 상위 분야: 제어 플랫폼과 운전논리
- 질문유형: `COMPARE_SELECTION`
- 난이도: `THEORY_CORE`
- 중요도: `CORE_MUST_PREPARE`

본 Topic은 PLC·DCS·SCADA·PC 기반 제어와 Remote I/O의 역할, 제어시스템 계층구조, CPU·전원·I/O·서버·통신망 이중화, 고장검출·상태동기화·Bumpless Transfer, Reliability·Maintainability·Availability, Single Point of Failure와 Common Cause Failure를 통합한다.

## 2. 핵심 요구사항

1. PLC·DCS·SCADA·PC 기반 제어와 Remote I/O의 역할·구조·선정
2. 현장·제어·감시계층과 End-to-End 제어경로
3. CPU·전원·I/O·서버·네트워크 이중화
4. Watchdog·Heartbeat·자가진단을 이용한 고장검출·격리
5. 상태동기화·출력추종·Bumpless Transfer
6. Failover 기준과 Degraded Mode·Local Control
7. Reliability·Maintainability·Availability와 MTBF·MTTR
8. Single Point of Failure와 Common Cause Failure
9. 독립성·다양성·물리적 분리
10. 정기 절체시험·복구훈련·정량 수용기준과 생애주기 Trade-off

## 3. 핵심 식

수리가능 시스템의 단순 정상상태 고유가용도는 다음과 같이 평가한다.

`A = MTBF / (MTBF + MTTR)`

단, 일정 고장률·수리율, 평균시간 및 계획정지 제외 등의 적용조건을 명시한다.

독립고장 가정에서 직렬구조의 신뢰도는 구성요소 신뢰도의 곱으로 감소한다. 병렬 이중화는 동시 독립고장 확률을 줄이지만 Common Cause Failure를 별도로 반영해야 한다.

## 4. 기존 Topic 관계

- `plc_dcs_remote_io`: Legacy Seed
- `reliability_maintainability_availability_ram`: Legacy Seed
- `hmi_scada`: SW-01 구조와 SW-03 운전정보 관리 사이의 Legacy Handoff
- `smart_mcc_motor_control_center_monitoring`: L3 Application Child

기존 Topic은 삭제하거나 이름을 변경하지 않는다.

## 5. 인접 Topic 경계

- SW-03: Alarm·Setpoint·Trip·SOE·화면·운전권한
- SW-05: SIS·SIL 안전무결성, 체계적 고장과 안전 V&V
- SW-07: 산업통신 프로토콜·매체·토폴로지·상호운용성
- SW-08: Latency·Jitter·결정성·시간동기화·복구시간
- SW-09: OT 사이버보안·Allowlisting·공급망·사고대응
- SW-10: 설계문서·FAT·SAT·시운전·인수
- SW-11: Historian·MES·ERP·IT/OT 데이터 통합
- SW-12: 이상탐지·예지보전·AI 모델 수명주기

## 6. 대표 문제

- PLC·DCS·SCADA·PC 기반 제어시스템과 Remote I/O의 구조, 특징 및 선정기준을 비교하시오.
- DCS의 CPU·전원·통신망 이중화와 고장진단·무정전 절체를 설명하시오.
- Active/Standby 제어기의 상태동기화와 Bumpless Transfer 절차를 설명하시오.
- 제어시스템의 Reliability·Maintainability·Availability와 MTBF·MTTR 관계를 설명하시오.
- 이중화 시스템의 Single Point of Failure와 Common Cause Failure 대책을 설명하시오.

## 7. 고득점 기준

- 장비명 나열이 아니라 제어경로와 장애영향을 구조적으로 설명한다.
- CPU 외의 전원·I/O·서버·네트워크 단일고장점을 포함한다.
- 상태동기화가 Bumpless Transfer의 전제임을 설명한다.
- Reliability와 Availability를 구분하고 MTBF·MTTR 관계를 정량화한다.
- 이중화의 한계인 Common Cause Failure와 유지보수·시험을 포함한다.
- 절체시간·출력변동·데이터손실·복구시간을 수용기준으로 제시한다.
