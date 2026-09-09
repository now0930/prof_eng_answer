import unittest

from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from topic_machine_contract import TopicMachineContractError, validate_topic_machine_contract


class MachineContractContradictionPolicyTests(unittest.TestCase):
    def test_relation_conflict_can_own_deterministic_fatal(self):
        result = evaluate_deterministic_requirements(
            claims=[{
                "claim_id": "wrong_nyquist_point",
                "subject": "nyquist_critical_point",
                "predicate": "equivalent_to",
                "object": "origin_point",
                "polarity": "positive",
                "assertion_context": "asserted",
            }],
            invariant_codes=[],
            topic_ids=["nyquist_stability_criterion_gain_phase_margin"],
            extraction_complete=True,
        )
        self.assertTrue(result["fatal_or_core_error"])
        self.assertEqual(result["requirements"][0]["status"], "WRONG")
        self.assertEqual(
            result["findings"][0]["invariant_code"],
            "MACHINE_CONTRACT_RELATION_CONTRADICTION",
        )

    def test_partial_contradiction_policy_is_rejected(self):
        contract = {
            "schema_version": "topic_machine_contract_v1",
            "owner_topic_id": "sample_topic",
            "authority": "deterministic_topic_contract",
            "score_effect": "downstream_deterministic_only",
            "facts": [{
                "fact_id": "a_controls_b", "subject": "a",
                "predicate": "controls", "object": "b", "polarity": "positive",
            }],
            "requirement_rules": [{
                "requirement_id": "relation", "required_fact_ids": ["a_controls_b"],
                "minimum_match_count": 1,
                "contradiction_rule_id": "sample_fatal",
            }],
            "invariant_bindings": [],
        }
        with self.assertRaises(TopicMachineContractError):
            validate_topic_machine_contract(contract, topic_id="sample_topic")


if __name__ == "__main__":
    unittest.main()
