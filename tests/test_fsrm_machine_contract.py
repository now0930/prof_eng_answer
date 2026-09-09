import json
import copy
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from topic_machine_contract import extract_fatal_rule_ids, validate_topic_machine_contract


TOPIC_ID = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"


class FsrmMachineContractTests(unittest.TestCase):
    def test_fatal_id_extraction_supports_dict_and_bracket_shapes(self):
        self.assertEqual(
            extract_fatal_rule_ids([{"id": "fatal_dict"}, "[fatal_string] text"]),
            {"fatal_dict", "fatal_string"},
        )

    @classmethod
    def setUpClass(cls):
        cls.logic = json.loads(
            (REPO / "rubrics/topic_packs" / TOPIC_ID / "logic_check.json")
            .read_text(encoding="utf-8")
        )
        cls.contract = cls.logic["machine_contract"]

    def test_contract_is_valid_and_reuses_existing_fatal_rule(self):
        fatal_ids = {
            row.split("]", 1)[0].lstrip("[")
            for row in self.logic["llm_profile"]["fatal_conditions"]
        }
        validated = validate_topic_machine_contract(
            self.contract,
            topic_id=TOPIC_ID,
            known_rule_ids=fatal_ids,
        )
        binding = validated["invariant_bindings"][0]
        self.assertEqual(binding["invariant_code"], "DIMENSIONALLY_INVALID_COMPARISON")
        self.assertEqual(binding["rule_id"], "failure_rate_compared_directly_to_pfd")
        self.assertEqual(binding["classification"], "fatal")

    def test_global_dimensions_are_not_duplicated_in_topic_contract(self):
        def keys(value):
            if isinstance(value, dict):
                for key, nested in value.items():
                    yield key
                    yield from keys(nested)
            elif isinstance(value, list):
                for nested in value:
                    yield from keys(nested)
        self.assertNotIn("dimension", set(keys(self.contract)))

    def test_demand_mode_relations_and_dimension_mutation_are_explicit(self):
        facts = {
            (row["subject"], row["predicate"], row["object"], row["polarity"])
            for row in self.contract["facts"]
        }
        self.assertIn(("pfdavg", "applies_to", "low_demand", "positive"), facts)
        self.assertIn(("pfh", "applies_to", "high_demand", "positive"), facts)
        self.assertIn(("pfh", "applies_to", "continuous_demand", "positive"), facts)
        self.assertIn(("pfdavg", "equivalent_to", "failure_rate", "negative"), facts)

    def test_optional_fact_conditions_are_machine_readable(self):
        contract = copy.deepcopy(self.contract)
        contract["facts"][0]["conditions"] = ["low_demand"]
        validated = validate_topic_machine_contract(
            contract,
            topic_id=TOPIC_ID,
            known_rule_ids={"failure_rate_compared_directly_to_pfd"},
        )
        self.assertEqual(validated["facts"][0]["conditions"], ["low_demand"])

    def test_machine_contract_is_additive_and_consumed_by_primary_extractor(self):
        production = (REPO / "deterministic_primary_grader.py").read_text(encoding="utf-8")
        self.assertIn("extract_canonical_claim_evidence", production)
        self.assertEqual(self.contract["score_effect"], "downstream_deterministic_only")


if __name__ == "__main__":
    unittest.main()
