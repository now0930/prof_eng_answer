#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

SOURCES = {
    "topic_pack": [
        ROOT / "rubrics" / "topic_packs",
    ],
    "generated": [
        ROOT / "rubrics" / "generated" / "fact_anchors.generated.json",
        ROOT / "rubrics" / "generated" / "model_answers.generated.json",
        ROOT / "rubrics" / "generated" / "topic_importance.generated.json",
        ROOT / "rubrics" / "generated" / "logic_checks.generated.json",
        ROOT / "rubrics" / "generated" / "logic_check_profiles.generated.json",
    ],
    "runtime": [
        ROOT / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json",
        ROOT / "rubrics" / "model_answers" / "industrial_instrumentation_control.json",
        ROOT / "rubrics" / "topic_importance" / "industrial_instrumentation_control.json",
        ROOT / "rubrics" / "logic_checks" / "industrial_instrumentation_control.json",
        ROOT / "rubrics" / "logic_check_profiles" / "industrial_instrumentation_control.json",
        ROOT / "rubrics" / "difficulty_profiles" / "default.json",
        ROOT / "rubrics" / "question_types" / "default.json",
        ROOT / "rubrics" / "subjects" / "industrial_instrumentation_control.json",
    ],
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_topic_ids_from_json(value: Any, path: Path) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}

    def add(topic_id: str) -> None:
        if not topic_id.strip():
            return
        found.setdefault(topic_id, set()).add(str(path.relative_to(ROOT)))

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            topic_id = node.get("topic_id")
            if isinstance(topic_id, str):
                add(topic_id)

            # 일부 파일은 id가 사실상 topic_id 역할을 할 수 있으므로 참고용으로만 수집하지 않는다.
            # 오탐을 줄이기 위해 topic_id 명시 필드만 기준으로 삼는다.

            for child in node.values():
                walk(child)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(value)
    return found


def merge(dst: dict[str, set[str]], src: dict[str, set[str]]) -> None:
    for topic_id, paths in src.items():
        dst.setdefault(topic_id, set()).update(paths)


def collect_topic_pack_ids(pack_root: Path) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}

    if not pack_root.exists():
        return found

    for pack_dir in sorted(p for p in pack_root.iterdir() if p.is_dir()):
        topic_id = pack_dir.name
        found.setdefault(topic_id, set()).add(str(pack_dir.relative_to(ROOT)))

        for json_file in sorted(pack_dir.glob("*.json")):
            try:
                data = load_json(json_file)
            except Exception:
                continue
            merge(found, collect_topic_ids_from_json(data, json_file))

    return found


def collect_source_group(group_name: str, paths: list[Path]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}

    for path in paths:
        if path.is_dir():
            if group_name == "topic_pack":
                merge(found, collect_topic_pack_ids(path))
            continue

        if not path.exists():
            continue

        try:
            data = load_json(path)
        except Exception:
            continue

        merge(found, collect_topic_ids_from_json(data, path))

    return found


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {path}")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "topic_id",
        "in_topic_pack",
        "in_generated",
        "in_runtime",
        "topic_pack_paths",
        "generated_paths",
        "runtime_paths",
        "status",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"wrote: {path}")


def write_markdown(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Topic ID Consistency Audit")
    lines.append("")
    lines.append(f"- generated_at: `{summary['generated_at']}`")
    lines.append(f"- total_topics: `{summary['total_topics']}`")
    lines.append(f"- topic_pack_topics: `{summary['topic_pack_topics']}`")
    lines.append(f"- generated_topics: `{summary['generated_topics']}`")
    lines.append(f"- runtime_topics: `{summary['runtime_topics']}`")
    lines.append("")

    lines.append("## Status counts")
    lines.append("")
    for key, value in summary["status_counts"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")

    lines.append("## Topic matrix")
    lines.append("")
    lines.append("| topic_id | topic_pack | generated | runtime | status |")
    lines.append("|---|---:|---:|---:|---|")

    for row in rows:
        lines.append(
            "| `{topic_id}` | {tp} | {gen} | {rt} | `{status}` |".format(
                topic_id=row["topic_id"],
                tp="Y" if row["in_topic_pack"] else "",
                gen="Y" if row["in_generated"] else "",
                rt="Y" if row["in_runtime"] else "",
                status=row["status"],
            )
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- `source_and_generated_and_runtime`: 이미 세 영역에 모두 존재한다.")
    lines.append("- `source_and_generated_only`: topic_pack과 generated에는 있으나 runtime에는 아직 없다.")
    lines.append("- `runtime_only`: 기존 runtime에는 있으나 topic_pack으로 아직 분리되지 않았다.")
    lines.append("- `source_only`: topic_pack은 있으나 generated 생성이 안 되었거나 누락되었다.")
    lines.append("- `generated_only`: generated에는 있으나 source가 사라졌거나 빌드 산출물이 오래되었을 수 있다.")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote: {path}")


def main() -> int:
    topic_pack = collect_source_group("topic_pack", SOURCES["topic_pack"])
    generated = collect_source_group("generated", SOURCES["generated"])
    runtime = collect_source_group("runtime", SOURCES["runtime"])

    all_topic_ids = sorted(set(topic_pack) | set(generated) | set(runtime))

    rows: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}

    for topic_id in all_topic_ids:
        in_tp = topic_id in topic_pack
        in_gen = topic_id in generated
        in_rt = topic_id in runtime

        if in_tp and in_gen and in_rt:
            status = "source_and_generated_and_runtime"
        elif in_tp and in_gen and not in_rt:
            status = "source_and_generated_only"
        elif in_rt and not in_tp and not in_gen:
            status = "runtime_only"
        elif in_tp and not in_gen and not in_rt:
            status = "source_only"
        elif in_gen and not in_tp and not in_rt:
            status = "generated_only"
        elif in_tp and in_rt and not in_gen:
            status = "source_and_runtime_missing_generated"
        elif in_gen and in_rt and not in_tp:
            status = "generated_and_runtime_missing_source"
        else:
            status = "mixed"

        status_counts[status] = status_counts.get(status, 0) + 1

        rows.append(
            {
                "topic_id": topic_id,
                "in_topic_pack": in_tp,
                "in_generated": in_gen,
                "in_runtime": in_rt,
                "topic_pack_paths": "; ".join(sorted(topic_pack.get(topic_id, []))),
                "generated_paths": "; ".join(sorted(generated.get(topic_id, []))),
                "runtime_paths": "; ".join(sorted(runtime.get(topic_id, []))),
                "status": status,
            }
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    summary = {
        "generated_at": timestamp,
        "total_topics": len(all_topic_ids),
        "topic_pack_topics": len(topic_pack),
        "generated_topics": len(generated),
        "runtime_topics": len(runtime),
        "status_counts": dict(sorted(status_counts.items())),
    }

    report = {
        "summary": summary,
        "rows": rows,
    }

    json_path = REPORT_DIR / f"topic_id_consistency_audit_{timestamp}.json"
    csv_path = REPORT_DIR / f"topic_id_consistency_audit_{timestamp}.csv"
    md_path = REPORT_DIR / f"topic_id_consistency_audit_{timestamp}.md"

    write_json(json_path, report)
    write_csv(csv_path, rows)
    write_markdown(md_path, rows, summary)

    print()
    print("TOPIC ID AUDIT OK")
    print(f"total_topics: {summary['total_topics']}")
    for key, value in summary["status_counts"].items():
        print(f"{key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
