"""Deterministic extraction of provider-neutral engineering claims.

The extractor may identify evidence, but it never assigns requirement states,
fatality, scores, or verdicts.  It uses global aliases and additive Topic
machine contracts; it does not special-case complete answer strings.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

from canonical_grading_evidence import build_canonical_grading_evidence
from deterministic_requirement_evaluator import load_machine_contracts
from quantity_dimension_evaluator import extract_quantity_relation_evidence


VERSION = "canonical_claim_extractor_v1"
MARKER = "CANONICAL_CLAIM_EXTRACTOR_V1"
ROOT = Path(__file__).resolve().parent
_SENTENCE = re.compile(r"[^\n!?。]+?(?:\.(?![A-Za-z0-9])|[!?。]|\n|$)")
_QUOTE = re.compile(r'["“”‘’「」『』](.*?)["“”‘’「」『』]')
_QUOTED_REPORT = re.compile(r"(?:라고|이라는|라는)\s*(?:주장|말|설명|견해)")
_REJECT = re.compile(
    r"(?:잘못|틀린|부정확|오류(?:이|인|로|라는|라고)|성립하지\s*않|invalid|incorrect|wrong)",
    re.I,
)
_CORRECT = re.compile(r"(?:정정|올바르게|실제로는|대신|correct(?:ly|ion)?)", re.I)
_NEGATE = re.compile(r"(?:하지\s*않|아니(?:다|며|고|라)|할\s*수\s*없|불가능|not\b|never\b)", re.I)
_CONDITION = re.compile(r"(?:경우|조건|에서는|일\s*때|when\b|if\b|under\b)", re.I)
_CLAUSE_BOUNDARY = re.compile(r";", re.I)


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", str(value or "")).casefold()


def _load_aliases() -> dict[str, list[str]]:
    concepts = json.loads(
        (ROOT / "grading_ontology/engineering_concepts.json").read_text(encoding="utf-8")
    )
    quantities = json.loads(
        (ROOT / "grading_ontology/quantities.json").read_text(encoding="utf-8")
    )
    output: dict[str, list[str]] = {}
    for row in [*concepts.get("concepts", []), *quantities.get("quantities", [])]:
        concept_id = str(row.get("id") or "")
        values = [concept_id.replace("_", " "), *row.get("aliases", [])]
        output.setdefault(concept_id, [])
        for value in values:
            normalized = _normalized(value).strip()
            if normalized and normalized not in output[concept_id]:
                output[concept_id].append(normalized)
    return output


def _load_predicates() -> dict[str, list[str]]:
    payload = json.loads(
        (ROOT / "grading_ontology/canonical_predicates.json").read_text(encoding="utf-8")
    )
    return {
        row["id"]: [_normalized(value) for value in row.get("aliases", [])]
        for row in payload.get("predicates", [])
    }


def _find_alias(
    text: str,
    aliases: list[str],
    *,
    start_at: int = 0,
) -> tuple[int, int] | None:
    normalized = _normalized(text)
    matches: list[tuple[int, int]] = []
    for alias in aliases:
        start = normalized.find(alias, start_at)
        if start >= 0:
            matches.append((start, start + len(alias)))
    return min(matches, key=lambda row: (row[0], -(row[1] - row[0]))) if matches else None


def _find_subject_alias(text: str, aliases: list[str]) -> tuple[int, int] | None:
    """Prefer an occurrence carrying an explicit Korean subject/topic marker."""
    normalized = _normalized(text)
    matches: list[tuple[int, int]] = []
    for alias in aliases:
        start = 0
        while True:
            index = normalized.find(alias, start)
            if index < 0:
                break
            matches.append((index, index + len(alias)))
            start = index + max(1, len(alias))
    if not matches:
        return None
    marked = [span for span in matches if _marked_as_subject(text, span)]
    return min(marked or matches, key=lambda row: (row[0], -(row[1] - row[0])))


def _assertion_context(text: str, fact_end: int) -> str:
    normalized = _normalized(text)
    correction = _CORRECT.search(normalized)
    if correction and fact_end >= correction.start():
        return "corrected"
    quote_ranges = [match.span(1) for match in _QUOTE.finditer(text)]
    if quote_ranges and any(start <= fact_end <= end for start, end in quote_ranges):
        return "rejected" if _REJECT.search(normalized) else "quoted"
    if _QUOTED_REPORT.search(normalized):
        return "rejected" if _REJECT.search(normalized) else "quoted"
    if _REJECT.search(normalized):
        return "rejected"
    return "asserted"


def _polarity(
    text: str,
    object_span: tuple[int, int],
    predicate_span: tuple[int, int],
    predicate_id: str,
) -> str:
    normalized = _normalized(text)
    predicate_text = normalized[predicate_span[0]:predicate_span[1]]
    # These predicates encode a negative surface relation as a positive
    # canonical fact ("does not replace" => supplements).  Do not invert the
    # claim merely because the predicate phrase itself contains negation.
    encoded_negative_relation = (
        predicate_id == "supplements" and "대체하지" in predicate_text
    ) or (
        predicate_id == "distinct_from"
        and any(token in predicate_text for token in ("동일하지", "distinct", "different"))
    ) or (
        predicate_id == "does_not_guarantee"
    )
    if encoded_negative_relation:
        return "positive"
    relation_start = min(predicate_span[0], object_span[0])
    relation_end = max(predicate_span[1], object_span[1]) + 12
    window = normalized[relation_start:relation_end]
    # In "A가 아니라 B" the object B is the adopted correction.
    not_but = normalized.find("아니라")
    if not_but >= 0 and object_span[0] > not_but:
        return "positive"
    return "negative" if _NEGATE.search(window) else "positive"


def _conditions(
    text: str,
    aliases: dict[str, list[str]],
    excluded: set[str],
) -> list[str]:
    if not _CONDITION.search(_normalized(text)):
        return []
    return sorted(
        concept_id for concept_id, values in aliases.items()
        if concept_id not in excluded and _find_alias(text, values) is not None
    )


def _same_clause(
    text: str,
    subject_span: tuple[int, int],
    object_span: tuple[int, int],
) -> bool:
    start = min(subject_span[1], object_span[1])
    end = max(subject_span[0], object_span[0])
    return not _CLAUSE_BOUNDARY.search(_normalized(text)[start:end])


def _marked_as_subject(text: str, span: tuple[int, int]) -> bool:
    """Return whether an occurrence can own a following coordinated relation."""
    tail = _normalized(text)[span[1]:span[1] + 12]
    return re.match(r"\s*(?:은|는|이(?!며)|가|:)", tail) is not None


def extract_canonical_claim_evidence(
    answer_text: str,
    *,
    question_text: str = "",
    topic_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Extract explicit contract relations and preserve unresolved spans."""
    aliases = _load_aliases()
    predicates = _load_predicates()
    contracts = load_machine_contracts(topic_ids)
    quantity_document = extract_quantity_relation_evidence(
        answer_text, question_text=question_text,
    )
    claims = [dict(row) for row in quantity_document["claims"]]
    unresolved: list[dict[str, Any]] = []

    facts = [
        (contract["owner_topic_id"], fact)
        for contract in contracts
        for fact in contract["facts"]
    ]
    relation_subjects = sorted({
        (owner_topic_id, fact["subject"], fact["predicate"])
        for owner_topic_id, fact in facts
    })
    predicate_objects: dict[str, set[str]] = {}
    for _, fact in facts:
        predicate_objects.setdefault(fact["predicate"], set()).add(fact["object"])
    for sentence_match in _SENTENCE.finditer(answer_text):
        sentence = sentence_match.group(0)
        sentence_claim_count = 0
        concept_ids_present = {
            concept_id for concept_id, values in aliases.items()
            if _find_alias(sentence, values) is not None
        }
        for owner_topic_id, subject_id, predicate_id in relation_subjects:
            subject_span = _find_subject_alias(sentence, aliases.get(subject_id, []))
            if not subject_span:
                continue
            predicate_span = _find_alias(
                sentence,
                predicates.get(predicate_id, []),
                start_at=subject_span[1],
            )
            if not predicate_span:
                continue
            object_matches = []
            for object_id in sorted(predicate_objects.get(predicate_id, set())):
                object_span = _find_alias(sentence, aliases.get(object_id, []))
                if (
                    not object_span
                    or subject_span[0] > min(predicate_span[0], object_span[0])
                    or not _same_clause(sentence, subject_span, object_span)
                ):
                    continue
                # In a coordinated sentence ("Verification ... and Validation ..."),
                # the nearest compatible subject owns the later object.  This
                # prevents an earlier subject from stealing another clause's
                # relation without relying on a language-specific conjunction.
                compatible_subjects = []
                for _, candidate_subject, candidate_predicate in relation_subjects:
                    if candidate_predicate != predicate_id:
                        continue
                    candidate_span = _find_subject_alias(
                        sentence, aliases.get(candidate_subject, [])
                    )
                    if (
                        candidate_span
                        and candidate_span[1] <= object_span[0]
                        and _marked_as_subject(sentence, candidate_span)
                    ):
                        compatible_subjects.append((candidate_span[0], candidate_subject))
                if compatible_subjects and max(compatible_subjects)[1] != subject_id:
                    continue
                object_matches.append((object_id, object_span))
            # One surface phrase owns one canonical object. Prefer the longest
            # alias span ("module interface" over the nested word "module").
            selected_objects: list[tuple[str, tuple[int, int]]] = []
            for object_id, object_span in sorted(
                object_matches,
                key=lambda row: (-(row[1][1] - row[1][0]), row[1][0], row[0]),
            ):
                if any(
                    object_span[0] < kept_span[1]
                    and object_span[1] > kept_span[0]
                    for _, kept_span in selected_objects
                ):
                    continue
                selected_objects.append((object_id, object_span))
            for object_id, object_span in sorted(selected_objects):
                observed_polarity = _polarity(
                    sentence, object_span, predicate_span, predicate_id
                )
                context = _assertion_context(sentence, max(subject_span[1], object_span[1]))
                claims.append({
                    "subject": subject_id,
                    "predicate": predicate_id,
                    "object": object_id,
                    "polarity": observed_polarity,
                    "conditions": _conditions(
                        sentence, aliases, {subject_id, object_id},
                    ),
                    "assertion_context": context,
                    "source_text": sentence,
                    "source_span": {
                        "start": sentence_match.start(),
                        "end": sentence_match.end(),
                    },
                    "requirement_refs": [],
                    "qualifiers": {"owner_topic_id": owner_topic_id},
                    "extraction_confidence": 1.0,
                })
                sentence_claim_count += 1
        if concept_ids_present and sentence_claim_count == 0 and not any(
            row["source_span"] == {
                "start": sentence_match.start(), "end": sentence_match.end(),
            }
            for row in quantity_document["claims"]
        ):
            unresolved.append({
                "start": sentence_match.start(),
                "end": sentence_match.end(),
                "source_text": sentence,
                "concept_candidates": sorted(concept_ids_present),
            })

    # Equivalent parser paths may produce the same relation. Keep one stable row.
    unique: dict[tuple[Any, ...], dict[str, Any]] = {}
    for claim in claims:
        key = (
            claim["source_span"]["start"], claim["source_span"]["end"],
            claim["subject"], claim["predicate"], claim["object"],
            claim.get("polarity", "positive"),
            claim.get("assertion_context", "asserted"),
        )
        unique.setdefault(key, claim)
    document = build_canonical_grading_evidence(
        question_text=question_text,
        answer_text=answer_text,
        source={
            "mode": "deterministic_parser",
            "resolver_id": "canonical_claim_extractor",
            "resolver_version": "1",
        },
        claims=list(unique.values()),
    )
    return {
        "version": VERSION,
        "marker": MARKER,
        "provider_calls": 0,
        "llm_verdict_authority": 0,
        "canonical_evidence": document,
        "unresolved_spans": unresolved,
        "extraction_complete": not unresolved,
    }
