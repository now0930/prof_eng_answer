# S7 Source-Owned Relation ID Bridge — 연구 전용 경로

**실행 기준:** PR #38 Draft, `feat/claim-alignment-verification-20261114`. 신규 커밋 후 전체 Actions 재검증 필요.

## 기준 및 관측

Actions #43977256043 (`5db9cba44e7a8068d950240ee7840defdc3857af`)의 네 Artifact를 직접 비교하여 다음 사실을 확인했다.

| 근거 | 실측 |
|---|---|
| 기존 canonical Claim Alignment | 작성자 정합 초안 20개 중 `EXACT_RELATION=0` |
| 반례 Claim Alignment | 20개 중 `EXACT_RELATION=0` — 인식 자체가 없어 성공을 뜻하지 않음 |
| S7 Alias inventory | 179 projection = 119 unique owner-Fact, 179 `ID_NOT_FOUND` |
| S7 Source Review | 119/119 HOLD, 117건은 조건 지정 필요, 승인된 새로운 Alias 0 |
| 제한 수식 Shadow | 정상 표면형식 6/6, 역방향 표면형식 6/6, 오탐 충돌 0/6 |

Registry가 독립적으로 승인/검증된 사실이라고 하여 Answer에서 동일 Subject/Predicate/Object relation이 **파싱되었다는 뜻은 아니다**. 실제 canonical extractor는 Topic Machine Contracts와 현재 Ontology 후보에서 추출하며, 다수 Registry ID가 그 범위에 없다.

## 이번 변경

`grading/evidence/s7_registry_relation_bridge.py`는 **새 파서가 아니라**, source-review와 20개 작성자 초안 및 6개 수식 결과를 ID 기준으로만 결합하는 연구용 감사 경로다.

1. 119개 source-review가 모두 HOLD/score-disabled인지 확인한다.
2. Source/Formula Artifact가 동일한 정확한 실행 HEAD의 결과인지 확인한다.
3. 수식과 원천 Fact의 owner/topic/fact/source/subject/predicate/object/polarity/condition ID가 6개 수식마다 정확히 부합하는지 확인한다.
4. 수식의 정상 문자형식인 6건에서 **source에 적힌** relation ID 후보를 별도로 표시한다. 이들은 사용자 답안에서 독립 파싱된 relation ID가 아니다.
5. 역방향 문자형식 6건은 `FORMULA_DIRECTION_CONFLICT_REVIEW`로만 표시하고 일반적인 오답 확정으로 사용하지 않는다.
6. 나머지 14개 수식 외 관계에는 새 인식 규칙을 제공하지 않고 `NO_FORMULA_SHADOW_COVERAGE`를 기록한다.
7. 어떠한 경우에도 `EXACT_RELATION`, 조건 성립 판정, A~E 점수, WRONG/Fatal/Ceiling/합격 여부, 새 Alias 승인으로 연결하지 않는다.

출력은 `s7-registry-relation-bridge` Artifact에 ID/관측 상태만 저장하고 원문 답안과 전체 문장 텍스트를 저장하지 않는다. Artifact를 얻기 위한 GitHub Workflow 옵션은 `Replay 47 Golden cases and audit 179 missing aliases (research only)` **ON**이며, independent expert baseline 옵션은 이 단계에 필요하지 않다.

## 연구 가설과 다음 판정

이 경로가 성공하면 **공식 Registry relation ID와 일부 문장형식 사이의 source-borrowed 연결 구현 가능성**만 확인되는 것이다. `EXACT_RELATION` 검출 개선이나 기술적 정합 판정 정확도 개선은 아직 입증되지 않는다.

이후 단계는 (a) 검증된 전문가 라벨, (b) 부정·인용·조건 미충족·동음이의 문구·수식 방향·단위·정의역 반례, (c) 독립 파서가 실제 답안으로부터 relation과 조건을 획득하는지 여부, (d) Source ID 재사용이 아닌 실제 엔진의 인식률 상승을 평가해야 한다. 통과 여부에 따라 제한된 owner-specific Ontology ID candidate를 별도 리뷰 대상으로 제시할 수 있으나 자동 승인하지 않는다.

**비변경 보장:** Fact Registry, Ontology, Topic Pack, Machine Contract, 생산 채점기, 정책, Golden 기대값, B7/D2/D3 OPEN, 119 HOLD, `score_admission=DISABLED`, Draft 상태를 변경하지 않는다.
