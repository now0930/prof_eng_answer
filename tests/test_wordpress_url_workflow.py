"""Offline regression tests for WordPress permalink intake and its approval boundaries."""
from __future__ import annotations

from argparse import Namespace
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
from test_master_topic_pack_schema import _valid_record
import wordpress_catalog as catalog
import wordpress_url_workflow as workflow


URL = "https://now0930.pe.kr/wordpress/pressure-sensor/"
TOPIC_ID = "pressure_sensor"


def post_payload(*, version: int = 1, assets: bool = True) -> dict:
    attachments = (
        '<img src="https://now0930.pe.kr/wordpress/wp-content/uploads/diagram.png">'
        '<a href="https://thirdparty.example/report.pdf">external PDF</a>'
        if assets else ""
    )
    return {
        "id": 101,
        "slug": "pressure-sensor",
        "link": URL,
        "categories": [7],
        "tags": [],
        "title": {"rendered": "Pressure Sensor"},
        "excerpt": {"rendered": "Pressure measurement"},
        "content": {"rendered": f"<p>Pressure sensor operating principle v{version}</p>{attachments}"},
        "date_gmt": "2026-11-01T00:00:00",
        "modified_gmt": f"2026-11-{version:02d}T00:00:00",
        "featured_media": 0,
        "_embedded": {"wp:term": []},
    }


def test_only_configured_post_permalink_is_accepted():
    normalized, slug = workflow.normalize_post_url(URL)
    assert (normalized, slug) == (URL, "pressure-sensor")
    for forbidden in (
        "http://now0930.pe.kr/wordpress/pressure-sensor/",
        "https://external.example/wordpress/pressure-sensor/",
        "https://now0930.pe.kr.evil.example/wordpress/pressure-sensor/",
        "https://now0930.pe.kr/wordpress/category/pressure-sensor/",
        "https://now0930.pe.kr/wordpress/pressure-sensor/?draft=true",
        "https://now0930.pe.kr/wordpress/%252e%252e/",
        "https://user:pass@now0930.pe.kr/wordpress/pressure-sensor/",
    ):
        with pytest.raises(ValueError):
            workflow.normalize_post_url(forbidden)


def test_api_post_identity_and_category_checked_before_database_writes():
    body = json.dumps([post_payload()], ensure_ascii=False).encode()
    with patch.object(catalog, "_request", return_value=(body, {})), \
         patch.object(catalog, "discover_category_id", return_value=7):
        item, category_id = workflow.fetch_wordpress_post(URL)
        assert item["id"] == 101 and category_id == 7
    outsider = post_payload()
    outsider["categories"] = [999]
    with patch.object(catalog, "_request", return_value=(json.dumps([outsider]).encode(), {})), \
         patch.object(catalog, "discover_category_id", return_value=7):
        with pytest.raises(ValueError, match="outside"):
            workflow.fetch_wordpress_post(URL)
    spoof = post_payload()
    spoof["link"] = "https://now0930.pe.kr/wordpress/different/"
    with patch.object(catalog, "_request", return_value=(json.dumps([spoof]).encode(), {})):
        with pytest.raises(ValueError, match="exactly one"):
            workflow.fetch_wordpress_post(URL)


def environment(tmp_path, *, assets=True):
    root = tmp_path / "checkout"
    topic_dir = root / "rubrics" / "topic_packs" / TOPIC_ID
    topic_dir.mkdir(parents=True)
    (topic_dir / "README.md").write_text(
        "# Pressure Sensor\n\nPrinciples and measurement ranges.\n", encoding="utf-8"
    )
    args = Namespace(
        url=URL, database=root / "data" / "wordpress_sources.sqlite3",
        topic_root=topic_dir.parent,
        cache=root / "data" / "wordpress_topic_match_cache.sqlite3",
        backup_dir=tmp_path / "private_backups",
        offline=False, skip_ocr=True, refresh_assets=False, skip_learning=False,
        build_learning=False, candidate_limit=12, topic_id=None,
        decision=None, reviewer=None, evidence=None,
    )
    topic = [{"topic_id": TOPIC_ID, "title": "Pressure Sensor",
              "terms": {"pressure", "sensor"}}]
    return root, args, topic


