"""Source-only, non-scoring audit of extracted Claim fidelity.

This module checks whether an extracted proposition is actually expressed by
its cited source span. It does not compare the proposition with a Fact Anchor
and does not decide technical truth or scoring.
"""

from __future__ import annotations

import re
from typing import Any

from grading.evidence.canonical_claim_extractor import _load_aliases, _find_alias


_ARITHMETIC = {
    "addition": re.compile(r"(?:의\s*합(?:이다|으로|으로?\s*계산)?|더한|더해|더하여|더하면|더하는|plus|sum(?:\s+of)?|added\s+to)", re.I),
    "multiplication": re.compile(r"(?:곱(?:이다|한다|으로|을|은|이)?|곱하|곱한|times|multipl(?:y|ied)|product\s+of)", re.I),
    "division": re.compile(r"(?:나누(?:다|면|어|어야|는|ㄴ)|분의|divid(?:e|ed)\s+by|over)", re.I),
}
_SUBJECT_TERMS = {
    "volumetric_flow": ("체적유량", "체적 유량", "volumetric flow"),
    "mass_flow": ("질량유량", "질량 유량", "mass flow"),
    "required_rrf": ("요구 RRF", "필요 RRF", "RRF_required", "required RRF", "RRF"),
    "emc_protective_earth": ("보호접지", "protective earth", "PE"),
    "mcdc": ("MC/DC", "MCDC", "modified condition decision coverage"),
    "verification": ("verification", "검증"),
}
_OBJECT_GROUPS = {
    "area_average_velocity_product": (("단면적", "area"), ("평균유속", "단면 평균유속", "average velocity")),
    "density_volume_flow_product": (("밀도", "density"), ("체적유량", "체적 유량", "volumetric flow")),
    "residual_tolerable_frequency_ratio": (("잔여빈도", "잔여 빈도", "잔여 사건빈도", "residual frequency"), ("허용빈도", "허용 빈도", "허용 사건빈도", "tolerable frequency")),
    "emc_signal_reference": (("신호접지", "신호 기준접지", "신호기준접지", "계측 기준전위", "signal/reference ground"),),
    "total_sil_assurance": (("전체 SIL", "전체 안전무결성", "total SIL", "SIL"),),
    "specification_conformance": (("명세 적합성", "명세 적합", "설계 기준", "specification", "design basis"),),
}
_POSITIVE_RELATION = re.compile(r"(?:이다|이며|이고|으로\s*산정|로\s*산정|확인한다|검증한다|곱(?:한|하|이다|으로)|비율|different|distinct|does not guarantee|doesn't guarantee|not guarantee|one of (?:the )?(?:several|multiple))", re.I)
_NEGATIVE_RELATION = re.compile(r"(?:아니(?:다|며|고)|않(?:다|는다|으며)|못(?:한다|하며)|틀리|잘못|같(?:다|은|으며)|동일(?:하다|한)|same|identical|does not differ|not different)", re.I)
_QUOTE_MARKS = ('"', "'", "“", "”", "‘", "’", "『", "』", "「", "」")
_REJECTION = re.compile(r"(?:틀리|잘못|오류|아니라|아닌|기각|wrong|false|incorrect|reject)", re.I)
_CORRECTION = re.compile(r"(?:실제로는|정정하면|올바른 관계는|정정|틀리(?:고|며|지만)|correct(?:ly)?|instead|rather)", re.I)


def relation_operation(text: str) -> str | None:
    """Return an explicitly stated arithmetic operation, if unambiguous."""
    found = [name for name, pattern in _ARITHMETIC.items() if pattern.search(text)]
    return found[0] if len(found) == 1 else None


def _has_term(text: str, terms: tuple[str, ...]) -> bool:
    folded = text.casefold()
    return any(term.casefold() in folded for term in terms)


def _has_object(text: str, object_id: str) -> bool:
    groups = _OBJECT_GROUPS.get(object_id)
    if not groups:
        aliases = _load_aliases().get(object_id, [])
        return bool(_find_alias(text, aliases))
    return all(any(_has_term(text, (term,)) for term in group) for group in groups)


