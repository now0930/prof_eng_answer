"""Expert-labelled, topic-independent grading accuracy benchmark.

Golden labels and model predictions are intentionally separate. Draft labels
may be inspected during development, but only reviewed/adjudicated labels are
eligible for official accuracy reporting.
"""

from __future__ import annotations

import json
import math
import re
from difflib import SequenceMatcher
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


GOLD_VERSION = "expert_accuracy_case_v1"
PREDICTION_VERSION = "expert_accuracy_prediction_v1"
FINAL_REVIEW_STATUSES = {"reviewed", "adjudicated"}
REVIEW_STATUSES = FINAL_REVIEW_STATUSES | {"draft", "excluded"}
DEMAND_STATES = {"CORRECT", "PARTIAL", "WRONG", "MISSING"}
PREDICTION_DEMAND_STATES = DEMAND_STATES | {"UNKNOWN"}
FINDING_SEVERITIES = {"minor", "major", "fatal"}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
_DEMAND_MATCH_STOPWORDS = {
    "설명", "제시", "정의", "평가", "검토", "방법", "절차", "기준",
    "한다", "하다", "포함", "대한", "위한", "그리고", "또는",
    "the", "and", "for", "with", "from",
}


class AccuracyBenchmarkError(ValueError):
    pass


def _text(value: Any) -> str:
    return str(value or "").strip()


