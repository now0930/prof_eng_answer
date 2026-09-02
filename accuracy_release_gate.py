"""Release readiness gate for expert-labelled cross-topic accuracy."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from expert_accuracy_benchmark import FINAL_REVIEW_STATUSES, validate_gold_case


POLICY_VERSION = "expert_accuracy_release_policy_v1"
GATE_MARKER = "EXPERT_ACCURACY_RELEASE_GATE_V1"


class AccuracyReleaseGateError(ValueError):
    pass


def validate_release_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("version") != POLICY_VERSION:
        raise AccuracyReleaseGateError("invalid release policy")
    policy = dict(value)
    integer_fields = (
        "minimum_reviewed_cases",
        "minimum_distinct_topics",
        "minimum_cases_per_question_type",
        "minimum_major_finding_labels",
        "maximum_false_pass_count",
        "maximum_false_strong_count",
        "maximum_confidence_ceiling_violation_count",
    )
    for key in integer_fields:
        number = policy.get(key)
        if isinstance(number, bool) or not isinstance(number, int) or number < 0:
            raise AccuracyReleaseGateError(f"{key} must be a non-negative integer")
    required_types = policy.get("required_question_types")
    if not isinstance(required_types, list) or not required_types:
        raise AccuracyReleaseGateError("required_question_types must not be empty")
    for key in (
        "minimum_demand_extraction_f1",
        "minimum_demand_state_accuracy",
        "minimum_major_finding_precision",
        "minimum_major_finding_recall",
    ):
        value = policy.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise AccuracyReleaseGateError(f"{key} must be within [0, 1]")
    mae = policy.get("maximum_score_range_mae")
    if isinstance(mae, bool) or not isinstance(mae, (int, float)) or mae < 0:
        raise AccuracyReleaseGateError("maximum_score_range_mae must be non-negative")
    return policy


def _metric(report: dict[str, Any], *path: str) -> Any:
    value: Any = report
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def evaluate_accuracy_release_gate(
    report: Any,
    gold_cases: Iterable[dict[str, Any]],
    policy: Any,
) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise AccuracyReleaseGateError("accuracy report must be an object")
    policy = validate_release_policy(policy)
    gold = [validate_gold_case(row) for row in gold_cases]
    reviewed = [row for row in gold if row["review_status"] in FINAL_REVIEW_STATUSES]
    topics = {
        str(topic).strip()
        for row in reviewed
        for topic in row.get("topic_ids", [])
        if str(topic).strip()
    }
    qtype_counts = Counter(str(row.get("question_type") or "").strip() for row in reviewed)
    major_labels = sum(
        1 for row in reviewed for finding in row["labels"]["findings"]
        if finding["severity"] in {"major", "fatal"}
    )
    blockers: list[dict[str, Any]] = []

    def minimum(code: str, actual: Any, required: Any) -> None:
        if actual is None or actual < required:
            blockers.append({"code": code, "actual": actual, "required": required})

    def maximum(code: str, actual: Any, required: Any) -> None:
        if actual is None or actual > required:
            blockers.append({"code": code, "actual": actual, "required": required})

    minimum("REVIEWED_CASE_COUNT", len(reviewed), policy["minimum_reviewed_cases"])
    minimum("DISTINCT_TOPIC_COUNT", len(topics), policy["minimum_distinct_topics"])
    minimum("MAJOR_FINDING_LABEL_COUNT", major_labels, policy["minimum_major_finding_labels"])
    for question_type in policy["required_question_types"]:
        minimum(
            f"QUESTION_TYPE_CASE_COUNT:{question_type}",
            qtype_counts.get(question_type, 0),
            policy["minimum_cases_per_question_type"],
        )
    minimum(
        "EVALUATED_CASE_COUNT",
        report.get("evaluated_case_count"),
        policy["minimum_reviewed_cases"],
    )
    minimum(
        "DEMAND_EXTRACTION_F1",
        _metric(report, "demand_extraction", "f1"),
        policy["minimum_demand_extraction_f1"],
    )
    minimum(
        "DEMAND_STATE_ACCURACY",
        report.get("demand_state_accuracy"),
        policy["minimum_demand_state_accuracy"],
    )
    minimum(
        "MAJOR_FINDING_PRECISION",
        _metric(report, "major_finding_detection", "precision"),
        policy["minimum_major_finding_precision"],
    )
    minimum(
        "MAJOR_FINDING_RECALL",
        _metric(report, "major_finding_detection", "recall"),
        policy["minimum_major_finding_recall"],
    )
    maximum("SCORE_RANGE_MAE", report.get("score_range_mae"), policy["maximum_score_range_mae"])
    maximum("FALSE_PASS_COUNT", report.get("false_pass_count"), policy["maximum_false_pass_count"])
    maximum("FALSE_STRONG_COUNT", report.get("false_strong_count"), policy["maximum_false_strong_count"])
    maximum(
        "CONFIDENCE_CEILING_VIOLATION_COUNT",
        report.get("confidence_ceiling_violation_count"),
        policy["maximum_confidence_ceiling_violation_count"],
    )
    return {
        "version": POLICY_VERSION,
        "marker": GATE_MARKER,
        "decision": "READY" if not blockers else "HOLD",
        "ready": not blockers,
        "blockers": blockers,
        "dataset": {
            "reviewed_case_count": len(reviewed),
            "distinct_topic_count": len(topics),
            "question_type_counts": dict(sorted(qtype_counts.items())),
            "major_finding_label_count": major_labels,
        },
        "policy": policy,
    }
