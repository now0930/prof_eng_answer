from __future__ import annotations

import json
import hashlib
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.learning_runtime import LearningRuntimeError, feedback_from_view
from study.master_topic_pack import project_diagnosis, project_training, project_grading
from test_master_topic_pack_schema import _valid_record


def _write_sources(tmp_path: Path, master: dict) -> None:
    topic_id = master["topic_id"]
    payloads = {
        "fact_anchor": {"topic_id": topic_id, "anchors": [{"id": "f1", "content": "fact"}], "fatal_wrong_claims": [{"id": "fatal1"}]},
        "logic_check": {"topic_id": topic_id, "deterministic_checks": [{"id": "check1"}], "llm_profile": {"focus": ["evidence"]}},
        "model_answer": {"topic_id": topic_id, "question_examples": ["Define the system."], "expected_question_patterns": [{"id": "q1", "pattern": "Explain the system."}], "recommended_outline": [{"section": "body"}], "high_score_points": ["depth"], "common_missing_points": ["verification"]},
        "topic_importance": {"topic_id": topic_id, "high_band_unlock_conditions": ["evidence"]},
    }
    for key, relative in master["legacy_topic_pack"]["source_files"].items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payloads[key]), encoding="utf-8")


def test_training_projection_has_content_and_daily_target() -> None:
    master = _valid_record()
    with tempfile.TemporaryDirectory(prefix="training-projection-") as directory:
        root = Path(directory)
        _write_sources(root, master)
        grading_before = project_grading(root, master)
        source_ref = {
            "source_id": "wp-post:42", "source_type": "wordpress_post",
            "wordpress_url": "https://now0930.pe.kr/wordpress/example/",
            "source_url": "https://now0930.pe.kr/wordpress/example/",
            "title": "Handwritten OCR notes", "version": "a" * 64,
            "page": None, "section": None, "updated_at": None,
            "verification_status": "unverified",
        }
        master["sources"] = [source_ref]
        text = "OCR study text from WordPress HTML."
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        source_ref["version"] = digest
        bundle_path = root / "data/wordpress_topic_packs" / f"{master['topic_id']}.json"
        bundle_path.parent.mkdir(parents=True)
        bundle_path.write_text(json.dumps({
            "topic_id": master["topic_id"], "private": True,
            "content_trust": "untrusted_source_text",
            "sources": [{
                "source_id": "wp-post:42", "source_type": "wordpress_post", "topic_id": master["topic_id"],
                "wordpress_url": source_ref["wordpress_url"], "title": source_ref["title"],
                "version": digest, "content_sha256": digest,
                "extracted_text_sha256": digest,
                "extraction_status": "extracted", "extraction_method": "wordpress_wxr_html",
                "extracted_text": text,
            }, {
                "source_id": "wp-post:unlinked", "extraction_status": "extracted",
                "extraction_method": "wordpress_wxr_html", "extracted_text": "must not leak",
            }],
        }), encoding="utf-8")
        result = project_training(root, master)
        assert project_grading(root, master) == grading_before
    assert result["projection_id"] == "training-projection-v1"
    assert result["daily_target"] == 2
    assert result["question_examples"] == ["Define the system."]
    assert result["question_patterns"][0]["id"] == "q1"
    assert result["fact_anchors"][0]["id"] == "f1"
    assert result["recommended_outline"][0]["section"] == "body"
    assert len(result["source_materials"]) == 1
    assert result["source_materials"][0]["text"] == text
    assert result["source_materials"][0]["content_sha256"] == digest


def test_diagnosis_projection_exposes_signals_without_score_effect() -> None:
    master = _valid_record()
    with tempfile.TemporaryDirectory(prefix="diagnosis-projection-") as directory:
        root = Path(directory)
        _write_sources(root, master)
        result = project_diagnosis(root, master)
    assert result["projection_id"] == "diagnosis-projection-v1"
    assert {"format", "content", "reasoning", "application", "verification"} <= set(result["dimensions"])
    assert result["fatal_wrong_claims"][0]["id"] == "fatal1"
    assert result["deterministic_checks"][0]["id"] == "check1"
    assert result["diagnostic_guidance"]["focus"] == ["evidence"]
    assert result["score_effect"] == "none"


