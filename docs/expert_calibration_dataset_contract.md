# Expert Calibration Dataset Contract

## 1. 목적

이 계약은 채점 모델 점수와 전문가 채점 결과를 오프라인에서 비교하기 위한 데이터 형식을 정의한다.

현재 구조화된 전문가 채점 라벨은 없다. 따라서 이 기능은 운영 점수를 변경하지 않는다.

- `production_calibration_enabled = false`
- `calibration_ready = false`
- `score_effect = none`
- `direct_score_application = false`

## 2. 구성

- 데이터 계약: `expert_calibration_dataset.py`
- 검증 명령: `scripts/validate_expert_calibration_dataset.py`
- 보조 Schema: `schemas/expert_calibration_record_v1.schema.json`

Python 데이터 계약을 최종 검증 기준으로 사용한다.

## 3. 저장 형식

UTF-8 JSONL 형식을 사용한다.

한 줄에는 하나의 `expert_calibration_record_v1` 객체만 저장한다.

전문가 라벨은 운영 세션과 분리한다. `data/sessions` 아래에는 저장할 수 없다.

## 4. 검증 명령

초안과 검토 완료 레코드를 모두 검증한다.

```bash
python3 scripts/validate_expert_calibration_dataset.py DATASET.jsonl
```

검토 완료 레코드만 허용한다.

```bash
python3 scripts/validate_expert_calibration_dataset.py \
    DATASET.jsonl \
    --require-finalized
```

## 5. Identity 계약

다음 값은 `grading_identity.py`와 같은 정규화 규칙으로 검증한다.

- `question_hash`: 문제 본문 identity
- `submission_hash`: 문제와 답안 identity
- `record_hash`: 전체 전문가 레코드 identity

동일한 `submission_hash`의 중복 레코드는 허용하지 않는다.

같은 문제의 서로 다른 답안은 각각 별도 레코드로 저장할 수 있다.

## 6. 점수 계약

| 레이어 | 최대점수 |
|---|---:|
| A | 3 |
| B | 6 |
| C | 8 |
| D | 6 |
| E | 2 |

최종 전문가 레코드의 `expert_total_score`는 A/B/C/D/E 합계와 일치해야 한다.

`model_total_score`는 cap 또는 reconcile 결과로 breakdown 합계보다 작을 수 있다. breakdown 합계보다 클 수는 없다.

## 7. 검토 상태

- `draft`: 전문가 점수 미입력
- `reviewed`: 전문가 검토 완료
- `adjudicated`: 복수 의견 조정 완료
- `excluded`: 분석 대상에서 제외

`reviewed`와 `adjudicated` 상태에는 다음 정보가 필요하다.

- 전문가 총점
- 전문가 A/B/C/D/E 점수
- reviewer ID
- timezone을 포함한 검토 시각
- 검토 방법

## 8. 데이터 분리

`deterministic_dataset_split()`은 `submission_hash`를 기준으로 train과 holdout을 안정적으로 구분한다.

동일 제출물이 두 집합에 동시에 포함되면 안 된다.

## 9. 운영 적용 조건

다음 조건을 충족하기 전에는 production 점수 보정을 구현하지 않는다.

1. 충분한 전문가 라벨 수
2. 독립 holdout 확보
3. reviewer 간 일치도 분석
4. Topic별 잔차 분석
5. 문제유형별 잔차 분석
6. 점수대별 오차 분석
7. 합격선 불일치 분석
8. versioned calibration artifact
9. rollback 경로

Logic Check와 Formula Check 결과는 독립 진단 근거이다. 전문가 점수를 대신하지 않으며 직접 점수 보정에 사용하지 않는다.
