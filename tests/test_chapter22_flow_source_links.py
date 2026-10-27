"""Chapter 22 flow source is scoped to its existing closed-pipe Topic."""

import json
from pathlib import Path

from study.master_topic_pack import (
    _apply_training_source_scopes,
    load_master_topic_pack,
    project_grading,
    project_training,
)


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "flow_measurement_meter_principles_velocity_selection"
SOURCE_ID = "wp-post:9774"


def test_chapter22_source_preserves_grading_and_excludes_open_channel_section():
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{TOPIC}.json")
    reference = next(row for row in master["sources"] if row["source_id"] == SOURCE_ID)
    assert reference["verification_status"] == "unverified"
    assert reference["content_sha256"] == reference["version"]
    assert reference["training_scope"]["mode"] == "text_ranges"
    assert project_grading(ROOT, master)["authority"] == "existing_topic_pack"
    training = project_training(ROOT, master)
    assert SOURCE_ID in {row["source_id"] for row in training["source_references"]}

    text = "\n".join((
        "1. 유량 측정의 기본 개념", "차압식과 층류식", "6. 위어(Weir)와 플룸(Flume)",
        "개수로 위어·플룸", "7. 터빈식 유량계", "터빈과 전자식",
        "13. 유량계별 관계식 통합 비교", "개수로 비교표",
    ))
    materials, excluded = _apply_training_source_scopes(
        [{"source_id": SOURCE_ID, "source_type": "wordpress_post", "text": text}],
        master["sources"],
    )
    assert not excluded
    assert len(materials) == 1
    assert "차압식과 층류식" in materials[0]["text"]
    assert "터빈과 전자식" in materials[0]["text"]
    assert "개수로 위어·플룸" not in materials[0]["text"]
    assert "개수로 비교표" not in materials[0]["text"]


def test_chapter22_open_channel_section_has_separate_approved_owner():
    sheet = ROOT / "docs" / "topic_sheets" / "open_channel_weir_flume_head_discharge_submergence_selection.md"
    content = sheet.read_text(encoding="utf-8")
    assert "post `9774`" in content
    assert "Q ∝ H^(3/2)" in content
    assert "Q ∝ H^(5/2)" in content
    topic = sheet.stem
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{topic}.json")
    assert master["sources"][0]["training_scope"]["mode"] == "text_ranges"
    status = json.loads((ROOT / "rubrics" / "topic_packs" / topic / "topic_status.json").read_text())
    assert status["status"] == "approved"
    assert status["reviewer"] == "now0930"
