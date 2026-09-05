#!/usr/bin/env python3
"""Executable Topic Pack authoring workflow.

The Markdown workflow remains the human explanation.  This controller owns the
machine-enforced order, approval metadata and promotion gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from create_topic_pack import create_topic_pack  # noqa: E402
from topic_pack_status import (  # noqa: E402
    load_status,
    now_stamp,
    project_root,
    topic_pack_dir,
    update_status,
    write_status,
)


WORKFLOW_CONTRACT = "topic_pack_workflow.v1"
REQUIRED_SOURCE_FILES = (
    "README.md",
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
)


def _resolve(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else root / path


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def _normalized_title(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.casefold())


def _existing_titles(root: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    base = root / "rubrics" / "topic_packs"
    for pack_dir in sorted(path for path in base.iterdir() if path.is_dir()):
        model_path = pack_dir / "model_answer.json"
        try:
            data = json.loads(model_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        title = str(data.get("title_ko") or data.get("title") or "").strip()
        if title:
            titles[pack_dir.name] = title
    return titles


def _check_new_topic(root: Path, topic_id: str, title: str, sheet: Path) -> None:
    if topic_pack_dir(root, topic_id).exists():
        raise SystemExit(f"ERROR: topic pack already exists: {topic_id}")
    if not sheet.is_file():
        raise SystemExit(f"ERROR: Topic Sheet not found: {sheet}")
    sheet_text = sheet.read_text(encoding="utf-8")
    if topic_id not in sheet_text:
        raise SystemExit(f"ERROR: Topic Sheet does not identify topic_id {topic_id!r}")

    wanted = _normalized_title(title)
    if not wanted:
        raise SystemExit("ERROR: --title must contain letters or numbers")
    duplicate_ids = [
        existing_id
        for existing_id, existing_title in _existing_titles(root).items()
        if _normalized_title(existing_title) == wanted
    ]
    if duplicate_ids:
        raise SystemExit(
            "ERROR: duplicate normalized Topic title owned by: "
            + ", ".join(duplicate_ids)
        )


def _write_draft_status(
    root: Path,
    topic_id: str,
    sheet: Path,
    *,
    generated: bool,
) -> None:
    pack_dir = topic_pack_dir(root, topic_id)
    status = load_status(pack_dir, topic_id)
    status.update(
        {
            "schema_version": "topic_status.v2",
            "workflow_contract": WORKFLOW_CONTRACT,
            "status": "draft",
            "review_state": "human_review_required",
            "content_hash": "",
            "reviewer": "",
            "review_method": "",
            "source_sheet": _relative(root, sheet),
            "source_sheet_hash": _sha256(sheet),
            "approved_source_hash": "",
            "created_at": now_stamp(),
            "generated_from_sheet": generated,
            "next_action": (
                "Review README.md and source JSON, then run approve-topic."
            ),
            "notes": [
                f"{now_stamp()}: managed Topic Pack workflow started"
            ],
        }
    )
    write_status(pack_dir, status)


def _run(root: Path, command: list[str]) -> None:
    print("RUN:", " ".join(command))
    result = subprocess.run(command, cwd=root, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _release_command(
    topic_id: str,
    *,
    promote: bool,
    smoke: bool = False,
) -> list[str]:
    command = [
        sys.executable,
        "scripts/validate_topic_pack_release.py",
        "--topic-id",
        topic_id,
    ]
    if promote:
        command.extend(["--promote-generated", "--sync-status"])
    if smoke:
        command.append("--smoke")
    return command


def managed_approval_errors(root: Path, topic_id: str) -> list[str]:
    """Return promotion blockers for workflow-managed Topic Packs."""
    pack_dir = topic_pack_dir(root, topic_id)
    status = load_status(pack_dir, topic_id)
    if status.get("workflow_contract") != WORKFLOW_CONTRACT:
        return []

    errors: list[str] = []
    if status.get("status") not in {"approved", "frozen"}:
        errors.append("status must be approved or frozen")
    if status.get("review_state") != "reviewed":
        errors.append("review_state must be reviewed")
    if not str(status.get("reviewer") or "").strip():
        errors.append("reviewer is required")
    if status.get("content_hash") != status.get("_current_hash"):
        errors.append("approved content hash does not match current source")
    if status.get("approved_source_hash") != status.get("_current_hash"):
        errors.append("approved_source_hash does not match current source")
    return errors


def _approval_precheck(root: Path, topic_id: str) -> dict[str, Any]:
    pack_dir = topic_pack_dir(root, topic_id)
    if not pack_dir.is_dir():
        raise SystemExit(f"ERROR: topic pack not found: {topic_id}")
    status = load_status(pack_dir, topic_id)
    if status.get("workflow_contract") != WORKFLOW_CONTRACT:
        raise SystemExit(
            "ERROR: Topic Pack is not managed by add-topic; "
            "legacy packs must be migrated explicitly"
        )
    missing = [name for name in REQUIRED_SOURCE_FILES if not (pack_dir / name).is_file()]
    if missing:
        raise SystemExit(f"ERROR: missing source files: {missing}")
    candidates = sorted(pack_dir.glob("*.candidate.json"))
    if candidates:
        raise SystemExit(
            "ERROR: unresolved candidate files: "
            + ", ".join(path.name for path in candidates)
        )
    placeholder_files: list[str] = []
    for filename in REQUIRED_SOURCE_FILES[1:]:
        text = (pack_dir / filename).read_text(encoding="utf-8", errors="replace")
        if "todo" in text.casefold() or "scaffold" in text.casefold():
            placeholder_files.append(filename)
    if placeholder_files:
        raise SystemExit(
            "ERROR: unresolved scaffold/TODO content: "
            + ", ".join(placeholder_files)
        )
    return status


def add_topic(args: argparse.Namespace) -> int:
    root = project_root()
    sheet = _resolve(root, args.sheet)
    _check_new_topic(root, args.topic_id, args.title, sheet)
    pack_dir = topic_pack_dir(root, args.topic_id)

    create_args = argparse.Namespace(
        topic_id=args.topic_id,
        title=args.title,
        question_type=args.question_type,
        difficulty=args.difficulty,
        importance=args.importance,
        overwrite=False,
    )
    try:
        create_topic_pack(create_args)
        _write_draft_status(
            root,
            args.topic_id,
            sheet,
            generated=args.generate,
        )
        if args.generate:
            command = [
                sys.executable,
                "scripts/generate_topic_pack_from_sheet.py",
                "--topic-id",
                args.topic_id,
                "--sheet",
                _relative(root, sheet),
            ]
            if args.model:
                command.extend(["--model", args.model])
            _run(root, command)
            _write_draft_status(
                root,
                args.topic_id,
                sheet,
                generated=True,
            )
    except BaseException:
        if pack_dir.exists():
            shutil.rmtree(pack_dir)
            print("ROLLBACK: removed incomplete Topic Pack:", pack_dir)
        raise

    print("TOPIC WORKFLOW STARTED")
    print("topic_id:", args.topic_id)
    print("status: draft / human_review_required")
    print("NEXT:")
    print(
        " ",
        "python3 scripts/rubric_manager.py approve-topic",
        "--topic-id",
        args.topic_id,
        "--reviewer <reviewer_id>",
    )
    return 0


def approve_topic(args: argparse.Namespace) -> int:
    root = project_root()
    reviewer = args.reviewer.strip()
    if not reviewer:
        raise SystemExit("ERROR: non-empty --reviewer is required")
    _approval_precheck(root, args.topic_id)

    # Validate draft source without publishing generated output.
    _run(root, _release_command(args.topic_id, promote=False))

    pack_dir = topic_pack_dir(root, args.topic_id)
    status_path = pack_dir / "topic_status.json"
    previous_status = status_path.read_bytes() if status_path.exists() else None
    status = load_status(pack_dir, args.topic_id)
    status = update_status(
        status,
        set_status="approved",
        sync_hash=True,
        mark_validated=True,
        mark_reviewed=True,
        note=f"human approval by {reviewer}",
    )
    status.update(
        {
            "schema_version": "topic_status.v2",
            "workflow_contract": WORKFLOW_CONTRACT,
            "reviewer": reviewer,
            "review_method": "human",
            "approved_source_hash": status["content_hash"],
            "next_action": "Run integration validation before merge.",
        }
    )
    source_sheet = str(status.get("source_sheet") or "")
    if source_sheet:
        sheet = _resolve(root, source_sheet)
        if sheet.is_file():
            status["reviewed_sheet_hash"] = _sha256(sheet)
    write_status(pack_dir, status)

    try:
        _run(
            root,
            _release_command(
                args.topic_id,
                promote=True,
                smoke=args.smoke,
            ),
        )
    except BaseException:
        if previous_status is None:
            status_path.unlink(missing_ok=True)
        else:
            status_path.write_bytes(previous_status)
        print("ROLLBACK: restored pre-approval topic_status.json")
        raise

    print("TOPIC WORKFLOW APPROVED")
    print("topic_id:", args.topic_id)
    print("reviewer:", reviewer)
    print("source_hash:", load_status(pack_dir, args.topic_id).get("content_hash"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Machine-enforced Topic Pack authoring workflow."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add-topic", help="create a managed draft Topic Pack")
    add.add_argument("--topic-id", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--sheet", required=True)
    add.add_argument("--question-type", default="PRINCIPLE_INTERPRETATION")
    add.add_argument("--difficulty", default="FIELD_APPLICATION")
    add.add_argument("--importance", default="NORMAL")
    add.add_argument("--generate", action="store_true", help="run assisted JSON authoring")
    add.add_argument("--model", default=None)
    add.set_defaults(func=add_topic)

    approve = subparsers.add_parser(
        "approve-topic",
        help="record human approval and promote generated banks",
    )
    approve.add_argument("--topic-id", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--smoke", action="store_true")
    approve.set_defaults(func=approve_topic)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
