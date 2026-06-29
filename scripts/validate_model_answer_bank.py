import json
from pathlib import Path

BANK_PATH = Path("rubrics/model_answers/industrial_instrumentation_control.json")
QUESTION_TYPE_PATH = Path("rubrics/question_types/default.json")

REQUIRED_TOP_KEYS = ["version", "subject", "policy", "answers"]
REQUIRED_ANSWER_KEYS = [
    "id",
    "topic_id",
    "question_type",
    "title",
    "question_examples",
    "expected_structure",
    "model_answer_outline",
    "high_score_features",
    "low_score_patterns",
    "field_connection_points",
    "revision_notes"
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    errors = []

    if not BANK_PATH.exists():
        errors.append(f"missing bank file: {BANK_PATH}")
        print_errors(errors)
        raise SystemExit(1)

    data = load_json(BANK_PATH)

    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"top-level key missing: {key}")

    answers = data.get("answers", [])
    if not isinstance(answers, list) or not answers:
        errors.append("answers must be non-empty list")

    allowed_types = set()
    if QUESTION_TYPE_PATH.exists():
        qtypes = load_json(QUESTION_TYPE_PATH)
        raw_types = qtypes.get("types", [])

    if isinstance(raw_types, dict):
        allowed_types = set(raw_types.keys())
    elif isinstance(raw_types, list):
        allowed_types = {
            x.get("id")
            for x in raw_types
            if isinstance(x, dict) and x.get("id")
        }
    else:
        allowed_types = set()

    legacy_mapping = qtypes.get("legacy_mapping", {})
    if isinstance(legacy_mapping, dict):
        allowed_types.update(
            v for v in legacy_mapping.values()
            if isinstance(v, str) and v
        )

    seen_ids = set()
    seen_pair = set()

    for idx, item in enumerate(answers):
        prefix = f"answers[{idx}]"

        if not isinstance(item, dict):
            errors.append(f"{prefix}: item must be object")
            continue

        for key in REQUIRED_ANSWER_KEYS:
            if key not in item:
                errors.append(f"{prefix}: missing key: {key}")

        aid = item.get("id")
        if aid in seen_ids:
            errors.append(f"{prefix}: duplicated id: {aid}")
        seen_ids.add(aid)

        qtype = item.get("question_type")
        if allowed_types and qtype not in allowed_types:
            errors.append(f"{prefix}: unknown question_type: {qtype}")

        legacy_qtype = item.get("legacy_question_type") or ""
        pair = (item.get("topic_id"), qtype, legacy_qtype)

        if pair in seen_pair:
            errors.append(
                f"{prefix}: duplicated topic_id + question_type + legacy_question_type pair: {pair}"
            )

        seen_pair.add(pair)

        for list_key in [
            "question_examples",
            "expected_structure",
            "model_answer_outline",
            "high_score_features",
            "low_score_patterns",
            "field_connection_points",
            "revision_notes"
        ]:
            value = item.get(list_key)
            if not isinstance(value, list) or not value:
                errors.append(f"{prefix}: {list_key} must be non-empty list")

        outline = item.get("model_answer_outline", [])
        if isinstance(outline, list) and len(outline) < 4:
            errors.append(f"{prefix}: model_answer_outline should have at least 4 bullets")

        high = item.get("high_score_features", [])
        low = item.get("low_score_patterns", [])
        if isinstance(high, list) and len(high) < 3:
            errors.append(f"{prefix}: high_score_features should have at least 3 items")
        if isinstance(low, list) and len(low) < 3:
            errors.append(f"{prefix}: low_score_patterns should have at least 3 items")

    if errors:
        print_errors(errors)
        raise SystemExit(1)

    print("VALID")
    print("bank:", BANK_PATH)
    print("answers:", len(answers))
    print()
    print("[entries]")
    for item in answers:
        print(f"- {item['id']} | {item['topic_id']} | {item['question_type']} | {item['title']}")


def print_errors(errors):
    print("INVALID")
    for e in errors:
        print("-", e)


if __name__ == "__main__":
    main()
