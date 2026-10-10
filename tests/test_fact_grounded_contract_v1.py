"""Stage 1: score-neutral, source-anchored evaluation inputs."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from grading.evidence.fact_grounded_contracts import (
    VERSION,
    FactGroundedContractError,
    build_evaluation_snapshot,
    fingerprint,
    legacy_anchor_index,
    validate_fact,
    validate_interpretation_candidate,
    validate_question_contract,
    validate_view_fact_refs,
)


ROOT = Path(__file__).resolve().parents[1]
QUESTION = "SIL 목표 결정 방법을 설명하라."
ANSWER = "LOPA는 위험감소 요구를 결정한다."


def fact(status: str = "approved") -> dict:
    return {
        "schema_version": VERSION,
        "fact_id": "risk_reduction",
        "topic_id": "hazop_lopa_ipl_risk_reduction_sil_target_allocation",
        "statement": "LOPA는 시나리오별 요구 위험감소를 결정한다.",
        "relation": {
            "subject": "lopa", "predicate": "determines", "object": "risk_reduction",
            "conditions": ["scenario_boundary"],
        },
        "source_refs": [{
            "source_id": "fixture_wp_1", "source_version": "1",
            "source_sha256": "a" * 64, "locator": "post:1#section:2",
        }],
        "review_status": status, "revision": 1, "score_effect": "none",
    }


def question(facts: list[dict]) -> dict:
    return {
        "schema_version": VERSION,
        "question_sha256": hashlib.sha256(QUESTION.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint(sorted(facts, key=lambda row: row["fact_id"])),
        "requirements": [{
            "requirement_id": "sil_method", "source_span": {"start": 0, "end": len(QUESTION)},
            "source_text": QUESTION, "task": "explain", "fact_refs": ["risk_reduction"],
            "resolution": "resolved",
        }],
        "score_effect": "none",
    }


def candidate() -> dict:
    return {
        "schema_version": VERSION, "candidate_id": "answer_1", "kind": "answer_claim",
        "source_span": {"start": 0, "end": len(ANSWER)}, "source_text": ANSWER,
        "proposal": {
            "subject": "lopa", "predicate": "determines", "object": "risk_reduction",
            "conditions": [], "polarity": "positive", "assertion_context": "asserted",
        },
        "producer": {"mode": "semantic_resolver", "resolver_id": "fixture", "resolver_version": "1"},
        "score_effect": "none",
    }


class FactGroundedContractTests(unittest.TestCase):
    def test_schema_catalog_has_strict_root_and_all_records(self) -> None:
        schema = json.loads((ROOT / "schemas/fact_grounded_contract_v1.schema.json").read_text())
        self.assertEqual(len(schema["oneOf"]), 4)
        for name in ("fact", "question_contract", "candidate", "snapshot"):
            self.assertFalse(schema["$defs"][name]["additionalProperties"])

    def test_fact_is_score_neutral_and_versioned(self) -> None:
        self.assertEqual(validate_fact(fact())["review_status"], "approved")
        invalid = fact()
        invalid["fatal"] = True
        with self.assertRaises(FactGroundedContractError):
            validate_fact(invalid)
        invalid = fact()
        invalid["source_refs"][0]["source_sha256"] = "stale"
        with self.assertRaises(FactGroundedContractError):
            validate_fact(invalid)

    def test_question_can_reference_only_approved_facts_in_snapshot(self) -> None:
        approved = [fact()]
        self.assertEqual(validate_question_contract(question(approved), QUESTION, {"risk_reduction"})["score_effect"], "none")
        with self.assertRaisesRegex(FactGroundedContractError, "unknown fact reference"):
            build_evaluation_snapshot(
                facts=[fact("candidate")], question_contract=question([fact("candidate")]),
                candidates=[], ontology_sha256="b" * 64, rubric_source_sha256="c" * 64,
                scoring_policy_version="v1", question_text=QUESTION, answer_text=ANSWER,
            )

    def test_candidate_requires_exact_span_and_cannot_claim_authority(self) -> None:
        self.assertEqual(validate_interpretation_candidate(candidate(), QUESTION, ANSWER)["candidate_id"], "answer_1")
        for key, value in (("score", 25), ("fatal", True), ("status", "SATISFIED")):
            invalid = candidate()
            invalid["proposal"][key] = value
            with self.subTest(key=key), self.assertRaises(FactGroundedContractError):
                validate_interpretation_candidate(invalid, QUESTION, ANSWER)
        invalid = candidate()
        invalid["source_text"] = "원문에 없는 문장"
        with self.assertRaisesRegex(FactGroundedContractError, "source text mismatch"):
            validate_interpretation_candidate(invalid, QUESTION, ANSWER)

    def test_snapshot_is_stable_and_mismatched_knowledge_is_rejected(self) -> None:
        rows = [fact()]
        contract = question(rows)
        args = dict(
            facts=rows, question_contract=contract, candidates=[candidate()],
            ontology_sha256="b" * 64, rubric_source_sha256="c" * 64,
            scoring_policy_version="v1", question_text=QUESTION, answer_text=ANSWER,
        )
        first = build_evaluation_snapshot(**args)
        self.assertEqual(first, build_evaluation_snapshot(**args))
        changed = copy.deepcopy(rows)
        changed[0]["source_refs"][0]["source_sha256"] = "d" * 64
        with self.assertRaisesRegex(FactGroundedContractError, "knowledge snapshot"):
            build_evaluation_snapshot(**{**args, "facts": changed})
        changed_contract = question(changed)
        second = build_evaluation_snapshot(**{**args, "facts": changed, "question_contract": changed_contract})
        self.assertNotEqual(first["snapshot_sha256"], second["snapshot_sha256"])

    def test_legacy_adapter_reads_ids_only(self) -> None:
        entry = legacy_anchor_index(ROOT, "hazop_lopa_ipl_risk_reduction_sil_target_allocation")
        self.assertTrue(entry["anchor_ids"])
        self.assertEqual(entry["score_effect"], "none")
        self.assertNotIn("statement", entry)

    def test_three_views_share_approved_fact_identity(self) -> None:
        refs = {"grading": ["risk_reduction"], "training": ["risk_reduction"], "diagnosis": []}
        self.assertIs(validate_view_fact_refs(refs, {"risk_reduction"}), refs)
        refs["diagnosis"] = ["unreviewed_fact"]
        with self.assertRaisesRegex(FactGroundedContractError, "unapproved fact"):
            validate_view_fact_refs(refs, {"risk_reduction"})


if __name__ == "__main__":
    unittest.main()
