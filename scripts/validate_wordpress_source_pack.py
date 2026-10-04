#!/usr/bin/env python3
"""Read-only validation for the local WordPress Source Pack catalog."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE_TYPES = {"wordpress_post", "wordpress_page", "pdf", "image", "overleaf", "html", "other"}
STATUSES = {"available", "metadata_only", "error", "pending"}


def validate_source_pack(database: Path, master_root: Path | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "counts": {}}
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            errors.append(f"sqlite integrity_check={integrity}")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {"posts", "sources", "post_sources", "topics", "topic_links"}
        missing = required - tables
        if missing:
            errors.append(f"missing catalog tables: {sorted(missing)}")
            return {"valid": False, "errors": errors, "warnings": warnings, "counts": {}}
        source_rows = connection.execute(
            "SELECT source_id,source_type,source_url,first_party,fetch_status,extraction_status,extraction_method,extracted_text FROM sources"
        ).fetchall()
        for source_id, source_type, url, first_party, fetch_status, extraction_status, method, text in source_rows:
            if source_type not in SOURCE_TYPES:
                errors.append(f"{source_id}: unsupported source_type={source_type}")
            if not re.match(r"^https?://[^\s]+$", url or ""):
                errors.append(f"{source_id}: invalid source_url")
            if fetch_status not in STATUSES:
                errors.append(f"{source_id}: unsupported fetch_status={fetch_status}")
            if not first_party and (text or "").strip():
                errors.append(f"{source_id}: external source has extracted text")
            if first_party and extraction_status == "extracted" and not (method or "").strip():
                errors.append(f"{source_id}: extracted first-party source has no extraction_method")
        topics = {row[0] for row in connection.execute("SELECT topic_id FROM topics")}
        for post_id, topic_id, status in connection.execute("SELECT post_id,topic_id,status FROM topic_links"):
            if topic_id not in topics:
                errors.append(f"topic_link ({post_id},{topic_id}) references unknown Topic")
            if status not in {"pending_review", "approved", "rejected"}:
                errors.append(f"topic_link ({post_id},{topic_id}) has invalid status={status}")
        if master_root is not None:
            master_count = 0
            for path in sorted(master_root.glob("*.json")):
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"Master {path.name}: {exc}")
                    continue
                master_count += 1
                for source in payload.get("sources", []):
                    if source.get("verification_status") not in {"unverified", "verified", "stale", "unavailable"}:
                        errors.append(f"Master {path.name}: invalid source verification_status")
            if master_count == 0:
                warnings.append("no Master JSON records found")
        counts = {
            "posts": connection.execute("SELECT count(*) FROM posts").fetchone()[0],
            "sources": len(source_rows),
            "topics": len(topics),
            "topic_links": connection.execute("SELECT count(*) FROM topic_links").fetchone()[0],
            "approved_links": connection.execute("SELECT count(*) FROM topic_links WHERE status='approved'").fetchone()[0],
            "pending_links": connection.execute("SELECT count(*) FROM topic_links WHERE status='pending_review'").fetchone()[0],
        }
        return {"valid": not errors, "errors": errors, "warnings": warnings, "counts": counts, "integrity": integrity}
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=ROOT / "data" / "wordpress_sources.sqlite3")
    parser.add_argument("--master-root", type=Path, default=ROOT / "master_topic_packs")
    parser.add_argument("--json", type=Path, help="write validation report JSON")
    args = parser.parse_args()
    result = validate_source_pack(args.database, args.master_root)
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WORDPRESS_SOURCE_PACK_VALIDATION={'PASS' if result['valid'] else 'FAIL'}")
    print(f"SQLITE_INTEGRITY={result.get('integrity', 'unknown')}")
    for name, count in result.get("counts", {}).items():
        print(f"{name.upper()}={count}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
