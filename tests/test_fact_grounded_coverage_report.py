from pathlib import Path

from scripts.report_fact_grounded_coverage import coverage_report


def test_metadata_only_coverage_report():
    result = coverage_report(Path(__file__).resolve().parents[1])
    assert result["master_topics"] >= 3
    assert result["representative_topics"] == 3
    assert result["reviewed_proposals"] == 3
    assert result["approved_facts"] == 3
    assert result["unapproved_proposals"] == 0
    assert result["eligible_for_runtime_activation"] is False
