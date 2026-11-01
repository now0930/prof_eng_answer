"""Score-reference exclusions for noncore/scoped/duplicate/unverified-correction Fact Anchors.

An exclusion is not a declaration that the underlying engineering claim is false.
Original Topic Pack and approved registry data remain intact for traceability.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

_EXCLUSIONS_FILE = Path(__file__).with_name("fact_anchor_scoring_exclusions_20261101.json")
_REVISION_HOLDS_FILE = Path(__file__).with_name("fact_anchor_independent_revision_holds_20261101.json")
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



@lru_cache(maxsize=1)
def independent_revision_holds() -> tuple[frozenset[str], frozenset[tuple[str, str]]]:
    """Hold independently reviewed claims requiring evidence-backed correction.

    Keep the 276 original screening exclusions separate and unchanged. The
    pending revision layer never means the physical statement is false.
    """
    payload = json.loads(_REVISION_HOLDS_FILE.read_text(encoding="utf-8"))
    if payload.get("version") != "independent-primary-source-revision-holds-v1":
        raise ValueError("unsupported Fact Anchor independent revision hold version")
    rows = payload.get("holds")
    if not isinstance(rows, list):
        raise ValueError("invalid independent Fact Anchor revision holds")
    fact_ids: set[str] = set()
    anchor_keys: set[tuple[str, str]] = set()
    screened_ids, screened_keys = scoring_exclusions()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"fact_id", "topic_id", "anchor_id", "reason"}:
            raise ValueError("malformed independent Fact Anchor revision hold")
        if row["reason"] != "primary_source_revision_pending":
            raise ValueError("unknown independent Fact Anchor revision hold reason")
        fid, topic, anchor = (row["fact_id"], row["topic_id"], row["anchor_id"])
        if any(not isinstance(x, str) or not x.strip() for x in (fid, topic, anchor)):
            raise ValueError("empty independent Fact Anchor revision hold identity")
        key = (topic, anchor)
        if fid in fact_ids or key in anchor_keys or fid in screened_ids or key in screened_keys:
            raise ValueError("duplicate or overlapping Fact Anchor revision hold")
        fact_ids.add(fid)
        anchor_keys.add(key)
    return frozenset(fact_ids), frozenset(anchor_keys)


def excluded_from_scoring(*, topic_id: str, anchor_id: str = "", fact_id: str = "") -> bool:
    fact_ids, anchor_keys = scoring_exclusions()
    revised_fact_ids, revised_anchor_keys = independent_revision_holds()
    return bool(
        (fact_id and (fact_id in fact_ids or fact_id in revised_fact_ids))
        or (
            anchor_id
            and (
                (topic_id, anchor_id) in anchor_keys
                or (topic_id, anchor_id) in revised_anchor_keys
            )
        )
    )
