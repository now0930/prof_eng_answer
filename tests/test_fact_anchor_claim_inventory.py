"""Synthetic offline, fail-closed regressions for the non-scoring Claim/Fact audit."""
import json
from pathlib import Path

import pytest

from scripts.audit_fact_anchor_claim_inventory import audit_inventory


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _fixture(root: Path) -> Path:
    ont = root / "grading_ontology"
    _write(ont / "canonical_predicates.json", {"predicates": [{"id": "defines"}]})
    _write(ont / "engineering_concepts.json", {
        "concepts": [{"id": "pressure"}, {"id": "area"}],
    })
    _write(ont / "quantities.json", {"quantities": [{"id": "force"}]})
    base = root / "rubrics" / "topic_packs"
    _write(base / "topic_one" / "fact_anchor.json", {
        "topic_id": "topic_one",
        "anchors": [
            {"anchor_id": "fact_one", "statement": "압력을 정의한다. 한계를 설명한다."},
            {"anchor_id": "fact_two", "statement": "조건에 따라 다르다."},
        ],
    })
    _write(base / "topic_two" / "fact_anchor.json", {
        "topic_id": "topic_two",
        "anchors": [
            {"anchor_id": "fact_three", "statement": "조건에 따라 다르다."},
        ],
    })
    _write(base / "topic_one" / "logic_check.json", {
        "machine_contract": {
            "owner_topic_id": "topic_one",
            "facts": [
                {
                    "fact_id": "fact_one",
                    "subject": "pressure",
                    "predicate": "defines",
                    "object": "force",
                    "polarity": "positive",
                },
                {
                    "fact_id": "fact_missing",
                    "subject": "unknown_subject",
                    "predicate": "not_defined",
                    "object": "area",
                    "polarity": "positive",
                    "conditions": ["unknown_condition"],
                },
            ],
        },
    })
    return base


def test_inventory_counts_claim_and_duplicate_diagnostics(tmp_path):
    _fixture(tmp_path)
    report = audit_inventory(tmp_path)
    summary = report["summary"]
    assert summary["topic_count"] == 2
    assert summary["anchor_count"] == 3
    assert summary["multi_sentence_candidate_count"] == 1
    assert summary["condition_cue_count"] == 2
    assert summary["machine_contract_fact_count"] == 2
    assert summary["contract_anchor_id_join_count"] == 1
    assert summary["relation_gap_count"] == 4
    assert summary["cross_topic_exact_duplicate_groups"] == 1
    assert report["score_admission"] == "DISABLED"
    assert report["score_effect"] == "none"


def test_audit_is_deterministic_and_never_edits_source(tmp_path):
    _fixture(tmp_path)
    before = {str(path): path.read_bytes() for path in tmp_path.rglob("*.json")}
    first = audit_inventory(tmp_path)
    second = audit_inventory(tmp_path)
    assert first == second
    assert before == {
        str(path): path.read_bytes() for path in tmp_path.rglob("*.json")
    }


def test_duplicate_fact_id_fails_closed(tmp_path):
    base = _fixture(tmp_path)
    path = base / "topic_one" / "fact_anchor.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["anchors"].append(dict(payload["anchors"][0]))
    _write(path, payload)
    with pytest.raises(ValueError, match="duplicate Fact ID"):
        audit_inventory(tmp_path)


def test_machine_contract_is_optional_and_has_no_score_authority(tmp_path):
    base = _fixture(tmp_path)
    (base / "topic_one" / "logic_check.json").unlink()
    result = audit_inventory(tmp_path)
    assert result["summary"]["machine_contract_fact_count"] == 0
    assert result["relation_gaps"] == []
    assert "score" not in result


def test_unknown_predicate_and_unmapped_terms_never_auto_admit(tmp_path):
    _fixture(tmp_path)
    result = audit_inventory(tmp_path)
    reasons = [row["reason"] for row in result["relation_gaps"]]
    assert "PREDICATE_ID_NOT_IN_GLOBAL_ONTOLOGY" in reasons
    assert "SUBJECT_ID_NOT_IN_GLOBAL_ONTOLOGY" in reasons
    assert "CONDITION_ID_NOT_IN_GLOBAL_ONTOLOGY" in reasons
    assert all(
        "SUPPORTED" not in str(row) and "SATISFIED" not in str(row)
        for row in result["relation_gaps"]
    )


def test_mismatched_topic_owner_fails_closed(tmp_path):
    base = _fixture(tmp_path)
    path = base / "topic_two" / "fact_anchor.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["topic_id"] = "topic_one"
    _write(path, payload)
    with pytest.raises(ValueError, match="invalid Topic owner"):
        audit_inventory(tmp_path)


def test_malformed_machine_contract_fails_closed(tmp_path):
    base = _fixture(tmp_path)
    path = base / "topic_one" / "logic_check.json"
    _write(path, {"machine_contract": {"owner_topic_id": "topic_one", "facts": {}}})
    with pytest.raises(ValueError, match="bad machine_contract"):
        audit_inventory(tmp_path)
