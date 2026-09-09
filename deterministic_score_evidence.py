"""Provider-free evidence for the non-fact technical-professional score axes."""

from __future__ import annotations

import re
from typing import Any

from answer_volume import estimate_ascii_answer_volume


VERSION = "deterministic_score_evidence_v1"
MARKER = "DETERMINISTIC_SCORE_EVIDENCE_V1"
_HEADING = re.compile(r"^\s*(?:#{1,4}\s*|\d+[.)]\s*|[ⅠⅡⅢⅣⅤⅥ]+[.)]?\s*)")
_BULLET = re.compile(r"^\s*[-*•]\s*")
_JUDGMENT_GROUPS = (
    ("현장", "운전", "공정", "설비", "plant", "field"),
    ("선정", "결정", "기준", "조건", "판단", "select"),
    ("검증", "시험", "측정", "기록", "확인", "test"),
    ("비용", "영향", "위험", "한계", "장점", "단점", "trade"),
    ("절차", "유지", "점검", "변경", "관리", "정비", "lifecycle"),
    ("=", "≈", "계산", "수식", "boundary", "경계"),
)
_LINK_CUES = ("따라", "때문", "따라서", "결론", "연결", "영향", "반면", "그러므로", "인해", "하면")
_FULL_DEPTH_ASCII_UNITS = 1800
_HIGH_SCORE_INELIGIBLE_CEILING = 18.5


def evaluate_score_evidence(answer_text: str) -> dict[str, Any]:
    """Measure visible structure, engineering judgment and logical linkage."""
    text = str(answer_text or "")
    folded = text.casefold()
    lines = text.splitlines()
    heading_count = sum(bool(_HEADING.match(line)) for line in lines)
    bullet_count = sum(bool(_BULLET.match(line)) for line in lines)
    structure_score = 1.5 if text.strip() else 0.0
    if len([row for row in re.split(r"[.!?。]\s*|\n+", text) if row.strip()]) >= 2:
        structure_score += 0.5
    structure_score += 1.5 if heading_count >= 2 else 0.75 if heading_count == 1 else 0.0
    structure_score += 1.0 if bullet_count >= 3 else 0.5 if bullet_count else 0.0
    structure_score = min(3.0, structure_score)

    judgment_groups = [
        [cue for cue in group if cue.casefold() in folded]
        for group in _JUDGMENT_GROUPS
    ]
    judgment_score = min(6.0, 1.05 * sum(bool(row) for row in judgment_groups))
    linkage_matches = [cue for cue in _LINK_CUES if cue in text]
    linkage_score = min(2.0, 0.5 * len(linkage_matches))
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
        },
        "linkage": {
            "score": linkage_score, "max_score": 2.0,
            "matched_cues": linkage_matches,
        },
        "volume": volume,
        "high_score_eligibility": {
            "eligible": volume["ascii_equivalent_count"] >= _FULL_DEPTH_ASCII_UNITS,
            "minimum_ascii_equivalent_count": _FULL_DEPTH_ASCII_UNITS,
            "ceiling_when_ineligible": _HIGH_SCORE_INELIGIBLE_CEILING,
        },
    }