def test_single_url_intake_idempotent_and_review_is_explicit(tmp_path):
    root, args, topics = environment(tmp_path)
    current_post = post_payload()
    with patch.object(workflow, "ROOT", root), \
         patch.object(workflow, "REPORT_DIR", root / "data" / "wordpress_url_intake"), \
         patch.object(catalog, "ROOT", root), \
         patch.object(catalog, "topic_catalog", return_value=topics), \
         patch.object(workflow, "fetch_wordpress_post", side_effect=lambda *_: (current_post, 7)):
        first, first_file = workflow.run(args)
        assert first["source_change"] == "new" and first["backup_path"] is None
        assert first["grading_files_modified"] is False
        assert first_file.stat().st_mode & 0o777 == 0o600
        assert first["topic_retrieval"]["retrieval_only"] is True
        assert not any(link["status"] == "approved" for link in first["topic_links"])
        sources = workflow.post_sources(args.database, 101)
        assert any(s["source_type"] == "image" and s["first_party"] for s in sources)
        assert any(s["source_type"] == "pdf" and not s["first_party"] for s in sources)
        with sqlite3.connect(args.database) as con:
            runs_before = con.execute("SELECT COUNT(*) FROM sync_runs").fetchone()[0]
        second, _ = workflow.run(args)
        assert second["source_change"] == "unchanged"
        assert second["backup_path"] is None
        with sqlite3.connect(args.database) as con:
            assert con.execute("SELECT COUNT(*) FROM sync_runs").fetchone()[0] == runs_before

        args.offline = True
        args.topic_id = TOPIC_ID
        args.decision = "approve"
        args.reviewer = "reviewer:source-checked"
        args.evidence = "Section 1: pressure sensor physical operating principle"
        approved, _ = workflow.run(args)
        assert approved["topic_links"][0]["status"] == "approved"
        assert approved["topic_links"][0]["reviewed_by"] == args.reviewer
        assert approved["source_proposals"]
        assert all(p["status"] in {"waiting_for_master", "pending_approval", "applied"}
                   for p in approved["source_proposals"])
        assert approved["backup_path"] is not None
        assert Path(approved["backup_path"]).is_file()
        again, _ = workflow.run(args)
        assert again["topic_links"][0]["status"] == "approved"
        assert again["backup_path"] is None
        args.decision = "reject"
        with pytest.raises(ValueError, match="overwritten"):
            workflow.run(args)
        assert workflow.post_links(args.database, 101)[0]["status"] == "approved"

        args.decision = None
        args.offline = False
        args.topic_id = None
        current_post = post_payload(version=2)
        changed, _ = workflow.run(args)
        assert changed["source_change"] == "changed"
        assert changed["backup_path"] is not None
        assert workflow.post_links(args.database, 101)[0]["status"] == "approved"


def test_asset_scope_excludes_unrelated_and_external_media(tmp_path):
    database = tmp_path / "db.sqlite3"
    con = catalog.initialize_database(database)
    con.executemany(
        """INSERT INTO sources(source_id,source_type,source_url,title,first_party,extraction_status)
           VALUES(?,?,?,?,?,?)""", [
            ("pdf-one", "pdf", "https://now0930.pe.kr/wordpress/wp-content/uploads/one.pdf",
             "one", 1, "pending"),
            ("pdf-other", "pdf", "https://now0930.pe.kr/wordpress/wp-content/uploads/other.pdf",
             "other", 1, "pending"),
            ("image-one", "image", "https://now0930.pe.kr/wordpress/wp-content/uploads/one.png",
             "one", 1, "metadata_only"),
            ("image-other", "image", "https://now0930.pe.kr/wordpress/wp-content/uploads/other.png",
             "other", 1, "metadata_only"),
            ("external", "pdf", "https://thirdparty.example/external.pdf",
             "external", 0, "pending"),
        ],
    )
    assert [x[0] for x in catalog.first_party_pdf_ocr_candidates(
        con, limit=None, refresh_changed=False, source_ids={"pdf-one", "external"}
    )] == ["pdf-one"]
    assert [x[0] for x in catalog.first_party_image_ocr_candidates(
        con, source_ids={"image-one", "external"}
    )] == ["image-one"]
    assert catalog.first_party_pdf_ocr_candidates(
        con, limit=None, refresh_changed=False, source_ids=set()
    ) == []
    assert catalog.first_party_image_ocr_candidates(con, source_ids=set()) == []
    con.close()


