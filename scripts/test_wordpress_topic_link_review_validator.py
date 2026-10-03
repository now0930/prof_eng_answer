from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from validate_wordpress_topic_link_review import BASE_COLUMNS, LLM_COLUMNS, validate_review_csv


def _row(*, post_id: str, status: str, candidate: str, recommendation: str, confidence: str, llm_topic: str = "") -> dict[str, str]:
    row = {column: "" for column in BASE_COLUMNS + LLM_COLUMNS}
    row.update(
        post_id=post_id,
        post_title=f"Post {post_id}",
        wordpress_url=f"https://example.org/{post_id}",
        link_status=status,
        candidate_topic_id=candidate,
        llm_recommendation=recommendation,
        llm_confidence=confidence,
        llm_topic_id=llm_topic,
        llm_evidence="Direct subject and Topic scope match.",
        llm_notes="Evidence checked against the existing Topic Pack.",
    )
    return row


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def test_review_csv_validator_checks_contract_without_authorizing_apply() -> None:
    with tempfile.TemporaryDirectory(prefix="wordpress-review-validator-") as directory:
        root = Path(directory)
        topic_root = root / "topic_packs"
        for topic_id in ("topic_alpha", "topic_beta"):
            topic_dir = topic_root / topic_id
            topic_dir.mkdir(parents=True)
            (topic_dir / "README.md").write_text(f"# {topic_id}\n", encoding="utf-8")

        source_rows = [
            _row(post_id="1", status="approved", candidate="topic_alpha", recommendation="", confidence=""),
            _row(post_id="2", status="pending_review", candidate="topic_alpha", recommendation="", confidence=""),
            _row(post_id="3", status="unmatched", candidate="", recommendation="", confidence=""),
        ]
        review_rows = [
            _row(post_id="1", status="approved", candidate="topic_alpha", recommendation="retain_approved", confidence="medium", llm_topic="topic_alpha"),
            _row(post_id="2", status="pending_review", candidate="topic_alpha", recommendation="recommend_approve", confidence="high", llm_topic="topic_alpha"),
            _row(post_id="3", status="unmatched", candidate="", recommendation="recommend_link", confidence="high", llm_topic="topic_beta"),
        ]
        source_path, review_path = root / "source.csv", root / "review.csv"
        _write_csv(source_path, BASE_COLUMNS, source_rows)
        _write_csv(review_path, BASE_COLUMNS + LLM_COLUMNS, review_rows)
        result = validate_review_csv(source_path, review_path, topic_pack_root=topic_root)
        assert result["valid"] is True
        assert result["source_rows"] == result["review_rows"] == 3
        assert len(result["warnings"]) == 1  # Existing approved Topic ID is only redundantly repeated.

        review_rows[1]["llm_confidence"] = "medium"
        _write_csv(review_path, BASE_COLUMNS + LLM_COLUMNS, review_rows)
        result = validate_review_csv(source_path, review_path, topic_pack_root=topic_root)
        assert result["valid"] is False
        assert any("must have high confidence" in error for error in result["errors"])

        review_rows[1]["llm_confidence"] = "high"
        review_rows[1]["review_action"] = "approve"
        _write_csv(review_path, BASE_COLUMNS + LLM_COLUMNS, review_rows)
        result = validate_review_csv(source_path, review_path, topic_pack_root=topic_root)
        assert result["valid"] is False
        assert any("human-decision fields" in error for error in result["errors"])

        review_rows[1]["review_action"] = ""
        review_rows[2]["llm_topic_id"] = "topic_missing"
        _write_csv(review_path, BASE_COLUMNS + LLM_COLUMNS, review_rows)
        result = validate_review_csv(source_path, review_path, topic_pack_root=topic_root)
        assert result["valid"] is False
        assert any("unknown Topic Pack" in error for error in result["errors"])


if __name__ == "__main__":
    test_review_csv_validator_checks_contract_without_authorizing_apply()
    print("WORDPRESS_TOPIC_LINK_REVIEW_VALIDATOR_TESTS=1_PASS")
