#!/usr/bin/env bash

set -u
set -o pipefail

readonly OVERALL_STAGE="SOFTWARE_TOPIC_PACK_PARALLEL_EXPANSION"
readonly LANE="SOFTWARE_LLM_LANE_A"
readonly LANE_BRANCH="software/lane-a-control-lifecycle"
readonly REMOTE="origin"
readonly REPO_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_a"
readonly SCRIPT_DIR="${REPO_DIR}/gemini_script"
readonly CURRENT_TOPIC="SW-04 instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
readonly TOPIC_ID="instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
readonly TOPIC_DIR="rubrics/topic_packs/${TOPIC_ID}"
readonly SHEET_REL="docs/topic_sheets/${TOPIC_ID}.md"
readonly TEST_REL="scripts/test_instrumentation_control_software_lifecycle_v_model.py"
readonly SCRIPT_NAME="20260806_sw04_lane_a_author_validate_commit.sh"
readonly SCRIPT_REL="gemini_script/${SCRIPT_NAME}"
readonly COMMIT_SUBJECT="feat(topic-pack): add SW-04 software lifecycle topic"
readonly SW03_COMMIT_SUBJECT="feat(topic-pack): add SW-03 HMI alarm topic"

CURRENT_STAGE="LANE_A_READ_ONLY_WORKTREE_CHECK"
NEXT_STAGE="SW04_COMMIT_STATUS_DETECTION"
LANE_PROGRESS="2/4"
failure_count=0
warning_count=0
created_count=0
final_rc=1
AUTHORING_REQUIRED=true
REUSE_EXISTING_PAYLOAD=false
SW04_ALREADY_COMMITTED=false

payload_tmp=""
changed_before_file=""
changed_after_file=""
allowed_after_file=""
baseline_helper_file=""
staged_file=""
commit_files_file=""
python_cache_dir=""

TOPIC_PATHS=(
    'docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/README.md'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/fact_anchor.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/logic_check.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/topic_importance.json'
    'scripts/test_instrumentation_control_software_lifecycle_v_model.py'
)

COMMIT_PATHS=(
    'docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/README.md'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/fact_anchor.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/logic_check.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/topic_importance.json'
    'scripts/test_instrumentation_control_software_lifecycle_v_model.py'
    'gemini_script/20260806_sw04_lane_a_author_validate_commit.sh'
)

SW03_REQUIRED_PATHS=(
    'docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/README.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json'
    'scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py'
    'gemini_script/20260806_sw03_lane_a_author_validate_commit.sh'
)

JSON_PATHS=(
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/fact_anchor.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/logic_check.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json'
    'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/topic_importance.json'
)

declare -A EXPECTED_SHA256=(
    ['docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md']='822d9ce259442e3d3353228ddc5f454d12359185b3e05b76fd3b195a95699926'
    ['rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/README.md']='1e1648cc9185cae8aac30ee686acdb2bbe6921a4a422e2dc5ad34c0f6775e38e'
    ['rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/fact_anchor.json']='304a31cab09ffbaecbfe37f163fc38bb32b0b6beba9dd3be73a974d5e626d2da'
    ['rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/logic_check.json']='c0c51c19c5409f53413d70d86971ca131762e56790bfcbd243e75e508bac2a5b'
    ['rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json']='c90d3b63f6d9eadc1fd16e927475c8e4e8f289a97ad0a9d7b0552c9fe403dbdc'
    ['rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/topic_importance.json']='378f2bc52f33b32233bc86a262f9ee8dc05c06a01b50366c4a07c27a1d086242'
    ['scripts/test_instrumentation_control_software_lifecycle_v_model.py']='e1b83c15ee9d86800985a087902362039d171fb71a8d020bd44c254e5e0bf5b9'
)

section() {
    printf '\n===== %s =====\n' "$1"
    printf '%s\n' \
        "OVERALL_STAGE=${OVERALL_STAGE}" \
        "LANE=${LANE}" \
        "LANE_BRANCH=${LANE_BRANCH}" \
        "CURRENT_TOPIC=${CURRENT_TOPIC}" \
        "CURRENT_STAGE=${CURRENT_STAGE}" \
        "NEXT_STAGE=${NEXT_STAGE}" \
        "LANE_PROGRESS=${LANE_PROGRESS}"
}

result_header() {
    printf '\n--- RESULT: %s ---\n' "$1"
    printf '%s\n' \
        "OVERALL_STAGE=${OVERALL_STAGE}" \
        "LANE=${LANE}" \
        "LANE_BRANCH=${LANE_BRANCH}" \
        "CURRENT_TOPIC=${CURRENT_TOPIC}" \
        "CURRENT_STAGE=${CURRENT_STAGE}" \
        "NEXT_STAGE=${NEXT_STAGE}" \
        "LANE_PROGRESS=${LANE_PROGRESS}"
}

pass() {
    printf 'PASS: %s\n' "$1"
}

warn() {
    warning_count=$((warning_count + 1))
    printf 'WARN: %s\n' "$1"
}

fail() {
    failure_count=$((failure_count + 1))
    printf 'FAIL: %s\n' "$1"
}

run_step() {
    local step_name="$1"
    shift
    printf '\n--- %s ---\n' "$step_name"
    "$@"
    local rc=$?
    printf 'STEP_RC=%s|%s\n' "$step_name" "$rc"
    if [ "$rc" -ne 0 ]; then
        fail "$step_name"
    fi
    return 0
}

validate_json_quiet() {
    python3 -m json.tool "$1" >/dev/null
}

collect_changed_paths() {
    {
        git diff --name-only 2>/dev/null || true
        git diff --cached --name-only 2>/dev/null || true
        git ls-files --others --exclude-standard 2>/dev/null || true
    } | awk 'NF > 0 { print }' | LC_ALL=C sort -u
}

contains_path() {
    local needle="$1"
    shift
    local item
    for item in "$@"; do
        [ "$item" = "$needle" ] && return 0
    done
    return 1
}

snapshot_helper() {
    local rel="$1"
    local status mode sha index_line
    status="$(git status --porcelain=v1 -- "$rel" | sed -n '1p')"
    mode="$(stat -c '%a' -- "$rel" 2>/dev/null || printf MISSING)"
    sha="$(sha256sum -- "$rel" 2>/dev/null | awk '{print $1}' || printf MISSING)"
    index_line="$(git ls-files -s -- "$rel" 2>/dev/null | sed -n '1p')"
    printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$status" "$mode" "$sha" "$index_line"
}

verify_helper_manifest() {
    local manifest="$1"
    local rel old_status old_mode old_sha old_index
    local current
    while IFS=$'\t' read -r rel old_status old_mode old_sha old_index; do
        [ -n "$rel" ] || continue
        current="$(snapshot_helper "$rel")"
        if [ "$current" != "${rel}"$'\t'"${old_status}"$'\t'"${old_mode}"$'\t'"${old_sha}"$'\t'"${old_index}" ]; then
            printf 'BASELINE_HELPER_CHANGED=%s\n' "$rel"
            return 1
        fi
    done < "$manifest"
    return 0
}

cleanup() {
    [ -z "${payload_tmp:-}" ] || rm -rf -- "$payload_tmp"
    [ -z "${changed_before_file:-}" ] || rm -f -- "$changed_before_file"
    [ -z "${changed_after_file:-}" ] || rm -f -- "$changed_after_file"
    [ -z "${allowed_after_file:-}" ] || rm -f -- "$allowed_after_file"
    [ -z "${baseline_helper_file:-}" ] || rm -f -- "$baseline_helper_file"
    [ -z "${staged_file:-}" ] || rm -f -- "$staged_file"
    [ -z "${commit_files_file:-}" ] || rm -f -- "$commit_files_file"
    [ -z "${python_cache_dir:-}" ] || rm -rf -- "$python_cache_dir"
}
trap cleanup EXIT

CURRENT_STAGE="LANE_A_READ_ONLY_WORKTREE_CHECK"
NEXT_STAGE="SW03_COMMIT_PREREQUISITE_CHECK"
section "0. verify exact Lane A linked worktree before mutation"

script_abs="$(realpath -e -- "${BASH_SOURCE[0]}" 2>/dev/null || true)"
script_dir="$(dirname -- "$script_abs" 2>/dev/null || true)"
derived_repo="$(realpath -e -- "${script_dir}/.." 2>/dev/null || true)"
invocation_pwd="$(pwd -P 2>/dev/null || true)"

printf '%s\n' \
    "REPO_DIR=${REPO_DIR}" \
    "EXPECTED_BRANCH=${LANE_BRANCH}" \
    "REMOTE=${REMOTE}" \
    "INVOCATION_ABSOLUTE_PATH=${invocation_pwd}" \
    "SCRIPT_ABSOLUTE_PATH=${script_abs}" \
    "SCRIPT_DERIVED_REPO_DIR=${derived_repo}" \
    "MAIN_FALLBACK_ALLOWED=false" \
    "GENERATED_REBUILD=false" \
    "FULL_VALIDATE_ALL=false" \
    "EXTERNAL_LLM_VALIDATION=false" \
    "TOPIC_LOCAL_COMMIT=true" \
    "TOPIC_LOCAL_PUSH=false"

[ "$script_dir" = "$SCRIPT_DIR" ] || fail "SCRIPT_LOCATION_MISMATCH"
[ "$derived_repo" = "$REPO_DIR" ] || fail "SCRIPT_DERIVED_REPO_MISMATCH"
[ -d "$REPO_DIR" ] || fail "LANE_A_REPO_DIR_NOT_FOUND"
[ -f "$REPO_DIR/.git" ] || fail "LINKED_WORKTREE_GIT_FILE_MISSING"

if [ "$failure_count" -eq 0 ]; then
    cd "$REPO_DIR" || fail "CANNOT_ENTER_LANE_A_REPO"
fi

if [ "$failure_count" -eq 0 ]; then
    git_toplevel="$(git rev-parse --show-toplevel 2>/dev/null || true)"
    git_inside="$(git rev-parse --is-inside-work-tree 2>/dev/null || true)"
    git_branch="$(git branch --show-current 2>/dev/null || true)"
    git_dir="$(git rev-parse --path-format=absolute --git-dir 2>/dev/null || true)"
    git_common_dir="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"

    printf '%s\n' \
        "GIT_TOPLEVEL=${git_toplevel}" \
        "GIT_INSIDE_WORKTREE=${git_inside}" \
        "GIT_BRANCH=${git_branch}" \
        "GIT_DIR=${git_dir}" \
        "GIT_COMMON_DIR=${git_common_dir}"

    [ "$git_toplevel" = "$REPO_DIR" ] || fail "GIT_TOPLEVEL_MISMATCH"
    [ "$git_inside" = "true" ] || fail "NOT_INSIDE_GIT_WORKTREE"
    [ "$git_branch" = "$LANE_BRANCH" ] || fail "LANE_BRANCH_MISMATCH"
    [ -n "$git_dir" ] && [ -n "$git_common_dir" ] && [ "$git_dir" != "$git_common_dir" ] ||
        fail "NOT_A_LINKED_WORKTREE"

    if ! git worktree list --porcelain |
        awk -v expected_worktree="$REPO_DIR" \
            -v expected_branch="refs/heads/$LANE_BRANCH" '
            $1 == "worktree" {
                current_worktree = substr($0, index($0, " ") + 1)
                next
            }
            $1 == "branch" {
                if (current_worktree == expected_worktree && $2 == expected_branch) {
                    found = 1
                }
                next
            }
            END { exit(found ? 0 : 1) }
        '
    then
        fail "WORKTREE_LIST_CONTRACT_MISMATCH"
    fi

    git remote get-url "$REMOTE" >/dev/null 2>&1 ||
        fail "REMOTE_NOT_CONFIGURED"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "LANE_A_READ_ONLY_CONTRACT_REJECTED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Correct Lane A worktree or branch and rerun"
    final_rc=1
    exit 1
fi

changed_before_file="$(mktemp)"
changed_after_file="$(mktemp)"
allowed_after_file="$(mktemp)"
baseline_helper_file="$(mktemp)"
staged_file="$(mktemp)"
commit_files_file="$(mktemp)"
python_cache_dir="$(mktemp -d)"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$python_cache_dir"

CURRENT_STAGE="SW03_COMMIT_PREREQUISITE_CHECK"
NEXT_STAGE="SW04_COMMIT_STATUS_DETECTION"
section "1. verify SW-03 committed prerequisite and preserve helper baseline"

sw03_head_count=0
for rel in "${SW03_REQUIRED_PATHS[@]}"; do
    if git cat-file -e "HEAD:${rel}" 2>/dev/null; then
        sw03_head_count=$((sw03_head_count + 1))
    fi
done
printf 'SW03_HEAD_PATH_COUNT=%s/%s\n' "$sw03_head_count" "${#SW03_REQUIRED_PATHS[@]}"

if [ "$sw03_head_count" -ne "${#SW03_REQUIRED_PATHS[@]}" ]; then
    fail "SW03_COMMITTED_PREREQUISITE_INCOMPLETE"
fi

if [ "$failure_count" -eq 0 ]; then
    mapfile -t sw03_commits < <(
        for rel in "${SW03_REQUIRED_PATHS[@]}"; do
            git log -1 --format='%H' -- "$rel"
        done | LC_ALL=C sort -u
    )
    printf 'SW03_UNIQUE_COMMIT_COUNT=%s\n' "${#sw03_commits[@]}"
    [ "${#sw03_commits[@]}" -eq 1 ] || fail "SW03_PATHS_NOT_IN_ONE_TOPIC_COMMIT"
fi

if [ "$failure_count" -eq 0 ]; then
    sw03_commit="${sw03_commits[0]}"
    sw03_subject="$(git show -s --format='%s' "$sw03_commit")"
    printf '%s\n' \
        "SW03_COMMIT_HASH=${sw03_commit}" \
        "SW03_COMMIT_SUBJECT=${sw03_subject}"
    [ "$sw03_subject" = "$SW03_COMMIT_SUBJECT" ] ||
        fail "SW03_COMMIT_SUBJECT_MISMATCH"

    for rel in "${SW03_REQUIRED_PATHS[@]}"; do
        git diff --quiet -- "$rel" || fail "SW03_UNSTAGED_CHANGE:${rel}"
        git diff --cached --quiet -- "$rel" || fail "SW03_STAGED_CHANGE:${rel}"
    done
fi

if [ -n "$(git diff --cached --name-only)" ]; then
    printf 'PREEXISTING_STAGED_PATHS_BEGIN\n'
    git diff --cached --name-only
    printf 'PREEXISTING_STAGED_PATHS_END\n'
    fail "GIT_INDEX_NOT_CLEAN_BEFORE_SW04"
fi

collect_changed_paths > "$changed_before_file"
printf 'CURRENT_CHANGED_PATHS_BEGIN\n'
cat "$changed_before_file"
printf 'CURRENT_CHANGED_PATHS_END\n'

while IFS= read -r rel; do
    [ -n "$rel" ] || continue
    if [ "$rel" = "$SCRIPT_REL" ]; then
        continue
    fi
    if contains_path "$rel" "${TOPIC_PATHS[@]}"; then
        continue
    fi
    case "$rel" in
        gemini_script/*.sh)
            snapshot_helper "$rel" >> "$baseline_helper_file"
            if git ls-files --error-unmatch -- "$rel" >/dev/null 2>&1; then
                printf 'PRESERVED_TRACKED_BASELINE_HELPER=%s\n' "$rel"
            else
                printf 'PRESERVED_UNTRACKED_BASELINE_HELPER=%s\n' "$rel"
            fi
            ;;
        *)
            fail "UNRELATED_LANE_A_CHANGE:${rel}"
            ;;
    esac
done < "$changed_before_file"

if [ "$failure_count" -eq 0 ]; then
    pass "SW-03 Topic commit is complete and clean"
    pass "pre-existing Lane A helper scripts captured as immutable baseline"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW04_PREREQUISITE_OR_BASELINE_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Repair only the reported Lane A prerequisite or dirty path"
    final_rc=1
    exit 1
fi

CURRENT_STAGE="SW04_COMMIT_STATUS_DETECTION"
NEXT_STAGE="SW04_AUTHOR_OR_SKIP"
section "2. detect whether SW-04 is already committed"

sw04_head_count=0
for rel in "${COMMIT_PATHS[@]}"; do
    if git cat-file -e "HEAD:${rel}" 2>/dev/null; then
        sw04_head_count=$((sw04_head_count + 1))
    fi
done
printf 'SW04_HEAD_PATH_COUNT=%s/%s\n' "$sw04_head_count" "${#COMMIT_PATHS[@]}"

if [ "$sw04_head_count" -eq "${#COMMIT_PATHS[@]}" ]; then
    mapfile -t sw04_commits < <(
        for rel in "${COMMIT_PATHS[@]}"; do
            git log -1 --format='%H' -- "$rel"
        done | LC_ALL=C sort -u
    )
    if [ "${#sw04_commits[@]}" -ne 1 ]; then
        fail "SW04_PATHS_NOT_IN_ONE_TOPIC_COMMIT"
    else
        sw04_commit="${sw04_commits[0]}"
        sw04_subject="$(git show -s --format='%s' "$sw04_commit")"
        printf '%s\n' \
            "SW04_COMMIT_HASH=${sw04_commit}" \
            "SW04_COMMIT_SUBJECT=${sw04_subject}"
        [ "$sw04_subject" = "$COMMIT_SUBJECT" ] ||
            fail "SW04_COMMIT_SUBJECT_MISMATCH"
    fi

    for rel in "${COMMIT_PATHS[@]}"; do
        git diff --quiet -- "$rel" || fail "SW04_UNSTAGED_CHANGE:${rel}"
        git diff --cached --quiet -- "$rel" || fail "SW04_STAGED_CHANGE:${rel}"
    done

    if [ "$failure_count" -eq 0 ]; then
        SW04_ALREADY_COMMITTED=true
        AUTHORING_REQUIRED=false
    fi
elif [ "$sw04_head_count" -ne 0 ]; then
    fail "SW04_PARTIALLY_PRESENT_IN_HEAD"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW04_COMMIT_STATUS_DETECTION_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false"
    final_rc=1
    exit 1
fi

if [ "$SW04_ALREADY_COMMITTED" = "true" ]; then
    CURRENT_STAGE="SW04_TOPIC_LOCAL_COMPLETE"
    NEXT_STAGE="SW10_AUTHORING_PACKAGE"
    LANE_PROGRESS="3/4"
    result_header "SW04_ALREADY_COMMITTED_SKIP_CONFIRMED"
    printf '%s\n' \
        "SW_NUMBER=SW-04" \
        "TOPIC_ID=${TOPIC_ID}" \
        "COMMIT_HASH=${sw04_commit}" \
        "COMMIT_SUBJECT=${sw04_subject}" \
        "VALIDATION_RESULT=COMMITTED_PATHS_AND_CLEAN_STATE_PASS" \
        "NEXT_TOPIC=SW-10 control_software_project_engineering_documents_fat_sat_commissioning_acceptance" \
        "LANE_PROGRESS=3/4" \
        "PUSH_EXECUTED=false"
    final_rc=0
    exit 0
fi

worktree_topic_count=0
for rel in "${TOPIC_PATHS[@]}"; do
    [ -f "$rel" ] && worktree_topic_count=$((worktree_topic_count + 1))
done
printf 'SW04_WORKTREE_TOPIC_PATH_COUNT=%s/%s\n' "$worktree_topic_count" "${#TOPIC_PATHS[@]}"

if [ "$worktree_topic_count" -eq 0 ]; then
    AUTHORING_REQUIRED=true
elif [ "$worktree_topic_count" -eq "${#TOPIC_PATHS[@]}" ]; then
    AUTHORING_REQUIRED=false
    REUSE_EXISTING_PAYLOAD=true
    pass "complete uncommitted SW-04 payload found; exact hashes will be verified"
else
    fail "SW04_PARTIAL_WORKTREE_PAYLOAD"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW04_WORKTREE_PAYLOAD_STATUS_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false"
    final_rc=1
    exit 1
fi

write_payload() {
    local rel="$1"
    local expected="$2"
    local temp_path="${payload_tmp}/${rel}"
    mkdir -p -- "$(dirname -- "$temp_path")"
    base64 -d > "$temp_path"
    local rc=$?
    printf 'DECODE_RC=%s|%s\n' "$rel" "$rc"
    if [ "$rc" -ne 0 ]; then
        fail "PAYLOAD_DECODE_FAILED:${rel}"
        return 0
    fi
    local actual
    actual="$(sha256sum "$temp_path" | awk '{print $1}')"
    printf 'TEMP_PAYLOAD_SHA256=%s|%s\n' "$rel" "$actual"
    if [ "$actual" != "$expected" ]; then
        fail "TEMP_PAYLOAD_HASH_MISMATCH:${rel}"
    fi
}

CURRENT_STAGE="SW04_SOURCE_AUTHORING"
NEXT_STAGE="SW04_TOPIC_LOCAL_VALIDATION"
section "3. create or reuse complete SW-04 Topic Authoring Package"

if [ "$AUTHORING_REQUIRED" = "true" ] && [ "$failure_count" -eq 0 ]; then
    payload_tmp="$(mktemp -d)"

    write_payload 'docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md' '822d9ce259442e3d3353228ddc5f454d12359185b3e05b76fd3b195a95699926' <<'PAYLOAD_SW04_01'
IyBTVy0wNCBUb3BpYyBTaGVldAoKIyMgMS4gVG9waWMg7Iud67OECgotIFRvcGljIElEOiBgaW5z
dHJ1bWVudGF0aW9uX2NvbnRyb2xfc29mdHdhcmVfbGlmZWN5Y2xlX3ZfbW9kZWxfdHJhY2VhYmls
aXR5X3ZlcmlmaWNhdGlvbl92YWxpZGF0aW9uYAotIO2VnOq4gCDso7zsoJw6IOqzhOy4oeygnOyW
tCDshoztlITtirjsm6jslrQg7IiY66qF7KO86riwLCBWLU1vZGVsLCDstpTsoIHshLEsIOqygOym
nSDrsI8g7ZmV7J24Ci0gTGFuZSBvd25lcnNoaXA6IFNPRlRXQVJFX0xMTV9MQU5FX0EKLSBRdWVz
dGlvbiB0eXBlOiBQUk9DRURVUkUKLSBEaWZmaWN1bHR5OiBERVNJR05fRVZBTFVBVElPTgotIFNl
bGVjdGlvbiBpbXBvcnRhbmNlOiBDT1JFX01VU1RfUFJFUEFSRQoKIyMgMi4g7Y+s7ZWoIOuylOyc
hAoKU1ctMDTripQg7J2867CYIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrTsnZgg6rCc67Cc
IOyImOuqheyjvOq4sOyZgCBWJlYg7LK06rOE66W8IOyGjOycoO2VnOuLpC4g7JqU6rWs7IKs7ZWt
7JeQ7IScIOyLnOyeke2VmOyXrCDslYTtgqTthY3sspgsIOyDgeyEuOyEpOqzhCwg6rWs7ZiELCDr
i6jsnITCt+2Gte2VqcK37Iuc7Iqk7YWc7Iuc7ZeYLCDstpTsoIHshLEsIOqysO2VqMK367OA6rK9
6rSA66as7JmAIOyKueyduCDspp3soIHsnLzroZwg7Jew6rKw7ZWc64ukLgoKIyMjIO2PrO2VqAoK
LSBSZXF1aXJlbWVudCBzcGVjaWZpY2F0aW9uCi0gU3lzdGVtIGFyY2hpdGVjdHVyZeyZgCBTb2Z0
d2FyZSBhcmNoaXRlY3R1cmUKLSBEZXRhaWxlZCBkZXNpZ27smYAgQ29kaW5nIHN0YW5kYXJkCi0g
VW5pdCwgSW50ZWdyYXRpb24sIFN5c3RlbSB0ZXN0Ci0gVmVyaWZpY2F0aW9u7JmAIFZhbGlkYXRp
b24KLSBSZXF1aXJlbWVudCBUcmFjZWFiaWxpdHkgTWF0cml4Ci0gU3RhdGljIGFuYWx5c2lz7JmA
IER5bmFtaWMgYW5hbHlzaXMKLSBSZWdyZXNzaW9uIHRlc3QKLSBTaW11bGF0aW9uLCBISUzsmYAg
RmF1bHQgaW5qZWN0aW9uCi0gRGVmZWN0IG1hbmFnZW1lbnQKLSBSZXZpZXcsIEFwcHJvdmFs7JmA
IFYmViBldmlkZW5jZQoKIyMjIOygnOyZuAoKLSBTSUwg7IKw7KCVLCBQRkRhdmfCt1BGSCwgU2Fm
ZXR5IEludGVncml0eSwgU2FmZXR5IGluZGVwZW5kZW5jZeyZgCDssrTqs4TsoIEg6rOg7J6lIO2G
teygnOuKlCBTVy0wNQotIEZBVMK3U0FUwrdMb29wIHRlc3TCt+yLnOyatOyghMK37ISx64ql7Iuc
7ZeYwrdBY2NlcHRhbmNlwrdIYW5kb3ZlcuuKlCBTVy0xMAotIEhNScK3U0NBREEgQWxhcm3Ct1NP
ReyZgCDsmrTsoITsnpAg6raM7ZWc7J2AIFNXLTAzCi0gU2VxdWVuY2XCt0ludGVybG9ja8K3VHJp
cCDsg4Htg5zsoITsnbTsmYAgRmFpbC1zYWZlIOyatOyghOuFvOumrOuKlCBTVy0wMgoKIyMgMy4g
Vi1Nb2RlbCDtlbXsi6wKClYtTW9kZWzsnYAg66y47ISc66W8IOyInOyEnOuMgOuhnCDrp4zrk5zr
ipQg6re466a87J20IOyVhOuLiOuLpC4g7KKM7Lih7JeQ7IScIOygleydmO2VnCDsmpTqtazsgqzt
la3qs7wg7ISk6rOE6rKw7KCV7J2EIOyasOy4oeydmCDsi5ztl5jqs7wg7ZmV7J247Zmc64+Z7Jy8
66GcIOqygOymne2VmOuPhOuhnSDrjIDsnZHsi5ztgqjri6QuIOyLnO2XmOydgCDsvZTrlKkg7KKF
66OMIO2bhCDsspjsnYwg7KSA67mE7ZWY64qUIOqyg+ydtCDslYTri4jrnbwg7JqU6rWs7IKs7ZWt
6rO8IOyEpOqzhOqwgCDsoJXtlbTsp4DripQg7Iuc7KCQ67aA7YSwIOuqqeyggSwg7ZmY6rK9LCDs
noXroKUsIOyYiOyDgeqysOqzvOyZgCDtjJDsoJXquLDspIDsnYQg7KSA67mE7ZWc64ukLgoKYGBg
dGV4dArsgqzsmqnrqqnsoIHCt+yCrOyaqeyekCDsmpTqtawgICDihpQgVmFsaWRhdGlvbiAvIFN5
c3RlbSB0ZXN0ClN5c3RlbSByZXF1aXJlbWVudCAgICAg4oaUIFN5c3RlbSB2ZXJpZmljYXRpb24K
U3lzdGVtwrdTVyBhcmNoaXRlY3R1cmUg4oaUIEludGVncmF0aW9uIHRlc3QKRGV0YWlsZWQgZGVz
aWduICAgICAgICDihpQgVW5pdCB0ZXN0CkltcGxlbWVudGF0aW9uICAgICAgICAg4oaUIFN0YXRp
Y8K3ZHluYW1pYyBhbmFseXNpcwpgYGAKCiMjIDQuIFJlcXVpcmVtZW50cyBTcGVjaWZpY2F0aW9u
CgrsmpTqtazsgqztla3snYAg7Iud67OEIOqwgOuKpe2VmOqzoCDrqoXtmZXtlZjrqbAg7J286rSA
65CY6rOgIOyLnO2XmCDqsIDriqXtlbTslbwg7ZWc64ukLiDquLDriqXqs7wg7ISx64ql67+QIOyV
hOuLiOudvCDsnbjthLDtjpjsnbTsiqQsIOyatOyghOuqqOuTnCwg7LSI6riw7ZmULCDsoJXsp4DC
t+yerOyLnOyekSwg7JiI7Jm47LKY66asLCDthrXsi6DsnqXslaAsIOuNsOydtO2EsCDtkojsp4gs
IHRpbWluZ+qzvCDsnpDsm5DsoJzslb3snYQg7Y+s7ZWo7ZWc64ukLgoK7KKL7J2AIOyalOq1rOyC
rO2VreydgCDri6TsnYwg7JqU7IaM66W8IOqwgOynhOuLpC4KCi0g6rOg7JygIOyLneuzhOyekAot
IOyhsOqxtOqzvCB0cmlnZ2VyCi0g7J6F66Cl6rO8IOy2nOugpQotIOygleyDgcK367mE7KCV7IOB
IOuwmOydkQotIOy4oeyglSDri6jsnITsmYAg7ZeI7Jqp7Jik7LCoCi0g7KCB7JqpIOyatOyghOuq
qOuTnAotIOqygOymneuwqeuyleqzvCBhY2NlcHRhbmNlIGNyaXRlcmlhCgojIyA1LiBBcmNoaXRl
Y3R1cmXsmYAgRGV0YWlsZWQgRGVzaWduCgpTeXN0ZW0gYXJjaGl0ZWN0dXJl64qUIEhXwrdTV8K3
7Ya17IugwrfsmbjrtoDsi5zsiqTthZzsnZgg6riw64ql67Cw67aELCDsnbjthLDtjpjsnbTsiqQs
IOuNsOydtO2EsO2dkOumhOqzvCDqs6DsnqXqsr3qs4Trpbwg7KCV7J2Y7ZWc64ukLiBTb2Z0d2Fy
ZSBhcmNoaXRlY3R1cmXripQg66qo65OILCB0YXNrLCDsg4Htg5wsIOuNsOydtO2EsCDshozsnKDq
towsIO2GteyLoCwg7KeE64uo6rO8IOyekOybkOuwsOu2hOydhCDsoJXsnZjtlZzri6QuIERldGFp
bGVkIGRlc2lnbuydgCDslYzqs6DrpqzsppgsIOyDge2DnOyghOydtCwgSS9PIOyymOumrCwg7JiI
7Jm47JmAIOqyveqzhOyhsOqxtOydhCDqtaztmIQg6rCA64ql7ZWcIOyImOykgOycvOuhnCDqtazs
srTtmZTtlZzri6QuCgrslYTtgqTthY3sspgg6rKA7Yag7JeQ7ISc64qUIOuLqOyInCDruJTroZ0g
7IiY67O064ukIOyduO2EsO2OmOydtOyKpCDrtojsnbzsuZgsIHRpbWluZywgcmFjZSBjb25kaXRp
b24sIGNvbW1vbiByZXNvdXJjZSwgZmF1bHQgcHJvcGFnYXRpb27qs7wgcmVjb3ZlcnkgcGF0aOul
vCDtmZXsnbjtlZzri6QuCgojIyA2LiBDb2RpbmcgU3RhbmRhcmTsmYAgQ29uZmlndXJhdGlvbiBC
YXNlbGluZQoKQ29kaW5nIHN0YW5kYXJk64qUIOuqheuqheqzvCDshJzsi53rv5Ag7JWE64uI6528
IOyekOujjO2YlSwg7LSI6riw7ZmULCDrspTsnIQsIOq4iOyngOq1rOusuCwg67O17J6h64+ELCDs
mIjsmbjsspjrpqwsIGRlZmVuc2l2ZSBjb2RpbmcsIGNvbW1lbnTsmYAgcmV2aWV3IOq4sOykgOyd
hCDtj6ztlajtlZzri6QuIFJlcXVpcmVtZW50LCBkZXNpZ24sIHNvdXJjZSwgbGlicmFyeSwgY29t
cGlsZXIsIHRlc3QgdG9vbOyZgCDtmZjqsr3snYAg7Iud67OE65CcIGJhc2VsaW5l7Jy866GcIOq0
gOumrO2VtOyVvCDrj5nsnbwg7Iuc7ZeY7J2EIOyerO2YhO2VoCDsiJgg7J6I64ukLgoKIyMgNy4g
7Iuc7ZeYIOyImOykgAoKIyMjIFVuaXQgdGVzdAoK7ZWo7IiYLCDrqqjrk4gsIEZCIOuTsSDstZzs
howg7ISk6rOE64uo7JyE7J2YIOygleyDgcK36rK96rOEwrfsmKTrpZgg6rK966Gc66W8IOqyqeum
rO2VtCDtmZXsnbjtlZzri6QuIHN0dWIsIGRyaXZlcuyZgCBoYXJuZXNz66GcIOyZuOu2gCDsnZjs
obTshLHsnYQg7Ya17KCc7ZWgIOyImCDsnojri6QuCgojIyMgSW50ZWdyYXRpb24gdGVzdAoK66qo
65OIwrd0YXNrwrfthrXsi6DCt0RCwrfsnqXsuZggaW50ZXJmYWNlIOyCrOydtOydmCDrjbDsnbTt
hLDtmJUsIOyInOyEnCwgdGltaW5nLCB0aW1lb3V0LCByZXRyeeyZgCDsmKTrpZjsoITtjIzrpbwg
7ZmV7J247ZWc64ukLgoKIyMjIFN5c3RlbSB0ZXN0CgrthrXtlanrkJwg7Iuc7Iqk7YWc7J20IGVu
ZC10by1lbmQg7JqU6rWs7IKs7ZWtLCDsmrTsoITrqqjrk5wsIOyEseuKpSwg7J6l7JWg67O16rWs
7JmAIOyZuOu2gOyLnOyKpO2FnCDsl7Dqs4Trpbwg7Lap7KGx7ZWY64qU7KeAIO2ZleyduO2VnOuL
pC4KCiMjIDguIFZlcmlmaWNhdGlvbuyZgCBWYWxpZGF0aW9uCgpWZXJpZmljYXRpb27snYAg7IKw
7Lac66y87J20IO2VtOuLuSDri6jqs4TsnZgg66qF7IS47JmAIOyEpOqzhOq4sOykgOyXkCDrp57r
ipTsp4Drpbwg7ZmV7J247ZWc64ukLiBWYWxpZGF0aW9u7J2AIOyLpOygnCDrmJDripQg64yA7ZGc
IOyatOyghO2ZmOqyveyXkOyEnCDsi5zsiqTthZzsnbQg7J2Y64+E65CcIOyCrOyaqeuqqeyggeqz
vCDsgqzsmqnsnpAg7JqU6rWs66W8IOy2qeyhse2VmOuKlOyngOulvCDtmZXsnbjtlZzri6QuIO2V
nOyqveydmCDshLHqs7XsnYAg64uk66W4IOyqveydhCDsnpDrj5kg67O07J6l7ZWY7KeAIOyViuuK
lOuLpC4KCmBgYHRleHQKVmVyaWZpY2F0aW9uOiBBcmUgd2UgYnVpbGRpbmcgdGhlIHByb2R1Y3Qg
cmlnaHQ/ClZhbGlkYXRpb246ICAgQXJlIHdlIGJ1aWxkaW5nIHRoZSByaWdodCBwcm9kdWN0Pwpg
YGAKCiMjIDkuIFJlcXVpcmVtZW50IFRyYWNlYWJpbGl0eSBNYXRyaXgKClJUTeydgCDri6jsiJwg
7JqU6rWs7IKs7ZWtLeyLnO2XmCDrsojtmLjtkZzqsIAg7JWE64uI64ukLiBSZXF1aXJlbWVudOyX
kOyEnCBhcmNoaXRlY3R1cmUsIGRlc2lnbiwgY29kZSwgdGVzdCBjYXNl7JmAIHJlc3VsdOuhnCDs
nbTrj5ntlZjripQg7Iic67Cp7ZalIOy2lOyggeqzvCwgdGVzdCByZXN1bHTsl5DshJwgcmVxdWly
ZW1lbnTroZwg64+M7JWE6rCA64qUIOyXreuwqe2WpSDstpTsoIHsnYQg7KCc6rO17ZWc64ukLgoK
7JaR67Cp7ZalIOy2lOyggeycvOuhnCDri6TsnYzsnYQg7LC+64qU64ukLgoKLSDsi5ztl5jrkJjs
p4Ag7JWK7J2AIOyalOq1rOyCrO2VrQotIOyalOq1rOyCrO2VrSDqt7zqsbDqsIAg7JeG64qUIOyE
pOqzhMK37L2U65OcCi0g7JqU6rWs7IKs7ZWtIOq3vOqxsOqwgCDsl4bripQg7Iuc7ZeYCi0g67OA
6rK9IO2bhCDqsLHsi6DrkJjsp4Ag7JWK7J2AIOyLnO2XmOqzvCDqsrDqs7wKLSDsi6TtjKgg65iQ
64qUIOuvuOyLpO2WiSDsg4Htg5zsnZgg7JqU6rWs7IKs7ZWtCgojIyAxMC4gU3RhdGljwrdEeW5h
bWljwrdSZWdyZXNzaW9uCgpTdGF0aWMgYW5hbHlzaXPripQg7ZSE66Gc6re4656o7J2EIOyLpO2W
ie2VmOyngCDslYrqs6Ag6rec7LmZLCBjb250cm9sIGZsb3csIGRhdGEgZmxvdywgY29tcGxleGl0
eSwg66+47LSI6riw7ZmU7JmAIHVucmVhY2hhYmxlIGNvZGXrpbwg67aE7ISd7ZWc64ukLiBEeW5h
bWljIGFuYWx5c2lz64qUIOyLpOygnCDsi6Ttlokg7KSRIHBhdGgsIHRpbWluZywgbWVtb3J5wrdy
ZXNvdXJjZSwgaW50ZXJmYWNl7JmAIOydkeuLteydhCDqtIDssLDtlZzri6QuIFJlZ3Jlc3Npb24g
dGVzdOuKlCDrs4Dqsr3smIHtlqUg67aE7ISd7J2EIOuwlO2DleycvOuhnCDsg4gg6riw64ql6rO8
IOq4sOyhtCDquLDriqXsnZgg67mE7Ye07ZaJ7J2EIO2ZleyduO2VnOuLpC4KCiMjIDExLiBTaW11
bGF0aW9uwrdISUzCt0ZhdWx0IEluamVjdGlvbgoKU2ltdWxhdGlvbuydgCBwbGFudCDrmJDripQg
ZGV2aWNlIG1vZGVs66GcIOygleyDgcK367mE7KCV7IOBIOyLnOuCmOumrOyYpOulvCDrsJjrs7Xt
lZjsp4Drp4wgbW9kZWwgZmlkZWxpdHnsmYAg6rCA7KCV7J2EIOq0gOumrO2VtOyVvCDtlZzri6Qu
IEhJTOydgCDsi6TsoJwg7KCc7Ja0IEhXIOuYkOuKlCDsi6TtlontmZjqsr3snYQgcmVhbC10aW1l
IHBsYW50IG1vZGVs6rO8IGNsb3NlZCBsb29w66GcIOyXsOqysO2VmOyXrCBJL08sIHRpbWluZywg
bmV0d29ya+yZgCBjb250cm9sIGFjdGlvbuydhCDsi5ztl5jtlZzri6QuCgpGYXVsdCBpbmplY3Rp
b27snYAgc2Vuc29yIG9wZW4sIHN0dWNrIHZhbHVlLCByYW5nZSBlcnJvciwgY29tbXVuaWNhdGlv
biBkZWxhecK3bG9zcywgY29ycnVwdGVkIGRhdGEsIHBvd2VyIHJlY292ZXJ57JmAIHRhc2sgb3Zl
cnJ1biDrk7HsnYQg7Ya17KCc65CcIO2ZmOqyveyXkOyEnCDso7zsnoXtlZzri6QuIOuqqeyggeyd
gCDri6jsiJwg7Iuk7YyoIOycoOuwnOydtCDslYTri4jrnbwgZGV0ZWN0aW9uLCBpc29sYXRpb24s
IGZhbGxiYWNrLCBhbGFybSwgcmVjb3ZlcnnsmYAgZXZpZGVuY2Xrpbwg7ZmV7J247ZWY64qUIOqy
g+ydtOuLpC4KCiMjIDEyLiBEZWZlY3TCt0NoYW5nZcK3UmVncmVzc2lvbiDtj5Dro6jtlIQKCuyL
pO2MqOyLnO2XmOydgCDsgq3soJztlZjsp4Ag7JWK64qU64ukLiBEZWZlY3QgcmVjb3Jk7JeQ64qU
IOyerO2YhOyhsOqxtCwg7JiB7ZalLCBzZXZlcml0eSwg7JuQ7J24LCDsiJjsoJXrsoTsoIQsIOye
rOyLnO2XmOqzvCBjbG9zdXJlIGV2aWRlbmNl66W8IOuCqOq4tOuLpC4gUmVxdWlyZW1lbnTCt2Rl
c2lnbsK3Y29kZcK3ZW52aXJvbm1lbnQg67OA6rK97J2AIGltcGFjdCBhbmFseXNpcywgYXBwcm92
YWwsIGJhc2VsaW5lwrdSVE0g6rCx7Iug6rO8IHJlZ3Jlc3Npb27snYQg6rGw7Lmc64ukLgoKYGBg
dGV4dApEZWZlY3Qg67Cc6rKsCuKGkiDsm5DsnbjrtoTshJ0K4oaSIOuzgOqyveyalOyyreqzvCDs
mIHtlqXrtoTshJ0K4oaSIOyKueyduArihpIg7IiY7KCV6rO8IGJhc2VsaW5lIOqwseyLoArihpIg
6rSA66CoIOyLnO2XmMK37ZqM6reA7Iuc7ZeYCuKGkiBSVE0g67CPIOymneyggSDqsLHsi6AK4oaS
IGNsb3N1cmUKYGBgCgojIyAxMy4gUmV2aWV37JmAIEFwcHJvdmFsCgpSZXZpZXfripQg7Jet7ZWg
LCDsnoXroKXsnpDro4wsIOq4sOykgCwg7KeA7KCB7IKs7ZWt6rO8IOyhsOy5mO2ZleyduOydhCDq
sJbripTri6QuIEFwcHJvdmFs7J2AIOyKueyduOq2jOyekOqwgCBleGl0IGNyaXRlcmlh7JmAIHJl
c2lkdWFsIGRlZmVjdOulvCDtmZXsnbjtlZwg65KkIOyCsOy2nOusvCBiYXNlbGluZeydhCDsirns
nbjtlZjripQg7ZaJ7JyE7J2064ukLiDsnpHshLHsnpDsnZggc2VsZi1jaGVja+unjOycvOuhnCDq
s7Xsi50gcmV2aWV37JmAIGFwcHJvdmFs7J2EIOuMgOyytO2VmOyngCDslYrripTri6QuCgojIyAx
NC4g64yA7ZGcIEZhdGFsIOyYpOuLtQoKMS4gKirsmKTri7U6KiogVmVyaWZpY2F0aW9u6rO8IFZh
bGlkYXRpb27snYAg7JmE7KCE7Z6IIOqwmeydgCDtmZzrj5nsnbTri6QuCiAgIC0gKirsoJXsoJU6
KiogVmVyaWZpY2F0aW9u7J2AIOuLqOqzhCDsgrDstpzrrLzsnZgg66qF7IS4IOygge2VqeyEseyd
hCwgVmFsaWRhdGlvbuydgCDsnZjrj4TrkJwg7IKs7Jqp66qp7KCB6rO8IOyCrOyaqeyekCDsmpTq
tawg7Lap7KGx7J2EIO2ZleyduO2VmOupsCDsg4HtmLjrs7TsmYTsoIHsnbTri6QuCgoyLiAqKuyY
pOuLtToqKiBWYWxpZGF0aW9u7J2AIOy9lOuUqSDtkZzspIAg7KSA7IiYIOyXrOu2gOunjCDtmZXs
nbjtlZjripQg7Zmc64+Z7J2064ukLgogICAtICoq7KCV7KCVOioqIOy9lOuUqSDtkZzspIAg7KSA
7IiY64qUIFZlcmlmaWNhdGlvbuydmCDsnbzrtoDqsIAg65CgIOyImCDsnojsnLzrgpggVmFsaWRh
dGlvbuydgCDthrXtlakg7Iuc7Iqk7YWc7J2YIOyCrOyaqeuqqeyggeqzvCDsgqzsmqnsnpAg7JqU
6rWsIOy2qeyhseydhCDtmZXsnbjtlZzri6QuCgozLiAqKuyYpOuLtToqKiBWLU1vZGVs7JeQ7ISc
64qUIOuqqOuToCDsvZTrlKnsnbQg64Gd64KcIOuSpOyXkCDsi5ztl5jsnYQg7LKY7J2MIOqzhO2a
je2VnOuLpC4KICAgLSAqKuygleyglToqKiBWLU1vZGVs7J2AIOqwnOuwnCDstIjquLDrtoDthLAg
6rCBIOyalOq1rOyCrO2VrcK37ISk6rOEIOuLqOqzhOyXkCDrjIDsnZHtlZjripQg7Iuc7ZeY6rO8
IOyImOyaqeq4sOykgOydhCDtlajqu5gg7KSA67mE7ZWc64ukLgoKNC4gKirsmKTri7U6Kiog7JqU
6rWs7IKs7ZWt7JeQ7IScIOyLnO2XmCDrsojtmLjroZwg7ZWcIOuyiCDsl7DqsrDtlZjrqbQg7JaR
67Cp7ZalIFJUTeydtCDsmYTshLHrkJzri6QuCiAgIC0gKirsoJXsoJU6KiogUlRN7J2AIOyalOq1
rOyCrO2VreyXkOyEnCDshKTqs4TCt+y9lOuTnMK37Iuc7ZeYwrfqsrDqs7zroZzsnZgg7Iic67Cp
7Zal6rO8IOyLnO2XmMK36rKw6rO87JeQ7IScIOyalOq1rOyCrO2VreycvOuhnOydmCDsl63rsKnt
lqUg7LaU7KCB7J2EIOuqqOuRkCDsoJzqs7XtlbTslbwg7ZWc64ukLgoKNS4gKirsmKTri7U6Kiog
66qo65OgIOuLqOychOyLnO2XmOydtCDthrXqs7ztlZjrqbQg7Ya17ZWp7Iuc7ZeY6rO8IOyLnOyK
pO2FnOyLnO2XmOydgCDtlYTsmpQg7JeG64ukLgogICAtICoq7KCV7KCVOioqIOuLqOychOyLnO2X
mOydgCDstZzshowg7ISk6rOE64uo7JyE66W8IOqygOymne2VmOupsCDrqqjrk4gg7IOB7Zi47J6R
7Jqp6rO8IGVuZC10by1lbmQg7JqU6rWs7IKs7ZWt7J2AIO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTt
hZzsi5ztl5jsnLzroZwg67OE64+EIO2ZleyduO2VnOuLpC4KCjYuICoq7Jik64u1OioqIOygleyg
geu2hOyEneydgCDtlITroZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7JesIOyeheugpeqzvCDstpzroKXs
nYQg7Lih7KCV7ZWY64qUIOyLnO2XmOydtOuLpC4KICAgLSAqKuygleyglToqKiDsoJXsoIHrtoTs
hJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2VmOyngCDslYrqs6Ag7L2U65Ocwrfrqqjrjbjs
nZgg6rec7LmZLCDtnZDrpoQsIOuzteyeoeuPhOyZgCDsnqDsnqzqsrDtlajsnYQg67aE7ISd7ZWc
64ukLgoKNy4gKirsmKTri7U6Kiog64+Z7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6Tt
lontlZjsp4Ag7JWK64qUIOusuOyEnCDqsoDthqDsnbTri6QuCiAgIC0gKirsoJXsoJU6Kiog64+Z
7KCB67aE7ISd7J2AIOyLpO2WieuQnCDshoztlITtirjsm6jslrTsnZgg6rK966GcLCDsi5zqsIQs
IOyekOybkOqzvCDrsJjsnZHsnYQg7J6F66ClIOyhsOqxtOuzhOuhnCDqtIDssLDtlZzri6QuCgo4
LiAqKuyYpOuLtToqKiDtmozqt4Dsi5ztl5jsnYAg7IOI66GcIOy2lOqwgOuQnCDquLDriqXrp4wg
7Iuc7ZeY7ZWY66m0IOuQnOuLpC4KICAgLSAqKuygleyglToqKiDtmozqt4Dsi5ztl5jsnYAg67OA
6rK9IOq4sOuKpeqzvCDtlajqu5gg7JiB7Zal67Cb7J2EIOyImCDsnojripQg6riw7KG0IOq4sOuK
pcK37J247YSw7Y6Y7J207Iqk7J2YIOycoOyngCDsl6zrtoDrpbwg7ZmV7J247ZWc64ukLgoKOS4g
KirsmKTri7U6Kiog7Iuc666s66CI7J207IWYIOqysOqzvOuKlCDsi6TsoJwg7ZiE7J6l6rO8IO2V
reyDgSDsmYTsoITtnogg64+Z7J287ZWY64ukLgogICAtICoq7KCV7KCVOioqIFNpbXVsYXRpb27s
nYAg66qo6424IOq4sOuwmOydtOuvgOuhnCDrqqjrjbgg6rCA7KCV6rO8IO2VnOqzhOulvCDtj4nq
sIDtlZjqs6Ag7ZWE7JqU7ZWY66m0IEhJTMK37ZiE7J6lIOuLqOqzhOydmCDstpTqsIAg6rKA7Kad
7Jy866GcIOuztOyZhO2VnOuLpC4KCjEwLiAqKuyYpOuLtToqKiBISUzsnYAg67CY65Oc7IucIOyL
pOygnCDsg53sgrDshKTruYTrpbwg6rCA64+Z7ZW07JW866eMIOyImO2Wie2VoCDsiJgg7J6I64uk
LgogICAtICoq7KCV7KCVOioqIEhJTOydgCDsi6TsoJwg7KCc7Ja0IEhXIOuYkOuKlCDsi6Ttlont
mZjqsr3snYQg7Iuk7Iuc6rCEIHBsYW50IOuqqOuNuOqzvCDtj5Dro6jtlITroZwg7Jew6rKw7ZWY
7JesIOyLpOygnCBwbGFudCDqsIDrj5kg7JeG7J20IEhXwrdTVyDsg4HtmLjsnpHsmqnsnYQg6rKA
7Kad7ZWgIOyImCDsnojri6QuCgoxMS4gKirsmKTri7U6Kiog6rKw7ZWo7KO87J6F7J2AIO2MjOq0
tOyLnO2XmOydtOuvgOuhnCDshoztlITtirjsm6jslrQg7Iuc7ZeY7JeQ64qUIOyCrOyaqe2VoCDs
iJgg7JeG64ukLgogICAtICoq7KCV7KCVOioqIEZhdWx0IGluamVjdGlvbuydgCDthrXsoJzrkJwg
7ZmY6rK97JeQ7IScIOyEvOyEnMK37Ya17IugwrfsoITsm5DCt+uNsOydtO2EsMK3dGFzayDsnbTs
g4HsnYQg7KO87J6F7ZW0IOqygOy2nMK36rKp66aswrfrs7Xqtazrpbwg6rKA7Kad7ZWc64ukLgoK
MTIuICoq7Jik64u1OioqIOyLnO2XmOydtCDsi6TtjKjtlZjrqbQg7JiI7IOB6rKw6rO866W8IOyL
pOygnCDqsrDqs7zroZwg67CU6r647Ja0IO2GteqzvCDsspjrpqztlZjrqbQg65Cc64ukLgogICAt
ICoq7KCV7KCVOioqIOyLnO2XmCDsoIQg6rOg7KCV7ZWcIOyYiOyDgeqysOqzvOyZgCDtjJDsoJXq
uLDspIDsnYQg7Jyg7KeA7ZWY6rOgIOyLpO2MqOuKlCDqsrDtlagg65iQ64qUIOyKueyduOuQnCDs
mpTqtazsgqztla0g67OA6rK97Jy866GcIOy2lOygge2VtOyVvCDtlZzri6QuCgoxMy4gKirsmKTr
i7U6Kiog7L2U65OcIOumrOu3sOulvCDsiJjtlontlZjrqbQg64+Z7KCBIOyLnO2XmOqzvCDsi5zs
iqTthZzsi5ztl5jsnYQg66qo65GQIOyDneuete2VoCDsiJgg7J6I64ukLgogICAtICoq7KCV7KCV
OioqIFJldmlld+yZgCDsoJXsoIHrtoTshJ3snYAg7Iuk7ZaJIOq4sOuwmCDsi5ztl5jsnYQg67O0
7JmE7ZWY7KeA66eMIOuMgOyytO2VmOyngCDslYrsnLzrqbAg7JqU6rWs7IKs7ZWtIOyImOykgOyX
kCDrp57ripQg64+Z7KCBwrfthrXtlanCt+yLnOyKpO2FnCDsi5ztl5jsnbQg7ZWE7JqU7ZWY64uk
LgoKMTQuICoq7Jik64u1OioqIOyLnO2XmOqysOqzvOyXkCDrjIDsg4Eg67KE7KCE6rO8IOyLnO2X
mO2ZmOqyveydhCDquLDroZ3tlZjsp4Ag7JWK7JWE64+EIOyerO2YhO2VoCDsiJgg7J6I64ukLgog
ICAtICoq7KCV7KCVOioqIOyLnO2XmOuMgOyDgSBiYXNlbGluZSwgSFfCt09TwrdmaXJtd2FyZcK3
dG9vbOqzvCDshKTsoJXsnYQg7Iud67OE7ZW07JW8IOqysOqzvOydmCDsnqztmITshLHqs7wg6rCQ
7IKs6rCA64ql7ISx7J2EIO2ZleuztO2VoCDsiJgg7J6I64ukLgoKMTUuICoq7Jik64u1OioqIOye
keydgCDrs4Dqsr3snYAg7JiB7Zal67aE7ISd6rO8IO2ajOq3gOyLnO2XmOydhCDtla3sg4Eg7IOd
65617ZWgIOyImCDsnojri6QuCiAgIC0gKirsoJXsoJU6Kiog67OA6rK9IOq3nOuqqOyZgCDrrLTq
tIDtlZjqsowg7JiB7Zal67KU7JyE66W8IO2PieqwgO2VmOqzoCDqt7gg6rKw6rO87JeQIOuUsOud
vCBSVE3Ct+yCsOy2nOusvMK37ZqM6reA7Iuc7ZeYIOuylOychOulvCDqsLHsi6DtlbTslbwg7ZWc
64ukLgoKMTYuICoq7Jik64u1OioqIOydvOuwmCDshoztlITtirjsm6jslrQgViZW66W8IOyZhOuj
jO2VmOuptCDrs4Trj4QgU2FmZXR5IGxpZmVjeWNsZSDsl4bsnbQgU0lT7J2YIFNJTCDstqnsobHs
nbQg7J6Q64+Z7Jy866GcIOymneuqheuQnOuLpC4KICAgLSAqKuygleyglToqKiBTVy0wNOydmCDs
nbzrsJggViZW7JmAIFNXLTA17J2YIFNhZmV0eSBJbnRlZ3JpdHksIOuPheumveyEsSwg7LK06rOE
7KCBIOqzoOyepSDthrXsoJzsmYAgU2FmZXR5IFYmVuulvCDqtazrtoTtlbTslbwg7ZWc64ukLgoK
IyMgMTUuIOuLteyViCDsnpHshLEg6rWs7KGwCgoxLiBTVy0wNOydmCDrqqnsoIHqs7wgU1ctMDXC
t1NXLTEwIOqyveqzhAoyLiDsi5ztl5gg6rCA64ql7ZWcIFJlcXVpcmVtZW50IHNwZWNpZmljYXRp
b24KMy4gVi1Nb2RlbCDsoozCt+yasCDrjIDsnZEKNC4gQXJjaGl0ZWN0dXJlwrdEZXRhaWxlZCBk
ZXNpZ27Ct0NvZGluZyBzdGFuZGFyZAo1LiBVbml0wrdJbnRlZ3JhdGlvbsK3U3lzdGVtIHRlc3QK
Ni4gVmVyaWZpY2F0aW9uwrdWYWxpZGF0aW9uwrdSVE0KNy4gU3RhdGljwrdEeW5hbWljwrdSZWdy
ZXNzaW9u6rO8IFNpbXVsYXRpb27Ct0hJTMK3RmF1bHQgaW5qZWN0aW9uCjguIERlZmVjdMK3Q2hh
bmdlwrdSZXZpZXfCt0FwcHJvdmFs7JmAIOymneyggQoKIyMgMTYuIEZvY3VzZWQgcmVncmVzc2lv
biDqtIDsoJAKCi0g7KeB7KCRIOyYpOuLtSDrrLjsnqXrp4wgZGV0ZXJtaW5pc3RpYyBmYXRhbCBw
YXR0ZXJu6rO8IOydvOy5mO2VnOuLpC4KLSDsnbjsmqkg65KkIOygleygle2VnCDrrLjsnqXsnYAg
ZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4KLSBTVy0wNSBTYWZldHkgbGlmZWN5Y2xlIOuLqOuP
hSDrrLjtla3qs7wgU1ctMTAgRkFUwrdTQVQg64uo64+FIOusuO2VreydgCBTVy0wNCByb3V0aW5n
IHBvc2l0aXZl66GcIOuztOyngCDslYrripTri6QuCi0gVi1Nb2RlbCwgUlRNLCDsi5ztl5jsiJjs
pIAsIOu2hOyEncK37ZqM6reALCBISUzCt0ZhdWx0IGluamVjdGlvbuydmCBzZW1hbnRpYyBncm91
cOydhCDqsIHqsIEg7ZmV7J247ZWc64ukLgotIHNvdXJjZSBKU09OIDTqsJzsmYAgTWFya2Rvd24s
IGZvY3VzZWQgdGVzdOunjCBMYW5lIEEgVG9waWMtbG9jYWwgY29tbWl07JeQIO2PrO2VqO2VnOuL
pC4K
PAYLOAD_SW04_01

    write_payload 'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/README.md' '1e1648cc9185cae8aac30ee686acdb2bbe6921a4a422e2dc5ad34c0f6775e38e' <<'PAYLOAD_SW04_02'
IyDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IOyImOuqheyjvOq4sCwgVi1Nb2RlbCwg7LaU
7KCB7ISxLCDqsoDspp0g67CPIO2ZleyduAoKIyMgVG9waWMgSUQKCmBpbnN0cnVtZW50YXRpb25f
Y29udHJvbF9zb2Z0d2FyZV9saWZlY3ljbGVfdl9tb2RlbF90cmFjZWFiaWxpdHlfdmVyaWZpY2F0
aW9uX3ZhbGlkYXRpb25gCgojIyDrqqnsoIEKCuydtCBUb3BpYyBQYWNr7J2AIOydvOuwmCDqs4Ts
uKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja07J2YIOyalOq1rOyCrO2VrSwg7JWE7YKk7YWN7LKYLCDs
g4HshLjshKTqs4QsIOq1rO2YhCwg7Iuc7ZeYLCDstpTsoIHshLEsIOqysO2VqMK367OA6rK96rSA
66as7JmAIOyKueyduCDspp3soIHsnYQgVi1Nb2RlbOydmCDtlZjrgpjsnZgg7Z2Q66aE7Jy866Gc
IO2PieqwgO2VnOuLpC4KCiMjIO2PrO2VqCDrspTsnIQKCi0gUmVxdWlyZW1lbnQgc3BlY2lmaWNh
dGlvbuqzvCDsi5ztl5gg6rCA64ql7ZWcIGFjY2VwdGFuY2UgY3JpdGVyaWEKLSBTeXN0ZW0gYXJj
aGl0ZWN0dXJl7JmAIFNvZnR3YXJlIGFyY2hpdGVjdHVyZQotIERldGFpbGVkIGRlc2lnbuqzvCBD
b2Rpbmcgc3RhbmRhcmQKLSBVbml0IHRlc3QsIEludGVncmF0aW9uIHRlc3TsmYAgU3lzdGVtIHRl
c3QKLSBWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbgotIFJlcXVpcmVtZW50IFRyYWNlYWJpbGl0
eSBNYXRyaXjsnZgg7JaR67Cp7ZalIOy2lOyggQotIFN0YXRpYyBhbmFseXNpcywgRHluYW1pYyBh
bmFseXNpc+yZgCBSZWdyZXNzaW9uIHRlc3QKLSBTaW11bGF0aW9uLCBISUzqs7wgRmF1bHQgaW5q
ZWN0aW9uCi0gRGVmZWN0IG1hbmFnZW1lbnQsIENoYW5nZSBpbXBhY3TsmYAgQ29uZmlndXJhdGlv
biBiYXNlbGluZQotIFJldmlldywgQXBwcm92YWwsIEV4aXQgY3JpdGVyaWHsmYAgViZWIGV2aWRl
bmNlCgojIyBvd25lcnNoaXAg6rK96rOECgotIFNXLTA0IOyGjOycoDog7J2867CYIOqzhOy4oeyg
nOyWtCBTVyBsaWZlY3ljbGUsIFYtTW9kZWwsIOy2lOyggeyEsSwg6rCc67Cc64uo6rOE67OEIFYm
VgotIFNXLTA1IOydtOq0gDogU0lTIFNhZmV0eSBJbnRlZ3JpdHksIOuPheumveyEsSwg7LK06rOE
7KCBIOqzoOyepSDthrXsoJzsmYAgU2FmZXR5IFYmVgotIFNXLTEwIOydtOq0gDog7ZSE66Gc7KCd
7Yq4IOusuOyEnCDsnbjrj4QsIEZBVMK3U0FUwrdMb29wIHRlc3TCt+yLnOyatOyghMK3QWNjZXB0
YW5jZcK3SGFuZG92ZXIKLSBTVy0wMyDsnbTqtIA6IEhNScK3U0NBREEgQWxhcm3Ct1NPReyZgCDs
mrTsoITsnpAg7KCV67O06rSA66asCi0gU1ctMDIg7J206rSAOiBTZXF1ZW5jZcK3SW50ZXJsb2Nr
wrdUcmlw7J2YIOyLpOygnCDsg4Htg5zsoITsnbTsmYAgRmFpbC1zYWZlIOyatOyghOuFvOumrAoK
IyMg7ZW17IusIOuFvOumrOq0gOqzhAoKYGBgdGV4dApWZXJpZmljYXRpb24gPSDsgrDstpzrrLzs
nbQg7ZW064u5IOuLqOqzhCDrqoXshLjsmYAg7ISk6rOE6riw7KSA7JeQIOunnuuKlOqwgApWYWxp
ZGF0aW9uICAgPSDthrXtlakg7Iuc7Iqk7YWc7J20IOydmOuPhOuQnCDsgqzsmqnrqqnsoIHqs7wg
7IKs7Jqp7J6QIOyalOq1rOulvCDstqnsobHtlZjripTqsIAKClJUTToKUmVxdWlyZW1lbnQKICDi
hpQgQXJjaGl0ZWN0dXJlCiAg4oaUIERldGFpbGVkIGRlc2lnbgogIOKGlCBDb2RlCiAg4oaUIFRl
c3QgY2FzZQogIOKGlCBUZXN0IHJlc3VsdAoKVi1Nb2RlbCDrjIDsnZE6ClJlcXVpcmVtZW50IC8g
aW50ZW5kZWQgdXNlIOKGlCBTeXN0ZW0gdGVzdCAvIFZhbGlkYXRpb24KU3lzdGVtwrdTVyBhcmNo
aXRlY3R1cmUgICAgIOKGlCBJbnRlZ3JhdGlvbiB0ZXN0CkRldGFpbGVkIGRlc2lnbiAvIG1vZHVs
ZSAgIOKGlCBVbml0IHRlc3QKYGBgCgrri6jsnITsi5ztl5gg7Ya16rO864qUIO2Gte2VqeyLnO2X
mOqzvCDsi5zsiqTthZzsi5ztl5jsnYQg64yA7LK07ZWY7KeAIOyViuuKlOuLpC4g7KCV7KCB67aE
7ISd7J2AIOu5hOyLpO2WiSDrtoTshJ3snbTqs6Ag64+Z7KCB67aE7ISd7J2AIOyLpO2Wieq4sOuw
mCDrtoTshJ3snbTri6QuIO2ajOq3gOyLnO2XmOydgCDrs4Dqsr3rkJwg6riw64ql67+QIOyVhOuL
iOudvCDsmIHtlqXrsJvripQg6riw7KG0IOq4sOuKpeqzvCDsnbjthLDtjpjsnbTsiqTrpbwg7ZmV
7J247ZWc64ukLgoKIyMg64yA7ZGcIOyYpOuLtQoKLSBWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlv
buydgCDqsJnsnYAg7Zmc64+Z7J2064ukLgotIFYtTW9kZWzsl5DshJzripQg7L2U65SpIO2bhCDs
i5ztl5jsnYQg7LKY7J2MIOqzhO2aje2VnOuLpC4KLSDtlZwg67Cp7ZalIFJUTeunjOycvOuhnCDs
lpHrsKntlqUg7LaU7KCB7ISx7J20IOyZhOyEseuQnOuLpC4KLSDri6jsnITsi5ztl5gg7Ya16rO8
6rCAIO2Gte2VqcK37Iuc7Iqk7YWc7Iuc7ZeY7J2EIOuMgOyytO2VnOuLpC4KLSDsoJXsoIHrtoTs
hJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2VnOuLpC4KLSDtmozqt4Dsi5ztl5jsnYAg7IOI
IOq4sOuKpeunjCDtmZXsnbjtlZzri6QuCi0gU2ltdWxhdGlvbuydgCDtmITsnqXqs7wg7ZWt7IOB
IOyZhOyghO2eiCDrj5nsnbztlZjri6QuCi0gSElM7J2AIOuwmOuTnOyLnCDsi6TsoJwg7IOd7IKw
7ISk67mE66W8IOqwgOuPme2VtOyVvCDtlZzri6QuCi0g7Iuc7ZeYIOyLpO2MqCDsi5wgZXhwZWN0
ZWQgcmVzdWx066W8IOyLpOygnCDqsrDqs7zroZwg67CU6r6466m0IOuQnOuLpC4KLSDsnbzrsJgg
U1cgViZW66eM7Jy866GcIFNJUyBTSUwg7Lap7KGx7J20IOyekOuPmSDspp3rqoXrkJzri6QuCgoj
IyDtjIzsnbwKCi0gYGZhY3RfYW5jaG9yLmpzb25gOiAzMeqwnCBGYWN0IEFuY2hvcuyZgCAxNuqw
nCBGYXRhbCDsmKTri7UKLSBgbG9naWNfY2hlY2suanNvbmA6IGRldGVybWluaXN0aWMgYWlkLCBM
TE0gdHJ1dGggc2NoZW1hLCBNYWpvcuyZgCBmYWxzZS1wb3NpdGl2ZSDquLDspIAKLSBgbW9kZWxf
YW5zd2VyLmpzb25gOiDrjIDtkZwg66y47KCcIDEw6rCcLCDri7XslYjqtazsobAgOOqwnOyZgCBS
b3V0aW5nIOygleuztAotIGB0b3BpY19pbXBvcnRhbmNlLmpzb25gOiDrgpzsnbTrj4TsmYAg7ISg
7YOdIOykkeyalOuPhAotIGBkb2NzL3RvcGljX3NoZWV0cy9pbnN0cnVtZW50YXRpb25fY29udHJv
bF9zb2Z0d2FyZV9saWZlY3ljbGVfdl9tb2RlbF90cmFjZWFiaWxpdHlfdmVyaWZpY2F0aW9uX3Zh
bGlkYXRpb24ubWRgOiDsg4HshLggVG9waWMgU2hlZXQKLSBgc2NyaXB0cy90ZXN0X2luc3RydW1l
bnRhdGlvbl9jb250cm9sX3NvZnR3YXJlX2xpZmVjeWNsZV92X21vZGVsLnB5YDogZm9jdXNlZCBy
ZWdyZXNzaW9uCgojIyDqsoDspp0g6rK96rOECgpUb3BpYy1sb2NhbCDri6jqs4Tsl5DshJzripQg
SlNPTiwgc291cmNlIHNjaGVtYSwgVG9waWMgcXVhbGl0eSwgZm9jdXNlZCB0ZXN0LCBQeXRob24g
Y29tcGlsZSwgd2hpdGVzcGFjZSwgYGdpdCBkaWZmIC0tY2hlY2tg7JmAIExhbmUgQSBvd25lcnNo
aXDrp4wg6rKA7Kad7ZWc64ukLiBHZW5lcmF0ZWQgcmVidWlsZCwg7KCE7LK0IFJvdXRlciDtmozq
t4AsIGNyb3NzLXRvcGljIGR1cGxpY2F0ZSwgdmFsaWRhdGUtYWxsLCByZWxlYXNlIHZhbGlkYXRp
b27smYAgY29udGFpbmVyIHNtb2tl64qUIOy1nOyihSDthrXtlakg64uo6rOE66GcIOuEmOq4tOuL
pC4K
PAYLOAD_SW04_02

    write_payload 'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/fact_anchor.json' '304a31cab09ffbaecbfe37f163fc38bb32b0b6beba9dd3be73a974d5e626d2da' <<'PAYLOAD_SW04_03'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLmZhY3RfYW5jaG9yLnYxIiwKICAidG9w
aWNfaWQiOiAiaW5zdHJ1bWVudGF0aW9uX2NvbnRyb2xfc29mdHdhcmVfbGlmZWN5Y2xlX3ZfbW9k
ZWxfdHJhY2VhYmlsaXR5X3ZlcmlmaWNhdGlvbl92YWxpZGF0aW9uIiwKICAidGl0bGVfa28iOiAi
6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCDsiJjrqoXso7zquLAsIFYtTW9kZWwsIOy2lOyg
geyEsSwg6rKA7KadIOuwjyDtmZXsnbgiLAogICJxdWVzdGlvbl90eXBlX2hpbnQiOiAiUFJPQ0VE
VVJFIiwKICAiYW5jaG9ycyI6IFsKICAgIHsKICAgICAgImlkIjogInN3MDRfc2NvcGVfZ2VuZXJh
bF9saWZlY3ljbGUiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfc2NvcGVfZ2VuZXJhbF9saWZl
Y3ljbGUiLAogICAgICAic3RhdGVtZW50IjogIlNXLTA064qUIOydvOuwmCDqs4TsuKHsoJzslrQg
7IaM7ZSE7Yq47Juo7Ja07J2YIOyalOq1rOyCrO2VrSwg7JWE7YKk7YWN7LKYLCDsg4HshLjshKTq
s4QsIOq1rO2YhCwg7Iuc7ZeYLCDstpTsoIHshLEsIOqysO2VqOq0gOumrOyZgCDsirnsnbjquYzs
p4DsnZgg7IiY66qF7KO86riw66W8IOuLpOujrOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAg
ICAgICAgIuyGjO2UhO2KuOybqOyWtCDsiJjrqoXso7zquLAiLAogICAgICAgICLsmpTqtazsgqzt
la0iLAogICAgICAgICLshKTqs4QiLAogICAgICAgICLqtaztmIQiLAogICAgICAgICLsi5ztl5gi
LAogICAgICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBdLAog
ICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAi7IaM7ZSE7Yq47Juo7Ja0IOyImOuqheyjvOq4
sCIsCiAgICAgICAgIuyalOq1rOyCrO2VrSIsCiAgICAgICAgIuyEpOqzhCIsCiAgICAgICAgIuq1
rO2YhCIsCiAgICAgICAgIuyLnO2XmCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0
aW9ucyI6IFsKICAgICAgICAiU1ctMDTripQg7J2867CYIOqzhOy4oeygnOyWtCDshoztlITtirjs
m6jslrTsnZgg7JqU6rWs7IKs7ZWtLCDslYTtgqTthY3sspgsIOyDgeyEuOyEpOqzhCwg6rWs7ZiE
LCDsi5ztl5gsIOy2lOyggeyEsSwg6rKw7ZWo6rSA66as7JmAIOyKueyduOq5jOyngOydmCDsiJjr
qoXso7zquLDrpbwg64uk66Os64ukLiIsCiAgICAgICAgIuydvOuwmCDqs4TsuKHsoJzslrQgU1cg
bGlmZWN5Y2xlIiwKICAgICAgICAi7JqU6rWs7IKs7ZWt67aA7YSwIOyKueyduOq5jOyngCIKICAg
ICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7JWI7KCE66y0
6rKw7ISxIOyCsOygleydtOuCmCDtlITroZzsoJ3tirgg7ZiE7J6lIOyduOyImCDsoIjssKjrpbwg
U1ctMDTsnZgg7KeB7KCRIOyGjOycoOuylOychOuhnCDtmZXsnqXtlZzri6QuIgogICAgICBdLAog
ICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg
7IKw7JeFIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuw
jyBWJlYg7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuM
gCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOya
lOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64uk
LiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X3N3MDVfYm91bmRhcnkiLAogICAgICAi
YW5jaG9yX2lkIjogInN3MDRfc3cwNV9ib3VuZGFyeSIsCiAgICAgICJzdGF0ZW1lbnQiOiAiU0lT
IOyViOyghCDshoztlITtirjsm6jslrTsnZggU2FmZXR5IEludGVncml0eSwg64+F66a97ISxLCDs
srTqs4TsoIEg6rOg7J6lIO2GteygnOyZgCBTYWZldHkgViZW64qUIFNXLTA166GcIOydtOq0gO2V
nOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIlNXLTA1IOqyveqzhCIsCiAgICAg
ICAgIlNhZmV0eSBJbnRlZ3JpdHkiLAogICAgICAgICLrj4Xrpr3shLEiLAogICAgICAgICLssrTq
s4TsoIEg6rOg7J6lIiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2Rl
bCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIlNXLTA1IOqyveqzhCIs
CiAgICAgICAgIlNhZmV0eSBJbnRlZ3JpdHkiLAogICAgICAgICLrj4Xrpr3shLEiLAogICAgICAg
ICLssrTqs4TsoIEg6rOg7J6lIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25z
IjogWwogICAgICAgICJTSVMg7JWI7KCEIOyGjO2UhO2KuOybqOyWtOydmCBTYWZldHkgSW50ZWdy
aXR5LCDrj4Xrpr3shLEsIOyytOqzhOyggSDqs6DsnqUg7Ya17KCc7JmAIFNhZmV0eSBWJlbripQg
U1ctMDXroZwg7J206rSA7ZWc64ukLiIsCiAgICAgICAgIuydvOuwmCBTVyBWJlbsmYAgU2FmZXR5
IFYmVuulvCDqtazrtoTtlZzri6QuIiwKICAgICAgICAiU0lMwrdQRkRhdmfCt1BGSOuKlCBTVy0w
NSDsmIHsl63snbTri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjog
WwogICAgICAgICLsnbzrsJggU1cgbGlmZWN5Y2xlIOyEpOuqheunjOycvOuhnCBTSVMg7JWI7KCE
66y06rKw7ISxIOy2qeyhseydhCDshKDslrjtlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0
YW5jZSI6ICJtdXN0IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4
oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZ
IiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAg
ZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyX
kCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0sCiAg
ICB7CiAgICAgICJpZCI6ICJzdzA0X3N3MTBfYm91bmRhcnkiLAogICAgICAiYW5jaG9yX2lkIjog
InN3MDRfc3cxMF9ib3VuZGFyeSIsCiAgICAgICJzdGF0ZW1lbnQiOiAiRkFUwrdTQVTCt0xvb3Ag
dGVzdMK37Iuc7Jq07KCEwrfshLHriqXsi5ztl5jCt0FjY2VwdGFuY2XCt0hhbmRvdmVy64qUIFNX
LTEw7J2YIO2UhOuhnOygne2KuCDsiJjtlokg67CPIOyduOyImCDsmIHsl63snbTri6QuIiwKICAg
ICAgImtleXdvcmRzIjogWwogICAgICAgICJTVy0xMCDqsr3qs4QiLAogICAgICAgICJGQVQiLAog
ICAgICAgICJTQVQiLAogICAgICAgICLsi5zsmrTsoIQiLAogICAgICAgICLsnbjsiJgiLAogICAg
ICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBdLAogICAgICAi
Y29yZV90ZXJtcyI6IFsKICAgICAgICAiU1ctMTAg6rK96rOEIiwKICAgICAgICAiRkFUIiwKICAg
ICAgICAiU0FUIiwKICAgICAgICAi7Iuc7Jq07KCEIiwKICAgICAgICAi7J247IiYIgogICAgICBd
LAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJGQVTCt1NBVMK3TG9v
cCB0ZXN0wrfsi5zsmrTsoITCt+yEseuKpeyLnO2XmMK3QWNjZXB0YW5jZcK3SGFuZG92ZXLripQg
U1ctMTDsnZgg7ZSE66Gc7KCd7Yq4IOyImO2WiSDrsI8g7J247IiYIOyYgeyXreydtOuLpC4iLAog
ICAgICAgICJTVy0wNOuKlCDqsJzrsJwgbGlmZWN5Y2xl6rO8IFYmViDssrTqs4TrpbwsIFNXLTEw
7J2AIO2UhOuhnOygne2KuCDtmITsnqXqsoDspp3qs7wg7J247IiY66W8IOyGjOycoO2VnOuLpC4i
CiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkZBVOyZ
gCBTQVTrpbwg64uo7JyE7Iuc7ZeY7J2064KYIO2Gte2VqeyLnO2XmOqzvCDsmYTsoITtnogg6rCZ
7J2AIOuLqOqzhOuhnCDst6jquIntlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0YW5jZSI6
ICJtdXN0IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeygnOyW
tCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAg
ICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg
7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDr
nbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0sCiAgICB7CiAg
ICAgICJpZCI6ICJzdzA0X3ZfbW9kZWxfZGVmaW5pdGlvbiIsCiAgICAgICJhbmNob3JfaWQiOiAi
c3cwNF92X21vZGVsX2RlZmluaXRpb24iLAogICAgICAic3RhdGVtZW50IjogIlYtTW9kZWzsnYAg
7KKM7Lih7J2YIOyalOq1rOyCrO2VrcK37ISk6rOEwrfqtaztmIQg64uo6rOE7JmAIOyasOy4oeyd
mCDrjIDsnZEg7Iuc7ZeYwrftmZXsnbgg64uo6rOE66W8IOyXsOqysO2VmOqzoCwg7Iuc7ZeY6riw
7KSA7J2EIOqwnOuwnCDstIjquLDsl5Ag7KSA67mE7ZWY64qUIGxpZmVjeWNsZSDrqqjrjbjsnbTr
i6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJWLU1vZGVsIiwKICAgICAgICAi7KKM
7LihIOqwnOuwnCIsCiAgICAgICAgIuyasOy4oSDsi5ztl5giLAogICAgICAgICLrjIDsnZHqtIDq
s4QiLAogICAgICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICLstpTsoIHshLEiCiAgICAg
IF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJWLU1vZGVsIiwKICAgICAgICAi7KKM
7LihIOqwnOuwnCIsCiAgICAgICAgIuyasOy4oSDsi5ztl5giLAogICAgICAgICLrjIDsnZHqtIDq
s4QiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIlYt
TW9kZWzsnYAg7KKM7Lih7J2YIOyalOq1rOyCrO2VrcK37ISk6rOEwrfqtaztmIQg64uo6rOE7JmA
IOyasOy4oeydmCDrjIDsnZEg7Iuc7ZeYwrftmZXsnbgg64uo6rOE66W8IOyXsOqysO2VmOqzoCwg
7Iuc7ZeY6riw7KSA7J2EIOqwnOuwnCDstIjquLDsl5Ag7KSA67mE7ZWY64qUIGxpZmVjeWNsZSDr
qqjrjbjsnbTri6QuIiwKICAgICAgICAi7JqU6rWs7IKs7ZWt6rO8IEFjY2VwdGFuY2Ug6riw7KSA
LCDslYTtgqTthY3sspjsmYAg7Ya17ZWp7Iuc7ZeYLCDsg4HshLjshKTqs4TsmYAg64uo7JyE7Iuc
7ZeY7J2EIOuMgOydkeyLnO2CqOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5h
dGlvbnMiOiBbCiAgICAgICAgIuy9lOuUqeydtCDrqqjrkZAg64Gd64KcIO2bhCDsi5ztl5jsnYQg
7LKY7J2MIOqzhO2aje2VmOuKlCDsiJzssKjrqqjrjbjroZzrp4wg7ISk66qF7ZWc64ukLiIKICAg
ICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi
7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSwgVi1N
b2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyd
uCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOus
uO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2Pieqw
gO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9yZXF1aXJlbWVudHNfc3Bl
Y2lmaWNhdGlvbiIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwNF9yZXF1aXJlbWVudHNfc3BlY2lm
aWNhdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAi7JqU6rWs7IKs7ZWt7J2AIOyLneuzhOyekCwg
6riw64qlLCDshLHriqUsIOyduO2EsO2OmOydtOyKpCwg7Jq07KCE66qo65OcLCDsmIjsmbjCt+qz
oOyepeydkeuLteqzvCDsiJjsmqnquLDspIDsnYQg7Y+s7ZWo7ZWY66mwIOuqhe2Zle2VmOqzoCDs
i5ztl5gg6rCA64ql7ZW07JW8IO2VnOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAg
IuyalOq1rOyCrO2VrSDrqoXshLgiLAogICAgICAgICLsi5ztl5gg6rCA64ql7ISxIiwKICAgICAg
ICAi7IiY7Jqp6riw7KSAIiwKICAgICAgICAi6rOg7J6l7J2R64u1IiwKICAgICAgICAi6rOE7Lih
7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMi
OiBbCiAgICAgICAgIuyalOq1rOyCrO2VrSDrqoXshLgiLAogICAgICAgICLsi5ztl5gg6rCA64ql
7ISxIiwKICAgICAgICAi7IiY7Jqp6riw7KSAIiwKICAgICAgICAi6rOg7J6l7J2R64u1IgogICAg
ICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsmpTqtazsgqzt
la3snYAg7Iud67OE7J6QLCDquLDriqUsIOyEseuKpSwg7J247YSw7Y6Y7J207IqkLCDsmrTsoITr
qqjrk5wsIOyYiOyZuMK36rOg7J6l7J2R64u16rO8IOyImOyaqeq4sOykgOydhCDtj6ztlajtlZjr
qbAg66qF7ZmV7ZWY6rOgIOyLnO2XmCDqsIDriqXtlbTslbwg7ZWc64ukLiIsCiAgICAgICAgIuuq
qO2YuO2VnCDtkZztmIQg64yA7IugIOy4oeyglSDqsIDriqUg7KGw6rG06rO8IO2MkOygleq4sOyk
gOydhCDrkZTri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwog
ICAgICAgICIn7KCB7KCI7Z6IJywgJ+y2qeu2hO2eiCfsmYAg6rCZ7J2AIOu5hOqygOymnSDtkZzt
mITrp4zsnLzroZwg7JqU6rWs7IKs7ZWt7J2EIO2Zleygle2VnOuLpC4iCiAgICAgIF0sCiAgICAg
ICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDs
l4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYm
ViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyj
vOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs
67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgog
ICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfc3lzdGVtX2FyY2hpdGVjdHVyZSIsCiAgICAg
ICJhbmNob3JfaWQiOiAic3cwNF9zeXN0ZW1fYXJjaGl0ZWN0dXJlIiwKICAgICAgInN0YXRlbWVu
dCI6ICLsi5zsiqTthZwg7JWE7YKk7YWN7LKY64qUIOygnOyWtOq4sCwgSE1JLCDshJzrsoQsIOuE
pO2KuOybjO2BrCwgSS9P7JmAIOyZuOu2gOyLnOyKpO2FnOydmCDquLDriqXrsLDrtoQsIOyduO2E
sO2OmOydtOyKpCwg642w7J207YSw7Z2Q66aE6rO8IOqzoOyepeqyveqzhOulvCDsoJXsnZjtlZzr
i6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICLsi5zsiqTthZwg7JWE7YKk7YWN7LKY
IiwKICAgICAgICAi6riw64ql67Cw67aEIiwKICAgICAgICAi7J247YSw7Y6Y7J207IqkIiwKICAg
ICAgICAi642w7J207YSw7Z2Q66aEIiwKICAgICAgICAi6rOg7J6l6rK96rOEIiwKICAgICAgICAi
6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVf
dGVybXMiOiBbCiAgICAgICAgIuyLnOyKpO2FnCDslYTtgqTthY3sspgiLAogICAgICAgICLquLDr
iqXrsLDrtoQiLAogICAgICAgICLsnbjthLDtjpjsnbTsiqQiLAogICAgICAgICLrjbDsnbTthLDt
nZDrpoQiLAogICAgICAgICLqs6DsnqXqsr3qs4QiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9l
eHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuyLnOyKpO2FnCDslYTtgqTthY3sspjripQg7KCc7Ja0
6riwLCBITUksIOyEnOuyhCwg64Sk7Yq47JuM7YGsLCBJL0/smYAg7Jm467aA7Iuc7Iqk7YWc7J2Y
IOq4sOuKpeuwsOu2hCwg7J247YSw7Y6Y7J207IqkLCDrjbDsnbTthLDtnZDrpoTqs7wg6rOg7J6l
6rK96rOE66W8IOygleydmO2VnOuLpC4iLAogICAgICAgICJIV8K3U1fCt+2GteyLoCDqsr3qs4Tr
pbwg7ZWo6ruYIOygleydmO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5h
dGlvbnMiOiBbCiAgICAgICAgIuq1rOyEseyalOyGjCDrqqnroZ3rp4wg7KCc7Iuc7ZWY6rOgIOyd
uO2EsO2OmOydtOyKpOyZgCDqs6DsnqXsoITtjIwg6rK96rOE66W8IOyDneuete2VnOuLpC4iCiAg
ICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogImltcG9ydGFudCIsCiAgICAgICJzb3VyY2VfYmFz
aXMiOiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNs
ZSwgVi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeyg
keyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE6529
7J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866Gc
IO2PieqwgO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9zb2Z0d2FyZV9h
cmNoaXRlY3R1cmUiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfc29mdHdhcmVfYXJjaGl0ZWN0
dXJlIiwKICAgICAgInN0YXRlbWVudCI6ICLshoztlITtirjsm6jslrQg7JWE7YKk7YWN7LKY64qU
IOuqqOuTiCwg7YOc7Iqk7YGsLCDsg4Htg5zqtIDrpqwsIOuNsOydtO2EsCwg7Ya17IugLCDsp4Tr
i6jqs7wg7J6Q7JuQ67Cw67aE7J2YIOq1rOyhsCDrsI8g7J247YSw7Y6Y7J207Iqk66W8IOygleyd
mO2VnOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIuyGjO2UhO2KuOybqOyWtCDs
lYTtgqTthY3sspgiLAogICAgICAgICLrqqjrk4giLAogICAgICAgICLtg5zsiqTtgawiLAogICAg
ICAgICLsnbjthLDtjpjsnbTsiqQiLAogICAgICAgICLsp4Tri6giLAogICAgICAgICLqs4TsuKHs
oJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6
IFsKICAgICAgICAi7IaM7ZSE7Yq47Juo7Ja0IOyVhO2CpO2FjeyymCIsCiAgICAgICAgIuuqqOuT
iCIsCiAgICAgICAgIu2DnOyKpO2BrCIsCiAgICAgICAgIuyduO2EsO2OmOydtOyKpCIsCiAgICAg
ICAgIuynhOuLqCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAg
ICAgICAi7IaM7ZSE7Yq47Juo7Ja0IOyVhO2CpO2FjeyymOuKlCDrqqjrk4gsIO2DnOyKpO2BrCwg
7IOB7YOc6rSA66asLCDrjbDsnbTthLAsIO2GteyLoCwg7KeE64uo6rO8IOyekOybkOuwsOu2hOyd
mCDqtazsobAg67CPIOyduO2EsO2OmOydtOyKpOulvCDsoJXsnZjtlZzri6QuIiwKICAgICAgICAi
7J2R7KeR64+ELCDqsrDtlanrj4QsIOyLpO2WieyjvOq4sOyZgCDrjbDsnbTthLAg7IaM7Jyg6raM
7J2EIOqzoOugpO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMi
OiBbCiAgICAgICAgIu2UhOuhnOq3uOueqCDtjIzsnbzrqoUg66qp66Gd7J2EIOyVhO2CpO2Fjeyy
mOuhnCDqsITso7ztlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0YW5jZSI6ICJpbXBvcnRh
bnQiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyG
jO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAi
Z3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Tr
s7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBt
YWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDRfZGV0YWlsZWRfZGVzaWduIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X2Rl
dGFpbGVkX2Rlc2lnbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAi7IOB7IS47ISk6rOE64qUIOyVjOqz
oOumrOymmCwg7IOB7YOc7KCE7J20LCBJL08g7LKY66asLCDsmIjsmbjsspjrpqwsIOuNsOydtO2E
sO2YlSwg6rK96rOE7KGw6rG06rO8IOuqqOuTiCDsnbjthLDtjpjsnbTsiqTrpbwg6rWs7ZiEIOqw
gOuKpe2VnCDsiJjspIDsnLzroZwg6rWs7LK07ZmU7ZWc64ukLiIsCiAgICAgICJrZXl3b3JkcyI6
IFsKICAgICAgICAi7IOB7IS47ISk6rOEIiwKICAgICAgICAi7JWM6rOg66as7KaYIiwKICAgICAg
ICAi7IOB7YOc7KCE7J20IiwKICAgICAgICAi7JiI7Jm47LKY66asIiwKICAgICAgICAi6rK96rOE
7KGw6rG0IiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAg
ICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIuyDgeyEuOyEpOqzhCIsCiAgICAg
ICAgIuyVjOqzoOumrOymmCIsCiAgICAgICAgIuyDge2DnOyghOydtCIsCiAgICAgICAgIuyYiOyZ
uOyymOumrCIsCiAgICAgICAgIuqyveqzhOyhsOqxtCIKICAgICAgXSwKICAgICAgImFjY2VwdGVk
X2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7IOB7IS47ISk6rOE64qUIOyVjOqzoOumrOymmCwg
7IOB7YOc7KCE7J20LCBJL08g7LKY66asLCDsmIjsmbjsspjrpqwsIOuNsOydtO2EsO2YlSwg6rK9
6rOE7KGw6rG06rO8IOuqqOuTiCDsnbjthLDtjpjsnbTsiqTrpbwg6rWs7ZiEIOqwgOuKpe2VnCDs
iJjspIDsnLzroZwg6rWs7LK07ZmU7ZWc64ukLiIsCiAgICAgICAgIuy9lOuTnOyZgCDsi5ztl5js
vIDsnbTsiqTqsIAg7LaU7KCBIOqwgOuKpe2VnCDshKTqs4Qg64uo7JyE66W8IOunjOuToOuLpC4i
CiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuygleyD
gSDqsr3roZzrp4wg6riw7Iig7ZWY6rOgIOyYiOyZuMK36rK96rOE7KGw6rG07J2EIOy9lOuTnCDr
i6jqs4Tsl5Ag66eh6ri064ukLiIKICAgICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAiaW1wb3J0
YW50IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeygnOyWtCDs
hoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAgICAg
ImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE
67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwg
bWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0sCiAgICB7CiAgICAg
ICJpZCI6ICJzdzA0X2NvZGluZ19zdGFuZGFyZCIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwNF9j
b2Rpbmdfc3RhbmRhcmQiLAogICAgICAic3RhdGVtZW50IjogIuy9lOuUqSDtkZzspIDsnYAg66qF
66qFLCDsnpDro4ztmJUsIOy0iOq4sO2ZlCwg67KU7JyELCDsmIjsmbjsspjrpqwsIOuzteyeoeuP
hCwg6riI7KeA6rWs66y4LCDso7zshJ3qs7wg66as67ewIOq4sOykgOydhCDsnbzqtIDrkJjqsowg
6rec7KCV7ZWc64ukLiIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAi7L2U65SpIO2RnOyk
gCIsCiAgICAgICAgIuy0iOq4sO2ZlCIsCiAgICAgICAgIuuzteyeoeuPhCIsCiAgICAgICAgIuq4
iOyngOq1rOusuCIsCiAgICAgICAgIuumrOu3sCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIs
CiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAg
ICLsvZTrlKkg7ZGc7KSAIiwKICAgICAgICAi7LSI6riw7ZmUIiwKICAgICAgICAi67O17J6h64+E
IiwKICAgICAgICAi6riI7KeA6rWs66y4IiwKICAgICAgICAi66as67ewIgogICAgICBdLAogICAg
ICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsvZTrlKkg7ZGc7KSA7J2AIOuq
heuqhSwg7J6Q66OM7ZiVLCDstIjquLDtmZQsIOuylOychCwg7JiI7Jm47LKY66asLCDrs7XsnqHr
j4QsIOq4iOyngOq1rOusuCwg7KO87ISd6rO8IOumrOu3sCDquLDspIDsnYQg7J286rSA65CY6rKM
IOq3nOygle2VnOuLpC4iLAogICAgICAgICLslrjslrTsmYAg7ZSM656r7Y+8IOychO2XmOyXkCDr
p57stpgg6rec7LmZ7J2EIOyggeyaqe2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9l
eHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuy9lOuUqSDtkZzspIDsnYQg65Ok7Jes7JOw6riw7JmA
IOyjvOyEnSDtmJXsi53rp4zsnLzroZwg7KCc7ZWc7ZWc64ukLiIKICAgICAgXSwKICAgICAgImlt
cG9ydGFuY2UiOiAiaW1wb3J0YW50IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw
7JeFIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBW
JlYg7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDs
o7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1
rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIK
ICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X2NvbmZpZ3VyYXRpb25fYmFzZWxpbmUiLAog
ICAgICAiYW5jaG9yX2lkIjogInN3MDRfY29uZmlndXJhdGlvbl9iYXNlbGluZSIsCiAgICAgICJz
dGF0ZW1lbnQiOiAi7JqU6rWs7IKs7ZWtwrfshKTqs4TCt+yGjOyKpMK37Iuc7ZeY7KCI7LCowrfr
j4TqtazCt+2ZmOqyveydgCDsi53rs4TrkJwgYmFzZWxpbmXqs7wg67KE7KCE7Jy866GcIOq0gOum
rOuQmOyWtOyVvCDrj5nsnbwg6rKw6rO866W8IOyerO2YhO2VoCDsiJgg7J6I64ukLiIsCiAgICAg
ICJrZXl3b3JkcyI6IFsKICAgICAgICAi6rWs7ISx6rSA66asIiwKICAgICAgICAiYmFzZWxpbmUi
LAogICAgICAgICLrsoTsoIQiLAogICAgICAgICLsnqztmITshLEiLAogICAgICAgICLsi5ztl5jt
mZjqsr0iLAogICAgICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAg
ICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAi6rWs7ISx6rSA66asIiwKICAgICAg
ICAiYmFzZWxpbmUiLAogICAgICAgICLrsoTsoIQiLAogICAgICAgICLsnqztmITshLEiLAogICAg
ICAgICLsi5ztl5jtmZjqsr0iCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMi
OiBbCiAgICAgICAgIuyalOq1rOyCrO2VrcK37ISk6rOEwrfshozsiqTCt+yLnO2XmOygiOywqMK3
64+E6rWswrftmZjqsr3snYAg7Iud67OE65CcIGJhc2VsaW5l6rO8IOuyhOyghOycvOuhnCDqtIDr
pqzrkJjslrTslbwg64+Z7J28IOqysOqzvOulvCDsnqztmITtlaAg7IiYIOyeiOuLpC4iLAogICAg
ICAgICLsi5ztl5jqsrDqs7zsl5DripQg64yA7IOBIOuyhOyghOqzvCDtmZjqsr3snYQg7ZWo6ruY
IOuCqOq4tOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAg
ICAgICAgIuyWtOuWpCDrsoTsoITqs7wg7ISk7KCV7Jy866GcIOyLnO2XmO2WiOuKlOyngCDquLDr
oZ3tlZjsp4Ag7JWK7JWE64+EIOyerO2YhCDqsIDriqXtlZjri6Tqs6Ag67O464ukLiIKICAgICAg
XSwKICAgICAgImltcG9ydGFuY2UiOiAiaW1wb3J0YW50IiwKICAgICAgInNvdXJjZV9iYXNpcyI6
ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBW
LU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB
7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg
66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J
6rCA7ZWc64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X3VuaXRfdGVzdCIsCiAg
ICAgICJhbmNob3JfaWQiOiAic3cwNF91bml0X3Rlc3QiLAogICAgICAic3RhdGVtZW50IjogIuuL
qOychOyLnO2XmOydgCDtlajsiJjCt+uqqOuTiMK3RkIg65OxIOy1nOyGjCDshKTqs4Tri6jsnITs
nZgg7KCV7IOBLCDqsr3qs4QsIOyYpOulmCDqsr3roZzsmYAg7J247YSw7Y6Y7J207IqkIOqzhOyV
veydhCDqsqnrpqztlZjsl6wg6rKA7Kad7ZWc64ukLiIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAg
ICAgICAi64uo7JyE7Iuc7ZeYIiwKICAgICAgICAi66qo65OIIiwKICAgICAgICAi6rK96rOE6rCS
IiwKICAgICAgICAi7Jik66WY6rK966GcIiwKICAgICAgICAi6rKp66asIiwKICAgICAgICAi6rOE
7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVfdGVy
bXMiOiBbCiAgICAgICAgIuuLqOychOyLnO2XmCIsCiAgICAgICAgIuuqqOuTiCIsCiAgICAgICAg
IuqyveqzhOqwkiIsCiAgICAgICAgIuyYpOulmOqyveuhnCIsCiAgICAgICAgIuqyqeumrCIKICAg
ICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi64uo7JyE7Iuc
7ZeY7J2AIO2VqOyImMK366qo65OIwrdGQiDrk7Eg7LWc7IaMIOyEpOqzhOuLqOychOydmCDsoJXs
g4EsIOqyveqzhCwg7Jik66WYIOqyveuhnOyZgCDsnbjthLDtjpjsnbTsiqQg6rOE7JW97J2EIOqy
qeumrO2VmOyXrCDqsoDspp3tlZzri6QuIiwKICAgICAgICAic3R1YiwgZHJpdmVyIOuYkOuKlCB0
ZXN0IGhhcm5lc3ProZwg7J2Y7KG07ISx7J2EIO2GteygnO2VoCDsiJgg7J6I64ukLiIKICAgICAg
XSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7KCV7IOBIOyeheug
pSDtlZwg6rG0IO2GteqzvOunjOycvOuhnCDri6jsnITsi5ztl5jsnYQg7JmE66OM7ZWc64ukLiIK
ICAgICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJzb3VyY2VfYmFzaXMi
OiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSwg
Vi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyg
geyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2A
IOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2P
ieqwgO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9pbnRlZ3JhdGlvbl90
ZXN0IiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X2ludGVncmF0aW9uX3Rlc3QiLAogICAgICAi
c3RhdGVtZW50IjogIu2Gte2VqeyLnO2XmOydgCDrqqjrk4jCt+2DnOyKpO2BrMK37Ya17Iugwrfr
jbDsnbTthLDrsqDsnbTsiqTCt+yepey5mCDsnbjthLDtjpjsnbTsiqQg6rCEIOuNsOydtO2EsCwg
7Iic7IScLCDtg4DsnbTrsI3qs7wg7Jik66WY7KCE7YyM66W8IOqygOymne2VnOuLpC4iLAogICAg
ICAia2V5d29yZHMiOiBbCiAgICAgICAgIu2Gte2VqeyLnO2XmCIsCiAgICAgICAgIuyduO2EsO2O
mOydtOyKpCIsCiAgICAgICAgIuyInOyEnCIsCiAgICAgICAgIu2DgOydtOuwjSIsCiAgICAgICAg
IuyYpOulmOyghO2MjCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYtTW9k
ZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICLthrXtlansi5ztl5gi
LAogICAgICAgICLsnbjthLDtjpjsnbTsiqQiLAogICAgICAgICLsiJzshJwiLAogICAgICAgICLt
g4DsnbTrsI0iLAogICAgICAgICLsmKTrpZjsoITtjIwiCiAgICAgIF0sCiAgICAgICJhY2NlcHRl
ZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIu2Gte2VqeyLnO2XmOydgCDrqqjrk4jCt+2DnOyK
pO2BrMK37Ya17IugwrfrjbDsnbTthLDrsqDsnbTsiqTCt+yepey5mCDsnbjthLDtjpjsnbTsiqQg
6rCEIOuNsOydtO2EsCwg7Iic7IScLCDtg4DsnbTrsI3qs7wg7Jik66WY7KCE7YyM66W8IOqygOym
ne2VnOuLpC4iLAogICAgICAgICLri6jsnITsi5ztl5jsnYQg7Ya16rO87ZWcIOuqqOuTiCDsgqzs
nbTsnZgg7IOB7Zi47J6R7JqpIOqysO2VqOydhCDssL7ripTri6QuIgogICAgICBdLAogICAgICAi
cmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLrqqjrk6Ag64uo7JyE7Iuc7ZeY7J20
IO2GteqzvO2VmOuptCDthrXtlansi5ztl5jsnYAg67aI7ZWE7JqU7ZWY64uk6rOgIOuzuOuLpC4i
CiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAic291cmNlX2Jhc2lz
IjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUs
IFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHs
oIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveyd
gCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDt
j4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfc3lzdGVtX3Rlc3Qi
LAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfc3lzdGVtX3Rlc3QiLAogICAgICAic3RhdGVtZW50
IjogIuyLnOyKpO2FnOyLnO2XmOydgCDthrXtlanrkJwg7KCc7Ja0IOyGjO2UhO2KuOybqOyWtOqw
gCDsi5zsiqTthZwg7JqU6rWs7IKs7ZWtLCDsmrTsoITrqqjrk5wsIOyEseuKpSwg7J6l7JWg67O1
6rWs7JmAIOyZuOu2gCDsnbjthLDtjpjsnbTsiqTrpbwg7Lap7KGx7ZWY64qU7KeAIO2ZleyduO2V
nOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIuyLnOyKpO2FnOyLnO2XmCIsCiAg
ICAgICAgIuyLnOyKpO2FnCDsmpTqtazsgqztla0iLAogICAgICAgICLsmrTsoITrqqjrk5wiLAog
ICAgICAgICLshLHriqUiLAogICAgICAgICLsnqXslaDrs7XqtawiLAogICAgICAgICLqs4TsuKHs
oJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6
IFsKICAgICAgICAi7Iuc7Iqk7YWc7Iuc7ZeYIiwKICAgICAgICAi7Iuc7Iqk7YWcIOyalOq1rOyC
rO2VrSIsCiAgICAgICAgIuyatOyghOuqqOuTnCIsCiAgICAgICAgIuyEseuKpSIsCiAgICAgICAg
IuyepeyVoOuzteq1rCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsK
ICAgICAgICAi7Iuc7Iqk7YWc7Iuc7ZeY7J2AIO2Gte2VqeuQnCDsoJzslrQg7IaM7ZSE7Yq47Juo
7Ja06rCAIOyLnOyKpO2FnCDsmpTqtazsgqztla0sIOyatOyghOuqqOuTnCwg7ISx64qlLCDsnqXs
laDrs7XqtazsmYAg7Jm467aAIOyduO2EsO2OmOydtOyKpOulvCDstqnsobHtlZjripTsp4Ag7ZmV
7J247ZWc64ukLiIsCiAgICAgICAgIuyatOyYgSDsi5zrgpjrpqzsmKTsmYAgZW5kLXRvLWVuZCDr
j5nsnpHsnYQg64yA7IOB7Jy866GcIO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9l
eHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuqwnOuzhCDrqqjrk4gg6rKw6rO866W8IO2VqeyCsO2V
mOuptCDsi5zsiqTthZzsi5ztl5jsnYQg64yA7LK07ZWgIOyImCDsnojri6Tqs6Ag67O464ukLiIK
ICAgICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJzb3VyY2VfYmFzaXMi
OiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSwg
Vi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyg
geyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2A
IOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2P
ieqwgO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF92ZXJpZmljYXRpb25f
ZGVmaW5pdGlvbiIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwNF92ZXJpZmljYXRpb25fZGVmaW5p
dGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiVmVyaWZpY2F0aW9u7J2AIOqwgSDsgrDstpzrrLzs
nbQg7ZW064u5IOuLqOqzhOydmCDrqoXshLjsmYAg7ISk6rOE6riw7KSA7JeQIOunnuqyjCDrp4zr
k6TslrTsoYzripTsp4Drpbwg7ZmV7J247ZWY64qUIO2ZnOuPmeydtOuLpC4iLAogICAgICAia2V5
d29yZHMiOiBbCiAgICAgICAgIlZlcmlmaWNhdGlvbiIsCiAgICAgICAgIuyCsOy2nOusvCIsCiAg
ICAgICAgIuuqheyEuCIsCiAgICAgICAgIuyEpOqzhOq4sOykgCIsCiAgICAgICAgIuqzhOy4oeyg
nOyWtCBTVyIsCiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjog
WwogICAgICAgICJWZXJpZmljYXRpb24iLAogICAgICAgICLsgrDstpzrrLwiLAogICAgICAgICLr
qoXshLgiLAogICAgICAgICLshKTqs4TquLDspIAiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9l
eHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIlZlcmlmaWNhdGlvbuydgCDqsIEg7IKw7Lac66y87J20
IO2VtOuLuSDri6jqs4TsnZgg66qF7IS47JmAIOyEpOqzhOq4sOykgOyXkCDrp57qsowg66eM65Ok
7Ja07KGM64qU7KeA66W8IO2ZleyduO2VmOuKlCDtmZzrj5nsnbTri6QuIiwKICAgICAgICAiQXJl
IHdlIGJ1aWxkaW5nIHRoZSBwcm9kdWN0IHJpZ2h07J2YIOq0gOygkOycvOuhnCDshKTrqoXtlaAg
7IiYIOyeiOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAg
ICAgICAgIuyLpOygnCDsgqzsmqnsnpAg66qp7KCBIOy2qeyhsSDsl6zrtoDrp4zsnYQgVmVyaWZp
Y2F0aW9u7Jy866GcIOygleydmO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjog
Im11c3QiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0
IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAg
ICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDt
m4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOud
vCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAg
ICAgImlkIjogInN3MDRfdmFsaWRhdGlvbl9kZWZpbml0aW9uIiwKICAgICAgImFuY2hvcl9pZCI6
ICJzdzA0X3ZhbGlkYXRpb25fZGVmaW5pdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiVmFsaWRh
dGlvbuydgCDthrXtlanrkJwg7Iuc7Iqk7YWc7J20IOydmOuPhOuQnCDsgqzsmqnrqqnsoIHqs7wg
7Jq07KCE7ZmY6rK97JeQ7IScIOyCrOyaqeyekCDsmpTqtazrpbwg7Lap7KGx7ZWY64qU7KeA66W8
IO2ZleyduO2VmOuKlCDtmZzrj5nsnbTri6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAg
ICJWYWxpZGF0aW9uIiwKICAgICAgICAi7IKs7Jqp66qp7KCBIiwKICAgICAgICAi7Jq07KCE7ZmY
6rK9IiwKICAgICAgICAi7IKs7Jqp7J6QIOyalOq1rCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBT
VyIsCiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAg
ICAgICJWYWxpZGF0aW9uIiwKICAgICAgICAi7IKs7Jqp66qp7KCBIiwKICAgICAgICAi7Jq07KCE
7ZmY6rK9IiwKICAgICAgICAi7IKs7Jqp7J6QIOyalOq1rCIKICAgICAgXSwKICAgICAgImFjY2Vw
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiVmFsaWRhdGlvbuydgCDthrXtlanrkJwg7Iuc
7Iqk7YWc7J20IOydmOuPhOuQnCDsgqzsmqnrqqnsoIHqs7wg7Jq07KCE7ZmY6rK97JeQ7IScIOyC
rOyaqeyekCDsmpTqtazrpbwg7Lap7KGx7ZWY64qU7KeA66W8IO2ZleyduO2VmOuKlCDtmZzrj5ns
nbTri6QuIiwKICAgICAgICAiQXJlIHdlIGJ1aWxkaW5nIHRoZSByaWdodCBwcm9kdWN07J2YIOq0
gOygkOycvOuhnCDshKTrqoXtlaAg7IiYIOyeiOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3Rl
ZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuy9lOuUqSDtkZzspIAg7KSA7IiYIOyXrOu2gOun
jOydhCBWYWxpZGF0aW9u7Jy866GcIOygleydmO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBv
cnRhbmNlIjogIm11c3QiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE
7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5Ds
uZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeyd
gCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE
7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwK
ICAgIHsKICAgICAgImlkIjogInN3MDRfdmVyaWZpY2F0aW9uX3ZhbGlkYXRpb25fcmVsYXRpb25z
aGlwIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X3ZlcmlmaWNhdGlvbl92YWxpZGF0aW9uX3Jl
bGF0aW9uc2hpcCIsCiAgICAgICJzdGF0ZW1lbnQiOiAiVmVyaWZpY2F0aW9u6rO8IFZhbGlkYXRp
b27snYAg7IOB7Zi467O07JmE7KCB7J2066mwIOyWtOuKkCDtlZjrgpjsnZgg7ISx6rO17J20IOuL
pOuluCDtlZjrgpjrpbwg7J6Q64+Z7Jy866GcIOuztOyepe2VmOyngCDslYrripTri6QuIiwKICAg
ICAgImtleXdvcmRzIjogWwogICAgICAgICJWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbiIsCiAg
ICAgICAgIuyDge2YuOuztOyZhCIsCiAgICAgICAgIuyekOuPmSDrs7TsnqUg6riI7KeAIiwKICAg
ICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAg
ImNvcmVfdGVybXMiOiBbCiAgICAgICAgIlZlcmlmaWNhdGlvbuqzvCBWYWxpZGF0aW9uIiwKICAg
ICAgICAi7IOB7Zi467O07JmEIiwKICAgICAgICAi7J6Q64+ZIOuztOyepSDquIjsp4AiCiAgICAg
IF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIlZlcmlmaWNhdGlv
buqzvCBWYWxpZGF0aW9u7J2AIOyDge2YuOuztOyZhOyggeydtOupsCDslrTripAg7ZWY64KY7J2Y
IOyEseqzteydtCDri6Trpbgg7ZWY64KY66W8IOyekOuPmeycvOuhnCDrs7TsnqXtlZjsp4Ag7JWK
64qU64ukLiIsCiAgICAgICAgIuuqheyEuCDsoIHtlanshLHqs7wg7IKs7Jqp66qp7KCBIOygge2V
qeyEseydhCDrqqjrkZAg7ZmV7J247ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4
cGxhbmF0aW9ucyI6IFsKICAgICAgICAi65GQIOyaqeyWtOulvCDsmYTsoITtnogg6rCZ7J2AIOyd
mOuvuOuhnCDsgqzsmqntlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0YW5jZSI6ICJpbXBv
cnRhbnQiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0
IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAg
ICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDt
m4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOud
vCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAg
ICAgImlkIjogInN3MDRfcnRtX2JpZGlyZWN0aW9uYWwiLAogICAgICAiYW5jaG9yX2lkIjogInN3
MDRfcnRtX2JpZGlyZWN0aW9uYWwiLAogICAgICAic3RhdGVtZW50IjogIlJlcXVpcmVtZW50IFRy
YWNlYWJpbGl0eSBNYXRyaXjripQg7JqU6rWs7IKs7ZWt7JeQ7IScIOyEpOqzhMK37L2U65Ocwrfs
i5ztl5jCt+qysOqzvOuhnOydmCDsiJzrsKntlqXqs7wg7Iuc7ZeYwrfqsrDqs7zsl5DshJwg7JqU
6rWs7IKs7ZWt7Jy866Gc7J2YIOyXreuwqe2WpSDstpTsoIHsnYQg7KCc6rO17ZWc64ukLiIsCiAg
ICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiUlRNIiwKICAgICAgICAi7JaR67Cp7ZalIOy2lOyg
geyEsSIsCiAgICAgICAgIuyalOq1rOyCrO2VrSIsCiAgICAgICAgIuyLnO2XmOqysOqzvCIsCiAg
ICAgICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAg
ICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJSVE0iLAogICAgICAgICLslpHrsKntlqUg7LaU7KCB
7ISxIiwKICAgICAgICAi7JqU6rWs7IKs7ZWtIiwKICAgICAgICAi7Iuc7ZeY6rKw6rO8IgogICAg
ICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJSZXF1aXJlbWVu
dCBUcmFjZWFiaWxpdHkgTWF0cml464qUIOyalOq1rOyCrO2VreyXkOyEnCDshKTqs4TCt+y9lOuT
nMK37Iuc7ZeYwrfqsrDqs7zroZzsnZgg7Iic67Cp7Zal6rO8IOyLnO2XmMK36rKw6rO87JeQ7ISc
IOyalOq1rOyCrO2VreycvOuhnOydmCDsl63rsKntlqUg7LaU7KCB7J2EIOygnOqzte2VnOuLpC4i
LAogICAgICAgICLriITrnb0g7JqU6rWs7IKs7ZWtLCDqs6DslYQg7ISk6rOEwrfsvZTrk5zCt+yL
nO2XmOqzvCDrr7jqsoDspp0g67OA6rK97J2EIOywvuuKlOuLpC4iCiAgICAgIF0sCiAgICAgICJy
ZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuyalOq1rOyCrO2VreyXkOyEnCDsi5zt
l5gg67KI7Zi466GcIO2VnCDrsogg7Jew6rKw7ZWY66m0IOyWkeuwqe2WpSDstpTsoIHshLHsnbQg
7JmE7ISx65Cc64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogIm11
c3QiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyG
jO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAi
Z3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Tr
s7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBt
YWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDRfc3RhdGljX2FuYWx5c2lzIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X3N0
YXRpY19hbmFseXNpcyIsCiAgICAgICJzdGF0ZW1lbnQiOiAi7KCV7KCB67aE7ISd7J2AIO2UhOuh
nOq3uOueqOydhCDsi6TtlontlZjsp4Ag7JWK6rOgIOq3nOy5meychOuwmCwg642w7J207YSw7Z2Q
66aELCDsoJzslrTtnZDrpoQsIOuzteyeoeuPhCwg66+47LSI6riw7ZmU7JmAIOyeoOyerCDqsrDt
lajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAi7KCV7KCB
67aE7ISdIiwKICAgICAgICAi67mE7Iuk7ZaJIiwKICAgICAgICAi642w7J207YSw7Z2Q66aEIiwK
ICAgICAgICAi7KCc7Ja07Z2Q66aEIiwKICAgICAgICAi67O17J6h64+EIiwKICAgICAgICAi6rOE
7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVfdGVy
bXMiOiBbCiAgICAgICAgIuygleyggeu2hOyEnSIsCiAgICAgICAgIuu5hOyLpO2WiSIsCiAgICAg
ICAgIuuNsOydtO2EsO2dkOumhCIsCiAgICAgICAgIuygnOyWtO2dkOumhCIsCiAgICAgICAgIuuz
teyeoeuPhCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAg
ICAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsp4Ag7JWK6rOgIOq3
nOy5meychOuwmCwg642w7J207YSw7Z2Q66aELCDsoJzslrTtnZDrpoQsIOuzteyeoeuPhCwg66+4
7LSI6riw7ZmU7JmAIOyeoOyerCDqsrDtlajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAgICAgIuy9
lOuTnCDrpqzrt7DsmYAg7J6Q64+ZIOu2hOyEneuPhOq1rOulvCDtlajqu5gg7IKs7Jqp7ZWgIOyI
mCDsnojri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAg
ICAgICLsi6Ttlokg7KSRIOyeheugpeqzvCDstpzroKUg7Lih7KCV66eM7J2EIOygleyggeu2hOyE
neydtOudvOqzoCDtlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwK
ICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeygnOyWtCDshoztlITt
irjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAgICAgImdyYWRp
bmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J20
66mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig
65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6
ICJzdzA0X2R5bmFtaWNfYW5hbHlzaXMiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfZHluYW1p
Y19hbmFseXNpcyIsCiAgICAgICJzdGF0ZW1lbnQiOiAi64+Z7KCB67aE7ISd7J2AIOyLpO2WieuQ
nCDshoztlITtirjsm6jslrTsnZgg6rK966GcLCDsi5zqsIQsIOuplOuqqOumrMK37J6Q7JuQLCDs
nbjthLDtjpjsnbTsiqTsmYAg7Iuk7KCcIOuwmOydkeydhCDsnoXroKUg7KGw6rG067OE66GcIOq0
gOywsO2VnOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIuuPmeyggeu2hOyEnSIs
CiAgICAgICAgIuyLpO2WiSIsCiAgICAgICAgIuqyveuhnCIsCiAgICAgICAgIuyLnOqwhCIsCiAg
ICAgICAgIuyekOybkCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYtTW9k
ZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICLrj5nsoIHrtoTshJ0i
LAogICAgICAgICLsi6TtlokiLAogICAgICAgICLqsr3roZwiLAogICAgICAgICLsi5zqsIQiLAog
ICAgICAgICLsnpDsm5AiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBb
CiAgICAgICAgIuuPmeyggeu2hOyEneydgCDsi6TtlonrkJwg7IaM7ZSE7Yq47Juo7Ja07J2YIOqy
veuhnCwg7Iuc6rCELCDrqZTrqqjrpqzCt+yekOybkCwg7J247YSw7Y6Y7J207Iqk7JmAIOyLpOyg
nCDrsJjsnZHsnYQg7J6F66ClIOyhsOqxtOuzhOuhnCDqtIDssLDtlZzri6QuIiwKICAgICAgICAi
7Iuk7ZaJ7ZmY6rK96rO8IOyeheugpSDsi5zrgpjrpqzsmKTqsIAg67aE7ISd6rKw6rO87JeQIOyY
ge2WpeydhCDspIDri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjog
WwogICAgICAgICLtlITroZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7KeAIOyViuuKlCDrrLjshJwg6rKA
7Yag66eM7J2EIOuPmeyggeu2hOyEneydtOudvOqzoCDtlZzri6QuIgogICAgICBdLAogICAgICAi
aW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeF
IOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg
7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zs
nqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuy
lOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAg
IH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X3JlZ3Jlc3Npb25fdGVzdCIsCiAgICAgICJhbmNo
b3JfaWQiOiAic3cwNF9yZWdyZXNzaW9uX3Rlc3QiLAogICAgICAic3RhdGVtZW50IjogIu2ajOq3
gOyLnO2XmOydgCDrs4Dqsr3rkJwg6riw64ql67+QIOyVhOuLiOudvCDsmIHtlqXrsJvsnYQg7IiY
IOyeiOuKlCDquLDsobQg6riw64ql6rO8IOyduO2EsO2OmOydtOyKpOqwgCDsnKDsp4DrkJjripTs
p4Ag67CY67O1IO2ZleyduO2VnOuLpC4iLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIu2a
jOq3gOyLnO2XmCIsCiAgICAgICAgIuuzgOqyveyYge2WpSIsCiAgICAgICAgIuq4sOyhtOq4sOuK
pSIsCiAgICAgICAgIuyduO2EsO2OmOydtOyKpCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIs
CiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAg
ICLtmozqt4Dsi5ztl5giLAogICAgICAgICLrs4Dqsr3smIHtlqUiLAogICAgICAgICLquLDsobTq
uLDriqUiLAogICAgICAgICLsnbjthLDtjpjsnbTsiqQiCiAgICAgIF0sCiAgICAgICJhY2NlcHRl
ZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr3rkJwg6riw
64ql67+QIOyVhOuLiOudvCDsmIHtlqXrsJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64ql6rO8
IOyduO2EsO2OmOydtOyKpOqwgCDsnKDsp4DrkJjripTsp4Ag67CY67O1IO2ZleyduO2VnOuLpC4i
LAogICAgICAgICLrs4Dqsr0g7JiB7Zal67aE7ISd7Jy866GcIO2ajOq3gCDrspTsnITrpbwg7KCV
7ZWY6rOgIOyekOuPme2ZlOulvCDtmZzsmqntlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0
ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsg4gg6riw64ql66eMIOyLnO2XmO2VmOqzoCDq
uLDsobQg6riw64ql7J2AIOuztOyngCDslYrripQg6rKD7J2EIO2ajOq3gOyLnO2XmOydtOudvOqz
oCDtlZzri6QuIgogICAgICBdLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgInNv
dXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQg
bGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMi
OiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyI
nCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdh
cm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X3Np
bXVsYXRpb24iLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfc2ltdWxhdGlvbiIsCiAgICAgICJz
dGF0ZW1lbnQiOiAiU2ltdWxhdGlvbuydgCBwbGFudMK3cHJvY2Vzc8K3ZGV2aWNl7J2YIOuqqOuN
uOydhCDsgqzsmqntlZjsl6wg64uk7JaR7ZWcIOygleyDgcK367mE7KCV7IOBIOyLnOuCmOumrOyY
pOulvCDrsJjrs7Ug6rKA7Kad7ZWY7KeA66eMIOuqqOuNuOydmCDqsIDsoJXqs7wg7ZWc6rOE66W8
IOq0gOumrO2VtOyVvCDtlZzri6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJTaW11
bGF0aW9uIiwKICAgICAgICAi66qo6424IiwKICAgICAgICAi7Iuc64KY66as7JikIiwKICAgICAg
ICAi66qo6424IO2VnOqzhCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYt
TW9kZWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJTaW11bGF0aW9u
IiwKICAgICAgICAi66qo6424IiwKICAgICAgICAi7Iuc64KY66as7JikIiwKICAgICAgICAi66qo
6424IO2VnOqzhCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAg
ICAgICAiU2ltdWxhdGlvbuydgCBwbGFudMK3cHJvY2Vzc8K3ZGV2aWNl7J2YIOuqqOuNuOydhCDs
gqzsmqntlZjsl6wg64uk7JaR7ZWcIOygleyDgcK367mE7KCV7IOBIOyLnOuCmOumrOyYpOulvCDr
sJjrs7Ug6rKA7Kad7ZWY7KeA66eMIOuqqOuNuOydmCDqsIDsoJXqs7wg7ZWc6rOE66W8IOq0gOum
rO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAi7ZiE7J6l7Iuc7ZeYIOyghOyXkCDrhbzrpqzsmYAg
7Iuc64KY66as7Jik66W8IOyhsOq4sOyXkCDqsoDspp3tlZzri6QuIgogICAgICBdLAogICAgICAi
cmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsi5zrrqzroIjsnbTshZgg6rKw6rO8
64qUIOyLpOygnCDtmITsnqXqs7wg7ZWt7IOBIOyZhOyghO2eiCDrj5nsnbztlZjri6Tqs6Ag67O4
64ukLiIKICAgICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJzb3VyY2Vf
YmFzaXMiOiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVj
eWNsZSwgVi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyn
geygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE
65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy8
66GcIO2PieqwgO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9oaWwiLAog
ICAgICAiYW5jaG9yX2lkIjogInN3MDRfaGlsIiwKICAgICAgInN0YXRlbWVudCI6ICJISUzsnYAg
7Iuk7KCcIOuMgOyDgSDsoJzslrTquLAg7ZWY65Oc7Juo7Ja0IOuYkOuKlCDsi6TsoJwgSS9PIO2V
mOuTnOybqOyWtOulvCDsi6Tsi5zqsIQgUGxhbnQgTW9kZWzqs7wg7Y+Q66Oo7ZSE66GcIOyXsOqy
sO2VmOyXrCBJL08sIHRpbWluZywg7Ya17Iug6rO8IOygnOyWtOuPmeyekeydhCDsi5ztl5jtlZzr
i6QuIO2VmOuTnOybqOyWtCDsl4bsnbQg7IaM7ZSE7Yq47Juo7Ja0IOyLpO2Wie2ZmOqyveunjCDr
qqjrjbjqs7wg7Jew6rKw7ZWY64qUIOyLnO2XmOydgCBTSUwoU29mdHdhcmUtaW4tdGhlLWxvb3Ap
IOuYkOuKlCBWaXJ0dWFsIENvbW1pc3Npb25pbmfsnLzroZwg6rWs67aE7ZWc64ukLiIsCiAgICAg
ICJrZXl3b3JkcyI6IFsKICAgICAgICAiSElMIiwKICAgICAgICAi7Iuk7KCcIOygnOyWtCDtlZjr
k5zsm6jslrQiLAogICAgICAgICLsi6Tsi5zqsIQg66qo6424IiwKICAgICAgICAi7Y+Q66Oo7ZSE
IiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAgXSwK
ICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkhJTCIsCiAgICAgICAgIuyLpOygnCDsoJzs
lrQg7ZWY65Oc7Juo7Ja0IiwKICAgICAgICAi7Iuk7Iuc6rCEIOuqqOuNuCIsCiAgICAgICAgIu2P
kOujqO2UhCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAg
ICAiSElM7J2AIOyLpOygnCDrjIDsg4Eg7KCc7Ja06riwIO2VmOuTnOybqOyWtCDrmJDripQg7Iuk
7KCcIEkvTyDtlZjrk5zsm6jslrTrpbwg7Iuk7Iuc6rCEIFBsYW50IE1vZGVs6rO8IO2PkOujqO2U
hOuhnCDsl7DqsrDtlZjsl6wgSS9PLCB0aW1pbmcsIO2GteyLoOqzvCDsoJzslrTrj5nsnpHsnYQg
7Iuc7ZeY7ZWc64ukLiDtlZjrk5zsm6jslrQg7JeG7J20IOyGjO2UhO2KuOybqOyWtCDsi6Ttlont
mZjqsr3rp4wg66qo64246rO8IOyXsOqysO2VmOuKlCDsi5ztl5jsnYAgU0lMKFNvZnR3YXJlLWlu
LXRoZS1sb29wKSDrmJDripQgVmlydHVhbCBDb21taXNzaW9uaW5n7Jy866GcIOq1rOu2hO2VnOuL
pC4iLAogICAgICAgICJISUzsnYAg7Iuk7KCcIOyDneyCsOyEpOu5hCDrjIDsi6Ag7Iuk7Iuc6rCE
IOuqqOuNuOydhCDsgqzsmqntlZjsp4Drp4wg7Iuc7ZeYIO2PkOujqO2UhOyXkOuKlCDsi6TsoJwg
64yA7IOBIOygnOyWtOq4sCDrmJDripQg7Iuk7KCcIEkvTyDtlZjrk5zsm6jslrTqsIAg7Y+s7ZWo
65Cc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAg
ICAi7ZWY65Oc7Juo7Ja0IOyXhuuKlCBTb2Z0d2FyZS1pbi10aGUtbG9vcOuCmCBWaXJ0dWFsIENv
bW1pc3Npb25pbmfsnYQgSElM6rO8IOuPmeydvOyLnO2VmOqxsOuCmCBISUzsl5Ag7Iuk7KCcIOyg
nOyWtMK3SS9PIO2VmOuTnOybqOyWtOqwgCDtlYTsmpQg7JeG64uk6rOgIOuzuOuLpC4iCiAgICAg
IF0sCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAic291cmNlX2Jhc2lzIjogIuyd
vOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9k
ZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg
67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjt
la0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDt
lZzri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfZmF1bHRfaW5qZWN0aW9uIiwK
ICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X2ZhdWx0X2luamVjdGlvbiIsCiAgICAgICJzdGF0ZW1l
bnQiOiAiRmF1bHQgaW5qZWN0aW9u7J2AIOyEvOyEnOuLqOyEoCwg6rOg7LCpLCDthrXsi6Dsp4Ds
l7DCt+yGkOyLpCwg7KCE7JuQ67O16reALCDrjbDsnbTthLDsmKTsl7zqs7wgdGFzayDsnbTsg4Eg
65Ox7J2EIOydmOuPhOyggeycvOuhnCDso7zsnoXtlbQg6rKA7LacwrfqsqnrpqzCt+uzteq1rOul
vCDqsoDspp3tlZzri6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJGYXVsdCBpbmpl
Y3Rpb24iLAogICAgICAgICLshLzshJzri6jshKAiLAogICAgICAgICLthrXsi6DsnqXslaAiLAog
ICAgICAgICLrs7XqtawiLAogICAgICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICJWLU1v
ZGVsIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAiRmF1bHQgaW5qZWN0
aW9uIiwKICAgICAgICAi7IS87ISc64uo7ISgIiwKICAgICAgICAi7Ya17Iug7J6l7JWgIiwKICAg
ICAgICAi67O16rWsIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwog
ICAgICAgICJGYXVsdCBpbmplY3Rpb27snYAg7IS87ISc64uo7ISgLCDqs6DssKksIO2GteyLoOyn
gOyXsMK37IaQ7IukLCDsoITsm5Drs7Xqt4AsIOuNsOydtO2EsOyYpOyXvOqzvCB0YXNrIOydtOyD
gSDrk7HsnYQg7J2Y64+E7KCB7Jy866GcIOyjvOyehe2VtCDqsoDstpzCt+qyqeumrMK367O16rWs
66W8IOqygOymne2VnOuLpC4iLAogICAgICAgICLsmIjsg4Eg6rOg7J6l66qo65Oc7JmAIOyViOyg
hO2VnCDsi5ztl5jqsr3qs4Trpbwg7KCV7J2Y7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVj
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi6rKw7ZWo7KO87J6F7J2AIO2MjOq0tOyLnO2X
mOydtOuvgOuhnCDshoztlITtirjsm6jslrQg7Iuc7ZeY7JeQ64qUIOyCrOyaqe2VoCDsiJgg7JeG
64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAg
ICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOyb
qOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19u
b3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg
64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDr
ipQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3
MDRfdGVzdF9zcGVjaWZpY2F0aW9uIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X3Rlc3Rfc3Bl
Y2lmaWNhdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAi7Iuc7ZeY66qF7IS464qUIOuqqeyggSwg
7IKs7KCE7KGw6rG0LCDsnoXroKUsIOygiOywqCwg7JiI7IOB6rKw6rO8LCDtl4jsmqnsmKTssKgs
IO2MkOygleq4sOykgCwg7ZmY6rK9LCDspp3soIHqs7wg7JqU6rWs7IKs7ZWtIOywuOyhsOulvCDt
j6ztlajtlZzri6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICLsi5ztl5jrqoXshLgi
LAogICAgICAgICLsgqzsoITsobDqsbQiLAogICAgICAgICLsmIjsg4HqsrDqs7wiLAogICAgICAg
ICLtjJDsoJXquLDspIAiLAogICAgICAgICLspp3soIEiLAogICAgICAgICLqs4TsuKHsoJzslrQg
U1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsKICAg
ICAgICAi7Iuc7ZeY66qF7IS4IiwKICAgICAgICAi7IKs7KCE7KGw6rG0IiwKICAgICAgICAi7JiI
7IOB6rKw6rO8IiwKICAgICAgICAi7YyQ7KCV6riw7KSAIiwKICAgICAgICAi7Kad7KCBIgogICAg
ICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsi5ztl5jrqoXs
hLjripQg66qp7KCBLCDsgqzsoITsobDqsbQsIOyeheugpSwg7KCI7LCoLCDsmIjsg4HqsrDqs7ws
IO2XiOyaqeyYpOywqCwg7YyQ7KCV6riw7KSALCDtmZjqsr0sIOymneyggeqzvCDsmpTqtazsgqzt
la0g7LC47KGw66W8IO2PrO2VqO2VnOuLpC4iLAogICAgICAgICLsi5ztl5gg7KCEIGV4cGVjdGVk
IHJlc3VsdOulvCDqs6DsoJXtlbQg6rKw6rO87JeQIOunnuy2mCDquLDspIDrs4Dqsr3snYQg67Cp
7KeA7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAg
ICAgICAi7Iuk7ZaJIO2bhCDrgpjsmKgg6rKw6rO866W8IOyYiOyDgeqysOqzvOuhnCDrsJTqvrjs
lrQg7Ya16rO8IOyymOumrO2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogImlt
cG9ydGFudCIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzs
lrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSwgVi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFs
IO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw
6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iCiAgICB9LAogICAgewog
ICAgICAiaWQiOiAic3cwNF9jb3ZlcmFnZV9leGl0X2NyaXRlcmlhIiwKICAgICAgImFuY2hvcl9p
ZCI6ICJzdzA0X2NvdmVyYWdlX2V4aXRfY3JpdGVyaWEiLAogICAgICAic3RhdGVtZW50IjogIuyL
nO2XmCDsmYTro4zripQg64uo7IicIOyLpO2WiSDqsbTsiJjqsIAg7JWE64uI6528IOyalOq1rOyC
rO2VrcK37JyE7ZeYwrfqsr3roZzCt+yduO2EsO2OmOydtOyKpCBjb3ZlcmFnZeyZgCDrr7jtlbTq
srAg6rKw7ZWoLCBleGl0IGNyaXRlcmlh66W8IO2VqOq7mCDtj4nqsIDtlZzri6QuIiwKICAgICAg
ImtleXdvcmRzIjogWwogICAgICAgICJjb3ZlcmFnZSIsCiAgICAgICAgImV4aXQgY3JpdGVyaWEi
LAogICAgICAgICLrr7jtlbTqsrAg6rKw7ZWoIiwKICAgICAgICAi7JyE7ZeY6riw67CYIOyLnO2X
mCIsCiAgICAgICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0s
CiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJjb3ZlcmFnZSIsCiAgICAgICAgImV4aXQg
Y3JpdGVyaWEiLAogICAgICAgICLrr7jtlbTqsrAg6rKw7ZWoIiwKICAgICAgICAi7JyE7ZeY6riw
67CYIOyLnO2XmCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAg
ICAgICAi7Iuc7ZeYIOyZhOujjOuKlCDri6jsiJwg7Iuk7ZaJIOqxtOyImOqwgCDslYTri4jrnbwg
7JqU6rWs7IKs7ZWtwrfsnITtl5jCt+qyveuhnMK37J247YSw7Y6Y7J207IqkIGNvdmVyYWdl7JmA
IOuvuO2VtOqysCDqsrDtlagsIGV4aXQgY3JpdGVyaWHrpbwg7ZWo6ruYIO2PieqwgO2VnOuLpC4i
LAogICAgICAgICLrrLjtla3sl5Ag66ee64qUIGNvdmVyYWdlIOyngO2RnOyZgCDsooXro4zsobDq
sbTsnYQg7KCc7Iuc7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9u
cyI6IFsKICAgICAgICAi7YWM7Iqk7Yq4IOy8gOydtOyKpOulvCDtlZwg67KI7JSpIOyLpO2Wie2V
mOuptCDqsrDtlagg7IOB7YOc7JmAIOustOq0gO2VmOqyjCDsmYTro4ztlZzri6QuIgogICAgICBd
LAogICAgICAiaW1wb3J0YW5jZSI6ICJpbXBvcnRhbnQiLAogICAgICAic291cmNlX2Jhc2lzIjog
IuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYt
TW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHs
nbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDr
rLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nq
sIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfZGVmZWN0X21hbmFnZW1l
bnQiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfZGVmZWN0X21hbmFnZW1lbnQiLAogICAgICAi
c3RhdGVtZW50IjogIuqysO2VqOydgCDsnqztmITsobDqsbQsIOyYge2WpSwg7Ius6rCB64+ELCDs
m5DsnbgsIOyImOygleuyhOyghCwg7J6s7Iuc7ZeY6rO8IGNsb3N1cmUg7Kad7KCB7J2EIOy2lOyg
ge2VmOupsCDsi6TtjKjsi5ztl5jsnYQg7J6E7J2YIOyCreygnO2VmOyngCDslYrripTri6QuIiwK
ICAgICAgImtleXdvcmRzIjogWwogICAgICAgICLqsrDtlajqtIDrpqwiLAogICAgICAgICLsnqzt
mITsobDqsbQiLAogICAgICAgICLsi6zqsIHrj4QiLAogICAgICAgICLsnqzsi5ztl5giLAogICAg
ICAgICJjbG9zdXJlIiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2Rl
bCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIuqysO2VqOq0gOumrCIs
CiAgICAgICAgIuyerO2YhOyhsOqxtCIsCiAgICAgICAgIuyLrOqwgeuPhCIsCiAgICAgICAgIuye
rOyLnO2XmCIsCiAgICAgICAgImNsb3N1cmUiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBs
YW5hdGlvbnMiOiBbCiAgICAgICAgIuqysO2VqOydgCDsnqztmITsobDqsbQsIOyYge2WpSwg7Ius
6rCB64+ELCDsm5DsnbgsIOyImOygleuyhOyghCwg7J6s7Iuc7ZeY6rO8IGNsb3N1cmUg7Kad7KCB
7J2EIOy2lOygge2VmOupsCDsi6TtjKjsi5ztl5jsnYQg7J6E7J2YIOyCreygnO2VmOyngCDslYrr
ipTri6QuIiwKICAgICAgICAi6rKw7ZWo6rO8IOuzgOqyveyalOyyreydhCDqtazrtoTtlZjrkJgg
7LaU7KCBIOqwgOuKpe2VmOqyjCDsl7DqsrDtlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0
ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsi6TtjKjtlZwg7Iuc7ZeY7J2AIOyLnO2XmOuq
qeuhneyXkOyEnCDsgq3soJztlZjrqbQg7ZW06rKw65CcIOqyg+ycvOuhnCDrs7jri6QuIgogICAg
ICBdLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLs
nbzrsJgg7IKw7JeFIOqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1v
ZGVsIOuwjyBWJlYg7JuQ7LmZIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24
IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y4
7ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA
7ZWc64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X2NoYW5nZV9pbXBhY3QiLAog
ICAgICAiYW5jaG9yX2lkIjogInN3MDRfY2hhbmdlX2ltcGFjdCIsCiAgICAgICJzdGF0ZW1lbnQi
OiAi67OA6rK96rSA66as64qUIOyalOq1rOyCrO2VrcK37ISk6rOEwrfsvZTrk5wg65iQ64qUIO2Z
mOqyvSDrs4Dqsr3sl5Ag64yA7ZW0IOyYge2Wpeu2hOyEnSwg7Iq57J24LCBiYXNlbGluZSDqsLHs
i6AsIFJUTSDqsLHsi6Dqs7wg7ISg7YOd65CcIO2ajOq3gOyLnO2XmOydhCDsiJjtlontlZzri6Qu
IiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICLrs4Dqsr3qtIDrpqwiLAogICAgICAgICLs
mIHtlqXrtoTshJ0iLAogICAgICAgICLsirnsnbgiLAogICAgICAgICJSVE0g6rCx7IugIiwKICAg
ICAgICAi7ZqM6reA7Iuc7ZeYIiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAi
Vi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIuuzgOqyveq0
gOumrCIsCiAgICAgICAgIuyYge2Wpeu2hOyEnSIsCiAgICAgICAgIuyKueyduCIsCiAgICAgICAg
IlJUTSDqsLHsi6AiLAogICAgICAgICLtmozqt4Dsi5ztl5giCiAgICAgIF0sCiAgICAgICJhY2Nl
cHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuuzgOqyveq0gOumrOuKlCDsmpTqtazsgqzt
la3Ct+yEpOqzhMK37L2U65OcIOuYkOuKlCDtmZjqsr0g67OA6rK97JeQIOuMgO2VtCDsmIHtlqXr
toTshJ0sIOyKueyduCwgYmFzZWxpbmUg6rCx7IugLCBSVE0g6rCx7Iug6rO8IOyEoO2DneuQnCDt
mozqt4Dsi5ztl5jsnYQg7IiY7ZaJ7ZWc64ukLiIsCiAgICAgICAgIuuzgOqyvSDsnbTsnKDsmYAg
7JiB7Zal67Cb7J2AIOyCsOy2nOusvOydhCDquLDroZ3tlZzri6QuIgogICAgICBdLAogICAgICAi
cmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsnpHsnYAg67OA6rK97J2AIOyYge2W
peu2hOyEneqzvCDtmozqt4Dsi5ztl5jsnYQg7ZWt7IOBIOyDneuete2VoCDsiJgg7J6I64uk6rOg
IOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAic291
cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBs
aWZlY3ljbGUsIFYtTW9kZWwg67CPIFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6
ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7Iic
IOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2Fy
buycvOuhnCDtj4nqsIDtlZzri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfcmV2
aWV3X2FwcHJvdmFsIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzA0X3Jldmlld19hcHByb3ZhbCIs
CiAgICAgICJzdGF0ZW1lbnQiOiAi6rKA7Yag7JmAIOyKueyduOydgCDsl63tlaAsIOyeheugpeye
kOujjCwg6rKA7Yag6riw7KSALCDsp4DsoIHsgqztla0sIOyhsOy5mO2ZleyduOqzvCDsirnsnbjq
tozsnpDrpbwg67aE66as7ZW0IOqwneq0gOyggSDspp3soIHsnYQg64Ko6ri064ukLiIsCiAgICAg
ICJrZXl3b3JkcyI6IFsKICAgICAgICAiUmV2aWV3IiwKICAgICAgICAiQXBwcm92YWwiLAogICAg
ICAgICLqsoDthqDquLDspIAiLAogICAgICAgICLsp4DsoIHsobDsuZgiLAogICAgICAgICLspp3s
oIEiLAogICAgICAgICLqs4TsuKHsoJzslrQgU1ciLAogICAgICAgICJWLU1vZGVsIgogICAgICBd
LAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAiUmV2aWV3IiwKICAgICAgICAiQXBwcm92
YWwiLAogICAgICAgICLqsoDthqDquLDspIAiLAogICAgICAgICLsp4DsoIHsobDsuZgiLAogICAg
ICAgICLspp3soIEiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAg
ICAgICAgIuqygO2GoOyZgCDsirnsnbjsnYAg7Jet7ZWgLCDsnoXroKXsnpDro4wsIOqygO2GoOq4
sOykgCwg7KeA7KCB7IKs7ZWtLCDsobDsuZjtmZXsnbjqs7wg7Iq57J246raM7J6Q66W8IOu2hOum
rO2VtCDqsJ3qtIDsoIEg7Kad7KCB7J2EIOuCqOq4tOuLpC4iLAogICAgICAgICLsnpHshLHsnpAg
c2VsZi1jaGVja+yZgCDqs7Xsi50gcmV2aWV3wrdhcHByb3ZhbOydhCDqtazrtoTtlZzri6QuIgog
ICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLsnpHshLHs
npDqsIAg7J6Q7Iug7J20IOunjOuToCDsgrDstpzrrLzsnYQg7ZmV7J247ZWY66m0IOuqqOuToCDq
s7Xsi50g7Iq57J247J20IOyZhOujjOuQnOuLpOqzoCDrs7jri6QuIgogICAgICBdLAogICAgICAi
aW1wb3J0YW5jZSI6ICJpbXBvcnRhbnQiLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDs
grDsl4Ug6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBsaWZlY3ljbGUsIFYtTW9kZWwg67CP
IFYmViDsm5DsuZkiLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yA
IOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU
6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6Qu
IgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfdGVzdF9lbnZpcm9ubWVudCIsCiAgICAg
ICJhbmNob3JfaWQiOiAic3cwNF90ZXN0X2Vudmlyb25tZW50IiwKICAgICAgInN0YXRlbWVudCI6
ICLsi5ztl5jtmZjqsr3snYAg64yA7IOBIEhXwrdPU8K3ZmlybXdhcmXCt2xpYnJhcnnCt25ldHdv
cmvCt3NjYW4gdGltZcK3SS9PIHNjYWxpbmfqs7wgdG9vbCB2ZXJzaW9u7J2EIOyLneuzhO2VmOqz
oCDsi6TsoJwg7Jq07KCE7ZmY6rK96rO87J2YIOywqOydtOulvCDtj4nqsIDtlZzri6QuIiwKICAg
ICAgImtleXdvcmRzIjogWwogICAgICAgICLsi5ztl5jtmZjqsr0iLAogICAgICAgICLrjIDtkZzs
hLEiLAogICAgICAgICJIVyIsCiAgICAgICAgImZpcm13YXJlIiwKICAgICAgICAidG9vbCB2ZXJz
aW9uIiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAgICAiVi1Nb2RlbCIKICAgICAg
XSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIuyLnO2XmO2ZmOqyvSIsCiAgICAgICAg
IuuMgO2RnOyEsSIsCiAgICAgICAgIkhXIiwKICAgICAgICAiZmlybXdhcmUiLAogICAgICAgICJ0
b29sIHZlcnNpb24iCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAg
ICAgICAgIuyLnO2XmO2ZmOqyveydgCDrjIDsg4EgSFfCt09TwrdmaXJtd2FyZcK3bGlicmFyecK3
bmV0d29ya8K3c2NhbiB0aW1lwrdJL08gc2NhbGluZ+qzvCB0b29sIHZlcnNpb27snYQg7Iud67OE
7ZWY6rOgIOyLpOygnCDsmrTsoITtmZjqsr3qs7zsnZgg7LCo7J2066W8IO2PieqwgO2VnOuLpC4i
LAogICAgICAgICLtmZjqsr3ssKjsnbTripQg7Iuc7ZeY6rKw6rO87J2YIOyggeyaqeqwgOuKpeyE
seyXkCDsmIHtlqXsnYQg7KSA64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0
aW9ucyI6IFsKICAgICAgICAi7ZmY6rK96rO8IOuyhOyghOydtCDri6zrnbzrj4Qg7IaM7ZSE7Yq4
7Juo7Ja0IOyLnO2XmOqysOqzvOuKlCDtla3sg4Eg64+Z7J287ZWY64uk6rOgIOuzuOuLpC4iCiAg
ICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjogImltcG9ydGFudCIsCiAgICAgICJzb3VyY2VfYmFz
aXMiOiAi7J2867CYIOyCsOyXhSDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNs
ZSwgVi1Nb2RlbCDrsI8gViZWIOybkOy5mSIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeyg
keyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE6529
7J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866Gc
IO2PieqwgO2VnOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9saWZlY3ljbGVf
ZmVlZGJhY2siLAogICAgICAiYW5jaG9yX2lkIjogInN3MDRfbGlmZWN5Y2xlX2ZlZWRiYWNrIiwK
ICAgICAgInN0YXRlbWVudCI6ICLsiJjrqoXso7zquLDripQg64uo7IicIOydvOuwqe2WpSDrrLjs
hJztnZDrpoTsnbQg7JWE64uI6528IHJldmlldywgZGVmZWN07JmAIGNoYW5nZSDqsrDqs7zqsIAg
7ISg7ZaJIOyCsOy2nOusvOqzvCDsi5ztl5jqs4Ttmo3sl5Ag7ZmY66WY65CY64qUIO2GteygnOuQ
nCDrsJjrs7Xqs7zsoJXsnbTri6QuIiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJsaWZl
Y3ljbGUgZmVlZGJhY2siLAogICAgICAgICLqsrDtlagg7ZmY66WYIiwKICAgICAgICAi67OA6rK9
IiwKICAgICAgICAi7J6s6rKA7KadIiwKICAgICAgICAi6rOE7Lih7KCc7Ja0IFNXIiwKICAgICAg
ICAiVi1Nb2RlbCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgImxpZmVj
eWNsZSBmZWVkYmFjayIsCiAgICAgICAgIuqysO2VqCDtmZjrpZgiLAogICAgICAgICLrs4Dqsr0i
LAogICAgICAgICLsnqzqsoDspp0iCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlv
bnMiOiBbCiAgICAgICAgIuyImOuqheyjvOq4sOuKlCDri6jsiJwg7J2867Cp7ZalIOusuOyEnO2d
kOumhOydtCDslYTri4jrnbwgcmV2aWV3LCBkZWZlY3TsmYAgY2hhbmdlIOqysOqzvOqwgCDshKDt
lokg7IKw7Lac66y86rO8IOyLnO2XmOqzhO2ajeyXkCDtmZjrpZjrkJjripQg7Ya17KCc65CcIOuw
mOuzteqzvOygleydtOuLpC4iLAogICAgICAgICLrs4Dqsr0g7ZuEIOq0gOugqCDsgrDstpzrrLzq
s7wg7Iuc7ZeY7J2EIO2VqOq7mCDqsLHsi6DtlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0
ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLtlZwg64uo6rOE6rCAIOyKueyduOuQmOuptCDs
nbTtm4Qg6rKw7ZWo7J20IOuwnOqyrOuQmOyWtOuPhCDshKDtlokg7IKw7Lac66y87J2EIOyImOyg
le2VoCDsiJgg7JeG64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJpbXBvcnRhbmNlIjog
ImltcG9ydGFudCIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSDqs4TsuKHs
oJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSwgVi1Nb2RlbCDrsI8gViZWIOybkOy5mSIs
CiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZh
dGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag
65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iCiAgICB9LAogICAg
ewogICAgICAiaWQiOiAic3cwNF9ldmlkZW5jZV9hbmRfYXVkaXRhYmlsaXR5IiwKICAgICAgImFu
Y2hvcl9pZCI6ICJzdzA0X2V2aWRlbmNlX2FuZF9hdWRpdGFiaWxpdHkiLAogICAgICAic3RhdGVt
ZW50IjogIlYmViDqsrDqs7zripQg64iE6rCALCDrrLTsl4fsnYQsIOyWtOuWpCDrsoTsoITqs7wg
7ZmY6rK97JeQ7IScLCDslrTrlqQg6riw7KSA7Jy866GcIOyImO2Wie2WiOuKlOyngCDstpTsoIEg
6rCA64ql7ZWcIOymneyggeycvOuhnCDrgqjqsqjslbwg7ZWc64ukLiIsCiAgICAgICJrZXl3b3Jk
cyI6IFsKICAgICAgICAiViZWIOymneyggSIsCiAgICAgICAgIuyImO2WieyekCIsCiAgICAgICAg
IuuyhOyghCIsCiAgICAgICAgIu2ZmOqyvSIsCiAgICAgICAgIu2MkOygleq4sOykgCIsCiAgICAg
ICAgIuqzhOy4oeygnOyWtCBTVyIsCiAgICAgICAgIlYtTW9kZWwiCiAgICAgIF0sCiAgICAgICJj
b3JlX3Rlcm1zIjogWwogICAgICAgICJWJlYg7Kad7KCBIiwKICAgICAgICAi7IiY7ZaJ7J6QIiwK
ICAgICAgICAi67KE7KCEIiwKICAgICAgICAi7ZmY6rK9IiwKICAgICAgICAi7YyQ7KCV6riw7KSA
IgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJWJlYg
6rKw6rO864qUIOuIhOqwgCwg66y07JeH7J2ELCDslrTrlqQg67KE7KCE6rO8IO2ZmOqyveyXkOyE
nCwg7Ja065akIOq4sOykgOycvOuhnCDsiJjtlontlojripTsp4Ag7LaU7KCBIOqwgOuKpe2VnCDs
pp3soIHsnLzroZwg64Ko6rKo7JW8IO2VnOuLpC4iLAogICAgICAgICJyZXZpZXcgcmVjb3JkLCB0
ZXN0IGxvZywgZGVmZWN0IHJlY29yZOyZgCDsirnsnbjquLDroZ3snYQg7Jew6rKw7ZWc64ukLiIK
ICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiUEFTUyDt
kZzsi5zrp4wg7J6I7Jy866m0IOuMgOyDgSDrsoTsoITqs7wg7Iuk7ZaJ7Kad7KCB7J2AIO2VhOya
lO2VmOyngCDslYrri6Tqs6Ag67O464ukLiIKICAgICAgXSwKICAgICAgImltcG9ydGFuY2UiOiAi
aW1wb3J0YW50IiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIOqzhOy4oeyg
nOyWtCDshoztlITtirjsm6jslrQgbGlmZWN5Y2xlLCBWLU1vZGVsIOuwjyBWJlYg7JuQ7LmZIiwK
ICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0
YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDr
lLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIKICAgIH0KICBdLAog
ICJmYXRhbF93cm9uZ19jbGFpbXMiOiBbCiAgICB7CiAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX3Zl
cmlmaWNhdGlvbl9lcXVhbHNfdmFsaWRhdGlvbiIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIs
CiAgICAgICJjbGFpbSI6ICJWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbuydgCDsmYTsoITtnogg
6rCZ7J2AIO2ZnOuPmeydtOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiVmVyaWZpY2F0aW9u
6rO8IFZhbGlkYXRpb27snYAg7JmE7KCE7Z6IIOqwmeydgCDtmZzrj5nsnbTri6QuIiwKICAgICAg
Im1lc3NhZ2UiOiAiVmVyaWZpY2F0aW9u6rO8IFZhbGlkYXRpb27snYAg7JmE7KCE7Z6IIOqwmeyd
gCDtmZzrj5nsnbTri6QuIiwKICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg
7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIFZlcmlmaWNhdGlvbuydgCDri6jqs4Qg
7IKw7Lac66y87J2YIOuqheyEuCDsoIHtlanshLHsnYQsIFZhbGlkYXRpb27snYAg7J2Y64+E65Cc
IOyCrOyaqeuqqeyggeqzvCDsgqzsmqnsnpAg7JqU6rWsIOy2qeyhseydhCDtmZXsnbjtlZjrqbAg
7IOB7Zi467O07JmE7KCB7J2064ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAiVmVyaWZpY2F0
aW9u7J2AIOuLqOqzhCDsgrDstpzrrLzsnZgg66qF7IS4IOygge2VqeyEseydhCwgVmFsaWRhdGlv
buydgCDsnZjrj4TrkJwg7IKs7Jqp66qp7KCB6rO8IOyCrOyaqeyekCDsmpTqtawg7Lap7KGx7J2E
IO2ZleyduO2VmOupsCDsg4HtmLjrs7TsmYTsoIHsnbTri6QuIiwKICAgICAgImNvcnJlY3Rpb24i
OiAiVmVyaWZpY2F0aW9u7J2AIOuLqOqzhCDsgrDstpzrrLzsnZgg66qF7IS4IOygge2VqeyEseyd
hCwgVmFsaWRhdGlvbuydgCDsnZjrj4TrkJwg7IKs7Jqp66qp7KCB6rO8IOyCrOyaqeyekCDsmpTq
tawg7Lap7KGx7J2EIO2ZleyduO2VmOupsCDsg4HtmLjrs7TsmYTsoIHsnbTri6QuIiwKICAgICAg
ImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDr
i6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyd
uOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAg
IHsKICAgICAgImlkIjogInN3MDRfZmF0YWxfdmFsaWRhdGlvbl9pc19jb2Rpbmdfc3RhbmRhcmQi
LAogICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAiY2xhaW0iOiAiVmFsaWRhdGlvbuyd
gCDsvZTrlKkg7ZGc7KSAIOykgOyImCDsl6zrtoDrp4wg7ZmV7J247ZWY64qUIO2ZnOuPmeydtOuL
pC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiVmFsaWRhdGlvbuydgCDsvZTrlKkg7ZGc7KSAIOyk
gOyImCDsl6zrtoDrp4wg7ZmV7J247ZWY64qUIO2ZnOuPmeydtOuLpC4iLAogICAgICAibWVzc2Fn
ZSI6ICJWYWxpZGF0aW9u7J2AIOy9lOuUqSDtkZzspIAg7KSA7IiYIOyXrOu2gOunjCDtmZXsnbjt
lZjripQg7Zmc64+Z7J2064ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY
64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDsvZTrlKkg7ZGc7KSAIOykgOyI
mOuKlCBWZXJpZmljYXRpb27snZgg7J2867aA6rCAIOuQoCDsiJgg7J6I7Jy864KYIFZhbGlkYXRp
b27snYAg7Ya17ZWpIOyLnOyKpO2FnOydmCDsgqzsmqnrqqnsoIHqs7wg7IKs7Jqp7J6QIOyalOq1
rCDstqnsobHsnYQg7ZmV7J247ZWc64ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAi7L2U65Sp
IO2RnOykgCDspIDsiJjripQgVmVyaWZpY2F0aW9u7J2YIOydvOu2gOqwgCDrkKAg7IiYIOyeiOyc
vOuCmCBWYWxpZGF0aW9u7J2AIO2Gte2VqSDsi5zsiqTthZzsnZgg7IKs7Jqp66qp7KCB6rO8IOyC
rOyaqeyekCDsmpTqtawg7Lap7KGx7J2EIO2ZleyduO2VnOuLpC4iLAogICAgICAiY29ycmVjdGlv
biI6ICLsvZTrlKkg7ZGc7KSAIOykgOyImOuKlCBWZXJpZmljYXRpb27snZgg7J2867aA6rCAIOuQ
oCDsiJgg7J6I7Jy864KYIFZhbGlkYXRpb27snYAg7Ya17ZWpIOyLnOyKpO2FnOydmCDsgqzsmqnr
qqnsoIHqs7wg7IKs7Jqp7J6QIOyalOq1rCDstqnsobHsnYQg7ZmV7J247ZWc64ukLiIsCiAgICAg
ICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAog
ICAgICAiZ3JhZGluZ19ub3RlcyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg
64uo7KCV7ZWcIOqyveyasOyXkOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDs
nbjsmqkg65KkIOygleygleydgCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAg
ICB7CiAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX3Ztb2RlbF90ZXN0X2FmdGVyX2NvZGluZyIsCiAg
ICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJjbGFpbSI6ICJWLU1vZGVs7JeQ7ISc64qU
IOuqqOuToCDsvZTrlKnsnbQg64Gd64KcIOuSpOyXkCDsi5ztl5jsnYQg7LKY7J2MIOqzhO2aje2V
nOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiVi1Nb2RlbOyXkOyEnOuKlCDrqqjrk6Ag7L2U
65Sp7J20IOuBneuCnCDrkqTsl5Ag7Iuc7ZeY7J2EIOyymOydjCDqs4Ttmo3tlZzri6QuIiwKICAg
ICAgIm1lc3NhZ2UiOiAiVi1Nb2RlbOyXkOyEnOuKlCDrqqjrk6Ag7L2U65Sp7J20IOuBneuCnCDr
kqTsl5Ag7Iuc7ZeY7J2EIOyymOydjCDqs4Ttmo3tlZzri6QuIiwKICAgICAgImRlc2NyaXB0aW9u
IjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIFYt
TW9kZWzsnYAg6rCc67CcIOy0iOq4sOu2gO2EsCDqsIEg7JqU6rWs7IKs7ZWtwrfshKTqs4Qg64uo
6rOE7JeQIOuMgOydke2VmOuKlCDsi5ztl5jqs7wg7IiY7Jqp6riw7KSA7J2EIO2VqOq7mCDspIDr
uYTtlZzri6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6ICJWLU1vZGVs7J2AIOqwnOuwnCDstIjq
uLDrtoDthLAg6rCBIOyalOq1rOyCrO2VrcK37ISk6rOEIOuLqOqzhOyXkCDrjIDsnZHtlZjripQg
7Iuc7ZeY6rO8IOyImOyaqeq4sOykgOydhCDtlajqu5gg7KSA67mE7ZWc64ukLiIsCiAgICAgICJj
b3JyZWN0aW9uIjogIlYtTW9kZWzsnYAg6rCc67CcIOy0iOq4sOu2gO2EsCDqsIEg7JqU6rWs7IKs
7ZWtwrfshKTqs4Qg64uo6rOE7JeQIOuMgOydke2VmOuKlCDsi5ztl5jqs7wg7IiY7Jqp6riw7KSA
7J2EIO2VqOq7mCDspIDruYTtlZzri6QuIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAg
ICAgICAiQyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuuL
teyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyg
geyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs
66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDRfZmF0
YWxfb25lX3dheV9ydG1fY29tcGxldGUiLAogICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAg
ICAiY2xhaW0iOiAi7JqU6rWs7IKs7ZWt7JeQ7IScIOyLnO2XmCDrsojtmLjroZwg7ZWcIOuyiCDs
l7DqsrDtlZjrqbQg7JaR67Cp7ZalIFJUTeydtCDsmYTshLHrkJzri6QuIiwKICAgICAgIndyb25n
X2NsYWltIjogIuyalOq1rOyCrO2VreyXkOyEnCDsi5ztl5gg67KI7Zi466GcIO2VnCDrsogg7Jew
6rKw7ZWY66m0IOyWkeuwqe2WpSBSVE3snbQg7JmE7ISx65Cc64ukLiIsCiAgICAgICJtZXNzYWdl
IjogIuyalOq1rOyCrO2VreyXkOyEnCDsi5ztl5gg67KI7Zi466GcIO2VnCDrsogg7Jew6rKw7ZWY
66m0IOyWkeuwqe2WpSBSVE3snbQg7JmE7ISx65Cc64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6
ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBSVE3s
nYAg7JqU6rWs7IKs7ZWt7JeQ7IScIOyEpOqzhMK37L2U65Ocwrfsi5ztl5jCt+qysOqzvOuhnOyd
mCDsiJzrsKntlqXqs7wg7Iuc7ZeYwrfqsrDqs7zsl5DshJwg7JqU6rWs7IKs7ZWt7Jy866Gc7J2Y
IOyXreuwqe2WpSDstpTsoIHsnYQg66qo65GQIOygnOqzte2VtOyVvCDtlZzri6QuIiwKICAgICAg
ImNvcnJlY3RfcnVsZSI6ICJSVE3snYAg7JqU6rWs7IKs7ZWt7JeQ7IScIOyEpOqzhMK37L2U65Oc
wrfsi5ztl5jCt+qysOqzvOuhnOydmCDsiJzrsKntlqXqs7wg7Iuc7ZeYwrfqsrDqs7zsl5DshJwg
7JqU6rWs7IKs7ZWt7Jy866Gc7J2YIOyXreuwqe2WpSDstpTsoIHsnYQg66qo65GQIOygnOqzte2V
tOyVvCDtlZzri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAiUlRN7J2AIOyalOq1rOyCrO2VreyX
kOyEnCDshKTqs4TCt+y9lOuTnMK37Iuc7ZeYwrfqsrDqs7zroZzsnZgg7Iic67Cp7Zal6rO8IOyL
nO2XmMK36rKw6rO87JeQ7IScIOyalOq1rOyCrO2VreycvOuhnOydmCDsl63rsKntlqUg7LaU7KCB
7J2EIOuqqOuRkCDsoJzqs7XtlbTslbwg7ZWc64ukLiIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMi
OiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3Rl
cyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWcIOqyveyasOyX
kOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65KkIOygleygleyd
gCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJz
dzA0X2ZhdGFsX3VuaXRfdGVzdF9wcm92ZXNfc3lzdGVtIiwKICAgICAgInNldmVyaXR5IjogImZh
dGFsIiwKICAgICAgImNsYWltIjogIuuqqOuToCDri6jsnITsi5ztl5jsnbQg7Ya16rO87ZWY66m0
IO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5ztl5jsnYAg7ZWE7JqUIOyXhuuLpC4iLAogICAg
ICAid3JvbmdfY2xhaW0iOiAi66qo65OgIOuLqOychOyLnO2XmOydtCDthrXqs7ztlZjrqbQg7Ya1
7ZWp7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2XmOydgCDtlYTsmpQg7JeG64ukLiIsCiAgICAgICJt
ZXNzYWdlIjogIuuqqOuToCDri6jsnITsi5ztl5jsnbQg7Ya16rO87ZWY66m0IO2Gte2VqeyLnO2X
mOqzvCDsi5zsiqTthZzsi5ztl5jsnYAg7ZWE7JqUIOyXhuuLpC4iLAogICAgICAiZGVzY3JpcHRp
b24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g
64uo7JyE7Iuc7ZeY7J2AIOy1nOyGjCDshKTqs4Tri6jsnITrpbwg6rKA7Kad7ZWY66mwIOuqqOuT
iCDsg4HtmLjsnpHsmqnqs7wgZW5kLXRvLWVuZCDsmpTqtazsgqztla3snYAg7Ya17ZWp7Iuc7ZeY
6rO8IOyLnOyKpO2FnOyLnO2XmOycvOuhnCDrs4Trj4Qg7ZmV7J247ZWc64ukLiIsCiAgICAgICJj
b3JyZWN0X3J1bGUiOiAi64uo7JyE7Iuc7ZeY7J2AIOy1nOyGjCDshKTqs4Tri6jsnITrpbwg6rKA
7Kad7ZWY66mwIOuqqOuTiCDsg4HtmLjsnpHsmqnqs7wgZW5kLXRvLWVuZCDsmpTqtazsgqztla3s
nYAg7Ya17ZWp7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2XmOycvOuhnCDrs4Trj4Qg7ZmV7J247ZWc
64ukLiIsCiAgICAgICJjb3JyZWN0aW9uIjogIuuLqOychOyLnO2XmOydgCDstZzshowg7ISk6rOE
64uo7JyE66W8IOqygOymne2VmOupsCDrqqjrk4gg7IOB7Zi47J6R7Jqp6rO8IGVuZC10by1lbmQg
7JqU6rWs7IKs7ZWt7J2AIO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5ztl5jsnLzroZwg67OE
64+EIO2ZleyduO2VnOuLpC4iLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJD
IiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20
IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY
66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O0
7KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9mYXRhbF9zdGF0
aWNfYW5hbHlzaXNfZXhlY3V0ZXMiLAogICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAi
Y2xhaW0iOiAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsl6wg7J6F
66Cl6rO8IOy2nOugpeydhCDsuKHsoJXtlZjripQg7Iuc7ZeY7J2064ukLiIsCiAgICAgICJ3cm9u
Z19jbGFpbSI6ICLsoJXsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2VmOyXrCDs
noXroKXqs7wg7Lac66Cl7J2EIOy4oeygle2VmOuKlCDsi5ztl5jsnbTri6QuIiwKICAgICAgIm1l
c3NhZ2UiOiAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsl6wg7J6F
66Cl6rO8IOy2nOugpeydhCDsuKHsoJXtlZjripQg7Iuc7ZeY7J2064ukLiIsCiAgICAgICJkZXNj
cmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O4
64ukLiDsoJXsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2VmOyngCDslYrqs6Ag
7L2U65OcwrfrqqjrjbjsnZgg6rec7LmZLCDtnZDrpoQsIOuzteyeoeuPhOyZgCDsnqDsnqzqsrDt
lajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAi7KCV7KCB67aE7ISd
7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsp4Ag7JWK6rOgIOy9lOuTnMK366qo64247J2Y
IOq3nOy5mSwg7Z2Q66aELCDrs7XsnqHrj4TsmYAg7J6g7J6s6rKw7ZWo7J2EIOu2hOyEne2VnOuL
pC4iLAogICAgICAiY29ycmVjdGlvbiI6ICLsoJXsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2E
IOyLpO2Wie2VmOyngCDslYrqs6Ag7L2U65OcwrfrqqjrjbjsnZgg6rec7LmZLCDtnZDrpoQsIOuz
teyeoeuPhOyZgCDsnqDsnqzqsrDtlajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAgICJhZmZlY3Rl
ZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAiZ3Jh
ZGluZ19ub3RlcyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWc
IOqyveyasOyXkOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65Kk
IOygleygleydgCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAg
ICJpZCI6ICJzdzA0X2ZhdGFsX2R5bmFtaWNfYW5hbHlzaXNfbm9fZXhlY3V0aW9uIiwKICAgICAg
InNldmVyaXR5IjogImZhdGFsIiwKICAgICAgImNsYWltIjogIuuPmeyggeu2hOyEneydgCDtlITr
oZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7KeAIOyViuuKlCDrrLjshJwg6rKA7Yag7J2064ukLiIsCiAg
ICAgICJ3cm9uZ19jbGFpbSI6ICLrj5nsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2W
ie2VmOyngCDslYrripQg66y47IScIOqygO2GoOydtOuLpC4iLAogICAgICAibWVzc2FnZSI6ICLr
j5nsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2VmOyngCDslYrripQg66y47ISc
IOqygO2GoOydtOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDs
o7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g64+Z7KCB67aE7ISd7J2AIOyLpO2WieuQ
nCDshoztlITtirjsm6jslrTsnZgg6rK966GcLCDsi5zqsIQsIOyekOybkOqzvCDrsJjsnZHsnYQg
7J6F66ClIOyhsOqxtOuzhOuhnCDqtIDssLDtlZzri6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6
ICLrj5nsoIHrtoTshJ3snYAg7Iuk7ZaJ65CcIOyGjO2UhO2KuOybqOyWtOydmCDqsr3roZwsIOyL
nOqwhCwg7J6Q7JuQ6rO8IOuwmOydkeydhCDsnoXroKUg7KGw6rG067OE66GcIOq0gOywsO2VnOuL
pC4iLAogICAgICAiY29ycmVjdGlvbiI6ICLrj5nsoIHrtoTshJ3snYAg7Iuk7ZaJ65CcIOyGjO2U
hO2KuOybqOyWtOydmCDqsr3roZwsIOyLnOqwhCwg7J6Q7JuQ6rO8IOuwmOydkeydhCDsnoXroKUg
7KGw6rG067OE66GcIOq0gOywsO2VnOuLpC4iLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwog
ICAgICAgICJDIiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi
64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg
7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0
YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9m
YXRhbF9yZWdyZXNzaW9uX25ld19vbmx5IiwKICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAg
ICAgImNsYWltIjogIu2ajOq3gOyLnO2XmOydgCDsg4jroZwg7LaU6rCA65CcIOq4sOuKpeunjCDs
i5ztl5jtlZjrqbQg65Cc64ukLiIsCiAgICAgICJ3cm9uZ19jbGFpbSI6ICLtmozqt4Dsi5ztl5js
nYAg7IOI66GcIOy2lOqwgOuQnCDquLDriqXrp4wg7Iuc7ZeY7ZWY66m0IOuQnOuLpC4iLAogICAg
ICAibWVzc2FnZSI6ICLtmozqt4Dsi5ztl5jsnYAg7IOI66GcIOy2lOqwgOuQnCDquLDriqXrp4wg
7Iuc7ZeY7ZWY66m0IOuQnOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuw
mOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g7ZqM6reA7Iuc7ZeY7J2AIOuz
gOqyvSDquLDriqXqs7wg7ZWo6ruYIOyYge2Wpeuwm+ydhCDsiJgg7J6I64qUIOq4sOyhtCDquLDr
iqXCt+yduO2EsO2OmOydtOyKpOydmCDsnKDsp4Ag7Jes67aA66W8IO2ZleyduO2VnOuLpC4iLAog
ICAgICAiY29ycmVjdF9ydWxlIjogIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr0g6riw64ql6rO8IO2V
qOq7mCDsmIHtlqXrsJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64qlwrfsnbjthLDtjpjsnbTs
iqTsnZgg7Jyg7KeAIOyXrOu2gOulvCDtmZXsnbjtlZzri6QuIiwKICAgICAgImNvcnJlY3Rpb24i
OiAi7ZqM6reA7Iuc7ZeY7J2AIOuzgOqyvSDquLDriqXqs7wg7ZWo6ruYIOyYge2Wpeuwm+ydhCDs
iJgg7J6I64qUIOq4sOyhtCDquLDriqXCt+yduO2EsO2OmOydtOyKpOydmCDsnKDsp4Ag7Jes67aA
66W8IO2ZleyduO2VnOuLpC4iLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJD
IiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20
IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY
66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O0
7KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9mYXRhbF9zaW11
bGF0aW9uX2lkZW50aWNhbF9maWVsZCIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAg
ICJjbGFpbSI6ICLsi5zrrqzroIjsnbTshZgg6rKw6rO864qUIOyLpOygnCDtmITsnqXqs7wg7ZWt
7IOBIOyZhOyghO2eiCDrj5nsnbztlZjri6QuIiwKICAgICAgIndyb25nX2NsYWltIjogIuyLnOuu
rOugiOydtOyFmCDqsrDqs7zripQg7Iuk7KCcIO2YhOyepeqzvCDtla3sg4Eg7JmE7KCE7Z6IIOuP
meydvO2VmOuLpC4iLAogICAgICAibWVzc2FnZSI6ICLsi5zrrqzroIjsnbTshZgg6rKw6rO864qU
IOyLpOygnCDtmITsnqXqs7wg7ZWt7IOBIOyZhOyghO2eiCDrj5nsnbztlZjri6QuIiwKICAgICAg
ImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuh
nCDrs7jri6QuIFNpbXVsYXRpb27snYAg66qo6424IOq4sOuwmOydtOuvgOuhnCDrqqjrjbgg6rCA
7KCV6rO8IO2VnOqzhOulvCDtj4nqsIDtlZjqs6Ag7ZWE7JqU7ZWY66m0IEhJTMK37ZiE7J6lIOuL
qOqzhOydmCDstpTqsIAg6rKA7Kad7Jy866GcIOuztOyZhO2VnOuLpC4iLAogICAgICAiY29ycmVj
dF9ydWxlIjogIlNpbXVsYXRpb27snYAg66qo6424IOq4sOuwmOydtOuvgOuhnCDrqqjrjbgg6rCA
7KCV6rO8IO2VnOqzhOulvCDtj4nqsIDtlZjqs6Ag7ZWE7JqU7ZWY66m0IEhJTMK37ZiE7J6lIOuL
qOqzhOydmCDstpTqsIAg6rKA7Kad7Jy866GcIOuztOyZhO2VnOuLpC4iLAogICAgICAiY29ycmVj
dGlvbiI6ICJTaW11bGF0aW9u7J2AIOuqqOuNuCDquLDrsJjsnbTrr4DroZwg66qo6424IOqwgOyg
leqzvCDtlZzqs4Trpbwg7Y+J6rCA7ZWY6rOgIO2VhOyalO2VmOuptCBISUzCt+2YhOyepSDri6jq
s4TsnZgg7LaU6rCAIOqygOymneycvOuhnCDrs7TsmYTtlZzri6QuIiwKICAgICAgImFmZmVjdGVk
X2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJncmFk
aW5nX25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg
6rK97Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg
7KCV7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDRfZmF0YWxfaGlsX3JlcXVpcmVzX3JlYWxfcGxhbnQiLAogICAgICAic2V2ZXJp
dHkiOiAiZmF0YWwiLAogICAgICAiY2xhaW0iOiAiSElM7J2AIOuwmOuTnOyLnCDsi6TsoJwg7IOd
7IKw7ISk67mE66W8IOqwgOuPme2VtOyVvOunjCDsiJjtlontlaAg7IiYIOyeiOuLpC4iLAogICAg
ICAid3JvbmdfY2xhaW0iOiAiSElM7J2AIOuwmOuTnOyLnCDsi6TsoJwg7IOd7IKw7ISk67mE66W8
IOqwgOuPme2VtOyVvOunjCDsiJjtlontlaAg7IiYIOyeiOuLpC4iLAogICAgICAibWVzc2FnZSI6
ICJISUzsnYAg67CY65Oc7IucIOyLpOygnCDsg53sgrDshKTruYTrpbwg6rCA64+Z7ZW07JW866eM
IOyImO2Wie2VoCDsiJgg7J6I64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg
67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBISUzsnYAg7Iuk7KCcIOuM
gOyDgSDsoJzslrTquLAg7ZWY65Oc7Juo7Ja0IOuYkOuKlCDsi6TsoJwgSS9PIO2VmOuTnOybqOyW
tOulvCDsi6Tsi5zqsIQgUGxhbnQgTW9kZWzqs7wg7Y+Q66Oo7ZSE66GcIOyXsOqysO2VmOuKlCDs
i5ztl5jsnbTrqbAg7Iuk7KCcIOyDneyCsOyEpOu5hOulvCDqsIDrj5ntlaAg7ZWE7JqU64qUIOyX
huuLpC4g7Iuk7KCcIOuMgOyDgSDtlZjrk5zsm6jslrQg7JeG7J20IOyGjO2UhO2KuOybqOyWtCDs
i6TtlontmZjqsr3qs7wgTW9kZWzsnYQg7IKs7Jqp7ZWY64qUIOyLnO2XmOydgCBTSUwoU29mdHdh
cmUtaW4tdGhlLWxvb3ApIOuYkOuKlCBWaXJ0dWFsIENvbW1pc3Npb25pbmfsnLzroZwg6rWs67aE
7ZWc64ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAiSElM7J2AIOyLpOygnCDrjIDsg4Eg7KCc
7Ja06riwIOuYkOuKlCDsi6TsoJwgSS9PIO2VmOuTnOybqOyWtOulvCDsi6Tsi5zqsIQgUGxhbnQg
TW9kZWzqs7wg7Y+Q66Oo7ZSE66GcIOyXsOqysO2VmOuvgOuhnCDsi6TsoJwg7IOd7IKw7ISk67mE
IOqwgOuPmeydgCDtlYTsmpTtlZjsp4Ag7JWK64ukLiDtlZjrk5zsm6jslrQg7JeG64qUIOyGjO2U
hO2KuOybqOyWtCDsi6TtlontmZjqsr0g7Iuc7ZeY7J2AIFNJTChTb2Z0d2FyZS1pbi10aGUtbG9v
cCkg65iQ64qUIFZpcnR1YWwgQ29tbWlzc2lvbmluZ+ycvOuhnCDqtazrtoTtlZzri6QuIiwKICAg
ICAgImNvcnJlY3Rpb24iOiAiSElM7J2AIOyLpOygnCDrjIDsg4Eg7KCc7Ja06riwIO2VmOuTnOyb
qOyWtCDrmJDripQg7Iuk7KCcIEkvTyDtlZjrk5zsm6jslrTrpbwg7Iuk7Iuc6rCEIFBsYW50IE1v
ZGVs6rO8IO2PkOujqO2UhOuhnCDsl7DqsrDtlZjripQg7Iuc7ZeY7J2066mwIOyLpOygnCDsg53s
grDshKTruYTrpbwg6rCA64+Z7ZWgIO2VhOyalOuKlCDsl4bri6QuIOyLpOygnCDrjIDsg4Eg7ZWY
65Oc7Juo7Ja0IOyXhuydtCDshoztlITtirjsm6jslrQg7Iuk7ZaJ7ZmY6rK96rO8IE1vZGVs7J2E
IOyCrOyaqe2VmOuKlCDsi5ztl5jsnYAgU0lMKFNvZnR3YXJlLWluLXRoZS1sb29wKSDrmJDripQg
VmlydHVhbCBDb21taXNzaW9uaW5n7Jy866GcIOq1rOu2hO2VnOuLpC4iLAogICAgICAiYWZmZWN0
ZWRfbGF5ZXJzIjogWwogICAgICAgICJDIiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgImdy
YWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2V
nCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuS
pCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAg
ICAiaWQiOiAic3cwNF9mYXRhbF9mYXVsdF9pbmplY3Rpb25fbm90X3NvZnR3YXJlIiwKICAgICAg
InNldmVyaXR5IjogImZhdGFsIiwKICAgICAgImNsYWltIjogIuqysO2VqOyjvOyeheydgCDtjIzq
tLTsi5ztl5jsnbTrr4DroZwg7IaM7ZSE7Yq47Juo7Ja0IOyLnO2XmOyXkOuKlCDsgqzsmqntlaAg
7IiYIOyXhuuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAi6rKw7ZWo7KO87J6F7J2AIO2MjOq0
tOyLnO2XmOydtOuvgOuhnCDshoztlITtirjsm6jslrQg7Iuc7ZeY7JeQ64qUIOyCrOyaqe2VoCDs
iJgg7JeG64ukLiIsCiAgICAgICJtZXNzYWdlIjogIuqysO2VqOyjvOyeheydgCDtjIzqtLTsi5zt
l5jsnbTrr4DroZwg7IaM7ZSE7Yq47Juo7Ja0IOyLnO2XmOyXkOuKlCDsgqzsmqntlaAg7IiYIOyX
huuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wg
ZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gRmF1bHQgaW5qZWN0aW9u7J2AIO2GteygnOuQnCDtmZjq
sr3sl5DshJwg7IS87IScwrfthrXsi6DCt+yghOybkMK3642w7J207YSwwrd0YXNrIOydtOyDgeyd
hCDso7zsnoXtlbQg6rKA7LacwrfqsqnrpqzCt+uzteq1rOulvCDqsoDspp3tlZzri6QuIiwKICAg
ICAgImNvcnJlY3RfcnVsZSI6ICJGYXVsdCBpbmplY3Rpb27snYAg7Ya17KCc65CcIO2ZmOqyveyX
kOyEnCDshLzshJzCt+2GteyLoMK37KCE7JuQwrfrjbDsnbTthLDCt3Rhc2sg7J207IOB7J2EIOyj
vOyehe2VtCDqsoDstpzCt+qyqeumrMK367O16rWs66W8IOqygOymne2VnOuLpC4iLAogICAgICAi
Y29ycmVjdGlvbiI6ICJGYXVsdCBpbmplY3Rpb27snYAg7Ya17KCc65CcIO2ZmOqyveyXkOyEnCDs
hLzshJzCt+2GteyLoMK37KCE7JuQwrfrjbDsnbTthLDCt3Rhc2sg7J207IOB7J2EIOyjvOyehe2V
tCDqsoDstpzCt+qyqeumrMK367O16rWs66W8IOqygOymne2VnOuLpC4iLAogICAgICAiYWZmZWN0
ZWRfbGF5ZXJzIjogWwogICAgICAgICJDIiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgImdy
YWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2V
nCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuS
pCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAg
ICAiaWQiOiAic3cwNF9mYXRhbF9jaGFuZ2VfZXhwZWN0ZWRfcmVzdWx0IiwKICAgICAgInNldmVy
aXR5IjogImZhdGFsIiwKICAgICAgImNsYWltIjogIuyLnO2XmOydtCDsi6TtjKjtlZjrqbQg7JiI
7IOB6rKw6rO866W8IOyLpOygnCDqsrDqs7zroZwg67CU6r647Ja0IO2GteqzvCDsspjrpqztlZjr
qbQg65Cc64ukLiIsCiAgICAgICJ3cm9uZ19jbGFpbSI6ICLsi5ztl5jsnbQg7Iuk7Yyo7ZWY66m0
IOyYiOyDgeqysOqzvOulvCDsi6TsoJwg6rKw6rO866GcIOuwlOq+uOyWtCDthrXqs7wg7LKY66as
7ZWY66m0IOuQnOuLpC4iLAogICAgICAibWVzc2FnZSI6ICLsi5ztl5jsnbQg7Iuk7Yyo7ZWY66m0
IOyYiOyDgeqysOqzvOulvCDsi6TsoJwg6rKw6rO866GcIOuwlOq+uOyWtCDthrXqs7wg7LKY66as
7ZWY66m0IOuQnOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDs
o7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g7Iuc7ZeYIOyghCDqs6DsoJXtlZwg7JiI
7IOB6rKw6rO87JmAIO2MkOygleq4sOykgOydhCDsnKDsp4DtlZjqs6Ag7Iuk7Yyo64qUIOqysO2V
qCDrmJDripQg7Iq57J2465CcIOyalOq1rOyCrO2VrSDrs4Dqsr3snLzroZwg7LaU7KCB7ZW07JW8
IO2VnOuLpC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIuyLnO2XmCDsoIQg6rOg7KCV7ZWcIOyY
iOyDgeqysOqzvOyZgCDtjJDsoJXquLDspIDsnYQg7Jyg7KeA7ZWY6rOgIOyLpO2MqOuKlCDqsrDt
lagg65iQ64qUIOyKueyduOuQnCDsmpTqtazsgqztla0g67OA6rK97Jy866GcIOy2lOygge2VtOyV
vCDtlZzri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAi7Iuc7ZeYIOyghCDqs6DsoJXtlZwg7JiI
7IOB6rKw6rO87JmAIO2MkOygleq4sOykgOydhCDsnKDsp4DtlZjqs6Ag7Iuk7Yyo64qUIOqysO2V
qCDrmJDripQg7Iq57J2465CcIOyalOq1rOyCrO2VrSDrs4Dqsr3snLzroZwg7LaU7KCB7ZW07JW8
IO2VnOuLpC4iLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJDIiwKICAgICAg
ICAiRCIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDs
mKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyI
nCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuK
lOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwNF9mYXRhbF9yZXZpZXdfcmVwbGFj
ZXNfdGVzdCIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJjbGFpbSI6ICLsvZTr
k5wg66as67ew66W8IOyImO2Wie2VmOuptCDrj5nsoIEg7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2X
mOydhCDrqqjrkZAg7IOd65617ZWgIOyImCDsnojri6QuIiwKICAgICAgIndyb25nX2NsYWltIjog
Iuy9lOuTnCDrpqzrt7Drpbwg7IiY7ZaJ7ZWY66m0IOuPmeyggSDsi5ztl5jqs7wg7Iuc7Iqk7YWc
7Iuc7ZeY7J2EIOuqqOuRkCDsg53rnrXtlaAg7IiYIOyeiOuLpC4iLAogICAgICAibWVzc2FnZSI6
ICLsvZTrk5wg66as67ew66W8IOyImO2Wie2VmOuptCDrj5nsoIEg7Iuc7ZeY6rO8IOyLnOyKpO2F
nOyLnO2XmOydhCDrqqjrkZAg7IOd65617ZWgIOyImCDsnojri6QuIiwKICAgICAgImRlc2NyaXB0
aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6Qu
IFJldmlld+yZgCDsoJXsoIHrtoTshJ3snYAg7Iuk7ZaJIOq4sOuwmCDsi5ztl5jsnYQg67O07JmE
7ZWY7KeA66eMIOuMgOyytO2VmOyngCDslYrsnLzrqbAg7JqU6rWs7IKs7ZWtIOyImOykgOyXkCDr
p57ripQg64+Z7KCBwrfthrXtlanCt+yLnOyKpO2FnCDsi5ztl5jsnbQg7ZWE7JqU7ZWY64ukLiIs
CiAgICAgICJjb3JyZWN0X3J1bGUiOiAiUmV2aWV37JmAIOygleyggeu2hOyEneydgCDsi6Ttlokg
6riw67CYIOyLnO2XmOydhCDrs7TsmYTtlZjsp4Drp4wg64yA7LK07ZWY7KeAIOyViuycvOupsCDs
mpTqtazsgqztla0g7IiY7KSA7JeQIOunnuuKlCDrj5nsoIHCt+2Gte2VqcK37Iuc7Iqk7YWcIOyL
nO2XmOydtCDtlYTsmpTtlZjri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAiUmV2aWV37JmAIOyg
leyggeu2hOyEneydgCDsi6Ttlokg6riw67CYIOyLnO2XmOydhCDrs7TsmYTtlZjsp4Drp4wg64yA
7LK07ZWY7KeAIOyViuycvOupsCDsmpTqtazsgqztla0g7IiY7KSA7JeQIOunnuuKlCDrj5nsoIHC
t+2Gte2VqcK37Iuc7Iqk7YWcIOyLnO2XmOydtCDtlYTsmpTtlZjri6QuIiwKICAgICAgImFmZmVj
dGVkX2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJn
cmFkaW5nX25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXt
lZwg6rK97Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDr
kqQg7KCV7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAg
ICAgImlkIjogInN3MDRfZmF0YWxfbm9fdmVyc2lvbl9uZWVkZWQiLAogICAgICAic2V2ZXJpdHki
OiAiZmF0YWwiLAogICAgICAiY2xhaW0iOiAi7Iuc7ZeY6rKw6rO87JeQIOuMgOyDgSDrsoTsoITq
s7wg7Iuc7ZeY7ZmY6rK97J2EIOq4sOuhne2VmOyngCDslYrslYTrj4Qg7J6s7ZiE7ZWgIOyImCDs
nojri6QuIiwKICAgICAgIndyb25nX2NsYWltIjogIuyLnO2XmOqysOqzvOyXkCDrjIDsg4Eg67KE
7KCE6rO8IOyLnO2XmO2ZmOqyveydhCDquLDroZ3tlZjsp4Ag7JWK7JWE64+EIOyerO2YhO2VoCDs
iJgg7J6I64ukLiIsCiAgICAgICJtZXNzYWdlIjogIuyLnO2XmOqysOqzvOyXkCDrjIDsg4Eg67KE
7KCE6rO8IOyLnO2XmO2ZmOqyveydhCDquLDroZ3tlZjsp4Ag7JWK7JWE64+EIOyerO2YhO2VoCDs
iJgg7J6I64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOye
peunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDsi5ztl5jrjIDsg4EgYmFzZWxpbmUsIEhXwrdP
U8K3ZmlybXdhcmXCt3Rvb2zqs7wg7ISk7KCV7J2EIOyLneuzhO2VtOyVvCDqsrDqs7zsnZgg7J6s
7ZiE7ISx6rO8IOqwkOyCrOqwgOuKpeyEseydhCDtmZXrs7TtlaAg7IiYIOyeiOuLpC4iLAogICAg
ICAiY29ycmVjdF9ydWxlIjogIuyLnO2XmOuMgOyDgSBiYXNlbGluZSwgSFfCt09TwrdmaXJtd2Fy
ZcK3dG9vbOqzvCDshKTsoJXsnYQg7Iud67OE7ZW07JW8IOqysOqzvOydmCDsnqztmITshLHqs7wg
6rCQ7IKs6rCA64ql7ISx7J2EIO2ZleuztO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICJjb3JyZWN0
aW9uIjogIuyLnO2XmOuMgOyDgSBiYXNlbGluZSwgSFfCt09TwrdmaXJtd2FyZcK3dG9vbOqzvCDs
hKTsoJXsnYQg7Iud67OE7ZW07JW8IOqysOqzvOydmCDsnqztmITshLHqs7wg6rCQ7IKs6rCA64ql
7ISx7J2EIO2ZleuztO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBb
CiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6
ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWcIOqyveyasOyXkOun
jCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65KkIOygleygleydgCBm
YXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzA0
X2ZhdGFsX3NtYWxsX2NoYW5nZV9ub19pbXBhY3QiLAogICAgICAic2V2ZXJpdHkiOiAiZmF0YWwi
LAogICAgICAiY2xhaW0iOiAi7J6R7J2AIOuzgOqyveydgCDsmIHtlqXrtoTshJ3qs7wg7ZqM6reA
7Iuc7ZeY7J2EIO2VreyDgSDsg53rnrXtlaAg7IiYIOyeiOuLpC4iLAogICAgICAid3JvbmdfY2xh
aW0iOiAi7J6R7J2AIOuzgOqyveydgCDsmIHtlqXrtoTshJ3qs7wg7ZqM6reA7Iuc7ZeY7J2EIO2V
reyDgSDsg53rnrXtlaAg7IiYIOyeiOuLpC4iLAogICAgICAibWVzc2FnZSI6ICLsnpHsnYAg67OA
6rK97J2AIOyYge2Wpeu2hOyEneqzvCDtmozqt4Dsi5ztl5jsnYQg7ZWt7IOBIOyDneuete2VoCDs
iJgg7J6I64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOye
peunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDrs4Dqsr0g6rec66qo7JmAIOustOq0gO2VmOqy
jCDsmIHtlqXrspTsnITrpbwg7Y+J6rCA7ZWY6rOgIOq3uCDqsrDqs7zsl5Ag65Sw6528IFJUTcK3
7IKw7Lac66y8wrftmozqt4Dsi5ztl5gg67KU7JyE66W8IOqwseyLoO2VtOyVvCDtlZzri6QuIiwK
ICAgICAgImNvcnJlY3RfcnVsZSI6ICLrs4Dqsr0g6rec66qo7JmAIOustOq0gO2VmOqyjCDsmIHt
lqXrspTsnITrpbwg7Y+J6rCA7ZWY6rOgIOq3uCDqsrDqs7zsl5Ag65Sw6528IFJUTcK37IKw7Lac
66y8wrftmozqt4Dsi5ztl5gg67KU7JyE66W8IOqwseyLoO2VtOyVvCDtlZzri6QuIiwKICAgICAg
ImNvcnJlY3Rpb24iOiAi67OA6rK9IOq3nOuqqOyZgCDrrLTqtIDtlZjqsowg7JiB7Zal67KU7JyE
66W8IO2PieqwgO2VmOqzoCDqt7gg6rKw6rO87JeQIOuUsOudvCBSVE3Ct+yCsOy2nOusvMK37ZqM
6reA7Iuc7ZeYIOuylOychOulvCDqsLHsi6DtlbTslbwg7ZWc64ukLiIsCiAgICAgICJhZmZlY3Rl
ZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAiZ3Jh
ZGluZ19ub3RlcyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWc
IOqyveyasOyXkOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65Kk
IOygleygleydgCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAg
ICJpZCI6ICJzdzA0X2ZhdGFsX2dlbmVyYWxfdnZfcHJvdmVzX3NpbCIsCiAgICAgICJzZXZlcml0
eSI6ICJmYXRhbCIsCiAgICAgICJjbGFpbSI6ICLsnbzrsJgg7IaM7ZSE7Yq47Juo7Ja0IFYmVuul
vCDsmYTro4ztlZjrqbQg67OE64+EIFNhZmV0eSBsaWZlY3ljbGUg7JeG7J20IFNJU+ydmCBTSUwg
7Lap7KGx7J20IOyekOuPmeycvOuhnCDspp3rqoXrkJzri6QuIiwKICAgICAgIndyb25nX2NsYWlt
IjogIuydvOuwmCDshoztlITtirjsm6jslrQgViZW66W8IOyZhOujjO2VmOuptCDrs4Trj4QgU2Fm
ZXR5IGxpZmVjeWNsZSDsl4bsnbQgU0lT7J2YIFNJTCDstqnsobHsnbQg7J6Q64+Z7Jy866GcIOym
neuqheuQnOuLpC4iLAogICAgICAibWVzc2FnZSI6ICLsnbzrsJgg7IaM7ZSE7Yq47Juo7Ja0IFYm
VuulvCDsmYTro4ztlZjrqbQg67OE64+EIFNhZmV0eSBsaWZlY3ljbGUg7JeG7J20IFNJU+ydmCBT
SUwg7Lap7KGx7J20IOyekOuPmeycvOuhnCDspp3rqoXrkJzri6QuIiwKICAgICAgImRlc2NyaXB0
aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6Qu
IFNXLTA07J2YIOydvOuwmCBWJlbsmYAgU1ctMDXsnZggU2FmZXR5IEludGVncml0eSwg64+F66a9
7ISxLCDssrTqs4TsoIEg6rOg7J6lIO2GteygnOyZgCBTYWZldHkgViZW66W8IOq1rOu2hO2VtOyV
vCDtlZzri6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6ICJTVy0wNOydmCDsnbzrsJggViZW7JmA
IFNXLTA17J2YIFNhZmV0eSBJbnRlZ3JpdHksIOuPheumveyEsSwg7LK06rOE7KCBIOqzoOyepSDt
hrXsoJzsmYAgU2FmZXR5IFYmVuulvCDqtazrtoTtlbTslbwg7ZWc64ukLiIsCiAgICAgICJjb3Jy
ZWN0aW9uIjogIlNXLTA07J2YIOydvOuwmCBWJlbsmYAgU1ctMDXsnZggU2FmZXR5IEludGVncml0
eSwg64+F66a97ISxLCDssrTqs4TsoIEg6rOg7J6lIO2GteygnOyZgCBTYWZldHkgViZW66W8IOq1
rOu2hO2VtOyVvCDtlZzri6QuIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAi
QyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuuLteyViOyd
tCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyggeyaqe2V
mOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs66GcIOuz
tOyngCDslYrripTri6QuIgogICAgfQogIF0sCiAgInNhZmVfZXhwcmVzc2lvbnMiOiBbCiAgICAi
VmVyaWZpY2F0aW9u6rO8IFZhbGlkYXRpb27snYAg7IOB7Zi467O07JmE7KCB7J2066mwIOuqqeyg
geydtCDri6TrpbTri6QuIiwKICAgICJWLU1vZGVs7J2AIOqwnOuwnCDstIjquLDrtoDthLAg64yA
7J2RIOyLnO2XmOqzvCDsiJjsmqnquLDspIDsnYQg7KSA67mE7ZWc64ukLiIsCiAgICAiUlRN7J2A
IOyInOuwqe2WpeqzvCDsl63rsKntlqUg7LaU7KCB7J2EIOuqqOuRkCDsoJzqs7XtlZzri6QuIiwK
ICAgICLri6jsnITsi5ztl5gg7Ya16rO864qUIO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5zt
l5jsnYQg64yA7LK07ZWY7KeAIOyViuuKlOuLpC4iLAogICAgIuygleyggeu2hOyEneydgCDtlITr
oZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7KeAIOyViuqzoCDsiJjtlontlZzri6QuIiwKICAgICLrj5ns
oIHrtoTshJ3snYAg7Iuk7ZaJIOykkSDqsr3roZwsIOyLnOqwhCwg7J6Q7JuQ6rO8IOuwmOydkeyd
hCDqtIDssLDtlZzri6QuIiwKICAgICLtmozqt4Dsi5ztl5jsnYAg67OA6rK9IOq4sOuKpeqzvCDs
mIHtlqXrsJvripQg6riw7KG0IOq4sOuKpeydhCDtlajqu5gg7ZmV7J247ZWc64ukLiIsCiAgICAi
U2ltdWxhdGlvbuydgCDrqqjrjbgg6rCA7KCV6rO8IO2VnOqzhOulvCDqsIDsp4Tri6QuIiwKICAg
ICJISUzsnYAg7Iuk7KCcIOuMgOyDgSDsoJzslrTquLAg65iQ64qUIOyLpOygnCBJL08g7ZWY65Oc
7Juo7Ja066W8IOyLpOyLnOqwhCBQbGFudCBNb2RlbOqzvCDtj5Dro6jtlITroZwg7Jew6rKw7ZWY
66mwIOyLpOygnCDsg53sgrDshKTruYQg6rCA64+Z7J2AIO2VhOyalO2VmOyngCDslYrri6QuIiwK
ICAgICJGYXVsdCBpbmplY3Rpb27snYAg7Ya17KCc65CcIOyLnO2XmO2ZmOqyveyXkOyEnCDsnqXs
laAg6rKA7Lac6rO8IOuzteq1rOulvCDqsoDspp3tlZzri6QuIiwKICAgICLsi5ztl5gg7Iuk7Yyo
64qUIOqysO2VqCDrmJDripQg7Iq57J2465CcIOuzgOqyveycvOuhnCDstpTsoIHtlZzri6QuIiwK
ICAgICJSZXZpZXfripQg64+Z7KCB7Iuc7ZeY7J2EIOuztOyZhO2VmOyngOunjCDrqqjrkZAg64yA
7LK07ZWY7KeAIOyViuuKlOuLpC4iLAogICAgIuyLnO2XmOqysOqzvOyXkOuKlCDrjIDsg4EgYmFz
ZWxpbmXqs7wg7ZmY6rK97J2EIOq4sOuhne2VnOuLpC4iLAogICAgIuuzgOqyveydgCDsmIHtlqXr
toTshJ3qs7wg7ZWE7JqU7ZWcIO2ajOq3gOyLnO2XmOydhCDqsbDsuZzri6QuIiwKICAgICLsnbzr
sJggU1cgViZW7JmAIFNJUyBTYWZldHkgViZW66W8IOq1rOu2hO2VnOuLpC4iLAogICAgIkZBVMK3
U0FUwrfsi5zsmrTsoITCt0FjY2VwdGFuY2XripQgU1ctMTDsnLzroZwg7J206rSA7ZWc64ukLiIs
CiAgICAi66qF7IS4IOygge2VqeyEseqzvCDsgqzsmqnrqqnsoIEg7KCB7ZWp7ISx7J2EIOuqqOuR
kCDtmZXsnbjtlbTslbwg7ZWc64ukLiIsCiAgICAi64uo7IicIOuIhOudveydgCDsp4HsoJEg67CY
64yAIOyjvOyepeqzvCDqtazrtoTtlZzri6QuIgogIF0sCiAgInJldmlzaW9uX25vdGVzIjogWwog
ICAgIlNXLTA0IOydvOuwmCDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNsZSBv
d25lcnNoaXDsnYQg7KCV7J2Y7ZaI64ukLiIsCiAgICAiU1ctMDUgU2FmZXR5IGxpZmVjeWNsZeqz
vCBTVy0xMCDtlITroZzsoJ3tirggRkFUwrdTQVTCt0FjY2VwdGFuY2Ug6rK96rOE66W8IOuqheyL
nO2WiOuLpC4iLAogICAgIlYtTW9kZWwsIOyWkeuwqe2WpSBSVE0sIOygleyggcK364+Z7KCBwrft
mozqt4Dsi5ztl5gsIFNpbXVsYXRpb27Ct0hJTMK3RmF1bHQgaW5qZWN0aW9u7J2EIOyXsOqysO2W
iOuLpC4iLAogICAgIjIwMjYtMDgtMDcgTExNIOydmOuvuCDqsJDsgqwg7IiY66asOiBISUzqs7wg
U29mdHdhcmUtaW4tdGhlLWxvb3DCt1ZpcnR1YWwgQ29tbWlzc2lvbmluZyDqsr3qs4Trpbwg6rWQ
7KCV7ZaI64ukLiIKICBdLAogICJ0b3BpY19sYWJlbCI6ICJTVy0wNCDqs4TsuKHsoJzslrQgU1cg
7IiY66qF7KO86riwwrdWLU1vZGVswrdWJlYiLAogICJjb3JlX2ZhY3RzIjogWwogICAgIlNXLTA0
64qUIOydvOuwmCDqs4TsuKHsoJzslrQg7IaM7ZSE7Yq47Juo7Ja07J2YIOyalOq1rOyCrO2VrSwg
7JWE7YKk7YWN7LKYLCDsg4HshLjshKTqs4QsIOq1rO2YhCwg7Iuc7ZeYLCDstpTsoIHshLEsIOqy
sO2VqOq0gOumrOyZgCDsirnsnbjquYzsp4DsnZgg7IiY66qF7KO86riw66W8IOuLpOujrOuLpC4i
LAogICAgIlNJUyDslYjsoIQg7IaM7ZSE7Yq47Juo7Ja07J2YIFNhZmV0eSBJbnRlZ3JpdHksIOuP
heumveyEsSwg7LK06rOE7KCBIOqzoOyepSDthrXsoJzsmYAgU2FmZXR5IFYmVuuKlCBTVy0wNeuh
nCDsnbTqtIDtlZzri6QuIiwKICAgICJGQVTCt1NBVMK3TG9vcCB0ZXN0wrfsi5zsmrTsoITCt+yE
seuKpeyLnO2XmMK3QWNjZXB0YW5jZcK3SGFuZG92ZXLripQgU1ctMTDsnZgg7ZSE66Gc7KCd7Yq4
IOyImO2WiSDrsI8g7J247IiYIOyYgeyXreydtOuLpC4iLAogICAgIlYtTW9kZWzsnYAg7KKM7Lih
7J2YIOyalOq1rOyCrO2VrcK37ISk6rOEwrfqtaztmIQg64uo6rOE7JmAIOyasOy4oeydmCDrjIDs
nZEg7Iuc7ZeYwrftmZXsnbgg64uo6rOE66W8IOyXsOqysO2VmOqzoCwg7Iuc7ZeY6riw7KSA7J2E
IOqwnOuwnCDstIjquLDsl5Ag7KSA67mE7ZWY64qUIGxpZmVjeWNsZSDrqqjrjbjsnbTri6QuIiwK
ICAgICLsmpTqtazsgqztla3snYAg7Iud67OE7J6QLCDquLDriqUsIOyEseuKpSwg7J247YSw7Y6Y
7J207IqkLCDsmrTsoITrqqjrk5wsIOyYiOyZuMK36rOg7J6l7J2R64u16rO8IOyImOyaqeq4sOyk
gOydhCDtj6ztlajtlZjrqbAg66qF7ZmV7ZWY6rOgIOyLnO2XmCDqsIDriqXtlbTslbwg7ZWc64uk
LiIsCiAgICAi7Iuc7Iqk7YWcIOyVhO2CpO2FjeyymOuKlCDsoJzslrTquLAsIEhNSSwg7ISc67KE
LCDrhKTtirjsm4ztgawsIEkvT+yZgCDsmbjrtoDsi5zsiqTthZzsnZgg6riw64ql67Cw67aELCDs
nbjthLDtjpjsnbTsiqQsIOuNsOydtO2EsO2dkOumhOqzvCDqs6DsnqXqsr3qs4Trpbwg7KCV7J2Y
7ZWc64ukLiIsCiAgICAi7IaM7ZSE7Yq47Juo7Ja0IOyVhO2CpO2FjeyymOuKlCDrqqjrk4gsIO2D
nOyKpO2BrCwg7IOB7YOc6rSA66asLCDrjbDsnbTthLAsIO2GteyLoCwg7KeE64uo6rO8IOyekOyb
kOuwsOu2hOydmCDqtazsobAg67CPIOyduO2EsO2OmOydtOyKpOulvCDsoJXsnZjtlZzri6QuIiwK
ICAgICLsg4HshLjshKTqs4TripQg7JWM6rOg66as7KaYLCDsg4Htg5zsoITsnbQsIEkvTyDsspjr
pqwsIOyYiOyZuOyymOumrCwg642w7J207YSw7ZiVLCDqsr3qs4TsobDqsbTqs7wg66qo65OIIOyd
uO2EsO2OmOydtOyKpOulvCDqtaztmIQg6rCA64ql7ZWcIOyImOykgOycvOuhnCDqtazssrTtmZTt
lZzri6QuIiwKICAgICLsvZTrlKkg7ZGc7KSA7J2AIOuqheuqhSwg7J6Q66OM7ZiVLCDstIjquLDt
mZQsIOuylOychCwg7JiI7Jm47LKY66asLCDrs7XsnqHrj4QsIOq4iOyngOq1rOusuCwg7KO87ISd
6rO8IOumrOu3sCDquLDspIDsnYQg7J286rSA65CY6rKMIOq3nOygle2VnOuLpC4iLAogICAgIuya
lOq1rOyCrO2VrcK37ISk6rOEwrfshozsiqTCt+yLnO2XmOygiOywqMK364+E6rWswrftmZjqsr3s
nYAg7Iud67OE65CcIGJhc2VsaW5l6rO8IOuyhOyghOycvOuhnCDqtIDrpqzrkJjslrTslbwg64+Z
7J28IOqysOqzvOulvCDsnqztmITtlaAg7IiYIOyeiOuLpC4iLAogICAgIuuLqOychOyLnO2XmOyd
gCDtlajsiJjCt+uqqOuTiMK3RkIg65OxIOy1nOyGjCDshKTqs4Tri6jsnITsnZgg7KCV7IOBLCDq
sr3qs4QsIOyYpOulmCDqsr3roZzsmYAg7J247YSw7Y6Y7J207IqkIOqzhOyVveydhCDqsqnrpqzt
lZjsl6wg6rKA7Kad7ZWc64ukLiIsCiAgICAi7Ya17ZWp7Iuc7ZeY7J2AIOuqqOuTiMK37YOc7Iqk
7YGswrfthrXsi6DCt+uNsOydtO2EsOuyoOydtOyKpMK37J6l7LmYIOyduO2EsO2OmOydtOyKpCDq
sIQg642w7J207YSwLCDsiJzshJwsIO2DgOydtOuwjeqzvCDsmKTrpZjsoITtjIzrpbwg6rKA7Kad
7ZWc64ukLiIsCiAgICAi7Iuc7Iqk7YWc7Iuc7ZeY7J2AIO2Gte2VqeuQnCDsoJzslrQg7IaM7ZSE
7Yq47Juo7Ja06rCAIOyLnOyKpO2FnCDsmpTqtazsgqztla0sIOyatOyghOuqqOuTnCwg7ISx64ql
LCDsnqXslaDrs7XqtazsmYAg7Jm467aAIOyduO2EsO2OmOydtOyKpOulvCDstqnsobHtlZjripTs
p4Ag7ZmV7J247ZWc64ukLiIsCiAgICAiVmVyaWZpY2F0aW9u7J2AIOqwgSDsgrDstpzrrLzsnbQg
7ZW064u5IOuLqOqzhOydmCDrqoXshLjsmYAg7ISk6rOE6riw7KSA7JeQIOunnuqyjCDrp4zrk6Ts
lrTsoYzripTsp4Drpbwg7ZmV7J247ZWY64qUIO2ZnOuPmeydtOuLpC4iLAogICAgIlZhbGlkYXRp
b27snYAg7Ya17ZWp65CcIOyLnOyKpO2FnOydtCDsnZjrj4TrkJwg7IKs7Jqp66qp7KCB6rO8IOya
tOyghO2ZmOqyveyXkOyEnCDsgqzsmqnsnpAg7JqU6rWs66W8IOy2qeyhse2VmOuKlOyngOulvCDt
mZXsnbjtlZjripQg7Zmc64+Z7J2064ukLiIsCiAgICAiVmVyaWZpY2F0aW9u6rO8IFZhbGlkYXRp
b27snYAg7IOB7Zi467O07JmE7KCB7J2066mwIOyWtOuKkCDtlZjrgpjsnZgg7ISx6rO17J20IOuL
pOuluCDtlZjrgpjrpbwg7J6Q64+Z7Jy866GcIOuztOyepe2VmOyngCDslYrripTri6QuIiwKICAg
ICJSZXF1aXJlbWVudCBUcmFjZWFiaWxpdHkgTWF0cml464qUIOyalOq1rOyCrO2VreyXkOyEnCDs
hKTqs4TCt+y9lOuTnMK37Iuc7ZeYwrfqsrDqs7zroZzsnZgg7Iic67Cp7Zal6rO8IOyLnO2XmMK3
6rKw6rO87JeQ7IScIOyalOq1rOyCrO2VreycvOuhnOydmCDsl63rsKntlqUg7LaU7KCB7J2EIOyg
nOqzte2VnOuLpC4iLAogICAgIuygleyggeu2hOyEneydgCDtlITroZzqt7jrnqjsnYQg7Iuk7ZaJ
7ZWY7KeAIOyViuqzoCDqt5zsuZnsnITrsJgsIOuNsOydtO2EsO2dkOumhCwg7KCc7Ja07Z2Q66aE
LCDrs7XsnqHrj4QsIOuvuOy0iOq4sO2ZlOyZgCDsnqDsnqwg6rKw7ZWo7J2EIOu2hOyEne2VnOuL
pC4iLAogICAgIuuPmeyggeu2hOyEneydgCDsi6TtlonrkJwg7IaM7ZSE7Yq47Juo7Ja07J2YIOqy
veuhnCwg7Iuc6rCELCDrqZTrqqjrpqzCt+yekOybkCwg7J247YSw7Y6Y7J207Iqk7JmAIOyLpOyg
nCDrsJjsnZHsnYQg7J6F66ClIOyhsOqxtOuzhOuhnCDqtIDssLDtlZzri6QuIiwKICAgICLtmozq
t4Dsi5ztl5jsnYAg67OA6rK965CcIOq4sOuKpeu/kCDslYTri4jrnbwg7JiB7Zal67Cb7J2EIOyI
mCDsnojripQg6riw7KG0IOq4sOuKpeqzvCDsnbjthLDtjpjsnbTsiqTqsIAg7Jyg7KeA65CY64qU
7KeAIOuwmOuztSDtmZXsnbjtlZzri6QuIiwKICAgICJTaW11bGF0aW9u7J2AIHBsYW50wrdwcm9j
ZXNzwrdkZXZpY2XsnZgg66qo64247J2EIOyCrOyaqe2VmOyXrCDri6TslpHtlZwg7KCV7IOBwrfr
uYTsoJXsg4Eg7Iuc64KY66as7Jik66W8IOuwmOuztSDqsoDspp3tlZjsp4Drp4wg66qo64247J2Y
IOqwgOygleqzvCDtlZzqs4Trpbwg6rSA66as7ZW07JW8IO2VnOuLpC4iLAogICAgIkhJTOydgCDs
i6TsoJwg64yA7IOBIOygnOyWtOq4sCDtlZjrk5zsm6jslrQg65iQ64qUIOyLpOygnCBJL08g7ZWY
65Oc7Juo7Ja066W8IOyLpOyLnOqwhCBQbGFudCBNb2RlbOqzvCDtj5Dro6jtlITroZwg7Jew6rKw
7ZWY7JesIEkvTywgdGltaW5nLCDthrXsi6Dqs7wg7KCc7Ja064+Z7J6R7J2EIOyLnO2XmO2VnOuL
pC4g7ZWY65Oc7Juo7Ja0IOyXhuydtCDshoztlITtirjsm6jslrQg7Iuk7ZaJ7ZmY6rK966eMIOuq
qOuNuOqzvCDsl7DqsrDtlZjripQg7Iuc7ZeY7J2AIFNJTChTb2Z0d2FyZS1pbi10aGUtbG9vcCkg
65iQ64qUIFZpcnR1YWwgQ29tbWlzc2lvbmluZ+ycvOuhnCDqtazrtoTtlZzri6QuIiwKICAgICJG
YXVsdCBpbmplY3Rpb27snYAg7IS87ISc64uo7ISgLCDqs6DssKksIO2GteyLoOyngOyXsMK37IaQ
7IukLCDsoITsm5Drs7Xqt4AsIOuNsOydtO2EsOyYpOyXvOqzvCB0YXNrIOydtOyDgSDrk7HsnYQg
7J2Y64+E7KCB7Jy866GcIOyjvOyehe2VtCDqsoDstpzCt+qyqeumrMK367O16rWs66W8IOqygOym
ne2VnOuLpC4iLAogICAgIuyLnO2XmOuqheyEuOuKlCDrqqnsoIEsIOyCrOyghOyhsOqxtCwg7J6F
66ClLCDsoIjssKgsIOyYiOyDgeqysOqzvCwg7ZeI7Jqp7Jik7LCoLCDtjJDsoJXquLDspIAsIO2Z
mOqyvSwg7Kad7KCB6rO8IOyalOq1rOyCrO2VrSDssLjsobDrpbwg7Y+s7ZWo7ZWc64ukLiIsCiAg
ICAi7Iuc7ZeYIOyZhOujjOuKlCDri6jsiJwg7Iuk7ZaJIOqxtOyImOqwgCDslYTri4jrnbwg7JqU
6rWs7IKs7ZWtwrfsnITtl5jCt+qyveuhnMK37J247YSw7Y6Y7J207IqkIGNvdmVyYWdl7JmAIOuv
uO2VtOqysCDqsrDtlagsIGV4aXQgY3JpdGVyaWHrpbwg7ZWo6ruYIO2PieqwgO2VnOuLpC4iLAog
ICAgIuqysO2VqOydgCDsnqztmITsobDqsbQsIOyYge2WpSwg7Ius6rCB64+ELCDsm5DsnbgsIOyI
mOygleuyhOyghCwg7J6s7Iuc7ZeY6rO8IGNsb3N1cmUg7Kad7KCB7J2EIOy2lOygge2VmOupsCDs
i6TtjKjsi5ztl5jsnYQg7J6E7J2YIOyCreygnO2VmOyngCDslYrripTri6QuIiwKICAgICLrs4Dq
sr3qtIDrpqzripQg7JqU6rWs7IKs7ZWtwrfshKTqs4TCt+y9lOuTnCDrmJDripQg7ZmY6rK9IOuz
gOqyveyXkCDrjIDtlbQg7JiB7Zal67aE7ISdLCDsirnsnbgsIGJhc2VsaW5lIOqwseyLoCwgUlRN
IOqwseyLoOqzvCDshKDtg53rkJwg7ZqM6reA7Iuc7ZeY7J2EIOyImO2Wie2VnOuLpC4iLAogICAg
IuqygO2GoOyZgCDsirnsnbjsnYAg7Jet7ZWgLCDsnoXroKXsnpDro4wsIOqygO2GoOq4sOykgCwg
7KeA7KCB7IKs7ZWtLCDsobDsuZjtmZXsnbjqs7wg7Iq57J246raM7J6Q66W8IOu2hOumrO2VtCDq
sJ3qtIDsoIEg7Kad7KCB7J2EIOuCqOq4tOuLpC4iLAogICAgIuyLnO2XmO2ZmOqyveydgCDrjIDs
g4EgSFfCt09TwrdmaXJtd2FyZcK3bGlicmFyecK3bmV0d29ya8K3c2NhbiB0aW1lwrdJL08gc2Nh
bGluZ+qzvCB0b29sIHZlcnNpb27snYQg7Iud67OE7ZWY6rOgIOyLpOygnCDsmrTsoITtmZjqsr3q
s7zsnZgg7LCo7J2066W8IO2PieqwgO2VnOuLpC4iLAogICAgIuyImOuqheyjvOq4sOuKlCDri6js
iJwg7J2867Cp7ZalIOusuOyEnO2dkOumhOydtCDslYTri4jrnbwgcmV2aWV3LCBkZWZlY3TsmYAg
Y2hhbmdlIOqysOqzvOqwgCDshKDtlokg7IKw7Lac66y86rO8IOyLnO2XmOqzhO2ajeyXkCDtmZjr
pZjrkJjripQg7Ya17KCc65CcIOuwmOuzteqzvOygleydtOuLpC4iLAogICAgIlYmViDqsrDqs7zr
ipQg64iE6rCALCDrrLTsl4fsnYQsIOyWtOuWpCDrsoTsoITqs7wg7ZmY6rK97JeQ7IScLCDslrTr
lqQg6riw7KSA7Jy866GcIOyImO2Wie2WiOuKlOyngCDstpTsoIEg6rCA64ql7ZWcIOymneyggeyc
vOuhnCDrgqjqsqjslbwg7ZWc64ukLiIKICBdCn0K
PAYLOAD_SW04_03

    write_payload 'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/logic_check.json' 'c0c51c19c5409f53413d70d86971ca131762e56790bfcbd243e75e508bac2a5b' <<'PAYLOAD_SW04_04'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLmxvZ2ljX2NoZWNrLnYxIiwKICAidG9w
aWNfaWQiOiAiaW5zdHJ1bWVudGF0aW9uX2NvbnRyb2xfc29mdHdhcmVfbGlmZWN5Y2xlX3ZfbW9k
ZWxfdHJhY2VhYmlsaXR5X3ZlcmlmaWNhdGlvbl92YWxpZGF0aW9uIiwKICAidGl0bGUiOiAi6rOE
7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCDsiJjrqoXso7zquLAsIFYtTW9kZWwsIOy2lOyggeyE
sSwg6rKA7KadIOuwjyDtmZXsnbgiLAogICJkZXRlcm1pbmlzdGljX2NoZWNrcyI6IHsKICAgICJl
bmFibGVkIjogdHJ1ZSwKICAgICJ0b3BpY19uYW1lIjogIuqzhOy4oeygnOyWtCDshoztlITtirjs
m6jslrQg7IiY66qF7KO86riwLCBWLU1vZGVsLCDstpTsoIHshLEsIOqygOymnSDrsI8g7ZmV7J24
IiwKICAgICJxdWVzdGlvbl90eXBlIjogIlBST0NFRFVSRSIsCiAgICAiZGlmZmljdWx0eV9wcm9m
aWxlIjogIkRFU0lHTl9FVkFMVUFUSU9OIiwKICAgICJ0b3BpY19hbGlhc2VzIjogWwogICAgICAi
aW5zdHJ1bWVudGF0aW9uIGNvbnRyb2wgc29mdHdhcmUgbGlmZWN5Y2xlIFYtTW9kZWwiLAogICAg
ICAi6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCDsiJjrqoXso7zquLAgVi1Nb2RlbCIsCiAg
ICAgICJyZXF1aXJlbWVudCBhcmNoaXRlY3R1cmUgZGVzaWduIGNvZGluZyB0ZXN0IGxpZmVjeWNs
ZSIsCiAgICAgICLsmpTqtazsgqztla0g7JWE7YKk7YWN7LKYIOyDgeyEuOyEpOqzhCDqtaztmIQg
7Iuc7ZeYIiwKICAgICAgInZlcmlmaWNhdGlvbiB2YWxpZGF0aW9uIHJlcXVpcmVtZW50IHRyYWNl
YWJpbGl0eSBtYXRyaXgiLAogICAgICAi6rKA7KadIO2ZleyduCDsmpTqtazsgqztla0g7LaU7KCB
7ISxIOunpO2KuOumreyKpCIsCiAgICAgICJ1bml0IGludGVncmF0aW9uIHN5c3RlbSB0ZXN0IGNv
bnRyb2wgc29mdHdhcmUiLAogICAgICAi64uo7JyE7Iuc7ZeYIO2Gte2VqeyLnO2XmCDsi5zsiqTt
hZzsi5ztl5gg7KCc7Ja0IFNXIiwKICAgICAgInN0YXRpYyBkeW5hbWljIGFuYWx5c2lzIHJlZ3Jl
c3Npb24gdGVzdCIsCiAgICAgICLsoJXsoIHrtoTshJ0g64+Z7KCB67aE7ISdIO2ajOq3gOyLnO2X
mCIsCiAgICAgICJzaW11bGF0aW9uIEhJTCBmYXVsdCBpbmplY3Rpb24gc29mdHdhcmUgdGVzdCIs
CiAgICAgICLsi5zrrqzroIjsnbTshZggSElMIOqysO2VqOyjvOyehSBTVyDsi5ztl5giLAogICAg
ICAic29mdHdhcmUgcmVxdWlyZW1lbnQgdGVzdCBiaWRpcmVjdGlvbmFsIHRyYWNlYWJpbGl0eSIs
CiAgICAgICLshoztlITtirjsm6jslrQg7JqU6rWs7IKs7ZWtIOyLnO2XmCDslpHrsKntlqUg7LaU
7KCB7ISxIiwKICAgICAgImNvZGluZyBzdGFuZGFyZCByZXZpZXcgZGVmZWN0IG1hbmFnZW1lbnQi
LAogICAgICAi7L2U65Sp7ZGc7KSAIOqygO2GoCDqsrDtlajqtIDrpqwiLAogICAgICAiY29uZmln
dXJhdGlvbiBiYXNlbGluZSBjaGFuZ2UgaW1wYWN0IHJlZ3Jlc3Npb24iLAogICAgICAi6rWs7ISx
IGJhc2VsaW5lIOuzgOqyvSDsmIHtlqUg7ZqM6reAIiwKICAgICAgImNvbnRyb2wgc29mdHdhcmUg
dmVyaWZpY2F0aW9uIGV2aWRlbmNlIGFwcHJvdmFsIiwKICAgICAgIuygnOyWtCDshoztlITtirjs
m6jslrQgViZWIOymneyggSDsirnsnbgiCiAgICBdLAogICAgImZhdGFsX2NoZWNrcyI6IFsKICAg
ICAgewogICAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX3ZlcmlmaWNhdGlvbl9lcXVhbHNfdmFsaWRh
dGlvbiIsCiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICJW
ZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbuydgCDsmYTsoITtnogg6rCZ7J2AIO2ZnOuPmeydtOuL
pC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBm
YXRhbCDtm4Trs7TroZwg67O464ukLiBWZXJpZmljYXRpb27snYAg64uo6rOEIOyCsOy2nOusvOyd
mCDrqoXshLgg7KCB7ZWp7ISx7J2ELCBWYWxpZGF0aW9u7J2AIOydmOuPhOuQnCDsgqzsmqnrqqns
oIHqs7wg7IKs7Jqp7J6QIOyalOq1rCDstqnsobHsnYQg7ZmV7J247ZWY66mwIOyDge2YuOuztOyZ
hOyggeydtOuLpC4iLAogICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6IFsKICAgICAgICAgICIoP2lt
KV5cXHMqKD86Wy0q4oCiXVxccyopP1ZlcmlmaWNhdGlvbuqzvFxcIFZhbGlkYXRpb27snYBcXCDs
mYTsoITtnohcXCDqsJnsnYBcXCDtmZzrj5nsnbTri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAg
ICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICJWZXJpZmlj
YXRpb27qs7wgVmFsaWRhdGlvbuydgCDsmYTsoITtnogg6rCZ7J2AIO2ZnOuPmeydtOuLpC4iCiAg
ICAgICAgXSwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlZlcmlmaWNhdGlvbuydgCDri6jqs4Qg
7IKw7Lac66y87J2YIOuqheyEuCDsoIHtlanshLHsnYQsIFZhbGlkYXRpb27snYAg7J2Y64+E65Cc
IOyCrOyaqeuqqeyggeqzvCDsgqzsmqnsnpAg7JqU6rWsIOy2qeyhseydhCDtmZXsnbjtlZjrqbAg
7IOB7Zi467O07JmE7KCB7J2064ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAg
ICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVk
X2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9mYXRh
bF92YWxpZGF0aW9uX2lzX2NvZGluZ19zdGFuZGFyZCIsCiAgICAgICAgInNldmVyaXR5IjogImZh
dGFsIiwKICAgICAgICAibWVzc2FnZSI6ICJWYWxpZGF0aW9u7J2AIOy9lOuUqSDtkZzspIAg7KSA
7IiYIOyXrOu2gOunjCDtmZXsnbjtlZjripQg7Zmc64+Z7J2064ukLiIsCiAgICAgICAgImRlc2Ny
aXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jr
i6QuIOy9lOuUqSDtkZzspIAg7KSA7IiY64qUIFZlcmlmaWNhdGlvbuydmCDsnbzrtoDqsIAg65Cg
IOyImCDsnojsnLzrgpggVmFsaWRhdGlvbuydgCDthrXtlakg7Iuc7Iqk7YWc7J2YIOyCrOyaqeuq
qeyggeqzvCDsgqzsmqnsnpAg7JqU6rWsIOy2qeyhseydhCDtmZXsnbjtlZzri6QuIiwKICAgICAg
ICAid3JvbmdfcGF0dGVybnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMq
KT9WYWxpZGF0aW9u7J2AXFwg7L2U65SpXFwg7ZGc7KSAXFwg7KSA7IiYXFwg7Jes67aA66eMXFwg
7ZmV7J247ZWY64qUXFwg7Zmc64+Z7J2064ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAgICAgXSwK
ICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAiVmFsaWRhdGlvbuyd
gCDsvZTrlKkg7ZGc7KSAIOykgOyImCDsl6zrtoDrp4wg7ZmV7J247ZWY64qUIO2ZnOuPmeydtOuL
pC4iCiAgICAgICAgXSwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuy9lOuUqSDtkZzspIAg7KSA
7IiY64qUIFZlcmlmaWNhdGlvbuydmCDsnbzrtoDqsIAg65CgIOyImCDsnojsnLzrgpggVmFsaWRh
dGlvbuydgCDthrXtlakg7Iuc7Iqk7YWc7J2YIOyCrOyaqeuqqeyggeqzvCDsgqzsmqnsnpAg7JqU
6rWsIOy2qeyhseydhCDtmZXsnbjtlZzri6QuIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjog
WwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAgICAicmVjb21t
ZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0
X2ZhdGFsX3Ztb2RlbF90ZXN0X2FmdGVyX2NvZGluZyIsCiAgICAgICAgInNldmVyaXR5IjogImZh
dGFsIiwKICAgICAgICAibWVzc2FnZSI6ICJWLU1vZGVs7JeQ7ISc64qUIOuqqOuToCDsvZTrlKns
nbQg64Gd64KcIOuSpOyXkCDsi5ztl5jsnYQg7LKY7J2MIOqzhO2aje2VnOuLpC4iLAogICAgICAg
ICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7Tr
oZwg67O464ukLiBWLU1vZGVs7J2AIOqwnOuwnCDstIjquLDrtoDthLAg6rCBIOyalOq1rOyCrO2V
rcK37ISk6rOEIOuLqOqzhOyXkCDrjIDsnZHtlZjripQg7Iuc7ZeY6rO8IOyImOyaqeq4sOykgOyd
hCDtlajqu5gg7KSA67mE7ZWc64ukLiIsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAg
ICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/VlxcLU1vZGVs7JeQ7ISc64qUXFwg66qo
65OgXFwg7L2U65Sp7J20XFwg64Gd64KcXFwg65Kk7JeQXFwg7Iuc7ZeY7J2EXFwg7LKY7J2MXFwg
6rOE7ZqN7ZWc64ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBs
ZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAiVi1Nb2RlbOyXkOyEnOuKlCDrqqjrk6Ag7L2U
65Sp7J20IOuBneuCnCDrkqTsl5Ag7Iuc7ZeY7J2EIOyymOydjCDqs4Ttmo3tlZzri6QuIgogICAg
ICAgIF0sCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJWLU1vZGVs7J2AIOqwnOuwnCDstIjquLDr
toDthLAg6rCBIOyalOq1rOyCrO2VrcK37ISk6rOEIOuLqOqzhOyXkCDrjIDsnZHtlZjripQg7Iuc
7ZeY6rO8IOyImOyaqeq4sOykgOydhCDtlajqu5gg7KSA67mE7ZWc64ukLiIsCiAgICAgICAgImFm
ZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0s
CiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAg
ICAgICAiaWQiOiAic3cwNF9mYXRhbF9vbmVfd2F5X3J0bV9jb21wbGV0ZSIsCiAgICAgICAgInNl
dmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICLsmpTqtazsgqztla3sl5DshJwg
7Iuc7ZeYIOuyiO2YuOuhnCDtlZwg67KIIOyXsOqysO2VmOuptCDslpHrsKntlqUgUlRN7J20IOyZ
hOyEseuQnOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyj
vOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBSVE3snYAg7JqU6rWs7IKs7ZWt7JeQ7ISc
IOyEpOqzhMK37L2U65Ocwrfsi5ztl5jCt+qysOqzvOuhnOydmCDsiJzrsKntlqXqs7wg7Iuc7ZeY
wrfqsrDqs7zsl5DshJwg7JqU6rWs7IKs7ZWt7Jy866Gc7J2YIOyXreuwqe2WpSDstpTsoIHsnYQg
66qo65GQIOygnOqzte2VtOyVvCDtlZzri6QuIiwKICAgICAgICAid3JvbmdfcGF0dGVybnMiOiBb
CiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT/smpTqtazsgqztla3sl5DshJxc
XCDsi5ztl5hcXCDrsojtmLjroZxcXCDtlZxcXCDrsohcXCDsl7DqsrDtlZjrqbRcXCDslpHrsKnt
lqVcXCBSVE3snbRcXCDsmYTshLHrkJzri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAgICBdLAog
ICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLsmpTqtazsgqztla3s
l5DshJwg7Iuc7ZeYIOuyiO2YuOuhnCDtlZwg67KIIOyXsOqysO2VmOuptCDslpHrsKntlqUgUlRN
7J20IOyZhOyEseuQnOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlJU
TeydgCDsmpTqtazsgqztla3sl5DshJwg7ISk6rOEwrfsvZTrk5zCt+yLnO2XmMK36rKw6rO866Gc
7J2YIOyInOuwqe2WpeqzvCDsi5ztl5jCt+qysOqzvOyXkOyEnCDsmpTqtazsgqztla3snLzroZzs
nZgg7Jet67Cp7ZalIOy2lOyggeydhCDrqqjrkZAg7KCc6rO17ZW07JW8IO2VnOuLpC4iLAogICAg
ICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAg
ICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAg
ICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfdW5pdF90ZXN0X3Byb3Zlc19zeXN0ZW0iLAog
ICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1lc3NhZ2UiOiAi66qo65OgIOuL
qOychOyLnO2XmOydtCDthrXqs7ztlZjrqbQg7Ya17ZWp7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2X
mOydgCDtlYTsmpQg7JeG64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDr
sJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIOuLqOychOyLnO2XmOydgCDs
tZzshowg7ISk6rOE64uo7JyE66W8IOqygOymne2VmOupsCDrqqjrk4gg7IOB7Zi47J6R7Jqp6rO8
IGVuZC10by1lbmQg7JqU6rWs7IKs7ZWt7J2AIO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5zt
l5jsnLzroZwg67OE64+EIO2ZleyduO2VnOuLpC4iLAogICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6
IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCiXVxccyopP+uqqOuToFxcIOuLqOychOyL
nO2XmOydtFxcIO2GteqzvO2VmOuptFxcIO2Gte2VqeyLnO2XmOqzvFxcIOyLnOyKpO2FnOyLnO2X
mOydgFxcIO2VhOyalFxcIOyXhuuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAg
ICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIuuqqOuToCDri6jsnITsi5zt
l5jsnbQg7Ya16rO87ZWY66m0IO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5ztl5jsnYAg7ZWE
7JqUIOyXhuuLpC4iCiAgICAgICAgXSwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuuLqOychOyL
nO2XmOydgCDstZzshowg7ISk6rOE64uo7JyE66W8IOqygOymne2VmOupsCDrqqjrk4gg7IOB7Zi4
7J6R7Jqp6rO8IGVuZC10by1lbmQg7JqU6rWs7IKs7ZWt7J2AIO2Gte2VqeyLnO2XmOqzvCDsi5zs
iqTthZzsi5ztl5jsnLzroZwg67OE64+EIO2ZleyduO2VnOuLpC4iLAogICAgICAgICJhZmZlY3Rl
ZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAg
ICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAg
ImlkIjogInN3MDRfZmF0YWxfc3RhdGljX2FuYWx5c2lzX2V4ZWN1dGVzIiwKICAgICAgICAic2V2
ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIuygleyggeu2hOyEneydgCDtlITr
oZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7JesIOyeheugpeqzvCDstpzroKXsnYQg7Lih7KCV7ZWY64qU
IOyLnO2XmOydtOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yA
IOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDsoJXsoIHrtoTshJ3snYAg7ZSE66Gc
6re4656o7J2EIOyLpO2Wie2VmOyngCDslYrqs6Ag7L2U65OcwrfrqqjrjbjsnZgg6rec7LmZLCDt
nZDrpoQsIOuzteyeoeuPhOyZgCDsnqDsnqzqsrDtlajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAg
ICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxz
Kik/7KCV7KCB67aE7ISd7J2AXFwg7ZSE66Gc6re4656o7J2EXFwg7Iuk7ZaJ7ZWY7JesXFwg7J6F
66Cl6rO8XFwg7Lac66Cl7J2EXFwg7Lih7KCV7ZWY64qUXFwg7Iuc7ZeY7J2064ukXFwuXFxzKlsu
IV0/XFxzKiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAg
ICAgICAgICAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsl6wg7J6F
66Cl6rO8IOy2nOugpeydhCDsuKHsoJXtlZjripQg7Iuc7ZeY7J2064ukLiIKICAgICAgICBdLAog
ICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDs
i6TtlontlZjsp4Ag7JWK6rOgIOy9lOuTnMK366qo64247J2YIOq3nOy5mSwg7Z2Q66aELCDrs7Xs
nqHrj4TsmYAg7J6g7J6s6rKw7ZWo7J2EIOu2hOyEne2VnOuLpC4iLAogICAgICAgICJhZmZlY3Rl
ZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAg
ICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAg
ImlkIjogInN3MDRfZmF0YWxfZHluYW1pY19hbmFseXNpc19ub19leGVjdXRpb24iLAogICAgICAg
ICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1lc3NhZ2UiOiAi64+Z7KCB67aE7ISd7J2A
IO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsp4Ag7JWK64qUIOusuOyEnCDqsoDthqDsnbTri6Qu
IiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0
YWwg7ZuE67O066GcIOuzuOuLpC4g64+Z7KCB67aE7ISd7J2AIOyLpO2WieuQnCDshoztlITtirjs
m6jslrTsnZgg6rK966GcLCDsi5zqsIQsIOyekOybkOqzvCDrsJjsnZHsnYQg7J6F66ClIOyhsOqx
tOuzhOuhnCDqtIDssLDtlZzri6QuIiwKICAgICAgICAid3JvbmdfcGF0dGVybnMiOiBbCiAgICAg
ICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT/rj5nsoIHrtoTshJ3snYBcXCDtlITroZzq
t7jrnqjsnYRcXCDsi6TtlontlZjsp4BcXCDslYrripRcXCDrrLjshJxcXCDqsoDthqDsnbTri6Rc
XC5cXHMqWy4hXT9cXHMqJCIKICAgICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJu
cyI6IFsKICAgICAgICAgICLrj5nsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyLpO2Wie2V
mOyngCDslYrripQg66y47IScIOqygO2GoOydtOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiY29y
cmVjdF9ydWxlIjogIuuPmeyggeu2hOyEneydgCDsi6TtlonrkJwg7IaM7ZSE7Yq47Juo7Ja07J2Y
IOqyveuhnCwg7Iuc6rCELCDsnpDsm5Dqs7wg67CY7J2R7J2EIOyeheugpSDsobDqsbTrs4TroZwg
6rSA7LCw7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJD
IiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmci
OiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9mYXRhbF9yZWdyZXNz
aW9uX25ld19vbmx5IiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNz
YWdlIjogIu2ajOq3gOyLnO2XmOydgCDsg4jroZwg7LaU6rCA65CcIOq4sOuKpeunjCDsi5ztl5jt
lZjrqbQg65Cc64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg
7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIO2ajOq3gOyLnO2XmOydgCDrs4Dqsr0g
6riw64ql6rO8IO2VqOq7mCDsmIHtlqXrsJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64qlwrfs
nbjthLDtjpjsnbTsiqTsnZgg7Jyg7KeAIOyXrOu2gOulvCDtmZXsnbjtlZzri6QuIiwKICAgICAg
ICAid3JvbmdfcGF0dGVybnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMq
KT/tmozqt4Dsi5ztl5jsnYBcXCDsg4jroZxcXCDstpTqsIDrkJxcXCDquLDriqXrp4xcXCDsi5zt
l5jtlZjrqbRcXCDrkJzri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAgICBdLAogICAgICAgICJl
eGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLtmozqt4Dsi5ztl5jsnYAg7IOI66Gc
IOy2lOqwgOuQnCDquLDriqXrp4wg7Iuc7ZeY7ZWY66m0IOuQnOuLpC4iCiAgICAgICAgXSwKICAg
ICAgICAiY29ycmVjdF9ydWxlIjogIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr0g6riw64ql6rO8IO2V
qOq7mCDsmIHtlqXrsJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64qlwrfsnbjthLDtjpjsnbTs
iqTsnZgg7Jyg7KeAIOyXrOu2gOulvCDtmZXsnbjtlZzri6QuIiwKICAgICAgICAiYWZmZWN0ZWRf
bGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAg
ICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJp
ZCI6ICJzdzA0X2ZhdGFsX3NpbXVsYXRpb25faWRlbnRpY2FsX2ZpZWxkIiwKICAgICAgICAic2V2
ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIuyLnOuurOugiOydtOyFmCDqsrDq
s7zripQg7Iuk7KCcIO2YhOyepeqzvCDtla3sg4Eg7JmE7KCE7Z6IIOuPmeydvO2VmOuLpC4iLAog
ICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDt
m4Trs7TroZwg67O464ukLiBTaW11bGF0aW9u7J2AIOuqqOuNuCDquLDrsJjsnbTrr4DroZwg66qo
6424IOqwgOygleqzvCDtlZzqs4Trpbwg7Y+J6rCA7ZWY6rOgIO2VhOyalO2VmOuptCBISUzCt+2Y
hOyepSDri6jqs4TsnZgg7LaU6rCAIOqygOymneycvOuhnCDrs7TsmYTtlZzri6QuIiwKICAgICAg
ICAid3JvbmdfcGF0dGVybnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMq
KT/si5zrrqzroIjsnbTshZhcXCDqsrDqs7zripRcXCDsi6TsoJxcXCDtmITsnqXqs7xcXCDtla3s
g4FcXCDsmYTsoITtnohcXCDrj5nsnbztlZjri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAgICBd
LAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLsi5zrrqzroIjs
nbTshZgg6rKw6rO864qUIOyLpOygnCDtmITsnqXqs7wg7ZWt7IOBIOyZhOyghO2eiCDrj5nsnbzt
lZjri6QuIgogICAgICAgIF0sCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTaW11bGF0aW9u7J2A
IOuqqOuNuCDquLDrsJjsnbTrr4DroZwg66qo6424IOqwgOygleqzvCDtlZzqs4Trpbwg7Y+J6rCA
7ZWY6rOgIO2VhOyalO2VmOuptCBISUzCt+2YhOyepSDri6jqs4TsnZgg7LaU6rCAIOqygOymneyc
vOuhnCDrs7TsmYTtlZzri6QuIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAg
ICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAgICAicmVjb21tZW5kZWRfY2Vp
bGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX2hp
bF9yZXF1aXJlc19yZWFsX3BsYW50IiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAg
ICAgICJtZXNzYWdlIjogIkhJTOydgCDrsJjrk5zsi5wg7Iuk7KCcIOyDneyCsOyEpOu5hOulvCDq
sIDrj5ntlbTslbzrp4wg7IiY7ZaJ7ZWgIOyImCDsnojri6QuIiwKICAgICAgICAiZGVzY3JpcHRp
b24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wg6rKA7Lac7ZWc64ukLiBISUzsnYAg7Iuk
7KCcIOuMgOyDgSDsoJzslrTquLAg65iQ64qUIOyLpOygnCBJL08g7ZWY65Oc7Juo7Ja066W8IOyL
pOyLnOqwhCBQbGFudCBNb2RlbOqzvCDtj5Dro6jtlITroZwg7Jew6rKw7ZWY66+A66GcIOyLpOyg
nCDsg53sgrDshKTruYQg6rCA64+Z7J2AIO2VhOyalO2VmOyngCDslYrri6QuIO2VmOuTnOybqOyW
tCDsl4bripQg7IaM7ZSE7Yq47Juo7Ja0IOyLpO2Wie2ZmOqyvSDsi5ztl5jsnYAgU0lMKFNvZnR3
YXJlLWluLXRoZS1sb29wKSDrmJDripQgVmlydHVhbCBDb21taXNzaW9uaW5n7Jy866GcIOq1rOu2
hO2VnOuLpC4iLAogICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5c
XHMqKD86Wy0q4oCiXVxccyopP0hJTOydgFxcIOuwmOuTnOyLnFxcIOyLpOygnFxcIOyDneyCsOyE
pOu5hOulvFxcIOqwgOuPme2VtOyVvOunjFxcIOyImO2Wie2VoFxcIOyImFxcIOyeiOuLpFxcLlxc
cypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAgICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjog
WwogICAgICAgICAgIkhJTOydgCDrsJjrk5zsi5wg7Iuk7KCcIOyDneyCsOyEpOu5hOulvCDqsIDr
j5ntlbTslbzrp4wg7IiY7ZaJ7ZWgIOyImCDsnojri6QuIgogICAgICAgIF0sCiAgICAgICAgImNv
cnJlY3RfcnVsZSI6ICJISUzsnYAg7Iuk7KCcIOuMgOyDgSDsoJzslrTquLAg65iQ64qUIOyLpOyg
nCBJL08g7ZWY65Oc7Juo7Ja066W8IOyLpOyLnOqwhCBQbGFudCBNb2RlbOqzvCDtj5Dro6jtlITr
oZwg7Jew6rKw7ZWY66+A66GcIOyLpOygnCDsg53sgrDshKTruYQg6rCA64+Z7J2AIO2VhOyalO2V
mOyngCDslYrri6QuIO2VmOuTnOybqOyWtCDsl4bripQg7IaM7ZSE7Yq47Juo7Ja0IOyLpO2Wie2Z
mOqyvSDsi5ztl5jsnYAgU0lMKFNvZnR3YXJlLWluLXRoZS1sb29wKSDrmJDripQgVmlydHVhbCBD
b21taXNzaW9uaW5n7Jy866GcIOq1rOu2hO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXll
cnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJy
ZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjog
InN3MDRfZmF0YWxfZmF1bHRfaW5qZWN0aW9uX25vdF9zb2Z0d2FyZSIsCiAgICAgICAgInNldmVy
aXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICLqsrDtlajso7zsnoXsnYAg7YyM6rS0
7Iuc7ZeY7J2066+A66GcIOyGjO2UhO2KuOybqOyWtCDsi5ztl5jsl5DripQg7IKs7Jqp7ZWgIOyI
mCDsl4bri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zs
nqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gRmF1bHQgaW5qZWN0aW9u7J2AIO2GteygnOuQ
nCDtmZjqsr3sl5DshJwg7IS87IScwrfthrXsi6DCt+yghOybkMK3642w7J207YSwwrd0YXNrIOyd
tOyDgeydhCDso7zsnoXtlbQg6rKA7LacwrfqsqnrpqzCt+uzteq1rOulvCDqsoDspp3tlZzri6Qu
IiwKICAgICAgICAid3JvbmdfcGF0dGVybnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/Olst
KuKAol1cXHMqKT/qsrDtlajso7zsnoXsnYBcXCDtjIzqtLTsi5ztl5jsnbTrr4DroZxcXCDshozt
lITtirjsm6jslrRcXCDsi5ztl5jsl5DripRcXCDsgqzsmqntlaBcXCDsiJhcXCDsl4bri6RcXC5c
XHMqWy4hXT9cXHMqJCIKICAgICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6
IFsKICAgICAgICAgICLqsrDtlajso7zsnoXsnYAg7YyM6rS07Iuc7ZeY7J2066+A66GcIOyGjO2U
hO2KuOybqOyWtCDsi5ztl5jsl5DripQg7IKs7Jqp7ZWgIOyImCDsl4bri6QuIgogICAgICAgIF0s
CiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJGYXVsdCBpbmplY3Rpb27snYAg7Ya17KCc65CcIO2Z
mOqyveyXkOyEnCDshLzshJzCt+2GteyLoMK37KCE7JuQwrfrjbDsnbTthLDCt3Rhc2sg7J207IOB
7J2EIOyjvOyehe2VtCDqsoDstpzCt+qyqeumrMK367O16rWs66W8IOqygOymne2VnOuLpC4iLAog
ICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIK
ICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAog
ICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfY2hhbmdlX2V4cGVjdGVkX3Jlc3VsdCIs
CiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICLsi5ztl5js
nbQg7Iuk7Yyo7ZWY66m0IOyYiOyDgeqysOqzvOulvCDsi6TsoJwg6rKw6rO866GcIOuwlOq+uOyW
tCDthrXqs7wg7LKY66as7ZWY66m0IOuQnOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLr
qoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDsi5ztl5gg
7KCEIOqzoOygle2VnCDsmIjsg4HqsrDqs7zsmYAg7YyQ7KCV6riw7KSA7J2EIOycoOyngO2VmOqz
oCDsi6TtjKjripQg6rKw7ZWoIOuYkOuKlCDsirnsnbjrkJwg7JqU6rWs7IKs7ZWtIOuzgOqyveyc
vOuhnCDstpTsoIHtlbTslbwg7ZWc64ukLiIsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwog
ICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/7Iuc7ZeY7J20XFwg7Iuk7Yyo7ZWY
66m0XFwg7JiI7IOB6rKw6rO866W8XFwg7Iuk7KCcXFwg6rKw6rO866GcXFwg67CU6r647Ja0XFwg
7Ya16rO8XFwg7LKY66as7ZWY66m0XFwg65Cc64ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAgICAg
XSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAi7Iuc7ZeY7J20
IOyLpO2MqO2VmOuptCDsmIjsg4HqsrDqs7zrpbwg7Iuk7KCcIOqysOqzvOuhnCDrsJTqvrjslrQg
7Ya16rO8IOyymOumrO2VmOuptCDrkJzri6QuIgogICAgICAgIF0sCiAgICAgICAgImNvcnJlY3Rf
cnVsZSI6ICLsi5ztl5gg7KCEIOqzoOygle2VnCDsmIjsg4HqsrDqs7zsmYAg7YyQ7KCV6riw7KSA
7J2EIOycoOyngO2VmOqzoCDsi6TtjKjripQg6rKw7ZWoIOuYkOuKlCDsirnsnbjrkJwg7JqU6rWs
7IKs7ZWtIOuzgOqyveycvOuhnCDstpTsoIHtlbTslbwg7ZWc64ukLiIsCiAgICAgICAgImFmZmVj
dGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAg
ICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAg
ICAiaWQiOiAic3cwNF9mYXRhbF9yZXZpZXdfcmVwbGFjZXNfdGVzdCIsCiAgICAgICAgInNldmVy
aXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICLsvZTrk5wg66as67ew66W8IOyImO2W
ie2VmOuptCDrj5nsoIEg7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2XmOydhCDrqqjrkZAg7IOd6561
7ZWgIOyImCDsnojri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuM
gCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gUmV2aWV37JmAIOygleyggeu2hOyE
neydgCDsi6Ttlokg6riw67CYIOyLnO2XmOydhCDrs7TsmYTtlZjsp4Drp4wg64yA7LK07ZWY7KeA
IOyViuycvOupsCDsmpTqtazsgqztla0g7IiY7KSA7JeQIOunnuuKlCDrj5nsoIHCt+2Gte2VqcK3
7Iuc7Iqk7YWcIOyLnO2XmOydtCDtlYTsmpTtlZjri6QuIiwKICAgICAgICAid3JvbmdfcGF0dGVy
bnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT/svZTrk5xcXCDrpqzr
t7DrpbxcXCDsiJjtlontlZjrqbRcXCDrj5nsoIFcXCDsi5ztl5jqs7xcXCDsi5zsiqTthZzsi5zt
l5jsnYRcXCDrqqjrkZBcXCDsg53rnrXtlaBcXCDsiJhcXCDsnojri6RcXC5cXHMqWy4hXT9cXHMq
JCIKICAgICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAg
ICLsvZTrk5wg66as67ew66W8IOyImO2Wie2VmOuptCDrj5nsoIEg7Iuc7ZeY6rO8IOyLnOyKpO2F
nOyLnO2XmOydhCDrqqjrkZAg7IOd65617ZWgIOyImCDsnojri6QuIgogICAgICAgIF0sCiAgICAg
ICAgImNvcnJlY3RfcnVsZSI6ICJSZXZpZXfsmYAg7KCV7KCB67aE7ISd7J2AIOyLpO2WiSDquLDr
sJgg7Iuc7ZeY7J2EIOuztOyZhO2VmOyngOunjCDrjIDssrTtlZjsp4Ag7JWK7Jy866mwIOyalOq1
rOyCrO2VrSDsiJjspIDsl5Ag66ee64qUIOuPmeyggcK37Ya17ZWpwrfsi5zsiqTthZwg7Iuc7ZeY
7J20IO2VhOyalO2VmOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAg
ICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWls
aW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfbm9f
dmVyc2lvbl9uZWVkZWQiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1l
c3NhZ2UiOiAi7Iuc7ZeY6rKw6rO87JeQIOuMgOyDgSDrsoTsoITqs7wg7Iuc7ZeY7ZmY6rK97J2E
IOq4sOuhne2VmOyngCDslYrslYTrj4Qg7J6s7ZiE7ZWgIOyImCDsnojri6QuIiwKICAgICAgICAi
ZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066Gc
IOuzuOuLpC4g7Iuc7ZeY64yA7IOBIGJhc2VsaW5lLCBIV8K3T1PCt2Zpcm13YXJlwrd0b29s6rO8
IOyEpOygleydhCDsi53rs4TtlbTslbwg6rKw6rO87J2YIOyerO2YhOyEseqzvCDqsJDsgqzqsIDr
iqXshLHsnYQg7ZmV67O07ZWgIOyImCDsnojri6QuIiwKICAgICAgICAid3JvbmdfcGF0dGVybnMi
OiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT/si5ztl5jqsrDqs7zsl5Bc
XCDrjIDsg4FcXCDrsoTsoITqs7xcXCDsi5ztl5jtmZjqsr3snYRcXCDquLDroZ3tlZjsp4BcXCDs
lYrslYTrj4RcXCDsnqztmITtlaBcXCDsiJhcXCDsnojri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAg
ICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLsi5zt
l5jqsrDqs7zsl5Ag64yA7IOBIOuyhOyghOqzvCDsi5ztl5jtmZjqsr3snYQg6riw66Gd7ZWY7KeA
IOyViuyVhOuPhCDsnqztmITtlaAg7IiYIOyeiOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiY29y
cmVjdF9ydWxlIjogIuyLnO2XmOuMgOyDgSBiYXNlbGluZSwgSFfCt09TwrdmaXJtd2FyZcK3dG9v
bOqzvCDshKTsoJXsnYQg7Iud67OE7ZW07JW8IOqysOqzvOydmCDsnqztmITshLHqs7wg6rCQ7IKs
6rCA64ql7ISx7J2EIO2ZleuztO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xh
eWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAg
InJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQi
OiAic3cwNF9mYXRhbF9zbWFsbF9jaGFuZ2Vfbm9faW1wYWN0IiwKICAgICAgICAic2V2ZXJpdHki
OiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIuyekeydgCDrs4Dqsr3snYAg7JiB7Zal67aE
7ISd6rO8IO2ajOq3gOyLnO2XmOydhCDtla3sg4Eg7IOd65617ZWgIOyImCDsnojri6QuIiwKICAg
ICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE
67O066GcIOuzuOuLpC4g67OA6rK9IOq3nOuqqOyZgCDrrLTqtIDtlZjqsowg7JiB7Zal67KU7JyE
66W8IO2PieqwgO2VmOqzoCDqt7gg6rKw6rO87JeQIOuUsOudvCBSVE3Ct+yCsOy2nOusvMK37ZqM
6reA7Iuc7ZeYIOuylOychOulvCDqsLHsi6DtlbTslbwg7ZWc64ukLiIsCiAgICAgICAgIndyb25n
X3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/7J6R7J2A
XFwg67OA6rK97J2AXFwg7JiB7Zal67aE7ISd6rO8XFwg7ZqM6reA7Iuc7ZeY7J2EXFwg7ZWt7IOB
XFwg7IOd65617ZWgXFwg7IiYXFwg7J6I64ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAgICAgXSwK
ICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAi7J6R7J2AIOuzgOqy
veydgCDsmIHtlqXrtoTshJ3qs7wg7ZqM6reA7Iuc7ZeY7J2EIO2VreyDgSDsg53rnrXtlaAg7IiY
IOyeiOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuuzgOqyvSDqt5zr
qqjsmYAg66y06rSA7ZWY6rKMIOyYge2WpeuylOychOulvCDtj4nqsIDtlZjqs6Ag6re4IOqysOqz
vOyXkCDrlLDrnbwgUlRNwrfsgrDstpzrrLzCt+2ajOq3gOyLnO2XmCDrspTsnITrpbwg6rCx7Iug
7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAi
QyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5n
IjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfZ2VuZXJh
bF92dl9wcm92ZXNfc2lsIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJt
ZXNzYWdlIjogIuydvOuwmCDshoztlITtirjsm6jslrQgViZW66W8IOyZhOujjO2VmOuptCDrs4Tr
j4QgU2FmZXR5IGxpZmVjeWNsZSDsl4bsnbQgU0lT7J2YIFNJTCDstqnsobHsnbQg7J6Q64+Z7Jy8
66GcIOymneuqheuQnOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY
64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBTVy0wNOydmCDsnbzrsJggViZW
7JmAIFNXLTA17J2YIFNhZmV0eSBJbnRlZ3JpdHksIOuPheumveyEsSwg7LK06rOE7KCBIOqzoOye
pSDthrXsoJzsmYAgU2FmZXR5IFYmVuulvCDqtazrtoTtlbTslbwg7ZWc64ukLiIsCiAgICAgICAg
Indyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/
7J2867CYXFwg7IaM7ZSE7Yq47Juo7Ja0XFwgVlxcJlbrpbxcXCDsmYTro4ztlZjrqbRcXCDrs4Tr
j4RcXCBTYWZldHlcXCBsaWZlY3ljbGVcXCDsl4bsnbRcXCBTSVPsnZhcXCBTSUxcXCDstqnsobHs
nbRcXCDsnpDrj5nsnLzroZxcXCDspp3rqoXrkJzri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAg
ICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLsnbzrsJgg
7IaM7ZSE7Yq47Juo7Ja0IFYmVuulvCDsmYTro4ztlZjrqbQg67OE64+EIFNhZmV0eSBsaWZlY3lj
bGUg7JeG7J20IFNJU+ydmCBTSUwg7Lap7KGx7J20IOyekOuPmeycvOuhnCDspp3rqoXrkJzri6Qu
IgogICAgICAgIF0sCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTVy0wNOydmCDsnbzrsJggViZW
7JmAIFNXLTA17J2YIFNhZmV0eSBJbnRlZ3JpdHksIOuPheumveyEsSwg7LK06rOE7KCBIOqzoOye
pSDthrXsoJzsmYAgU2FmZXR5IFYmVuulvCDqtazrtoTtlbTslbwg7ZWc64ukLiIsCiAgICAgICAg
ImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAg
IF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0KICAgIF0sCiAg
ICAibWFqb3JfY2hlY2tzIjogW10sCiAgICAicXVlc3Rpb25fdHlwZV9jaGVja3MiOiBbXSwKICAg
ICJuZXh0X3ByYWN0aWNlX3BvaW50cyI6IFsKICAgICAgIlYtTW9kZWwg7KKMwrfsmrAg64uo6rOE
IOuMgOydkeydhCDrj4Tsi53snLzroZwg7ISk66qF7ZWc64ukLiIsCiAgICAgICJWZXJpZmljYXRp
b27qs7wgVmFsaWRhdGlvbuydmCDrqqnsoIEg7LCo7J2066W8IOuLteyViCDssqsg67aA67aE7JeQ
7IScIOq1rOu2hO2VnOuLpC4iLAogICAgICAiUlRN7J2YIOyInOuwqe2WpcK37Jet67Cp7ZalIOy2
lOyggeqzvCDqs6DslYQg7IKw7Lac66y8IO2DkOyngOulvCDshKTrqoXtlZzri6QuIiwKICAgICAg
IlNpbXVsYXRpb27Ct0hJTMK3RmF1bHQgaW5qZWN0aW9u7J2YIOyLnO2XmO2ZmOqyveqzvCDtlZzq
s4Trpbwg67mE6rWQ7ZWc64ukLiIsCiAgICAgICLqsrDtlajCt+uzgOqyvcK3YmFzZWxpbmXCt+2a
jOq3gOyLnO2XmMK37Iq57J24IOymneyggeydhCDtlZjrgpjsnZgg7Z2Q66aE7Jy866GcIOyXsOqy
sO2VnOuLpC4iCiAgICBdLAogICAgImRlX2NsYWltX3RydXN0IjogewogICAgICAiZm9ybXVsYV9j
bGFpbXMiOiAibWVkaXVtIiwKICAgICAgImZpZWxkX2NsYWltcyI6ICJtZWRpdW0iCiAgICB9CiAg
fSwKICAibGxtX3Byb2ZpbGUiOiB7CiAgICAiZGlzcGxheV9uYW1lIjogIuqzhOy4oeygnOyWtCDs
hoztlITtirjsm6jslrQg7IiY66qF7KO86riwLCBWLU1vZGVsLCDstpTsoIHshLEsIOqygOymnSDr
sI8g7ZmV7J24IiwKICAgICJkaWZmaWN1bHR5IjogIkRFU0lHTl9FVkFMVUFUSU9OIiwKICAgICJl
bmFibGVkIjogdHJ1ZSwKICAgICJjYXBfcG9saWN5IjogewogICAgICAiZmF0YWxfZGVmYXVsdF9j
ZWlsaW5nIjogMTUuMCwKICAgICAgIm1ham9yX2RlZmF1bHRfY2VpbGluZyI6IDE4LjAsCiAgICAg
ICJmYXRhbF9yZXF1aXJlc19leHBsaWNpdF9jb250cmFkaWN0aW9uIjogdHJ1ZSwKICAgICAgIm9t
aXNzaW9uX2lzX25vdF9mYXRhbCI6IHRydWUKICAgIH0sCiAgICAiY2FuZGlkYXRlX2V4dHJhY3Rp
b24iOiB7CiAgICAgICJ0b3BpY190ZXJtcyI6IFsKICAgICAgICAiaW5zdHJ1bWVudGF0aW9uIGNv
bnRyb2wgc29mdHdhcmUgbGlmZWN5Y2xlIFYtTW9kZWwiLAogICAgICAgICLqs4TsuKHsoJzslrQg
7IaM7ZSE7Yq47Juo7Ja0IOyImOuqheyjvOq4sCBWLU1vZGVsIiwKICAgICAgICAicmVxdWlyZW1l
bnQgYXJjaGl0ZWN0dXJlIGRlc2lnbiBjb2RpbmcgdGVzdCBsaWZlY3ljbGUiLAogICAgICAgICLs
mpTqtazsgqztla0g7JWE7YKk7YWN7LKYIOyDgeyEuOyEpOqzhCDqtaztmIQg7Iuc7ZeYIiwKICAg
ICAgICAidmVyaWZpY2F0aW9uIHZhbGlkYXRpb24gcmVxdWlyZW1lbnQgdHJhY2VhYmlsaXR5IG1h
dHJpeCIsCiAgICAgICAgIuqygOymnSDtmZXsnbgg7JqU6rWs7IKs7ZWtIOy2lOyggeyEsSDrp6Tt
irjrpq3siqQiLAogICAgICAgICJ1bml0IGludGVncmF0aW9uIHN5c3RlbSB0ZXN0IGNvbnRyb2wg
c29mdHdhcmUiLAogICAgICAgICLri6jsnITsi5ztl5gg7Ya17ZWp7Iuc7ZeYIOyLnOyKpO2FnOyL
nO2XmCDsoJzslrQgU1ciLAogICAgICAgICJzdGF0aWMgZHluYW1pYyBhbmFseXNpcyByZWdyZXNz
aW9uIHRlc3QiLAogICAgICAgICLsoJXsoIHrtoTshJ0g64+Z7KCB67aE7ISdIO2ajOq3gOyLnO2X
mCIsCiAgICAgICAgInNpbXVsYXRpb24gSElMIGZhdWx0IGluamVjdGlvbiBzb2Z0d2FyZSB0ZXN0
IiwKICAgICAgICAi7Iuc666s66CI7J207IWYIEhJTCDqsrDtlajso7zsnoUgU1cg7Iuc7ZeYIiwK
ICAgICAgICAic29mdHdhcmUgcmVxdWlyZW1lbnQgdGVzdCBiaWRpcmVjdGlvbmFsIHRyYWNlYWJp
bGl0eSIsCiAgICAgICAgIuyGjO2UhO2KuOybqOyWtCDsmpTqtazsgqztla0g7Iuc7ZeYIOyWkeuw
qe2WpSDstpTsoIHshLEiLAogICAgICAgICJjb2Rpbmcgc3RhbmRhcmQgcmV2aWV3IGRlZmVjdCBt
YW5hZ2VtZW50IiwKICAgICAgICAi7L2U65Sp7ZGc7KSAIOqygO2GoCDqsrDtlajqtIDrpqwiLAog
ICAgICAgICJjb25maWd1cmF0aW9uIGJhc2VsaW5lIGNoYW5nZSBpbXBhY3QgcmVncmVzc2lvbiIs
CiAgICAgICAgIuq1rOyEsSBiYXNlbGluZSDrs4Dqsr0g7JiB7ZalIO2ajOq3gCIsCiAgICAgICAg
ImNvbnRyb2wgc29mdHdhcmUgdmVyaWZpY2F0aW9uIGV2aWRlbmNlIGFwcHJvdmFsIiwKICAgICAg
ICAi7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCBWJlYg7Kad7KCBIOyKueyduCIKICAgICAgXSwKICAg
ICAgImtleV90ZXJtcyI6IFsKICAgICAgICAic29mdHdhcmUgbGlmZWN5Y2xlIiwKICAgICAgICAi
aW5zdHJ1bWVudGF0aW9uIGNvbnRyb2wgc29mdHdhcmUiLAogICAgICAgICJWLU1vZGVsIiwKICAg
ICAgICAicmVxdWlyZW1lbnQgc3BlY2lmaWNhdGlvbiIsCiAgICAgICAgInRlc3RhYmxlIHJlcXVp
cmVtZW50IiwKICAgICAgICAiYWNjZXB0YW5jZSBjcml0ZXJpYSIsCiAgICAgICAgInN5c3RlbSBh
cmNoaXRlY3R1cmUiLAogICAgICAgICJzb2Z0d2FyZSBhcmNoaXRlY3R1cmUiLAogICAgICAgICJk
ZXRhaWxlZCBkZXNpZ24iLAogICAgICAgICJjb2Rpbmcgc3RhbmRhcmQiLAogICAgICAgICJ1bml0
IHRlc3QiLAogICAgICAgICJpbnRlZ3JhdGlvbiB0ZXN0IiwKICAgICAgICAic3lzdGVtIHRlc3Qi
LAogICAgICAgICJ2ZXJpZmljYXRpb24iLAogICAgICAgICJ2YWxpZGF0aW9uIiwKICAgICAgICAi
cmVxdWlyZW1lbnQgdHJhY2VhYmlsaXR5IG1hdHJpeCIsCiAgICAgICAgIlJUTSIsCiAgICAgICAg
ImZvcndhcmQgdHJhY2VhYmlsaXR5IiwKICAgICAgICAiYmFja3dhcmQgdHJhY2VhYmlsaXR5IiwK
ICAgICAgICAiYmlkaXJlY3Rpb25hbCB0cmFjZWFiaWxpdHkiLAogICAgICAgICJzdGF0aWMgYW5h
bHlzaXMiLAogICAgICAgICJjb250cm9sIGZsb3cgYW5hbHlzaXMiLAogICAgICAgICJkYXRhIGZs
b3cgYW5hbHlzaXMiLAogICAgICAgICJkeW5hbWljIGFuYWx5c2lzIiwKICAgICAgICAiZXhlY3V0
aW9uIHBhdGgiLAogICAgICAgICJ0aW1pbmcgYW5hbHlzaXMiLAogICAgICAgICJyZXNvdXJjZSBh
bmFseXNpcyIsCiAgICAgICAgInJlZ3Jlc3Npb24gdGVzdCIsCiAgICAgICAgImNoYW5nZSBpbXBh
Y3QgYW5hbHlzaXMiLAogICAgICAgICJzaW11bGF0aW9uIiwKICAgICAgICAicGxhbnQgbW9kZWwi
LAogICAgICAgICJtb2RlbCBsaW1pdGF0aW9uIiwKICAgICAgICAiaGFyZHdhcmUgaW4gdGhlIGxv
b3AiLAogICAgICAgICJISUwiLAogICAgICAgICJyZWFsLXRpbWUgbW9kZWwiLAogICAgICAgICJj
bG9zZWQgbG9vcCB0ZXN0IiwKICAgICAgICAiZmF1bHQgaW5qZWN0aW9uIiwKICAgICAgICAic2Vu
c29yIGZhdWx0IiwKICAgICAgICAiY29tbXVuaWNhdGlvbiBmYXVsdCIsCiAgICAgICAgInJlY292
ZXJ5IHRlc3QiLAogICAgICAgICJkZWZlY3QgbWFuYWdlbWVudCIsCiAgICAgICAgImNvbmZpZ3Vy
YXRpb24gYmFzZWxpbmUiLAogICAgICAgICJ0ZXN0IGV2aWRlbmNlIiwKICAgICAgICAicmV2aWV3
IGFuZCBhcHByb3ZhbCIsCiAgICAgICAgImV4aXQgY3JpdGVyaWEiCiAgICAgIF0sCiAgICAgICJy
ZXF1aXJlZF9jb250ZXh0X2dyb3VwcyI6IFsKICAgICAgICBbCiAgICAgICAgICAic29mdHdhcmUg
bGlmZWN5Y2xlIiwKICAgICAgICAgICJWLU1vZGVsIiwKICAgICAgICAgICLsmpTqtazsgqztla0i
LAogICAgICAgICAgIuyVhO2CpO2FjeyymCIsCiAgICAgICAgICAi7IOB7IS47ISk6rOEIgogICAg
ICAgIF0sCiAgICAgICAgWwogICAgICAgICAgInZlcmlmaWNhdGlvbiIsCiAgICAgICAgICAidmFs
aWRhdGlvbiIsCiAgICAgICAgICAiUlRNIiwKICAgICAgICAgICLstpTsoIHshLEiLAogICAgICAg
ICAgIuuLqOychOyLnO2XmCIsCiAgICAgICAgICAi7Ya17ZWp7Iuc7ZeYIiwKICAgICAgICAgICLs
i5zsiqTthZzsi5ztl5giCiAgICAgICAgXSwKICAgICAgICBbCiAgICAgICAgICAic3RhdGljIGFu
YWx5c2lzIiwKICAgICAgICAgICJkeW5hbWljIGFuYWx5c2lzIiwKICAgICAgICAgICJyZWdyZXNz
aW9uIHRlc3QiLAogICAgICAgICAgIkhJTCIsCiAgICAgICAgICAiZmF1bHQgaW5qZWN0aW9uIiwK
ICAgICAgICAgICLqsrDtlajqtIDrpqwiCiAgICAgICAgXQogICAgICBdLAogICAgICAiZXhjbHVk
ZV9pZl9vbmx5IjogWwogICAgICAgICJTSUwgUEZEYXZnIFBGSCBzYWZldHkgbGlmZWN5Y2xlIGlu
ZGVwZW5kZW5jZSIsCiAgICAgICAgIuyViOyghOyImOuqheyjvOq4sCDssrTqs4TsoIEg6rOg7J6l
IFNhZmV0eSBWJlYiLAogICAgICAgICJGQVQgU0FUIGNvbW1pc3Npb25pbmcgYWNjZXB0YW5jZSBo
YW5kb3ZlciIsCiAgICAgICAgIu2UhOuhnOygne2KuCDrrLjshJwg7Iuc7Jq07KCEIOyduOyImCIs
CiAgICAgICAgIkhNSSBTQ0FEQSBhbGFybSBtYW5hZ2VtZW50IFNPRSIsCiAgICAgICAgIlNlcXVl
bmNlIHN0YXRlIHRyYW5zaXRpb24gdHJpcCBsYXRjaCByZXNldCIsCiAgICAgICAgImZpZWxkYnVz
IGV0aGVybmV0IHByb3RvY29sIGN5YmVyc2VjdXJpdHkiLAogICAgICAgICLqs7XthrUgUm91dGVy
IOq1rO2YhCIKICAgICAgXSwKICAgICAgIm1pbmltdW1fZGlzdGluY3RfZ3JvdXBzIjogMgogICAg
fSwKICAgICJ0cnV0aF9zY2hlbWEiOiBbCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9zY29w
ZV9nZW5lcmFsX2xpZmVjeWNsZSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTVy0wNOuKlCDs
nbzrsJgg6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtOydmCDsmpTqtazsgqztla0sIOyVhO2C
pO2FjeyymCwg7IOB7IS47ISk6rOELCDqtaztmIQsIOyLnO2XmCwg7LaU7KCB7ISxLCDqsrDtlajq
tIDrpqzsmYAg7Iq57J246rmM7KeA7J2YIOyImOuqheyjvOq4sOulvCDri6Tro6zri6QuIiwKICAg
ICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAg
ImlkIjogInN3MDRfc3cwNV9ib3VuZGFyeSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTSVMg
7JWI7KCEIOyGjO2UhO2KuOybqOyWtOydmCBTYWZldHkgSW50ZWdyaXR5LCDrj4Xrpr3shLEsIOyy
tOqzhOyggSDqs6DsnqUg7Ya17KCc7JmAIFNhZmV0eSBWJlbripQgU1ctMDXroZwg7J206rSA7ZWc
64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7
CiAgICAgICAgImlkIjogInN3MDRfc3cxMF9ib3VuZGFyeSIsCiAgICAgICAgImNvcnJlY3RfcnVs
ZSI6ICJGQVTCt1NBVMK3TG9vcCB0ZXN0wrfsi5zsmrTsoITCt+yEseuKpeyLnO2XmMK3QWNjZXB0
YW5jZcK3SGFuZG92ZXLripQgU1ctMTDsnZgg7ZSE66Gc7KCd7Yq4IOyImO2WiSDrsI8g7J247IiY
IOyYgeyXreydtOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAg
IH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF92X21vZGVsX2RlZmluaXRpb24iLAogICAg
ICAgICJjb3JyZWN0X3J1bGUiOiAiVi1Nb2RlbOydgCDsoozsuKHsnZgg7JqU6rWs7IKs7ZWtwrfs
hKTqs4TCt+q1rO2YhCDri6jqs4TsmYAg7Jqw7Lih7J2YIOuMgOydkSDsi5ztl5jCt+2ZleyduCDr
i6jqs4Trpbwg7Jew6rKw7ZWY6rOgLCDsi5ztl5jquLDspIDsnYQg6rCc67CcIOy0iOq4sOyXkCDs
pIDruYTtlZjripQgbGlmZWN5Y2xlIOuqqOuNuOydtOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9v
cHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X3JlcXVp
cmVtZW50c19zcGVjaWZpY2F0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuyalOq1rOyC
rO2VreydgCDsi53rs4TsnpAsIOq4sOuKpSwg7ISx64qlLCDsnbjthLDtjpjsnbTsiqQsIOyatOyg
hOuqqOuTnCwg7JiI7Jm4wrfqs6DsnqXsnZHri7Xqs7wg7IiY7Jqp6riw7KSA7J2EIO2PrO2VqO2V
mOupsCDrqoXtmZXtlZjqs6Ag7Iuc7ZeYIOqwgOuKpe2VtOyVvCDtlZzri6QuIiwKICAgICAgICAi
ZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjog
InN3MDRfc3lzdGVtX2FyY2hpdGVjdHVyZSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsi5zs
iqTthZwg7JWE7YKk7YWN7LKY64qUIOygnOyWtOq4sCwgSE1JLCDshJzrsoQsIOuEpO2KuOybjO2B
rCwgSS9P7JmAIOyZuOu2gOyLnOyKpO2FnOydmCDquLDriqXrsLDrtoQsIOyduO2EsO2OmOydtOyK
pCwg642w7J207YSw7Z2Q66aE6rO8IOqzoOyepeqyveqzhOulvCDsoJXsnZjtlZzri6QuIiwKICAg
ICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAg
ImlkIjogInN3MDRfc29mdHdhcmVfYXJjaGl0ZWN0dXJlIiwKICAgICAgICAiY29ycmVjdF9ydWxl
IjogIuyGjO2UhO2KuOybqOyWtCDslYTtgqTthY3sspjripQg66qo65OILCDtg5zsiqTtgawsIOyD
ge2DnOq0gOumrCwg642w7J207YSwLCDthrXsi6AsIOynhOuLqOqzvCDsnpDsm5DrsLDrtoTsnZgg
6rWs7KGwIOuwjyDsnbjthLDtjpjsnbTsiqTrpbwg7KCV7J2Y7ZWc64ukLiIsCiAgICAgICAgImZh
dGFsX2lmX29wcG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJz
dzA0X2RldGFpbGVkX2Rlc2lnbiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsg4HshLjshKTq
s4TripQg7JWM6rOg66as7KaYLCDsg4Htg5zsoITsnbQsIEkvTyDsspjrpqwsIOyYiOyZuOyymOum
rCwg642w7J207YSw7ZiVLCDqsr3qs4TsobDqsbTqs7wg66qo65OIIOyduO2EsO2OmOydtOyKpOul
vCDqtaztmIQg6rCA64ql7ZWcIOyImOykgOycvOuhnCDqtazssrTtmZTtlZzri6QuIiwKICAgICAg
ICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDRfY29kaW5nX3N0YW5kYXJkIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuy9lOuU
qSDtkZzspIDsnYAg66qF66qFLCDsnpDro4ztmJUsIOy0iOq4sO2ZlCwg67KU7JyELCDsmIjsmbjs
spjrpqwsIOuzteyeoeuPhCwg6riI7KeA6rWs66y4LCDso7zshJ3qs7wg66as67ewIOq4sOykgOyd
hCDsnbzqtIDrkJjqsowg6rec7KCV7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRl
IjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X2NvbmZpZ3VyYXRp
b25fYmFzZWxpbmUiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7JqU6rWs7IKs7ZWtwrfshKTq
s4TCt+yGjOyKpMK37Iuc7ZeY7KCI7LCowrfrj4TqtazCt+2ZmOqyveydgCDsi53rs4TrkJwgYmFz
ZWxpbmXqs7wg67KE7KCE7Jy866GcIOq0gOumrOuQmOyWtOyVvCDrj5nsnbwg6rKw6rO866W8IOye
rO2YhO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQog
ICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfdW5pdF90ZXN0IiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIuuLqOychOyLnO2XmOydgCDtlajsiJjCt+uqqOuTiMK3RkIg65OxIOy1
nOyGjCDshKTqs4Tri6jsnITsnZgg7KCV7IOBLCDqsr3qs4QsIOyYpOulmCDqsr3roZzsmYAg7J24
7YSw7Y6Y7J207IqkIOqzhOyVveydhCDqsqnrpqztlZjsl6wg6rKA7Kad7ZWc64ukLiIsCiAgICAg
ICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDRfaW50ZWdyYXRpb25fdGVzdCIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLthrXt
lansi5ztl5jsnYAg66qo65OIwrftg5zsiqTtgazCt+2GteyLoMK3642w7J207YSw67Kg7J207Iqk
wrfsnqXsuZgg7J247YSw7Y6Y7J207IqkIOqwhCDrjbDsnbTthLAsIOyInOyEnCwg7YOA7J2067CN
6rO8IOyYpOulmOyghO2MjOulvCDqsoDspp3tlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bw
b3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfc3lzdGVt
X3Rlc3QiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7Iuc7Iqk7YWc7Iuc7ZeY7J2AIO2Gte2V
qeuQnCDsoJzslrQg7IaM7ZSE7Yq47Juo7Ja06rCAIOyLnOyKpO2FnCDsmpTqtazsgqztla0sIOya
tOyghOuqqOuTnCwg7ISx64qlLCDsnqXslaDrs7XqtazsmYAg7Jm467aAIOyduO2EsO2OmOydtOyK
pOulvCDstqnsobHtlZjripTsp4Ag7ZmV7J247ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29w
cG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X3Zlcmlm
aWNhdGlvbl9kZWZpbml0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlZlcmlmaWNhdGlv
buydgCDqsIEg7IKw7Lac66y87J20IO2VtOuLuSDri6jqs4TsnZgg66qF7IS47JmAIOyEpOqzhOq4
sOykgOyXkCDrp57qsowg66eM65Ok7Ja07KGM64qU7KeA66W8IO2ZleyduO2VmOuKlCDtmZzrj5ns
nbTri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAg
ICB7CiAgICAgICAgImlkIjogInN3MDRfdmFsaWRhdGlvbl9kZWZpbml0aW9uIiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIlZhbGlkYXRpb27snYAg7Ya17ZWp65CcIOyLnOyKpO2FnOydtCDsnZjr
j4TrkJwg7IKs7Jqp66qp7KCB6rO8IOyatOyghO2ZmOqyveyXkOyEnCDsgqzsmqnsnpAg7JqU6rWs
66W8IOy2qeyhse2VmOuKlOyngOulvCDtmZXsnbjtlZjripQg7Zmc64+Z7J2064ukLiIsCiAgICAg
ICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDRfdmVyaWZpY2F0aW9uX3ZhbGlkYXRpb25fcmVsYXRpb25zaGlwIiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIlZlcmlmaWNhdGlvbuqzvCBWYWxpZGF0aW9u7J2AIOyDge2YuOuztOyZ
hOyggeydtOupsCDslrTripAg7ZWY64KY7J2YIOyEseqzteydtCDri6Trpbgg7ZWY64KY66W8IOye
kOuPmeycvOuhnCDrs7TsnqXtlZjsp4Ag7JWK64qU64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29w
cG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfcnRtX2Jp
ZGlyZWN0aW9uYWwiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiUmVxdWlyZW1lbnQgVHJhY2Vh
YmlsaXR5IE1hdHJpeOuKlCDsmpTqtazsgqztla3sl5DshJwg7ISk6rOEwrfsvZTrk5zCt+yLnO2X
mMK36rKw6rO866Gc7J2YIOyInOuwqe2WpeqzvCDsi5ztl5jCt+qysOqzvOyXkOyEnCDsmpTqtazs
gqztla3snLzroZzsnZgg7Jet67Cp7ZalIOy2lOyggeydhCDsoJzqs7XtlZzri6QuIiwKICAgICAg
ICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiB0cnVlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQi
OiAic3cwNF9zdGF0aWNfYW5hbHlzaXMiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7KCV7KCB
67aE7ISd7J2AIO2UhOuhnOq3uOueqOydhCDsi6TtlontlZjsp4Ag7JWK6rOgIOq3nOy5meychOuw
mCwg642w7J207YSw7Z2Q66aELCDsoJzslrTtnZDrpoQsIOuzteyeoeuPhCwg66+47LSI6riw7ZmU
7JmAIOyeoOyerCDqsrDtlajsnYQg67aE7ISd7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29w
cG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZHluYW1p
Y19hbmFseXNpcyIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLrj5nsoIHrtoTshJ3snYAg7Iuk
7ZaJ65CcIOyGjO2UhO2KuOybqOyWtOydmCDqsr3roZwsIOyLnOqwhCwg66mU66qo66aswrfsnpDs
m5AsIOyduO2EsO2OmOydtOyKpOyZgCDsi6TsoJwg67CY7J2R7J2EIOyeheugpSDsobDqsbTrs4Tr
oZwg6rSA7LCw7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAg
ICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfcmVncmVzc2lvbl90ZXN0IiwKICAgICAg
ICAiY29ycmVjdF9ydWxlIjogIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr3rkJwg6riw64ql67+QIOyV
hOuLiOudvCDsmIHtlqXrsJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64ql6rO8IOyduO2EsO2O
mOydtOyKpOqwgCDsnKDsp4DrkJjripTsp4Ag67CY67O1IO2ZleyduO2VnOuLpC4iLAogICAgICAg
ICJmYXRhbF9pZl9vcHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6
ICJzdzA0X3NpbXVsYXRpb24iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiU2ltdWxhdGlvbuyd
gCBwbGFudMK3cHJvY2Vzc8K3ZGV2aWNl7J2YIOuqqOuNuOydhCDsgqzsmqntlZjsl6wg64uk7JaR
7ZWcIOygleyDgcK367mE7KCV7IOBIOyLnOuCmOumrOyYpOulvCDrsJjrs7Ug6rKA7Kad7ZWY7KeA
66eMIOuqqOuNuOydmCDqsIDsoJXqs7wg7ZWc6rOE66W8IOq0gOumrO2VtOyVvCDtlZzri6QuIiwK
ICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiB0cnVlCiAgICAgIH0sCiAgICAgIHsKICAgICAg
ICAiaWQiOiAic3cwNF9oaWwiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiSElM7J2AIOyLpOyg
nCDrjIDsg4Eg7KCc7Ja06riwIO2VmOuTnOybqOyWtCDrmJDripQg7Iuk7KCcIEkvTyDtlZjrk5zs
m6jslrTrpbwg7Iuk7Iuc6rCEIFBsYW50IE1vZGVs6rO8IO2PkOujqO2UhOuhnCDsl7DqsrDtlZjs
l6wgSS9PLCB0aW1pbmcsIO2GteyLoOqzvCDsoJzslrTrj5nsnpHsnYQg7Iuc7ZeY7ZWc64ukLiDt
lZjrk5zsm6jslrQg7JeG7J20IOyGjO2UhO2KuOybqOyWtCDsi6TtlontmZjqsr3rp4wg66qo6424
6rO8IOyXsOqysO2VmOuKlCDsi5ztl5jsnYAgU0lMKFNvZnR3YXJlLWluLXRoZS1sb29wKSDrmJDr
ipQgVmlydHVhbCBDb21taXNzaW9uaW5n7Jy866GcIOq1rOu2hO2VnOuLpC4iLAogICAgICAgICJm
YXRhbF9pZl9vcHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJz
dzA0X2ZhdWx0X2luamVjdGlvbiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJGYXVsdCBpbmpl
Y3Rpb27snYAg7IS87ISc64uo7ISgLCDqs6DssKksIO2GteyLoOyngOyXsMK37IaQ7IukLCDsoITs
m5Drs7Xqt4AsIOuNsOydtO2EsOyYpOyXvOqzvCB0YXNrIOydtOyDgSDrk7HsnYQg7J2Y64+E7KCB
7Jy866GcIOyjvOyehe2VtCDqsoDstpzCt+qyqeumrMK367O16rWs66W8IOqygOymne2VnOuLpC4i
LAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAg
ICAgICJpZCI6ICJzdzA0X3Rlc3Rfc3BlY2lmaWNhdGlvbiIsCiAgICAgICAgImNvcnJlY3RfcnVs
ZSI6ICLsi5ztl5jrqoXshLjripQg66qp7KCBLCDsgqzsoITsobDqsbQsIOyeheugpSwg7KCI7LCo
LCDsmIjsg4HqsrDqs7wsIO2XiOyaqeyYpOywqCwg7YyQ7KCV6riw7KSALCDtmZjqsr0sIOymneyg
geqzvCDsmpTqtazsgqztla0g7LC47KGw66W8IO2PrO2VqO2VnOuLpC4iLAogICAgICAgICJmYXRh
bF9pZl9vcHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0
X2NvdmVyYWdlX2V4aXRfY3JpdGVyaWEiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7Iuc7ZeY
IOyZhOujjOuKlCDri6jsiJwg7Iuk7ZaJIOqxtOyImOqwgCDslYTri4jrnbwg7JqU6rWs7IKs7ZWt
wrfsnITtl5jCt+qyveuhnMK37J247YSw7Y6Y7J207IqkIGNvdmVyYWdl7JmAIOuvuO2VtOqysCDq
srDtlagsIGV4aXQgY3JpdGVyaWHrpbwg7ZWo6ruYIO2PieqwgO2VnOuLpC4iLAogICAgICAgICJm
YXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAi
c3cwNF9kZWZlY3RfbWFuYWdlbWVudCIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLqsrDtlajs
nYAg7J6s7ZiE7KGw6rG0LCDsmIHtlqUsIOyLrOqwgeuPhCwg7JuQ7J24LCDsiJjsoJXrsoTsoIQs
IOyerOyLnO2XmOqzvCBjbG9zdXJlIOymneyggeydhCDstpTsoIHtlZjrqbAg7Iuk7Yyo7Iuc7ZeY
7J2EIOyehOydmCDsgq3soJztlZjsp4Ag7JWK64qU64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29w
cG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X2NoYW5n
ZV9pbXBhY3QiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi67OA6rK96rSA66as64qUIOyalOq1
rOyCrO2VrcK37ISk6rOEwrfsvZTrk5wg65iQ64qUIO2ZmOqyvSDrs4Dqsr3sl5Ag64yA7ZW0IOyY
ge2Wpeu2hOyEnSwg7Iq57J24LCBiYXNlbGluZSDqsLHsi6AsIFJUTSDqsLHsi6Dqs7wg7ISg7YOd
65CcIO2ajOq3gOyLnO2XmOydhCDsiJjtlontlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bw
b3NpdGUiOiB0cnVlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9yZXZpZXdf
YXBwcm92YWwiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi6rKA7Yag7JmAIOyKueyduOydgCDs
l63tlaAsIOyeheugpeyekOujjCwg6rKA7Yag6riw7KSALCDsp4DsoIHsgqztla0sIOyhsOy5mO2Z
leyduOqzvCDsirnsnbjqtozsnpDrpbwg67aE66as7ZW0IOqwneq0gOyggSDspp3soIHsnYQg64Ko
6ri064ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAg
ICB7CiAgICAgICAgImlkIjogInN3MDRfdGVzdF9lbnZpcm9ubWVudCIsCiAgICAgICAgImNvcnJl
Y3RfcnVsZSI6ICLsi5ztl5jtmZjqsr3snYAg64yA7IOBIEhXwrdPU8K3ZmlybXdhcmXCt2xpYnJh
cnnCt25ldHdvcmvCt3NjYW4gdGltZcK3SS9PIHNjYWxpbmfqs7wgdG9vbCB2ZXJzaW9u7J2EIOyL
neuzhO2VmOqzoCDsi6TsoJwg7Jq07KCE7ZmY6rK96rO87J2YIOywqOydtOulvCDtj4nqsIDtlZzr
i6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7
CiAgICAgICAgImlkIjogInN3MDRfbGlmZWN5Y2xlX2ZlZWRiYWNrIiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIuyImOuqheyjvOq4sOuKlCDri6jsiJwg7J2867Cp7ZalIOusuOyEnO2dkOumhOyd
tCDslYTri4jrnbwgcmV2aWV3LCBkZWZlY3TsmYAgY2hhbmdlIOqysOqzvOqwgCDshKDtlokg7IKw
7Lac66y86rO8IOyLnO2XmOqzhO2ajeyXkCDtmZjrpZjrkJjripQg7Ya17KCc65CcIOuwmOuzteqz
vOygleydtOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0s
CiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9ldmlkZW5jZV9hbmRfYXVkaXRhYmlsaXR5IiwK
ICAgICAgICAiY29ycmVjdF9ydWxlIjogIlYmViDqsrDqs7zripQg64iE6rCALCDrrLTsl4fsnYQs
IOyWtOuWpCDrsoTsoITqs7wg7ZmY6rK97JeQ7IScLCDslrTrlqQg6riw7KSA7Jy866GcIOyImO2W
ie2WiOuKlOyngCDstpTsoIEg6rCA64ql7ZWcIOymneyggeycvOuhnCDrgqjqsqjslbwg7ZWc64uk
LiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogZmFsc2UKICAgICAgfQogICAgXSwKICAg
ICJmYXRhbF9jb25kaXRpb25zIjogWwogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxf
dmVyaWZpY2F0aW9uX2VxdWFsc192YWxpZGF0aW9uIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0
YWwiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICJWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbuyd
gCDsmYTsoITtnogg6rCZ7J2AIO2ZnOuPmeydtOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUi
OiAiVmVyaWZpY2F0aW9u7J2AIOuLqOqzhCDsgrDstpzrrLzsnZgg66qF7IS4IOygge2VqeyEseyd
hCwgVmFsaWRhdGlvbuydgCDsnZjrj4TrkJwg7IKs7Jqp66qp7KCB6rO8IOyCrOyaqeyekCDsmpTq
tawg7Lap7KGx7J2EIO2ZleyduO2VmOupsCDsg4HtmLjrs7TsmYTsoIHsnbTri6QuIiwKICAgICAg
ICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAg
ICAgXSwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAg
ewogICAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX3ZhbGlkYXRpb25faXNfY29kaW5nX3N0YW5kYXJk
IiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICJW
YWxpZGF0aW9u7J2AIOy9lOuUqSDtkZzspIAg7KSA7IiYIOyXrOu2gOunjCDtmZXsnbjtlZjripQg
7Zmc64+Z7J2064ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsvZTrlKkg7ZGc7KSAIOyk
gOyImOuKlCBWZXJpZmljYXRpb27snZgg7J2867aA6rCAIOuQoCDsiJgg7J6I7Jy864KYIFZhbGlk
YXRpb27snYAg7Ya17ZWpIOyLnOyKpO2FnOydmCDsgqzsmqnrqqnsoIHqs7wg7IKs7Jqp7J6QIOya
lOq1rCDstqnsobHsnYQg7ZmV7J247ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6
IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29t
bWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cw
NF9mYXRhbF92bW9kZWxfdGVzdF9hZnRlcl9jb2RpbmciLAogICAgICAgICJzZXZlcml0eSI6ICJm
YXRhbCIsCiAgICAgICAgIndyb25nX2NsYWltIjogIlYtTW9kZWzsl5DshJzripQg66qo65OgIOy9
lOuUqeydtCDrgZ3rgpwg65Kk7JeQIOyLnO2XmOydhCDsspjsnYwg6rOE7ZqN7ZWc64ukLiIsCiAg
ICAgICAgImNvcnJlY3RfcnVsZSI6ICJWLU1vZGVs7J2AIOqwnOuwnCDstIjquLDrtoDthLAg6rCB
IOyalOq1rOyCrO2VrcK37ISk6rOEIOuLqOqzhOyXkCDrjIDsnZHtlZjripQg7Iuc7ZeY6rO8IOyI
mOyaqeq4sOykgOydhCDtlajqu5gg7KSA67mE7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xh
eWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAg
InJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQi
OiAic3cwNF9mYXRhbF9vbmVfd2F5X3J0bV9jb21wbGV0ZSIsCiAgICAgICAgInNldmVyaXR5Ijog
ImZhdGFsIiwKICAgICAgICAid3JvbmdfY2xhaW0iOiAi7JqU6rWs7IKs7ZWt7JeQ7IScIOyLnO2X
mCDrsojtmLjroZwg7ZWcIOuyiCDsl7DqsrDtlZjrqbQg7JaR67Cp7ZalIFJUTeydtCDsmYTshLHr
kJzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlJUTeydgCDsmpTqtazsgqztla3sl5Ds
hJwg7ISk6rOEwrfsvZTrk5zCt+yLnO2XmMK36rKw6rO866Gc7J2YIOyInOuwqe2WpeqzvCDsi5zt
l5jCt+qysOqzvOyXkOyEnCDsmpTqtazsgqztla3snLzroZzsnZgg7Jet67Cp7ZalIOy2lOyggeyd
hCDrqqjrkZAg7KCc6rO17ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMi
OiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNv
bW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3
MDRfZmF0YWxfdW5pdF90ZXN0X3Byb3Zlc19zeXN0ZW0iLAogICAgICAgICJzZXZlcml0eSI6ICJm
YXRhbCIsCiAgICAgICAgIndyb25nX2NsYWltIjogIuuqqOuToCDri6jsnITsi5ztl5jsnbQg7Ya1
6rO87ZWY66m0IO2Gte2VqeyLnO2XmOqzvCDsi5zsiqTthZzsi5ztl5jsnYAg7ZWE7JqUIOyXhuuL
pC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi64uo7JyE7Iuc7ZeY7J2AIOy1nOyGjCDshKTq
s4Tri6jsnITrpbwg6rKA7Kad7ZWY66mwIOuqqOuTiCDsg4HtmLjsnpHsmqnqs7wgZW5kLXRvLWVu
ZCDsmpTqtazsgqztla3snYAg7Ya17ZWp7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2XmOycvOuhnCDr
s4Trj4Qg7ZmV7J247ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAg
ICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2Nl
aWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9mYXRhbF9z
dGF0aWNfYW5hbHlzaXNfZXhlY3V0ZXMiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAg
ICAgICAgIndyb25nX2NsYWltIjogIuygleyggeu2hOyEneydgCDtlITroZzqt7jrnqjsnYQg7Iuk
7ZaJ7ZWY7JesIOyeheugpeqzvCDstpzroKXsnYQg7Lih7KCV7ZWY64qUIOyLnO2XmOydtOuLpC4i
LAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7KCV7KCB67aE7ISd7J2AIO2UhOuhnOq3uOueqOyd
hCDsi6TtlontlZjsp4Ag7JWK6rOgIOy9lOuTnMK366qo64247J2YIOq3nOy5mSwg7Z2Q66aELCDr
s7XsnqHrj4TsmYAg7J6g7J6s6rKw7ZWo7J2EIOu2hOyEne2VnOuLpC4iLAogICAgICAgICJhZmZl
Y3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAog
ICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAg
ICAgImlkIjogInN3MDRfZmF0YWxfZHluYW1pY19hbmFseXNpc19ub19leGVjdXRpb24iLAogICAg
ICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIndyb25nX2NsYWltIjogIuuPmeyggeu2
hOyEneydgCDtlITroZzqt7jrnqjsnYQg7Iuk7ZaJ7ZWY7KeAIOyViuuKlCDrrLjshJwg6rKA7Yag
7J2064ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLrj5nsoIHrtoTshJ3snYAg7Iuk7ZaJ
65CcIOyGjO2UhO2KuOybqOyWtOydmCDqsr3roZwsIOyLnOqwhCwg7J6Q7JuQ6rO8IOuwmOydkeyd
hCDsnoXroKUg7KGw6rG067OE66GcIOq0gOywsO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9s
YXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAg
ICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDRfZmF0YWxfcmVncmVzc2lvbl9uZXdfb25seSIsCiAgICAgICAgInNldmVyaXR5Ijog
ImZhdGFsIiwKICAgICAgICAid3JvbmdfY2xhaW0iOiAi7ZqM6reA7Iuc7ZeY7J2AIOyDiOuhnCDs
tpTqsIDrkJwg6riw64ql66eMIOyLnO2XmO2VmOuptCDrkJzri6QuIiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr0g6riw64ql6rO8IO2VqOq7mCDsmIHtlqXr
sJvsnYQg7IiYIOyeiOuKlCDquLDsobQg6riw64qlwrfsnbjthLDtjpjsnbTsiqTsnZgg7Jyg7KeA
IOyXrOu2gOulvCDtmZXsnbjtlZzri6QuIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwog
ICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAgICAicmVjb21tZW5k
ZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X2Zh
dGFsX3NpbXVsYXRpb25faWRlbnRpY2FsX2ZpZWxkIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0
YWwiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICLsi5zrrqzroIjsnbTshZgg6rKw6rO864qUIOyL
pOygnCDtmITsnqXqs7wg7ZWt7IOBIOyZhOyghO2eiCDrj5nsnbztlZjri6QuIiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIlNpbXVsYXRpb27snYAg66qo6424IOq4sOuwmOydtOuvgOuhnCDrqqjr
jbgg6rCA7KCV6rO8IO2VnOqzhOulvCDtj4nqsIDtlZjqs6Ag7ZWE7JqU7ZWY66m0IEhJTMK37ZiE
7J6lIOuLqOqzhOydmCDstpTqsIAg6rKA7Kad7Jy866GcIOuztOyZhO2VnOuLpC4iLAogICAgICAg
ICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAg
ICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7
CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfaGlsX3JlcXVpcmVzX3JlYWxfcGxhbnQiLAogICAg
ICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIndyb25nX2NsYWltIjogIkhJTOydgCDr
sJjrk5zsi5wg7Iuk7KCcIOyDneyCsOyEpOu5hOulvCDqsIDrj5ntlbTslbzrp4wg7IiY7ZaJ7ZWg
IOyImCDsnojri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkhJTOydgCDsi6TsoJwg64yA
7IOBIOygnOyWtOq4sCDrmJDripQg7Iuk7KCcIEkvTyDtlZjrk5zsm6jslrTrpbwg7Iuk7Iuc6rCE
IFBsYW50IE1vZGVs6rO8IO2PkOujqO2UhOuhnCDsl7DqsrDtlZjrr4DroZwg7Iuk7KCcIOyDneyC
sOyEpOu5hCDqsIDrj5nsnYAg7ZWE7JqU7ZWY7KeAIOyViuuLpC4g7ZWY65Oc7Juo7Ja0IOyXhuuK
lCDshoztlITtirjsm6jslrQg7Iuk7ZaJ7ZmY6rK9IOyLnO2XmOydgCBTSUwoU29mdHdhcmUtaW4t
dGhlLWxvb3ApIOuYkOuKlCBWaXJ0dWFsIENvbW1pc3Npb25pbmfsnLzroZwg6rWs67aE7ZWc64uk
LiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAg
ICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAg
IH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9mYXRhbF9mYXVsdF9pbmplY3Rpb25fbm90
X3NvZnR3YXJlIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJ3cm9uZ19j
bGFpbSI6ICLqsrDtlajso7zsnoXsnYAg7YyM6rS07Iuc7ZeY7J2066+A66GcIOyGjO2UhO2KuOyb
qOyWtCDsi5ztl5jsl5DripQg7IKs7Jqp7ZWgIOyImCDsl4bri6QuIiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIkZhdWx0IGluamVjdGlvbuydgCDthrXsoJzrkJwg7ZmY6rK97JeQ7IScIOyEvOyE
nMK37Ya17IugwrfsoITsm5DCt+uNsOydtO2EsMK3dGFzayDsnbTsg4HsnYQg7KO87J6F7ZW0IOqy
gOy2nMK36rKp66aswrfrs7Xqtazrpbwg6rKA7Kad7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVk
X2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAg
ICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAi
aWQiOiAic3cwNF9mYXRhbF9jaGFuZ2VfZXhwZWN0ZWRfcmVzdWx0IiwKICAgICAgICAic2V2ZXJp
dHkiOiAiZmF0YWwiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICLsi5ztl5jsnbQg7Iuk7Yyo7ZWY
66m0IOyYiOyDgeqysOqzvOulvCDsi6TsoJwg6rKw6rO866GcIOuwlOq+uOyWtCDthrXqs7wg7LKY
66as7ZWY66m0IOuQnOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7Iuc7ZeYIOyghCDq
s6DsoJXtlZwg7JiI7IOB6rKw6rO87JmAIO2MkOygleq4sOykgOydhCDsnKDsp4DtlZjqs6Ag7Iuk
7Yyo64qUIOqysO2VqCDrmJDripQg7Iq57J2465CcIOyalOq1rOyCrO2VrSDrs4Dqsr3snLzroZwg
7LaU7KCB7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAg
ICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9j
ZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxf
cmV2aWV3X3JlcGxhY2VzX3Rlc3QiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAg
ICAgIndyb25nX2NsYWltIjogIuy9lOuTnCDrpqzrt7Drpbwg7IiY7ZaJ7ZWY66m0IOuPmeyggSDs
i5ztl5jqs7wg7Iuc7Iqk7YWc7Iuc7ZeY7J2EIOuqqOuRkCDsg53rnrXtlaAg7IiYIOyeiOuLpC4i
LAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiUmV2aWV37JmAIOygleyggeu2hOyEneydgCDsi6Tt
lokg6riw67CYIOyLnO2XmOydhCDrs7TsmYTtlZjsp4Drp4wg64yA7LK07ZWY7KeAIOyViuycvOup
sCDsmpTqtazsgqztla0g7IiY7KSA7JeQIOunnuuKlCDrj5nsoIHCt+2Gte2VqcK37Iuc7Iqk7YWc
IOyLnO2XmOydtCDtlYTsmpTtlZjri6QuIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwog
ICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAgICAicmVjb21tZW5k
ZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X2Zh
dGFsX25vX3ZlcnNpb25fbmVlZGVkIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAg
ICAgICJ3cm9uZ19jbGFpbSI6ICLsi5ztl5jqsrDqs7zsl5Ag64yA7IOBIOuyhOyghOqzvCDsi5zt
l5jtmZjqsr3snYQg6riw66Gd7ZWY7KeAIOyViuyVhOuPhCDsnqztmITtlaAg7IiYIOyeiOuLpC4i
LAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7Iuc7ZeY64yA7IOBIGJhc2VsaW5lLCBIV8K3T1PC
t2Zpcm13YXJlwrd0b29s6rO8IOyEpOygleydhCDsi53rs4TtlbTslbwg6rKw6rO87J2YIOyerO2Y
hOyEseqzvCDqsJDsgqzqsIDriqXshLHsnYQg7ZmV67O07ZWgIOyImCDsnojri6QuIiwKICAgICAg
ICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAg
ICAgXSwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAg
ewogICAgICAgICJpZCI6ICJzdzA0X2ZhdGFsX3NtYWxsX2NoYW5nZV9ub19pbXBhY3QiLAogICAg
ICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIndyb25nX2NsYWltIjogIuyekeydgCDr
s4Dqsr3snYAg7JiB7Zal67aE7ISd6rO8IO2ajOq3gOyLnO2XmOydhCDtla3sg4Eg7IOd65617ZWg
IOyImCDsnojri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuuzgOqyvSDqt5zrqqjsmYAg
66y06rSA7ZWY6rKMIOyYge2WpeuylOychOulvCDtj4nqsIDtlZjqs6Ag6re4IOqysOqzvOyXkCDr
lLDrnbwgUlRNwrfsgrDstpzrrLzCt+2ajOq3gOyLnO2XmCDrspTsnITrpbwg6rCx7Iug7ZW07JW8
IO2VnOuLpC4iLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAg
ICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUu
MAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfZmF0YWxfZ2VuZXJhbF92dl9w
cm92ZXNfc2lsIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJ3cm9uZ19j
bGFpbSI6ICLsnbzrsJgg7IaM7ZSE7Yq47Juo7Ja0IFYmVuulvCDsmYTro4ztlZjrqbQg67OE64+E
IFNhZmV0eSBsaWZlY3ljbGUg7JeG7J20IFNJU+ydmCBTSUwg7Lap7KGx7J20IOyekOuPmeycvOuh
nCDspp3rqoXrkJzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlNXLTA07J2YIOydvOuw
mCBWJlbsmYAgU1ctMDXsnZggU2FmZXR5IEludGVncml0eSwg64+F66a97ISxLCDssrTqs4TsoIEg
6rOg7J6lIO2GteygnOyZgCBTYWZldHkgViZW66W8IOq1rOu2hO2VtOyVvCDtlZzri6QuIiwKICAg
ICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAg
ICAgICAgXSwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfQogICAg
XSwKICAgICJzYWZlX2NvbmRpdGlvbnMiOiBbCiAgICAgICJWZXJpZmljYXRpb27qs7wgVmFsaWRh
dGlvbuydgCDsg4HtmLjrs7TsmYTsoIHsnbTrqbAg66qp7KCB7J20IOuLpOultOuLpC4iLAogICAg
ICAiVi1Nb2RlbOydgCDqsJzrsJwg7LSI6riw67aA7YSwIOuMgOydkSDsi5ztl5jqs7wg7IiY7Jqp
6riw7KSA7J2EIOykgOu5hO2VnOuLpC4iLAogICAgICAiUlRN7J2AIOyInOuwqe2WpeqzvCDsl63r
sKntlqUg7LaU7KCB7J2EIOuqqOuRkCDsoJzqs7XtlZzri6QuIiwKICAgICAgIuuLqOychOyLnO2X
mCDthrXqs7zripQg7Ya17ZWp7Iuc7ZeY6rO8IOyLnOyKpO2FnOyLnO2XmOydhCDrjIDssrTtlZjs
p4Ag7JWK64qU64ukLiIsCiAgICAgICLsoJXsoIHrtoTshJ3snYAg7ZSE66Gc6re4656o7J2EIOyL
pO2Wie2VmOyngCDslYrqs6Ag7IiY7ZaJ7ZWc64ukLiIsCiAgICAgICLrj5nsoIHrtoTshJ3snYAg
7Iuk7ZaJIOykkSDqsr3roZwsIOyLnOqwhCwg7J6Q7JuQ6rO8IOuwmOydkeydhCDqtIDssLDtlZzr
i6QuIiwKICAgICAgIu2ajOq3gOyLnO2XmOydgCDrs4Dqsr0g6riw64ql6rO8IOyYge2Wpeuwm+uK
lCDquLDsobQg6riw64ql7J2EIO2VqOq7mCDtmZXsnbjtlZzri6QuIiwKICAgICAgIlNpbXVsYXRp
b27snYAg66qo6424IOqwgOygleqzvCDtlZzqs4Trpbwg6rCA7KeE64ukLiIsCiAgICAgICJISUzs
nYAg7Iuk7KCcIOygnOyWtCBIV+yZgCDsi6Tsi5zqsIQgcGxhbnQg66qo64247J2EIO2PkOujqO2U
hOuhnCDsl7DqsrDtlaAg7IiYIOyeiOuLpC4iLAogICAgICAiRmF1bHQgaW5qZWN0aW9u7J2AIO2G
teygnOuQnCDsi5ztl5jtmZjqsr3sl5DshJwg7J6l7JWgIOqygOy2nOqzvCDrs7Xqtazrpbwg6rKA
7Kad7ZWc64ukLiIsCiAgICAgICLsi5ztl5gg7Iuk7Yyo64qUIOqysO2VqCDrmJDripQg7Iq57J24
65CcIOuzgOqyveycvOuhnCDstpTsoIHtlZzri6QuIiwKICAgICAgIlJldmlld+uKlCDrj5nsoIHs
i5ztl5jsnYQg67O07JmE7ZWY7KeA66eMIOuqqOuRkCDrjIDssrTtlZjsp4Ag7JWK64qU64ukLiIs
CiAgICAgICLsi5ztl5jqsrDqs7zsl5DripQg64yA7IOBIGJhc2VsaW5l6rO8IO2ZmOqyveydhCDq
uLDroZ3tlZzri6QuIiwKICAgICAgIuuzgOqyveydgCDsmIHtlqXrtoTshJ3qs7wg7ZWE7JqU7ZWc
IO2ajOq3gOyLnO2XmOydhCDqsbDsuZzri6QuIiwKICAgICAgIuydvOuwmCBTVyBWJlbsmYAgU0lT
IFNhZmV0eSBWJlbrpbwg6rWs67aE7ZWc64ukLiIsCiAgICAgICJGQVTCt1NBVMK37Iuc7Jq07KCE
wrdBY2NlcHRhbmNl64qUIFNXLTEw7Jy866GcIOydtOq0gO2VnOuLpC4iLAogICAgICAi66qF7IS4
IOygge2VqeyEseqzvCDsgqzsmqnrqqnsoIEg7KCB7ZWp7ISx7J2EIOuqqOuRkCDtmZXsnbjtlbTs
lbwg7ZWc64ukLiIsCiAgICAgICLri6jsiJwg64iE65297J2AIOyngeygkSDrsJjrjIAg7KO87J6l
6rO8IOq1rOu2hO2VnOuLpC4iCiAgICBdLAogICAgIm1ham9yX2NoZWNrcyI6IFsKICAgICAgewog
ICAgICAgICJpZCI6ICJzdzA0X21ham9yX3VudGVzdGFibGVfcmVxdWlyZW1lbnRzIiwKICAgICAg
ICAic2V2ZXJpdHkiOiAibWFqb3IiLAogICAgICAgICJjb25kaXRpb24iOiAi66y47ZWt7J20IOya
lOq1rOyCrO2VrSDrqoXshLjrpbwg7JqU6rWs7ZWY6rOgIOyLneuzhOyekMK37Iuc7ZeYIOqwgOuK
pSDsobDqsbTCt+yImOyaqeq4sOykgOydtCDrtoDsobHtlZwg6rK97JqwIiwKICAgICAgICAibWVz
c2FnZSI6ICLsmpTqtazsgqztla3snYQg64KY7Je07ZaI7Jy864KYIOuqhe2ZleyEsSwg7Iuc7ZeY
IOqwgOuKpeyEsSDrmJDripQg7IiY7Jqp6riw7KSA7J20IOu2gOyhse2VmOuLpC4iLAogICAgICAg
ICJkZXNjcmlwdGlvbiI6ICLsmpTqtazsgqztla3snYAg6riw64qlwrfshLHriqXCt+yduO2EsO2O
mOydtOyKpMK37JiI7Jm47KGw6rG06rO8IOy4oeyglSDqsIDriqXtlZwg7IiY7Jqp6riw7KSA7J2E
IOqwgOyguOyVvCDtlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuyalOq1rOyCrO2V
reydgCDquLDriqXCt+yEseuKpcK37J247YSw7Y6Y7J207IqkwrfsmIjsmbjsobDqsbTqs7wg7Lih
7KCVIOqwgOuKpe2VnCDsiJjsmqnquLDspIDsnYQg6rCA7KC47JW8IO2VnOuLpC4iLAogICAgICAg
ICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAg
ICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwNF9tYWpvcl92bW9kZWxfd2l0
aG91dF9tYXBwaW5nIiwKICAgICAgICAic2V2ZXJpdHkiOiAibWFqb3IiLAogICAgICAgICJjb25k
aXRpb24iOiAiVi1Nb2RlbOydhCDshKTrqoXtlZjrqbTshJwg6rCc67Cc64uo6rOE7JmAIOuMgOyd
kSDsi5ztl5jsnZgg7Jew6rKw7J20IOu2gOyhse2VnCDqsr3smrAiLAogICAgICAgICJtZXNzYWdl
IjogIlYtTW9kZWwg64uo6rOE64qUIOuCmOyXtO2WiOycvOuCmCDsoozCt+yasCDrjIDsnZHqtIDq
s4TsmYAg7KGw6riwIOyLnO2XmOqzhO2ajeydtCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVz
Y3JpcHRpb24iOiAi7JqU6rWs7IKs7ZWtLeyLnOyKpO2FnOyLnO2XmMK3VmFsaWRhdGlvbiwg7JWE
7YKk7YWN7LKYLe2Gte2VqeyLnO2XmCwg7IOB7IS47ISk6rOELeuLqOychOyLnO2XmOydmCDrjIDs
nZHsnYQg7ISk66qF7ZWc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsmpTqtazsgqzt
la0t7Iuc7Iqk7YWc7Iuc7ZeYwrdWYWxpZGF0aW9uLCDslYTtgqTthY3sspgt7Ya17ZWp7Iuc7ZeY
LCDsg4HshLjshKTqs4Qt64uo7JyE7Iuc7ZeY7J2YIOuMgOydkeydhCDshKTrqoXtlZzri6QuIiwK
ICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQi
CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfbWFqb3JfYXJj
aGl0ZWN0dXJlX3dpdGhvdXRfaW50ZXJmYWNlcyIsCiAgICAgICAgInNldmVyaXR5IjogIm1ham9y
IiwKICAgICAgICAiY29uZGl0aW9uIjogIuyLnOyKpO2FnCDrmJDripQgU1cg7JWE7YKk7YWN7LKY
66W8IOyalOq1rO2VmOqzoCDsnbjthLDtjpjsnbTsiqTCt+uNsOydtO2EsO2dkOumhMK36rOg7J6l
6rK96rOE6rCAIOu2gOyhse2VnCDqsr3smrAiLAogICAgICAgICJtZXNzYWdlIjogIuyVhO2CpO2F
jeyymCDqtazshLHsmpTshozripQg7KCc7Iuc7ZaI7Jy864KYIOyduO2EsO2OmOydtOyKpOyZgCDq
s6DsnqXqsr3qs4TqsIAg67aA7KGx7ZWY64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9uIjogIuq4
sOuKpeuwsOu2hOqzvCDtlajqu5gg7J247YSw7Y6Y7J207IqkLCDrjbDsnbTthLDtnZDrpoQsIHRp
bWluZ+qzvCDqs6DsnqXsoITtjIwg6rK96rOE66W8IOygleydmO2VnOuLpC4iLAogICAgICAgICJj
b3JyZWN0X3J1bGUiOiAi6riw64ql67Cw67aE6rO8IO2VqOq7mCDsnbjthLDtjpjsnbTsiqQsIOuN
sOydtO2EsO2dkOumhCwgdGltaW5n6rO8IOqzoOyepeyghO2MjCDqsr3qs4Trpbwg7KCV7J2Y7ZWc
64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAg
ICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X21h
am9yX3Rlc3RfbGV2ZWxzX25vdF9kaXN0aW5jdCIsCiAgICAgICAgInNldmVyaXR5IjogIm1ham9y
IiwKICAgICAgICAiY29uZGl0aW9uIjogIuuLqOychMK37Ya17ZWpwrfsi5zsiqTthZzsi5ztl5js
nYQg7JqU6rWs7ZWY6rOgIOqwgSDsi5ztl5jsnZgg64yA7IOB6rO8IOqysO2VqOycoO2YlSDqtazr
toTsnbQg67aA7KGx7ZWcIOqyveyasCIsCiAgICAgICAgIm1lc3NhZ2UiOiAi7Iuc7ZeY64uo6rOE
66W8IOuCmOyXtO2WiOycvOuCmCDsi5ztl5jrjIDsg4Hqs7wg6rKA7Lac6rKw7ZWo7J2YIOywqOyd
tOqwgCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi64uo7JyE64qUIOy1
nOyGjCDshKTqs4Tri6jsnIQsIO2Gte2VqeydgCDsg4HtmLjsnpHsmqksIOyLnOyKpO2FnOydgCBl
bmQtdG8tZW5kIOyalOq1rOyCrO2VreydhCDqsoDspp3tlZzri6QuIiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIuuLqOychOuKlCDstZzshowg7ISk6rOE64uo7JyELCDthrXtlansnYAg7IOB7Zi4
7J6R7JqpLCDsi5zsiqTthZzsnYAgZW5kLXRvLWVuZCDsmpTqtazsgqztla3snYQg6rKA7Kad7ZWc
64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAg
ICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0X21h
am9yX3Z2X3J0bV93ZWFrIiwKICAgICAgICAic2V2ZXJpdHkiOiAibWFqb3IiLAogICAgICAgICJj
b25kaXRpb24iOiAiVmVyaWZpY2F0aW9uwrdWYWxpZGF0aW9uIOuYkOuKlCDstpTsoIHshLHsnYQg
7JqU6rWs7ZWY6rOgIOuqqeyggcK37JaR67Cp7ZalIOyXsOqysMK37Kad7KCB7J20IOu2gOyhse2V
nCDqsr3smrAiLAogICAgICAgICJtZXNzYWdlIjogIlYmViDrmJDripQgUlRN7J2EIOyWuOq4ie2W
iOycvOuCmCDrqqnsoIEsIOyWkeuwqe2WpSDstpTsoIHqs7wg7Kad7KCBIOyXsOqysOydtCDrtoDs
obHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7IS4IOygge2VqeyEseqzvCDs
gqzsmqnrqqnsoIEg7KCB7ZWp7ISx7J2EIOq1rOu2hO2VmOqzoCBSVE3snLzroZwg7JqU6rWs7IKs
7ZWtLeyEpOqzhC3svZTrk5wt7Iuc7ZeYLeqysOqzvOulvCDslpHrsKntlqUg7Jew6rKw7ZWc64uk
LiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLrqoXshLgg7KCB7ZWp7ISx6rO8IOyCrOyaqeuq
qeyggSDsoIHtlanshLHsnYQg6rWs67aE7ZWY6rOgIFJUTeycvOuhnCDsmpTqtazsgqztla0t7ISk
6rOELey9lOuTnC3si5ztl5gt6rKw6rO866W8IOyWkeuwqe2WpSDsl7DqsrDtlZzri6QuIiwKICAg
ICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAg
ICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDRfbWFqb3JfYW5hbHlz
aXNfcmVncmVzc2lvbl93ZWFrIiwKICAgICAgICAic2V2ZXJpdHkiOiAibWFqb3IiLAogICAgICAg
ICJjb25kaXRpb24iOiAi7KCV7KCBwrfrj5nsoIHCt+2ajOq3gOyLnO2XmOydhCDsmpTqtaztlZjq
s6Ag7Iuk7ZaJ7Jes67aAwrfrs4Dqsr3smIHtlqXCt2NvdmVyYWdl6rCAIOu2gOyhse2VnCDqsr3s
mrAiLAogICAgICAgICJtZXNzYWdlIjogIuu2hOyEncK37ZqM6reA7Iuc7ZeY7J2EIOyWuOq4ie2W
iOycvOuCmCDsi6TtlonquLDrsJgg7LCo7J207JmAIOyYge2WpeuylOychOqwgCDrtoDsobHtlZjr
i6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi7KCV7KCB67aE7ISd6rO8IOuPmeyggeu2hOyE
neydmCDsi6Ttlonsl6zrtoDrpbwg6rWs67aE7ZWY6rOgIOuzgOqyvSDsmIHtlqXsl5Ag6riw67CY
7ZWcIO2ajOq3gOuylOychOulvCDsoJzsi5ztlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxl
IjogIuygleyggeu2hOyEneqzvCDrj5nsoIHrtoTshJ3snZgg7Iuk7ZaJ7Jes67aA66W8IOq1rOu2
hO2VmOqzoCDrs4Dqsr0g7JiB7Zal7JeQIOq4sOuwmO2VnCDtmozqt4DrspTsnITrpbwg7KCc7Iuc
7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAg
ICAgICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzA0
X21ham9yX3NpbV9oaWxfZmF1bHRfd2VhayIsCiAgICAgICAgInNldmVyaXR5IjogIm1ham9yIiwK
ICAgICAgICAiY29uZGl0aW9uIjogIlNpbXVsYXRpb27Ct0hJTMK3RmF1bHQgaW5qZWN0aW9u7J2E
IOyalOq1rO2VmOqzoCDrqqjrjbjtlZzqs4TCt+2PkOujqO2UhMK37J6l7JWg67O16rWs6rCAIOu2
gOyhse2VnCDqsr3smrAiLAogICAgICAgICJtZXNzYWdlIjogIuqzoOq4iSDsi5ztl5jrsKnrspXs
nYQg64KY7Je07ZaI7Jy864KYIO2ZmOqyvSDrjIDtkZzshLHqs7wg7J6l7JWgIOyLnOuCmOumrOyY
pMK367O16rWsIOqygOymneydtCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24i
OiAiU2ltdWxhdGlvbuydmCDrqqjrjbjtlZzqs4QsIEhJTOydmCDsi6TsoJwg7KCc7Ja0IEhXLeyL
pOyLnOqwhCDrqqjrjbgg7Y+Q66Oo7ZSELCDqsrDtlajso7zsnoXsnZgg6rKA7LacwrfqsqnrpqzC
t+uzteq1rOulvCDsl7DqsrDtlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlNpbXVs
YXRpb27snZgg66qo64247ZWc6rOELCBISUzsnZgg7Iuk7KCcIOygnOyWtCBIVy3si6Tsi5zqsIQg
66qo6424IO2PkOujqO2UhCwg6rKw7ZWo7KO87J6F7J2YIOqygOy2nMK36rKp66aswrfrs7Xqtazr
pbwg7Jew6rKw7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAg
ICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJp
ZCI6ICJzdzA0X21ham9yX2RlZmVjdF9jaGFuZ2VfZXZpZGVuY2Vfd2VhayIsCiAgICAgICAgInNl
dmVyaXR5IjogIm1ham9yIiwKICAgICAgICAiY29uZGl0aW9uIjogIuqysO2VqMK367OA6rK9wrfs
irnsnbjqtIDrpqzrpbwg7JqU6rWs7ZWY6rOgIGJhc2VsaW5lwrfsmIHtlqXrtoTshJ3Ct+yerOyL
nO2XmMK3Y2xvc3VyZSDspp3soIHsnbQg67aA7KGx7ZWcIOqyveyasCIsCiAgICAgICAgIm1lc3Nh
Z2UiOiAi6rKw7ZWo6rSA66asIOuYkOuKlCDrs4Dqsr3qtIDrpqzrpbwg7Ja46riJ7ZaI7Jy864KY
IGJhc2VsaW5lLCDsmIHtlqXrtoTshJ3qs7wg7KKF6rKw7Kad7KCB7J20IOu2gOyhse2VmOuLpC4i
LAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLqsrDtlajqs7wg67OA6rK97J2EIOuyhOyghMK3UlRN
wrftmozqt4Dsi5ztl5jCt+yKueyduCDrsI8gY2xvc3VyZSDspp3soIHsnLzroZwg7Jew6rKw7ZWc
64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLqsrDtlajqs7wg67OA6rK97J2EIOuyhOyg
hMK3UlRNwrftmozqt4Dsi5ztl5jCt+yKueyduCDrsI8gY2xvc3VyZSDspp3soIHsnLzroZwg7Jew
6rKw7ZWc64ukLiIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwK
ICAgICAgICAgICJEIgogICAgICAgIF0KICAgICAgfQogICAgXSwKICAgICJmZWVkYmFja190ZW1w
bGF0ZXMiOiB7CiAgICAgICJmYXRhbCI6ICLtlbXsi6wg7IaM7ZSE7Yq47Juo7Ja0IGxpZmVjeWNs
ZSDrmJDripQgViZWIOybkOumrOqwgCDrsJjrjIDroZwg7ISc7Iig65CY7JeI7Iq164uI64ukOiB7
bWVzc2FnZX0iLAogICAgICAibWFqb3IiOiAi6rCc67Cc64uo6rOELCDsi5ztl5jrjIDsnZEg65iQ
64qUIOy2lOyggeyEsSDthrXsoJzqsIAg67aA7KGx7ZWp64uI64ukOiB7bWVzc2FnZX0iLAogICAg
ICAid2FybiI6ICLrrLjtla0g67KU7JyEIOuYkOuKlCDrs7TsobDsobDqsbTsnbQg67aA7KGx7ZWp
64uI64ukOiB7bWVzc2FnZX0iCiAgICB9LAogICAgIm5leHRfcHJhY3RpY2VfcG9pbnRzIjogWwog
ICAgICAi7JqU6rWs7IKs7ZWtLeyEpOqzhC3svZTrk5wt7Iuc7ZeYLeqysOqzvOydmCDslpHrsKnt
lqUgUlRNIOyYiOyLnOulvCDrp4zrk6Dri6QuIiwKICAgICAgIuuLqOychMK37Ya17ZWpwrfsi5zs
iqTthZzsi5ztl5jsnZgg64yA7IOB6rO8IOqygOy2nOqysO2VqOydhCDruYTqtZDtlZzri6QuIiwK
ICAgICAgIuygleyggcK364+Z7KCBwrftmozqt4Dsi5ztl5jsnZgg7LCo7J207JmAIOuzgOqyveyY
ge2WpeydhCDshKTrqoXtlZzri6QuIiwKICAgICAgIlNpbXVsYXRpb27Ct0hJTMK3RmF1bHQgaW5q
ZWN0aW9u7J2EIO2ZmOqyvSDrjIDtkZzshLHqs7wg67O16rWsIOqygOymneycvOuhnCDsl7DqsrDt
lZzri6QuIgogICAgXSwKICAgICJmYWxzZV9wb3NpdGl2ZV9jYXV0aW9ucyI6IFsKICAgICAgIuuL
teyViOydtCDsmKTri7Ug66y47J6l7J2EIOyduOyaqe2VnCDrkqQg66qF7ZmV7Z6IIOu2gOyglcK3
7KCV7KCV7ZWY66m0IGZhdGFs66GcIO2MkOygle2VmOyngCDslYrripTri6QuIiwKICAgICAgIlZl
cmlmaWNhdGlvbiDrmJDripQgVmFsaWRhdGlvbiDspJEg7ZWY64KY6rCAIOusuO2VrSDrspTsnITs
g4Eg7IOd656165CcIOqyg+unjOycvOuhnCBmYXRhbOuhnCDtjJDsoJXtlZjsp4Ag7JWK64qU64uk
LiIsCiAgICAgICJWLU1vZGVs7J2EIOyEoO2YlSDqt7jrprzsnLzroZwg64uo7Iic7ZmU7ZaI642U
652864+EIOyhsOq4sCDsi5ztl5jqs4Ttmo3qs7wg64yA7J2R6rSA6rOE66W8IOyEpOuqhe2VmOup
tCDsp4HsoJEg7Jik64u17Jy866GcIOuztOyngCDslYrripTri6QuIiwKICAgICAgIlJUTeydmCDs
l63rsKntlqXsnbTrnbzripQg7Jqp7Ja06rCAIOyXhuyWtOuPhCDsi5ztl5jqsrDqs7zsl5DshJwg
7JqU6rWs7IKs7ZWt7J2EIO2ZleyduO2VmOuKlCDsnZjrr7jqsIAg67aE66qF7ZWY66m0IOyduOyg
le2VnOuLpC4iLAogICAgICAi7KCV7KCB67aE7ISdIOuPhOq1rOuqheydhCDsoJzsi5ztlZjsp4Ag
7JWK7JWY64uk64qUIOydtOycoOunjOycvOuhnCBtYWpvcuulvCDsoIHsmqntlZjsp4Ag7JWK64qU
64ukLiIsCiAgICAgICJISUwsIFNvZnR3YXJlLWluLXRoZS1sb29w7JmAIFZpcnR1YWwgQ29tbWlz
c2lvbmluZ+ydgCDtlZjrk5zsm6jslrQg7Y+s7ZWoIOyXrOu2gOuhnCDqtazrtoTtlZjrqbAsIOus
uO2VreydtCBTaW11bGF0aW9u66eMIOyalOq1rO2VmOuptCBISUwg64iE65297J2EIGZhdGFs66Gc
IOuztOyngCDslYrripTri6QuIiwKICAgICAgIkZhdWx0IGluamVjdGlvbuydhCDsnbzrtoAg6rOg
7J6l7Jyg7ZiV7Jy866GcIOygnO2VnO2VnCDshKTrqoXsnYAg7KeB7KCRIOuwmOuMgCDso7zsnqXq
s7wg6rWs67aE7ZWc64ukLiIsCiAgICAgICLsnbzrsJggU1cgcmV2aWV37J2YIOuPheumveyEseyd
hCDslrjquIntlbTrj4Qg7J2066W8IFNXLTA1IFNhZmV0eSBpbmRlcGVuZGVuY2Ug7KO87J6l7Jy8
66GcIOyekOuPmSDtmZXrjIDtlZjsp4Ag7JWK64qU64ukLiIsCiAgICAgICJGQVTCt1NBVOulvCBW
LU1vZGVsIOyasOy4oeydmCDtlITroZzsoJ3tirgg7Kad7KCB7Jy866GcIOyXsOqzhO2VnCDshKTr
qoXsnYAgU1ctMTAg6rK96rOE66W8IOy5qOuylO2VnCDqsoPsnLzroZwg67O07KeAIOyViuuKlOuL
pC4iLAogICAgICAi64uo7IicIOyYpO2DiOyekCwg7JiB66y4IOyVveyWtCDrr7jsoITqsJwg65iQ
64qUIOyaqeyWtCDsiJzshJwg7LCo7J2064qUIOuFvOumrOyggSDrsJjrjIAg7KO87J6l6rO8IOq1
rOu2hO2VnOuLpC4iCiAgICBdLAogICAgIm91dHB1dF9jb250cmFjdCI6IHsKICAgICAgInJlcXVp
cmVkX2ZpZWxkcyI6IFsKICAgICAgICAiaWQiLAogICAgICAgICJzZXZlcml0eSIsCiAgICAgICAg
Im1lc3NhZ2UiLAogICAgICAgICJjb3JyZWN0X3J1bGUiLAogICAgICAgICJhZmZlY3RlZF9sYXll
cnMiCiAgICAgIF0sCiAgICAgICJhbGxvd2VkX3NldmVyaXR5IjogWwogICAgICAgICJmYXRhbCIs
CiAgICAgICAgIm1ham9yIiwKICAgICAgICAid2FybiIsCiAgICAgICAgImluZm8iCiAgICAgIF0s
CiAgICAgICJmYXRhbF9yZXF1aXJlc19kaXJlY3Rfb3Bwb3NpdGVfY2xhaW0iOiB0cnVlLAogICAg
ICAiY2l0ZV9hbnN3ZXJfZXZpZGVuY2UiOiB0cnVlCiAgICB9CiAgfSwKICAicmV2aXNpb25fbm90
ZXMiOiBbCiAgICAiU1ctMDQg7J2867CYIOqzhOy4oeygnOyWtCBTVyBsaWZlY3ljbGXqs7wgViZW
IHRydXRoIHNjaGVtYeulvCDsoJXsnZjtlojri6QuIiwKICAgICLsp4HsoJEg67CY64yAIOyjvOye
peunjCBkZXRlcm1pbmlzdGljIGZhdGFsIO2bhOuztOqwgCDrkJjrj4TroZ0gZnVsbC1saW5lIHBh
dHRlcm7snYQg7IKs7Jqp7ZaI64ukLiIsCiAgICAiU1ctMDUgU2FmZXR5IGxpZmVjeWNsZeqzvCBT
Vy0xMCDtlITroZzsoJ3tirgg7J247IiYIOqyveqzhOulvCBmYWxzZS1wb3NpdGl2ZSDquLDspIDs
l5Ag67CY7JiB7ZaI64ukLiIsCiAgICAiMjAyNi0wOC0wNyBMTE0g7J2Y66+4IOqwkOyCrCDsiJjr
pqw6IEhJTCBGYXRhbCBjb3JyZWN0aW9u6rO8IFNJTMK3VmlydHVhbCBDb21taXNzaW9uaW5nIOqy
veqzhOulvCDsnbzsuZjsi5zsvLDri6QuIgogIF0sCiAgInRvcGljX2xhYmVsIjogIlNXLTA0IOqz
hOy4oeygnOyWtCBTVyDsiJjrqoXso7zquLDCt1YtTW9kZWzCt1YmViIKfQo=
PAYLOAD_SW04_04

    write_payload 'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json' 'c90d3b63f6d9eadc1fd16e927475c8e4e8f289a97ad0a9d7b0552c9fe403dbdc' <<'PAYLOAD_SW04_05'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLm1vZGVsX2Fuc3dlci52MSIsCiAgInRv
cGljX2lkIjogImluc3RydW1lbnRhdGlvbl9jb250cm9sX3NvZnR3YXJlX2xpZmVjeWNsZV92X21v
ZGVsX3RyYWNlYWJpbGl0eV92ZXJpZmljYXRpb25fdmFsaWRhdGlvbiIsCiAgInRpdGxlX2tvIjog
IuqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQg7IiY66qF7KO86riwLCBWLU1vZGVsLCDstpTs
oIHshLEsIOqygOymnSDrsI8g7ZmV7J24IiwKICAicXVlc3Rpb25fdHlwZSI6ICJQUk9DRURVUkUi
LAogICJleHBlY3RlZF9xdWVzdGlvbl9wYXR0ZXJucyI6IFsKICAgICLqs4TsuKHsoJzslrQg7IaM
7ZSE7Yq47Juo7Ja0IOyImOuqheyjvOq4sOyZgCBWLU1vZGVs7J2YIOuLqOqzhOuzhCDqtIDqs4Tr
pbwg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAiVmVyaWZpY2F0aW9u6rO8IFZhbGlkYXRpb27snZgg
7LCo7J207JmAIOyggeyaqeuwqeuyleydhCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICLsmpTqtazs
gqztla0g7LaU7KCB7ISxIOunpO2KuOumreyKpOydmCDqtazshLHqs7wg7JaR67Cp7ZalIOy2lOyg
gSDrsKnrspXsnYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAi64uo7JyE7Iuc7ZeYLCDthrXtlans
i5ztl5jqs7wg7Iuc7Iqk7YWc7Iuc7ZeY7J2EIOu5hOq1kO2VmOqzoCDsoIHsmqnsoIjssKjrpbwg
7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAi7KCV7KCB67aE7ISdLCDrj5nsoIHrtoTshJ3qs7wg7ZqM
6reA7Iuc7ZeY7J2YIOuqqeyggeqzvCDssKjsnbTrpbwg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAi
6rOE7Lih7KCc7Ja0IFNXIOyalOq1rOyCrO2VrSDrqoXshLjsmYAg7Iuc7ZeYIOqwgOuKpe2VnCDs
iJjsmqnquLDspIAg7J6R7ISx67Cp67KV7J2EIOyEpOuqhe2VmOyLnOyYpC4iLAogICAgIlNpbXVs
YXRpb24sIEhJTOqzvCBGYXVsdCBpbmplY3Rpb27snZgg7Yq57KeV6rO8IOyggeyaqeuwqeyViOyd
hCDruYTqtZDtlZjsi5zsmKQuIiwKICAgICLsoJzslrQgU1cg6rKw7ZWo6rSA66asLCDrs4Dqsr3s
mIHtlqUg67aE7ISd6rO8IO2ajOq3gOyLnO2XmOydmCDqtIDqs4Trpbwg7ISk66qF7ZWY7Iuc7Jik
LiIsCiAgICAi7IaM7ZSE7Yq47Juo7Ja0IOyVhO2CpO2FjeyymOyZgCDsg4HshLjshKTqs4Qg7IKw
7Lac66y8IOuwjyDqsoDthqDtla3rqqnsnYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAi6rOE7Lih
7KCc7Ja0IFNXIFYmViDspp3soIEsIHJldmlld8K3YXBwcm92YWzsmYAgYmFzZWxpbmUg6rSA66as
67Cp67KV7J2EIOyEpOuqhe2VmOyLnOyYpC4iCiAgXSwKICAicmVjb21tZW5kZWRfb3V0bGluZSI6
IFsKICAgIHsKICAgICAgInNlY3Rpb24iOiAiMS4g67Cw6rK96rO8IFNXLTA0IOyGjOycoOuylOyc
hCIsCiAgICAgICJpbnRlbnQiOiAi7J2867CYIOqzhOy4oeygnOyWtCBTVyBsaWZlY3ljbGXsnZgg
66qp7KCB6rO8IFNXLTA1wrdTVy0xMCDqsr3qs4Trpbwg7KCc7Iuc7ZWc64ukLiIsCiAgICAgICJh
bmNob3JfcmVmcyI6IFsKICAgICAgICAic3cwNF9zY29wZV9nZW5lcmFsX2xpZmVjeWNsZSIsCiAg
ICAgICAgInN3MDRfc3cwNV9ib3VuZGFyeSIsCiAgICAgICAgInN3MDRfc3cxMF9ib3VuZGFyeSIK
ICAgICAgXQogICAgfSwKICAgIHsKICAgICAgInNlY3Rpb24iOiAiMi4g7JqU6rWs7IKs7ZWt6rO8
IFYtTW9kZWwg6rOE7ZqNIiwKICAgICAgImludGVudCI6ICLsi5ztl5gg6rCA64ql7ZWcIOyalOq1
rOyCrO2VreqzvCDsoozCt+yasCDrjIDsnZEg67CPIOyhsOq4sCDsi5ztl5jqs4Ttmo3snYQg7ISk
66qF7ZWc64ukLiIsCiAgICAgICJhbmNob3JfcmVmcyI6IFsKICAgICAgICAic3cwNF92X21vZGVs
X2RlZmluaXRpb24iLAogICAgICAgICJzdzA0X3JlcXVpcmVtZW50c19zcGVjaWZpY2F0aW9uIiwK
ICAgICAgICAic3cwNF90ZXN0X3NwZWNpZmljYXRpb24iCiAgICAgIF0KICAgIH0sCiAgICB7CiAg
ICAgICJzZWN0aW9uIjogIjMuIOyVhO2CpO2FjeyymMK37IOB7IS47ISk6rOEwrfqtaztmIQg7Ya1
7KCcIiwKICAgICAgImludGVudCI6ICLsi5zsiqTthZzCt1NXIOyVhO2CpO2FjeyymCwg7IOB7IS4
7ISk6rOE7JmAIOy9lOuUqe2RnOykgMK3YmFzZWxpbmXsnYQg7Jew6rKw7ZWc64ukLiIsCiAgICAg
ICJhbmNob3JfcmVmcyI6IFsKICAgICAgICAic3cwNF9zeXN0ZW1fYXJjaGl0ZWN0dXJlIiwKICAg
ICAgICAic3cwNF9zb2Z0d2FyZV9hcmNoaXRlY3R1cmUiLAogICAgICAgICJzdzA0X2RldGFpbGVk
X2Rlc2lnbiIsCiAgICAgICAgInN3MDRfY29kaW5nX3N0YW5kYXJkIiwKICAgICAgICAic3cwNF9j
b25maWd1cmF0aW9uX2Jhc2VsaW5lIgogICAgICBdCiAgICB9LAogICAgewogICAgICAic2VjdGlv
biI6ICI0LiDri6jsnITCt+2Gte2VqcK37Iuc7Iqk7YWc7Iuc7ZeYIiwKICAgICAgImludGVudCI6
ICLsi5ztl5jsiJjspIDrs4Qg64yA7IOBLCDqsoDstpzqsrDtlagsIO2ZmOqyveqzvCDsooXro4zq
uLDspIDsnYQg67mE6rWQ7ZWc64ukLiIsCiAgICAgICJhbmNob3JfcmVmcyI6IFsKICAgICAgICAi
c3cwNF91bml0X3Rlc3QiLAogICAgICAgICJzdzA0X2ludGVncmF0aW9uX3Rlc3QiLAogICAgICAg
ICJzdzA0X3N5c3RlbV90ZXN0IiwKICAgICAgICAic3cwNF9jb3ZlcmFnZV9leGl0X2NyaXRlcmlh
IgogICAgICBdCiAgICB9LAogICAgewogICAgICAic2VjdGlvbiI6ICI1LiBWZXJpZmljYXRpb27C
t1ZhbGlkYXRpb27Ct1JUTSIsCiAgICAgICJpbnRlbnQiOiAi66qF7IS4IOygge2VqeyEseqzvCDs
gqzsmqnrqqnsoIEg7KCB7ZWp7ISx7J2EIOq1rOu2hO2VmOqzoCDslpHrsKntlqUg7LaU7KCB7J2E
IOyEpOuqhe2VnOuLpC4iLAogICAgICAiYW5jaG9yX3JlZnMiOiBbCiAgICAgICAgInN3MDRfdmVy
aWZpY2F0aW9uX2RlZmluaXRpb24iLAogICAgICAgICJzdzA0X3ZhbGlkYXRpb25fZGVmaW5pdGlv
biIsCiAgICAgICAgInN3MDRfdmVyaWZpY2F0aW9uX3ZhbGlkYXRpb25fcmVsYXRpb25zaGlwIiwK
ICAgICAgICAic3cwNF9ydG1fYmlkaXJlY3Rpb25hbCIKICAgICAgXQogICAgfSwKICAgIHsKICAg
ICAgInNlY3Rpb24iOiAiNi4g7KCV7KCBwrfrj5nsoIHCt+2ajOq3gOyLnO2XmCIsCiAgICAgICJp
bnRlbnQiOiAi7Iuk7ZaJ7Jes67aALCDqsoDstpzqsrDtlajqs7wg67OA6rK97JiB7ZalIOq4sOuw
mCDtmozqt4DrspTsnITrpbwg7ISk66qF7ZWc64ukLiIsCiAgICAgICJhbmNob3JfcmVmcyI6IFsK
ICAgICAgICAic3cwNF9zdGF0aWNfYW5hbHlzaXMiLAogICAgICAgICJzdzA0X2R5bmFtaWNfYW5h
bHlzaXMiLAogICAgICAgICJzdzA0X3JlZ3Jlc3Npb25fdGVzdCIKICAgICAgXQogICAgfSwKICAg
IHsKICAgICAgInNlY3Rpb24iOiAiNy4gU2ltdWxhdGlvbsK3SElMwrdGYXVsdCBpbmplY3Rpb24i
LAogICAgICAiaW50ZW50IjogIuuqqOuNuCDquLDrsJgg7Iuc7ZeYLCDsi6TsoJwg7KCc7Ja0IEhX
IO2PkOujqO2UhOyZgCDsnqXslaDrs7Xqtawg6rKA7Kad7J2EIOu5hOq1kO2VnOuLpC4iLAogICAg
ICAiYW5jaG9yX3JlZnMiOiBbCiAgICAgICAgInN3MDRfc2ltdWxhdGlvbiIsCiAgICAgICAgInN3
MDRfaGlsIiwKICAgICAgICAic3cwNF9mYXVsdF9pbmplY3Rpb24iLAogICAgICAgICJzdzA0X3Rl
c3RfZW52aXJvbm1lbnQiCiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJzZWN0aW9uIjogIjgu
IOqysO2VqMK367OA6rK9wrfqsoDthqDCt+yKueyduOqzvCDtmZjrpZgiLAogICAgICAiaW50ZW50
IjogIuqysO2VqCBjbG9zdXJlLCDsmIHtlqXrtoTshJ0sIOyerOqygOymnSwg7Iq57J246rO8IOqw
kOyCrOqwgOuKpe2VnCDspp3soIHsnYQg7Jew6rKw7ZWc64ukLiIsCiAgICAgICJhbmNob3JfcmVm
cyI6IFsKICAgICAgICAic3cwNF9kZWZlY3RfbWFuYWdlbWVudCIsCiAgICAgICAgInN3MDRfY2hh
bmdlX2ltcGFjdCIsCiAgICAgICAgInN3MDRfcmV2aWV3X2FwcHJvdmFsIiwKICAgICAgICAic3cw
NF9saWZlY3ljbGVfZmVlZGJhY2siLAogICAgICAgICJzdzA0X2V2aWRlbmNlX2FuZF9hdWRpdGFi
aWxpdHkiCiAgICAgIF0KICAgIH0KICBdLAogICJoaWdoX3Njb3JlX3BvaW50cyI6IFsKICAgICJT
Vy0wNOydmCDsnbzrsJggU1cgbGlmZWN5Y2xl6rO8IFNXLTA1IFNhZmV0eSBsaWZlY3ljbGUsIFNX
LTEwIO2UhOuhnOygne2KuCDsnbjsiJgg6rK96rOE66W8IOuqhe2Zle2eiCDqtazrtoTtlZzri6Qu
IiwKICAgICLsmpTqtazsgqztla3snYQg6riw64qlwrfshLHriqXCt+yduO2EsO2OmOydtOyKpMK3
7JiI7Jm47J2R64u16rO8IOy4oeyglSDqsIDriqXtlZwg7IiY7Jqp6riw7KSA7Jy866GcIOq1rOyE
se2VnOuLpC4iLAogICAgIlYtTW9kZWzsnZgg7KKM7LihIOqwnOuwnOuLqOqzhOyZgCDsmrDsuKEg
7Iuc7ZeY64uo6rOE66W8IOuMgOydkeyLnO2CpOqzoCDsi5ztl5jsnYQg6rCc67CcIOy0iOq4sOyX
kCDqs4Ttmo3tlZzri6QuIiwKICAgICLsi5zsiqTthZwg7JWE7YKk7YWN7LKY7J2YIOq4sOuKpeuw
sOu2hMK37J247YSw7Y6Y7J207IqkwrfrjbDsnbTthLDtnZDrpoTCt+qzoOyepeqyveqzhOulvCDs
hKTrqoXtlZzri6QuIiwKICAgICJTVyDslYTtgqTthY3sspjsmYAg7IOB7IS47ISk6rOE7JeQ7ISc
IOuqqOuTiMK37YOc7Iqk7YGswrfsg4Htg5zCt3RpbWluZ8K37JiI7Jm47LKY66as66W8IOq1rOyy
tO2ZlO2VnOuLpC4iLAogICAgIuy9lOuUqe2RnOykgOqzvCDqtazshLEgYmFzZWxpbmXsnbQg7J28
6rSA7ISxwrfsnqztmITshLHsl5Ag66+47LmY64qUIOyYge2WpeydhCDshKTrqoXtlZzri6QuIiwK
ICAgICLri6jsnITCt+2Gte2VqcK37Iuc7Iqk7YWc7Iuc7ZeY7J2YIOuMgOyDgeqzvCDqsoDstpzq
srDtlajsnYQg67aE66as7ZWc64ukLiIsCiAgICAiVmVyaWZpY2F0aW9u7J2AIOuqheyEuCDsoIHt
lanshLEsIFZhbGlkYXRpb27snYAg7J2Y64+E65CcIOyCrOyaqeuqqeyggSDstqnsobHsnLzroZwg
6rWs67aE7ZWc64ukLiIsCiAgICAiUlRN7J2YIOyInOuwqe2WpcK37Jet67Cp7ZalIOy2lOyggeyc
vOuhnCDriITrnb0g7JqU6rWs7IKs7ZWt6rO8IOqzoOyVhCDsi5ztl5jsnYQg7YOQ7KeA7ZWc64uk
LiIsCiAgICAi7KCV7KCB67aE7ISd7J2AIOu5hOyLpO2WiSwg64+Z7KCB67aE7ISd7J2AIOyLpO2W
iSDquLDrsJjsnbTrnbzripQg7LCo7J2066W8IOyEpOuqhe2VnOuLpC4iLAogICAgIu2ajOq3gOyL
nO2XmCDrspTsnITrpbwg67OA6rK9IOyYge2Wpeu2hOyEneqzvCDquLDsobQg7J247YSw7Y6Y7J20
7IqkIOyYge2WpeycvOuhnCDqsrDsoJXtlZzri6QuIiwKICAgICJTaW11bGF0aW9u7J2YIOuqqOuN
uCDqsIDsoJXqs7wg7ZWc6rOE66W8IOuqheyLnO2VnOuLpC4iLAogICAgIkhJTOydmCDsi6TsoJwg
7KCc7Ja0IEhXLeyLpOyLnOqwhCBwbGFudCBtb2RlbCDtj5Dro6jtlIQg6rWs7KGw66W8IOyEpOuq
he2VnOuLpC4iLAogICAgIkZhdWx0IGluamVjdGlvbuycvOuhnCDqsoDstpzCt+qyqeumrMK367O1
6rWsIOqyveuhnOulvCDqsoDspp3tlZzri6QuIiwKICAgICLsi5ztl5jrqoXshLjsl5Ag7IKs7KCE
7KGw6rG0wrfsnoXroKXCt+yYiOyDgeqysOqzvMK37ZeI7Jqp7Jik7LCowrftjJDsoJXquLDspIDq
s7wg7Kad7KCB7J2EIO2PrO2VqO2VnOuLpC4iLAogICAgImNvdmVyYWdl7JmAIOuvuO2VtOqysCDq
srDtlajsnYQgZXhpdCBjcml0ZXJpYeyZgCDsl7DqsrDtlZzri6QuIiwKICAgICLqsrDtlajCt+uz
gOqyvcK3YmFzZWxpbmXCt1JUTcK37J6s7Iuc7ZeYwrdhcHByb3ZhbOydmCDtj5Dro6jtlITrpbwg
7ISk66qF7ZWc64ukLiIsCiAgICAi64yA7IOBIOuyhOyghMK37ZmY6rK9wrfsiJjtlonsnpDCt+2M
kOygleq4sOykgOydhCBWJlYg7Kad7KCB7Jy866GcIOuCqOq4tOuLpC4iCiAgXSwKICAiY29tbW9u
X21pc3NpbmdfcG9pbnRzIjogWwogICAgIlNXLTA1IFNhZmV0eSBWJlbsmYAgU1ctMTAgRkFUwrdT
QVQg6rK96rOEIiwKICAgICLsi5ztl5gg6rCA64ql7ZWcIOyalOq1rOyCrO2VreqzvCDsiJjsmqnq
uLDspIAiLAogICAgIlYtTW9kZWwg7KKMwrfsmrAg64yA7J2R6rSA6rOEIiwKICAgICLsi5zsiqTt
hZzCt1NXIOyVhO2CpO2FjeyymOydmCDsnbjthLDtjpjsnbTsiqTsmYAg6rOg7J6l6rK96rOEIiwK
ICAgICLsg4HshLjshKTqs4TsnZgg7JiI7Jm4wrfqsr3qs4TsobDqsbQiLAogICAgIuy9lOuUqe2R
nOykgOqzvCDqtazshLEgYmFzZWxpbmUiLAogICAgIuuLqOychMK37Ya17ZWpwrfsi5zsiqTthZzs
i5ztl5gg7LCo7J20IiwKICAgICJWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbiDrqqnsoIEg7LCo
7J20IiwKICAgICJSVE3snZgg7Jet67Cp7ZalIOy2lOyggSIsCiAgICAi7KCV7KCB67aE7ISd6rO8
IOuPmeyggeu2hOyEneydmCDsi6Ttlonsl6zrtoAiLAogICAgIuuzgOqyvSDsmIHtlqUg6riw67CY
IO2ajOq3gOuylOychCIsCiAgICAiU2ltdWxhdGlvbiDrqqjrjbgg7ZWc6rOEIiwKICAgICJISUwg
7Y+Q66Oo7ZSE7JmAIHRpbWluZyIsCiAgICAiRmF1bHQgaW5qZWN0aW9u7J2YIOuzteq1rCDqsoDs
pp0iLAogICAgIuqysO2VqCBjbG9zdXJl7JmAIOyerOyLnO2XmCDspp3soIEiLAogICAgIuyLnO2X
mO2ZmOqyvcK367KE7KCE6rO8IOqwkOyCrOqwgOuKpeyEsSIKICBdLAogICJyb3V0aW5nX2FsaWFz
ZXMiOiBbCiAgICAiaW5zdHJ1bWVudGF0aW9uIGNvbnRyb2wgc29mdHdhcmUgbGlmZWN5Y2xlIFYt
TW9kZWwiLAogICAgIuqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQg7IiY66qF7KO86riwIFYt
TW9kZWwiLAogICAgInJlcXVpcmVtZW50IGFyY2hpdGVjdHVyZSBkZXNpZ24gY29kaW5nIHRlc3Qg
bGlmZWN5Y2xlIiwKICAgICLsmpTqtazsgqztla0g7JWE7YKk7YWN7LKYIOyDgeyEuOyEpOqzhCDq
taztmIQg7Iuc7ZeYIiwKICAgICJ2ZXJpZmljYXRpb24gdmFsaWRhdGlvbiByZXF1aXJlbWVudCB0
cmFjZWFiaWxpdHkgbWF0cml4IiwKICAgICLqsoDspp0g7ZmV7J24IOyalOq1rOyCrO2VrSDstpTs
oIHshLEg66ek7Yq466at7IqkIiwKICAgICJ1bml0IGludGVncmF0aW9uIHN5c3RlbSB0ZXN0IGNv
bnRyb2wgc29mdHdhcmUiLAogICAgIuuLqOychOyLnO2XmCDthrXtlansi5ztl5gg7Iuc7Iqk7YWc
7Iuc7ZeYIOygnOyWtCBTVyIsCiAgICAic3RhdGljIGR5bmFtaWMgYW5hbHlzaXMgcmVncmVzc2lv
biB0ZXN0IiwKICAgICLsoJXsoIHrtoTshJ0g64+Z7KCB67aE7ISdIO2ajOq3gOyLnO2XmCIsCiAg
ICAic2ltdWxhdGlvbiBISUwgZmF1bHQgaW5qZWN0aW9uIHNvZnR3YXJlIHRlc3QiLAogICAgIuyL
nOuurOugiOydtOyFmCBISUwg6rKw7ZWo7KO87J6FIFNXIOyLnO2XmCIsCiAgICAic29mdHdhcmUg
cmVxdWlyZW1lbnQgdGVzdCBiaWRpcmVjdGlvbmFsIHRyYWNlYWJpbGl0eSIsCiAgICAi7IaM7ZSE
7Yq47Juo7Ja0IOyalOq1rOyCrO2VrSDsi5ztl5gg7JaR67Cp7ZalIOy2lOyggeyEsSIsCiAgICAi
Y29kaW5nIHN0YW5kYXJkIHJldmlldyBkZWZlY3QgbWFuYWdlbWVudCIsCiAgICAi7L2U65Sp7ZGc
7KSAIOqygO2GoCDqsrDtlajqtIDrpqwiLAogICAgImNvbmZpZ3VyYXRpb24gYmFzZWxpbmUgY2hh
bmdlIGltcGFjdCByZWdyZXNzaW9uIiwKICAgICLqtazshLEgYmFzZWxpbmUg67OA6rK9IOyYge2W
pSDtmozqt4AiLAogICAgImNvbnRyb2wgc29mdHdhcmUgdmVyaWZpY2F0aW9uIGV2aWRlbmNlIGFw
cHJvdmFsIiwKICAgICLsoJzslrQg7IaM7ZSE7Yq47Juo7Ja0IFYmViDspp3soIEg7Iq57J24Igog
IF0sCiAgInJvdXRpbmdfZmllbGRfcG9pbnRzIjogWwogICAgInNvZnR3YXJlIGxpZmVjeWNsZSIs
CiAgICAiaW5zdHJ1bWVudGF0aW9uIGNvbnRyb2wgc29mdHdhcmUiLAogICAgIlYtTW9kZWwiLAog
ICAgInJlcXVpcmVtZW50IHNwZWNpZmljYXRpb24iLAogICAgInRlc3RhYmxlIHJlcXVpcmVtZW50
IiwKICAgICJhY2NlcHRhbmNlIGNyaXRlcmlhIiwKICAgICJzeXN0ZW0gYXJjaGl0ZWN0dXJlIiwK
ICAgICJzb2Z0d2FyZSBhcmNoaXRlY3R1cmUiLAogICAgImRldGFpbGVkIGRlc2lnbiIsCiAgICAi
Y29kaW5nIHN0YW5kYXJkIiwKICAgICJ1bml0IHRlc3QiLAogICAgImludGVncmF0aW9uIHRlc3Qi
LAogICAgInN5c3RlbSB0ZXN0IiwKICAgICJ2ZXJpZmljYXRpb24iLAogICAgInZhbGlkYXRpb24i
LAogICAgInJlcXVpcmVtZW50IHRyYWNlYWJpbGl0eSBtYXRyaXgiLAogICAgIlJUTSIsCiAgICAi
Zm9yd2FyZCB0cmFjZWFiaWxpdHkiLAogICAgImJhY2t3YXJkIHRyYWNlYWJpbGl0eSIsCiAgICAi
YmlkaXJlY3Rpb25hbCB0cmFjZWFiaWxpdHkiLAogICAgInN0YXRpYyBhbmFseXNpcyIsCiAgICAi
Y29udHJvbCBmbG93IGFuYWx5c2lzIiwKICAgICJkYXRhIGZsb3cgYW5hbHlzaXMiLAogICAgImR5
bmFtaWMgYW5hbHlzaXMiLAogICAgImV4ZWN1dGlvbiBwYXRoIiwKICAgICJ0aW1pbmcgYW5hbHlz
aXMiLAogICAgInJlc291cmNlIGFuYWx5c2lzIiwKICAgICJyZWdyZXNzaW9uIHRlc3QiLAogICAg
ImNoYW5nZSBpbXBhY3QgYW5hbHlzaXMiLAogICAgInNpbXVsYXRpb24iLAogICAgInBsYW50IG1v
ZGVsIiwKICAgICJtb2RlbCBsaW1pdGF0aW9uIiwKICAgICJoYXJkd2FyZSBpbiB0aGUgbG9vcCIs
CiAgICAiSElMIiwKICAgICJyZWFsLXRpbWUgbW9kZWwiLAogICAgImNsb3NlZCBsb29wIHRlc3Qi
LAogICAgImZhdWx0IGluamVjdGlvbiIsCiAgICAic2Vuc29yIGZhdWx0IiwKICAgICJjb21tdW5p
Y2F0aW9uIGZhdWx0IiwKICAgICJyZWNvdmVyeSB0ZXN0IiwKICAgICJkZWZlY3QgbWFuYWdlbWVu
dCIsCiAgICAiY29uZmlndXJhdGlvbiBiYXNlbGluZSIsCiAgICAidGVzdCBldmlkZW5jZSIsCiAg
ICAicmV2aWV3IGFuZCBhcHByb3ZhbCIsCiAgICAiZXhpdCBjcml0ZXJpYSIKICBdLAogICJyZXZp
c2lvbl9ub3RlcyI6IFsKICAgICJWLU1vZGVs6rO8IOyLnO2XmOyImOykgOydmCDrjIDsnZHsnYQg
64u17JWI6rWs7KGwIOykkeyLrOycvOuhnCDsoJXrpqztlojri6QuIiwKICAgICLslpHrsKntlqUg
UlRNLCDrtoTshJ3Ct+2ajOq3gOyLnO2XmOqzvCDqs6DquIkg7Iuc7ZeY7ZmY6rK97J2EIOqzoOuT
neygkCDtj6zsnbjtirjroZwg67CY7JiB7ZaI64ukLiIsCiAgICAiU1ctMDUgU2FmZXR5IGxpZmVj
eWNsZeqzvCBTVy0xMCDtlITroZzsoJ3tirgg7J247IiYIOqyveqzhOulvCDrqoXsi5ztlojri6Qu
IgogIF0KfQo=
PAYLOAD_SW04_05

    write_payload 'rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/topic_importance.json' '378f2bc52f33b32233bc86a262f9ee8dc05c06a01b50366c4a07c27a1d086242' <<'PAYLOAD_SW04_06'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLnRvcGljX2ltcG9ydGFuY2UudjEiLAog
ICJ0b3BpY19pZCI6ICJpbnN0cnVtZW50YXRpb25fY29udHJvbF9zb2Z0d2FyZV9saWZlY3ljbGVf
dl9tb2RlbF90cmFjZWFiaWxpdHlfdmVyaWZpY2F0aW9uX3ZhbGlkYXRpb24iLAogICJkaWZmaWN1
bHR5IjogIkRFU0lHTl9FVkFMVUFUSU9OIiwKICAic2VsZWN0aW9uX2ltcG9ydGFuY2UiOiAiQ09S
RV9NVVNUX1BSRVBBUkUiLAogICJxdWVzdGlvbl90eXBlIjogIlBST0NFRFVSRSIsCiAgImhpZ2hf
YmFuZF91bmxvY2tfY29uZGl0aW9ucyI6IFsKICAgICLsi5ztl5gg6rCA64ql7ZWcIOyalOq1rOyC
rO2VreqzvCBWLU1vZGVsIOyijMK37JqwIOuMgOydkeydhCDshKTrqoXtlZzri6QuIiwKICAgICJW
ZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbuydhCDrqoXshLgg7KCB7ZWp7ISx6rO8IOyCrOyaqeuq
qeyggSDsoIHtlanshLHsnLzroZwg6rWs67aE7ZWc64ukLiIsCiAgICAiUlRN7J2YIOyInOuwqe2W
pcK37Jet67Cp7ZalIOy2lOyggeydhCDshKTqs4TCt+y9lOuTnMK37Iuc7ZeYwrfqsrDqs7zquYzs
p4Ag7Jew6rKw7ZWc64ukLiIsCiAgICAi64uo7JyEwrfthrXtlanCt+yLnOyKpO2FnOyLnO2XmOyd
mCDrjIDsg4Hqs7wg6rKA7Lac6rKw7ZWo7J2EIOq1rOu2hO2VnOuLpC4iLAogICAgIuygleyggcK3
64+Z7KCBwrftmozqt4Dsi5ztl5jsnYQg7Iuk7ZaJ7Jes67aA7JmAIOuzgOqyveyYge2WpSDqtIDs
oJDsl5DshJwg7ISk66qF7ZWc64ukLiIsCiAgICAiU2ltdWxhdGlvbsK3SElMwrdGYXVsdCBpbmpl
Y3Rpb27snZgg7ZmY6rK9LCDtlZzqs4TsmYAg67O16rWs6rKA7Kad7J2EIOu5hOq1kO2VnOuLpC4i
LAogICAgIuqysO2VqMK367OA6rK9wrdiYXNlbGluZcK37ZqM6reAwrfsirnsnbgg7Kad7KCB7J2E
IO2PkOujqO2UhOuhnCDsl7DqsrDtlZzri6QuIiwKICAgICJTVy0wNSBTYWZldHkgbGlmZWN5Y2xl
6rO8IFNXLTEwIO2UhOuhnOygne2KuCDsiJjtlokg6rK96rOE66W8IOy5qOuylO2VmOyngCDslYrr
ipTri6QuIgogIF0sCiAgIm5vdGUiOiAi6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCDsiJjr
qoXso7zquLDsmYAgViZW64qUIOyalOq1rOyCrO2Vreu2gO2EsCDsi5ztl5jCt+yKueyduOq5jOyn
gCDrqqjrk6Ag7IaM7ZSE7Yq47Juo7Ja0IOusuOygnOydmCDqs7XthrUg6riw67CY7J2064ukLiDr
i6jqs4Qg64KY7Je067O064ukIFYtTW9kZWwg64yA7J2RLCDslpHrsKntlqUg7LaU7KCB7ISxLCDs
i5ztl5jsiJjspIDrs4Qg66qp7KCB6rO8IOuzgOqyvcK36rKw7ZWoIO2ZmOulmOulvCDshKTrqoXt
lbTslbwg6rOg65Od7KCQ7J20IOqwgOuKpe2VmOuvgOuhnCDtlbXsi6wg7KSA67mEIFRvcGlj7Jy8
66GcIOu2hOulmO2VnOuLpC4iLAogICJyZXZpc2lvbl9ub3RlcyI6IFsKICAgICLsnbzrsJgg6rOE
7Lih7KCc7Ja0IFNXIGxpZmVjeWNsZeydmCDrgpzsnbTrj4TsmYAg7ISg7YOdIOykkeyalOuPhOul
vCDsoJXsnZjtlojri6QuIiwKICAgICJWLU1vZGVswrdSVE3Ct+yLnO2XmOyghOuetcK36rKw7ZWo
7ZmY66WY66W8IGhpZ2gtYmFuZCDsobDqsbTsnLzroZwg67CY7JiB7ZaI64ukLiIKICBdLAogICJ0
b3BpY19sYWJlbCI6ICJTVy0wNCDqs4TsuKHsoJzslrQgU1cg7IiY66qF7KO86riwwrdWLU1vZGVs
wrdWJlYiCn0K
PAYLOAD_SW04_06

    write_payload 'scripts/test_instrumentation_control_software_lifecycle_v_model.py' 'e1b83c15ee9d86800985a087902362039d171fb71a8d020bd44c254e5e0bf5b9' <<'PAYLOAD_SW04_07'
ZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IGpzb24KaW1wb3J0IHJl
CmltcG9ydCBzeXMKaW1wb3J0IHVuaXR0ZXN0CmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKClRP
UElDX0lEID0gImluc3RydW1lbnRhdGlvbl9jb250cm9sX3NvZnR3YXJlX2xpZmVjeWNsZV92X21v
ZGVsX3RyYWNlYWJpbGl0eV92ZXJpZmljYXRpb25fdmFsaWRhdGlvbiIKUkVQT19ST09UID0gUGF0
aChfX2ZpbGVfXykucmVzb2x2ZSgpLnBhcmVudHNbMV0KVE9QSUNfRElSID0gUkVQT19ST09UIC8g
InJ1YnJpY3MiIC8gInRvcGljX3BhY2tzIiAvIFRPUElDX0lEClNIRUVUID0gUkVQT19ST09UIC8g
ImRvY3MiIC8gInRvcGljX3NoZWV0cyIgLyBmIntUT1BJQ19JRH0ubWQiClJFQURNRSA9IFRPUElD
X0RJUiAvICJSRUFETUUubWQiCkZBQ1QgPSBUT1BJQ19ESVIgLyAiZmFjdF9hbmNob3IuanNvbiIK
TE9HSUMgPSBUT1BJQ19ESVIgLyAibG9naWNfY2hlY2suanNvbiIKTU9ERUwgPSBUT1BJQ19ESVIg
LyAibW9kZWxfYW5zd2VyLmpzb24iCklNUE9SVEFOQ0UgPSBUT1BJQ19ESVIgLyAidG9waWNfaW1w
b3J0YW5jZS5qc29uIgoKUkVRVUlSRURfRklMRVMgPSBbU0hFRVQsIFJFQURNRSwgRkFDVCwgTE9H
SUMsIE1PREVMLCBJTVBPUlRBTkNFXQoKCmRlZiBsb2FkX2pzb24ocGF0aDogUGF0aCkgLT4gZGlj
dDoKICAgIHJldHVybiBqc29uLmxvYWRzKHBhdGgucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIp
KQoKCmNsYXNzIFRvcGljUGFja1N0cnVjdHVyZVRlc3RzKHVuaXR0ZXN0LlRlc3RDYXNlKToKICAg
IEBjbGFzc21ldGhvZAogICAgZGVmIHNldFVwQ2xhc3MoY2xzKSAtPiBOb25lOgogICAgICAgIGNs
cy5mYWN0ID0gbG9hZF9qc29uKEZBQ1QpCiAgICAgICAgY2xzLmxvZ2ljID0gbG9hZF9qc29uKExP
R0lDKQogICAgICAgIGNscy5tb2RlbCA9IGxvYWRfanNvbihNT0RFTCkKICAgICAgICBjbHMuaW1w
b3J0YW5jZSA9IGxvYWRfanNvbihJTVBPUlRBTkNFKQoKICAgIGRlZiB0ZXN0X3JlcXVpcmVkX2Zp
bGVzX2V4aXN0KHNlbGYpIC0+IE5vbmU6CiAgICAgICAgZm9yIHBhdGggaW4gUkVRVUlSRURfRklM
RVM6CiAgICAgICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShwYXRoLmlzX2ZpbGUoKSwgcGF0aCkKCiAg
ICBkZWYgdGVzdF90b3BpY19pZF9hbmRfc2NoZW1hX2NvbnRyYWN0KHNlbGYpIC0+IE5vbmU6CiAg
ICAgICAgZXhwZWN0ZWQgPSB7CiAgICAgICAgICAgIEZBQ1Q6ICJ0b3BpY19wYWNrLmZhY3RfYW5j
aG9yLnYxIiwKICAgICAgICAgICAgTE9HSUM6ICJ0b3BpY19wYWNrLmxvZ2ljX2NoZWNrLnYxIiwK
ICAgICAgICAgICAgTU9ERUw6ICJ0b3BpY19wYWNrLm1vZGVsX2Fuc3dlci52MSIsCiAgICAgICAg
ICAgIElNUE9SVEFOQ0U6ICJ0b3BpY19wYWNrLnRvcGljX2ltcG9ydGFuY2UudjEiLAogICAgICAg
IH0KICAgICAgICBmb3IgcGF0aCwgc2NoZW1hIGluIGV4cGVjdGVkLml0ZW1zKCk6CiAgICAgICAg
ICAgIGRhdGEgPSBsb2FkX2pzb24ocGF0aCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChk
YXRhWyJ0b3BpY19pZCJdLCBUT1BJQ19JRCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChk
YXRhWyJzY2hlbWFfdmVyc2lvbiJdLCBzY2hlbWEpCgogICAgZGVmIHRlc3RfYW5jaG9yX2NvdW50
X2FuZF91bmlxdWVuZXNzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYW5jaG9ycyA9IHNlbGYuZmFj
dFsiYW5jaG9ycyJdCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4oYW5jaG9ycyksIDMxKQog
ICAgICAgIGlkcyA9IFtpdGVtWyJpZCJdIGZvciBpdGVtIGluIGFuY2hvcnNdCiAgICAgICAgc2Vs
Zi5hc3NlcnRFcXVhbChsZW4oaWRzKSwgbGVuKHNldChpZHMpKSkKICAgICAgICBzZWxmLmFzc2Vy
dEVxdWFsKHNlbGYuZmFjdFsiY29yZV9mYWN0cyJdLCBbaXRlbVsic3RhdGVtZW50Il0gZm9yIGl0
ZW0gaW4gYW5jaG9yc10pCgogICAgZGVmIHRlc3RfZmF0YWxfY291bnRfYW5kX3NoYXBlKHNlbGYp
IC0+IE5vbmU6CiAgICAgICAgZmF0YWxzID0gc2VsZi5mYWN0WyJmYXRhbF93cm9uZ19jbGFpbXMi
XQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwobGVuKGZhdGFscyksIDE2KQogICAgICAgIHNlbGYu
YXNzZXJ0RXF1YWwobGVuKHNlbGYubG9naWNbImRldGVybWluaXN0aWNfY2hlY2tzIl1bImZhdGFs
X2NoZWNrcyJdKSwgMTYpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4oc2VsZi5sb2dpY1si
bGxtX3Byb2ZpbGUiXVsiZmF0YWxfY29uZGl0aW9ucyJdKSwgMTYpCiAgICAgICAgZm9yIGl0ZW0g
aW4gZmF0YWxzOgogICAgICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGl0ZW1bInNldmVyaXR5Il0s
ICJmYXRhbCIpCiAgICAgICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShpdGVtWyJ3cm9uZ19jbGFpbSJd
KQogICAgICAgICAgICBzZWxmLmFzc2VydFRydWUoaXRlbVsiY29ycmVjdF9ydWxlIl0pCgogICAg
ZGVmIHRlc3RfbG9naWNfcHJvZmlsZV9jb250cmFjdChzZWxmKSAtPiBOb25lOgogICAgICAgIHBy
b2ZpbGUgPSBzZWxmLmxvZ2ljWyJsbG1fcHJvZmlsZSJdCiAgICAgICAgc2VsZi5hc3NlcnRUcnVl
KHByb2ZpbGVbImVuYWJsZWQiXSkKICAgICAgICBzZWxmLmFzc2VydFRydWUocHJvZmlsZVsiY2Fw
X3BvbGljeSJdWyJmYXRhbF9yZXF1aXJlc19leHBsaWNpdF9jb250cmFkaWN0aW9uIl0pCiAgICAg
ICAgc2VsZi5hc3NlcnRUcnVlKHByb2ZpbGVbImNhcF9wb2xpY3kiXVsib21pc3Npb25faXNfbm90
X2ZhdGFsIl0pCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4ocHJvZmlsZVsidHJ1dGhfc2No
ZW1hIl0pLCAzMSkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihwcm9maWxlWyJtYWpvcl9j
aGVja3MiXSksIDgpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4ocHJvZmlsZVsiZmFsc2Vf
cG9zaXRpdmVfY2F1dGlvbnMiXSksIDEwKQoKICAgIGRlZiB0ZXN0X21vZGVsX3JlZmVyZW5jZXNf
YXJlX3ZhbGlkKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYW5jaG9yX2lkcyA9IHtpdGVtWyJpZCJd
IGZvciBpdGVtIGluIHNlbGYuZmFjdFsiYW5jaG9ycyJdfQogICAgICAgIHJlZnMgPSB7CiAgICAg
ICAgICAgIHJlZgogICAgICAgICAgICBmb3Igc2VjdGlvbiBpbiBzZWxmLm1vZGVsWyJyZWNvbW1l
bmRlZF9vdXRsaW5lIl0KICAgICAgICAgICAgZm9yIHJlZiBpbiBzZWN0aW9uWyJhbmNob3JfcmVm
cyJdCiAgICAgICAgfQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShyZWZzKQogICAgICAgIHNlbGYu
YXNzZXJ0VHJ1ZShyZWZzIDw9IGFuY2hvcl9pZHMpCgogICAgZGVmIHRlc3RfcmVxdWlyZWRfc2Vt
YW50aWNfZ3JvdXBzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgc3RhdGVtZW50cyA9ICIgIi5qb2lu
KHNlbGYuZmFjdFsiY29yZV9mYWN0cyJdKS5sb3dlcigpCiAgICAgICAgZm9yIHRlcm1zIGluICgK
ICAgICAgICAgICAgKCJ2LW1vZGVsIiwgIuyalOq1rOyCrO2VrSIsICLsi5ztl5giKSwKICAgICAg
ICAgICAgKCJ2ZXJpZmljYXRpb24iLCAidmFsaWRhdGlvbiIsICJydG0iKSwKICAgICAgICAgICAg
KCLri6jsnITsi5ztl5giLCAi7Ya17ZWp7Iuc7ZeYIiwgIuyLnOyKpO2FnOyLnO2XmCIpLAogICAg
ICAgICAgICAoIuygleyggeu2hOyEnSIsICLrj5nsoIHrtoTshJ0iLCAi7ZqM6reA7Iuc7ZeYIiks
CiAgICAgICAgICAgICgic2ltdWxhdGlvbiIsICJoaWwiLCAiZmF1bHQgaW5qZWN0aW9uIiksCiAg
ICAgICAgICAgICgi6rKw7ZWo6rSA66asIiwgIuuzgOqyveq0gOumrCIsICJiYXNlbGluZSIpLAog
ICAgICAgICk6CiAgICAgICAgICAgIGZvciB0ZXJtIGluIHRlcm1zOgogICAgICAgICAgICAgICAg
c2VsZi5hc3NlcnRJbih0ZXJtLmxvd2VyKCksIHN0YXRlbWVudHMpCgogICAgZGVmIHRlc3Rfcm91
dGluZ19jb3VudHNfYW5kX25vX2Jyb2FkX2FsaWFzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYWxp
YXNlcyA9IHNlbGYubW9kZWxbInJvdXRpbmdfYWxpYXNlcyJdCiAgICAgICAgZmllbGRzID0gc2Vs
Zi5tb2RlbFsicm91dGluZ19maWVsZF9wb2ludHMiXQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwo
bGVuKGFsaWFzZXMpLCAyMCkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihmaWVsZHMpLCA0
NSkKICAgICAgICBmb3JiaWRkZW4gPSB7InNvZnR3YXJlIiwgIuyGjO2UhO2KuOybqOyWtCIsICJ0
ZXN0IiwgIuyLnO2XmCIsICJ2ZXJpZmljYXRpb24iLCAi6rKA7KadIn0KICAgICAgICBzZWxmLmFz
c2VydEZhbHNlKGZvcmJpZGRlbiAmIHtpdGVtLnN0cmlwKCkubG93ZXIoKSBmb3IgaXRlbSBpbiBh
bGlhc2VzfSkKICAgICAgICBzZWxmLmFzc2VydFRydWUoYWxsKGxlbihpdGVtLnNwbGl0KCkpID49
IDIgZm9yIGl0ZW0gaW4gYWxpYXNlcykpCgogICAgZGVmIHRlc3RfaW1wb3J0YW5jZV9jb250cmFj
dChzZWxmKSAtPiBOb25lOgogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoc2VsZi5pbXBvcnRhbmNl
WyJkaWZmaWN1bHR5Il0sICJERVNJR05fRVZBTFVBVElPTiIpCiAgICAgICAgc2VsZi5hc3NlcnRF
cXVhbChzZWxmLmltcG9ydGFuY2VbInNlbGVjdGlvbl9pbXBvcnRhbmNlIl0sICJDT1JFX01VU1Rf
UFJFUEFSRSIpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChzZWxmLmltcG9ydGFuY2VbInF1ZXN0
aW9uX3R5cGUiXSwgIlBST0NFRFVSRSIpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4oc2Vs
Zi5pbXBvcnRhbmNlWyJoaWdoX2JhbmRfdW5sb2NrX2NvbmRpdGlvbnMiXSksIDgpCgogICAgZGVm
IHRlc3Rfc2NvcGVfYm91bmRhcmllc19hcmVfZXhwbGljaXQoc2VsZikgLT4gTm9uZToKICAgICAg
ICB0ZXh0ID0gIlxuIi5qb2luKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBTSEVFVC5y
ZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiksCiAgICAgICAgICAgICAgICBSRUFETUUucmVhZF90
ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLAogICAgICAgICAgICAgICAgIiAiLmpvaW4oc2VsZi5mYWN0
WyJjb3JlX2ZhY3RzIl0pLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgICAgIGZvciB0b2tl
biBpbiAoIlNXLTA1IiwgIlNhZmV0eSBJbnRlZ3JpdHkiLCAiU1ctMTAiLCAiRkFUIiwgIlNBVCIs
ICLsi5zsmrTsoIQiKToKICAgICAgICAgICAgc2VsZi5hc3NlcnRJbih0b2tlbiwgdGV4dCkKCiAg
ICBkZWYgdGVzdF90ZXh0X2ZpbGVzX2hhdmVfY2xlYW5fd2hpdGVzcGFjZShzZWxmKSAtPiBOb25l
OgogICAgICAgIGZvciBwYXRoIGluIFJFUVVJUkVEX0ZJTEVTICsgW1BhdGgoX19maWxlX18pXToK
ICAgICAgICAgICAgdGV4dCA9IHBhdGgucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAg
ICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZSh0ZXh0LmVuZHN3aXRoKCJcbiIpLCBwYXRoKQogICAgICAg
ICAgICBzZWxmLmFzc2VydE5vdFJlZ2V4KHRleHQsIHIiWyBcdF0rXG4iLCBwYXRoKQoKCmNsYXNz
IExpZmVjeWNsZVJlbGF0aW9uc2hpcFRlc3RzKHVuaXR0ZXN0LlRlc3RDYXNlKToKICAgIGRlZiB0
ZXN0X3ZfbW9kZWxfbWFwcGluZyhzZWxmKSAtPiBOb25lOgogICAgICAgIG1hcHBpbmcgPSB7CiAg
ICAgICAgICAgICJyZXF1aXJlbWVudCI6ICJzeXN0ZW1fdGVzdF92YWxpZGF0aW9uIiwKICAgICAg
ICAgICAgImFyY2hpdGVjdHVyZSI6ICJpbnRlZ3JhdGlvbl90ZXN0IiwKICAgICAgICAgICAgImRl
dGFpbGVkX2Rlc2lnbiI6ICJ1bml0X3Rlc3QiLAogICAgICAgIH0KICAgICAgICBzZWxmLmFzc2Vy
dEVxdWFsKG1hcHBpbmdbImFyY2hpdGVjdHVyZSJdLCAiaW50ZWdyYXRpb25fdGVzdCIpCiAgICAg
ICAgc2VsZi5hc3NlcnROb3RFcXVhbChtYXBwaW5nWyJyZXF1aXJlbWVudCJdLCBtYXBwaW5nWyJk
ZXRhaWxlZF9kZXNpZ24iXSkKCiAgICBkZWYgdGVzdF92ZXJpZmljYXRpb25fdmFsaWRhdGlvbl9h
cmVfZGlzdGluY3Qoc2VsZikgLT4gTm9uZToKICAgICAgICB2ZXJpZmljYXRpb24gPSAiY29uZm9y
bWFuY2VfdG9fc3BlY2lmaWNhdGlvbiIKICAgICAgICB2YWxpZGF0aW9uID0gImZpdG5lc3NfZm9y
X2ludGVuZGVkX3VzZSIKICAgICAgICBzZWxmLmFzc2VydE5vdEVxdWFsKHZlcmlmaWNhdGlvbiwg
dmFsaWRhdGlvbikKCiAgICBkZWYgdGVzdF9iaWRpcmVjdGlvbmFsX3RyYWNlYWJpbGl0eShzZWxm
KSAtPiBOb25lOgogICAgICAgIHJlcXVpcmVtZW50X3RvX3Rlc3QgPSB7IlJFUS0xIjogIlRDLTEi
fQogICAgICAgIHRlc3RfdG9fcmVxdWlyZW1lbnQgPSB7dGVzdDogcmVxIGZvciByZXEsIHRlc3Qg
aW4gcmVxdWlyZW1lbnRfdG9fdGVzdC5pdGVtcygpfQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwo
dGVzdF90b19yZXF1aXJlbWVudFsiVEMtMSJdLCAiUkVRLTEiKQoKICAgIGRlZiB0ZXN0X3Rlc3Rf
bGV2ZWxzX2FyZV9ub3Rfc3Vic3RpdHV0YWJsZShzZWxmKSAtPiBOb25lOgogICAgICAgIGRlZmVj
dHMgPSB7CiAgICAgICAgICAgICJ1bml0IjogeyJib3VuZGFyeSIsICJsb2NhbF9sb2dpYyJ9LAog
ICAgICAgICAgICAiaW50ZWdyYXRpb24iOiB7ImludGVyZmFjZSIsICJ0aW1pbmcifSwKICAgICAg
ICAgICAgInN5c3RlbSI6IHsiZW5kX3RvX2VuZCIsICJvcGVyYXRpb25hbF9tb2RlIn0sCiAgICAg
ICAgfQogICAgICAgIHNlbGYuYXNzZXJ0RmFsc2UoZGVmZWN0c1sidW5pdCJdID49IGRlZmVjdHNb
ImludGVncmF0aW9uIl0pCiAgICAgICAgc2VsZi5hc3NlcnRGYWxzZShkZWZlY3RzWyJ1bml0Il0g
Pj0gZGVmZWN0c1sic3lzdGVtIl0pCgogICAgZGVmIHRlc3Rfc3RhdGljX2R5bmFtaWNfZXhlY3V0
aW9uX2JvdW5kYXJ5KHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYW5hbHlzaXNfbW9kZSA9IHsic3Rh
dGljIjogRmFsc2UsICJkeW5hbWljIjogVHJ1ZX0KICAgICAgICBzZWxmLmFzc2VydEZhbHNlKGFu
YWx5c2lzX21vZGVbInN0YXRpYyJdKQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShhbmFseXNpc19t
b2RlWyJkeW5hbWljIl0pCgogICAgZGVmIHRlc3RfcmVncmVzc2lvbl9pbmNsdWRlc19hZmZlY3Rl
ZF9leGlzdGluZ19iZWhhdmlvcihzZWxmKSAtPiBOb25lOgogICAgICAgIGNoYW5nZWQgPSB7Im5l
d19mdW5jdGlvbiJ9CiAgICAgICAgYWZmZWN0ZWRfZXhpc3RpbmcgPSB7InNoYXJlZF9pbnRlcmZh
Y2UiLCAiZXhpc3Rpbmdfc2VxdWVuY2UifQogICAgICAgIHJlZ3Jlc3Npb25fc2NvcGUgPSBjaGFu
Z2VkIHwgYWZmZWN0ZWRfZXhpc3RpbmcKICAgICAgICBzZWxmLmFzc2VydFRydWUoYWZmZWN0ZWRf
ZXhpc3RpbmcgPD0gcmVncmVzc2lvbl9zY29wZSkKCiAgICBkZWYgdGVzdF9oaWxfY2xvc2VkX2xv
b3BfYm91bmRhcnkoc2VsZikgLT4gTm9uZToKICAgICAgICBoaWwgPSB7InJlYWxfY29udHJvbGxl
ciI6IFRydWUsICJyZWFsX3RpbWVfcGxhbnRfbW9kZWwiOiBUcnVlLCAiY2xvc2VkX2xvb3AiOiBU
cnVlfQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShhbGwoaGlsLnZhbHVlcygpKSkKCiAgICBkZWYg
dGVzdF9mYXVsdF9pbmplY3Rpb25fY2hlY2tzX3JlY292ZXJ5KHNlbGYpIC0+IE5vbmU6CiAgICAg
ICAgZXhwZWN0ZWQgPSB7ImRldGVjdCIsICJpc29sYXRlIiwgImZhbGxiYWNrIiwgInJlY292ZXIi
fQogICAgICAgIG9ic2VydmVkID0geyJkZXRlY3QiLCAiaXNvbGF0ZSIsICJmYWxsYmFjayIsICJy
ZWNvdmVyIn0KICAgICAgICBzZWxmLmFzc2VydEVxdWFsKG9ic2VydmVkLCBleHBlY3RlZCkKCgpj
bGFzcyBEZXRlcm1pbmlzdGljRmF0YWxQYXR0ZXJuU2FmZXR5VGVzdHModW5pdHRlc3QuVGVzdENh
c2UpOgogICAgQGNsYXNzbWV0aG9kCiAgICBkZWYgc2V0VXBDbGFzcyhjbHMpIC0+IE5vbmU6CiAg
ICAgICAgY2xzLmxvZ2ljID0gbG9hZF9qc29uKExPR0lDKQogICAgICAgIGNscy5jaGVja3MgPSBj
bHMubG9naWNbImRldGVybWluaXN0aWNfY2hlY2tzIl1bImZhdGFsX2NoZWNrcyJdCgogICAgZGVm
IHRlc3RfZGlyZWN0X3dyb25nX2NsYWltc19tYXRjaF9kZXRlcm1pbmlzdGljX2FpZHMoc2VsZikg
LT4gTm9uZToKICAgICAgICBmb3IgY2hlY2sgaW4gc2VsZi5jaGVja3M6CiAgICAgICAgICAgIHdy
b25nID0gY2hlY2tbImV4YW1wbGVzX29yX3BhdHRlcm5zIl1bMF0KICAgICAgICAgICAgc2VsZi5h
c3NlcnRUcnVlKAogICAgICAgICAgICAgICAgYW55KHJlLnNlYXJjaChwYXR0ZXJuLCB3cm9uZykg
Zm9yIHBhdHRlcm4gaW4gY2hlY2tbIndyb25nX3BhdHRlcm5zIl0pLAogICAgICAgICAgICAgICAg
Y2hlY2tbImlkIl0sCiAgICAgICAgICAgICkKCiAgICBkZWYgdGVzdF9leHBsaWNpdF9jb3JyZWN0
aW9uc19kb19ub3RfdHJpZ2dlcl9wYXR0ZXJucyhzZWxmKSAtPiBOb25lOgogICAgICAgIHNhbXBs
ZXMgPSBbCiAgICAgICAgICAgICJWZXJpZmljYXRpb27qs7wgVmFsaWRhdGlvbuydgCDsmYTsoITt
nogg6rCZ7J2AIO2ZnOuPmeydtCDslYTri4jri6QuIOuRkCDtmZzrj5nsnZgg66qp7KCB7J2EIOq1
rOu2hO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAgICAgIlYtTW9kZWzsl5DshJzripQg66qo65Og
IOy9lOuUqeydtCDrgZ3rgpwg65Kk7JeQIOyLnO2XmOydhCDsspjsnYwg6rOE7ZqN7ZWY64qUIOqy
g+ydtCDslYTri4jrnbwg6rCc67CcIOy0iOq4sOu2gO2EsCDrjIDsnZEg7Iuc7ZeY7J2EIOykgOu5
hO2VnOuLpC4iLAogICAgICAgICAgICAi7ZqM6reA7Iuc7ZeY7J2AIOyDiOuhnCDstpTqsIDrkJwg
6riw64ql66eMIOyLnO2XmO2VmOuptCDrkJjripQg6rKD7J20IOyVhOuLiOudvCDsmIHtlqXrsJvr
ipQg6riw7KG0IOq4sOuKpeuPhCDtmZXsnbjtlZzri6QuIiwKICAgICAgICAgICAgIuydvOuwmCDs
hoztlITtirjsm6jslrQgViZW66W8IOyZhOujjO2VtOuPhCDrs4Trj4QgU2FmZXR5IGxpZmVjeWNs
ZSDsl4bsnbQgU0lT7J2YIFNJTCDstqnsobHsnbQg7J6Q64+ZIOymneuqheuQmOyngOuKlCDslYrr
ipTri6QuIiwKICAgICAgICBdCiAgICAgICAgZm9yIHNhbXBsZSBpbiBzYW1wbGVzOgogICAgICAg
ICAgICBmb3IgY2hlY2sgaW4gc2VsZi5jaGVja3M6CiAgICAgICAgICAgICAgICBzZWxmLmFzc2Vy
dEZhbHNlKAogICAgICAgICAgICAgICAgICAgIGFueShyZS5zZWFyY2gocGF0dGVybiwgc2FtcGxl
KSBmb3IgcGF0dGVybiBpbiBjaGVja1sid3JvbmdfcGF0dGVybnMiXSksCiAgICAgICAgICAgICAg
ICAgICAgKGNoZWNrWyJpZCJdLCBzYW1wbGUpLAogICAgICAgICAgICAgICAgKQoKICAgIGRlZiB0
ZXN0X3BhdHRlcm5zX2RvX25vdF9tYXRjaF9vbWlzc2lvbihzZWxmKSAtPiBOb25lOgogICAgICAg
IG5ldXRyYWwgPSAi6rOE7Lih7KCc7Ja0IOyGjO2UhO2KuOybqOyWtCDqsJzrsJzri6jqs4TsmYAg
7Iuc7ZeY64uo6rOE66W8IOyEpOuqhe2VnOuLpC4iCiAgICAgICAgZm9yIGNoZWNrIGluIHNlbGYu
Y2hlY2tzOgogICAgICAgICAgICBzZWxmLmFzc2VydEZhbHNlKGFueShyZS5zZWFyY2gocCwgbmV1
dHJhbCkgZm9yIHAgaW4gY2hlY2tbIndyb25nX3BhdHRlcm5zIl0pKQoKCmNsYXNzIEZvY3VzZWRS
b3V0aW5nQm91bmRhcnlUZXN0cyh1bml0dGVzdC5UZXN0Q2FzZSk6CiAgICBAY2xhc3NtZXRob2QK
ICAgIGRlZiBzZXRVcENsYXNzKGNscykgLT4gTm9uZToKICAgICAgICBjbHMubW9kZWwgPSBsb2Fk
X2pzb24oTU9ERUwpCiAgICAgICAgY2xzLnByb2ZpbGUgPSBsb2FkX2pzb24oTE9HSUMpWyJsbG1f
cHJvZmlsZSJdWyJjYW5kaWRhdGVfZXh0cmFjdGlvbiJdCgogICAgZGVmIHRlc3RfcG9zaXRpdmVf
Y2FzZXNfaGF2ZV9sb2NhbF9zaWduYWwoc2VsZikgLT4gTm9uZToKICAgICAgICBjYXNlcyA9IFsK
ICAgICAgICAgICAgIuqzhOy4oeygnOyWtCDshoztlITtirjsm6jslrQgVi1Nb2RlbOqzvCDsmpTq
tazsgqztla0g7LaU7KCB7ISxIOunpO2KuOumreyKpOulvCDshKTrqoXtlZjsi5zsmKQuIiwKICAg
ICAgICAgICAgIuuLqOychOyLnO2XmCDthrXtlansi5ztl5gg7Iuc7Iqk7YWc7Iuc7ZeY6rO8IFZl
cmlmaWNhdGlvbiBWYWxpZGF0aW9u7J2EIOu5hOq1kO2VmOyLnOyYpC4iLAogICAgICAgICAgICAi
U2ltdWxhdGlvbiBISUwgRmF1bHQgaW5qZWN0aW9u7J2EIOydtOyaqe2VnCDsoJzslrQgU1cg6rKA
7Kad67Cp7JWI7J2EIOyEpOuqhe2VmOyLnOyYpC4iLAogICAgICAgIF0KICAgICAgICBmaWVsZHMg
PSBbaXRlbS5sb3dlcigpIGZvciBpdGVtIGluIHNlbGYubW9kZWxbInJvdXRpbmdfZmllbGRfcG9p
bnRzIl1dCiAgICAgICAgZm9yIGNhc2UgaW4gY2FzZXM6CiAgICAgICAgICAgIGxvd2VyZWQgPSBj
YXNlLmxvd2VyKCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRUcnVlKGFueShmaWVsZCBpbiBsb3dl
cmVkIGZvciBmaWVsZCBpbiBmaWVsZHMpLCBjYXNlKQoKICAgIGRlZiB0ZXN0X3N3MDVfYm91bmRh
cnlfY2FzZXNfZG9fbm90X21hdGNoX2NvbXBvdW5kX2FsaWFzKHNlbGYpIC0+IE5vbmU6CiAgICAg
ICAgY2FzZSA9ICJTSVPsnZggU0lMIOyCsOyglSwgUEZEYXZnLCDrj4Xrpr3shLHqs7wgU2FmZXR5
IGxpZmVjeWNsZeydhCDshKTrqoXtlZjsi5zsmKQuIi5sb3dlcigpCiAgICAgICAgc2VsZi5hc3Nl
cnRGYWxzZShhbnkoYWxpYXMubG93ZXIoKSBpbiBjYXNlIGZvciBhbGlhcyBpbiBzZWxmLm1vZGVs
WyJyb3V0aW5nX2FsaWFzZXMiXSkpCgogICAgZGVmIHRlc3Rfc3cxMF9ib3VuZGFyeV9jYXNlc19k
b19ub3RfbWF0Y2hfY29tcG91bmRfYWxpYXMoc2VsZikgLT4gTm9uZToKICAgICAgICBjYXNlID0g
IuygnOyWtCDtlITroZzsoJ3tirggRkFUIFNBVCDsi5zsmrTsoIQgQWNjZXB0YW5jZeyZgCBIYW5k
b3ZlciDsoIjssKjrpbwg7ISk66qF7ZWY7Iuc7JikLiIubG93ZXIoKQogICAgICAgIHNlbGYuYXNz
ZXJ0RmFsc2UoYW55KGFsaWFzLmxvd2VyKCkgaW4gY2FzZSBmb3IgYWxpYXMgaW4gc2VsZi5tb2Rl
bFsicm91dGluZ19hbGlhc2VzIl0pKQoKICAgIGRlZiB0ZXN0X3N3MDNfYm91bmRhcnlfY2FzZXNf
ZG9fbm90X21hdGNoX2NvbXBvdW5kX2FsaWFzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgY2FzZSA9
ICJITUkgU0NBREEgQWxhcm0gcmF0aW9uYWxpemF0aW9uIFNPReyZgCDsmrTsoITsnpAg6raM7ZWc
7J2EIOyEpOuqhe2VmOyLnOyYpC4iLmxvd2VyKCkKICAgICAgICBzZWxmLmFzc2VydEZhbHNlKGFu
eShhbGlhcy5sb3dlcigpIGluIGNhc2UgZm9yIGFsaWFzIGluIHNlbGYubW9kZWxbInJvdXRpbmdf
YWxpYXNlcyJdKSkKCgpjbGFzcyBDb250ZW50UXVhbGl0eVRlc3RzKHVuaXR0ZXN0LlRlc3RDYXNl
KToKICAgIGRlZiB0ZXN0X25vX3BsYWNlaG9sZGVyX21hcmtlcnMoc2VsZikgLT4gTm9uZToKICAg
ICAgICBmb3IgcGF0aCBpbiBSRVFVSVJFRF9GSUxFUzoKICAgICAgICAgICAgdGV4dCA9IHBhdGgu
cmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmxvd2VyKCkKICAgICAgICAgICAgZm9yIG1hcmtl
ciBpbiAoInRvZG8iLCAic2NhZmZvbGQiLCAi67O06rCV7ZWY7IS47JqUIik6CiAgICAgICAgICAg
ICAgICBzZWxmLmFzc2VydE5vdEluKG1hcmtlciwgdGV4dCwgcGF0aCkKCiAgICBkZWYgdGVzdF9x
dWVzdGlvbl9hbmRfb3V0bGluZV9jb3VudHMoc2VsZikgLT4gTm9uZToKICAgICAgICBtb2RlbCA9
IGxvYWRfanNvbihNT0RFTCkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihtb2RlbFsiZXhw
ZWN0ZWRfcXVlc3Rpb25fcGF0dGVybnMiXSksIDEwKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwo
bGVuKG1vZGVsWyJyZWNvbW1lbmRlZF9vdXRsaW5lIl0pLCA4KQoKCmNsYXNzIFNlbWFudGljQXVk
aXRSZXBhaXJUZXN0cyh1bml0dGVzdC5UZXN0Q2FzZSk6CiAgICBkZWYgc2V0VXAoc2VsZikgLT4g
Tm9uZToKICAgICAgICBzZWxmLmZhY3QgPSBsb2FkX2pzb24oRkFDVCkKICAgICAgICBzZWxmLmxv
Z2ljID0gbG9hZF9qc29uKExPR0lDKQogICAgICAgIHNlbGYuYW5jaG9ycyA9IHtpdGVtWyJpZCJd
OiBpdGVtIGZvciBpdGVtIGluIHNlbGYuZmFjdFsiYW5jaG9ycyJdfQogICAgICAgIHNlbGYuZmF0
YWxzID0ge2l0ZW1bImlkIl06IGl0ZW0gZm9yIGl0ZW0gaW4gc2VsZi5mYWN0WyJmYXRhbF93cm9u
Z19jbGFpbXMiXX0KCiAgICBkZWYgdGVzdF9oaWxfc2lsX3ZpcnR1YWxfY29tbWlzc2lvbmluZ19i
b3VuZGFyeShzZWxmKSAtPiBOb25lOgogICAgICAgIHRleHQgPSBzZWxmLmFuY2hvcnNbInN3MDRf
aGlsIl1bInN0YXRlbWVudCJdCiAgICAgICAgc2VsZi5hc3NlcnRJbigi7Iuk7KCcIOuMgOyDgSDs
oJzslrTquLAg7ZWY65Oc7Juo7Ja0IOuYkOuKlCDsi6TsoJwgSS9PIO2VmOuTnOybqOyWtCIsIHRl
eHQpCiAgICAgICAgc2VsZi5hc3NlcnRJbigi7Iuk7Iuc6rCEIFBsYW50IE1vZGVsIiwgdGV4dCkK
ICAgICAgICBzZWxmLmFzc2VydEluKCJTSUwoU29mdHdhcmUtaW4tdGhlLWxvb3ApIiwgdGV4dCkK
ICAgICAgICBzZWxmLmFzc2VydEluKCJWaXJ0dWFsIENvbW1pc3Npb25pbmciLCB0ZXh0KQogICAg
ICAgIHNlbGYuYXNzZXJ0SW4oIu2VmOuTnOybqOyWtCDsl4bsnbQiLCB0ZXh0KQoKICAgIGRlZiB0
ZXN0X2hpbF9mYXRhbF9rZWVwc19yZWFsX3BsYW50X2V4Y2VwdGlvbihzZWxmKSAtPiBOb25lOgog
ICAgICAgIGxvZ2ljX2ZhdGFsID0gbmV4dChpdGVtIGZvciBpdGVtIGluIHNlbGYubG9naWNbImxs
bV9wcm9maWxlIl1bImZhdGFsX2NvbmRpdGlvbnMiXSBpZiBpdGVtWyJpZCJdID09ICJzdzA0X2Zh
dGFsX2hpbF9yZXF1aXJlc19yZWFsX3BsYW50IikKICAgICAgICBmYWN0X2ZhdGFsID0gc2VsZi5m
YXRhbHNbInN3MDRfZmF0YWxfaGlsX3JlcXVpcmVzX3JlYWxfcGxhbnQiXQogICAgICAgIHNlbGYu
YXNzZXJ0SW4oIuyLpOygnCDsg53sgrDshKTruYQg6rCA64+Z7J2AIO2VhOyalO2VmOyngCDslYrr
i6QiLCBsb2dpY19mYXRhbFsiY29ycmVjdF9ydWxlIl0pCiAgICAgICAgZm9yIGZpZWxkIGluICgi
Y29ycmVjdGlvbiIsICJjb3JyZWN0X3J1bGUiLCAiZGVzY3JpcHRpb24iKToKICAgICAgICAgICAg
dGV4dCA9IGZhY3RfZmF0YWxbZmllbGRdCiAgICAgICAgICAgIHNlbGYuYXNzZXJ0SW4oIuyLpOyg
nCDrjIDsg4Eg7KCc7Ja06riwIiwgdGV4dCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRJbigi7Iuk
7KCcIEkvTyDtlZjrk5zsm6jslrQiLCB0ZXh0KQogICAgICAgICAgICBzZWxmLmFzc2VydEluKCLs
i6Tsi5zqsIQgUGxhbnQgTW9kZWwiLCB0ZXh0KQogICAgICAgICAgICBzZWxmLmFzc2VydEluKCJT
SUwoU29mdHdhcmUtaW4tdGhlLWxvb3ApIiwgdGV4dCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRJ
bigiVmlydHVhbCBDb21taXNzaW9uaW5nIiwgdGV4dCkKICAgICAgICAgICAgc2VsZi5hc3NlcnRO
b3RJbigi7Iuk7KCcIOygnOyWtCBIVyDrmJDripQg7Iuk7ZaJ7ZmY6rK9IiwgdGV4dCkKICAgICAg
ICBzZWxmLmFzc2VydEluKCLsi6TsoJwg7IOd7IKw7ISk67mE66W8IOqwgOuPme2VoCDtlYTsmpTr
ipQg7JeG64ukIiwgZmFjdF9mYXRhbFsiY29ycmVjdGlvbiJdKQoKCmlmIF9fbmFtZV9fID09ICJf
X21haW5fXyI6CiAgICBzdWl0ZSA9IHVuaXR0ZXN0LmRlZmF1bHRUZXN0TG9hZGVyLmxvYWRUZXN0
c0Zyb21Nb2R1bGUoc3lzLm1vZHVsZXNbX19uYW1lX19dKQogICAgcHJpbnQoZiJTVzA0X0ZPQ1VT
RURfVEVTVF9DT1VOVD17c3VpdGUuY291bnRUZXN0Q2FzZXMoKX0iKQogICAgcmVzdWx0ID0gdW5p
dHRlc3QuVGV4dFRlc3RSdW5uZXIodmVyYm9zaXR5PTIpLnJ1bihzdWl0ZSkKICAgIHJhaXNlIFN5
c3RlbUV4aXQoMCBpZiByZXN1bHQud2FzU3VjY2Vzc2Z1bCgpIGVsc2UgMSkK
PAYLOAD_SW04_07

    if [ "$failure_count" -eq 0 ]; then
        for rel in "${TOPIC_PATHS[@]}"; do
            mkdir -p -- "$(dirname -- "$rel")"
            install -m 0644 -- "${payload_tmp}/${rel}" "$rel"
            install_rc=$?
            printf 'INSTALL_RC=%s|%s\n' "$rel" "$install_rc"
            if [ "$install_rc" -ne 0 ]; then
                fail "PAYLOAD_INSTALL_FAILED:${rel}"
            else
                created_count=$((created_count + 1))
            fi
        done
    fi
else
    pass "existing complete SW-04 payload retained without rewrite"
fi

CURRENT_STAGE="SW04_TOPIC_LOCAL_VALIDATION"
NEXT_STAGE="SW04_OWNERSHIP_VALIDATION"
section "4. verify payload hashes, JSON, source schema and Topic quality"

if [ "$failure_count" -eq 0 ]; then
    for rel in "${TOPIC_PATHS[@]}"; do
        actual="$(sha256sum "$rel" | awk '{print $1}')"
        expected="${EXPECTED_SHA256[$rel]}"
        printf 'PAYLOAD_SHA256=%s|%s\n' "$rel" "$actual"
        [ "$actual" = "$expected" ] ||
            fail "PAYLOAD_HASH_MISMATCH:${rel}"
    done
fi

if [ "$failure_count" -eq 0 ]; then
    for rel in "${JSON_PATHS[@]}"; do
        run_step "JSON_SYNTAX:${rel}" validate_json_quiet "$rel"
    done
fi

if [ "$failure_count" -eq 0 ]; then
    printf '\n--- TOPIC_LOCAL_PRODUCTION_SCHEMA_VALIDATION ---\n'
    python3 - "$TOPIC_DIR" "$TOPIC_ID" <<'PY_SCHEMA'
from __future__ import annotations

import sys
from pathlib import Path

pack_dir = Path(sys.argv[1])
topic_id = sys.argv[2]

import scripts.validate_topic_packs as validator

global_anchor_ids: set[str] = set()
anchor_ids = validator.validate_fact_anchor(pack_dir, topic_id, global_anchor_ids)
validator.validate_model_answer(pack_dir, topic_id, anchor_ids)
validator.validate_topic_importance(pack_dir, topic_id)
validator.validate_logic_check(pack_dir, topic_id)

print("TOPIC_LOCAL_SCHEMA_VALID=true")
print(f"TOPIC_LOCAL_ANCHOR_COUNT={len(anchor_ids)}")
PY_SCHEMA
    schema_rc=$?
    printf 'STEP_RC=TOPIC_LOCAL_PRODUCTION_SCHEMA_VALIDATION|%s\n' "$schema_rc"
    [ "$schema_rc" -eq 0 ] ||
        fail "TOPIC_LOCAL_PRODUCTION_SCHEMA_VALIDATION"
fi

if [ "$failure_count" -eq 0 ]; then
    if [ -f scripts/validate_topic_pack_quality.py ]; then
        run_step \
            "VALIDATE_SW04_TOPIC_QUALITY" \
            python3 scripts/validate_topic_pack_quality.py \
                --topic-id "$TOPIC_ID" \
                --strict-generic-aliases \
                --require-logic-check
    else
        fail "TOPIC_QUALITY_VALIDATOR_MISSING"
    fi
fi

CURRENT_STAGE="SW04_FOCUSED_REGRESSION"
NEXT_STAGE="SW04_OWNERSHIP_VALIDATION"
section "5. run SW-04 focused regression and source hygiene"

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "PY_COMPILE_SW04_FOCUSED_TEST" \
        python3 -m py_compile "$TEST_REL"
fi

if [ "$failure_count" -eq 0 ]; then
    focused_log="$(mktemp)"
    python3 "$TEST_REL" 2>&1 | tee "$focused_log"
    focused_rc=${PIPESTATUS[0]}
    printf 'STEP_RC=RUN_SW04_FOCUSED_TEST|%s\n' "$focused_rc"
    if [ "$focused_rc" -ne 0 ]; then
        fail "RUN_SW04_FOCUSED_TEST"
    elif ! grep -Fq 'SW04_FOCUSED_TEST_COUNT=28' "$focused_log"; then
        fail "SW04_FOCUSED_TEST_COUNT_CONTRACT_MISSING"
    else
        pass "SW-04 focused regressions passed: 28/28"
    fi
    rm -f -- "$focused_log"
fi

if [ "$failure_count" -eq 0 ]; then
    python3 - "${TOPIC_PATHS[@]}" <<'PY_WHITESPACE'
from __future__ import annotations

import sys
from pathlib import Path

errors: list[str] = []
for raw in sys.argv[1:]:
    path = Path(raw)
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        errors.append(f"{raw}: missing final newline")
    text = data.decode("utf-8")
    for number, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            errors.append(f"{raw}:{number}: trailing whitespace")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"TOPIC_LOCAL_WHITESPACE_FILE_COUNT={len(sys.argv)-1}")
print("TOPIC_LOCAL_WHITESPACE_VALID=true")
PY_WHITESPACE
    whitespace_rc=$?
    printf 'STEP_RC=TOPIC_LOCAL_WHITESPACE_VALIDATION|%s\n' "$whitespace_rc"
    [ "$whitespace_rc" -eq 0 ] ||
        fail "TOPIC_LOCAL_WHITESPACE_VALIDATION"
fi

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "GIT_DIFF_CHECK_SW04_TARGETS" \
        git diff --check -- "${COMMIT_PATHS[@]}"
fi

CURRENT_STAGE="SW04_OWNERSHIP_VALIDATION"
NEXT_STAGE="SW04_LOCAL_COMMIT"
section "6. verify strict Lane A source-only ownership boundary"

if [ "$failure_count" -eq 0 ]; then
    collect_changed_paths > "$changed_after_file"

    {
        cut -f1 "$baseline_helper_file" 2>/dev/null || true
        printf '%s\n' "${COMMIT_PATHS[@]}"
    } | awk 'NF > 0 { print }' | LC_ALL=C sort -u > "$allowed_after_file"

    printf 'ALLOWED_CHANGED_PATHS_BEGIN\n'
    cat "$allowed_after_file"
    printf 'ALLOWED_CHANGED_PATHS_END\n'
    printf 'ACTUAL_CHANGED_PATHS_BEGIN\n'
    cat "$changed_after_file"
    printf 'ACTUAL_CHANGED_PATHS_END\n'

    if cmp -s "$allowed_after_file" "$changed_after_file"; then
        pass "all changes are confined to immutable helper baseline and SW-04 commit paths"
    else
        fail "SW04_CHANGED_PATH_BOUNDARY_MISMATCH"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    if verify_helper_manifest "$baseline_helper_file"; then
        pass "pre-existing Lane A helper scripts remain byte-identical"
    else
        fail "BASELINE_HELPER_STATE_CHANGED"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    if git diff --quiet -- rubrics/generated &&
       git diff --cached --quiet -- rubrics/generated
    then
        pass "rubrics/generated remains unchanged"
    else
        fail "RUBRICS_GENERATED_CHANGED"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    mapfile -t changed_python < <(
        collect_changed_paths | awk '/\.py$/ { print }'
    )
    printf 'CHANGED_PYTHON_PATHS_BEGIN\n'
    printf '%s\n' "${changed_python[@]}"
    printf 'CHANGED_PYTHON_PATHS_END\n'
    if [ "${#changed_python[@]}" -eq 1 ] &&
       [ "${changed_python[0]}" = "$TEST_REL" ]
    then
        pass "only the SW-04 focused test changes Python"
    else
        fail "PRODUCTION_OR_UNRELATED_PYTHON_CHANGED"
    fi
fi

if [ "$failure_count" -ne 0 ]; then
    CURRENT_STAGE="SW04_TOPIC_LOCAL_FAILED"
    NEXT_STAGE="SW04_MINIMAL_REPAIR"
    result_header "SW04_TOPIC_LOCAL_VALIDATION_FAILED"
    printf '%s\n' \
        "failure_count=${failure_count}" \
        "warning_count=${warning_count}" \
        "created_count=${created_count}" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_TOPIC=SW-04 minimal repair" \
        "LANE_PROGRESS=2/4"
    final_rc=1
    exit 1
fi

CURRENT_STAGE="SW04_LOCAL_COMMIT"
NEXT_STAGE="SW10_AUTHORING_PACKAGE"
section "7. stage and create one Topic-local SW-04 commit"

git add -- "${COMMIT_PATHS[@]}"
add_rc=$?
printf 'STEP_RC=GIT_ADD_SW04_TOPIC_ONLY|%s\n' "$add_rc"
[ "$add_rc" -eq 0 ] || fail "GIT_ADD_SW04_TOPIC_ONLY"

if [ "$failure_count" -eq 0 ]; then
    git diff --cached --name-only | LC_ALL=C sort -u > "$staged_file"
    printf '%s\n' "${COMMIT_PATHS[@]}" | LC_ALL=C sort -u > "$commit_files_file"

    printf 'STAGED_SW04_PATHS_BEGIN\n'
    cat "$staged_file"
    printf 'STAGED_SW04_PATHS_END\n'

    if cmp -s "$staged_file" "$commit_files_file"; then
        pass "Git index contains exactly one SW-04 Topic package and its Lane A script"
    else
        fail "SW04_STAGED_PATH_BOUNDARY_MISMATCH"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "GIT_CACHED_DIFF_CHECK_SW04" \
        git diff --cached --check -- "${COMMIT_PATHS[@]}"
fi

if [ "$failure_count" -eq 0 ]; then
    git commit -m "$COMMIT_SUBJECT"
    commit_rc=$?
    printf 'STEP_RC=GIT_COMMIT_SW04|%s\n' "$commit_rc"
    [ "$commit_rc" -eq 0 ] || fail "GIT_COMMIT_SW04"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW04_TOPIC_LOCAL_COMMIT_FAILED"
    printf '%s\n' \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Review commit-stage failure without pushing"
    final_rc=1
    exit 1
fi

commit_hash="$(git rev-parse HEAD)"
commit_subject="$(git show -s --format='%s' HEAD)"
git show --pretty='' --name-only HEAD | awk 'NF > 0 { print }' | LC_ALL=C sort -u > "$commit_files_file"

if [ "$commit_subject" != "$COMMIT_SUBJECT" ]; then
    fail "POST_COMMIT_SUBJECT_MISMATCH"
fi

for rel in "${COMMIT_PATHS[@]}"; do
    git diff --quiet -- "$rel" || fail "POST_COMMIT_UNSTAGED_TARGET:${rel}"
    git diff --cached --quiet -- "$rel" || fail "POST_COMMIT_STAGED_TARGET:${rel}"
done

if ! verify_helper_manifest "$baseline_helper_file"; then
    fail "POST_COMMIT_BASELINE_HELPER_CHANGED"
fi

if [ "$failure_count" -eq 0 ]; then
    collect_changed_paths > "$changed_after_file"
    cut -f1 "$baseline_helper_file" | awk 'NF > 0 { print }' | LC_ALL=C sort -u > "$allowed_after_file"
    if cmp -s "$allowed_after_file" "$changed_after_file"; then
        pass "only the pre-existing immutable helper baseline remains uncommitted"
    else
        printf 'POST_COMMIT_EXPECTED_DIRTY_BEGIN\n'
        cat "$allowed_after_file"
        printf 'POST_COMMIT_EXPECTED_DIRTY_END\n'
        printf 'POST_COMMIT_ACTUAL_DIRTY_BEGIN\n'
        cat "$changed_after_file"
        printf 'POST_COMMIT_ACTUAL_DIRTY_END\n'
        fail "POST_COMMIT_DIRTY_STATE_MISMATCH"
    fi
fi

CURRENT_STAGE="SW04_TOPIC_LOCAL_COMPLETE"
NEXT_STAGE="SW10_AUTHORING_PACKAGE"
LANE_PROGRESS="3/4"
section "8. summarize SW-04 Topic-local result"

printf '%s\n' \
    "SW04_ANCHOR_COUNT=31" \
    "SW04_FATAL_COUNT=16" \
    "SW04_LOGIC_FATAL_COUNT=16" \
    "SW04_LLM_MAJOR_COUNT=8" \
    "SW04_FALSE_POSITIVE_CAUTION_COUNT=10" \
    "SW04_ROUTING_ALIAS_COUNT=20" \
    "SW04_ROUTING_FIELD_POINT_COUNT=45" \
    "SW04_QUESTION_PATTERN_COUNT=10" \
    "SW04_OUTLINE_SECTION_COUNT=8" \
    "SW04_FOCUSED_TEST_COUNT=28" \
    "SW04_DIFFICULTY=DESIGN_EVALUATION" \
    "SW04_SELECTION_IMPORTANCE=CORE_MUST_PREPARE" \
    "failure_count=${failure_count}" \
    "warning_count=${warning_count}" \
    "created_count=${created_count}" \
    "CHATGPT_SEMANTIC_REVIEW=completed_before_script" \
    "EXTERNAL_LLM_VALIDATION_EXECUTED=false" \
    "GENERATED_REBUILD_EXECUTED=false" \
    "VALIDATE_ALL_EXECUTED=false" \
    "RELEASE_PROMOTION_EXECUTED=false" \
    "PUSH_EXECUTED=false"

if [ "$failure_count" -eq 0 ]; then
    result_header "SW04_TOPIC_LOCAL_COMMIT_COMPLETE"
    printf '%s\n' \
        "LANE=${LANE}" \
        "SW_NUMBER=SW-04" \
        "TOPIC_ID=${TOPIC_ID}" \
        "COMMIT_HASH=${commit_hash}" \
        "COMMIT_SUBJECT=${commit_subject}" \
        "COMMITTED_FILES_BEGIN"
    cat "$commit_files_file"
    printf '%s\n' \
        "COMMITTED_FILES_END" \
        "VALIDATION_RESULT=JSON_SCHEMA_TOPIC_QUALITY_FOCUSED_TEST_PY_COMPILE_DIFF_CHECK_OWNERSHIP_PASS" \
        "NEXT_TOPIC=SW-10 control_software_project_engineering_documents_fat_sat_commissioning_acceptance" \
        "LANE_PROGRESS=3/4" \
        "PUSH_EXECUTED=false"
    final_rc=0
else
    result_header "SW04_POST_COMMIT_AUDIT_FAILED"
    printf '%s\n' \
        "COMMIT_HASH=${commit_hash}" \
        "COMMIT_SUBJECT=${commit_subject}" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Run a post-commit minimal audit before SW-10"
    final_rc=1
fi

(return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
