# Historian·MES·IT/OT 통합, 산업데이터 품질 및 실시간 처리

## Topic

- SW 번호: `SW-11`
- Topic ID: `historian_mes_it_ot_integration_industrial_data_quality_realtime_processing`
- 한글 주제: Historian·MES·IT/OT 통합, 산업데이터 품질 및 실시간 처리
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`

## 범위

포함 범위:

1. Historian의 시계열 수집·저장·조회·압축·Retention
2. MES와 ERP의 역할 및 ISA-95 기반 계층·인터페이스
3. IT/OT 통합, Edge와 Gateway
4. Timestamp, Event Time, Time synchronization과 Time alignment
5. Quality Code, Bad·Uncertain 데이터와 Data Quality
6. Streaming, Event, Store-and-forward와 실시간 처리
7. Compression, Deadband와 Event 보존
8. Metadata, Context, Tag Naming, Namespace와 Information Model
9. Master Data, Data Governance, Retention과 Traceability
10. Batch Genealogy

## 제외 범위

- OPC UA, MQTT, Modbus, EtherNet/IP 등 Protocol Frame·QoS·Wire-level 상호운용 상세
- 산업 AI의 Training, Validation, Precision·Recall, Drift와 MLOps
- PLC Sequence, Interlock, Trip과 실시간 제어 Logic
- Network Segmentation, Zero Trust와 Cybersecurity 상세
- Digital Twin, Robot Planning과 Closed-loop AI
- Generated Bank, 공통 Router, Production Python과 공통 Release Script 수정

## 인접 Topic Ownership

### SW-07과의 경계

SW-07이 소유하는 내용:

- 산업통신 Protocol 구조와 전송 메커니즘
- OPC UA, MQTT, Modbus 등 Protocol 특성
- QoS, Session, Addressing과 Wire-level 상호운용

SW-11이 소유하는 내용:

- 전달된 값의 Timestamp, Quality와 Context
- Historian 저장·압축·Retention
- MES·ERP 연계와 ISA-95 정보경계
- Metadata, Master Data, Information Model과 Governance
- Traceability와 Batch Genealogy

### SW-12와의 경계

SW-11이 소유하는 내용:

- 학습 전 산업데이터 수집, 품질, 시간, Context와 관리 기반

SW-12가 소유하는 내용:

- Feature Engineering, Training, Validation, Inference
- Anomaly Detection, Predictive Maintenance
- Precision·Recall·F1, Drift, Retraining과 MLOps

### SW-02와의 경계

- SW-02는 PLC/DCS의 Sequence, Interlock, Trip과 Fail-safe Logic을 소유한다.
- SW-11은 해당 제어계층에서 생성된 데이터를 상위 시스템이 해석·저장·활용하는 구조를 소유한다.


## 대표 문제

> Historian·MES·ERP의 역할과 ISA-95 기반 IT/OT 통합 구조를 설명하고, 산업데이터의 Timestamp·Quality·Context·실시간 처리 및 Traceability 관리방안을 제시하시오.

## 핵심 Fact

1. Historian은 공정·설비의 시계열 데이터를 장기간 수집·압축·조회하고 품질·시간 정보를 함께 보존하는 운영 데이터 기반이다.
2. Historian은 단순 백업 저장소가 아니며 추세, Event, 품질, 압축, Context와 추적성 조회를 지원한다.
3. MES는 생산지시를 현장 실행으로 전개하고 작업·실적·품질·자원·공정상태와 Genealogy를 관리하는 제조운영 계층이다.
4. ERP는 주문, 계획, 자재, 원가, 재무와 기업 자원을 관리하며 MES의 상세 실시간 제어 기능을 대체하지 않는다.
5. ISA-95는 기업과 제조운영·제어 계층의 기능, 정보객체와 인터페이스 경계를 정리하는 참조모델이지 단일 통신 Protocol이 아니다.
6. IT/OT 통합은 제어 안정성을 보존하면서 Edge·Gateway·Historian·MES·ERP 사이의 책임, 데이터 계약과 보안 경계를 계층적으로 설계해야 한다.
7. Edge와 Gateway는 현장 Protocol 수용, Buffering, 전처리, 품질 매핑과 Store-and-forward를 수행할 수 있으나 중앙 Context와 Governance를 대체하지 않는다.
8. Timestamp는 가능하면 데이터 발생원에 가까운 곳에서 Event Time으로 생성하고 수집·처리·저장 시간과 구분한다.
9. 다중 설비 데이터의 인과관계와 순서를 비교하려면 Clock 동기화, 시간대·Offset·Drift 관리와 Time alignment가 필요하다.
10. Quality Code는 Good·Bad·Uncertain과 원인·상태 정보를 데이터 값과 함께 전달하며 시스템 간 의미 매핑이 필요하다.
11. Bad·Uncertain 데이터는 유효값이나 0으로 묵시 변환하지 말고 원 품질, 대체 규칙, 추정 여부와 사용 제한을 전파해야 한다.
12. 데이터 완전성은 기대한 Record 또는 Tag·주기 대비 실제 유효하게 수집된 데이터의 비율과 Gap 분포로 평가한다.
13. 데이터 적시성은 Event 발생부터 소비 시스템에서 사용 가능해질 때까지의 지연과 변동을 업무 요구와 비교해 평가한다.
14. Store-and-forward는 통신 단절 중 데이터를 Local Buffer에 보관하고 복구 후 재전송하지만 용량, 순서, 중복, 만료와 재전송 속도를 설계해야 한다.
15. Streaming 처리는 연속 데이터와 Event를 도착 즉시 또는 작은 Window 단위로 처리하며 Event Time, 순서 뒤바뀜과 Late Data 정책을 가져야 한다.
16. Compression과 Deadband는 저장량·통신량을 줄이지만 작은 변화, 짧은 Event와 분석 재현성을 손상할 수 있어 목적별 한계와 예외를 설정한다.
17. 값 변화가 작아도 Quality 변경, 상태 전이, Alarm·Event와 Batch 경계는 Deadband와 Compression에서 별도 보존해야 한다.
18. Metadata와 Context는 Tag의 단위, 설비, 위치, 측정점, 공정단계, 제품, Batch와 Calibration 상태를 연결해 데이터 의미를 만든다.
19. Tag Naming과 Namespace는 중복과 충돌을 줄이는 식별체계이며 이름만으로 전체 의미를 표현하려 하지 말고 Metadata와 Information Model에 연결한다.
20. Information Model은 Asset·공정·제품·상태와 관계를 구조화하여 서로 다른 시스템이 같은 의미로 데이터를 해석하도록 한다.
21. 설비, 품목, 공정, Recipe, 작업장과 단위 같은 Master Data의 식별자와 Version을 시스템 간 일관되게 관리해야 한다.
22. Data Governance는 데이터 Owner·Steward, 정의, 품질규칙, 접근권한, 변경승인과 문제조치 책임을 정한다.
23. Retention 정책은 원시값·압축값·Event·Audit 데이터별 보존기간, 법규·업무 요구, 비용, 삭제와 Archive를 구분한다.
24. Traceability는 원천, 변환, 품질판정, 전송, 저장, 소비와 변경이력을 연결해 결과의 재현과 Audit을 가능하게 한다.
25. Batch Genealogy는 원자재 Lot, 설비, Recipe·Version, 작업·공정조건, 품질결과와 완제품 Lot의 관계를 시간과 식별자로 연결한다.
26. Data Acquisition은 Scan 주기, Sampling, Exception·Report 정책, Scaling, 단위와 품질을 함께 정의해야 하며 단순 수집속도만의 문제가 아니다.
27. Event와 상태 Snapshot은 목적이 다르며 Event 순서·원인 분석에는 상태 변화 기록과 Sequence 정보가 필요하다.
28. 실시간 처리는 지연이 0이라는 뜻이 아니라 업무·제어 목적에 맞는 유한한 Deadline, 지연 예산과 결정성 수준을 만족하는 것이다.
29. Protocol 연결이 성공해도 단위, 품질, Timestamp, 식별자와 Context가 일치하지 않으면 Semantic Interoperability는 달성되지 않는다.
30. SW-07은 데이터 전달 Protocol과 상호운용을, SW-11은 전달된 데이터의 의미·품질·저장·Context와 상위 통합을, SW-12는 그 데이터를 이용한 학습·추론을 소유한다.


## 필수 수식·지표

### 데이터 완전성

\[
C_{\mathrm{complete}}=
\frac{N_{\mathrm{valid}}}{N_{\mathrm{expected}}}
\]

- 기대 Record의 정의에는 Tag 수, Sampling 주기, 계획정지와 품질 허용기준을 포함한다.
- 단일 평균뿐 아니라 연속 Gap의 길이와 위치를 함께 본다.

### 데이터 적시성

\[
L=t_{\mathrm{available}}-t_{\mathrm{event}}
\]

- \(t_{\mathrm{event}}\)는 발생시각, \(t_{\mathrm{available}}\)은 소비 시스템에서 사용 가능한 시각이다.
- Clock 오류가 있으면 음수 또는 비정상 지연이 나타날 수 있으므로 시간품질을 함께 확인한다.

### Time alignment 오차

\[
E_{\mathrm{align}}=
\max_i \left|t^{\mathrm{corr}}_i-t_{\mathrm{ref}}\right|
\]

- \(t^{\mathrm{corr}}_i\)는 Offset·Drift를 보정한 Timestamp다.
- 허용오차는 공정 Dynamics와 분석목적에 따라 정한다.

### Compression Ratio

\[
CR=
\frac{N_{\mathrm{raw}}}{N_{\mathrm{stored}}}
\quad\text{또는}\quad
CR_B=
\frac{B_{\mathrm{raw}}}{B_{\mathrm{stored}}}
\]

- 높은 압축률이 높은 데이터 품질을 뜻하지 않는다.
- 재구성오차, Event 보존과 조회 목적을 함께 평가한다.

### Deadband 저장조건의 단순 예

\[
|x_k-x_{\mathrm{last}}| \ge \Delta x
\]

- 실제 Historian은 시간·편차·Swinging-door 등 다양한 알고리즘을 사용할 수 있다.
- Quality 변경과 Event 경계는 값 Deadband와 별도 처리해야 한다.

### Store-and-forward Backlog

\[
B(t)=\max\{0,\;B_0+A(t)-S(t)\}
\]

- \(A(t)\)는 누적 유입량, \(S(t)\)는 누적 재전송량이다.
- 복구 후 Backlog를 줄이려면 일정 구간에서 전송 처리율이 유입률보다 커야 한다.

### Traceability Coverage

\[
C_{\mathrm{trace}}=
\frac{N_{\mathrm{linked}}}{N_{\mathrm{applicable}}}
\]

- 원천, 변환, Lot, Recipe Version, 품질결과 등 적용 대상 관계의 연결비율이다.
- 비율만으로 정확성은 보장되지 않으므로 표본 Audit과 재현시험이 필요하다.


## Fatal 오류

1. **Historian은 장기 백업용 Database이므로 Timestamp, Quality, Event와 Context를 별도로 관리할 필요가 없다.** → Historian은 시계열 운용 데이터의 시간·품질·Event·압축·Context와 조회 요구를 함께 관리한다.
2. **MES와 ERP는 같은 시스템이므로 생산실행과 기업자원관리 기능을 구분할 필요가 없다.** → MES는 제조운영 실행을, ERP는 기업자원·계획·원가를 중심으로 하며 책임과 인터페이스를 구분한다.
3. **ISA-95는 PLC와 ERP 사이에 사용하는 단일 통신 Protocol이다.** → ISA-95는 기능·계층·정보객체와 인터페이스 경계를 정리하는 참조모델이며 특정 전송 Protocol과 동일하지 않다.
4. **MES를 도입하면 PLC·DCS의 실시간 제어 Loop와 Interlock을 MES가 직접 대체한다.** → MES는 제조운영 실행계층이며 시간결정적 제어와 보호논리는 적합한 OT 제어계층에 유지한다.
5. **IT/OT 통합은 PLC를 ERP에 직접 연결할수록 지연이 작고 가장 바람직하다.** → 직접 연결이 아니라 계층적 책임, Gateway·Historian·MES, 보안경계와 데이터 계약을 설계한다.
6. **중앙 Server의 도착시간을 기록하면 모든 데이터의 실제 발생시간을 정확히 알 수 있다.** → Event Time과 수집·도착·처리시간을 구분하고 가능한 한 원천 Timestamp와 Clock 품질을 보존한다.
7. **Tag 값만 비교하면 되므로 여러 설비의 Clock 동기화와 Time alignment는 필요 없다.** → 인과관계·순서·Batch 분석을 위해 동기화, Drift, Offset과 시간대 관리를 수행한다.
8. **Bad 또는 Uncertain 데이터는 계산 편의를 위해 0이나 최근값으로 바꾸면 정상 데이터와 동일하게 사용할 수 있다.** → 대체값은 원 품질, 대체·추정 표시, 규칙과 사용 제한을 함께 전파해야 한다.
9. **상위 시스템에는 값만 전송하면 되므로 Quality Code는 저장하거나 전달하지 않아도 된다.** → Quality 의미를 값과 함께 보존하고 시스템 간 상태 Mapping과 소비정책을 정의한다.
10. **Historian Compression과 Deadband를 적용해도 모든 짧은 Event와 원시 변화가 완전히 보존된다.** → 압축·Deadband는 정보손실 가능성이 있으므로 목적별 한계, Event·Quality 예외와 원시데이터 정책을 정한다.
11. **Store-and-forward를 사용하면 Buffer 용량과 재전송 순서에 관계없이 데이터 유실·중복이 절대 발생하지 않는다.** → Buffer 용량, 단절시간, 순서, 중복제거, 만료와 Recovery 처리율을 설계하고 검증한다.
12. **Tag 이름을 표준화하면 단위, 설비관계, Batch와 품질을 포함한 모든 Context가 자동 완성된다.** → Tag Naming은 식별체계의 일부이며 Metadata, Master Data와 Information Model에 연결해야 한다.
13. **실시간 처리는 Network와 연산 지연이 항상 0인 처리다.** → 실시간성은 목적에 맞는 Deadline, 지연예산과 결정성 요구를 만족하는 것으로 정의한다.
14. **Edge에서 데이터를 처리하면 중앙 Historian, Metadata, Retention과 Data Governance가 필요 없다.** → Edge 처리와 중앙 Context·보존·Governance는 상호보완 관계이며 책임과 동기화 정책이 필요하다.
15. **OPC UA나 MQTT로 연결되면 단위, Timestamp, Quality와 설비 의미도 자동으로 일치한다.** → 전송 연결과 Semantic Interoperability를 구분하고 공통 Information Model과 Mapping을 검증한다.
16. **현재 Historian 값만 조회하면 원자재 Lot부터 완제품까지 Batch Genealogy가 자동 재구성된다.** → Genealogy에는 Lot·작업·Recipe Version·설비·공정조건·품질결과의 식별자와 Event 관계를 보존해야 한다.

## Warn 기준

1. Historian, MES와 ERP를 나열하지만 각 계층의 책임과 데이터 흐름을 구분하지 않음 → Historian의 시계열 보존, MES의 제조실행, ERP의 기업자원 역할과 인터페이스를 연결한다.
2. Timestamp를 언급하지만 Event Time, 도착시간과 원천 위치를 구분하지 않음 → 원천 Timestamp와 수집·처리시간을 구분하고 Clock 품질을 설명한다.
3. 다설비 분석에서 동기화, Offset, Drift 또는 Time alignment가 없음 → Clock 동기화와 정렬오차 관리방안을 제시한다.
4. Quality Code를 언급하지만 Bad·Uncertain의 전파·대체 규칙이 없음 → 원 품질 보존, 대체 표시와 소비 제한을 설명한다.
5. 데이터 품질을 정확도만으로 설명하고 완전성·적시성·일관성 중 핵심이 없음 → Completeness, Timeliness, Consistency와 Context 적합성을 함께 평가한다.
6. Compression·Deadband의 절감효과만 설명하고 짧은 Event·Quality 손실 위험을 누락함 → 목적별 Threshold와 Event·Quality 예외를 제시한다.
7. Store-and-forward를 언급하지만 Buffer 용량, 순서, 중복 또는 Recovery 처리율이 없음 → 단절·복구 시나리오와 Backlog 해소조건을 설명한다.
8. Metadata를 Tag 설명 정도로만 보고 Asset·공정·제품·Batch 관계를 누락함 → Information Model과 Context 관계를 설명한다.
9. Tag Naming은 제시하지만 Master Data Version, Owner와 변경통제가 없음 → Identifier, Version, Owner·Steward와 변경승인을 연결한다.
10. 저장기간만 언급하고 Archive·삭제·Lineage·Audit 요구가 없음 → 데이터 종류별 Retention과 Traceability를 함께 설계한다.
11. Batch Genealogy에서 Lot·Recipe Version·설비·품질결과 중 핵심 연결이 누락됨 → 시간과 식별자를 사용해 투입부터 산출까지 관계를 보존한다.
12. Protocol 전달, 데이터 관리와 AI 분석의 Topic Ownership을 혼용함 → SW-07은 전달, SW-11은 의미·품질·저장·통합, SW-12는 학습·추론으로 경계를 구분한다.

## False Positive 기준

1. Historian이 관계형 Database를 내부적으로 사용한다는 설명은 틀리지 않지만 시계열·품질·시간 기능을 함께 평가한다.
2. MES가 설비와 직접 Interface할 수 있으나 PLC·DCS의 시간결정적 제어와 보호논리를 자동 대체한다는 뜻은 아니다.
3. ISA-95 기반 Interface라는 표현은 허용하되 ISA-95 자체를 Wire Protocol로 단정하면 오류다.
4. 실시간은 0 ms가 아니라 업무 목적에 맞는 Deadline과 지연예산으로 정의할 수 있다.
5. Deadband와 Compression은 허용되는 Engineering 수단이며 적용 자체를 오류로 보지 않는다.
6. Bad 데이터의 대체는 명시된 규칙, Flag와 원 품질 보존이 있으면 허용할 수 있다.
7. Source Timestamp를 얻을 수 없는 경우 Server Timestamp를 사용할 수 있으나 한계와 불확실성을 표시해야 한다.
8. Edge Historian 또는 Local Store는 중앙 Historian과 병행할 수 있다.
9. Tag Naming Convention은 Context 구성요소이며 Metadata·Information Model을 모두 대체한다고 하지 않으면 허용한다.
10. Compression은 구현에 따라 Lossless 또는 Lossy일 수 있으므로 방식과 목적을 확인한다.
11. ERP가 Near-real-time 생산정보를 받을 수 있으나 제어 Loop를 소유한다는 뜻은 아니다.
12. Quality Code 명칭과 Bit 구조는 Vendor별로 다를 수 있으나 Good·Bad·Uncertain 의미 Mapping은 필요하다.
13. Store-and-forward는 유실 저감수단이며 충분한 Buffer와 전달보장이 입증된 범위에서 높은 신뢰성을 가질 수 있다.
14. Streaming Window는 Processing Time 또는 Event Time 기준으로 설계할 수 있으나 선택과 Late Data 정책을 명시한다.
15. Batch Genealogy는 Historian, MES, LIMS 등 여러 시스템의 Event를 결합해 구성할 수 있다.
16. 표준 계층 번호나 세부 기능 배치는 적용 Edition과 조직 Architecture로 verify-first 한다.

## Model Answer

Historian은 공정과 설비의 시계열 데이터를 Timestamp와 Quality Code와 함께 수집하고, 압축·보존·추세·Event 조회를 제공하는 운영 데이터 기반이다. MES는 생산지시를 현장 실행으로 전개하여 작업실적, 자원, 품질과 Batch Genealogy를 관리한다. ERP는 주문, 계획, 자재, 원가와 기업자원을 관리한다. ISA-95는 이 계층의 기능과 정보 인터페이스를 정리하는 참조모델이며 단일 통신 Protocol이 아니다.

IT/OT 통합은 PLC를 ERP에 직접 연결하는 작업이 아니다. 제어 안정성을 보존하면서 Edge·Gateway, Historian, MES와 ERP의 책임을 계층적으로 배치한다. Edge와 Gateway는 Protocol 수용, Buffering, 전처리, 품질 Mapping과 Store-and-forward를 수행할 수 있다. 통신 단절 후에는 Buffer 용량, 순서, 중복, 만료와 Backlog 해소속도를 검증해야 한다.

산업데이터의 핵심은 값뿐 아니라 시간과 품질이다. Timestamp는 가능한 한 발생원에서 생성한 Event Time을 보존하고 도착시간·처리시간과 구분한다. 여러 설비의 인과관계를 분석하려면 Clock 동기화, Offset, Drift와 Time alignment가 필요하다. Quality Code의 Good·Bad·Uncertain 상태는 값과 함께 전파한다. Bad 값을 0이나 최근값으로 대체할 때는 원 품질, 대체 Flag와 사용 제한을 남긴다.

데이터 품질은 정확도만이 아니다. 완전성은 기대 Record 대비 유효 수집비율과 Gap으로, 적시성은 Event 발생부터 사용 가능 시점까지의 Latency로 평가한다. Compression과 Deadband는 저장량을 줄이지만 작은 변화와 짧은 Event를 잃을 수 있다. 따라서 Quality 변경, 상태 전이, Alarm·Event와 Batch 경계는 별도 보존한다.

Tag Naming과 Namespace는 식별체계다. 단위, 설비, 위치, 공정단계, 제품과 Batch 의미는 Metadata, Master Data와 Information Model로 연결한다. Protocol 연결이 성공해도 Timestamp, Quality, 단위와 Context가 다르면 Semantic Interoperability는 달성되지 않는다.

Data Governance는 Owner·Steward, 정의, 품질규칙, 접근, 변경승인과 조치책임을 정한다. Retention은 원시값, 압축값, Event와 Audit 데이터별 보존·Archive·삭제 정책을 구분한다. Traceability와 Batch Genealogy는 원천, 변환, Lot, Recipe Version, 설비, 공정조건, 품질결과와 완제품 관계를 시간과 식별자로 연결한다.

실시간 처리는 지연이 0인 상태가 아니라 업무 목적에 맞는 Deadline과 지연예산을 만족하는 것이다. 결론적으로 SW-07은 데이터를 전달하는 Protocol을, SW-11은 전달된 데이터의 시간·품질·의미·저장·Context와 상위 시스템 통합을, SW-12는 해당 데이터를 이용한 학습과 추론을 담당한다.

## Topic Importance

- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- 고득점 조건:
  1. Historian–MES–ERP와 ISA-95 계층 관계를 정확히 설명한다.
  2. Event Time, Clock 동기화, Time alignment와 Latency를 연결한다.
  3. Quality Code와 Bad·Uncertain 데이터 처리정책을 제시한다.
  4. Completeness·Timeliness·Compression Ratio 등 품질지표를 적용한다.
  5. Compression·Deadband와 Event 보존의 Trade-off를 설명한다.
  6. Store-and-forward의 Buffer와 Recovery 설계를 설명한다.
  7. Metadata·Tag Naming·Master Data·Information Model의 관계를 설명한다.
  8. Governance·Retention·Traceability·Batch Genealogy를 연결한다.
  9. Protocol 연결과 Semantic Interoperability를 구분한다.
  10. SW-07·SW-11·SW-12의 Topic Ownership을 구분한다.

## Routing Alias

1. `historian MES ISA-95 integration`
2. `industrial historian timestamp quality code`
3. `IT OT data contextualization`
4. `edge gateway store and forward`
5. `event time processing time alignment`
6. `bad uncertain industrial data quality`
7. `historian compression deadband retention`
8. `tag naming namespace information model`
9. `master data metadata data governance`
10. `MES ERP production integration`
11. `batch genealogy traceability`
12. `industrial streaming real-time processing`
13. `semantic interoperability industrial data`
14. `historian MES edge architecture`

Broad Alias로 단독 사용하지 않는 표현:

```text
Historian
MES
ERP
ISA-95
Edge
Gateway
Timestamp
Metadata
Streaming
Data quality
```

## Question Examples

### Positive

1. Historian·MES·ERP의 역할과 ISA-95 기반 IT/OT 통합 구조를 설명하시오.
2. 산업 Historian의 Timestamp, Quality Code와 Time alignment 관리방안을 설명하시오.
3. 산업데이터 품질의 완전성·적시성·일관성 관리방안을 설명하시오.
4. Edge·Gateway와 Store-and-forward를 이용한 산업데이터 수집 구조를 설명하시오.
5. Historian의 Compression·Deadband 적용 시 고려사항을 설명하시오.
6. Tag Naming, Namespace, Metadata와 Information Model의 관계를 설명하시오.
7. 산업데이터 Governance, Retention과 Traceability를 설명하시오.
8. MES의 Batch Genealogy와 생산 추적성 구현방안을 설명하시오.
9. 산업 Streaming과 실시간 처리에서 Event Time, Window와 Late Data를 설명하시오.
10. Protocol 상호운용성과 Semantic Interoperability의 차이를 설명하시오.

### Negative Boundary

1. OPC UA, Modbus TCP와 MQTT Protocol의 Frame 및 QoS를 비교하시오. → SW-07
2. 산업 Ethernet의 실시간 통신과 TSN을 설명하시오. → SW-07
3. AI 이상탐지 모델의 Precision, Recall과 F1을 설명하시오. → SW-12
4. 예지보전 Model의 Drift와 Retraining 절차를 설명하시오. → SW-12
5. PLC Sequence, Interlock과 Trip Logic을 설명하시오. → SW-02
6. 산업제어시스템 Network Segmentation과 Zero Trust를 설명하시오. → SW-08
7. Digital Twin 기반 Robot 자율제어를 설명하시오. → SW-13
8. 일반 Software 요구분석과 Unit Test 절차를 설명하시오. → SW-04

## Focused Regression

1. Source 6개와 Focused Test 1개 존재
2. JSON 4개 Parsing
3. Topic ID 일치
4. Anchor 30개
5. Fatal 16개
6. Major 12개
7. Modern Root Schema
8. Historian–MES–ERP–ISA-95 경계
9. Event Time·Clock·Quality Code
10. Compression·Deadband·Store-and-forward
11. Metadata·Master Data·Information Model
12. Governance·Retention·Traceability·Genealogy
13. SW-07·SW-11·SW-12 경계
14. Routing Alias 구체성
15. Generated/Production 수정 금지
16. Topic Importance와 Model Answer 깊이

## 생성 파일

```text
docs/topic_sheets/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing.md
rubrics/topic_packs/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing/README.md
rubrics/topic_packs/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing/fact_anchor.json
rubrics/topic_packs/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing/logic_check.json
rubrics/topic_packs/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing/model_answer.json
rubrics/topic_packs/historian_mes_it_ot_integration_industrial_data_quality_realtime_processing/topic_importance.json
scripts/test_historian_mes_it_ot_data_integration_topic.py
```

## Verify-first

- 적용 ISA-95 Edition과 세부 Level Mapping
- Vendor별 Quality Code Bit와 Mapping
- Historian Compression Algorithm과 재구성 보장
- 업무별 Real-time Deadline과 Latency Budget
- Clock 동기화 정확도와 Source Timestamp 지원
- Store-and-forward의 순서·중복·전달 보장
- Retention 기간, 법규와 Legal Hold
