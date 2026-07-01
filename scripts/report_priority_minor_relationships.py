#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "reports/model_answer_relationship_validation.csv"
OUT_PATH = ROOT / "reports/model_answer_relationship_priority_minors.md"

PRIORITY_KEYWORDS = [
    "동일 문장",
    "연결이 약한",
    "근거 약함",
    "전개 순서",
]

def to_float(value: str) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None

def priority_of(row: dict[str, str]) -> str | None:
    """Return priority only for actionable P1 issues.

    Policy:
    - MAJOR is handled by validate-all / --fail-on-major.
    - P1 is actionable cleanup.
    - P2/P3 are advisory because outline/high-score matching can be intentionally loose.
    """
    if row.get("severity") != "MINOR":
        return None

    score = to_float(row.get("score", ""))

    if score is not None and score <= 0.60:
        return "P1_score_le_0.60"

    text = " ".join([
        row.get("message", ""),
        row.get("detail", ""),
    ])

    if "동일 문장" in text:
        return "P1_role_overlap"

    return None

def main() -> int:
    if not CSV_PATH.exists():
        raise SystemExit(f"ERROR: missing report: {CSV_PATH}")

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    minors = [r for r in rows if r.get("severity") == "MINOR"]

    picked = []
    for r in minors:
        p = priority_of(r)
        if p:
            r = dict(r)
            r["priority"] = p
            picked.append(r)

    picked.sort(key=lambda r: (
        r["priority"],
        to_float(r.get("score", "")) if to_float(r.get("score", "")) is not None else 9.9,
        r.get("answer_id", ""),
    ))

    by_priority = Counter(r["priority"] for r in picked)
    by_relation = Counter(r["relation"] for r in picked)
    by_answer = defaultdict(list)
    for r in picked:
        by_answer[r["answer_id"]].append(r)

    lines = []
    lines.append("# Priority MINOR relationship issues")
    lines.append("")
    lines.append(f"- source: `{CSV_PATH.relative_to(ROOT)}`")
    lines.append(f"- total MINOR: {len(minors)}")
    lines.append(f"- picked priority MINOR: {len(picked)}")
    lines.append("")
    lines.append("## By priority")
    lines.append("")
    for k, v in by_priority.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## By relation")
    lines.append("")
    for k, v in by_relation.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Targets")
    lines.append("")

    for answer_id, items in sorted(by_answer.items()):
        topic_id = items[0].get("topic_id", "")
        lines.append(f"### {answer_id}")
        lines.append(f"- topic_id: `{topic_id}`")
        for r in items:
            score = r.get("score") or "-"
            lines.append(f"- {r['priority']} / `{r['relation']}` / score={score}")
            lines.append(f"  - message: {r.get('message', '')}")
            detail = r.get("detail", "")
            if detail:
                lines.append(f"  - detail: {detail[:700]}")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("total MINOR:", len(minors))
    print("priority MINOR:", len(picked))
    print("by priority:")
    for k, v in by_priority.most_common():
        print(f"- {k}: {v}")
    print("by relation:")
    for k, v in by_relation.most_common():
        print(f"- {k}: {v}")
    print("wrote:", OUT_PATH)

    print()
    print("top targets:")
    for answer_id, items in list(sorted(by_answer.items()))[:30]:
        scores = [x.get("score") or "-" for x in items]
        print(f"- {answer_id} | issues={len(items)} | scores={','.join(scores)}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
