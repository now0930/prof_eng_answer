#!/usr/bin/env python3
"""Safely ingest one WordPress permalink and resume its Topic/learning workflow.

This workflow never auto-approves a Topic link, Master source or grading fact.
The private catalog, immutable review evidence and canonical bank stay separate.
"""
from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
from urllib.parse import quote, unquote, urlsplit
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import wordpress_catalog as catalog
import match_wordpress_posts_to_topic_packs as matcher
import build_wordpress_topic_packs as bundle_builder
from study.master_topic_pack import validate_master_topic_pack

DB_DEFAULT = ROOT / "data" / "wordpress_sources.sqlite3"
REPORT_DIR = ROOT / "data" / "wordpress_url_intake"
BACKUP_DIR = Path.home() / "hermes" / "private_backups" / "prof_eng_answer" / "wordpress_url_intake"
SCHEMA_VERSION = "wordpress-url-workflow-v1"
MAX_API_BYTES = 16 * 1024 * 1024
BLOCKED_PREFIXES = {"category", "tag", "wp-json", "wp-admin", "wp-content", "feed", "author", "page"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_post_url(value: str) -> tuple[str, str]:
    """Validate against SSRF and return a stable permalink identity and slug."""
    parsed = urlsplit(value.strip())
    if (parsed.scheme != "https" or parsed.hostname != catalog.ALLOWED_HOST
            or parsed.username or parsed.password or parsed.port is not None
            or parsed.query or parsed.fragment):
        raise ValueError("only plain HTTPS WordPress permalinks on the configured host are accepted")
    path = unquote(parsed.path)
    if re.search(r"[\x00-\x1f\x7f]", path) or "%" in path:
        raise ValueError("ambiguous or doubly encoded post path")
    parts = [part for part in path.split("/") if part]
    if (len(parts) != 2 or parts[0] != "wordpress"
            or parts[1].lower() in BLOCKED_PREFIXES
            or parts[1] in {".", ".."}):
        raise ValueError("expected a single post permalink under /wordpress/<slug>/")
    return f"https://{catalog.ALLOWED_HOST}/wordpress/{parts[1]}/", parts[1]


def fetch_wordpress_post(url: str) -> tuple[dict, int]:
    expected_url, slug = normalize_post_url(url)
    api = (f"https://{catalog.ALLOWED_HOST}/wordpress/wp-json/wp/v2/posts"
           f"?slug={quote(slug, safe='')}&per_page=100&_embed=1")
    payload, _ = catalog._request(api, max_bytes=MAX_API_BYTES, first_party_only=True)
    posts = json.loads(payload.decode("utf-8"))
    if not isinstance(posts, list):
        raise ValueError("WordPress posts API returned an unexpected document")
    matching = []
    for item in posts:
        if not isinstance(item, dict):
            continue
        try:
            actual_url, _ = normalize_post_url(item.get("link", ""))
        except (ValueError, TypeError):
            continue
        if actual_url == expected_url:
            matching.append(item)
    if len(matching) != 1:
        raise ValueError("WordPress permalink did not resolve to exactly one REST post")
    post = matching[0]
    category_id = catalog.discover_category_id(catalog.DEFAULT_CATEGORY_URL)
    if not isinstance(post.get("categories"), list) or category_id not in post["categories"]:
        raise ValueError("post is outside the configured technical-study WordPress category")
    if not isinstance(post.get("id"), int) or post["id"] <= 0:
        raise ValueError("WordPress REST response lacks a valid post ID")
    if not isinstance(post.get("content", {}).get("rendered"), str):
        raise ValueError("WordPress REST response lacks rendered post content")
    return post, category_id


def read_post(database: Path, *, post_id: int | None = None, url: str | None = None) -> dict | None:
    if not database.is_file():
        return None
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        if post_id is not None:
            row = connection.execute(
                "SELECT * FROM posts WHERE post_id=?", (post_id,)
            ).fetchone()
            return dict(row) if row else None
        for row in connection.execute("SELECT * FROM posts ORDER BY post_id"):
            try:
                normalized, _ = normalize_post_url(row["url"])
            except (ValueError, TypeError):
                continue
            if normalized == url:
                return dict(row)
        return None
    finally:
        connection.close()


def needs_ingest(old: dict | None, post: dict) -> bool:
    if old is None:
        return True
    digest = hashlib.sha256(post["content"]["rendered"].encode("utf-8")).hexdigest()
    title = catalog._plain_text(post["title"]["rendered"])[0].strip()
    excerpt = catalog._plain_text(post.get("excerpt", {}).get("rendered", ""))[0].strip()
    tags, categories = catalog.post_taxonomy(post)
    return any((
        old["content_sha256"] != digest,
        old["title"] != title,
        old["excerpt"] != excerpt,
        old["modified_at"] != (post.get("modified_gmt") or post.get("modified")),
        old["slug"] != post.get("slug", ""),
        old["tags_json"] != json.dumps(tags, ensure_ascii=False),
        old["categories_json"] != json.dumps(categories, ensure_ascii=False),
        old["featured_media_id"] != (post.get("featured_media") or None),
    ))


def post_sources(database: Path, post_id: int) -> list[dict]:
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """SELECT DISTINCT s.source_id,s.source_type,s.source_url,s.first_party,
                      s.version,s.content_sha256,s.extraction_status,s.page_count
               FROM post_sources ps JOIN sources s ON s.source_id=ps.source_id
               WHERE ps.post_id=? ORDER BY s.source_id""", (post_id,)
        )
        return [dict(row) for row in rows]
    finally:
        connection.close()


