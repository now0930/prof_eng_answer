# Rubric Audit Tools

이 디렉토리는 산업계측제어기술사 채점 Bot의 rubric 품질 검증과 model answer 관계 검증을 위한 audit 도구를 모아둔다.

## Main entry point

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

## Audit gate

운영 통과 기준은 다음과 같다.

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```

일반 `MINOR`는 모두 제거하지 않는다. 일반 `MINOR`는 advisory로 유지하며, `priority MINOR`가 0이면 운영상 통과로 본다.

## Files

```text
run_rubric_audit.py
  - 전체 audit 진입점
  - audit_rubric_quality() 함수 제공
  - reports/rubric_audit_summary.md 생성

analyze_model_answer_relationship_minors.py
  - relationship MINOR를 P1/P2/P3로 분류
  - reports/model_answer_relationship_minor_analysis.csv 생성

export_p2_model_answer_repair_context.py
  - P2 repair context 추출

export_remaining_p2_coverage_context.py
  - 남은 coverage 계열 P2 context 추출

export_remaining_p2_order_context.py
  - 남은 order/weak 계열 P2 context 추출
```

## Why this exists

이 audit workflow는 다음 원칙을 따른다.

1. `MAJOR`는 반드시 0이어야 한다.
2. `priority MINOR`는 운영 전 반드시 0이어야 한다.
3. 일반 `MINOR`를 0으로 만들기 위해 model answer를 과도하게 늘리지 않는다.
4. validator 점수 맞추기보다 답안 구조 안정성과 채점 기준 일관성을 우선한다.
5. 실험성 패치 스크립트는 `scripts/experiments/`에 격리한다.

## Generated reports

대표 산출물은 다음과 같다.

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
