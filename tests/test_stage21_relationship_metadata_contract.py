from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import logic_check_evaluator as evaluator
from scripts.topic_pack_contract import validate_against_schema
from scripts.topic_pack_tool import render_topic


METADATA = {
    "error_class": "RELATIONSHIP_DIRECTION",
    "claim_signature": "A->B",
    "anchor_refs": ["anchor_direction"],
    "demand_refs": ["demand_explain_direction"],
}
METADATA_KEYS = tuple(METADATA)


def _load_json(relative_path: str) -> dict:
    return json.loads(
        (REPO_ROOT / relative_path).read_text(encoding="utf-8")
    )


def _minimal_spec(*, include_metadata: bool) -> dict:
    fatal = {
        "id": "fatal_relationship_direction",
        "claim": "A causes B.",
        "correct_rule": "B causes A.",
        "rationale": "The direction is reversed.",
        "keywords": ["direction", "relationship"],
    }
    if include_metadata:
        fatal.update(copy.deepcopy(METADATA))

    return {
        "$schema": "schemas/topic_pack_spec.schema.json",
        "schema_version": "topic-spec-v1",
        "profile_id": "implementation_evaluation_v1",
        "topic_id": "stage21_relationship_metadata",
        "title_ko": "관계 오류 메타데이터",
        "question_type": "IMPLEMENTATION_EVALUATION",
        "difficulty": "high",
        "selection_importance": "high",
        "scope_summary": "relationship metadata contract",
        "ownership_statements": [
            {
                "kind": "OWNED",
                "statement": "relationship metadata",
            }
        ],
        "counts": {
            "anchors": 1,
            "fatal_wrong_claims": 1,
            "major_checks": 1,
            "question_patterns": 1,
            "recommended_outline": 1,
            "routing_aliases": 1,
            "high_band_unlock_conditions": 1,
            "revision_notes": 1,
        },
        "anchors": [
            {
                "id": "anchor_direction",
                "title": "Direction",
                "content": "B causes A.",
                "keywords": ["direction"],
                "importance": "core",
            }
        ],
        "fatal_wrong_claims": [fatal],
        "major_checks": [
            {
                "id": "major_direction",
                "check": "direction",
                "expected": "B causes A.",
                "rationale": "direction",
                "keywords": ["direction"],
            }
        ],
        "question_patterns": [
            {
                "id": "pattern_direction",
                "pattern": "Explain direction.",
                "required_anchor_ids": ["anchor_direction"],
            }
        ],
        "recommended_outline": [
            {
                "section": "Direction",
                "purpose": "Explain",
                "anchor_ids": ["anchor_direction"],
            }
        ],
        "routing_aliases": ["relationship direction"],
        "high_band_unlock_conditions": ["Correct direction"],
        "revision_notes": ["Stage21"],
        "handoffs": [],
        "standards_and_sources": [],
        "expected_question_patterns": [
            {
                "pattern": "Explain direction.",
                "intent": "relationship",
            }
        ],
        "high_score_points": ["Correct direction"],
    }


def _bank_rule(*, include_metadata: bool) -> dict:
    rule = {
        "id": "fatal_relationship_direction",
        "severity": "fatal",
        "message": "Relationship direction is reversed.",
        "correct_rule": "B causes A.",
        "affected_layers": ["B", "C"],
        "recommended_ceiling": 10.0,
        "wrong_patterns": ["A causes B"],
    }
    if include_metadata:
        rule.update(copy.deepcopy(METADATA))
    return rule


