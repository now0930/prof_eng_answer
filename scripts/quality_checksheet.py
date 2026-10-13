#!/usr/bin/env python3
"""List and triage private grading-quality checksheets; never change a grade."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.quality.operational_checksheet import (
    add_manual_issue, advance_issue, load_quality_checksheet, reclassify_issue,
    save_quality_checksheet,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="Summarize private session issues")
    listing.add_argument("--sessions-root", type=Path, default=ROOT / "data/sessions")
    export = commands.add_parser("export", help="Save a private CSV issue checklist")
    export.add_argument("--sessions-root", type=Path, default=ROOT / "data/sessions")
    export.add_argument("--output", required=True, type=Path)
    show = commands.add_parser("show", help="Display issue IDs/status without answer text")
    show.add_argument("--session", required=True, type=Path)
    add = commands.add_parser("add", help="Record a manually observed problem")
    add.add_argument("--session", required=True, type=Path)
    add.add_argument("--category", required=True, choices=[
        "benchmark_conflict", "false_high", "false_low", "wrong_route", "missing_fact",
        "source_conflict", "formatting", "other",
    ])
    add.add_argument("--priority", required=True, choices=["P0", "P1", "P2", "P3"])
    add.add_argument("--note", required=True)
    update = commands.add_parser("advance", help="Record triage/fix/retest/closure")
    update.add_argument("--session", required=True, type=Path)
    update.add_argument("--issue-id", required=True)
    update.add_argument("--status", required=True, choices=[
        "triaged", "deferred", "fix_pending_retest", "retested", "closed",
    ])
    update.add_argument("--note", required=True)
    update.add_argument("--fix-reference")
    update.add_argument("--retest-session", type=Path)
    classify = commands.add_parser("reclassify", help="Correct a premature issue category")
    classify.add_argument("--session", required=True, type=Path)
    classify.add_argument("--issue-id", required=True)
    classify.add_argument("--category", required=True, choices=[
        "benchmark_conflict", "false_high", "false_low", "wrong_route", "missing_fact",
        "source_conflict", "formatting", "other",
    ])
    classify.add_argument("--note", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            output_path = args.output
            if (not output_path.is_absolute()
                    or output_path.resolve().is_relative_to(ROOT)
                    or output_path.exists() or output_path.is_symlink()
                    or not output_path.parent.is_dir()):
                raise ValueError("CSV export must be a new private path outside repository")
            if not args.sessions_root.is_dir():
                raise ValueError("sessions root is missing")
            fields = ("session_id", "topic_id", "issue_id", "check_id", "category",
                      "priority", "status", "finding", "review_note", "fix_reference",
                      "retest_sheet_sha256", "updated_at")
            rows = []
            for path in sorted(args.sessions_root.glob("*/quality_checksheet.json")):
                sheet = load_quality_checksheet(path.parent)
                rows.extend({**{field: issue.get(field) for field in fields},
                             "session_id": path.parent.name,
                             "topic_id": sheet["topic_id"]}
                            for issue in sheet["issues"])
            descriptor = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            output = {"exported_issues": len(rows), "private_csv": str(output_path)}
        elif args.command == "list":
            if not args.sessions_root.is_dir():
                raise ValueError("sessions root is missing")
            status = Counter()
            topics = Counter()
            sessions = 0
            for path in sorted(args.sessions_root.glob("*/quality_checksheet.json")):
                sheet = load_quality_checksheet(path.parent)
                sessions += 1
                for issue in sheet["issues"]:
                    status[issue["status"]] += 1
                    if issue["status"] != "closed":
                        topics[sheet["topic_id"]] += 1
            output = {"sessions": sessions, "issue_status": dict(status),
                      "open_by_topic": dict(topics)}
        elif args.command == "show":
            sheet = load_quality_checksheet(args.session)
            output = {"topic_id": sheet["topic_id"],
                      "checks": [{"check_id": row["check_id"], "result": row["result"]}
                                 for row in sheet["checks"]],
                      "issues": [{"issue_id": row["issue_id"], "category": row["category"],
                                  "priority": row["priority"], "status": row["status"]}
                                 for row in sheet["issues"]]}
        elif args.command == "add":
            sheet = load_quality_checksheet(args.session)
            add_manual_issue(sheet, category=args.category, priority=args.priority,
                             note=args.note)
            save_quality_checksheet(args.session, sheet, overwrite=True)
            output = {"issue_id": sheet["issues"][-1]["issue_id"], "status": "open"}
        elif args.command == "reclassify":
            sheet = load_quality_checksheet(args.session)
            reclassify_issue(sheet, issue_id=args.issue_id,
                             category=args.category, note=args.note)
            save_quality_checksheet(args.session, sheet, overwrite=True)
            output = {"issue_id": args.issue_id, "category": args.category}
        else:
            sheet = load_quality_checksheet(args.session)
            retest = (load_quality_checksheet(args.retest_session)
                      if args.retest_session else None)
            advance_issue(sheet, issue_id=args.issue_id, status=args.status,
                          note=args.note, fix_reference=args.fix_reference,
                          retest_sheet=retest)
            save_quality_checksheet(args.session, sheet, overwrite=True)
            output = {"issue_id": args.issue_id, "status": args.status}
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        # Do not print a private answer, note, or filesystem path from an exception.
        print(json.dumps({"ok": False, "error_type": type(error).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
