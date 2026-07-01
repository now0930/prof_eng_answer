#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_CSV = ROOT / "reports/fact_anchor_quality_audit.csv"
OUT_CSV = ROOT / "reports/fact_anchor_support_term_rewrite_candidates.csv"

VERB_SUFFIXES = [
    "을 설명한다",
    "를 설명한다",
    "을 제시한다",
    "를 제시한다",
    "을 정리한다",
    "를 정리한다",
    "을 구분한다",
    "를 구분한다",
    "을 비교한다",
    "를 비교한다",
    "을 포함한다",
    "를 포함한다",
    "을 평가한다",
    "를 평가한다",
    "을 검토한다",
    "를 검토한다",
    "을 작성한다",
    "를 작성한다",
    "을 언급한다",
    "를 언급한다",
    "해야 한다",
    "할 수 있다",
]

def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip(" .")

def propose(term: str) -> tuple[str, str]:
    original = normalize_spaces(term)

    s = original
    action = "review"

    for suffix in VERB_SUFFIXES:
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            action = "rewrite"
            break

    s = normalize_spaces(s)

    # 너무 긴 문장을 그대로 남기지 않기 위한 보수적 후처리
    s = s.replace(" 및 ", "·")
    s = s.replace(" 또는 ", "·")
    s = s.replace("와 ", "와 ")
    s = s.replace("과 ", "과 ")

    # 'A와 B 비교' 형태 보정
    if original.endswith(("을 비교한다", "를 비교한다")) and not s.endswith("비교"):
        s = normalize_spaces(s + " 비교")

    if original.endswith(("을 구분한다", "를 구분한다")) and not s.endswith("구분"):
        s = normalize_spaces(s + " 구분")

    if original.endswith(("을 평가한다", "를 평가한다")) and not s.endswith("평가"):
        s = normalize_spaces(s + " 평가")

    if original.endswith(("을 검토한다", "를 검토한다")) and not s.endswith("검토"):
        s = normalize_spaces(s + " 검토")

    if original.endswith(("을 작성한다", "를 작성한다")) and not s.endswith("작성"):
        s = normalize_spaces(s + " 작성")

    # 여전히 문장 냄새가 강하거나 너무 길면 수동 검토로 표시
    if len(s) > 45 or any(x in s for x in ["설명", "제시", "정리", "포함", "언급"]):
        action = "manual_review"

    if not s or s == original:
        action = "manual_review"

    return action, s

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
    seen = set()

    for r in targets:
        key = (r["topic_id"], r["anchor_id"], r["value"])
        if key in seen:
            continue
        seen.add(key)

        old = r["value"]
        action, suggested = propose(old)

        out.append({
            "action": action,
            "topic_id": r["topic_id"],
            "anchor_id": r["anchor_id"],
            "old_term": old,
            "suggested_terms": suggested,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["action", "topic_id", "anchor_id", "old_term", "suggested_terms"],
        )
        writer.writeheader()
        writer.writerows(out)

    print("candidates:", len(out))
    print("wrote:", OUT_CSV)

    from collections import Counter
    print()
    print("[by action]")
    for k, v in Counter(r["action"] for r in out).most_common():
        print(f"{k}: {v}")

    print()
    print("[sample]")
    for r in out[:80]:
        print(f"- {r['action']} | {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['suggested_terms']}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
