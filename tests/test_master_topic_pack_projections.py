from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.master_topic_pack import _apply_training_source_scopes, grading_compatibility_payload, project_grading, project_training
from test_master_topic_pack_schema import _valid_record


def test_grading_projection_matches_legacy_sources_without_mutation() -> None:
    with tempfile.TemporaryDirectory(prefix="master-topic-projection-") as temp_dir:
        _test_grading_projection_matches_legacy_sources_without_mutation(Path(temp_dir))


def _test_grading_projection_matches_legacy_sources_without_mutation(tmp_path: Path) -> None:
    master = _valid_record()
    expected = {}
    for key, relative in master["legacy_topic_pack"]["source_files"].items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"topic_id": master["topic_id"], "source_key": key, "content": [key]}
        path.write_text(json.dumps(payload), encoding="utf-8")
        expected[key] = payload

    original = copy.deepcopy(master)
    projected = project_grading(tmp_path, master)
    assert projected["projection_id"] == "grading-projection-v1"
    assert projected["authority"] == "existing_topic_pack"
    assert projected["topic_id"] == master["topic_id"]
    assert projected["sources"] == expected
    assert grading_compatibility_payload(tmp_path, master) == expected
    assert master == original

    projected["sources"]["fact_anchor"]["content"].append("projection-only")
    assert expected["fact_anchor"]["content"] == ["fact_anchor"]


def test_grading_projection_fails_on_mismatched_legacy_topic_id() -> None:
    with tempfile.TemporaryDirectory(prefix="master-topic-mismatch-") as temp_dir:
        _test_grading_projection_fails_on_mismatched_legacy_topic_id(Path(temp_dir))


def _test_grading_projection_fails_on_mismatched_legacy_topic_id(tmp_path: Path) -> None:
    master = _valid_record()
    for key, relative in master["legacy_topic_pack"]["source_files"].items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload_topic_id = "wrong_topic_id" if key == "logic_check" else master["topic_id"]
        path.write_text(json.dumps({"topic_id": payload_topic_id}), encoding="utf-8")
    try:
        project_grading(tmp_path, master)
    except ValueError as exc:
        assert "topic_id mismatch" in str(exc)
    else:
        raise AssertionError("projection accepted a source owned by another topic")


def test_training_scope_excludes_mixed_sources_and_selects_exact_pdf_pages() -> None:
    references = [
        {"source_id": "wp-post:mixed", "source_type": "wordpress_post", "training_scope": {
            "mode": "exclude", "reason": "스마트/전통형 혼합 원문은 합성 학습 섹션으로 대체"}},
        {"source_id": "wpurl:manual", "source_type": "pdf", "training_scope": {
            "mode": "pages", "reason": "전통 공압식 포지셔너 내용만 포함",
            "page_ranges": [{"start": 1, "end": 2}]}},
    ]
    materials = [
        {"source_id": "wp-post:mixed", "text": "P/P와 Smart Positioner 혼합 원문", "content_sha256": "raw"},
        {"source_id": "wpurl:manual", "source_type": "pdf",
         "text": "[Page 1]\n공압식 포지셔너\n[Page 2]\n기계식 피드백\n[Page 3]\n전자식 스마트 진단",
         "content_sha256": "raw-pdf"},
    ]
    included, excluded = _apply_training_source_scopes(materials, references)
    assert [item["source_id"] for item in included] == ["wpurl:manual"]
    assert included[0]["text"] == "[Page 1]\n공압식 포지셔너\n\n[Page 2]\n기계식 피드백"
    assert included[0]["content_sha256"] == "raw-pdf"
    assert included[0]["training_text_sha256"] == hashlib.sha256(included[0]["text"].encode("utf-8")).hexdigest()
    assert "스마트 진단" not in included[0]["text"]
    assert [(item["source_id"], item["exclusion_reason"]) for item in excluded] == [
        ("wp-post:mixed", "스마트/전통형 혼합 원문은 합성 학습 섹션으로 대체")
    ]


def test_training_scope_fails_closed_when_pdf_page_markers_are_missing() -> None:
    reference = {"source_id": "wpurl:manual", "source_type": "pdf", "training_scope": {
        "mode": "pages", "reason": "범위 제한", "page_ranges": [{"start": 1, "end": 2}]}}
    included, excluded = _apply_training_source_scopes(
        [{"source_id": "wpurl:manual", "source_type": "pdf", "text": "페이지 경계 없는 OCR", "content_sha256": "raw"}],
        [reference],
    )
    assert included == []
    assert excluded[0]["exclusion_reason"] == "PDF page markers did not permit safe scope extraction"


