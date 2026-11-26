"""Offline diagnostic for explicit relations in existing Topic machine contracts."""

from __future__ import annotations

import re
import hashlib

from grading.evidence.canonical_grading_evidence import (
    CanonicalEvidenceError,
    validate_canonical_grading_evidence,
)

from grading.evidence.canonical_claim_extractor import (
    _CORRECT,
    _REJECT,
    _find_alias,
    _find_subject_alias,
    _load_aliases,
    extract_canonical_claim_evidence,
)
from grading.evidence.claim_fidelity_audit import (
    assess_claim_fidelity,
    assess_deterministic_claim_fidelity,
)
from grading.evidence.cross_topic_question_contract import evaluate_cross_topic_question
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements, requirement_scope_by_topic
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_requirement_evaluator import load_machine_contracts

# The pilot accepts complete Korean declaratives only. The existing extractor
# also recognizes relation vocabulary in fragments, including comma lists.
_KOREAN_DECLARATIVE = re.compile(r"[가-힣](?:다|요)[.!?。]?\s*$")
_ENGLISH_DECLARATIVE = re.compile(
    r"\b(?:is|are|was|were|has|have|provides?|serves?|differs?|remain(?:s)?|"
    r"equals?|represents?|checks?|verifies?|guarantees?)\b[^.!?]*[.!?]\s*$", re.I,
)
_QUOTATION = re.compile(r'"[^"]*"|“[^”]*”|‘[^’]*’|「[^」]*」|『[^』]*』')
_CONDITIONAL = re.compile(r"경우|조건에서|일\s*때|\b(?:if|when|unless)\b", re.I)
_QUOTE_MARKS = frozenset('"“”‘’「」『』')


