# TIER1 Topic 2 — P&ID 배관계장도 기호·태그·제어루프·관련 문서와 설계 검토

## 0. Topic identity

- Topic ID: `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
- Primary official criterion: `IC-2027-W-3-7`
- Official scope: `P&ID`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`
- Historical frequency: 사용하지 않음

## 1. 출제 의도

P&ID는 단순한 기호 암기 문제가 아니다. 장비·배관·밸브·계기와 제어루프의 기능 연결을 읽고, PFD·Loop Diagram·Logic Diagram·Control Narrative 등 관련 문서와의 역할을 구분해야 한다. 설계·시공·운전 단계에서는 tag, service, signal, fail action, revision의 정합성을 확인할 수 있어야 한다.

## 2. 직접 포함 범위

1. P&ID 정의와 목적
2. PFD 및 physical layout과의 차이
3. Equipment·piping·valve 표현
4. Instrument symbol과 위치표기
5. Function letters·Tag·Loop number
6. Signal/connection line
7. Measurement 및 feedback control loop
8. Control valve·actuator·positioner·fail action
9. Alarm·Trip·Interlock의 기능적 표시
10. Loop Diagram·Logic Diagram·Control Narrative 관계
11. Instrument Index·I/O List·Line List·datasheet 정합성
12. Revision·MOC·walkdown·redline·as-built

## 3. Ownership 제외 범위

- `pid_controller_tuning_sequence_gain_effects`: P/I/D 동작, gain 영향, tuning sequence
- `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`: cascade·ratio·feedforward·override·split-range 구조선정 상세
- `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`: sequence·permissive·interlock·trip Boolean logic 상세
- `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`: alarm philosophy·SOE·operator information
- `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability`: PLC/DCS/SCADA hardware architecture
- `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`: software project FAT/SAT lifecycle

## 4. P&ID ↔ PID controller routing guard

- Bare `PID`는 P&ID routing alias로 사용하지 않는다.
- P&ID alias에는 `P&ID`, `Piping and Instrumentation Diagram`, `배관계장도`, `instrument loop` 등 도면 문맥을 포함한다.
- PID controller가 P&ID에 표현될 수 있다는 사실과 두 Topic을 동일시하는 것은 구분한다.

## 5. 핵심 Fact 구조

- P&ID는 process equipment, piping, valve, instrument, control relationship의 기능적 문서다.
- PFD는 주요 공정흐름 중심이고 P&ID는 배관·계기·제어 연결을 더 상세히 다룬다.
- P&ID는 일반적으로 physical layout·축척 도면이 아니다.
- Symbol, function letter, signal line은 적용 표준과 project legend를 함께 확인한다.
- Instrument Tag와 loop number는 관련 문서 간 traceability의 기준이 된다.
- P&ID의 feedback loop는 measurement → controller → final element의 기능 연결로 읽는다.
- Loop Diagram은 wiring/termination, Logic Diagram은 상세 logic, Control Narrative는 운전철학을 보완한다.
- P&ID 설계검토는 Instrument Index, I/O List, Line List, datasheet, Cause & Effect 등과 교차 검증한다.
- 변경 시 revision, MOC, walkdown, redline, as-built 추적성을 확보한다.

## 6. 대표 오답

- P&ID와 PFD를 동일 문서로 설명
- P&ID를 actual piping layout로 설명
- 모든 밸브를 control valve로 설명
- dashed line을 project와 무관하게 항상 electrical signal로 단정
- P&ID만으로 wiring·전체 interlock logic·운전 narrative가 모두 완성된다고 설명
- P&ID와 PID controller를 동일 주제로 설명
- redline만으로 as-built가 완료된다고 설명

## 7. 답안 전개 권장

1. 정의 및 PFD/layout과 차이
2. 장비·배관·밸브
3. Instrument symbol·Tag·Loop
4. Signal line과 control loop
5. 관련 문서 ownership
6. Cross-document consistency
7. Revision·MOC·field verification
8. P&ID/PID controller 용어 경계

## 8. Step 1 변경 제한

- Source Topic Pack만 작성한다.
- Classification policy와 focused test는 Step 2에서 처리한다.
- Generated bank와 release registration은 변경하지 않는다.
- Production Python과 Question Type taxonomy는 변경하지 않는다.
