from __future__ import annotations

import copy
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.learning_workflow import record_result_and_build_queue
from study.learning_runtime import feedback_from_view
from study.master_topic_pack import grading_compatibility_payload, load_master_topic_pack, project_diagnosis, project_training
from study.training_history import TrainingHistoryStore


def test_representative_topics_project_and_complete_learning_cycle() -> None:
    master_paths = sorted((ROOT / "master_topic_packs").glob("*.json"))
    master_topic_ids = {path.stem for path in master_paths}
    assert {
        "control_valve_authority_rangeability_gain_installed_performance",
        "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response",
        "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
        "final_control_element_sil_sis_esd_valve_partial_stroke_test",
    } <= master_topic_ids
    for index, path in enumerate(master_paths):
        master = load_master_topic_pack(path)
        before = copy.deepcopy(master)
        grading = grading_compatibility_payload(ROOT, master)
        training = project_training(ROOT, master)
        diagnosis_projection = project_diagnosis(ROOT, master)
        assert set(grading) == {"fact_anchor", "logic_check", "model_answer", "topic_importance"}
        assert all(payload["topic_id"] == master["topic_id"] for payload in grading.values())
        assert training["topic_id"] == diagnosis_projection["topic_id"] == master["topic_id"]
        assert training["daily_target"] == 2
        assert diagnosis_projection["score_effect"] == "none"
        assert master == before

        if index == 0:
            with tempfile.TemporaryDirectory(prefix="master-learning-cycle-") as directory:
                history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
                result = record_result_and_build_queue(
                    history,
                    question_id="demo-question-001",
                    topic_id=master["topic_id"],
                    attempted_at="2026-10-03T12:00:00+09:00",
                    grade_result={"final_total_score": 15.5, "total_score": 14.0},
                    diagnosis={"format": [], "content": ["add verification evidence"]},
                    queue_candidates=[
                        {"topic_id": master["topic_id"], "reason": "weak_topic", "question_id": "demo-question-001"},
                        {"topic_id": "control_valve_memory_topic", "reason": "long_unreviewed_topic", "question_id": "demo-question-002"},
                    ],
                    generated_at="2026-10-03T12:10:00+09:00",
                    next_review_at="2026-10-06T12:00:00+09:00",
                )
                assert result["training_attempt"]["score"] == 15.5
                assert result["training_attempt"]["review_status"] == "scheduled"
                assert len(result["review_queue"]["items"]) == 2
                assert history.list_attempts()[0]["diagnosis"]["content"] == ["add verification evidence"]


def test_ocr_worked_example_is_training_only_and_diagnosis_recommends_it() -> None:
    path = ROOT / "master_topic_packs/nyquist_stability_criterion_gain_phase_margin.json"
    master = load_master_topic_pack(path)
    grading_before = grading_compatibility_payload(ROOT, master)
    training = project_training(ROOT, master)
    diagnosis = project_diagnosis(ROOT, master)
    material_id = "nyquist_time_delay_margin_worked_example"
    material = next(item for item in training["curated_learning_materials"] if item["material_id"] == material_id)
    assert material["review_status"] == "llm_reviewed_human_pending"
    assert "π/4 s≈0.785 s" in " ".join(material["steps"])
    assert any(item["material_id"] == material_id for item in diagnosis["recommended_materials"])
    feedback = feedback_from_view(
        {"topic_id": master["topic_id"], "final_total_score": 12.0}, diagnosis
    )
    assert any(item["material_id"] == material_id for item in feedback["recommended_materials"])
    assert diagnosis["score_effect"] == "none"
    assert grading_compatibility_payload(ROOT, master) == grading_before


if __name__ == "__main__":
    test_representative_topics_project_and_complete_learning_cycle()
    test_ocr_worked_example_is_training_only_and_diagnosis_recommends_it()
    print("MASTER_TOPIC_PACK_INTEGRATION_TESTS=2_PASS")
