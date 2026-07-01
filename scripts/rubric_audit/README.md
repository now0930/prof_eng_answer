# Rubric Audit Tools

이 디렉터리는 산업계측제어기술사 채점 Bot의 Rubric 품질 검증과 Model Answer 관계 검증 도구를 모아둔다.

## 1. Main entry point

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

## 2. Audit gate

운영 통과 기준:

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```

일반 `MINOR`는 advisory로 유지할 수 있다. 일반 `MINOR`를 0으로 만들기 위해 Model Answer를 과도하게 늘리거나 validator에 과적합하지 않는다.

## 3. Files

| 파일 | 역할 |
|---|---|
| `run_rubric_audit.py` | 전체 audit 진입점, summary report 생성 |
| `analyze_model_answer_relationship_minors.py` | relationship MINOR를 P1/P2/P3로 분류 |
| `export_p2_model_answer_repair_context.py` | P2 repair context 추출 |
| `export_remaining_p2_coverage_context.py` | 남은 coverage 계열 P2 context 추출 |
| `export_remaining_p2_order_context.py` | 남은 order/weak 계열 P2 context 추출 |

## 4. Generated reports

```text
reports/rubric_audit_summary.md
reports/model_answer_relationship_validation.csv
reports/model_answer_relationship_validation.md
reports/model_answer_relationship_minor_analysis.csv
reports/model_answer_relationship_minor_analysis.md
reports/model_answer_relationship_priority_minors.md
reports/fact_anchor_quality_audit.csv
reports/fact_anchor_quality_audit.md
```

## 5. 운영 원칙

1. `MAJOR`는 반드시 0이어야 한다.
2. `priority MINOR`는 운영 전 0이어야 한다.
3. 일반 `MINOR`는 advisory로 유지할 수 있다.
4. validator 점수 맞추기보다 답안 구조 안정성과 채점 기준 일관성을 우선한다.
5. 실험성 패치 스크립트는 `scripts/experiments/`에 격리한다.

## 6. Commit 전 권장 검증

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/rubric_audit/run_rubric_audit.py
python3 scripts/rubric_manager.py validate-all
git diff --check
git status --short
```
