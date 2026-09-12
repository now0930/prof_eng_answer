"""Deterministic score/verdict owner with explicit abstention on coverage gaps."""

from __future__ import annotations

import re
from typing import Any, Mapping

from deterministic_score_evidence import evaluate_score_evidence


VERSION = "deterministic_score_engine_v1"
MARKER = "DETERMINISTIC_SCORE_ENGINE_V1"
_CREDIT = {"SATISFIED": 1.0, "PARTIAL": 0.5, "WRONG": 0.0, "MISSING": 0.0}
_IMPORTANCE_WEIGHT = {"core": 2.0, "important": 1.5, "normal": 1.0, "supporting": 0.75}
MINIMUM_SATISFIED_RATIO_FOR_PASS = 0.25
PASS_EVIDENCE_CEILING_RATIO = 0.58
NO_SATISFIED_NONFATAL_CEILING_RATIO = 0.44
MAXIMUM_AUTOMATIC_SCORE_RATIO = 0.96
HIGH_SCORE_MINIMUM_SATISFIED_RATIO = 0.60
HIGH_SCORE_MAXIMUM_MISSING_RATIO = 0.10
HIGH_SCORE_EVIDENCE_CEILING_RATIO = 0.7996
MINIMUM_NONEMPTY_ATTEMPT_SCORE = 4.5
MINIMUM_EVIDENCED_ATTEMPT_SCORE = 7.0
TECHNICALLY_ADEQUATE_SCORE_FLOOR = 15.0
_SELF_DECLARED_GAP = re.compile(
    r"(?:설명|제시|검토|작성|포함)(?:하|되)?지\s*못|누락(?:했|되|함)|모르(?:겠|는)"
)


