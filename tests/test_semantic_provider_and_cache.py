import io
import json
import os
from pathlib import Path
import urllib.error

import pytest

from grading.evidence.gemini_semantic_provider import (
    GeminiSemanticProvider, SemanticProviderError, docker_urlopen,
)
from grading.evidence.private_semantic_cache import PrivateSemanticCache
from grading.evidence.unresolved_semantic_assist import build_assist_request
from test_fact_candidate_resolver import fact


def request():
    text = "LOPA lowers risk."
    return build_assist_request(
        question="Explain LOPA.", answer=text, facts=[fact()],
        work_item={"requirement_id": "r1", "fact_ids": ["risk_reduction"],
                   "source_span": {"start": 0, "end": len(text)},
                   "reason": "unresolved"},
        versions={key: "v1" for key in ("model", "prompt", "parser", "verifier", "policy")},
    )


class Response:
    def __init__(self, body):
        self.body = io.BytesIO(body)
    def __enter__(self):
        return self.body
    def __exit__(self, *args):
        return False


def test_provider_sends_only_excerpt_and_fact_statement():
    captured = []
    def urlopen(http_request, timeout):
        captured.append((http_request, timeout))
        body = {"candidates": [{"content": {"parts": [{"text": '{"rows":[]}' }]}}]}
        return Response(json.dumps(body).encode())
    provider = GeminiSemanticProvider(model="gemini-fixture", api_key="private-key",
                                      urlopen=urlopen)
    assert provider(request()) == {"rows": []}
    sent = json.loads(captured[0][0].data)["contents"][0]["parts"][0]["text"]
    assert "LOPA lowers risk." in sent
    assert "source_refs" not in sent and "verification_refs" not in sent
    assert "private-key" not in sent


def test_provider_errors_do_not_include_remote_body_or_key():
    def fail(http_request, timeout):
        raise urllib.error.HTTPError("https://example.test", 402, "private-key", {},
                                     io.BytesIO(b"PRIVATE ANSWER"))
    provider = GeminiSemanticProvider(model="gemini-fixture", api_key="private-key", urlopen=fail)
    with pytest.raises(SemanticProviderError, match="http_402") as exc:
        provider(request())
    assert "private-key" not in str(exc.value)
    assert "PRIVATE ANSWER" not in str(exc.value)


def test_docker_transport_keeps_key_in_container(monkeypatch):
    from types import SimpleNamespace
    seen = []
    def run(argv, **kwargs):
        seen.append((argv, kwargs))
        reply = {"ok": True, "response": {"candidates": [{"content": {"parts": [
            {"text": '{"rows":[]}'},
        ]}}]}}
        return SimpleNamespace(returncode=0, stdout=json.dumps(reply))
    monkeypatch.setattr("grading.evidence.gemini_semantic_provider.subprocess.run", run)
    provider = GeminiSemanticProvider(model="gemini-fixture", api_key="bridge-placeholder",
                                      urlopen=docker_urlopen("bot-container"))
    assert provider(request()) == {"rows": []}
    assert "bridge-placeholder" not in str(seen)
    assert seen[0][0][:4] == ["docker", "exec", "-i", "bot-container"]


def test_docker_transport_sanitizes_failure(monkeypatch):
    from types import SimpleNamespace
    def run(argv, **kwargs):
        return SimpleNamespace(returncode=2, stdout=json.dumps({
            "ok": False, "error_type": "http_error", "status": 402,
        }), stderr="private answer")
    monkeypatch.setattr("grading.evidence.gemini_semantic_provider.subprocess.run", run)
    provider = GeminiSemanticProvider(model="gemini-fixture", api_key="bridge-placeholder",
                                      urlopen=docker_urlopen("bot-container"))
    with pytest.raises(SemanticProviderError, match="container_http_error_402") as exc:
        provider(request())
    assert "private answer" not in str(exc.value)


def test_private_cache_persists_replay_and_rejects_public_or_open_permissions(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    private = tmp_path / "private.db"
    with PrivateSemanticCache(private, repository_root=repository) as cache:
        cache["a" * 64] = {"rows": [{"quote": "private answer"}]}
    assert private.stat().st_mode & 0o777 == 0o600
    with PrivateSemanticCache(private, repository_root=repository) as cache:
        assert cache.get("a" * 64)["rows"][0]["quote"] == "private answer"
    with pytest.raises(ValueError):
        PrivateSemanticCache(repository / "public.db", repository_root=repository)
    os.chmod(private, 0o644)
    with pytest.raises(ValueError):
        PrivateSemanticCache(private, repository_root=repository)


def test_cache_rejects_symlink(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    real = tmp_path / "real.db"
    real.touch(mode=0o600)
    link = tmp_path / "link.db"
    link.symlink_to(real)
    with pytest.raises(ValueError):
        PrivateSemanticCache(link, repository_root=repository)


def test_private_cli_reports_only_counts_and_writes_mode_0600(tmp_path, monkeypatch, capsys):
    import importlib.util
    import hashlib
    from grading.evidence.fact_grounded_contracts import fingerprint

    script = Path(__file__).resolve().parents[1] / "scripts/run_semantic_assist_private.py"
    spec = importlib.util.spec_from_file_location("private_semantic_cli", script)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    row = fact()
    question = "Explain risk reduction."
    answer = "LOPA reduces risk."
    contract = {
        "schema_version": row["schema_version"],
        "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint([row]),
        "requirements": [{"requirement_id": "r1", "source_span": {"start": 0, "end": len(question)},
                          "source_text": question, "task": "explain",
                          "fact_refs": [row["fact_id"]], "resolution": "resolved"}],
        "score_effect": "none",
    }
    private_input = tmp_path / "input.json"
    private_input.write_text(json.dumps({"question": question, "answer": answer,
                                         "topic_ids": [row["topic_id"]],
                                         "question_contract": contract}))
    monkeypatch.setattr(cli, "load_approved_fact_registry", lambda root: {"facts": [row]})
    monkeypatch.setattr(cli, "GeminiSemanticProvider", lambda **kw: lambda req: {})
    monkeypatch.setattr(cli, "assist_parser_unresolved", lambda **kw: {
        "queued_count": 0, "reviewer_calls": 0,
        "assistance": {"provider_calls": 0}, "score_effect": "none",
        "final_grade_allowed": False,
    })
    output = tmp_path / "result.json"
    assert cli.main(["--input", str(private_input), "--output", str(output),
                     "--cache", str(tmp_path / "cache.db")]) == 0
    assert output.stat().st_mode & 0o777 == 0o600
    assert json.loads(output.read_text())["question_scope_status"] == "provisional_unreviewed"
    assert "LOPA reduces risk." not in output.read_text() + capsys.readouterr().out
    with pytest.raises(SystemExit, match="2"):
        cli.main(["--input", str(private_input), "--output", str(output),
                  "--cache", str(tmp_path / "cache.db")])
