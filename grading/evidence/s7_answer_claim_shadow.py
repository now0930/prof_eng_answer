"""Answer-derived S7 surface Claim pilot. Isolated from operational grading."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .approved_fact_registry import load_approved_fact_registry

VERSION = "s7_answer_derived_shadow.v1"
_QUOTE = re.compile(r'["“”‘’「」『』]')
_SUBJECTS = {
    "deadband": ("제어밸브 데드밴드", "데드밴드"),
    "baseline": ("승인된 기준선", "형상 기준선"),
    "area": ("실효 불평형 면적",),
    "vmodel": ("개발 단계", "설계 단계"),
    "nyquist": ("Nyquist 경로", "Nyquist contour"),
}


def _span(sentence: str, offset: int, text: str) -> dict[str, Any] | None:
    """Return the original-cased source slice and its absolute character span."""
    match = re.search(re.escape(text), sentence, flags=re.IGNORECASE)
    if match is None:
        return None
    return {
        "text": match.group(),
        "span": {"start": offset + match.start(), "end": offset + match.end()},
    }


def _split_sentences(text: str):
    return [(m.group(), m.start()) for m in re.finditer(r"[^.!?。\n]+(?:[.!?。]|$)", text)]


def extract_answer_claims(answer_text: str) -> dict[str, Any]:
    """Parse a small set of explicit Korean surface relations from answer text only."""
    if not isinstance(answer_text, str):
        raise ValueError("answer_text must be a string")
    claims = []
    for sentence, offset in _split_sentences(answer_text):
        text = sentence.strip()
        left_trim = len(sentence) - len(sentence.lstrip())
        base = offset + left_trim
        norm = text.casefold()
        # A quoted assertion is reported only as an abstention; it is not the
        # author's asserted relation. This pilot does not resolve attribution.
        quoted = bool(_QUOTE.search(text))
        rows = []
        patterns = [
            ("deadband", re.compile(r"(?P<s>제어밸브\s*데드밴드|데드밴드)는\s*(?:입력\s*방향(?:을)?\s*반전(?:할\s*때|시))\s*(?P<p>출력\s*변화가\s*없는|출력\s*변화가\s*발생하지\s*않는)\s*(?P<o>입력\s*구간|범위)")),
            ("baseline", re.compile(r"(?P<s>승인된\s*기준선|형상\s*기준선)은\s*(?P<o>변경\s*관리(?:의)?\s*기준)(?P<p>으로\s*사용(?:된다|한다)?)")),
            ("area", re.compile(r"(?P<s>실효\s*불평형\s*면적)은\s*(?P<o>압력\s*작용면과\s*밸브\s*구조)(?P<p>에\s*따라\s*결정(?:된다|한다)?)")),
            ("vmodel", re.compile(r"(?P<s>개발\s*단계|설계\s*단계)는\s*(?P<o>검증\s*단계|시험\s*단계)(?P<p>에\s*대응(?:한다|된다)?)")),
            ("nyquist", re.compile(r"(?P<s>Nyquist\s*(?:경로|contour))(?:은|는)\s*(?P<o>우반평면)을\s*(?P<p>둘러싸고)" , re.I)),
            ("nyquist_mapping", re.compile(r"(?P<s>L\s*\(\s*s\s*\))의\s*(?P<o>복소평면)\s*(?P<p>사상)" , re.I)),
        ]
        if "데드밴드" in text and re.search(r"입력\s*방향.*무관", text):
            m = re.search(r"(?P<s>데드밴드)는\s*(?P<o>입력\s*방향)(?P<p>.*?무관)", text)
            if m:
                claims.append({"surface_kind": "deadband", "subject": {"text": m.group("s"), "span": {"start": base+m.start("s"), "end": base+m.end("s")}},
                    "relation": {"text": m.group("p"), "span": {"start": base+m.start("p"), "end": base+m.end("p")}},
                    "object": {"text": m.group("o"), "span": {"start": base+m.start("o"), "end": base+m.end("o")}},
                    "polarity": "NEGATIVE_OR_AMBIGUOUS", "conditions": [], "condition_status": "NOT_EXTRACTED",
                    "evidence_span": {"start": base+m.start(), "end": base+m.end()}, "extraction_status": "ABSTAIN"})
        for kind, pattern in patterns:
            for match in pattern.finditer(text):
                rows.append((kind, match))
        for kind, match in rows:
            # Negation scoped to the relation phrase; deadband's "변화가 없는"
            # is the positive definition, not negation of the whole relation.
            relation_text = match.group("p")
            negative = bool(re.search(r"(?:무관|관계가\s*없|not\b|never\b|틀리|잘못)", text, re.I))
            ambiguous_negation = negative or (kind != "deadband" and "않" in relation_text)
            if quoted or ambiguous_negation:
                status, polarity = "ABSTAIN", "NEGATIVE_OR_AMBIGUOUS" if negative else "UNKNOWN"
            else:
                status, polarity = "SURFACE_CLAIM_REVIEW_ONLY", "POSITIVE"
            fields = {name: {"text": match.group(name), "span": {"start": base + match.start(name), "end": base + match.end(name)}}
                      for name in ("s", "p", "o")}
            claims.append({
                "surface_kind": kind,
                "subject": fields["s"], "relation": fields["p"], "object": fields["o"],
                "polarity": polarity, "conditions": [], "condition_status": "NOT_EXTRACTED",
                "evidence_span": {"start": base + match.start(), "end": base + match.end()},
                "extraction_status": status,
            })
        # Recognizable topic terms without the complete supported relation are
        # explicitly unresolved; no Registry facts are consulted to fill gaps.
        if not rows and not any(c["evidence_span"]["start"] >= base and c["evidence_span"]["end"] <= base + len(text) for c in claims):
            for kind, subjects in _SUBJECTS.items():
                hit = next((s for s in subjects if s.casefold() in norm), None)
                if hit:
                    located = _span(text, base, hit)
                    claim = {
                        "surface_kind": kind,
                        "subject": located,
                        "relation": None,
                        "object": None,
                        "polarity": "UNKNOWN",
                        "conditions": [],
                        "condition_status": "NOT_EXTRACTED",
                        "evidence_span": {"start": base, "end": base + len(text)},
                        "extraction_status": "ABSTAIN",
                    }
                    if located is None:
                        claim["extraction_reason"] = "SUBJECT_SPAN_UNRESOLVED"
                    claims.append(claim)
    return {"schema_version": VERSION, "mode": "RESEARCH_ONLY", "claims": claims,
            "score_admission": "DISABLED", "score_effect": "none"}


def _scope_facts(
    registry_facts: Any, *, scope_topic_id: str | None,
    repository_root: str | Path | None,
) -> tuple[list[dict[str, Any]], str | None]:
    """Validate caller-selected facts against the approved on-disk Registry."""
    if not isinstance(registry_facts, list):
        return [], "INVALID_SCOPE_LIST"
    if not registry_facts:
        return [], None
    if not isinstance(scope_topic_id, str) or not scope_topic_id.strip():
        return [], "TOPIC_SCOPE_REQUIRED"
    ids = [row.get("fact_id") if isinstance(row, dict) else None for row in registry_facts]
    valid_ids = [fact_id for fact_id in ids if isinstance(fact_id, str)]
    if len(valid_ids) != len(set(valid_ids)):
        return [], "DUPLICATE_FACT_ID_IN_SCOPE"
    try:
        root = Path(repository_root).resolve() if repository_root is not None else Path(__file__).resolve().parents[2]
        registry = load_approved_fact_registry(root)
    except Exception:
        return [], "APPROVED_REGISTRY_INVALID_OR_UNAVAILABLE"
    canonical = {row["fact_id"]: row for row in registry["facts"]}
    validated: list[dict[str, Any]] = []
    for row in registry_facts:
        if not isinstance(row, dict):
            return [], "INVALID_FACT_SCHEMA"
        fact_id = row.get("fact_id")
        authoritative = canonical.get(fact_id) if isinstance(fact_id, str) else None
        if authoritative is None or row != authoritative:
            return [], "FACT_NOT_IDENTICAL_TO_APPROVED_REGISTRY"
        if authoritative.get("topic_id") != scope_topic_id:
            return [], "FACT_TOPIC_SCOPE_MISMATCH"
        validated.append(authoritative)
    return validated, None


def _comparison_record(
    claim: dict[str, Any], claim_index: int, registry_fact: dict[str, Any] | None,
    *, rejection_reason: str | None = None, requested_fact_id: Any = None,
) -> dict[str, Any]:
    claim_ready = (
        isinstance(claim, dict)
        and claim.get("extraction_status") == "SURFACE_CLAIM_REVIEW_ONLY"
        and all(isinstance(claim.get(key), dict) for key in ("subject", "relation", "object"))
    )
    if rejection_reason is not None:
        relation_status, condition_status = "ABSTAIN", "ABSTAIN"
        reason = rejection_reason
        validation_status = "REJECTED"
    elif registry_fact is None:
        relation_status, condition_status = "ABSTAIN", "ABSTAIN"
        reason = "NO_COMPARISON_TARGET"
        validation_status = "NOT_PROVIDED"
    elif not claim_ready:
        relation_status, condition_status = "ABSTAIN", "ABSTAIN"
        reason = "ANSWER_CLAIM_NOT_ESTABLISHED_BY_STAGE_A"
        validation_status = "APPROVED_VERIFIED"
    else:
        relation_status = "NOT_ESTABLISHED"
        condition_status = (
            "NO_REGISTRY_REQUIRED_CONDITIONS"
            if not registry_fact["relation"]["conditions"]
            else "NOT_ASSESSED_ANSWER_CONDITIONS_NOT_EXTRACTED"
        )
        reason = "NO_REVIEWED_SEMANTIC_CROSSWALK"
        validation_status = "APPROVED_VERIFIED"
    claim_record = claim if isinstance(claim, dict) else {}
    return {
        "claim_index": claim_index,
        "claim_extraction_status": claim_record.get("extraction_status", "ABSTAIN"),
        "claim_evidence_span": claim_record.get("evidence_span"),
        # This ID identifies only the caller-supplied comparison target.
        "comparison_fact_id": registry_fact.get("fact_id") if registry_fact else None,
        "requested_comparison_fact_id": (
            registry_fact.get("fact_id") if registry_fact else
            requested_fact_id if isinstance(requested_fact_id, str) else None
        ),
        "comparison_topic_id": registry_fact.get("topic_id") if registry_fact else None,
        "registry_relation_ids": (
            {key: registry_fact["relation"][key] for key in ("subject", "predicate", "object")}
            if registry_fact else None
        ),
        "registry_required_condition_ids": (
            list(registry_fact["relation"]["conditions"]) if registry_fact else None
        ),
        "registry_validation_status": validation_status,
        "relation_comparison_status": relation_status,
        "condition_comparison_status": condition_status,
        "crosswalk_status": "MISSING_REVIEWED_CROSSWALK" if registry_fact else "NOT_AVAILABLE",
        "reason": reason,
        "source_match_proven": False,
        "score_admission": "DISABLED",
        "score_effect": "none",
    }


def compare_claim_to_registry(
    claim: dict[str, Any], registry_fact: dict[str, Any], *,
    scope_topic_id: str | None = None, repository_root: str | Path | None = None,
) -> dict[str, Any]:
    """Audit one explicitly scoped target without asserting semantic identity."""
    validated, error = _scope_facts(
        [registry_fact], scope_topic_id=scope_topic_id, repository_root=repository_root,
    )
    target = validated[0] if validated else None
    record = _comparison_record(claim, 0, target, rejection_reason=error)
    return {"status": record["relation_comparison_status"], **record}


def evaluate_answer_shadow(
    answer_text: str, registry_facts: list[dict[str, Any]], *,
    scope_topic_id: str | None = None, repository_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run independent answer extraction, then audit caller-selected Registry targets."""
    extracted = extract_answer_claims(answer_text)
    targets, scope_error = _scope_facts(
        registry_facts, scope_topic_id=scope_topic_id, repository_root=repository_root,
    )
    claims = extracted["claims"]
    comparisons: list[dict[str, Any]] = []
    if scope_error:
        comparisons = [
            _comparison_record(
                claim, index, None, rejection_reason=scope_error,
                requested_fact_id=(row.get("fact_id") if isinstance(row, dict) else None),
            )
            for index, claim in enumerate(claims)
            for row in (registry_facts if isinstance(registry_facts, list) else [None])
        ]
    elif not targets:
        comparisons = [
            _comparison_record(claim, index, None)
            for index, claim in enumerate(claims)
        ]
    else:
        # Pair every extracted Claim with every independently supplied target.
        # Neither Claim surface text nor surface_kind selects a Fact ID.
        comparisons = [
            _comparison_record(claim, index, fact)
            for index, claim in enumerate(claims)
            for fact in targets
        ]
    status = (
        "SCOPE_REJECTED" if scope_error else
        "NO_CLAIMS" if not claims else
        "NO_COMPARISON_TARGET" if not targets else
        "COMPARISONS_GENERATED"
    )
    return {
        **extracted,
        "comparison_status": status,
        "comparison_scope": {
            "topic_id": scope_topic_id,
            "provided_fact_count": len(registry_facts) if isinstance(registry_facts, list) else 0,
            "validated_fact_count": len(targets),
            "rejection_reason": scope_error,
        },
        "comparisons": comparisons,
        "accuracy": None,
        "accuracy_status": "NOT_ESTABLISHED",
        "score_admission": "DISABLED",
        "score_effect": "none",
    }