def audit_relation_recognition(
    *, question_text: str, answer_text: str, topic_id: str, requirement_id: str,
    canonical_evidence_override: dict | None = None,
) -> dict:
    """Inspect an explicitly selected demand in the question's existing scope.

    Expose grounded contract matches for review. The output has no grading
    authority. Absence of a machine relation alone does not prove an omission.
    """
    fidelity_failures: list[dict] = []
    fidelity_checks: list[dict] = []

    def result(status: str, reason: str, spans: set[tuple[int, int]] | None = None) -> dict:
        return {
            "status": status,
            "reason": reason,
            "score_effect": "none",
            "evidence_spans": [{"start": start, "end": end} for start, end in sorted(spans or ())],
            "claim_fidelity_failures": list(fidelity_failures),
            "claim_fidelity_checks": list(fidelity_checks),
        }

    topics = route_question_topics(question_text)["topic_ids"]
    if (
        not topic_id
        or not requirement_id
        or topic_id not in topics
        or excluded_from_scoring(topic_id=topic_id, anchor_id=requirement_id)
    ):
        return result("RECOGNITION_UNCERTAIN", "OWNER_OR_EXCLUSION")

    contracts = load_machine_contracts([topic_id])
    if not contracts:
        return result("RECOGNITION_UNCERTAIN", "NO_MACHINE_CONTRACT")
    contract = contracts[0]
    rule = next((row for row in contract["requirement_rules"]
                 if row["requirement_id"] == requirement_id and not row.get("violation_only")), None)
    if rule is None:
        return result("RECOGNITION_UNCERTAIN", "NO_REQUIREMENT_RULE")
    scope_inputs = {"question_text": question_text, "answer_text": answer_text, "topic_ids": topics}
    scope = evaluate_cross_topic_question(**scope_inputs) or evaluate_fact_anchor_requirements(**scope_inputs)
    if requirement_id not in requirement_scope_by_topic(scope).get(topic_id, []):
        return result("RECOGNITION_UNCERTAIN", "OUTSIDE_QUESTION_SCOPE")
    if not answer_text.strip():
        return result("CONTENT_INSUFFICIENT", "EMPTY_ANSWER")

    if canonical_evidence_override is None:
        extraction = extract_canonical_claim_evidence(answer_text, question_text=question_text, topic_ids=[topic_id])
    else:
        try:
            evidence = validate_canonical_grading_evidence(
                canonical_evidence_override, answer_text=answer_text,
            )
        except (CanonicalEvidenceError, TypeError, ValueError):
            return result("RECOGNITION_UNCERTAIN", "INVALID_EVIDENCE_OVERRIDE")
        expected_question_sha = hashlib.sha256(question_text.encode("utf-8")).hexdigest()
        if evidence["input_fingerprint"].get("question_sha256") != expected_question_sha:
            return result("RECOGNITION_UNCERTAIN", "QUESTION_FINGERPRINT_MISMATCH")
        if evidence["source"].get("mode") not in {"semantic_resolver", "deterministic_parser"}:
            return result("RECOGNITION_UNCERTAIN", "UNSUPPORTED_EVIDENCE_SOURCE")
        if any(
            (claim.get("qualifiers") or {}).get("owner_topic_id") != topic_id
            for claim in evidence["claims"]
        ):
            return result("RECOGNITION_UNCERTAIN", "EVIDENCE_OWNER_MISMATCH")
        extraction = {"canonical_evidence": evidence, "unresolved_spans": []}
    required = set(rule["required_fact_ids"])
    facts = [fact for fact in contract["facts"] if fact["fact_id"] in required]

    quoted_spans = [match.span() for match in _QUOTATION.finditer(answer_text)]
    supported = set()
    support_spans = set()
    contradiction_spans = set()
    supported_claims = []
    contradiction_claims = []
    unbound_alternative = False
    extracted_claims = extraction["canonical_evidence"]["claims"]
    for claim in extracted_claims:
        qualifiers = claim["qualifiers"]
        context_inferred = qualifiers.get("context_inferred_subject")
        inferred_correction_grounded = (
            claim["assertion_context"] == "corrected"
            and any(
                prior["subject"] == claim["subject"]
                and prior["predicate"] == claim["predicate"]
                and prior["object"] == claim["object"]
                and prior["polarity"] != claim["polarity"]
                and prior["assertion_context"] in {"rejected", "asserted"}
                and (
                    prior["source_span"]["end"] <= claim["source_span"]["start"]
                    and (
                        _REJECT.search(answer_text[
                            prior["source_span"]["end"]:claim["source_span"]["start"]
                        ])
                        or _REJECT.search(prior["source_text"])
                    )
                    or prior["source_span"] == claim["source_span"]
                    and _REJECT.search(claim["source_text"])
                )
                for prior in extracted_claims
            )
        )
        if (
            claim["assertion_context"] not in {"asserted", "corrected"}
            or context_inferred not in {None, "False"} and not inferred_correction_grounded
            or qualifiers.get("owner_topic_id", topic_id) != topic_id
        ):
            continue
        start, end = claim["source_span"]["start"], claim["source_span"]["end"]
        if not 0 <= start < end <= len(answer_text) or answer_text[start:end] != claim["source_text"]:
            continue
        if (
            _QUOTE_MARKS.intersection(claim["source_text"])
            or any(start < quote_end and quote_start < end for quote_start, quote_end in quoted_spans)
            or not (
                _KOREAN_DECLARATIVE.search(claim["source_text"])
                or _ENGLISH_DECLARATIVE.search(claim["source_text"])
            )
        ):
            continue
        for fact in facts:
            if any(claim[key] != fact[key] for key in ("subject", "predicate", "object")):
                continue
            evidence_source = extraction["canonical_evidence"].get("source", {}).get("mode")
            if evidence_source == "deterministic_parser":
                fidelity = assess_deterministic_claim_fidelity(
                    answer_text=answer_text, claim=claim, topic_id=topic_id,
                    expected_claim=fact,
                )
            else:
                fidelity = assess_claim_fidelity(
                    answer_text=answer_text, claim=claim, topic_id=topic_id,
                )
            fidelity_checks.append({
                "fact_id": fact["fact_id"], "start": start, "end": end,
                "status": fidelity["status"], "reason": fidelity["reason"],
                "score_effect": "none",
            })
            if fidelity["status"] == "FAIL":
                fidelity_failures.append({
                    "fact_id": fact["fact_id"], "start": start, "end": end,
                    "reason": fidelity["reason"],
                })
                continue
            required_conditions = set(fact.get("conditions", []))
            claimed_conditions = set(claim.get("conditions", []))
            if required_conditions:
                if not required_conditions <= claimed_conditions:
                    unbound_alternative = True
                    continue
                aliases = _load_aliases()
                subject_aliases = aliases.get(fact["subject"], [])
                subject_span = _find_subject_alias(
                    claim["source_text"], subject_aliases,
                    predicate_id=fact["predicate"],
                )
                # A required condition must be explicitly stated before the
                # relation subject, in the same source sentence. Merely
                # co-occurring elsewhere in the sentence is insufficient.
                condition_bound = bool(subject_span)
                for condition_id in required_conditions:
                    condition_span = _find_alias(
                        claim["source_text"], aliases.get(condition_id, []),
                    )
                    if not condition_span or not subject_span or condition_span[1] > subject_span[0]:
                        condition_bound = False
                        break
                if not condition_bound:
                    unbound_alternative = True
                    continue
            elif _CONDITIONAL.search(claim["source_text"]):
                # Conditional language with no extracted condition cannot
                # establish the contract's relation scope.
                unbound_alternative = True
                continue
            if claim["polarity"] == fact["polarity"]:
                supported.add(fact["fact_id"])
                support_spans.add((start, end))
                supported_claims.append({
                    "fact_id": fact["fact_id"],
                    "start": start,
                    "end": end,
                    "assertion_context": claim["assertion_context"],
                    "source_text": claim["source_text"],
                    "polarity": claim["polarity"],
                })
            else:
                contradiction_claims.append({
                    "fact_id": fact["fact_id"],
                    "start": start,
                    "end": end,
                    "source_text": claim["source_text"],
                    "assertion_context": claim["assertion_context"],
                })

    # When an explicit rejection is followed by a corrected claim about the
    # same fact in the same source span, treat the earlier polarity as the
    # rejected proposition rather than as a second adopted assertion.
    active_contradictions = []
    for contradiction in contradiction_claims:
        corrected = any(
            supported["fact_id"] == contradiction["fact_id"]
            and supported["assertion_context"] == "corrected"
            and (
                (
                    supported["start"] >= contradiction["end"]
                    and (
                        _REJECT.search(
                            answer_text[contradiction["end"]:supported["start"]]
                        )
                        or _REJECT.search(contradiction["source_text"])
                    )
                    and _CORRECT.search(supported["source_text"])
                )
                or (
                    supported["start"] == contradiction["start"]
                    and supported["end"] == contradiction["end"]
                    and _REJECT.search(contradiction["source_text"])
                    and _CORRECT.search(contradiction["source_text"])
                )
            )
            for supported in supported_claims
        )
        if not corrected:
            active_contradictions.append(contradiction)
    contradiction_spans = {
        (row["start"], row["end"]) for row in active_contradictions
    }

    all_spans = support_spans | contradiction_spans
    unresolved_relation_spans = []
    for unresolved in extraction.get("unresolved_spans", []):
        concepts = set(unresolved.get("concept_candidates", []))
        candidate_facts = [
            fact for fact in facts
            if {fact["subject"], fact["object"]} <= concepts
        ]
        if not candidate_facts:
            continue
        corrected_later = any(
            claim["assertion_context"] == "corrected"
            and claim["start"] >= unresolved["end"]
            and claim["fact_id"] in {fact["fact_id"] for fact in candidate_facts}
            for claim in supported_claims
        )
        if not corrected_later:
            unresolved_relation_spans.append(unresolved)
    if unresolved_relation_spans and (supported or contradiction_spans):
        return result(
            "RECOGNITION_UNCERTAIN", "UNRESOLVED_EXTRACTION_SPAN", all_spans,
        )
    if fidelity_failures:
        return result("RECOGNITION_UNCERTAIN", "CLAIM_FIDELITY_FAILURE", all_spans | {
            (row["start"], row["end"]) for row in fidelity_failures
        })
    if unbound_alternative or (supported and contradiction_spans):
        return result("RECOGNITION_UNCERTAIN", "CONDITIONAL_OR_MIXED_EVIDENCE", all_spans)
    if contradiction_spans:
        return result("CONFIRMED_CONTRADICTION", "EXPLICIT_OPPOSITE_POLARITY", all_spans)
    if len(supported) >= rule["minimum_match_count"]:
        return result("CONFIRMED_RELATION", "EXPLICIT_CONTRACT_MATCH", support_spans)
    reason = "PARTIAL_CONTRACT_EVIDENCE" if supported else "NO_CONFIRMED_RELATION"
    return result("RECOGNITION_UNCERTAIN", reason, support_spans)
