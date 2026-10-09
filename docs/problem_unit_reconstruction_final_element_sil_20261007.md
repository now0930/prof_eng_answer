# Final-element SIL/SIS Topic Pack 감사

작성일: 2026-10-07
대상: `final_control_element_sil_sis_esd_valve_partial_stroke_test`

## 판정

10개 예상문항은 SIF의 Final Element라는 일관된 subsystem owner 안에서 역할/boundary, PST 비교, PFDavg/PFH, ESD architecture, safe-state, failure/diagnostic, proof-test program, response time, bypass, lifecycle evidence라는 독립 문제 단위로 성립한다. PST 비교(P2)와 proof-test program(P7)은 일부 지식이 겹치지만 전자는 coverage/failure-set 비교, 후자는 interval·repair·restoration·records를 포함한 program 설계라 분리 유지한다.

## 보완

- 기존 required-anchor union은 46/48이었다. `actuator_force_margin_handoff`를 P4 architecture/P8 response-time handoff에, `seat_leakage_as_safety_requirement`를 P1 scope/P7 proof-test/P10 acceptance에 연결해 질문 요구를 반영했다. 보완 후 union은 48/48이고 outline coverage도 48/48이다.
- 기존 10개 intent는 ID형 접두사 뒤 동일 generic 문구를 사용했다. 각 question demand에 맞는 고유 intent로 교체했다.
- Pattern 3은 PFDavg/PFH 계산과 직접 관련된 demand mode, subsystem budget, failure rate partition, test interval, PTC와 imperfect test risk에 집중하고 PST-specific detail은 강제하지 않는다.
- High-score/common-missing/high-band 조건을 pattern별로 표시했다. P2/P7은 test scope, P3은 reliability calculation, P8은 response time, P9는 bypass/common cause에 한정하는 등 다른 문항 지식을 일괄 요구하지 않는다.
- Topic ID, question text, Question Type, Router, fatal/major checks, scoring contract, deterministic authority는 변경하지 않았다.

## 표준 기준 대조

공식 IEC 공개 scope에 따르면 IEC 61511은 process-sector SIS의 specification, design, installation, operation, maintenance를 다루며 SIS가 process safe state를 달성/유지하도록 하는 framework다. IEC 61511은 IEC 61508의 process-sector implementation이다. 본 감사는 이 상위 lifecycle/boundary 관점만 확인했고, 개별 조항·판본별 세부 요구나 현재 project compliance를 판정하지 않았다. 적용 edition과 실제 의무는 project SRS/controlled standards copy에서 확인해야 한다.

## 원자성 경고 및 후속

48-Anchor ownership warning은 유지한다. Anchor 수만으로 topic을 쪼개지 않는다. Current owner는 “SIF Final Element subsystem의 functional performance and verification”; actuator mechanical sizing, generic dynamics, valve taxonomy, cavitation/noise, leakage/packing, severe service, full package lifecycle는 인접 packs와 handoff한다. 별도 Topic/Router 추가는 Stage 6 overlap audit에서만 결정한다.

## 검증

- `validate_topic_packs.py --topic-id ...`: PASS (global Anchor uniqueness 포함).
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS, 기존 empty deterministic aliases warning 1건.
- Atomicity audit: PASS, 48-Anchor ownership warning 1건 유지.
- Scoped Topic Pack release: PASS; generated pipeline PASS, LLM smoke 미실행, generated banks는 사전 snapshot으로 복원.
- Pattern/example mirror 10/10, intent 고유 10/10, required Anchor union 48/48, outline refs 48/48, JSON parsing 및 `git diff --check`: PASS.
- `scripts/test_final_control_element_sil_sis_esd_pst_topic.py`: 57개 중 55 PASS, 2 FAIL. `test_manifest_alignment`는 알려진 87 source/82 manifest inventory 차이다. `test_model_importance`는 source 변경 후 checked-in generated bank가 재생성되지 않아 생긴 parity mismatch다. 기존 grader/router 경로 테스트와 공식 표준/Formula tests는 나머지 55개 PASS.
- Generated projection parity는 현재 source-only stage에서 승격하지 않았으며 Stage 7 integration에서 rebuild·재검증 필요.
