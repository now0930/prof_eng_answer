# S7 — 독립 Claim 정확도 평가 및 검토 절차 (점수 반영 금지)

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
- **후속 진단 커밋 전체 검증은 아직 미실행.** 통과한 이전 HEAD 결과를
  신규 HEAD에 전용하지 않는다. `admit_verified` 비활성, PR Draft,
  Fact/Topic Pack/Logic 및 운영 채점 불변.

직전 커밋 `dd8098bfb7df907a09eb3a8960a3eceeba57a027`는
[2026-11-14 GitHub Actions 실행 #43552790853](https://github.com/now0930/prof_eng_answer/actions/runs/43552790853)
에서 **1,685 passed, 2 skipped, VALIDATION=PASS**를 확인했다.

**본 S7 신규 코드·테스트·워크플로 변경분은 해당 커밋 이후 작성되어
아직 동일 Release Gate를 통과하지 않았다.** 새 브랜치 HEAD 검증 전
S7 정확도 향상이나 Ready-for-Score 상태를 주장하지 않는다.
