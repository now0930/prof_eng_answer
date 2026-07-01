#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"INVALID: cannot read {path}: {e}")
        sys.exit(1)

def nonempty_str(x):
    return isinstance(x, str) and bool(x.strip())

def nonempty_list(x):
    return isinstance(x, list) and len(x) > 0

def main():
    model = load_json(MODEL_PATH)
    fact = load_json(FACT_PATH)

    answers = model.get("answers")
    topics = fact.get("topics")

    errors = []
    warnings = []

    if not isinstance(answers, list):
        errors.append("model_answers JSON must contain list field: answers")
        answers = []

    if not isinstance(topics, list):
        errors.append("fact_anchors JSON must contain list field: topics")
        topics = []

    model_ids = []
    model_topics = []
    model_keys = []

    for i, a in enumerate(answers):
        p = f"model.answers[{i}]"
        if not isinstance(a, dict):
            errors.append(f"{p}: must be object")
            continue

        aid = a.get("id")
        tid = a.get("topic_id")
        qtype = a.get("question_type")
        legacy = a.get("legacy_question_type", "")

        if not nonempty_str(aid):
            errors.append(f"{p}: missing id")
        else:
            model_ids.append(aid)

        if not nonempty_str(tid):
            errors.append(f"{p}: missing topic_id")
        else:
            model_topics.append(tid)

        if not nonempty_str(qtype):
            errors.append(f"{p}: missing question_type")

        # This is the intended uniqueness rule:
        # same topic_id may have multiple current question_type entries when
        # legacy_question_type distinguishes old-style answer variants.
        if nonempty_str(tid) and nonempty_str(qtype):
            model_keys.append((tid, qtype, legacy or ""))

        for key in [
            "question_examples",
            "expected_structure",
            "model_answer_outline",
            "high_score_features",
            "low_score_patterns",
            "field_connection_points",
            "revision_notes",
        ]:
            if not nonempty_list(a.get(key)):
                errors.append(f"{p}: {key} must be non-empty list")

        if not isinstance(a.get("topic_aliases", []), list):
            errors.append(f"{p}: topic_aliases must be list")

    for value, count in Counter(model_ids).items():
        if count > 1:
            errors.append(f"duplicate model answer id: {value}")

    for key, count in Counter(model_keys).items():
        if count > 1:
            tid, qtype, legacy = key
            errors.append(
                "duplicate model answer key: "
                f"topic_id={tid}, question_type={qtype}, legacy_question_type={legacy}"
            )

    fact_topics = []
    for i, t in enumerate(topics):
        p = f"fact.topics[{i}]"
        if not isinstance(t, dict):
            errors.append(f"{p}: must be object")
            continue

        tid = t.get("topic_id")
        if not nonempty_str(tid):
            errors.append(f"{p}: missing topic_id")
        else:
            fact_topics.append(tid)

        if not nonempty_str(t.get("name")):
            errors.append(f"{p}: missing name")

        if not isinstance(t.get("triggers", []), list):
            errors.append(f"{p}: triggers must be list")

        if not isinstance(t.get("aliases", []), list):
            errors.append(f"{p}: aliases must be list")

        anchors = t.get("anchors")
        if not nonempty_list(anchors):
            errors.append(f"{p}: anchors must be non-empty list")
            continue

        anchor_ids = []
        for j, an in enumerate(anchors):
            ap = f"{p}.anchors[{j}]"
            if not isinstance(an, dict):
                errors.append(f"{ap}: must be object")
                continue

            anchor_id = an.get("id")
            if not nonempty_str(anchor_id):
                errors.append(f"{ap}: missing id")
            else:
                anchor_ids.append(anchor_id)

            for key in ["name", "expected"]:
                if not nonempty_str(an.get(key)):
                    errors.append(f"{ap}: missing {key}")

            if not nonempty_list(an.get("core_terms")):
                errors.append(f"{ap}: core_terms must be non-empty list")

            if not isinstance(an.get("support_terms", []), list):
                errors.append(f"{ap}: support_terms must be list")

        for value, count in Counter(anchor_ids).items():
            if count > 1:
                errors.append(f"{p}: duplicate anchor id {value}")

    for value, count in Counter(fact_topics).items():
        if count > 1:
            errors.append(f"duplicate fact topic_id: {value}")

    model_set = set(model_topics)
    fact_set = set(fact_topics)

    for tid in sorted(model_set - fact_set):
        errors.append(f"topic_id exists in model_answers but not in fact_anchors: {tid}")

    for tid in sorted(fact_set - model_set):
        warnings.append(f"topic_id exists in fact_anchors but has no model_answer: {tid}")

    for tid in sorted({x for x, c in Counter(model_topics).items() if c > 1}):
        warnings.append(f"multiple model answers share topic_id: {tid}")

    if errors:
        print("INVALID")
        for e in errors:
            print("ERROR:", e)
        for w in warnings:
            print("WARN:", w)
        sys.exit(1)

    print("VALID")
    print("model answers:", len(answers))
    print("model topics:", len(model_set))
    print("fact topics:", len(fact_set))
    print("shared topics:", len(model_set & fact_set))
    for w in warnings:
        print("WARN:", w)

if __name__ == "__main__":
    main()