def _finite(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise AccuracyBenchmarkError(f"{field} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as error:
        raise AccuracyBenchmarkError(f"{field} must be numeric") from error
    if not math.isfinite(result):
        raise AccuracyBenchmarkError(f"{field} must be finite")
    return result


def normalize_demand_state(value: Any, *, allow_unknown: bool = False) -> str:
    state = _text(value).upper()
    aliases = {
        # Presence establishes addressing, not technical correctness.
        "PRESENT": "PARTIAL",
        "INCORRECT": "WRONG",
        "ABSENT": "MISSING",
    }
    state = aliases.get(state, state)
    allowed = PREDICTION_DEMAND_STATES if allow_unknown else DEMAND_STATES
    if state not in allowed:
        raise AccuracyBenchmarkError(f"unsupported demand state: {value!r}")
    return state


def validate_gold_case(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AccuracyBenchmarkError("gold case must be an object")
    case = dict(value)
    if case.get("version") != GOLD_VERSION:
        raise AccuracyBenchmarkError("unsupported gold case version")

    case_id = _text(case.get("case_id"))
    if not case_id:
        raise AccuracyBenchmarkError("case_id is required")
    review_status = _text(case.get("review_status")).lower()
    if review_status not in REVIEW_STATUSES:
        raise AccuracyBenchmarkError("invalid review_status")
    review = case.get("review")
    if review_status in FINAL_REVIEW_STATUSES:
        if not isinstance(review, dict):
            raise AccuracyBenchmarkError("final review status requires review evidence")
        reviewer = _text(review.get("reviewer"))
        method = _text(review.get("method")).lower()
        reviewed_at = _text(review.get("reviewed_at"))
        if not reviewer:
            raise AccuracyBenchmarkError("review.reviewer is required")
        if method not in {"expert_review", "user_approval", "adjudication"}:
            raise AccuracyBenchmarkError("invalid review.method")
        try:
            timestamp = datetime.fromisoformat(reviewed_at)
        except ValueError as error:
            raise AccuracyBenchmarkError("review.reviewed_at must be ISO-8601") from error
        if timestamp.tzinfo is None:
            raise AccuracyBenchmarkError("review.reviewed_at must include timezone")
        case["review"] = {
            "reviewer": reviewer,
            "method": method,
            "reviewed_at": reviewed_at,
            "evidence_path": _text(review.get("evidence_path")),
        }

    labels = case.get("labels")
    if not isinstance(labels, dict):
        raise AccuracyBenchmarkError("labels must be an object")

    demand_rows = labels.get("demands")
    if not isinstance(demand_rows, list) or not demand_rows:
        raise AccuracyBenchmarkError("labels.demands must not be empty")
    demands: list[dict[str, Any]] = []
    demand_ids: set[str] = set()
    for row in demand_rows:
        if not isinstance(row, dict):
            raise AccuracyBenchmarkError("demand row must be an object")
        demand_id = _text(row.get("demand_id"))
        if not demand_id or demand_id in demand_ids:
            raise AccuracyBenchmarkError("demand_id must be unique and non-empty")
        demand_ids.add(demand_id)
        demands.append({
            "demand_id": demand_id,
            "requirement": _text(row.get("requirement")),
            "core": bool(row.get("core", True)),
            "status": normalize_demand_state(row.get("status")),
        })

    finding_rows = labels.get("findings") or []
    if not isinstance(finding_rows, list):
        raise AccuracyBenchmarkError("labels.findings must be a list")
    findings: list[dict[str, str]] = []
    finding_ids: set[str] = set()
    for row in finding_rows:
        if not isinstance(row, dict):
            raise AccuracyBenchmarkError("finding row must be an object")
        finding_id = _text(row.get("finding_id"))
        severity = _text(row.get("severity")).lower()
        if not finding_id or finding_id in finding_ids:
            raise AccuracyBenchmarkError("finding_id must be unique and non-empty")
        if severity not in FINDING_SEVERITIES:
            raise AccuracyBenchmarkError("invalid finding severity")
        finding_ids.add(finding_id)
        findings.append({"finding_id": finding_id, "severity": severity})

    score_range = labels.get("score_range")
    if not isinstance(score_range, dict):
        raise AccuracyBenchmarkError("labels.score_range must be an object")
    minimum = _finite(score_range.get("min"), "score_range.min")
    maximum = _finite(score_range.get("max"), "score_range.max")
    if minimum < 0 or maximum > 25 or minimum > maximum:
        raise AccuracyBenchmarkError("invalid score range")

    expert_total_score = labels.get("expert_total_score")
    if expert_total_score is not None:
        expert_total_score = _finite(expert_total_score, "expert_total_score")
        if not 0 <= expert_total_score <= 25:
            raise AccuracyBenchmarkError("invalid expert_total_score")

    expert_layer_scores = labels.get("layer_scores")
    if expert_layer_scores is not None:
        if not isinstance(expert_layer_scores, dict):
            raise AccuracyBenchmarkError("labels.layer_scores must be an object")
        expert_layer_scores = {
            str(layer).upper(): _finite(score, f"layer_scores.{layer}")
            for layer, score in expert_layer_scores.items()
            if str(layer).upper() in {"A", "B", "C", "D", "E"}
        }

    flags = labels.get("flags")
    if not isinstance(flags, dict):
        raise AccuracyBenchmarkError("labels.flags must be an object")
    confidence_ceiling = _text(flags.get("confidence_ceiling")).lower()
    if confidence_ceiling not in CONFIDENCE_RANK:
        raise AccuracyBenchmarkError("invalid confidence_ceiling")

    case.update({
        "case_id": case_id,
        "review_status": review_status,
        "padding_group": _text(case.get("padding_group")),
        "labels": {
            "demands": demands,
            "findings": findings,
            "score_range": {"min": minimum, "max": maximum},
            "expert_total_score": expert_total_score,
            "layer_scores": expert_layer_scores,
            "flags": {
                "passing_score_allowed": bool(flags.get("passing_score_allowed")),
                "strong_verdict_allowed": bool(flags.get("strong_verdict_allowed")),
                "confidence_ceiling": confidence_ceiling,
            },
        },
    })
    return case


def _walk_findings(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return []
    output: list[dict[str, Any]] = []
    logic = value.get("logic_check_evaluation")
    if isinstance(logic, dict):
        output.extend(row for row in logic.get("findings") or [] if isinstance(row, dict))
    general = value.get("general_evidence_contract")
    if isinstance(general, dict):
        output.extend(row for row in general.get("defects") or [] if isinstance(row, dict))
    return output


def _prediction_demands(grade: dict[str, Any]) -> list[dict[str, Any]]:
    ledger = grade.get("canonical_evaluation_ledger")
    if isinstance(ledger, dict) and ledger.get("marker") == (
        "CANONICAL_EVALUATION_LEDGER_V1"
    ):
        ledger_rows = ledger.get("rows")
        if isinstance(ledger_rows, list) and ledger_rows:
            rows = [
                {
                    "requirement_id": row.get("requirement_id"),
                    "requirement_text": row.get("requirement_text"),
                    "status": row.get("status"),
                }
                for row in ledger_rows
                if isinstance(row, dict)
            ]
        else:
            rows = []
    else:
        rows = None
    coverage = grade.get("question_type_coverage")
    if not isinstance(coverage, dict):
        coverage = {}
    explicit = coverage.get("explicit_requirement_coverage")
    if rows is None:
        rows = explicit.get("requirements") if isinstance(explicit, dict) else None
    if rows is None:
        summary = grade.get("question_type_coverage_summary")
        rows = summary.get("criteria_status_rows") if isinstance(summary, dict) else []

    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        demand_id = _text(
            row.get("demand_id")
            or row.get("requirement_id")
            or row.get("criterion")
        )
        if not demand_id or demand_id in seen:
            continue
        try:
            state = normalize_demand_state(
                row.get("demand_state") or row.get("status"),
                allow_unknown=True,
            )
        except AccuracyBenchmarkError:
            continue
        seen.add(demand_id)
        output.append({
            "demand_id": demand_id,
            "requirement": _text(
                row.get("requirement_text")
                or row.get("requirement")
                or row.get("criterion_text")
            ),
            "status": state,
        })
    return output


def prediction_from_grade(case_id: str, grade: Any) -> dict[str, Any]:
    if not isinstance(grade, dict):
        raise AccuracyBenchmarkError("grade must be an object")
    findings: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in _walk_findings(grade):
        finding_id = _text(
            row.get("finding_id")
            or row.get("rule_id")
            or row.get("source_rule_id")
            or row.get("defect_id")
            or row.get("id")
        )
        severity = _text(row.get("severity")).lower()
        if not finding_id or finding_id in seen or severity not in FINDING_SEVERITIES:
            continue
        seen.add(finding_id)
        findings.append({"finding_id": finding_id, "severity": severity})

    coverage_summary = grade.get("question_type_coverage_summary")
    overall = _text(
        coverage_summary.get("overall_coverage")
        if isinstance(coverage_summary, dict)
        else ""
    ).lower()
    score = grade.get("total_score", grade.get("final_total_score"))
    passing = grade.get("passing_score_allowed")
    if passing is None:
        passing = bool(grade.get("official_pass_met"))
    strong = grade.get("strong_verdict_allowed")
    if strong is None:
        strong = overall == "strong"

    return {
        "version": PREDICTION_VERSION,
        "case_id": _text(case_id),
        "demands": _prediction_demands(grade),
        "findings": findings,
        "total_score": _finite(score, "total_score"),
        "passing_score_allowed": bool(passing),
        "strong_verdict_allowed": bool(strong),
        "confidence": _text(grade.get("confidence")).lower() or "low",
        "layer_scores": {
            str(row.get("layer_id") or row.get("layer") or "").upper(): float(row["score"])
            for row in (grade.get("breakdown") or grade.get("layer_scores") or [])
            if isinstance(row, dict)
            and str(row.get("layer_id") or row.get("layer") or "").upper() in {"A", "B", "C", "D", "E"}
            and isinstance(row.get("score"), (int, float))
            and not isinstance(row.get("score"), bool)
        },
    }


def validate_prediction(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("version") != PREDICTION_VERSION:
        raise AccuracyBenchmarkError("invalid prediction")
    case_id = _text(value.get("case_id"))
    if not case_id:
        raise AccuracyBenchmarkError("prediction case_id is required")
    demands = []
    seen_demands: set[str] = set()
    for row in value.get("demands") or []:
        demand_id = _text(row.get("demand_id")) if isinstance(row, dict) else ""
        if not demand_id or demand_id in seen_demands:
            continue
        seen_demands.add(demand_id)
        demands.append({
            "demand_id": demand_id,
            "requirement": _text(row.get("requirement")),
            "status": normalize_demand_state(
                row.get("status"),
                allow_unknown=True,
            ),
        })
    findings = []
    seen_findings: set[str] = set()
    for row in value.get("findings") or []:
        finding_id = _text(row.get("finding_id")) if isinstance(row, dict) else ""
        severity = _text(row.get("severity")).lower() if isinstance(row, dict) else ""
        if not finding_id or finding_id in seen_findings or severity not in FINDING_SEVERITIES:
            continue
        seen_findings.add(finding_id)
        findings.append({"finding_id": finding_id, "severity": severity})
    confidence = _text(value.get("confidence")).lower()
    if confidence not in CONFIDENCE_RANK:
        confidence = "low"
    return {
        "version": PREDICTION_VERSION,
        "case_id": case_id,
        "demands": demands,
        "findings": findings,
        "total_score": _finite(value.get("total_score"), "total_score"),
        "passing_score_allowed": bool(value.get("passing_score_allowed")),
        "strong_verdict_allowed": bool(value.get("strong_verdict_allowed")),
        "confidence": confidence,
        "layer_scores": {
            str(layer).upper(): _finite(score, f"layer_scores.{layer}")
            for layer, score in (value.get("layer_scores") or {}).items()
            if str(layer).upper() in {"A", "B", "C", "D", "E"}
        } if isinstance(value.get("layer_scores"), dict) else {},
    }


def load_jsonl(path: Path, validator) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            rows.append(validator(json.loads(line)))
        except (json.JSONDecodeError, AccuracyBenchmarkError) as error:
            raise AccuracyBenchmarkError(f"{path}:{line_number}: {error}") from error
    return rows


def _demand_match_tokens(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(
            r"[0-9a-zA-Z가-힣]+",
            _text(value).casefold(),
        )
        if token not in _DEMAND_MATCH_STOPWORDS and len(token) >= 2
    }


def _demand_text_similarity(left: Any, right: Any) -> float:
    left_text = re.sub(r"\s+", " ", _text(left).casefold()).strip()
    right_text = re.sub(r"\s+", " ", _text(right).casefold()).strip()
    if not left_text or not right_text:
        return 0.0
    left_tokens = _demand_match_tokens(left_text)
    right_tokens = _demand_match_tokens(right_text)
    overlap = left_tokens & right_tokens
    if not overlap:
        return 0.0
    containment = len(overlap) / min(len(left_tokens), len(right_tokens))
    sequence = SequenceMatcher(None, left_text, right_text).ratio()
    return max(sequence, containment)


def _match_demand_rows(
    gold_rows: list[dict[str, Any]],
    predicted_rows: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Match exact canonical IDs first, then unique high-similarity texts."""

    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    used_gold: set[int] = set()
    used_predicted: set[int] = set()
    predicted_by_id: dict[str, list[int]] = {}
    for index, row in enumerate(predicted_rows):
        predicted_by_id.setdefault(row["demand_id"], []).append(index)
    for gold_index, gold in enumerate(gold_rows):
        candidates = predicted_by_id.get(gold["demand_id"], [])
        available = [index for index in candidates if index not in used_predicted]
        if len(available) != 1:
            continue
        predicted_index = available[0]
        used_gold.add(gold_index)
        used_predicted.add(predicted_index)
        matches.append((gold, predicted_rows[predicted_index]))

    candidates: list[tuple[float, int, int]] = []
    for gold_index, gold in enumerate(gold_rows):
        if gold_index in used_gold:
            continue
        for predicted_index, predicted in enumerate(predicted_rows):
            if predicted_index in used_predicted:
                continue
            similarity = _demand_text_similarity(
                gold.get("requirement"),
                predicted.get("requirement"),
            )
            if similarity >= 0.55:
                candidates.append((similarity, gold_index, predicted_index))
    for _similarity, gold_index, predicted_index in sorted(
        candidates,
        key=lambda row: (-row[0], row[1], row[2]),
    ):
        if gold_index in used_gold or predicted_index in used_predicted:
            continue
        used_gold.add(gold_index)
        used_predicted.add(predicted_index)
        matches.append((gold_rows[gold_index], predicted_rows[predicted_index]))
    return matches


def _prf(gold: set[str], predicted: set[str]) -> dict[str, float | int | None]:
    if not gold and not predicted:
        return {
            "true_positive": 0,
            "gold": 0,
            "predicted": 0,
            "precision": None,
            "recall": None,
            "f1": None,
        }
    true_positive = len(gold & predicted)
    precision = true_positive / len(predicted) if predicted else 0.0
    recall = true_positive / len(gold) if gold else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "true_positive": true_positive,
        "gold": len(gold),
        "predicted": len(predicted),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def _prf_counts(
    true_positive: int,
    gold: int,
    predicted: int,
) -> dict[str, float | int | None]:
    if not gold and not predicted:
        return {
            "true_positive": 0,
            "gold": 0,
            "predicted": 0,
            "precision": None,
            "recall": None,
            "f1": None,
        }
    precision = true_positive / predicted if predicted else 0.0
    recall = true_positive / gold if gold else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "true_positive": true_positive,
        "gold": gold,
        "predicted": predicted,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def measure_accuracy(
    gold_cases: Iterable[dict[str, Any]],
    predictions: Iterable[dict[str, Any]],
    *,
    include_draft: bool = False,
) -> dict[str, Any]:
    gold = [validate_gold_case(row) for row in gold_cases]
    prediction_map = {
        row["case_id"]: row
        for row in (validate_prediction(item) for item in predictions)
    }
    eligible = [
        row for row in gold
        if row["review_status"] in FINAL_REVIEW_STATUSES
        or (include_draft and row["review_status"] == "draft")
    ]
    evaluated = [row for row in eligible if row["case_id"] in prediction_map]

    gold_demand_count = 0
    predicted_demand_count = 0
    matched_demand_count = 0
    gold_finding_ids: set[str] = set()
    predicted_finding_ids: set[str] = set()
    matched_states = 0
    correct_states = 0
    score_distances: list[float] = []
    actual_total_errors: list[float] = []
    signed_total_errors: list[float] = []
    layer_errors: dict[str, list[float]] = {layer: [] for layer in "ABCDE"}
    exact_total_pairs: list[tuple[float, float]] = []
    padding_groups: dict[str, list[float]] = {}
    false_pass = 0
    false_strong = 0
    confidence_violations = 0
    false_high_score = 0
    case_rows = []

    for case in evaluated:
        case_id = case["case_id"]
        prediction = prediction_map[case_id]
        labels = case["labels"]
        gold_demands = labels["demands"]
        predicted_demands = prediction["demands"]
        demand_matches = _match_demand_rows(gold_demands, predicted_demands)
        gold_demand_count += len(gold_demands)
        predicted_demand_count += len(predicted_demands)
        matched_demand_count += len(demand_matches)
        for gold_demand, predicted_demand in demand_matches:
            matched_states += 1
            correct_states += int(
                gold_demand["status"] == predicted_demand["status"]
            )

        gold_major = {
            f"{case_id}:{row['finding_id']}"
            for row in labels["findings"]
            if row["severity"] in {"major", "fatal"}
        }
        predicted_major = {
            f"{case_id}:{row['finding_id']}"
            for row in prediction["findings"]
            if row["severity"] in {"major", "fatal"}
        }
        gold_finding_ids.update(gold_major)
        predicted_finding_ids.update(predicted_major)

        bounds = labels["score_range"]
        score = prediction["total_score"]
        distance = max(bounds["min"] - score, 0.0, score - bounds["max"])
        score_distances.append(distance)
        expert_total = labels.get("expert_total_score")
        if isinstance(expert_total, (int, float)):
            signed_error = score - float(expert_total)
            signed_total_errors.append(signed_error)
            actual_total_errors.append(abs(signed_error))
            exact_total_pairs.append((float(expert_total), score))
        expert_layers = labels.get("layer_scores")
        predicted_layers = prediction.get("layer_scores")
        if isinstance(expert_layers, dict) and isinstance(predicted_layers, dict):
            for layer in "ABCDE":
                if layer in expert_layers and layer in predicted_layers:
                    layer_errors[layer].append(abs(float(predicted_layers[layer]) - float(expert_layers[layer])))
        flags = labels["flags"]
        false_pass += int(prediction["passing_score_allowed"] and not flags["passing_score_allowed"])
        false_strong += int(prediction["strong_verdict_allowed"] and not flags["strong_verdict_allowed"])
        confidence_violations += int(
            CONFIDENCE_RANK[prediction["confidence"]]
            > CONFIDENCE_RANK[flags["confidence_ceiling"]]
        )
        false_high_score += int(score >= 20.0 and bounds["max"] < 20.0)
        padding_group = str(case.get("padding_group") or "").strip()
        if padding_group:
            padding_groups.setdefault(padding_group, []).append(score)
        case_rows.append({
            "case_id": case_id,
            "review_status": case["review_status"],
            "score": score,
            "score_range": bounds,
            "out_of_range_distance": round(distance, 4),
            "signed_total_error": round(score - float(expert_total), 4)
            if isinstance(expert_total, (int, float)) else None,
        })

    status = "OK"
    if not eligible:
        status = "NO_ELIGIBLE_CASES"
    elif not evaluated:
        status = "NO_MATCHED_PREDICTIONS"

    pairwise_total = 0
    pairwise_correct = 0
    for left_index, (left_gold, left_predicted) in enumerate(exact_total_pairs):
        for right_gold, right_predicted in exact_total_pairs[left_index + 1:]:
            if left_gold == right_gold:
                continue
            pairwise_total += 1
            if (left_gold > right_gold) == (left_predicted > right_predicted):
                pairwise_correct += 1
    padding_spreads = [
        max(scores) - min(scores)
        for scores in padding_groups.values()
        if len(scores) >= 2
    ]

    return {
        "schema_version": "expert_accuracy_report_v2",
        "status": status,
        "include_draft": bool(include_draft),
        "gold_case_count": len(gold),
        "eligible_case_count": len(eligible),
        "evaluated_case_count": len(evaluated),
        "demand_extraction": _prf_counts(
            matched_demand_count,
            gold_demand_count,
            predicted_demand_count,
        ),
        "demand_state_accuracy": (
            round(correct_states / matched_states, 4) if matched_states else None
        ),
        "matched_demand_state_count": matched_states,
        "major_finding_detection": _prf(gold_finding_ids, predicted_finding_ids),
        "mean_out_of_range_distance": (
            round(sum(score_distances) / len(score_distances), 4)
            if score_distances else None
        ),
        "actual_total_mae": (
            round(sum(actual_total_errors) / len(actual_total_errors), 4)
            if actual_total_errors else None
        ),
        "mean_signed_total_error": (
            round(sum(signed_total_errors) / len(signed_total_errors), 4)
            if signed_total_errors else None
        ),
        "layer_mae": {
            layer: round(sum(errors) / len(errors), 4) if errors else None
            for layer, errors in layer_errors.items()
        },
        "false_pass_count": false_pass,
        "false_strong_count": false_strong,
        "false_high_score_count": false_high_score,
        "confidence_ceiling_violation_count": confidence_violations,
        "pairwise_ordering_accuracy": (
            round(pairwise_correct / pairwise_total, 4)
            if pairwise_total else None
        ),
        "pairwise_ordering_pair_count": pairwise_total,
        "padding_sensitivity": {
            "group_count": len(padding_spreads),
            "mean_score_spread": round(sum(padding_spreads) / len(padding_spreads), 4)
            if padding_spreads else None,
            "max_score_spread": round(max(padding_spreads), 4)
            if padding_spreads else None,
        },
        "cases": case_rows,
    }
