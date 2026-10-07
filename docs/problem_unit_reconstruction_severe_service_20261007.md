# Severe-service control-valve Topic Pack 감사

작성일: 2026-10-07
대상: `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`

## 판정

10개 예상문항은 하나의 상위 응용영역인 severe-service valve selection 안의 서로 다른 시험 단위로 성립한다: (1) 복합 위험/운전 envelope, (2) high·low flow, (3) micro-flow, (4) 고온, (5) 극저온, (6) 입자·slurry·fibrous fluid, (7) 고장 원인진단, (8) screening 계산, (9) lifecycle workflow, (10) 경제성 trade-off. 별도 Topic 분할보다 같은 service-selection domain의 문항군으로 유지하되 평가조건을 pattern별로 제한한다.

## 누락 및 오연결

- 기존 48 Anchor 중 expected question required union은 43/48이었다. 다섯 Anchor를 질문 요구에 맞춰 연결했다.
  - `multiphase_entrained_gas_uncertainty` → P1 combined risk/envelope.
  - `downstream_piping_outlet_effect` → P2 high-flow downstream effect.
  - `actuator_breakaway_thermal_friction_handoff`, `seat_packing_material_tradeoff` → P4 고온 package/packing 상호작용.
  - `cavitation_flashing_noise_handoff` → P7 성능저하 진단의 전문 손상원인 handoff.
- Outline은 이미 48/48 연결돼 있었다. 보완 후 required union도 48/48이 됐다.
- 기존 10개 `intent`는 질문 문장을 다시 쓰고 generic suffix를 붙여 문항별 의도를 구분하지 못했다. 각 질문의 demand를 반영한 intent로 바꿨다.
- High-score/common-missing/importance 기준은 pattern별 적용범위를 명시했다. 예를 들어 고온, 극저온, 입자 내용은 해당 문항에서만 요구한다.
- 상세 actuator thrust, cavitation/flashing/noise physics 등 specialist Topic 소유 지식은 재수행·재소유하지 않고 handoff로 남겼다.
- Topic ID, question wording, Question Type, Router, fatal/major checks, scoring contract와 deterministic authority는 변경하지 않았다.

## 구조 경고 및 후속

Atomicity audit는 48 Anchor inventory에 대한 ownership 경고를 낸다. 질문 패턴들은 서로 다른 severe-service 상황을 덮지만 공통 선정·failure-mitigation domain을 공유하고 P1/P9가 workflow를 묶으므로 현재 Pack을 유지한다. 별도 Topic 또는 Router owner 추가는 Stage 6 교차영역 검토에서만 판단한다.

## 검증

- `validate_topic_packs.py --topic-id ...`: PASS (global 2,066 Anchor uniqueness 포함).
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS, 기존 empty deterministic aliases warning 1건.
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS, `LARGE_ANCHOR_INVENTORY` 48-Anchor owner warning 1건 유지.
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS, LLM smoke 미실행, generated output은 사전 snapshot으로 복원.
- Pattern/example mirror 10/10, intent 고유 10/10, required-anchor union 48/48, JSON parsing 및 `git diff --check`: PASS.
- Severe-service 전용 focused regression은 찾지 못해 실행하지 않음. Runtime scoring이나 routing 수정은 없다.
