"""Deterministic, topic-neutral quantity/dimension consistency pilot."""

from __future__ import annotations

import copy
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from canonical_grading_evidence import build_canonical_grading_evidence


VERSION = "quantity_dimension_evaluation_v1"
MARKER = "QUANTITY_DIMENSION_EVALUATION_V1"
ONTOLOGY_DIR = Path(__file__).resolve().parent / "grading_ontology"

_NEGATED_CONTEXT = re.compile(
    r"(?:비교할\s*수\s*없|비교하지\s*않|비교하면\s*안|"
    r"하면\s*안|해서는\s*안|잘못|틀린|오류|금지|반례|"
    r"아니(?:다|며|고|라)|동일하지\s*않|"
    r"cannot\s+(?:be\s+)?compar|must\s+not\s+compar|invalid)",
    re.IGNORECASE,
)
_SENTENCE = re.compile(r"[^\n.!?。]+(?:[.!?。]|$)")
_QUOTED_CONTEXT = re.compile(
    r"(?:라고|이라는|라는)\s*(?:주장|말|설명|견해)|[\"“”‘’「」『』]",
    re.IGNORECASE,
)
_REJECTED_CONTEXT = re.compile(
    r"(?:잘못|틀린|오류|금지|반례|invalid|incorrect|wrong)",
    re.IGNORECASE,
)
_SYMBOL_RELATIONS = {
    "<": "less_than",
    "<=": "less_than_or_equal",
    ">": "greater_than",
    ">=": "greater_than_or_equal",
    "≤": "less_than_or_equal",
    "≥": "greater_than_or_equal",
}
_DIMENSION_PHRASES = {
    "inverse_time": re.compile(
        r"(?:시간당\s*(?:고장률|빈도)|1\s*/\s*(?:time|시간)|"
        r"inverse[_\s-]*time|(?:h|hr|hour)\s*\^?\s*-?1)",
        re.IGNORECASE,
    ),
    "dimensionless": re.compile(
        r"(?:무차원|dimensionless|단위가\s*없)",
        re.IGNORECASE,
    ),
}


class QuantityOntologyError(ValueError):
    pass


def _load_json(name: str) -> dict[str, Any]:
    return json.loads((ONTOLOGY_DIR / name).read_text(encoding="utf-8"))


def load_quantity_dimension_ontology() -> dict[str, Any]:
    dimensions = _load_json("dimensions.json")
    quantities = _load_json("quantities.json")
    relations = _load_json("relations.json")
    dimension_map = {
        row["id"]: copy.deepcopy(row)
        for row in dimensions.get("dimensions", [])
    }
    quantity_map = {
        row["id"]: copy.deepcopy(row)
        for row in quantities.get("quantities", [])
    }
    relation_map = {
        row["id"]: copy.deepcopy(row)
        for row in relations.get("relations", [])
    }
    for quantity in quantity_map.values():
        if quantity.get("dimension") not in dimension_map:
            raise QuantityOntologyError(
                f"unknown dimension for {quantity.get('id')}"
            )
    return {
        "dimensions": dimension_map,
        "quantities": quantity_map,
        "relations": relation_map,
    }


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(_normalized(alias)).replace(r"\ ", r"\s*")
    if re.fullmatch(r"[a-z0-9_ ]+", _normalized(alias)):
        return re.compile(rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])", re.I)
    return re.compile(escaped, re.I)


