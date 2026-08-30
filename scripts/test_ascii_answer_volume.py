#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import grading_agents
from answer_volume import (
    ASCII_UNITS_PER_PAGE,
    VOLUME_METHOD,
    ascii_equivalent_count,
    estimate_ascii_answer_volume,
    normalize_volume_text,
)

SAMPLE_ANSWER = '/grade\n[문제] 공압식 구동기 선정 시 고려할 밸브 불평형력, 마찰력 개념 설명, Fail-Safe 동작 구현을 위한 스프링 설계 기준을 설명\n1. 배경\n  1) Actuator : Stem에 연결되어 Plug에 힘을 인가하는 역할을 수행\n  2) Linear / Rotary motion 2가지가 있음\n  3) 제어 방식으로 어느 정도 밸브를 열고 닫을지 결정\n  4) BPCS 이외에도 비상시 결과를 최소로 하기 위해 설계 필요\n\n2. 불평형력 개념 설명\n  1) Globe 밸브는 주로 actuator가 linear로 동작\n  2) 밸브 구조에 따라 Single port, Post/port guide, Cage valve로 나누어질 수 있음\n  3) Plug는 Stem에 연결되어 seat leakage를 최소로 하는 역할을 수행\n  4) Actuator는 압력 차이(ΔP = P1 - P2, P1 : Upstream, P2 : Downstream)를 극복해야 함\n  5) 불평형력은 Plug와 ΔP로 인하여 발생하는 모든 힘으로, Plug는 이를 극복 => Actuator 대형화\n  6) Balanced trim은 Plug에 압력이 걸리도록 설계되어 있어, Actuator는 조그만한 힘을 주어도 Plug 이동\n\n3. Fail Safe 동작 설명\n  1) SIS를 만족시키기 위하여 BPCS, 이상시 중지 계층, SIS, 능동적 계층, 수동적 계층, 비상대응 계층으로 분리\n  2) 이상 상황에서 안정적 상황으로 돌리는 동작이 Fail safe (Fail state는 각 공정에 따라 다를 수 있음)\n  3) 에너지를 공급하는 공정이라면 Fail Close로 연료 공급 차단\n  4) 압력이 증가하는 공정이라면 Fail Open으로 압력 개방\n\n4. Spring 설계 기준\n  1) 밸브를 선정 후 설치 시 bench set 필요\n  2) Bench set은 구동 압력 시작과 끝으로 Stem Stroke를 조정하는 작업\n  3) 이때 시작 압력을 스프링 길이(장력)로 조절\n  4) Actuator에 걸리는 힘 Factuator = 모터/압축공기에서 한 힘 + 스프링 장력(탄성)에 의한 힘이 포함\n  5) 수식으로 표현하면 :\n     Factuator = F불평형 + Fseat load + F마찰력 + F기타\n  6) 따라서 불평형력과 시트 로딩(기밀과 관련), 마찰력을 극복하는 힘의 actuator가 필요\n\n5. 마찰력\n  1) 마찰력은 대부분 Valve stem을 body가 잡아주기 때문에 발생함\n  2) 밸브가 닫히기 직전에도 가장 큰 힘이 필요하고, 여기에 마찰력이 포함됨\n\n6. 결론\n  1) 밸브 선정 후 동작 압력에 따른 스트로크 동작 보증을 위해서는 bench set으로 스프링 조절 필요\n  2) 불평형력은 유체 상·하에 따른 고유 압력, 플러그 면적에 따라 힘으로 변환\n  3) 마찰력은 밸브 기밀을 위해서 필요\n  4) Actuator가 극복하는 힘은 마찰력, 불평형력, Seat load 힘\n  5) Fail safe일 경우 Actuator는 0의 힘을 발생\n     => 스프링은 이를 온전하게 극복하여 Safe 위치로 이동\n     => Fspring = F불평형 + Fseat load + F기타.\n끝.\n'


class AsciiEquivalentRegressionTests(unittest.TestCase):
    def test_ascii_visible_character_is_one_unit(self) -> None:
        self.assertEqual(ascii_equivalent_count("abc123"), 6)

    def test_non_ascii_character_is_two_units(self) -> None:
        self.assertEqual(ascii_equivalent_count("한Δ"), 4)

    def test_whitespace_is_not_counted(self) -> None:
        self.assertEqual(
            ascii_equivalent_count("a b\n한\t"),
            4,
        )

    def test_control_lines_are_removed(self) -> None:
        normalized = normalize_volume_text(
            "/grade\n[문제] 문제 문장\n1. 답안\n끝."
        )
        self.assertEqual(normalized, "1. 답안")


    def test_problem_and_answer_same_line_after_separator_is_preserved(
        self,
    ) -> None:
        answer = "1. 배경\n" + ("a" * 1500)
        text = (
            "/grade\n"
            "문제: 반응기 과압력 SIL 결정과 SIS 아키텍처 설명"
            + ("=" * 80)
            + answer
            + "\n끝."
        )
        normalized = normalize_volume_text(text)
        self.assertEqual(normalized, answer)

        result = estimate_ascii_answer_volume(text)
        self.assertEqual(result["level"], "three_page_text")
        self.assertIsNone(result["cap"])

    def test_line_breaks_do_not_change_volume(self) -> None:
        continuous = "a" * 1200
        split = "\n".join(["a" * 100] * 12)
        self.assertEqual(
            ascii_equivalent_count(continuous),
            ascii_equivalent_count(split),
        )
        self.assertEqual(
            estimate_ascii_answer_volume(continuous)["cap"],
            estimate_ascii_answer_volume(split)["cap"],
        )


