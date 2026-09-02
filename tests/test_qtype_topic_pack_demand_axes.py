from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from question_demand_contract import (
    _load_topic_pack_demand_axis_contracts,
    build_question_demand_contract,
)


CASE_ROOT = ROOT / "calibration" / "qtype_golden" / "cases"


def test_reviewed_qtype_demands_are_published_question_only() -> None:
    _load_topic_pack_demand_axis_contracts.cache_clear()
    seen_questions: set[str] = set()
    for path in sorted(CASE_ROOT.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for case in payload["cases"]:
            question = str(case["question"])
            if question in seen_questions:
                continue
            seen_questions.add(question)
            contract = build_question_demand_contract(question)
            expected = case["expected"]["question_demands"]
            assert [row["requirement_id"] for row in contract["requirements"]] == [
                row["id"] for row in expected
            ]
            assert contract["primary_lens"] == payload["question_type"]
            assert contract["topic_pack_demand_axes"]["topic_id"] == (
                case["expected"]["expected_topic_ids"][0]
            )


if __name__ == "__main__":
    test_reviewed_qtype_demands_are_published_question_only()
    print("QTYPE_TOPIC_PACK_DEMAND_AXES_TESTS=1_PASS")
