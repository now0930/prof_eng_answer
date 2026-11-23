"""Guard the exact 457-row, score-neutral Fact atomicity review queue.

These checks validate identity and source snapshots only; they do NOT certify
technical correctness, source locators, approval, or scoring eligibility.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "rubrics" / "topic_packs"
TRIAGE_ROOT = ROOT / "reports" / "fact_atomicity_triage"
HEURISTIC = re.compile(r"[.!?。]\s+")


def _git_blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def test_all_fact_atomicity_triage_rows_match_frozen_source():
    sources = {}
    all_candidates = {}
    for path in sorted(SOURCE_ROOT.glob("*/fact_anchor.json")):
        raw = path.read_bytes()
        source = json.loads(raw.decode("utf-8"))
        topic = path.parent.name
        assert source["topic_id"] == topic
        sources[topic] = _git_blob_hash(raw)
        for a in source["anchors"]:
            statement = a.get("statement") or ""
            if HEURISTIC.search(statement):
                key = (topic, a.get("anchor_id") or a.get("id"))
                assert key not in all_candidates
                all_candidates[key] = {
                    "statement": statement,
                    "source_basis": a.get("source_basis") or None,
                    "importance": a.get("importance") or None,
                }
    assert len(sources) == 89
    assert len(all_candidates) == 457

    files = sorted(TRIAGE_ROOT.glob("batch_??.json"))
    assert len(files) == 7
    row_keys = set()
    for index, path in enumerate(files, start=1):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["batch_index"] == index
        assert payload["basis_commit"] == "30b13262ad3899919edae7cb72be3ddeca677f18"
        assert payload["schema_version"] == "fact_anchor_atomicity_triage.v1"
        assert payload["score_effect"] == "none"
        assert payload["review_decision_authority"] == "none"
        assert isinstance(payload["entries"], list)
        for entry in payload["entries"]:
            key = (entry["topic_id"], entry["anchor_id"])
            assert key in all_candidates and key not in row_keys
            row_keys.add(key)
            original = all_candidates[key]
            assert entry["statement"] == original["statement"]
            assert entry["source_basis"] == original["source_basis"]
            assert entry["importance"] == original["importance"]
            assert entry["source_file_blob_sha"] == sources[entry["topic_id"]]
            assert entry["sentence_count_heuristic"] == len(
                HEURISTIC.split(entry["statement"])
            )
            assert entry["review_status"] == "HOLD_INDEPENDENT_TECHNICAL_SOURCE_CHECK"
            assert entry["recommended_canonical_action"] == "KEEP_CURRENT_CANONICAL_UNCHANGED"
            assert entry["score_effect"] == "none"
            assert "NO_INDEPENDENT_SOURCE_LOCATOR_VERIFIED_IN_THIS_BATCH" in entry["reasons"]
            assert "technical_approval" not in entry
            assert "scoring_status" not in entry
    assert row_keys == set(all_candidates)


def test_triage_batches_are_metadata_only_not_canonical_sources():
    paths = sorted(TRIAGE_ROOT.glob("batch_??.json"))
    assert len(paths) == 7
    assert all("HOLD_INDEPENDENT_TECHNICAL_SOURCE_CHECK" in p.read_text(encoding="utf-8") for p in paths)
    assert all('"score_effect": "none"' in p.read_text(encoding="utf-8") for p in paths)
