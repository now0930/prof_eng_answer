"""Question-only deterministic Topic routing for verdict-authority migration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fact_anchor_evidence_adapter import _question_similarity
from model_answer_router import find_model_answer_reference
from question_type_router import detect_question_type
from rubric_registry import normalize_text


VERSION = "deterministic_topic_router_v1"
MARKER = "DETERMINISTIC_TOPIC_ROUTER_V1"
ROOT = Path(__file__).resolve().parent


def _pack_candidates(question_text: str) -> list[dict[str, Any]]:
    normalized_question = normalize_text(question_text)
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "rubrics/topic_packs").glob("*/model_answer.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        patterns = []
        pattern_rows: list[dict[str, Any]] = []
        for value in payload.get("expected_question_patterns", []):
            pattern = str(
                value.get("pattern") or value.get("question") or ""
                if isinstance(value, dict) else value
            )
            patterns.append(pattern)
            if isinstance(value, dict):
                pattern_rows.append({
                    "pattern": pattern,
                    "routing_exclusive": bool(value.get("routing_exclusive")),
                    "routing_exclusive_block_terms": [
                        str(term) for term in value.get("routing_exclusive_block_terms", [])
                        if str(term).strip()
                    ],
                })
        patterns.extend(str(value) for value in payload.get("question_examples", []))
        pattern_score = max(
            [_question_similarity(question_text, value) for value in patterns] or [0.0]
        )
        title = str(payload.get("title_ko") or payload.get("title") or "")
        title_score = 2.0 * _question_similarity(question_text, title)
        aliases = list(payload.get("routing_aliases") or payload.get("topic_aliases") or [])
        aliases.extend(payload.get("deterministic_routing_aliases") or [])
        alias_hits = sorted({
            str(value) for value in aliases
            if normalize_text(str(value))
            and normalize_text(str(value)) in normalized_question
        })
        rows.append({
            "topic_id": path.parent.name,
            "score": round(max(pattern_score, title_score), 6),
            "alias_hits": alias_hits,
            "exclusive_pattern_score": round(max(
                [
                    _question_similarity(question_text, row["pattern"])
                    for row in pattern_rows
                    if row["routing_exclusive"]
                    and not any(
                        normalize_text(term) in normalized_question
                        for term in row["routing_exclusive_block_terms"]
                    )
                ] or [0.0]
            ), 6),
        })
    return sorted(rows, key=lambda row: (-row["score"], row["topic_id"]))


def route_question_topics(question_text: str) -> dict[str, Any]:
    """Route from the immutable question only; answer text is never consulted."""
    legacy = find_model_answer_reference(
        question_text, "", question_type_eval=detect_question_type(question_text),
    )
    candidates = _pack_candidates(question_text)
    exclusive = [
        row for row in candidates if row["exclusive_pattern_score"] >= 0.2
    ]
    if exclusive:
        selected = max(
            exclusive,
            key=lambda row: (row["exclusive_pattern_score"], row["score"], row["topic_id"]),
        )
        return {
            "version": VERSION,
            "marker": MARKER,
            "engine": "deterministic",
            "provider_calls": 0,
            "answer_text_used": False,
            "status": "ROUTED",
            "source": "exclusive_question_contract",
            "primary_topic_id": selected["topic_id"],
            "topic_ids": [selected["topic_id"]],
            "candidates": candidates[:3],
        }
    primary = str((legacy.get("primary_reference") or {}).get("topic_id") or "")
    source = "question_model_answer_router"
    fallback_primary = ""
    if not primary and candidates and candidates[0]["score"] >= 0.1:
        primary = candidates[0]["topic_id"]
        fallback_primary = primary
        source = "question_pack_similarity_fallback"
    if source == "question_pack_similarity_fallback":
        specific_alias_candidates = [
            row for row in candidates
            if max((len(normalize_text(alias)) for alias in row["alias_hits"]), default=0) >= 4
        ]
        if specific_alias_candidates:
            selected = max(
                specific_alias_candidates,
                key=lambda row: (
                    max(len(normalize_text(alias)) for alias in row["alias_hits"]),
                    row["score"],
                    row["topic_id"],
                ),
            )
            primary = selected["topic_id"]
            source = "specific_question_alias"
    topic_ids = [primary] if primary else []
    if fallback_primary and fallback_primary not in topic_ids:
        topic_ids.append(fallback_primary)
    for row in candidates:
        if row["alias_hits"] and row["topic_id"] not in topic_ids:
            topic_ids.append(row["topic_id"])
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
        "answer_text_used": False,
        "status": "ROUTED" if topic_ids else "ABSTAIN",
        "source": source if topic_ids else "no_safe_question_match",
        "primary_topic_id": primary or None,
        "topic_ids": topic_ids,
        "candidates": candidates[:3],
    }
