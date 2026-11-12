import sys
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.scoring.deterministic_primary_grader import (
    _unresolved_requirement_ids, grade_deterministically, persist_deterministic_grade,
)
from grading_agents import finalize_grade_after_score_reconciliation, run_agent_pipeline


class DeterministicPrimaryGraderTests(unittest.TestCase):

    def test_sw02_trip_latch_reset_is_not_required_by_generic_question_patterns(self):
        from grading.evidence.fact_anchor_evidence_adapter import (
            _required_anchor_ids, evaluate_fact_anchor_requirements,
        )

        topic = "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
        topic_path = REPO / "rubrics/topic_packs" / topic
        cases = [
            (
                "Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.",
                "기계 비상정지는 수동 Reset 후 정상 조작부로 별도 재기동한다.",
            ),
            (
                "Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.",
                "원인 제거와 안전조건을 확인한 뒤 설계된 복귀 절차를 따른다.",
            ),
            (
                "제어시스템 Restart 및 Recovery 논리의 설계기준을 설명하시오.",
                "비안전 정상 시퀀스는 정의된 조건이 충족되면 자동 복귀할 수 있다.",
            ),
            (
                "Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.",
                "기계 비상정지는 수동 Reset 후 별도 재기동하고, 일반 공정 Trip은 해당 시퀀스의 복귀 방식을 따른다.",
            ),
            (
                "PLC Sequence에서 Timer, Feedback, Edge 및 Latch 적용 시 주의사항을 설명하시오.",
                "Trip latch는 보호상태를 유지하고 원인과 안전조건 확인 후 설계된 복귀 방식으로 복귀한다.",
            ),
        ]
        for question, answer in cases:
            selected, selection = _required_anchor_ids(topic_path, question)
            self.assertEqual(selection["mode"], "explicit_question_contract")
            self.assertNotIn("sw02_trip_latch_reset", selected)
            requirements = evaluate_fact_anchor_requirements(
                answer_text=answer,
                topic_ids=[topic],
                question_text=question,
            )["requirements"]
            self.assertFalse(any(
                row["requirement_id"] == "sw02_trip_latch_reset"
                for row in requirements
            ))

    def test_sil_moc_anchor_requires_bounded_comah_evidence(self):
        from grading.evidence.fact_anchor_evidence_adapter import (
            evaluate_fact_anchor_requirements,
        )

        topic = "sil_target_determination_risk_reduction_and_lifecycle"
        question = (
            "SIL 결정 방법을 설명하고 이를 실제 플랜트 운영 및 최신 산업 이슈와 연계하여 설명하시오."
        )
        cases = {
            "bounded": (
                "In the COMAH assessment context, routine maintenance and SIS-specific "
                "maintenance are documented; proof-test frequency and its frequency "
                "derivation are shown, together with the SIS modification procedure."
            ),
            "generic_record_list": (
                "All listed trend fields and all process, component, software, hazard "
                "and test-interval changes are mandatory records in every industry "
                "and jurisdiction."
            ),
        }
        statuses = {}
        for label, answer in cases.items():
            requirements = evaluate_fact_anchor_requirements(
                answer_text=answer,
                topic_ids=[topic],
                question_text=question,
            )["requirements"]
            row = next(
                item for item in requirements
                if item["requirement_id"] == "operations_moc_revalidation"
            )
            statuses[label] = row["status"]
        self.assertEqual(statuses, {"bounded": "SATISFIED", "generic_record_list": "MISSING"})

    def test_sil_unrelated_endpoint_mentions_do_not_trigger_provisional_review(self):
        topic = "sil_target_determination_risk_reduction_and_lifecycle"
        rows = [
            {"owner_topic_id": topic, "requirement_id": rid, "status": "MISSING"}
            for rid in ("operations_moc_revalidation", "cyber_ai_safety_boundary")
        ]
        spans = [
            {
                "source_text": "단종 및 변경 부품의 버전과 인증 상태를 형상관리한다.",
                "concept_candidates": ["safety_change"],
            },
            {
                "source_text": (
                    "AI가 작성한 코드는 verification과 traceability를 확보하고 "
                    "운영 프로그램과 데이터 프로그램을 분리한다."
                ),
                "concept_candidates": ["ai_generated_change", "verification"],
            },
        ]
        self.assertEqual(_unresolved_requirement_ids(spans, rows, [topic]), [])

    def test_sil_ambiguous_required_relation_remains_provisional(self):
        topic = "sil_target_determination_risk_reduction_and_lifecycle"
        rows = [
            {"owner_topic_id": topic, "requirement_id": rid, "status": "MISSING"}
            for rid in ("operations_moc_revalidation", "cyber_ai_safety_boundary")
        ]
        spans = [
            {
                "source_text": "안전 변경과 MOC 재검증의 관계를 검토한다.",
                "concept_candidates": ["safety_change", "moc_revalidation"],
            },
            {
                "source_text": "AI 변경과 안전 생애주기 관리의 관련성을 검토한다.",
                "concept_candidates": ["ai_generated_change", "safety_lifecycle_controls"],
            },
            {
                "source_text": "OT 보안과 기능안전의 상호 영향을 검토한다.",
                "concept_candidates": ["ot_security", "functional_safety_interaction"],
            },
        ]
        self.assertEqual(
            _unresolved_requirement_ids(spans, rows, [topic]),
            ["cyber_ai_safety_boundary", "operations_moc_revalidation"],
        )

    def test_sil_reviewed_case_keeps_missing_credit_without_false_hold(self):
        from grading.scoring.grade_submission_normalizer import normalize_grade_submission
        from grading.quality.expert_accuracy_benchmark import load_jsonl, validate_gold_case
        from scripts.regrade_expert_accuracy_seed import _fixture_input

        cases = load_jsonl(REPO / "calibration/expert_accuracy_golden.jsonl", validate_gold_case)
        case = next(row for row in cases if row["case_id"] == "sil_target_operations_issue1")
        submission = normalize_grade_submission(_fixture_input(case))
        grade = grade_deterministically(
            question_text=submission["question_text"],
            answer_text=submission["answer_text"],
            qualitative_de_mode="off",
        )
        targets = {"operations_moc_revalidation", "cyber_ai_safety_boundary"}
        statuses = {
            row["requirement_id"]: row["status"]
            for row in grade["requirements"]
            if row["requirement_id"] in targets
        }
        self.assertEqual(statuses, {rid: "MISSING" for rid in targets})
        self.assertFalse(targets & set(grade["resolution_review"]["requirement_ids"]))
        self.assertTrue(grade["logic_check_evaluation"]["fatal_error_detected"])
        self.assertFalse(grade["passing_score_allowed"])

    def test_sil_original_and_corrected_answers_preserve_safety_boundary(self):
        import json

        fixture = json.loads(
            (
                REPO / "calibration/sil_target_operations_overgrading_regression.json"
            ).read_text(encoding="utf-8")
        )

        focus = {
            "operations_moc_revalidation",
            "cyber_ai_safety_boundary",
        }

        grades = {}

        for label, answer in (
            ("original", fixture["original_answer"]),
            ("corrected", fixture["corrected_answer"]),
        ):
            grades[label] = grade_deterministically(
                question_text=fixture["question"],
                answer_text=answer,
                qualitative_de_mode="off",
            )

        original = grades["original"]
        corrected = grades["corrected"]

        self.assertTrue(
            original["logic_check_evaluation"]["fatal_error_detected"]
        )
        self.assertFalse(original["passing_score_allowed"])

        original_status = {
            row["requirement_id"]: row["status"]
            for row in original["requirements"]
            if row["requirement_id"] in focus
        }

        corrected_status = {
            row["requirement_id"]: row["status"]
            for row in corrected["requirements"]
            if row["requirement_id"] in focus
        }

        self.assertEqual(set(original_status), focus)
        self.assertNotIn("SATISFIED", original_status.values())

        self.assertEqual(
            corrected_status,
            {key: "SATISFIED" for key in focus},
        )
        self.assertFalse(
            corrected["logic_check_evaluation"]["fatal_error_detected"]
        )

    def test_provider_free_grade_has_public_score_and_fatal_consistency(self):
        grade = grade_deterministically(
            question_text="SIL 결정 방법을 설명하시오.",
            answer_text="lambda_SIS 비율이 PFD 비율보다 작도록 설계한다.",
        )
        self.assertEqual(grade["provider_calls"], 0)
        self.assertEqual(grade["llm_verdict_authority"], 0)
        self.assertTrue(grade["logic_check_evaluation"]["fatal_error_detected"])
        self.assertFalse(grade["official_pass_met"])
        self.assertFalse(grade["passing_score_allowed"])
        from grading.quality.expert_accuracy_benchmark import prediction_from_grade
        predicted = prediction_from_grade("synthetic-fatal-case", grade)
        self.assertFalse(predicted["passing_score_allowed"])

    def test_persistence_is_provider_neutral_json(self):
        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과로 온도차에 따른 열기전력을 측정한다.",
        )
        with tempfile.TemporaryDirectory() as directory:
            raw = persist_deterministic_grade(directory, grade)
            self.assertIn("DETERMINISTIC_GRADING_PRIMARY_V1", raw)
            self.assertTrue((Path(directory) / "deterministic_grade.json").is_file())
            quality_path = Path(directory) / "quality_checksheet.json"
            self.assertTrue(quality_path.is_file())
            quality = json.loads(quality_path.read_text(encoding="utf-8"))
            self.assertEqual(quality["score_effect"], "none")
            self.assertEqual(quality_path.stat().st_mode & 0o777, 0o600)

    def test_production_entrypoint_bypasses_llm_callable(self):
        calls = []

        def forbidden_call(prompt):
            calls.append(prompt)
            raise AssertionError("external LLM must not be called")

        with tempfile.TemporaryDirectory() as directory, patch.dict(
            "os.environ", {"DETERMINISTIC_GRADING_PRIMARY": "true"}, clear=False,
        ):
            _, grade = run_agent_pipeline(
                call_ollama_fn=forbidden_call,
                raw_text=(
                    "[문제] 열전대 온도센서의 측정 원리를 설명하시오.\n"
                    "[답안]\n열전대는 제벡 효과에 따른 열기전력을 측정한다."
                ),
                rubric={}, sid="deterministic-primary-test", image_count=0,
                session_dir=directory,
            )
        self.assertEqual(calls, [])
        self.assertEqual(grade["marker"], "DETERMINISTIC_GRADING_PRIMARY_V1")
        self.assertGreater(grade["total_score"], 0.0)
        # The production entrypoint persists a separate, score-neutral sheet.
        self.assertEqual(grade["llm_verdict_authority"], 0)

    def test_reconciler_cannot_call_llm_or_change_deterministic_grade(self):
        from grading.scoring.grade_score_reconciler import reconcile_grade_score

        grade = {
            "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
            "total_score": 14.5,
            "max_score": 25.0,
            "verdict": "FAIL",
            "deterministic_score": {
                "total_score": 14.5,
                "raw_score": 16.37,
                "applied_ceiling": 14.5,
            },
        }
        result = reconcile_grade_score(
            parsed=grade,
            raw_text="unused",
            call_llm_fn=lambda _: (_ for _ in ()).throw(AssertionError("LLM called")),
        )
        self.assertIs(result, grade)

    def test_legacy_finalizers_cannot_change_deterministic_grade(self):
        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과에 따른 열기전력을 측정한다.",
        )
        result = finalize_grade_after_score_reconciliation(grade)
        self.assertIs(result, grade)
        self.assertEqual(result["total_score"], grade["deterministic_score"]["total_score"])

    def test_telegram_formatting_does_not_call_llm(self):
        import bot

        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대는 제벡 효과에 따른 열기전력을 측정한다.",
        )
        with patch.object(
            bot,
            "call_ollama",
            side_effect=AssertionError("LLM called"),
        ):
            rendered = bot.format_result(grade)
        self.assertIn("채점 완료:", rendered)
        self.assertIn("[결정론적 요구 판정]", rendered)
        self.assertEqual(grade["verdict"], grade["deterministic_score"]["verdict"])

    def test_telegram_breakdown_rounds_display_only_and_lists_missing_ids(self):
        import bot

        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text="열전대를 언급한다.",
        )
        grade["breakdown"][1]["score"] = 4.434783
        rendered = bot.format_result(grade)
        self.assertIn("4.43/6", rendered)
        self.assertNotIn("4.434783/6", rendered)
        self.assertIn("누락 요구:", rendered)
        self.assertEqual(grade["breakdown"][1]["score"], 4.434783)

    def test_partial_mentions_alone_cannot_reach_passing_score(self):
        grade = grade_deterministically(
            question_text=(
                "제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, "
                "시스템 시험과 SIL 달성을 위한 검증 방안을 설명하시오."
            ),
            answer_text=(
                "V-Model과 검증, 시험, 시스템, 요구사항, 인터페이스, 모델, "
                "복잡도, 변경관리의 필요성을 언급한다."
            ),
        )
        score = grade["deterministic_score"]
        self.assertFalse(score["pass_evidence_eligible"])
        self.assertLess(grade["total_score"], 15.0)

    def test_explicitly_omitted_requirement_remains_missing_but_final(self):
        # These reviewed answers expressly say the second demand was not
        # explained. Neither is a semantic parsing ambiguity.
        fixture = json.loads(
            (REPO / "calibration/risk_golden/stage50_54_priority_bundle_cases.json")
            .read_text(encoding="utf-8")
        )
        cases = {
            case["case_id"]: case for case in fixture["cases"]
            if case["case_id"] in {"risk_nyquist_partial_01", "risk_lead_lag_partial_01"}
        }
        expected = {
            "risk_nyquist_partial_01": "argument_principle_pnz_relation",
            "risk_lead_lag_partial_01": "lag_compensator_design",
        }
        self.assertEqual(set(cases), set(expected))
        for case_id, missing_id in expected.items():
            with self.subTest(case_id=case_id):
                row = cases[case_id]
                grade = grade_deterministically(
                    question_text=row["question"],
                    answer_text=row["answer"],
                    qualitative_de_mode="off",
                )
                status_by_id = {
                    req["requirement_id"]: req["status"]
                    for req in grade["requirements"]
                }
                self.assertEqual(status_by_id[missing_id], "MISSING")
                self.assertFalse(grade["resolution_review"]["required"])
                self.assertEqual(grade["resolution_review"]["score_status"], "final")
                self.assertEqual(grade["total_score"], grade["deterministic_score"]["total_score"])
                self.assertFalse(grade["official_pass_met"])

    def test_wrong_scoring_group_does_not_stay_provisional_for_duplicate_missing_row(self):
        # The reviewed integration-test answer contains an explicit HFT/software
        # category error. Both rows share the approved scoring group; the
        # unresolved interface mention cannot overturn that WRONG outcome.
        from grading.scoring.grade_submission_normalizer import normalize_grade_submission
        from grading.quality.expert_accuracy_benchmark import load_jsonl, validate_gold_case
        from scripts.regrade_expert_accuracy_seed import _fixture_input

        cases = load_jsonl(REPO / "calibration/expert_accuracy_golden.jsonl", validate_gold_case)
        case = next(row for row in cases if row["case_id"] == "mcdc_vmodel_sil_issue1")
        submission = normalize_grade_submission(_fixture_input(case))
        grade = grade_deterministically(
            question_text=submission["question_text"],
            answer_text=submission["answer_text"],
            qualitative_de_mode="off",
        )
        by_id = {row["requirement_id"]: row for row in grade["requirements"]}
        self.assertEqual(by_id["sw04_integration_test"]["status"], "MISSING")
        self.assertEqual(by_id["hardware_architecture_test_boundary"]["status"], "WRONG")
        self.assertEqual(
            by_id["sw04_integration_test"]["score_group_id"],
            by_id["hardware_architecture_test_boundary"]["score_group_id"],
        )
        self.assertEqual(grade["resolution_review"]["requirement_ids"], [])
        self.assertEqual(grade["resolution_review"]["score_status"], "final")
        self.assertTrue(grade["logic_check_evaluation"]["fatal_error_detected"])

    def test_sil_band_outline_heading_is_not_unresolved_evidence(self):
        from grading.scoring.grade_submission_normalizer import normalize_grade_submission
        from grading.quality.expert_accuracy_benchmark import load_jsonl, validate_gold_case
        from scripts.regrade_expert_accuracy_seed import _fixture_input

        cases = load_jsonl(REPO / "calibration/expert_accuracy_golden.jsonl", validate_gold_case)
        case = next(row for row in cases if row["case_id"] == "sis_lopa_architecture_issue1")
        submission = normalize_grade_submission(_fixture_input(case))
        grade = grade_deterministically(
            question_text=submission["question_text"],
            answer_text=submission["answer_text"],
            qualitative_de_mode="off",
        )
        by_id = {row["requirement_id"]: row["status"] for row in grade["requirements"]}
        self.assertEqual(by_id["hazop_lopa_sil_band_mapping"], "MISSING")
        self.assertEqual(grade["resolution_review"]["requirement_ids"], [])
        self.assertEqual(grade["resolution_review"]["score_status"], "final")
        self.assertTrue(grade["logic_check_evaluation"]["fatal_error_detected"])

    def test_unrelated_wrong_group_cannot_hide_an_unresolved_missing_demand(self):
        topic = "lead_lag_compensator_phase_margin_steady_state_error"
        rows = [
            {"owner_topic_id": topic, "requirement_id": "lag_compensator_design",
             "score_group_id": "lag_compensator_design", "status": "MISSING"},
            {"owner_topic_id": topic, "requirement_id": "lead_compensator_design",
             "score_group_id": "lead_compensator_design", "status": "WRONG"},
        ]
        span = [{"source_text": "지상 보상기와 정상상태 정확도 사이의 관계",
                 "concept_candidates": ["lag_compensator", "steady_state_accuracy"]}]
        self.assertEqual(
            _unresolved_requirement_ids(span, rows, [topic]),
            ["lag_compensator_design"],
        )

    def test_unexplained_relation_still_requires_provisional_review(self):
        topic = "lead_lag_compensator_phase_margin_steady_state_error"
        requirements = [{
            "owner_topic_id": topic,
            "requirement_id": "lag_compensator_design",
            "status": "MISSING",
        }]
        ambiguous = [{
            "source_text": "지상 보상기와 정상상태 정확도 사이의 관계",
            "concept_candidates": ["lag_compensator", "steady_state_accuracy"],
        }]
        self.assertEqual(
            _unresolved_requirement_ids(ambiguous, requirements, [topic]),
            ["lag_compensator_design"],
        )
        explicit_omission = [{
            **ambiguous[0],
            "source_text": "지상 보상기의 정상상태 정확도 개선 원리는 설명하지 못했다.",
        }]
        self.assertEqual(
            _unresolved_requirement_ids(explicit_omission, requirements, [topic]),
            [],
        )

    def test_explicit_gap_with_two_missing_demands_remains_provisional(self):
        topic = "lead_lag_compensator_phase_margin_steady_state_error"
        requirements = [
            {"owner_topic_id": topic, "requirement_id": "lead_compensator_design",
             "status": "MISSING"},
            {"owner_topic_id": topic, "requirement_id": "lag_compensator_design",
             "status": "MISSING"},
        ]
        spans = [{
            "source_text": "진상 보상기는 설명하지 못했지만 지상 보상기는 보완이 필요하다.",
            "concept_candidates": ["lead_compensator", "lag_compensator"],
        }]
        self.assertEqual(
            _unresolved_requirement_ids(spans, requirements, [topic]),
            ["lag_compensator_design", "lead_compensator_design"],
        )

    def test_explicit_gap_cannot_finalize_unrelated_ambiguous_demand(self):
        topic = "lead_lag_compensator_phase_margin_steady_state_error"
        requirements = [{
            "owner_topic_id": topic, "requirement_id": "lag_compensator_design",
            "status": "MISSING",
        }]
        spans = [{
            "source_text": "진상 보상기는 설명하지 못했지만 지상 보상기는 추가 검토가 필요하다.",
            "concept_candidates": ["lead_compensator", "lag_compensator"],
        }]
        self.assertEqual(
            _unresolved_requirement_ids(spans, requirements, [topic]),
            ["lag_compensator_design"],
        )

    def test_many_missing_with_unresolved_spans_exposes_recall_warning(self):
        import bot

        fixture = json.loads(
            (REPO / "calibration/sis_lopa_architecture_overgrading_regression.json")
            .read_text(encoding="utf-8")
        )
        grade = grade_deterministically(
            question_text=fixture["question"], answer_text=fixture["answer"],
        )
        diagnostic = grade["evidence_recall_diagnostic"]
        self.assertEqual(diagnostic["code"], "LOW_EVIDENCE_RECALL")
        self.assertTrue(diagnostic["warning"])
        self.assertEqual(diagnostic["score_effect"], "none")
        self.assertIn("LOW_EVIDENCE_RECALL", bot.format_result(grade))


if __name__ == "__main__":
    unittest.main()
