import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bot_base_dir_is_configurable_for_host_and_reproducibility_runs(tmp_path):
    env = os.environ.copy()
    env['PROF_ENG_BASE_DIR'] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, '-c', 'import bot; print(bot.BASE_DIR); print(bot.RUBRIC_FILE)'],
        cwd=ROOT, env=env, text=True, capture_output=True, check=True,
    )
    lines = result.stdout.strip().splitlines()
    assert lines == [str(tmp_path), str(tmp_path / 'rubrics/default.json')]
