from __future__ import annotations

import importlib.util
import inspect
import json
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability"
SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
GENERATED_DIR = ROOT / "rubrics" / "generated"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_topic(value: Any, topic_id: str) -> Any:
    if isinstance(value, dict):
        if value.get("topic_id") == topic_id or value.get("canonical_topic_id") == topic_id:
            return value
        if topic_id in value:
            return value[topic_id]
        for child in value.values():
            found = find_topic(child, topic_id)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_topic(child, topic_id)
            if found is not None:
                return found
    return None


def item_id(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    for key in ("id", "anchor_id", "fact_id", "claim_id", "check_id", "pattern_id"):
        candidate = value.get(key)
        if isinstance(candidate, str):
            return candidate
    return None


def _invoke_route_helper(route: Any, question: str, answer: str) -> Any:
    signature = inspect.signature(route)
    positional = []
    keyword = {}

    for parameter in signature.parameters.values():
        name = parameter.name.lower()

        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue

        if name in {"topic_id", "target_topic_id", "canonical_topic_id"}:
            value = TOPIC_ID
        elif "question" in name or name in {"query", "prompt", "text"}:
            value = question
        elif "answer" in name or name in {"response", "submission"}:
            value = answer
        elif parameter.default is not inspect._empty:
            continue
        else:
            raise RuntimeError(
                f"Unsupported required router-helper parameter: {parameter.name}"
            )

        if parameter.kind in (
            parameter.POSITIONAL_ONLY,
            parameter.POSITIONAL_OR_KEYWORD,
        ):
            positional.append(value)
        else:
            keyword[parameter.name] = value

    return route(*positional, **keyword)


def _extract_primary_topic(module: Any, result: Any) -> str | None:
    for selector_name in ("selected_topic", "_primary_topic", "primary_topic"):
        selector = getattr(module, selector_name, None)
        if callable(selector):
            try:
                selected = selector(result)
            except TypeError:
                continue

            if isinstance(selected, str):
                return selected
            if isinstance(selected, dict):
                candidate = selected.get("topic_id") or selected.get("id")
                if isinstance(candidate, str):
                    return candidate

    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        for key in (
            "primary_topic",
            "topic_id",
            "selected_topic",
            "primary",
            "top_topic",
        ):
            value = result.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                candidate = value.get("topic_id") or value.get("id")
                if isinstance(candidate, str):
                    return candidate

        for key in ("candidates", "topics", "matches", "ranked_topics"):
            value = result.get(key)
            if isinstance(value, list) and value:
                first = value[0]
                if isinstance(first, str):
                    return first
                if isinstance(first, dict):
                    candidate = first.get("topic_id") or first.get("id")
                    if isinstance(candidate, str):
                        return candidate

    if isinstance(result, (list, tuple)) and result:
        first = result[0]
        if isinstance(first, str):
            return first
        if isinstance(first, dict):
            candidate = first.get("topic_id") or first.get("id")
            if isinstance(candidate, str):
                return candidate

    return None


def route_primary(question: str, answer: str = "") -> str | None:
    helper_paths = [
        ROOT / "scripts" / "test_control_valve_selection_process_lifecycle_topic.py",
        ROOT / "scripts" / "test_final_control_element_sil_sis_esd_pst_topic.py",
        ROOT / "scripts" / "test_control_valve_types_body_actuator_topic.py",
    ]

    diagnostics = []

    for index, path in enumerate(helper_paths):
        if not path.is_file():
            diagnostics.append(f"missing:{path.name}")
            continue

        spec = importlib.util.spec_from_file_location(
            f"_sw01_router_reference_{index}",
            path,
        )
        if spec is None or spec.loader is None:
            diagnostics.append(f"load_spec_failed:{path.name}")
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        route = getattr(module, "route_reference", None)
        if not callable(route):
            diagnostics.append(f"route_reference_missing:{path.name}")
            continue

        try:
            result = _invoke_route_helper(route, question, answer)
        except Exception as exc:
            diagnostics.append(
                f"route_reference_failed:{path.name}:"
                f"{type(exc).__name__}:{exc}"
            )
            continue

        primary = _extract_primary_topic(module, result)
        if primary is not None:
            return primary

        diagnostics.append(f"primary_extraction_failed:{path.name}")

    raise RuntimeError(
        "No compatible production-router test helper was available: "
        + " | ".join(diagnostics)
    )


class SW01SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(SOURCE_DIR / "topic_importance.json")
        cls.source_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SOURCE_DIR.glob("*"))
            if path.is_file()
        )

    def test_source_files_exist(self) -> None:
        expected = {
            "README.md",
            "fact_anchor.json",
            "logic_check.json",
            "model_answer.json",
            "topic_importance.json",
        }
        self.assertEqual(expected, {path.name for path in SOURCE_DIR.iterdir() if path.is_file()})

    def test_topic_ids_are_exact(self) -> None:
        for payload in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(TOPIC_ID, payload.get("topic_id"))

    def test_anchor_contract_is_unique(self) -> None:
        anchors = self.fact["anchors"]
        ids = [item_id(item) for item in anchors]
        self.assertEqual(26, len(anchors))
        self.assertNotIn(None, ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_fatal_contract_is_unique(self) -> None:
        rows = self.fact["fatal_wrong_claims"]
        ids = [item_id(item) for item in rows]
        self.assertEqual(12, len(rows))
        self.assertNotIn(None, ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_semantic_markers(self) -> None:
        markers = [
            "Remote I/O",
            "Active/Standby",
            "Bumpless Transfer",
            "MTBF",
            "MTTR",
            "Single Point of Failure",
            "Common Cause Failure",
            "Degraded Mode",
            "Local Control",
            "상태동기화",
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source_text)

    def test_availability_formula_and_conditions(self) -> None:
        self.assertIn("A = MTBF / (MTBF + MTTR)", self.source_text)
        self.assertIn("적용조건", self.source_text)
        self.assertIn("일정 고장률", self.source_text)

    def test_boundary_markers(self) -> None:
        for marker in ("SW-03", "SW-05", "SW-07", "SW-08", "SW-09", "SW-10", "SW-11", "SW-12"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source_text)

    def test_legacy_handoff_markers(self) -> None:
        for marker in (
            "plc_dcs_remote_io",
            "reliability_maintainability_availability_ram",
            "hmi_scada",
            "smart_mcc_motor_control_center_monitoring",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source_text)

    def test_no_reference_topic_leakage(self) -> None:
        lowered = self.source_text.lower()
        for marker in ("control valve", "제어밸브", "control_valve_selection_process_pressure_temperature_flow_media_lifecycle"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker.lower(), lowered)

    def test_importance_contract(self) -> None:
        self.assertEqual("COMPARE_SELECTION", self.importance.get("question_type"))
        self.assertEqual("THEORY_CORE", self.importance.get("difficulty"))
        self.assertEqual("CORE_MUST_PREPARE", self.importance.get("selection_importance"))


class SW01GeneratedContractTests(unittest.TestCase):
    def test_generated_topic_contracts_exist(self) -> None:
        for name in (
            "fact_anchors.generated.json",
            "logic_check_profiles.generated.json",
            "logic_checks.generated.json",
            "model_answers.generated.json",
            "topic_importance.generated.json",
            "topic_pack_manifest.generated.json",
        ):
            payload = load_json(GENERATED_DIR / name)
            with self.subTest(name=name):
                self.assertIsNotNone(find_topic(payload, TOPIC_ID))

    def test_source_generated_anchor_alignment(self) -> None:
        source = load_json(SOURCE_DIR / "fact_anchor.json")
        generated = load_json(GENERATED_DIR / "fact_anchors.generated.json")
        target = find_topic(generated, TOPIC_ID)
        self.assertIsNotNone(target)
        source_ids = {item_id(item) for item in source["anchors"]}
        generated_ids = {item_id(item) for item in target["anchors"]}
        self.assertEqual(source_ids, generated_ids)

    def test_manifest_topic_count_and_membership(self) -> None:
        manifest = load_json(GENERATED_DIR / "topic_pack_manifest.generated.json")
        source_topic_count = len(
            [
                path
                for path in (ROOT / "rubrics" / "topic_packs").iterdir()
                if path.is_dir() and not path.name.startswith(".")
            ]
        )
        self.assertEqual(
            source_topic_count,
            manifest.get("topic_count"),
        )
        self.assertIsNotNone(find_topic(manifest, TOPIC_ID))


class SW01RoutingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")

    def test_specific_routing_aliases_exist(self) -> None:
        aliases = self.model.get("routing_aliases") or []
        self.assertGreaterEqual(len(aliases), 10)
        required = [
            "PLC DCS SCADA Remote I/O 구조와 선정",
            "제어기 상태동기화 Bumpless Transfer",
            "제어시스템 단일고장점 공통원인고장",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, aliases)

    def test_routing_field_points_cover_core_clusters(self) -> None:
        points = "\n".join(
            str(value)
            for value in (self.model.get("routing_field_points") or [])
        )
        for marker in (
            "CPU 전원 I/O 통신망 이중화",
            "Bumpless Transfer",
            "MTBF MTTR 가용도",
            "Common Cause Failure",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, points)

    def test_deterministic_alias_projection(self) -> None:
        deterministic = self.logic.get("deterministic_checks") or {}
        aliases = deterministic.get("topic_aliases") or []
        self.assertEqual(
            self.model.get("routing_aliases") or [],
            aliases,
        )

    def test_no_single_word_generic_alias(self) -> None:
        aliases = self.model.get("routing_aliases") or []
        generic = {
            "PLC",
            "DCS",
            "SCADA",
            "이중화",
            "가용도",
            "신뢰도",
            "reliability",
            "availability",
        }
        self.assertFalse(generic.intersection(set(aliases)))


if __name__ == "__main__":
    unittest.main()
