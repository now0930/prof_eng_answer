# 진동 자이로스코프의 코리올리 각속도 검출

## Topic ID

`vibratory_gyroscope_coriolis_angular_rate_sensing`

## Question type

`PRINCIPLE_INTERPRETATION`

## 작성 상태

WordPress HTML의 진동 자이로 원리를 기존 회전수 계측·코리올리스 유량계와 분리한 관리형 Pack이다. 사용자가 위임한 Astra 검토 및 운영 반영 상태는 `topic_status.json`의 승인 해시를 따른다.

## 소유 범위와 핵심 원리

- 회전 좌표계에서 상대속도 `v`인 질량의 코리올리 가속도 크기는 `2|Ω||v|sinθ`; `Ω ⟂ v`이면 `2ωv`이다.
- 진동 질량 `m`의 구동축에 직교하는 감지축 응답은 이상화된 조건에서 `|F_C|=2mωv`로 표현한다. 부호는 좌표계·힘의 정의에 따라 명시한다.
- 구동 진동 방향이 반전되면 원시 코리올리 힘의 방향도 반전된다. 감지축 진동에는 동특성에 따른 위상 지연이 있을 수 있으며, 일정한 본체 각속도의 복조 후 출력까지 반전되는 것은 아니다. 대표적인 변위 검출 방식은 횡방향 진동을 읽고, 힘 재평형 방식은 교정된 피드백량으로 각속도를 환산할 수 있다.
- 순간 힘은 직교 조건에서 `|F_C(t)|=2m|Ω||v(t)|`이다. 진동속도는 시간에 따라 변한다. 일정한 구동 진폭·주파수에서 속도 진폭이 정해지며 감지부 동특성·복조·교정으로 각속도를 환산한다.

## 인접 Topic 경계

- `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`: 회전축의 RPM을 pulse/voltage로 계측한다. 진동 자이로의 본체 각속도 검출과 다르다.
- `flow_measurement_meter_principles_velocity_selection`: 진동 튜브로 유체 질량유량을 계측한다. 코리올리 물리 원리는 관련되지만 출력량과 대상이 다르다.
- RPM과 rad/s는 환산 가능하다. 두 Pack은 출력 단위가 아니라 검출 방식과 출제 범위로 구분한다. 원문 그림의 좌/우 방향과 부호는 좌표계 정의를 확인한다.

## 대표 질문 예시

1. 진동 자이로스코프에서 코리올리 가속도와 각속도 검출 원리를 설명하시오.
2. 진동 자이로의 구동축·감지축 관계와 구동 방향 반전 시 원시 감지 신호 및 복조 후 각속도 출력의 차이를 설명하시오.
3. `|F_C|=2mωv`의 적용조건과 실제 센서의 감지 물리량을 설명하시오.

## 출처와 검토

- [WordPress 원문 HTML](https://now0930.pe.kr/wordpress/%ec%bd%94%eb%a6%ac%ec%98%ac%eb%a6%ac-%ed%9e%98-%ea%b0%80%ec%86%8d%eb%8f%84/), post `8253`, 최신 저장본의 1~2절(SHA-256 `360461342211e20c6b06083caa5d691c85ca2f19ffe3161cddec2b287574c764`). PDF·이미지 OCR은 Fact 근거에 쓰지 않았다.
- [Analog Devices 기술 설명](https://www.analog.com/en/resources/analog-dialogue/articles/imems-angular-rate-sensing-gyroscope.html)과 물리 원리·정전용량식 감지를 대조했다.
- Astra 검토 항목: 원문의 그림 방향, 코리올리 부호 정의, 대표 문항의 소유 범위와 Anchor 문구. 원문은 수정하지 않았다. 일정 구동속도 표현은 시간에 따른 순간속도와 일정한 진폭·주파수로 구분해 보완했다.
