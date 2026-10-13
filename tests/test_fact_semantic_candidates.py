import copy

import pytest

from grading.evidence.fact_grounded_contracts import FactGroundedContractError
from grading.evidence.fact_semantic_candidates import build_request, parse_candidates


def response():
    return {"candidates": [{"source_text": "X is Y.", "proposal": {
        "subject": "x", "predicate": "is", "object": "y", "conditions": [],
        "polarity": "positive", "assertion_context": "asserted",
    }}]}


def parse(value, answer="X is Y."):
    return parse_candidates(value, question="Explain X.", answer=answer,
                            kind="answer_claim", model="fixture")


def test_question_request_cannot_leak_answer():
    request = build_request("Explain X.", "PRIVATE_ANSWER", [], kind="question_requirement")
    assert "PRIVATE_ANSWER" not in str(request)


def test_candidate_is_exact_span_and_not_verified():
    row = parse(response())[0]
    assert row["source_span"] == {"start": 0, "end": 7}
    assert row["score_effect"] == "none"
    assert row["producer"]["mode"] == "semantic_resolver"
    assert "independently_verified" not in row


@pytest.mark.parametrize("text", ["invented", "", "X is Y. X is Y."])
def test_absent_empty_or_repeated_source_rejected(text):
    with pytest.raises(FactGroundedContractError):
        parse(response(), answer=text)


def test_grading_authority_rejected():
    value = response()
    value["candidates"][0]["proposal"]["score"] = 25
    with pytest.raises(FactGroundedContractError):
        parse(value)


def test_duplicate_rejected():
    value = response()
    value["candidates"].append(copy.deepcopy(value["candidates"][0]))
    with pytest.raises(FactGroundedContractError):
        parse(value)


def test_polarity_preserved():
    value = response()
    value["candidates"][0]["proposal"]["polarity"] = "negative"
    assert parse(value)[0]["proposal"]["polarity"] == "negative"


@pytest.mark.parametrize("task", ["explain", "compare", "apply", "설명"])
def test_question_tasks_preserve_original_response(task):
    value = {"candidates": [{"source_text": "Explain X.", "proposal": {
        "task": task, "target_concepts": ["x"], "conditions": []}}]}
    original = copy.deepcopy(value)
    parsed = parse_candidates(value, question="Explain X.", answer="",
                              kind="question_requirement", model="fixture")
    assert parsed[0]["proposal"]["task"] == ("explain" if task == "설명" else task)
    assert value == original


def test_cli_failure_is_private_and_not_success(tmp_path, monkeypatch, capsys):
    import importlib.util
    import json
    import os
    from pathlib import Path
    from types import SimpleNamespace

    path = Path(__file__).resolve().parents[1] / "scripts/extract_fact_shadow_candidates.py"
    spec = importlib.util.spec_from_file_location("candidate_cli", path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"question": "Explain X.", "answer": "X is Y.",
                                  "topic_ids": ["fixture"]}))
    output = tmp_path / "private.json"
    monkeypatch.setattr(cli, "load_approved_fact_registry", lambda root: {
        "facts": [{"topic_id": "fixture", "fact_id": "x"}]})
    monkeypatch.setattr(cli, "build_request", lambda *a, **kw: {"kind": kw["kind"]})
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **kw: SimpleNamespace(
        stdout="", stderr="SECRET_SHOULD_NOT_LEAK", returncode=1))
    monkeypatch.setattr(cli.sys, "argv", [str(path), "--input", str(source), "--output", str(output)])
    old_umask = os.umask(0o077)
    try:
        assert cli.main() == 1
    finally:
        os.umask(old_umask)
    report = json.loads(output.read_text())
    assert report["ok"] is False
    assert report["stage6_complete"] is False
    assert report["independently_verified"] is False
    assert report["candidates"] == []
    assert output.stat().st_mode & 0o777 == 0o600
    assert "SECRET_SHOULD_NOT_LEAK" not in output.read_text() + capsys.readouterr().out
