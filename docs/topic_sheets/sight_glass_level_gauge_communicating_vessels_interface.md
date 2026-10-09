# Sight Glass 액면계의 연통 원리와 계면 연결

## Topic metadata

- topic_id: `sight_glass_level_gauge_communicating_vessels_interface`
- question_type: PRINCIPLE_INTERPRETATION
- difficulty: FIELD_APPLICATION
- 상태: draft / human_review_required

## Scope and ownership

DP 수두·밀도·LRV 계산은 기존 차압식 레벨 토픽에 위임한다. Float 위치변환의 상세 구조는 float_level_measurement_buoyancy_guidance_tape_errors가 소유한다.

## Core correct facts

- 정상 연결된 Sight Glass는 용기와 게이지 사이 정수압 평형으로 액면을 재현한다. 양측 유체 밀도와 기상부 압력이 같고 연결부가 개방되어 있어야 동일 높이를 지시한다.
- 단일 액체의 외부 액면계는 상부 연결을 기상부에, 하부 연결을 액체에 둔다. 측정범위를 벗어나거나 밸브가 닫히면 용기 액면을 정상적으로 재현하지 못할 수 있다.
- 불혼화 두 액체의 계면을 재현하려면 상부 노즐은 경액, 하부 노즐은 중액에 연결하고 게이지 안에도 대응하는 두 액층이 존재해야 한다.
- 오염은 육안 판독을 방해하고 막힌 연결관이나 닫힌 차단밸브는 압력 평형을 깨뜨린다. 세척과 연결상태 확인을 구분해 지시오차를 진단한다.
- 유리식 게이지는 사용 압력·온도·재질 적합성과 열충격·기계충격에 따른 파손을 검토한다. 자기식 게이지의 챔버·자성 부자·경보 스위치는 비교가 직접 요구될 때만 보조 설명으로 다룬다.

## Acceptable answer expressions

- 용기와 외부 관의 압력 평형으로 액면을 직접 읽는다.
- 상부는 가스 압력을 공유하고 하부는 액주를 연결한다.
- 상부와 하부 연결에서 각 상을 올바르게 재현해야 계면을 읽을 수 있다.
- 게이지가 깨끗해도 연결관이 막히면 지시가 고정될 수 있다.
- 자기식 지시는 유리관 직접 관찰과 구분하고 부자 및 챔버 조건을 확인한다.

## Fatal wrong claims / warn-level weak claims

명시적인 측정원리 반전만 핵심 오류 후보이다. 단순 누락은 fatal이 아니다.
- 오답 예: 기상부 압력이나 유체 밀도가 달라도 항상 같은 높이를 표시한다.
- 오답 예: 상부 기상부 연결을 차단해도 모든 밀폐탱크에서 정확하다.
- 오답 예: 계면 측정에서 노즐 위치와 연결 유체는 무관하다.
- 오답 예: 유리관만 깨끗하면 배관 막힘에 관계없이 정확하다.
- 오답 예: 자기식 게이지에는 부자가 필요 없다.

## False positive cautions / Regex candidate patterns

오답 인용·부정·정정은 오답 주장으로 취급하지 않는다. 조건과 기호가 일관된 동등식은 인정한다. 신규 regex 및 결정론적 fatal rule은 이번 초안에 추가하지 않는다.

## Expected question patterns

- Sight Glass의 연통 원리와 단일 액체 및 계면 측정의 연결조건을 설명하시오. — sight_glass_pressure_equilibrium, sight_glass_upper_lower_connections, sight_glass_interface_connections
- 유리관 액면계의 지시 불량 원인과 고온·고압 적용 시 유의사항을 설명하시오. — sight_glass_pressure_equilibrium, sight_glass_indication_faults, sight_glass_service_limits

각 pattern의 intent와 example을 source Model Answer에 함께 두고, 고득점·누락 조건을 해당 pattern으로 제한한다. 자기식 지시 원리 누락만으로 위 두 문제의 점수를 낮추지 않는다.

## Source JSON guidance

fact_anchor.json은 원자 Fact와 허용·거부 표현을 사용한다. model_answer.json의 required_anchor_ids는 질문별 범위만 포함한다. logic_check.json은 명시적 모순과 정상 문맥을 구분하며 runtime 결정론적 검출을 검증했다고 주장하지 않는다. topic_importance.json은 FIELD_APPLICATION / NORMAL이다.

## Human review checklist

- [ ] README와 source JSON의 물리적 조건·단위·오류 경계 검토
- [ ] 인접 토픽 ownership 및 질문별 anchor 검토
- [ ] 검토자가 approve-topic 수행

## Reference

[Lessons In Industrial Instrumentation, Chapter 20](https://now0930.pe.kr/wordpress/chapter-20/) — 2026-09-30 열람. 조건과 경계 설명은 정수압·부력 관계로 보완했다.
