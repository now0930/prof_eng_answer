"""Stage 1 contracts for source facts, question scope, interpretation and snapshots.

These records are read-only inputs. None grants a WordPress claim grading authority
or changes the current Topic Pack / generated bank runtime.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any


VERSION = "fact-grounded-contract-v1"
_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_TASKS = {"define", "explain", "compare", "calculate", "design", "evaluate", "apply"}
_FORBIDDEN = {
    "score", "total_score", "final_score", "grade", "verdict", "fatal",
    "requirement_status", "demand_state", "severity", "cap", "floor",
    "passing_score_allowed", "strong_verdict_allowed", "status",
}


class FactGroundedContractError(ValueError):
    """A stage-one record crossed a trust, provenance or identity boundary."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise FactGroundedContractError(message)


def _fields(value: Any, required: set[str], optional: set[str] = frozenset()) -> None:
    _require(isinstance(value, dict), "record must be an object")
    _require(required <= set(value) <= required | optional, "record fields do not match contract")


def _id(value: Any, name: str) -> None:
    _require(isinstance(value, str) and _ID.fullmatch(value) is not None, f"invalid {name}")


def _sha(value: Any, name: str) -> None:
    _require(isinstance(value, str) and _SHA.fullmatch(value) is not None, f"invalid {name}")


def _string(value: Any, name: str) -> None:
    _require(isinstance(value, str) and bool(value.strip()), f"empty {name}")


def _list_of_ids(value: Any, name: str) -> None:
    _require(isinstance(value, list), f"{name} must be an array")
    for item in value:
        _id(item, name)
    _require(len(value) == len(set(value)), f"duplicate {name}")


def _span(value: Any, source: str, name: str) -> None:
    _fields(value, {"start", "end"})
    start, end = value["start"], value["end"]
    _require(type(start) is int and type(end) is int and 0 <= start < end <= len(source), f"invalid {name}")


