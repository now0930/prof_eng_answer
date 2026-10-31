"""Regression for 2026-11-01 general-scoring exclusion policy."""

import csv
import json
from collections import Counter
from pathlib import Path

from grading.evidence.fact_anchor_scoring_exclusions import (
    excluded_from_scoring,
    scoring_exclusions,
)
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "grading/evidence/fact_anchor_scoring_exclusions_20261101.json"
LEDGER = ROOT / "reports/fact_anchor_chat_ledger_20261101.csv"


def test_276_exclusions_match_full_queue_ids_without_duplicates():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = payload["exclusions"]
    assert payload["version"] == "fact-anchor-scoring-exclusions-v1"
    assert len(rows) == 276
    assert Counter(row["reason"] for row in rows) == {
        "noncore_detail": 190,
        "scoped_standard_or_jurisdiction": 66,
        "duplicate_scoring_requirement": 17,
        "overgeneralization_or_correction_required": 3,
    }
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        ledger = {row["fact_id"]: row for row in csv.DictReader(handle)}
    assert len(ledger) == 1290
    assert len({row["fact_id"] for row in rows}) == len(rows)
    assert len({(row["topic_id"], row["anchor_id"]) for row in rows}) == len(rows)
    for row in rows:
        original = ledger[row["fact_id"]]
        assert original["topic_id"] == row["topic_id"]
        assert original["anchor_id"] == row["anchor_id"]
        assert excluded_from_scoring(
            fact_id=row["fact_id"], topic_id=row["topic_id"], anchor_id=row["anchor_id"]
        )
    assert len(scoring_exclusions()[0]) == len(rows)
    assert len(scoring_exclusions()[1]) == len(rows)


def test_exclusion_applies_to_all_anchor_and_explicit_question_scopes():
    topic = "control_valve_types_globe_rotary_body_actuator_selection"
    excluded_anchor = "butterfly_compact_high_capacity"
    for question_text in (
        "",
        "Sliding-stem valve와 rotary valve의 구조, 장단점과 적용 조건을 비교하시오.",
    ):
        result = evaluate_fact_anchor_requirements(
            question_text=question_text,
            answer_text="Butterfly 형식은 높은 유량을 처리할 수 있다.",
            topic_ids=[topic],
        )
        assert excluded_anchor not in {
            row["requirement_id"] for row in result["requirements"]
        }


def test_exclusions_do_not_blanket_block_other_anchors():
    topic = "final_control_element_sil_sis_esd_valve_partial_stroke_test"
    result = evaluate_fact_anchor_requirements(
        question_text="SIF에서 Final Element의 역할과 구성, subsystem boundary를 설명하시오.",
        answer_text="Final Element는 SIF의 출력이다.",
        topic_ids=[topic],
    )
    ids = {row["requirement_id"] for row in result["requirements"]}
    assert "valve_actuator_solenoid_architecture" not in ids
    assert "final_element_role_in_sif" in ids