def test_learning_bundle_preserves_other_approved_posts(tmp_path):
    root, args, topics = environment(tmp_path, assets=False)
    post = post_payload(assets=False)
    with patch.object(workflow, "ROOT", root), \
         patch.object(workflow, "REPORT_DIR", root / "data" / "wordpress_url_intake"), \
         patch.object(catalog, "ROOT", root), \
         patch.object(catalog, "topic_catalog", return_value=topics), \
         patch.object(workflow, "fetch_wordpress_post", return_value=(post, 7)), \
         patch.object(workflow.bundle_builder, "ROOT", root):
        workflow.run(args)
        with sqlite3.connect(args.database) as con:
            run_id = con.execute("SELECT run_id FROM sync_runs LIMIT 1").fetchone()[0]
            con.execute(
                "UPDATE topic_links SET status='approved',evidence='section verified' WHERE post_id=101"
            )
            second_url = "https://now0930.pe.kr/wordpress/second/"
            con.execute(
                """INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,content_html,
                   content_text,tags_json,categories_json,content_sha256,last_seen_run)
                   VALUES(102,7,'second',?,'Pressure Sensor Other','','','Sensor other',
                          '[]','[]','hash-two',?)""", (second_url, run_id)
            )
            con.execute(
                """INSERT INTO sources(source_id,source_type,source_url,title,first_party,version,
                   content_sha256,extraction_status,extracted_text)
                   VALUES('wp-post:102','wordpress_post',?,'Other',1,'hash-two','hash-two',
                          'extracted','Sensor other')""", (second_url,)
            )
            con.execute(
                "INSERT INTO post_sources VALUES(102,'wp-post:102','other',0)"
            )
            con.execute(
                """INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence)
                   VALUES(102,?,'approved',1,'[]','reviewed')""", (TOPIC_ID,)
            )
        master_dir = root / "master_topic_packs"
        master_dir.mkdir(parents=True)
        digest = hashlib.sha256(post["content"]["rendered"].encode()).hexdigest()
        master = _valid_record()
        master["topic_id"] = TOPIC_ID
        source_root = f"rubrics/topic_packs/{TOPIC_ID}"
        master["legacy_topic_pack"]["source_root"] = source_root
        for key in master["legacy_topic_pack"]["source_files"]:
            master["legacy_topic_pack"]["source_files"][key] = f"{source_root}/{key}.json"
        master["sources"] = [{
            "source_id": "wp-post:101", "source_type": "wordpress_post",
            "wordpress_url": URL, "source_url": URL, "title": "Pressure sensor",
            "version": digest, "page": None, "section": None,
            "updated_at": None, "verification_status": "unverified",
        }]
        (master_dir / f"{TOPIC_ID}.json").write_text(
            json.dumps(master), encoding="utf-8"
        )
        args.offline = True
        args.build_learning = True
        report, _ = workflow.run(args)
        assert report["learning"]["status"] == "bundle_built_check_review_consumer"
        private_pack = root / "data" / "wordpress_topic_packs" / f"{TOPIC_ID}.json"
        package = json.loads(private_pack.read_text(encoding="utf-8"))
        assert {record["post_id"] for record in package["sources"]} == {101, 102}
        assert all(record["verification_status"] == "unverified"
                   for record in package["sources"])


def test_review_requires_source_grounded_evidence_and_offline_mode(tmp_path):
    _, args, _ = environment(tmp_path)
    args.decision = "approve"
    args.topic_id = TOPIC_ID
    args.reviewer = "reviewer"
    args.evidence = "too short"
    with pytest.raises(ValueError, match="offline"):
        workflow.run(args)
    args.offline = True
    with pytest.raises(ValueError, match="at least 12"):
        workflow.run(args)


