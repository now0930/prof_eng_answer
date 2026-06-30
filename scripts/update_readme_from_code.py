#!/usr/bin/env python3
"""Generate README.md from current code and Rubric Bank JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
QTYPE_PATH = ROOT / "rubrics/question_types/default.json"
README_PATH = ROOT / "README.md"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def question_types() -> list[tuple[str, str]]:
    data = load_json(QTYPE_PATH, {"types": []})
    types = data.get("types", [])
    result: list[tuple[str, str]] = []

    if isinstance(types, dict):
        iterable = types.values()
    else:
        iterable = types

    for item in iterable:
        if not isinstance(item, dict):
            continue
        type_id = item.get("id") or item.get("type") or item.get("name")
        label = item.get("name") or item.get("label") or item.get("description") or ""
        if isinstance(type_id, str) and type_id:
            result.append((type_id, str(label)))

    return result


def existing_docs() -> list[str]:
    candidates = [
        "docs/README.md",
        "docs/operation_runbook.md",
        "docs/docker_compose_usage.md",
        "docs/grading_architecture.md",
        "docs/question_type_taxonomy.md",
        "docs/difficulty_and_selection_strategy.md",
        "docs/llm_provider.md",
        "docs/rubric_authoring_guide.md",
        "docs/model_answer_generator_prompt.md",
        "docs/fact_anchor_generator_prompt.md",
        "docs/topic_importance_generator_prompt.md",
    ]
    return [item for item in candidates if (ROOT / item).exists()]


def render_question_types(items: list[tuple[str, str]]) -> str:
    if not items:
        return "- 현재 question type 파일을 확인해야 한다."
    lines = []
    for type_id, label in items:
        if label and label != type_id:
            lines.append(f"- `{type_id}`: {label}")
        else:
            lines.append(f"- `{type_id}`")
    return "\n".join(lines)


def render_docs(items: list[str]) -> str:
    if not items:
        return "- docs 문서 없음"
    return "\n".join(f"- `{item}`" for item in items)


def generate() -> str:
    model = load_json(MODEL_PATH, {"answers": []})
    fact = load_json(FACT_PATH, {"topics": []})

    answers = model.get("answers", []) if isinstance(model, dict) else []
    topics = fact.get("topics", []) if isinstance(fact, dict) else []

    model_topics = sorted(
        {
            answer.get("topic_id")
            for answer in answers
            if isinstance(answer, dict) and isinstance(answer.get("topic_id"), str)
        }
    )
    fact_topics = sorted(
        {
            topic.get("topic_id")
            for topic in topics
            if isinstance(topic, dict) and isinstance(topic.get("topic_id"), str)
        }
    )

    qtype_block = render_question_types(question_types())
    doc_block = render_docs(existing_docs())
    shared_count = len(set(model_topics) & set(fact_topics))

    return f"""# prof_eng_answer

산업계측제어기술사 답안 평가와 Rubric Bank 관리를 위한 프로젝트이다.

이 문서는 현재 repository의 코드와 JSON 파일을 기준으로 생성되었다.

## 핵심 파일

| 구분 | 경로 | 역할 |
|---|---|---|
| Model Answer Bank | `rubrics/model_answers/industrial_instrumentation_control.json` | 모범답안 구조, 고득점 요소, 저득점 패턴, 현장 연결 포인트 |
| Fact Anchor Bank | `rubrics/fact_anchors/industrial_instrumentation_control.json` | topic별 핵심 fact, core terms, support terms |
| Question Type Profile | `rubrics/question_types/default.json` | 문제 유형 분류 기준 |
| Rubric Manager | `scripts/rubric_manager.py` | 전체 검증 실행 진입점 |
| Model/Fact Consistency Validator | `scripts/validate_model_fact_consistency.py` | 두 Bank의 topic 정합성 검증 |

## 현재 Bank 규모

- model answers: {len(answers)}
- model topics: {len(model_topics)}
- fact topics: {len(fact_topics)}
- shared topics: {shared_count}

## 현재 Question Type

{qtype_block}

신규 모범답안은 위 question type 중 하나를 사용해야 한다. 오래된 legacy type은 신규 항목에 사용하지 않는다.

## Model Answer Bank 수정 방법

대상 파일:

```bash
rubrics/model_answers/industrial_instrumentation_control.json
```

각 answer는 최소한 다음 필드를 갖는다.

```text
id
topic_id
question_type
title
question_examples
topic_aliases
expected_structure
model_answer_outline
high_score_features
low_score_patterns
field_connection_points
revision_notes
```

### 기존 모범답안 수정

