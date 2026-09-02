from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from question_demand_contract import (
    ATOMIC_QUESTION_DEMAND_VERSION,
    build_question_demand_contract,
)


VMODEL_QUESTION = """🚨 [제어 소프트웨어] 개발 수명 주기(V-Model) 기반 SW 검증 방안
📌 문제 정의
제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, 시스템 시험의 정의
안전 무결성 기준(SIL) 달성을 위한 소프트웨어 검증 방안"""


def test_vmodel_question_is_four_atomic_demands() -> None:
    contract = build_question_demand_contract(VMODEL_QUESTION)
    rows = contract["requirements"]
    assert contract["atomic_question_demands_applied"] is True
    assert contract["atomic_question_demand_version"] == ATOMIC_QUESTION_DEMAND_VERSION
    assert len(rows) == 4
    assert [row["object_text"] for row in rows[:3]] == [
        "단위 시험",
        "통합 시험",
        "시스템 시험",
    ]
    assert rows[3]["demand_kind"] == "EVALUATE_VERIFY"
    assert all(row["source"] == "question_text_only" for row in rows)


def test_coordinated_actions_create_one_row_per_requested_output() -> None:
    contract = build_question_demand_contract(
        "PID 제어의 동작 원리를 설명하고 현장 튜닝 절차를 제시하시오."
    )
    assert [row["demand_kind"] for row in contract["requirements"]] == [
        "PRINCIPLE_INTERPRET",
        "PROCEDURE",
    ]
    assert {
        row["demand_kind"] for row in contract["secondary_demands"]
    } == {"PROCEDURE"}


def test_compare_and_selection_do_not_create_generic_extra_axis() -> None:
    contract = build_question_demand_contract(
        "열전대와 RTD의 특성을 비교하고 적용 조건에 따른 선정 기준을 설명하시오."
    )
    assert [row["demand_kind"] for row in contract["requirements"]] == [
        "COMPARE",
        "SELECT",
    ]
    assert contract["secondary_demands"] == []


def test_one_semantic_output_is_not_duplicated_by_keyword_kinds() -> None:
    contract = build_question_demand_contract(
        "스마트 MCC 적용 방법과 도입 효과를 평가하시오."
    )
    assert len(contract["requirements"]) == 1
    assert contract["requirements"][0]["demand_kind"] == "EVALUATE_VERIFY"
    assert set(contract["requirements"][0]["demand_kinds"]) == {
        "PROCEDURE",
        "IMPLEMENT",
        "EVALUATE_VERIFY",
    }


def test_contract_is_answer_independent_and_ids_are_stable() -> None:
    first = build_question_demand_contract(VMODEL_QUESTION)
    contaminated = build_question_demand_contract(
        VMODEL_QUESTION
        + "\n🔹 1. 배경 (Background)\n답안의 HIL, MC/DC, ALARP 내용"
    )
    assert first["requirements"] == contaminated["requirements"]
    assert first["question_hash"] == contaminated["question_hash"]


def test_compound_software_question_expands_shared_suffix_outputs() -> None:
    contract = build_question_demand_contract(
        "안전필수 소프트웨어의 V-Model과 단위·통합·시스템시험을 설명하고, "
        "SIL 관점의 정적·동적 분석, MC/DC 및 검증방안을 제시하시오."
    )
    assert len(contract["requirements"]) == 8
    assert contract["primary_lens"] == "IMPLEMENTATION_EVALUATION"
    objects = [row["object_text"] for row in contract["requirements"]]
    assert objects == [
        "안전필수 소프트웨어의 V-Model",
        "단위 시험",
        "통합 시험",
        "시스템시험",
        "SIL 관점의 정적 분석",
        "동적 분석",
        "MC/DC",
        "검증방안",
    ]


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} atomic demand contract checks")


if __name__ == "__main__":
    main()
