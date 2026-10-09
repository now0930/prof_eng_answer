from __future__ import annotations

import csv
import hashlib
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prepare_wordpress_topic_link_review import prepare_review_template
from validate_wordpress_topic_link_review import BASE_COLUMNS, LLM_COLUMNS


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _row(post_id: str, status: str, topic_id: str) -> dict[str, str]:
    row = {column: "" for column in BASE_COLUMNS}
    row.update(
        post_id=post_id,
        post_title=f"Post {post_id}",
        link_status=status,
        candidate_topic_id=topic_id,
        review_action="",
        review_topic_id="",
        reviewer_notes="",
    )
    return row


def test_prepare_template_preserves_rows_and_refuses_unsafe_inputs() -> None:
    with tempfile.TemporaryDirectory(prefix="wordpress-review-template-") as directory:
        root = Path(directory)
        source = root / "source.csv"
        output = root / "review.csv"
        rows = [
            _row("1", "approved", "topic_alpha"),
            _row("1", "pending_review", "topic_beta"),
            _row("2", "unmatched", ""),
        ]
        _write_csv(source, BASE_COLUMNS, rows)
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()

        result = prepare_review_template(source, output)
        assert result["rows"] == 3
        assert result["counts"] == {"approved": 1, "pending_review": 1, "unmatched": 1}
        assert result["source_sha256"] == source_hash
        assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash

        with output.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            assert reader.fieldnames == BASE_COLUMNS + LLM_COLUMNS
            review_rows = list(reader)
        assert [
            (row["post_id"], row["link_status"], row["candidate_topic_id"])
            for row in review_rows
        ] == [
            ("1", "approved", "topic_alpha"),
            ("1", "pending_review", "topic_beta"),
            ("2", "unmatched", ""),
        ]
        assert all(not row[column] for row in review_rows for column in LLM_COLUMNS)
        assert all(
            not row[column]
            for row in review_rows
            for column in ("review_action", "review_topic_id", "reviewer_notes")
        )
        output_bytes = output.read_bytes()
        try:
            prepare_review_template(source, output)
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing review output must not be overwritten")
        assert output.read_bytes() == output_bytes
        try:
            prepare_review_template(source, source)
        except ValueError:
            pass
        else:
            raise AssertionError("source CSV must not be used as output")

        invalid_cases = [
            ([rows[0], dict(rows[0])], "duplicate source row identity"),
            ([{**rows[0], "link_status": "unknown"}], "unsupported source link status"),
            ([{**rows[0], "candidate_topic_id": ""}], "no candidate Topic ID"),
            ([{**rows[2], "candidate_topic_id": "topic_alpha"}], "unmatched source row"),
        ]
        for index, (invalid_rows, expected_error) in enumerate(invalid_cases):
            invalid_source = root / f"invalid-{index}.csv"
            invalid_output = root / f"invalid-review-{index}.csv"
            _write_csv(invalid_source, BASE_COLUMNS, invalid_rows)
            try:
                prepare_review_template(invalid_source, invalid_output)
            except ValueError as exc:
                assert expected_error in str(exc)
            else:
                raise AssertionError(f"invalid source was accepted: {expected_error}")
            assert not invalid_output.exists()


if __name__ == "__main__":
    test_prepare_template_preserves_rows_and_refuses_unsafe_inputs()
    print("WORDPRESS_TOPIC_LINK_REVIEW_TEMPLATE_TESTS=1_PASS")