def post_links(database: Path, post_id: int) -> list[dict]:
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute(
            """SELECT topic_id,status,reviewed_by,reviewed_at,evidence
               FROM topic_links WHERE post_id=? ORDER BY topic_id""", (post_id,)
        )]
    finally:
        connection.close()


def post_proposals(database: Path, post_id: int) -> list[dict]:
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute(
            """SELECT DISTINCT p.proposal_id,p.topic_id,p.source_id,p.status,p.base_revision
               FROM source_update_proposals p
               JOIN post_sources ps ON ps.source_id=p.source_id
               WHERE ps.post_id=? ORDER BY p.topic_id,p.source_id,p.proposal_id""", (post_id,)
        )]
    finally:
        connection.close()


@contextmanager
def workflow_lock():
    REPORT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    REPORT_DIR.chmod(0o700)
    lock_path = REPORT_DIR / ".workflow.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            yield
    finally:
        pass


def backup_database(database: Path, backup_dir: Path, post_id: int) -> str | None:
    if not database.is_file():
        return None
    backup_dir = backup_dir.resolve()
    if backup_dir.is_relative_to(ROOT.resolve()):
        raise ValueError("private SQLite backups must be stored outside the public repository")
    backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    backup_dir.chmod(0o700)
    filename = f"wordpress_{post_id}_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}_{uuid4().hex[:8]}.sqlite3"
    target = backup_dir / filename
    temporary = backup_dir / ("." + filename + ".partial")
    try:
        with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as original:
            with closing(sqlite3.connect(temporary)) as snapshot:
                original.backup(snapshot)
                if snapshot.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
                    raise RuntimeError("private SQLite backup failed integrity check")
        os.chmod(temporary, 0o600)
        os.replace(temporary, target)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return str(target)


def pending_ocr(source_rows: list[dict], refresh: bool) -> tuple[bool, bool]:
    pdf_states = {"pending", "error", "stale"}
    image_states = {"pending", "error", "stale", "metadata_only"}
    pdf = any(
        row["first_party"] and row["source_type"] == "pdf"
        and (row["extraction_status"] in pdf_states or refresh)
        for row in source_rows
    )
    images = any(
        row["first_party"] and row["source_type"] == "image"
        and (row["extraction_status"] in image_states or refresh)
        for row in source_rows
    )
    return pdf, images


