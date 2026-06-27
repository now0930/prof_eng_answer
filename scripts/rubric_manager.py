#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rubric_registry import (  # noqa: E402
    build_model_answer_template,
    load_model_answer_bank,
    load_question_type_profile,
    model_answer_key,
    question_type_ids,
    save_model_answer_bank,
    upsert_model_answer,
    validate_model_answer_bank,
    write_json,
)


def cmd_list_types(_args: argparse.Namespace) -> int:
    profile = load_question_type_profile()
    for item in profile.get("types", []):
        print(f"{item.get('id'):14} | {item.get('name')} | {item.get('c_lens')}")
    return 0


def cmd_list_model_answers(args: argparse.Namespace) -> int:
    bank = load_model_answer_bank(args.bank)
    rows = bank.get("answers", [])

    for item in rows:
        if args.topic and item.get("topic_id") != args.topic:
            continue
        if args.type and item.get("question_type") != args.type:
            continue

        aliases = ", ".join(item.get("topic_aliases", [])[:5])
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

    out = Path(args.out) if args.out else (
        ROOT / "rubrics" / "model_answers" / "candidates" /
        f"{entry['id']}.json"
    )

    write_json(out, entry)
    print("created:", out)
    print()
    print("다음 순서:")
    print(f"1) vim {out}")
    print(f"2) python3 scripts/rubric_manager.py promote-model-answer --candidate {out}")
    print("3) python3 scripts/rubric_manager.py validate-all")
    return 0


def cmd_promote_model_answer(args: argparse.Namespace) -> int:
    candidate_path = Path(args.candidate)
    if not candidate_path.is_absolute():
        candidate_path = ROOT / candidate_path

    if not candidate_path.exists():
        print(f"ERROR: candidate not found: {candidate_path}", file=sys.stderr)
        return 1

    entry = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(entry, dict):
        print("ERROR: candidate must be a JSON object", file=sys.stderr)
        return 1

    bank = load_model_answer_bank(args.bank)
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

    before_pairs = {model_answer_key(x) for x in bank.get("answers", []) if isinstance(x, dict)}
    pair = model_answer_key(entry)

    if pair in before_pairs and not args.replace:
        print(f"ERROR: topic_id + question_type already exists: {pair}", file=sys.stderr)
        print("Use --replace to overwrite the existing entry.", file=sys.stderr)
        return 1

    bank = upsert_model_answer(bank, entry)
    save_model_answer_bank(bank, args.bank)

    print("promoted:", entry.get("id"))
    print("bank:", args.bank or "rubrics/model_answers/industrial_instrumentation_control.json")
    return 0


def cmd_validate_model_answers(args: argparse.Namespace) -> int:
    bank = load_model_answer_bank(args.bank)
    allowed = question_type_ids()
    errors = validate_model_answer_bank(bank, allowed_types=allowed)

    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1

    print("VALID")
    print("answers:", len(bank.get("answers", [])))
    return 0


def run_script(path: str) -> int:
    script = ROOT / path
    if not script.exists():
        print("SKIP missing:", path)
        return 0

    print("RUN:", path)
    return subprocess.call([sys.executable, str(script)], cwd=str(ROOT))


def cmd_validate_all(_args: argparse.Namespace) -> int:
    scripts = [
        "scripts/validate_question_type_profile.py",
        "scripts/validate_model_answer_bank.py",
        "scripts/validate_config.py",
        "scripts/validate_fact_anchor_bank.py",
    ]

    rc = 0
    for script in scripts:
        rc = max(rc, run_script(script))

    print("RUN: py_compile")
    files = [
        "rubric_registry.py",
        "question_type_router.py",
        "model_answer_router.py",
        "originality_grader.py",
        "gemini_grader.py",
        "grading_config.py",
        "grading_agents.py",
        "bot.py",
    ]
    existing = [str(ROOT / f) for f in files if (ROOT / f).exists()]
    rc = max(rc, subprocess.call([sys.executable, "-m", "py_compile", *existing]))

    if rc == 0:
        print("ALL VALID")
    return rc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rubric, question type, and model-answer management helper"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-types", help="List question types")
    p.set_defaults(func=cmd_list_types)

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

    p = sub.add_parser("promote-model-answer", help="Promote candidate JSON into main bank")
    p.add_argument("--candidate", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--replace", action="store_true")
    p.set_defaults(func=cmd_promote_model_answer)

    p = sub.add_parser("validate-model-answers", help="Validate model answer bank")
    p.add_argument("--bank", default=None)
    p.set_defaults(func=cmd_validate_model_answers)

    p = sub.add_parser("validate-all", help="Run all rubric validators and py_compile")
    p.set_defaults(func=cmd_validate_all)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
