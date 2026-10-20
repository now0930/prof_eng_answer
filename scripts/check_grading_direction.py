#!/usr/bin/env python3
"""Narrow static and runtime guard for D/E shadow development.

This does not certify semantic validity, model stability, or expert accuracy.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BASELINE = "af0dc3333619e2db42598ade22b7adf1db9a6443"
PROTECTED = (
    "grading/scoring/deterministic_score_engine.py",
    "grading/scoring/deterministic_score_evidence.py",
    "grading_agents.py", "bot.py",
)


def check() -> dict:
    checks: dict[str, str] = {}
    changed = subprocess.run(
        ["git", "diff", "--name-only", BASELINE, "--", *PROTECTED,
         "rubrics/topic_packs", "rubrics/generated", "grading/ontology"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.splitlines()
    checks["protected_scoring_and_topic_files"] = "PASS" if not changed else "FAIL"
    from grading.scoring.deterministic_score_engine import calculate_deterministic_score
    from grading.scoring.deterministic_primary_grader import grade_deterministically
    from grading.qualitative.de_shadow import LIMITS, evaluate_qualitative_de
    sample = {"requirements": [{"requirement_id": "f1", "owner_topic_id": "sample",
                                "status": "SATISFIED", "importance": "core"}],
              "findings": [], "fatal_or_core_error": False}
    grade = calculate_deterministic_score(sample, answer_text="1. 원리\n2. 판단")
    breakdown = grade["score_breakdown"]
    checks["abc_de_point_contract"] = "PASS" if (
        set(breakdown) == {"A_structure", "B_requirement_completeness", "C_fact_correctness",
                           "D_engineering_judgment", "E_linkage"}
        and LIMITS == {"D1": 2.0, "D2": 2.0, "D3": 2.0, "E1": 1.0, "E2": 1.0}
        and 0 <= breakdown["A_structure"] <= 3
        and 0 <= breakdown["B_requirement_completeness"] <= 6
        and 0 <= breakdown["C_fact_correctness"] <= 8
    ) else "FAIL"
    question = "열전대와 RTD의 원리, 특성 비교, 정확도 요인과 개선 방안을 설명하시오."
    answer = "열전대는 제벡 효과로 온도차를 잰다."
    base_grade = grade_deterministically(question_text=question, answer_text=answer)
    suggested_grade = grade_deterministically(
        question_text=question, answer_text=answer,
        llm_evidence_fn=lambda _: json.dumps({"judgments": [{
            "requirement_id": "tc_seebeck_temperature_difference",
            "status": "SATISFIED", "quote": answer,
        }]}, ensure_ascii=False),
    )
    checks["llm_cannot_mutate_abc_or_total"] = "PASS" if (
        base_grade["deterministic_score"]["score_breakdown"] ==
        suggested_grade["deterministic_score"]["score_breakdown"]
        and base_grade["requirements"] == suggested_grade["requirements"]
        and base_grade["total_score"] == suggested_grade["total_score"]
    ) else "FAIL"
    shadow = evaluate_qualitative_de(
        "sample question", "sample technical answer", {"score_breakdown": breakdown,
        "requirements": sample["requirements"]}, {"topic_ids": ["sample"]},
    )
    checks["unevaluated_is_not_zero_or_total"] = "PASS" if (
        shadow["status"] == "UNEVALUATED" and shadow["score_effect"] == "none"
        and "proposed_d" not in shadow and "proposed_e" not in shadow
        and "total_score" not in shadow
    ) else "FAIL"
    checks["semantic_validity"] = "REVIEW_REQUIRED"
    checks["expert_benchmark_and_repeatability"] = "REVIEW_REQUIRED"
    decision = "FAIL" if "FAIL" in checks.values() else "REVIEW_REQUIRED"
    return {"decision": decision, "baseline": BASELINE, "checks": checks,
            "protected_changed": changed}


if __name__ == "__main__":
    result = check()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(1 if result["decision"] == "FAIL" else 0)
