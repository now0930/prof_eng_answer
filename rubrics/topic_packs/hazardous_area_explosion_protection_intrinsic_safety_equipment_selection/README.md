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

## Chapter 32.1 출처와 적용 경계

[공정안전·방폭 글](https://now0930.pe.kr/wordpress/chapter32-1-process-safety-20261031/)
(`post_id=9814`, §32.1.1~32.1.3)은 LEL/UEL·MIE와 MESG/MICR, 방폭
보호방식의 물리적 차이를 학습 출처로 연결한다. 위험장소 Zone/Division은
폭발성 분위기의 존재 가능성·지속시간을 다루고, Group은 물질의 점화·
화염전파 특성을 다룬다. MIE 하나로 Group이나 기기 적합성을 판정하지
않는다. 내압방폭은 내부 점화 가능성을 없애는 방식이 아니라 화염의
외부 전파를 방지하며, 본질안전은 인증된 전체 회로의 에너지를 제한한다.
블로그의 특정 물질 수치·NEC 조항·단순기기 한계는 시험조건·판본·관할에
묶여 있으므로 일반 채점의 보편 필수값으로 승격하지 않는다.