def _mentions(text: str, ontology: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for quantity_id, quantity in ontology["quantities"].items():
        for alias in sorted(quantity.get("aliases", []), key=len, reverse=True):
            for match in _alias_pattern(alias).finditer(_normalized(text)):
                candidates.append({
                    "quantity_id": quantity_id,
                    "start": match.start(),
                    "end": match.end(),
                    "surface": text[match.start():match.end()],
                })
    # Prefer the longest alias when aliases overlap (PFDavg before PFD).
    candidates.sort(key=lambda row: (row["start"], -(row["end"] - row["start"])))
    output: list[dict[str, Any]] = []
    for row in candidates:
        if any(row["start"] < kept["end"] and row["end"] > kept["start"] for kept in output):
            continue
        output.append(row)
    return sorted(output, key=lambda row: row["start"])


def _relation_between(sentence: str, left: dict[str, Any], right: dict[str, Any]):
    between = sentence[left["end"]:right["start"]]
    after_right = sentence[right["end"]:]
    symbol = re.search(r"(<=|>=|≤|≥|<|>)", between)
    if symbol:
        return left, _SYMBOL_RELATIONS[symbol.group(1)], right

    english_relation = re.search(
        r"\b(?:is|are)?\s*(less|smaller|greater|larger)\s+than\b",
        between,
        re.IGNORECASE,
    )
    if english_relation:
        token = english_relation.group(1).casefold()
        predicate = "less_than" if token in {"less", "smaller"} else "greater_than"
        return left, predicate, right

    # A is less/greater than B; A가 B보다 작다/크다.
    tail_relation = re.search(
        r"보다\s*(?:더\s*)?(작|크)|(?:less|smaller|greater|larger)\s+than",
        after_right,
        re.IGNORECASE,
    )
    if tail_relation:
        token = tail_relation.group(1) or tail_relation.group(0).casefold()
        predicate = "less_than" if token.startswith(("작", "less", "smaller")) else "greater_than"
        return left, predicate, right

    # A보다 B가 작다/크다 reverses the grammatical subject.
    if re.search(r"보다", between):
        reverse = re.search(r"(?:작|낮|적)|(?:크|높|많)", after_right)
        if reverse:
            token = reverse.group(0)
            predicate = "less_than" if token in {"작", "낮", "적"} else "greater_than"
            return right, predicate, left

    if re.search(r"(?:직접\s*(?:대소\s*)?비교|directly\s+compar)", sentence, re.I):
        return left, "directly_compared_with", right
    if (
        re.search(r"(?:은|는|이|가)\s*(?:시간당\s*)?$", between)
        and re.search(r"^\s*(?:이|인|으로|라고)", after_right)
    ) or (
        re.search(r"\b(?:is|are)\s+(?:a\s+|an\s+)?$", between, re.I)
    ) or (
        re.search(r"^\s*(?:이|가)?\s*아니", after_right)
    ):
        return left, "equivalent_to", right
    return None


def extract_quantity_relation_evidence(
    answer_text: str,
    *,
    question_text: str = "",
) -> dict[str, Any]:
    ontology = load_quantity_dimension_ontology()
    claims: list[dict[str, Any]] = []
    for sentence_match in _SENTENCE.finditer(answer_text):
        sentence = sentence_match.group(0)
        mentions = _mentions(sentence, ontology)
        polarity = "negative" if _NEGATED_CONTEXT.search(sentence) else "positive"
        assertion_context = (
            "rejected" if _REJECTED_CONTEXT.search(sentence)
            else "quoted" if _QUOTED_CONTEXT.search(sentence)
            else "asserted"
        )
        for left, right in zip(mentions, mentions[1:]):
            relation = _relation_between(sentence, left, right)
            if relation is None:
                continue
            subject, predicate, object_ = relation
            claims.append({
                "subject": subject["quantity_id"],
                "predicate": predicate,
                "object": object_["quantity_id"],
                "polarity": polarity,
                "conditions": [],
                "assertion_context": assertion_context,
                "source_text": sentence,
                "source_span": {
                    "start": sentence_match.start(),
                    "end": sentence_match.end(),
                },
                "qualifiers": {},
                "requirement_refs": [],
                "extraction_confidence": 1.0,
            })

        # Explicit dimension assertions are also ontology relations.
        for mention_index, mention in enumerate(mentions):
            assertion_end = (
                mentions[mention_index + 1]["start"]
                if mention_index + 1 < len(mentions)
                else len(sentence)
            )
            assertion_text = sentence[mention["end"]:assertion_end]
            for dimension_id, pattern in _DIMENSION_PHRASES.items():
                if pattern.search(assertion_text):
                    claims.append({
                        "subject": mention["quantity_id"],
                        "predicate": "has_dimension",
                        "object": dimension_id,
                        "polarity": polarity,
                        "conditions": [],
                        "assertion_context": assertion_context,
                        "source_text": sentence,
                        "source_span": {
                            "start": sentence_match.start(),
                            "end": sentence_match.end(),
                        },
                        "qualifiers": {},
                        "requirement_refs": [],
                        "extraction_confidence": 1.0,
                    })
                    break
    return build_canonical_grading_evidence(
        question_text=question_text,
        answer_text=answer_text,
        source={
            "mode": "deterministic_parser",
            "resolver_id": "quantity_relation_parser",
            "resolver_version": "1",
        },
        claims=claims,
    )


def find_unresolved_quantity_spans(
    answer_text: str,
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return quantity-bearing sentences with no deterministic claim."""

    ontology = load_quantity_dimension_ontology()
    resolved_spans = {
        (row["source_span"]["start"], row["source_span"]["end"])
        for row in evidence.get("claims", [])
        if isinstance(row, dict) and isinstance(row.get("source_span"), dict)
    }
    output: list[dict[str, Any]] = []
    for match in _SENTENCE.finditer(answer_text):
        span = (match.start(), match.end())
        if span in resolved_spans:
            continue
        mentions = _mentions(match.group(0), ontology)
        if not mentions:
            continue
        output.append({
            "start": match.start(),
            "end": match.end(),
            "source_text": match.group(0),
            "concept_candidates": sorted({row["quantity_id"] for row in mentions}),
        })
    return output


def evaluate_quantity_dimension_consistency(
    evidence: dict[str, Any],
) -> dict[str, Any]:
    ontology = load_quantity_dimension_ontology()
    violations: list[dict[str, Any]] = []
    checked = 0
    for claim in evidence.get("claims", []):
        if (
            not isinstance(claim, dict)
            or claim.get("polarity") != "positive"
            or claim.get("assertion_context", "asserted") not in {"asserted", "corrected"}
        ):
            continue
        subject = ontology["quantities"].get(claim.get("subject"))
        if subject is None:
            continue
        predicate = str(claim.get("predicate") or "")
        if predicate == "has_dimension":
            checked += 1
            expected = subject["dimension"]
            observed = claim.get("object")
            if observed != expected:
                violations.append({
                    "code": "INVALID_DIMENSION_ASSERTION",
                    "claim_id": claim.get("claim_id"),
                    "subject": claim.get("subject"),
                    "expected_dimension": expected,
                    "observed_dimension": observed,
                    "source_text": claim.get("source_text"),
                })
            continue
        relation = ontology["relations"].get(predicate)
        object_ = ontology["quantities"].get(claim.get("object"))
        if not relation or not object_ or not relation.get("requires_same_dimension"):
            continue
        checked += 1
        if subject["dimension"] != object_["dimension"]:
            violations.append({
                "code": "DIMENSIONALLY_INVALID_COMPARISON",
                "claim_id": claim.get("claim_id"),
                "subject": claim.get("subject"),
                "predicate": predicate,
                "object": claim.get("object"),
                "lhs_dimension": subject["dimension"],
                "rhs_dimension": object_["dimension"],
                "source_text": claim.get("source_text"),
            })
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "score_effect": "none",
        "checked_claim_count": checked,
        "violation_count": len(violations),
        "technical_error_detected": bool(violations),
        "requirement_full_credit_allowed": not violations,
        "perfect_theory_comment_allowed": not violations,
        "violations": violations,
    }


def analyze_quantity_dimensions(
    answer_text: str,
    *,
    question_text: str = "",
) -> dict[str, Any]:
    evidence = extract_quantity_relation_evidence(
        answer_text,
        question_text=question_text,
    )
    result = evaluate_quantity_dimension_consistency(evidence)
    result["canonical_evidence"] = evidence
    return result