def ingest_post(database: Path, post: dict, category_id: int, *, write_post: bool,
                do_pdf: bool, do_image: bool, refresh_assets: bool) -> dict:
    """Re-use catalog ingestion and OCR with strictly post-scoped source IDs."""
    summary = {"post_written": write_post, "pdf_processed": 0, "pdf_errors": 0,
               "images_processed": 0, "image_errors": 0, "warnings": []}
    conn = catalog.initialize_database(database)
    try:
        run_id = int(conn.execute(
            """INSERT INTO sync_runs(started_at,category_url,category_id,expected_posts)
               VALUES(?,?,?,1)""",
            (utc_now(), catalog.DEFAULT_CATEGORY_URL, category_id),
        ).lastrowid)
        if write_post:
            topics = catalog.topic_catalog()
            for item in topics:
                conn.execute(
                    """INSERT INTO topics(topic_id,title,terms_json) VALUES(?,?,?)
                       ON CONFLICT(topic_id) DO UPDATE SET title=excluded.title,
                         terms_json=excluded.terms_json""",
                    (item["topic_id"], item["title"], json.dumps(sorted(item["terms"]), ensure_ascii=False)),
                )
            catalog._store_post(conn, post, category_id, run_id, topics)
        conn.commit()
        source_ids = {
            row[0] for row in conn.execute(
                "SELECT DISTINCT source_id FROM post_sources WHERE post_id=?", (post["id"],)
            )
        }
        # A new post can contain no assets; do not report missing OCR tools
        # unless there really is eligible media awaiting extraction.
        do_pdf = do_pdf and bool(catalog.first_party_pdf_ocr_candidates(
            conn, limit=None, refresh_changed=refresh_assets, source_ids=source_ids
        ))
        do_image = do_image and bool(catalog.first_party_image_ocr_candidates(
            conn, refresh_changed=refresh_assets, source_ids=source_ids
        ))
        tesseract = shutil.which("tesseract")
        if (do_pdf or do_image) and not tesseract:
            summary["warnings"].append("OCR pending: tesseract is not installed")
            do_pdf = do_image = False
        pdf_utils = ("pdfinfo", "pdftotext", "pdftoppm")
        if do_pdf and any(not shutil.which(name) for name in pdf_utils):
            summary["warnings"].append("PDF OCR pending: poppler-utils are not installed")
            do_pdf = False
        if do_pdf:
            processed, errors = catalog.index_first_party_pdfs(
                conn, run_id, tesseract=tesseract, tessdata=None,
                language="kor+eng", delay=0.15, refresh_changed=refresh_assets,
                source_ids=source_ids,
            )
            summary.update(pdf_processed=processed, pdf_errors=errors)
        if do_image:
            processed, errors = catalog.index_first_party_images(
                conn, run_id, tesseract=tesseract, tessdata=None,
                language="kor+eng", delay=0.15, refresh_changed=refresh_assets,
                source_ids=source_ids,
            )
            summary.update(images_processed=processed, image_errors=errors)
        conn.execute(
            """UPDATE sync_runs SET finished_at=?,posts_seen=1,
               sources_seen=?,pdfs_ocred=?,images_ocred=?,errors=? WHERE run_id=?""",
            (utc_now(), len(source_ids), summary["pdf_processed"],
             summary["images_processed"], summary["pdf_errors"] + summary["image_errors"], run_id),
        )
        conn.commit()
        return summary
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def master_link_state(topic_id: str, sources: list[dict]) -> dict:
    path = ROOT / "master_topic_packs" / f"{topic_id}.json"
    if not path.is_file():
        return {"status": "missing_master", "missing_or_stale": []}
    try:
        master = json.loads(path.read_text(encoding="utf-8"))
        validate_master_topic_pack(master)
    except (OSError, ValueError, TypeError, KeyError):
        return {"status": "invalid_master", "missing_or_stale": []}
    refs = {item.get("source_id"): item for item in master.get("sources", [])}
    missing = []
    for source in sources:
        if source["source_type"] not in {"wordpress_post", "pdf", "image"}:
            continue
        if not source["first_party"]:
            continue
        ref = refs.get(source["source_id"])
        if (not ref or ref.get("source_url") != source["source_url"]
                or ref.get("version") != (source["version"] or "unversioned")):
            missing.append(source["source_id"])
    ocr_pending = [
        source["source_id"] for source in sources
        if source["source_type"] in {"pdf", "image"} and source["first_party"]
        and source["extraction_status"] != "extracted"
    ]
    if missing:
        return {"status": "pending_master_source_approval", "missing_or_stale": missing,
                "ocr_pending": ocr_pending}
    if ocr_pending:
        return {"status": "pending_ocr", "missing_or_stale": [],
                "ocr_pending": ocr_pending}
    return {"status": "current", "missing_or_stale": [], "ocr_pending": []}


def write_private_report(report: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    REPORT_DIR.chmod(0o700)
    name = f"post_{report['post_id']}_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}_{uuid4().hex[:8]}.json"
    path = REPORT_DIR / name
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, sort_keys=True, indent=2)
        file.write("\n")
    return path


