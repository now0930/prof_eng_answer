#!/usr/bin/env python3
"""Validate formal consistency between Model Answer Bank and Fact Anchor Bank.

This script checks:
- JSON files can be parsed.
- Required top-level lists exist.
- Model answer entries have required fields.
- Fact anchor topic entries have required fields.
- Every model answer topic_id exists in fact anchors.
- Fact anchor topic_id values are unique.
- Model answer id values are unique.

It intentionally validates structure, not technical correctness.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"


MODEL_REQUIRED_LIST_FIELDS = [
    "question_examples",
    "expected_structure",
    "model_answer_outline",
    "high_score_features",
    "low_score_patterns",
    "field_connection_points",
    "revision_notes",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"INVALID: cannot read {path.relative_to(ROOT)}: {exc}")
        sys.exit(1)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def validate_model_answers(model: dict[str, Any], errors: list[str], warnings: list[str]) -> tuple[list[str], list[str]]:
    answers = model.get("answers")
    if not isinstance(answers, list):
        errors.append("model_answers JSON must contain list field: answers")
        return [], []

    model_ids: list[str] = []
    topic_ids: list[str] = []

    for index, answer in enumerate(answers):
        prefix = f"model.answers[{index}]"
        if not isinstance(answer, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        answer_id = answer.get("id")
        topic_id = answer.get("topic_id")
        question_type = answer.get("question_type")

        if nonempty_string(answer_id):
            model_ids.append(answer_id)
        else:
            errors.append(f"{prefix}: missing id")

        if nonempty_string(topic_id):
            topic_ids.append(topic_id)
        else:
            errors.append(f"{prefix}: missing topic_id")

        if not nonempty_string(question_type):
            errors.append(f"{prefix}: missing question_type")

        if not nonempty_string(answer.get("title")):
            warnings.append(f"{prefix}: title is empty")

        if not isinstance(answer.get("topic_aliases", []), list):
            errors.append(f"{prefix}: topic_aliases must be a list")

        for field in MODEL_REQUIRED_LIST_FIELDS:
            if not nonempty_list(answer.get(field)):
                errors.append(f"{prefix}: {field} must be a non-empty list")

    duplicate_ids = sorted([value for value, count in Counter(model_ids).items() if count > 1])
    for answer_id in duplicate_ids:
        errors.append(f"duplicate model answer id: {answer_id}")

    duplicate_topic_question_pairs = []
    pair_values = [
        (answer.get("topic_id"), answer.get("question_type"))
        for answer in answers
        if isinstance(answer, dict)
        and nonempty_string(answer.get("topic_id"))
        and nonempty_string(answer.get("question_type"))
    ]
    pair_counts = Counter(pair_values)
    for pair, count in pair_counts.items():
        if count > 1:
            duplicate_topic_question_pairs.append(pair)

    for topic_id, question_type in duplicate_topic_question_pairs:
        errors.append(f"duplicate model answer pair: topic_id={topic_id}, question_type={question_type}")

    duplicate_topics = sorted([value for value, count in Counter(topic_ids).items() if count > 1])
    for topic_id in duplicate_topics:
        warnings.append(f"multiple model answers share topic_id: {topic_id}")

    return topic_ids, model_ids


def validate_fact_topics(fact: dict[str, Any], errors: list[str], warnings: list[str]) -> list[str]:
    topics = fact.get("topics")
    if not isinstance(topics, list):
        errors.append("fact_anchors JSON must contain list field: topics")
        return []

    topic_ids: list[str] = []

    for index, topic in enumerate(topics):
        prefix = f"fact.topics[{index}]"
        if not isinstance(topic, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        topic_id = topic.get("topic_id")
        if nonempty_string(topic_id):
            topic_ids.append(topic_id)
        else:
            errors.append(f"{prefix}: missing topic_id")

        if not nonempty_string(topic.get("name")):
            warnings.append(f"{prefix}: name is empty")

        if not isinstance(topic.get("triggers", []), list):
            errors.append(f"{prefix}: triggers must be a list")

        if not isinstance(topic.get("aliases", []), list):
            errors.append(f"{prefix}: aliases must be a list")

        anchors = topic.get("anchors")
        if not nonempty_list(anchors):
            errors.append(f"{prefix}: anchors must be a non-empty list")
            continue

        anchor_ids: list[str] = []
        for anchor_index, anchor in enumerate(anchors):
            anchor_prefix = f"{prefix}.anchors[{anchor_index}]"
            if not isinstance(anchor, dict):
                errors.append(f"{anchor_prefix}: must be an object")
                continue

            anchor_id = anchor.get("id")
            if nonempty_string(anchor_id):
                anchor_ids.append(anchor_id)
            else:
                errors.append(f"{anchor_prefix}: missing id")

            for field in ["name", "expected"]:
                if not nonempty_string(anchor.get(field)):
                    errors.append(f"{anchor_prefix}: missing {field}")

            if not nonempty_list(anchor.get("core_terms")):
                errors.append(f"{anchor_prefix}: core_terms must be a non-empty list")

            if not isinstance(anchor.get("support_terms", []), list):
                errors.append(f"{anchor_prefix}: support_terms must be a list")

        duplicate_anchor_ids = sorted([value for value, count in Counter(anchor_ids).items() if count > 1])
        for anchor_id in duplicate_anchor_ids:
            errors.append(f"{prefix}: duplicate anchor id: {anchor_id}")

    duplicate_topic_ids = sorted([value for value, count in Counter(topic_ids).items() if count > 1])
    for topic_id in duplicate_topic_ids:
        errors.append(f"duplicate fact anchor topic_id: {topic_id}")

    return topic_ids


def main() -> int:
    model = load_json(MODEL_PATH)
    fact = load_json(FACT_PATH)

    if not isinstance(model, dict):
        print("INVALID")
        print("ERROR: model answer JSON root must be an object")
        return 1

    if not isinstance(fact, dict):
        print("INVALID")
        print("ERROR: fact anchor JSON root must be an object")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    model_topic_ids, model_ids = validate_model_answers(model, errors, warnings)
    fact_topic_ids = validate_fact_topics(fact, errors, warnings)

    model_topic_set = set(model_topic_ids)
    fact_topic_set = set(fact_topic_ids)

    for topic_id in sorted(model_topic_set - fact_topic_set):
        errors.append(f"topic_id exists in model_answers but not in fact_anchors: {topic_id}")

    for topic_id in sorted(fact_topic_set - model_topic_set):
        warnings.append(f"topic_id exists in fact_anchors but has no model_answer: {topic_id}")

    if errors:
        print("INVALID")
        for error in errors:
            print("ERROR:", error)
        for warning in warnings:
            print("WARN:", warning)
        return 1

    print("VALID")
    print("model answers:", len(model.get("answers", [])))
    print("model ids:", len(set(model_ids)))
    print("model topics:", len(model_topic_set))
    print("fact topics:", len(fact_topic_set))
    print("shared topics:", len(model_topic_set & fact_topic_set))
    for warning in warnings:
        print("WARN:", warning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
