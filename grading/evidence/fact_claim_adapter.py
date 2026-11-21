"""Project score-eligible Fact Anchors to verified, source-owned relations.

Original Fact Anchor and Logic Check files are never modified. The independently
verified Fact registry has priority over a machine relation used for scoring.
An unverified source relation may appear in diagnostics but cannot be claimed
to be independently verified or used to promote new scoring evidence.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from grading.evidence.approved_fact_registry import (
    REGISTRY_PATH, load_approved_fact_registry,
)
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.evidence.claim_alignment_contract import canonical_relation
from grading.scoring.deterministic_requirement_evaluator import load_machine_contracts

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=4)
def _registry_index(root_str: str, modified_ns: int, size: int
                    ) -> dict[tuple[str, str], dict[str, Any]]:
    """Cache only validated source-owned Facts keyed by rooted file identity."""
    del modified_ns, size  # Included in cache key to invalidate on source revision.
    registry = load_approved_fact_registry(root_str)
    index: dict[tuple[str, str], dict[str, Any]] = {}
    ambiguous: set[tuple[str, str]] = set()
    for fact in registry["facts"]:
        if fact["review_status"] != "approved" or fact.get("verification_status") != "verified":
            continue
        legacy_id = str(fact.get("legacy_anchor_id") or fact["fact_id"])
        key = (fact["topic_id"], legacy_id)
        if key in ambiguous:
            continue
        if key in index:
            # Multiple independently verified Facts may legitimately descend
            # from one legacy Anchor. Do not choose a relation arbitrarily.
            ambiguous.add(key)
            index.pop(key)
            continue
        index[key] = {
            "source_fact_id": fact["fact_id"],
            "relation": canonical_relation({**fact["relation"], "polarity": "positive"}),
            "revision": fact["revision"],
        }
    return index


def _verified_source_index() -> dict[tuple[str, str], dict[str, Any]]:
    path = ROOT / REGISTRY_PATH
    if not path.is_file():
        return {}
    stat = path.stat()
    return _registry_index(str(ROOT.resolve()), stat.st_mtime_ns, stat.st_size)


def project_fact_claims(
    topic_ids: Iterable[str],
    required_by_topic: dict[str, set[str]] | None = None,
) -> list[dict[str, Any]]:
    """Project only selected and eligible Anchors, never expanding an unknown scope."""
    topics = sorted(set(str(t) for t in topic_ids if str(t)))
    contracts = {row["owner_topic_id"]: row for row in load_machine_contracts(topics)}
    verified = _verified_source_index()
    results: list[dict[str, Any]] = []
    for topic in topics:
        if required_by_topic is not None and topic not in required_by_topic:
            continue
        path = ROOT / "rubrics" / "topic_packs" / topic / "fact_anchor.json"
        if not path.is_file():
            continue
        anchors = json.loads(path.read_text(encoding="utf-8")).get("anchors", [])
        machine = {
            row["fact_id"]: canonical_relation(row)
            for row in contracts.get(topic, {}).get("facts", [])
        }
        selected = required_by_topic.get(topic) if required_by_topic is not None else None
        for anchor in anchors:
            if not isinstance(anchor, dict):
                continue
            aid = str(anchor.get("anchor_id") or anchor.get("id") or "").strip()
            if not aid or excluded_from_scoring(topic_id=topic, anchor_id=aid):
                continue
            if selected is not None and aid not in selected:
                continue
            source_fact = verified.get((topic, aid))
            machine_relation = machine.get(aid)
            relation = source_fact["relation"] if source_fact else machine_relation
            status = (
                "VERIFIED_REGISTRY_RELATION" if source_fact else
                "STRUCTURED_MACHINE_RELATION" if machine_relation else
                "UNSTRUCTURED_REVIEW_REQUIRED"
            )
            results.append({
                "owner_topic_id": topic,
                "fact_id": aid,
                "parent_anchor_id": aid,
                "relation": relation,
                "projection_status": status,
                "source_fact_id": source_fact["source_fact_id"] if source_fact else None,
                "relation_source": "verified_registry" if source_fact else (
                    "machine_contract" if machine_relation else "unstructured"
                ),
                "machine_relation_differs": bool(
                    source_fact and machine_relation and
                    source_fact["relation"] != machine_relation
                ),
                "importance": str(anchor.get("importance") or "normal"),
            })
    return results
