"""Source linkage and question-scoped grading facts for Chapters 22, 31 and 32."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLOW = "flow_measurement_meter_principles_velocity_selection"
PROCESS = "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_five_blog_posts_are_linked_without_duplicate_source_ids():
    targets = {
        FLOW: "wp-post:9782",
        PROCESS: "wp-post:9789",
        "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection": "wp-post:9814",
        "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh": "wp-post:9839",
        "sil_target_determination_risk_reduction_and_lifecycle": "wp-post:9839",
    }
    for topic_id, source_id in targets.items():
        master = _read(ROOT / "master_topic_packs" / f"{topic_id}.json")
        ids = [source["source_id"] for source in master["sources"]]
        assert source_id in ids
        assert len(ids) == len(set(ids))
        linked = next(source for source in master["sources"] if source["source_id"] == source_id)
        assert linked["verification_status"] == "unverified"

    flow_master = _read(ROOT / "master_topic_packs" / f"{FLOW}.json")
    assert "wp-post:9774" in {source["source_id"] for source in flow_master["sources"]}


def test_new_facts_only_required_in_explicit_question_patterns():
    facts = {
        FLOW: {"flow_inventory_change_net_balance"},
        PROCESS: {
            "relation_control_offset_setpoint",
            "feedforward_dynamic_compensation_timing",
            "limit_control_bound_signal",
        },
    }
    for topic_id, new_ids in facts.items():
        pack_root = ROOT / "rubrics" / "topic_packs" / topic_id
        anchors = _read(pack_root / "fact_anchor.json")["anchors"]
        anchor_ids = {anchor.get("anchor_id", anchor.get("id")) for anchor in anchors}
        assert new_ids <= anchor_ids
        patterns = _read(pack_root / "model_answer.json")["expected_question_patterns"]
        new_patterns = [pattern for pattern in patterns if new_ids.intersection(pattern["required_anchor_ids"])]
        assert len(new_patterns) == len(new_ids)
        assert all(len(set(pattern["required_anchor_ids"])) == len(pattern["required_anchor_ids"]) for pattern in patterns)


def test_four_new_anchors_have_independent_score_neutral_registry_evidence():
    registry = _read(ROOT / "grading/evidence/approved_fact_registry.json")
    expected = {
        (FLOW, "flow_inventory_change_net_balance"),
        (PROCESS, "relation_control_offset_setpoint"),
        (PROCESS, "feedforward_dynamic_compensation_timing"),
        (PROCESS, "limit_control_bound_signal"),
    }
    facts = {
        (fact["topic_id"], fact.get("legacy_anchor_id")): fact
        for fact in registry["facts"]
    }
    assert expected <= facts.keys()
    for key in expected:
        fact = facts[key]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert all(ref["authority_type"] == "textbook" and ref["locator"] for ref in fact["verification_refs"])
