#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topic_pack_status import iter_topic_ids, load_status, project_root, topic_pack_dir, update_status, write_status  # noqa: E402


def latest_review_report(root: Path, topic_id: str) -> str:
    reports = sorted((root / "reports").glob(f"topic_pack_gemini_review_{topic_id}_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(reports[0].relative_to(root)) if reports else ""


def select_topics(root: Path, args: argparse.Namespace) -> list[str]:
    topic_ids = args.topic_id or iter_topic_ids(root)
    selected: list[str] = []
    for topic_id in topic_ids:
        pack_dir = topic_pack_dir(root, topic_id)
        if not pack_dir.is_dir():
            raise SystemExit(f"ERROR: topic pack not found: {topic_id}")
        status = load_status(pack_dir, topic_id)
        if args.changed_only and not status.get("_changed"):
            print(f"SKIP unchanged: {topic_id}")
            continue
        if not args.include_frozen and status.get("status") == "frozen" and not status.get("_changed"):
            print(f"SKIP frozen unchanged: {topic_id}")
            continue
        selected.append(topic_id)
    return selected


def build_review_cmd(args: argparse.Namespace, topic_id: str) -> list[str]:
    cmd = [sys.executable, "scripts/rubric_manager.py", "review-topic-pack", "--topic-id", topic_id]
    for opt, value in [
        ("--model", args.model),
        ("--timeout", args.timeout),
        ("--temperature", args.temperature),
        ("--max-output-tokens", args.max_output_tokens),
        ("--max-context-chars", args.max_context_chars),
    ]:
        if value is not None:
            cmd.extend([opt, str(value)])
    return cmd


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Review multiple topic packs with Gemini.")
    p.add_argument("--topic-id", action="append", default=None)
    p.add_argument("--changed-only", action="store_true")
    p.add_argument("--include-frozen", action="store_true")
    p.add_argument("--keep-going", action="store_true")
    p.add_argument("--no-sync-status", action="store_true")
    p.add_argument("--model", default=None)
    p.add_argument("--timeout", type=int, default=None)
    p.add_argument("--temperature", type=float, default=None)
    p.add_argument("--max-output-tokens", type=int, default=None)
    p.add_argument("--max-context-chars", type=int, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = project_root()
    topics = select_topics(root, args)

    print("TOPIC PACK REVIEW ALL")
    print("topics:", len(topics))
    for topic_id in topics:
        print(" -", topic_id)

    failures: list[tuple[str, int]] = []
    model_name = args.model or os.getenv("TOPIC_REVIEW_GEMINI_MODEL") or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

    for topic_id in topics:
        cmd = build_review_cmd(args, topic_id)
        print()
        print("RUN:", " ".join(cmd))
        rc = subprocess.run(cmd, cwd=root).returncode
        if rc != 0:
            failures.append((topic_id, rc))
            if not args.keep_going:
                break
            continue

        if not args.no_sync_status:
            pack_dir = topic_pack_dir(root, topic_id)
            status = load_status(pack_dir, topic_id)
            status = update_status(status, set_status="reviewed", sync_hash=True, mark_reviewed=True, review_model=model_name, review_report=latest_review_report(root, topic_id))
            write_status(pack_dir, status)
            print("updated status:", pack_dir / "topic_status.json")

    print()
    print("TOPIC PACK REVIEW ALL SUMMARY")
    print("reviewed:", len(topics) - len(failures))
    print("failed:", len(failures))
    for topic_id, rc in failures:
        print(f" - {topic_id}: rc={rc}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
