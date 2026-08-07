# P&ID 배관계장도 기호·태그·제어루프·관련 문서와 설계 검토

## Topic ID

`pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`

## 공식 기준

- `IC-2027-W-3-7`
- P&ID

## 분류

- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`

## 핵심 소유범위

P&ID의 기호·Tag·Loop·signal line 판독, PFD/Loop Diagram/Logic Diagram/Control Narrative와의 관계, cross-document consistency, revision·MOC·as-built를 소유한다.

## 명시적 경계

Bare `PID`를 routing alias로 사용하지 않는다. PID controller의 P/I/D 동작과 tuning은 `pid_controller_tuning_sequence_gain_effects`가 소유한다.

## 검증 원칙

Project-specific symbol과 numbering convention은 project legend를 직접 기준으로 한다. Generated bank와 release registration은 source/focused validation 이후 별도 단계에서 처리한다.
