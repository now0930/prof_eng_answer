#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SRC = ROOT / "wordpress_docs" / "industrial_instrumentation_posts.json"
DEFAULT_DECISIONS = ROOT / "wordpress_docs" / "review_decisions" / "batch_001_decisions.tsv"
DEFAULT_OUT = ROOT / "wordpress_docs" / "rubric_work_packs" / "batch_001_priority_003_006_010.md"


QUESTION_TYPE_HINTS = {
    "temperature_measurement_error_heat_transfer": "CAUSE_ACTION",
    "temperature_sensor_immersion_depth_error": "PROCEDURE",
    "inverter_dc_to_ac_commutation": "PRINCIPLE",
    "nand_nor_universal_gate_logic": "PRINCIPLE",
    "power_semiconductor_switch_thyristor_gto_compare": "COMPARE",
    "ip_controller_purpose_implementation": "PRINCIPLE",
}


def clean_text(value: str) -> str:
    value = value or ""
    value = html.unescape(value)
    value = re.sub(r"<!--\s*/?wp:[^>]*?-->", "\n", value)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\r\n?", "\n", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def parse_nos(value: str) -> set[int]:
    result: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        result.add(int(part))
    return result


def load_posts(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("ERROR: WordPress JSON must be a list")
    return {str(post.get("id")): post for post in data}


def load_decisions(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not reader.fieldnames or "no" not in reader.fieldnames:
            raise SystemExit("ERROR: decisions file must be TSV with header including 'no'")
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def make_pack(rows: list[dict[str, str]], posts: dict[str, dict[str, Any]], max_chars: int) -> str:
    lines: list[str] = []

    lines.extend([
        "# Rubric Work Pack - Batch 001 Priority Items",
        "",
        "아래 WordPress 글을 기반으로 Rubric Bank 후보를 작성한다.",
        "",
        "## 작업 원칙",
        "",
        "1. Model Answer Bank는 20점대 모범답안 기준으로 작성한다.",
        "2. Fact Anchor는 키워드 암기가 아니라 채점 가능한 핵심 fact 기준으로 작성한다.",
        "3. 설치·안전·방폭·접지 주제는 법령·기준 근거가 필요하지만, 이번 3개는 원리·오차·시공 방법 중심으로 처리한다.",
        "4. 기존 topic과 중복되면 새 topic을 만들지 말고 MERGE_EXISTING으로 돌린다.",
        "5. 각 항목마다 다음을 판단한다.",
        "",
        "| 항목 | 작성 내용 |",
        "|---|---|",
        "| keep_or_merge | NEW topic 유지 또는 기존 topic 병합 여부 |",
        "| question_type | DEFINE / PRINCIPLE / STRUCTURE / COMPARE / PROBLEM_SOLVE / CAUSE_ACTION / PROCEDURE / CALC_DESIGN / APPLICATION / EVALUATION 중 선택 |",
        "| model_answer_outline | 20점대 답안의 핵심 구조 |",
        "| fact_anchors | 5개 이내, 채점 가능한 핵심 fact |",
        "| risk | 기존 bank와 중복 또는 품질상 위험 |",
        "",
        "---",
        "",
    ])

    for row in rows:
        post_id = row["post_id"]
        post = posts.get(str(post_id))
        if not post:
            raise SystemExit(f"ERROR: post_id not found in WordPress JSON: {post_id}")

        title = row["title"]
        topic_id = row["suggested_topic_id"]
        question_type = QUESTION_TYPE_HINTS.get(topic_id, "PRINCIPLE")

        content = clean_text(str(post.get("content_text") or post.get("content_raw") or ""))
        if len(content) > max_chars:
            content = content[:max_chars].rstrip() + "\n\n...[TRUNCATED]"

        lines.extend([
            f"## Item {row['no']} - {title}",
            "",
            f"- post_id: {post_id}",
            f"- final_class: {row['final_class']}",
            f"- suggested_topic_id: {topic_id}",
            f"- proposed_question_type: {question_type}",
            f"- decision_reason: {row['reason']}",
            f"- needed_action: {row['needed_action']}",
            "",
            "### Source Content",
            "",
            "```text",
            content,
            "```",
            "",
            "### Required Output For This Item",
            "",
            "아래 형식으로 작성하라.",
            "",
            "```text",
            f"topic_id: {topic_id}",
            f"question_type: {question_type}",
            "keep_or_merge: NEW 또는 MERGE_EXISTING",
            "model_answer_summary:",
            "- ...",
            "fact_anchor_summary:",
            "1. ...",
            "2. ...",
            "3. ...",
            "4. ...",
            "5. ...",
            "risk:",
            "- ...",
            "```",
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default=str(DEFAULT_SRC))
    parser.add_argument("--decisions", default=str(DEFAULT_DECISIONS))
    parser.add_argument("--nos", default="3,6,10")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--max-chars", type=int, default=7000)
    args = parser.parse_args()

    selected_nos = parse_nos(args.nos)
    posts = load_posts(Path(args.src))
    decisions = load_decisions(Path(args.decisions))

    selected = []
    for row in decisions:
        try:
            no = int(row["no"])
        except ValueError:
            continue
        if no in selected_nos:
            selected.append(row)

    if not selected:
        raise SystemExit("ERROR: no selected rows")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(make_pack(selected, posts, args.max_chars), encoding="utf-8")

    print("created:", out)
    print("items:", ", ".join(row["no"] for row in selected))
    print("size:", out.stat().st_size)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
