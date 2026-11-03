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
from scripts.promote_reviewed_fact_anchors import (
    SECOND_BATCH_RETAINED_HOLDS,
    build as build_promotions,
)

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv"
MANIFEST = ROOT / "grading/evidence/fact_anchor_unresolved_source_holds_20261101.json"
UNREVIEWED = "PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW"
INSUFFICIENT = "HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE"
SCOPED = "SOURCE_CHECKED_SCOPED_STANDARD_HOLD"
VENDOR = "SOURCE_CHECKED_VENDOR_APPLICATION_HOLD"
REVIEW = ROOT / "reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv"


def audit():
    with AUDIT.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_hold_snapshot_matches_independent_audit_exactly():
    rows = audit()
    assert len(rows) == 1290
    with REVIEW.open(encoding="utf-8", newline="") as f:
        review = {r["fact_id"]: r for r in csv.DictReader(f)}
    expected = {
        (r["fact_id"], r["topic_id"], r["anchor_id"])
        for r in rows if r["final_technical_verdict"] in (UNREVIEWED, INSUFFICIENT, SCOPED, VENDOR)
    }
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    actual = {
        (r["fact_id"], r["topic_id"], r["anchor_id"]) for r in manifest["holds"]
    }
    reviewed_pending = {
        (r["fact_id"], r["topic_id"], r["anchor_id"])
        for r in manifest["holds"] if r["reason"] == "reviewed_but_canonical_promotion_pending"
    }
    promoted = {
        (r["fact_id"], r["topic_id"], r["anchor_id"])
        for r in build_promotions()["entries"]
    }
    assert len(promoted) == 103
    assert not promoted & actual
    assert len(reviewed_pending) == 9
    assert {fid for fid, _, _ in reviewed_pending} == SECOND_BATCH_RETAINED_HOLDS
    assert all(
        review[fid]["latest_report_disposition"] == "KEEP_BOUNDED"
        and review[fid]["core_scoring_promotion_by_this_review"] == "NOT_AUTHORIZED_BY_RECONCILIATION"
        for fid, _, _ in reviewed_pending
    )
    expected |= reviewed_pending
    assert manifest["version"] == "fact-anchor-unresolved-source-holds-v1"
    assert actual == expected
    assert len(actual) == len(manifest["holds"]) == 81
    assert Counter(r["reason"] for r in manifest["holds"]) == {
        "reviewed_but_canonical_promotion_pending": 9,
        "insufficient_direct_primary_source_scope": 50,
        "source_checked_scoped_standard_not_generic": 11,
        "source_checked_vendor_application_not_generic": 11,
    }
    a, b = unresolved_source_holds()
    assert len(a) == len(b) == 81


def test_promoted_canonical_claims_are_available_to_scoring():
    for row in build_promotions()["entries"]:
        assert not excluded_from_scoring(
            topic_id=row["topic_id"], anchor_id=row["anchor_id"], fact_id=row["fact_id"]
        )


def test_all_unresolved_holds_are_excluded_and_disjoint():
    old_ids, old_keys = scoring_exclusions()
    revision_ids, revision_keys = independent_revision_holds()
    pending_ids, pending_keys = unresolved_source_holds()
    assert not (old_ids & pending_ids or revision_ids & pending_ids)
    assert not (old_keys & pending_keys or revision_keys & pending_keys)
    _, pending_keys = unresolved_source_holds()
    for row in audit():
        if (row["topic_id"], row["anchor_id"]) in pending_keys:
            assert excluded_from_scoring(
                topic_id=row["topic_id"], anchor_id=row["anchor_id"],
                fact_id=row["fact_id"],
            )


def test_scoped_question_cannot_force_unreviewed_anchor_into_requirements():
    topic = "analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting"
    anchor = "acl_closed_loop_verification"
    assert excluded_from_scoring(topic_id=topic, anchor_id=anchor)
    for question in ("", "4~20mA 계장 루프 수리 후 전체 기능 검증을 설명하시오."):
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
        if row["scoring_exclusion_reason"] or excluded_from_scoring(
            topic_id=row["topic_id"], anchor_id=row["anchor_id"], fact_id=row["fact_id"]
        ):
            continue
        assert not excluded_from_scoring(
            topic_id=row["topic_id"], anchor_id=row["anchor_id"],
            fact_id=row["fact_id"],
        )
