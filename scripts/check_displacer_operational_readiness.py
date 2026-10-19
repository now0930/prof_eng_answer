"""Read-only preflight for the seven verified displacer Facts and grading Pack."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements
from grading.routing.deterministic_topic_router import route_question_topics


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "displacer_level_buoyancy_torque_tube_density_interface_calibration"


def check_contract(root: Path = ROOT) -> dict[str, object]:
    root = root.resolve()
    registry = load_approved_fact_registry(root)
    reviews = json.loads(
        (root / "reports/displacer_anchor_verification_20261019.json").read_text(encoding="utf-8")
    )
    pack_dir = root / "rubrics/topic_packs" / TOPIC_ID
    status = json.loads((pack_dir / "topic_status.json").read_text(encoding="utf-8"))
    source = json.loads((pack_dir / "fact_anchor.json").read_text(encoding="utf-8"))
    generated = json.loads(
        (root / "rubrics/generated/fact_anchors.generated.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (root / "rubrics/generated/topic_pack_manifest.generated.json").read_text(encoding="utf-8")
    )
    model = json.loads((pack_dir / "model_answer.json").read_text(encoding="utf-8"))
    facts = [row for row in registry["facts"] if row["topic_id"] == TOPIC_ID]
    expected = {row["anchor_id"]: row["fact_id"] for row in reviews["reviews"]}
    by_anchor = {row["legacy_anchor_id"]: row for row in facts}
    source_anchors = {row["anchor_id"]: row for row in source["anchors"]}
    generated_topics = [row for row in generated["topics"] if row["topic_id"] == TOPIC_ID]
    generated_anchors = (
        {row["anchor_id"]: row for row in generated_topics[0]["anchors"]}
        if len(generated_topics) == 1 else {}
    )
    listed = any(row["topic_id"] == TOPIC_ID for row in manifest["topics"])
    problems = []
    if status.get("status") != "approved" or status.get("review_method") != "human":
        problems.append("Topic Pack is not human-approved")
    if reviews.get("status") != "verified" or len(expected) != 7:
        problems.append("seven-Fact verification report is incomplete")
    if set(by_anchor) != set(expected) or set(source_anchors) != set(expected):
        problems.append("Fact-to-Anchor mapping is incomplete or ambiguous")
    if not listed or set(generated_anchors) != set(expected):
        problems.append("generated grading bank is missing the seven Anchors")
    for anchor_id, fact_id in expected.items():
        fact = by_anchor.get(anchor_id, {})
        statement = source_anchors.get(anchor_id, {}).get("statement")
        if (fact.get("fact_id") != fact_id
                or fact.get("statement") != statement
                or generated_anchors.get(anchor_id, {}).get("statement") != statement):
            problems.append(f"Fact, Pack, or generated text differs: {anchor_id}")
        if (fact.get("review_status") != "approved"
                or fact.get("verification_status") != "verified"
                or fact.get("score_effect") != "none"
                or not fact.get("verification_refs")):
            problems.append(f"Fact verification is incomplete: {anchor_id}")
    covered = set().union(*(
        set(row["required_anchor_ids"])
        for row in model["expected_question_patterns"]
    ))
    if covered != set(expected):
        problems.append("question contracts do not cover exactly the seven Anchors")
    return {
        "ready": not problems,
        "topic_id": TOPIC_ID,
        "verified_facts": len(facts),
        "question_patterns": len(model["expected_question_patterns"]),
        "problems": problems,
    }


def check_runtime() -> dict[str, object]:
    """Exercise actual question routing and scoped Anchor selection, without scoring."""
    model = json.loads(
        (ROOT / "rubrics/topic_packs" / TOPIC_ID / "model_answer.json").read_text(encoding="utf-8")
    )
    problems = []
    for row in model["expected_question_patterns"]:
        question = row["pattern"]
        route = route_question_topics(question)
        if route["status"] != "ROUTED" or route["primary_topic_id"] != TOPIC_ID:
            problems.append(f"question routed to another Topic: {question}")
            continue
        evaluated = evaluate_fact_anchor_requirements(
            answer_text="", question_text=question, topic_ids=[TOPIC_ID]
        )
        selected = {item["requirement_id"] for item in evaluated["requirements"]}
        if selected != set(row["required_anchor_ids"]):
            problems.append(f"question selected wrong Anchors: {question}")
    return {"ready": not problems, "problems": problems}


def main() -> int:
    contract = check_contract()
    runtime = check_runtime() if contract["ready"] else {"ready": False, "problems": []}
    print(json.dumps({"contract": contract, "runtime": runtime}, ensure_ascii=False, indent=2))
    return 0 if contract["ready"] and runtime["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
