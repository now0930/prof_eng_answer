#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
AUDIT_CSV = ROOT / "reports/fact_anchor_quality_audit.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_terms_final_review.csv"
OUT_MD = ROOT / "reports/fact_anchor_support_terms_final_review.md"

def classify(term: str) -> tuple[str, str]:
    remove_hits = [
        "명확히 설명한다",
        "정확히 설명한다",
        "정확히 제시한다",
        "단계적으로 제시한다",
        "쓴다",
        "답안",
        "모범",
    ]
    rewrite_hits = [
        "연결된다",
        "설정한다",
        "확인한다",
        "고려한다",
        "설명한다",
        "구분하여 설명한다",
        "혼동하지 않는다",
    ]

    if any(x in term for x in remove_hits):
        return "remove_or_rewrite", "답안 작성 행위 표현 가능성"
    if any(x in term for x in rewrite_hits):
        return "rewrite", "fact 의미는 있으나 문장형"
    return "keep_or_exception", "현장 표현 또는 장문 키워드 가능성"

def main() -> int:
    with AUDIT_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    targets = [
        r for r in rows
        if r.get("severity") == "MINOR"
        and r.get("field") == "support_terms"
    ]

    out = []
    for r in targets:
        decision, reason = classify(r["value"])
        out.append({
            "decision": decision,
            "topic_id": r["topic_id"],
            "anchor_id": r["anchor_id"],
            "old_term": r["value"],
            "new_term": "",
            "reason": reason,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["decision", "topic_id", "anchor_id", "old_term", "new_term", "reason"],
        )
        writer.writeheader()
        writer.writerows(out)

    lines = []
    lines.append("# Final Fact Anchor Support Terms Review")
    lines.append("")
    lines.append(f"- total: {len(out)}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for k, v in Counter(r["decision"] for r in out).most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Items")
    lines.append("")
    for r in out:
        lines.append(f"### {r['topic_id']} / {r['anchor_id']}")
        lines.append(f"- decision: {r['decision']}")
        lines.append(f"- old_term: {r['old_term']}")
        lines.append(f"- new_term: ")
        lines.append(f"- reason: {r['reason']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("final review terms:", len(out))
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_MD)
    print()
    for k, v in Counter(r["decision"] for r in out).most_common():
        print(f"{k}: {v}")

if __name__ == "__main__":
    raise SystemExit(main())
