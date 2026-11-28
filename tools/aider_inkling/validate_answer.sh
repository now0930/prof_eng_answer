#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/aider_inkling"
REPO="$BASE/repo"
PYTHON="$HOME/hermes/validation/.venv-xdist/bin/python"
INPUT="${1:-$BASE/test_answers/feedback_control.txt}"

if [ ! -s "$INPUT" ]; then
    echo "오류: 답안 파일이 없거나 비어 있습니다."
    exit 1
fi

INPUT=$(realpath "$INPUT")

mkdir -p "$BASE/test_answers/runs"

RUN=$(mktemp -d \
    "$BASE/test_answers/runs/$(date +%Y%m%d_%H%M%S)_XXXXXX")

cd "$REPO"

export DETERMINISTIC_GRADING_PRIMARY=true

echo "========================================"
echo "실제 답안 자동 재채점"
echo "답안: $INPUT"
echo "========================================"

if ! "$PYTHON" -B scripts/regrade_to_telegram.py \
    --input "$INPUT" \
    --chat-id 1 \
    --dry-run \
    --no-source-text \
    2>&1 | tee "$RUN/grade.log"
then
    echo "채점 실행 실패"
    echo "로그: $RUN/grade.log"
    exit 1
fi

"$PYTHON" - "$RUN" <<'PY'
import sys
import json
import re
from pathlib import Path

run = Path(sys.argv[1])
log = (run / "grade.log").read_text(encoding="utf-8")

summary = None

for line in reversed(log.splitlines()):
    try:
        obj = json.loads(line)
        if (
            isinstance(obj, dict)
            and obj.get("marker") == "TELEGRAM_DETERMINISTIC_REGRADE_V1"
        ):
            summary = obj
            break
    except json.JSONDecodeError:
        continue

if summary is None:
    sys.exit("실패: 채점 완료 정보 없음")

score = re.search(
    r"채점 완료:\s*(\d+(?:\.\d+)?)\s*/\s*25",
    log
)

success = (
    summary.get("decision") == "PASS"
    and summary.get("passed") == 1
    and summary.get("failed") == 0
    and summary.get("provider_calls") == 0
    and score is not None
    and 0 <= float(score.group(1)) <= 25
)

summary["score"] = float(score.group(1)) if score else None
summary["validation_passed"] = success

(run / "summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\n========================================")
print("자동 재채점 검증:", "PASS" if success else "FAIL")
print("최종 점수:", summary["score"], "/ 25")
print("외부 API 호출:", summary.get("provider_calls"))
print("결과 저장:", run)
print("========================================")

sys.exit(0 if success else 1)
PY
