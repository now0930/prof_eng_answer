#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

BANKS = {
    "fact_anchors": {
        "runtime": ROOT / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json",
        "generated": ROOT / "rubrics" / "generated" / "fact_anchors.generated.json",
        "candidate_containers": ["topics", "anchors", "fact_anchors"],
    },
    "model_answers": {
        "runtime": ROOT / "rubrics" / "model_answers" / "industrial_instrumentation_control.json",
        "generated": ROOT / "rubrics" / "generated" / "model_answers.generated.json",
        "candidate_containers": ["answers", "model_answers", "topics"],
    },
    "topic_importance": {
        "runtime": ROOT / "rubrics" / "topic_importance" / "industrial_instrumentation_control.json",
        "generated": ROOT / "rubrics" / "generated" / "topic_importance.generated.json",
        "candidate_containers": ["topics", "topic_importance", "importance"],
    },
    "logic_checks": {
        "runtime": ROOT / "rubrics" / "logic_checks" / "industrial_instrumentation_control.json",
        "generated": ROOT / "rubrics" / "generated" / "logic_checks.generated.json",
        "candidate_containers": ["topic_logic_checks"],
    },
    "logic_check_profiles": {
        "runtime": ROOT / "rubrics" / "logic_check_profiles" / "industrial_instrumentation_control.json",
        "generated": ROOT / "rubrics" / "generated" / "logic_check_profiles.generated.json",
        "candidate_containers": ["profiles"],
    },
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


def find_container(data: dict[str, Any], candidates: list[str]) -> tuple[str | None, list[Any]]:
    for key in candidates:
        value = data.get(key)
        if isinstance(value, list):
            return key, value
    return None, []


def topic_id_of(item: Any) -> str | None:
    if isinstance(item, dict):
        value = item.get("topic_id")
        if isinstance(value, str) and value.strip():
            return value
    return None


def index_by_topic_id(items: list[Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}

    for item in items:
        if not isinstance(item, dict):
            continue

        topic_id = topic_id_of(item)
        if not topic_id:
            continue

        out[topic_id] = item

    return out


def summarize_value(value: Any) -> dict[str, Any]:
    if isinstance(value, list):
        return {"type": "list", "count": len(value)}
    if isinstance(value, dict):
        return {"type": "object", "keys": sorted(value.keys())}
    return {"type": type(value).__name__, "value": value}


def compare_bank(name: str, spec: dict[str, Any]) -> dict[str, Any]:
    runtime_path: Path = spec["runtime"]
    generated_path: Path = spec["generated"]
    candidates: list[str] = spec["candidate_containers"]

    runtime = load_json(runtime_path)
    generated = load_json(generated_path)

    runtime_container, runtime_items = find_container(runtime, candidates)
    generated_container, generated_items = find_container(generated, candidates)

    runtime_index = index_by_topic_id(runtime_items)
    generated_index = index_by_topic_id(generated_items)

    runtime_ids = set(runtime_index)
    generated_ids = set(generated_index)
    overlap_ids = sorted(runtime_ids & generated_ids)

    overlap_details = []
    for topic_id in overlap_ids:
        runtime_obj = runtime_index[topic_id]
        generated_obj = generated_index[topic_id]

        runtime_keys = set(runtime_obj.keys())
        generated_keys = set(generated_obj.keys())

        common_keys = sorted(runtime_keys & generated_keys)
        runtime_only = sorted(runtime_keys - generated_keys)
        generated_only = sorted(generated_keys - runtime_keys)

        common_type_mismatch = []
        for key in common_keys:
            if type(runtime_obj.get(key)).__name__ != type(generated_obj.get(key)).__name__:
                common_type_mismatch.append(
                    {
                        "key": key,
                        "runtime_type": type(runtime_obj.get(key)).__name__,
                        "generated_type": type(generated_obj.get(key)).__name__,
                    }
                )

        overlap_details.append(
            {
                "topic_id": topic_id,
                "runtime_key_count": len(runtime_keys),
                "generated_key_count": len(generated_keys),
                "runtime_only_keys": runtime_only,
                "generated_only_keys": generated_only,
                "common_keys": common_keys,
                "common_type_mismatch": common_type_mismatch,
                "runtime_summary": {
                    key: summarize_value(value)
                    for key, value in runtime_obj.items()
                },
                "generated_summary": {
                    key: summarize_value(value)
                    for key, value in generated_obj.items()
                },
            }
        )

    container_compatible = (
        runtime_container is not None
        and generated_container is not None
        and runtime_container == generated_container
    )

    topic_overlap_ok = len(generated_ids) > 0 and generated_ids.issubset(runtime_ids | generated_ids)

    return {
        "bank": name,
        "runtime_file": str(runtime_path.relative_to(ROOT)),
        "generated_file": str(generated_path.relative_to(ROOT)),
        "runtime_container": runtime_container,
        "generated_container": generated_container,
        "container_compatible": container_compatible,
        "runtime_item_count": len(runtime_items),
        "generated_item_count": len(generated_items),
        "runtime_topic_count": len(runtime_ids),
        "generated_topic_count": len(generated_ids),
        "overlap_topic_count": len(overlap_ids),
        "runtime_only_topics": sorted(runtime_ids - generated_ids),
        "generated_only_topics": sorted(generated_ids - runtime_ids),
        "overlap_topics": overlap_ids,
        "overlap_details": overlap_details,
        "readiness": "container_ready" if container_compatible else "container_mismatch",
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

    lines.append("# Generated Runtime Schema Audit")
    lines.append("")
    lines.append(f"- generated_at: `{report['generated_at']}`")
    lines.append("- purpose: generated JSON이 기존 runtime JSON과 같은 실행 container 구조를 갖는지 확인")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| bank | runtime container | generated container | compatible | runtime topics | generated topics | overlap | readiness |")
    lines.append("|---|---|---|---:|---:|---:|---:|---|")

    for item in report["banks"]:
        lines.append(
            "| {bank} | `{runtime_container}` | `{generated_container}` | {compatible} | {rt} | {gt} | {overlap} | `{readiness}` |".format(
                bank=item["bank"],
                runtime_container=item["runtime_container"],
                generated_container=item["generated_container"],
                compatible="Y" if item["container_compatible"] else "N",
                rt=item["runtime_topic_count"],
                gt=item["generated_topic_count"],
                overlap=item["overlap_topic_count"],
                readiness=item["readiness"],
            )
        )

    lines.append("")
    lines.append("## Overlap key differences")
    lines.append("")

    for item in report["banks"]:
        lines.append(f"### {item['bank']}")
        lines.append("")
        if not item["overlap_details"]:
            lines.append("- No overlapping topic_id.")
            lines.append("")
            continue

        lines.append("| topic_id | runtime only keys | generated only keys | type mismatches |")
        lines.append("|---|---:|---:|---:|")

        for detail in item["overlap_details"]:
            lines.append(
                "| `{topic_id}` | {ro} | {go} | {tm} |".format(
                    topic_id=detail["topic_id"],
                    ro=len(detail["runtime_only_keys"]),
                    go=len(detail["generated_only_keys"]),
                    tm=len(detail["common_type_mismatch"]),
                )
            )

        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- `container_ready`: generated 파일이 기존 runtime과 같은 top-level list container를 사용한다.")
    lines.append("- `container_mismatch`: generated 파일의 top-level container가 기존 runtime과 달라 loader 전환 전에 builder 수정이 필요하다.")
    lines.append("- key difference는 바로 오류는 아니다. topic_pack source와 기존 runtime schema 차이를 보여주는 참고 정보다.")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote: {path}")


def main() -> int:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    banks = [
        compare_bank(name, spec)
        for name, spec in BANKS.items()
    ]

    report = {
        "generated_at": timestamp,
        "banks": banks,
    }

    json_path = REPORT_DIR / f"generated_runtime_schema_audit_{timestamp}.json"
    md_path = REPORT_DIR / f"generated_runtime_schema_audit_{timestamp}.md"

    write_json(json_path, report)
    write_markdown(md_path, report)

    print()
    print("GENERATED RUNTIME SCHEMA AUDIT OK")
    for item in banks:
        print(
            "{bank}: runtime_container={runtime_container} generated_container={generated_container} compatible={compatible}".format(
                bank=item["bank"],
                runtime_container=item["runtime_container"],
                generated_container=item["generated_container"],
                compatible=item["container_compatible"],
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
