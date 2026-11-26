from scripts.check_private_paths import is_private_path

import pytest


@pytest.mark.parametrize("path", [
    ".env", "nested/.env.local", "data/sessions/attempt.json",
    "data/training_history.sqlite3-wal", "data/private/result.json",
    "reports/private/replay.json", "private/manifest.json",
    "archive/PRODUCTION.DB", "reports/release_candidates/run/manifest.json",
    "data/state.json", "wordpress_docs/source.txt", "logs/bot.log",
])
def test_private_path_is_rejected(path):
    assert is_private_path(path)


@pytest.mark.parametrize("path", [
    ".env.example", "data/question_contract_cache/synthetic.json",
    "rubrics/topic_packs/example/fact_anchor.json",
    "reports/public_synthetic_summary.json", "docs/operation_runbook.md",
    "scripts/check_private_paths.py",
])
def test_public_path_is_allowed(path):
    assert not is_private_path(path)
