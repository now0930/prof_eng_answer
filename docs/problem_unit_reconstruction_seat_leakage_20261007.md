# Seat leakage·packing·fugitive emission Topic Pack 감사

작성일: 2026-10-07
대상: `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`

## 판정

10개 대표 질문은 leakage containment/performance라는 큰 공통 축 안에 있으나, 실제 질문의 지식 단위는 shutoff class, seat 설계·고장진단, 누설량 측정, stem packing/fugitive emission, acceptance workflow로 구분된다. 따라서 이 Pack의 48개 Anchor를 각 질문에 공통 적용하면 과잉 요구가 된다.

기존 pattern별 Anchor 연결은 48/48이고 Outline도 48/48을 참조한다. 내용 coverage를 늘리기보다는 high-score, common-missing, high-band 조건의 적용 pattern을 명시하여 문항 밖 지식을 요구하지 않도록 source를 보완했다. 새로운 Topic ID, active alias, Router, fatal/scoring contract는 바꾸지 않았다.

## 패턴별 범위 결정

| Pattern | 중심 단위 | 평가 한계 |
|---|---|---|
| 1 | Internal seat vs external packing leakage, shutoff class/test contract | 전용 시험조건 계약; emission 정량·packing 비교는 불필요 |
| 2 | Soft/metal seat와 sealing 구조 비교 | seat·구조 trade-off; gas reference 변환은 불필요 |
| 3 | Seat load/contact stress/pressure direction | actuator sizing은 별도 owner이며 작동력 영향 설명까지만 |
| 4 | Volumetric·mass·bubble 및 gas reference conversion | 환산 basis/단위/절대조건이 핵심; packing·seat 원인 불필요 |
| 5 | Seat leakage 원인 진단 | 원인 분류와 service evidence; repair procedure는 maintenance handoff |
| 6 | Packing·live loading·bellows·low-emission qualification | packing 구조·성능 trade-off; shutoff seat class는 자동 요구 아님 |
| 7 | Screening·bagging·fugitive-emission 측정 | 농도/질량배출률과 측정한계 구분 |
| 8 | 구매부터 현장까지 acceptance workflow | 질문에 든 단계/기록/인수 기준만 요구; 표준판 상세 암기 불필요 |
| 9 | As-found/as-left와 uncertainty-aware 판정 | 측정조건·불확도·검출한계·false decision |
| 10 | seat·class·packing·emission·maintenance의 명시 요구 통합 | 종합문항이나 48개 Anchor 전부를 자동 요구하지 않음 |

## 구조 경고 및 owner 보류

- Atomicity screen은 48 Anchor의 ownership review 경고를 낸다. Pattern 1–9는 위 leakage 성능의 세부 질문으로 성립하며 Pattern 10만 명시적 통합형이다.
- 내부 seat leakage/shutoff class와 external packing/fugitive emissions를 완전 별도 Topic으로 나누는 안은 가능하지만, 이 source review만으로 별도 canonical owner를 승인하지 않는다. 현재 Pack은 누설 경로와 acceptance를 함께 다루므로 임시 유지한다.
- Topic Sheet에 미래 maintenance/standard 전문 Topic handoff가 언급되지만, 아직 존재하지 않는 ID는 source에 활성 routing alias로 추가하지 않는다.
- 개별 표준 class의 정확한 시험조건/판본 값은 이번 경계 작업에서 새로 검증하거나 확정하지 않았다. 이는 후속 내용 검토로 남긴다.

## 변경 및 검증

- `model_answer.json`: 16 high-score, 12 common-missing 항목에 적용 pattern을 명시; 종합 feature/low-score 문구도 Pattern 10 및 관련 문항으로 한정.
- `topic_importance.json`: 8 high-band unlock 조건을 pattern 번호로 제한.
- README/Topic Sheet: pattern별 평가표를 추가해 지식 family 간 불필요한 감점을 방지.
- Question pattern, required Anchor, outline, Topic ID, Question Type, routing, fatal conditions와 score contract는 변경하지 않음.
- `validate_topic_packs.py --topic-id ...`: PASS (global 2,066 Anchor uniqueness 포함).
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS, 기존 `deterministic_checks.topic_aliases empty` warning 1건.
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS, `LARGE_ANCHOR_INVENTORY` 1건 유지; warning을 숨기거나 자동 해소하지 않음.
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS, LLM smoke는 미실행, generated banks는 사전 snapshot으로 복원.
- 두 수정 JSON `json.tool` parsing 및 `git diff --check`: PASS.
