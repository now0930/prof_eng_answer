"""Layer-specific semantic downward guard.

The module preserves the existing guard ratios but decides eligibility per
owner layer. It activates only when the general evidence contract is present.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Callable

LAYER_EVIDENCE_GUARD_SCHEMA_VERSION = "1.0"
LAYER_EVIDENCE_GUARD_MARKER = "LAYER_SPECIFIC_EVIDENCE_GUARD_V1"

_ALLOWED_LAYERS = ("A", "B", "C", "D", "E")
_MAX_DROP_RATIO = {
    "A": 0.15,
    "B": 0.15,
    "C": 0.20,
    "D": 0.15,
    "E": 0.15,
}

_REQUIREMENT_OWNER = {
    "DEFINE_EXPLAIN": "C",
    "PRINCIPLE_INTERPRET": "C",
    "COMPARE": "C",
    "DIAGNOSE_CAUSE": "C",
    "CALCULATE": "C",
    "SELECT": "D",
    "ACTION_IMPROVE": "D",
    "PROCEDURE": "D",
    "DESIGN": "D",
    "IMPLEMENT": "D",
    "EVALUATE_VERIFY": "D",
}

_DEFECT_TYPE_ALIASES = {
    "depth_gap": "core_depth_gap",
    "advanced_missing": "advanced_detail_missing",
    "formula_integrity_warning": "presentation_issue",
    "operator_missing": "presentation_issue",
}


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value or "").strip()


def _layer(value: Any) -> str:
    token = _text(value).upper()
    return token if token in _ALLOWED_LAYERS else ""


def _defect_type(value: Any) -> str:
    token = _text(value).lower()
    return _DEFECT_TYPE_ALIASES.get(token, token)


def _severity(value: Any) -> str:
    return _text(value).lower()


def _parsed(gemini_eval: Any) -> dict[str, Any]:
    root = _dict(gemini_eval)
    parsed = root.get("parsed")
    return parsed if isinstance(parsed, dict) else root


def _contract(
    gemini_eval: Any,
    key: str,
) -> dict[str, Any]:
    root = _dict(gemini_eval)
    parsed = _parsed(gemini_eval)

    value = root.get(key)
    if isinstance(value, dict):
        return value

    value = parsed.get(key)
    return value if isinstance(value, dict) else {}


def has_general_evidence_contract(
    gemini_eval: Any,
) -> bool:
    return bool(
        _contract(
            gemini_eval,
            "general_evidence_contract",
        )
    )


def _stable_issue_id(row: dict[str, Any]) -> str:
    explicit = _text(
        row.get("defect_id")
        or row.get("issue_id")
        or row.get("id")
    )
    if explicit:
        return explicit

    payload = {
        "type": _defect_type(
            row.get("defect_type")
            or row.get("issue_type")
            or row.get("type")
        ),
        "owner": _layer(
            row.get("owner_layer")
            or row.get("primary_owner_layer")
        ),
        "evidence": _text(
            row.get("evidence_text")
            or row.get("evidence")
        ),
        "explanation": _text(
            row.get("explanation")
            or row.get("reason")
            or row.get("description")
        ),
    }
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:12]
    return f"issue_{digest}"


def _canonical_issue_rows(
    gemini_eval: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parsed = _parsed(gemini_eval)
    general = _contract(
        gemini_eval,
        "general_evidence_contract",
    )

    source_rows = []

    for row in _list(general.get("defects")):
        if isinstance(row, dict):
            source_rows.append(("general", row))

    for row in _list(parsed.get("layer_issue_ownership")):
        if isinstance(row, dict):
            source_rows.append(("legacy", row))

    canonical: dict[str, dict[str, Any]] = {}
    conflicts = []

    for source, raw in source_rows:
        issue_id = _stable_issue_id(raw)
        owner = _layer(
            raw.get("owner_layer")
            or raw.get("primary_owner_layer")
        )
        normalized = {
            "issue_id": issue_id,
            "source": source,
            "owner_layer": owner,
            "defect_type": _defect_type(
                raw.get("defect_type")
                or raw.get("issue_type")
                or raw.get("type")
            ),
            "severity": _severity(raw.get("severity")),
            "invalidates_core_conclusion": (
                raw.get("invalidates_core_conclusion")
                is True
            ),
            "requirement_id": _text(
                raw.get("requirement_id")
                or raw.get("requirement")
            ),
            "evidence_text": _text(
                raw.get("evidence_text")
                or raw.get("evidence")
            ),
            "explanation": _text(
                raw.get("explanation")
                or raw.get("reason")
                or raw.get("description")
            ),
        }

        previous = canonical.get(issue_id)

        if previous is None:
            canonical[issue_id] = normalized
            continue

        previous_owner = previous.get("owner_layer")
        if (
            owner
            and previous_owner
            and owner != previous_owner
        ):
            conflicts.append(
                {
                    "issue_id": issue_id,
                    "canonical_owner_layer": previous_owner,
                    "ignored_owner_layer": owner,
                    "canonical_source": previous.get("source"),
                    "ignored_source": source,
                }
            )

        if (
            previous.get("source") != "general"
            and source == "general"
        ):
            canonical[issue_id] = normalized

    return list(canonical.values()), conflicts


def _question_requirement_map(
    gemini_eval: Any,
) -> dict[str, str]:
    contract = _contract(
        gemini_eval,
        "question_demand_contract",
    )
    result = {}

    for row in _list(contract.get("requirements")):
        if not isinstance(row, dict):
            continue

        requirement_id = _text(
            row.get("requirement_id")
        )
        demand_kind = _text(
            row.get("demand_kind")
        ).upper()

        if requirement_id:
            result[requirement_id] = demand_kind

    return result


def _explicit_requirement_rows(
    gemini_eval: Any,
) -> list[dict[str, Any]]:
    parsed = _parsed(gemini_eval)
    coverage = _dict(
        parsed.get("question_type_coverage")
    )
    explicit = _dict(
        coverage.get("explicit_requirement_coverage")
    )
    return [
        row
        for row in _list(explicit.get("requirements"))
        if isinstance(row, dict)
    ]


def _block(
    policy: dict[str, Any],
    layer_id: str,
    reason: str,
    *,
    issue_id: str = "",
    requirement_id: str = "",
) -> None:
    if layer_id not in policy:
        return

    row = policy[layer_id]
    row["eligible"] = False

    if reason not in row["blocked_reasons"]:
        row["blocked_reasons"].append(reason)

    if issue_id and issue_id not in row["owned_issue_ids"]:
        row["owned_issue_ids"].append(issue_id)

    if (
        requirement_id
        and requirement_id
        not in row["blocking_requirement_ids"]
    ):
        row["blocking_requirement_ids"].append(
            requirement_id
        )


def build_layer_evidence_policy(
    gemini_eval: Any,
) -> dict[str, Any]:
    layer_policy = {
        layer_id: {
            "eligible": True,
            "max_drop_ratio": _MAX_DROP_RATIO[layer_id],
            "blocked_reasons": [],
            "owned_issue_ids": [],
            "blocking_requirement_ids": [],
        }
        for layer_id in _ALLOWED_LAYERS
    }

    issues, ownership_conflicts = (
        _canonical_issue_rows(gemini_eval)
    )
    requirement_map = _question_requirement_map(
        gemini_eval
    )
    incorrect_count = 0
    missing_count = 0
    core_incorrect = 0
    core_missing = 0

    for issue in issues:
        owner = issue["owner_layer"]
        defect_type = issue["defect_type"]
        severity = issue["severity"]
        invalidates = issue[
            "invalidates_core_conclusion"
        ]
        issue_id = issue["issue_id"]

        if not owner:
            continue

        if defect_type == "correctness_error":
            if severity != "warning" or invalidates:
                _block(
                    layer_policy,
                    owner,
                    "owned_correctness_error",
                    issue_id=issue_id,
                )
            continue

        if defect_type == "core_depth_gap":
            if severity in {"major", "fatal"} or invalidates:
                _block(
                    layer_policy,
                    owner,
                    "owned_major_core_depth_gap",
                    issue_id=issue_id,
                )

    for requirement in _explicit_requirement_rows(
        gemini_eval
    ):
        status = _text(
            requirement.get("status")
        ).lower()

        if status == "incorrect":
            incorrect_count += 1
        elif status == "missing":
            missing_count += 1
        else:
            continue

        if requirement.get("is_core") is not True:
            continue

        requirement_id = _text(
            requirement.get("requirement_id")
            or requirement.get("id")
        )

        if status == "incorrect":
            core_incorrect += 1
        else:
            core_missing += 1

        _block(
            layer_policy,
            "B",
            f"core_requirement_{status}",
            requirement_id=requirement_id,
        )

        owner = _layer(
            requirement.get("owner_layer")
            or requirement.get("primary_owner_layer")
        )

        if not owner and requirement_id:
            demand_kind = requirement_map.get(
                requirement_id,
                "",
            )
            owner = _REQUIREMENT_OWNER.get(
                demand_kind,
                "",
            )

        if owner and owner != "B":
            _block(
                layer_policy,
                owner,
                f"owned_core_requirement_{status}",
                requirement_id=requirement_id,
            )

    eligible_layers = [
        layer_id
        for layer_id, row in layer_policy.items()
        if row["eligible"] is True
    ]
    blocked_layers = [
        layer_id
        for layer_id, row in layer_policy.items()
        if row["eligible"] is not True
    ]

    return {
        "schema_version": LAYER_EVIDENCE_GUARD_SCHEMA_VERSION,
        "marker": LAYER_EVIDENCE_GUARD_MARKER,
        "mode": "layer_specific",
        "one_issue_one_owner": True,
        "eligible": bool(eligible_layers),
        "all_layers_eligible": not blocked_layers,
        "eligible_layers": eligible_layers,
        "blocked_layers": blocked_layers,
        "layers": layer_policy,
        "canonical_issue_rows": issues,
        "ownership_conflicts": ownership_conflicts,
        "incorrect_count": incorrect_count,
        "missing_count": missing_count,
        "core_incorrect": core_incorrect,
        "core_missing": core_missing,
    }


def apply_layer_specific_evidence_guard(
    layer_scores: Any,
    baseline_scores: Any,
    gemini_eval: Any,
    scoring_model: Any,
    *,
    maximum_resolver: Callable[
        [str, dict[str, Any], Any],
        float,
    ],
) -> tuple[Any, dict[str, Any]]:
    policy = build_layer_evidence_policy(
        gemini_eval
    )
    diagnostic = {
        **policy,
        "applied": False,
        "adjustments": [],
        "reason": (
            "계층별 owner evidence에 따라 semantic "
            "하향 제한 적용 여부를 분리함."
        ),
    }

    if not isinstance(layer_scores, list):
        return layer_scores, diagnostic

    baseline = (
        dict(baseline_scores)
        if isinstance(baseline_scores, dict)
        else {}
    )
    result = copy.deepcopy(layer_scores)

    for row in result:
        if not isinstance(row, dict):
            continue

        layer_id = _layer(row.get("layer_id"))
        layer_policy = policy["layers"].get(layer_id)

        if not layer_id or not isinstance(
            layer_policy,
            dict,
        ):
            continue

        row["layer_evidence_guard_eligible"] = (
            layer_policy["eligible"]
        )
        row["layer_evidence_guard_blocked_reasons"] = list(
            layer_policy["blocked_reasons"]
        )
        row["layer_evidence_guard_owned_issue_ids"] = list(
            layer_policy["owned_issue_ids"]
        )

        if layer_policy["eligible"] is not True:
            row["layer_evidence_guard_applied"] = False
            continue

        try:
            before_semantic = float(
                baseline.get(layer_id)
            )
            current_score = float(
                row.get("score") or 0.0
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
        ):
            continue

        try:
            maximum = float(
                maximum_resolver(
                    layer_id,
                    row,
                    scoring_model,
                )
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
        ):
            continue

        max_drop = round(
            maximum
            * float(
                layer_policy["max_drop_ratio"]
            ),
            4,
        )
        minimum_allowed = round(
            max(
                0.0,
                before_semantic - max_drop,
            ),
            4,
        )

        row["layer_evidence_guard_floor"] = round(
            minimum_allowed,
            2,
        )

        if current_score >= minimum_allowed:
            row["layer_evidence_guard_applied"] = False
            continue

        guarded_score = round(
            min(
                before_semantic,
                minimum_allowed,
            ),
            2,
        )
        row[
            "score_before_layer_evidence_guard"
        ] = current_score
        row["score"] = guarded_score
        row["layer_evidence_guard_applied"] = True

        diagnostic["adjustments"].append(
            {
                "layer_id": layer_id,
                "before": round(current_score, 2),
                "after": guarded_score,
                "baseline": round(
                    before_semantic,
                    2,
                ),
                "floor": round(
                    minimum_allowed,
                    2,
                ),
                "max_drop_ratio": layer_policy[
                    "max_drop_ratio"
                ],
            }
        )

    diagnostic["applied"] = bool(
        diagnostic["adjustments"]
    )
    return result, diagnostic
