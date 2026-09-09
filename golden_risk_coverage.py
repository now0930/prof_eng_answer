"""Risk-ranked Topic coverage inventory for deterministic Golden expansion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from expert_accuracy_benchmark import load_jsonl, validate_gold_case


VERSION = "golden_risk_coverage_v1"
MARKER = "GOLDEN_RISK_COVERAGE_V1"
_IMPORTANCE_WEIGHT = {"CORE_MUST_PREPARE": 4, "HIGH": 3, "NORMAL": 1}
_DIFFICULTY_WEIGHT = {"THEORY_CORE": 3, "DESIGN_EVALUATION": 2, "FIELD_APPLICATION": 1}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_golden_risk_coverage(*, root: Path, golden_path: Path) -> dict[str, Any]:
    cases = load_jsonl(golden_path, validate_gold_case)
    cases_by_topic: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        if case["review_status"] not in {"reviewed", "adjudicated"}:
            continue
        for topic_id in case.get("topic_ids") or []:
            cases_by_topic.setdefault(str(topic_id), []).append(case)

    rows: list[dict[str, Any]] = []
    topic_root = root / "rubrics/topic_packs"
    for topic_dir in sorted(path for path in topic_root.iterdir() if path.is_dir()):
        importance = _load(topic_dir / "topic_importance.json")
        logic = _load(topic_dir / "logic_check.json")
        linked = cases_by_topic.get(topic_dir.name, [])
        fatal_count = len(logic.get("llm_profile", {}).get("fatal_conditions") or [])
        machine_contract = isinstance(logic.get("machine_contract"), dict)
        normal_count = sum(
            not case["labels"]["findings"]
            and case["labels"]["flags"]["passing_score_allowed"]
            for case in linked
        )
        adverse_count = sum(
            bool(case["labels"]["findings"])
            or not case["labels"]["flags"]["passing_score_allowed"]
            for case in linked
        )
        fatal_case_count = sum(
            any(row["severity"] == "fatal" for row in case["labels"]["findings"])
            for case in linked
        )
        importance_name = str(importance.get("selection_importance") or "NORMAL")
        difficulty_name = str(importance.get("difficulty") or "FIELD_APPLICATION")
        intrinsic_risk = (
            _IMPORTANCE_WEIGHT.get(importance_name, 0)
            + _DIFFICULTY_WEIGHT.get(difficulty_name, 0)
            + min(fatal_count, 3)
            + int(machine_contract)
        )
        missing_lanes = [
            lane for lane, count in (
                ("normal", normal_count),
                ("adverse", adverse_count),
                ("fatal", fatal_case_count if fatal_count else 1),
            ) if count == 0
        ]
        rows.append({
            "topic_id": topic_dir.name,
            "selection_importance": importance_name,
            "difficulty": difficulty_name,
            "fatal_rule_count": fatal_count,
            "machine_contract": machine_contract,
            "reviewed_case_count": len(linked),
            "normal_case_count": normal_count,
            "adverse_case_count": adverse_count,
            "fatal_case_count": fatal_case_count,
            "missing_lanes": missing_lanes,
            "intrinsic_risk_score": intrinsic_risk,
            "expansion_priority": intrinsic_risk * len(missing_lanes),
        })
    rows.sort(key=lambda row: (-row["expansion_priority"], -row["intrinsic_risk_score"], row["topic_id"]))
    return {
        "version": VERSION,
        "marker": MARKER,
        "topic_count": len(rows),
        "reviewed_case_count": len([
            case for case in cases
            if case["review_status"] in {"reviewed", "adjudicated"}
        ]),
        "covered_topic_count": sum(row["reviewed_case_count"] > 0 for row in rows),
        "fully_laned_topic_count": sum(not row["missing_lanes"] for row in rows),
        "topics": rows,
    }
