"""Provider-free evidence for the non-fact technical-professional score axes."""

from __future__ import annotations

import re
from typing import Any

from answer_volume import estimate_ascii_answer_volume


VERSION = "deterministic_score_evidence_v1"
MARKER = "DETERMINISTIC_SCORE_EVIDENCE_V1"
_HEADING = re.compile(r"^\s*(?:#{1,4}\s*|\d+[.)]\s*|[ⅠⅡⅢⅣⅤⅥ]+[.)]?\s*)")
_BULLET = re.compile(r"^\s*[-*•]\s*")
_JUDGMENT_RELATIONS = (
    (("현장", "운전", "공정", "설비", "plant", "field"), ("선정", "결정", "기준", "조건", "판단", "select")),
    (("검증", "시험", "측정", "test"), ("기준", "결과", "기록", "확인", "판정", "수용")),
    (("비용", "위험", "장점", "단점", "trade"), ("영향", "한계", "비교", "절충", "대안")),
    (("변경", "점검", "정비", "유지", "lifecycle"), ("검증", "시험", "확인", "관리", "기록")),
    (("=", "≈", "계산", "수식", "정량"), ("조건", "한계", "경계", "범위", "기준")),
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
    # Production scoring passes requirement-owned spans. D/E therefore cannot
    # be earned by an unrelated but professionally worded paragraph.
    evidence_text = (
        text if (not evidence_binding_requested or bound_evidence) else ""
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
    judgment_groups = []
    for context_cues, decision_cues in _JUDGMENT_RELATIONS:
        matched = [
            clause for clause in clauses
            if any(cue.casefold() in clause for cue in context_cues)
            and any(cue.casefold() in clause for cue in decision_cues)
        ]
        judgment_groups.append(matched)
    judgment_score = min(6.0, 1.25 * sum(bool(row) for row in judgment_groups))
    linkage_matches = [
        clause for clause in clauses
        if any(cue in clause for cue in _LINK_CUES)
        and any(token in clause for pair in _JUDGMENT_RELATIONS for side in pair for token in side)
    ]
    linkage_score = min(2.0, 1.0 * len(linkage_matches))
    volume = estimate_ascii_answer_volume(text)
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
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