def run(args: argparse.Namespace) -> tuple[dict, Path]:
    identity, _ = normalize_post_url(args.url)
    database = args.database.resolve()
    if not args.offline and args.decision:
        raise ValueError("link review requires --offline to prevent a simultaneous source refresh")
    if args.decision and not (args.topic_id and args.reviewer and args.evidence):
        raise ValueError("link decisions require --topic-id, --reviewer, and --evidence")
    if args.evidence and len(args.evidence.strip()) < 12:
        raise ValueError("review evidence must include a concrete source locator and be at least 12 characters")
    if args.topic_id and not args.decision:
        raise ValueError("--topic-id requires --decision")
    if args.decision and args.decision not in {"approve", "reject"}:
        raise ValueError("invalid review decision")
    with workflow_lock():
        if args.offline:
            stored = read_post(database, url=identity)
            if not stored:
                raise ValueError("URL is not in the private catalog; run online intake first")
            post_id = stored["post_id"]
            category_id = stored["category_id"]
            input_version = stored["content_sha256"]
            source_change = "offline_existing"
        else:
            post, category_id = fetch_wordpress_post(args.url)
            post_id = post["id"]
            stored = read_post(database, post_id=post_id)
            if stored and normalize_post_url(stored["url"])[0] != identity:
                raise ValueError("post ID previously belonged to a different permalink; manual reconciliation needed")
            input_version = hashlib.sha256(post["content"]["rendered"].encode("utf-8")).hexdigest()
            source_change = ("new" if stored is None else
                             "changed" if needs_ingest(stored, post) else "unchanged")
        backup = None
        ingestion = {"post_written": False, "pdf_processed": 0, "pdf_errors": 0,
                     "images_processed": 0, "image_errors": 0, "warnings": []}
        if args.offline:
            if args.decision:
                before = next((link for link in post_links(database, post_id)
                               if link["topic_id"] == args.topic_id), None)
                desired = "approved" if args.decision == "approve" else "rejected"
                if not before or before["status"] != desired:
                    backup = backup_database(database, args.backup_dir, post_id)
                    catalog.review_topic_link(
                        database, post_id, args.topic_id, args.decision,
                        reviewed_by=args.reviewer, evidence=args.evidence,
                    )
        else:
            original_assets = post_sources(database, post_id) if stored else []
            pdf_needed, image_needed = pending_ocr(original_assets, args.refresh_assets)
            needs_write = source_change != "unchanged"
            if needs_write:
                # New/changed posts can introduce first-party PDF/image sources.
                pdf_needed = image_needed = not args.skip_ocr
            elif args.skip_ocr:
                pdf_needed = image_needed = False
            tesseract_available = shutil.which("tesseract") is not None
            available_pdf = tesseract_available and all(
                shutil.which(x) for x in ("pdfinfo", "pdftotext", "pdftoppm")
            )
            can_ocr = ((pdf_needed and available_pdf) or
                       (image_needed and tesseract_available))
            if needs_write or can_ocr:
                backup = backup_database(database, args.backup_dir, post_id)
                ingestion = ingest_post(
                    database, post, category_id, write_post=needs_write,
                    do_pdf=pdf_needed and not args.skip_ocr,
                    do_image=image_needed and not args.skip_ocr,
                    refresh_assets=args.refresh_assets,
                )
            elif (pdf_needed or image_needed) and not args.skip_ocr:
                ingestion["warnings"].append("OCR pending: local Tesseract/Poppler dependency missing")
        stored = read_post(database, post_id=post_id)
        if not stored:
            raise RuntimeError("catalog did not retain the target post")
        sources = post_sources(database, post_id)
        links = post_links(database, post_id)
        proposals = post_proposals(database, post_id)
        retrieval = matcher.retrieve_posts(
            database, args.topic_root, args.cache,
            candidate_limit=args.candidate_limit, post_ids={post_id},
        )
        post_results = retrieval["posts"]
        if len(post_results) != 1:
            raise RuntimeError("retrieval did not return the requested post")
        approved_topics = sorted(
            link["topic_id"] for link in links if link["status"] == "approved"
        )
        master_states = {
            topic_id: master_link_state(topic_id, sources) for topic_id in approved_topics
        }
        current_topics = sorted(
            topic_id for topic_id, state in master_states.items()
            if state["status"] == "current"
        )
        learning = {"status": "pending_approval", "built_topics": [], "stats": None}
        should_build = (not args.offline and not args.skip_learning) or args.build_learning
        if should_build and current_topics:
            # No post_ids: retain ALL approved posts for a Topic in the bundle.
            stats = bundle_builder.build_topic_packs(
                database, ROOT / "data" / "wordpress_topic_packs",
                topic_ids=current_topics,
            )
            learning = {"status": "bundle_built_check_review_consumer",
                        "built_topics": current_topics, "stats": stats}
        elif not approved_topics:
            learning["status"] = "pending_topic_link_review"
        elif current_topics:
            learning["status"] = "eligible_not_built"
        report = {
            "schema_version": SCHEMA_VERSION, "generated_at": utc_now(),
            "url": identity, "post_id": post_id, "source_version_or_hash": input_version,
            "source_change": source_change, "offline": args.offline,
            "backup_path": backup, "ingestion": ingestion,
            "sources": sources, "topic_links": links, "source_proposals": proposals,
            "topic_retrieval": {
                "retrieval_only": True, "candidate_count": len(post_results[0]["candidates"]),
                "candidates": post_results[0]["candidates"],
                "topic_index_sha256": retrieval["topic_index_sha256"],
            },
            "master_source_states": master_states, "learning": learning,
            "fact_triage": "requires_independent_source_verification; no automatic scoring promotion",
            "grading_files_modified": False, "master_files_modified": False,
            "next_action": (
                "resolve OCR errors/dependencies" if
                (ingestion["pdf_errors"] + ingestion["image_errors"] or ingestion["warnings"]) else
                "review Topic candidates with source locators" if not approved_topics else
                "review and separately approve pending Master source proposals" if
                any(x["status"] in {"waiting_for_master", "pending_approval"} for x in proposals)
                else "verify /review learning source and triage Fact claims independently"
            ),
        }
        report_path = write_private_report(report)
        return report, report_path


