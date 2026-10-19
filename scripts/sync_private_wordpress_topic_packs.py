#!/usr/bin/env python3
"""Copy private WordPress text bundles into a checkout without publishing them."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from study.master_topic_pack import load_master_topic_pack, _load_linked_wordpress_materials


def sync(source_directory: Path, target_repository: Path, topic_ids: list[str], verify_only: bool = False) -> list[str]:
    """Fail closed on changed sources, bad hashes, or conflicting private files."""
    source_directory = source_directory.resolve(strict=True)
    target_repository = target_repository.resolve(strict=True)
    if not source_directory.is_dir():
        raise ValueError("source must be a private bundle directory")
    destination = target_repository / "data" / "wordpress_topic_packs"
    if destination.exists() and destination.is_symlink():
        raise ValueError("target private bundle directory cannot be a symlink")
    prepared: list[tuple[Path, bytes]] = []
    for topic_id in topic_ids:
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", topic_id):
            raise ValueError(f"invalid topic ID: {topic_id}")
        master = load_master_topic_pack(target_repository / "master_topic_packs" / f"{topic_id}.json")
        source_file = source_directory / f"{topic_id}.json"
        if source_file.is_symlink() or not source_file.is_file():
            raise ValueError(f"private source bundle missing or symlinked: {topic_id}")
        raw = source_file.read_bytes()
        payload = json.loads(raw)
        if not isinstance(payload, dict) or payload.get("private") is not True or payload.get("topic_id") != topic_id:
            raise ValueError(f"invalid private bundle identity: {topic_id}")
        rows = payload.get("sources")
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"private bundle has no sources: {topic_id}")
        references = {row["source_id"]: row for row in master["sources"]}
        seen = set()
        for row in rows:
            if not isinstance(row, dict) or row.get("source_id") not in references or row["source_id"] in seen:
                raise ValueError(f"unlinked or duplicate private source: {topic_id}")
            seen.add(row["source_id"])
            ref = references[row["source_id"]]
            for key in ("source_type", "wordpress_url", "version"):
                if row.get(key) != ref[key]:
                    raise ValueError(f"Master/source {key} mismatch: {topic_id} {row['source_id']}")
            if row.get("source_url", row.get("wordpress_url")) != ref.get("source_url", ref["wordpress_url"]):
                raise ValueError(f"Master/source URL mismatch: {topic_id} {row['source_id']}")
            body = row.get("extracted_text")
            if not isinstance(body, str) or row.get("extracted_text_sha256") != hashlib.sha256(body.encode()).hexdigest():
                raise ValueError(f"private source text hash mismatch: {topic_id} {row['source_id']}")
        target_file = destination / f"{topic_id}.json"
        if target_file.is_symlink():
            raise ValueError(f"target private bundle cannot be a symlink: {topic_id}")
        if target_file.exists() and target_file.read_bytes() != raw:
            raise ValueError(f"target has a different private bundle; reconcile manually: {topic_id}")
        prepared.append((target_file, raw))
    if not verify_only:
        destination.mkdir(parents=True, exist_ok=True, mode=0o700)
        destination.chmod(0o700)
        for target_file, raw in prepared:
            if target_file.exists():
                continue
            fd, temporary = tempfile.mkstemp(prefix=".private-sync-", dir=destination)
            try:
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(raw)
                os.replace(temporary, target_file)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        for topic_id in topic_ids:
            master = load_master_topic_pack(target_repository / "master_topic_packs" / f"{topic_id}.json")
            _load_linked_wordpress_materials(target_repository, master)
    return [topic_id for topic_id in topic_ids]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-directory", type=Path, required=True, help="private bundle directory from an existing checkout or secure backup")
    parser.add_argument("--target-repository", type=Path, default=ROOT, help="new checkout; defaults to this repository")
    parser.add_argument("--topic-id", action="append", required=True, dest="topic_ids")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    topics = sync(args.source_directory, args.target_repository, args.topic_ids, args.verify_only)
    print(f"PRIVATE_WORDPRESS_SYNC={'VERIFIED' if args.verify_only else 'PASS'} topics={len(topics)}; body remains outside Git")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
