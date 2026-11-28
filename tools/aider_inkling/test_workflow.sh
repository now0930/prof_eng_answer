set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
base=$(mktemp -d)
app="$base/aider_inkling"
platform=${1:-$(cd "$(dirname "$0")" && pwd)}
trap 'rm -rf -- "$base"' EXIT
mkdir -p "$app/repo/grading" "$app/repo/tests" "$app/test_answers" "$base/bin"
cp "$platform/"{develop.py,develop.sh,planner.py,compiler.py,executor.py,validator.py,run_context.py,ai_backends.py,edit_contract.py,gemini_backend.py,plan_schema.py} "$app/"
cd "$app"
python3 -m py_compile *.py
printf 'def score():\n    return 1\n' > repo/grading/sample.py
printf 'def test_sample():\n    assert True\n' > repo/tests/test_sample.py
git -C repo init -q
git -C repo add grading tests
git -C repo -c user.name=Test -c user.email=test@example.invalid commit -qm baseline
export HOME="$base/home"
mkdir -p "$HOME/hermes/validation/.venv-xdist/bin"
cat > "$HOME/hermes/validation/.venv-xdist/bin/python" <<'SH'
#!/usr/bin/env bash
test "$*" = '-m pytest -n 6 --dist loadfile -q'
SH
chmod +x "$HOME/hermes/validation/.venv-xdist/bin/python"
printf 'fixture\n' > test_answers/feedback_control.txt
printf 'echo "채점 완료: 1.0 / 25"\n' > validate_answer.sh
cat > "$base/fake_planner.py" <<'PY'
import json, sys
from pathlib import Path
assert "smoke objective" in sys.stdin.read()
assert Path("grading/sample.py").is_file()
assert not Path("tests/test_sample.py").exists()
json.dump({"schema_version": "inkling_plan_v6", "tasks": [{
    "id": 1, "files": ["grading/sample.py"], "target_symbols": ["score"],
    "instruction": "fixture edit", "acceptance": ["return updated value"],
    "test_files": ["tests/test_sample.py"],
    "edits": [{"search": "    return 1\n", "replace": "    return 2\n"}]
}]}, sys.stdout)
PY
cat > "$base/bin/docker" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
if test "$1" = ps; then exit 0; fi
test "$1 $2" = "compose run"
[[ " $* " == *" --model ollama_chat/inkling-2-mini-aider "* ]]
[[ " $* " == *" --file grading/sample.py "* ]]
sed -i 's/return 1/return 2/' repo/grading/sample.py
if [[ "${EXTRA_CHANGE:-0}" == 1 ]]; then printf '# side effect\n' >> repo/tests/test_sample.py; fi
SH
chmod +x "$base/bin/docker"
export PATH="$base/bin:$PATH"
export V6_PLANNER_COMMAND=$(python3 -c 'import json,sys; print(json.dumps(["python3",sys.argv[1]]))' "$base/fake_planner.py")
export V6_EXTERNAL_PLAN_CONTEXT='["grading/sample.py"]'
V6_OLLAMA_PLAN_MODEL=check python3 develop.py 'smoke objective' --compile-only > rejected.log 2>&1 && exit 1
grep -q 'requires an external provider' rejected.log
python3 develop.py 'smoke objective' --compile-only > compiled.log
grep -q 'V6 exact-edit preflight PASS' compiled.log
test -z "$(git -C repo status --porcelain)"
plan_dir=$(sed -n 's/^로그 위치: //p' compiled.log)
cp "$plan_dir/plan.json" plan.json
cat > "$base/gemini_smoke.py" <<'PY'
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

import develop

plan = json.loads(Path(os.environ["SMOKE_PLAN"]).read_text())
def open_gemini(request, timeout):
    assert request.full_url == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.8-flash:generateContent"
    )
    assert request.get_header("X-goog-api-key") == "fixture-only"
    assert timeout == 120
    body = json.loads(request.data)
    assert body["generationConfig"]["responseMimeType"] == "application/json"
    assert body["generationConfig"]["responseJsonSchema"]["type"] == "object"
    prompt = body["contents"][0]["parts"][0]["text"]
    assert "grading/sample.py" in prompt
    assert "reset private answer" not in prompt
    assert "fixture-only" not in prompt
    assert "def test_sample" not in prompt
    return io.BytesIO(json.dumps({"candidates": [{
        "finishReason": "STOP",
        "content": {"parts": [{"text": json.dumps(plan)}]},
    }]}).encode())

os.environ.pop("V6_PLANNER_COMMAND", None)
os.environ["V6_PLAN_PROVIDER"] = "gemini"
os.environ["GEMINI_API_KEY"] = "fixture-only"
with patch("gemini_backend.HTTP.open", side_effect=open_gemini) as request:
    develop.main(["smoke objective", "--compile-only"])
    request.assert_called_once()
PY
printf 'reset private answer\n' > test_answers/feedback_control.txt
SMOKE_PLAN="$app/plan.json" PYTHONPATH="$app" python3 "$base/gemini_smoke.py" > gemini.log
grep -q 'V6 exact-edit preflight PASS' gemini.log
python3 develop.py --plan --compile-only > replay.log
grep -q 'V6 exact-edit preflight PASS' replay.log
V6_OLLAMA_EDIT_MODEL=check python3 develop.py --plan plan.json > alternate.log 2>&1 && exit 1
grep -q 'uses Aider + Inkling' alternate.log
cat > "$base/execute.py" <<'PY'
import sys
from unittest.mock import patch
import develop
with patch("ai_backends.EditBackend.preflight"):
    develop.main(sys.argv[1:])
PY
printf 'y\n' | PYTHONPATH="$app" python3 "$base/execute.py" --plan plan.json > passed.log
grep -q '전체 계획 실행 및 pytest 검증 통과' passed.log
test "$(git -C repo diff --name-only)" = grading/sample.py
git -C repo restore -- grading/sample.py
printf 'y\n' | EXTRA_CHANGE=1 PYTHONPATH="$app" python3 "$base/execute.py" --plan plan.json > unexpected.log 2>&1 && exit 1
grep -q '지정 범위 외 파일 변경' unexpected.log
printf 'Refactored V6 smoke passed\n'