def main() -> int:
    # Catalog and search cache may contain the full source text.
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="one HTTPS permalink on now0930.pe.kr/wordpress")
    parser.add_argument("--database", type=Path, default=DB_DEFAULT)
    parser.add_argument("--topic-root", type=Path, default=ROOT / "rubrics" / "topic_packs")
    parser.add_argument("--cache", type=Path, default=ROOT / "data" / "wordpress_topic_match_cache.sqlite3")
    parser.add_argument("--backup-dir", type=Path, default=BACKUP_DIR)
    parser.add_argument("--offline", action="store_true", help="use only the existing catalog; no web requests")
    parser.add_argument("--skip-ocr", action="store_true", help="skip media OCR for this run")
    parser.add_argument("--refresh-assets", action="store_true", help="re-download unchanged first-party media")
    parser.add_argument("--skip-learning", action="store_true", help="do not rebuild eligible private bundles")
    parser.add_argument("--build-learning", action="store_true", help="explicitly rebuild eligible bundles when offline")
    parser.add_argument("--candidate-limit", type=int, default=12)
    parser.add_argument("--topic-id", help="existing Topic ID to review; only with --offline")
    parser.add_argument("--decision", choices=("approve", "reject"), help="explicit reviewed link decision")
    parser.add_argument("--reviewer", help="actual reviewer identity")
    parser.add_argument("--evidence", help="verifiable post section/formula/page locator and rationale")
    args = parser.parse_args()
    if args.candidate_limit < 1 or args.candidate_limit > 100:
        parser.error("--candidate-limit must be 1..100")
    try:
        report, path = run(args)
    except (ValueError, RuntimeError, OSError, sqlite3.Error) as error:
        parser.exit(2, f"WORDPRESS_URL_WORKFLOW=BLOCKED {type(error).__name__}: {error}\n")
    warnings = report["ingestion"]["warnings"]
    errors = report["ingestion"]["pdf_errors"] + report["ingestion"]["image_errors"]
    print(f"WORDPRESS_URL_WORKFLOW={'PARTIAL' if warnings or errors else 'REVIEW_REQUIRED'}")
    print(f"POST_ID={report['post_id']} SOURCE_CHANGE={report['source_change']}")
    print(f"TOPIC_CANDIDATES={report['topic_retrieval']['candidate_count']}")
    print(f"APPROVED_LINKS={sum(x['status']=='approved' for x in report['topic_links'])}")
    print(f"PRIVATE_REPORT={path}")
    print(f"NEXT_ACTION={report['next_action']}")
    return 2 if warnings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