def test_feedback_adapter_is_separate_and_rejects_scoring_or_wrong_topic_views() -> None:
    grade = {"topic_id": "sample_topic_id", "final_total_score": 12.5, "verdict": "below", "overall_summary": "Needs evidence."}
    before = json.loads(json.dumps(grade))
    view = {
        "projection_id": "diagnosis-projection-v1",
        "topic_id": "sample_topic_id",
        "title_ko": "샘플",
        "dimensions": ["content", "verification"],
        "fact_anchors": [{"id": "a1"}],
        "deterministic_checks": [{"id": "c1"}],
        "diagnostic_guidance": {"focus": ["evidence"]},
        "common_missing_points": ["verification"],
        "score_effect": "none",
    }
    feedback = feedback_from_view(grade, view)
    assert feedback["grade_summary"] == "Needs evidence."
    assert feedback["score_effect"] == "none"
    assert grade == before

    try:
        feedback_from_view(grade, {**view, "score_effect": "reduce"})
    except LearningRuntimeError:
        pass
    else:
        raise AssertionError("scoring diagnosis view must be rejected")

    try:
        feedback_from_view(grade, {**view, "topic_id": "another_topic_id"})
    except LearningRuntimeError:
        pass
    else:
        raise AssertionError("mismatched Topic diagnosis view must be rejected")


def test_wordpress_references_reach_learning_views_without_becoming_grading_content() -> None:
    master = _valid_record()
    reference = {
        "source_id": "wp-post:42", "source_type": "wordpress_post",
        "wordpress_url": "https://now0930.pe.kr/wordpress/example/",
        "source_url": "https://now0930.pe.kr/wordpress/example/",
        "title": "Reference only", "version": "v1", "page": None,
        "section": None, "updated_at": None, "verification_status": "unverified",
    }
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _write_sources(root, master)
        original_grade_view = project_grading(root, master)
        master["sources"] = [reference]
        training = project_training(root, master)
        diagnosis = project_diagnosis(root, master)
        grade = {"topic_id": master["topic_id"], "final_total_score": 12.5}
        feedback = feedback_from_view(grade, diagnosis)
        assert training["source_references"] == diagnosis["source_references"] == feedback["source_references"] == [reference]
        assert project_grading(root, master) == original_grade_view
        assert feedback["score_effect"] == "none" and grade["final_total_score"] == 12.5
        feedback["source_references"][0]["title"] = "local change"
        training["source_references"][0]["verification_status"] = "verified"
        assert master["sources"][0] == reference
        assert diagnosis["source_references"][0] == reference


def test_extracted_wordpress_material_requires_matching_hash_and_reference() -> None:
    master = _valid_record()
    reference = {
        "source_id": "wp-post:42", "source_type": "wordpress_post",
        "wordpress_url": "https://now0930.pe.kr/wordpress/example/",
        "source_url": "https://now0930.pe.kr/wordpress/example/",
        "title": "Reference", "version": "v1", "page": None,
        "section": None, "updated_at": None, "verification_status": "unverified",
    }
    master["sources"] = [reference]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _write_sources(root, master)
        bundle = root / "data/wordpress_topic_packs" / f"{master['topic_id']}.json"
        bundle.parent.mkdir(parents=True)
        bundle.write_text(json.dumps({
            "topic_id": master["topic_id"], "private": True,
            "sources": [{
                "source_id": "wp-post:42", "source_type": "wordpress_post", "wordpress_url": reference["wordpress_url"],
                "extraction_status": "extracted", "extraction_method": "wordpress_wxr_html",
                "extracted_text": "content", "extracted_text_sha256": "0" * 64,
                "version": "v1",
            }],
        }), encoding="utf-8")
        try:
            project_training(root, master)
        except ValueError as exc:
            assert "hash mismatch" in str(exc)
        else:
            raise AssertionError("source material with a mismatched content hash must fail closed")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"TRAINING_DIAGNOSIS_PROJECTION_TESTS={len(tests)}_PASS")
