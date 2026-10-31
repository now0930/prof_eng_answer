"""Score-reference exclusions for noncore/scoped/duplicate/unverified-correction Fact Anchors.

An exclusion is not a declaration that the underlying engineering claim is false.
Original Topic Pack and approved registry data remain intact for traceability.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

_EXCLUSIONS_FILE = Path(__file__).with_name("fact_anchor_scoring_exclusions_20261101.json")
_ALLOWED_REASONS = frozenset({
    "noncore_detail",
    "scoped_standard_or_jurisdiction",
    "duplicate_scoring_requirement",
    "overgeneralization_or_correction_required",
})


@lru_cache(maxsize=1)
def scoring_exclusions() -> tuple[frozenset[str], frozenset[tuple[str, str]]]:
    """Return excluded Fact IDs and (topic, Anchor) pairs; reject invalid policy data."""
    payload = json.loads(_EXCLUSIONS_FILE.read_text(encoding="utf-8"))
    if payload.get("version") != "fact-anchor-scoring-exclusions-v1":
        raise ValueError("unsupported Fact Anchor scoring exclusions version")
    rows = payload.get("exclusions")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Fact Anchor scoring exclusions cannot be empty")
    fact_ids: set[str] = set()
    anchor_keys: set[tuple[str, str]] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"fact_id", "topic_id", "anchor_id", "reason"}:
            raise ValueError("malformed Fact Anchor scoring exclusion")
        fid, topic, anchor = (row["fact_id"], row["topic_id"], row["anchor_id"])
        if any(not isinstance(x, str) or not x.strip() for x in (fid, topic, anchor)):
            raise ValueError("empty Fact Anchor scoring exclusion identity")
        if row["reason"] not in _ALLOWED_REASONS:
            raise ValueError("unknown Fact Anchor exclusion reason")
        if fid in fact_ids or (topic, anchor) in anchor_keys:
            raise ValueError("duplicate Fact Anchor scoring exclusion identity")
        fact_ids.add(fid)
        anchor_keys.add((topic, anchor))
    return frozenset(fact_ids), frozenset(anchor_keys)


def excluded_from_scoring(*, topic_id: str, anchor_id: str = "", fact_id: str = "") -> bool:
    fact_ids, anchor_keys = scoring_exclusions()
    return bool((fact_id and fact_id in fact_ids) or (
        anchor_id and (topic_id, anchor_id) in anchor_keys
    ))
