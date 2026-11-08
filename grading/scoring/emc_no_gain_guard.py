"""Conservative EMC wrong-claim score monotonicity guard.

A detected, topic-owned EMC error must not increase the score relative to
exactly the same answer without that error sentence.  This does NOT award
credit, alter requirements, resolve unknown evidence, or unhold any anchor.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


EMC_TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"


def strip_detected_emc_error_units(
    answer_text: str,
    violations: Iterable[Mapping[str, Any]],
    *,
    active_topic_ids: Iterable[str],
) -> str | None:
    """Strip only exact, source-owned units marked as violations.

    Offsets and literal source text must match, otherwise do not construct
    a counterfactual.  Newlines between units are preserved.  A single
    sentence can carry legitimate evidence too; removing the entire detected
    unit is deliberately conservative and must not promote any fact.
    """
    if EMC_TOPIC not in set(active_topic_ids):
        return None
    spans: set[tuple[int, int]] = set()
    for row in violations:
        if not str(row.get("code") or "").startswith("EMC_"):
            continue
        loc = row.get("source_span")
        if not isinstance(loc, Mapping):
            return None
        start, end = loc.get("start"), loc.get("end")
        source = row.get("source_text")
        if (
            isinstance(start, bool) or isinstance(end, bool)
            or not isinstance(start, int) or not isinstance(end, int)
            or not 0 <= start < end <= len(answer_text)
            or source != answer_text[start:end]
        ):
            return None
        spans.add((start, end))
    if not spans:
        return None
    masked = list(answer_text)
    for start, end in spans:
        for index in range(start, end):
            if masked[index] not in "\r\n":
                masked[index] = " "
    candidate = "".join(masked).rstrip()
    return candidate if candidate.strip() and candidate != answer_text else None


def cap_score_to_counterfactual(
    score: Mapping[str, Any],
    *,
    clean_score_total: float,
    fatal_or_core_error: bool,
) -> tuple[dict[str, Any], bool]:
    """Add a bounded ceiling without changing grading groups or policies."""
    current = float(score["total_score"])
    if not 0 <= clean_score_total < current:
        return dict(score), False
    result = dict(score)
    result["total_score"] = round(clean_score_total, 2)
    current_ceiling = result.get("applied_ceiling")
    result["applied_ceiling"] = min(
        float(current_ceiling) if current_ceiling is not None else float(result["max_score"]),
        clean_score_total,
    )
    total = result["total_score"]
    maximum = float(result["max_score"])
    result["official_pass_met"] = bool(
        result.get("official_pass_met") and total >= maximum * 0.6
    )
    result["high_score_met"] = bool(
        result.get("high_score_met") and total >= maximum * 0.8
    )
    if fatal_or_core_error:
        result["verdict"] = "NEEDS_CORRECTION"
    elif total >= maximum * 0.8:
        result["verdict"] = "HIGH_SCORE"
    elif total >= maximum * 0.7:
        result["verdict"] = "PRACTICAL_TARGET"
    elif total >= maximum * 0.6:
        result["verdict"] = "PASS"
    else:
        result["verdict"] = "FAIL"
    return result, True
