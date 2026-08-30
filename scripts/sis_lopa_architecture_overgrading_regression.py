#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from answer_volume import estimate_ascii_answer_volume, normalize_volume_text

HAZOP = "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
FSRM = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
HAZARDOUS_AREA = (
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection"
)
FATAL_ID = "failure_rate_compared_directly_to_pfd"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fatal_ids(items: list[Any]) -> set[str]:
    result: set[str] = set()
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result.add(item["id"])
        elif isinstance(item, str):
            match = re.match(r"\s*\[([^\]]+)\]", item)
            if match:
                result.add(match.group(1))
    return result


def main() -> None:
    fixture = load_json(
        REPO / "calibration"
        / "sis_lopa_architecture_overgrading_regression.json"
    )
    hazop_model = load_json(
        REPO / "rubrics" / "topic_packs" / HAZOP / "model_answer.json"
    )
    fsrm_logic = load_json(
        REPO / "rubrics" / "topic_packs" / FSRM / "logic_check.json"
    )

    expected = fixture["expected"]
    volume_expected = expected["volume"]
    inline_submission = (
        "/grade\n"
        "문제: "
        + fixture["question"]
        + ("=" * 80)
        + fixture["answer"]
        + "\n끝."
    )

    normalized = normalize_volume_text(inline_submission)
    expected_normalized = normalize_volume_text(fixture["answer"])
    assert normalized == expected_normalized
    assert normalized != fixture["answer"]

    volume = estimate_ascii_answer_volume(inline_submission)
    assert volume["ascii_equivalent_count"] == 1755
    assert volume["ascii_equivalent_count"] == volume_expected["ascii_equivalent_count"]
    assert volume["page_equivalent"] == 2.92
    assert volume["level"] == "three_page_text"
    assert volume["cap"] is None
    assert volume_expected["volume_cap_allowed"] is False

    patterns = hazop_model["expected_question_patterns"]
    assert any(
        item.get("intent")
        == "reactor overpressure target SIL determination and "
        "SIS architecture handoff"
        for item in patterns
    )

    aliases = set(hazop_model["routing_aliases"])
    assert {
        "반응기 과압력 시나리오 SIL 결정 과정",
        "과압력 시나리오 목표 SIL 결정",
        "기존 보호장치 불충분 SIS 도입",
        "SIL 결정과 SIS 아키텍처",
    } <= aliases

    ids = fatal_ids(fsrm_logic["llm_profile"]["fatal_conditions"])
    assert FATAL_ID in ids
    assert fsrm_logic["deterministic_checks"]["enabled"] is False

    fatal_text = "\n".join(fsrm_logic["llm_profile"]["fatal_conditions"])
    assert "lambda_SIS" in fatal_text
    assert "차원이 다르므로 직접 비교할 수 없다" in fatal_text

    topics = fixture["expected_topics"]
    assert topics["primary"] == HAZOP
    assert topics["adjacent"] == [FSRM]
    assert topics["forbidden"] == [HAZARDOUS_AREA]

    statuses = expected["demand_status"]
    assert sum(value == "present" for value in statuses.values()) == 1
    assert sum(value == "partial" for value in statuses.values()) == 4
    assert sum(value == "incorrect" for value in statuses.values()) == 2
    assert sum(value == "missing" for value in statuses.values()) == 1

    assert expected["requirements_full_credit_allowed"] is False
    assert expected["strong_verdict_allowed"] is False
    assert expected["passing_score_allowed"] is False
    assert expected["maximum_total_score"] == 13.0
    assert expected["total_range"]["max"] == 13.0
    assert FATAL_ID in expected["required_fatal_ids"]

    forbidden = "\n".join(expected["forbidden_feedback_elements"])
    assert "100%" in forbidden
    assert "0.5쪽 미만" in forbidden
    assert "9.0점" in forbidden
    assert "15점 이상" in forbidden

    print("SIS_LOPA_ARCHITECTURE_OVERGRADING_REGRESSION=PASS")
    print("INLINE_ANSWER_ASCII_COUNT=1755")
    print("INLINE_ANSWER_LEVEL=three_page_text")
    print("VOLUME_CAP=NONE")
    print(f"PRIMARY_TOPIC={HAZOP}")
    print(f"ADJACENT_TOPIC={FSRM}")
    print(f"FATAL_ID={FATAL_ID}")
    print("DEMAND_STATUS=present:1,partial:4,incorrect:2,missing:1")
    print("TOTAL_MAX=13.0")


if __name__ == "__main__":
    main()
