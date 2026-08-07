# 계측제어 시스템 설계기준, Code·Standard·Specification 및 Deviation 관리

## 0. Topic identity

- Topic ID: `instrumentation_system_design_basis_codes_standards_specification_deviation_management`
- Official criterion: `IC-2027-W-2-8`
- Official scope label: 설계규정
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음
- Grading mode: LLM semantic review 중심
- Deterministic fatal keyword rule: 사용하지 않음

## 1. 출제 의도

이 Topic은 표준 번호 암기보다 계측제어 설계의 **governing basis를 실제 설계·구매·검증·인수 기준선으로 전개하는 능력**을 평가한다.

핵심 흐름은 다음과 같다.

`법규·계약·표준 식별 → Design Basis → Specification/Data Sheet → Vendor compliance/deviation → impact/approval → disposition/document update → FAT/SAT/commissioning → as-built baseline`

## 2. 문서 역할

### 2.1 Design Basis

Design Basis는 공정조건, 설비 운영철학, 성능목표, 환경·안전 제약, architecture, interface와 주요 가정을 설계 입력으로 정리한다.

회사에 따라 Design Criteria, Engineering Design Basis, Instrumentation Design Criteria 등 문서명이 다를 수 있다. 시험에서는 문서명보다 **설계 입력의 기준선과 downstream requirement의 근거**라는 기능이 중요하다.

### 2.2 Code, Standard, Specification

- Code: 채택 주체와 관할에 따라 법적 또는 계약상 강제성이 생길 수 있는 기술규정 체계
- Standard: 공통 기술 요구·방법·표현을 제공하는 합의 기준
- Specification: 특정 프로젝트·기기·서비스에 필요한 검증 가능한 요구사항을 구체화한 문서

세 용어를 동의어로 취급하지 않는다.

표준도 법규나 계약에 편입되면 의무가 될 수 있다. 반대로 국제표준이라는 이유만으로 모든 국가·모든 프로젝트에 자동 법적 강제가 생기는 것은 아니다.

## 3. Governing requirements와 판본관리

프로젝트는 적용할 법규, 계약조건, Owner/EPC 기준, 국제·산업표준, project specification을 식별해야 한다.

적용표준 register 또는 동등한 목록에는 최소한 다음을 명확히 하는 것이 좋다.

1. 문서번호와 명칭
2. 적용범위
3. 적용 edition/revision 또는 project cut-off
4. 적용근거
5. 관련 specification/document
6. conflict 발생 시 precedence 또는 해결절차

'모든 관련 표준 준수'라는 한 문장만으로는 설계·구매·검증 기준을 충분히 고정하기 어렵다.

항상 최신판을 기존설비까지 자동 소급 적용한다고 단정하지 않는다. 실제 적용판본은 법규, 계약, 변경범위와 승인절차를 확인한다.

## 4. Design Basis의 주요 입력

### 4.1 Process condition

정상·최소·최대·시동·정지·비정상 조건을 검토한다.

압력, 온도, 유량, 조성 등은 계기 range, 재질, process connection, impulse line, protection 요구의 입력이 된다.

### 4.2 Measurement performance

정확도만 보지 않는다.

- Range와 turndown
- 응답시간
- 반복성·안정성
- 전체 loop 성능
- 진단성
- 교정·시험 가능성

을 서비스 목적에 맞게 정의한다.

### 4.3 Environment and safety

주위온도, 습도, 진동, 부식, 침수·분진, EMC, 위험장소, 기능안전 등 적용 가능한 제약을 별도 검토한다.

위험장소와 SIS/SIL의 세부 기술요건은 각각의 기존 Topic이 소유한다.

### 4.4 Architecture and maintainability

가용성, 신뢰성, 유지보수성, redundancy, fail-safe/degraded operation, spare와 교체성을 서비스 중요도와 lifecycle cost에 맞춰 결정한다.

### 4.5 Interface

전원, 접지, instrument air, I/O, signal type, communication protocol, time synchronization, package interface와 data ownership을 명확히 한다.

## 5. Engineering document 전개

Design Basis는 다음 문서와 일관되게 전개되어야 한다.

- P&ID
- Instrument Index
- Instrument Datasheet
- I/O List
- Control Narrative
- Cause & Effect
- Loop Diagram
- Wiring/Termination document
- Package interface document

ISA-5.1과 같은 표준은 symbol과 tag의 공통 해석에 활용할 수 있다.

Specification과 Datasheet는 설계기준을 **검증 가능한 requirement**로 변환해야 한다. 재질, range, accuracy, enclosure, certification, inspection/test와 acceptance criterion을 확인 가능한 값 또는 조건으로 명시한다.

## 6. Vendor compliance와 Deviation

