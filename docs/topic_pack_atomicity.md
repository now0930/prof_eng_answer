# Topic Pack Atomicity 운영 기준

## 목적

한 Topic Pack이 하나의 출제 문제군과 지식 소유 경계를 유지하는지 자동 점검한다.
anchor 수가 많다는 사실만으로 분리하지 않으며, 실제 기출문제·routing·Golden 회귀가
독립 소유권을 입증할 때만 새 Topic으로 분리한다.

## 자동 Gate

```bash
python3 scripts/audit_topic_pack_atomicity.py
python3 scripts/audit_topic_pack_atomicity.py \
  --output reports/topic_pack_atomicity_audit_YYYYMMDD.json
```

다음은 release 차단 오류다.

- Topic owner와 다른 model ID 또는 중복 model ID
- `required_anchor_ids`가 없는 문자열 질문 계약
- modern/legacy 질문·alias mirror의 명백한 의미 불일치
- Fact Anchor와 Logic truth schema의 명백한 의미 불일치
- 다른 Topic의 긴 `core_facts`가 3개 이상 그대로 복제된 경우

다음은 검토 경고이며 자동 분리 사유가 아니다.

- anchor 40개 이상
- 질문 계약이 3개 이상의 anchor-disconnected family로 나뉨
- 두 Topic 사이에 정규화 alias가 2개 이상 겹침
- 공식 출제기준 분류 문서 누락

`--strict-warnings`는 inventory 정리 작업에서만 사용한다. 일반 release는 오류 0건을
요구하고 경고는 추적 대상으로 남긴다.

## 2026-09-09 기준선

- 전체 78 Topic, 2,010 anchors
- 차단 오류: 128 → 0
- 문자열 질문 계약: 116 → 0
- P0 소유권 오염 복구:
  - Thermistor Pack의 RTD·Thermocouple mirror
  - 제어밸브 정비 Pack의 positioner·selection mirror
  - Nyquist Pack의 Routh mirror
  - 압전센서 Logic truth schema의 strain-gauge mirror
- 남은 경고: 40
  - disconnected question families 24
  - large anchor inventory 10
  - cross-topic alias collision 6

상세 기계 판정은
[`reports/topic_pack_atomicity_audit_20260909.json`](../reports/topic_pack_atomicity_audit_20260909.json)에
보존한다.

## P1 분리 판단

현재 경고는 기존 Pack을 즉시 분리하지 않는다. 다음 증거가 모두 있어야 한 Topic씩
분리한다.

1. 서로 독립된 실제 기출 또는 운영 질문군이 존재한다.
2. 두 질문군의 `required_anchor_ids` 교집합이 작고 각각 독립 답안을 구성한다.
3. 기존 router에서 오라우팅 또는 후보 간격 저하가 재현된다.
4. 정상·부분·오답·fatal Golden fixture를 새 owner별로 만들 수 있다.
5. 분리 전후 동일 입력의 score·fatal·routing 차이를 설명할 수 있다.

경고만 있고 3~5의 회귀 증거가 없으면 현재 owner를 유지한다. 기술적으로 관련된
하위 질문이 서로 다른 anchor를 쓰는 것은 곧바로 다중 Topic이라는 뜻이 아니다.

## 변경 전후 회귀 계약

동일 문제·동일 답안에 대해 다음을 기록한다.

```text
primary_topic_id
candidate topic order and score
total_score
fatal_error_detected
final verdict
```

순수 질문 계약 구조화는 점수·fatal·routing을 바꾸지 않아야 한다. P0 오염 복구처럼
의도된 변화가 있으면 올바른 owner로의 routing 개선과 foreign evidence 제거를 별도로
설명한다. 어떤 경우에도 test expected 완화나 fatal rule 삭제로 차이를 숨기지 않는다.

## 유지관리

- 신규·수정 Topic은 source 검토 후 이 Gate를 실행한다.
- 질문 패턴은 항상 객체형 `pattern + required_anchor_ids`로 작성한다.
- Fact Anchor가 정본이며 Logic truth schema와 legacy mirror는 정본에서 투영한다.
- generated bank는 직접 수정하지 않는다.
- 경고 수 증가는 PR에서 원인과 유지/분리 결정을 기록한다.
- 실제 오판정이 없는 P1 후보는 묶음 분리하지 않는다.
