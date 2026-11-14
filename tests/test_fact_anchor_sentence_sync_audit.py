"""Source/generated Fact sentence drift audit is non-scoring and fail-closed."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_fact_anchor_sentence_sync import audit_source_generated


def _write(path: Path, value: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _fixture(root: Path, *, generated_text: str | None = "짧은 사실이다."):
    old, new, topic, fact_id = (
        "이전 기술 사실이다. 별도의 조건을 설명한다.",
        "짧은 사실이다.", "test_topic", "fact_one"
    )
    _write(root / "calibration/fact_anchor_simplification_review_20261114.json", {
        "schema_version": "fact_anchor_simplification_review.v1",
        "review_status": "PENDING_TECHNICAL_REVIEW",
        "score_effect": "none",
        "changed_anchor_count": 1,
        "entries": [{
            "topic_id": topic,
            "anchor_id": fact_id,
            "previous_statement": old,
            "simplified_statement": new,
            "review_status": "PENDING_TECHNICAL_REVIEW",
        }],
    })
    source = root / f"rubrics/topic_packs/{topic}/fact_anchor.json"
    _write(source, {
        "topic_id": topic,
        "anchors": [{
            "anchor_id": fact_id, "statement": new,
            "accepted_explanations": [old],
        }],
    })
    generated = root / "rubrics/generated/fact_anchors.generated.json"
    _write(generated, {
        "topics": [{
            "topic_id": topic,
            "anchors": (
                [] if generated_text is None else [{
                    "anchor_id": fact_id, "expected": generated_text,
                }]
            ),
        }],
    })
    return old, new, source, generated


@pytest.mark.parametrize(("generated_value", "expected_status"), [
    ("new", "GENERATED_WORDING_MATCHES_SOURCE"),
    ("old", "GENERATED_WORDING_MATCHES_PREVIOUS"),
    ("other", "GENERATED_WORDING_OTHER"),
    ("missing", "GENERATED_ANCHOR_MISSING"),
])
def test_read_only_audit_identifies_wording_drift(tmp_path, generated_value, expected_status):
    old, new, source, generated = _fixture(tmp_path)
    value = {"new": new, "old": old, "other": "서로 다른 사실이다.",
             "missing": None}[generated_value]
    _write(generated, {
        "topics": [{"topic_id": "test_topic",
                    "anchors": [] if value is None else [
                        {"anchor_id": "fact_one", "expected": value},
                    ]}],
    })
    source_before, generated_before = source.read_bytes(), generated.read_bytes()
    report = audit_source_generated(tmp_path)
    assert report["generated_wording_counts"] == {expected_status: 1}
    assert report["score_effect"] == "none"
    assert report["score_admission"] == "DISABLED"
    assert report["technical_equivalence_reviewed"] is False
    assert report["safe_to_promote_automatically"] is False
    assert report["generated_wording_match_is_not_routing_equivalence"] is True
    assert source.read_bytes() == source_before
    assert generated.read_bytes() == generated_before
    assert new not in str(report)
    assert old not in str(report)


def test_source_wording_mismatch_is_never_silently_accepted(tmp_path):
    _old, _new, source, _generated = _fixture(tmp_path)
    _write(source, {
        "topic_id": "test_topic",
        "anchors": [{
            "anchor_id": "fact_one",
            "statement": "승인받지 않은 다른 내용이다.",
            "accepted_explanations": [],
        }],
    })
    with pytest.raises(ValueError, match="source text drifted"):
        audit_source_generated(tmp_path)


def test_manifest_count_and_identity_must_match(tmp_path):
    _old, _new, _source, _generated = _fixture(tmp_path)
    manifest = tmp_path / "calibration/fact_anchor_simplification_review_20261114.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["changed_anchor_count"] = 2
    _write(manifest, payload)
    with pytest.raises(ValueError, match="invalid Fact sentence review manifest"):
        audit_source_generated(tmp_path)


def test_duplicated_source_and_generated_fact_ids_fail_closed(tmp_path):
    _old, new, source, generated = _fixture(tmp_path)
    raw = json.loads(source.read_text(encoding="utf-8"))
    raw["anchors"].append(dict(raw["anchors"][0]))
    _write(source, raw)
    with pytest.raises(ValueError, match="duplicate or invalid source Fact"):
        audit_source_generated(tmp_path)
    raw["anchors"] = raw["anchors"][:1]
    _write(source, raw)
    generated_data = json.loads(generated.read_text(encoding="utf-8"))
    generated_data["topics"][0]["anchors"].append({
        "anchor_id": "fact_one", "expected": new,
    })
    _write(generated, generated_data)
    with pytest.raises(ValueError, match="duplicate or invalid generated Fact ID"):
        audit_source_generated(tmp_path)
