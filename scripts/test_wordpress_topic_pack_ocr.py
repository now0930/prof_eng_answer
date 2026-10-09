from __future__ import annotations

import hashlib
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import wordpress_catalog as catalog
import build_wordpress_topic_packs as builder
from study.wordpress_topic_pack import load_wordpress_topic_pack


def test_image_candidate_scope_and_ocr_indexing() -> None:
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "catalog.sqlite3"
        connection = catalog.initialize_database(database)
        run_id = connection.execute(
            "INSERT INTO sync_runs(started_at,category_url,category_id) VALUES('now','https://example.org',1)"
        ).lastrowid
        connection.execute("""INSERT INTO sources(source_id,source_type,source_url,title,first_party,extraction_status)
            VALUES('first','image','https://now0930.pe.kr/wordpress/wp-content/uploads/first.png','first.png',1,'metadata_only'),
                  ('external','image','https://external.example/image.png','external.png',0,'metadata_only')""")
        connection.commit()
        assert [row[0] for row in catalog.first_party_image_ocr_candidates(connection)] == ["first"]
        png = b"\x89PNG\r\n\x1a\nmock"
        with patch.object(catalog, "_request", return_value=(png, {"ETag": "v1"})) as request, \
             patch.object(catalog, "image_text", return_value="한글 OCR evidence") as ocr:
            assert catalog.index_first_party_images(
                connection, run_id, tesseract="unused", tessdata=None,
                language="kor+eng", delay=0,
            ) == (1, 0)
            request.assert_called_once()
            assert request.call_args.kwargs["first_party_only"] is True
            ocr.assert_called_once_with(png, tesseract="unused", language="kor+eng", tessdata=None)
        row = connection.execute(
            "SELECT extraction_status,extraction_method,extracted_text,content_sha256 FROM sources WHERE source_id='first'"
        ).fetchone()
        assert row == ("extracted", "tesseract_ocr", "한글 OCR evidence", hashlib.sha256(png).hexdigest())
        assert connection.execute("SELECT text FROM source_search WHERE source_id='first'").fetchone()[0] == "한글 OCR evidence"
        connection.close()


def test_private_topic_pack_contains_linked_ocr_and_learning_consumer_reads_it() -> None:
    with tempfile.TemporaryDirectory() as directory:
        repo = Path(directory)
        database = repo / "catalog.sqlite3"
        connection = catalog.initialize_database(database)
        run_id = connection.execute(
            "INSERT INTO sync_runs(started_at,category_url,category_id) VALUES('now','https://example.org',1)"
        ).lastrowid
        connection.execute("""INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,content_html,content_text,
            tags_json,categories_json,content_sha256,last_seen_run)
            VALUES(1,1,'post','https://now0930.pe.kr/wordpress/post/','Post','','','Post context','[]','[]','hash',?)""", (run_id,))
        connection.executemany("""INSERT INTO sources(source_id,source_type,source_url,title,first_party,
            version,content_sha256,fetch_status,extraction_status,extraction_method,page_count,extracted_text)
            VALUES(?,?,?,?,?,'v1','hash','available','extracted',?, ?,?)""", [
                ("wp-post:1", "wordpress_post", "https://now0930.pe.kr/wordpress/post/", "Post", 1, "wordpress_rest_html", None, "Post context"),
                ("image:1", "image", "https://now0930.pe.kr/wordpress/wp-content/uploads/diagram.png", "Diagram", 1, "tesseract_ocr", 1, "Diagram OCR text"),
                ("pdf:external", "pdf", "https://external.example/file.pdf", "External", 0, "metadata_only", None, "must not enter pack"),
            ])
        connection.executemany("INSERT INTO post_sources VALUES(1,?, ?,?)", [("wp-post:1", "post", 0), ("image:1", "diagram", 1), ("pdf:external", "pdf", 2)])
        connection.execute("INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence) VALUES(1,'topic_alpha','approved',1,'[]','reviewed')")
        connection.execute("INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence) VALUES(1,'topic_beta','approved',1,'[]','reviewed')")
        connection.commit()
        connection.close()
        output_directory = repo / "data" / "wordpress_topic_packs"
        output_directory.mkdir(parents=True)
        untouched = output_directory / "topic_beta.json"
        untouched.write_text("preserve this unrelated pack", encoding="utf-8")
        with patch.object(builder, "ROOT", repo):
            stats = builder.build_topic_packs(
                database,
                output_directory,
                topic_ids=["topic_alpha"],
            )
        assert stats["topics"] == 1 and stats["image_sources"] == 1
        assert untouched.read_text(encoding="utf-8") == "preserve this unrelated pack"
        pack = load_wordpress_topic_pack(repo, "topic_alpha")
        assert pack is not None and pack["private"] is True
        assert [source["source_id"] for source in pack["sources"]] == ["wp-post:1", "image:1"], pack
        assert pack["sources"][1]["extracted_text"] == "Diagram OCR text"
        assert all(source["verification_status"] == "unverified" for source in pack["sources"])
        try:
            builder.build_topic_packs(database, repo / "data" / "public")
        except ValueError:
            pass
        else:
            raise AssertionError("Topic OCR content escaped the private data directory")


if __name__ == "__main__":
    test_image_candidate_scope_and_ocr_indexing()
    test_private_topic_pack_contains_linked_ocr_and_learning_consumer_reads_it()
    print("WORDPRESS_TOPIC_PACK_OCR_TESTS=2_PASS")