class ThresholdRegressionTests(unittest.TestCase):
    def assert_volume(
        self,
        ascii_count: int,
        *,
        level: str,
        pages: int,
        cap: float | None,
    ) -> None:
        result = estimate_ascii_answer_volume(
            "a" * ascii_count
        )
        self.assertEqual(result["ascii_equivalent_count"], ascii_count)
        self.assertEqual(result["level"], level)
        self.assertEqual(
            result["estimated_answer_sheet_pages"],
            pages,
        )
        self.assertEqual(result["cap"], cap)
        self.assertEqual(
            result["measurement_method"],
            VOLUME_METHOD,
        )
        self.assertFalse(result["image_count_used"])
        self.assertFalse(result["pdf_page_count_used"])
        self.assertFalse(result["line_count_used"])

    def test_299_ascii_units_is_short_answer(self) -> None:
        self.assert_volume(
            299,
            level="text_only_short_answer",
            pages=0,
            cap=9.0,
        )

    def test_300_ascii_units_is_less_than_one_page(self) -> None:
        self.assert_volume(
            300,
            level="less_than_one_page_text",
            pages=1,
            cap=10.5,
        )

    def test_600_ascii_units_is_one_page(self) -> None:
        self.assert_volume(
            600,
            level="one_page_text",
            pages=1,
            cap=13.0,
        )

    def test_899_ascii_units_remains_one_page(self) -> None:
        self.assert_volume(
            899,
            level="one_page_text",
            pages=1,
            cap=13.0,
        )

    def test_900_ascii_units_is_two_pages(self) -> None:
        self.assert_volume(
            900,
            level="two_page_text",
            pages=2,
            cap=19.0,
        )

    def test_1499_ascii_units_remains_two_pages(self) -> None:
        self.assert_volume(
            1499,
            level="two_page_text",
            pages=2,
            cap=19.0,
        )

    def test_1500_ascii_units_is_three_pages(self) -> None:
        self.assert_volume(
            1500,
            level="three_page_text",
            pages=3,
            cap=None,
        )

    def test_2099_ascii_units_remains_three_pages(self) -> None:
        self.assert_volume(
            2099,
            level="three_page_text",
            pages=3,
            cap=None,
        )

    def test_2100_ascii_units_is_four_pages(self) -> None:
        self.assert_volume(
            2100,
            level="four_page_text",
            pages=4,
            cap=None,
        )


class IntegrationRegressionTests(unittest.TestCase):
    def test_user_session_fixture_is_three_pages(self) -> None:
        result = estimate_ascii_answer_volume(SAMPLE_ANSWER)
        self.assertEqual(result["ascii_equivalent_count"], 1700)
        self.assertTrue(
            math.isclose(
                result["page_equivalent"],
                2.83,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
        self.assertEqual(
            result["estimated_answer_sheet_pages"],
            3,
        )
        self.assertEqual(result["level"], "three_page_text")
        self.assertIsNone(result["cap"])

    def test_grading_agents_wrapper_ignores_image_count(self) -> None:
        text = "a" * 1200
        without_image = (
            grading_agents._phase2_estimate_volume_level(
                text,
                0,
            )
        )
        with_images = (
            grading_agents._phase2_estimate_volume_level(
                text,
                99,
            )
        )
        self.assertEqual(without_image, with_images)
        self.assertEqual(without_image["cap"], 19.0)
        self.assertFalse(without_image["image_count_used"])

    def test_three_page_volume_does_not_cap_scores(self) -> None:
        volume = estimate_ascii_answer_volume("a" * 1500)
        layers = [
            {"layer_id": "X1", "score": 5.0},
            {"layer_id": "X2", "score": 5.0},
            {"layer_id": "X3", "score": 5.0},
            {"layer_id": "X4", "score": 5.0},
            {"layer_id": "X5", "score": 5.0},
        ]
        before, after, applied = grading_agents._phase2_apply_caps(
            layers,
            volume,
        )
        self.assertEqual(before, 25.0)
        self.assertEqual(after, 25.0)
        self.assertEqual(applied, [])

    def test_two_page_volume_caps_scores_at_nineteen(self) -> None:
        volume = estimate_ascii_answer_volume("a" * 1200)
        layers = [
            {"layer_id": "X1", "score": 5.0},
            {"layer_id": "X2", "score": 5.0},
            {"layer_id": "X3", "score": 5.0},
            {"layer_id": "X4", "score": 5.0},
            {"layer_id": "X5", "score": 5.0},
        ]
        before, after, applied = grading_agents._phase2_apply_caps(
            layers,
            volume,
        )
        self.assertEqual(before, 25.0)
        self.assertTrue(
            math.isclose(
                after,
                19.0,
                rel_tol=0.0,
                abs_tol=0.01,
            )
        )
        self.assertEqual(applied[0]["cap"], 19.0)

    def test_ascii_units_per_page_contract(self) -> None:
        self.assertEqual(ASCII_UNITS_PER_PAGE, 600)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(
        __import__(__name__)
    )
    count = suite.countTestCases()
    print(
        "ASCII_VOLUME_TEST_INVENTORY "
        f"classes=3 tests={count}"
    )
    if count != 20:
        raise RuntimeError(
            f"Expected 20 tests, discovered {count}"
        )
    result = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)
    print(
        "ASCII_VOLUME_TEST_RESULT "
        f"run={result.testsRun} "
        f"failures={len(result.failures)} "
        f"errors={len(result.errors)}"
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