def test_training_projection_includes_only_master_linked_first_party_pdf_and_image_text() -> None:
    with tempfile.TemporaryDirectory(prefix="master-topic-training-media-") as temp_dir:
        root = Path(temp_dir)
        master = _valid_record()
        topic_id = master["topic_id"]
        post_url = "https://now0930.pe.kr/wordpress/example-post/"
        sources = [
            {
                "source_id": "wp-post:101",
                "source_type": "wordpress_post",
                "wordpress_url": post_url,
                "source_url": post_url,
                "title": "Source post",
                "version": "post-v1",
                "page": None,
                "section": None,
                "updated_at": "2026-10-01T00:00:00+00:00",
                "verification_status": "unverified",
            },
            {
                "source_id": "wpurl:pdf101",
                "source_type": "pdf",
                "wordpress_url": post_url,
                "source_url": "https://now0930.pe.kr/wordpress/wp-content/uploads/source.pdf",
                "title": "Source PDF",
                "version": "pdf-v1",
                "page": "1-2",
                "section": None,
                "updated_at": None,
                "verification_status": "unverified",
            },
            {
                "source_id": "wpurl:image101",
                "source_type": "image",
                "wordpress_url": post_url,
                "source_url": "https://now0930.pe.kr/wordpress/wp-content/uploads/source.png",
                "title": "Source image",
                "version": "image-v1",
                "page": None,
                "section": None,
                "updated_at": None,
                "verification_status": "unverified",
            },
            {
                "source_id": "wpurl:pdf_stale",
                "source_type": "pdf",
                "wordpress_url": post_url,
                "source_url": "https://now0930.pe.kr/wordpress/wp-content/uploads/old.pdf",
                "title": "Old source PDF",
                "version": "pdf-old-v1",
                "page": None,
                "section": None,
                "updated_at": None,
                "verification_status": "unverified",
            },
        ]
        master["sources"] = sources
        for key, relative in master["legacy_topic_pack"]["source_files"].items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"topic_id": topic_id, "source_key": key}), encoding="utf-8")

        texts = {
            "wp-post:101": ("wordpress_post", post_url, "HTML에 적힌 원문"),
            "wpurl:pdf101": ("pdf", sources[1]["source_url"], "PDF 방정식 OCR"),
            "wpurl:image101": ("image", sources[2]["source_url"], "이미지 도식 OCR"),
            "wpurl:pdf_stale": ("pdf", sources[3]["source_url"], "변경된 PDF - 승인 전 제외"),
            "unlinked:external": ("pdf", "https://external.example/file.pdf", "외부·미연결 자료"),
        }
        pack_sources = []
        for source_id, (source_type, source_url, text) in texts.items():
            version = next((item["version"] for item in sources if item["source_id"] == source_id), "external-v1")
            if source_id == "wpurl:pdf_stale":
                version = "pdf-new-v2"
            pack_sources.append({
                "source_id": source_id,
                "source_type": source_type,
                "topic_id": topic_id,
                "wordpress_url": post_url,
                "source_url": source_url,
                "version": version,
                "extraction_status": "extracted",
                "extraction_method": {
                    "wordpress_post": "wordpress_rest_html",
                    "pdf": "pdftotext",
                    "image": "tesseract_ocr",
                }[source_type],
                "extracted_text": text,
                "extracted_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "verification_status": "unverified",
            })
        bundle = root / "data" / "wordpress_topic_packs" / f"{topic_id}.json"
        bundle.parent.mkdir(parents=True, exist_ok=True)
        bundle.write_text(json.dumps({
            "schema_version": "wordpress-topic-pack-v1",
            "topic_id": topic_id,
            "private": True,
            "content_trust": "untrusted_source_text",
            "sources": pack_sources,
        }), encoding="utf-8")

        training = project_training(root, master)
        material_by_type = {item["source_type"]: item for item in training["source_materials"]}
        assert set(material_by_type) == {"wordpress_post", "pdf", "image"}
        assert material_by_type["pdf"]["text"] == "PDF 방정식 OCR"
        assert material_by_type["image"]["text"] == "이미지 도식 OCR"
        source_ids = {item["source_id"] for item in training["source_materials"]}
        assert "unlinked:external" not in source_ids
        assert "wpurl:pdf_stale" not in source_ids
        assert grading_compatibility_payload(root, master)["model_answer"]["source_key"] == "model_answer"


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"MASTER_TOPIC_PACK_PROJECTION_TESTS={len(tests)}_PASS")
