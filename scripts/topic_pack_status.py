#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


PACK_FILES = ["README.md", "fact_anchor.json", "model_answer.json", "topic_importance.json", "logic_check.json"]
STATUS_FILE = "topic_status.json"
VALID_STATUSES = {"draft", "reviewed", "approved", "frozen"}


def project_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parents[1], Path.cwd(), Path("/workspace/prof_eng_answer")]:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate
    raise SystemExit("ERROR: project root not found. Run from prof_eng_answer repo.")


def topic_pack_dir(root: Path, topic_id: str) -> Path:
    return root / "rubrics" / "topic_packs" / topic_id


def iter_topic_ids(root: Path) -> list[str]:
    base = root / "rubrics" / "topic_packs"
    return sorted(path.name for path in base.iterdir() if path.is_dir()) if base.exists() else []


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def content_hash(pack_dir: Path) -> str:
    h = hashlib.sha256()
    for filename in PACK_FILES:
        path = pack_dir / filename
        h.update(filename.encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes() if path.exists() else b"<MISSING>")
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def default_status(topic_id: str, current_hash: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "status": "draft",
        "review_state": "not_reviewed",
        "content_hash": "",
        "last_validated_at": "",
        "last_reviewed_at": "",
        "last_review_model": "",
        "last_review_report": "",
        "approved_at": "",
        "frozen_at": "",
        "notes": [],
        "_current_hash": current_hash,
        "_changed": True,
    }


def load_status(pack_dir: Path, topic_id: str) -> dict[str, Any]:
    current_hash = content_hash(pack_dir)
    path = pack_dir / STATUS_FILE
    if not path.exists():
        return default_status(topic_id, current_hash)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        data = default_status(topic_id, current_hash)
        data["review_state"] = "status_parse_error"
        data["notes"] = [f"topic_status.json parse error: {exc}"]

    if not isinstance(data, dict):
        data = default_status(topic_id, current_hash)

    for key, value in default_status(topic_id, current_hash).items():
        data.setdefault(key, value)

    data["_current_hash"] = current_hash
    data["_changed"] = data.get("content_hash") != current_hash
    return data


def public_status(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if not k.startswith("_")}


def write_status(pack_dir: Path, data: dict[str, Any]) -> None:
    (pack_dir / STATUS_FILE).write_text(json.dumps(public_status(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def select_topic_ids(root: Path, selected: list[str] | None, *, all_topics: bool, changed_only: bool, include_frozen: bool) -> list[str]:
    if selected:
        topic_ids = selected
    elif all_topics:
        topic_ids = iter_topic_ids(root)
    else:
        raise SystemExit("ERROR: use --topic-id or --all")

    missing = [tid for tid in topic_ids if not topic_pack_dir(root, tid).is_dir()]
    if missing:
        raise SystemExit(f"ERROR: missing topic packs: {missing}")

    result: list[str] = []
    for topic_id in topic_ids:
        status = load_status(topic_pack_dir(root, topic_id), topic_id)
        if changed_only and not status.get("_changed"):
            continue
        if not include_frozen and status.get("status") == "frozen" and not status.get("_changed"):
            continue
        result.append(topic_id)
    return result


def update_status(
    data: dict[str, Any],
    *,
    set_status: str | None = None,
    sync_hash: bool = False,
    mark_validated: bool = False,
    mark_reviewed: bool = False,
    review_model: str = "",
    review_report: str = "",
    note: str | None = None,
) -> dict[str, Any]:
    stamp = now_stamp()
    if set_status:
        if set_status not in VALID_STATUSES:
            raise SystemExit(f"ERROR: invalid status: {set_status}")
        data["status"] = set_status
        if set_status == "approved":
            data["approved_at"] = stamp
        if set_status == "frozen":
            data["frozen_at"] = stamp
            data["approved_at"] = data.get("approved_at") or stamp
    if mark_validated:
        data["last_validated_at"] = stamp
    if mark_reviewed:
        data["review_state"] = "reviewed"
        data["last_reviewed_at"] = stamp
        if review_model:
            data["last_review_model"] = review_model
        if review_report:
            data["last_review_report"] = review_report
    if sync_hash:
        data["content_hash"] = data["_current_hash"]
        data["_changed"] = False
    if note:
        notes = data.get("notes") if isinstance(data.get("notes"), list) else []
        notes.append(f"{stamp}: {note}")
        data["notes"] = notes
    return data


def print_table(rows: list[dict[str, Any]]) -> None:
    print("topic_id\tstatus\treview_state\tchanged\tlast_validated_at\tlast_reviewed_at")
    for row in rows:
        print("\t".join([
            str(row.get("topic_id", "")),
            str(row.get("status", "")),
            str(row.get("review_state", "")),
            "yes" if row.get("_changed") else "no",
            str(row.get("last_validated_at", "")),
            str(row.get("last_reviewed_at", "")),
        ]))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Manage topic_pack status/hash metadata.")
    p.add_argument("--topic-id", action="append", default=None)
    p.add_argument("--all", action="store_true")
    p.add_argument("--changed-only", action="store_true")
    p.add_argument("--include-frozen", action="store_true")
    p.add_argument("--set-status", choices=sorted(VALID_STATUSES), default=None)
    p.add_argument("--sync-hash", action="store_true")
    p.add_argument("--mark-validated", action="store_true")
    p.add_argument("--mark-reviewed", action="store_true")
    p.add_argument("--review-model", default="")
    p.add_argument("--review-report", default="")
    p.add_argument("--note", default=None)
    p.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = project_root()
    topic_ids = select_topic_ids(root, args.topic_id, all_topics=args.all, changed_only=args.changed_only, include_frozen=args.include_frozen)

    should_write = any([args.set_status, args.sync_hash, args.mark_validated, args.mark_reviewed, args.note])
    rows: list[dict[str, Any]] = []
    for topic_id in topic_ids:
        pack_dir = topic_pack_dir(root, topic_id)
        status = load_status(pack_dir, topic_id)
        if should_write:
            status = update_status(
                status,
                set_status=args.set_status,
                sync_hash=args.sync_hash,
                mark_validated=args.mark_validated,
                mark_reviewed=args.mark_reviewed,
                review_model=args.review_model,
                review_report=args.review_report,
                note=args.note,
            )
            write_status(pack_dir, status)
        rows.append(status)

    if args.json:
        print(json.dumps([public_status(r) | {"changed": r.get("_changed")} for r in rows], ensure_ascii=False, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
