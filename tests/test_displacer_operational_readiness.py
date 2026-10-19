import json
import shutil

from scripts.check_displacer_operational_readiness import check_contract, check_runtime


def test_seven_verified_facts_match_approved_pack_and_generated_bank():
    result = check_contract()
    assert result["ready"], result["problems"]
    assert result["verified_facts"] == 7


def test_displacer_questions_route_and_select_only_their_required_anchors():
    result = check_runtime()
    assert result["ready"], result["problems"]


def test_changed_fact_statement_blocks_operational_preflight(tmp_path):
    from scripts.check_displacer_operational_readiness import ROOT, TOPIC_ID

    paths = (
        "grading/evidence/approved_fact_registry.json",
        "reports/displacer_anchor_verification_20261019.json",
        f"rubrics/topic_packs/{TOPIC_ID}/topic_status.json",
        f"rubrics/topic_packs/{TOPIC_ID}/fact_anchor.json",
        f"rubrics/topic_packs/{TOPIC_ID}/model_answer.json",
        "rubrics/generated/fact_anchors.generated.json",
        "rubrics/generated/topic_pack_manifest.generated.json",
    )
    for relative in paths:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    shutil.copytree(ROOT / "master_topic_packs", tmp_path / "master_topic_packs")
    path = tmp_path / f"rubrics/topic_packs/{TOPIC_ID}/fact_anchor.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    pack["anchors"][0]["statement"] = "changed after approval"
    path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    result = check_contract(tmp_path)
    assert not result["ready"]
    assert any("text differs" in problem for problem in result["problems"])
