"""Provider-free evidence for the non-fact technical-professional score axes."""

from __future__ import annotations

import os
import re
from typing import Any

from grading.scoring.answer_volume import estimate_ascii_answer_volume


VERSION = "deterministic_score_evidence_v1"
MARKER = "DETERMINISTIC_SCORE_EVIDENCE_V1"
_HEADING = re.compile(r"^\s*(?:#{1,4}\s*|\d+[.)]\s*|[ⅠⅡⅢⅣⅤⅥ]+[.)]?\s*)")
_BULLET = re.compile(r"^\s*[-*•]\s*")
_LEGACY_JUDGMENT_RELATIONS = (
    (("현장", "운전", "공정", "설비", "plant", "field"), ("선정", "결정", "기준", "조건", "판단", "select")),
    (("검증", "시험", "측정", "test"), ("기준", "결과", "기록", "확인", "판정", "수용")),
    (("비용", "위험", "장점", "단점", "trade"), ("영향", "한계", "비교", "절충", "대안")),
    (("변경", "점검", "정비", "유지", "lifecycle"), ("검증", "시험", "확인", "관리", "기록")),
    (("=", "≈", "계산", "수식", "정량"), ("조건", "한계", "경계", "범위", "기준")),
)
_BOUND_DESIGN_CONSTRAINT_RELATIONS = (
    # Unit normalization and actuator/input saturation are distinct design
    # constraints. Credit only a requirement-owned span, even under the
    # historic full-answer evidence policy for older D/E cues.
    (("단위 정규화", "unit normalization", "per-unit normalization"), ("반복 조정", "재조정", "tuning")),
    (("포화 한계", "입력 포화", "actuator saturation", "input saturation"), ("반복 조정", "재조정", "tuning")),
)
_LINK_CUES = ("때문", "따라서", "반면", "그러므로", "인해", "하면", "연결")
_FULL_DEPTH_ASCII_UNITS = 1800
_HIGH_SCORE_INELIGIBLE_CEILING = 18.5


def evaluate_score_evidence(
    answer_text: str, *, technical_evidence_texts: list[str] | None = None
) -> dict[str, Any]:
    """Measure visible structure, engineering judgment and logical linkage."""
    text = str(answer_text or "")
    evidence_binding_requested = technical_evidence_texts is not None
    bound_evidence = list(dict.fromkeys(
        row.strip() for row in (technical_evidence_texts or []) if row.strip()
    ))
    # The legacy path scores the full answer whenever any positive span exists.
    # Strict binding remains a pilot until the reviewed calibration gate passes;
    # otherwise production authority would be switched to an unready policy.
    strict_binding = os.getenv("ESSAY_STRICT_EVIDENCE_BINDING") == "1"
    evidence_text = (
        "\n".join(bound_evidence) if strict_binding and evidence_binding_requested
        else text if (not evidence_binding_requested or bound_evidence) else ""
    )
    folded = evidence_text.casefold()
    lines = text.splitlines()
    heading_count = sum(bool(_HEADING.match(line)) for line in lines)
    bullet_count = sum(bool(_BULLET.match(line)) for line in lines)
    structure_score = 1.5 if text.strip() else 0.0
    if len([row for row in re.split(r"[.!?。]\s*|\n+", text) if row.strip()]) >= 2:
        structure_score += 0.5
    structure_score += 1.5 if heading_count >= 2 else 0.75 if heading_count == 1 else 0.0
    structure_score += 1.0 if bullet_count >= 3 else 0.5 if bullet_count else 0.0
    structure_score = min(3.0, structure_score)

    clauses = [row.strip().casefold() for row in re.split(r"[.!?。;\n]+", evidence_text) if row.strip()]
    bound_clauses = [
        row.strip().casefold()
        for row in re.split(r"[.!?。;\n]+", "\n".join(bound_evidence))
        if row.strip()
    ] if evidence_binding_requested else clauses
    judgment_groups = []
    for context_cues, decision_cues in _LEGACY_JUDGMENT_RELATIONS + _BOUND_DESIGN_CONSTRAINT_RELATIONS:
        candidate_clauses = (
            bound_clauses
            if (context_cues, decision_cues) in _BOUND_DESIGN_CONSTRAINT_RELATIONS
            else clauses
        )
        matched = [
            clause for clause in candidate_clauses
            if any(cue.casefold() in clause for cue in context_cues)
            and any(cue.casefold() in clause for cue in decision_cues)
        ]
        judgment_groups.append(matched)
    judgment_score = min(6.0, 1.25 * sum(bool(row) for row in judgment_groups))
    linkage_matches = [
        clause for clause in clauses
        if any(cue in clause for cue in _LINK_CUES)
        and any(token in clause for pair in _LEGACY_JUDGMENT_RELATIONS for side in pair for token in side)
    ]
    linkage_score = min(2.0, 1.0 * len(linkage_matches))
    volume = estimate_ascii_answer_volume(text)
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
        "evidence_binding_policy": "strict" if strict_binding else "legacy",
        "structure": {
            "score": structure_score, "max_score": 3.0,
            "heading_count": heading_count, "bullet_count": bullet_count,
        },
        "engineering_judgment": {
            "score": judgment_score, "max_score": 6.0,
            "matched_groups": judgment_groups,
            "evidence_bound": evidence_binding_requested,
            "technical_evidence_span_count": len(bound_evidence),
        },
        "linkage": {
            "score": linkage_score, "max_score": 2.0,
            "matched_cues": linkage_matches,
            "evidence_bound": evidence_binding_requested,
            "technical_evidence_span_count": len(bound_evidence),
        },
        "volume": volume,
        "high_score_eligibility": {
            "eligible": volume["ascii_equivalent_count"] >= _FULL_DEPTH_ASCII_UNITS,
            "minimum_ascii_equivalent_count": _FULL_DEPTH_ASCII_UNITS,
            "ceiling_when_ineligible": _HIGH_SCORE_INELIGIBLE_CEILING,
        },
    }
