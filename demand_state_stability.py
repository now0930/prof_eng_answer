"""Topic-independent demand-state stability measurement.

The accuracy benchmark measures one prediction run against reviewed labels.
This module compares repeated runs over the same reviewed demand universe so
that provider variance cannot be hidden by unmatched or omitted rows.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable

from expert_accuracy_benchmark import (
    FINAL_REVIEW_STATUSES,
    _match_demand_rows,
    load_jsonl,
    validate_gold_case,
    validate_prediction,
)


SCHEMA_VERSION = "demand_state_stability_report_v1"
UNRESOLVED_STATE = "UNKNOWN"
ASSESSED_STATES = {"CORRECT", "PARTIAL", "MISSING", "WRONG"}


def _material_transition(left: str, right: str) -> bool:
    """Ignore UNKNOWN and normal CORRECT/PARTIAL boundary noise only."""
    if left not in ASSESSED_STATES or right not in ASSESSED_STATES:
        return False
    return {left, right} != {"CORRECT", "PARTIAL"}


def _eligible_gold(gold_cases: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        validate_gold_case(case)
        for case in gold_cases
        if str(case.get("review_status", "")).lower() in FINAL_REVIEW_STATUSES
    ]


def _aligned_states(
    gold_cases: list[dict[str, Any]],
    predictions: Iterable[dict[str, Any]],
) -> tuple[dict[tuple[str, str], str], set[str]]:
    prediction_map = {
        row["case_id"]: row
        for row in (validate_prediction(item) for item in predictions)
    }
    states: dict[tuple[str, str], str] = {}
    missing_cases: set[str] = set()
    for case in gold_cases:
        case_id = case["case_id"]
        prediction = prediction_map.get(case_id)
        if prediction is None:
            missing_cases.add(case_id)
            matched: dict[str, str] = {}
        else:
            matched = {
                gold["demand_id"]: predicted["status"]
                for gold, predicted in _match_demand_rows(
                    case["labels"]["demands"], prediction["demands"]
                )
            }
        for demand in case["labels"]["demands"]:
            key = (case_id, demand["demand_id"])
            states[key] = matched.get(demand["demand_id"], UNRESOLVED_STATE)
    return states, missing_cases


def analyze_stability(
    gold_cases: Iterable[dict[str, Any]],
    prediction_runs: Iterable[tuple[str, Iterable[dict[str, Any]]]],
) -> dict[str, Any]:
    """Compare two or more runs on the complete reviewed demand universe."""
    gold = _eligible_gold(gold_cases)
    runs = list(prediction_runs)
    if len(runs) < 2:
        raise ValueError("at least two prediction runs are required")
    names = [str(name).strip() for name, _ in runs]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError("run names must be unique and non-empty")

    gold_states = {
        (case["case_id"], row["demand_id"]): row["status"]
        for case in gold
        for row in case["labels"]["demands"]
    }
    aligned: dict[str, dict[tuple[str, str], str]] = {}
    run_rows: list[dict[str, Any]] = []
    for name, predictions in runs:
        validated = [validate_prediction(row) for row in predictions]
        states, missing_cases = _aligned_states(gold, validated)
        correct = sum(states[key] == expected for key, expected in gold_states.items())
        run_rows.append({
            "name": name,
            "prediction_case_count": len(validated),
            "missing_case_count": len(missing_cases),
            "missing_cases": sorted(missing_cases),
            "complete_universe_state_accuracy": round(correct / len(gold_states), 4)
            if gold_states else None,
            "unresolved_demand_count": sum(
                state == UNRESOLVED_STATE for state in states.values()
            ),
        })
        aligned[name] = states

    transition_counts: Counter[str] = Counter()
    changed_keys: set[tuple[str, str]] = set()
    material_keys: set[tuple[str, str]] = set()
    pair_rows: list[dict[str, Any]] = []
    for left_name, right_name in combinations(names, 2):
        left = aligned[left_name]
        right = aligned[right_name]
        pair_changed = 0
        pair_material = 0
        for key in gold_states:
            before, after = left[key], right[key]
            if before == after:
                continue
            pair_changed += 1
            changed_keys.add(key)
            transition_counts[f"{before}->{after}"] += 1
            if _material_transition(before, after):
                pair_material += 1
                material_keys.add(key)
        denominator = len(gold_states)
        pair_rows.append({
            "left": left_name,
            "right": right_name,
            "agreement": round((denominator - pair_changed) / denominator, 4)
            if denominator else None,
            "changed_demand_count": pair_changed,
            "material_transition_count": pair_material,
        })

    unstable_rows = []
    for case_id, demand_id in sorted(changed_keys):
        states = {name: aligned[name][(case_id, demand_id)] for name in names}
        unstable_rows.append({
            "case_id": case_id,
            "demand_id": demand_id,
            "gold": gold_states[(case_id, demand_id)],
            "states": states,
            "material": (case_id, demand_id) in material_keys,
        })

    scores_by_case: dict[str, list[float]] = {}
    for _name, predictions in runs:
        for row in predictions:
            prediction = validate_prediction(row)
            scores_by_case.setdefault(prediction["case_id"], []).append(
                prediction["total_score"]
            )
    score_spreads = [
        {
            "case_id": case_id,
            "minimum": min(scores),
            "maximum": max(scores),
            "spread": round(max(scores) - min(scores), 4),
        }
        for case_id, scores in sorted(scores_by_case.items())
        if len(scores) == len(runs)
    ]
    max_spread = max((row["spread"] for row in score_spreads), default=None)

    denominator = len(gold_states)
    all_run_agreement = sum(
        len({aligned[name][key] for name in names}) == 1 for key in gold_states
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "run_count": len(runs),
        "reviewed_case_count": len(gold),
        "reviewed_demand_count": denominator,
        "runs": run_rows,
        "pairwise": pair_rows,
        "all_run_state_agreement": round(all_run_agreement / denominator, 4)
        if denominator else None,
        "unstable_demand_count": len(changed_keys),
        "materially_unstable_demand_count": len(material_keys),
        "transition_counts": dict(sorted(transition_counts.items())),
        "unstable_demands": unstable_rows,
        "score_spreads": score_spreads,
        "maximum_case_score_spread": max_spread,
    }


def load_stability_inputs(
    golden_path: Path,
    prediction_paths: Iterable[Path],
) -> tuple[list[dict[str, Any]], list[tuple[str, list[dict[str, Any]]]]]:
    gold = load_jsonl(golden_path, validate_gold_case)
    runs = [
        (str(path), load_jsonl(path, validate_prediction))
        for path in prediction_paths
    ]
    return gold, runs
