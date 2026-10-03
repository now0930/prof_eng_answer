"""Optional local semantic resolver with zero grading authority."""

from __future__ import annotations

import json
from typing import Any, Callable

from canonical_grading_evidence import (
    CanonicalEvidenceError,
    build_canonical_grading_evidence,
)
from canonical_claim_extractor import extract_canonical_claim_evidence


VERSION = "local_semantic_resolver_v1"
MARKER = "LOCAL_SEMANTIC_RESOLVER_V1"


def build_semantic_evidence_prompt(
    unresolved_spans: list[dict[str, Any]],
) -> str:
    return "\n".join((
        "[CANONICAL_EVIDENCE_ONLY_V1]",
        "Extract only explicit canonical subject-predicate-object claims.",
        "For every claim include conditions and assertion_context.",
        "assertion_context must be asserted, quoted, rejected, or corrected.",
        "Do not output score, status, verdict, severity, fatal, cap, or grade.",
        "Use absolute source_span offsets and copy source_text exactly.",
        "Allowed top-level JSON: {\"claims\": [...]}",
        "Unresolved spans:",
        json.dumps(unresolved_spans, ensure_ascii=False, sort_keys=True),
        "[/CANONICAL_EVIDENCE_ONLY_V1]",
    ))


def resolve_with_optional_local_semantics(
    *,
    question_text: str,
    answer_text: str,
    semantic_call: Callable[[str], Any] | None = None,
    resolver_id: str = "local_k2_semantic_resolver",
    resolver_version: str = "pilot",
    topic_ids: list[str] | None = None,
) -> dict[str, Any]:
    extraction = extract_canonical_claim_evidence(
        answer_text,
        question_text=question_text,
        topic_ids=topic_ids,
    )
    deterministic = extraction["canonical_evidence"]
    unresolved = extraction["unresolved_spans"]
    result = {
        "version": VERSION,
        "marker": MARKER,
        "llm_verdict_authority": 0,
        "provider_calls": 0,
        "status": "deterministic_only" if not unresolved else "unresolved",
        "evidence_documents": [deterministic],
        "unresolved_spans": unresolved,
        "diagnostics": [],
    }
    if not unresolved or semantic_call is None:
        return result

    try:
        payload = semantic_call(build_semantic_evidence_prompt(unresolved))
        result["provider_calls"] = 1
        if not isinstance(payload, dict) or set(payload) != {"claims"}:
            raise CanonicalEvidenceError(
                "semantic resolver output must contain only claims"
            )
        if any(
            not isinstance(claim, dict)
            or "conditions" not in claim
            or "assertion_context" not in claim
            for claim in payload["claims"]
        ):
            raise CanonicalEvidenceError(
                "semantic claims must declare conditions and assertion_context"
            )
        semantic = build_canonical_grading_evidence(
            question_text=question_text,
            answer_text=answer_text,
            source={
                "mode": "semantic_resolver",
                "resolver_id": resolver_id,
                "resolver_version": resolver_version,
            },
            claims=payload["claims"],
        )
        allowed_spans = {
            (row["start"], row["end"])
            for row in unresolved
        }
        if any(
            (row["source_span"]["start"], row["source_span"]["end"])
            not in allowed_spans
            for row in semantic["claims"]
        ):
            raise CanonicalEvidenceError(
                "semantic resolver emitted evidence outside unresolved spans"
            )
        result["evidence_documents"].append(semantic)
        result["status"] = "semantic_evidence_added"
        result["unresolved_spans"] = []
    except Exception as error:
        result["status"] = "semantic_resolver_failed"
        result["diagnostics"].append({
            "code": "SEMANTIC_RESOLVER_FAILED",
            "message": str(error)[:500],
            "score_effect": "none",
        })
    return result
