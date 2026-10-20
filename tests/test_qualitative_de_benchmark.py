"""Expert D/E worklist must preserve provenance without inventing labels."""

import json
from collections import Counter
from pathlib import Path

from grading.qualitative.de_benchmark import blank_labels, build_manifest, validate_labels


ROOT = Path(__file__).resolve().parents[1]


def test_stratified_manifest_is_stable_and_does_not_copy_answers():
    first = build_manifest(ROOT)
    second = build_manifest(ROOT)
    assert first == second
    assert first["case_count"] == 25
    assert set(Counter(row["question_type"] for row in first["cases"]).values()) == {5}
    assert len({row["case_id"] for row in first["cases"]}) == 25
    assert all(row["expert_de_status"] == "UNLABELED" for row in first["cases"])
    assert all("answer" not in row and "question" not in row for row in first["cases"])
    assert all(len(row["answer_sha256"]) == 64 for row in first["cases"])


def test_blank_labels_are_not_accepted_as_expert_truth():
    manifest = build_manifest(ROOT)
    labels = blank_labels(manifest)
    errors = validate_labels(manifest, labels, ROOT)
    assert len(labels["labels"]) == 25
    assert errors
    assert any("missing_review_provenance" in error for error in errors)
    assert any("invalid_score" in error for error in errors)


def test_evidence_and_source_hash_are_required():
    manifest = build_manifest(ROOT, per_type=1)
    labels = blank_labels(manifest)
    first = labels["labels"][0]
    first["answer_sha256"] = "0" * 64
    first["reviewer"] = "expert"
    first["reviewed_at"] = "2026-10-20T00:00:00+09:00"
    for criterion in first["criteria"]:
        criterion.update(score=0, reason="No demonstrated evidence")
    first["criteria"][0].update(score=1, quote="invented", start=0, end=8)
    errors = validate_labels(manifest, labels, ROOT)
    case_id = first["case_id"]
    assert f"{case_id}:answer_hash_mismatch" in errors
    assert f"{case_id}:D1:invalid_evidence" in errors


def test_manifest_serializes_to_json():
    assert json.loads(json.dumps(build_manifest(ROOT)))["case_count"] == 25
