#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_COMPOSE_DIR="$(cd -- "${REPO_DIR}/../.." && pwd)"
COMPOSE_DIR="${PROF_ENG_COMPOSE_DIR:-${DEFAULT_COMPOSE_DIR}}"
SERVICE="${PROF_ENG_COMPOSE_SERVICE:-prof-eng-answer-bot}"
MODE="${1:-all}"

usage() {
  cat <<'EOF'
사용법:
  run_telegram_regrade.sh all [추가 옵션]
  run_telegram_regrade.sh latest [추가 옵션]
  run_telegram_regrade.sh session <SESSION_ID> [추가 옵션]
  run_telegram_regrade.sh input <CONTAINER_TEXT_PATH> [추가 옵션]

기본 all 옵션:
  --resume --changed-only --delay 5

예:
  bash workspace/prof_eng_answer/scripts/run_telegram_regrade.sh all
  bash workspace/prof_eng_answer/scripts/run_telegram_regrade.sh all --send-summary
  bash workspace/prof_eng_answer/scripts/run_telegram_regrade.sh latest --dry-run
  bash workspace/prof_eng_answer/scripts/run_telegram_regrade.sh session 20260901_125506_5960502198

환경변수:
  PROF_ENG_COMPOSE_DIR      docker-compose.yml이 있는 경로
  PROF_ENG_COMPOSE_SERVICE Compose 서비스명(기본 prof-eng-answer-bot)
EOF
}

if [[ "${MODE}" == "-h" || "${MODE}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ ! -f "${COMPOSE_DIR}/docker-compose.yml" && ! -f "${COMPOSE_DIR}/compose.yml" && ! -f "${COMPOSE_DIR}/docker-compose.yaml" && ! -f "${COMPOSE_DIR}/compose.yaml" ]]; then
  echo "ERROR: Compose 파일을 찾을 수 없습니다: ${COMPOSE_DIR}" >&2
  echo "PROF_ENG_COMPOSE_DIR을 지정하세요." >&2
  exit 2
fi

shift || true
case "${MODE}" in
  all)
    SOURCE_ARGS=(--all --resume --changed-only --delay 5)
    ;;
  latest)
    SOURCE_ARGS=(--latest)
    ;;
  session)
    [[ $# -ge 1 ]] || { echo "ERROR: SESSION_ID가 필요합니다." >&2; usage; exit 2; }
    SOURCE_ARGS=(--session-id "$1")
    shift
    ;;
  input)
    [[ $# -ge 1 ]] || { echo "ERROR: 컨테이너 내부 텍스트 경로가 필요합니다." >&2; usage; exit 2; }
    SOURCE_ARGS=(--input "$1")
    shift
    ;;
  *)
    echo "ERROR: 지원하지 않는 모드입니다: ${MODE}" >&2
    usage
    exit 2
    ;;
esac

cd "${COMPOSE_DIR}"

if ! docker compose ps --status running --services | grep -Fxq "${SERVICE}"; then
  echo "ERROR: Compose 서비스가 실행 중이 아닙니다: ${SERVICE}" >&2
  echo "먼저 docker compose up -d ${SERVICE} 를 실행하세요." >&2
  exit 3
fi

echo "COMPOSE_DIR=${COMPOSE_DIR}"
echo "SERVICE=${SERVICE}"
echo "MODE=${MODE}"

exec docker compose exec -T \
  -e DETERMINISTIC_GRADING_PRIMARY=true \
  "${SERVICE}" \
  python3 -B /workspace/prof_eng_answer/scripts/regrade_to_telegram.py \
  "${SOURCE_ARGS[@]}" "$@"
