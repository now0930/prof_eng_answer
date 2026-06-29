from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rubric_registry import (
    build_model_answer_template,
    load_model_answer_bank,
    model_answer_key,
    question_type_ids,
    save_model_answer_bank,
    upsert_model_answer,
    validate_model_answer_bank,
)

from rubric_content.common import (
    MODEL_ANSWER_BANK,
    backup_file,
    candidate_path,
    listify,
    print_next_steps,
    project_path,
    read_json,
    write_json,
)


def _model_answer_aliases(item: dict) -> list[str]:
    aliases: list[str] = []
    for key in ("topic_aliases", "aliases"):
        for alias in listify(item.get(key)):
            if alias not in aliases:
                aliases.append(alias)
    return aliases


def cmd_list_model_answers(args: argparse.Namespace) -> int:
    bank = load_model_answer_bank(args.bank)
    for item in bank.get("answers", []):
        if not isinstance(item, dict):
            continue
        if args.topic and item.get("topic_id") != args.topic:
            continue
        if args.type and item.get("question_type") != args.type:
            continue

        aliases = ", ".join(_model_answer_aliases(item)[:8])
        print(
            f"{item.get('topic_id')} | {item.get('question_type')} | "
            f"{item.get('id')} | {item.get('title')} | aliases=[{aliases}]"
        )
    return 0


def cmd_new_model_answer(args: argparse.Namespace) -> int:
    allowed = set(question_type_ids())
    if args.question_type not in allowed:
        print(f"ERROR: unknown question_type: {args.question_type}", file=sys.stderr)
        print("Allowed:", ", ".join(sorted(allowed)), file=sys.stderr)
        return 1

    entry = build_model_answer_template(
        topic_id=args.topic_id,
        question_type=args.question_type,
        title=args.title,
    )

    if args.question:
        entry["question_examples"] = args.question
    if args.alias:
        entry["topic_aliases"] = args.alias
    if args.field:
        entry["field_connection_points"] = args.field

    out = Path(args.out) if args.out else candidate_path("model_answers", entry["id"])
    write_json(out, entry)
    print_next_steps(out, "promote-model-answer")
    return 0


def cmd_promote_model_answer(args: argparse.Namespace) -> int:
    candidate = Path(args.candidate)
    if not candidate.is_absolute():
        from rubric_content.common import ROOT
        candidate = ROOT / candidate

    if not candidate.exists():
        print(f"ERROR: candidate not found: {candidate}", file=sys.stderr)
        return 1

    entry = read_json(candidate)
    if not isinstance(entry, dict):
        print("ERROR: candidate must be a JSON object", file=sys.stderr)
        return 1

    if "aliases" in entry:
        print("ERROR: use topic_aliases, not aliases", file=sys.stderr)
        return 1

    bank_path = project_path(args.bank, MODEL_ANSWER_BANK)
    bank = load_model_answer_bank(bank_path)

    allowed = question_type_ids()
    temp_bank = dict(bank)
    existing = [
        item for item in bank.get("answers", [])
        if isinstance(item, dict) and item.get("id") != entry.get("id")
    ]
    temp_bank["answers"] = existing + [entry]

    errors = validate_model_answer_bank(temp_bank, allowed_types=allowed)
    if errors:
        print("INVALID candidate or bank")
        for error in errors:
            print("-", error)
        return 1

    before_pairs = {
        model_answer_key(x)
        for x in bank.get("answers", [])
        if isinstance(x, dict)
    }
    pair = model_answer_key(entry)

    if pair in before_pairs and not args.replace:
        print(f"ERROR: topic_id + question_type already exists: {pair}", file=sys.stderr)
        print("Use --replace to overwrite the existing entry.", file=sys.stderr)
        return 1

    if args.backup:
        print("backup:", backup_file(bank_path))

    bank = upsert_model_answer(bank, entry)
    save_model_answer_bank(bank, bank_path)

    print("promoted:", entry.get("id"))
    print("bank:", bank_path)
    return 0


def cmd_delete_model_answer(args: argparse.Namespace) -> int:
    bank_path = project_path(args.bank, MODEL_ANSWER_BANK)
    bank = load_model_answer_bank(bank_path)
    answers = bank.get("answers", [])

    before = len(answers)
    if args.id:
        answers = [
            x for x in answers
            if not (isinstance(x, dict) and x.get("id") == args.id)
        ]
    elif args.topic and args.type:
        answers = [
            x for x in answers
            if not (
                isinstance(x, dict)
                and x.get("topic_id") == args.topic
                and x.get("question_type") == args.type
            )
        ]
    else:
        print("ERROR: provide --id or both --topic and --type", file=sys.stderr)
        return 1

    after = len(answers)
    if before == after:
        print("ERROR: target not found", file=sys.stderr)
        return 1

    bank["answers"] = answers
    errors = validate_model_answer_bank(bank, allowed_types=question_type_ids())
    if errors:
        print("INVALID after delete")
        for error in errors:
            print("-", error)
        return 1

    if args.backup:
        print("backup:", backup_file(bank_path))

    save_model_answer_bank(bank, bank_path)
    print("deleted:", before - after)
    print("bank:", bank_path)
    return 0


def cmd_validate_model_answers(args: argparse.Namespace) -> int:
    bank = load_model_answer_bank(args.bank)
    errors = validate_model_answer_bank(bank, allowed_types=question_type_ids())

    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1

    print("VALID")
    print("answers:", len(bank.get("answers", [])))
    return 0


def add_parsers(sub) -> None:
    p = sub.add_parser("list-model-answers", help="List model answers")
    p.add_argument("--bank", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--type", default=None)
    p.set_defaults(func=cmd_list_model_answers)

    p = sub.add_parser("new-model-answer", help="Create editable model-answer candidate JSON")
    p.add_argument("--topic-id", required=True)
    p.add_argument("--question-type", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--question", action="append", default=[])
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--field", action="append", default=[])
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_new_model_answer)

    p = sub.add_parser("promote-model-answer", help="Promote candidate JSON into model answer bank")
    p.add_argument("--candidate", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--replace", action="store_true")
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_promote_model_answer, backup=True)

    p = sub.add_parser("delete-model-answer", help="Delete model answer by id or topic/type")
    p.add_argument("--id", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--type", default=None)
    p.add_argument("--bank", default=None)
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_delete_model_answer, backup=True)

    p = sub.add_parser("validate-model-answers", help="Validate model answer bank")
    p.add_argument("--bank", default=None)
    p.set_defaults(func=cmd_validate_model_answers)
