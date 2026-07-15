# 레이더식 레벨계의 FMCW·펄스 방식, 거리·레벨 측정원리, 유전율 영향 및 허위에코·설치오차

## Topic metadata

- Topic ID: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Semantic execution: `LLM_ONLY`
- Deterministic checks: disabled
- Candidate extraction: `{}`

## Source files

- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

## Core contracts

- 20 Fact Anchors
- 10 Fatal Wrong Claims
- 32 Routing Aliases
- 5 Routing Field Points
- 14 Question Examples
- 14 Expected Question Patterns
- 펄스식 왕복시간과 `D=cτ/2`
- FMCW 처프·비트주파수와 `D=cf_b/(2S)`
- 변조 대역폭과 거리 분해능
- 상대유전율과 반사에코
- 블로킹 거리, 허위에코와 다중반사
- 노즐·안테나 부착물·응축 및 설치오차

## Validation policy

Source JSON은 Requirements Markdown을 기준으로 직접 관리한다.
Generated bank는 Source 검토 완료 후 재빌드한다.
LLM 의미검증은 ChatGPT가 직접 수행한다.
컨테이너 전용 실행경로를 변경하지 않으므로 컨테이너 E2E는 생략한다.
