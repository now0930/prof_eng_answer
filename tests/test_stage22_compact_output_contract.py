from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "logic_llm_verifier.py"


def _load_stage22_compact_output_verifier_module():
    import importlib.util
    import sys

    module_path = VERIFIER
    spec = importlib.util.spec_from_file_location(
        "stage22_compact_output_contract_verifier_parser",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load logic_llm_verifier.py")

    module = importlib.util.module_from_spec(spec)
    prior_module = sys.modules.get(spec.name)
    prior_sys_path = list(sys.path)
    sys.modules[spec.name] = module
    sys.path.insert(0, str(module_path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = prior_sys_path
        if prior_module is None:
            sys.modules.pop(spec.name, None)
        else:
            sys.modules[spec.name] = prior_module
    return module


class Stage22CompactOutputContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = VERIFIER.read_text(encoding="utf-8")
        marker = "STAGE22E21S18_EXPLICIT_REQUIRED_OUTPUT_FIELDS_V1"
        assert cls.source.count(marker) == 1
        start = cls.source.index(marker)
        end = cls.source.index('"canonical axes:\\n"', start)
        cls.contract = cls.source[start:end]

    def test_top_level_required_fields_are_explicit(self) -> None:
        required = {
            "verdict",
            "confidence",
            "reason",
            "checks",
            "findings",
            "alignments",
        }
        for field in required:
            with self.subTest(field=field):
                self.assertIn(field, self.contract)

    def test_alignment_required_fields_are_explicit(self) -> None:
        required = {
            "axis_id",
            "answer_claim",
            "canonical_claim",
            "claim_signature",
            "status",
            "criticality",
            "confidence",
            "reason",
            "error_class",
            "anchor_refs",
            "demand_refs",
        }
        for field in required:
            with self.subTest(field=field):
                self.assertIn(field, self.contract)

    def test_required_key_and_type_rules_are_explicit(self) -> None:
        self.assertIn("필수 key는 생략하지 않는다", self.contract)
        self.assertIn("0~1 finite number", self.contract)
        self.assertIn(
            "reason,claim_signature,error_class는 문자열",
            self.contract,
        )
        self.assertIn(
            "checks,findings,alignments,anchor_refs,demand_refs는 JSON array",
            self.contract,
        )

    def test_generic_exclusive_role_contradiction_rule_is_explicit(self) -> None:
        for binding in (
            "각 원자 주장마다 별도 alignment",
            "직접 소유하는 가장 구체적 axis에 1:1",
            "포괄 axis 병합 금지",
            "source-owned 필드는 source 복사",
            "타 축 독점·전담·단독",
            "error_class=CANONICAL_RELATION_CONTRADICTION",
            "claim_signature=<subject>.exclusively_establishes.<target>",
            "source fatal+confidence>=0.80",
            "status=FATAL_CONTRADICTION",
        ):
            with self.subTest(binding=binding):
                self.assertIn(binding, self.contract)
        self.assertNotIn(
            "PARTIAL이 아니라 CANONICAL_RELATION_CONTRADICTION",
            self.contract,
        )
        for topic_specific in (
            "Random Hardware Integrity",
            "HFT/SFF",
            "Systematic Integrity",
            "sw04_unit_test",
            "sw04_integration_test",
            "sw04_system_test",
        ):
            with self.subTest(topic_specific=topic_specific):
                self.assertNotIn(topic_specific, self.contract)

    def test_output_contract_precedes_canonical_axes_suffix(self) -> None:
        output_index = self.source.index(
            '"STAGE22_COMPACT_OUTPUT_CONTRACT_V1\\n"'
        )
        axes_index = self.source.index('"canonical axes:\\n"', output_index)
        axis_payload_index = self.source.index(
            'f"{axis_payload}"',
            axes_index,
        )
        self.assertLess(output_index, axes_index)
        self.assertLess(axes_index, axis_payload_index)

    def test_global_fallback_prompt_uses_line_preserving_claims_array(
        self,
    ) -> None:
        import importlib.util
        import sys
        from pathlib import Path

        module_path = (
            Path(__file__).resolve().parents[1]
            / "logic_llm_verifier.py"
        )
        spec = importlib.util.spec_from_file_location(
            "stage22_compact_output_contract_verifier",
            module_path,
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        prior_module = sys.modules.get(spec.name)
        prior_sys_path = list(sys.path)
        sys.modules[spec.name] = module
        sys.path.insert(0, str(module_path.parent))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path[:] = prior_sys_path
            if prior_module is None:
                sys.modules.pop(spec.name, None)
            else:
                sys.modules[spec.name] = prior_module
        source = module_path.read_text(encoding="utf-8")
        compact = module._compact_prompt_candidates(
            [
                {
                    "id": "C1",
                    "kind": "global_answer_context",
                    "text": (
                        "저수요 모드 목표는 PFDavg=1.0E-3이다.\n"
                        "감쇠비 ζ=0.707이다.\n"
                        "예시는 e.g. proof test이다."
                    ),
                },
                {
                    "id": "C2",
                    "kind": "key_term_context",
                    "text": "단일 evidence block",
                },
            ]
        )

        self.assertEqual(
            [
                "저수요 모드 목표는 PFDavg=1.0E-3이다.",
                "감쇠비 ζ=0.707이다.",
                "예시는 e.g. proof test이다.",
            ],
            compact[0]["claims"],
        )
        self.assertNotIn("text", compact[0])
        self.assertEqual(
            "단일 evidence block",
            compact[1]["text"],
        )
        self.assertNotIn("claims", compact[1])

        for binding in (
            "STAGE22E21S36_GLOBAL_FALLBACK_PROMPT_CLAIMS_ARRAY_V1",
            "def _compact_prompt_candidates(",
            'compact_candidate["claims"] = _lines(text)',
            "_compact_prompt_candidates(candidates)",
        ):
            with self.subTest(binding=binding):
                self.assertIn(binding, source)

        for unsafe_splitter in (
            "_split_clauses",
            "_split_claim_segments",
            "sent_tokenize",
            "spacy",
        ):
            with self.subTest(unsafe_splitter=unsafe_splitter):
                self.assertNotIn(
                    unsafe_splitter,
                    source[
                        source.index(
                            "STAGE22E21S36_"
                            "GLOBAL_FALLBACK_PROMPT_CLAIMS_ARRAY_V1"
                        ):
                        source.index(
                            "def _build_logic_prompt",
                            source.index(
                                "STAGE22E21S36_"
                                "GLOBAL_FALLBACK_PROMPT_CLAIMS_ARRAY_V1"
                            ),
                        )
                    ],
                )

    # STAGE22E21S47_STRICT_SINGLE_BRACE_PARSER_REGRESSION_V1
    def test_extract_json_object_repairs_one_missing_top_level_closing_brace(self):
        import json
        _extract_json_object = _load_stage22_compact_output_verifier_module()._extract_json_object

        payload = {
            "verdict": "fatal",
            "confidence": 0.9,
            "reason": "captured contract-shaped response",
            "checks": [],
            "findings": [],
            "alignments": [
                {"axis_id": "a"},
                {"axis_id": "b"},
                {"axis_id": "c"},
            ],
        }
        valid = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        repaired = _extract_json_object(valid[:-1])
        self.assertEqual(payload, repaired)
        self.assertEqual(3, len(repaired["alignments"]))

    def test_extract_json_object_rejects_unclosed_string(self):
        _extract_json_object = _load_stage22_compact_output_verifier_module()._extract_json_object

        self.assertIsNone(
            _extract_json_object('{"verdict":"fatal')
        )

    def test_extract_json_object_rejects_missing_array_closer(self):
        _extract_json_object = _load_stage22_compact_output_verifier_module()._extract_json_object

        self.assertIsNone(
            _extract_json_object(
                '{"alignments":[{"axis_id":"x"}'
            )
        )

    def test_extract_json_object_rejects_multiple_missing_closers(self):
        _extract_json_object = _load_stage22_compact_output_verifier_module()._extract_json_object

        self.assertIsNone(
            _extract_json_object('{"outer":{"value":1')
        )

    def test_extract_json_object_keeps_valid_json_unchanged(self):
        import json
        _extract_json_object = _load_stage22_compact_output_verifier_module()._extract_json_object

        payload = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": "valid",
            "checks": [],
            "findings": [],
            "alignments": [],
        }
        valid = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        self.assertEqual(
            payload,
            _extract_json_object(valid),
        )


if __name__ == "__main__":
    unittest.main()
