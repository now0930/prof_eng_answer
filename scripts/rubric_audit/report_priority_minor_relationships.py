#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN_CSV = ROOT / "reports/model_answer_relationship_minor_analysis.csv"
OUT_MD = ROOT / "reports/model_answer_relationship_priority_minors.md"

PRIORITY_LEVELS = {"P1", "P2"}


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(
            f"ERROR: missing {path}\n"
            "Run first: "
            "python3 scripts/rubric_audit/"
            "analyze_model_answer_relationship_minors.py"
        )

    with path.open(
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    if rows and "priority" not in rows[0]:
        raise SystemExit(
            f"ERROR: missing priority column in {path}"
        )

    return rows


def select_priority_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if (row.get("priority") or "").strip().upper()
        in PRIORITY_LEVELS
    ]

    order = {"P1": 0, "P2": 1}

    selected.sort(
        key=lambda row: (
            order.get(
                (row.get("priority") or "").upper(),
                9,
            ),
            row.get("topic_id") or "",
            row.get("answer_id") or "",
            row.get("action") or "",
        )
    )

    return selected


def write_report(
    path: Path,
    all_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
) -> None:
    counts = Counter(
        (row.get("priority") or "").strip().upper()
        for row in priority_rows
    )

    lines = [
        "# Model Answer Relationship Priority MINORs",
        "",
        f"- priority MINOR: {len(priority_rows)}",
        f"- P1: {counts.get('P1', 0)}",
        f"- P2: {counts.get('P2', 0)}",
        f"- analyzed MINOR: {len(all_rows)}",
        "",
        "P1과 P2만 운영 전 해소가 필요한 priority MINOR로 집계한다.",
        "P3는 advisory로 유지할 수 있다.",
        "",
        "## Items",
        "",
    ]

    if not priority_rows:
        lines.append("- 없음")
    else:
        for row in priority_rows:
            priority = (
                row.get("priority") or ""
            ).strip().upper()
            answer_id = (
                row.get("answer_id") or ""
            ).strip()
            topic_id = (
                row.get("topic_id") or ""
            ).strip()
            action = (
                row.get("action") or ""
            ).strip()
            score = (
                row.get("score") or ""
            ).strip()
            message = (
                row.get("message") or ""
            ).strip()
            action_reason = (
                row.get("action_reason") or ""
            ).strip()

            lines.extend(
                [
                    f"### {priority} / {answer_id}",
                    "",
                    f"- topic_id: `{topic_id}`",
                    f"- action: `{action}`",
                    f"- score: `{score}`",
                    f"- message: {message}",
                    f"- suggested_action: {action_reason}",
                    "",
                ]
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def main() -> int:
    rows = load_rows(IN_CSV)
    priority_rows = select_priority_rows(rows)
    write_report(
        OUT_MD,
        rows,
        priority_rows,
    )

    counts = Counter(
        (row.get("priority") or "").strip().upper()
        for row in priority_rows
    )

    print(f"priority MINOR: {len(priority_rows)}")
    print(f"P1: {counts.get('P1', 0)}")
    print(f"P2: {counts.get('P2', 0)}")
    print("wrote:", OUT_MD)

    return 1 if priority_rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
