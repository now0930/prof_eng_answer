#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
OUT_MD = ROOT / "reports/fact_anchor_quality_audit.md"
OUT_CSV = ROOT / "reports/fact_anchor_quality_audit.csv"

SENTENCE_PATTERNS = [
    "설명한다",
    "설명해야",
    "제시한다",
    "정리한다",
    "구분한다",
    "비교한다",
    "연결한다",
    "포함한다",
    "언급한다",
    "평가한다",
    "검토한다",
    "작성한다",
    "해야 한다",
    "할 수 있다",
]

POLLUTION_PATTERNS = [
    "모범 답안",
    "모범답안",
    "설명하시오",
    "비교하시오",
    "논하시오",
    "서술하시오",
    "작성하시오",
    "기술하시오",
    "고득점",
    "high_score",
    "model_answer",
    "expected_structure",
    "outline",
    "출제",
]

def load_topics(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ["topics", "fact_anchors", "items", "data"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        # 단일 topic 파일 가능성
        if "topic_id" in data and "anchors" in data:
            return [data]
    raise SystemExit("ERROR: unsupported fact anchor json structure")

def text_len(s: Any) -> int:
    return len(str(s or "").strip())

def has_any(text: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if p in text]

def is_sentence_like(term: str) -> bool:
    term = term.strip()
    if len(term) >= 45:
        return True
    if any(p in term for p in SENTENCE_PATTERNS):
        return True
    if term.endswith(("다.", "다", "함", "해야 함", "할 것")) and len(term) >= 18:
        return True
    return False

def add_issue(
    issues: list[dict[str, str]],
    severity: str,
    topic_id: str,
    anchor_id: str,
    field: str,
    message: str,
    value: Any = "",
) -> None:
    issues.append({
        "severity": severity,
        "topic_id": topic_id,
        "anchor_id": anchor_id,
        "field": field,
        "message": message,
        "value": str(value)[:700],
    })

def main() -> int:
    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    issues: list[dict[str, str]] = []

    topic_ids = [str(t.get("topic_id", "")).strip() for t in topics]
    topic_counter = Counter(topic_ids)

    for topic_id, cnt in topic_counter.items():
        if not topic_id:
            add_issue(issues, "MAJOR", "", "", "topic_id", "topic_id 없음")
        elif cnt > 1:
            add_issue(issues, "MAJOR", topic_id, "", "topic_id", f"topic_id 중복: {cnt}")

    for topic in topics:
        topic_id = str(topic.get("topic_id", "")).strip()
        anchors = topic.get("anchors", [])

        if not isinstance(anchors, list):
            add_issue(issues, "MAJOR", topic_id, "", "anchors", "anchors가 list가 아님")
            continue

        if len(anchors) != 5:
            add_issue(issues, "MAJOR", topic_id, "", "anchors", f"anchors 개수 {len(anchors)}개, 권장 5개")

        ids = [str(a.get("id", "")).strip() for a in anchors if isinstance(a, dict)]
        expected_ids = [f"F{i}" for i in range(1, 6)]
        if len(anchors) == 5 and ids != expected_ids:
            add_issue(issues, "MINOR", topic_id, "", "anchors.id", f"anchor id 순서가 F1~F5가 아님: {ids}")

        for idx, anchor in enumerate(anchors, 1):
            if not isinstance(anchor, dict):
                add_issue(issues, "MAJOR", topic_id, f"F{idx}", "anchor", "anchor가 object가 아님")
                continue

            anchor_id = str(anchor.get("id", f"F{idx}")).strip()
            expected = str(anchor.get("expected", "")).strip()
            core_terms = anchor.get("core_terms", [])
            support_terms = anchor.get("support_terms", [])

            if not expected:
                add_issue(issues, "MAJOR", topic_id, anchor_id, "expected", "expected 없음")
            elif text_len(expected) < 20:
                add_issue(issues, "MINOR", topic_id, anchor_id, "expected", "expected가 너무 짧음", expected)
            elif text_len(expected) > 220:
                add_issue(issues, "MINOR", topic_id, anchor_id, "expected", "expected가 너무 김", expected)

            if not isinstance(core_terms, list):
                add_issue(issues, "MAJOR", topic_id, anchor_id, "core_terms", "core_terms가 list가 아님")
                core_terms = []

            if not isinstance(support_terms, list):
                add_issue(issues, "MAJOR", topic_id, anchor_id, "support_terms", "support_terms가 list가 아님")
                support_terms = []

            if len(core_terms) < 3:
                add_issue(issues, "MINOR", topic_id, anchor_id, "core_terms", f"core_terms가 적음: {len(core_terms)}")
            if len(core_terms) > 15:
                add_issue(issues, "MINOR", topic_id, anchor_id, "core_terms", f"core_terms가 많음: {len(core_terms)}")

            if len(support_terms) > 25:
                add_issue(issues, "MINOR", topic_id, anchor_id, "support_terms", f"support_terms가 많음: {len(support_terms)}")

            core_set = {str(x).strip() for x in core_terms if str(x).strip()}
            support_set = {str(x).strip() for x in support_terms if str(x).strip()}

            overlap = sorted(core_set & support_set)
            if overlap:
                add_issue(issues, "MINOR", topic_id, anchor_id, "core/support", "core_terms와 support_terms 중복", ", ".join(overlap[:20]))

            for term in core_terms:
                term = str(term).strip()
                if not term:
                    add_issue(issues, "MINOR", topic_id, anchor_id, "core_terms", "빈 core_term")
                    continue
                polluted = has_any(term, POLLUTION_PATTERNS)
                if polluted:
                    add_issue(issues, "MAJOR", topic_id, anchor_id, "core_terms", f"core_term에 오염 패턴 포함: {polluted}", term)
                elif is_sentence_like(term):
                    add_issue(issues, "MINOR", topic_id, anchor_id, "core_terms", "core_term이 문장형 또는 과도하게 김", term)

            for term in support_terms:
                term = str(term).strip()
                if not term:
                    add_issue(issues, "MINOR", topic_id, anchor_id, "support_terms", "빈 support_term")
                    continue
                polluted = has_any(term, POLLUTION_PATTERNS)
                if polluted:
                    add_issue(issues, "MAJOR", topic_id, anchor_id, "support_terms", f"support_term에 오염 패턴 포함: {polluted}", term)
                elif is_sentence_like(term):
                    add_issue(issues, "MINOR", topic_id, anchor_id, "support_terms", "support_term이 문장형 또는 과도하게 김", term)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "severity",
                "topic_id",
                "anchor_id",
                "field",
                "message",
                "value",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(issues)

    by_sev = Counter(i["severity"] for i in issues)
    by_field = Counter(i["field"] for i in issues)

    try:
        source_display = FACT_PATH.relative_to(ROOT)
    except ValueError:
        source_display = FACT_PATH

    lines = []
    lines.append("# Fact Anchor Quality Audit")
    lines.append("")
    lines.append(f"- source: `{source_display}`")
    lines.append(f"- topics: {len(topics)}")
    lines.append(f"- issues: {len(issues)}")
    lines.append(f"- MAJOR: {by_sev.get('MAJOR', 0)}")
    lines.append(f"- MINOR: {by_sev.get('MINOR', 0)}")
    lines.append("")
    lines.append("## By field")
    lines.append("")
    for k, v in by_field.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Top issues")
    lines.append("")
    for issue in issues[:120]:
        lines.append(f"### {issue['severity']} / {issue['topic_id']} / {issue['anchor_id']} / {issue['field']}")
        lines.append(f"- message: {issue['message']}")
        if issue["value"]:
            lines.append(f"- value: `{issue['value']}`")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("topics:", len(topics))
    print("issues:", len(issues))
    print("MAJOR:", by_sev.get("MAJOR", 0))
    print("MINOR:", by_sev.get("MINOR", 0))
    print("wrote:", OUT_MD)
    print("wrote:", OUT_CSV)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
