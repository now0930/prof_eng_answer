# 4-QType Production Golden Set

## 1. 역할

이 디렉터리는 산업계측제어기술사 채점 Bot의 4개 Canonical Question Type에 대한 Production Golden Regression source of truth를 관리한다.

Golden Set은 Topic Pack 전체를 복제하는 문제은행이 아니다. Router, Question Demand, A/B/C/D/E score ownership, Fact Dependency, Originality scope, Feedback scope가 기존 정상 동작을 유지하는지 검증하는 대표 회귀 기준집이다.

## 2. 기준선

- 기능 안정 기준선: `49ac8e220404d9e9d277b601c21d21930b38d42a`
- G0 공통 계약 작성 기준: `c8b13cac1a8918d8079f44ac1f5afe6854aea0a6`
- G0 상태: `COMMON_CONTRACT`
- 실제 Golden Case 작성: G0 merge/push 이후 A~D 병렬 Lane에서 수행
- Regression Runner: Lane E에서 수행

## 3. Canonical QType / Lane

| Lane | Question Type | 소유 Case 파일 |
|---|---|---|
| A | `PRINCIPLE_INTERPRETATION` | `cases/principle_interpretation.json` |
| B | `COMPARE_SELECTION` | `cases/compare_selection.json` |
| C | `DIAGNOSIS_ACTION` | `cases/diagnosis_action.json` |
| D | `IMPLEMENTATION_EVALUATION` | `cases/implementation_evaluation.json` |
| E | Regression Runner | Case 파일 수정 금지 |

A~D는 각각 LOW / PASS / HIGH 한 건씩 총 3 Case를 작성한다.

## 4. Golden v1 작성 원칙

Golden v1에서는 신규 Topic을 동시에 만들지 않는다. 반드시 이미 검증된 Topic Pack을 사용한다.

Golden 실패가 신규 Topic 결함인지 채점 Architecture 결함인지 섞이지 않도록 하기 위함이다. 각 QType에서 가능하면 서로 다른 안정 Topic을 선택한다.

## 5. Answer Level 계약

### LOW

- 공식 합격선 미만 대표
- `expected.total_range.max < 15.0`

### PASS

- 공식 합격선 이상, 고득점 기준 미만 대표
- `expected.total_range.min >= 15.0`
- `expected.total_range.max < 20.0`

### HIGH

- 고득점 기준 이상 대표
- `expected.total_range.min >= 20.0`
- `expected.total_range.max <= 25.0`

점수는 exact number가 아니라 Case별 허용 range로 관리한다.

## 6. Deterministic invariant

반복 실행에서 가능한 한 고정한다.

- Question Type
- Question Demand
- Expected Topic
- Routing Mode
- Evidence Scope
- Critical Fact expectation
- Fatal Logic expectation
- Feedback Scope

LLM 문장의 exact text equality는 요구하지 않는다. 초기 총점 반복 편차 목표는 ±0.5점이다.

## 7. Case ID

```text
QG-<QTYPE>-<LEVEL>-<NN>
```

Short code:

- `PI`: PRINCIPLE_INTERPRETATION
- `CS`: COMPARE_SELECTION
- `DA`: DIAGNOSIS_ACTION
- `IE`: IMPLEMENTATION_EVALUATION

## 8. Validation

G0 / 개별 Lane:

```bash
python3 scripts/validate_qtype_golden_set.py
python3 -m unittest scripts.test_qtype_golden_contract
```

특정 Lane:

```bash
python3 scripts/validate_qtype_golden_set.py --qtype PRINCIPLE_INTERPRETATION
```

통합 후 12 Case 완성 gate:

```bash
python3 scripts/validate_qtype_golden_set.py --require-complete
```

## 9. Shared-file ownership

A~E 병렬 Lane에서는 다음 shared 파일을 수정하지 않는다.

- `calibration/qtype_golden/README.md`
- `calibration/qtype_golden/golden_case.schema.json`
- `calibration/qtype_golden/manifest.json`
- `scripts/validate_qtype_golden_set.py`
- `scripts/test_qtype_golden_contract.py`
- `scripts/validate_release.sh`
- `docs/TOPIC_ROUTER.md`

shared 변경은 Lane 통합 후 integration 단계에서만 수행한다.

## 10. Release 연결

G0에서는 `scripts/validate_release.sh`에 `--require-complete`를 아직 등록하지 않는다.

12 Case와 Runner가 모두 통합된 후 integration 단계에서 complete gate를 release validation에 연결한다.
