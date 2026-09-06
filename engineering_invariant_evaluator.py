"""Deterministic, ontology-driven engineering relation invariants."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


VERSION = "engineering_invariant_evaluator_v1"
MARKER = "ENGINEERING_INVARIANT_EVALUATION_V1"
ROOT = Path(__file__).resolve().parent
ONTOLOGY = ROOT / "grading_ontology"
_UNIT = re.compile(r"[^\n.!?。]+(?:\n|[.!?。]|$)")
_CORRECTION = re.compile(
    r"(?:잘못된\s*(?:예|주장)|오류\s*(?:예|주장)|혼동(?:하면|해서는)\s*안|"
    r"대체하지\s*않|자동으로\s*(?:줄어들|감소하)지\s*않|"
    r"분류하지\s*않|서로\s*구분|다른\s*분류축|별도로?\s*(?:평가|검증|수행)|"
    r"incorrect\s+example|must\s+not|does\s+not\s+replace)",
    re.IGNORECASE,
)


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _pattern(alias: str) -> re.Pattern[str]:
    normalized = _normalized(alias)
    escaped = re.escape(normalized).replace(r"\ ", r"\s*")
    if re.fullmatch(r"[a-z0-9_, ]+", normalized):
        return re.compile(rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])", re.I)
    return re.compile(escaped, re.I)


def load_engineering_ontology() -> dict[str, Any]:
    concepts_payload = json.loads(
        (ONTOLOGY / "engineering_concepts.json").read_text(encoding="utf-8")
    )
    invariants_payload = json.loads(
        (ONTOLOGY / "engineering_invariants.json").read_text(encoding="utf-8")
    )
    concepts = {row["id"]: row for row in concepts_payload["concepts"]}
    cues = concepts_payload["cue_groups"]
    for rule in invariants_payload["rules"]:
        required = list(rule.get("all_concepts", []))
        required.extend(rule.get("none_concepts", []))
        for alternative in rule.get("alternatives", []):
            required.extend(alternative.get("all_concepts", []))
            required.extend(alternative.get("none_concepts", []))
        if not set(required) <= set(concepts):
            raise ValueError(f"unknown concept in {rule['code']}")
        cue_refs = list(rule.get("any_cue_groups", []))
        for alternative in rule.get("alternatives", []):
            cue_refs.extend(alternative.get("any_cue_groups", []))
        if not set(cue_refs) <= set(cues):
            raise ValueError(f"unknown cue group in {rule['code']}")
    return {"concepts": concepts, "cue_groups": cues, "rules": invariants_payload["rules"]}


def _present_concepts(text: str, concepts: dict[str, Any]) -> set[str]:
    return {
        concept_id
        for concept_id, concept in concepts.items()
        if any(_pattern(alias).search(_normalized(text)) for alias in concept["aliases"])
    }


def _has_any_cue(text: str, group_ids: list[str], cues: dict[str, list[str]]) -> bool:
    if not group_ids:
        return True
    normalized = _normalized(text)
    return any(
        _pattern(alias).search(normalized)
        for group_id in group_ids
        for alias in cues[group_id]
    )


def _matches_clause(
    text: str,
    present: set[str],
    clause: dict[str, Any],
    cues: dict[str, list[str]],
) -> bool:
    return (
        set(clause.get("all_concepts", [])) <= present
        and not (set(clause.get("none_concepts", [])) & present)
        and _has_any_cue(text, clause.get("any_cue_groups", []), cues)
    )


def evaluate_engineering_invariants(answer_text: str) -> dict[str, Any]:
    ontology = load_engineering_ontology()
    violations: list[dict[str, Any]] = []
    for match in _UNIT.finditer(answer_text):
        source = match.group(0)
        if _CORRECTION.search(source):
            continue
        present = _present_concepts(source, ontology["concepts"])
        for rule in ontology["rules"]:
            if not _matches_clause(source, present, rule, ontology["cue_groups"]):
                continue
            alternatives = rule.get("alternatives", [])
            if alternatives and not any(
                _matches_clause(source, present, row, ontology["cue_groups"])
                for row in alternatives
            ):
                continue
            violations.append({
                "code": rule["code"],
                "source_text": source,
                "source_span": {"start": match.start(), "end": match.end()},
                "matched_concepts": sorted(present),
            })
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
        "score_effect": "none",
        "violations": violations,
        "technical_error_detected": bool(violations),
    }
