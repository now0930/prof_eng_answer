# 초음파 센서의 비행시간 원리, 거리·레벨 측정, 온도보상 및 반사·설치 오차

- Topic ID: `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Semantic execution: `LLM_ONLY`
- Deterministic checks: disabled
- Candidate extraction: empty

## Core contract

1. 압전소자가 전기 펄스와 초음파 진동을 상호 변환한다.
2. 반사형 펄스 에코는 왕복 비행시간을 측정한다.
3. 기본 거리식은 `d=ct/2`이다.
4. 공기 중 음속의 온도 및 매질 의존성을 보상한다.
5. 링다운과 수신회복시간에 따른 사각지대를 구분한다.
6. 빔각, 대상물 반사특성, 주파수와 감쇠를 평가한다.
7. 탱크 기준높이와 액면 거리로 레벨을 계산한다.
8. 허위에코, 다중반사, 공정조건과 설치오차를 진단한다.
9. 반복주기와 평균화의 동적 절충관계를 고려한다.
10. 필요하면 레이더식 측정과 적용성을 비교한다.

## Files

- `fact_anchor.json`: 20 Fact Anchors와 10 Fatal Wrong Claims
- `logic_check.json`: LLM_ONLY 의미평가 계약
- `model_answer.json`: 14 Question Patterns, 14 Examples와 Routing 계약
- `topic_importance.json`: 난이도와 문항 선택 중요도
