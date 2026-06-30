#!/usr/bin/env python3
"""
Validate formal consistency between Model Answer Bank and Fact Anchor Bank.

This script does not judge technical correctness. It checks that both rubric
files can be parsed, have the expected top-level collections, and share the
same topic_id set.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
DEFAULT_FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

VALID_QUESTION_TYPES = {
    "PRINCIPLE_INTERPRETATION",
    "DIAGNOSIS_ACTION",
    "COMPARE_SELECTION",
    "IMPLEMENTATION_EVALUATION",
}

TOPIC_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
ANCHOR_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")

MODEL_REQUIRED_FIELDS = [
    "id",
    "topic_id",
    "question_type",
    "title",
    "topic_aliases",
    "question_examples",
    "expected_structure",
    "model_answer_outline",
    "high_score_features",
    "low_score_patterns",
    "field_connection_points",
    "revision_notes",
]

FACT_TOPIC_REQUIRED_FIELDS = [
    "topic_id",
    "name",
    "triggers",
    "aliases",
    "anchors",
]

ANCHOR_REQUIRED_FIELDS = [
    "id",
    "name",
    "expected",
    "core_terms",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON: {path}: {exc}")


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_string_list(value: Any, *, allow_empty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if not allow_empty and not value:
        return False
    return all(isinstance(item, str) and bool(item.strip()) for item in value)


def add_issue(bucket: list[str], message: str) -> None:
    bucket.append(message)


def validate_model_bank(model: Any) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(model, dict):
        add_issue(errors, "model bank root must be an object")
        return errors, warnings, []

    answers = model.get("answers")
    if not isinstance(answers, list):
        add_issue(errors, "model bank must contain list field: answers")
        return errors, warnings, []

    ids: list[str] = []
    topic_question_pairs: list[tuple[str, str]] = []

    for idx, item in enumerate(answers):
        loc = f"model.answers[{idx}]"
        if not isinstance(item, dict):
            add_issue(errors, f"{loc} must be an object")
            continue

        missing = [field for field in MODEL_REQUIRED_FIELDS if field not in item]
        if missing:
            add_issue(errors, f"{loc} missing fields: {missing}")

        answer_id = item.get("id")
        topic_id = item.get("topic_id")
        question_type = item.get("question_type")

        if not is_non_empty_string(answer_id):
            add_issue(errors, f"{loc}.id must be a non-empty string")
        else:
            ids.append(answer_id)

        if not is_non_empty_string(topic_id):
            add_issue(errors, f"{loc}.topic_id must be a non-empty string")
        elif not TOPIC_ID_RE.match(topic_id):
            add_issue(warnings, f"{loc}.topic_id has unusual format: {topic_id}")

        if is_non_empty_string(answer_id) and is_non_empty_string(topic_id):
            if not str(answer_id).startswith(str(topic_id)):
                add_issue(warnings, f"{loc}.id does not start with topic_id: id={answer_id}, topic_id={topic_id}")

        if question_type not in VALID_QUESTION_TYPES:
            add_issue(errors, f"{loc}.question_type invalid: {question_type}")

        if is_non_empty_string(topic_id) and is_non_empty_string(question_type):
            topic_question_pairs.append((topic_id, question_type))

        for field in ["title"]:
            if field in item and not is_non_empty_string(item[field]):
                add_issue(errors, f"{loc}.{field} must be a non-empty string")

        for field in [
            "topic_aliases",
            "question_examples",
            "expected_structure",
            "model_answer_outline",
            "high_score_features",
            "low_score_patterns",
            "field_connection_points",
            "revision_notes",
        ]:
            if field in item and not is_string_list(item[field], allow_empty=(field in {"topic_aliases", "field_connection_points"})):
                add_issue(errors, f"{loc}.{field} must be a list of strings")

        if "aliases" in item:
            add_issue(errors, f"{loc} uses aliases; use topic_aliases in model answers")

    for answer_id, count in Counter(ids).items():
        if count > 1:
            add_issue(errors, f"duplicate model answer id: {answer_id} count={count}")

    for pair, count in Counter(topic_question_pairs).items():
        if count > 1:
            topic_id, question_type = pair
            add_issue(warnings, f"duplicate topic_id/question_type pair: {topic_id}/{question_type} count={count}")

    return errors, warnings, answers


def validate_fact_bank(fact: Any) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(fact, dict):
        add_issue(errors, "fact anchor bank root must be an object")
        return errors, warnings, []

    topics = fact.get("topics")
    if not isinstance(topics, list):
        add_issue(errors, "fact anchor bank must contain list field: topics")
        return errors, warnings, []

    topic_ids: list[str] = []

    for idx, item in enumerate(topics):
        loc = f"fact.topics[{idx}]"
        if not isinstance(item, dict):
            add_issue(errors, f"{loc} must be an object")
            continue

        missing = [field for field in FACT_TOPIC_REQUIRED_FIELDS if field not in item]
        if missing:
            add_issue(errors, f"{loc} missing fields: {missing}")

        topic_id = item.get("topic_id")
        if not is_non_empty_string(topic_id):
            add_issue(errors, f"{loc}.topic_id must be a non-empty string")
        else:
            topic_ids.append(topic_id)
            if not TOPIC_ID_RE.match(topic_id):
                add_issue(warnings, f"{loc}.topic_id has unusual format: {topic_id}")

        if "name" in item and not is_non_empty_string(item["name"]):
            add_issue(errors, f"{loc}.name must be a non-empty string")

        for field in ["triggers", "aliases"]:
            if field in item and not is_string_list(item[field], allow_empty=(field == "aliases")):
                add_issue(errors, f"{loc}.{field} must be a list of strings")

        anchors = item.get("anchors")
        if not isinstance(anchors, list) or not anchors:
            add_issue(errors, f"{loc}.anchors must be a non-empty list")
            continue

        anchor_ids: list[str] = []
        for aidx, anchor in enumerate(anchors):
            aloc = f"{loc}.anchors[{aidx}]"
            if not isinstance(anchor, dict):
                add_issue(errors, f"{aloc} must be an object")
                continue

            missing = [field for field in ANCHOR_REQUIRED_FIELDS if field not in anchor]
            if missing:
                add_issue(errors, f"{aloc} missing fields: {missing}")

            anchor_id = anchor.get("id")
            if not is_non_empty_string(anchor_id):
                add_issue(errors, f"{aloc}.id must be a non-empty string")
            else:
                anchor_ids.append(anchor_id)
                if not ANCHOR_ID_RE.match(anchor_id):
                    add_issue(warnings, f"{aloc}.id has unusual format: {anchor_id}")

            for field in ["name", "expected"]:
                if field in anchor and not is_non_empty_string(anchor[field]):
                    add_issue(errors, f"{aloc}.{field} must be a non-empty string")

            for field in ["core_terms", "support_terms"]:
                if field in anchor and not is_string_list(anchor[field], allow_empty=(field == "support_terms")):
                    add_issue(errors, f"{aloc}.{field} must be a list of strings")

        for anchor_id, count in Counter(anchor_ids).items():
            if count > 1:
                add_issue(errors, f"{loc} duplicate anchor id: {anchor_id} count={count}")

    for topic_id, count in Counter(topic_ids).items():
        if count > 1:
            add_issue(errors, f"duplicate fact topic_id: {topic_id} count={count}")

    return errors, warnings, topics


def validate_cross_consistency(
    answers: list[dict[str, Any]],
    topics: list[dict[str, Any]],
    *,
    allow_extra_fact_topics: bool,
) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    model_topic_to_answers: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for answer in answers:
        topic_id = answer.get("topic_id")
        if is_non_empty_string(topic_id):
            model_topic_to_answers[topic_id].append(answer)

    fact_topic_to_item: dict[str, dict[str, Any]] = {}
    for topic in topics:
        topic_id = topic.get("topic_id")
        if is_non_empty_string(topic_id):
            fact_topic_to_item[topic_id] = topic

    model_topics = set(model_topic_to_answers)
    fact_topics = set(fact_topic_to_item)

    for topic_id in sorted(model_topics - fact_topics):
        add_issue(errors, f"model topic missing in fact anchors: {topic_id}")

    for topic_id in sorted(fact_topics - model_topics):
        message = f"fact topic has no model answer: {topic_id}"
        if allow_extra_fact_topics:
            add_issue(warnings, message)
        else:
            add_issue(errors, message)

    for topic_id in sorted(model_topics & fact_topics):
        model_answers = model_topic_to_answers[topic_id]
        fact_topic = fact_topic_to_item[topic_id]
        anchors = fact_topic.get("anchors", [])

        if len(model_answers) > 1:
            qtypes = sorted(str(a.get("question_type")) for a in model_answers)
            if len(qtypes) != len(set(qtypes)):
                add_issue(warnings, f"topic has duplicate question_type entries: {topic_id}: {qtypes}")

        combined_model_terms: set[str] = set()
        for answer in model_answers:
            for field in ["title", "topic_aliases", "question_examples"]:
                value = answer.get(field)
                if isinstance(value, str):
                    combined_model_terms.add(value.lower())
                elif isinstance(value, list):
                    combined_model_terms.update(str(x).lower() for x in value if isinstance(x, str))

        fact_terms: set[str] = set()
        for field in ["name", "triggers", "aliases"]:
            value = fact_topic.get(field)
            if isinstance(value, str):
                fact_terms.add(value.lower())
            elif isinstance(value, list):
                fact_terms.update(str(x).lower() for x in value if isinstance(x, str))

        if combined_model_terms and fact_terms:
            model_blob = " ".join(sorted(combined_model_terms))
            fact_blob = " ".join(sorted(fact_terms))
            topic_words = [w for w in topic_id.split("_") if len(w) >= 3]
            has_overlap = any(w.lower() in model_blob and w.lower() in fact_blob for w in topic_words)
            has_alias_overlap = bool(combined_model_terms & fact_terms)
            if not has_overlap and not has_alias_overlap:
                add_issue(warnings, f"weak alias/trigger overlap between model and fact topic: {topic_id}")

        if isinstance(anchors, list) and len(anchors) < 3:
            add_issue(warnings, f"topic has fewer than 3 fact anchors: {topic_id} count={len(anchors)}")

    summary = {
        "model_answers": len(answers),
        "fact_topics": len(topics),
        "model_topics": len(model_topics),
        "shared_topics": len(model_topics & fact_topics),
        "model_only_topics": sorted(model_topics - fact_topics),
        "fact_only_topics": sorted(fact_topics - model_topics),
        "answers_per_topic": {key: len(value) for key, value in sorted(model_topic_to_answers.items())},
        "anchors_per_topic": {
            key: len(value.get("anchors", []))
            for key, value in sorted(fact_topic_to_item.items())
        },
    }

    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Model Answer / Fact Anchor topic consistency.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH, help="model answer bank JSON path")
    parser.add_argument("--fact", type=Path, default=DEFAULT_FACT_PATH, help="fact anchor bank JSON path")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failure")
    parser.add_argument("--allow-extra-fact-topics", action="store_true", help="warn instead of failing when a fact topic has no model answer")
    parser.add_argument("--json", action="store_true", help="print machine-readable result")
    args = parser.parse_args(argv)

    model = load_json(args.model)
    fact = load_json(args.fact)

    errors: list[str] = []
    warnings: list[str] = []

    model_errors, model_warnings, answers = validate_model_bank(model)
    fact_errors, fact_warnings, topics = validate_fact_bank(fact)
    cross_errors, cross_warnings, summary = validate_cross_consistency(
        answers,
        topics,
        allow_extra_fact_topics=args.allow_extra_fact_topics,
    )

    errors.extend(model_errors)
    errors.extend(fact_errors)
    errors.extend(cross_errors)
    warnings.extend(model_warnings)
    warnings.extend(fact_warnings)
    warnings.extend(cross_warnings)

    ok = not errors and (not warnings or not args.strict)

    if args.json:
        print(json.dumps({"ok": ok, "errors": errors, "warnings": warnings, "summary": summary}, ensure_ascii=False, indent=2))
    else:
        print("VALID" if ok else "INVALID")
        print(f"model answers: {summary['model_answers']}")
        print(f"model topics: {summary['model_topics']}")
        print(f"fact topics: {summary['fact_topics']}")
        print(f"shared topics: {summary['shared_topics']}")

        if errors:
            print("")
            print("ERRORS")
            for issue in errors:
                print("- " + issue)

        if warnings:
            print("")
            print("WARNINGS")
            for issue in warnings:
                print("- " + issue)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
