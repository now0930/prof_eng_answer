"""The ChatGPT packet is exact, source-preserving and non-authoritative."""

import csv
import hashlib
import io
from collections import Counter
import pytest

from scripts.export_blocked_fact_review_packet import BATCH_SIZE, build_rows, render
from scripts.validate_blocked_fact_review import validate


def test_blocked_packet_exact_ids_counts_and_originals():
    rows = build_rows()
    assert len(rows) == len({row["fact_id"] for row in rows}) == 436
    assert Counter(row["block_group"] for row in rows) == {
        "revision": 80,
        "source_or_promotion": 80,
        "general_exclusion": 276,
    }
    assert all(row["current_topic_statement"] and row["current_registry_statement"] for row in rows)
    assert all(
        row["current_statement_sha256"] == hashlib.sha256(row["current_topic_statement"].encode()).hexdigest()
        for row in rows
    )
    assert all(row["chatgpt_decision"] == "UNREVIEWED" and not row["proposed_statement"] for row in rows)
    assert len(list(csv.DictReader(io.StringIO(render(rows))))) == 436


def test_nine_batches_partition_master_without_loss():
    master = build_rows()
    recovered = []
    for index in range(1, 10):
        text = render(master[(index - 1) * BATCH_SIZE:index * BATCH_SIZE])
        rows = list(csv.DictReader(io.StringIO(text)))
        assert len(rows) == (BATCH_SIZE if index < 9 else 36)
        recovered.extend(rows)
    assert recovered == master


def test_returned_review_format_is_checked_without_unblocking(tmp_path):
    path = tmp_path / "review.csv"
    rows = build_rows()[:2]
    path.write_text(render(rows), encoding="utf-8")
    assert validate(path) == {"UNREVIEWED": 2}
    rows[0]["current_topic_statement"] = "silently changed"
    path.write_text(render(rows), encoding="utf-8")
    with pytest.raises(ValueError, match="Original field changed"):
        validate(path)
    rows = build_rows()[:2]
    rows[0]["chatgpt_decision"] = "GENERAL_CANDIDATE"
    path.write_text(render(rows), encoding="utf-8")
    with pytest.raises(ValueError, match="Source-grounded review incomplete"):
        validate(path)
