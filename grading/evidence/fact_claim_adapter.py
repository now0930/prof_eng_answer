"""Project existing Fact Anchors and approved machine relations without rewriting source."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.evidence.claim_alignment_contract import canonical_relation
from grading.scoring.deterministic_requirement_evaluator import load_machine_contracts

ROOT = Path(__file__).resolve().parents[2]


def project_fact_claims(topic_ids: Iterable[str],
                        required_by_topic: dict[str, set[str]] | None = None
                        ) -> list[dict[str, Any]]:
    """Only eligible source anchors appear. Missing machine relations stay unstructured."""
    topics = sorted(set(topic_ids))
    contracts = {r["owner_topic_id"]: r for r in load_machine_contracts(topics)}
    result: list[dict[str, Any]] = []
    for topic in topics:
        path = ROOT / "rubrics" / "topic_packs" / topic / "fact_anchor.json"
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        known = {f["fact_id"]: canonical_relation(f)
                 for f in contracts.get(topic, {}).get("facts", [])}
        allowed = required_by_topic.get(topic) if required_by_topic is not None else None
        for anchor in payload.get("anchors", []):
            if not isinstance(anchor, dict):
                continue
            aid = str(anchor.get("anchor_id") or anchor.get("id") or "").strip()
            if not aid or excluded_from_scoring(topic_id=topic, anchor_id=aid):
                continue
            if allowed is not None and aid not in allowed:
                continue
            result.append({
                "owner_topic_id": topic,
                "fact_id": aid,
                "parent_anchor_id": aid,
                "relation": known.get(aid),
                "projection_status": (
                    "STRUCTURED_APPROVED_RELATION" if aid in known
                    else "UNSTRUCTURED_REVIEW_REQUIRED"
                ),
                "importance": str(anchor.get("importance") or "normal"),
            })
    return result
