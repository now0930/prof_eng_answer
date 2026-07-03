#!/usr/bin/env python3
"""Common helpers for Rubric Bank validators."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = REPO_ROOT / "reports" / "rubric_bank"


RUBRIC_PATHS = {
    "scoring_model": "rubrics/scoring_model/default.json",
    "rater_profile": "rubrics/raters/layered_default.json",
    "question_type_profile": "rubrics/question_types/default.json",
    "model_answer_bank": "rubrics/model_answers/industrial_instrumentation_control.json",
    "fact_anchor_bank": "rubrics/fact_anchors/industrial_instrumentation_control.json",
    "topic_importance": "rubrics/topic_importance/industrial_instrumentation_control.json",
    "logic_check_bank": "rubrics/logic_checks/industrial_instrumentation_control.json",
    "logic_check_profile": "rubrics/logic_check_profiles/industrial_instrumentation_control.json",
}


def load_json(rel_path: str) -> dict[str, Any]:
    path = REPO_ROOT / rel_path
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise TypeError(f"{rel_path}: root must be object/dict")

    return data


def collection(data: dict[str, Any], *keys: str) -> list[Any]:
    for key in keys:
        value = data.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return list(value.values())
    return []


def item_id(item: Any, *keys: str) -> str | None:
    if not isinstance(item, dict):
        return None

    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return None


def duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    dup: set[str] = set()

    for value in values:
        if value in seen:
            dup.add(value)
        else:
            seen.add(value)

    return sorted(dup)


def run_script(name: str, args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    return {
        "name": name,
        "args": args,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "output_head": proc.stdout.splitlines()[:80],
    }


def write_report(filename: str, report: dict[str, Any]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / filename
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
