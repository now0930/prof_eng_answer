#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

PATTERNS = {
    "direct_topic_importance_runtime_path": r"rubrics/topic_importance|rubrics[/\"]\s*/?\s*[\"']?topic_importance",
    "industrial_topic_importance_file": r"topic_importance.+industrial_instrumentation_control\.json|industrial_instrumentation_control\.json.+topic_importance",
    "topic_importance_constant": r"TOPIC_IMPORTANCE|IMPORTANCE_BANK|TOPIC_PRIORITY",
    "topic_importance_loader": r"load_topic_importance_bank|save_topic_importance_bank",
    "topic_importance_text": r"topic_importance|Topic Importance|TOPIC IMPORTANCE",
    "resolver_topic_importance": r"resolve_rubric_bank_path\([\"']topic_importance[\"']\)",
}

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "data",
    "logs",
    "backups",
    "tmp",
    "reports",
}

SCAN_SUFFIXES = {".py"}


def should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_SUFFIXES:
        return False

    rel_parts = path.relative_to(ROOT).parts
    return not any(part in SKIP_DIRS for part in rel_parts)


def classify(file: str, pattern: str, text: str) -> str:
    if file == "rubric_registry.py":
        return "registry_loader"

    if pattern in {
        "direct_topic_importance_runtime_path",
        "industrial_topic_importance_file",
        "topic_importance_constant",
    }:
        return "direct_runtime_candidate"

    if pattern == "resolver_topic_importance":
        return "already_uses_resolver"

    if pattern == "topic_importance_loader":
        return "uses_registry_loader"

    return "reference_only"


def scan_file(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []

    hits: list[dict[str, Any]] = []

    for lineno, line in enumerate(lines, start=1):
        for name, pattern in PATTERNS.items():
            if re.search(pattern, line, flags=re.IGNORECASE):
                rel = str(path.relative_to(ROOT))
                hits.append(
                    {
                        "file": rel,
                        "line": lineno,
                        "pattern": name,
                        "classification": classify(rel, name, line),
                        "text": line.strip()[:240],
                    }
                )

    return hits


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {path}")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Topic Importance Usage Audit")
    lines.append("")
    lines.append(f"- generated_at: `{report['generated_at']}`")
    lines.append("- purpose: topic_importance runtime path를 직접 읽는 코드와 resolver 적용 후보를 찾는다.")
    lines.append("")

    lines.append("## Summary by classification")
    lines.append("")
    for key, value in report["summary_by_classification"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")

    lines.append("## Direct runtime candidates")
    lines.append("")
    direct = [
        hit for hit in report["hits"]
        if hit["classification"] == "direct_runtime_candidate"
    ]

    if not direct:
        lines.append("- No direct runtime candidates found.")
    else:
        lines.append("| file | line | pattern | text |")
        lines.append("|---|---:|---|---|")
        for hit in direct:
            text = hit["text"].replace("|", "\\|")
            lines.append(
                f"| `{hit['file']}` | {hit['line']} | `{hit['pattern']}` | `{text}` |"
            )
    lines.append("")

    lines.append("## All hits")
    lines.append("")
    lines.append("| file | line | classification | pattern | text |")
    lines.append("|---|---:|---|---|---|")
    for hit in report["hits"]:
        text = hit["text"].replace("|", "\\|")
        lines.append(
            f"| `{hit['file']}` | {hit['line']} | `{hit['classification']}` | `{hit['pattern']}` | `{text}` |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote: {path}")


def main() -> int:
    hits: list[dict[str, Any]] = []

    for path in sorted(ROOT.rglob("*.py")):
        if not should_scan(path):
            continue
        hits.extend(scan_file(path))

    summary_by_classification: dict[str, int] = {}
    summary_by_pattern: dict[str, int] = {}

    for hit in hits:
        summary_by_classification[hit["classification"]] = (
            summary_by_classification.get(hit["classification"], 0) + 1
        )
        summary_by_pattern[hit["pattern"]] = (
            summary_by_pattern.get(hit["pattern"], 0) + 1
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "generated_at": timestamp,
        "hit_count": len(hits),
        "summary_by_classification": dict(sorted(summary_by_classification.items())),
        "summary_by_pattern": dict(sorted(summary_by_pattern.items())),
        "hits": hits,
    }

    json_path = REPORT_DIR / f"topic_importance_usage_audit_{timestamp}.json"
    md_path = REPORT_DIR / f"topic_importance_usage_audit_{timestamp}.md"

    write_json(json_path, report)
    write_markdown(md_path, report)

    print()
    print("TOPIC IMPORTANCE USAGE AUDIT OK")
    print(f"hits: {len(hits)}")
    for key, value in report["summary_by_classification"].items():
        print(f"{key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
