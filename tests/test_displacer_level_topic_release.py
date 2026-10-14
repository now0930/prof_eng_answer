"""Regression contract for the approved Displacer level Topic Pack."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.topic_pack_status import content_hash
from grading.routing.deterministic_topic_router import route_question_topics
from study.master_topic_pack import (
    load_master_topic_pack,
    project_diagnosis,
    project_grading,
    project_training,
)


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "displacer_level_buoyancy_torque_tube_density_interface_calibration"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
GENERATED = ROOT / "rubrics" / "generated"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_displacer_approved_source_hash_is_current() -> None:
    status = _read(PACK / "topic_status.json")
    assert status["status"] == "approved"
    assert status["review_state"] == "reviewed"
    assert status["reviewer"] == "now0930"
    assert status["content_hash"] == status["approved_source_hash"] == content_hash(PACK)


def test_displacer_question_patterns_only_require_their_own_anchors() -> None:
    anchor_ids = {row["anchor_id"] for row in _read(PACK / "fact_anchor.json")["anchors"]}
    patterns = _read(PACK / "model_answer.json")["expected_question_patterns"]
    assert len(anchor_ids) == 7
    assert len(patterns) == 3
    for pattern in patterns:
        required = set(pattern["required_anchor_ids"])
        assert required and required < anchor_ids
    assert "displacer_interface_density_difference" not in patterns[0]["required_anchor_ids"]
    assert "displacer_wet_dry_calibration" not in patterns[1]["required_anchor_ids"]


def test_displacer_is_in_runtime_banks_without_deterministic_fatal_rule() -> None:
    for filename, collection in (
        ("fact_anchors.generated.json", "topics"),
        ("logic_check_profiles.generated.json", "profiles"),
        ("logic_checks.generated.json", "topic_logic_checks"),
        ("model_answers.generated.json", "answers"),
        ("topic_importance.generated.json", "topics"),
        ("topic_pack_manifest.generated.json", "topics"),
    ):
        rows = _read(GENERATED / filename)[collection]
        assert sum(row.get("topic_id") == TOPIC_ID for row in rows) == 1

    logic = _read(PACK / "logic_check.json")["deterministic_checks"]
    assert logic["enabled"] is False
    assert logic["fatal_checks"] == []


def test_displacer_master_projects_three_views_with_scoped_wordpress_sources() -> None:
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{TOPIC_ID}.json")
    grading = project_grading(ROOT, master)
    training = project_training(ROOT, master)
    diagnosis = project_diagnosis(ROOT, master)
    assert grading["sources"]["fact_anchor"] == _read(PACK / "fact_anchor.json")
    assert training["question_patterns"] == _read(PACK / "model_answer.json")["expected_question_patterns"]
    assert diagnosis["score_effect"] == "none"
    assert {source["source_type"] for source in master["sources"]} == {"wordpress_post", "pdf"}
    assert all(source["section"].startswith("20.4") for source in master["sources"])
    assert all(source["training_scope"]["mode"] == "text_ranges" for source in master["sources"])


def test_displacer_questions_route_to_the_new_owner_without_stealing_dp() -> None:
    patterns = _read(PACK / "model_answer.json")["expected_question_patterns"]
    for pattern in patterns:
        result = route_question_topics(pattern["pattern"])
        assert result["provider_calls"] == 0
        assert result["primary_topic_id"] == TOPIC_ID
    dp_result = route_question_topics("차압식 레벨계의 Wet Leg와 Dry Leg 적용조건을 설명하시오.")
    assert dp_result["primary_topic_id"] != TOPIC_ID
