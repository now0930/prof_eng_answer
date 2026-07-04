#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

SCAN_SUFFIXES = {".py", ".json", ".md", ".yaml", ".yml"}
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

PATTERNS = {
    "fact_anchors_runtime": r"rubrics/(?:fact_anchors|fact_anchor)",
    "model_answers_runtime": r"rubrics/(?:model_answers|model_answer)",
    "topic_importance_runtime": r"rubrics/topic_importance",
    "logic_checks_runtime": r"rubrics/logic_checks",
    "logic_check_profiles_runtime": r"rubrics/logic_check_profiles",
    "generated_rubrics": r"rubrics/generated",
    "active_profile": r"active_profile\.json",
    "industrial_subject_json": r"industrial_instrumentation_control\.json",
    "default_rubric_json": r"rubrics/default\.json",
    "hardcoded_rubrics_path": r"rubrics/",
    "pathlib_rubrics": r"Path\([^)]*rubrics|ROOT\s*/\s*[\"']rubrics[\"']|BASE_DIR\s*/\s*[\"']rubrics[\"']",
    "env_rubric_mode": r"RUBRIC_BANK_MODE|RUBRIC_MODE|GENERATED_RUBRIC",
}


def should_scan(path: Path) -> bool:
    if path.suffix not in SCAN_SUFFIXES:
        return False

    rel_parts = path.relative_to(ROOT).parts
    return not any(part in SKIP_DIRS for part in rel_parts)


def scan_file(path: Path) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    except Exception:
        return []

    hits: list[dict[str, Any]] = []
    lines = text.splitlines()

    for lineno, line in enumerate(lines, start=1):
        for name, pattern in PATTERNS.items():
            if re.search(pattern, line):
                hits.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "line": lineno,
                        "pattern": name,
                        "text": line.strip()[:240],
                    }
                )

    return hits


def classify_hit(hit: dict[str, Any]) -> str:
    file = hit["file"]
    pattern = hit["pattern"]

    if file.startswith("scripts/"):
        return "script_or_validator"
    if file.startswith("rubrics/"):
        return "rubric_json_reference"
    if pattern in {"logic_checks_runtime", "logic_check_profiles_runtime", "fact_anchors_runtime", "model_answers_runtime", "topic_importance_runtime"}:
        return "runtime_loader_candidate"
    if pattern == "active_profile":
        return "active_profile_loader_candidate"
    return "other"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {path}")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Rubric Path Usage Audit")
    lines.append("")
    lines.append(f"- generated_at: `{report['generated_at']}`")
    lines.append("- purpose: generated rubric mode 도입 전에 runtime JSON 경로 사용처를 찾는다.")
    lines.append("")

    lines.append("## Summary by classification")
    lines.append("")
    for key, value in report["summary_by_classification"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")

    lines.append("## Summary by pattern")
    lines.append("")
    for key, value in report["summary_by_pattern"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")

    lines.append("## Loader candidates")
    lines.append("")
    loader_hits = [
        h for h in report["hits"]
        if h["classification"] in {
            "runtime_loader_candidate",
            "active_profile_loader_candidate",
        }
    ]

    if not loader_hits:
        lines.append("- No direct runtime loader candidates found.")
    else:
        lines.append("| file | line | pattern | text |")
        lines.append("|---|---:|---|---|")
        for hit in loader_hits:
            text = hit["text"].replace("|", "\\|")
            lines.append(f"| `{hit['file']}` | {hit['line']} | `{hit['pattern']}` | `{text}` |")
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

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if not should_scan(path):
            continue

        for hit in scan_file(path):
            hit["classification"] = classify_hit(hit)
            hits.append(hit)

    summary_by_pattern: dict[str, int] = {}
    summary_by_classification: dict[str, int] = {}

    for hit in hits:
        summary_by_pattern[hit["pattern"]] = summary_by_pattern.get(hit["pattern"], 0) + 1
        summary_by_classification[hit["classification"]] = summary_by_classification.get(hit["classification"], 0) + 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "generated_at": timestamp,
        "hit_count": len(hits),
        "summary_by_pattern": dict(sorted(summary_by_pattern.items())),
        "summary_by_classification": dict(sorted(summary_by_classification.items())),
        "hits": hits,
    }

    json_path = REPORT_DIR / f"rubric_path_usage_audit_{timestamp}.json"
    md_path = REPORT_DIR / f"rubric_path_usage_audit_{timestamp}.md"

    write_json(json_path, report)
    write_markdown(md_path, report)

    print()
    print("RUBRIC PATH USAGE AUDIT OK")
    print(f"hits: {len(hits)}")
    for key, value in report["summary_by_classification"].items():
        print(f"{key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
