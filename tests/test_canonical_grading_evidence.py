import copy
import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from canonical_grading_evidence import (
    CanonicalEvidenceError,
    build_canonical_grading_evidence,
    validate_canonical_grading_evidence,
)


ANSWER = "저수요 모드에서는 PFDavg를 적용한다."
QUOTE = "PFDavg를 적용한다"
START = ANSWER.index(QUOTE)


def sample_claim():
    return {
        "subject": "pfdavg",
        "predicate": "applies_to",
        "object": "low_demand",
        "polarity": "positive",
        "source_text": QUOTE,
        "source_span": {"start": START, "end": START + len(QUOTE)},
        "requirement_refs": ["demand_mode_metric_selection"],
        "qualifiers": {},
        "extraction_confidence": 1,
    }


class CanonicalGradingEvidenceTests(unittest.TestCase):
    def build(self, *, source_mode="deterministic_parser", claims=None):
        return build_canonical_grading_evidence(
            question_text="SIL 결정 방법을 설명하시오.",
            answer_text=ANSWER,
            source={
                "mode": source_mode,
                "resolver_id": "test_resolver",
                "resolver_version": "1",
            },
            claims=claims if claims is not None else [sample_claim()],
        )

    def test_builds_traceable_evidence_without_grading_authority(self):
        evidence = self.build()
        self.assertEqual(evidence["authority"], "evidence_only")
        self.assertEqual(evidence["score_effect"], "none")
        self.assertEqual(evidence["claims"][0]["subject"], "pfdavg")
        validate_canonical_grading_evidence(evidence, answer_text=ANSWER)

    def test_semantic_resolver_has_same_evidence_contract(self):
        evidence = self.build(source_mode="semantic_resolver")
        self.assertEqual(evidence["source"]["mode"], "semantic_resolver")
        self.assertNotIn("provider", json.dumps(evidence, ensure_ascii=False))

    def test_input_order_does_not_change_canonical_document(self):
        second_quote = "저수요 모드"
        second = {
            "subject": "pfdavg",
            "predicate": "used_in",
            "object": "low_demand",
            "source_text": second_quote,
            "source_span": {"start": 0, "end": len(second_quote)},
        }
        left = self.build(claims=[sample_claim(), second])
        right = self.build(claims=[second, sample_claim()])
        self.assertEqual(left, right)

    def test_rejects_verdict_score_and_fatal_fields_at_any_depth(self):
        for key, value in (
            ("verdict", "satisfied"),
            ("score", 25),
            ("fatal", False),
            ("demand_state", "correct"),
        ):
            claim = sample_claim()
            claim["qualifiers"] = {"nested": {key: value}}
            with self.subTest(key=key), self.assertRaises(CanonicalEvidenceError):
                self.build(claims=[claim])

    def test_rejects_untraceable_or_mutated_source_quote(self):
        claim = sample_claim()
        claim["source_text"] = "PFDavg는 시간당 고장률이다"
        with self.assertRaises(CanonicalEvidenceError):
            self.build(claims=[claim])

        evidence = self.build()
        mutated = copy.deepcopy(evidence)
        mutated["claims"][0]["object"] = "high_demand"
        with self.assertRaises(CanonicalEvidenceError):
            validate_canonical_grading_evidence(mutated, answer_text=ANSWER)

    def test_schema_forbids_additional_authority_fields(self):
        schema = json.loads(
            (REPO / "schemas/canonical_grading_evidence_v1.schema.json")
            .read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["properties"]["claims"]["items"]["additionalProperties"])
        properties = schema["properties"]["claims"]["items"]["properties"]
        self.assertTrue({"score", "verdict", "fatal", "status"}.isdisjoint(properties))

    def test_stage35b_does_not_enter_production_scoring(self):
        production = (REPO / "grading_agents.py").read_text(encoding="utf-8")
        self.assertNotIn("canonical_grading_evidence", production)


if __name__ == "__main__":
    unittest.main()
