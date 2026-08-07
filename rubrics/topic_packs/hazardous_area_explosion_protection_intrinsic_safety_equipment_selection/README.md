# 위험장소 방폭 방식, 본질안전 회로 및 계측기기 선정

## Topic ID

`hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

## Official criterion

`IC-2027-W-4-2` — 위험 환경 제어요소/대책

## Classification

- Question Type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 사용하지 않음
- Logic mode: LLM semantic review
- Deterministic fatal rules: disabled

## Core answer flow

`Hazardous-area classification → EPL → protection method → Ex marking/certificate → intrinsic-safety loop compatibility → installation/inspection`

## Core facts

- Gas Zone 0/1/2와 Dust Zone 20/21/22를 구분한다.
- Zone에 필요한 EPL을 먼저 정하고 전체 Ex marking을 확인한다.
- Ex d/e/i/p는 서로 다른 점화방지 원리를 사용한다.
- Intrinsic safety는 field apparatus, associated apparatus 및 cable을 하나의 system으로 검토한다.
- Entity parameter 방향은 `Uo≤Ui`, `Io≤Ii`, `Po≤Pi`이다.
- Cable capacitance/inductance를 포함하여 `Co`, `Lo` 또는 certificate system limit을 확인한다.
- Zener barrier와 galvanic isolator의 접지·절연 조건을 구분한다.
- Certificate special condition과 control drawing은 실제 설치조건이다.
- IP·부식·진동 등 환경 적합성은 Ex certification과 별도로 확인한다.

## Ownership boundary

본 Topic은 Explosion protection과 intrinsic-safety equipment/loop selection을 소유한다.
SIS/SIL software lifecycle, final-element SIL/PST, OT cybersecurity는 다른 Topic 소유다.

## Source files

- `fact_anchor.json`: 22 Anchors / 13 Fatal misconceptions
- `model_answer.json`: 10 question patterns / 8 outline sections
- `logic_check.json`: deterministic keyword fatal disabled, LLM semantic review
- `topic_importance.json`: `FIELD_APPLICATION / NORMAL / COMPARE_SELECTION`

## Standards orientation

IEC 60079 series를 기술적 기준축으로 사용하되 특정 판년을 암기 점수요소로 고정하지 않는다.
적용 관할의 현행 채택표준, certification marking 및 certificate conditions를 우선 확인한다.
