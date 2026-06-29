from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from rubric_content.common import (
    FACT_ANCHOR_BANK,
    ROOT,
    backup_file,
    candidate_path,
    listify,
    print_next_steps,
    project_path,
    read_json,
    write_json,
)


def load_fact_anchor_bank(path: str | Path | None = None) -> dict[str, Any]:
    return read_json(project_path(path, FACT_ANCHOR_BANK))


def save_fact_anchor_bank(data: dict[str, Any], path: str | Path | None = None) -> Path:
    return write_json(project_path(path, FACT_ANCHOR_BANK), data)


def build_fact_anchor_topic_template(topic_id: str, name: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "name": name,
        "aliases": [],
        "anchors": [
            {
                "id": f"{topic_id}_anchor_{idx}",
                "name": f"핵심 Fact {idx}",
                "expected": "이 anchor에서 기대하는 핵심 설명을 작성한다.",
                "core_terms": ["필수 용어"],
                "support_terms": ["보조 용어"],
            }
            for idx in range(1, 6)
        ],
    }


def validate_fact_anchor_bank_data(data: dict[str, Any]) -> list[str]:
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

        if not str(topic.get("name", "")).strip():
            errors.append(f"{topic_id}: name missing")

        anchors = topic.get("anchors", [])
        if not isinstance(anchors, list):
            errors.append(f"{topic_id}: anchors must be list")
            continue

        if len(anchors) != 5:
            errors.append(f"{topic_id}: anchors count must be 5: {len(anchors)}")

        anchor_ids: set[str] = set()
        for aidx, anchor in enumerate(anchors):
            aprefix = f"{topic_id}/anchors[{aidx}]"
            if not isinstance(anchor, dict):
                errors.append(f"{aprefix}: anchor must be object")
                continue

            for key in ["id", "name", "expected", "core_terms", "support_terms"]:
                if key not in anchor:
                    errors.append(f"{aprefix}: {key} missing")

            aid = str(anchor.get("id", "")).strip()
            if not aid:
                errors.append(f"{aprefix}: id empty")
            elif aid in anchor_ids:
                errors.append(f"{aprefix}: duplicated anchor id: {aid}")
            anchor_ids.add(aid)

            if not listify(anchor.get("core_terms")):
                errors.append(f"{aprefix}: core_terms must be non-empty")
            if not isinstance(anchor.get("support_terms", []), list):
                errors.append(f"{aprefix}: support_terms must be list")

    return errors


def upsert_fact_anchor_topic(bank: dict[str, Any], topic: dict[str, Any]) -> dict[str, Any]:
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


def cmd_list_fact_anchors(args: argparse.Namespace) -> int:
    bank = load_fact_anchor_bank(args.bank)

    for topic in bank.get("topics", []):
        if not isinstance(topic, dict):
            continue
        if args.topic and topic.get("topic_id") != args.topic:
            continue

        anchors = topic.get("anchors", [])
        aliases = ", ".join(listify(topic.get("aliases"))[:8])
        print(
            f"{topic.get('topic_id')} | {topic.get('name')} | "
            f"anchors={len(anchors) if isinstance(anchors, list) else 'invalid'} | aliases=[{aliases}]"
        )

        if args.detail and isinstance(anchors, list):
            for anchor in anchors:
                if isinstance(anchor, dict):
                    print(f"  - {anchor.get('id')} | {anchor.get('name')} | core={listify(anchor.get('core_terms'))}")
    return 0


def cmd_new_fact_anchor_topic(args: argparse.Namespace) -> int:
    entry = build_fact_anchor_topic_template(args.topic_id, args.name)
    if args.alias:
        entry["aliases"] = args.alias

    out = Path(args.out) if args.out else candidate_path("fact_anchors", entry["topic_id"])
    write_json(out, entry)
    print_next_steps(out, "promote-fact-anchor-topic")
    return 0


def cmd_promote_fact_anchor_topic(args: argparse.Namespace) -> int:
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

    bank_path = project_path(args.bank, FACT_ANCHOR_BANK)
    bank = load_fact_anchor_bank(bank_path)

    temp = dict(bank)
    temp["topics"] = [
        t for t in bank.get("topics", [])
        if isinstance(t, dict) and t.get("topic_id") != entry.get("topic_id")
    ] + [entry]

    errors = validate_fact_anchor_bank_data(temp)
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

    upsert_fact_anchor_topic(bank, entry)
    save_fact_anchor_bank(bank, bank_path)
    print("promoted:", entry.get("topic_id"))
    print("bank:", bank_path)
    return 0


def cmd_delete_fact_anchor_topic(args: argparse.Namespace) -> int:
    bank_path = project_path(args.bank, FACT_ANCHOR_BANK)
    bank = load_fact_anchor_bank(bank_path)
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

    errors = validate_fact_anchor_bank_data(bank)
    if errors:
        print("INVALID after delete")
        for error in errors:
            print("-", error)
        return 1

    if args.backup:
        print("backup:", backup_file(bank_path))

    save_fact_anchor_bank(bank, bank_path)
    print("deleted:", args.topic_id)
    print("bank:", bank_path)
    return 0


def cmd_validate_fact_anchors(args: argparse.Namespace) -> int:
    bank = load_fact_anchor_bank(args.bank)
    errors = validate_fact_anchor_bank_data(bank)

    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1

    print("VALID")
    print("topics:", len(bank.get("topics", [])))
    return 0


def add_parsers(sub) -> None:
    p = sub.add_parser("list-fact-anchors", help="List fact anchor topics")
    p.add_argument("--bank", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--detail", action="store_true")
    p.set_defaults(func=cmd_list_fact_anchors)

    p = sub.add_parser("new-fact-anchor-topic", help="Create editable fact-anchor topic candidate")
    p.add_argument("--topic-id", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--alias", action="append", default=[])
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_new_fact_anchor_topic)

    p = sub.add_parser("promote-fact-anchor-topic", help="Promote candidate into fact anchor bank")
    p.add_argument("--candidate", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--replace", action="store_true")
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_promote_fact_anchor_topic, backup=True)

    p = sub.add_parser("delete-fact-anchor-topic", help="Delete fact anchor topic")
    p.add_argument("--topic-id", required=True)
    p.add_argument("--bank", default=None)
    p.add_argument("--no-backup", dest="backup", action="store_false")
    p.set_defaults(func=cmd_delete_fact_anchor_topic, backup=True)

    p = sub.add_parser("validate-fact-anchors", help="Validate fact anchor bank")
    p.add_argument("--bank", default=None)
    p.set_defaults(func=cmd_validate_fact_anchors)
