"""Source/generated Fact sentence drift audit is non-scoring and fail-closed."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_fact_anchor_sentence_sync import (
    PRECISION_CORRECTION_STATEMENT,
    audit_source_generated,
)


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
        "application_status": "CANDIDATE_ONLY_NOT_APPLIED",
        "applied_anchor_count": 0,
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
            "anchor_id": fact_id, "statement": old,
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
    ("new", "GENERATED_WORDING_MATCHES_CANDIDATE"),
    ("old", "GENERATED_WORDING_MATCHES_CANONICAL"),
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


def test_pending_candidate_applied_to_canonical_is_rejected(tmp_path):
    _old, new, source, _generated = _fixture(tmp_path)
    data = json.loads(source.read_text(encoding="utf-8"))
    data["anchors"][0]["statement"] = new
    _write(source, data)
    with pytest.raises(ValueError, match="source text drifted"):
        audit_source_generated(tmp_path)


def test_pending_manifest_cannot_claim_applied_anchors(tmp_path):
    _old, _new, _source, _generated = _fixture(tmp_path)
    manifest = tmp_path / "calibration/fact_anchor_simplification_review_20261114.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["applied_anchor_count"] = 1
    _write(manifest, data)
    with pytest.raises(ValueError, match="invalid Fact sentence review manifest"):
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


def test_only_reviewed_encoder_correction_can_differ_from_historical_previous(tmp_path):
    old, pending, source, generated = _fixture(tmp_path)
    topic = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
    anchor_id = "encoder_frequency_limit_selection"
    corrected = PRECISION_CORRECTION_STATEMENT
    metadata = {
        "statement": corrected,
        "review_report": "reports/pr38_encoder_frequency_canonical_precision_review_20261115.md",
        "review_method": "ai",
        "application_scope": "CANONICAL_PRECISION_ONLY_NOT_SIMPLIFICATION",
        "release_status": "PENDING_VALIDATION",
        "score_effect": "none",
    }
    manifest = tmp_path / "calibration/fact_anchor_simplification_review_20261114.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    item = payload["entries"][0]
    item["topic_id"], item["anchor_id"] = topic, anchor_id
    item["canonical_precision_correction"] = metadata
    _write(manifest, payload)
    target = tmp_path / "rubrics/topic_packs" / topic / "fact_anchor.json"
    _write(target, {
        "topic_id": topic,
        "anchors": [{
            "anchor_id": anchor_id,
            "statement": corrected,
            "claim": corrected,
            "description": corrected,
            "accepted_explanations": [corrected],
        }],
    })
    source.unlink()
    _write(generated, {"topics": [{
        "topic_id": topic,
        "anchors": [{"anchor_id": anchor_id, "expected": old}],
    }]})
    report = tmp_path / metadata["review_report"]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("Old: " + old + "\nCorrected: " + corrected, encoding="utf-8")

    result = audit_source_generated(tmp_path)
    assert result["anchor_count"] == 1
    assert result["precision_corrected_anchor_count"] == 1
    assert result["score_effect"] == "none"
    assert result["score_admission"] == "DISABLED"
    assert result["generated_wording_counts"] == {
        "GENERATED_WORDING_MATCHES_SUPERSEDED_CANONICAL": 1
    }
    assert result["cases"][0]["canonical_wording_status"] == (
        "SOURCE_REVIEWED_PRECISION_CORRECTION"
    )
    assert result["safe_to_promote_automatically"] is False

    # A similarly worded unreviewed claim must fail, even when it retains all
    # the old check's terms (PPR/60, N_eff/60, x1/x2/x4, decoder, and rate).
    modified = corrected.replace(
        "별도의 처리율 한계가 명시된 경우",
        "내부 처리율을 검토하지 않아도 되는 경우",
    )
    assert modified != corrected
    assert all(token in modified for token in (
        "PPR/60", "N_eff/60", "x1/x2/x4", "복호모드별", "처리율",
    ))
    tampered = json.loads(target.read_text(encoding="utf-8"))
    for key in ("statement", "claim", "description"):
        tampered["anchors"][0][key] = modified
    tampered["anchors"][0]["accepted_explanations"][0] = modified
    _write(target, tampered)
    tampered_manifest = json.loads(manifest.read_text(encoding="utf-8"))
    tampered_manifest["entries"][0]["canonical_precision_correction"]["statement"] = modified
    _write(manifest, tampered_manifest)
    report.write_text(
        "Old: " + old + "\nCorrected: " + corrected + "\nAlternative: " + modified,
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="differs from reviewed wording"):
        audit_source_generated(tmp_path)

    # Restore approved manifest/source and then test that applying the old
    # unapproved simplification is still rejected.
    tampered_manifest["entries"][0]["canonical_precision_correction"]["statement"] = corrected
    _write(manifest, tampered_manifest)
    for key in ("statement", "claim", "description"):
        tampered["anchors"][0][key] = corrected
    tampered["anchors"][0]["accepted_explanations"][0] = corrected
    _write(target, tampered)

    # The old shortened candidate must still fail even if the repair was recorded.
    data = json.loads(target.read_text(encoding="utf-8"))
    for key in ("statement", "claim", "description"):
        data["anchors"][0][key] = pending
    data["anchors"][0]["accepted_explanations"][0] = pending
    _write(target, data)
    with pytest.raises(ValueError, match="source text drifted"):
        audit_source_generated(tmp_path)


def test_fake_canonical_precision_correction_is_rejected(tmp_path):
    old, pending, _source, _generated = _fixture(tmp_path)
    manifest = tmp_path / "calibration/fact_anchor_simplification_review_20261114.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["entries"][0]["canonical_precision_correction"] = {
        "statement": "허가 없이 변경한 사실이다.",
        "review_report": "reports/pr38_encoder_frequency_canonical_precision_review_20261115.md",
        "review_method": "ai",
        "application_scope": "CANONICAL_PRECISION_ONLY_NOT_SIMPLIFICATION",
        "release_status": "PENDING_VALIDATION",
        "score_effect": "none",
    }
    _write(manifest, payload)
    with pytest.raises(ValueError, match="unauthorized canonical precision correction"):
        audit_source_generated(tmp_path)
