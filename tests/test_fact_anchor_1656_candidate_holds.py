"""The private full-review proposal may only add fail-closed reference holds."""

import json
from collections import Counter
from pathlib import Path

from grading.evidence.fact_anchor_scoring_exclusions import (
    candidate_review_holds,
    excluded_from_scoring,
    independent_revision_holds,
    scoring_exclusions,
    unresolved_source_holds,
)
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "grading/evidence/fact_anchor_1656_candidate_holds_20261104.json"


def test_103_candidate_holds_are_disjoint_and_source_pinned():
    rows = json.loads(MANIFEST.read_text(encoding="utf-8"))["holds"]
    keys = {(r["topic_id"], r["anchor_id"]) for r in rows}
    assert len(rows) == len(keys) == len(candidate_review_holds()) == 103
    assert Counter(r["reason"] for r in rows) == {
        "candidate_source_review_pending": 17,
        "candidate_formula_safety_review_pending": 5,
        "candidate_non_scoring_metadata": 76,
        "candidate_nonfact_routing_metadata": 5,
    }
    old = scoring_exclusions()[1] | independent_revision_holds()[1] | unresolved_source_holds()[1]
    assert len(old) == 436
    assert not old & keys
    for topic_id, anchor_id in keys:
        assert excluded_from_scoring(topic_id=topic_id, anchor_id=anchor_id)


def test_explicit_question_cannot_resurrect_unapproved_formula_fact():
    topic = "root_locus_stability_gain_design"
    anchor = "asymptote_centroid"
    assert (topic, anchor) in candidate_review_holds()
    result = evaluate_fact_anchor_requirements(
        question_text="근궤적 점근선의 중심을 설명하시오.",
        answer_text="극점과 영점의 합으로 계산한다.",
        topic_ids=[topic],
    )
    assert anchor not in {row["requirement_id"] for row in result["requirements"]}


def test_other_fact_remains_available():
    assert not excluded_from_scoring(
        topic_id="displacer_level_buoyancy_torque_tube_density_interface_calibration",
        anchor_id="displacer_buoyancy",
    )
