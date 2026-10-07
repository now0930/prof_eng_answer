#!/usr/bin/env python3
"""Interactively review and explicitly approve blocked managed Topic Packs.

This helper never edits approval metadata itself. After the operator reviews a
pack and enters its exact approval phrase, it delegates to the repository's
approve-topic workflow, which validates the pack and handles rollback.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topic_pack_status import iter_topic_ids, load_status, project_root, topic_pack_dir  # noqa: E402
from topic_pack_workflow_controller import managed_approval_errors  # noqa: E402


def _changed_paths(root: Path, topic_id: str) -> list[str]:
    proc = subprocess.run(
        [
            "git", "status", "--short", "--untracked-files=all", "--",
            f"rubrics/topic_packs/{topic_id}",
        ],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "git status failed")
    return proc.stdout.splitlines()


def _candidate_topics(root: Path, requested: list[str] | None) -> list[str]:
    topics = requested or iter_topic_ids(root)
    missing = [topic_id for topic_id in topics if not topic_pack_dir(root, topic_id).is_dir()]
    if missing:
        raise SystemExit("Unknown Topic Pack(s): " + ", ".join(missing))
    return [
        topic_id for topic_id in topics
        if managed_approval_errors(root, topic_id)
    ]


def _show_candidate(root: Path, topic_id: str) -> None:
    pack_dir = topic_pack_dir(root, topic_id)
    status = load_status(pack_dir, topic_id)
    print("\n" + "=" * 78)
    print(f"TOPIC: {topic_id}")
    print(f"STATUS: {status.get('status')} / {status.get('review_state')}")
    print(f"REVIEWER: {status.get('reviewer') or '(none recorded)'}")
    source_sheet = str(status.get("source_sheet") or "")
    print(f"SOURCE SHEET: {source_sheet or '(not recorded)'}")
    if source_sheet and (root / source_sheet).is_file():
        print(f"SOURCE SHEET FILE: {root / source_sheet}")
    print("APPROVAL BLOCKERS:")
    for error in managed_approval_errors(root, topic_id):
        print(f"  - {error}")
    changed = _changed_paths(root, topic_id)
    print("CHANGED FILES:")
    if changed:
        for row in changed:
            print(f"  {row}")
    else:
        print("  (no working-tree changes; approval metadata may be stale)")
    print("PACK DIRECTORY:")
    print(f"  {pack_dir}")
    print(
        "Review README.md, the source sheet, and fact_anchor/logic_check/"
        "model_answer/topic_importance JSON before approving."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "List blocked Topic Packs and, only after explicit operator confirmation, "
            "run the existing approve-topic workflow."
        )
    )
    parser.add_argument(
        "--topic-id", action="append", dest="topic_ids",
        help="limit review to this Topic Pack (repeatable; default: all blocked packs)",
    )
    parser.add_argument(
        "--reviewer", help="reviewer identity to record (prompted if omitted)",
    )
    parser.add_argument(
        "--list-only", action="store_true",
        help="show blocked packs and exit without prompting or changing files",
    )
    args = parser.parse_args(argv)

    root = project_root()
    candidates = _candidate_topics(root, args.topic_ids)
    if not candidates:
        print("No managed Topic Packs are blocked on approval.")
        return 0

    print(f"Blocked Topic Packs: {len(candidates)}")
    for topic_id in candidates:
        _show_candidate(root, topic_id)
    if args.list_only:
        print("\nList only: no files changed and no approvals recorded.")
        return 0
    if not sys.stdin.isatty():
        raise SystemExit("ERROR: approval mode requires an interactive terminal.")

    reviewer = (args.reviewer or input("\nReviewer name/ID to record: ")).strip()
    if not reviewer:
        raise SystemExit("ERROR: reviewer identity cannot be empty.")

    approved = 0
    skipped = 0
    for topic_id in candidates:
        print(f"\nReview {topic_id} in your editor before continuing.")
        reviewed = input("Have you personally reviewed the README and source JSON? Type yes: ").strip()
        if reviewed != "yes":
            print("SKIP: review was not confirmed.")
            skipped += 1
            continue
        phrase = input(f"To approve this pack, type exactly: APPROVE {topic_id}\n> ").strip()
        if phrase != f"APPROVE {topic_id}":
            print("SKIP: exact approval phrase did not match.")
            skipped += 1
            continue

        command = [
            sys.executable,
            str(root / "scripts" / "rubric_manager.py"),
            "approve-topic",
            "--topic-id", topic_id,
            "--reviewer", reviewer,
        ]
        print("\nRunning the repository approval workflow:")
        print(" ", " ".join(command))
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode:
            print(f"FAILED: {topic_id} (exit {result.returncode}); approval workflow was not completed.")
            return result.returncode
        approved += 1

    print(f"\nApproved: {approved}; skipped: {skipped}.")
    print("Run scripts/validate_release.sh again after all required packs are approved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
