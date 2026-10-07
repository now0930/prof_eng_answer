# 압전센서 Topic Pack 문제 단위 감사 — 2026-10-07

대상: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`
유형: 문항별 intent·채점범위 및 독립 요구군 검토

## 판정

압전 직접효과를 시작점으로 전하 발생, conditioning, 동적 측정과 현장 오차를 다루는 하나의 학습 Pack으로 유지한다. 힘·압력·가속도 및 회로·오차 문항은 개별 답안 요구가 다르므로 하나의 종합 답안을 모든 질문에 강제하지 않는다. Required Anchor union은 이미 20/20이므로 연결률을 높이기 위한 불필요한 required Anchor는 추가하지 않았다.

## 발견과 보완

- 14개 예상 문항의 `intent`가 모두 동일한 일반 문장이어서 질문별 답안 의도를 구별하지 못했다. 문항별로 원리·등가회로·전하증폭기·IEPE·힘/압력/가속도·대역·케이블·온도·비교선정 요구를 각각 작성했다.
- 초기 screen의 4개 연결요소(2·7·2·3)는 직접효과/역효과 원리, 등가회로 및 센서 특성, conditioner/ADC, 압력·케이블·온도 오차군이다. 이들은 모두 압전 측정사슬과 현장 사용에 속하지만 서로 다른 예상 질문이므로 공통 필수 Anchor를 억지로 추가하지 않았다. 이 구조 경고는 의도된 문항 다양성 신호로 남긴다.
- 20개 Anchor 모두 적어도 한 expected pattern에 연결되어 있었고 `question_examples` 14개도 pattern과 일치했다. 기존 required-Anchor 연결은 재작성하지 않았다.
- 전역 `high_score_points`, `common_missing_points`, `high_band_unlock_conditions`에 각 적용 문항 번호를 명시해, 예를 들어 IEPE 세부사항을 모든 압전 질문에 일괄 요구하지 않도록 했다.
- README와 Topic Sheet의 “candidate extraction rules empty”는 `logic_check.json` 전체 설정이 비어 있다는 오해를 만들 수 있었다. 실제 custom `rules` 배열은 비어 있지만 LLM profile의 `key_terms` 추출은 설정되어 있음을 명확히 했다.
- 스트레인 게이지 비교, 압전센서 오차 종류, 합성 채점 문항은 답안 coverage를 넓히되 기존 별도 Topic의 owner나 routing을 변경하지 않았다.

## 보호한 경계

- Question Type `PRINCIPLE_INTERPRETATION`, 기존 anchor/fatal inventory, LLM-only truth/logic 권한, alias와 deterministic scoring은 변경하지 않았다.
- 새 Anchor·토픽·runtime 분기를 추가하지 않았다. 고득점·누락 문구의 문항번호는 적용범위 설명이며 점수 계산 로직 변경이 아니다.
- 전체 Topic Pack 정확성 및 재료별 외부 handbook 판본 대조는 이번 검증 범위 밖이다.

## 검증

- `scripts/test_piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration.py`: 6 tests PASS
- `validate_topic_packs.py --topic-id ...`: PASS
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS, warning 1건(`DISCONNECTED_QUESTION_FAMILIES`, 독립 문항군을 연결하지 않음)
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; live LLM smoke 생략
- Release validator가 `rubrics/generated/`를 검증 전 snapshot으로 복원했다. Runtime projection promote는 하지 않았다.
- `git diff --check`: PASS

## 남은 검토

Topic Sheet에는 재료별 측정 원리와 적용 세부사항이 넓게 정리되어 있다. 추후 기술 검토에서는 힘센서 예압·하중 우회, 동압 설치·열충격, 가속도계 장착공진 항목을 주 출처와 대조하면 된다. 현재 독립 연결요소만으로 별도 Pack 생성이나 owner 이관은 하지 않는다.
