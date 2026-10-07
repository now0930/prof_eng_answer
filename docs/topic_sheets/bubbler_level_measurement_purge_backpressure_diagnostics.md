# Bubbler 액면계의 퍼지 배압 원리와 유량·고장 진단

## Topic metadata

- topic_id: `bubbler_level_measurement_purge_backpressure_diagnostics`
- question_type: PRINCIPLE_INTERPRETATION
- difficulty: FIELD_APPLICATION
- 상태: draft / human_review_required

## Scope and ownership

정수압은 배압식 설명에 필요한 조건만 사용한다. Wet/Dry Leg·Remote Seal·계면·Tank Expert 밀도 계산은 기존 차압식 레벨 토픽이 소유한다. Sight feed는 액면 관찰용 Sight Glass와 구분한다.

## Core correct facts

- Bubbler는 잠긴 dip tube에 작은 가스 유량을 공급하고 기포가 배출될 때 형성되는 배압을 측정한다. 기포의 개수 자체가 액위 측정량은 아니다.
- 관 마찰·출구 기포 생성 압력 등을 무시할 수 있는 낮은 안정 유량에서는 P_tube-P_surface≈ρgh이다. h는 관 끝의 침수깊이이며 개방탱크는 대기 기준, 밀폐탱크는 기상부 압력 보상이 필요하다.
- 퍼지 유량이 너무 크면 관내 마찰손실이 배압에 더해져 높게 지시할 수 있다. 측정은 공급 조정기 압력 자체가 아니라 유량 제한부 하류의 dip tube 배압을 기준으로 한다.
- Sight feed bubbler는 퍼지 흐름 유무를 시각적으로 확인하고 rotameter는 유량을 확인한다. 압력전송기는 배압을 측정하며 세 장치의 역할을 구분한다.
- 퍼지 공급 부족·중단, 튜브 누설 및 막힘을 확인한다. 누설은 낮은 배압, 막힘은 공급 조건에 따른 높은 압력이나 응답 정지를 유발할 수 있으며 단일 압력 지시만으로 원인을 단정하지 않는다.
- 배압 센서를 공정 액체와 직접 접촉시키지 않아도 되지만 dip tube는 접액된다. 튜브 재질, 퍼지 가스의 공정 적합성·소비량과 안정 공급을 검토한다.

## Acceptable answer expressions

- 기포를 유지하는 압력으로 침수 깊이를 구한다.
- 개방탱크의 게이지 배압은 근사적으로 액주 수두에 해당한다.
- 과다 퍼지는 양의 압력 편차를 만들 수 있다.
- 유량 확인과 배압 측정은 다른 기능이다.
- 배압과 유량 및 공급상태를 함께 확인해 고장을 구분한다.
- 센서 격리는 dip tube까지 비접촉이라는 뜻이 아니다.

## Fatal wrong claims / warn-level weak claims

명시적인 측정원리 반전만 핵심 오류 후보이다. 단순 누락은 fatal이 아니다.
- 오답 예: 기포 개수만 세어 액위를 직접 결정한다.
- 오답 예: 밀폐탱크 기상부 압력은 배압에 영향을 주지 않는다.
- 오답 예: 퍼지 유량은 클수록 무조건 정확하다.
- 오답 예: Rotameter가 배압 측정을 대체한다.
- 오답 예: 어떤 막힘도 항상 실제 액위 저하를 뜻한다.
- 오답 예: Bubbler의 모든 부품은 공정 액체와 비접촉이다.

## False positive cautions / Regex candidate patterns

오답 인용·부정·정정은 오답 주장으로 취급하지 않는다. 조건과 기호가 일관된 동등식은 인정한다. 신규 regex 및 결정론적 fatal rule은 이번 초안에 추가하지 않는다.

## Expected question patterns

- Bubbler 액면계의 배압 측정원리와 개방·밀폐탱크 적용조건을 설명하시오. — bubbler_backpressure_principle, bubbler_pressure_reference
- 기포식 액면계의 퍼지 유량 선정과 과다 유량·누설·막힘의 진단방법을 설명하시오. — bubbler_pressure_reference, bubbler_flow_friction_bias, bubbler_flow_monitoring, bubbler_failure_diagnosis
- Bubbler를 부식성 액체에 적용할 때 구성과 재질·가스 선정조건을 설명하시오. — bubbler_backpressure_principle, bubbler_flow_monitoring, bubbler_material_process_compatibility

## Source JSON guidance

fact_anchor.json은 원자 Fact와 허용·거부 표현을 사용한다. model_answer.json의 required_anchor_ids는 질문별 범위만 포함한다. logic_check.json은 명시적 모순과 정상 문맥을 구분하며 runtime 결정론적 검출을 검증했다고 주장하지 않는다. topic_importance.json은 FIELD_APPLICATION / NORMAL이다.

## Human review checklist

- [ ] README와 source JSON의 물리적 조건·단위·오류 경계 검토
- [ ] 인접 토픽 ownership 및 질문별 anchor 검토
- [ ] 검토자가 approve-topic 수행

## Reference

[Lessons In Industrial Instrumentation, Chapter 20](https://now0930.pe.kr/wordpress/chapter-20/) — 2026-09-30 열람. 조건과 경계 설명은 정수압·부력 관계로 보완했다.
