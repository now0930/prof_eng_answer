# Float 액면계의 부력·위치 전달과 기계적 오차

## Topic metadata

- topic_id: `float_level_measurement_buoyancy_guidance_tape_errors`
- question_type: PRINCIPLE_INTERPRETATION
- difficulty: FIELD_APPLICATION
- 상태: draft / human_review_required

## Scope and ownership

Sight Glass 연결은 sight_glass_level_gauge_communicating_vessels_interface에 위임한다. 초음파 TOF 상세식은 기존 초음파 토픽, DP 식과 계면 밀도차 계산은 기존 차압식 레벨 토픽이 소유한다.

## Core correct facts

- Float 액면계는 부력과 유효 하중이 평형을 이루는 부자가 액면을 따라 움직이는 위치를 검출한다. 뜰 수 있는 밀도·부피·하중 조건과 자유로운 이동이 필요하다.
- 공정 밀도가 달라지면 같은 하중을 지탱하는 부자의 침수체적이 바뀌므로 액면과 부자 기준점 사이 위치 오차가 생길 수 있다.
- Guide wire 또는 가이드는 난류로 인한 부자의 횡방향 흔들림을 제한한다. 수직 이동을 방해하는 마찰·걸림·침적을 함께 확인해야 한다.
- Tape 또는 기계적 linkage는 부자 위치를 외부 지시부로 전달한다. 마찰·테이프 늘어남·기계적 마모·sticking은 지연과 지시 편차를 만든다.
- Float는 움직이는 부자의 위치를 측정하며 초음파 TOF 거리 측정 및 고정된 displacer의 부력 변화 검출과 구분한다. 적용 시 유체 적합성, 난류, 가이드와 전달부 점검 가능성을 평가한다.

## Acceptable answer expressions

- 부자의 위치가 액면 높이 변화를 따른다.
- 자유 부자도 밀도 변화에 따른 잠김 깊이를 확인한다.
- 가이드는 좌우 흔들림을 줄이되 상하 이동을 허용한다.
- 부자는 따라 움직여도 테이프 전달부가 걸리면 지시가 달라질 수 있다.
- 자유 부자의 액면 추종과 고정 displacer의 힘 변화를 구분한다.

## Fatal wrong claims / warn-level weak claims

명시적인 측정원리 반전만 핵심 오류 후보이다. 단순 누락은 fatal이 아니다.
- 오답 예: 부자는 초음파 왕복시간으로 액면 위치를 검출한다.
- 오답 예: 부자 침수깊이는 어떤 유체 밀도에서도 일정하다.
- 오답 예: 가이드는 액면 변화에 따른 상하 이동까지 고정한다.
- 오답 예: 테이프 늘어남과 마찰은 지시에 영향을 주지 않는다.
- 오답 예: 부자식과 초음파식은 동일한 시간 측정 원리이다.

## False positive cautions / Regex candidate patterns

오답 인용·부정·정정은 오답 주장으로 취급하지 않는다. 조건과 기호가 일관된 동등식은 인정한다. 신규 regex 및 결정론적 fatal rule은 이번 초안에 추가하지 않는다.

## Expected question patterns

- 부자식 액면계의 측정원리와 밀도 변화의 영향을 설명하시오. — float_buoyancy_position, float_density_immersion
- Float tape 액면계에서 guide wire의 역할과 마찰·걸림에 의한 오차를 설명하시오. — float_buoyancy_position, float_guidance_turbulence, float_tape_motion_transfer
- Float 액면계와 초음파 액면계의 측정원리를 구분하시오. — float_buoyancy_position, float_method_boundary

## Source JSON guidance

fact_anchor.json은 원자 Fact와 허용·거부 표현을 사용한다. model_answer.json의 required_anchor_ids는 질문별 범위만 포함한다. logic_check.json은 명시적 모순과 정상 문맥을 구분하며 runtime 결정론적 검출을 검증했다고 주장하지 않는다. topic_importance.json은 FIELD_APPLICATION / NORMAL이다.

## Human review checklist

- [ ] README와 source JSON의 물리적 조건·단위·오류 경계 검토
- [ ] 인접 토픽 ownership 및 질문별 anchor 검토
- [ ] 검토자가 approve-topic 수행

## Reference

[Lessons In Industrial Instrumentation, Chapter 20](https://now0930.pe.kr/wordpress/chapter-20/) — 2026-09-30 열람. 조건과 경계 설명은 정수압·부력 관계로 보완했다.