def _no_authority(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _require(str(key).casefold() not in _FORBIDDEN, f"candidate carries grading authority: {key}")
            _no_authority(item)
    elif isinstance(value, list):
        for item in value:
            _no_authority(item)


def fingerprint(value: Any) -> str:
    """Hash an immutable JSON snapshot with stable field ordering."""
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate_fact(value: Any) -> dict[str, Any]:
    _fields(value, {
        "schema_version", "fact_id", "topic_id", "statement", "relation",
        "source_refs", "review_status", "revision", "score_effect",
    }, {"legacy_anchor_id"})
    _require(value["schema_version"] == VERSION, "unsupported fact contract version")
    _id(value["fact_id"], "fact_id")
    _id(value["topic_id"], "topic_id")
    _string(value["statement"], "statement")
    _require(type(value["revision"]) is int and value["revision"] > 0, "invalid revision")
    _require(value["review_status"] in {"candidate", "approved", "conflict"}, "invalid review_status")
    _require(value["score_effect"] == "none", "facts cannot assign scores")
    relation = value["relation"]
    _fields(relation, {"subject", "predicate", "object", "conditions"})
    for key in ("subject", "predicate", "object"):
        _id(relation[key], key)
    _list_of_ids(relation["conditions"], "conditions")
    refs = value["source_refs"]
    _require(isinstance(refs, list) and bool(refs), "fact requires source_refs")
    seen: set[tuple[str, str]] = set()
    for ref in refs:
        _fields(ref, {"source_id", "source_version", "source_sha256", "locator"})
        _string(ref["source_id"], "source_id")
        _string(ref["source_version"], "source_version")
        _sha(ref["source_sha256"], "source_sha256")
        _string(ref["locator"], "locator")
        key = (ref["source_id"], ref["locator"])
        _require(key not in seen, "duplicate source reference")
        seen.add(key)
    if "legacy_anchor_id" in value:
        _id(value["legacy_anchor_id"], "legacy_anchor_id")
    return value


def validate_question_contract(value: Any, question_text: str, known_fact_ids: set[str]) -> dict[str, Any]:
    _fields(value, {"schema_version", "question_sha256", "knowledge_snapshot_sha256", "requirements", "score_effect"})
    _require(value["schema_version"] == VERSION and value["score_effect"] == "none", "invalid question contract")
    _require(value["question_sha256"] == hashlib.sha256(question_text.encode()).hexdigest(), "question hash mismatch")
    _sha(value["knowledge_snapshot_sha256"], "knowledge_snapshot_sha256")
    rows = value["requirements"]
    _require(isinstance(rows, list), "requirements must be an array")
    seen: set[str] = set()
    for row in rows:
        _fields(row, {"requirement_id", "source_span", "source_text", "task", "fact_refs", "resolution"})
        _id(row["requirement_id"], "requirement_id")
        _require(row["requirement_id"] not in seen, "duplicate requirement")
        seen.add(row["requirement_id"])
        _span(row["source_span"], question_text, "question span")
        _require(question_text[row["source_span"]["start"]:row["source_span"]["end"]] == row["source_text"], "question source text mismatch")
        _require(row["task"] in _TASKS, "unsupported question task")
        _list_of_ids(row["fact_refs"], "fact_refs")
        _require(row["resolution"] in {"resolved", "knowledge_gap", "ambiguous"}, "invalid question resolution")
        _require(set(row["fact_refs"]) <= known_fact_ids, "unknown fact reference")
        _require(row["resolution"] != "resolved" or bool(row["fact_refs"]), "resolved requirement lacks facts")
    return value


def validate_interpretation_candidate(value: Any, question_text: str, answer_text: str) -> dict[str, Any]:
    """Allow an LLM to propose only source-anchored meaning, never decisions."""
    _no_authority(value)
    _fields(value, {"schema_version", "candidate_id", "kind", "source_span", "source_text", "proposal", "producer", "score_effect"})
    _require(value["schema_version"] == VERSION and value["score_effect"] == "none", "invalid candidate contract")
    _id(value["candidate_id"], "candidate_id")
    _require(value["kind"] in {"question_requirement", "answer_claim"}, "invalid candidate kind")
    source = question_text if value["kind"] == "question_requirement" else answer_text
    _span(value["source_span"], source, "candidate span")
    _require(source[value["source_span"]["start"]:value["source_span"]["end"]] == value["source_text"], "candidate source text mismatch")
    _fields(value["producer"], {"mode", "resolver_id", "resolver_version"})
    _require(value["producer"]["mode"] in {"deterministic_parser", "semantic_resolver"}, "invalid producer mode")
    _id(value["producer"]["resolver_id"], "resolver_id")
    _string(value["producer"]["resolver_version"], "resolver_version")
    proposal = value["proposal"]
    if value["kind"] == "question_requirement":
        _fields(proposal, {"task", "target_concepts", "conditions"})
        _require(proposal["task"] in _TASKS, "invalid proposed task")
        _list_of_ids(proposal["target_concepts"], "target_concepts")
        _require(bool(proposal["target_concepts"]), "question proposal lacks target concepts")
    else:
        _fields(proposal, {"subject", "predicate", "object", "conditions", "polarity", "assertion_context"})
        for key in ("subject", "predicate", "object"):
            _id(proposal[key], key)
        _require(proposal["polarity"] in {"positive", "negative"}, "invalid polarity")
        _require(proposal["assertion_context"] in {"asserted", "quoted", "rejected", "corrected"}, "invalid assertion_context")
    _list_of_ids(proposal["conditions"], "conditions")
    return value


def build_evaluation_snapshot(
    *, facts: list[dict[str, Any]], question_contract: dict[str, Any],
    candidates: list[dict[str, Any]], ontology_sha256: str,
    rubric_source_sha256: str, scoring_policy_version: str,
    question_text: str, answer_text: str,
) -> dict[str, Any]:
    """Pin evaluated inputs without assigning status, score or verdict."""
    _sha(ontology_sha256, "ontology_sha256")
    _sha(rubric_source_sha256, "rubric_source_sha256")
    _string(scoring_policy_version, "scoring_policy_version")
    ids: set[str] = set()
    for fact in facts:
        validate_fact(fact)
        _require(fact["fact_id"] not in ids, "duplicate fact_id")
        ids.add(fact["fact_id"])
    facts_sha256 = fingerprint(sorted(facts, key=lambda row: row["fact_id"]))
    _require(
        question_contract.get("knowledge_snapshot_sha256") == facts_sha256,
        "question knowledge snapshot does not match facts",
    )
    approved = {row["fact_id"] for row in facts if row["review_status"] == "approved"}
    validate_question_contract(question_contract, question_text, approved)
    candidate_ids: set[str] = set()
    for candidate in candidates:
        validate_interpretation_candidate(candidate, question_text, answer_text)
        _require(candidate["candidate_id"] not in candidate_ids, "duplicate candidate_id")
        candidate_ids.add(candidate["candidate_id"])
    payload = {
        "schema_version": VERSION,
        "question_sha256": question_contract["question_sha256"],
        "answer_sha256": hashlib.sha256(answer_text.encode()).hexdigest(),
        "facts_sha256": facts_sha256,
        "question_contract_sha256": fingerprint(question_contract),
        "candidates_sha256": fingerprint(sorted(candidates, key=lambda row: row["candidate_id"])),
        "ontology_sha256": ontology_sha256,
        "rubric_source_sha256": rubric_source_sha256,
        "scoring_policy_version": scoring_policy_version,
        "approved_fact_ids": sorted(approved),
        "score_effect": "none",
    }
    payload["snapshot_sha256"] = fingerprint(payload)
    return payload


def legacy_anchor_index(repository_root: str | Path, topic_id: str) -> dict[str, Any]:
    """Read identity and file hash only; legacy prose is not a new approved fact."""
    _id(topic_id, "topic_id")
    root = Path(repository_root).resolve()
    path = (root / "rubrics" / "topic_packs" / topic_id / "fact_anchor.json").resolve()
    _require(path.is_relative_to(root) and path.is_file(), "missing legacy fact anchor")
    raw = path.read_bytes()
    payload = json.loads(raw)
    _require(payload.get("topic_id") == topic_id, "legacy topic_id mismatch")
    anchor_ids = [str(row.get("anchor_id") or row.get("id") or "") for row in payload.get("anchors", [])]
    for anchor_id in anchor_ids:
        _id(anchor_id, "legacy anchor id")
    _require(len(anchor_ids) == len(set(anchor_ids)), "duplicate legacy anchor id")
    return {
        "topic_id": topic_id,
        "source_path": path.relative_to(root).as_posix(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "anchor_ids": anchor_ids,
        "score_effect": "none",
    }


def validate_view_fact_refs(view_refs: Any, approved_fact_ids: set[str]) -> dict[str, list[str]]:
    """Require all three future projections to use the same approved Fact IDs."""
    _fields(view_refs, {"grading", "training", "diagnosis"})
    for name, refs in view_refs.items():
        _list_of_ids(refs, f"{name} fact refs")
        _require(set(refs) <= approved_fact_ids, f"{name} references an unapproved fact")
    return view_refs
