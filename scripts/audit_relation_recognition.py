"""Offline diagnostic for explicit relations in existing Topic machine contracts."""

from __future__ import annotations

import re

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.cross_topic_question_contract import evaluate_cross_topic_question
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements, requirement_scope_by_topic
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_requirement_evaluator import load_machine_contracts

# The pilot accepts complete Korean declaratives only. The existing extractor
# also recognizes relation vocabulary in fragments, including comma lists.
_KOREAN_DECLARATIVE = re.compile(r"[가-힣](?:다|요)[.!?。]?\s*$")
_QUOTATION = re.compile(r'"[^"]*"|“[^”]*”|‘[^’]*’|「[^」]*」|『[^』]*』')
_CONDITIONAL = re.compile(r"경우|조건에서|일\s*때|\b(?:if|when|unless)\b", re.I)
_QUOTE_MARKS = frozenset('"“”‘’「」『』')


def audit_relation_recognition(
    *, question_text: str, answer_text: str, topic_id: str, requirement_id: str,
) -> dict:
    """Inspect an explicitly selected demand in the question's existing scope.

    Expose grounded contract matches for review. The output has no grading
    authority. Absence of a machine relation alone does not prove an omission.
    """
    def result(status: str, reason: str, spans: set[tuple[int, int]] | None = None) -> dict:
        return {
            "status": status,
            "reason": reason,
            "score_effect": "none",
            "evidence_spans": [{"start": start, "end": end} for start, end in sorted(spans or ())],
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

    extraction = extract_canonical_claim_evidence(answer_text, question_text=question_text, topic_ids=[topic_id])
    required = set(rule["required_fact_ids"])
    facts = [fact for fact in contract["facts"] if fact["fact_id"] in required]

    quoted_spans = [match.span() for match in _QUOTATION.finditer(answer_text)]
    supported = set()
    support_spans = set()
    contradiction_spans = set()
    unbound_alternative = False
    for claim in extraction["canonical_evidence"]["claims"]:
        qualifiers = claim["qualifiers"]
        if (
            claim["assertion_context"] not in {"asserted", "corrected"}
            or qualifiers.get("context_inferred_subject") not in {None, "False"}
            or qualifiers.get("owner_topic_id", topic_id) != topic_id
        ):
            continue
        start, end = claim["source_span"]["start"], claim["source_span"]["end"]
        if not 0 <= start < end <= len(answer_text) or answer_text[start:end] != claim["source_text"]:
            continue
        if (
            _QUOTE_MARKS.intersection(claim["source_text"])
            or any(start < quote_end and quote_start < end for quote_start, quote_end in quoted_spans)
            or not _KOREAN_DECLARATIVE.search(claim["source_text"])
        ):
            continue
        for fact in facts:
            if any(claim[key] != fact[key] for key in ("subject", "predicate", "object")):
                continue
            # Exact condition names still do not establish that a multi-clause
            # condition governs the relation. Keep the pilot to unconditional
            # contracts and claims.
            if fact.get("conditions") or claim["conditions"] or _CONDITIONAL.search(claim["source_text"]):
                unbound_alternative = True
                continue
            if claim["polarity"] == fact["polarity"]:
                supported.add(fact["fact_id"])
                support_spans.add((start, end))
            else:
                contradiction_spans.add((start, end))

    all_spans = support_spans | contradiction_spans
    if unbound_alternative or (supported and contradiction_spans):
        return result("RECOGNITION_UNCERTAIN", "CONDITIONAL_OR_MIXED_EVIDENCE", all_spans)
    if contradiction_spans:
        return result("CONFIRMED_CONTRADICTION", "EXPLICIT_OPPOSITE_POLARITY", all_spans)
    if len(supported) >= rule["minimum_match_count"]:
        return result("CONFIRMED_RELATION", "EXPLICIT_CONTRACT_MATCH", support_spans)
    reason = "PARTIAL_CONTRACT_EVIDENCE" if supported else "NO_CONFIRMED_RELATION"
    return result("RECOGNITION_UNCERTAIN", reason, support_spans)
