#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "reports/fact_anchor_support_term_rewrite_candidates.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_term_rewrite_candidates_strict.csv"

UNSAFE_FRAGMENTS = [
    "해야",
    "할 수",
    "하지 말고",
    "필요함",
    "필요하다",
    "고려한다",
    "연결한다",
    "제시한다",
    "설명한다",
    "비교한다",
    "구분한다",
    "포함한다",
    "언급한다",
    "평가한다",
    "검토한다",
    "작성한다",
    "쓴다",
    "삼는다",
    "설정한다",
    "정확히",
    "명확히",
    "단계적으로",
]

def strict_action(row: dict[str, str]) -> str:
    if row.get("action") != "rewrite":
        return "manual_review"

    suggested = row.get("suggested_terms", "").strip()

    if not suggested:
        return "manual_review"

    if len(suggested) > 45:
        return "manual_review"

    if any(x in suggested for x in UNSAFE_FRAGMENTS):
        return "manual_review"

    # 조사/동사형 잔재가 강하면 보류
    if suggested.endswith(("한다", "된다", "있다", "없다", "이다", "함", "것")):
        return "manual_review"

    return "safe_rewrite"

def main() -> int:
    with IN_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    out = []
    for r in rows:
        new_action = strict_action(r)
        out.append({
            "action": new_action,
            "old_action": r.get("action", ""),
            "topic_id": r.get("topic_id", ""),
            "anchor_id": r.get("anchor_id", ""),
            "old_term": r.get("old_term", ""),
            "suggested_terms": r.get("suggested_terms", ""),
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["action", "old_action", "topic_id", "anchor_id", "old_term", "suggested_terms"],
        )
        writer.writeheader()
        writer.writerows(out)

    print("wrote:", OUT_CSV)
    print()
    print("[by action]")
    for k, v in Counter(r["action"] for r in out).most_common():
        print(f"{k}: {v}")

    print()
    print("[safe_rewrite sample]")
    for r in [x for x in out if x["action"] == "safe_rewrite"][:100]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['suggested_terms']}")

    print()
    print("[manual_review sample]")
    for r in [x for x in out if x["action"] == "manual_review"][:60]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['suggested_terms']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
