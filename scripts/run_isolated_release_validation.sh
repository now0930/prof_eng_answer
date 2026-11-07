#!/usr/bin/env bash
# Reproducible, isolated validation; never mutates/restarts the live bot.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
command -v docker >/dev/null
command -v git >/dev/null
test -z "$(git -C "$ROOT" status --porcelain)" || {
  echo "HOLD: validate only a clean, committed candidate checkout" >&2
  exit 2
}
COMMIT="$(git -C "$ROOT" rev-parse HEAD)"
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/prof-eng-release-validation.XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT
# Local clone transfers tracked source only: never copy ignored personal sessions,
# WordPress OCR, .env, chat IDs, or production databases into the validator.
git clone --quiet --no-hardlinks --no-checkout "$ROOT" "$SCRATCH/checkout"
git -C "$SCRATCH/checkout" checkout --quiet --detach "$COMMIT"

# Pin pytest and runtime major/minor; record the resulting image ID with report.
IMAGE="prof-eng-answer-validator:py311-pytest842"
docker build --quiet -t "$IMAGE" -f - "$SCRATCH" <<'DOCKERFILE'
FROM python:3.11-bookworm
RUN python3 -m pip install --no-cache-dir 'pytest==8.4.2'
DOCKERFILE
echo "VALIDATOR_COMMIT=$COMMIT"
echo "VALIDATOR_IMAGE_ID=$(docker image inspect "$IMAGE" --format '{{.Id}}')"
docker run --rm --network none \
  --mount "type=bind,source=$SCRATCH/checkout,target=/workspace/prof_eng_answer" \
  --workdir /workspace/prof_eng_answer \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e PROMOTE_GENERATED=0 \
  -e RUN_SMOKE_TOPIC_PACKS=0 \
  -e RUN_GRADING_REPRODUCIBILITY=0 \
  "$IMAGE" bash -euc '
    git config --global --add safe.directory /workspace/prof_eng_answer
    python3 -B -m pytest -q tests/test_expert_accuracy_production_gate.py tests/test_release_candidate.py
    python3 -B scripts/rubric_manager.py validate-all
    PROMOTE_GENERATED=0 scripts/validate_release.sh
    echo "ISOLATED_VALIDATION=PASS"
  '
