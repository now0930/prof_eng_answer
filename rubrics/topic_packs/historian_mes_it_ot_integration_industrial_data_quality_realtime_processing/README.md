# Historian·MES·IT/OT 통합, 산업데이터 품질 및 실시간 처리

## Topic ID

`historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`

## Lane

`SOFTWARE_LLM_LANE_C`

## Scope

- Historian, MES, ERP와 ISA-95
- IT/OT integration, Edge와 Gateway
- Timestamp, Time alignment와 Quality Code
- Store-and-forward, Streaming, Compression과 Deadband
- Metadata, Context, Tag Naming, Namespace와 Information Model
- Master Data, Governance, Retention, Traceability와 Batch Genealogy

## Ownership Boundary

- SW-07: 데이터를 전달하는 Protocol과 Wire-level 상호운용
- SW-11: 전달된 데이터의 시간·품질·의미·저장·Context와 상위 시스템 통합
- SW-12: 산업데이터를 이용한 학습·추론과 Model Lifecycle
- SW-02: PLC/DCS Sequence, Interlock과 Trip Logic

## Authoring Contract

- Fact Anchor: 30
- Fatal misconception: 16
- Major/Warn condition: 12
- Routing alias: 14
- Positive question: 10
- Negative boundary question: 8
- Deterministic checks: disabled
- Generated Bank promotion: excluded
- Production Python/Common Router modification: excluded

## Representative Question

Historian·MES·ERP의 역할과 ISA-95 기반 IT/OT 통합 구조를 설명하고, 산업데이터의 Timestamp·Quality·Context·실시간 처리 및 Traceability 관리방안을 제시하시오.

## Fatal Guard

- Historian은 단순 Backup Database가 아니다.
- MES와 ERP의 역할은 동일하지 않다.
- ISA-95는 단일 Wire Protocol이 아니다.
- 도착시간은 항상 Event Time과 같지 않다.
- Bad·Uncertain 데이터와 Quality Code를 묵시적으로 폐기하지 않는다.
- Compression·Deadband와 Store-and-forward는 완전 보존을 자동 보장하지 않는다.
- Protocol 연결은 Semantic Interoperability를 자동 보장하지 않는다.
- 실시간 처리는 0 지연을 의미하지 않는다.

## Verify-first

ISA-95 세부 Mapping, Vendor Quality Bit, Historian Compression, Deadline, Clock 정확도, Store-and-forward 전달보장과 Retention 수치는 적용 Architecture로 확인한다.
