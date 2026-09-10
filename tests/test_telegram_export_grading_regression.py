import unittest

from deterministic_primary_grader import grade_deterministically


class TelegramExportGradingRegressionTests(unittest.TestCase):
    def test_vmodel_question_activates_only_explicit_cross_topic_demands(self):
        question = (
            "제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, "
            "시스템 시험의 정의와 안전 무결성 기준(SIL) 달성을 위한 "
            "소프트웨어 검증 방안을 설명하시오."
        )
        answer = """
1. V-Model
요구사항과 설계, 구현에 대응하여 단위시험, 통합시험, 시스템시험을 수행한다.
단위시험은 함수와 모듈의 세부 요구사항을 격리하여 검증한다.
통합시험은 모듈 간 인터페이스와 상호작용을 검증한다.
시스템시험은 통합 시스템이 시스템 요구사항과 운전환경을 만족하는지 확인한다.
2. SIL 검증
Verification은 단계별 산출물이 입력 명세를 만족하는지 확인하고 Validation은
통합된 시스템이 의도된 사용목적과 안전 요구사항을 만족하는지 확인한다.
요구사항-설계-코드-시험-결과의 양방향 RTM을 유지한다.
Compiler, CPU, library와 시험환경의 version을 baseline으로 형상관리하고 변경 시
영향분석, 회귀시험 및 필요한 재검증을 수행한다.
"""
        grade = grade_deterministically(question_text=question, answer_text=answer)
        self.assertTrue(grade["question_scope_evaluation"]["resolved"])
        self.assertLessEqual(grade["deterministic_score"]["raw_requirement_count"], 16)

    def test_second_order_answer_missing_zero_and_negative_damping_is_not_high_score(self):
        question = (
            "2차 지연시스템의 응답 특성을 감쇠비에 따라 구분하고, "
            "그 특성을 비교하여 설명하시오."
        )
        answer = """
1. 표준형
G(s)=Kωn²/(s²+2ζωns+ωn²)이며 감쇠비는 진동성과 오버슈트를 결정한다.
2. 비교
0<ζ<1은 복소극점과 감쇠진동 및 오버슈트가 있고, ζ=1은 중근으로
오버슈트 없이 응답하며, ζ>1은 서로 다른 실근으로 느리게 응답한다.
극점은 -ζωn±jωn√(1-ζ²)이다.
3. 부가 설명
시간지연은 위상여유를 감소시키며 FOC와 센서리스 제어를 적용할 수 있다.
""" + "부가 현장 설명 " * 400
        grade = grade_deterministically(question_text=question, answer_text=answer)
        self.assertTrue(grade["question_scope_evaluation"]["resolved"])
        self.assertFalse(grade["high_score_met"])
        self.assertLess(grade["total_score"], 20.0)
        statuses = {
            row["requirement_id"]: row["status"] for row in grade["requirements"]
        }
        self.assertIn(statuses["so2_zero_negative_damping"], {"PARTIAL", "MISSING"})

    def test_actuator_comparison_does_not_activate_unrelated_entire_pack(self):
        question = (
            "공압식, 전동식, 유압식 제어밸브 액추에이터의 구조와 동작원리, "
            "장단점, 적용조건, 에너지원 상실 시 fail-safe 특성과 현장 선정기준을 비교하시오."
        )
        answer = """
공압식은 diaphragm 또는 piston과 spring, positioner로 구성되며 공기압으로
force를 만든다. Spring-return은 공기 상실 시 fail-open 또는 fail-close로 간다.
전동식은 motor와 gear 및 위치검출기로 구성되고 정전 시 일반적으로 정지하므로
spring 또는 battery 같은 저장에너지가 있어야 안전 위치로 이동한다.
유압식은 pump, 방향밸브와 cylinder의 고압 작동유로 큰 추력을 만들며 accumulator와
dump 회로로 안전 위치를 구현할 수 있지만 누유와 오염관리가 필요하다.
필요 force·torque, 속도, duty, 동력원, 방폭, 유지보수와 lifecycle cost로 선정한다.
"""
        grade = grade_deterministically(question_text=question, answer_text=answer)
        self.assertEqual(
            grade["topic_id"],
            "control_valve_types_globe_rotary_body_actuator_selection",
        )
        self.assertTrue(grade["question_scope_evaluation"]["resolved"])
        self.assertLessEqual(grade["deterministic_score"]["raw_requirement_count"], 6)
        hydraulic = next(
            row for row in grade["requirements"]
            if row["requirement_id"] == "hydraulic_actuator_force_and_stored_energy_fail_safe"
        )
        self.assertIn(hydraulic["status"], {"SATISFIED", "PARTIAL"})


if __name__ == "__main__":
    unittest.main()