def _scoring_groups(requirements: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Collapse multiple evidence rows that represent one engineering demand."""
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for index, row in enumerate(requirements):
        group_id = str(
            row.get("score_group_id")
            or f"{row.get('owner_topic_id', '')}:{row.get('requirement_id', index)}"
        ).strip()
        grouped.setdefault(group_id, []).append(row)
    output = []
    for group_id, rows in grouped.items():
        statuses = [str(row.get("status") or "") for row in rows]
        if "WRONG" in statuses:
            status = "WRONG"
        elif "SATISFIED" in statuses:
            status = "SATISFIED"
        elif "PARTIAL" in statuses:
            status = "PARTIAL"
        elif "MISSING" in statuses:
            status = "MISSING"
        else:
            status = statuses[0] if statuses else "UNKNOWN"
        output.append({
            "score_group_id": group_id,
            "status": status,
            "requirement_ids": [str(row.get("requirement_id") or "") for row in rows],
            "importance": max(
                (str(row.get("importance") or "normal").casefold() for row in rows),
                key=lambda value: _IMPORTANCE_WEIGHT.get(value, 1.0),
            ),
            "pass_required": any(bool(row.get("pass_required")) for row in rows),
        })
    return output


def calculate_deterministic_score(
    requirement_evaluation: Mapping[str, Any],
    *,
    max_score: float = 25.0,
    answer_text: str | None = None,
) -> dict[str, Any]:
    requirements = requirement_evaluation.get("requirements")
    if not isinstance(requirements, list):
        requirements = []
    scoring_groups = _scoring_groups(requirements)
    unknown = [row for row in scoring_groups if row.get("status") not in _CREDIT]
    coverage_complete = bool(scoring_groups) and not unknown
    base = {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "llm_verdict_authority": 0,
        "max_score": float(max_score),
        "coverage_complete": coverage_complete,
    }
    if not coverage_complete:
        return {
            **base,
            "decision": "ABSTAIN",
            "total_score": None,
            "verdict": "UNKNOWN",
            "external_llm_required_for_verdict": True,
            "reason": "deterministic_requirement_coverage_incomplete",
        }

    def weight(row: Mapping[str, Any]) -> float:
        return _IMPORTANCE_WEIGHT.get(str(row.get("importance") or "normal"), 1.0)

    total_weight = sum(weight(row) for row in scoring_groups)
    requirement_ratio = sum(
        _CREDIT[row["status"]] * weight(row) for row in scoring_groups
    ) / total_weight
    satisfied_ratio = sum(
        weight(row) for row in scoring_groups if row["status"] == "SATISFIED"
    ) / total_weight
    technical_evidence_texts = [
        str(row.get("evidence_text") or "")
        for row in requirements
        if row.get("status") in {"SATISFIED", "PARTIAL"}
        and str(row.get("evidence_text") or "").strip()
    ]
    score_evidence = (
        evaluate_score_evidence(
            answer_text,
            technical_evidence_texts=technical_evidence_texts,
        ) if answer_text is not None else None
    )
    if score_evidence is None:
        raw_score = float(max_score) * requirement_ratio
        breakdown = None
        correctness_ratio = requirement_ratio
    else:
        addressed = [row for row in scoring_groups if row["status"] != "MISSING"]
        correctness_ratio = (
            sum(_CREDIT[row["status"]] * weight(row) for row in addressed)
            / sum(weight(row) for row in addressed)
            if addressed else 0.0
        )
        breakdown = {
            "A_structure": score_evidence["structure"]["score"],
            "B_requirement_completeness": round(6.0 * requirement_ratio, 6),
            "C_fact_correctness": round(8.0 * correctness_ratio, 6),
            "D_engineering_judgment": min(
                score_evidence["engineering_judgment"]["score"],
                round(6.0 * requirement_ratio, 6),
            ),
            "E_linkage": min(
                score_evidence["linkage"]["score"],
                round(2.0 * requirement_ratio, 6),
            ),
        }
        raw_score = sum(breakdown.values())
    score_before_floors = raw_score
    attempt_floor_applied = bool(answer_text and answer_text.strip() and raw_score < MINIMUM_NONEMPTY_ATTEMPT_SCORE)
    if attempt_floor_applied:
        raw_score = MINIMUM_NONEMPTY_ATTEMPT_SCORE
    evidenced_attempt_floor_applied = bool(
        not requirement_evaluation.get("fatal_or_core_error")
        and requirement_ratio > 0.0
        and raw_score < MINIMUM_EVIDENCED_ATTEMPT_SCORE
    )
    if evidenced_attempt_floor_applied:
        raw_score = MINIMUM_EVIDENCED_ATTEMPT_SCORE
    technically_adequate_floor_applied = bool(
        not requirement_evaluation.get("fatal_or_core_error")
        and requirement_ratio >= 0.5
        and correctness_ratio >= 0.875
        and satisfied_ratio >= 0.5
        and not _SELF_DECLARED_GAP.search(str(answer_text or ""))
        and raw_score < TECHNICALLY_ADEQUATE_SCORE_FLOOR
    )
    if technically_adequate_floor_applied:
        raw_score = TECHNICALLY_ADEQUATE_SCORE_FLOOR
    # Fatal findings cap a score; they never create credit or a minimum score.
    substantive_fatal_floor_applied = False
    ceilings = [
        float(row["recommended_ceiling"])
        for row in requirement_evaluation.get("findings", [])
        if row.get("classification") in {"fatal", "core_error"}
        and isinstance(row.get("recommended_ceiling"), (int, float))
    ]
    all_ceilings = list(ceilings)
    # The generic structure/judgment/linkage cues are necessary supporting
    # evidence, but they cannot prove the exceptional depth needed for a
    # perfect score.  Reserve the final point until a future deterministic
    # exceptional-evidence contract owns that decision.
    all_ceilings.append(float(max_score) * MAXIMUM_AUTOMATIC_SCORE_RATIO)
    missing_ratio = sum(
        weight(row) for row in scoring_groups if row["status"] == "MISSING"
    ) / total_weight
    wrong_count = sum(row["status"] == "WRONG" for row in scoring_groups)
    core_requirement_gap_count = sum(
        row["importance"] == "core" and row["status"] in {"WRONG", "MISSING"}
        for row in scoring_groups
    )
    pass_required_gap_count = sum(
        row["pass_required"] and row["status"] != "SATISFIED"
        for row in scoring_groups
    )
    minimum_satisfied_ratio_for_pass = MINIMUM_SATISFIED_RATIO_FOR_PASS
    pass_evidence_eligible = bool(
        satisfied_ratio >= minimum_satisfied_ratio_for_pass
        and wrong_count == 0
        and pass_required_gap_count == 0
    )
    if not pass_evidence_eligible:
        all_ceilings.append(float(max_score) * PASS_EVIDENCE_CEILING_RATIO)
    high_score_evidence_eligible = bool(
        satisfied_ratio >= HIGH_SCORE_MINIMUM_SATISFIED_RATIO
        and missing_ratio <= HIGH_SCORE_MAXIMUM_MISSING_RATIO
        and wrong_count == 0
        and core_requirement_gap_count == 0
    )
    if not high_score_evidence_eligible:
        all_ceilings.append(float(max_score) * HIGH_SCORE_EVIDENCE_CEILING_RATIO)
    if (
        score_evidence is not None
        and not score_evidence["high_score_eligibility"]["eligible"]
    ):
        all_ceilings.append(
            float(score_evidence["high_score_eligibility"]["ceiling_when_ineligible"])
        )
    total = min([raw_score, *all_ceilings]) if all_ceilings else raw_score
    total = round(total, 2)
    fatal = bool(requirement_evaluation.get("fatal_or_core_error"))
    no_satisfied_nonfatal_ceiling_applied = bool(not fatal and satisfied_ratio == 0.0)
    if no_satisfied_nonfatal_ceiling_applied:
        # A collection of partial lexical matches must not become a mid-band
        # answer merely because an exact question contract has fewer anchors.
        # Fatal/core-error scores retain their separately reviewed ceilings.
        all_ceilings.append(float(max_score) * NO_SATISFIED_NONFATAL_CEILING_RATIO)
        total = min([raw_score, *all_ceilings])
        total = round(total, 2)
    if fatal:
        verdict = "NEEDS_CORRECTION"
    elif total >= max_score * 0.8:
        verdict = "HIGH_SCORE"
    elif total >= max_score * 0.7:
        verdict = "PRACTICAL_TARGET"
    elif total >= max_score * 0.6:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    return {
        **base,
        "decision": "SCORED",
        "total_score": total,
        "raw_score": round(raw_score, 2),
        "score_before_floors": round(score_before_floors, 2),
        "attempt_floor_applied": attempt_floor_applied,
        "evidenced_attempt_floor_applied": evidenced_attempt_floor_applied,
        "technically_adequate_floor_applied": technically_adequate_floor_applied,
        "substantive_fatal_floor_applied": substantive_fatal_floor_applied,
        "applied_ceiling": min(all_ceilings) if all_ceilings else None,
        "score_breakdown": breakdown,
        "score_evidence": score_evidence,
        "raw_requirement_count": len(requirements),
        "scoring_group_count": len(scoring_groups),
        "scoring_groups": scoring_groups,
        "satisfied_requirement_ratio": round(satisfied_ratio, 6),
        "minimum_satisfied_ratio_for_pass": minimum_satisfied_ratio_for_pass,
        "maximum_automatic_score": round(
            float(max_score) * MAXIMUM_AUTOMATIC_SCORE_RATIO, 2
        ),
        "high_score_ineligible_ceiling": round(
            float(score_evidence["high_score_eligibility"]["ceiling_when_ineligible"]), 2
        ) if score_evidence is not None else None,
        "pass_evidence_eligible": pass_evidence_eligible,
        "high_score_evidence_eligible": high_score_evidence_eligible,
        "missing_requirement_ratio": round(missing_ratio, 6),
        "wrong_requirement_count": wrong_count,
        "core_requirement_gap_count": core_requirement_gap_count,
        "pass_required_gap_count": pass_required_gap_count,
        "no_satisfied_nonfatal_ceiling_applied": no_satisfied_nonfatal_ceiling_applied,
        "verdict": verdict,
        "external_llm_required_for_verdict": False,
        "official_pass_met": bool(
            not fatal and pass_evidence_eligible and total >= max_score * 0.6
        ),
        "high_score_met": bool(not fatal and total >= max_score * 0.8),
    }
