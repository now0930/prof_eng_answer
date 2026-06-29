from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from rubric_content.common import (
    ROOT,
    TOPIC_IMPORTANCE_BANK,
    backup_file,
    candidate_path,
    listify,
    print_next_steps,
    project_path,
    read_json,
    write_json,
)

VALID_DIFFICULTY = {
    "BASIC_CONCEPT",
    "FIELD_APPLICATION",
    "DESIGN_EVALUATION",
    "THEORY_CORE",
}

VALID_SELECTION_IMPORTANCE = {
    "CORE_MUST_PREPARE",
    "HIGH_PRIORITY",
    "NORMAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "OPTIONAL",
}


def load_topic_importance_bank(path: str | Path | None = None) -> dict[str, Any]:
    return read_json(project_path(path, TOPIC_IMPORTANCE_BANK))


def save_topic_importance_bank(data: dict[str, Any], path: str | Path | None = None) -> Path:
    return write_json(project_path(path, TOPIC_IMPORTANCE_BANK), data)


def build_topic_importance_template(topic_id: str, label: str, difficulty: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "label": label,
        "aliases": [],
        "difficulty": difficulty,
        "selection_importance": "NORMAL",
        "selection_policy": "safe_or_balanced_choice",
        "minimum_attempt_floor": 10,
        "target_score": 15,
        "excellent_score_band": [15.0, 15.75],
        "omission_risk": "low",
        "fatal_error_risk": "medium",
        "score_ceiling_policy": "field_application_practical_ceiling",
    }


def _is_number(value: Any) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


def _valid_score_band(value: Any) -> bool:
    if _is_number(value):
        return True
    if isinstance(value, list) and len(value) == 2:
        return all(_is_number(x) for x in value)
    return False


def validate_topic_importance_bank_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    topics = data.get("topics", [])

    if not isinstance(topics, list) or not topics:
        errors.append("topics must be non-empty list")
        return errors

    seen: set[str] = set()

    for idx, topic in enumerate(topics):
        prefix = f"topics[{idx}]"
        if not isinstance(topic, dict):
            errors.append(f"{prefix}: topic must be object")
            continue

        topic_id = str(topic.get("topic_id", "")).strip()
        if not topic_id:
            errors.append(f"{prefix}: topic_id missing")
            continue
        if topic_id in seen:
            errors.append(f"{prefix}: duplicated topic_id: {topic_id}")
        seen.add(topic_id)

        if not str(topic.get("label", "")).strip():
            errors.append(f"{topic_id}: label missing")

        aliases = topic.get("aliases", [])
        if not isinstance(aliases, list) or not aliases:
            errors.append(f"{topic_id}: aliases must be non-empty list")

        difficulty = topic.get("difficulty")
        if difficulty not in VALID_DIFFICULTY:
            errors.append(f"{topic_id}: invalid difficulty: {difficulty}")

        selection_importance = topic.get("selection_importance")
        if selection_importance and selection_importance not in VALID_SELECTION_IMPORTANCE:
            errors.append(f"{topic_id}: suspicious selection_importance: {selection_importance}")

        for key in ["minimum_attempt_floor", "target_score"]:
            if key in topic and not _is_number(topic.get(key)):
                errors.append(f"{topic_id}: {key} must be numeric")

        if "excellent_score_band" in topic and not _valid_score_band(topic.get("excellent_score_band")):
            errors.append(f"{topic_id}: excellent_score_band must be number or [min, max]")

        score_ceiling_policy = topic.get("score_ceiling_policy")
        if score_ceiling_policy is not None and not isinstance(score_ceiling_policy, (str, dict)):
            errors.append(f"{topic_id}: score_ceiling_policy must be string or object")

    return errors


def upsert_topic_importance(bank: dict[str, Any], topic: dict[str, Any]) -> dict[str, Any]:
    topics = bank.setdefault("topics", [])
    if not isinstance(topics, list):
        bank["topics"] = topics = []

    target = str(topic.get("topic_id", "")).strip()
    for idx, old in enumerate(topics):
        if isinstance(old, dict) and str(old.get("topic_id", "")).strip() == target:
            topics[idx] = topic
            return bank

    topics.append(topic)
    return bank


def cmd_list_topic_importance(args: argparse.Namespace) -> int:
    bank = load_topic_importance_bank(args.bank)

    for topic in bank.get("topics", []):
        if not isinstance(topic, dict):
            continue
        if args.topic and topic.get("topic_id") != args.topic:
            continue

        aliases = ", ".join(listify(topic.get("aliases"))[:8])
        print(
            f"{topic.get('topic_id')} | {topic.get('label')} | "
            f"{topic.get('difficulty')} | {topic.get('selection_importance')} | aliases=[{aliases}]"
        )

        if args.detail:
            print(f"  policy: {topic.get('selection_policy')}")
            print(f"  floor/target/band: {topic.get('minimum_attempt_floor')} / {topic.get('target_score')} / {topic.get('excellent_score_band')}")
            print(f"  ceiling: {topic.get('score_ceiling_policy')}")
    return 0


