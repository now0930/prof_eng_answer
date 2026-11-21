"""Fact Anchors remain source-owned short engineering sentences, not triples."""
from __future__ import annotations

import json

import pytest

from grading.evidence.fact_anchor_sentence_view import (
    project_fact_anchor_sentences,
)


TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"


def test_existing_fact_anchor_uses_original_sentence_not_machine_relation():
    view = project_fact_anchor_sentences([TOPIC])
    rows = {row["fact_id"]: row for row in view["rows"]}
    fact = rows["fsrm_low_demand_pfdavg"]
    assert fact["statement"] == (
        "저수요 SIF의 정량 목표는 일반적으로 평균 요구시 실패확률인 PFDavg로 표현한다."
    )
    assert fact["style_status"] == "SINGLE_STATEMENT"
    assert fact["score_effect"] == "none"
    assert view["score_admission"] == "DISABLED"
    assert all("relation" not in row for row in view["rows"])


def test_multi_sentence_anchor_is_not_split_or_promoted(tmp_path):
    topic = "sentence_test_topic"
    root = tmp_path / "rubrics/topic_packs" / topic
    root.mkdir(parents=True)
    original = "첫 번째 공학 주장은 조건에 따라 성립한다. 두 번째 주장은 별도 검토한다."
    (root / "fact_anchor.json").write_text(json.dumps({
        "topic_id": topic,
        "anchors": [{
            "id": "one",
            "anchor_id": "one",
            "statement": original,
        }],
    }, ensure_ascii=False), encoding="utf-8")
    view = project_fact_anchor_sentences([topic], root=tmp_path)
    assert view["multi_sentence_count"] == 1
    assert view["rows"][0]["statement"] == original
    assert view["rows"][0]["style_status"] == "MANUAL_SIMPLIFICATION_REQUIRED"
    assert view["score_effect"] == "none"


def test_path_traversal_and_duplicate_anchor_ids_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="Topic identity"):
        project_fact_anchor_sentences(["../secrets"], root=tmp_path)
    path = tmp_path / "rubrics/topic_packs/safe_topic"
    path.mkdir(parents=True)
    (path / "fact_anchor.json").write_text(json.dumps({
        "topic_id": "safe_topic",
        "anchors": [
            {"id": "same", "statement": "첫 번째 문장이다."},
            {"id": "same", "statement": "다른 문장이다."},
        ],
    }, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate Fact Anchor"):
        project_fact_anchor_sentences(["safe_topic"], root=tmp_path)


def test_missing_topic_and_missing_statement_are_not_accepted(tmp_path):
    with pytest.raises(ValueError, match="source missing"):
        project_fact_anchor_sentences(["not_found"], root=tmp_path)
    root = tmp_path / "rubrics/topic_packs/example_topic"
    root.mkdir(parents=True)
    (root / "fact_anchor.json").write_text(json.dumps({
        "topic_id": "example_topic",
        "anchors": [{"id": "empty", "statement": " "}],
    }), encoding="utf-8")
    with pytest.raises(ValueError, match="sentence missing"):
        project_fact_anchor_sentences(["example_topic"], root=tmp_path)
