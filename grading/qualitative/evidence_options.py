"""Bounded, literal answer excerpts for provider-side D/E evidence selection."""

from __future__ import annotations

import re
from typing import Any, Mapping


def build_evidence_options(answer: str, requirements: list[Mapping[str, Any]], *, limit: int = 80) -> list[dict[str, Any]]:
    if not isinstance(answer, str) or not isinstance(requirements, list):
        raise ValueError("invalid_evidence_inputs")
    supported = []
    wrong = []
    for row in requirements:
        span = row.get("source_span") or {}
        start, end = span.get("start"), span.get("end")
        if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(answer):
            continue
        if row.get("status") in {"SATISFIED", "PARTIAL"}:
            supported.append((start, end, row.get("owner_topic_id")))
        elif row.get("status") == "WRONG":
            wrong.append((start, end))
    options = []
    # Preserve exact offsets; strip only edges, never normalize the excerpt.
    for line_match in re.finditer(r"[^\n]+", answer):
        line = line_match.group()
        for match in re.finditer(r"[^.!?;]+(?:[.!?;]+|$)", line):
            raw = match.group()
            core = raw.strip()
            # A short bare heading can match a deterministic requirement span
            # yet cannot substantiate a qualitative D/E rationale by itself.
            if len(core) < 8 or (len(core) < 20 and not core.endswith((".", "!", "?", ";"))):
                continue
            start = line_match.start() + match.start() + len(raw) - len(raw.lstrip())
            end = start + len(core)
            if answer.count(core) != 1:
                continue
            owners = sorted({owner for left, right, owner in supported
                             if isinstance(owner, str) and start < right and left < end})
            if not owners or any(start < right and left < end for left, right in wrong):
                continue
            options.append({"evidence_id": f"ev_{len(options) + 1:03d}",
                            "quote": core, "start": start, "end": end,
                            "topic_ids": owners})
            if len(options) >= limit:
                return options
    return options


def resolve_evidence_id(row: Mapping[str, Any], options: Mapping[str, Mapping[str, Any]],
                        *, zero_score: bool = False) -> dict[str, Any]:
    result = dict(row)
    evidence_id = result.pop("evidence_id", None)
    if zero_score:
        if evidence_id is not None:
            raise ValueError("zero_score_evidence_id")
        return {**result, "quote": None, "start": None, "end": None}
    option = options.get(evidence_id)
    if option is None or result.get("topic_id") not in option["topic_ids"]:
        raise ValueError("invalid_evidence_id")
    return {**result, "quote": option["quote"], "start": option["start"], "end": option["end"]}
