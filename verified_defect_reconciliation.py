from __future__ import annotations

import copy
import re
from typing import Any


# VERIFIED_DEFECT_RECONCILIATION_V1

_MAJOR_SEVERITIES = {
    "major",
    "fatal",
}
_ALLOWED_STATUSES = {
    "present",
    "partial",
    "incorrect",
    "missing",
}
_SCORE_FIELDS = (
    "score",
    "total_score",
    "final_score",
    "raw_total_score",
    "adjusted_total_score",
    "layer_scores",
)

_FINDING_POLICY = {
    "friction_viscous_model_overgeneralized": {
        "keywords": (
            "마찰",
            "불평형력",
            "friction",
            "definition",
            "concept",
            "개념",
        ),
        "category_tokens": (
            "definition",
            "concept",
            "principle",
            "개념",
            "원리",
        ),
    },
    "force_balance_requirement_sign_contradiction": {
        "keywords": (
            "spring",
            "스프링",
            "fail safe",
            "설계",
            "힘 평형",
            "calculation",
            "interpretation",
        ),
        "category_tokens": (
            "calculation",
            "interpretation",
            "design",
            "설계",
            "해석",
        ),
    },
}

_DEMAND_CATEGORY_TOKENS = {
    "DEFINE_EXPLAIN": (
        "definition",
        "concept",
        "정의",
        "개념",
        "explain",
        "설명",
    ),
    "PRINCIPLE_INTERPRET": (
        "principle",
        "interpretation",
        "calculation",
        "원리",
        "해석",
        "계산",
    ),
    "DESIGN": (
        "design",
        "calculation",
        "설계",
        "선정",
    ),
    "SELECT": (
        "select",
        "selection",
        "선정",
        "선택",
    ),
    "IMPLEMENT": (
        "implement",
        "application",
        "구현",
        "적용",
    ),
}


def _score_snapshot(
    grade: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: copy.deepcopy(grade.get(key))
        for key in _SCORE_FIELDS
        if key in grade
    }


def _normalise_text(value: Any) -> str:
    return re.sub(
        r"\s+",
        " ",
        str(value or ""),
    ).strip().lower()


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


def _general_contract(
    grade: dict[str, Any],
) -> dict[str, Any]:
    direct = grade.get(
        "general_evidence_contract"
    )

    if isinstance(direct, dict):
        return direct

    parsed = grade.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "general_evidence_contract"
        )

        if isinstance(nested, dict):
            return nested

    return {}


def _coverage(
    grade: dict[str, Any],
) -> dict[str, Any] | None:
    direct = grade.get(
        "question_type_coverage"
    )

    if isinstance(direct, dict):
        return copy.deepcopy(direct)

    parsed = grade.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "question_type_coverage"
        )

        if isinstance(nested, dict):
            return copy.deepcopy(nested)

    return None


