#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "reports/fact_anchor_support_terms_manual_review.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_terms_manual_review_resolved.csv"

def clean_term(term: str) -> str:
    s = term.strip()

    replacements = [
        ("정확히 ", ""),
        ("명확히 ", ""),
        ("단계적으로 ", ""),
        ("구분하여 설명한다", "구분"),
        ("연결하여 설명한다", "연계"),
        ("으로 연결한다", " 연계"),
        ("로 연결한다", " 연계"),
        ("과 연결한다", "과 연계"),
        ("와 연결한다", "와 연계"),
        ("까지 연결한다", "까지 연계"),
        ("을 고려한다", " 고려"),
        ("를 고려한다", " 고려"),
        ("을 확인한다", " 확인"),
        ("를 확인한다", " 확인"),
        ("여부를 확인한다", "여부 확인"),
        ("한다고 쓴다", ""),
        ("을 혼동하지 않는다", " 구분"),
        ("를 혼동하지 않는다", " 구분"),
        ("을 비교축으로 삼는다", " 비교축"),
        ("를 비교축으로 삼는다", " 비교축"),
        ("을 설명한다", ""),
        ("를 설명한다", ""),
        ("을 제시한다", ""),
        ("를 제시한다", ""),
        ("을 구분한다", " 구분"),
        ("를 구분한다", " 구분"),
        ("을 포함한다", ""),
        ("를 포함한다", ""),
        ("을 언급한다", ""),
        ("를 언급한다", ""),
        ("을 평가한다", " 평가"),
        ("를 평가한다", " 평가"),
        ("을 검토한다", " 검토"),
        ("를 검토한다", " 검토"),
        ("해야 함을 설명한다", " 필요성"),
        ("할 수 있음을 고려한다", " 가능성 고려"),
    ]

    for old, new in replacements:
        s = s.replace(old, new)

    s = s.replace(" 및 ", "·")
    s = s.replace(" 또는 ", "·")
    s = s.replace(", ", ", ")
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" .")

    # 남은 어미 정리
    s = re.sub(r"\s*한다$", "", s)
    s = re.sub(r"\s*된다$", "", s)
    s = re.sub(r"\s*있다$", "", s)
    s = re.sub(r"\s*없다$", "", s)
    s = s.strip(" .")

    return s

def main() -> int:
    with IN_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    out = []

    for r in rows:
        decision = r["decision"]
        old = r["old_term"].strip()

        new_term = ""

        if decision == "rewrite_candidate":
            new_term = clean_term(old)
        elif decision == "keep_candidate":
            new_term = old
        elif decision == "remove_candidate":
            new_term = ""

        out.append({
            "decision": decision,
            "topic_id": r["topic_id"],
            "anchor_id": r["anchor_id"],
            "old_term": old,
            "new_term": new_term,
            "reason": r["reason"],
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["decision", "topic_id", "anchor_id", "old_term", "new_term", "reason"],
        )
        writer.writeheader()
        writer.writerows(out)

    print("wrote:", OUT_CSV)
    print()
    print("[by decision]")
    for k, v in Counter(r["decision"] for r in out).most_common():
        print(f"{k}: {v}")

    print()
    print("[rewrite preview]")
    for r in [x for x in out if x["decision"] == "rewrite_candidate"][:80]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['new_term']}")

    print()
    print("[remove preview]")
    for r in [x for x in out if x["decision"] == "remove_candidate"]:
        print(f"- {r['topic_id']} / {r['anchor_id']} :: {r['old_term']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
