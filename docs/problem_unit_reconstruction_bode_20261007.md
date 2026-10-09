# Bode 주파수응답 Topic Pack 문제 단위 보완 — 2026-10-07

## 판정

`bode_frequency_response_stability_margin_bandwidth`는 Bode 주파수응답이라는 공통 원리를
사용하는 8개의 출제 가능한 질문 패턴을 유지한다. 원리·작도, 여유 계산, 교차주파수 정의,
폐루프 대역폭, gain 설계, lead/lag 설계, 시간지연 영향, 다중 교차점 한계는 서로 연관되지만
각 문항의 요구가 다르므로 모든 내용을 모든 답안의 필수점으로 취급하지 않는다.

## 확인된 문제와 수정

1. 기존 expected pattern은 14개 Anchor 중 12개를 required union으로 참조했다(12/14 = 85.7%,
   screen 정수 표시 86%). 위상 기여 Anchor는 원리·작도 질문에서 빠져 있어 해당 패턴에 추가했다.
2. “이득교차주파수와 위상교차주파수의 차이” 질문은 각 주파수의 정의 차이를 묻는다. 기존에는
   이 패턴이 PM·GM 수치 계산까지 요구했으므로 두 계산 Anchor를 필수에서 제거했다.
3. 시간응답 근사 Anchor는 현재 8개 대표 패턴 중 직접 요구하는 패턴이 없다. 이를 다른 질문에
   억지로 요구하지 않고 선택 지식으로 유지했다. 그 결과 required union은 13/14 (92.9%)다.
4. 8개 recommended outline 모두에 Anchor 참조를 연결했다. Outline은 종합 학습 전개 구조이고,
   전체 outline을 개별 질문의 필수 답안으로 요구하는 것은 아니다.
5. 전역 high-score/common-missing 설명과 `high_band_unlock_conditions`를 pattern별 문구로 바꿔,
   대역폭·지연·보상기·현장 검증이 무관한 질문의 공통 감점/고득점 조건으로 읽히지 않도록 했다.

## 적용 경계

- `expected_question_patterns[].required_anchor_ids`가 질문별 필수 지식 범위다.
- outline Anchor 참조는 학습 순서/내용 탐색용이다.
- 누락된 선택 지식 자체는 오답 또는 fatal 근거가 아니다. fatal misconception은 답안이 실제로
  해당 오개념을 주장했을 때만 적용한다.
- 이는 Topic Pack source 및 작성 문서의 계약 명료화다. 현재 runtime이 pattern별 score
  gating을 수행한다고 주장하거나, 채점기 알고리즘·점수 계약을 변경하지 않았다.

## 검증 결과

- `validate_topic_packs.py --topic-id ...`: PASS; global anchor uniqueness 포함 2,066 Anchor 검사
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS; error 0, warning 0
- `audit_topic_pack_atomicity.py --topic-id ...`: PASS; warning 0
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS
- 별도 참조 검사: 8 patterns, 13/14 required-anchor union, outline 14/14 Anchor 참조, 미해결 참조 0
- Release 검증 산출 `rubrics/generated/`는 검증 전 snapshot으로 복원했다.

## 변경 파일

- `rubrics/topic_packs/bode_frequency_response_stability_margin_bandwidth/model_answer.json`
- `rubrics/topic_packs/bode_frequency_response_stability_margin_bandwidth/topic_importance.json`
- `rubrics/topic_packs/bode_frequency_response_stability_margin_bandwidth/README.md`
- `docs/topic_sheets/bode_frequency_response_stability_margin_bandwidth.md`
- `docs/topic_pack_reorganization_progress_20261007.md`
- `docs/README.md`

기존 Grader 계약, 결정론 점수, canonical Question Type/Router, fatal ID, Golden test와 전체
release gate는 수정하지 않았다. 커밋·push하지 않았다.
