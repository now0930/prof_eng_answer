from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


# CONTROL_VALVE_CORRECTNESS_BRIDGE_V1

_MAJOR_SEVERITIES = {
    "major",
    "fatal",
}
_SCORE_FIELDS = (
    "score",
    "total_score",
    "final_score",
    "raw_total_score",
    "adjusted_total_score",
    "layer_scores",
)

_FINDING_REQUIREMENT_POLICY = {
    "friction_viscous_model_overgeneralized": {
        "preferred_demands": (
            "DEFINE_EXPLAIN",
            "PRINCIPLE_INTERPRET",
        ),
        "keywords": (
            "마찰",
            "불평형력",
            "friction",
        ),
    },
    "force_balance_requirement_sign_contradiction": {
        "preferred_demands": (
            "DESIGN",
            "PRINCIPLE_INTERPRET",
            "IMPLEMENT",
        ),
        "keywords": (
            "spring",
            "스프링",
            "fail safe",
            "설계",
        ),
    },
}


def _score_snapshot(
    grade: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: copy.deepcopy(grade.get(key))
        for key in _SCORE_FIELDS
        if key in grade
    }


def _stable_defect_id(
    finding: dict[str, Any],
) -> str:
    payload = {
        "source": "control_valve_formula_check",
        "finding_id": str(
            finding.get("id") or ""
        ),
        "evidence": str(
            finding.get("evidence") or ""
        ),
    }
    digest = hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:12]
    return f"defect_{digest}"


def _question_contract(
    grade: dict[str, Any],
) -> dict[str, Any]:
    direct = grade.get("question_demand_contract")

    if isinstance(direct, dict):
        return direct

    parsed = grade.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "question_demand_contract"
        )

        if isinstance(nested, dict):
            return nested

    return {}


def _requirement_id_for_finding(
    grade: dict[str, Any],
    finding_id: str,
) -> str:
    policy = _FINDING_REQUIREMENT_POLICY.get(
        finding_id,
        {},
    )
    requirements = _question_contract(
        grade
    ).get("requirements")

    if not isinstance(requirements, list):
        return ""

    preferred_demands = tuple(
        str(value)
        for value in policy.get(
            "preferred_demands",
            (),
        )
    )
    keywords = tuple(
        str(value).lower()
        for value in policy.get(
            "keywords",
            (),
        )
    )

    candidates = []

    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue

        requirement_id = str(
            requirement.get("requirement_id")
            or ""
        )
        demand_kind = str(
            requirement.get("demand_kind")
            or ""
        )
        text = str(
            requirement.get("requirement_text")
            or ""
        )
        lowered = text.lower()

        if not requirement_id:
            continue

        score = 0

        if demand_kind in preferred_demands:
            score += (
                len(preferred_demands)
                - preferred_demands.index(
                    demand_kind
                )
            ) * 10

        score += sum(
            1
            for keyword in keywords
            if keyword in lowered
        )

        candidates.append(
            (
                score,
                requirement_id,
            )
        )

    if not candidates:
        return ""

    candidates.sort(
        key=lambda row: (
            row[0],
            row[1],
        ),
        reverse=True,
    )
    return candidates[0][1]


def _empty_contract() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "contract_marker": (
            "GENERAL_EVIDENCE_CONTRACT_V1"
        ),
        "mode": "diagnostic_only",
        "score_effect": "none",
        "claims": [],
        "formulas": [],
        "defects": [],
        "field_judgements": [],
        "summary": {},
    }


def _current_contract(
    grade: dict[str, Any],
) -> dict[str, Any]:
    direct = grade.get(
        "general_evidence_contract"
    )

    if isinstance(direct, dict):
        return copy.deepcopy(direct)

    parsed = grade.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "general_evidence_contract"
        )

        if isinstance(nested, dict):
            return copy.deepcopy(nested)

    return _empty_contract()


def _major_findings(
    grade: dict[str, Any],
) -> list[dict[str, Any]]:
    evaluation = grade.get(
        "formula_check_evaluation"
    )

    if not isinstance(evaluation, dict):
        return []

    if not evaluation.get("applicable"):
        return []

    findings = evaluation.get("findings")

    if not isinstance(findings, list):
        return []

    return [
        copy.deepcopy(finding)
        for finding in findings
        if isinstance(finding, dict)
        and str(
            finding.get("severity") or ""
        ).lower()
        in _MAJOR_SEVERITIES
    ]


def merge_control_valve_findings_into_evidence(
    grade: Any,
) -> Any:
    if not isinstance(grade, dict):
        return grade

    output = copy.deepcopy(grade)
    before = _score_snapshot(output)
    findings = _major_findings(output)

    if not findings:
        return output

    contract = _current_contract(output)
    defects = contract.get("defects")

    if not isinstance(defects, list):
        defects = []

    existing_source_ids = {
        str(
            defect.get("source_finding_id")
            or ""
        )
        for defect in defects
        if isinstance(defect, dict)
    }
    merged_ids = []

    for finding in findings:
        finding_id = str(
            finding.get("id") or ""
        )

        if not finding_id:
            continue

        if finding_id in existing_source_ids:
            continue

        defect_id = _stable_defect_id(
            finding
        )
        defects.append(
            {
                "defect_id": defect_id,
                "defect_type": (
                    "correctness_error"
                ),
                "severity": "major",
                "owner_layer": "C",
                "requirement_id": (
                    _requirement_id_for_finding(
                        output,
                        finding_id,
                    )
                ),
                "affected_claim_ids": [],
                "evidence_text": str(
                    finding.get("evidence")
                    or ""
                ),
                "explanation": str(
                    finding.get("message")
                    or ""
                ),
                "correct_rule": str(
                    finding.get("correct_rule")
                    or ""
                ),
                "source": (
                    "control_valve_formula_check"
                ),
                "source_finding_id": finding_id,
                "diagnostic_only": True,
            }
        )
        existing_source_ids.add(
            finding_id
        )
        merged_ids.append(defect_id)

    contract["defects"] = defects
    summary = contract.get("summary")

    if not isinstance(summary, dict):
        summary = {}

    summary[
        "verified_correctness_defect_count"
    ] = sum(
        1
        for defect in defects
        if isinstance(defect, dict)
        and defect.get("defect_type")
        == "correctness_error"
    )
    summary[
        "control_valve_bridge_marker"
    ] = "CONTROL_VALVE_CORRECTNESS_BRIDGE_V1"
    contract["summary"] = summary

    output[
        "general_evidence_contract"
    ] = copy.deepcopy(contract)
    parsed = output.get("parsed")

    if not isinstance(parsed, dict):
        parsed = {}
        output["parsed"] = parsed

    parsed[
        "general_evidence_contract"
    ] = copy.deepcopy(contract)
    output[
        "control_valve_correctness_bridge"
    ] = {
        "schema_version": "1.0",
        "marker": (
            "CONTROL_VALVE_CORRECTNESS_BRIDGE_V1"
        ),
        "score_effect": "none",
        "direct_score_application": False,
        "merged_defect_ids": merged_ids,
        "merged_count": len(merged_ids),
    }

    if before != _score_snapshot(output):
        raise RuntimeError(
            "Control-valve correctness bridge "
            "changed numeric score state"
        )

    return output
