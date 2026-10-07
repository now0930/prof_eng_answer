# Control-valve selection process Topic Pack 감사

작성일: 2026-10-07
대상: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`

## 판정

12개 질문은 하나의 상위 단위인 “전문 분석 결과를 인수해 제어밸브 package를 선정하고 조달·인수·운전 feedback까지 닫는 workflow”를 이룬다. Pattern 1은 전체 workflow, Pattern 2–12는 process data, governing case, component/material selection, 전문결과 통합, actuator package, 문서조달, bid 검증, acceptance, lifecycle 및 field feedback을 각각 묻는 하위 질문이다. 별도 Topic 분리보다 상위 절차 Pack + 독립 하위문항으로 유지하는 것이 타당하다.

## 발견 사항과 조치

- 52개 Anchor가 12개 질문에 52/52 required union, outline도 전체 52개를 연결한다. 단, 자동 atomicity 경고는 큰 inventory 경계를 추가 검토하라고 알리므로 유지한다.
- 12개 pattern의 `intent`가 모두 같은 generic 문장이었다. 각 질문의 직접 요구에 맞게 intent를 고쳐 Model Answer/Grader projection이 문제 의도를 구분할 수 있도록 했다.
- Pattern 7(재질·sealing 선정)에 `actuator_thrust_torque_supply_minimum` Anchor가 들어가 질문과 불일치했다. 이를 제거하고 직접 요구되는 온도 envelope/thermal transient Anchor를 연결했다. 52개 Anchor는 다른 패턴의 actuator package 문항에서 계속 사용되므로 required union은 유지된다.
- Pattern 5의 Cv·sizing 통합 문항은 liquid/gas sizing handoff를 명시적으로 포함하고 있는지 확인했다. 해당 Anchor는 이미 포함돼 있어 유지했다.
- 전역 high-score/common-missing/importance 기준을 pattern별로 한정했다. Pattern 1은 전체 절차를 다루지만 전문계산 자체의 재수행이 아니라 assumption·margin·limitation·evidence를 포함한 handoff를 평가한다. Pattern 2–12는 질문 밖의 전문 지식 누락으로 감점하지 않는다.
- Topic ID, question examples, canonical Question Type, existing routing, fatal/major checks, score contract 및 deterministic authority는 바꾸지 않았다.

## 경계·후속 검토

- specialist Pack은 전문 물리·상세 계산을 소유하고, 현재 Pack은 통합된 입력·결과의 정합성, package trade-off, 조달·인수·수명주기 폐루프를 소유한다.
- Pattern 1의 31개 required Anchor는 넓은 전 과정 서술을 나타내지만, 이를 31개를 모두 상세 산출/암기해야 한다는 의미로 채점하면 과잉 요구다. 고득점 설명은 workflow 및 traceability에 집중한다.
- 상세 표준·판본·법규값의 정답성은 이번 문제 경계 작업에서 재검증하지 않았다.

## 검증

## 검증

- `validate_topic_packs.py --topic-id ...`: PASS (global 2,066 Anchor uniqueness 포함).
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS, 기존 empty deterministic aliases warning 1건.
- Atomicity audit: PASS, `LARGE_ANCHOR_INVENTORY` 52개 경계 warning 1건을 유지.
- Scoped Topic Pack release: PASS; generated pipeline PASS, LLM smoke 미실행, generated banks는 release validator가 사전 snapshot으로 복원.
- 구조 점검: 12 patterns / 12 question examples, 각 intent 고유, 예문 mirror 일치, required union 52/52. Pattern 7의 온도/열과도 입력을 명시하고 actuator-force Anchor를 제외.
- `scripts/test_control_valve_selection_process_lifecycle_topic.py`: 65개 중 63 PASS, 2 FAIL. `test_manifest_alignment`는 알려진 source 87개 / generated manifest 82개 inventory 불일치와 일치한다. `test_model_importance`는 수정된 source와 사전 snapshot generated bank가 다르기 때문에 실패한다. 이를 우회하거나 생성 bank를 승격하지 않았으며, 후속 integration stage에서 generated projection을 rebuild하고 관련 계약을 재검증해야 한다.
- JSON parsing 및 `git diff --check`: PASS.

따라서 source contract는 유효하지만 generated-bank parity는 아직 완료 판정하지 않는다.
