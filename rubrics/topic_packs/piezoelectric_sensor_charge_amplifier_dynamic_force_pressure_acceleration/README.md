# 압전식 센서의 원리, 전하증폭기, 동적 힘·압력·가속도 측정 및 오차

- Topic ID: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`
- 문항 유형: `PRINCIPLE_INTERPRETATION`
- 이론 깊이: `FIELD_APPLICATION`
- 준비 우선순위: `NORMAL`
- 채점 방식: `LLM_ONLY`

## Source

- 요구사항: `docs/topic_sheets/piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration.md`
- `fact_anchor.json`: 20개 핵심 사실 Anchor와 10개 Fatal 오개념
- `logic_check.json`: deterministic check 비활성, LLM profile 활성
- `model_answer.json`: 답안 구조, 고득점 요소와 data-driven routing
- `topic_importance.json`: 중요도와 준비전략

## Topic 경계

압전효과, `Q=dF`, 전하증폭기, IEPE, `pC/N`, 동적 힘·압력·가속도, 공진과 설치오차가 중심이면 이 Topic을 Primary로 사용한다.

게이지율, Wheatstone bridge, `mV/V`, 크리프와 장시간 정하중이 중심이면 `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`를 Primary로 사용한다.

저항형·용량형·유도형 수동센서의 일반 비교가 중심이면 `passive_sensor_resistive_capacitive_inductive_transduction`을 Primary로 사용한다.

## Validation

- deterministic fatal 및 major check는 사용하지 않는다.
- candidate extraction 규칙은 비워 둔다.
- ChatGPT가 승인된 요구사항 Markdown과 Source JSON을 직접 의미 검토한다.
- 독립 LLM semantic evaluation과 로컬 Ollama E2E는 실행하지 않는다.
