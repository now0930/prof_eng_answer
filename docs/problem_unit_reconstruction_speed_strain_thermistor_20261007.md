# 회전속도·스트레인게이지·Thermistor Pack 문제 단위 보충 감사

이 문서는 screen inventory의 미완료 3개 Pack을 별도 보충 감사한 결과다. 자동 연결률을 위해 독립 질문에 관계없는 Anchor를 억지로 공유시키지 않았다.

## 회전속도 계측

`speed_rotation_measurement_encoder_proximity_tachometer_selection_error`는 10개 패턴·22개 Anchor다. 패턴 intent 및 question example은 이미 구체적이고 required union은 22/22다. High-score·common-missing·importance 조건에 P1–P10 범위를 명시했다. 엔코더, inductive proximity, variable-reluctance pickup, tachogenerator, 비교선정/retrofit의 서로 다른 네 연결요소는 속도 측정이라는 공통 변수와 비교·선정 질문으로 묶인 것으로 보아 임의 연결 없이 유지했다.

## 스트레인 게이지·로드셀

`strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`는 13개 패턴·14개 Anchor의 required union이 14/14다. High-score·common-missing·importance 기준을 측정원리, bridge 구성, signal conditioning, 보상, 오차 및 설치 문항에 각각 범위화했다. 원리·브리지·온도보상·현장오차로 나뉜 4개 연결요소는 strain-gauge load-cell 측정사슬의 독립 시험문항으로 유지하고 허위 Anchor 연결은 만들지 않았다.

## Thermistor

`thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`은 3개 패턴·14개 Anchor다. 기존 세 intent가 비어 있었고, 적용온도범위·안정성 Anchor가 어떤 질문에도 required 연결되지 않았으며 topic importance 설명에는 RTD 내용과 중복된 잘못된 문장이 있었다. P1 질문에 센서특성·적용조건을 명시하고 해당 Anchor를 연결했으며 세 intent, 문항별 scoring scope와 RTD owner 경계 설명을 보완했다. Required union은 14/14가 됐다.

## 보존한 계약과 검증 상태

- Question Type, aliases/routing authority, fatal 처리, deterministic scoring 및 logic/evaluator 권한은 바꾸지 않았다.
- 개별 schema/quality/atomicity와 focused regressions는 함께 실행했다. 3개 source에 schema 오류는 없었다.
- 세 Pack 모두 scoped release validation PASS; generated bank는 사전 snapshot으로 복원해 promote하지 않았다.
- Atomicity의 disconnected-family warning은 회전속도 1건, 스트레인 게이지 1건, Thermistor 1건 남는다. 문제 패턴이 독립 시험요구를 갖는 신호로 기록했으며, 경고를 숨기거나 패턴을 강제로 결합하지 않았다.
- 기술 내용의 표준 적합성·전문가 승인을 의미하지 않는다.