def _evaluate_deterministic(*, include_metadata: bool) -> dict:
    topic_id = "stage21_relationship_metadata"
    bank = {
        "topic_logic_checks": [
            {
                "topic_id": topic_id,
                "topic_name": "Stage21 relationship metadata",
                "topic_aliases": ["stage21 relationship"],
                "enabled": True,
                "fatal_checks": [
                    _bank_rule(include_metadata=include_metadata)
                ],
                "major_checks": [],
                "question_type_checks": [],
                "next_practice_points": [],
            }
        ]
    }

    with tempfile.TemporaryDirectory() as temporary:
        bank_path = Path(temporary) / "logic_checks.json"
        bank_path.write_text(
            json.dumps(bank, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        result = evaluator.evaluate_logic_checks(
            "stage21 relationship: A causes B",
            grade={"topic_id": topic_id},
            bank_path=bank_path,
        )

    fatal = [
        finding
        for finding in result["findings"]
        if finding.get("severity") == "fatal"
    ]
    if len(fatal) != 1:
        raise AssertionError(f"unexpected fatal findings: {fatal!r}")
    return fatal[0]


class Stage21RelationshipMetadataContractTests(unittest.TestCase):
    def test_spec_schema_accepts_optional_metadata_and_legacy(self) -> None:
        schema = _load_json("schemas/topic_pack_spec.schema.json")

        metadata_issues = validate_against_schema(
            _minimal_spec(include_metadata=True),
            schema,
            code="TEST",
        )
        legacy_issues = validate_against_schema(
            _minimal_spec(include_metadata=False),
            schema,
            code="TEST",
        )

        self.assertEqual([], metadata_issues)
        self.assertEqual([], legacy_issues)

        item = (
            schema["properties"]["fatal_wrong_claims"]["items"]
        )
        for key in METADATA_KEYS:
            self.assertIn(key, item["properties"])
            self.assertNotIn(key, item["required"])

    def test_profile_projection_preserves_metadata_without_legacy_materialization(
        self,
    ) -> None:
        profile = _load_json(
            "rubrics/topic_profiles/implementation_evaluation_v1.json"
        )

        rendered = render_topic(
            _minimal_spec(include_metadata=True),
            profile,
        )
        fact_anchor = json.loads(rendered["fact_anchor.json"])
        logic_check = json.loads(rendered["logic_check.json"])

        metadata_row = fact_anchor["fatal_wrong_claims"][0]
        for key, value in METADATA.items():
            self.assertEqual(value, metadata_row[key])

        encoded_condition = (
            logic_check["llm_profile"]["fatal_conditions"][0]
        )
        decoded_condition = json.loads(encoded_condition)
        for key, value in METADATA.items():
            self.assertEqual(value, decoded_condition[key])

        legacy_rendered = render_topic(
            _minimal_spec(include_metadata=False),
            profile,
        )
        legacy_fact = json.loads(legacy_rendered["fact_anchor.json"])
        legacy_row = legacy_fact["fatal_wrong_claims"][0]
        for key in METADATA_KEYS:
            self.assertNotIn(key, legacy_row)

        fact_contract = profile["canonical_files"]["fact_anchor.json"]
        shape_template = fact_contract["template"][
            "fatal_wrong_claims"
        ][0]
        item_template = profile["canonical_items"][
            "fatal_wrong_claims"
        ]["item_template"]
        for key in METADATA_KEYS:
            self.assertNotIn(key, shape_template)
            self.assertNotIn(key, item_template)

    def test_source_metadata_overrides_untrusted_finding_values(self) -> None:
        finding = {
            "error_class": "MODEL_VALUE",
            "claim_signature": "MODEL_VALUE",
            "anchor_refs": ["model_anchor"],
            "demand_refs": ["model_demand"],
        }
        source = copy.deepcopy(METADATA)

        returned = evaluator._copy_optional_fatal_rule_metadata(
            finding,
            source,
        )

        self.assertIs(returned, finding)
        for key, value in METADATA.items():
            self.assertEqual(value, finding[key])

    def test_deterministic_fatal_finding_copies_metadata(self) -> None:
        finding = _evaluate_deterministic(include_metadata=True)
        for key, value in METADATA.items():
            self.assertEqual(value, finding[key])

    def test_legacy_deterministic_finding_omits_metadata(self) -> None:
        finding = _evaluate_deterministic(include_metadata=False)
        for key in METADATA_KEYS:
            self.assertNotIn(key, finding)


if __name__ == "__main__":
    unittest.main()
