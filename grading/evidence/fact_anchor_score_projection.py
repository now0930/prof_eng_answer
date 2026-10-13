"""Opt-in shadow projection of independently verified Fact evidence to Anchor rows.

This adapter never consumes raw LLM agreement. The caller supplies reviewed
source-anchored evidence; the existing deterministic score engine remains owner.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .fact_grounded_contracts import (
    FactGroundedContractError, fingerprint, validate_fact, validate_question_contract,
)
from grading.scoring.deterministic_score_engine import calculate_deterministic_score


def project_verified_fact_evidence(*, question_text: str, answer_text: str,
                                   facts: list[dict[str, Any]], question_contract: dict[str, Any],
                                   requirement_evaluation: dict[str, Any],
                                   reviewed_evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """Promote only scoped, separately reviewed Fact evidence; never override WRONG."""
    by_id = {}
    for fact in facts:
        validate_fact(fact)
        if fact["fact_id"] in by_id:
            raise FactGroundedContractError("duplicate Fact ID")
        by_id[fact["fact_id"]] = fact
    if question_contract.get("knowledge_snapshot_sha256") != fingerprint(
        sorted(facts, key=lambda row: row["fact_id"])
    ):
        raise FactGroundedContractError("stale question Fact snapshot")
    approved = {fid for fid, fact in by_id.items() if fact["review_status"] == "approved"}
    validate_question_contract(question_contract, question_text, approved)
    scoped = {fid for requirement in question_contract["requirements"]
              if requirement["resolution"] == "resolved" for fid in requirement["fact_refs"]}
    output = deepcopy(requirement_evaluation)
    rows = output.get("requirements")
    if not isinstance(rows, list) or not isinstance(reviewed_evidence, list):
        raise FactGroundedContractError("invalid projection inputs")
    by_anchor = {(row.get("owner_topic_id"), row.get("requirement_id")): row for row in rows}
    anchor_fact_ids: dict[tuple[str, str], set[str]] = {}
    for fid, fact in by_id.items():
        if fact["review_status"] != "approved":
            continue
        if fact.get("legacy_anchor_id"):
            anchor_fact_ids.setdefault((fact["topic_id"], fact["legacy_anchor_id"]), set()).add(fid)
    promoted = []
    skipped = []
    seen = set()
    verified_by_anchor: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for evidence in reviewed_evidence:
        required = {"fact_id", "source_span", "source_text", "reviewer_id",
                    "verification_mode", "knowledge_snapshot_sha256"}
        if not isinstance(evidence, dict) or set(evidence) != required:
            raise FactGroundedContractError("invalid reviewed evidence fields")
        fid = evidence["fact_id"]
        if not isinstance(fid, str) or fid not in scoped or fid in seen:
            raise FactGroundedContractError("unscoped or duplicate reviewed Fact")
        seen.add(fid)
        fact = by_id[fid]
        if fact.get("verification_status") != "verified":
            raise FactGroundedContractError("Fact has no independent verification")
        if (evidence["knowledge_snapshot_sha256"]
                != question_contract["knowledge_snapshot_sha256"]):
            raise FactGroundedContractError("review references stale knowledge")
        if evidence["verification_mode"] not in {"human_review", "deterministic_entailment"}:
            raise FactGroundedContractError("LLM agreement is not verified evidence")
        if not isinstance(evidence["reviewer_id"], str) or not evidence["reviewer_id"].strip():
            raise FactGroundedContractError("reviewer identity missing")
        span = evidence["source_span"]
        if (not isinstance(span, dict) or set(span) != {"start", "end"}
                or type(span["start"]) is not int or type(span["end"]) is not int
                or not 0 <= span["start"] < span["end"] <= len(answer_text)
                or answer_text[span["start"]:span["end"]] != evidence["source_text"]):
            raise FactGroundedContractError("review quote mismatch")
        key = (fact["topic_id"], fact.get("legacy_anchor_id"))
        anchor = by_anchor.get(key)
        if anchor is None or not key[1]:
            skipped.append({"fact_id": fid, "reason": "no_scored_anchor"})
            continue
        if anchor.get("status") == "WRONG" or output.get("fatal_or_core_error"):
            skipped.append({"fact_id": fid, "reason": "contradiction_or_fatal_preserved"})
            continue
        if anchor.get("status") not in {"MISSING", "PARTIAL", "UNKNOWN", "SATISFIED"}:
            raise FactGroundedContractError("unknown Anchor status")
        verified_by_anchor.setdefault(key, []).append(evidence)
    for key, evidence_rows in verified_by_anchor.items():
        anchor = by_anchor[key]
        if anchor["status"] == "SATISFIED":
            skipped.extend({"fact_id": row["fact_id"], "reason": "already_satisfied"}
                           for row in evidence_rows)
            continue
        if {row["fact_id"] for row in evidence_rows} != anchor_fact_ids[key]:
            skipped.extend({"fact_id": row["fact_id"], "reason": "anchor_fact_group_incomplete"}
                           for row in evidence_rows)
            continue
        anchor["status"] = "SATISFIED"
        anchor["evidence_mode"] = "reviewed_fact_projection"
        anchor["evidence_text"] = "\n".join(row["source_text"] for row in evidence_rows)
        anchor["source_span"] = dict(evidence_rows[0]["source_span"])
        anchor["matched_fact_ids"] = sorted(row["fact_id"] for row in evidence_rows)
        promoted.append({"fact_ids": anchor["matched_fact_ids"],
                         "owner_topic_id": key[0], "requirement_id": key[1]})
    output["summary"] = {status: sum(row.get("status") == status for row in rows)
                         for status in ("SATISFIED", "PARTIAL", "WRONG", "MISSING", "UNKNOWN")}
    return {"requirement_evaluation": output, "promoted": promoted,
            "skipped": skipped, "score_effect": "shadow_only"}


def calculate_shadow_score(*, answer_text: str, projection: dict[str, Any]) -> dict[str, Any]:
    """Call the existing score owner; never relabel ABSTAIN as a final grade."""
    if projection.get("score_effect") != "shadow_only":
        raise FactGroundedContractError("invalid shadow score projection")
    score = calculate_deterministic_score(
        projection["requirement_evaluation"], answer_text=answer_text,
    )
    return {"score": score, "final_grade_allowed": False,
            "production_score_changed": False, "score_effect": "shadow_only"}
