"""Sentence-first, score-neutral view of existing Topic Pack Fact Anchors.

Fact Anchor's canonical human meaning is its plain-language `statement`, not
the machine-contract subject/predicate/object triple. Never rewrite/split
source statements automatically: removing a qualifier can change the fact.
This view does not approve claims, promote registry data or change scoring.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring

ROOT = Path(__file__).resolve().parents[2]
VERSION = "fact_anchor_sentence_view.v1"
_TOPIC = re.compile(r"^[a-z][a-z0-9_]*$")
# Terminating sentence punctuation in Korean natural prose. Decimal points,
# dotted acronyms and trailing symbols inside formulae are not boundaries.
_SENTENCE_END = re.compile(r"(?<=[가-힣])(?:[.!?。])(?=\s|$)")


def _sentence_count(value: str) -> int:
    pieces = [part.strip() for part in _SENTENCE_END.split(value) if part.strip()]
    return max(1, len(pieces))


def project_fact_anchor_sentences(
    topic_ids: Iterable[str] | None = None,
    *,
    root: Path | None = None,
    score_eligible_only: bool = False,
) -> dict[str, Any]:
    """Expose original factual sentences; do not guess their atomic split.

    The projection is read-only and retains source-derived IDs. Multi-sentence
    text is flagged for manual simplification; it remains unchanged here.
    """
    base = (root or ROOT).resolve()
    if topic_ids is None:
        paths = sorted((base / "rubrics/topic_packs").glob("*/fact_anchor.json"))
    else:
        topics = sorted(set(topic_ids))
        if any(not isinstance(t, str) or not _TOP.fullmatch(t) for t in topics):
            raise ValueError("invalid Topic identity")
        paths = [base / "rubrics/topic_packs" / t / "fact_anchor.json" for t in topics]
    rows = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        if not path.is_file():
            if topic_ids is not None:
                raise ValueError("Topic fact_anchor source missing")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        topic = path.parent.name
        if data.get("topic_id") != topic or not isinstance(data.get("anchors"), list):
            raise ValueError("invalid Topic fact_anchor ownership")
        for anchor in data["anchors"]:
            if not isinstance(anchor, dict):
                raise ValueError("invalid Fact Anchor record")
            anchor_id = anchor.get("anchor_id") or anchor.get("id")
            statement = anchor.get("statement")
            if (
                not isinstance(anchor_id, str) or not anchor_id
                or not isinstance(statement, str) or not statement.strip()
            ):
                raise ValueError("Fact Anchor sentence missing")
            key = (topic, anchor_id)
            if key in seen:
                raise ValueError("duplicate Fact Anchor ownership")
            seen.add(key)
            excluded = excluded_from_scoring(topic_id=topic, anchor_id=anchor_id)
            if score_eligible_only and excluded:
                continue
            normalized = statement.strip()
            sentence_count = _sentence_count(normalized)
            rows.append({
                "owner_topic_id": topic,
                "fact_id": anchor_id,
                "statement": normalized,
                "statement_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                "sentence_count": sentence_count,
                "style_status": (
                    "SINGLE_STATEMENT" if sentence_count == 1
                    else "MANUAL_SIMPLIFICATION_REQUIRED"
                ),
                "general_scoring_excluded": excluded,
                "source_path": str(path.relative_to(base)),
                "score_effect": "none",
            })
    return {
        "schema_version": VERSION,
        "authority": "source_statement_view_only",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "anchor_count": len(rows),
        "multi_sentence_count": sum(
            row["style_status"] == "MANUAL_SIMPLIFICATION_REQUIRED" for row in rows
        ),
        "rows": rows,
    }
