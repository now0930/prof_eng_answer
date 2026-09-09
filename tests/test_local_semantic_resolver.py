import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from local_semantic_resolver import resolve_with_optional_local_semantics


class LocalSemanticResolverTests(unittest.TestCase):
    def test_resolved_deterministic_claim_does_not_call_local_model(self):
        calls = []
        result = resolve_with_optional_local_semantics(
            question_text="차원을 검토하시오.",
            answer_text="lambda < PFDavg로 설계한다.",
            semantic_call=lambda prompt: calls.append(prompt),
        )
        self.assertEqual(calls, [])
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["llm_verdict_authority"], 0)

    def test_unresolved_span_can_add_only_canonical_evidence(self):
        answer = "PFDavg는 저수요 모드와 관련된다."
        start, end = 0, len(answer)

        def fake_call(prompt):
            self.assertIn("Do not output score", prompt)
            return {"claims": [{
                "subject": "pfdavg",
                "predicate": "applies_to",
                "object": "low_demand",
                "conditions": [],
                "assertion_context": "asserted",
                "source_text": answer,
                "source_span": {"start": start, "end": end},
            }]}

        result = resolve_with_optional_local_semantics(
            question_text="요구모드별 지표를 설명하시오.",
            answer_text=answer,
            semantic_call=fake_call,
        )
        self.assertEqual(result["status"], "semantic_evidence_added")
        self.assertEqual(result["provider_calls"], 1)
        semantic = result["evidence_documents"][1]
        self.assertEqual(semantic["authority"], "evidence_only")
        self.assertNotIn("verdict", semantic)

    def test_authority_fields_from_model_are_rejected_fail_closed(self):
        answer = "PFDavg는 저수요 모드와 관련된다."
        result = resolve_with_optional_local_semantics(
            question_text="요구모드별 지표를 설명하시오.",
            answer_text=answer,
            semantic_call=lambda _prompt: {
                "claims": [{
                    "subject": "pfdavg",
                    "predicate": "applies_to",
                    "object": "low_demand",
                    "conditions": [],
                    "assertion_context": "asserted",
                    "source_text": answer,
                    "source_span": {"start": 0, "end": len(answer)},
                    "verdict": "satisfied",
                }]
            },
        )
        self.assertEqual(result["status"], "semantic_resolver_failed")
        self.assertEqual(len(result["evidence_documents"]), 1)
        self.assertEqual(result["llm_verdict_authority"], 0)

    def test_model_failure_preserves_deterministic_result(self):
        answer = "PFDavg를 검토한다."

        def fail(_prompt):
            raise RuntimeError("local model unavailable")

        first = resolve_with_optional_local_semantics(
            question_text="검토하시오.", answer_text=answer, semantic_call=None
        )
        failed = resolve_with_optional_local_semantics(
            question_text="검토하시오.", answer_text=answer, semantic_call=fail
        )
        self.assertEqual(
            first["evidence_documents"][0],
            failed["evidence_documents"][0],
        )
        self.assertEqual(failed["status"], "semantic_resolver_failed")

    def test_semantic_claim_without_discourse_context_is_rejected(self):
        answer = "PFDavg는 저수요 모드와 관련된다."
        result = resolve_with_optional_local_semantics(
            question_text="요구모드별 지표를 설명하시오.",
            answer_text=answer,
            semantic_call=lambda _prompt: {"claims": [{
                "subject": "pfdavg",
                "predicate": "applies_to",
                "object": "low_demand",
                "source_text": answer,
                "source_span": {"start": 0, "end": len(answer)},
            }]},
        )
        self.assertEqual(result["status"], "semantic_resolver_failed")
        self.assertEqual(result["provider_calls"], 1)


if __name__ == "__main__":
    unittest.main()
