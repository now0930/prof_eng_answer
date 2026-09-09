"""Provider-neutral, evidence-only intermediate representation.

This boundary records what was extracted from an answer.  It deliberately
cannot carry requirement states, fatal decisions, scores, caps, or verdicts.
Those decisions belong to deterministic evaluators downstream.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any


SCHEMA_VERSION = "1.0"
MARKER = "CANONICAL_GRADING_EVIDENCE_V1"
SOURCE_MODES = {
    "deterministic_parser",
    "semantic_resolver",
    "human_adapter",
    "legacy_adapter",
}
POLARITIES = {"positive", "negative"}
ASSERTION_CONTEXTS = {"asserted", "quoted", "rejected", "corrected"}

# Evidence producers must never smuggle grading authority through metadata.
FORBIDDEN_AUTHORITY_KEYS = {
    "score",
    "total_score",
    "final_score",
    "layer_scores",
    "grade",
    "verdict",
    "requirement_verdict",
    "requirement_status",
    "demand_state",
    "status",
    "fatal",
    "fatal_error_detected",
    "severity",
    "recommended_ceiling",
    "cap",
    "floor",
    "passing_score_allowed",
    "strong_verdict_allowed",
}

_CANONICAL_ID = re.compile(r"^[a-z][a-z0-9_]*$")


class CanonicalEvidenceError(ValueError):
    """Raised when evidence violates the authority boundary."""


def _fingerprint(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _reject_authority_fields(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).strip().casefold()
            if normalized in FORBIDDEN_AUTHORITY_KEYS:
                raise CanonicalEvidenceError(
                    f"grading authority field is forbidden at {path}.{key}"
                )
            _reject_authority_fields(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_authority_fields(nested, f"{path}[{index}]")


def _canonical_id(value: Any, field: str) -> str:
    result = str(value or "").strip().casefold()
    if not _CANONICAL_ID.fullmatch(result):
        raise CanonicalEvidenceError(f"{field} must be a canonical snake_case id")
    return result


def _span(value: Any, answer_text: str, source_text: str) -> dict[str, int]:
    if not isinstance(value, dict):
        raise CanonicalEvidenceError("source_span must be an object")
    start = value.get("start")
    end = value.get("end")
    if (
        isinstance(start, bool)
        or isinstance(end, bool)
        or not isinstance(start, int)
        or not isinstance(end, int)
        or start < 0
        or end <= start
        or end > len(answer_text)
    ):
        raise CanonicalEvidenceError("source_span is outside the answer")
    if answer_text[start:end] != source_text:
        raise CanonicalEvidenceError("source_text must exactly match source_span")
    return {"start": start, "end": end}


def _confidence(value: Any) -> float:
    if isinstance(value, bool):
        raise CanonicalEvidenceError("extraction_confidence must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise CanonicalEvidenceError(
            "extraction_confidence must be numeric"
        ) from error
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise CanonicalEvidenceError(
            "extraction_confidence must be between zero and one"
        )
    return round(result, 6)


def _normalize_source(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise CanonicalEvidenceError("source must be an object")
    allowed = {"mode", "resolver_id", "resolver_version"}
    unknown = set(value) - allowed
    if unknown:
        raise CanonicalEvidenceError(f"unsupported source fields: {sorted(unknown)}")
    mode = str(value.get("mode") or "").strip().casefold()
    if mode not in SOURCE_MODES:
        raise CanonicalEvidenceError(f"unsupported source mode: {mode!r}")
    return {
        "mode": mode,
        "resolver_id": _canonical_id(value.get("resolver_id"), "resolver_id"),
        "resolver_version": str(value.get("resolver_version") or "").strip(),
    }


def _normalize_claim(raw: Any, answer_text: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise CanonicalEvidenceError("claim must be an object")
    allowed = {
        "claim_id",
        "subject",
        "predicate",
        "object",
        "polarity",
        "conditions",
        "assertion_context",
        "source_text",
        "source_span",
        "requirement_refs",
        "qualifiers",
        "extraction_confidence",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise CanonicalEvidenceError(f"unsupported claim fields: {sorted(unknown)}")
    source_text = str(raw.get("source_text") or "")
    if not source_text:
        raise CanonicalEvidenceError("source_text is required")
    polarity = str(raw.get("polarity") or "positive").strip().casefold()
    if polarity not in POLARITIES:
        raise CanonicalEvidenceError(f"unsupported polarity: {polarity!r}")
    refs = raw.get("requirement_refs") or []
    if not isinstance(refs, list):
        raise CanonicalEvidenceError("requirement_refs must be an array")
    qualifiers = raw.get("qualifiers") or {}
    if not isinstance(qualifiers, dict):
        raise CanonicalEvidenceError("qualifiers must be an object")
    conditions = raw.get("conditions") or []
    if not isinstance(conditions, list):
        raise CanonicalEvidenceError("conditions must be an array")
    assertion_context = str(
        raw.get("assertion_context") or "asserted"
    ).strip().casefold()
    if assertion_context not in ASSERTION_CONTEXTS:
        raise CanonicalEvidenceError(
            f"unsupported assertion_context: {assertion_context!r}"
        )
    row = {
        "subject": _canonical_id(raw.get("subject"), "subject"),
        "predicate": _canonical_id(raw.get("predicate"), "predicate"),
        "object": _canonical_id(raw.get("object"), "object"),
        "polarity": polarity,
        "conditions": sorted({
            _canonical_id(item, "condition") for item in conditions
        }),
        "assertion_context": assertion_context,
        "source_text": source_text,
        "source_span": _span(raw.get("source_span"), answer_text, source_text),
        "requirement_refs": sorted({
            _canonical_id(item, "requirement_ref") for item in refs
        }),
        "qualifiers": {
            _canonical_id(key, "qualifier key"): str(value).strip()
            for key, value in sorted(qualifiers.items())
        },
        "extraction_confidence": _confidence(
            raw.get("extraction_confidence", 1.0)
        ),
    }
    row["claim_id"] = str(raw.get("claim_id") or "").strip() or (
        "claim_" + _fingerprint(row)[:16]
    )
    return row


def build_canonical_grading_evidence(
    *,
    question_text: str,
    answer_text: str,
    source: dict[str, Any],
    claims: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build deterministic evidence without making any grading decision."""

    _reject_authority_fields(source)
    _reject_authority_fields(claims)
    if not isinstance(claims, list):
        raise CanonicalEvidenceError("claims must be an array")
    normalized_claims = [_normalize_claim(row, answer_text) for row in claims]
    normalized_claims.sort(
        key=lambda row: (
            row["source_span"]["start"],
            row["source_span"]["end"],
            row["claim_id"],
        )
    )
    claim_ids = [row["claim_id"] for row in normalized_claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise CanonicalEvidenceError("claim_id must be unique")
    output = {
        "schema_version": SCHEMA_VERSION,
        "marker": MARKER,
        "authority": "evidence_only",
        "score_effect": "none",
        "input_fingerprint": {
            "question_sha256": hashlib.sha256(
                question_text.encode("utf-8")
            ).hexdigest(),
            "answer_sha256": hashlib.sha256(
                answer_text.encode("utf-8")
            ).hexdigest(),
        },
        "source": _normalize_source(source),
        "claims": normalized_claims,
        "summary": {"claim_count": len(normalized_claims)},
    }
    output["evidence_sha256"] = _fingerprint(output)
    return output


def validate_canonical_grading_evidence(
    value: Any,
    *,
    answer_text: str | None = None,
) -> dict[str, Any]:
    """Strictly validate an already canonical evidence document."""

    _reject_authority_fields(value)
    if not isinstance(value, dict):
        raise CanonicalEvidenceError("evidence document must be an object")
    required = {
        "schema_version", "marker", "authority", "score_effect",
        "input_fingerprint", "source", "claims", "summary", "evidence_sha256",
    }
    if set(value) != required:
        raise CanonicalEvidenceError("canonical evidence top-level fields mismatch")
    if value.get("schema_version") != SCHEMA_VERSION or value.get("marker") != MARKER:
        raise CanonicalEvidenceError("canonical evidence version mismatch")
    if value.get("authority") != "evidence_only" or value.get("score_effect") != "none":
        raise CanonicalEvidenceError("canonical evidence cannot own grading decisions")
    if answer_text is not None:
        expected = build_canonical_grading_evidence(
            question_text="",
            answer_text=answer_text,
            source=value.get("source"),
            claims=value.get("claims"),
        )
        if value["input_fingerprint"].get("answer_sha256") != expected[
            "input_fingerprint"
        ]["answer_sha256"]:
            raise CanonicalEvidenceError("answer fingerprint mismatch")
        for row in value.get("claims") or []:
            _span(row.get("source_span"), answer_text, row.get("source_text"))
    payload = dict(value)
    digest = payload.pop("evidence_sha256")
    if digest != _fingerprint(payload):
        raise CanonicalEvidenceError("evidence fingerprint mismatch")
    return value
