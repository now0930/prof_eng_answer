from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.topic_pack_contract import (
    COUNT_FIELDS,
    ERROR_CODES,
    PROFILE_SCHEMA_PATH,
    SPEC_SCHEMA_PATH,
    issue_codes,
    load_json,
    load_profile,
    validate_profile,
    validate_spec,
)


class TopicPackContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec_schema = load_json(SPEC_SCHEMA_PATH)
        cls.profile_schema = load_json(PROFILE_SCHEMA_PATH)
        cls.profile = load_profile("implementation_evaluation_v1")

    def make_spec(self) -> dict:
        return {
            "$schema": "../../schemas/topic_pack_spec.schema.json",
            "schema_version": "topic-spec-v1",
            "profile_id": "implementation_evaluation_v1",
            "topic_id": "example_compiler_managed_topic",
            "title_ko": "컴파일러 관리 예제 토픽",
            "question_type": "IMPLEMENTATION_EVALUATION",
            "difficulty": "HIGH",
            "selection_importance": "HIGH",
            "scope_summary": "예제 토픽의 기술 범위와 평가 기준을 정의한다.",
            "ownership_statements": [
                {
                    "kind": "OWNED",
                    "statement": "예제 토픽의 핵심 기술 판단을 소유한다.",
                },
                {
                    "kind": "EXCLUDED",
                    "statement": "인접 토픽의 상세 설계는 소유하지 않는다.",
                },
            ],
            "counts": {
                "anchors": 2,
                "fatal_wrong_claims": 1,
                "major_checks": 1,
                "question_patterns": 1,
                "recommended_outline": 1,
                "routing_aliases": 2,
                "high_band_unlock_conditions": 1,
                "revision_notes": 1,
            },
            "anchors": [
                {
                    "id": "definition",
                    "title": "정의",
                    "content": "핵심 개념을 조건과 함께 정의한다.",
                    "keywords": ["정의", "조건"],
                    "importance": "core",
                },
                {
                    "id": "application",
                    "title": "적용",
                    "content": "설계 및 검토 단계의 적용 판단을 설명한다.",
                    "keywords": ["적용", "검토"],
                    "importance": "core",
                },
            ],
            "fatal_wrong_claims": [
                {
                    "id": "fatal_reversal",
                    "claim": "핵심 인과관계를 반대로 설명한다.",
                    "correct_rule": "원인과 결과의 방향을 유지해야 한다.",
                    "rationale": "반대 설명은 기술 판단을 무효화한다.",
                    "keywords": ["반전", "오류"],
                }
            ],
            "major_checks": [
                {
                    "id": "major_boundary",
                    "check": "적용 조건과 제외 조건을 구분했는가.",
                    "expected": "조건과 경계를 함께 제시한다.",
                    "rationale": "경계가 없으면 과도한 일반화가 발생한다.",
                    "keywords": ["조건", "경계"],
                }
            ],
            "question_patterns": [
                {
                    "id": "pattern_explain_apply",
                    "pattern": "원리와 적용 방법을 설명하라.",
                    "required_anchor_ids": ["definition", "application"],
                }
            ],
            "recommended_outline": [
                {
                    "section": "정의·원리·적용",
                    "purpose": "핵심 개념에서 현장 판단으로 전개한다.",
                    "anchor_ids": ["definition", "application"],
                }
            ],
            "routing_aliases": [
                "compiler managed example",
                "topic compiler example",
            ],
            "high_band_unlock_conditions": [
                "조건과 적용 한계를 함께 설명한다."
            ],
            "revision_notes": [
                "topic-spec-v1 acceptance fixture"
            ],
            "handoffs": [
                {
                    "topic_id": "existing_handoff_topic",
                    "trigger": "인접 토픽의 상세 판단이 요구될 때",
                    "scope": "상세 판단만 인접 토픽으로 이관한다.",
                }
            ],
            "standards_and_sources": [
                {
                    "reference": "Internal acceptance fixture",
                    "edition": "v1",
                    "relevance": "계약 검증용 데이터",
                }
            ],

            "expected_question_patterns": [{"pattern": "Topic Pack plan 계약을 설명하라.", "intent": "Topic Pack plan의 입력 계약, projection 결과, 검증 및 rollback 경계를 설명한다."}],
            "high_score_points": ["핵심 채점 포인트를 구조, 검증, 운영 경계와 함께 설명한다."],}

    def make_topic_root(self, root: Path) -> Path:
        topic_root = root / "rubrics" / "topic_packs"
        (topic_root / "existing_handoff_topic").mkdir(
            parents=True,
            exist_ok=True,
        )
        return topic_root

    def test_schema_and_profile_are_valid(self) -> None:
        self.assertEqual(
            self.spec_schema["$id"],
            "https://prof-eng-answer.local/schemas/topic_pack_spec.schema.json",
        )
        self.assertEqual(
            self.profile_schema["$id"],
            "https://prof-eng-answer.local/schemas/topic_pack_profile.schema.json",
        )
        self.assertEqual(validate_profile(self.profile), [])
        self.assertEqual(
            self.profile["profile_id"],
            "implementation_evaluation_v1",
        )
        self.assertFalse(
            self.profile["policies"]["runtime_donor_dependency"]
        )

    def test_positive_spec_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                self.make_spec(),
                self.profile,
                topic_root=topic_root,
            )
        self.assertEqual(issues, [])

    def test_spec_schema_error_is_structured(self) -> None:
        spec = self.make_spec()
        spec["topic_id"] = "BAD-ID"
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )
        self.assertIn(
            "TP001_SPEC_SCHEMA_INVALID",
            issue_codes(issues),
        )

    def test_count_mismatch_is_detected(self) -> None:
        spec = self.make_spec()
        spec["counts"]["anchors"] = 3
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )
        self.assertIn("TP004_COUNT_MISMATCH", issue_codes(issues))

    def test_anchor_reference_is_checked(self) -> None:
        spec = self.make_spec()
        spec["recommended_outline"][0]["anchor_ids"] = [
            "missing_anchor"
        ]
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )
        self.assertIn(
            "TP005_ANCHOR_REFERENCE_INVALID",
            issue_codes(issues),
        )

    def test_handoff_destination_is_checked(self) -> None:
        spec = self.make_spec()
        spec["handoffs"][0]["topic_id"] = "missing_handoff_topic"
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )
        self.assertIn(
            "TP006_HANDOFF_DESTINATION_INVALID",
            issue_codes(issues),
        )

    def test_topic_and_alias_collisions_are_checked(self) -> None:
        spec = self.make_spec()
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            (topic_root / spec["topic_id"]).mkdir(parents=True)
            owner = topic_root / "alias_owner_topic"
            owner.mkdir()
            (owner / "model_answer.json").write_text(
                json.dumps(
                    {
                        "routing_aliases": [
                            spec["routing_aliases"][0]
                        ]
                    }
                ),
                encoding="utf-8",
            )
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )

        codes = issue_codes(issues)
        self.assertIn("TP003_TOPIC_ID_COLLISION", codes)
        self.assertIn("TP007_ALIAS_COLLISION", codes)

    def test_profile_mismatch_is_detected(self) -> None:
        spec = self.make_spec()
        spec["profile_id"] = "other_profile_v1"
        with tempfile.TemporaryDirectory() as temporary:
            topic_root = self.make_topic_root(Path(temporary))
            issues = validate_spec(
                spec,
                self.profile,
                topic_root=topic_root,
            )
        self.assertIn("TP002_PROFILE_NOT_FOUND", issue_codes(issues))

    def test_error_registry_and_count_fields_are_stable(self) -> None:
        self.assertEqual(len(ERROR_CODES), 16)
        self.assertEqual(len(set(ERROR_CODES)), 16)
        self.assertEqual(
            tuple(self.profile["content_contract"]["count_fields"]),
            COUNT_FIELDS,
        )
        profile_codes = {
            item["error_code"]
            for item in self.profile["error_codes"]
        }
        self.assertEqual(profile_codes, set(ERROR_CODES))

    def test_profile_rejects_runtime_donor_dependency(self) -> None:
        invalid = copy.deepcopy(self.profile)
        invalid["policies"]["runtime_donor_dependency"] = True
        self.assertIn(
            "TP009_FORBIDDEN_RESIDUE",
            issue_codes(validate_profile(invalid)),
        )