def _requirement_map(
    grade: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    requirements = _question_contract(
        grade
    ).get("requirements")

    if not isinstance(requirements, list):
        return {}

    return {
        str(row.get("requirement_id") or ""): row
        for row in requirements
        if isinstance(row, dict)
        and str(row.get("requirement_id") or "")
    }


def _verified_defects(
    grade: dict[str, Any],
) -> list[dict[str, Any]]:
    defects = _general_contract(
        grade
    ).get("defects")

    if not isinstance(defects, list):
        return []

    return [
        copy.deepcopy(row)
        for row in defects
        if isinstance(row, dict)
        and str(
            row.get("defect_type") or ""
        ).lower()
        == "correctness_error"
        and str(
            row.get("severity") or ""
        ).lower()
        in _MAJOR_SEVERITIES
        and str(
            row.get("owner_layer") or ""
        ).upper()
        == "C"
    ]


def _row_text(
    row: dict[str, Any],
) -> str:
    values = []

    for key in (
        "requirement",
        "requirement_text",
        "criterion",
        "category",
        "demand_kind",
        "demand_label",
    ):
        value = row.get(key)

        if value not in (None, ""):
            values.append(str(value))

    return _normalise_text(" ".join(values))


def _match_score(
    row: dict[str, Any],
    defect: dict[str, Any],
    contract_requirement: dict[str, Any] | None,
) -> int:
    row_requirement_id = str(
        row.get("requirement_id") or ""
    )
    defect_requirement_id = str(
        defect.get("requirement_id") or ""
    )

    if (
        row_requirement_id
        and defect_requirement_id
        and row_requirement_id
        == defect_requirement_id
    ):
        return 1000

    text = _row_text(row)
    finding_id = str(
        defect.get("source_finding_id")
        or ""
    )
    policy = _FINDING_POLICY.get(
        finding_id,
        {},
    )
    score = 0

    for keyword in policy.get(
        "keywords",
        (),
    ):
        if _normalise_text(keyword) in text:
            score += 20

    for token in policy.get(
        "category_tokens",
        (),
    ):
        if _normalise_text(token) in text:
            score += 10

    if isinstance(contract_requirement, dict):
        requirement_text = _normalise_text(
            contract_requirement.get(
                "requirement_text"
            )
        )
        demand_kind = str(
            contract_requirement.get(
                "demand_kind"
            )
            or ""
        )

        for token in re.findall(
            r"[a-z0-9가-힣]+",
            requirement_text,
        ):
            if len(token) >= 2 and token in text:
                score += 2

        for token in _DEMAND_CATEGORY_TOKENS.get(
            demand_kind,
            (),
        ):
            if _normalise_text(token) in text:
                score += 8

    return score


def _select_requirement_index(
    rows: list[Any],
    defect: dict[str, Any],
    requirement_map: dict[
        str,
        dict[str, Any],
    ],
) -> int | None:
    requirement_id = str(
        defect.get("requirement_id") or ""
    )
    contract_requirement = (
        requirement_map.get(requirement_id)
    )
    candidates = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue

        score = _match_score(
            row,
            defect,
            contract_requirement,
        )
        candidates.append(
            (
                score,
                -index,
                index,
            )
        )

    if not candidates:
        return None

    candidates.sort(reverse=True)
    best_score, _negative_index, best_index = (
        candidates[0]
    )

    if best_score <= 0:
        return None

    return best_index


def _append_evidence(
    original: Any,
    message: str,
) -> str:
    base = str(original or "").strip()
    addition = str(message or "").strip()

    if not addition:
        return base

    marker = f"[검증 오류] {addition}"

    if marker in base:
        return base

    return (
        f"{base} / {marker}"
        if base
        else marker
    )


def _status_counts(
    rows: list[Any],
) -> dict[str, int]:
    counts = {
        "present": 0,
        "partial": 0,
        "incorrect": 0,
        "missing": 0,
        "unknown": 0,
        "total": 0,
    }

    for row in rows:
        if not isinstance(row, dict):
            continue

        status = str(
            row.get("status") or ""
        ).lower()
        counts["total"] += 1

        if status in _ALLOWED_STATUSES:
            counts[status] += 1
        else:
            counts["unknown"] += 1

    return counts


def _downgrade_overall(
    current: Any,
    incorrect_count: int,
) -> str:
    value = str(
        current or "adequate"
    ).lower()
    ranks = {
        "strong": 3,
        "adequate": 2,
        "weak": 1,
        "poor": 0,
    }
    current_rank = ranks.get(value, 2)
    maximum_rank = (
        1
        if incorrect_count >= 2
        else 2
    )
    target_rank = min(
        current_rank,
        maximum_rank,
    )

    for name, rank in ranks.items():
        if rank == target_rank:
            return name

    return "adequate"


def reconcile_verified_defects_with_coverage(
    grade: Any,
) -> Any:
    if not isinstance(grade, dict):
        return grade

    output = copy.deepcopy(grade)
    before = _score_snapshot(output)
    defects = _verified_defects(output)
    coverage = _coverage(output)

    if not defects or not isinstance(
        coverage,
        dict,
    ):
        return output

    explicit = coverage.get(
        "explicit_requirement_coverage"
    )

    if not isinstance(explicit, dict):
        return output

    rows = explicit.get("requirements")

    if not isinstance(rows, list):
        return output

    rows = copy.deepcopy(rows)
    requirement_map = _requirement_map(
        output
    )
    applied_defect_ids = []
    unresolved_defect_ids = []

    for defect in defects:
        defect_id = str(
            defect.get("defect_id") or ""
        )
        index = _select_requirement_index(
            rows,
            defect,
            requirement_map,
        )

        if index is None:
            unresolved_defect_ids.append(
                defect_id
            )
            continue

        row = rows[index]
        previous_status = str(
            row.get("status") or ""
        ).lower()

        if (
            "status_before_verified_defect"
            not in row
        ):
            row[
                "status_before_verified_defect"
            ] = previous_status or "unknown"

        row["status"] = "incorrect"
        defect_ids = row.get(
            "verified_defect_ids"
        )

        if not isinstance(defect_ids, list):
            defect_ids = []

        if defect_id and defect_id not in defect_ids:
            defect_ids.append(defect_id)

        row[
            "verified_defect_ids"
        ] = defect_ids
        source_ids = row.get(
            "verified_source_finding_ids"
        )

        if not isinstance(source_ids, list):
            source_ids = []

        source_finding_id = str(
            defect.get(
                "source_finding_id"
            )
            or ""
        )

        if (
            source_finding_id
            and source_finding_id
            not in source_ids
        ):
            source_ids.append(
                source_finding_id
            )

        row[
            "verified_source_finding_ids"
        ] = source_ids
        requirement_id = str(
            defect.get("requirement_id")
            or ""
        )

        if requirement_id:
            row.setdefault(
                "requirement_id",
                requirement_id,
            )

        row["evidence"] = _append_evidence(
            row.get("evidence"),
            defect.get("explanation"),
        )
        rows[index] = row
        applied_defect_ids.append(
            defect_id
        )

    if not applied_defect_ids:
        return output

    explicit["requirements"] = rows
    counts = _status_counts(rows)
    explicit[
        "verified_status_counts"
    ] = counts
    explicit[
        "verified_incorrect_count"
    ] = counts["incorrect"]
    explicit[
        "verified_defect_reconciliation"
    ] = {
        "marker": (
            "VERIFIED_DEFECT_RECONCILIATION_V1"
        ),
        "score_effect": "none",
        "primary_score_owner": "C",
        "b_completeness_double_deduction": False,
        "applied_defect_ids": applied_defect_ids,
        "unresolved_defect_ids": (
            unresolved_defect_ids
        ),
    }
    coverage[
        "explicit_requirement_coverage"
    ] = explicit
    coverage["coverage_counts"] = counts
    coverage["overall_coverage"] = (
        _downgrade_overall(
            coverage.get("overall_coverage"),
            counts["incorrect"],
        )
    )
    hint = str(
        coverage.get("scoring_hint")
        or ""
    ).strip()
    verified_hint = (
        "검증된 기술 오류는 요구사항 status를 "
        "incorrect로 표시하되 주 점수 소유권은 C에 "
        "두고 B 완전성에는 중복 차감하지 않는다."
    )

    if verified_hint not in hint:
        coverage["scoring_hint"] = (
            f"{hint} {verified_hint}".strip()
        )

    parsed = output.get("parsed")

    if not isinstance(parsed, dict):
        parsed = {}
        output["parsed"] = parsed

    parsed[
        "question_type_coverage"
    ] = copy.deepcopy(coverage)

    if isinstance(
        output.get("question_type_coverage"),
        dict,
    ):
        output[
            "question_type_coverage"
        ] = copy.deepcopy(coverage)

    output[
        "verified_defect_reconciliation"
    ] = {
        "schema_version": "1.0",
        "marker": (
            "VERIFIED_DEFECT_RECONCILIATION_V1"
        ),
        "score_effect": "none",
        "direct_score_application": False,
        "primary_score_owner": "C",
        "b_completeness_double_deduction": False,
        "status_counts": counts,
        "overall_coverage": coverage[
            "overall_coverage"
        ],
        "applied_defect_ids": (
            applied_defect_ids
        ),
        "unresolved_defect_ids": (
            unresolved_defect_ids
        ),
    }

    if before != _score_snapshot(output):
        raise RuntimeError(
            "Verified-defect reconciliation "
            "changed numeric score state"
        )

    return output


# === VERIFIED_DEFECT_EMPTY_REQUIREMENT_FALLBACK_V2 ===
_VERIFIED_DEFECT_PREVIOUS_SELECT_REQUIREMENT_V2 = (
    _select_requirement_index
)


def _verified_requirement_text_v2(
    row: Any,
) -> str:
    if not isinstance(row, dict):
        return ""

    return " ".join(
        str(row.get(key) or "")
        for key in (
            "requirement",
            "category",
            "criterion",
            "evidence",
        )
    ).lower()


def _verified_finding_keyword_groups_v2(
    finding_id: str,
) -> tuple[tuple[str, ...], ...]:
    mappings = {
        (
            "friction_viscous_model_"
            "overgeneralized"
        ): (
            ("마찰",),
            ("friction",),
        ),
        (
            "force_balance_requirement_"
            "sign_contradiction"
        ): (
            ("fail", "safe"),
            ("스프링",),
            ("spring",),
            ("힘", "평형"),
        ),
    }
    return mappings.get(
        finding_id,
        (),
    )


def _verified_unique_keyword_index_v2(
    rows: Any,
    keyword_groups: tuple[
        tuple[str, ...],
        ...,
    ],
) -> int | None:
    if not isinstance(rows, list):
        return None

    scored = []

    for index, row in enumerate(rows):
        text = _verified_requirement_text_v2(
            row
        )

        if not text:
            continue

        score = 0

        for group in keyword_groups:
            if all(
                token.lower() in text
                for token in group
            ):
                score += len(group) * 10

        if score > 0:
            scored.append((score, index))

    if not scored:
        return None

    scored.sort(
        key=lambda item: (
            -item[0],
            item[1],
        )
    )
    top_score = scored[0][0]
    top_indexes = [
        index
        for score, index in scored
        if score == top_score
    ]

    if len(top_indexes) != 1:
        return None

    return top_indexes[0]


def _select_requirement_index(
    rows: list[dict[str, Any]],
    defect: dict[str, Any],
    requirement_map: dict[str, Any],
) -> int | None:
    if isinstance(defect, dict):
        requirement_id = str(
            defect.get("requirement_id")
            or ""
        ).strip()
        defect_type = str(
            defect.get("defect_type")
            or ""
        ).lower()
        owner_layer = str(
            defect.get("owner_layer")
            or ""
        ).upper()
        source = str(
            defect.get("source")
            or ""
        )
        finding_id = str(
            defect.get("source_finding_id")
            or ""
        )

        is_known_empty_control_valve_defect = (
            not requirement_id
            and defect_type
            == "correctness_error"
            and owner_layer == "C"
            and source
            == "control_valve_formula_check"
        )

        if is_known_empty_control_valve_defect:
            keyword_groups = (
                _verified_finding_keyword_groups_v2(
                    finding_id
                )
            )

            if keyword_groups:
                selected = (
                    _verified_unique_keyword_index_v2(
                        rows,
                        keyword_groups,
                    )
                )

                if selected is not None:
                    return selected

    return (
        _VERIFIED_DEFECT_PREVIOUS_SELECT_REQUIREMENT_V2(
            rows,
            defect,
            requirement_map,
        )
    )


# === VERIFIED_DEFECT_DISPLAY_SUMMARY_SYNC_V4 ===
_VERIFIED_DEFECT_PREVIOUS_RECONCILE_DISPLAY_V4 = (
    reconcile_verified_defects_with_coverage
)


def _verified_display_rows_v4(
    coverage: Any,
) -> list[dict[str, Any]]:
    if not isinstance(coverage, dict):
        return []

    explicit = coverage.get(
        "explicit_requirement_coverage"
    )

    if not isinstance(explicit, dict):
        return []

    rows = explicit.get("requirements")

    if not isinstance(rows, list):
        return []

    return [
        row
        for row in rows
        if isinstance(row, dict)
    ]


def _verified_display_summary_v4(
    coverage: dict[str, Any],
    previous_summary: Any,
) -> dict[str, Any]:
    rows = _verified_display_rows_v4(
        coverage
    )

    if not rows:
        return (
            copy.deepcopy(previous_summary)
            if isinstance(previous_summary, dict)
            else {}
        )

    normalised = []
    counts = {
        "present": 0,
        "partial": 0,
        "incorrect": 0,
        "missing": 0,
    }
    weights = {
        "present": 1.0,
        "partial": 0.5,
        "incorrect": 0.0,
        "missing": 0.0,
    }

    for row in rows:
        status = str(
            row.get("status") or ""
        ).strip().lower()

        if status not in counts:
            status = "missing"

        criterion = str(
            row.get("requirement")
            or row.get("criterion")
            or ""
        ).strip()

        evidence = str(
            row.get("evidence") or ""
        ).strip()

        counts[status] += 1
        normalised.append(
            {
                "criterion": criterion,
                "status": status,
                "evidence": evidence,
            }
        )

    total = len(normalised)
    weighted_score = sum(
        weights[row["status"]]
        for row in normalised
    )
    ratio = (
        weighted_score / total
        if total
        else 0.0
    )

    summary = (
        copy.deepcopy(previous_summary)
        if isinstance(previous_summary, dict)
        else {}
    )
    summary.update(
        {
            "question_type": coverage.get(
                "question_type"
            ),
            "name_ko": coverage.get(
                "name_ko"
            ),
            "overall_coverage": coverage.get(
                "overall_coverage"
            ),
            "sub_criteria_total": total,
            "sub_criteria_present": (
                counts["present"]
            ),
            "sub_criteria_partial": (
                counts["partial"]
            ),
            "sub_criteria_incorrect": (
                counts["incorrect"]
            ),
            "sub_criteria_missing": (
                counts["missing"]
            ),
            "weighted_coverage_score": round(
                weighted_score,
                2,
            ),
            "weighted_coverage_ratio": round(
                ratio,
                4,
            ),
            "weighted_coverage_percent": round(
                ratio * 100.0,
                1,
            ),
            "present_criteria": [
                row["criterion"]
                for row in normalised
                if row["status"] == "present"
            ],
            "partial_criteria": [
                row["criterion"]
                for row in normalised
                if row["status"] == "partial"
            ],
            "incorrect_criteria": [
                row["criterion"]
                for row in normalised
                if row["status"] == "incorrect"
            ],
            "missing_criteria": [
                row["criterion"]
                for row in normalised
                if row["status"] == "missing"
            ],
            "criteria_status_rows": normalised,
            "verified_defect_display_sync": {
                "marker": (
                    "VERIFIED_DEFECT_DISPLAY_SUMMARY_SYNC_V4"
                ),
                "source": (
                    "explicit_requirement_coverage"
                ),
                "overall_coverage": coverage.get(
                    "overall_coverage"
                ),
                "status_counts": copy.deepcopy(
                    counts
                ),
                "score_effect": "none",
            },
        }
    )
    return summary


def reconcile_verified_defects_with_coverage(
    grade: Any,
) -> Any:
    output = (
        _VERIFIED_DEFECT_PREVIOUS_RECONCILE_DISPLAY_V4(
            grade
        )
    )

    if not isinstance(output, dict):
        return output

    reconciliation = output.get(
        "verified_defect_reconciliation"
    )

    if not isinstance(reconciliation, dict):
        return output

    if (
        reconciliation.get("marker")
        != "VERIFIED_DEFECT_RECONCILIATION_V1"
    ):
        return output

    before = _score_snapshot(output)

    from question_type_coverage_adapter import (
        attach_question_type_coverage_feedback,
    )

    output = attach_question_type_coverage_feedback(
        output
    )

    coverage = output.get(
        "question_type_coverage"
    )

    if isinstance(coverage, dict):
        output[
            "question_type_coverage_summary"
        ] = _verified_display_summary_v4(
            coverage,
            output.get(
                "question_type_coverage_summary"
            ),
        )

    if before != _score_snapshot(output):
        raise RuntimeError(
            "Verified-defect display summary sync "
            "changed numeric score state"
        )

    return output