def test_changed_post_ocr_is_scoped_to_its_own_media(tmp_path):
    root, args, topics = environment(tmp_path)
    args.skip_ocr = True
    post = post_payload(version=1)
    with patch.object(workflow, "ROOT", root), \
         patch.object(workflow, "REPORT_DIR", root / "data" / "wordpress_url_intake"), \
         patch.object(catalog, "ROOT", root), \
         patch.object(catalog, "topic_catalog", return_value=topics), \
         patch.object(workflow, "fetch_wordpress_post", side_effect=lambda *_: (post, 7)):
        workflow.run(args)
        with sqlite3.connect(args.database) as con:
            con.execute(
                """INSERT INTO sources(source_id,source_type,source_url,title,first_party,extraction_status)
                   VALUES('unrelated-image','image',
                          'https://now0930.pe.kr/wordpress/wp-content/uploads/unrelated.png',
                          'other',1,'metadata_only')"""
            )
        post = post_payload(version=2)
        args.skip_ocr = False
        png = b"\x89PNG\r\n\x1a\nfake_png"
        with patch.object(workflow.shutil, "which", return_value="tesseract"), \
             patch.object(catalog, "_request", return_value=(png, {"ETag": "v2"})) as request, \
             patch.object(catalog, "image_text", return_value="Pressure sensor OCR evidence"):
            report, _ = workflow.run(args)
        assert report["ingestion"]["images_processed"] == 1
        assert report["ingestion"]["image_errors"] == 0
        request.assert_called_once()
        assert "diagram.png" in request.call_args.args[0]
        assert request.call_args.kwargs["first_party_only"] is True
        with sqlite3.connect(args.database) as con:
            assert con.execute(
                "SELECT extraction_status FROM sources WHERE source_id='unrelated-image'"
            ).fetchone()[0] == "metadata_only"
            text = con.execute(
                """SELECT extracted_text FROM sources
                   WHERE source_url LIKE '%/diagram.png'"""
            ).fetchone()[0]
            assert text == "Pressure sensor OCR evidence"


def test_new_text_only_post_does_not_require_ocr_binaries(tmp_path):
    root, args, topics = environment(tmp_path)
    args.skip_ocr = False
    no_media_post = post_payload(assets=False)
    with patch.object(workflow, "ROOT", root), \
         patch.object(workflow, "REPORT_DIR", root / "data" / "wordpress_url_intake"), \
         patch.object(catalog, "ROOT", root), \
         patch.object(catalog, "topic_catalog", return_value=topics), \
         patch.object(workflow, "fetch_wordpress_post", return_value=(no_media_post, 7)), \
         patch.object(workflow.shutil, "which", return_value=None):
        report, _ = workflow.run(args)
    assert report["source_change"] == "new"
    assert report["ingestion"]["warnings"] == []
    assert report["ingestion"]["pdf_processed"] == 0
    assert report["ingestion"]["images_processed"] == 0


def test_first_party_embedded_pdf_is_discovered_without_external_fetch():
    markup = (
        '<iframe src="https://now0930.pe.kr/wordpress/wp-content/uploads/note.pdf#page=2"></iframe>'
        '<object data="https://now0930.pe.kr/wordpress/wp-content/uploads/handwritten.pdf"></object>'
        '<iframe src="https://www.youtube.com/embed/video"></iframe>'
    )
    _, urls = catalog._plain_text(markup)
    kinds = {
        catalog.canonical_url(url): catalog.classify_source(catalog.canonical_url(url))
        for url, _ in urls
    }
    assert kinds["https://now0930.pe.kr/wordpress/wp-content/uploads/note.pdf"] == "pdf"
    assert kinds["https://now0930.pe.kr/wordpress/wp-content/uploads/handwritten.pdf"] == "pdf"
    assert "pdf" not in [kind for url, kind in kinds.items() if "youtube" in url]
