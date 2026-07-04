#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "rubrics" / "generated"
REPORT_DIR = ROOT / "reports"

RUNTIME_FILES = {
    "fact_anchors": ROOT / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json",
    "model_answers": ROOT / "rubrics" / "model_answers" / "industrial_instrumentation_control.json",
    "topic_importance": ROOT / "rubrics" / "topic_importance" / "industrial_instrumentation_control.json",
    "logic_checks": ROOT / "rubrics" / "logic_checks" / "industrial_instrumentation_control.json",
    "logic_check_profiles": ROOT / "rubrics" / "logic_check_profiles" / "industrial_instrumentation_control.json",
}

GENERATED_FILES = {
    "fact_anchors": GENERATED_DIR / "fact_anchors.generated.json",
    "model_answers": GENERATED_DIR / "model_answers.generated.json",
    "topic_importance": GENERATED_DIR / "topic_importance.generated.json",
    "logic_checks": GENERATED_DIR / "logic_checks.generated.json",
    "logic_check_profiles": GENERATED_DIR / "logic_check_profiles.generated.json",
}


def fail(msg: str) -> None:
    raise SystemExit(f"ERROR: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing file: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"invalid JSON: {path}: {e}")

    if not isinstance(data, dict):
        fail(f"root must be object: {path}")

    return data


def collect_topic_objects(obj: Any) -> dict[str, dict[str, Any]]:
    """
    JSON 내부에서 topic_id를 가진 dict를 재귀적으로 찾는다.
    단, 같은 topic_id가 여러 번 나오면 더 큰 dict를 우선 보존한다.
    기존 runtime schema가 파일마다 조금 달라도 topic_id 기준으로 비교하기 위함이다.
    """
    found: dict[str, dict[str, Any]] = {}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            topic_id = value.get("topic_id")
            if isinstance(topic_id, str) and topic_id.strip():
                prev = found.get(topic_id)
                if prev is None or len(json.dumps(value, ensure_ascii=False)) > len(
                    json.dumps(prev, ensure_ascii=False)
                ):
                    found[topic_id] = value

            for child in value.values():
                walk(child)

        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(obj)
    return found


def summarize_topic_object(obj: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}

    for key, value in obj.items():
        if key == "topic_id":
            continue

        if isinstance(value, list):
            summary[key] = {
                "type": "list",
                "count": len(value),
            }
        elif isinstance(value, dict):
            summary[key] = {
                "type": "object",
                "keys": sorted(value.keys()),
            }
        else:
            summary[key] = {
                "type": type(value).__name__,
                "value": value,
            }

    return summary


def compare_bank(bank_name: str) -> dict[str, Any]:
    runtime_path = RUNTIME_FILES[bank_name]
    generated_path = GENERATED_FILES[bank_name]

    runtime_data = load_json(runtime_path)
    generated_data = load_json(generated_path)

    runtime_topics = collect_topic_objects(runtime_data)
    generated_topics = collect_topic_objects(generated_data)

    runtime_ids = set(runtime_topics)
    generated_ids = set(generated_topics)
    overlap = sorted(runtime_ids & generated_ids)

    overlap_details = []
    for topic_id in overlap:
        runtime_obj = runtime_topics[topic_id]
        generated_obj = generated_topics[topic_id]

        runtime_summary = summarize_topic_object(runtime_obj)
        generated_summary = summarize_topic_object(generated_obj)

        runtime_keys = set(runtime_summary)
        generated_keys = set(generated_summary)

        overlap_details.append(
            {
                "topic_id": topic_id,
                "runtime_key_count": len(runtime_keys),
                "generated_key_count": len(generated_keys),
                "runtime_only_keys": sorted(runtime_keys - generated_keys),
                "generated_only_keys": sorted(generated_keys - runtime_keys),
                "common_keys": sorted(runtime_keys & generated_keys),
                "runtime_summary": runtime_summary,
                "generated_summary": generated_summary,
            }
        )

    return {
        "bank": bank_name,
        "runtime_file": str(runtime_path.relative_to(ROOT)),
        "generated_file": str(generated_path.relative_to(ROOT)),
        "runtime_topic_count": len(runtime_ids),
        "generated_topic_count": len(generated_ids),
        "overlap_topic_count": len(overlap),
        "runtime_only_topics": sorted(runtime_ids - generated_ids),
        "generated_only_topics": sorted(generated_ids - runtime_ids),
        "overlap_topics": overlap,
        "overlap_details": overlap_details,
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {path}")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Generated vs Runtime Rubric Audit")
    lines.append("")
    lines.append(f"- generated_at: `{report['generated_at']}`")
    lines.append(f"- purpose: topic_packs generated 결과와 기존 runtime JSON의 topic 단위 차이 확인")
    lines.append("")

    for item in report["banks"]:
        lines.append(f"## {item['bank']}")
        lines.append("")
        lines.append(f"- runtime: `{item['runtime_file']}`")
        lines.append(f"- generated: `{item['generated_file']}`")
        lines.append(f"- runtime_topic_count: `{item['runtime_topic_count']}`")
        lines.append(f"- generated_topic_count: `{item['generated_topic_count']}`")
        lines.append(f"- overlap_topic_count: `{item['overlap_topic_count']}`")
        lines.append("")

        if item["generated_only_topics"]:
            lines.append("### Generated only topics")
            for topic_id in item["generated_only_topics"]:
                lines.append(f"- `{topic_id}`")
            lines.append("")

        if item["runtime_only_topics"]:
            lines.append("### Runtime only topics")
            for topic_id in item["runtime_only_topics"]:
                lines.append(f"- `{topic_id}`")
            lines.append("")

        if item["overlap_details"]:
            lines.append("### Overlap details")
            lines.append("")
            lines.append("| topic_id | runtime_only_keys | generated_only_keys | common_keys |")
            lines.append("|---|---:|---:|---:|")
            for detail in item["overlap_details"]:
                lines.append(
                    "| `{topic_id}` | {ro} | {go} | {common} |".format(
                        topic_id=detail["topic_id"],
                        ro=len(detail["runtime_only_keys"]),
                        go=len(detail["generated_only_keys"]),
                        common=len(detail["common_keys"]),
                    )
                )
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote: {path}")


def main() -> int:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    banks = [compare_bank(name) for name in GENERATED_FILES]

    report = {
        "generated_at": timestamp,
        "purpose": "Compare generated rubric banks from topic_packs against current runtime rubric JSON files.",
        "banks": banks,
    }

    json_path = REPORT_DIR / f"generated_vs_runtime_audit_{timestamp}.json"
    md_path = REPORT_DIR / f"generated_vs_runtime_audit_{timestamp}.md"

    write_json(json_path, report)
    write_markdown(md_path, report)

    print()
    print("AUDIT OK")
    for item in banks:
        print(
            "{bank}: runtime={runtime} generated={generated} overlap={overlap}".format(
                bank=item["bank"],
                runtime=item["runtime_topic_count"],
                generated=item["generated_topic_count"],
                overlap=item["overlap_topic_count"],
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
