#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="${PROF_ENG_REPO_DIR:-/home/now0930/hermes/workspace/prof_eng_answer}"
COMPOSE_DIR="${PROF_ENG_COMPOSE_DIR:-/home/now0930/hermes}"
SERVICE="${PROF_ENG_COMPOSE_SERVICE:-prof-eng-answer-bot}"
CONTAINER="${PROF_ENG_CONTAINER_NAME:-prof_eng_answer_bot}"
ENV_FILE="$COMPOSE_DIR/.env"

cd "$REPO_DIR"

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERROR: tracked working-tree changes exist; refusing to pull." >&2
  exit 2
fi

git pull --ff-only origin main

# The root Compose project requires /home/now0930/hermes/.env. If it was lost,
# recover only the
# application settings from the currently running container without printing
# their values. The resulting secret file is mode 0600.
if [[ ! -f "$ENV_FILE" ]]; then
  if ! docker inspect "$CONTAINER" >/dev/null 2>&1; then
    echo "ERROR: .env is missing and no existing container can recover it." >&2
    exit 2
  fi
  umask 077
  python3 - "$ENV_FILE" "$CONTAINER" <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

target = Path(sys.argv[1])
container = sys.argv[2]
allowed_exact = {
    "ASSISTED_ROUTING_ENABLED",
    "DIFFICULTY_CEILING_MODE",
    "HYBRID_GENERAL_GRADING_ENABLED",
    "MULTI_TOPIC_GRADING_ENABLED",
    "PROF_ENG_CHAT_ID",
    "QUESTION_DEMAND_SHADOW_ENABLED",
    "RUBRIC_BANK_MODE",
    "SEMANTIC_ROUTER_SHADOW_ENABLED",
    "TECH_BRIEF_MAX_CHECK",
    "TELEGRAM_TOKEN",
    "TELEGRAM_BOT_TOKEN",
}
allowed_prefixes = ("CLOVA_", "GEMINI_", "LLM_", "OLLAMA_")
result = subprocess.run(
    ["docker", "inspect", container, "--format", "{{json .Config.Env}}"],
    check=True,
    capture_output=True,
    text=True,
)
values = {}
for entry in json.loads(result.stdout):
    key, separator, value = entry.partition("=")
    if not separator:
        continue
    if key in allowed_exact or key.startswith(allowed_prefixes):
        if "\n" in value or "\r" in value:
            raise SystemExit(f"cannot recover multiline environment value: {key}")
        values[key] = value
values["DETERMINISTIC_GRADING_PRIMARY"] = "true"
if not (values.get("TELEGRAM_TOKEN") or values.get("TELEGRAM_BOT_TOKEN")):
    raise SystemExit("Telegram token was not found in the existing container")
temporary = target.with_suffix(".tmp")
temporary.write_text(
    "".join(f"{key}={values[key]}\n" for key in sorted(values)),
    encoding="utf-8",
)
os.chmod(temporary, 0o600)
temporary.replace(target)
PY
  echo "Recovered .env from existing container (values not printed)."
else
  cp -p "$ENV_FILE" "$ENV_FILE.backup.$(date -u +%Y%m%dT%H%M%SZ)"
  python3 - "$ENV_FILE" <<'PY'
import os
import sys
from pathlib import Path

target = Path(sys.argv[1])
lines = target.read_text(encoding="utf-8").splitlines()
key = "DETERMINISTIC_GRADING_PRIMARY"
replacement = f"{key}=true"
updated = []
found = False
for line in lines:
    if line.startswith(f"{key}="):
        if not found:
            updated.append(replacement)
            found = True
        continue
    updated.append(line)
if not found:
    updated.append(replacement)
temporary = target.with_suffix(".tmp")
temporary.write_text("\n".join(updated) + "\n", encoding="utf-8")
os.chmod(temporary, 0o600)
temporary.replace(target)
PY
fi

python3 - "$ENV_FILE" <<'PY'
import sys
from pathlib import Path

values = {}
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if not line or line.lstrip().startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    values[key.strip()] = value.strip()
if not (values.get("TELEGRAM_TOKEN") or values.get("TELEGRAM_BOT_TOKEN")):
    raise SystemExit("ERROR: .env has no Telegram token; refusing to recreate")
if values.get("DETERMINISTIC_GRADING_PRIMARY", "").lower() != "true":
    raise SystemExit("ERROR: deterministic-primary flag was not written")
PY

python3 -B "$REPO_DIR/scripts/check_deterministic_authority_gate.py" --require-ready

cd "$COMPOSE_DIR"
docker compose config --quiet
docker compose up -d --force-recreate "$SERVICE"

docker compose exec -T "$SERVICE" python3 -B \
  /workspace/prof_eng_answer/scripts/run_deterministic_primary_smoke.py

docker compose exec -T "$SERVICE" python3 -B - <<'PY'
from grading_authority_policy import enforce_requested_authority_mode

mode = enforce_requested_authority_mode()
assert mode["DETERMINISTIC_GRADING_PRIMARY"] is True
assert mode["LLM_VERDICT_AUTHORITY"] == 0
assert mode["EXTERNAL_LLM_REQUIRED_FOR_VERDICT"] == 0
print("RUNTIME_AUTHORITY=DETERMINISTIC_PRIMARY")
PY

HOST_COMMIT="$(git -C "$REPO_DIR" rev-parse HEAD)"
CONTAINER_STARTED="$(docker inspect "$CONTAINER" --format '{{.State.StartedAt}}')"
CONTAINER_RUNNING="$(docker inspect "$CONTAINER" --format '{{.State.Running}}')"

echo "DEPLOY_COMMIT=$HOST_COMMIT"
echo "CONTAINER_STARTED_AT=$CONTAINER_STARTED"
echo "CONTAINER_RUNNING=$CONTAINER_RUNNING"
echo "RESULT=PASS"