1. `topic_id`로 기존 answer를 찾는다.
2. `question_examples`, `expected_structure`, `model_answer_outline`, `high_score_features`, `low_score_patterns`, `field_connection_points`를 수정한다.
3. factual 내용은 반드시 Fact Anchor와 모순되지 않게 한다.
4. 수정 후 검증한다.

```bash
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

### 신규 모범답안 추가

1. 새 `topic_id`를 정한다.
2. Model Answer Bank에 answer를 추가한다.
3. 같은 `topic_id`가 Fact Anchor Bank에도 있어야 한다.
4. 같은 topic에 여러 question type의 모범답안이 필요한 경우 model answer는 여러 개 둘 수 있다.
5. Fact Anchor는 topic별 fact 기준이므로 보통 topic당 하나를 둔다.

### 모범답안 삭제

1. 해당 `id`의 answer를 삭제한다.
2. 같은 `topic_id`를 쓰는 다른 model answer가 남아 있는지 확인한다.
3. 다른 model answer가 남아 있으면 Fact Anchor는 유지한다.
4. 해당 topic의 model answer가 모두 없어졌다면 Fact Anchor 삭제 여부를 검토한다.
5. 검증한다.

## Fact Anchor Bank 수정 방법

대상 파일:

```bash
rubrics/fact_anchors/industrial_instrumentation_control.json
```

각 topic은 최소한 다음 필드를 갖는다.

```text
topic_id
name
triggers
aliases
anchors
```

각 anchor는 최소한 다음 필드를 갖는다.

```text
id
name
expected
core_terms
support_terms
```

### 기존 Fact Anchor 수정

1. `topic_id`로 topic을 찾는다.
2. `anchors[].expected`에 반드시 알아야 할 fact를 쓴다.
3. `core_terms`에는 채점에서 핵심으로 볼 용어를 둔다.
4. `support_terms`에는 보조 용어와 현장 표현을 둔다.
5. Model Answer의 설명과 충돌하지 않게 맞춘다.

### 신규 Fact Anchor 추가

1. Model Answer Bank에 추가할 `topic_id`와 동일한 `topic_id`를 사용한다.
2. topic의 `name`, `triggers`, `aliases`를 작성한다.
3. 최소 1개 이상의 anchor를 작성한다.
4. 가능하면 주요 fact 기준을 3~5개 anchor로 나눈다.

### Fact Anchor 삭제

1. 먼저 같은 `topic_id`를 사용하는 model answer가 남아 있는지 확인한다.
2. model answer가 남아 있으면 삭제하면 안 된다.
3. model answer가 모두 삭제된 topic만 Fact Anchor 삭제를 검토한다.

## Model Answer와 Fact Anchor의 topic 관계

핵심 원칙은 다음이다.

```text
Model Answer의 모든 topic_id는 Fact Anchor Bank에 존재해야 한다.
Fact Anchor는 topic별 fact 기준이다.
Model Answer는 topic_id + question_type별 답안 구조이다.
하나의 Fact Anchor topic을 여러 Model Answer가 공유할 수 있다.
```

허용되는 관계:

```text
fact topic 1개 : model answer 1개
fact topic 1개 : model answer 여러 개
```

허용하지 않는 관계:

```text
model answer topic_id가 fact anchor에 없음
fact anchor topic_id 중복
model answer id 중복
빈 anchors
빈 model_answer_outline
```

## Review Design Importer 사용

batch별 검토 markdown은 보통 아래에 둔다.

```bash
wordpress_docs/review_designs/
```

실행 예:

```bash
python3 scripts/import_review_design.py wordpress_docs/review_designs/batch_014_design_1topic.md
```

주의 사항:

- importer 내부에 topic별 `META`를 누적하지 않는다.
- 한글 metadata는 markdown 또는 JSON Bank에 둔다.
- importer는 변환 도구이며 기술적 사실 검증 도구가 아니다.

## 검증 명령

기본 검증:

```bash
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

commit 전 검증:

```bash
git diff --check
python3 -m py_compile scripts/validate_model_fact_consistency.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

## 문서 구조

현재 활성 문서:

{doc_block}

오래된 문서는 삭제하지 않고 `docs/archive/` 아래로 이동한다.

## 문서 재생성

현재 코드와 JSON 기준으로 README를 재생성하려면 다음을 실행한다.

```bash
python3 scripts/update_readme_from_code.py --check
python3 scripts/update_readme_from_code.py --write
```

오래된 문서 정리:

```bash
python3 scripts/cleanup_stale_docs.py --dry-run
python3 scripts/cleanup_stale_docs.py --apply
```
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()

    text = generate()

    if args.check:
        old = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
        if old == text:
            print("README.md is up to date")
        else:
            print("README.md would be updated")
        return 0

    README_PATH.write_text(text, encoding="utf-8")
    print("wrote: README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
