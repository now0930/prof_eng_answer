#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_CSV = ROOT / "reports/fact_anchor_quality_audit.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_terms_manual_review.csv"
OUT_MD = ROOT / "reports/fact_anchor_support_terms_manual_review.md"

def guess_decision(term: str) -> tuple[str, str]:
    remove_patterns = [
        "비교축을 명확히 제시한다",
        "정확히 제시한다",
        "명확히 설명한다",
        "단계적으로 제시한다",
        "답안",
        "모범",
        "설명하시오",
    ]

    rewrite_patterns = [
        "연결한다",
        "고려한다",
        "확인한다",
        "설명한다",
        "제시한다",
        "구분하여 설명한다",
        "비교축으로 삼는다",
        "혼동하지 않는다",
    ]

    if any(p in term for p in remove_patterns):
        return "remove_candidate", "답안 작성 행위/채점 표현에 가까움"

    if any(p in term for p in rewrite_patterns):
        return "rewrite_candidate", "fact 의미는 있으나 문장형이므로 명사구화 필요"

    return "keep_candidate", "장문이지만 현장 표현일 수 있어 검토 필요"

def main() -> int:
    with AUDIT_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    targets = [
        r for r in rows
        if r.get("severity") == "MINOR"
        and r.get("field") == "support_terms"
        and "문장형" in r.get("message", "")
    ]

    out = []
    for r in targets:
        term = r.get("value", "")
        decision, reason = guess_decision(term)
        out.append({
            "decision": decision,
            "topic_id": r.get("topic_id", ""),
            "anchor_id": r.get("anchor_id", ""),
            "old_term": term,
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

    by_topic = Counter(r["topic_id"] for r in out)
    by_decision = Counter(r["decision"] for r in out)

    grouped = defaultdict(list)
    for r in out:
        grouped[r["topic_id"]].append(r)

    lines = []
    lines.append("# Fact Anchor Support Terms Manual Review")
    lines.append("")
    lines.append(f"- total: {len(out)}")
    lines.append("")
    lines.append("## Decision summary")
    lines.append("")
    for k, v in by_decision.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Topic summary")
    lines.append("")
    for topic, count in by_topic.most_common():
        lines.append(f"- {topic}: {count}")
    lines.append("")
    lines.append("## Review items")
    lines.append("")

    for topic, items in grouped.items():
        lines.append(f"### {topic}")
        lines.append("")
        for r in items:
            lines.append(f"- `{r['anchor_id']}` [{r['decision']}] {r['old_term']}")
            lines.append(f"  - reason: {r['reason']}")
            lines.append("  - new_term: ")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("manual review terms:", len(out))
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_MD)
    print()
    print("[by decision]")
    for k, v in by_decision.most_common():
        print(f"{k}: {v}")
    print()
    print("[by topic]")
    for k, v in by_topic.most_common(30):
        print(f"{v:3} | {k}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
