#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PROMOTE_GENERATED="${PROMOTE_GENERATED:-1}"
RUN_SMOKE_TOPIC_PACKS="${RUN_SMOKE_TOPIC_PACKS:-0}"

TOPIC_IDS=(
  "pid_controller_tuning_sequence_gain_effects"
  "second_order_system_resonance_frequency_response"
)

TRANSIENT_REPORTS=(
  "reports/fact_anchor_quality_audit.csv"
  "reports/fact_anchor_quality_audit.md"
  "reports/model_fact_relationship_audit.csv"
  "reports/model_fact_relationship_audit.md"
  "reports/model_answer_relationship_validation.csv"
  "reports/model_answer_relationship_validation.md"
  "reports/model_answer_relationship_minor_analysis.csv"
  "reports/model_answer_relationship_minor_analysis.md"
  "reports/model_answer_relationship_priority_minors.md"
  "reports/rubric_audit_summary.md"
)

REPORT_SNAPSHOT_DIR="$(
  mktemp -d \
    "${TMPDIR:-/tmp}/prof_eng_answer_validation_reports.XXXXXX"
)"
REPORT_SNAPSHOT_MANIFEST="${REPORT_SNAPSHOT_DIR}/existing.txt"

snapshot_transient_reports() {
  local report
  local snapshot_path

  : > "${REPORT_SNAPSHOT_MANIFEST}"

  for report in "${TRANSIENT_REPORTS[@]}"; do
    if [[ -f "${report}" ]]; then
      snapshot_path="${REPORT_SNAPSHOT_DIR}/files/${report}"
      mkdir -p "$(dirname "${snapshot_path}")"
      cp -p -- "${report}" "${snapshot_path}"
      printf '%s\n' "${report}" >> "${REPORT_SNAPSHOT_MANIFEST}"
    fi
  done
}

restore_transient_reports() {
  local report
  local snapshot_path

  if [[ -z "${REPORT_SNAPSHOT_DIR:-}" ]] ||
     [[ ! -d "${REPORT_SNAPSHOT_DIR}" ]]; then
    return 0
  fi

  for report in "${TRANSIENT_REPORTS[@]}"; do
    rm -f -- "${report}"
  done

  if [[ -f "${REPORT_SNAPSHOT_MANIFEST}" ]]; then
    while IFS= read -r report; do
      [[ -n "${report}" ]] || continue

      snapshot_path="${REPORT_SNAPSHOT_DIR}/files/${report}"
      mkdir -p "$(dirname "${report}")"
      cp -p -- "${snapshot_path}" "${report}"
    done < "${REPORT_SNAPSHOT_MANIFEST}"
  fi

  rm -rf -- "${REPORT_SNAPSHOT_DIR}"
}

snapshot_transient_reports
trap restore_transient_reports EXIT

echo "===== py_compile: core entrypoints ====="
python3 -m py_compile \
  bot.py \
  grade_output_summarizer.py \
  logic_check_evaluator.py \
  grade_score_reconciler.py \
  grading_agents.py \
  originality_grader.py \
  rubric_registry.py \
  rubric_bank_paths.py \
  scripts/rubric_manager.py \
  scripts/validate_topic_pack_release.py \
  scripts/validate_release_test_coverage.py \
  scripts/validate_model_answer_relationships.py \
  scripts/rubric_audit/report_priority_minor_relationships.py \
  scripts/rubric_audit/audit_fact_anchor_quality.py \
  scripts/rubric_audit/build_rubric_work_pack.py \
  scripts/test_restored_rubric_audit_tools.py \
  scripts/test_rubric_content_crud.py \
  scripts/rubric_audit/deep_model_fact_relationship_audit.py \
  scripts/test_model_answer_relationship_validator.py \
  scripts/test_priority_minor_reporter.py \
  scripts/test_deep_model_fact_relationship_auditor.py \
  scripts/test_release_test_coverage_validator.py \
  scripts/smoke_topic_pack.py

echo
echo "===== release test coverage validation ====="
python3 scripts/validate_release_test_coverage.py

echo
echo "===== release-test coverage validator regression ====="
python3 -m unittest scripts.test_release_test_coverage_validator

echo
echo "===== formatter regression tests ====="
python3 -m unittest scripts.test_grade_output_formatter

echo
echo "===== logic_check evaluator regression tests ====="
python3 -m unittest scripts.test_logic_check_evaluator

echo
echo "===== model-answer relationship validator regression ====="
python3 -m unittest scripts.test_model_answer_relationship_validator

echo
echo "===== priority-minor reporter regression ====="
python3 -m unittest scripts.test_priority_minor_reporter

echo
echo "===== deep Model Answer ↔ Fact Anchor auditor regression ====="
python3 -m unittest scripts.test_deep_model_fact_relationship_auditor

echo "===== restored rubric audit tools regression ====="
python3 -m unittest scripts.test_restored_rubric_audit_tools

echo
echo "===== rubric content CRUD integration regression ====="
python3 scripts/test_rubric_content_crud.py

echo
echo "===== rubric quality audit ====="
python3 scripts/rubric_audit/run_rubric_audit.py

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
restore_transient_reports
trap - EXIT

echo
echo
echo
echo "===== active JSON parser contract regression ====="
PYTHONPATH=. python3 scripts/test_json_parser_contract.py

echo "===== requirement coverage regression ====="
python3 scripts/test_requirement_coverage.py

echo
echo "===== explicit requirement cap regression ====="
python3 scripts/test_explicit_requirement_cap.py

echo
echo "===== originality and final score metadata regression ====="
python3 -m unittest scripts.test_score_metadata_originality_consistency

echo
echo "===== bot logging regression ====="
python3 scripts/test_bot_logging.py

echo
echo "===== score flow guard regression ====="
python3 scripts/test_score_flow_guards.py

echo
echo "===== model answer router regression ====="
python3 scripts/test_model_answer_router.py

echo
echo "===== topic importance scope validation regression ====="
python3 scripts/test_topic_importance_scope_validation.py

echo
echo "===== whitespace check ====="
git diff --check

echo
echo "VALIDATION OK"
