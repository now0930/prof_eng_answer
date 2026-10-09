# Topic Pack cross-topic owner·routing·view 영향 점검

> 이 문서는 통합 전 owner 경계 검토 기록이다. 87개 source/82개 운영 Pack 수치와 generated 미승격 상태는 당시 기준이며, 현행 수치는 [전체 내용·View 연결 감사](topic_pack_content_completion_20261007.md)를 따른다.

## 판정

Stage 6는 소스/기존계약 수준 점검을 완료했다. 기존 Topic routing authority를 바꾸지 않았고, ambiguity나 대형 Pack 경고를 “해결”로 위장하지 않았다. generated Grader·Training·Diagnosis view는 이 작업으로 활성화되지 않았다. 원천 검토 후 전체 bank를 다시 빌드하는 Stage 7에서 통합해야 한다.

## Inventory와 기계 점검

- Source directory: 87개 Pack, 2,068개 Anchor. 기존 운영/generated inventory는 82개이며, 나머지 5개는 미승격 managed drafts다.
- Full atomicity audit 전에는 error 0, warning 34였다. 두 managed draft ID를 classification 문서의 별도 draft section에 기록하고, 그 관계가 공식 분류가 아니라 내부 가설임을 다시 명시했다. 재검사에서 `CLASSIFICATION_TOPIC_MISSING` 두 건이 해소되어 현재는 error 0, warning 32 (disconnected question families 20, large-anchor inventory 10, cross-topic alias collision 2)다.
- 40/40 우선 구조·coverage 후보 각각의 owner 경계와 경고 처분은 진행 현황 및 개별 reconstruction 기록을 따른다. disconnected-family 경고는 독립 예상문항의 신호일 수 있으므로 Anchor를 인위적으로 공유시키지 않았다.

## 남겨둔 owner/routing 경계

- `lead_lag_compensator_phase_margin_steady_state_error`와 `root_locus_stability_gain_design`의 generic `lead compensator`/`lag compensator` 두 alias는 충돌한다. 패턴별 문제 문장에서는 구별되나 단독 짧은 질의는 모호할 수 있다. 기존 router authority와 dedicated test가 두 alias를 보존하도록 요구하므로 수정하지 않았다. 별도 owner 결정 없이 자동으로 한쪽에 고정하지 않는다.
- 10개 large-inventory 경고는 configuration lifecycle, 전통 positioner, seat/leakage, valve selection, severe service, final element, wired/wireless network, realtime network, smart positioner, OT security에 남아 있다. 패턴별 required coverage는 감사했지만, 서로 다른 question family를 하나의 runtime owner로 유지할지 분할할지는 학습·진단 view와 route 참조 migration을 묶어 별도 결정해야 한다.
- 새 pneumatic accessory 및 GWR Pack은 `draft / human_review_required` 상태를 보존한다. 내부 참고 정렬을 추가했어도 승인·운영 routing·generated promotion은 하지 않았다.

## View 영향

- 수정한 intent·pattern-scoped scoring/importance는 Topic Pack source의 콘텐츠 계약이다.
- 이번 단계는 Grader/Training/Diagnosis view 구현·projection을 수정하지 않았다. ephemeral full-bank rebuild로 호환 regressions만 검증하고 checked-in generated files는 복구했다.
- 현재 manifest는 82개 active pack이고, 87개 source 중 draft 5개를 제외한 것과 정확히 일치한다. Changed-source projection은 ephemeral rebuild 후 tests에 사용했으나 promote하지 않았다. 따라서 Topic source 변경이 현재 production runtime에 반영됐다고 말할 수 없다.

## 보호 조건

Question Type canonical values, existing topic-routing authority, fatal/logic/evaluator ownership 및 deterministic primary scoring은 그대로다.
