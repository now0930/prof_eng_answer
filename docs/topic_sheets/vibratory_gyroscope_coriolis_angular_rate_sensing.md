# Topic Sheet: 진동 자이로스코프의 코리올리 각속도 검출

## Topic metadata

- topic_id: `vibratory_gyroscope_coriolis_angular_rate_sensing`
- question_type: `PRINCIPLE_INTERPRETATION`
- difficulty: `FIELD_APPLICATION`
- status: 승인 상태와 source hash는 Pack의 `topic_status.json`을 따른다.

## Scope and ownership

진동 질량을 가진 자이로스코프가 회전 좌표계의 코리올리 응답을 횡방향 변위/진동으로 검출하여 본체의 각속도를 추정하는 원리를 소유한다. 축의 RPM을 encoder·proximity·tachometer로 측정하는 `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`와 다르다. 유체 질량유량을 진동 튜브로 측정하는 `flow_measurement_meter_principles_velocity_selection`의 코리올리스 유량계와도 구별한다.

## Candidate core facts

1. 회전 좌표계에서 상대속도 **v**를 가진 질량의 코리올리 가속도 크기는 `2|Ω||v|sinθ`이다. 회전 좌표계의 가상 가속도는 `-2(Ω×v)`이며, 관성계 가속도 분해의 `+2Ω×v` 항 및 물체가 프레임에 가하는 반력과 구분한다.
2. `Ω ⟂ v(t)`일 때 가속도 순간 크기는 `2|Ω||v(t)|`, 힘 크기는 `2m|Ω||v(t)|`이다. `|Ω|=|F_C(t)|/(2m|v(t)|)`는 직교 조건과 `|v(t)|>0`인 순간의 관계다. 진동속도 자체는 시간에 따라 변하며, 일정한 구동 진폭·주파수에서는 속도 진폭이 정해진다.
3. 진동 질량의 구동축과 직교하는 감지축에 코리올리 응답이 나타난다. 구동 진동 방향이 반전되면 감지 응답의 방향/위상도 반전한다.
4. 실제 계기는 힘을 직접 읽는다고 단정하지 않고 횡방향 변위·진동을 변환기(예: 정전용량 감지)로 읽어 각속도를 추정한다. 회전율과 출력 사이의 비례는 구동 진폭·주파수, 감지부 동특성, 교정 상태가 일정한 범위에서 성립한다.

블로그 HTML은 위 원리의 1차 개인 지식 원천이며, 기술적 사실은 별도로 [Analog Devices 진동 자이로 설명](https://www.analog.com/en/resources/analog-dialogue/articles/imems-angular-rate-sensing-gyroscope.html)과 대조했다. HTML 내 그림의 좌·우 방향은 좌표계 정의 없는 보편 법칙으로 승격하지 않는다. PDF·이미지 OCR은 이번 후보 작성에 사용하지 않았다.

## Representative exam-style questions

1. 진동 자이로스코프에서 코리올리 가속도와 각속도 검출 원리를 설명하시오.
2. 진동 자이로의 구동축·감지축 관계와 진동 방향 반전에 따른 출력 변화를 설명하시오.
3. `|F_C|=2mωv`의 적용조건을 제시하고, 실제 센서가 검출하는 물리량과 각속도 환산 과정을 설명하시오.

## Answer and error boundaries

정답은 좌표계와 크기/방향을 먼저 구별하고, 구동 진동→직교 코리올리 응답→변위/진동 검출→각속도 환산의 흐름을 제시한다. `F_C∝ω`를 무조건적 관계로 일반화하거나, 코리올리스 유량계의 질량유량을 자이로의 출력량이라고 쓰지 않는다. 부호나 좌·우 방향은 좌표계가 명시되지 않으면 기계적으로 fatal 처리하지 않는다. 수식 누락은 질문이 수식을 직접 요구하지 않았다면 단순 부족으로 다룬다.

## Source references and review

- [WordPress: 코리올리 힘, 가속도](https://now0930.pe.kr/wordpress/%ec%bd%94%eb%a6%ac%ec%98%ac%eb%a6%ac-%ed%9e%98-%ea%b0%80%ec%86%8d%eb%8f%84/) — post 8253, HTML modified `2026-10-28T12:38:29Z`, content SHA-256 `854790f1a14378169bafee0c41edff949cf33b4779f3e6cb24bda6f63fcabb96`, section `1. 코리올리 가속도와 진동 자이로`. 원문과 초안의 차이를 검토한다.
- [Analog Devices: angular-rate-sensing gyroscope](https://www.analog.com/en/resources/analog-dialogue/articles/imems-angular-rate-sensing-gyroscope.html) — 구동 질량, 코리올리 응답, 정전용량 변위 검출에 대한 독립 참고.
- 사용자가 Astra에 검토·승인을 위임했다. AI 검토 보고서와 승인 source hash를 기록하며, 사람 검토로 표시하지 않는다.

후속 원문 갱신: 위 12:38:29Z 버전 검토 이후 2절이 추가되었다. 최종 출처는 `2026-10-28T13:00:39Z`, HTML SHA-256 `360461342211e20c6b06083caa5d691c85ca2f19ffe3161cddec2b287574c764`, 1~2절이다. Astra가 +z 회전·+y 속도에서 외적은 -x, 회전계 가상 가속도는 +x라는 계산과 0.004 N 예제를 재검토했다. 구동 진동을 회전이 발생시키는 것으로 해석하지 않는다.
