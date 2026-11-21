# S7 B7 — 독립 검토자 2인 판정 검증 (2026-11-17)

## 목적

[이전 기준선](https://github.com/now0930/prof_eng_answer/actions/runs/43999331291): HEAD `a1396838c51ae0bfd5784ee42b46cd083a2ea42b`, 1,949 passed, 2 skipped, VALIDATION=PASS. 기존 119 Fact는 HOLD, Source Review 누락 179 projection, 기존 정합 초안 20건에서 EXACT_RELATION 인식 0건이다. 마지막 비수식 5건의 전문가 대기 목록이 생성됐지만 **독립 전문가 판정은 아직 0건**이다.

이 단계에서 **검토자가 작성한 판정 문서 2개를 안전하게 비교하는 오프라인 검사기**만 추가한다. 실제 검토가 이루어졌다는 주장은 하지 않는다.

## 절차

1. [이전 프로토콜](s7_remaining_five_independent_review_protocol_20261117.md)에 따라 **실제 같은 HEAD에 해당하는** `s7-alias-source-review.json` 및 `s7-remaining-five-expert-queue.json`에서 `prepare_s7_private_expert_review_packet.py`으로 비공개 원본 검토 패킷을 생성한다. 저자가 만든 정합/반례 표시는 별도 sealed-map에만 보관한다.
2. 같은 label-hidden 패킷을 두 검토자에게 **개별적으로** 전달한다. 서로의 판정, 저자 표지, sealed-map은 보여주지 않는다. 검토자는 독립적으로 10개 문장 각각의 `expert_label`, `condition_ids_explicitly_asserted`, `condition_ids_missing_or_ambiguous`, `expert_rationale`, `disputed_claim_or_scope_notes`, `reviewer_confidence`를 채운다.
3. 검토 완료된 두 패킷은 `reviewer_id`가 서로 다르고, `review_date`는 ISO 날짜이며, `evaluation_status=COMPLETE_BY_INDEPENDENT_REVIEWER`이어야 한다. 정답 판정 후보는 네 가지로 제한한다: `RELATION_WITH_REQUIRED_CONDITIONS`, `RELATION_BUT_CONDITIONS_MISSING`, `CONTRADICTORY_RELATION`, `UNDETERMINED_OR_OUT_OF_SCOPE`. 각 조건 ID는 원본 Registry에 존재해야 하며, 완전한 관계 판정에는 필요한 조건 ID가 전부 명시되어 있어야 한다.
4. 별도 비공개 디렉터리에서 아래 명령을 실행한다. 출력은 두 사람의 **라벨/조건 일치 수와 불일치한 항목 ID**뿐이며, 검토 내용·원문·출처 상세나 저자의 예상 정답은 포함되지 않는다.

```bash
python3 -B scripts/audit_s7_private_expert_reviews.py \
  --original-packet /private/s7_review_packet_original.json \
  --reviewer-a /private/s7_review_A_completed.json \
  --reviewer-b /private/s7_review_B_completed.json \
  --report /private/s7_reviewer_agreement_report.json
```

## 엄격한 제한

- 동일 reviewer ID, 잘못된 날짜, 답안 내용 수정, Fact ID/Source 카드 수정, 누락/중복 판정, 출처에 없는 조건 ID, 상충된 조건 목록 또는 승인되지 않은 라벨 => 실패 후 HOLD.
- 라벨 10/10 일치하더라도 **실제 검토자의 독립성은 시스템이 인증하지 못한다**. 일치율은 정확도/정밀도/재현율이 아니다. 시스템은 항상 `human_identity_independence_verified=false`, `expert_benchmark_ready=false`, `scorer_accuracy=null`, `score_admission=DISABLED`를 보고한다.
- 전문가 판단의 출처와 충돌·합의를 별도로 기록하고, **독립적으로 새로 작성한 답안 예제**에 대한 학습·평가 분리 및 오검출 시험을 완료하기 전에는 S7 B7을 닫을 수 없다.
- 원본 reviewer packet과 sealed-map, 판정 제출 파일, 사적 감사 보고서는 **GitHub/PR/Issue/Actions Artifact에 올리지 않는다**. 이 단계의 스크립트는 Actions에서 실행하지 않는다. CI에는 코드를 대상으로 한 **가상 검토자 테스트만** 실행된다.
- Registry/Fact Anchor/Ontology/Topic Pack/정규 채점기/Golden 변경 없음. PR #38 Draft, 119 HOLD, B7/D2/D3 OPEN, `score_admission=DISABLED`, 자동 Alias 승격·병합·배포 금지.

## 새 구현 경로

- `grading/evidence/s7_independent_review_validation.py` — 2인 검토 문서 불변성, 라벨·조건 ID 검증 및 비공개 집계.
- `scripts/audit_s7_private_expert_reviews.py` — 수동 실행 전용; 리포지토리 외부의 별도 신규 보고서만 생성.
- `tests/test_s7_independent_review_validation.py` — 가상 응답, 판정 누락·변조·중복·조건 충돌·비인가 라벨에 대한 방어 시험.

### 다음 검증 게이트

이 파일을 포함한 **최신 HEAD**에 대한 전체 `validation.yml` 수동 실행이 필요하다. 이전 HEAD의 PASS를 전용하지 않는다. 연구 Artifact 8개의 보존과 독립 검토용 private-runner가 CI에서 실행되지 않았음을 확인한 뒤, 실제 독립 검토자 데이터를 수집한다.
