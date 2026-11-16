"""Keep a pending sentence edit from silently adding qualitative evidence axes."""

import json
from pathlib import Path

import pytest

from grading.evidence.logic_check_evaluator import _build_canonical_axis_context


ROOT = Path(__file__).resolve().parents[1]
HUMIDITY = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
ROTATION = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
PENDING = (
    (HUMIDITY, "relative_humidity_definition"),
    (HUMIDITY, "dew_point_definition"),
    (ROTATION, "quadrature_direction_principle"),
    (ROTATION, "tachogenerator_voltage_speed_principle"),
    (ROTATION, "counting_window_speed_equation"),
    (ROTATION, "gear_tooth_speed_equation"),
)


@pytest.mark.parametrize(("topic", "anchor_id"), PENDING)
def test_pending_shortening_keeps_original_axis_ownership(topic, anchor_id):
    manifest = json.loads((ROOT / "calibration/fact_anchor_simplification_review_20261114.json").read_text(encoding="utf-8"))
    previous = next(row["previous_statement"] for row in manifest["entries"]
                    if (row["topic_id"], row["anchor_id"]) == (topic, anchor_id))
    source = json.loads((ROOT / "rubrics/topic_packs" / topic / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in source["anchors"] if row["anchor_id"] == anchor_id)
    assert anchor["statement"] == previous
    assert anchor["accepted_explanations"][0] == previous
    axes = _build_canonical_axis_context({"fact_anchor": {"anchors": [anchor]}})
    assert len(axes) == 2
    assert sum(axis["canonical_claim"] == previous for axis in axes) == 1


@pytest.mark.parametrize(("question", "owner"), [
    ("Subzero moisture specification에서 frost point 계산 기준을 설명하시오.", HUMIDITY),
    ("누락 톱니 missing-tooth encoder 신호로 회전속도를 측정하는 방법을 설명하시오.", ROTATION),
])
def test_fallback_fact_bank_keeps_prior_question_owner(monkeypatch, question, owner):
    import grading_agents

    bank = json.loads((ROOT / "rubrics/generated/fact_anchors.generated.json").read_text(encoding="utf-8"))
    monkeypatch.setattr(grading_agents, "_phase3_load_fact_anchor_bank", lambda *args, **kwargs: bank)
    result = grading_agents._phase3_select_fact_anchors_from_bank(question, "")
    assert result is not None
    assert result["topic_id"] == owner