def cmd_new_topic_importance(args: argparse.Namespace) -> int:
    if args.difficulty not in VALID_DIFFICULTY:
        print(f"ERROR: invalid difficulty: {args.difficulty}", file=sys.stderr)
        print("Allowed:", ", ".join(sorted(VALID_DIFFICULTY)), file=sys.stderr)
        return 1

    entry = build_topic_importance_template(args.topic_id, args.label, args.difficulty)

    if args.alias:
        entry["aliases"] = args.alias
    if args.selection_importance:
        entry["selection_importance"] = args.selection_importance

    out = Path(args.out) if args.out else candidate_path("topic_importance", entry["topic_id"])
    write_json(out, entry)
    print_next_steps(out, "promote-topic-importance")
    return 0


def cmd_promote_topic_importance(args: argparse.Namespace) -> int:
    candidate = Path(args.candidate)
    if not candidate.is_absolute():
        candidate = ROOT / candidate

    if not candidate.exists():
        print(f"ERROR: candidate not found: {candidate}", file=sys.stderr)
        return 1

    entry = read_json(candidate)
    if not isinstance(entry, dict):
        print("ERROR: candidate must be object", file=sys.stderr)
        return 1

    bank_path = project_path(args.bank, TOPIC_IMPORTANCE_BANK)
    bank = load_topic_importance_bank(bank_path)

    temp = dict(bank)
    temp["topics"] = [
        t for t in bank.get("topics", [])
        if isinstance(t, dict) and t.get("topic_id") != entry.get("topic_id")
    ] + [entry]

    errors = validate_topic_importance_bank_data(temp)
    if errors:
        print("INVALID candidate or bank")
        for error in errors:
            print("-", error)
        return 1

    exists = any(
        isinstance(t, dict) and t.get("topic_id") == entry.get("topic_id")
        for t in bank.get("topics", [])
    )
    if exists and not args.replace:
        print(f"ERROR: topic_id already exists: {entry.get('topic_id')}", file=sys.stderr)
        print("Use --replace to overwrite.", file=sys.stderr)
        return 1

    if args.backup:
        print("backup:", backup_file(bank_path))

    upsert_topic_importance(bank, entry)
    save_topic_importance_bank(bank, bank_path)

    print("promoted:", entry.get("topic_id"))
    print("bank:", bank_path)
    return 0


def cmd_delete_topic_importance(args: argparse.Namespace) -> int:
    bank_path = project_path(args.bank, TOPIC_IMPORTANCE_BANK)
    bank = load_topic_importance_bank(bank_path)
    topics = bank.get("topics", [])

    before = len(topics)
    bank["topics"] = [
        t for t in topics
        if not (isinstance(t, dict) and t.get("topic_id") == args.topic_id)
    ]
    after = len(bank["topics"])

    if before == after:
        print(f"ERROR: topic_id not found: {args.topic_id}", file=sys.stderr)
        return 1

    errors = validate_topic_importance_bank_data(bank)
    if errors:
        print("INVALID after delete")
        for error in errors:
            print("-", error)
        return 1

    if args.backup:
        print("backup:", backup_file(bank_path))

    save_topic_importance_bank(bank, bank_path)
    print("deleted:", args.topic_id)
    print("bank:", bank_path)
    return 0


def cmd_validate_topic_importance(args: argparse.Namespace) -> int:
    bank = load_topic_importance_bank(args.bank)
    errors = validate_topic_importance_bank_data(bank)

    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1

    print("VALID")
    print("topics:", len(bank.get("topics", [])))
    return 0


def add_parsers(sub) -> None:
    p = sub.add_parser("list-topic-importance", help="List topic importance entries")
    p.add_argument("--bank", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--detail", action="store_true")
    p.set_defaults(func=cmd_list_topic_importance)

    p = sub.add_parser("new-topic-importance", help="Create editable topic-importance candidate")
    p.add_argument("--topic-id", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--difficulty", required=True)
    p.add_argument("--selection-importance", default=None)
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_new_topic_importance)

    p = sub.add_parser("promote-topic-importance", help="Promote candidate into topic importance bank")
    p.add_argument("--candidate", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--replace", action="store_true")
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_promote_topic_importance, backup=True)

    p = sub.add_parser("delete-topic-importance", help="Delete topic importance entry")
    p.add_argument("--topic-id", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_delete_topic_importance, backup=True)

    p = sub.add_parser("validate-topic-importance", help="Validate topic importance bank")
    p.add_argument("--bank", default=None)
    p.set_defaults(func=cmd_validate_topic_importance)