Vendor가 사양과 다른 제안을 할 때 deviation 또는 exception을 숨기지 않고 명시해야 한다.

좋은 deviation list에는 다음이 포함된다.

1. 원 requirement clause
2. 요구내용
3. Vendor 제안
4. deviation 이유
5. 기술·안전·운영 영향
6. 비용·납기 영향
7. Vendor가 제시한 대안
8. 발주자 disposition

Technical Bid Evaluation은 compliance, deviation과 clarification을 requirement 단위로 검토하여 최종 구매조건과 vendor document에 반영한다.

## 7. Deviation 관리 절차

Deviation은 승인된 baseline에서 벗어나는 사항을 통제하는 기록이다.

### 7.1 등록

원 requirement와 proposed departure를 식별한다.

### 7.2 Impact/Risk assessment

영향범위에 따라 다음을 평가한다.

- 안전과 규제·인증
- 측정·제어 성능
- reliability/availability
- maintainability와 spare
- package·전기·배관·software interface
- FAT/SAT·시운전
- 일정·비용
- 기존설비와 shutdown 영향

### 7.3 Approval

영향도와 project governance에 맞는 authority가 승인 또는 거절한다.

Vendor와 담당자의 구두합의만으로 baseline을 바꾸지 않는다.

### 7.4 Disposition

Accept, conditional accept, redesign 등의 결과와 후속조건을 기록한다.

### 7.5 Closure

승인번호만 있다고 끝나는 것이 아니다.

관련 specification, datasheet, drawing, calculation, PO, test procedure와 as-built document가 실제 disposition과 일치하는지 확인한다.

## 8. Deviation과 MOC

Deviation control과 Management of Change는 모두 변경을 통제한다.

그러나 적용 시점, 승인권한, risk review, 운영승인 절차는 조직과 산업에 따라 다를 수 있다. 따라서 둘을 항상 같은 절차라고 하거나 deviation만 있으면 MOC가 필요 없다고 단정하지 않는다.

공통적으로 다음이 남아야 한다.

`변경사유 → 영향평가 → 승인 → 구현 → 검증 → 관련문서 갱신 → 운영 baseline 반영`

## 9. Verification, FAT/SAT와 Handover

핵심 requirement는 Design Basis에서 Specification, Datasheet, Drawing, Configuration으로 traceability를 유지한다.

그 요구사항은 design review, vendor document review, FAT, SAT, commissioning 또는 동등한 검증에서 acceptance evidence로 확인한다.

최종 handover에는 승인된 변경과 deviation을 반영한 다음 baseline이 필요하다.

- As-built drawing
- Final datasheet/index
- Configuration/software setting
- Certificate
- FAT/SAT/commissioning record
- Calibration/test record
- Open item 및 residual restriction

운영단계 MOC는 이 handover baseline을 기준으로 시작한다.

## 10. Existing plant 적용 시 실무 고려

기존 설비에 신규 기준을 적용할 때 단순 전면 교체만이 답은 아니다.

다음을 함께 본다.

1. 법적 강제사항과 grandfathering 또는 적용범위
2. 기존설비 위험과 실제 failure history
3. 신규 장비와 기존 DCS/PLC/I/O/통신 interface
4. Shutdown 가능시간과 production loss
5. Spare·교육·정비체계
6. 단계적 retrofit 가능성
7. deviation 또는 MOC 승인 필요성
8. lifecycle cost

법규·안전에 직접 관련된 미충족은 비용만으로 정당화할 수 없다. 반면 강제요건이 아닌 개선항목은 risk, 실현가능성, downtime과 lifecycle benefit을 근거로 단계적 적용할 수 있다.

## 11. 표준 예시와 scope boundary

- ANSI/ISA-5.1-2024: Instrumentation and Control – Symbols and Identification
- ISA-20 계열: Process Measurement and Control Instrument specification form 관련 기준
- IEC 61511-1:2016+A1:2017: Process industry SIS의 specification, design, installation, operation, maintenance lifecycle

이 표준들은 설계규정 관리방법을 설명하기 위한 대표 사례다.

특정 표준의 세부 requirement를 이 Topic이 모두 소유하지 않는다. 표준번호 또는 판년 자체를 암기 점수요소로 사용하지 않는다.

## 12. Grading boundary

이 Topic의 핵심은 다음 다섯 연결이다.

1. Governing requirement를 확정한다.
2. Design Basis를 measurable requirement로 변환한다.
3. Vendor deviation을 숨기지 않고 평가·승인한다.
4. 승인 결과를 downstream document와 시험기준에 반영한다.
5. FAT/SAT·as-built evidence까지 baseline을 닫는다.

다음 기존 Topic과 ownership을 분리한다.

- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
- `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
- `configuration_change_release_backup_rollback_migration_obsolescence_management`
