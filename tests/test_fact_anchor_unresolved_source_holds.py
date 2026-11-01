"""Fail-closed scoring reference tests for independently unresolved facts."""
import csv
import json
from collections import Counter
from pathlib import Path

from grading.evidence.fact_anchor_scoring_exclusions import (
    excluded_from_scoring,
    scoring_exclusions,
    independent_revision_holds,
    unresolved_source_holds,
)
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv"
MANIFEST = ROOT / "grading/evidence/fact_anchor_unresolved_source_holds_20261101.json"
UNREVIEWED = "PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW"
INSUFFICIENT = "HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE"


def audit():
    with AUDIT.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_hold_snapshot_matches_independent_audit_exactly():
    rows = audit()
    assert len(rows) == 1290
    expected = {
        (r["fact_id"], r["topic_id"], r["anchor_id"])
        for r in rows if r["final_technical_verdict"] in (UNREVIEWED, INSUFFICIENT)
    }
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    actual = {
        (r["fact_id"], r["topic_id"], r["anchor_id"]) for r in manifest["holds"]
    }
    assert manifest["version"] == "fact-anchor-unresolved-source-holds-v1"
    assert actual == expected
    assert len(actual) == len(manifest["holds"]) == 595
    assert Counter(r["reason"] for r in manifest["holds"]) == {
        "independent_primary_source_check_pending": 590,
        "insufficient_direct_primary_source_scope": 5,
    }
    a, b = unresolved_source_holds()
    assert len(a) == len(b) == 595


def test_all_unresolved_holds_are_excluded_and_disjoint():
    old_ids, old_keys = scoring_exclusions()
    revision_ids, revision_keys = independent_revision_holds()
    pending_ids, pending_keys = unresolved_source_holds()
    assert not (old_ids & pending_ids or revision_ids & pending_ids)
    assert not (old_keys & pending_keys or revision_keys & pending_keys)
    for row in audit():
        if row["final_technical_verdict"] in (UNREVIEWED, INSUFFICIENT):
            assert excluded_from_scoring(
                topic_id=row["topic_id"], anchor_id=row["anchor_id"],
                fact_id=row["fact_id"],
            )


def test_scoped_question_cannot_force_unreviewed_anchor_into_requirements():
    topic = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    anchor = "hysteresis_direction_dependent_output"
    assert excluded_from_scoring(topic_id=topic, anchor_id=anchor)
    for question in ("", "Hysteresis의 정의와 검증 방법을 기술하시오."):
        result = evaluate_fact_anchor_requirements(
            question_text=question,
            answer_text="같은 입력에서도 상승/하강 경로의 밸브 출력이 달라진다.",
            topic_ids=[topic],
        )
        assert anchor not in {r["requirement_id"] for r in result["requirements"]}


def test_still_supported_independently_bounded_fact_is_not_blocked():
    for row in audit():
        if row["final_technical_verdict"] != "KEEP_BOUNDED":
            continue
        if row["scoring_exclusion_reason"]:
            continue
        assert not excluded_from_scoring(
            topic_id=row["topic_id"], anchor_id=row["anchor_id"],
            fact_id=row["fact_id"],
        )