# STAGE17C4_IMPORTANCE_CONTRACT_TESTS_V1
import json as _stage17c4_json
import unittest as _stage17c4_unittest
from pathlib import Path as _Stage17C4Path


class Stage17C4ImportanceContractTests(_stage17c4_unittest.TestCase):
    _allowed = ["core", "must", "important"]

    @staticmethod
    def _resolve(root, node):
        seen = set()
        while isinstance(node, dict) and "$ref" in node:
            ref = node["$ref"]
            if not ref.startswith("#/") or ref in seen:
                raise AssertionError(f"invalid local ref: {ref}")
            seen.add(ref)
            current = root
            for token in ref[2:].split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                current = current[int(token)] if isinstance(current, list) else current[token]
            node = current
        return node

    def test_spec_anchor_importance_is_required_enum(self):
        root = _Stage17C4Path(__file__).resolve().parents[1]
        schema = _stage17c4_json.loads(
            (root / "schemas/topic_pack_spec.schema.json").read_text(encoding="utf-8")
        )
        anchors = self._resolve(schema, schema["properties"]["anchors"])
        item = self._resolve(schema, anchors["items"])
        self.assertIn("importance", item["required"])
        self.assertEqual(
            item["properties"]["importance"],
            {"type": "string", "enum": self._allowed},
        )

    def test_profile_anchor_importance_is_required_enum(self):
        root = _Stage17C4Path(__file__).resolve().parents[1]
        profile = _stage17c4_json.loads(
            (
                root
                / "rubrics/topic_profiles/implementation_evaluation_v1.json"
            ).read_text(encoding="utf-8")
        )
        shape = profile["canonical_files"]["fact_anchor.json"]["shape_schema"]
        anchors = self._resolve(shape, shape["properties"]["anchors"])
        item = self._resolve(shape, anchors["items"])
        self.assertIn("importance", item["required"])
        self.assertEqual(
            item["properties"]["importance"],
            {"type": "string", "enum": self._allowed},
        )

if __name__ == "__main__":
    unittest.main()
