# Physical AI·로봇·자율제조 Topic Pack 문제 단위 감사

갱신: 2026-10-07
대상: `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
판정: 통합 Physical-AI system 문제 단위를 유지하고 question-to-anchor trace를 보완했다.

## 발견과 조치

- 초기 atomicity audit에서 `DISCONNECTED_QUESTION_FAMILIES: 8, 1, 1`이 확인됐다. Sensor Fusion 문항(2)과 State Estimation/Localization/SLAM 문항(3)이 폐루프 Physical AI 문항(1)과 required Anchor를 공유하지 않았다.
- 센서 관측 융합은 State Estimation의 입력이고, 추정 상태는 World Model/Planning과 폐루프 제어에 전달된다. 이 기술적 연결을 반영해 기존 `state_estimation` Anchor를 질문 1·2·3에 연결했다. 새 Fact Anchor, 새 Topic, alias나 Router 규칙은 만들지 않았다.
- 문항 3을 `State Estimation·Localization·SLAM·World Model 연계`로 구체화해 기존 World Model Anchor도 직접 요구하도록 했다. 이에 30개 Fact Anchor 모두 적어도 한 문항의 required Anchor에 포함되고, outline도 기존대로 30/30을 유지한다.
- 10개 question pattern에 각각 별도 intent를 작성하고 `question_examples`를 같은 순서로 투영했다. High-score/common-missing 및 importance unlock 조건은 문항별 적용범위로 한정해 서로 다른 하위 문제의 내용을 한 답안에 일괄 요구하지 않는다.
- 8개 question pattern으로 연결된 다른 분야는 Physical AI의 sensor-state-action-runtime assurance system에 종속된 응용 문항으로 유지했다. 기준은 단순히 키워드가 비슷해서가 아니라 perception→estimation→world representation/planning→safety-constrained actuation→monitoring의 인과연결이다.
- Question Type, difficulty/importance, topic aliases, fatal 16건, LLM-only semantic authority 및 생산 코드/Router 변경은 유지했다.

## 검증

- SW-13 focused regression: 16 tests PASS
- Topic schema validation: PASS
- Topic quality validation: PASS, errors 0, warnings 1. 기존 LLM-only Pack의 빈 deterministic topic alias 경고이며 의미 판정은 LLM profile 단독 소유다.
- Atomicity audit: PASS, 0 warnings; question family가 하나의 연결 component로 확인됨
- Scoped generated-pipeline release: PASS; live LLM smoke는 생략
- Release validator가 `rubrics/generated/`를 사전 snapshot으로 복원했으며 generated projection은 promote하지 않았다.
- `git diff --check`: PASS

이번 수정은 source Topic Pack과 focused test/문서에 한정했다. 전체 worktree에 기존 미커밋 변경이 있어 commit/push하지 않았다.