def _polarity_fidelity(text: str, claim: dict[str, Any]) -> bool | None:
    polarity = claim.get("polarity")
    predicate = claim.get("predicate")
    if polarity not in {"positive", "negative"}:
        return None
    if predicate == "does_not_guarantee":
        has_guarantee = bool(re.search(r"(?:보장|입증|guarantee|assur)", text, re.I))
        if not has_guarantee:
            # “one of several evidence” expresses non-sufficiency without a
            # literal guarantee verb; it still needs both subject and object.
            return bool(re.search(r"(?:여러|복수|하나의|among|one of|several)", text, re.I)) if polarity == "positive" else None
        negated = bool(re.search(r"(?:않|못|아니|not|never|doesn't|does not)", text, re.I))
        return negated if polarity == "positive" else not negated
    if predicate == "distinct_from":
        distinct = bool(re.search(r"(?:다르|별개|different|distinct)", text, re.I))
        same = bool(re.search(r"(?:같|동일|same|identical)", text, re.I))
        if distinct == same:
            return None
        return (distinct and polarity == "positive") or (same and polarity == "negative")
    if predicate not in {"equivalent_to", "derived_by_ratio", "checks"}:
        return None
    positive = bool(_POSITIVE_RELATION.search(text))
    negative = bool(_NEGATIVE_RELATION.search(text))
    if positive == negative:
        return None
    return (not negative) == (polarity == "positive")


def _condition_fidelity(text: str, claim: dict[str, Any]) -> bool | None:
    conditions = set(claim.get("conditions", []))
    density_relation = (
        claim.get("predicate") == "equivalent_to"
        and claim.get("object") == "density_volume_flow_product"
    )
    spatial_uniform = bool(re.search(
        r"(?:밀도.{0,12}(?:단면|단면적).{0,12}(?:일정|균일)|(?:단면|단면적).{0,12}밀도.{0,12}(?:일정|균일)|(?:uniform|constant).{0,12}density.{0,20}(?:cross[ -]?section|section))",
        text, re.I,
    ))
    if density_relation and spatial_uniform and "uniform_density" not in conditions:
        return False
    if not conditions:
        return True
    if conditions != {"uniform_density"}:
        aliases = _load_aliases()
        return all(bool(_find_alias(text, aliases.get(condition, []))) for condition in conditions) or None
    spatial = bool(re.search(r"(?:단면|단면적|cross[ -]?section|across the section)", text, re.I))
    uniform = bool(re.search(r"(?:밀도.{0,12}(?:일정|균일)|(?:일정|균일).{0,12}밀도|uniform.{0,12}density|constant.{0,12}density)", text, re.I))
    temporal = bool(re.search(r"(?:시간(?:에\s*따라|적으로)?|시간상|temporal|over time|with time)", text, re.I))
    return spatial and uniform and not temporal


def _relation_fidelity(text: str, claim: dict[str, Any]) -> bool | None:
    subject, predicate, object_id = claim.get("subject"), claim.get("predicate"), claim.get("object")
    subject_terms = _SUBJECT_TERMS.get(subject)
    if subject_terms is None:
        aliases = _load_aliases().get(subject, [])
        subject_ok = bool(_find_alias(text, aliases))
    else:
        subject_ok = _has_term(text, subject_terms)
    if not subject_ok:
        return None
    if predicate == "equivalent_to" and object_id in {"area_average_velocity_product", "density_volume_flow_product"}:
        operation = relation_operation(text)
        # The object has two semantically required operands. Both must occur,
        # and only multiplication can establish this product relation.
        groups = _OBJECT_GROUPS[object_id]
        operands_present = all(any(_has_term(text, (term,)) for term in group) for group in groups)
        return operands_present and operation == "multiplication"
    if predicate == "derived_by_ratio" and object_id == "residual_tolerable_frequency_ratio":
        residual = re.search(r"(?:잔여\s*(?:사건)?빈도|residual\s+frequency)", text, re.I)
        tolerable = re.search(r"(?:허용\s*(?:사건)?빈도|tolerable\s+frequency)", text, re.I)
        if not residual or not tolerable:
            return None
        # Korean “Y에 대한 X의 비율” and a division expression both require
        # residual frequency as numerator and tolerable frequency as divisor.
        if re.search(r"(?:허용\s*(?:사건)?빈도.{0,20}대한.{0,20}잔여\s*(?:사건)?빈도.{0,8}비율)", text):
            return tolerable.start() < residual.start()
        operation = relation_operation(text)
        if operation == "division":
            return residual.start() < tolerable.start()
        if "비율" in text and "대한" in text:
            return tolerable.start() < residual.start()
        return None
    if predicate == "distinct_from" and object_id == "emc_signal_reference":
        other = re.search(r"(?:신호\s*(?:기준)?\s*접지|계측\s*기준전위|signal/reference\s+ground)", text, re.I)
        if not other:
            return None
        relation = bool(re.search(r"(?:다르|별개|different|distinct)", text, re.I))
        same = bool(re.search(r"(?:같|동일|same|identical)", text, re.I))
        if relation == same:
            return None
        return (relation and claim.get("polarity") == "positive") or (same and claim.get("polarity") == "negative")
    if predicate == "does_not_guarantee" and object_id == "total_sil_assurance":
        object_ok = _has_object(text, object_id)
        return object_ok and _polarity_fidelity(text, claim) is not None
    if predicate == "checks" and object_id == "specification_conformance":
        return bool(re.search(r"(?:확인|대조|검증|check|verify|compare)", text, re.I))
    return None


