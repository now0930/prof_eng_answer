# S7 — 독립 Claim 정확도 평가 및 검토 절차 (점수 반영 금지)

## 2026-11-14 S7 원인 분해 후속 작업 — 신규 코드 재검증 전

- [Actions #43557519949](https://github.com/now0930/prof_eng_answer/actions/runs/43557519949):
  검증 HEAD `52b31e121376183a0d9c29ac38d47d7bfaecf015`,
  **1,703 passed, 2 skipped, VALIDATION=PASS**.
- 선택적 S7 연구는 **exit code 1 / INCOMPLETE_BASELINE**.
  실패 문항은 `model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc`.
  이 사례에 대해 기존 `tests/test_emc_fatal_scope.py`의
  `test_emc_model_answer_still_abstains` 및
  `tests/test_emc_remaining_six_rules.py`의
  `test_integration_scoring_unchanged_and_golden_abstains`가
  **`deterministic score engine abstained`를 명시적으로 예상**한다.
  해당 EMC Topic의 승인된 긍정 Anchor 채점 제외와 연결된
  **기존 안전 정책상 의도된 abstention**이며, S7 실험을 48/48로
  보이게 하려고 본 채점기를 수정하거나 Fact를 강제 해제하지 않는다.
  연구 집계는 `baseline_abstention_count`를 별도로 기록하며,
  `unexpected_baseline_failure_count`와 분리한다.
  새 S7 실험에서 이유 코드를 다시 확인하기 전까지 수치는
  이전 실행의 47/48을 기준으로 해석한다.
  예외 원문은 공개하지 않고 허용 목록의 `SCORE_COVERAGE_ABSTAIN`
  등만 출력한다.
- 전문가 Golden 47건 분석에서 검증 Registry Fact 179건을 투영했으나
  `EXACT_RELATION`은 0건이었다. 39건은 `NO_EXACT_RELATION`,
  8건은 `NO_VERIFIED_FACT_PROJECTION`.
  정답이 없다는 뜻이 아니라 **이번 구조의 근거 연결 결과가 비어 있다는 뜻**.
- 코드 구조상 `canonical_claim_extractor`는 **Machine Contract**의
  관계(subject/predicate/object)로 Claim을 추출하고,
  `fact_claim_adapter`는 승인 **Registry Relation**을 우선 투영한다.
  두 관계의 차이는 가능한 원인이지만 실제 충돌 비율은 아직 미측정.
- 신규 `claim_alignment_gap_diagnostics.py`가 Registry Fact별로
  `NO_ASSERTED_CLAIMS_FOR_TOPIC`, `NO_SUBJECT_MATCH`,
  `SUBJECT_ONLY`, `SUBJECT_PREDICATE_ONLY`,
  `TRIPLE_POLARITY_DIFFERS`, `TRIPLE_CONDITIONS_INCOMPLETE`,
  `TRIPLE_COMPATIBLE_AUDIT_ONLY`를 구분하여 **개수만** 출력한다.
  `verified_machine_relation_differs_count`로 기존
  `machine_relation_differs`와 함께 두 관계의 불일치를 집계한다.
  이 진단은 **정답 생성도, Claim 승격도, 채점도 수행하지 않는다**.
- `scripts/evaluate_claim_alignment_s7.py`에서 동일 질문/답안에 대해
  canonical extractor를 한 번 호출하고 결과를 기존 Claim Alignment에
  공급해 원문·question/answer fingerprint를 계속 검증한다.
  그 다음 진단 단계에서 parsed Claim과 승인 Registry Fact를 비교한다.
- 신규 회귀: 검증되지 않은 Fact, 인용/다른 Topic, 주어·술어·목적어,
  부정, 조건 미충족, forged canonical source,
  Primary abort 사유 비공개 처리까지 포함.
- **신규 커밋에 대한 전체 pytest 및 S7 연구 재실행은 아직 미완료.**
  이전 `52b31e12` PASS를 새 HEAD의 검증으로 대체하지 않으며,
  `CLAIM_ALIGNMENT_MODE=admit_verified`는 계속 비활성이다.
  PR Draft·미병합·실운영/점수/Registry/Logic 불변.

## 2026-11-14 후속 단계 — Registry surface recall (신규, 검증 전)

### 선행 실측 결과

[GitHub Actions #43559659003](https://github.com/now0930/prof_eng_answer/actions/runs/43559659003),
HEAD `09e4b1c7`: **1,718 passed, 2 skipped / VALIDATION=PASS**.
S7 연구는 47/48 사례, EMC 정책상 `SCORE_COVERAGE_ABSTAIN` 1건,
예상 밖 실패 0건, 승인 Fact 투영 누계 179건(고유 Fact 179개라는 뜻 아님),
단정형 Claim 110건 중 `mentioned` 63건, `EXACT_RELATION` 0건이다.

Fact 투영 누계 179건에 대한 실패 원인:
`NO_ASSERTED_CLAIMS_FOR_TOPIC=104`, `NO_SUBJECT_MATCH=72`,
`SUBJECT_ONLY=3`. 질문 Topic routing 미달은 0건.
**답안에 정답이 전혀 없다는 결론이 아니라 추출한 관계 대응이 비었다는 의미이다.**

### 새로운 분리된 실험 경로

- `grading/evidence/registry_surface_recall_audit.py`는 원본 approved Fact
  projection의 **검증된 Relation**에 한하여 표면형 subject/predicate/object가
  실제 답안의 **같은 문장**에 존재하는지 찾는다. 이 경로는
  `canonical_claim_extractor.py`나 `deterministic_primary_grader.py`를
  바꾸지 않으며, 임의 Fact·Topic·요구사항을 추가하지 않는다.
- 일치한 것도 `REVIEW_LITERAL_TRIPLET_ONLY`이며 정답 승인, 동등성 인정,
  Claim 추출의 정밀도 증명 또는 점수 가점이 **아니다**. 텍스트 동시 출현은
  물리법칙·조건·문맥의 실제 성립을 검증하지 못한다.
- 부정, 인용·거부·정정, 모든 조건부 Fact, 절대 표현은 **HOLD**이다.
  서로 다른 주어로 연결된 복합절에서 단어들을 교차결합하는 위험도
  `HOLD_COMPOSITE_CLAUSE`로 차단한다.
- 관련 Golden 반례: `risk_fsrm_demand_mode_fatal_01`의
  "PFDavg는 고수요 ...이고 PFH는 저수요 ..."에서 첫 주어(PFDavg)를
  두 번째 절의 목적어(저수요)와 결합하면 실제 오답이 정답 후보처럼
  보인다. `tests/test_registry_surface_recall_audit.py`는 이를 금지하고
  같은 자료의 정상 사례를 함께 검사한다.
- `scripts/evaluate_claim_alignment_s7.py`에는 **기존 canonical 후보와
  새 literal 리뷰 후보를 별도 항목으로 출력**한다.
  `candidate_count`는 기존 Canonical Claim–Fact 검토 후보이고,
  `registry_literal_candidate_count`는 새 **문자열 후보**이다.
  둘을 더하거나 자동으로 `SATISFIED`에 반영하지 않는다.
- `calibration/claim_alignment_s7_expected_abstentions.json`에는 기존
  두 회귀시험이 명시적으로 요구하는 EMC `SCORE_COVERAGE_ABSTAIN`
  한 건만 고정한다. 해당 ID·Gold 원본·원인 코드가 모두 일치하면
  실험 결과를 `RESEARCH_WITH_KNOWN_ABSTENTIONS`로 보고하고 실행
  자체의 실패로 처리하지 않는다. **47/48 채점과 1건 보류를 그대로 공개**한다.
  다른 문항/사유가 보류되면 `INCOMPLETE_BASELINE`로 실패해야 한다.
- 이전 Run의 1,718 PASS는 **이 신규 코드의 검증 증거가 아니다**.
  전체 pytest 및 선택 연구 실험 재실행 전 S7 Claim 정확도나 재현성을
  통과했다고 주장하지 않는다. PR Draft, 운영 배포 금지,
  `score_admission=DISABLED` 유지.

### 검증 명령

```bash
python3 -B -m pytest -q \
  tests/test_registry_surface_recall_audit.py \
  tests/test_claim_alignment_s7_experiment.py

python3 -B scripts/evaluate_claim_alignment_s7.py \
  --output /tmp/s7_registry_surface_research_new.json
```

실제 GitHub에서는 `validation` 워크플로를 수동 실행하면서
`run_s7_experiment=true`를 선택한다. 새 결과의
`registry_literal_candidate_count`, `registry_literal_disposition_counts`,
`baseline_abstention_count`, `expected_policy_abstention_count`,
`unexpected_baseline_failure_count`를 함께 확인한다. 다른 오류가 0이어도
새 **literal 리뷰 후보는 인간 판정 없이는 정답/채점 근거로 승격 금지**.

## 1. 실험 질문

`REVIEW_POTENTIAL_RECALL_MISS`는 **누락 가능성**이다. 기존 채점기가
`MISSING/PARTIAL/UNKNOWN`으로 본 Fact를 `EXACT_RELATION`이 찾아냈더라도
그 문장이 실제로 해당 기술적 관계·조건·문맥을 충족한다는 증거는 아니다.

따라서 다음을 별도로 측정한다.

1. **문항 단위 baseline:** 기존 전문가 Golden의 점수 범위·false pass·finding과,
   기존 결정론적 채점기의 OFF 결과를 대조한다.
2. **Claim 단위 정확도:** 독립 리뷰어가 원문 span과 승인 Fact 관계를 대조해
   개별 후보를 `CREDITABLE/NOT_CREDITABLE/UNRESOLVED`로 판정한다.
3. **안전성:** 인용된 오류/부정/조건 누락/절대 양화사, 기존 WRONG·Fatal,
   scope 보류·기계 계약 불일치를 새 점수 근거로 사용하지 않는다.

## 2. 확인된 기존 데이터의 범위

`calibration/expert_accuracy_golden.jsonl`의 2026-11-14 점검 결과:
**48건** (reviewed 45, adjudicated 3), **31개 서로 다른 Topic ID**,
**141개의 문항 수준 demand 라벨**.

| Question Type | 사례 수 |
| --- | ---: |
| IMPLEMENTATION_EVALUATION | 16 |
| COMPARE_SELECTION | 6 |
| DIAGNOSIS_ACTION | 6 |
| PRINCIPLE_INTERPRETATION | 11 |
| CALC_DESIGN | 9 |

**중요:** 기존 `labels.demands[].demand_id`는 Topic Pack의
`Fact Anchor ID`와 동일하다는 보장이 없다. 복합 요구는 여러 Fact를
묶는다. 기존 Golden의 `present/partial/wrong/missing`을 특정 Fact의
자동 정답 라벨로 변환하거나 문자열 유사도로 매핑하는 행위는 금지한다.

이 데이터는 **문항 단위 기준선**을 평가하는 용도이다.
Claim별 참/거짓/조건충족 라벨은 별도 독립 검토가 필요하다.
이 48건이 모든 과목의 품질을 대표한다고 주장하지 않는다.

## 3. 현재 구현 범위

- `grading/quality/claim_alignment_s7_benchmark.py`
  - source answer SHA, question SHA, alignment fingerprint, Topic/Fact/Claim ID,
    source span을 결박한 review candidate ID 생성
  - 승인 Registry 기반 EXACT + 기존 MISSING/PARTIAL/UNKNOWN만 검토 후보
  - 리뷰 증거(상태·방법·검토자·일시·경로) 검증, 중복/변조/기준 변경 차단
  - 무라벨은 무라벨로, 불일치·불인정은 별도 집계
  - `score_admission=DISABLED`, `score_effect=none` 고정
- `scripts/evaluate_claim_alignment_s7.py`
  - Reviewed/adjudicated Golden만 사용, 기존 OFF grade 재현
  - 동일 질문·답안·Topic 범위로 **새 Claim Alignment 계산**
  - case-level `measure_accuracy`와 claim-level 후보/독립 검토 결과 분리
  - 원문 답안은 기록하지 않으며, 결과는 저장소 밖의 절대 경로에만
    신규 생성(0600, 덮어쓰기 거부). 실패는 비식별 오류 유형만 기록
  - 일부 사례 실패 시 `INCOMPLETE_BASELINE`로 보고
- `.github/workflows/validation.yml`은 수동 입력
  `run_s7_experiment=true`인 경우에만 연구용 실험을 추가 수행한다.
  **S7은 새로운 배포 필수 Gate가 아니며**, 실패하더라도 기존
  `release_candidate.py validate`의 Pass/Fail 정책을 변경하지 않는다.
  외부 LLM API 키를 비활성화하고 임시 러너 경로에만 결과를 저장한다.

## 4. 실행

기존 workflow에서 브랜치 `feat/claim-alignment-verification-20261114`를
선택하고 **Run workflow → run_s7_experiment 체크**하여 실행한다.
기본값은 체크 해제이며 그 경우 기존 전체 오프라인 pytest만 수행한다.

로컬 환경에서 독립적으로 수행하려면:

```bash
python3 -B -m pytest -q \
  tests/test_claim_alignment_s7_benchmark.py \
  tests/test_claim_alignment_s7_experiment.py

python3 -B scripts/evaluate_claim_alignment_s7.py \
  --output /tmp/claim_alignment_s7_report.json
```

보고서의 `expert_accuracy_baseline`은 기존 채점 점수의 적정성이고,
`s7_independent_review`는 Claim별 별도 판정 결과이다.
`candidate_count`가 0이거나 `reviewed_candidate_count`가 0이라면
**정확도 100%가 아니다**. 아직 비교 대상 또는 라벨이 없다는 뜻이다.

## 5. 독립 리뷰 기록 방법

검토자는 `case_snapshots[].review_candidates[]`를 통해
`candidate_id`, Topic, 기존 Anchor, 승인 Fact ID와 답안 위치(offset)를
확인한다. **원문**은 공개 로그가 아니라 원본 `calibration` 사례를 통해
확인한다. 각 Fact의 물리법칙·표준·공식 문서 근거와 조건/부정/인용을
별도로 점검한다.

전용 비공개 JSONL에 **후보당 하나의 검토 기록**을 저장한다. JSONL은 JSON 객체 1개를 **한 줄**에 기록한다(아래는 가독성을 위해 줄바꿈한 예시이다).
아래 예시의 placeholder는 실제 ID/해시가 아니며 **승인 라벨이 아니다**.

```json
{
  "schema_version": "claim_alignment_s7_adjudication.v1",
  "case_id": "COPY_CASE_ID_FROM_REPORT",
  "candidate_id": "COPY_CANDIDATE_ID_FROM_REPORT",
  "answer_sha256": "COPY_ANSWER_SHA256_FROM_REPORT",
  "decision": "UNRESOLVED",
  "review_status": "draft",
  "review": {
    "reviewer": "INDEPENDENT_REVIEWER",
    "method": "expert_review",
    "reviewed_at": "2026-11-14T12:00:00+09:00",
    "evidence_path": "PRIVATE_REVIEW_EVIDENCE_REFERENCE"
  }
}
```

`decision`은 `CREDITABLE`, `NOT_CREDITABLE`, `UNRESOLVED` 중 하나.
실제로 전문가가 검토하지 않은 항목을 `reviewed`로 입력하지 않는다.
기존 사용자의 최종 승인 없는 자동 라벨 생성이나 리뷰 표식 위조는 금지한다.

```bash
python3 -B scripts/evaluate_claim_alignment_s7.py \
  --adjudications /private/s7_adjudications.jsonl \
  --output /private/s7_reviewed_report.json
```

저장소 내 JSONL 검토 기록이나 실제 개인 답안 커밋 금지.
재실행 시 기존 출력 덮어쓰기 금지.

## 6. 향후 점수 반영 검토 기준

- 독립 리뷰의 누락 후보 중 **불인정 후보(`NOT_CREDITABLE`)와
  보류(`UNRESOLVED`)를 숨기지 않고** 원인별 분석
- 여러 Topic/문제 유형에서 정답·부분정답·오답·정정/인용·조건 부족을
  동시 검증; 새 Fact/Logic/중복 점수 Owner는 생성하지 않음
- Claim 단위 라벨이 없는 범위에 대해 실험 precision을 일반화하지 않음
- 동일 baseline vs 실험안에서 A/B/C·Fatal·상한·합격 정책 불변,
  S5 focused regressions 및 S6 full pytest PASS 필요
- 독립 리뷰와 품질 측정이 끝나더라도 **별도 명시적 설계·승인·검증 없이는
  `CLAIM_ALIGNMENT_MODE=admit_verified` 등을 추가하거나 활성화하지 않음**

## 7. 검증 상태

### 2026-11-14 S7 최초 실험 실행 및 후속 진단

- [GitHub Actions #43555357559](https://github.com/now0930/prof_eng_answer/actions/runs/43555357559):
  **커밋 `9ac4504b`**에서 전체 오프라인 pytest **1,700 passed, 2 skipped**,
  `VALIDATION=PASS`를 확인.
- 선택적 S7 실험은 `INCOMPLETE_BASELINE`: 48건 중 47건 baseline 채점,
  1건 오류, Claim 누락 후보 0건, 전문가의 Claim 독립 검토 0건.
- 기존 채점기 `passing_score_allowed`가 전문가의 허용 플래그와 불일치한
  항목은 **12건**. 이는 **실제 15점 합격을 12건 잘못 승인했다는 뜻이 아니라**,
  기존 결정론적 결과의 *합격 허용/불허 표시*를 비교한 수치이다.
  `baseline_mean_out_of_range_distance=0.3157` 역시 **47건 완료한
  baseline의 평균 점수 범위 이탈**이며 S7 점수 개선 성과가 아니다.
- 최초 실행 스크립트는 비공개 JSON에만 실패 문항 ID/오류 유형을 저장하고
  Actions 로그에는 개수만 남겼다. 따라서 최초 로그만으로 실패 1건의 원인을
  확정할 수 없다.
- 후속 커밋에서 개인정보 없는 `failure_details`(`case_id/stage/error_type`),
  `fact_projection_status_counts`, `alignment_relation_counts`,
  `recall_disposition_counts`, `baseline_false_pass_case_ids`와
  **실제 `official_pass_met` 거짓 양성 사례**를 분리 출력하도록 보강했다.
  0건 후보의 원인(검증 Registry 부재/EXACT 부재/기존 SATISFIED 등)은
  해당 후속 실행 집계를 보고 판단한다.
- 선택적 S7 단계에는 `continue-on-error`가 있어 전체 Actions 화면이
  녹색이어도 연구 스크립트의 exit code 1을 숨기지 말아야 한다.
  **pytest PASS와 S7 실험 완료는 별개**이다.
- **후속 원인 분해 보강:** `baseline_failure_count`와
  `alignment_failure_count`를 별도 구분한다. 47건만 `graded_cases`에
  집계된 기존 실행은 **후보 비교 단계가 아니라**
  `fixture/deterministic_grade/gold_prediction` 중 실패했음을 의미한다.
  기존 Golden 48건의 원본 JSON 10종·nested case/질문/답안이 모두
  존재함을 GitHub 저장소 원본으로 확인했다. 그러므로 다음 실행에서
  우선 `failure_details[].stage/error_type`으로 특정한다.
- **후보 0건 분석:** 다음 실행은 `NO_SELECTED_REQUIREMENTS`,
  `NO_PROJECTED_ANCHORS`, `NO_VERIFIED_FACT_PROJECTION`,
  `NO_EXACT_RELATION`, `EXACT_WITHOUT_MISSED_RECALL`,
  `HAS_REVIEW_CANDIDATES`로 사례별 **단계별 탈락 이유**를 출력한다.
  기술적 동등성·정답 여부를 새로 추측하는 기능은 추가하지 않았다.
  승인 Registry Fact와 정확한 관계 일치가 0건일 수 있는 원인으로
  질문 Topic routing 불일치도 별도 진단한다.
- **Topic routing:** 전문가 Golden의 `topic_ids`와 결정론적 라우터
  `topic_ids`를 비교한 `routing_expected_topic_missing_case_count`
  및 공개된 Topic ID만 출력한다. Golden이 기대한 Topic이 없다고 해서
  실제 점수나 라우팅을 자동으로 바꾸지는 않는다.
- **후속 진단 커밋 전체 검증은 아직 미실행.** 통과한 이전 HEAD 결과를
  신규 HEAD에 전용하지 않는다. `admit_verified` 비활성, PR Draft,
  Fact/Topic Pack/Logic 및 운영 채점 불변.

직전 커밋 `dd8098bfb7df907a09eb3a8960a3eceeba57a027`는
[2026-11-14 GitHub Actions 실행 #43552790853](https://github.com/now0930/prof_eng_answer/actions/runs/43552790853)
에서 **1,685 passed, 2 skipped, VALIDATION=PASS**를 확인했다.

**본 S7 신규 코드·테스트·워크플로 변경분은 해당 커밋 이후 작성되어
아직 동일 Release Gate를 통과하지 않았다.** 새 브랜치 HEAD 검증 전
S7 정확도 향상이나 Ready-for-Score 상태를 주장하지 않는다.
