import json
import unittest
from pathlib import Path
from unittest.mock import patch

from grading.evidence import fact_anchor_evidence_adapter as adapter
from grading.evidence.engineering_invariant_evaluator import (
    evaluate_engineering_invariants,
)
from grading.evidence.fact_anchor_scoring_exclusions import (
    excluded_from_scoring,
)
from grading.scoring.deterministic_primary_grader import (
    DeterministicPrimaryError,
    grade_deterministically,
)

ROOT = Path(__file__).resolve().parents[1]

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"

CANDIDATES = {
    "ipgse_scope_chain",
    "ipgse_emi_coupling_paths",
    "ipgse_power_quality_scope",
    "ipgse_final_verification",
}

ALL_REQUIRED = CANDIDATES | {"ipgse_diagnostic_workflow"}

CODES = {
    "EMC_UNSAFE_PE_DISCONNECTION",
    "EMC_SHIELD_ONE_END_UNIVERSAL",
    "EMC_UPS_UNIVERSAL_FIX",
}

QUESTION = (
    "계장 시스템의 전원, 접지, 차폐와 EMC 문제를 "
    "진단하고 대책을 설명하시오."
)

# (case_id, answer, expected EMC invariant code)
CASES = [
    (
        "wrong_pe",
        "계장 노이즈를 없애기 위해 보호접지 PE를 제거한다.",
        "EMC_UNSAFE_PE_DISCONNECTION",
    ),
    (
        "wrong_pe_variant",
        "계장 잡음 감소를 위해 보호접지 PE를 분리해야 한다.",
        "EMC_UNSAFE_PE_DISCONNECTION",
    ),
    (
        "wrong_shield",
        "모든 차폐 케이블은 반드시 한쪽만 접지한다.",
        "EMC_SHIELD_ONE_END_UNIVERSAL",
    ),
    (
        "wrong_shield_variant",
        "모든 차폐 케이블은 한쪽에만 접지한다.",
        "EMC_SHIELD_ONE_END_UNIVERSAL",
    ),
    (
        "wrong_ups",
        "UPS를 사용하면 모든 EMC 문제가 해결된다.",
        "EMC_UPS_UNIVERSAL_FIX",
    ),
    (
        "wrong_ups_variant",
        "UPS를 설치하면 모든 EMI 간섭이 사라진다.",
        "EMC_UPS_UNIVERSAL_FIX",
    ),
    (
        "safe_pe",
        "보호접지 PE는 제거하지 않고 유지한다.",
        None,
    ),
    (
        "safe_pe_other_removal",
        "보호접지 PE는 유지하고 불필요한 필터를 제거한다.",
        None,
    ),
    (
        "safe_shield",
        "차폐 케이블 접지는 주파수와 본딩 구조에 따라 결정한다.",
        None,
    ),
    (
        "safe_ups",
        "UPS는 전원 유지 수단이며 모든 EMC 문제를 해결하지는 못한다.",
        None,
    ),
    (
        "safe_ups_bounded",
        "UPS는 전원 유지 수단이고 EMC 문제는 별도 대책이 필요하다.",
        None,
    ),
    (
        "rejected_wrong_pe",
        "보호접지 PE를 제거한다는 주장은 잘못이다.",
        None,
    ),
    (
        "rejected_wrong_shield",
        "모든 차폐 케이블은 반드시 한쪽 끝만 접지한다는 주장은 틀리다.",
        None,
    ),
    (
        "rejected_wrong_ups",
        "UPS로 모든 EMC 문제가 해결된다는 주장은 틀리다.",
        None,
    ),
]


class EMCFatalScopeTests(unittest.TestCase):

    def test_fatal_detection_and_rebuttal_boundaries(self):
        for name, answer, expected_code in CASES:
            with self.subTest(case=name):
                result = evaluate_engineering_invariants(
                    answer,
                    topic_ids=[TOPIC],
                )

                actual = {
                    row["code"]
                    for row in result["violations"]
                } & CODES

                expected = (
                    {expected_code}
                    if expected_code else set()
                )

                self.assertEqual(actual, expected)

    def test_topic_ownership_prevents_cross_topic_fatal(self):
        wrong_emc = (
            "계장 노이즈를 없애기 위해 보호접지 PE를 제거한다."
        )

        result = evaluate_engineering_invariants(
            wrong_emc,
            topic_ids=[
                "thermocouple_temperature_sensor_seebeck_reference_junction_compensation"
            ],
        )

        actual = {
            row["code"] for row in result["violations"]
        }

        self.assertFalse(actual & CODES)

        grade = grade_deterministically(
            question_text="열전대 온도센서의 측정 원리를 설명하시오.",
            answer_text=(
                "열전대는 제벡 효과로 온도차에 따른 열기전력을 측정한다. "
                "보호접지 PE는 유지하고 불필요한 필터를 제거한다."
            ),
            qualitative_de_mode="off",
        )

        self.assertFalse(
            grade["logic_check_evaluation"]["fatal_error_detected"]
        )

    def test_emc_positive_scoring_exclusions_remain(self):
        for anchor_id in ALL_REQUIRED:
            with self.subTest(anchor_id=anchor_id):
                self.assertTrue(
                    excluded_from_scoring(
                        topic_id=TOPIC,
                        anchor_id=anchor_id,
                    )
                )

    def test_emc_model_answer_still_abstains(self):
        data = json.loads(
            (ROOT / "calibration/expert_accuracy_model_answer_cases.json")
            .read_text(encoding="utf-8")
        )

        case = next(
            row for row in data["cases"]
            if row["case_id"].startswith(
                "model_reference_08_instrumentation_power"
            )
        )

        with self.assertRaisesRegex(
            DeterministicPrimaryError,
            "deterministic score engine abstained",
        ):
            grade_deterministically(
                question_text=case["question"],
                answer_text=case["answer"],
                qualitative_de_mode="off",
            )

    def test_fatal_reaches_final_grading_without_unblocking_facts(self):
        original = adapter.excluded_from_scoring

        def shadow(*, topic_id, anchor_id="", fact_id=""):
            if topic_id == TOPIC and anchor_id in CANDIDATES:
                return False
            return original(
                topic_id=topic_id,
                anchor_id=anchor_id,
                fact_id=fact_id,
            )

        # 이 블록 안에서만 가상 해제. 영구적인 정책 변경 없음.
        with patch.object(
            adapter,
            "excluded_from_scoring",
            side_effect=shadow,
        ):
            for name, answer, expected_code in CASES:
                with self.subTest(case=name):
                    grade = grade_deterministically(
                        question_text=QUESTION,
                        answer_text=answer,
                        qualitative_de_mode="off",
                    )

                    actual_fatal = bool(
                        grade["logic_check_evaluation"][
                            "fatal_error_detected"
                        ]
                    )
                    expected_fatal = expected_code is not None

                    self.assertEqual(
                        actual_fatal,
                        expected_fatal,
                    )

                    if expected_fatal:
                        self.assertFalse(
                            grade["passing_score_allowed"]
                        )


if __name__ == "__main__":
    unittest.main()