def _context_fidelity(answer: str, start: int, end: int, text: str, claim: dict[str, Any]) -> bool | None:
    context = claim.get("assertion_context")
    left, right = answer[max(0, start - 100):start], answer[end:min(len(answer), end + 100)]
    quote_pairs = (("\"", "\""), ("'", "'"), ("“", "”"), ("‘", "’"), ("『", "』"), ("「", "」"))
    quoted = any(
        opening in answer[:start] and closing in answer[end:]
        for opening, closing in quote_pairs
    ) or any(mark in text for mark in _QUOTE_MARKS)
    rejection = bool(_REJECTION.search(text + " " + right) or _REJECTION.search(left[-60:]))
    correction = bool(_CORRECTION.search(text + " " + right) or _CORRECTION.search(left[-60:]))
    if context == "asserted":
        return not quoted and not rejection and not correction
    if context == "quoted":
        return quoted
    if context == "rejected":
        return quoted and rejection
    if context == "corrected":
        return correction or (quoted and rejection and bool(re.search(r"(?:실제로|정정|올바르|correct|instead)", text, re.I)))
    return None


def assess_claim_fidelity(
    *, answer_text: str, claim: dict[str, Any], topic_id: str,
    expected_claim: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Check F1–F6 from source only; ``expected_claim`` is ignored.

    A PASS means the span supports the extracted proposition and attribution,
    not that the proposition is technically true or matches a Fact Anchor.
    """
    del expected_claim  # Fact comparison is deliberately a separate layer.
    span = claim.get("source_span") or {}
    start, end = span.get("start"), span.get("end")
    if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(answer_text):
        return {"status": "FAIL", "reason": "INVALID_SOURCE_SPAN", "score_effect": "none"}
    source = answer_text[start:end]
    if source != claim.get("source_text"):
        return {"status": "FAIL", "reason": "SOURCE_TEXT_MISMATCH", "score_effect": "none"}
    if claim.get("qualifiers", {}).get("owner_topic_id", topic_id) != topic_id:
        return {"status": "FAIL", "reason": "OWNER_MISMATCH", "score_effect": "none"}
    if claim.get("qualifiers", {}).get("context_inferred_subject") not in {None, False, "False"}:
        return {"status": "NOT_ESTABLISHED", "reason": "INFERRED_SUBJECT", "score_effect": "none"}

    subject_terms = _SUBJECT_TERMS.get(claim.get("subject"), ())
    if not subject_terms:
        subject_terms = tuple(_load_aliases().get(claim.get("subject"), []))
    f2_subject = _has_term(source, subject_terms) if subject_terms else False
    f2_object = _has_object(source, claim.get("object", ""))
    f2 = f2_subject and f2_object
    f3 = _relation_fidelity(source, claim)
    f4 = _condition_fidelity(source, claim)
    f5 = _polarity_fidelity(source, claim)
    f6 = _context_fidelity(answer_text, start, end, source, claim)
    criteria = {"F1_span": "PASS", "F2_subject_object": "PASS" if f2 else "NOT_ESTABLISHED", "F3_relation_order": "PASS" if f3 is True else "FAIL" if f3 is False else "NOT_ESTABLISHED", "F4_conditions": "PASS" if f4 is True else "FAIL" if f4 is False else "NOT_ESTABLISHED", "F5_polarity": "PASS" if f5 is True else "FAIL" if f5 is False else "NOT_ESTABLISHED", "F6_assertion_context": "PASS" if f6 is True else "FAIL" if f6 is False else "NOT_ESTABLISHED"}
    if "FAIL" in criteria.values():
        status, reason = "FAIL", "SOURCE_CONTRADICTS_CLAIM_STRUCTURE"
    elif all(value == "PASS" for value in criteria.values()):
        status, reason = "PASS", "SOURCE_SUPPORTS_CLAIM_STRUCTURE"
    else:
        status, reason = "NOT_ESTABLISHED", "SOURCE_DOES_NOT_ESTABLISH_ALL_F1_F6"
    return {"status": status, "reason": reason, "criteria": criteria, "observed_operation": relation_operation(source), "score_effect": "none"}


def assess_deterministic_claim_fidelity(
    *, answer_text: str, claim: dict[str, Any], topic_id: str,
    expected_claim: dict[str, Any] | None,
) -> dict[str, Any]:
    """Preserve the pre-existing A-arm guard behavior unchanged."""
    span = claim.get("source_span") or {}
    start, end = span.get("start"), span.get("end")
    if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(answer_text):
        return {"status": "FAIL", "reason": "INVALID_SOURCE_SPAN", "score_effect": "none"}
    source = answer_text[start:end]
    if source != claim.get("source_text"):
        return {"status": "FAIL", "reason": "SOURCE_TEXT_MISMATCH", "score_effect": "none"}
    if claim.get("qualifiers", {}).get("owner_topic_id", topic_id) != topic_id:
        return {"status": "FAIL", "reason": "OWNER_MISMATCH", "score_effect": "none"}
    if claim.get("assertion_context") not in {"asserted", "corrected"}:
        return {"status": "NOT_ESTABLISHED", "reason": "NOT_ADOPTED_ASSERTION", "score_effect": "none"}
    if claim.get("qualifiers", {}).get("context_inferred_subject") not in {None, False, "False"}:
        return {"status": "NOT_ESTABLISHED", "reason": "INFERRED_SUBJECT", "score_effect": "none"}
    operation = relation_operation(source)
    if operation and claim.get("predicate") == "equivalent_to":
        expected_object = (expected_claim or {}).get("object")
        if operation == "addition":
            return {"status": "FAIL", "reason": "OPERATION_NOT_EQUIVALENCE", "observed_operation": operation, "score_effect": "none"}
        if operation == "division" and expected_object not in {"residual_tolerable_frequency_ratio"}:
            return {"status": "FAIL", "reason": "OPERATION_TARGET_MISMATCH", "observed_operation": operation, "score_effect": "none"}
    if expected_claim is None:
        return {"status": "NOT_ESTABLISHED", "reason": "NO_GROUNDED_TARGET_RELATION", "score_effect": "none"}
    mismatched = [key for key in ("subject", "predicate", "object") if claim.get(key) != expected_claim.get(key)]
    if not set(expected_claim.get("conditions", [])) <= set(claim.get("conditions", [])):
        mismatched.append("conditions")
    if mismatched:
        return {"status": "FAIL", "reason": "CLAIM_TARGET_MISMATCH", "mismatched_fields": mismatched, "score_effect": "none"}
    if operation == "addition":
        return {"status": "FAIL", "reason": "OPERATION_NOT_EQUIVALENCE", "observed_operation": operation, "score_effect": "none"}
    return {"status": "NOT_ESTABLISHED", "reason": "SURFACE_SCHEMA_MATCH_NOT_SEMANTIC_PROOF", "observed_operation": operation, "score_effect": "none"}
