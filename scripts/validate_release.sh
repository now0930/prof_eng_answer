#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PROMOTE_GENERATED="${PROMOTE_GENERATED:-1}"
RUN_SMOKE_TOPIC_PACKS="${RUN_SMOKE_TOPIC_PACKS:-0}"

TOPIC_IDS=(
  "pid_controller_tuning_sequence_gain_effects"
  "second_order_system_resonance_frequency_response"
)

echo "===== py_compile: core entrypoints ====="
python3 -m py_compile \
  bot.py \
  grade_output_summarizer.py \
  logic_check_evaluator.py \
  grade_score_reconciler.py \
  rubric_registry.py \
  rubric_bank_paths.py \
  scripts/rubric_manager.py \
  scripts/validate_topic_pack_release.py \
  scripts/smoke_topic_pack.py

echo
echo "===== formatter regression tests ====="
python3 -m unittest scripts.test_grade_output_formatter

echo
echo "===== logic_check evaluator regression tests ====="
python3 -m unittest scripts.test_logic_check_evaluator

echo
echo "===== rubric validation: validate-all ====="
python3 scripts/rubric_manager.py validate-all

echo
if [[ "${PROMOTE_GENERATED}" == "1" ]]; then
  echo "===== topic pack release validation: promote generated ====="
  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --promote-generated \
    --skip-smoke
else
  echo "===== topic pack release validation: no promote ====="
  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --skip-smoke
fi

echo
echo "===== optional smoke topic packs ====="
mkdir -p data/sessions

if [[ "${RUN_SMOKE_TOPIC_PACKS}" != "1" ]]; then
  echo "SKIP: smoke-topic-pack is opt-in. Set RUN_SMOKE_TOPIC_PACKS=1 to run it locally."
elif find data/sessions -mindepth 1 -maxdepth 1 -type d | grep -q .; then
  for topic_id in "${TOPIC_IDS[@]}"; do
    echo
    echo "----- smoke-topic-pack: ${topic_id} -----"
    python3 scripts/rubric_manager.py smoke-topic-pack \
      --topic-id "${topic_id}" \
      --require-logic-check
  done
else
  echo "SKIP: smoke-topic-pack requires at least one usable base session under data/sessions."
  echo "      Run smoke locally after creating a grading session, or pass --base-session manually."
fi

echo
echo "===== cleanup transient validation reports ====="
rm -f reports/model_answer_relationship_validation.csv
rm -f reports/model_answer_relationship_validation.md

echo
echo
echo "===== model answer router regression ====="
python3 scripts/test_model_answer_router.py

echo "===== whitespace check ====="
git diff --check

echo
echo "VALIDATION OK"
