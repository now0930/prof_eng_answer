#!/usr/bin/env bash

set -u
set -o pipefail

readonly OVERALL_STAGE="SOFTWARE_TOPIC_PACK_PARALLEL_EXPANSION"
readonly LANE="SOFTWARE_LLM_LANE_A"
readonly LANE_BRANCH="software/lane-a-control-lifecycle"
readonly REMOTE="origin"
readonly REPO_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_a"
readonly SCRIPT_DIR="${REPO_DIR}/gemini_script"
readonly CURRENT_TOPIC="SW-03 hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
readonly TOPIC_ID="hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
readonly TOPIC_DIR="rubrics/topic_packs/${TOPIC_ID}"
readonly SHEET_REL="docs/topic_sheets/${TOPIC_ID}.md"
readonly TEST_REL="scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py"
readonly SCRIPT_NAME="20260806_sw03_lane_a_author_validate_commit.sh"
readonly SCRIPT_REL="gemini_script/${SCRIPT_NAME}"
readonly COMMIT_SUBJECT="feat(topic-pack): add SW-03 HMI alarm topic"
readonly SW02_COMMIT_SUBJECT="feat(topic-pack): add SW-02 control logic topic"

CURRENT_STAGE="LANE_A_READ_ONLY_WORKTREE_CHECK"
NEXT_STAGE="SW03_COMMIT_STATUS_DETECTION"
LANE_PROGRESS="1/4"
failure_count=0
warning_count=0
created_count=0
final_rc=1
AUTHORING_REQUIRED=true
REUSE_EXISTING_PAYLOAD=false
SW03_ALREADY_COMMITTED=false

payload_tmp=""
changed_before_file=""
changed_after_file=""
allowed_after_file=""
baseline_helper_file=""
staged_file=""
commit_files_file=""
python_cache_dir=""

TOPIC_PATHS=(
    'docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/README.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json'
    'scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py'
)

COMMIT_PATHS=(
    'docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/README.md'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json'
    'scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py'
    'gemini_script/20260806_sw03_lane_a_author_validate_commit.sh'
)

SW02_REQUIRED_PATHS=(
    'docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md'
    'rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md'
    'rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json'
    'rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json'
    'rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json'
    'rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json'
    'scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py'
    'gemini_script/20260806_sw02_lane_a_author_commit_topic_pack.sh'
)

JSON_PATHS=(
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json'
    'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json'
)

declare -A EXPECTED_SHA256=(
    ['docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md']='0026a7bed0ed7067a87a004a761286cffefb575e8392c365310d776c96238dd1'
    ['rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/README.md']='7318bfde752b002b7dc2950536895403e6549f229fc1261221ef5dd1a8c2ca1e'
    ['rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json']='9a3524311a28d89f9b9cbd795f1561975eed4df8c63550981439d86ab1dba0dd'
    ['rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json']='ea925b4121be491825e1b041efa5f02405cb682e5a72e53267a922765b83e2c7'
    ['rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json']='5d39a524114f60163721ec70af8249f20b6698d05a8bc97bc6f18f7d6198b01f'
    ['rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json']='5d936639664912dca2c987d226adaea6180d0d78b033f3de1d3bf9698ef56eae'
    ['scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py']='775c03be9399d6064d441f4acea5a5fe5d323e0315c733386fce67d5010519a5'
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
NEXT_STAGE="SW02_COMMIT_PREREQUISITE_CHECK"
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

CURRENT_STAGE="SW02_COMMIT_PREREQUISITE_CHECK"
NEXT_STAGE="SW03_COMMIT_STATUS_DETECTION"
section "1. verify SW-02 committed prerequisite and preserve helper baseline"

sw02_head_count=0
for rel in "${SW02_REQUIRED_PATHS[@]}"; do
    if git cat-file -e "HEAD:${rel}" 2>/dev/null; then
        sw02_head_count=$((sw02_head_count + 1))
    fi
done
printf 'SW02_HEAD_PATH_COUNT=%s/%s\n' "$sw02_head_count" "${#SW02_REQUIRED_PATHS[@]}"

if [ "$sw02_head_count" -ne "${#SW02_REQUIRED_PATHS[@]}" ]; then
    fail "SW02_COMMITTED_PREREQUISITE_INCOMPLETE"
fi

if [ "$failure_count" -eq 0 ]; then
    mapfile -t sw02_commits < <(
        for rel in "${SW02_REQUIRED_PATHS[@]}"; do
            git log -1 --format='%H' -- "$rel"
        done | LC_ALL=C sort -u
    )
    printf 'SW02_UNIQUE_COMMIT_COUNT=%s\n' "${#sw02_commits[@]}"
    [ "${#sw02_commits[@]}" -eq 1 ] || fail "SW02_PATHS_NOT_IN_ONE_TOPIC_COMMIT"
fi

if [ "$failure_count" -eq 0 ]; then
    sw02_commit="${sw02_commits[0]}"
    sw02_subject="$(git show -s --format='%s' "$sw02_commit")"
    printf '%s\n' \
        "SW02_COMMIT_HASH=${sw02_commit}" \
        "SW02_COMMIT_SUBJECT=${sw02_subject}"
    [ "$sw02_subject" = "$SW02_COMMIT_SUBJECT" ] ||
        fail "SW02_COMMIT_SUBJECT_MISMATCH"

    for rel in "${SW02_REQUIRED_PATHS[@]}"; do
        git diff --quiet -- "$rel" || fail "SW02_UNSTAGED_CHANGE:${rel}"
        git diff --cached --quiet -- "$rel" || fail "SW02_STAGED_CHANGE:${rel}"
    done
fi

if [ -n "$(git diff --cached --name-only)" ]; then
    printf 'PREEXISTING_STAGED_PATHS_BEGIN\n'
    git diff --cached --name-only
    printf 'PREEXISTING_STAGED_PATHS_END\n'
    fail "GIT_INDEX_NOT_CLEAN_BEFORE_SW03"
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
    pass "SW-02 Topic commit is complete and clean"
    pass "pre-existing Lane A helper scripts captured as immutable baseline"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW03_PREREQUISITE_OR_BASELINE_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Repair only the reported Lane A prerequisite or dirty path"
    final_rc=1
    exit 1
fi

CURRENT_STAGE="SW03_COMMIT_STATUS_DETECTION"
NEXT_STAGE="SW03_AUTHOR_OR_SKIP"
section "2. detect whether SW-03 is already committed"

sw03_head_count=0
for rel in "${COMMIT_PATHS[@]}"; do
    if git cat-file -e "HEAD:${rel}" 2>/dev/null; then
        sw03_head_count=$((sw03_head_count + 1))
    fi
done
printf 'SW03_HEAD_PATH_COUNT=%s/%s\n' "$sw03_head_count" "${#COMMIT_PATHS[@]}"

if [ "$sw03_head_count" -eq "${#COMMIT_PATHS[@]}" ]; then
    mapfile -t sw03_commits < <(
        for rel in "${COMMIT_PATHS[@]}"; do
            git log -1 --format='%H' -- "$rel"
        done | LC_ALL=C sort -u
    )
    if [ "${#sw03_commits[@]}" -ne 1 ]; then
        fail "SW03_PATHS_NOT_IN_ONE_TOPIC_COMMIT"
    else
        sw03_commit="${sw03_commits[0]}"
        sw03_subject="$(git show -s --format='%s' "$sw03_commit")"
        printf '%s\n' \
            "SW03_COMMIT_HASH=${sw03_commit}" \
            "SW03_COMMIT_SUBJECT=${sw03_subject}"
        [ "$sw03_subject" = "$COMMIT_SUBJECT" ] ||
            fail "SW03_COMMIT_SUBJECT_MISMATCH"
    fi

    for rel in "${COMMIT_PATHS[@]}"; do
        git diff --quiet -- "$rel" || fail "SW03_UNSTAGED_CHANGE:${rel}"
        git diff --cached --quiet -- "$rel" || fail "SW03_STAGED_CHANGE:${rel}"
    done

    if [ "$failure_count" -eq 0 ]; then
        SW03_ALREADY_COMMITTED=true
        AUTHORING_REQUIRED=false
    fi
elif [ "$sw03_head_count" -ne 0 ]; then
    fail "SW03_PARTIALLY_PRESENT_IN_HEAD"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW03_COMMIT_STATUS_DETECTION_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false"
    final_rc=1
    exit 1
fi

if [ "$SW03_ALREADY_COMMITTED" = "true" ]; then
    CURRENT_STAGE="SW03_TOPIC_LOCAL_COMPLETE"
    NEXT_STAGE="SW04_AUTHORING_PACKAGE"
    LANE_PROGRESS="2/4"
    result_header "SW03_ALREADY_COMMITTED_SKIP_CONFIRMED"
    printf '%s\n' \
        "SW_NUMBER=SW-03" \
        "TOPIC_ID=${TOPIC_ID}" \
        "COMMIT_HASH=${sw03_commit}" \
        "COMMIT_SUBJECT=${sw03_subject}" \
        "VALIDATION_RESULT=COMMITTED_PATHS_AND_CLEAN_STATE_PASS" \
        "NEXT_TOPIC=SW-04 instrumentation_control_software_lifecycle_v_model_traceability_verification_validation" \
        "LANE_PROGRESS=2/4" \
        "PUSH_EXECUTED=false"
    final_rc=0
    exit 0
fi

worktree_topic_count=0
for rel in "${TOPIC_PATHS[@]}"; do
    [ -f "$rel" ] && worktree_topic_count=$((worktree_topic_count + 1))
done
printf 'SW03_WORKTREE_TOPIC_PATH_COUNT=%s/%s\n' "$worktree_topic_count" "${#TOPIC_PATHS[@]}"

if [ "$worktree_topic_count" -eq 0 ]; then
    AUTHORING_REQUIRED=true
elif [ "$worktree_topic_count" -eq "${#TOPIC_PATHS[@]}" ]; then
    AUTHORING_REQUIRED=false
    REUSE_EXISTING_PAYLOAD=true
    pass "complete uncommitted SW-03 payload found; exact hashes will be verified"
else
    fail "SW03_PARTIAL_WORKTREE_PAYLOAD"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW03_WORKTREE_PAYLOAD_STATUS_FAILED"
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

CURRENT_STAGE="SW03_SOURCE_AUTHORING"
NEXT_STAGE="SW03_TOPIC_LOCAL_VALIDATION"
section "3. create or reuse complete SW-03 Topic Authoring Package"

if [ "$AUTHORING_REQUIRED" = "true" ] && [ "$failure_count" -eq 0 ]; then
    payload_tmp="$(mktemp -d)"

    write_payload 'docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md' '0026a7bed0ed7067a87a004a761286cffefb575e8392c365310d776c96238dd1' <<'PAYLOAD_SW03_01'
IyBTVy0wMyBUb3BpYyBTaGVldAoKIyMgMS4gVG9waWMg7Iud67OECgotIFRvcGljIElEOiBgaG1p
X3NjYWRhX2FsYXJtX3NldHBvaW50X3RyaXBfaW50ZXJsb2NrX3NvZV9vcGVyYXRvcl9pbmZvcm1h
dGlvbl9tYW5hZ2VtZW50YAotIO2VnOq4gCDso7zsoJw6IEhNScK3U0NBREHCt0FsYXJtwrdTZXRw
b2ludMK3VHJpcMK3SW50ZXJsb2NrwrdTT0Ug67CPIOyatOyghOygleuztCDqtIDrpqwKLSBMYW5l
OiBgU09GVFdBUkVfTExNX0xBTkVfQWAKLSDshozsnKDrspTsnIQ6IOyatOyghOyekOyXkOqyjCDs
oJzqs7XrkJjripQg6rO17KCV7KCV67O0LCBBbGFybSwgU2V0cG9pbnQsIFNPRSwg6raM7ZWc6rO8
IOyatOyghOygleuztCDqtIDrpqwKLSDsoJzsmbjrspTsnIQ6IEludGVybG9ja8K3VHJpcOydmCDs
g4Htg5zsoITsnbQg7Iuk7ZaJ64W866asLCBTSUwg7IKw7KCVLCDsnbzrsJggU1cgViZWLCDtlITr
oZzsoJ3tirggRkFUwrdTQVQg7IiY7ZaJCgojIyAyLiDtlbXsi6wg66y47KCc7J2Y7IudCgrsoJzs
lrTsi5zsiqTthZzsnbQg7KCV7ZmV7ZWcIOygnOyWtOuFvOumrOulvCDrs7TsnKDtlbTrj4Qg7Jq0
7KCE7J6Q6rCAIO2YhOyerCDqs7XsoJXsg4Htg5zsmYAg7KCV67O07J2YIOyLoOuisOuPhOulvCDs
nbTtlbTtlZjsp4Ag66q77ZWY66m0IOyggeygiO2VnCDtjJDri6jqs7wg7KGw7LmY66W8IOyImO2W
ie2VmOq4sCDslrTroLXri6QuIFNXLTAz7J2AIEhNSeyZgCBTQ0FEQeulvCDri6jsiJwg7ZmU66m0
IOuYkOuKlCDrjbDsnbTthLAg7IiY7KeRIOyepey5mOuhnCDrs7Tsp4Ag7JWK64qU64ukLiDqs7Xs
oJXsg4Htg5zrpbwg7J247KeA7ZWY6rOgLCDruYTsoJXsg4Eg7KeV7ZuE66W8IOuwnOqyrO2VmOup
sCwgQWxhcm3snYQg7KeE64uo7ZWY6rOgLCDqtoztlZzsl5Ag65Sw6528IOyhsOy5mO2VnCDrkqQs
IFNPReyZgCBBdWRpdCB0cmFpbOuhnCDqsrDqs7zrpbwg7LaU7KCB7ZWY64qUIOyatOyghOygleuz
tCDssrTqs4TroZwg64uk66Os64ukLgoKIyMgMy4g7Y+s7ZWoIOuylOychAoKMS4gSE1J7JmAIFND
QURB7J2YIOyXre2VoCDrsI8g6rWs7KGwCjIuIOyEnOuyhMK37Ya17IugIOyepeyVoCwgRmFpbG92
ZXLsmYAg642w7J207YSwIO2SiOyniCDtkZzsi5wKMy4gSGlnaC1wZXJmb3JtYW5jZSBITUnsmYAg
7ZmU66m06rOE7Li1CjQuIEFsYXJtIGRlZmluaXRpb24sIHBoaWxvc29waHnsmYAgcmF0aW9uYWxp
emF0aW9uCjUuIEFsYXJtIHByaW9yaXR5LCBBY2tub3dsZWRnZeyZgCBSZXR1cm4tdG8tbm9ybWFs
CjYuIERlYWRiYW5kLCBEZWxheSwgU2hlbHZpbmfqs7wgU3VwcHJlc3Npb24KNy4gQWxhcm0gZmxv
b2QsIENoYXR0ZXJpbmcsIFN0YW5kaW5nIGFsYXJt6rO8IEtQSQo4LiBTZXRwb2ludMK3QWxhcm3C
t1RyaXDCt0ludGVybG9jayDqsJIg6rSA66asCjkuIFNPRSwg7Iuc6rCB64+Z6riwLCBIaXN0b3Jp
YW7qs7wgRmlyc3Qtb3V0CjEwLiBBdWRpdCB0cmFpbCwg7Jq07KCE7J6QIOq2jO2VnOqzvCBIdW1h
biBlcnJvciDrsKnsp4AKMTEuIEFibm9ybWFsIHNpdHVhdGlvbiBtYW5hZ2VtZW50CgojIyA0LiDs
oJzsmbgg67KU7JyE7JmAIG93bmVyc2hpcAoKIyMjIDQuMSBTVy0wMiDqsr3qs4QKClNXLTAz64qU
IEFsYXJtLCBTZXRwb2ludCwgU09FLCDtmZTrqbTtkZzsi5zsmYAg7Jq07KCE7J6QIOq2jO2VnOyd
hCDshozsnKDtlZzri6QuIEludGVybG9ja+qzvCBUcmlw7J2YIOyLpOygnCDsg4Htg5zsoITsnbQs
IExhdGNowrdSZXNldCwgQ2F1c2UgJiBFZmZlY3Qg7Iuk7ZaJ64W866asLCBGYWlsLXNhZmXsmYAg
UmVzdGFydOuKlCBTVy0wMuqwgCDshozsnKDtlZzri6QuCgojIyMgNC4yIFNXLTA0IOqyveqzhAoK
U1ctMDPripQg7Jq07KCE7KCV67O07J2YIOq4sOuKpeqzvCDsmrTsmIHsoJXssYXsnYQg64uk66Os
64ukLiBSZXF1aXJlbWVudCB0cmFjZWFiaWxpdHksIFVuaXTCt0ludGVncmF0aW9uwrdTeXN0ZW0g
dGVzdCwgU3RhdGljwrdEeW5hbWljIGFuYWx5c2lz7JmAIOydvOuwmCBTVyBWJlbripQgU1ctMDTq
sIAg7IaM7Jyg7ZWc64ukLgoKIyMjIDQuMyBTVy0xMCDqsr3qs4QKClNXLTAz64qUIFNldHBvaW50
IGxpc3QsIEFsYXJtIGxpc3TsmYAgSW50ZXJsb2NrIHZhbHVl7J2YIOuCtOyaqcK36rSA66as7JuQ
7LmZ7J2EIOuLpOujrOuLpC4g7ZSE66Gc7KCd7Yq4IOusuOyEnCDsnbjrj4QsIEZBVMK3U0FULCBM
b29wIHRlc3QsIENvbW1pc3Npb25pbmfsmYAgQWNjZXB0YW5jZSDsoIjssKjripQgU1ctMTDsnbQg
7IaM7Jyg7ZWc64ukLgoKIyMjIDQuNCBTVy0wNcK3U1ctMDgg6rK96rOECgpTSUwsIFBGRGF2Zywg
UEZILCBTYWZldHkgbGlmZWN5Y2xl7JmAIOuPheumveyEseydgCBTVy0wNeqwgCDshozsnKDtlZzr
i6QuIFNDQURBIO2GteyLoOuztOyViCwg64Sk7Yq47JuM7YGsIOu2hOumrOyZgCDsoJHqt7zthrXs
oJwg7JWE7YKk7YWN7LKY64qUIOuztOyViCBUb3BpY+ydtCDshozsnKDtlZzri6QuIFNXLTAz64qU
IOyatOyghOyekCDsl63tlaDqs7wg7ZmU66m07KGw7J6RIOq2jO2VnOunjCDri6Tro6zri6QuCgoj
IyA1LiBITUnCt1NDQURBIOq1rOyhsAoKSE1J64qUIOyatOyghOyekOqwgCDqs7XsoJXsg4Htg5zr
pbwg67O06rOgIOuqheugueydhCDsnoXroKXtlZjripQg7J247YSw7Y6Y7J207Iqk7J2064ukLiBT
Q0FEQeuKlCDsm5Dqsqkg7ISk67mE7JmAIOygnOyWtOq4sOydmCDrjbDsnbTthLDrpbwg7IiY7KeR
7ZWY6rOgIOqwkOyLnCwg66qF66C5LCBBbGFybSwg7J2066Cl6rO8IOuztOqzoOq4sOuKpeydhCDs
oJzqs7XtlZjripQg7IOB7JyEIOqwkOyLnOyytOqzhOydtOuLpC4KCuq1rOyhsCDshKTrqoXsl5Dr
ipQg64uk7J2MIO2dkOumhOydtCDtj6ztlajrkJjslrTslbwg7ZWc64ukLgoKYGBgdGV4dApTZW5z
b3LCt0FjdHVhdG9yCuKGkiBQTEPCt0RDU8K3UlRVCuKGkiBDb250cm9sIG5ldHdvcmsK4oaSIFND
QURBIHNlcnZlcsK3QWxhcm0gc2VydmVywrdIaXN0b3JpYW4K4oaSIEhNSSBjbGllbnTCt0VuZ2lu
ZWVyaW5nIHN0YXRpb24K4oaSIE9wZXJhdG9yIGFjdGlvbsK3QXVkaXQKYGBgCgrshJzrsoQg7J20
7KSR7ZmUIOyekOyytOunjOycvOuhnCDsi6DrorDshLHsnbQg7ZmV67O065CY64qUIOqyg+ydgCDs
lYTri4jri6QuIO2GteyLoOuLqOygiCwgRmFpbG92ZXIg7KeE7ZaJ7IOB7YOcLCBCYWTCt1VuY2Vy
dGFpbsK3U3RhbGUgcXVhbGl0eSwg7IiY64+Z64yA7LK06rCS6rO8IOyerOyXsOqysCDtm4Qg642w
7J207YSwIOydvOy5mOyEseydhCDtmZTrqbTsl5DshJwg6rWs67aE7ZW07JW8IO2VnOuLpC4KCiMj
IDYuIEhpZ2gtcGVyZm9ybWFuY2UgSE1JCgpIaWdoLXBlcmZvcm1hbmNlIEhNSeydmCDrqqnsoIHs
nYAg7ZmU66Ck7ZWcIO2ZlOuptOydtCDslYTri4jrnbwg67mg66W4IOyDge2ZqeyduOyLneydtOuL
pC4KCi0g7KCV7IOB7IOB7YOc64qUIOuCruydgCDsi5zqsIHsoIEg6rCV7KGw66W8IOyCrOyaqe2V
nOuLpC4KLSBBbGFybeqzvCDruYTsoJXsg4Eg7IOB7YOc64qUIOygnO2VnOuQnCDsg4nsg4Hqs7wg
6riw7Zi466GcIOqwleyhsO2VnOuLpC4KLSDtmITsnqzqsJLrp4wg7JWE64uI6528IOygleyDgeuy
lOychCwg7Y647LCoLCDrs4DtmZTrsKntlqXqs7wgVHJlbmTrpbwg7ZWo6ruYIOygnOqzte2VnOuL
pC4KLSDtmZTrqbQg7J2064+ZIO2bhOyXkOuPhCDshKTruYQg7JyE7LmYLCDsmrTsoITrqqjrk5ws
IOyEoO2DneuMgOyDgeqzvCDqtIDroKggQWxhcm3snZgg66el65297J2EIOycoOyngO2VnOuLpC4K
LSBDb21tYW5k7JmAIEZlZWRiYWNr7J2EIOuLpOuluCDtkZzsi5zroZwg6rWs67aE7ZWc64ukLgot
IEJhZMK3U3RhbGUgcXVhbGl0eeulvCDsoJXsg4Eg7LWc7Iug6rCS7LKY65+8IO2RnOyLnO2VmOyn
gCDslYrripTri6QuCgrtmZTrqbTqs4TsuLUg7JiI7Iuc64qUIOuLpOydjOqzvCDqsJnri6QuCgp8
IExldmVsIHwg66qp7KCBIHwg7ZW17IusIOygleuztCB8CnwtLS18LS0tfC0tLXwKfCBMZXZlbCAx
IHwg6rO17KCVIOyghOyytCBPdmVydmlldyB8IOyDneyCsOyDge2DnCwg7KO87JqUIOygnOyVvSwg
7J207IOBIOychOy5mCB8CnwgTGV2ZWwgMiB8IFVuaXTCt0FyZWEgfCDsnqXsuZjqtbAg7IOB7YOc
LCDso7zsmpQgQWxhcm3qs7wgVHJlbmQgfAp8IExldmVsIDMgfCDsg4HshLgg7Jq07KCEIHwgTG9v
cCwgVmFsdmUsIE1vdG9yLCBTZXF1ZW5jZSDsg4Htg5wgfAp8IExldmVsIDQgfCDsp4Tri6jCt+yg
leu5hCB8IOyDgeyEuCDsi6DtmLgsIO2SiOyniCwg7J2066ClLCDsnqXsuZjsp4Tri6ggfAoKIyMg
Ny4gQWxhcm3snZgg7KCV7J2Y7JmAIExpZmVjeWNsZQoKQWxhcm3snYAg67mE7KCV7IOBIOyDge2D
nOulvCDslYzrpqzqs6Ag7Jq07KCE7J6Q6rCAIOygle2VtOynhCDsi5zqsIQg7JWI7JeQIO2MkOuL
qCDrmJDripQg7KGw7LmY66W8IO2VmOuPhOuhnSDsmpTqtaztlZzri6QuIOyhsOy5mOqwgCDtlYTs
mpTtlZjsp4Ag7JWK7J2AIEV2ZW50LCBTdGF0dXPsmYAgTm90aWZpY2F0aW9u7J2AIEFsYXJt7Jy8
66GcIOunjOuTpOyngCDslYrripTri6QuCgpBbGFybSDsg4Htg5zripQgUHJvY2VzcyBjb25kaXRp
b27qs7wgQWNrbm93bGVkZ2VtZW5066W8IOu2hOumrO2VtOyEnCDsnbTtlbTtlbTslbwg7ZWc64uk
LgoKYGBgdGV4dApDb25kaXRpb24gbm9ybWFsCuKGkiBBbGFybSBhY3RpdmUgYW5kIHVuYWNrbm93
bGVkZ2VkCuKGkiBBbGFybSBhY3RpdmUgYW5kIGFja25vd2xlZGdlZArihpIgQ29uZGl0aW9uIHJl
dHVybmVkIHRvIG5vcm1hbArihpIgQWxhcm0gY2xlYXJlZCBhY2NvcmRpbmcgdG8gY29uZmlndXJl
ZCBhY2tub3dsZWRnZW1lbnQgcG9saWN5CmBgYAoKQWNrbm93bGVkZ2XripQg7Jq07KCE7J6Q6rCA
IEFsYXJt7J2EIOyduOyngO2WiOuLpOuKlCDquLDroZ3snbTri6QuIOybkOyduCDsoJzqsbAsIFBy
b2Nlc3MgY29uZGl0aW9uIO2VtOygnCDrmJDripQg7ISk67mE67O16rWs66W8IOydmOuvuO2VmOyn
gCDslYrripTri6QuCgojIyA4LiBBbGFybSBwaGlsb3NvcGh57JmAIHJhdGlvbmFsaXphdGlvbgoK
QWxhcm0gcGhpbG9zb3BoeeuKlCDsobDsp4Eg7KCE7LK07JeQIOyggeyaqe2VmOuKlCDsg4HsnIQg
7KCV7LGF7J2064ukLiDsl63tlaAsIOyasOyEoOyInOychCwg7ZGc7IucLCDsg4nsg4EsIEFja25v
d2xlZGdlLCBTaGVsdmluZywgU3VwcHJlc3Npb24sIEtQSSwg67OA6rK96rSA66as7JmAIOqygO2G
oOyjvOq4sOulvCDsoJXtlZzri6QuCgpBbGFybSByYXRpb25hbGl6YXRpb27snYAg6rCBIEFsYXJt
IO2bhOuztOulvCDqsoDthqDtlZjripQg7Zmc64+Z7J2064ukLgoKfCDtla3rqqkgfCDqsoDthqDr
grTsmqkgfAp8LS0tfC0tLXwKfCDsm5DsnbggfCDslrTrlqQg67mE7KCV7IOBIOyDge2DnOqwgCDr
sJzsg53tlojripTqsIAgfAp8IOqysOqzvCB8IOyhsOy5mO2VmOyngCDslYrsnLzrqbQg66y07JeH
7J20IOuwnOyDne2VmOuKlOqwgCB8Cnwg7KGw7LmYIHwg7Jq07KCE7J6Q6rCAIOyWtOuWpCDtlonr
j5nsnYQg7ZW07JW8IO2VmOuKlOqwgCB8Cnwg7J2R64u17Iuc6rCEIHwg7KGw7LmY6rCAIOycoO2a
qO2VnCDstZzrjIDsi5zqsITsnYAg7Ja866eI7J246rCAIHwKfCDsmrDshKDsiJzsnIQgfCDqsrDq
s7zsmYAg7J2R64u17Iuc6rCE7J2EIOyWtOuWu+qyjCDrsJjsmIHtlZjripTqsIAgfAp8IOyEpOyg
lSB8IEFsYXJtIHZhbHVlLCBEZWFkYmFuZOyZgCBEZWxheeuKlCDrrLTsl4fsnbjqsIAgfAp8IOyD
ge2DnOq0gOumrCB8IFNoZWx2aW5nIOuYkOuKlCBTdXBwcmVzc2lvbiDtl4jsmqnsobDqsbTsnYAg
66y07JeH7J246rCAIHwKfCDqt7zqsbAgfCDsirnsnbjsnpAsIOusuOyEnOyZgCDrs4Dqsr3snbTr
oKXsnYAg66y07JeH7J246rCAIHwKCiMjIDkuIEFsYXJtIHByaW9yaXR5CgpQcmlvcml0eeuKlCDs
uKHsoJXqsJLsnZgg7KCI64yA7YGs6riw66GcIOygle2VmOyngCDslYrripTri6QuCgpgYGB0ZXh0
ClByaW9yaXR5ID0gZihDb25zZXF1ZW5jZSBzZXZlcml0eSwgTWF4aW11bSBvcGVyYXRvciByZXNw
b25zZSB0aW1lKQpgYGAKCuqysOqzvOqwgCDsi6zqsIHtlZjqs6Ag7ZeI7JqpIOydkeuLteyLnOqw
hOydtCDsp6fsnYTsiJjroZ0g64aS7J2AIOyasOyEoOyInOychOqwgCDtlYTsmpTtlZjri6QuIOuP
meydvO2VnCBQcmlvcml0eeuKlCDtkZzsi5wsIOydjO2WpSwg64yA7J2R7KCI7LCo7JmAIOq1kOyc
oeyXkOyEnCDsnbzqtIDrkJwg7J2Y66+466W8IOqwgOyguOyVvCDtlZzri6QuCgojIyAxMC4gRGVh
ZGJhbmTsmYAgRGVsYXkKCkhpZ2ggYWxhcm3snZgg6rCc64WQ7KCBIOq0gOqzhOuKlCDri6TsnYzq
s7wg6rCZ64ukLgoKYGBgdGV4dArrsJzsg506ClBWIOKJpSBTUF9IIOyDge2DnOqwgCBUX29uIOyd
tOyDgSDsp4Dsho0KCuuzteq3gDoKUFYg4omkIFNQX0ggLSBEQl9IIOyDge2DnOqwgCBUX29mZiDs
nbTsg4Eg7KeA7IaNCmBgYAoKLSBEZWFkYmFuZOuKlCDrsJzsg50g7J6E6rOE6rCS6rO8IOuzteq3
gCDsnoTqs4TqsJIg7IKs7J207J2YIOqwkiDssKjsnbTsnbTri6QuCi0gRGVsYXnripQg7KGw6rG0
7J20IOycoOyngOuQmOyWtOyVvCDtlZjripQg7Iuc6rCE7J2064ukLgotIERlYWRiYW5k64qUIOqy
veqzhOu2gCDrhbjsnbTspojsl5Ag7Zqo6rO87KCB7J2064ukLgotIERlbGF564qUIOynp+ydgCDs
nbzsi5zrs4Drj5nsl5Ag7Zqo6rO87KCB7J2064ukLgotIOuRkCDqsJLsnbQg64SI66y0IO2BrOup
tCDsi6TsoJwgQWxhcm3snYQg64qm7LaU6rGw64KYIOqwgOumtCDsiJgg7J6I64ukLgoKIyMgMTEu
IFNoZWx2aW5n6rO8IFN1cHByZXNzaW9uCgp8IOq1rOu2hCB8IFNoZWx2aW5nIHwgU3VwcHJlc3Np
b24gfAp8LS0tfC0tLXwtLS18Cnwg7KCB7Jqp7KO87LK0IHwg6raM7ZWcIOyeiOuKlCDsmrTsoITs
npAgfCDshKTqs4TrkJwg7J6Q64+Z64W866asIHwKfCBUcmlnZ2VyIHwg7JWM66Ck7KeEIOydvOyL
nOyggSDsgqzsnKAgfCDshKTruYTsg4Htg5zCt+yatOyghOuqqOuTnMK364W866as7KGw6rG0IHwK
fCDquLDqsIQgfCDsoJztlZzsi5zqsIQgfCDsobDqsbTsnbQg7LC47J24IOuPmeyViCB8Cnwg6riw
66GdIHwg7IKs7Jqp7J6QLCDsgqzsnKAsIOyLnOyekSwg66eM66OMIHwgU3VwcHJlc3Npb24g7KGw
6rG06rO8IOyggeyaqeyDge2DnCB8Cnwg7ZW17Ius7JyE7ZeYIHwg66y06riw7ZWcIOydgO2PkCB8
IOyemOuqu+uQnCDsobDqsbTshKTqs4TroZwg7ZWE7JqU7ZWcIEFsYXJtIOuIhOudvSB8CgpTaGVs
dmluZ+ydgCBBbGFybSDsoJXsnZjsmYAg7J2066Cl7J2EIOyCreygnO2VmOyngCDslYrripTri6Qu
IFN1cHByZXNzaW9u7J2AIOyatOyghOyekOqwgCDtjrjsnZjsg4Eg7J6E7J2Y66GcIOyIqOq4sOuK
lCDquLDriqXsnbQg7JWE64uI64ukLgoKIyMgMTIuIEFsYXJtIGZsb29k7JmAIEtQSQoKQWxhcm0g
Zmxvb2TripQg7Ken7J2AIOyLnOqwhOyXkCBBbGFybeydtCDsp5HspJHrkJjslrQg7Jq07KCE7J6Q
7J2YIOyduOyngCwg7KeE64uo6rO8IOuMgOydkeydhCDrsKntlbTtlZjripQg7IOB7YOc7J2064uk
LiBDaGF0dGVyaW5n7J2AIOqwmeydgCBBbGFybeydtCDrsJjrs7Ug67Cc7IOdwrftlbTsoJzrkJjr
ipQg7ZiE7IOB7J2064ukLiBTdGFuZGluZyBhbGFybeydgCDsnqXquLDqsIQgQWN0aXZlIOyDge2D
nOuhnCDrgqjslYQg7KCV7IOBIOuwsOqyveyymOufvCDsnbjsi53rkJjripQgQWxhcm3snbTri6Qu
CgrqsJzshKDsiJzshJzripQg64uk7J2M6rO8IOqwmeuLpC4KCmBgYHRleHQK7JuQ7J247ISk67mE
7JmAIOyLoO2YuO2SiOyniCDqsJzshKAK4oaSIOu2iO2VhOyalCBBbGFybSDsoJzqsbAK4oaSIFJh
dGlvbmFsaXphdGlvbiDsnqzqsoDthqAK4oaSIERlYWRiYW5kwrdEZWxheSDsobDsoJUK4oaSIOyD
ge2DnOq4sOuwmCBTdXBwcmVzc2lvbgrihpIg7ZmU66m0wrfsoIjssKgg6rCc7ISgCuKGkiBLUEkg
7J6s7Y+J6rCACmBgYAoKS1BJIOyImOy5mOuKlCDtmITsnqUgQWxhcm0gcGhpbG9zb3BoeeyXkCDr
lLDrnbwg7KCV7ZWc64ukLiDsi5zqsITri7kg67Cc7IOd66WgLCBQZWFrIHJhdGUsIEZsb29kIOq1
rOqwhCwgU3RhbmRpbmfCt0NoYXR0ZXJpbmcgYWxhcm0sIOyasOyEoOyInOychCDrtoTtj6zsmYAg
U2hlbHZpbmcg7IKs7Jqp7ZiE7Zmp7J2EIOy2lOygge2VnOuLpC4KCiMjIDEzLiBTZXRwb2ludMK3
QWxhcm3Ct1RyaXDCt0ludGVybG9jayDqsJIKCnwg6rCSIHwg66qp7KCBIHwg7J2867CYIOyGjOyc
oCB8CnwtLS18LS0tfC0tLXwKfCDsmrTsoIQgU2V0cG9pbnQgfCDrqqntkZwg7Jq07KCE6rCSIHwg
7Jq07KCEwrfqs7XsoJUg7KCc7Ja0IHwKfCBBbGFybSB2YWx1ZSB8IOyatOyghOyekCDsobDsuZgg
7LSJ6rWsIHwgQWxhcm0g6rSA66asIHwKfCBUcmlwIHZhbHVlIHwg7J6Q64+ZIOuztO2YuOygleyn
gCB8IOuztO2YuOuFvOumrCB8CnwgSW50ZXJsb2NrIHZhbHVlIHwg64+Z7J6R7ZeI7JqpwrfquIjs
p4Ag7KGw6rG0IHwg7Iuk7ZaJIOygnOyWtOuFvOumrCB8Cgrsg4HsirnrsKntlqUg7JyE7ZeY67OA
7IiY7JeQ7ISc64qUIOygleyDgeyatOyghOuylOychCwgQWxhcm3qs7wgVHJpcCDsgqzsnbTsl5Ag
7Jq07KCE7J6QIOydkeuLteqzvCDqs7XsoJXrj5ntirnshLHsnYQg6rOg66Ck7ZWcIOyXrOycoOul
vCDrkZgg7IiYIOyeiOuLpC4g6re465+s64KYIOyDgeuMgOyInOyEnOuKlCDsnITtl5jrsKntlqXq
s7wg64W866as7JeQIOuUsOudvCDri6zrnbzsp4Drr4DroZwg66qo65OgIOqzteygleyXkCDtlZjr
gpjsnZgg7Iir7J6Q7Iic7ISc66W8IOqwleygnO2VmOuptCDslYgg65Cc64ukLgoKU2V0cG9pbnQg
bGlzdOyXkOuKlCBUYWcsIOq4sOuKpSwg6rCSLCDri6jsnIQsIOuwqe2WpSwgRGVhZGJhbmTCt0Rl
bGF5LCDsoIHsmqnrqqjrk5wsIOq3vOqxsCwg7Iq57J247J6QLCDrs4Dqsr3snbTroKXqs7wg6rSA
66CoIOuztO2YuOq4sOuKpSDssLjsobDrpbwg7Y+s7ZWo7ZWc64ukLgoKIyMgMTQuIFNPRSwgSGlz
dG9yaWFuLCBGaXJzdC1vdXTqs7wgQXVkaXQgdHJhaWwKClNPRSBldmVudOuKlCDri6TsnYwg7KCV
67O066GcIO2RnO2YhO2VoCDsiJgg7J6I64ukLgoKYGBgdGV4dAplX2kgPSAoU291cmNlIHRpbWVz
dGFtcCwgU2lnbmFsIHNvdXJjZSwgT2xkIHN0YXRlLCBOZXcgc3RhdGUsIFF1YWxpdHkpCmBgYAoK
U09F7J2YIOyEoO2bhOq0gOqzhOulvCDsi6DrorDtlZjroKTrqbQg7J6l7LmY7J2YIOyLnOqwgeuP
meq4sCwgVGltZXN0YW1wIOyDneyEseychOy5mCwg7KCV7ZmV64+ELCDrtoTtlbTriqUsIO2GteyL
oOyngOyXsOqzvCBUaW1lIHF1YWxpdHnrpbwg6rSA66as7ZW07JW8IO2VnOuLpC4KCnwg6riw64ql
IHwg6riw66Gd64yA7IOBIHwg7KO866qp7KCBIHwKfC0tLXwtLS18LS0tfAp8IEhpc3RvcmlhbiB8
IOqzteygleqwkuqzvCBUcmVuZCB8IOyepeq4sCDstpTshLjCt+yEseuKpSDrtoTshJ0gfAp8IFNP
RSB8IOydtOyCsCDsg4Htg5zrs4DtmZQgfCDsgqzqsbQg7ISg7ZuE6rSA6rOEIOu2hOyEnSB8Cnwg
Rmlyc3Qtb3V0IHwg7LWc7LSIIOycoO2aqCDsm5DsnbggfCDruaDrpbgg7LSI6riw7JuQ7J24IOyn
gOyLnCB8CnwgQXVkaXQgdHJhaWwgfCDsgqzsmqnsnpAg7ZaJ7JyE7JmAIOuzgOqyvSB8IOq2jO2V
nMK37LGF7J6Ewrfrs4Dqsr0g7LaU7KCBIHwKCiMjIDE1LiDsmrTsoITsnpAg6raM7ZWc6rO8IEh1
bWFuIGVycm9yIOuwqeyngAoK6raM7ZWc7J2AIOyXre2VoOq4sOuwmCDstZzshozqtoztlZzsnLzr
oZwg7ISk6rOE7ZWc64ukLiDspJHsmpQgU2V0cG9pbnQg67OA6rK9LCBTaGVsdmluZywgU3VwcHJl
c3Npb24g7Iq57J246rO8IOuztO2YuOq0gOugqCDsobDsnpHsnYAg7J6s7ZmV7J24LCDsnbTspJHs
irnsnbgg65iQ64qUIOuzhOuPhCDqtoztlZzsnbQg7ZWE7JqU7ZWgIOyImCDsnojri6QuCgpIdW1h
biBlcnJvciDrsKnsp4Drpbwg7JyE7ZW0IOuLpOydjOydhCDsoJzqs7XtlZzri6QuCgotIO2YhOye
rCBMb2NhbMK3UmVtb3Rl7JmAIE1hbnVhbMK3QXV0byDsg4Htg5wKLSDrqoXroLkg7IaM7Jyg6raM
6rO8IOyhsOyekeqwgOuKpSDsl6zrtoAKLSBJbnRlcmxvY2vCt1Blcm1pc3NpdmUg67aI66eM7KGx
IOyCrOycoAotIOyhsOyekeuMgOyDgeqzvCDsmIjsg4HqsrDqs7zsnZgg66qF7ZmV7ZWcIO2RnOyL
nAotIOykkeyalOyhsOyekSDtmZXsnbjqs7wg7Leo7IaMIOqyveuhnAotIENvbW1hbmQg7KCE7Iah
6rO8IOyLpOygnCBGZWVkYmFjayDrtoTrpqwKLSBUaW1lb3V0LCDrtojsnbzsuZjsmYAgQmFkIHF1
YWxpdHkg7ZGc7IucCi0g67O16rWs7JmAIFJvbGxiYWNrIOygiOywqAoKIyMgMTYuIEFibm9ybWFs
IHNpdHVhdGlvbiBtYW5hZ2VtZW50CgpgYGB0ZXh0CkRldGVjdArihpIgRGlhZ25vc2UK4oaSIFJl
c3BvbmQK4oaSIFJlY292ZXIK4oaSIFJldmlldwpgYGAKCk92ZXJ2aWV37JmAIFRyZW5k66GcIOyd
tOyDgeydhCDsobDquLDsl5Ag67Cc6rKs7ZWc64ukLiBBbGFybSwgU09F7JmAIOqzteygleunpeud
veycvOuhnCDsm5DsnbjsnYQg7KeE64uo7ZWc64ukLiDqtoztlZzqs7wg7KCI7LCo7JeQIOuUsOud
vCDrjIDsnZHtlZzri6QuIOyLpOygnCBGZWVkYmFja+qzvCDtkojsp4jsnYQg7ZmV7J247ZWY66mw
IOuzteq1rO2VnOuLpC4g7IKs7ZuE7JeQ64qUIEFsYXJtIEtQSSwgU09F7JmAIEF1ZGl0IHRyYWls
66GcIOuwmOuzteybkOyduOydhCDqsJzshKDtlZzri6QuCgojIyAxNy4g64yA7ZGcIEZhdGFsIOyY
pOulmAoKMS4g66qo65OgIEV2ZW5066W8IEFsYXJt7Jy866GcIOq1rOyEse2VnOuLpC4KMi4gQWxh
cm0sIFRyaXDqs7wgSW50ZXJsb2Nr7J2EIOqwmeydgCDquLDriqXsnLzroZwg67O464ukLgozLiBB
Y2tub3dsZWRnZeqwgCDqs7XsoJXsm5DsnbjsnYQg7ZW07KCc7ZWc64uk6rOgIOuzuOuLpC4KNC4g
UHJpb3JpdHnrpbwg7Lih7KCV6rCSIO2BrOq4sOunjOycvOuhnCDsoJXtlZzri6QuCjUuIERlYWRi
YW5k7JmAIERlbGF566W8IOqwmeydgCDquLDriqXsnLzroZwg67O464ukLgo2LiBTaGVsdmluZ+yd
tCBBbGFybSDsnbTroKXsnYQg7IKt7KCc7ZWc64uk6rOgIOuzuOuLpC4KNy4gU3VwcHJlc3Npb27q
s7wgU2hlbHZpbmfrpbwg64+Z7J287Iuc7ZWc64ukLgo4LiBTaGVsdmluZ+ulvCDrrLTquLDtlZwg
7Jyg7KeA7ZWc64ukLgo5LiDrhKQg7KKF66WY7J2YIOqwkuydhCDshJzroZwg67CU6r647Ja0IOyC
rOyaqe2VnOuLpC4KMTAuIOyLnOqwgeuPmeq4sCDsl4bsnbQgU09FIOyInOyEnOulvCDsi6DrorDt
lZzri6QuCjExLiBIaXN0b3JpYW7snbQgU09F66W8IO2VreyDgSDrjIDssrTtlZzri6Tqs6Ag67O4
64ukLgoxMi4gQXVkaXQgdHJhaWzqs7wgU09F66W8IOuPmeydvOyLnO2VnOuLpC4KMTMuIOuwneyd
gCDsg4nsnYQg66eO7J20IOyTuOyImOuhnSDsoovsnYAgSE1J65286rOgIOuzuOuLpC4KMTQuIOuq
qOuToCDqsJLsnYQg66y07KCc7ZWcIOuzgOqyve2VmOuPhOuhnSDtl4jsmqntlZzri6QuCjE1LiBI
TUkg66qF66C57J20IO2YhOyepeuPmeyekSDsmYTro4zrpbwg7Kad66qF7ZWc64uk6rOgIOuzuOuL
pC4KMTYuIOuqqOuToCBBbGFybeydmCBQcmlvcml0eeulvCDrhpLsl6wgRmxvb2Trpbwg7ZW06rKw
7ZWc64ukLgoKIyMgMTguIFdhcm4g7IiY7KSAIOu2gOyhseyCrO2VrQoKLSBITUnCt1NDQURBIOq1
rOyEseyalOyGjOunjCDrgpjsl7TtlZjqs6Ag7KCV67O07Iug66Kw7ISx7J2EIOuIhOudve2VqAot
IOyDieyDgeunjCDshKTrqoXtlZjqs6Ag7ZmU66m06rOE7Li16rO8IFRyZW5k66W8IOuIhOudve2V
qAotIFJhdGlvbmFsaXphdGlvbuyXkOyEnCDsmrTsoITsnpAg7KGw7LmY7JmAIOydkeuLteyLnOqw
hOydhCDriITrnb3tlagKLSBEZWFkYmFuZCwgRGVsYXksIFNoZWx2aW5n6rO8IFN1cHByZXNzaW9u
7J2YIOywqOydtOulvCDriITrnb3tlagKLSBTZXRwb2ludCBsaXN07J2YIOq3vOqxsCwg6raM7ZWc
6rO8IOuzgOqyveydtOugpeydhCDriITrnb3tlagKLSBTT0Xsl5DshJwg7Iuc6rCB64+Z6riw7JmA
IFRpbWUgcXVhbGl0eeulvCDriITrnb3tlagKLSDqtoztlZzsl5DshJwgQXVkaXQgdHJhaWzqs7wg
7KSR7JqU7KGw7J6RIO2ZleyduOydhCDriITrnb3tlagKLSDruYTsoJXsg4Hsg4HtmansnZgg67O1
6rWs7JmAIOyCrO2bhOqygO2GoOulvCDriITrnb3tlagKCiMjIDE5LiBGYWxzZSBwb3NpdGl2ZSDr
sKnsp4AKCuyngeygkeyggeyduCDrsJjrjIAg64uo7KCV66y466eMIEZhdGFsIO2bhOuztOuhnCDr
s7jri6QuIEFsYXJt7J20IFRyaXDsnYQg7Jyg67Cc7ZWgIOyImCDsnojri6TripQg7ISk66qF7J2A
IOuRkCDquLDriqXsnYQg64+Z7J287Iuc7ZWcIOqyg+ydtCDslYTri4jri6QuIFNoZWx2aW5n7J20
IO2ZlOuptOyXkOyEnCDsiKjquLTri6TripQg7ISk66qF64+EIOydtOugpSDsgq3soJwg7KO87J6l
6rO8IOuLpOultOuLpC4gSGlnaC1wZXJmb3JtYW5jZSBITUnripQg7IOJ7IOB7J2EIOyghO2YgCDs
gqzsmqntlZjsp4Ag7JWK64qUIOuwqeyLneydtCDslYTri4jrnbwg7KCc7ZWc65CcIOydmOuvuOuh
nCDsgqzsmqntlZjripQg67Cp7Iud7J2064ukLgoKIyMgMjAuIE1vZGVsIEFuc3dlciDqtozsnqUg
7Z2Q66aECgoxLiDsmrTsoITsoJXrs7Qg6rSA66as7J2YIOuqqeyggeqzvCBvd25lcnNoaXAKMi4g
SE1JwrdTQ0FEQSDqtazsobDsmYAg7KCV67O07Iug66Kw7ISxCjMuIEhpZ2gtcGVyZm9ybWFuY2Ug
SE1J7JmAIO2ZlOuptOqzhOy4tQo0LiBBbGFybSDssqDtlZnCt+2VqeumrO2ZlMK37Jqw7ISg7Iic
7JyECjUuIEFsYXJtIOyDge2DnOyZgCBudWlzYW5jZSDqtIDrpqwKNi4gU2V0cG9pbnTCt0FsYXJt
wrdUcmlwwrdJbnRlcmxvY2sg6rCSIOq0gOumrAo3LiBTT0XCt0hpc3RvcmlhbsK3Rmlyc3Qtb3V0
wrdBdWRpdCB0cmFpbAo4LiDqtoztlZzCt0h1bWFuIGVycm9ywrfruYTsoJXsg4Hsg4Htmakg64yA
7J2RCgojIyAyMS4g64yA7ZGcIOy2nOygnOusuOygnAoKMS4gSE1J7JmAIFNDQURB7J2YIOq1rOyh
sCwg6riw64qlIOuwjyDsi6DrorDshLEg7ISk6rOE6riw7KSA7J2EIOyEpOuqhe2VmOyLnOyYpC4K
Mi4gSGlnaC1wZXJmb3JtYW5jZSBITUnsnZgg7ISk6rOE7JuQ7LmZ6rO8IO2ZlOuptOqzhOy4teyd
hCDshKTrqoXtlZjsi5zsmKQuCjMuIEFsYXJtIHBoaWxvc29waHnsmYAgQWxhcm0gcmF0aW9uYWxp
emF0aW9u7J2YIOuqqeyggSDrsI8g7KCI7LCo66W8IOyEpOuqhe2VmOyLnOyYpC4KNC4gQWxhcm0g
cHJpb3JpdHksIERlYWRiYW5k7JmAIERlbGF57J2YIOyEoOygleq4sOykgOydhCDshKTrqoXtlZjs
i5zsmKQuCjUuIEFsYXJtIFNoZWx2aW5n6rO8IFN1cHByZXNzaW9u7J2YIOywqOydtOyZgCDqtIDr
pqzrsKnslYjsnYQg7ISk66qF7ZWY7Iuc7JikLgo2LiBTZXRwb2ludCwgQWxhcm0gdmFsdWUsIFRy
aXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl7J2YIOywqOydtCDrsI8g6rSA66as6riw7KSA7J2E
IOyEpOuqhe2VmOyLnOyYpC4KNy4gU09F7J2YIOybkOumrOyZgCDsi5zqsIHrj5nquLAsIEhpc3Rv
cmlhbiDrsI8gRmlyc3Qtb3V06rO87J2YIOq0gOqzhOulvCDshKTrqoXtlZjsi5zsmKQuCjguIOya
tOyghOygleuztCDsi5zsiqTthZzsnZggQXVkaXQgdHJhaWzqs7wg7Jq07KCE7J6QIOq2jO2VnCDq
tIDrpqzrsKnslYjsnYQg7ISk66qF7ZWY7Iuc7JikLgo5LiBBbGFybSBmbG9vZOyZgCBDaGF0dGVy
aW5n7J2YIOusuOygnOygkCDrsI8g6rCc7ISg67Cp7JWI7J2EIOyEpOuqhe2VmOyLnOyYpC4KMTAu
IEhNScK3U0NBREHrpbwg7J207Jqp7ZWcIEFibm9ybWFsIHNpdHVhdGlvbiBtYW5hZ2VtZW50IOuw
qeyViOydhCDshKTrqoXtlZjsi5zsmKQuCgojIyAyMi4gRm9jdXNlZCByZWdyZXNzaW9uIOuylOyc
hAoKLSBUb3BpYyBJROyZgCBzY2hlbWEgY29udHJhY3QKLSBBbmNob3IgSUQg7KSR67O16rO8IO2V
hOyImCDsnZjrr7jqtbAKLSBGYXRhbMK3TWFqb3LCt0ZhbHNlLXBvc2l0aXZlIGNvdW50Ci0gTW9k
ZWwgQW5zd2Vy7J2YIEFuY2hvciDssLjsobAg66y06rKw7ISxCi0g64ST7J2AIOuLqOydvCBSb3V0
aW5nIGFsaWFzIOuwsOygnAotIFNXLTAywrdTVy0wNMK3U1ctMTAg6rK96rOECi0gQWxhcm0gQWN0
aXZlwrdBY2tub3dsZWRnZSDqtIDqs4QKLSBEZWFkYmFuZMK3RGVsYXkg64W866asCi0gUHJpb3Jp
dHkg6rKw7KCV7JqU7IaMCi0gU09FIFRpbWVzdGFtcOyZgCDsi5zqsIHrj5nquLAKLSDsp4HsoJEg
7Jik64u1IO2MqO2EtOqzvCDrqoXsi5zsoIEg7KCV7KCV66y4IOq1rOu2hAo=
PAYLOAD_SW03_01

    write_payload 'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/README.md' '7318bfde752b002b7dc2950536895403e6549f229fc1261221ef5dd1a8c2ca1e' <<'PAYLOAD_SW03_02'
IyBITUnCt1NDQURBwrdBbGFybcK3U2V0cG9pbnTCt1RyaXDCt0ludGVybG9ja8K3U09FIOuwjyDs
mrTsoITsoJXrs7Qg6rSA66asCgojIyBUb3BpYyBJRAoKYGhtaV9zY2FkYV9hbGFybV9zZXRwb2lu
dF90cmlwX2ludGVybG9ja19zb2Vfb3BlcmF0b3JfaW5mb3JtYXRpb25fbWFuYWdlbWVudGAKCiMj
IOuqqeyggQoK7J20IFRvcGljIFBhY2vsnYAgSE1JwrdTQ0FEQSwgSGlnaC1wZXJmb3JtYW5jZSBI
TUksIEFsYXJtIGxpZmVjeWNsZSwgQWxhcm0gcmF0aW9uYWxpemF0aW9uLCBTZXRwb2ludCDqtIDr
pqwsIFNPRSwgQXVkaXQgdHJhaWwsIOyatOyghOyekCDqtoztlZzqs7wg67mE7KCV7IOB7IOB7Zmp
IOuMgOydkeydhCDtlZjrgpjsnZgg7Jq07KCE7KCV67O0IOq0gOumrCDssrTqs4TroZwg7Y+J6rCA
7ZWc64ukLgoKIyMg7Y+s7ZWoIOuylOychAoKLSBITUnCt1NDQURBIOq1rOyhsOyZgCDrjbDsnbTt
hLAg7ZKI7KeICi0gSGlnaC1wZXJmb3JtYW5jZSBITUnsmYAg7ZmU66m06rOE7Li1Ci0gQWxhcm0g
cGhpbG9zb3BoeeyZgCByYXRpb25hbGl6YXRpb24KLSBQcmlvcml0eSwgQWNrbm93bGVkZ2UsIERl
YWRiYW5k7JmAIERlbGF5Ci0gU2hlbHZpbmcsIFN1cHByZXNzaW9uLCBBbGFybSBmbG9vZOyZgCBL
UEkKLSBTZXRwb2ludMK3QWxhcm3Ct1RyaXDCt0ludGVybG9jayDqsJIg6rSA66asCi0gU09FLCBI
aXN0b3JpYW4sIEZpcnN0LW91dOqzvCBBdWRpdCB0cmFpbAotIE9wZXJhdG9yIGF1dGhvcml0eeyZ
gCBIdW1hbiBlcnJvciBwcmV2ZW50aW9uCi0gQWJub3JtYWwgc2l0dWF0aW9uIG1hbmFnZW1lbnQK
CiMjIG93bmVyc2hpcCDqsr3qs4QKCi0gU1ctMDMg7IaM7JygOiDsmrTsoITsnpAg7KCV67O0LCBB
bGFybSwgU2V0cG9pbnQsIFNPRSwgQXVkaXTsmYAg6raM7ZWcCi0gU1ctMDIg7J206rSAOiBUcmlw
wrdJbnRlcmxvY2sg7Iuk7ZaJ64W866asLCDsg4Htg5zsoITsnbQsIExhdGNowrdSZXNldOyZgCBG
YWlsLXNhZmUKLSBTVy0wNCDsnbTqtIA6IFYtTW9kZWwsIOy2lOyggeyEsSwg7J2867CYIFNXIFZl
cmlmaWNhdGlvbsK3VmFsaWRhdGlvbgotIFNXLTEwIOydtOq0gDog7ZSE66Gc7KCd7Yq4IOusuOyE
nCDsnbjrj4QsIEZBVMK3U0FULCDsi5zsmrTsoITsmYAgQWNjZXB0YW5jZQotIFNXLTA1IOydtOq0
gDogU0lMLCBQRkRhdmfCt1BGSOyZgCBTYWZldHkgbGlmZWN5Y2xlCgojIyDtlbXsi6wg64W866as
6rSA6rOECgpgYGB0ZXh0CkFsYXJtID0gYWJub3JtYWwgY29uZGl0aW9uIHJlcXVpcmluZyB0aW1l
bHkgb3BlcmF0b3IgYWN0aW9uClByaW9yaXR5ID0gZihjb25zZXF1ZW5jZSBzZXZlcml0eSwgYWxs
b3dhYmxlIHJlc3BvbnNlIHRpbWUpCkhpZ2ggYWxhcm0gYWN0aXZlOiBQViDiiaUgU1BfSCBmb3Ig
VF9vbgpIaWdoIGFsYXJtIGNsZWFyOiBQViDiiaQgU1BfSCAtIERCX0ggZm9yIFRfb2ZmClNPRSBl
dmVudCA9IHRpbWVzdGFtcCArIHNvdXJjZSArIHN0YXRlIHRyYW5zaXRpb24gKyBxdWFsaXR5CmBg
YAoKQWNrbm93bGVkZ2XripQg7Jq07KCE7J6QIOyduOyngOq4sOuhneydtOupsCBBbGFybSBjb25k
aXRpb24g7ZW07KCc6rCAIOyVhOuLiOuLpC4gRGVhZGJhbmTripQg6rCSIOq4sOuwmCDsnbTroKXt
j63snbTqs6AgRGVsYXnripQg7Iuc6rCEIOq4sOuwmCDtlYTthLDsnbTri6QuIFNoZWx2aW5n7J2A
IOygnO2VnOyLnOqwhOydmCDsmrTsoITsnpAg7J6E7Iuc7KGw7LmY7J206rOgIFN1cHByZXNzaW9u
7J2AIOyEpOqzhOuQnCDsg4Htg5zsobDqsbTsl5Ag65Sw66W4IOyekOuPmeygnOyZuOydtOuLpC4K
CiMjIOuMgO2RnCDsmKTri7UKCi0g66qo65OgIEV2ZW5064qUIEFsYXJt7J2064ukLgotIEFsYXJt
LCBUcmlw6rO8IEludGVybG9ja+ydgCDqsJnsnYAg6riw64ql7J2064ukLgotIEFja25vd2xlZGdl
6rCAIOybkOyduOydhCDtlbTsoJztlZzri6QuCi0gRGVhZGJhbmTsmYAgRGVsYXnripQg6rCZ7J2A
IOq4sOuKpeydtOuLpC4KLSBTaGVsdmluZ+ydtCBBbGFybSDsnbTroKXsnYQg7IKt7KCc7ZWc64uk
LgotIOyLnOqwgeuPmeq4sCDsl4bsnbTrj4QgU09FIOyInOyEnOuKlCDtla3sg4Eg7KCV7ZmV7ZWY
64ukLgotIEhpc3RvcmlhbiwgU09F7JmAIEF1ZGl0IHRyYWls7J2AIOqwmeydgCDquLDroZ3snbTr
i6QuCi0g67Cd7J2AIOyDieydhCDrp47snbQg7JOw64qUIEhNSeqwgCDrjZQg7Jqw7IiY7ZWY64uk
LgotIEhNSSDrqoXroLkg7KCE7Iah7J20IO2YhOyepeuPmeyekSDsmYTro4zrpbwg7Kad66qF7ZWc
64ukLgoKIyMg7YyM7J28CgotIGBmYWN0X2FuY2hvci5qc29uYDogMzHqsJwgRmFjdCBBbmNob3Ls
mYAgMTbqsJwgRmF0YWwg7Jik64u1Ci0gYGxvZ2ljX2NoZWNrLmpzb25gOiBkZXRlcm1pbmlzdGlj
IGFpZCwgTExNIHRydXRoIHNjaGVtYSwgTWFqb3LsmYAgZmFsc2UtcG9zaXRpdmUg7KGw6rG0Ci0g
YG1vZGVsX2Fuc3dlci5qc29uYDog64yA7ZGcIOusuOygnCAxMOqwnCwg64u17JWI6rWs7KGwIDjq
sJzsmYAgUm91dGluZyDsoJXrs7QKLSBgdG9waWNfaW1wb3J0YW5jZS5qc29uYDog64Kc7J2064+E
7JmAIOyEoO2DnSDspJHsmpTrj4QKLSBgZG9jcy90b3BpY19zaGVldHMvaG1pX3NjYWRhX2FsYXJt
X3NldHBvaW50X3RyaXBfaW50ZXJsb2NrX3NvZV9vcGVyYXRvcl9pbmZvcm1hdGlvbl9tYW5hZ2Vt
ZW50Lm1kYDog7IOB7IS4IFRvcGljIFNoZWV0Ci0gYHNjcmlwdHMvdGVzdF9obWlfc2NhZGFfYWxh
cm1fc2V0cG9pbnRfc29lX29wZXJhdG9yX2luZm9ybWF0aW9uLnB5YDogZm9jdXNlZCByZWdyZXNz
aW9uCgojIyDqsoDspp0g6rK96rOECgpUb3BpYy1sb2NhbCBhdXRob3Jpbmcg64uo6rOE7JeQ7ISc
64qUIEpTT04sIHNvdXJjZSBzY2hlbWEsIFRvcGljIHF1YWxpdHksIGZvY3VzZWQgdGVzdCwgd2hp
dGVzcGFjZSwgYGdpdCBkaWZmIC0tY2hlY2tg7JmAIExhbmUgQSBvd25lcnNoaXDrp4wg6rKA7Kad
7ZWc64ukLiBHZW5lcmF0ZWQgcmVidWlsZCwg7KCE7LK0IFJvdXRlciDtmozqt4AsIGNyb3NzLXRv
cGljIGR1cGxpY2F0ZSwgdmFsaWRhdGUtYWxsLCByZWxlYXNlIHZhbGlkYXRpb27smYAgY29udGFp
bmVyIHNtb2tl64qUIOy1nOyihSDthrXtlakg64uo6rOE66GcIOuEmOq4tOuLpC4K
PAYLOAD_SW03_02

    write_payload 'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/fact_anchor.json' '9a3524311a28d89f9b9cbd795f1561975eed4df8c63550981439d86ab1dba0dd' <<'PAYLOAD_SW03_03'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLmZhY3RfYW5jaG9yLnYxIiwKICAidG9w
aWNfaWQiOiAiaG1pX3NjYWRhX2FsYXJtX3NldHBvaW50X3RyaXBfaW50ZXJsb2NrX3NvZV9vcGVy
YXRvcl9pbmZvcm1hdGlvbl9tYW5hZ2VtZW50IiwKICAidGl0bGVfa28iOiAiSE1JwrdTQ0FEQcK3
QWxhcm3Ct1NldHBvaW50wrdUcmlwwrdJbnRlcmxvY2vCt1NPRSDrsI8g7Jq07KCE7KCV67O0IOq0
gOumrCIsCiAgInF1ZXN0aW9uX3R5cGVfaGludCI6ICJQUklOQ0lQTEVfSU5URVJQUkVUQVRJT04i
LAogICJhbmNob3JzIjogWwogICAgewogICAgICAiaWQiOiAic3cwM19zY29wZV9vcGVyYXRvcl9p
bmZvcm1hdGlvbiIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwM19zY29wZV9vcGVyYXRvcl9pbmZv
cm1hdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiU1ctMDPripQgSE1JwrdTQ0FEQSDqtazsobAs
IOqzoOyEseuKpSBITUksIEFsYXJtIOq0gOumrCwgU2V0cG9pbnTCt0FsYXJtwrdUcmlwwrdJbnRl
cmxvY2sg6rCSIOq0gOumrCwgU09FLCBBdWRpdCB0cmFpbCwg7Jq07KCE7J6QIOq2jO2VnOqzvCDr
uYTsoJXsg4Hsg4Htmakg64yA7J2R7J2EIOyatOyghOygleuztCDqtIDrpqwg7LK06rOE66GcIOyX
sOqysO2VnOuLpC4iLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdvcmRz
IjogWwogICAgICAgICLsmrTsoITsoJXrs7Qg6rSA66asIiwKICAgICAgICAiSE1JIiwKICAgICAg
ICAiU0NBREEiLAogICAgICAgICJBbGFybSIsCiAgICAgICAgIlNldHBvaW50IiwKICAgICAgICAi
U09FIiwKICAgICAgICAi7Jq07KCE7J6QIOq2jO2VnCIKICAgICAgXSwKICAgICAgImNvcmVfdGVy
bXMiOiBbCiAgICAgICAgIuyatOyghOygleuztCDqtIDrpqwiLAogICAgICAgICJITUkiLAogICAg
ICAgICJBbGFybSIsCiAgICAgICAgIlNPRSIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxh
bmF0aW9ucyI6IFsKICAgICAgICAiU1ctMDPripQgSE1JwrdTQ0FEQSDqtazsobAsIOqzoOyEseuK
pSBITUksIEFsYXJtIOq0gOumrCwgU2V0cG9pbnTCt0FsYXJtwrdUcmlwwrdJbnRlcmxvY2sg6rCS
IOq0gOumrCwgU09FLCBBdWRpdCB0cmFpbCwg7Jq07KCE7J6QIOq2jO2VnOqzvCDruYTsoJXsg4Hs
g4Htmakg64yA7J2R7J2EIOyatOyghOygleuztCDqtIDrpqwg7LK06rOE66GcIOyXsOqysO2VnOuL
pC4iLAogICAgICAgICLsmrTsoITsoJXrs7Qg6rSA66asLCBITUksIEFsYXJtLCBTT0XsnZgg6rSA
6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzsi5wsIOyatOyghOyekCDsobDsuZjsmYAg6riw66Gd
IOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhw
bGFuYXRpb25zIjogWwogICAgICAgICJITUnCt0FsYXJtwrdTT0Xrpbwg6rCZ7J2AIOq4sOuKpeyc
vOuhnCDst6jquIntlZjqsbDrgpggU1ctMDIg7Iuk7ZaJ64W866as7JmAIFNXLTEwIOyduOyImOyg
iOywqOq5jOyngCBTVy0wM+ydtCDsp4HsoJEg7IaM7Jyg7ZWc64uk6rOgIOuzuOuLpC4iCiAgICAg
IF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2A
IGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITs
l5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAi
c291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyg
hOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfaG1p
X3NjYWRhX2FyY2hpdGVjdHVyZSIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwM19obWlfc2NhZGFf
YXJjaGl0ZWN0dXJlIiwKICAgICAgInN0YXRlbWVudCI6ICJITUnripQg7Jq07KCE7J6Q7JmAIOyg
nOyWtOyLnOyKpO2FnOydmCDsg4HtmLjsnpHsmqkg7ZmU66m07J2EIOygnOqzte2VmOqzoCwgU0NB
REHripQg7JuQ6rKpIOqwkOyLnMK3642w7J207YSwIOyImOynkcK366qF66C5wrfqsr3rs7TCt+yd
tOugpSDquLDriqXsnYQg7ISc67KELCDthrXsi6Drp50sIO2YhOyepSDsoJzslrTquLDsmYAg7Jew
6rOE7ZWY64qUIOyDgeychCDqsJDsi5zssrTqs4TsnbTri6QuIiwKICAgICAgImltcG9ydGFuY2Ui
OiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiSE1JIiwKICAgICAgICAiU0NB
REEiLAogICAgICAgICLshJzrsoQiLAogICAgICAgICLtmITsnqUg7KCc7Ja06riwIiwKICAgICAg
ICAi642w7J207YSwIOyImOynkSIsCiAgICAgICAgIuqwkOyLnCIsCiAgICAgICAgIuuqheuguSIK
ICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkhNSSIsCiAgICAgICAgIlND
QURBIiwKICAgICAgICAi7IOB7JyEIOqwkOyLnOyytOqzhCIsCiAgICAgICAgIu2YhOyepSDsoJzs
lrTquLAiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAg
IkhNSeuKlCDsmrTsoITsnpDsmYAg7KCc7Ja07Iuc7Iqk7YWc7J2YIOyDge2YuOyekeyaqSDtmZTr
qbTsnYQg7KCc6rO17ZWY6rOgLCBTQ0FEQeuKlCDsm5Dqsqkg6rCQ7IucwrfrjbDsnbTthLAg7IiY
7KeRwrfrqoXroLnCt+qyveuztMK37J2066ClIOq4sOuKpeydhCDshJzrsoQsIO2GteyLoOunnSwg
7ZiE7J6lIOygnOyWtOq4sOyZgCDsl7Dqs4TtlZjripQg7IOB7JyEIOqwkOyLnOyytOqzhOydtOuL
pC4iLAogICAgICAgICJITUksIFNDQURBLCDsg4HsnIQg6rCQ7Iuc7LK06rOELCDtmITsnqUg7KCc
7Ja06riw7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw
7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAg
InJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiSE1J7JmAIFNDQURB66W8IOuPmeyd
vCDsnqXsuZjroZwg67O06rGw64KYIFNDQURB7J2YIOybkOqyqeyImOynkcK37ISc67KEwrfthrXs
i6DCt+ydtOugpSDqtazsobDrpbwg7ISk66qF7ZWY7KeAIOyViuuKlOuLpC4iCiAgICAgIF0sCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFs
IO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw
6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNl
X2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuz
tCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfYXJjaGl0ZWN0
dXJlX3JlZHVuZGFuY3lfcXVhbGl0eSIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwM19hcmNoaXRl
Y3R1cmVfcmVkdW5kYW5jeV9xdWFsaXR5IiwKICAgICAgInN0YXRlbWVudCI6ICJITUnCt1NDQURB
IOq1rOyhsOuKlCDshJzrsoTsmYAg64Sk7Yq47JuM7YGs7J2YIOydtOykke2ZlCDsl6zrtoDrv5Ag
7JWE64uI6528IO2GteyLoCDri6jsoIgsIEZhaWxvdmVyLCDrjbDsnbTthLAg7ZKI7KeILCBTdGFs
ZSDsg4Htg5wg67CPIOyerOyXsOqysCDtm4Qg642w7J207YSwIOydvOy5mOyEseydhCDsmrTsoITs
npDsl5Dqsowg66qF7ZmV7Z6IIOyghOuLrO2VtOyVvCDtlZzri6QuIiwKICAgICAgImltcG9ydGFu
Y2UiOiAiaW1wb3J0YW50IiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJSZWR1bmRhbmN5
IiwKICAgICAgICAiRmFpbG92ZXIiLAogICAgICAgICJEYXRhIHF1YWxpdHkiLAogICAgICAgICJT
dGFsZSIsCiAgICAgICAgIu2GteyLoCDri6jsoIgiLAogICAgICAgICLsnqzsl7DqsrAiCiAgICAg
IF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJGYWlsb3ZlciIsCiAgICAgICAgIuuN
sOydtO2EsCDtkojsp4giLAogICAgICAgICJTdGFsZSIsCiAgICAgICAgIuyerOyXsOqysCIKICAg
ICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiSE1JwrdTQ0FE
QSDqtazsobDripQg7ISc67KE7JmAIOuEpO2KuOybjO2BrOydmCDsnbTspJHtmZQg7Jes67aA67+Q
IOyVhOuLiOudvCDthrXsi6Ag64uo7KCILCBGYWlsb3Zlciwg642w7J207YSwIO2SiOyniCwgU3Rh
bGUg7IOB7YOcIOuwjyDsnqzsl7DqsrAg7ZuEIOuNsOydtO2EsCDsnbzsuZjshLHsnYQg7Jq07KCE
7J6Q7JeQ6rKMIOuqhe2Zle2eiCDsoITri6ztlbTslbwg7ZWc64ukLiIsCiAgICAgICAgIkZhaWxv
dmVyLCDrjbDsnbTthLAg7ZKI7KeILCBTdGFsZSwg7J6s7Jew6rKw7J2YIOq0gOqzhOulvCDrqqns
oIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5Ds
hJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6
IFsKICAgICAgICAi7ISc67KEwrfrhKTtirjsm4ztgawg7J207KSR7ZmU66eMIOyeiOycvOuptCBG
YWlsb3ZlciDspJEg7ZKI7KeIwrdTdGFsZcK37Ya17Iug64uo7KCIwrfsnqzsl7DqsrAg67aI7J28
7LmY66W8IO2RnOyLnO2VoCDtlYTsmpTqsIAg7JeG64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFs
IO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw
6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNl
X2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuz
tCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfaGlnaF9wZXJm
b3JtYW5jZV9obWkiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfaGlnaF9wZXJmb3JtYW5jZV9o
bWkiLAogICAgICAic3RhdGVtZW50IjogIkhpZ2gtcGVyZm9ybWFuY2UgSE1J64qUIOygleyDgeyD
ge2DnOydmCDrtojtlYTsmpTtlZwg7J6l7Iud7J2EIOykhOydtOqzoCDqs7XsoJXsg4Htg5wsIO2O
uOywqCwg7LaU7IS47JmAIOu5hOygleyDgSDsp5Xtm4Trpbwg67mg66W06rKMIOyduOyngO2VmOuP
hOuhnSDsoJXrs7Qg67CA64+E7JmAIOyLnOqwgeyggSDsmrDshKDsiJzsnITrpbwg7ISk6rOE7ZWc
64ukLiIsCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAia2V5d29yZHMiOiBbCiAg
ICAgICAgIkhpZ2gtcGVyZm9ybWFuY2UgSE1JIiwKICAgICAgICAi7IOB7Zmp7J247IudIiwKICAg
ICAgICAi7Y647LCoIiwKICAgICAgICAi7LaU7IS4IiwKICAgICAgICAi7Iuc6rCB7KCBIOyasOyE
oOyInOychCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkhpZ2gtcGVy
Zm9ybWFuY2UgSE1JIiwKICAgICAgICAi7IOB7Zmp7J247IudIiwKICAgICAgICAi7LaU7IS4IiwK
ICAgICAgICAi7Jqw7ISg7Iic7JyEIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRp
b25zIjogWwogICAgICAgICJIaWdoLXBlcmZvcm1hbmNlIEhNSeuKlCDsoJXsg4Hsg4Htg5zsnZgg
67aI7ZWE7JqU7ZWcIOyepeyLneydhCDspITsnbTqs6Ag6rO17KCV7IOB7YOcLCDtjrjssKgsIOy2
lOyEuOyZgCDruYTsoJXsg4Eg7KeV7ZuE66W8IOu5oOultOqyjCDsnbjsp4DtlZjrj4TroZ0g7KCV
67O0IOuwgOuPhOyZgCDsi5zqsIHsoIEg7Jqw7ISg7Iic7JyE66W8IOyEpOqzhO2VnOuLpC4iLAog
ICAgICAgICJIaWdoLXBlcmZvcm1hbmNlIEhNSSwg7IOB7Zmp7J247IudLCDstpTshLgsIOyasOyE
oOyInOychOydmCDqtIDqs4Trpbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg7Jq07KCE7J6QIOyh
sOy5mOyZgCDquLDroZ0g6rSA7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAgICAgIF0sCiAgICAg
ICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuuwneydgCDsg4nqs7wgM0Qg7J6l
7Iud7J2EIOunjuydtCDsgqzsmqntlaDsiJjroZ0g7IOB7Zmp7J247Iud7J20IO2WpeyDgeuQnOuL
pOqzoCDrs7jri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHs
nbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDr
rLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nq
sIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIEhNScK3U0NB
REEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5mSIKICAgIH0sCiAgICB7CiAg
ICAgICJpZCI6ICJzdzAzX2Rpc3BsYXlfaGllcmFyY2h5IiwKICAgICAgImFuY2hvcl9pZCI6ICJz
dzAzX2Rpc3BsYXlfaGllcmFyY2h5IiwKICAgICAgInN0YXRlbWVudCI6ICLtmZTrqbTqs4TsuLXs
nYAg7J2867CY7KCB7Jy866GcIExldmVsIDEg6rO17KCVIOyghOyytCBPdmVydmlldywgTGV2ZWwg
MiBVbml0wrdBcmVhLCBMZXZlbCAzIOyDgeyEuCDsmrTsoIQsIExldmVsIDQg7KeE64uowrfsoJXr
uYQg7KCV67O066GcIOq1rOyEse2VmOupsCDsg4HsnITsl5DshJwg7J207IOBIOychOy5mOulvCDs
sL7qs6Ag7ZWY7JyE7JeQ7IScIOybkOyduOqzvCDsobDsuZjrpbwg7ZmV7J247ZWY64+E66GdIOyX
sOqysO2VnOuLpC4iLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdvcmRz
IjogWwogICAgICAgICJEaXNwbGF5IGhpZXJhcmNoeSIsCiAgICAgICAgIkxldmVsIDEiLAogICAg
ICAgICJMZXZlbCAyIiwKICAgICAgICAiTGV2ZWwgMyIsCiAgICAgICAgIkxldmVsIDQiLAogICAg
ICAgICJPdmVydmlldyIsCiAgICAgICAgIuynhOuLqCIKICAgICAgXSwKICAgICAgImNvcmVfdGVy
bXMiOiBbCiAgICAgICAgIkRpc3BsYXkgaGllcmFyY2h5IiwKICAgICAgICAiT3ZlcnZpZXciLAog
ICAgICAgICLsg4HshLgg7Jq07KCEIiwKICAgICAgICAi7KeE64uoIgogICAgICBdLAogICAgICAi
YWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLtmZTrqbTqs4TsuLXsnYAg7J2867CY
7KCB7Jy866GcIExldmVsIDEg6rO17KCVIOyghOyytCBPdmVydmlldywgTGV2ZWwgMiBVbml0wrdB
cmVhLCBMZXZlbCAzIOyDgeyEuCDsmrTsoIQsIExldmVsIDQg7KeE64uowrfsoJXruYQg7KCV67O0
66GcIOq1rOyEse2VmOupsCDsg4HsnITsl5DshJwg7J207IOBIOychOy5mOulvCDssL7qs6Ag7ZWY
7JyE7JeQ7IScIOybkOyduOqzvCDsobDsuZjrpbwg7ZmV7J247ZWY64+E66GdIOyXsOqysO2VnOuL
pC4iLAogICAgICAgICJEaXNwbGF5IGhpZXJhcmNoeSwgT3ZlcnZpZXcsIOyDgeyEuCDsmrTsoIQs
IOynhOuLqOydmCDqtIDqs4Trpbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg7Jq07KCE7J6QIOyh
sOy5mOyZgCDquLDroZ0g6rSA7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAgICAgIF0sCiAgICAg
ICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIk92ZXJ2aWV3IOyXhuydtCDsg4Hs
hLjtmZTrqbTrp4wg7KCc6rO17ZWY6rGw64KYIO2ZlOuptOqzhOy4tSDsgqzsnbTsnZgg7J207IOB
IOychOy5mMK37JuQ7J24wrfsobDsuZgg66el6529IOyXsOqysOydtCDtlYTsmpQg7JeG64uk6rOg
IOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDr
sJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2V
rSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2V
nOuLpC4iLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDr
sI8gQWxhcm3Ct+yatOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDNfY29sb3JfY29udGV4dF9uYXZpZ2F0aW9uIiwKICAgICAgImFuY2hvcl9pZCI6
ICJzdzAzX2NvbG9yX2NvbnRleHRfbmF2aWdhdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAi7IOJ
7IOB7J2AIOygleyDgSDsnqXsi53rs7Tri6QgQWxhcm0sIOu5hOygleyDgSwg7ISg7YOd7IOB7YOc
7JmAIO2SiOyniOyggO2VmCDrk7Eg7KCc7ZWc65CcIOydmOuvuOyXkCDsnbzqtIDrkJjqsowg7IKs
7Jqp7ZWY6rOgLCDtmZTrqbQg7J2064+ZIOyLnCDshKTruYQg7JyE7LmYwrfsmrTsoITrqqjrk5zC
t+y2lOyEuMK36rSA66CoIEFsYXJt7J2YIOunpeudveydtCDsnKDsp4DrkJjslrTslbwg7ZWc64uk
LiIsCiAgICAgICJpbXBvcnRhbmNlIjogImltcG9ydGFudCIsCiAgICAgICJrZXl3b3JkcyI6IFsK
ICAgICAgICAiQ29sb3IgY29kaW5nIiwKICAgICAgICAiQ29udGV4dCIsCiAgICAgICAgIk5hdmln
YXRpb24iLAogICAgICAgICLsmrTsoITrqqjrk5wiLAogICAgICAgICJBbGFybSIsCiAgICAgICAg
Iu2SiOyniOyggO2VmCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIuyD
ieyDgSIsCiAgICAgICAgIuunpeudvSIsCiAgICAgICAgIu2ZlOuptCDsnbTrj5kiLAogICAgICAg
ICLtkojsp4jsoIDtlZgiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBb
CiAgICAgICAgIuyDieyDgeydgCDsoJXsg4Eg7J6l7Iud67O064ukIEFsYXJtLCDruYTsoJXsg4Es
IOyEoO2DneyDge2DnOyZgCDtkojsp4jsoIDtlZgg65OxIOygnO2VnOuQnCDsnZjrr7jsl5Ag7J28
6rSA65CY6rKMIOyCrOyaqe2VmOqzoCwg7ZmU66m0IOydtOuPmSDsi5wg7ISk67mEIOychOy5mMK3
7Jq07KCE66qo65OcwrfstpTshLjCt+q0gOugqCBBbGFybeydmCDrp6Xrnb3snbQg7Jyg7KeA65CY
7Ja07JW8IO2VnOuLpC4iLAogICAgICAgICLsg4nsg4EsIOunpeudvSwg7ZmU66m0IOydtOuPmSwg
7ZKI7KeI7KCA7ZWY7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITs
npAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwK
ICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7KCV7IOB7IOB7YOc6rmM
7KeAIOqwle2VnCDsg4nsnLzroZwg7IOB7IucIOyepeyLne2VmOqxsOuCmCDtmZTrqbQg7J2064+Z
IOyLnCDshKTruYQg7JyE7LmYwrdNb2RlwrdUcmVuZMK36rSA66CoIEFsYXJtIOunpeudveydhCDs
noPslrTrj4Qg65Cc64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVz
IjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6js
iJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3
YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDs
grDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgog
ICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfYWxhcm1fZGVmaW5pdGlvbiIsCiAgICAgICJh
bmNob3JfaWQiOiAic3cwM19hbGFybV9kZWZpbml0aW9uIiwKICAgICAgInN0YXRlbWVudCI6ICJB
bGFybeydgCDruYTsoJXsg4Eg7IOB7YOc66W8IOyatOyghOyekOyXkOqyjCDslYzrpqzqs6Ag7KCV
7ZW07KeEIOyLnOqwhCDslYjsl5Ag7YyQ64uoIOuYkOuKlCDsobDsuZjrpbwg7JqU6rWs7ZWY64qU
IOq4sOuKpeydtOupsCwg7KGw7LmY6rCAIO2VhOyalO2VmOyngCDslYrsnYAg64uo7IicIEV2ZW50
wrdTdGF0dXPCt05vdGlmaWNhdGlvbuqzvCDqtazrtoTtlZzri6QuIiwKICAgICAgImltcG9ydGFu
Y2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiQWxhcm0iLAogICAgICAg
ICLsmrTsoITsnpAg7KGw7LmYIiwKICAgICAgICAi67mE7KCV7IOBIOyDge2DnCIsCiAgICAgICAg
IkV2ZW50IiwKICAgICAgICAiU3RhdHVzIiwKICAgICAgICAiTm90aWZpY2F0aW9uIgogICAgICBd
LAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAiQWxhcm0iLAogICAgICAgICLsmrTsoITs
npAg7KGw7LmYIiwKICAgICAgICAiRXZlbnQiLAogICAgICAgICLruYTsoJXsg4Eg7IOB7YOcIgog
ICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJBbGFybeyd
gCDruYTsoJXsg4Eg7IOB7YOc66W8IOyatOyghOyekOyXkOqyjCDslYzrpqzqs6Ag7KCV7ZW07KeE
IOyLnOqwhCDslYjsl5Ag7YyQ64uoIOuYkOuKlCDsobDsuZjrpbwg7JqU6rWs7ZWY64qUIOq4sOuK
peydtOupsCwg7KGw7LmY6rCAIO2VhOyalO2VmOyngCDslYrsnYAg64uo7IicIEV2ZW50wrdTdGF0
dXPCt05vdGlmaWNhdGlvbuqzvCDqtazrtoTtlZzri6QuIiwKICAgICAgICAiQWxhcm0sIOyatOyg
hOyekCDsobDsuZgsIEV2ZW50LCDruYTsoJXsg4Eg7IOB7YOc7J2YIOq0gOqzhOulvCDrqqnsoIEs
IOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg
7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsK
ICAgICAgICAi66qo65OgIEV2ZW50wrdTdGF0dXPCt05vdGlmaWNhdGlvbuydhCBBbGFybeycvOuh
nCDrp4zrk6TqsbDrgpgg7Jq07KCE7J6QIOyhsOy5mOqwgCDtlYTsmpQg7JeG64qUIOyDge2DnOuP
hCBBbGFybeydtOudvOqzoCDrs7jri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6
ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7Iic
IOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2Fy
buycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw
7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5mSIKICAg
IH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX2FsYXJtX3BoaWxvc29waHkiLAogICAgICAiYW5j
aG9yX2lkIjogInN3MDNfYWxhcm1fcGhpbG9zb3BoeSIsCiAgICAgICJzdGF0ZW1lbnQiOiAiQWxh
cm0gcGhpbG9zb3BoeeuKlCBBbGFybeydmCDrqqnsoIEsIOyXre2VoCwg7Jqw7ISg7Iic7JyEIOq4
sOykgCwg7IOB7YOc7ZGc7ZiELCDsirnsnbjqtoztlZwsIFNoZWx2aW5nwrdTdXBwcmVzc2lvbiwg
7ISx64ql7KeA7ZGcLCDrs4Dqsr3qtIDrpqzsmYAg7KO86riw7KCBIOqygO2GoCDsm5DsuZnsnYQg
7KGw7KeBIOywqOybkOyXkOyEnCDsoJXsnZjtlZwg7IOB7JyEIOygleyxheydtOuLpC4iLAogICAg
ICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJBbGFy
bSBwaGlsb3NvcGh5IiwKICAgICAgICAi7KCV7LGFIiwKICAgICAgICAi7Jqw7ISg7Iic7JyEIiwK
ICAgICAgICAiU2hlbHZpbmciLAogICAgICAgICJTdXBwcmVzc2lvbiIsCiAgICAgICAgIuyEseuK
peyngO2RnCIsCiAgICAgICAgIuuzgOqyveq0gOumrCIKICAgICAgXSwKICAgICAgImNvcmVfdGVy
bXMiOiBbCiAgICAgICAgIkFsYXJtIHBoaWxvc29waHkiLAogICAgICAgICLsg4HsnIQg7KCV7LGF
IiwKICAgICAgICAi7Jqw7ISg7Iic7JyEIiwKICAgICAgICAi67OA6rK96rSA66asIgogICAgICBd
LAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJBbGFybSBwaGlsb3Nv
cGh564qUIEFsYXJt7J2YIOuqqeyggSwg7Jet7ZWgLCDsmrDshKDsiJzsnIQg6riw7KSALCDsg4Ht
g5ztkZztmIQsIOyKueyduOq2jO2VnCwgU2hlbHZpbmfCt1N1cHByZXNzaW9uLCDshLHriqXsp4Dt
kZwsIOuzgOqyveq0gOumrOyZgCDso7zquLDsoIEg6rKA7YagIOybkOy5meydhCDsobDsp4Eg7LCo
7JuQ7JeQ7IScIOygleydmO2VnCDsg4HsnIQg7KCV7LGF7J2064ukLiIsCiAgICAgICAgIkFsYXJt
IHBoaWxvc29waHksIOyDgeychCDsoJXssYUsIOyasOyEoOyInOychCwg67OA6rK96rSA66as7J2Y
IOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4
sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVk
X2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm0gcGhpbG9zb3BoeeulvCDqsJzrs4QgVGFn
IOyEpOygle2RnOyZgCDrj5nsnbzsi5ztlZjqsbDrgpgg7Jqw7ISg7Iic7JyEwrdTaGVsdmluZ8K3
U3VwcHJlc3Npb27Ct+uzgOqyveq0gOumrCDsm5DsuZkg7JeG7J20IOyatOyYge2VnOuLpC4iCiAg
ICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l
7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTs
nITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAg
ICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+ya
tOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNf
YWxhcm1fcmF0aW9uYWxpemF0aW9uIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX2FsYXJtX3Jh
dGlvbmFsaXphdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiQWxhcm0gcmF0aW9uYWxpemF0aW9u
7J2AIOqwgSDtm4Trs7QgQWxhcm3sl5Ag64yA7ZW0IOybkOyduCwg6rKw6rO8LCDsmrTsoITsnpAg
7KGw7LmYLCDtl4jsmqkg7J2R64u17Iuc6rCELCDsmrDshKDsiJzsnIQsIOyEpOygleqwkiwgRGVh
ZGJhbmQsIERlbGF5LCBTaGVsdmluZyDtl4jsmqnsobDqsbTqs7wg66y47IScIOq3vOqxsOulvCDq
soDthqDtlZjsl6wg7ZWE7JqU7ZWcIEFsYXJt66eMIOyKueyduO2VmOuKlCDtmZzrj5nsnbTri6Qu
IiwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAg
ICAiQWxhcm0gcmF0aW9uYWxpemF0aW9uIiwKICAgICAgICAi7JuQ7J24IiwKICAgICAgICAi6rKw
6rO8IiwKICAgICAgICAi7Jq07KCE7J6QIOyhsOy5mCIsCiAgICAgICAgIuydkeuLteyLnOqwhCIs
CiAgICAgICAgIkRlYWRiYW5kIiwKICAgICAgICAiRGVsYXkiCiAgICAgIF0sCiAgICAgICJjb3Jl
X3Rlcm1zIjogWwogICAgICAgICJBbGFybSByYXRpb25hbGl6YXRpb24iLAogICAgICAgICLsmrTs
oITsnpAg7KGw7LmYIiwKICAgICAgICAi7J2R64u17Iuc6rCEIiwKICAgICAgICAi7ISk7KCV6rCS
IgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJBbGFy
bSByYXRpb25hbGl6YXRpb27snYAg6rCBIO2bhOuztCBBbGFybeyXkCDrjIDtlbQg7JuQ7J24LCDq
srDqs7wsIOyatOyghOyekCDsobDsuZgsIO2XiOyaqSDsnZHri7Xsi5zqsIQsIOyasOyEoOyInOyc
hCwg7ISk7KCV6rCSLCBEZWFkYmFuZCwgRGVsYXksIFNoZWx2aW5nIO2XiOyaqeyhsOqxtOqzvCDr
rLjshJwg6re86rGw66W8IOqygO2GoO2VmOyXrCDtlYTsmpTtlZwgQWxhcm3rp4wg7Iq57J247ZWY
64qUIO2ZnOuPmeydtOuLpC4iLAogICAgICAgICJBbGFybSByYXRpb25hbGl6YXRpb24sIOyatOyg
hOyekCDsobDsuZgsIOydkeuLteyLnOqwhCwg7ISk7KCV6rCS7J2YIOq0gOqzhOulvCDrqqnsoIEs
IOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg
7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsK
ICAgICAgICAi7JuQ7J24wrfqsrDqs7zCt+yatOyghOyekCDsobDsuZjCt+2XiOyaqSDsnZHri7Xs
i5zqsIQg6rKA7YagIOyXhuydtCDtm4Trs7Qg7Iug7Zi466W8IOuqqOuRkCBBbGFybeycvOuhnCDs
irnsnbjtlZzri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHs
nbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDr
rLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nq
sIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIEhNScK3U0NB
REEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5mSIKICAgIH0sCiAgICB7CiAg
ICAgICJpZCI6ICJzdzAzX2FsYXJtX3ByaW9yaXR5IiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAz
X2FsYXJtX3ByaW9yaXR5IiwKICAgICAgInN0YXRlbWVudCI6ICJBbGFybSBwcmlvcml0eeuKlCDr
i6jsiJwg7Lih7KCV6rCSIO2BrOq4sOqwgCDslYTri4jrnbwg7KGw7LmY7ZWY7KeAIOyViuyVmOyd
hCDrlYzsnZgg6rKw6rO8IOyLrOqwgeuPhOyZgCDsmrTsoITsnpDsl5Dqsowg7ZeI7Jqp65CcIOyd
keuLteyLnOqwhOydhCDtlajqu5gg7Y+J6rCA7ZWY7JesIOqysOygle2VmOupsCwg7Jqw7ISg7Iic
7JyE67OEIO2RnOyLnOyZgCDrjIDsnZHsoIjssKjqsIAg7J286rSA65CY7Ja07JW8IO2VnOuLpC4i
LAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdvcmRzIjogWwogICAgICAg
ICJBbGFybSBwcmlvcml0eSIsCiAgICAgICAgIkNvbnNlcXVlbmNlIHNldmVyaXR5IiwKICAgICAg
ICAiUmVzcG9uc2UgdGltZSIsCiAgICAgICAgIuyasOyEoOyInOychCIsCiAgICAgICAgIuuMgOyd
keygiOywqCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkFsYXJtIHBy
aW9yaXR5IiwKICAgICAgICAi6rKw6rO8IOyLrOqwgeuPhCIsCiAgICAgICAgIuydkeuLteyLnOqw
hCIsCiAgICAgICAgIuuMgOydkeygiOywqCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxh
bmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm0gcHJpb3JpdHnripQg64uo7IicIOy4oeygleqwkiDt
gazquLDqsIAg7JWE64uI6528IOyhsOy5mO2VmOyngCDslYrslZjsnYQg65WM7J2YIOqysOqzvCDs
i6zqsIHrj4TsmYAg7Jq07KCE7J6Q7JeQ6rKMIO2XiOyaqeuQnCDsnZHri7Xsi5zqsITsnYQg7ZWo
6ruYIO2PieqwgO2VmOyXrCDqsrDsoJXtlZjrqbAsIOyasOyEoOyInOychOuzhCDtkZzsi5zsmYAg
64yA7J2R7KCI7LCo6rCAIOydvOq0gOuQmOyWtOyVvCDtlZzri6QuIiwKICAgICAgICAiQWxhcm0g
cHJpb3JpdHksIOqysOqzvCDsi6zqsIHrj4QsIOydkeuLteyLnOqwhCwg64yA7J2R7KCI7LCo7J2Y
IOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4
sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVk
X2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiUFYg7YGs6riw64KYIOyepeu5hCDspJHsmpTrj4Qg
7ZWY64KY66eM7Jy866GcIEFsYXJtIHByaW9yaXR566W8IOygle2VmOqzoCDqsrDqs7wg7Ius6rCB
64+E7JmAIO2XiOyaqSDsnZHri7Xsi5zqsITsnYQg6rOg66Ck7ZWY7KeAIOyViuuKlOuLpC4iCiAg
ICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l
7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTs
nITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAg
ICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+ya
tOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNf
YWxhcm1fc3RhdGVfYWNrbm93bGVkZ2VtZW50IiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX2Fs
YXJtX3N0YXRlX2Fja25vd2xlZGdlbWVudCIsCiAgICAgICJzdGF0ZW1lbnQiOiAiQWxhcm3snZgg
UHJvY2VzcyBjb25kaXRpb24sIEFjdGl2ZcK3UmV0dXJuLXRvLW5vcm1hbCDsg4Htg5zsmYAgQWNr
bm93bGVkZ2VtZW50IOyDge2DnOuKlCDrs4TqsJzsnbTrqbAsIOyatOyghOyekCBBY2tub3dsZWRn
ZeuKlCDsnbjsp4Ag6riw66Gd7J28IOu/kCDsm5Dsnbgg7KCc6rGwIOuYkOuKlCBBbGFybSDsobDq
sbQg7ZW07KCc66W8IOydmOuvuO2VmOyngCDslYrripTri6QuIiwKICAgICAgImltcG9ydGFuY2Ui
OiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiQWxhcm0gc3RhdGUiLAogICAg
ICAgICJBY3RpdmUiLAogICAgICAgICJSZXR1cm4gdG8gbm9ybWFsIiwKICAgICAgICAiQWNrbm93
bGVkZ2VtZW50IiwKICAgICAgICAi7JuQ7J24IOygnOqxsCIKICAgICAgXSwKICAgICAgImNvcmVf
dGVybXMiOiBbCiAgICAgICAgIkFsYXJtIHN0YXRlIiwKICAgICAgICAiQWNrbm93bGVkZ2VtZW50
IiwKICAgICAgICAiUmV0dXJuLXRvLW5vcm1hbCIsCiAgICAgICAgIuybkOyduCIKICAgICAgXSwK
ICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm3snZggUHJvY2Vz
cyBjb25kaXRpb24sIEFjdGl2ZcK3UmV0dXJuLXRvLW5vcm1hbCDsg4Htg5zsmYAgQWNrbm93bGVk
Z2VtZW50IOyDge2DnOuKlCDrs4TqsJzsnbTrqbAsIOyatOyghOyekCBBY2tub3dsZWRnZeuKlCDs
nbjsp4Ag6riw66Gd7J28IOu/kCDsm5Dsnbgg7KCc6rGwIOuYkOuKlCBBbGFybSDsobDqsbQg7ZW0
7KCc66W8IOydmOuvuO2VmOyngCDslYrripTri6QuIiwKICAgICAgICAiQWxhcm0gc3RhdGUsIEFj
a25vd2xlZGdlbWVudCwgUmV0dXJuLXRvLW5vcm1hbCwg7JuQ7J247J2YIOq0gOqzhOulvCDrqqns
oIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5Ds
hJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6
IFsKICAgICAgICAiQWNrbm93bGVkZ2XqsIAg6rO17KCVIOybkOyduCDsoJzqsbDsmYAgQWN0aXZl
IGNvbmRpdGlvbiDtlbTsoJzrpbwg7J2Y66+47ZWc64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFs
IO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw
6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNl
X2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuz
tCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfYWxhcm1fZGVh
ZGJhbmQiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfYWxhcm1fZGVhZGJhbmQiLAogICAgICAi
c3RhdGVtZW50IjogIkRlYWRiYW5k64qUIEFsYXJt7J20IOuwnOyDne2VnCDrkqQg7KCV7IOBIOuz
teq3gCDsnoTqs4TqsJLsnYQg67Cc7IOdIOyehOqzhOqwkuqzvCDri6TrpbTqsowg65GQ64qUIOqw
kuydmCDsnbTroKXtj63snLzroZwsIOqyveqzhCDrtoDqt7wg64W47J207KaI7JeQIOydmO2VnCDr
sJjrs7Ug67Cc7IOd6rO8IO2VtOygnOulvCDspITsnbjri6QuIiwKICAgICAgImltcG9ydGFuY2Ui
OiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiRGVhZGJhbmQiLAogICAgICAg
ICJIeXN0ZXJlc2lzIiwKICAgICAgICAi67Cc7IOdIOyehOqzhOqwkiIsCiAgICAgICAgIuuzteq3
gCDsnoTqs4TqsJIiLAogICAgICAgICJDaGF0dGVyaW5nIgogICAgICBdLAogICAgICAiY29yZV90
ZXJtcyI6IFsKICAgICAgICAiRGVhZGJhbmQiLAogICAgICAgICLrsJzsg50g7J6E6rOE6rCSIiwK
ICAgICAgICAi67O16reAIOyehOqzhOqwkiIsCiAgICAgICAgIkNoYXR0ZXJpbmciCiAgICAgIF0s
CiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkRlYWRiYW5k64qUIEFs
YXJt7J20IOuwnOyDne2VnCDrkqQg7KCV7IOBIOuzteq3gCDsnoTqs4TqsJLsnYQg67Cc7IOdIOye
hOqzhOqwkuqzvCDri6TrpbTqsowg65GQ64qUIOqwkuydmCDsnbTroKXtj63snLzroZwsIOqyveqz
hCDrtoDqt7wg64W47J207KaI7JeQIOydmO2VnCDrsJjrs7Ug67Cc7IOd6rO8IO2VtOygnOulvCDs
pITsnbjri6QuIiwKICAgICAgICAiRGVhZGJhbmQsIOuwnOyDnSDsnoTqs4TqsJIsIOuzteq3gCDs
noTqs4TqsJIsIENoYXR0ZXJpbmfsnZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzsi5ws
IOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6QuIgog
ICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJEZWFkYmFu
ZOulvCDsi5zqsITsp4Dsl7Dqs7wg64+Z7J287Iuc7ZWY6rGw64KYIOuwnOyDncK367O16reAIOye
hOqzhOqwkiDssKjsnbQg7JeG7J20IENoYXR0ZXJpbmfsnYQg7ZW06rKw7ZWc64uk6rOgIOuzuOuL
pC4iCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg
7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTq
tazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4i
LAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxh
cm3Ct+yatOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjog
InN3MDNfYWxhcm1fZGVsYXkiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfYWxhcm1fZGVsYXki
LAogICAgICAic3RhdGVtZW50IjogIkFsYXJtIGRlbGF564qUIOyhsOqxtOydtCDsnbzsoJUg7Iuc
6rCEIOyXsOyGjSDsnKDsp4DrkKAg65WMIOuwnOyDneyLnO2CpOqxsOuCmCDsoJXsg4Hsg4Htg5zq
sIAg7J287KCVIOyLnOqwhCDsnKDsp4DrkKAg65WMIO2VtOygnO2VmOuKlCDsi5zqsIQg7ZWE7YSw
7J2066mwLCDsi6TsoJzroZwg7ZWE7JqU7ZWcIOynp+ydgCDsnZHri7XsnYQg6rCA66as7KeAIOyV
iuuPhOuhnSDqs7XsoJUg64+Z7Yq57ISx6rO8IO2XiOyaqSDsnZHri7Xsi5zqsITsnYQg6rOg66Ck
7ZWc64ukLiIsCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAia2V5d29yZHMiOiBb
CiAgICAgICAgIkFsYXJtIGRlbGF5IiwKICAgICAgICAiT24tZGVsYXkiLAogICAgICAgICJPZmYt
ZGVsYXkiLAogICAgICAgICLsi5zqsIQg7ZWE7YSwIiwKICAgICAgICAi6rO17KCVIOuPme2KueyE
sSIsCiAgICAgICAgIuydkeuLteyLnOqwhCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBb
CiAgICAgICAgIkFsYXJtIGRlbGF5IiwKICAgICAgICAi7Iuc6rCEIO2VhO2EsCIsCiAgICAgICAg
IuqzteyglSDrj5ntirnshLEiLAogICAgICAgICLsnZHri7Xsi5zqsIQiCiAgICAgIF0sCiAgICAg
ICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkFsYXJtIGRlbGF564qUIOyhsOqx
tOydtCDsnbzsoJUg7Iuc6rCEIOyXsOyGjSDsnKDsp4DrkKAg65WMIOuwnOyDneyLnO2CpOqxsOuC
mCDsoJXsg4Hsg4Htg5zqsIAg7J287KCVIOyLnOqwhCDsnKDsp4DrkKAg65WMIO2VtOygnO2VmOuK
lCDsi5zqsIQg7ZWE7YSw7J2066mwLCDsi6TsoJzroZwg7ZWE7JqU7ZWcIOynp+ydgCDsnZHri7Xs
nYQg6rCA66as7KeAIOyViuuPhOuhnSDqs7XsoJUg64+Z7Yq57ISx6rO8IO2XiOyaqSDsnZHri7Xs
i5zqsITsnYQg6rOg66Ck7ZWc64ukLiIsCiAgICAgICAgIkFsYXJtIGRlbGF5LCDsi5zqsIQg7ZWE
7YSwLCDqs7XsoJUg64+Z7Yq57ISxLCDsnZHri7Xsi5zqsITsnZgg6rSA6rOE66W8IOuqqeyggSwg
7KGw6rG0LCDtkZzsi5wsIOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDs
hKTrqoXtlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwog
ICAgICAgICJEZWxheeulvCDqsJLsnZgg7J2066Cl7Y+t7Jy866GcIOyEpOuqhe2VmOqxsOuCmCDq
s7XsoJUg64+Z7Yq57ISx6rO8IO2XiOyaqSDsnZHri7Xsi5zqsITsl5Ag6rSA6rOE7JeG7J20IOq4
uOqyjCDshKTsoJXtlbTrj4Qg65Cc64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAgICJncmFk
aW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2bhOuztOyd
tOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528IG1ham9y
IOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNlX2Jhc2lzIjog
IuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuztCDqtIDrpqwg
7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfYWxhcm1fc2hlbHZpbmciLAog
ICAgICAiYW5jaG9yX2lkIjogInN3MDNfYWxhcm1fc2hlbHZpbmciLAogICAgICAic3RhdGVtZW50
IjogIlNoZWx2aW5n7J2AIOq2jO2VnCDsnojripQg7Jq07KCE7J6Q6rCAIOyVjOugpOynhCDsgqzs
nKDroZwg7Yq57KCVIEFsYXJt7J2EIOygnO2VnOyLnOqwhCDrj5nslYggQWN0aXZlIGRpc3BsYXns
l5DshJwg7J6E7Iuc66GcIOyIqOq4sOuKlCDsmrTsoITtlonsnITsnbTrqbAsIEFsYXJtIOygleyd
mOyZgCDsnbTroKXsnYAg7Jyg7KeA7ZWY6rOgIOyCrOycoMK37IKs7Jqp7J6Qwrfsi5zsnpHCt+un
jOujjOulvCDquLDroZ3tlZzri6QuIiwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAg
ICJrZXl3b3JkcyI6IFsKICAgICAgICAiU2hlbHZpbmciLAogICAgICAgICLsoJztlZzsi5zqsIQi
LAogICAgICAgICLqtoztlZwiLAogICAgICAgICJBY3RpdmUgZGlzcGxheSIsCiAgICAgICAgIuyC
rOycoCIsCiAgICAgICAgIuunjOujjCIsCiAgICAgICAgIuydtOugpSIKICAgICAgXSwKICAgICAg
ImNvcmVfdGVybXMiOiBbCiAgICAgICAgIlNoZWx2aW5nIiwKICAgICAgICAi7KCc7ZWc7Iuc6rCE
IiwKICAgICAgICAi6raM7ZWcIiwKICAgICAgICAi7J2066ClIgogICAgICBdLAogICAgICAiYWNj
ZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJTaGVsdmluZ+ydgCDqtoztlZwg7J6I64qU
IOyatOyghOyekOqwgCDslYzroKTsp4Qg7IKs7Jyg66GcIO2KueyglSBBbGFybeydhCDsoJztlZzs
i5zqsIQg64+Z7JWIIEFjdGl2ZSBkaXNwbGF57JeQ7IScIOyehOyLnOuhnCDsiKjquLDripQg7Jq0
7KCE7ZaJ7JyE7J2066mwLCBBbGFybSDsoJXsnZjsmYAg7J2066Cl7J2AIOycoOyngO2VmOqzoCDs
gqzsnKDCt+yCrOyaqeyekMK37Iuc7J6Rwrfrp4zro4zrpbwg6riw66Gd7ZWc64ukLiIsCiAgICAg
ICAgIlNoZWx2aW5nLCDsoJztlZzsi5zqsIQsIOq2jO2VnCwg7J2066Cl7J2YIOq0gOqzhOulvCDr
qqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDs
l5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9u
cyI6IFsKICAgICAgICAiU2hlbHZpbmfsnbQgQWxhcm0g7KCV7J2YwrfsnbTroKXsnYQg7IKt7KCc
7ZWc64uk6rOgIOuztOqxsOuCmCDsgqzsnKDCt+q2jO2VnMK366eM66OMIOyXhuydtCDrrLTquLDt
lZwg7Iio6rKo64+EIOuQnOuLpOqzoCDrs7jri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19u
b3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg
64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDr
ipQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzr
sJgg7IKw7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5
mSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX2FsYXJtX3N1cHByZXNzaW9uIiwKICAg
ICAgImFuY2hvcl9pZCI6ICJzdzAzX2FsYXJtX3N1cHByZXNzaW9uIiwKICAgICAgInN0YXRlbWVu
dCI6ICJTdXBwcmVzc2lvbuydgCDshKTruYTsg4Htg5wsIOyatOyghOuqqOuTnCDrmJDripQg64W8
66as7KGw6rG07IOBIOydmOuvuOqwgCDsl4bripQgQWxhcm3snYQg7ISk6rOE65CcIOyhsOqxtOyX
kCDrlLDrnbwg7J6Q64+Z7Jy866GcIOuwnOyDne2VmOyngCDslYrqsowg7ZWY6rGw64KYIO2RnOyL
nOuMgOyDgeyXkOyEnCDsoJzsmbjtlZjripQg6riw64ql7J2066mwLCDsmrTsoITsnpAg7J6E7J2Y
IFNoZWx2aW5n6rO8IOq1rOu2hO2VnOuLpC4iLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwK
ICAgICAgImtleXdvcmRzIjogWwogICAgICAgICJTdXBwcmVzc2lvbiIsCiAgICAgICAgIuyatOyg
hOuqqOuTnCIsCiAgICAgICAgIuyEpOu5hOyDge2DnCIsCiAgICAgICAgIuyekOuPmSDsobDqsbQi
LAogICAgICAgICJTaGVsdmluZyDqtazrtoQiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjog
WwogICAgICAgICJTdXBwcmVzc2lvbiIsCiAgICAgICAgIuyEpOqzhCDsobDqsbQiLAogICAgICAg
ICLsmrTsoITrqqjrk5wiLAogICAgICAgICJTaGVsdmluZyIKICAgICAgXSwKICAgICAgImFjY2Vw
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiU3VwcHJlc3Npb27snYAg7ISk67mE7IOB7YOc
LCDsmrTsoITrqqjrk5wg65iQ64qUIOuFvOumrOyhsOqxtOyDgSDsnZjrr7jqsIAg7JeG64qUIEFs
YXJt7J2EIOyEpOqzhOuQnCDsobDqsbTsl5Ag65Sw6528IOyekOuPmeycvOuhnCDrsJzsg53tlZjs
p4Ag7JWK6rKMIO2VmOqxsOuCmCDtkZzsi5zrjIDsg4Hsl5DshJwg7KCc7Jm47ZWY64qUIOq4sOuK
peydtOupsCwg7Jq07KCE7J6QIOyehOydmCBTaGVsdmluZ+qzvCDqtazrtoTtlZzri6QuIiwKICAg
ICAgICAiU3VwcHJlc3Npb24sIOyEpOqzhCDsobDqsbQsIOyatOyghOuqqOuTnCwgU2hlbHZpbmfs
nZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzsi5wsIOyatOyghOyekCDsobDsuZjsmYAg
6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6QuIgogICAgICBdLAogICAgICAicmVqZWN0
ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJTdXBwcmVzc2lvbuydhCDsmrTsoITsnpDsnZgg
7J6E7J2YIFNoZWx2aW5n6rO8IOuPmeydvOyLnO2VmOqxsOuCmCDshKTqs4TrkJwg7IOB7YOcwrdN
b2RlIOyhsOqxtCDsl4bsnbQg7IiY64+Z7Jy866GcIOyIqOq4sOuKlCDquLDriqXsnbTrnbzqs6Ag
67O464ukLiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuw
mOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWt
IOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc
64ukLiIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuw
jyBBbGFybcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAi
aWQiOiAic3cwM19hbGFybV9mbG9vZF9jaGF0dGVyaW5nIiwKICAgICAgImFuY2hvcl9pZCI6ICJz
dzAzX2FsYXJtX2Zsb29kX2NoYXR0ZXJpbmciLAogICAgICAic3RhdGVtZW50IjogIkFsYXJtIGZs
b29k64qUIOynp+ydgCDsi5zqsITsl5Ag66eO7J2AIEFsYXJt7J20IOynkeykkeuQmOyWtCDsmrTs
oITsnpDsnZgg7J247KeAwrfsp4Tri6jCt+yhsOy5mOulvCDrsKntlbTtlZjripQg7IOB7YOc7J20
6rOgLCBDaGF0dGVyaW5n7J2AIOqwmeydgCBBbGFybeydtCDrsJjrs7Ug67Cc7IOdwrftlbTsoJzr
kJjripQg7ZiE7IOB7J2066+A66GcIOybkOyduCDsoJzqsbAsIO2VqeumrO2ZlCwgRGVhZGJhbmTC
t0RlbGF57JmAIOyDge2DnOq4sOuwmCBTdXBwcmVzc2lvbuycvOuhnCDqsJzshKDtlZzri6QuIiwK
ICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAi
QWxhcm0gZmxvb2QiLAogICAgICAgICJDaGF0dGVyaW5nIiwKICAgICAgICAi7J247KeA67aA7ZWY
IiwKICAgICAgICAiRGVhZGJhbmQiLAogICAgICAgICJEZWxheSIsCiAgICAgICAgIlN1cHByZXNz
aW9uIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAiQWxhcm0gZmxvb2Qi
LAogICAgICAgICJDaGF0dGVyaW5nIiwKICAgICAgICAi7J247KeA67aA7ZWYIiwKICAgICAgICAi
7JuQ7J24IOygnOqxsCIKICAgICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsK
ICAgICAgICAiQWxhcm0gZmxvb2TripQg7Ken7J2AIOyLnOqwhOyXkCDrp47snYAgQWxhcm3snbQg
7KeR7KSR65CY7Ja0IOyatOyghOyekOydmCDsnbjsp4DCt+ynhOuLqMK37KGw7LmY66W8IOuwqe2V
tO2VmOuKlCDsg4Htg5zsnbTqs6AsIENoYXR0ZXJpbmfsnYAg6rCZ7J2AIEFsYXJt7J20IOuwmOuz
tSDrsJzsg53Ct+2VtOygnOuQmOuKlCDtmITsg4HsnbTrr4DroZwg7JuQ7J24IOygnOqxsCwg7ZWp
66as7ZmULCBEZWFkYmFuZMK3RGVsYXnsmYAg7IOB7YOc6riw67CYIFN1cHByZXNzaW9u7Jy866Gc
IOqwnOyEoO2VnOuLpC4iLAogICAgICAgICJBbGFybSBmbG9vZCwgQ2hhdHRlcmluZywg7J247KeA
67aA7ZWYLCDsm5Dsnbgg7KCc6rGw7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7Iuc
LCDsmrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIK
ICAgICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm0g
Zmxvb2Trpbwg66qo65OgIFByaW9yaXR5IOyDge2WpeydtOuCmCBBbGFybSDstpTqsIDroZwg7ZW0
6rKw7ZWY6rOgIENoYXR0ZXJpbmfCt+uwmOuzteybkOyduMK37IOB7YOc6riw67CYIFN1cHByZXNz
aW9u7J2EIOqygO2GoO2VmOyngCDslYrripTri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19u
b3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg
64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDr
ipQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzr
sJgg7IKw7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5
mSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX2FsYXJtX3BlcmZvcm1hbmNlX2twaSIs
CiAgICAgICJhbmNob3JfaWQiOiAic3cwM19hbGFybV9wZXJmb3JtYW5jZV9rcGkiLAogICAgICAi
c3RhdGVtZW50IjogIkFsYXJtIOyEseuKpeydgCDsi5zqsITri7kg67Cc7IOd66WgLCBQZWFrIGFs
YXJtIHJhdGUsIFN0YW5kaW5nIGFsYXJtLCBDaGF0dGVyaW5nIGFsYXJtLCBGbG9vZCDqtazqsIQs
IOyasOyEoOyInOychCDrtoTtj6zsmYAgU2hlbHZpbmcg7IKs7Jqp7J2EIO2YhOyepSDquLDspIDs
nLzroZwg7LaU7KCB7ZWY6rOgIOuwmOuztSDsm5DsnbjsnYQg6rCc7ISg7ZW07JW8IO2VnOuLpC4i
LAogICAgICAiaW1wb3J0YW5jZSI6ICJpbXBvcnRhbnQiLAogICAgICAia2V5d29yZHMiOiBbCiAg
ICAgICAgIkFsYXJtIEtQSSIsCiAgICAgICAgIkFsYXJtIHJhdGUiLAogICAgICAgICJTdGFuZGlu
ZyBhbGFybSIsCiAgICAgICAgIkNoYXR0ZXJpbmciLAogICAgICAgICJGbG9vZCIsCiAgICAgICAg
IlByaW9yaXR5IGRpc3RyaWJ1dGlvbiIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAg
ICAgICAgIkFsYXJtIEtQSSIsCiAgICAgICAgIlN0YW5kaW5nIGFsYXJtIiwKICAgICAgICAiRmxv
b2QiLAogICAgICAgICLsmrDshKDsiJzsnIQg67aE7Y+sIgogICAgICBdLAogICAgICAiYWNjZXB0
ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJBbGFybSDshLHriqXsnYAg7Iuc6rCE64u5IOuw
nOyDneuloCwgUGVhayBhbGFybSByYXRlLCBTdGFuZGluZyBhbGFybSwgQ2hhdHRlcmluZyBhbGFy
bSwgRmxvb2Qg6rWs6rCELCDsmrDshKDsiJzsnIQg67aE7Y+s7JmAIFNoZWx2aW5nIOyCrOyaqeyd
hCDtmITsnqUg6riw7KSA7Jy866GcIOy2lOygge2VmOqzoCDrsJjrs7Ug7JuQ7J247J2EIOqwnOyE
oO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAiQWxhcm0gS1BJLCBTdGFuZGluZyBhbGFybSwgRmxv
b2QsIOyasOyEoOyInOychCDrtoTtj6zsnZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzs
i5wsIOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6Qu
IgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLri6js
nbwg7Y+J6regIOuwnOyDneuloOunjOycvOuhnCBBbGFybSDshLHriqXsnbQg7Lap67aE7ZWY64uk
6rOgIOuztOqzoCBQZWFrwrdTdGFuZGluZ8K3Q2hhdHRlcmluZ8K3Rmxvb2Qg6rWs6rCE7J2EIOy2
lOygge2VmOyngCDslYrripTri6QuIgogICAgICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLs
p4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuI
hOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2Fybuyc
vOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeF
IEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOybkOy5mSIKICAgIH0s
CiAgICB7CiAgICAgICJpZCI6ICJzdzAzX3NldHBvaW50X3ZhbHVlX2NsYXNzZXMiLAogICAgICAi
YW5jaG9yX2lkIjogInN3MDNfc2V0cG9pbnRfdmFsdWVfY2xhc3NlcyIsCiAgICAgICJzdGF0ZW1l
bnQiOiAi7Jq07KCEIFNldHBvaW50LCBBbGFybSB2YWx1ZSwgVHJpcCB2YWx1ZeyZgCBJbnRlcmxv
Y2sgdmFsdWXripQg66qp7KCB6rO8IOyGjOycoOq2jOydtCDri6TrpbTrqbAsIEFsYXJt7J2AIOya
tOyghOyekCDsobDsuZjrpbwg7LSJ6rWs7ZWY6rOgIFRyaXDCt0ludGVybG9ja+ydgCDsnpDrj5kg
67O07Zi4IOuYkOuKlCDrj5nsnpHsoJzslb3sl5Ag7IKs7Jqp65CY66+A66GcIOqwmeydgCDqsJLs
nLzroZwg7J6E7J2YIO2Gte2Vqe2VmOyngCDslYrripTri6QuIiwKICAgICAgImltcG9ydGFuY2Ui
OiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiU2V0cG9pbnQiLAogICAgICAg
ICJBbGFybSB2YWx1ZSIsCiAgICAgICAgIlRyaXAgdmFsdWUiLAogICAgICAgICJJbnRlcmxvY2sg
dmFsdWUiLAogICAgICAgICLshozsnKDqtowiLAogICAgICAgICLrs7TtmLgiCiAgICAgIF0sCiAg
ICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJTZXRwb2ludCIsCiAgICAgICAgIkFsYXJtIHZh
bHVlIiwKICAgICAgICAiVHJpcCB2YWx1ZSIsCiAgICAgICAgIkludGVybG9jayB2YWx1ZSIKICAg
ICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7Jq07KCEIFNl
dHBvaW50LCBBbGFybSB2YWx1ZSwgVHJpcCB2YWx1ZeyZgCBJbnRlcmxvY2sgdmFsdWXripQg66qp
7KCB6rO8IOyGjOycoOq2jOydtCDri6TrpbTrqbAsIEFsYXJt7J2AIOyatOyghOyekCDsobDsuZjr
pbwg7LSJ6rWs7ZWY6rOgIFRyaXDCt0ludGVybG9ja+ydgCDsnpDrj5kg67O07Zi4IOuYkOuKlCDr
j5nsnpHsoJzslb3sl5Ag7IKs7Jqp65CY66+A66GcIOqwmeydgCDqsJLsnLzroZwg7J6E7J2YIO2G
te2Vqe2VmOyngCDslYrripTri6QuIiwKICAgICAgICAiU2V0cG9pbnQsIEFsYXJtIHZhbHVlLCBU
cmlwIHZhbHVlLCBJbnRlcmxvY2sgdmFsdWXsnZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDt
kZzsi5wsIOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzr
i6QuIgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICLs
mrTsoIQgU2V0cG9pbnQsIEFsYXJtLCBUcmlw6rO8IEludGVybG9jayDqsJLsnYQg6rCZ7J2AIOuq
qeyggeydmCDqsJLsnLzroZwg67O06rOgIOyEnOuhnCDsnoTsnZgg6rWQ7ZmY7ZWc64ukLiIKICAg
ICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXs
nYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOyc
hOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIsCiAgICAg
ICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuwjyBBbGFybcK37Jq0
7KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19z
ZXRwb2ludF9nb3Zlcm5hbmNlIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX3NldHBvaW50X2dv
dmVybmFuY2UiLAogICAgICAic3RhdGVtZW50IjogIlNldHBvaW50IGxpc3TripQgVGFnLCDquLDr
iqUsIOqwkiwg64uo7JyELCDrsKntlqUsIERlYWRiYW5kwrdEZWxheSwg7KCB7Jqp66qo65OcLCDq
t7zqsbAsIOyKueyduOyekCwg67OA6rK97J2066Cl6rO8IOq0gOugqCBUcmlwwrdJbnRlcmxvY2sg
7LC47KGw66W8IOq0gOumrO2VmOqzoCDsmKjrnbzsnbgg67OA6rK97J2AIOq2jO2VnMK36rKA7Yag
wrfquLDroZ3Ct+uzteq1rOygiOywqOulvCDqsbDss5Dslbwg7ZWc64ukLiIsCiAgICAgICJpbXBv
cnRhbmNlIjogIm11c3QiLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIlNldHBvaW50IGxp
c3QiLAogICAgICAgICJUYWciLAogICAgICAgICLri6jsnIQiLAogICAgICAgICLsoIHsmqnrqqjr
k5wiLAogICAgICAgICLsirnsnbgiLAogICAgICAgICLrs4Dqsr3snbTroKUiLAogICAgICAgICLr
s7XqtawiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJTZXRwb2ludCBs
aXN0IiwKICAgICAgICAi7Iq57J24IiwKICAgICAgICAi67OA6rK97J2066ClIiwKICAgICAgICAi
6re86rGwIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAg
ICJTZXRwb2ludCBsaXN064qUIFRhZywg6riw64qlLCDqsJIsIOuLqOychCwg67Cp7ZalLCBEZWFk
YmFuZMK3RGVsYXksIOyggeyaqeuqqOuTnCwg6re86rGwLCDsirnsnbjsnpAsIOuzgOqyveydtOug
peqzvCDqtIDroKggVHJpcMK3SW50ZXJsb2NrIOywuOyhsOulvCDqtIDrpqztlZjqs6Ag7Jio6528
7J24IOuzgOqyveydgCDqtoztlZzCt+qygO2GoMK36riw66Gdwrfrs7XqtazsoIjssKjrpbwg6rGw
7LOQ7JW8IO2VnOuLpC4iLAogICAgICAgICJTZXRwb2ludCBsaXN0LCDsirnsnbgsIOuzgOqyveyd
tOugpSwg6re86rGw7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITs
npAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwK
ICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi6re86rGwwrfqtoztlZzC
t+yKueyduMK367OA6rK97J2066Clwrfrs7XqtazsoIjssKgg7JeG7J20IOyYqOudvOyduCBTZXRw
b2ludOuCmCDrs7TtmLjqtIDroKgg6rCS7J2EIOuzgOqyve2VtOuPhCDrkJzri6Tqs6Ag67O464uk
LiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuMgCDs
o7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOyalOq1
rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64ukLiIs
CiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuwjyBBbGFy
bcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAiaWQiOiAi
c3cwM19hbGFybV90cmlwX2ludGVybG9ja19ib3VuZGFyeSIsCiAgICAgICJhbmNob3JfaWQiOiAi
c3cwM19hbGFybV90cmlwX2ludGVybG9ja19ib3VuZGFyeSIsCiAgICAgICJzdGF0ZW1lbnQiOiAi
QWxhcm3snYAg7Jq07KCE7J6QIO2MkOuLqOqzvCDsobDsuZjrpbwg7KeA7JuQ7ZWY64qUIOygleuz
tCDquLDriqXsnbTqs6AgVHJpcOydgCDrs7TtmLjsobDqsbTsl5Ag65Sw66W4IOyekOuPmSDsoJXs
p4AsIEludGVybG9ja+ydgCDsnITtl5jtlZjqsbDrgpgg7ZeI7Jqp65CY7KeAIOyViuydgCDrj5ns
npHsnYQg6riI7KeAwrfqsJXsoJztlZjripQg64W866as7J2066+A66GcIO2RnOyLnOygleuztOyZ
gCDsi6Ttlonrhbzrpqzrpbwg6rWs67aE7ZWc64ukLiIsCiAgICAgICJpbXBvcnRhbmNlIjogIm11
c3QiLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIkFsYXJtIiwKICAgICAgICAiVHJpcCIs
CiAgICAgICAgIkludGVybG9jayIsCiAgICAgICAgIuyatOyghOyekCDsobDsuZgiLAogICAgICAg
ICLsnpDrj5kg7KCV7KeAIiwKICAgICAgICAi6riI7KeAIOuFvOumrCIKICAgICAgXSwKICAgICAg
ImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkFsYXJtIiwKICAgICAgICAiVHJpcCIsCiAgICAgICAg
IkludGVybG9jayIsCiAgICAgICAgIuyLpO2WieuFvOumrCIKICAgICAgXSwKICAgICAgImFjY2Vw
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm3snYAg7Jq07KCE7J6QIO2MkOuLqOqz
vCDsobDsuZjrpbwg7KeA7JuQ7ZWY64qUIOygleuztCDquLDriqXsnbTqs6AgVHJpcOydgCDrs7Tt
mLjsobDqsbTsl5Ag65Sw66W4IOyekOuPmSDsoJXsp4AsIEludGVybG9ja+ydgCDsnITtl5jtlZjq
sbDrgpgg7ZeI7Jqp65CY7KeAIOyViuydgCDrj5nsnpHsnYQg6riI7KeAwrfqsJXsoJztlZjripQg
64W866as7J2066+A66GcIO2RnOyLnOygleuztOyZgCDsi6Ttlonrhbzrpqzrpbwg6rWs67aE7ZWc
64ukLiIsCiAgICAgICAgIkFsYXJtLCBUcmlwLCBJbnRlcmxvY2ssIOyLpO2WieuFvOumrOydmCDq
tIDqs4Trpbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg7Jq07KCE7J6QIOyhsOy5mOyZgCDquLDr
oZ0g6rSA7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9l
eHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkFsYXJt7J2EIOyekOuPmeygleyngMK364+Z7J6R7LCo
64uoIOuFvOumrOyZgCDrj5nsnbzsi5ztlZjqsbDrgpggVHJpcMK3SW50ZXJsb2Nr7J2EIOuLqOyI
nCDtkZzsi5zsoJXrs7TroZwg67O464ukLiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMi
OiAi7KeB7KCR7KCB7J24IOuwmOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyI
nCDriITrnb3snYAg66y47ZWtIOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdh
cm7snLzroZwg7Y+J6rCA7ZWc64ukLiIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyC
sOyXhSBITUnCt1NDQURBIOuwjyBBbGFybcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAg
ICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19zb2VfZGVmaW5pdGlvbiIsCiAgICAgICJhbmNo
b3JfaWQiOiAic3cwM19zb2VfZGVmaW5pdGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiU09F64qU
IOygkeygkMK37IOB7YOcwrfrqoXroLnCt+uztO2YuOuPmeyekSDrk7HsnZgg67OA7ZmUIOyLnOqw
gSwg7Iug7Zi47JuQLCDsnbTsoITqsJLCt+yDiOqwkuqzvCDtkojsp4jsnYQg6rO17Ya1IOyLnOqw
hOy2leyXkCDqs6DtlbTsg4Hrj4TroZwg6riw66Gd7ZWY7JesIOyCrOqxtOydmCDshKDtm4TqtIDq
s4TsmYAg7JuQ7J247KCE7YyM66W8IOu2hOyEne2VmOuKlCDquLDriqXsnbTri6QuIiwKICAgICAg
ImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiU09FIiwK
ICAgICAgICAiU2VxdWVuY2Ugb2YgRXZlbnRzIiwKICAgICAgICAiVGltZXN0YW1wIiwKICAgICAg
ICAiU3RhdGUgY2hhbmdlIiwKICAgICAgICAiU2lnbmFsIHNvdXJjZSIsCiAgICAgICAgIlF1YWxp
dHkiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJTT0UiLAogICAgICAg
ICJUaW1lc3RhbXAiLAogICAgICAgICLsg4Htg5zrs4DtmZQiLAogICAgICAgICLqs7XthrUg7Iuc
6rCE7LaVIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAg
ICJTT0XripQg7KCR7KCQwrfsg4Htg5zCt+uqheugucK367O07Zi464+Z7J6RIOuTseydmCDrs4Dt
mZQg7Iuc6rCBLCDsi6DtmLjsm5AsIOydtOyghOqwksK37IOI6rCS6rO8IO2SiOyniOydhCDqs7Xt
hrUg7Iuc6rCE7LaV7JeQIOqzoO2VtOyDgeuPhOuhnCDquLDroZ3tlZjsl6wg7IKs6rG07J2YIOyE
oO2bhOq0gOqzhOyZgCDsm5DsnbjsoITtjIzrpbwg67aE7ISd7ZWY64qUIOq4sOuKpeydtOuLpC4i
LAogICAgICAgICJTT0UsIFRpbWVzdGFtcCwg7IOB7YOc67OA7ZmULCDqs7XthrUg7Iuc6rCE7LaV
7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmA
IOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVj
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7IiY7KeRIOyEnOuyhCDrj4TssKnsi5zqsITr
p4wg6riw66Gd7ZW064+EIOybkCDsi6DtmLjsnZgg7KCV7ZmV7ZWcIOuwnOyDneyInOyEnOyZgCDt
kojsp4jsnYQg7ZWt7IOBIOyVjCDsiJgg7J6I64uk6rOgIOuzuOuLpC4iCiAgICAgIF0sCiAgICAg
ICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFsIO2b
hOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw6528
IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNlX2Jh
c2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuztCDq
tIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfdGltZV9zeW5jX3Jl
c29sdXRpb24iLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfdGltZV9zeW5jX3Jlc29sdXRpb24i
LAogICAgICAic3RhdGVtZW50IjogIlNPReydmCDsnbjqs7zsiJzshJzrpbwg7Iug66Kw7ZWY66Ck
66m0IFBMQ8K3RENTwrdTQ0FEQcK367O07Zi47J6l7LmY7J2YIOyLnOqzhOulvCDrj5nquLDtmZTt
lZjqs6AgU291cmNlIHRpbWVzdGFtcCwg7Iuc6rCE7KCV7ZmV64+ELCDrtoTtlbTriqUsIO2GteyL
oOyngOyXsOqzvCBUaW1lIHF1YWxpdHnrpbwg7ZWo6ruYIOq0gOumrO2VtOyVvCDtlZzri6QuIiwK
ICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAi
VGltZSBzeW5jaHJvbml6YXRpb24iLAogICAgICAgICJTb3VyY2UgdGltZXN0YW1wIiwKICAgICAg
ICAiUmVzb2x1dGlvbiIsCiAgICAgICAgIkFjY3VyYWN5IiwKICAgICAgICAiVGltZSBxdWFsaXR5
IiwKICAgICAgICAi7Ya17Iug7KeA7JewIgogICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsK
ICAgICAgICAi7Iuc6rCB64+Z6riwIiwKICAgICAgICAiU291cmNlIHRpbWVzdGFtcCIsCiAgICAg
ICAgIuu2hO2VtOuKpSIsCiAgICAgICAgIlRpbWUgcXVhbGl0eSIKICAgICAgXSwKICAgICAgImFj
Y2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiU09F7J2YIOyduOqzvOyInOyEnOulvCDs
i6DrorDtlZjroKTrqbQgUExDwrdEQ1PCt1NDQURBwrfrs7TtmLjsnqXsuZjsnZgg7Iuc6rOE66W8
IOuPmeq4sO2ZlO2VmOqzoCBTb3VyY2UgdGltZXN0YW1wLCDsi5zqsITsoJXtmZXrj4QsIOu2hO2V
tOuKpSwg7Ya17Iug7KeA7Jew6rO8IFRpbWUgcXVhbGl0eeulvCDtlajqu5gg6rSA66as7ZW07JW8
IO2VnOuLpC4iLAogICAgICAgICLsi5zqsIHrj5nquLAsIFNvdXJjZSB0aW1lc3RhbXAsIOu2hO2V
tOuKpSwgVGltZSBxdWFsaXR57J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDs
mrTsoITsnpAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAg
ICAgXSwKICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi7Iuc6rCB64+Z
6riwwrdUaW1lc3RhbXAgc291cmNlwrfsoJXtmZXrj4TCt+u2hO2VtOuKpcK3VGltZSBxdWFsaXR5
IOyXhuydtOuPhCBTT0Ug7J246rO87Iic7ISc6rCAIO2VreyDgSDsoJXtmZXtlZjri6Tqs6Ag67O4
64ukLiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuM
gCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOya
lOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64uk
LiIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuwjyBB
bGFybcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAiaWQi
OiAic3cwM19oaXN0b3JpYW5fdnNfc29lIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX2hpc3Rv
cmlhbl92c19zb2UiLAogICAgICAic3RhdGVtZW50IjogIkhpc3RvcmlhbuydgCDso7zquLAg65iQ
64qUIOuzgO2ZlOq4sOuwmOycvOuhnCDqs7XsoJXqsJIg7LaU7IS466W8IOyepeq4sCDsoIDsnqXt
lZjripQg6riw64ql7J20IOykkeyLrOydtOqzoCBTT0XripQg7J207IKwIOydtOuypO2KuOydmCDs
oJXtmZXtlZwg67Cc7IOd7Iic7ISc66W8IOu2hOyEne2VmOuKlCDquLDriqXsnbQg7KSR7Ius7J20
66+A66GcIO2RnOuzuOyjvOq4sOyZgCBUaW1lc3RhbXAg7Lac7LKY66W8IOq1rOu2hO2VnOuLpC4i
LAogICAgICAiaW1wb3J0YW5jZSI6ICJpbXBvcnRhbnQiLAogICAgICAia2V5d29yZHMiOiBbCiAg
ICAgICAgIkhpc3RvcmlhbiIsCiAgICAgICAgIlNPRSIsCiAgICAgICAgIlNhbXBsaW5nIiwKICAg
ICAgICAiRXZlbnQgb3JkZXIiLAogICAgICAgICJUaW1lc3RhbXAgc291cmNlIiwKICAgICAgICAi
VHJlbmQiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rlcm1zIjogWwogICAgICAgICJIaXN0b3JpYW4i
LAogICAgICAgICJTT0UiLAogICAgICAgICLtkZzrs7jso7zquLAiLAogICAgICAgICLrsJzsg53s
iJzshJwiCiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAg
Ikhpc3RvcmlhbuydgCDso7zquLAg65iQ64qUIOuzgO2ZlOq4sOuwmOycvOuhnCDqs7XsoJXqsJIg
7LaU7IS466W8IOyepeq4sCDsoIDsnqXtlZjripQg6riw64ql7J20IOykkeyLrOydtOqzoCBTT0Xr
ipQg7J207IKwIOydtOuypO2KuOydmCDsoJXtmZXtlZwg67Cc7IOd7Iic7ISc66W8IOu2hOyEne2V
mOuKlCDquLDriqXsnbQg7KSR7Ius7J2066+A66GcIO2RnOuzuOyjvOq4sOyZgCBUaW1lc3RhbXAg
7Lac7LKY66W8IOq1rOu2hO2VnOuLpC4iLAogICAgICAgICJIaXN0b3JpYW4sIFNPRSwg7ZGc67O4
7KO86riwLCDrsJzsg53siJzshJzsnZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzsi5ws
IOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6QuIgog
ICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJIaXN0b3Jp
YW4g7ZGc67O46rCS66eM7Jy866GcIOydtOyCsCDsgqzqsbTsnZggU09FIOyInOyEnOulvCDtla3s
g4Eg64+Z7J287ZWY6rKMIOyerO2YhO2VoCDsiJgg7J6I64uk6rOgIOuzuOuLpC4iCiAgICAgIF0s
CiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZh
dGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag
65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291
cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOyg
leuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfZmlyc3Rf
b3V0X3JlbGF0aW9uIiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX2ZpcnN0X291dF9yZWxhdGlv
biIsCiAgICAgICJzdGF0ZW1lbnQiOiAiRmlyc3Qtb3V07J2AIO2VnCDsl7Dsh4TsgqzqsbTsl5Ds
hJwg7LWc7LSI66GcIOycoO2aqO2VtOynhCDsm5DsnbjsnYQgTGF0Y2jtlZjsl6wg67O07KG07ZWY
64qUIOuFvOumrOydtOqzoCBTT0XripQg7KCE7LK0IOydtOuypO2KuCDsiJzshJzrpbwg6riw66Gd
7ZWY66+A66GcLCBGaXJzdC1vdXTsnYAg67mg66W4IOybkOyduOyngOyLnOulvCDsoJzqs7XtlZjq
s6AgU09F64qUIOyDgeyEuCDqsoDspp3snYQg67O07JmE7ZWc64ukLiIsCiAgICAgICJpbXBvcnRh
bmNlIjogImltcG9ydGFudCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiRmlyc3Qtb3V0
IiwKICAgICAgICAiU09FIiwKICAgICAgICAi7LWc7LSIIOybkOyduCIsCiAgICAgICAgIkxhdGNo
IiwKICAgICAgICAi7J2067Kk7Yq4IOyInOyEnCIsCiAgICAgICAgIuybkOyduOu2hOyEnSIKICAg
ICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIkZpcnN0LW91dCIsCiAgICAgICAg
IlNPRSIsCiAgICAgICAgIuy1nOy0iCDsm5DsnbgiLAogICAgICAgICLsm5DsnbjrtoTshJ0iCiAg
ICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkZpcnN0LW91
dOydgCDtlZwg7Jew7IeE7IKs6rG07JeQ7IScIOy1nOy0iOuhnCDsnKDtmqjtlbTsp4Qg7JuQ7J24
7J2EIExhdGNo7ZWY7JesIOuztOyhtO2VmOuKlCDrhbzrpqzsnbTqs6AgU09F64qUIOyghOyytCDs
nbTrsqTtirgg7Iic7ISc66W8IOq4sOuhne2VmOuvgOuhnCwgRmlyc3Qtb3V07J2AIOu5oOuluCDs
m5Dsnbjsp4Dsi5zrpbwg7KCc6rO17ZWY6rOgIFNPReuKlCDsg4HshLgg6rKA7Kad7J2EIOuztOyZ
hO2VnOuLpC4iLAogICAgICAgICJGaXJzdC1vdXQsIFNPRSwg7LWc7LSIIOybkOyduCwg7JuQ7J24
67aE7ISd7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw
7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAg
InJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiRmlyc3Qtb3V07J2EIOyghOyytCDs
nbTrsqTtirgg7J2066Cl7J2064KYIOuniOyngOuniSDsnpTrpZjsi6DtmLjsmYAg64+Z7J287Iuc
7ZWY6rOgIFNPReyZgCDqsJnsnYAg6riw64ql7J2065286rOgIOuzuOuLpC4iCiAgICAgIF0sCiAg
ICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO87J6l7J2AIGZhdGFs
IO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazrspTsnITsl5Ag65Sw
6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAogICAgICAic291cmNl
X2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3Ct+yatOyghOygleuz
tCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfYXVkaXRfdHJh
aWwiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfYXVkaXRfdHJhaWwiLAogICAgICAic3RhdGVt
ZW50IjogIkF1ZGl0IHRyYWls7J2AIOyCrOyaqeyekOqwgCDsiJjtlontlZwgQWNrbm93bGVkZ2Us
IFNoZWx2aW5nLCBTdXBwcmVzc2lvbiDsirnsnbgsIFNldHBvaW50IOuzgOqyvSwgTG9naW7Ct0xv
Z291dOqzvCDtmZTrqbQg66qF66C57JeQIOuMgO2VtCDsgqzsmqnsnpAsIOyLnOqwgSwg64yA7IOB
LCDsnbTsoITqsJLCt+yDiOqwkiwg7IKs7Jyg7JmAIOqysOqzvOulvCDquLDroZ3tlZzri6QuIiwK
ICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAi
QXVkaXQgdHJhaWwiLAogICAgICAgICJVc2VyIiwKICAgICAgICAiU2V0cG9pbnQgY2hhbmdlIiwK
ICAgICAgICAiQWNrbm93bGVkZ2UiLAogICAgICAgICJTaGVsdmluZyIsCiAgICAgICAgIk9sZCB2
YWx1ZSIsCiAgICAgICAgIk5ldyB2YWx1ZSIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBb
CiAgICAgICAgIkF1ZGl0IHRyYWlsIiwKICAgICAgICAi7IKs7Jqp7J6QIiwKICAgICAgICAi67OA
6rK96riw66GdIiwKICAgICAgICAi7IKs7JygIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhw
bGFuYXRpb25zIjogWwogICAgICAgICJBdWRpdCB0cmFpbOydgCDsgqzsmqnsnpDqsIAg7IiY7ZaJ
7ZWcIEFja25vd2xlZGdlLCBTaGVsdmluZywgU3VwcHJlc3Npb24g7Iq57J24LCBTZXRwb2ludCDr
s4Dqsr0sIExvZ2luwrdMb2dvdXTqs7wg7ZmU66m0IOuqheugueyXkCDrjIDtlbQg7IKs7Jqp7J6Q
LCDsi5zqsIEsIOuMgOyDgSwg7J207KCE6rCSwrfsg4jqsJIsIOyCrOycoOyZgCDqsrDqs7zrpbwg
6riw66Gd7ZWc64ukLiIsCiAgICAgICAgIkF1ZGl0IHRyYWlsLCDsgqzsmqnsnpAsIOuzgOqyveq4
sOuhnSwg7IKs7Jyg7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITs
npAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwK
ICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQXVkaXQgdHJhaWzsnYQg
6rO17KCVIOydtOuypO2KuCDsiJzshJwg6riw66Gd7Jy866Gc66eMIOuztOqxsOuCmCDsgqzsmqns
npDCt+uMgOyDgcK37J207KCE6rCSwrfsg4jqsJLCt+yCrOycoOulvCDquLDroZ3tlZjsp4Ag7JWK
64qU64ukLiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuw
mOuMgCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWt
IOyalOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc
64ukLiIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuw
jyBBbGFybcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAi
aWQiOiAic3cwM19vcGVyYXRvcl9hdXRob3JpdHkiLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNf
b3BlcmF0b3JfYXV0aG9yaXR5IiwKICAgICAgInN0YXRlbWVudCI6ICLsmrTsoITsnpAg6raM7ZWc
7J2AIOyXre2VoOq4sOuwmCDstZzshozqtoztlZwsIOyEpOu5hMK36riw64qlwrfsmrTsoITrqqjr
k5zrs4Qg67KU7JyELCDspJHsmpTsobDsnpHsnZgg7J6s7ZmV7J24IOuYkOuKlCDsnbTspJHsirns
nbgsIOyEuOyFmOq0gOumrOyZgCBBdWRpdCB0cmFpbOydhCDthrXtlbQg7Ya17KCc7ZWc64ukLiIs
CiAgICAgICJpbXBvcnRhbmNlIjogIm11c3QiLAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAg
Ik9wZXJhdG9yIGF1dGhvcml0eSIsCiAgICAgICAgIlJvbGUgYmFzZWQgYWNjZXNzIiwKICAgICAg
ICAiTGVhc3QgcHJpdmlsZWdlIiwKICAgICAgICAi7J207KSR7Iq57J24IiwKICAgICAgICAi7IS4
7IWY6rSA66asIiwKICAgICAgICAiQXVkaXQgdHJhaWwiCiAgICAgIF0sCiAgICAgICJjb3JlX3Rl
cm1zIjogWwogICAgICAgICLsmrTsoITsnpAg6raM7ZWcIiwKICAgICAgICAi7Jet7ZWg6riw67CY
IiwKICAgICAgICAi7LWc7IaM6raM7ZWcIiwKICAgICAgICAiQXVkaXQgdHJhaWwiCiAgICAgIF0s
CiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIuyatOyghOyekCDqtozt
lZzsnYAg7Jet7ZWg6riw67CYIOy1nOyGjOq2jO2VnCwg7ISk67mEwrfquLDriqXCt+yatOyghOuq
qOuTnOuzhCDrspTsnIQsIOykkeyalOyhsOyekeydmCDsnqztmZXsnbgg65iQ64qUIOydtOykkeyK
ueyduCwg7IS47IWY6rSA66as7JmAIEF1ZGl0IHRyYWls7J2EIO2Gte2VtCDthrXsoJztlZzri6Qu
IiwKICAgICAgICAi7Jq07KCE7J6QIOq2jO2VnCwg7Jet7ZWg6riw67CYLCDstZzshozqtoztlZws
IEF1ZGl0IHRyYWls7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITs
npAg7KGw7LmY7JmAIOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwK
ICAgICAgInJlamVjdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAi66qo65OgIOyCrOyaqeye
kOyXkOqyjCDrs7TtmLjqtIDroKgg6rCS6rO8IOykkeyalOyhsOyekSDqtoztlZzsnYQg7KCc7ZWc
IOyXhuydtCDrtoDsl6ztlZjripQg6rKD7J20IOyViOyghO2VmOuLpOqzoCDrs7jri6QuIgogICAg
ICBdLAogICAgICAiZ3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeyd
gCBmYXRhbCDtm4Trs7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE
7JeQIOuUsOudvCBtYWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAg
InNvdXJjZV9iYXNpcyI6ICLsnbzrsJgg7IKw7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTs
oITsoJXrs7Qg6rSA66asIOybkOy5mSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX2h1
bWFuX2Vycm9yX3ByZXZlbnRpb24iLAogICAgICAiYW5jaG9yX2lkIjogInN3MDNfaHVtYW5fZXJy
b3JfcHJldmVudGlvbiIsCiAgICAgICJzdGF0ZW1lbnQiOiAiSHVtYW4gZXJyb3Ig67Cp7KeA64qU
IO2YhOyerCBNb2RlwrfshozsnKDqtozCt0ludGVybG9jayDsgqzsnKDCt+uqheugueuMgOyDgcK3
7JiI7IOB6rKw6rO866W8IOuqhe2Zle2eiCDtkZzsi5ztlZjqs6AsIOykkeyalOyhsOyekSDtmZXs
nbgsIOyemOuqu+uQnCDrjIDsg4Eg7ISg7YOdIOuwqeyngCwgQ29tbWFuZOyZgCBGZWVkYmFjayDr
toTrpqwsIOy3qOyGjMK367O16rWsIOqyveuhnOulvCDsoJzqs7XtlZjripQg67Cp7Iud7Jy866Gc
IOq1rO2YhO2VnOuLpC4iLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdv
cmRzIjogWwogICAgICAgICJIdW1hbiBlcnJvciIsCiAgICAgICAgIk1vZGUiLAogICAgICAgICJJ
bnRlcmxvY2sgcmVhc29uIiwKICAgICAgICAiQ29uZmlybWF0aW9uIiwKICAgICAgICAiQ29tbWFu
ZCBmZWVkYmFjayIsCiAgICAgICAgIlJlY292ZXJ5IgogICAgICBdLAogICAgICAiY29yZV90ZXJt
cyI6IFsKICAgICAgICAiSHVtYW4gZXJyb3IiLAogICAgICAgICJNb2RlIiwKICAgICAgICAiQ29t
bWFuZCIsCiAgICAgICAgIkZlZWRiYWNrIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFu
YXRpb25zIjogWwogICAgICAgICJIdW1hbiBlcnJvciDrsKnsp4DripQg7ZiE7J6sIE1vZGXCt+yG
jOycoOq2jMK3SW50ZXJsb2NrIOyCrOycoMK366qF66C564yA7IOBwrfsmIjsg4HqsrDqs7zrpbwg
66qF7ZmV7Z6IIO2RnOyLnO2VmOqzoCwg7KSR7JqU7KGw7J6RIO2ZleyduCwg7J6Y66q765CcIOuM
gOyDgSDshKDtg50g67Cp7KeALCBDb21tYW5k7JmAIEZlZWRiYWNrIOu2hOumrCwg7Leo7IaMwrfr
s7Xqtawg6rK966Gc66W8IOygnOqzte2VmOuKlCDrsKnsi53snLzroZwg6rWs7ZiE7ZWc64ukLiIs
CiAgICAgICAgIkh1bWFuIGVycm9yLCBNb2RlLCBDb21tYW5kLCBGZWVkYmFja+ydmCDqtIDqs4Tr
pbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg7Jq07KCE7J6QIOyhsOy5mOyZgCDquLDroZ0g6rSA
7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5h
dGlvbnMiOiBbCiAgICAgICAgIkNvbW1hbmQg7KCE7Iah7J2EIOyEpOu5hCDrj5nsnpHsmYTro4zr
oZwg7ZGc7Iuc7ZWY6rGw64KYIE1vZGXCt+uMgOyDgcK3RmVlZGJhY2vCt+y3qOyGjMK367O16rWs
6rK966Gc66W8IOq1rOu2hO2VmOyngCDslYrripTri6QuIgogICAgICBdLAogICAgICAiZ3JhZGlu
Z19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Trs7TsnbTr
qbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBtYWpvciDr
mJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNpcyI6ICLs
nbzrsJgg7IKw7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA66asIOyb
kOy5mSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX2RhdGFfcXVhbGl0eV9kaXNwbGF5
IiwKICAgICAgImFuY2hvcl9pZCI6ICJzdzAzX2RhdGFfcXVhbGl0eV9kaXNwbGF5IiwKICAgICAg
InN0YXRlbWVudCI6ICJCYWQsIFVuY2VydGFpbiwgU3RhbGUsIENvbW11bmljYXRpb24gbG9zdOyZ
gCBNYW51YWwgc3Vic3RpdHV0aW9uIOqwmeydgCDrjbDsnbTthLAg7ZKI7KeI7J2AIOqwkiDsnpDs
srTsmYAg67OE64+EIOyDge2DnOuhnCDtkZzsi5ztlZjqs6AsIO2SiOyniOydtCDrgpjsgZwg6rCS
7J2EIOygleyDgSDstZzsi6DqsJLsspjrn7wg7KCc7Ja07YyQ64uo7J2064KYIOyatOyghOyekCDt
jJDri6jsl5Ag7IKs7Jqp7ZWY7KeAIOyViuuPhOuhnSDtlZzri6QuIiwKICAgICAgImltcG9ydGFu
Y2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsKICAgICAgICAiRGF0YSBxdWFsaXR5IiwK
ICAgICAgICAiQmFkIiwKICAgICAgICAiVW5jZXJ0YWluIiwKICAgICAgICAiU3RhbGUiLAogICAg
ICAgICJDb21tdW5pY2F0aW9uIGxvc3QiLAogICAgICAgICJNYW51YWwgc3Vic3RpdHV0aW9uIgog
ICAgICBdLAogICAgICAiY29yZV90ZXJtcyI6IFsKICAgICAgICAiRGF0YSBxdWFsaXR5IiwKICAg
ICAgICAiQmFkIiwKICAgICAgICAiU3RhbGUiLAogICAgICAgICJDb21tdW5pY2F0aW9uIGxvc3Qi
CiAgICAgIF0sCiAgICAgICJhY2NlcHRlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkJhZCwg
VW5jZXJ0YWluLCBTdGFsZSwgQ29tbXVuaWNhdGlvbiBsb3N07JmAIE1hbnVhbCBzdWJzdGl0dXRp
b24g6rCZ7J2AIOuNsOydtO2EsCDtkojsp4jsnYAg6rCSIOyekOyytOyZgCDrs4Trj4Qg7IOB7YOc
66GcIO2RnOyLnO2VmOqzoCwg7ZKI7KeI7J20IOuCmOyBnCDqsJLsnYQg7KCV7IOBIOy1nOyLoOqw
kuyymOufvCDsoJzslrTtjJDri6jsnbTrgpgg7Jq07KCE7J6QIO2MkOuLqOyXkCDsgqzsmqntlZjs
p4Ag7JWK64+E66GdIO2VnOuLpC4iLAogICAgICAgICJEYXRhIHF1YWxpdHksIEJhZCwgU3RhbGUs
IENvbW11bmljYXRpb24gbG9zdOydmCDqtIDqs4Trpbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg
7Jq07KCE7J6QIOyhsOy5mOyZgCDquLDroZ0g6rSA7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAg
ICAgIF0sCiAgICAgICJyZWplY3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkJhZMK3VW5j
ZXJ0YWluwrdTdGFsZcK3Q29tbXVuaWNhdGlvbiBsb3N0IOqwkuydhCDstZzsi6Ag7KCV7IOB6rCS
7LKY65+8IO2RnOyLnO2VmOqzoCDsmrTsoITsnpDCt+ygnOyWtCDtjJDri6jsl5Ag7IKs7Jqp7ZWc
64ukLiIKICAgICAgXSwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi7KeB7KCR7KCB7J24IOuwmOuM
gCDso7zsnqXsnYAgZmF0YWwg7ZuE67O07J2066mwIOuLqOyInCDriITrnb3snYAg66y47ZWtIOya
lOq1rOuylOychOyXkCDrlLDrnbwgbWFqb3Ig65iQ64qUIHdhcm7snLzroZwg7Y+J6rCA7ZWc64uk
LiIsCiAgICAgICJzb3VyY2VfYmFzaXMiOiAi7J2867CYIOyCsOyXhSBITUnCt1NDQURBIOuwjyBB
bGFybcK37Jq07KCE7KCV67O0IOq0gOumrCDsm5DsuZkiCiAgICB9LAogICAgewogICAgICAiaWQi
OiAic3cwM19hYm5vcm1hbF9zaXR1YXRpb25fbWFuYWdlbWVudCIsCiAgICAgICJhbmNob3JfaWQi
OiAic3cwM19hYm5vcm1hbF9zaXR1YXRpb25fbWFuYWdlbWVudCIsCiAgICAgICJzdGF0ZW1lbnQi
OiAiQWJub3JtYWwgc2l0dWF0aW9uIG1hbmFnZW1lbnTripQgT3ZlcnZpZXfsl5DshJwg7J207IOB
IOynle2bhOulvCDsobDquLDsl5Ag67Cc6rKs7ZWY6rOgIEFsYXJt6rO8IFRyZW5k66GcIOynhOuL
qO2VmOupsCDsoIjssKjsmYAg6raM7ZWc7JeQIOuUsOudvCDrjIDsnZHtlZwg65KkIOygleyDgeuz
teq1rOyZgCDsgqztm4TrtoTshJ3snLzroZwg7J207Ja07KeA64qUIERldGVjdC1EaWFnbm9zZS1S
ZXNwb25kLVJlY292ZXIg7Z2Q66aE7J2064ukLiIsCiAgICAgICJpbXBvcnRhbmNlIjogIm11c3Qi
LAogICAgICAia2V5d29yZHMiOiBbCiAgICAgICAgIkFibm9ybWFsIHNpdHVhdGlvbiBtYW5hZ2Vt
ZW50IiwKICAgICAgICAiRGV0ZWN0IiwKICAgICAgICAiRGlhZ25vc2UiLAogICAgICAgICJSZXNw
b25kIiwKICAgICAgICAiUmVjb3ZlciIsCiAgICAgICAgIlRyZW5kIgogICAgICBdLAogICAgICAi
Y29yZV90ZXJtcyI6IFsKICAgICAgICAi67mE7KCV7IOB7IOB7ZmpIiwKICAgICAgICAiRGV0ZWN0
IiwKICAgICAgICAiRGlhZ25vc2UiLAogICAgICAgICJSZWNvdmVyIgogICAgICBdLAogICAgICAi
YWNjZXB0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJBYm5vcm1hbCBzaXR1YXRpb24gbWFu
YWdlbWVudOuKlCBPdmVydmlld+yXkOyEnCDsnbTsg4Eg7KeV7ZuE66W8IOyhsOq4sOyXkCDrsJzq
sqztlZjqs6AgQWxhcm3qs7wgVHJlbmTroZwg7KeE64uo7ZWY66mwIOygiOywqOyZgCDqtoztlZzs
l5Ag65Sw6528IOuMgOydke2VnCDrkqQg7KCV7IOB67O16rWs7JmAIOyCrO2bhOu2hOyEneycvOuh
nCDsnbTslrTsp4DripQgRGV0ZWN0LURpYWdub3NlLVJlc3BvbmQtUmVjb3ZlciDtnZDrpoTsnbTr
i6QuIiwKICAgICAgICAi67mE7KCV7IOB7IOB7ZmpLCBEZXRlY3QsIERpYWdub3NlLCBSZWNvdmVy
7J2YIOq0gOqzhOulvCDrqqnsoIEsIOyhsOqxtCwg7ZGc7IucLCDsmrTsoITsnpAg7KGw7LmY7JmA
IOq4sOuhnSDqtIDsoJDsl5DshJwg7ISk66qF7ZWc64ukLiIKICAgICAgXSwKICAgICAgInJlamVj
dGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiQWxhcm0g7ZGc7Iuc66eM7Jy866GcIOu5hOyg
leyDgeyDge2ZqSDrjIDsnZHsnbQg64Gd64Kc64uk6rOgIOuztOqzoCDsp4Tri6jCt+ygiOywqMK3
6raM7ZWcwrfrs7XqtazCt+yCrO2bhOu2hOyEnSDtnZDrpoTsnYQg65GQ7KeAIOyViuuKlOuLpC4i
CiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg7KO8
7J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTqtazr
spTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4iLAog
ICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxhcm3C
t+yatOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3
MDNfc3cwMl9ib3VuZGFyeSIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwM19zdzAyX2JvdW5kYXJ5
IiwKICAgICAgInN0YXRlbWVudCI6ICJTVy0wM+uKlCBBbGFybcK3U2V0cG9pbnTCt1NPRcK37ZmU
66m0wrfqtoztlZwg65OxIOyatOyghOyekCDsoJXrs7TsmYAg6rSA66as7KCV7LGF7J2EIOyGjOyc
oO2VmOqzoCwgSW50ZXJsb2NrwrdUcmlw7J2YIOyLpOygnCDrhbzrpqzqtazsobAsIOyDge2DnOyg
hOydtCwgTGF0Y2jCt1Jlc2V0IOuwjyBGYWlsLXNhZmUg64+Z7J6R7J2AIFNXLTAy66GcIOuEmOq4
tOuLpC4iLAogICAgICAiaW1wb3J0YW5jZSI6ICJtdXN0IiwKICAgICAgImtleXdvcmRzIjogWwog
ICAgICAgICJTVy0wMyIsCiAgICAgICAgIlNXLTAyIiwKICAgICAgICAiQWxhcm0g7KCV67O0IiwK
ICAgICAgICAiU2V0cG9pbnQiLAogICAgICAgICJTT0UiLAogICAgICAgICLsg4Htg5zsoITsnbQi
LAogICAgICAgICJMYXRjaCBSZXNldCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAg
ICAgICAgIlNXLTAzIiwKICAgICAgICAiU1ctMDIiLAogICAgICAgICLsmrTsoITsnpAg7KCV67O0
IiwKICAgICAgICAi7Iuk7ZaJ64W866asIgogICAgICBdLAogICAgICAiYWNjZXB0ZWRfZXhwbGFu
YXRpb25zIjogWwogICAgICAgICJTVy0wM+uKlCBBbGFybcK3U2V0cG9pbnTCt1NPRcK37ZmU66m0
wrfqtoztlZwg65OxIOyatOyghOyekCDsoJXrs7TsmYAg6rSA66as7KCV7LGF7J2EIOyGjOycoO2V
mOqzoCwgSW50ZXJsb2NrwrdUcmlw7J2YIOyLpOygnCDrhbzrpqzqtazsobAsIOyDge2DnOyghOyd
tCwgTGF0Y2jCt1Jlc2V0IOuwjyBGYWlsLXNhZmUg64+Z7J6R7J2AIFNXLTAy66GcIOuEmOq4tOuL
pC4iLAogICAgICAgICJTVy0wMywgU1ctMDIsIOyatOyghOyekCDsoJXrs7QsIOyLpO2WieuFvOum
rOydmCDqtIDqs4Trpbwg66qp7KCBLCDsobDqsbQsIO2RnOyLnCwg7Jq07KCE7J6QIOyhsOy5mOyZ
gCDquLDroZ0g6rSA7KCQ7JeQ7IScIOyEpOuqhe2VnOuLpC4iCiAgICAgIF0sCiAgICAgICJyZWpl
Y3RlZF9leHBsYW5hdGlvbnMiOiBbCiAgICAgICAgIkludGVybG9ja8K3VHJpcOydmCDsi6TsoJwg
7IOB7YOc7KCE7J207JmAIExhdGNowrdSZXNldMK3RmFpbC1zYWZl66W8IFNXLTAz7J2YIO2ZlOup
tMK37Jq07JiB7KCV7LGFIOuylOychOuhnCDtnaHsiJjtlZzri6QuIgogICAgICBdLAogICAgICAi
Z3JhZGluZ19ub3RlcyI6ICLsp4HsoJHsoIHsnbgg67CY64yAIOyjvOyepeydgCBmYXRhbCDtm4Tr
s7TsnbTrqbAg64uo7IicIOuIhOudveydgCDrrLjtla0g7JqU6rWs67KU7JyE7JeQIOuUsOudvCBt
YWpvciDrmJDripQgd2FybuycvOuhnCDtj4nqsIDtlZzri6QuIiwKICAgICAgInNvdXJjZV9iYXNp
cyI6ICLsnbzrsJgg7IKw7JeFIEhNScK3U0NBREEg67CPIEFsYXJtwrfsmrTsoITsoJXrs7Qg6rSA
66asIOybkOy5mSIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJzdzAzX3N3MDRfc3cxMF9ib3Vu
ZGFyeSIsCiAgICAgICJhbmNob3JfaWQiOiAic3cwM19zdzA0X3N3MTBfYm91bmRhcnkiLAogICAg
ICAic3RhdGVtZW50IjogIlNXLTAz64qUIOyatOyghOygleuztOydmCDrgrTsmqnqs7wg7Jq07JiB
6rSA66asIOybkOy5meydhCDshozsnKDtlZjqs6AsIOydvOuwmCDshoztlITtirjsm6jslrQgVi1N
b2RlbMK37LaU7KCB7ISxwrfsi5ztl5jssrTqs4TripQgU1ctMDQsIO2UhOuhnOygne2KuCDrrLjs
hJwg7J2464+EwrdGQVTCt1NBVMK37Iuc7Jq07KCEIOygiOywqOuKlCBTVy0xMOycvOuhnCDrhJjq
uLTri6QuIiwKICAgICAgImltcG9ydGFuY2UiOiAibXVzdCIsCiAgICAgICJrZXl3b3JkcyI6IFsK
ICAgICAgICAiU1ctMDMiLAogICAgICAgICJTVy0wNCIsCiAgICAgICAgIlNXLTEwIiwKICAgICAg
ICAiVi1Nb2RlbCIsCiAgICAgICAgIkZBVCIsCiAgICAgICAgIlNBVCIsCiAgICAgICAgIuyatOyg
hOygleuztCIKICAgICAgXSwKICAgICAgImNvcmVfdGVybXMiOiBbCiAgICAgICAgIlNXLTAzIiwK
ICAgICAgICAiU1ctMDQiLAogICAgICAgICJTVy0xMCIsCiAgICAgICAgIm93bmVyc2hpcCIKICAg
ICAgXSwKICAgICAgImFjY2VwdGVkX2V4cGxhbmF0aW9ucyI6IFsKICAgICAgICAiU1ctMDPripQg
7Jq07KCE7KCV67O07J2YIOuCtOyaqeqzvCDsmrTsmIHqtIDrpqwg7JuQ7LmZ7J2EIOyGjOycoO2V
mOqzoCwg7J2867CYIOyGjO2UhO2KuOybqOyWtCBWLU1vZGVswrfstpTsoIHshLHCt+yLnO2XmOyy
tOqzhOuKlCBTVy0wNCwg7ZSE66Gc7KCd7Yq4IOusuOyEnCDsnbjrj4TCt0ZBVMK3U0FUwrfsi5zs
mrTsoIQg7KCI7LCo64qUIFNXLTEw7Jy866GcIOuEmOq4tOuLpC4iLAogICAgICAgICJTVy0wMywg
U1ctMDQsIFNXLTEwLCBvd25lcnNoaXDsnZgg6rSA6rOE66W8IOuqqeyggSwg7KGw6rG0LCDtkZzs
i5wsIOyatOyghOyekCDsobDsuZjsmYAg6riw66GdIOq0gOygkOyXkOyEnCDshKTrqoXtlZzri6Qu
IgogICAgICBdLAogICAgICAicmVqZWN0ZWRfZXhwbGFuYXRpb25zIjogWwogICAgICAgICJWLU1v
ZGVswrfsnbzrsJggViZWIOuYkOuKlCBGQVTCt1NBVMK37Iuc7Jq07KCEwrfsnbjsiJjrpbwgU1ct
MDPsnZgg7Jq07KCE7KCV67O0IOybkOumrOyZgCDqsJnsnYAg7IaM7Jyg67KU7JyE66GcIOuzuOuL
pC4iCiAgICAgIF0sCiAgICAgICJncmFkaW5nX25vdGVzIjogIuyngeygkeyggeyduCDrsJjrjIAg
7KO87J6l7J2AIGZhdGFsIO2bhOuztOydtOupsCDri6jsiJwg64iE65297J2AIOusuO2VrSDsmpTq
tazrspTsnITsl5Ag65Sw6528IG1ham9yIOuYkOuKlCB3YXJu7Jy866GcIO2PieqwgO2VnOuLpC4i
LAogICAgICAic291cmNlX2Jhc2lzIjogIuydvOuwmCDsgrDsl4UgSE1JwrdTQ0FEQSDrsI8gQWxh
cm3Ct+yatOyghOygleuztCDqtIDrpqwg7JuQ7LmZIgogICAgfQogIF0sCiAgImZhdGFsX3dyb25n
X2NsYWltcyI6IFsKICAgIHsKICAgICAgImlkIjogInN3MDNfZmF0YWxfYWxsX2V2ZW50c19hcmVf
YWxhcm1zIiwKICAgICAgImNsYWltIjogIuuqqOuToCBFdmVudOyZgCBTdGF0dXPripQgQWxhcm3s
nLzroZwg66eM65Ok7Ja07JW8IO2VnOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAi66qo65Og
IEV2ZW507JmAIFN0YXR1c+uKlCBBbGFybeycvOuhnCDrp4zrk6TslrTslbwg7ZWc64ukLiIsCiAg
ICAgICJjb3JyZWN0aW9uIjogIkFsYXJt7J2AIOygle2VtOynhCDsi5zqsIQg7JWI7JeQIOyatOyg
hOyekCDsobDsuZjqsIAg7ZWE7JqU7ZWcIOu5hOygleyDgSDsg4Htg5zrp4wg64yA7IOB7Jy866Gc
IO2VmOupsCDri6jsiJwgRXZlbnTCt1N0YXR1c+yZgCDqtazrtoTtlZzri6QuIiwKICAgICAgImNv
cnJlY3RfcnVsZSI6ICJBbGFybeydgCDsoJXtlbTsp4Qg7Iuc6rCEIOyViOyXkCDsmrTsoITsnpAg
7KGw7LmY6rCAIO2VhOyalO2VnCDruYTsoJXsg4Eg7IOB7YOc66eMIOuMgOyDgeycvOuhnCDtlZjr
qbAg64uo7IicIEV2ZW50wrdTdGF0dXPsmYAg6rWs67aE7ZWc64ukLiIsCiAgICAgICJzZXZlcml0
eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAogICAg
ICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6ICLrqqjrk6AgRXZlbnTsmYAgU3RhdHVz
64qUIEFsYXJt7Jy866GcIOunjOuTpOyWtOyVvCDtlZzri6QuIiwKICAgICAgImRlc2NyaXB0aW9u
IjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIEFs
YXJt7J2AIOygle2VtOynhCDsi5zqsIQg7JWI7JeQIOyatOyghOyekCDsobDsuZjqsIAg7ZWE7JqU
7ZWcIOu5hOygleyDgSDsg4Htg5zrp4wg64yA7IOB7Jy866GcIO2VmOupsCDri6jsiJwgRXZlbnTC
t1N0YXR1c+yZgCDqtazrtoTtlZzri6QuIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI
7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp
7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg
67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19mYXRhbF9h
bGFybV9lcXVhbHNfdHJpcF9pbnRlcmxvY2siLAogICAgICAiY2xhaW0iOiAiQWxhcm0sIFRyaXDq
s7wgSW50ZXJsb2Nr7J2AIOqwmeydgCDquLDriqXsnbTri6QuIiwKICAgICAgIndyb25nX2NsYWlt
IjogIkFsYXJtLCBUcmlw6rO8IEludGVybG9ja+ydgCDqsJnsnYAg6riw64ql7J2064ukLiIsCiAg
ICAgICJjb3JyZWN0aW9uIjogIkFsYXJt7J2AIOyatOyghOyekCDsobDsuZjrpbwg7KeA7JuQ7ZWY
64qUIOygleuztCDquLDriqXsnbTqs6AgVHJpcMK3SW50ZXJsb2Nr7J2AIOyekOuPmSDrs7TtmLgg
65iQ64qUIOuPmeyekeygnOyVvSDrhbzrpqzsnbTri6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6
ICJBbGFybeydgCDsmrTsoITsnpAg7KGw7LmY66W8IOyngOybkO2VmOuKlCDsoJXrs7Qg6riw64ql
7J206rOgIFRyaXDCt0ludGVybG9ja+ydgCDsnpDrj5kg67O07Zi4IOuYkOuKlCDrj5nsnpHsoJzs
lb0g64W866as7J2064ukLiIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZl
Y3RlZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAi
bWVzc2FnZSI6ICJBbGFybSwgVHJpcOqzvCBJbnRlcmxvY2vsnYAg6rCZ7J2AIOq4sOuKpeydtOuL
pC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0
YWwg7ZuE67O066GcIOuzuOuLpC4gQWxhcm3snYAg7Jq07KCE7J6QIOyhsOy5mOulvCDsp4Dsm5Dt
lZjripQg7KCV67O0IOq4sOuKpeydtOqzoCBUcmlwwrdJbnRlcmxvY2vsnYAg7J6Q64+ZIOuztO2Y
uCDrmJDripQg64+Z7J6R7KCc7JW9IOuFvOumrOydtOuLpC4iLAogICAgICAiZ3JhZGluZ19ub3Rl
cyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWcIOqyveyasOyX
kOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65KkIOygleygleyd
gCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAgICJpZCI6ICJz
dzAzX2ZhdGFsX2Fja19jbGVhcnNfY29uZGl0aW9uIiwKICAgICAgImNsYWltIjogIkFsYXJt7J2E
IEFja25vd2xlZGdl7ZWY66m0IOqzteyglSDsm5Dsnbjqs7wgQWxhcm0g7KGw6rG07J20IO2VtOyg
nOuQnOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiQWxhcm3snYQgQWNrbm93bGVkZ2XtlZjr
qbQg6rO17KCVIOybkOyduOqzvCBBbGFybSDsobDqsbTsnbQg7ZW07KCc65Cc64ukLiIsCiAgICAg
ICJjb3JyZWN0aW9uIjogIkFja25vd2xlZGdl64qUIOyatOyghOyekCDsnbjsp4Ag6riw66Gd7J20
66mwIFByb2Nlc3MgY29uZGl0aW9u6rO8IEFjdGl2ZSDsg4Htg5zrpbwg7ZW07KCc7ZWY7KeAIOyV
iuuKlOuLpC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIkFja25vd2xlZGdl64qUIOyatOyghOye
kCDsnbjsp4Ag6riw66Gd7J2066mwIFByb2Nlc3MgY29uZGl0aW9u6rO8IEFjdGl2ZSDsg4Htg5zr
pbwg7ZW07KCc7ZWY7KeAIOyViuuKlOuLpC4iLAogICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAog
ICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJDIiwKICAgICAgICAiRCIKICAgICAg
XSwKICAgICAgIm1lc3NhZ2UiOiAiQWxhcm3snYQgQWNrbm93bGVkZ2XtlZjrqbQg6rO17KCVIOyb
kOyduOqzvCBBbGFybSDsobDqsbTsnbQg7ZW07KCc65Cc64ukLiIsCiAgICAgICJkZXNjcmlwdGlv
biI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBB
Y2tub3dsZWRnZeuKlCDsmrTsoITsnpAg7J247KeAIOq4sOuhneydtOupsCBQcm9jZXNzIGNvbmRp
dGlvbuqzvCBBY3RpdmUg7IOB7YOc66W8IO2VtOygnO2VmOyngCDslYrripTri6QuIiwKICAgICAg
ImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOyg
le2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247Jqp
IOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewog
ICAgICAiaWQiOiAic3cwM19mYXRhbF9wcmlvcml0eV9ieV9wdl9vbmx5IiwKICAgICAgImNsYWlt
IjogIkFsYXJtIOyasOyEoOyInOychOuKlCDsuKHsoJXqsJLsnZgg7YGs6riw66eM7Jy866GcIOyg
le2VnOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiQWxhcm0g7Jqw7ISg7Iic7JyE64qUIOy4
oeygleqwkuydmCDtgazquLDrp4zsnLzroZwg7KCV7ZWc64ukLiIsCiAgICAgICJjb3JyZWN0aW9u
IjogIkFsYXJtIOyasOyEoOyInOychOuKlCDqsrDqs7wg7Ius6rCB64+E7JmAIO2XiOyaqSDsnZHr
i7Xsi5zqsITsnYQg7ZWo6ruYIO2PieqwgO2VmOyXrCDsoJXtlZzri6QuIiwKICAgICAgImNvcnJl
Y3RfcnVsZSI6ICJBbGFybSDsmrDshKDsiJzsnITripQg6rKw6rO8IOyLrOqwgeuPhOyZgCDtl4js
mqkg7J2R64u17Iuc6rCE7J2EIO2VqOq7mCDtj4nqsIDtlZjsl6wg7KCV7ZWc64ukLiIsCiAgICAg
ICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAg
IkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6ICJBbGFybSDsmrDshKDs
iJzsnITripQg7Lih7KCV6rCS7J2YIO2BrOq4sOunjOycvOuhnCDsoJXtlZzri6QuIiwKICAgICAg
ImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuh
nCDrs7jri6QuIEFsYXJtIOyasOyEoOyInOychOuKlCDqsrDqs7wg7Ius6rCB64+E7JmAIO2XiOya
qSDsnZHri7Xsi5zqsITsnYQg7ZWo6ruYIO2PieqwgO2VmOyXrCDsoJXtlZzri6QuIiwKICAgICAg
ImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOyg
le2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247Jqp
IOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewog
ICAgICAiaWQiOiAic3cwM19mYXRhbF9kZWFkYmFuZF9lcXVhbHNfZGVsYXkiLAogICAgICAiY2xh
aW0iOiAiQWxhcm0gRGVhZGJhbmTsmYAgRGVsYXnripQg6rCZ7J2AIOq4sOuKpeydtOuLpC4iLAog
ICAgICAid3JvbmdfY2xhaW0iOiAiQWxhcm0gRGVhZGJhbmTsmYAgRGVsYXnripQg6rCZ7J2AIOq4
sOuKpeydtOuLpC4iLAogICAgICAiY29ycmVjdGlvbiI6ICJEZWFkYmFuZOuKlCDqsJLsnZgg67O1
6reAIOydtOugpe2PreydtOqzoCBEZWxheeuKlCDsobDqsbQg7KeA7IaN7Iuc6rCE7J2EIOydtOya
qe2VmOuKlCDsi5zqsIQg7ZWE7YSw7J2064ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAiRGVh
ZGJhbmTripQg6rCS7J2YIOuzteq3gCDsnbTroKXtj63snbTqs6AgRGVsYXnripQg7KGw6rG0IOyn
gOyGjeyLnOqwhOydhCDsnbTsmqntlZjripQg7Iuc6rCEIO2VhO2EsOydtOuLpC4iLAogICAgICAi
c2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJD
IiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgIm1lc3NhZ2UiOiAiQWxhcm0gRGVhZGJhbmTs
mYAgRGVsYXnripQg6rCZ7J2AIOq4sOuKpeydtOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi
66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gRGVhZGJh
bmTripQg6rCS7J2YIOuzteq3gCDsnbTroKXtj63snbTqs6AgRGVsYXnripQg7KGw6rG0IOyngOyG
jeyLnOqwhOydhCDsnbTsmqntlZjripQg7Iuc6rCEIO2VhO2EsOydtOuLpC4iLAogICAgICAiZ3Jh
ZGluZ19ub3RlcyI6ICLri7XslYjsnbQg7ZW064u5IOyYpOuLteydhCDsp4HsoJEg64uo7KCV7ZWc
IOqyveyasOyXkOunjCDsoIHsmqntlZjrqbAg64uo7IicIOuIhOudveydtOuCmCDsnbjsmqkg65Kk
IOygleygleydgCBmYXRhbOuhnCDrs7Tsp4Ag7JWK64qU64ukLiIKICAgIH0sCiAgICB7CiAgICAg
ICJpZCI6ICJzdzAzX2ZhdGFsX3NoZWx2aW5nX2RlbGV0ZXNfaGlzdG9yeSIsCiAgICAgICJjbGFp
bSI6ICJTaGVsdmluZ+2VmOuptCBBbGFybSDsoJXsnZjsmYAg7J2066Cl7J20IOyCreygnOuQnOuL
pC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiU2hlbHZpbmftlZjrqbQgQWxhcm0g7KCV7J2Y7JmA
IOydtOugpeydtCDsgq3soJzrkJzri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAiU2hlbHZpbmfs
nYAg7KCc7ZWc7Iuc6rCEIOuPmeyViCBBY3RpdmUgZGlzcGxheeyXkOyEnCDsnoTsi5zroZwg7Iio
6riw64qUIOq4sOuKpeydtOupsCDsoJXsnZjsmYAg7J2066Cl7J2AIOycoOyngO2VnOuLpC4iLAog
ICAgICAiY29ycmVjdF9ydWxlIjogIlNoZWx2aW5n7J2AIOygnO2VnOyLnOqwhCDrj5nslYggQWN0
aXZlIGRpc3BsYXnsl5DshJwg7J6E7Iuc66GcIOyIqOq4sOuKlCDquLDriqXsnbTrqbAg7KCV7J2Y
7JmAIOydtOugpeydgCDsnKDsp4DtlZzri6QuIiwKICAgICAgInNldmVyaXR5IjogImZhdGFsIiwK
ICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQiCiAgICAg
IF0sCiAgICAgICJtZXNzYWdlIjogIlNoZWx2aW5n7ZWY66m0IEFsYXJtIOygleydmOyZgCDsnbTr
oKXsnbQg7IKt7KCc65Cc64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY
64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBTaGVsdmluZ+ydgCDsoJztlZzs
i5zqsIQg64+Z7JWIIEFjdGl2ZSBkaXNwbGF57JeQ7IScIOyehOyLnOuhnCDsiKjquLDripQg6riw
64ql7J2066mwIOygleydmOyZgCDsnbTroKXsnYAg7Jyg7KeA7ZWc64ukLiIsCiAgICAgICJncmFk
aW5nX25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg
6rK97Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg
7KCV7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDNfZmF0YWxfc3VwcHJlc3Npb25fZXF1YWxzX3NoZWx2aW5nIiwKICAgICAgImNs
YWltIjogIlN1cHByZXNzaW9u6rO8IFNoZWx2aW5n7J2AIOyatOyghOyekOqwgCDsnoTsnZjroZwg
QWxhcm3snYQg7Iio6riw64qUIOuPmeydvCDquLDriqXsnbTri6QuIiwKICAgICAgIndyb25nX2Ns
YWltIjogIlN1cHByZXNzaW9u6rO8IFNoZWx2aW5n7J2AIOyatOyghOyekOqwgCDsnoTsnZjroZwg
QWxhcm3snYQg7Iio6riw64qUIOuPmeydvCDquLDriqXsnbTri6QuIiwKICAgICAgImNvcnJlY3Rp
b24iOiAiU3VwcHJlc3Npb27snYAg7ISk6rOE65CcIOyDge2DnMK364W866as7KGw6rG07JeQIOuU
sOuluCDsnpDrj5kg7KCc7Jm47J206rOgIFNoZWx2aW5n7J2AIOq2jO2VnCDsnojripQg7Jq07KCE
7J6Q7J2YIOygnO2VnOyLnOqwhCDsnoTsi5wg7KGw7LmY7J2064ukLiIsCiAgICAgICJjb3JyZWN0
X3J1bGUiOiAiU3VwcHJlc3Npb27snYAg7ISk6rOE65CcIOyDge2DnMK364W866as7KGw6rG07JeQ
IOuUsOuluCDsnpDrj5kg7KCc7Jm47J206rOgIFNoZWx2aW5n7J2AIOq2jO2VnCDsnojripQg7Jq0
7KCE7J6Q7J2YIOygnO2VnOyLnOqwhCDsnoTsi5wg7KGw7LmY7J2064ukLiIsCiAgICAgICJzZXZl
cml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgIkMiLAog
ICAgICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6ICJTdXBwcmVzc2lvbuqzvCBTaGVs
dmluZ+ydgCDsmrTsoITsnpDqsIAg7J6E7J2Y66GcIEFsYXJt7J2EIOyIqOq4sOuKlCDrj5nsnbwg
6riw64ql7J2064ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyj
vOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBTdXBwcmVzc2lvbuydgCDshKTqs4TrkJwg
7IOB7YOcwrfrhbzrpqzsobDqsbTsl5Ag65Sw66W4IOyekOuPmSDsoJzsmbjsnbTqs6AgU2hlbHZp
bmfsnYAg6raM7ZWcIOyeiOuKlCDsmrTsoITsnpDsnZgg7KCc7ZWc7Iuc6rCEIOyehOyLnCDsobDs
uZjsnbTri6QuIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTr
i7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDr
iITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuL
pC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19mYXRhbF9pbmRlZmluaXRlX3NoZWx2
aW5nIiwKICAgICAgImNsYWltIjogIkFsYXJtIFNoZWx2aW5n7J2AIOyCrOycoOyZgCDrp4zro4zs
i5zqsIQg7JeG7J20IOustOq4sO2VnCDsnKDsp4DtlbTrj4Qg65Cc64ukLiIsCiAgICAgICJ3cm9u
Z19jbGFpbSI6ICJBbGFybSBTaGVsdmluZ+ydgCDsgqzsnKDsmYAg66eM66OM7Iuc6rCEIOyXhuyd
tCDrrLTquLDtlZwg7Jyg7KeA7ZW064+EIOuQnOuLpC4iLAogICAgICAiY29ycmVjdGlvbiI6ICJT
aGVsdmluZ+ydgCDsirnsnbjqtoztlZwsIOyCrOycoCwg7KCc7ZWc7Iuc6rCELCDtkZzsi5wsIOun
jOujjOyZgCDrs7XqtaztmZXsnbjsnYQg6rSA66as7ZW07JW8IO2VnOuLpC4iLAogICAgICAiY29y
cmVjdF9ydWxlIjogIlNoZWx2aW5n7J2AIOyKueyduOq2jO2VnCwg7IKs7JygLCDsoJztlZzsi5zq
sIQsIO2RnOyLnCwg66eM66OM7JmAIOuzteq1rO2ZleyduOydhCDqtIDrpqztlbTslbwg7ZWc64uk
LiIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBb
CiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6ICJBbGFy
bSBTaGVsdmluZ+ydgCDsgqzsnKDsmYAg66eM66OM7Iuc6rCEIOyXhuydtCDrrLTquLDtlZwg7Jyg
7KeA7ZW064+EIOuQnOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuM
gCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gU2hlbHZpbmfsnYAg7Iq57J246raM
7ZWcLCDsgqzsnKAsIOygnO2VnOyLnOqwhCwg7ZGc7IucLCDrp4zro4zsmYAg67O16rWs7ZmV7J24
7J2EIOq0gOumrO2VtOyVvCDtlZzri6QuIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI
7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp
7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg
67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19mYXRhbF92
YWx1ZXNfaW50ZXJjaGFuZ2VhYmxlIiwKICAgICAgImNsYWltIjogIuyatOyghCBTZXRwb2ludCwg
QWxhcm0gdmFsdWUsIFRyaXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl64qUIOyEnOuhnCDrsJTq
vrjslrQg7IKs7Jqp7ZW064+EIOuQnOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAi7Jq07KCE
IFNldHBvaW50LCBBbGFybSB2YWx1ZSwgVHJpcCB2YWx1ZeyZgCBJbnRlcmxvY2sgdmFsdWXripQg
7ISc66GcIOuwlOq+uOyWtCDsgqzsmqntlbTrj4Qg65Cc64ukLiIsCiAgICAgICJjb3JyZWN0aW9u
IjogIuuEpCDqsJLsnYAg66qp7KCB6rO8IOyGjOycoOq2jOydtCDri6TrpbTrr4DroZwg6re86rGw
7JmAIOuzgOqyveq0gOumrOulvCDrtoTrpqztlbTslbwg7ZWc64ukLiIsCiAgICAgICJjb3JyZWN0
X3J1bGUiOiAi64SkIOqwkuydgCDrqqnsoIHqs7wg7IaM7Jyg6raM7J20IOuLpOultOuvgOuhnCDq
t7zqsbDsmYAg67OA6rK96rSA66as66W8IOu2hOumrO2VtOyVvCDtlZzri6QuIiwKICAgICAgInNl
dmVyaXR5IjogImZhdGFsIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAiQyIs
CiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJtZXNzYWdlIjogIuyatOyghCBTZXRwb2ludCwg
QWxhcm0gdmFsdWUsIFRyaXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl64qUIOyEnOuhnCDrsJTq
vrjslrQg7IKs7Jqp7ZW064+EIOuQnOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc
7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g64SkIOqwkuydgCDr
qqnsoIHqs7wg7IaM7Jyg6raM7J20IOuLpOultOuvgOuhnCDqt7zqsbDsmYAg67OA6rK96rSA66as
66W8IOu2hOumrO2VtOyVvCDtlZzri6QuIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u17JWI
7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB7Jqp
7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzroZwg
67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19mYXRhbF9z
b2Vfd2l0aG91dF9zeW5jIiwKICAgICAgImNsYWltIjogIuyLnOqwgeuPmeq4sOqwgCDsl4bslrTr
j4QgU09F7J2YIOydtOuypO2KuCDshKDtm4TqtIDqs4TripQg7ZWt7IOBIOygle2Zle2VmOuLpC4i
LAogICAgICAid3JvbmdfY2xhaW0iOiAi7Iuc6rCB64+Z6riw6rCAIOyXhuyWtOuPhCBTT0XsnZgg
7J2067Kk7Yq4IOyEoO2bhOq0gOqzhOuKlCDtla3sg4Eg7KCV7ZmV7ZWY64ukLiIsCiAgICAgICJj
b3JyZWN0aW9uIjogIlNPReydmCDsnbjqs7zsiJzshJzrpbwg7Iug66Kw7ZWY66Ck66m0IOqzte2G
tSDsi5zqsITrj5nquLAsIFRpbWVzdGFtcCDstpzsspgsIOygle2ZleuPhOyZgCBUaW1lIHF1YWxp
dHnqsIAg7ZWE7JqU7ZWY64ukLiIsCiAgICAgICJjb3JyZWN0X3J1bGUiOiAiU09F7J2YIOyduOqz
vOyInOyEnOulvCDsi6DrorDtlZjroKTrqbQg6rO17Ya1IOyLnOqwhOuPmeq4sCwgVGltZXN0YW1w
IOy2nOyymCwg7KCV7ZmV64+E7JmAIFRpbWUgcXVhbGl0eeqwgCDtlYTsmpTtlZjri6QuIiwKICAg
ICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAg
ICAiQyIsCiAgICAgICAgIkQiCiAgICAgIF0sCiAgICAgICJtZXNzYWdlIjogIuyLnOqwgeuPmeq4
sOqwgCDsl4bslrTrj4QgU09F7J2YIOydtOuypO2KuCDshKDtm4TqtIDqs4TripQg7ZWt7IOBIOyg
le2Zle2VmOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zs
nqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gU09F7J2YIOyduOqzvOyInOyEnOulvCDsi6Dr
orDtlZjroKTrqbQg6rO17Ya1IOyLnOqwhOuPmeq4sCwgVGltZXN0YW1wIOy2nOyymCwg7KCV7ZmV
64+E7JmAIFRpbWUgcXVhbGl0eeqwgCDtlYTsmpTtlZjri6QuIiwKICAgICAgImdyYWRpbmdfbm90
ZXMiOiAi64u17JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDs
l5Drp4wg7KCB7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXs
nYAgZmF0YWzroZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAi
c3cwM19mYXRhbF9oaXN0b3JpYW5fZXF1YWxzX3NvZSIsCiAgICAgICJjbGFpbSI6ICJIaXN0b3Jp
YW4g7ZGc67O47Iuc6rCE66eM7Jy866GcIFNPReyZgCDrj5nsnbztlZwg7J2067Kk7Yq4IOyInOyE
nOulvCDtla3sg4Eg7J6s7ZiE7ZWgIOyImCDsnojri6QuIiwKICAgICAgIndyb25nX2NsYWltIjog
Ikhpc3RvcmlhbiDtkZzrs7jsi5zqsITrp4zsnLzroZwgU09F7JmAIOuPmeydvO2VnCDsnbTrsqTt
irgg7Iic7ISc66W8IO2VreyDgSDsnqztmITtlaAg7IiYIOyeiOuLpC4iLAogICAgICAiY29ycmVj
dGlvbiI6ICJIaXN0b3JpYW4g7LaU7IS47JmAIFNPRSDsnbTrsqTtirjsiJzshJzripQg7ZGc67O4
7KO86riw7JmAIFRpbWVzdGFtcCDstpzsspjqsIAg64uk66W066+A66GcIOuPmeydvO2VmOuLpOqz
oCDri6jsoJXtlaAg7IiYIOyXhuuLpC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIkhpc3Rvcmlh
biDstpTshLjsmYAgU09FIOydtOuypO2KuOyInOyEnOuKlCDtkZzrs7jso7zquLDsmYAgVGltZXN0
YW1wIOy2nOyymOqwgCDri6TrpbTrr4DroZwg64+Z7J287ZWY64uk6rOgIOuLqOygle2VoCDsiJgg
7JeG64ukLiIsCiAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXll
cnMiOiBbCiAgICAgICAgIkMiLAogICAgICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6
ICJIaXN0b3JpYW4g7ZGc67O47Iuc6rCE66eM7Jy866GcIFNPReyZgCDrj5nsnbztlZwg7J2067Kk
7Yq4IOyInOyEnOulvCDtla3sg4Eg7J6s7ZiE7ZWgIOyImCDsnojri6QuIiwKICAgICAgImRlc2Ny
aXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jr
i6QuIEhpc3RvcmlhbiDstpTshLjsmYAgU09FIOydtOuypO2KuOyInOyEnOuKlCDtkZzrs7jso7zq
uLDsmYAgVGltZXN0YW1wIOy2nOyymOqwgCDri6TrpbTrr4DroZwg64+Z7J287ZWY64uk6rOgIOuL
qOygle2VoCDsiJgg7JeG64ukLiIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuuLteyViOydtCDt
lbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyggeyaqe2VmOup
sCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs66GcIOuztOyn
gCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfZmF0YWxfYXVkaXRf
ZXF1YWxzX3NvZSIsCiAgICAgICJjbGFpbSI6ICJBdWRpdCB0cmFpbOqzvCBTT0XripQg64+Z7J28
7ZWcIOq4sOuhneydtOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiQXVkaXQgdHJhaWzqs7wg
U09F64qUIOuPmeydvO2VnCDquLDroZ3snbTri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAiQXVk
aXQgdHJhaWzsnYAg7IKs7Jqp7J6QIO2WieychOyZgCDrs4Dqsr3snYQg6riw66Gd7ZWY6rOgIFNP
ReuKlCDqs7XsoJXCt+yEpOu5hCDsg4Htg5zrs4DtmZTsnZgg7Iic7ISc66W8IOq4sOuhne2VnOuL
pC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIkF1ZGl0IHRyYWls7J2AIOyCrOyaqeyekCDtlons
nITsmYAg67OA6rK97J2EIOq4sOuhne2VmOqzoCBTT0XripQg6rO17KCVwrfshKTruYQg7IOB7YOc
67OA7ZmU7J2YIOyInOyEnOulvCDquLDroZ3tlZzri6QuIiwKICAgICAgInNldmVyaXR5IjogImZh
dGFsIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQi
CiAgICAgIF0sCiAgICAgICJtZXNzYWdlIjogIkF1ZGl0IHRyYWls6rO8IFNPReuKlCDrj5nsnbzt
lZwg6riw66Gd7J2064ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yA
IOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBBdWRpdCB0cmFpbOydgCDsgqzsmqns
npAg7ZaJ7JyE7JmAIOuzgOqyveydhCDquLDroZ3tlZjqs6AgU09F64qUIOqzteyglcK37ISk67mE
IOyDge2DnOuzgO2ZlOydmCDsiJzshJzrpbwg6riw66Gd7ZWc64ukLiIsCiAgICAgICJncmFkaW5n
X25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK9
7Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV
7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAgImlk
IjogInN3MDNfZmF0YWxfYnJpZ2h0X2NvbG9ycyIsCiAgICAgICJjbGFpbSI6ICJIaWdoLXBlcmZv
cm1hbmNlIEhNSeuKlCDrsJ3snYAg7IOJ7J2EIOunjuydtCDsgqzsmqntlaDsiJjroZ0g7IOB7Zmp
7J247Iud7J20IOyii+yVhOynhOuLpC4iLAogICAgICAid3JvbmdfY2xhaW0iOiAiSGlnaC1wZXJm
b3JtYW5jZSBITUnripQg67Cd7J2AIOyDieydhCDrp47snbQg7IKs7Jqp7ZWg7IiY66GdIOyDge2Z
qeyduOyLneydtCDsoovslYTsp4Tri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAiSGlnaC1wZXJm
b3JtYW5jZSBITUnripQg7IOJ7IOB7J2EIOygnO2VnOuQnCDruYTsoJXsg4Eg7J2Y66+47JeQIOyd
vOq0gOuQmOqyjCDsgqzsmqntlZjsl6wg7Iuc6rCB7KCBIOyasOyEoOyInOychOulvCDrp4zrk6Dr
i6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6ICJIaWdoLXBlcmZvcm1hbmNlIEhNSeuKlCDsg4ns
g4HsnYQg7KCc7ZWc65CcIOu5hOygleyDgSDsnZjrr7jsl5Ag7J286rSA65CY6rKMIOyCrOyaqe2V
mOyXrCDsi5zqsIHsoIEg7Jqw7ISg7Iic7JyE66W8IOunjOuToOuLpC4iLAogICAgICAic2V2ZXJp
dHkiOiAiZmF0YWwiLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJDIiwKICAg
ICAgICAiRCIKICAgICAgXSwKICAgICAgIm1lc3NhZ2UiOiAiSGlnaC1wZXJmb3JtYW5jZSBITUnr
ipQg67Cd7J2AIOyDieydhCDrp47snbQg7IKs7Jqp7ZWg7IiY66GdIOyDge2ZqeyduOyLneydtCDs
oovslYTsp4Tri6QuIiwKICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO8
7J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIEhpZ2gtcGVyZm9ybWFuY2UgSE1J64qUIOyD
ieyDgeydhCDsoJztlZzrkJwg67mE7KCV7IOBIOydmOuvuOyXkCDsnbzqtIDrkJjqsowg7IKs7Jqp
7ZWY7JesIOyLnOqwgeyggSDsmrDshKDsiJzsnITrpbwg66eM65Og64ukLiIsCiAgICAgICJncmFk
aW5nX25vdGVzIjogIuuLteyViOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg
6rK97Jqw7JeQ66eMIOyggeyaqe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg
7KCV7KCV7J2AIGZhdGFs66GcIOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAg
ImlkIjogInN3MDNfZmF0YWxfdW5yZXN0cmljdGVkX2F1dGhvcml0eSIsCiAgICAgICJjbGFpbSI6
ICLsmrTsoITsnpDsl5Dqsowg66qo65OgIFNldHBvaW507JmAIOuztO2YuOq0gOugqCDqsJLsnYQg
7KCc7ZWcIOyXhuydtCDrs4Dqsr3tlZjqsowg7ZW07JW8IOyViOyghO2VmOuLpC4iLAogICAgICAi
d3JvbmdfY2xhaW0iOiAi7Jq07KCE7J6Q7JeQ6rKMIOuqqOuToCBTZXRwb2ludOyZgCDrs7TtmLjq
tIDroKgg6rCS7J2EIOygnO2VnCDsl4bsnbQg67OA6rK97ZWY6rKMIO2VtOyVvCDslYjsoITtlZjr
i6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAi7KSR7JqUIOqwkuqzvCDsobDsnpHsnYAg7Jet7ZWg
6riw67CYIOy1nOyGjOq2jO2VnCwg7Iq57J24LCDtmZXsnbjqs7wgQXVkaXQgdHJhaWzroZwg7Ya1
7KCc7ZW07JW8IO2VnOuLpC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIuykkeyalCDqsJLqs7wg
7KGw7J6R7J2AIOyXre2VoOq4sOuwmCDstZzshozqtoztlZwsIOyKueyduCwg7ZmV7J246rO8IEF1
ZGl0IHRyYWls66GcIO2GteygnO2VtOyVvCDtlZzri6QuIiwKICAgICAgInNldmVyaXR5IjogImZh
dGFsIiwKICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAiQyIsCiAgICAgICAgIkQi
CiAgICAgIF0sCiAgICAgICJtZXNzYWdlIjogIuyatOyghOyekOyXkOqyjCDrqqjrk6AgU2V0cG9p
bnTsmYAg67O07Zi46rSA66CoIOqwkuydhCDsoJztlZwg7JeG7J20IOuzgOqyve2VmOqyjCDtlbTs
lbwg7JWI7KCE7ZWY64ukLiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yA
IOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDspJHsmpQg6rCS6rO8IOyhsOyekeyd
gCDsl63tlaDquLDrsJgg7LWc7IaM6raM7ZWcLCDsirnsnbgsIO2ZleyduOqzvCBBdWRpdCB0cmFp
bOuhnCDthrXsoJztlbTslbwg7ZWc64ukLiIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuuLteyV
iOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyggeya
qe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs66Gc
IOuztOyngCDslYrripTri6QuIgogICAgfSwKICAgIHsKICAgICAgImlkIjogInN3MDNfZmF0YWxf
Y29tbWFuZF9wcm92ZXNfYWN0aW9uIiwKICAgICAgImNsYWltIjogIkhNSeyXkOyEnCDrqoXroLns
nYQg7KCE7Iah7ZWY66m0IO2YhOyepeyEpOu5hCDrj5nsnpHsnbQg7JmE66OM65CcIOqyg+ycvOuh
nCDtjJDri6jtlZzri6QuIiwKICAgICAgIndyb25nX2NsYWltIjogIkhNSeyXkOyEnCDrqoXroLns
nYQg7KCE7Iah7ZWY66m0IO2YhOyepeyEpOu5hCDrj5nsnpHsnbQg7JmE66OM65CcIOqyg+ycvOuh
nCDtjJDri6jtlZzri6QuIiwKICAgICAgImNvcnJlY3Rpb24iOiAi66qF66C5IOyghOyGoeqzvCDs
i6TsoJwgRmVlZGJhY2vsnYQg67aE66as7ZWY6rOgIFRpbWVvdXTCt+u2iOydvOy5mMK37ZKI7KeI
7IOB7YOc66W8IO2ZleyduO2VtOyVvCDtlZzri6QuIiwKICAgICAgImNvcnJlY3RfcnVsZSI6ICLr
qoXroLkg7KCE7Iah6rO8IOyLpOygnCBGZWVkYmFja+ydhCDrtoTrpqztlZjqs6AgVGltZW91dMK3
67aI7J287LmYwrftkojsp4jsg4Htg5zrpbwg7ZmV7J247ZW07JW8IO2VnOuLpC4iLAogICAgICAi
c2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICJD
IiwKICAgICAgICAiRCIKICAgICAgXSwKICAgICAgIm1lc3NhZ2UiOiAiSE1J7JeQ7IScIOuqheug
ueydhCDsoITshqHtlZjrqbQg7ZiE7J6l7ISk67mEIOuPmeyekeydtCDsmYTro4zrkJwg6rKD7Jy8
66GcIO2MkOuLqO2VnOuLpC4iLAogICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuM
gCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g66qF66C5IOyghOyGoeqzvCDsi6Ts
oJwgRmVlZGJhY2vsnYQg67aE66as7ZWY6rOgIFRpbWVvdXTCt+u2iOydvOy5mMK37ZKI7KeI7IOB
7YOc66W8IO2ZleyduO2VtOyVvCDtlZzri6QuIiwKICAgICAgImdyYWRpbmdfbm90ZXMiOiAi64u1
7JWI7J20IO2VtOuLuSDsmKTri7XsnYQg7KeB7KCRIOuLqOygle2VnCDqsr3smrDsl5Drp4wg7KCB
7Jqp7ZWY66mwIOuLqOyInCDriITrnb3snbTrgpgg7J247JqpIOuSpCDsoJXsoJXsnYAgZmF0YWzr
oZwg67O07KeAIOyViuuKlOuLpC4iCiAgICB9LAogICAgewogICAgICAiaWQiOiAic3cwM19mYXRh
bF9yYWlzZV9hbGxfcHJpb3JpdGllcyIsCiAgICAgICJjbGFpbSI6ICJBbGFybSBmbG9vZOuKlCDr
qqjrk6AgQWxhcm0g7Jqw7ISg7Iic7JyE66W8IOuGkuydtOuptCDtlbTqsrDrkJzri6QuIiwKICAg
ICAgIndyb25nX2NsYWltIjogIkFsYXJtIGZsb29k64qUIOuqqOuToCBBbGFybSDsmrDshKDsiJzs
nITrpbwg64aS7J2066m0IO2VtOqysOuQnOuLpC4iLAogICAgICAiY29ycmVjdGlvbiI6ICJBbGFy
bSBmbG9vZOuKlCDsm5Dsnbgg7KCc6rGwLCDtlanrpqztmZQsIENoYXR0ZXJpbmcg6rCc7ISgLCDs
g4Htg5zquLDrsJggU3VwcHJlc3Npb27qs7wg7ZmU66m0wrfsoIjssKgg6rCc7ISg7Jy866GcIOyk
hOyduOuLpC4iLAogICAgICAiY29ycmVjdF9ydWxlIjogIkFsYXJtIGZsb29k64qUIOybkOyduCDs
oJzqsbAsIO2VqeumrO2ZlCwgQ2hhdHRlcmluZyDqsJzshKAsIOyDge2DnOq4sOuwmCBTdXBwcmVz
c2lvbuqzvCDtmZTrqbTCt+ygiOywqCDqsJzshKDsnLzroZwg7KSE7J2464ukLiIsCiAgICAgICJz
ZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgIkMi
LAogICAgICAgICJEIgogICAgICBdLAogICAgICAibWVzc2FnZSI6ICJBbGFybSBmbG9vZOuKlCDr
qqjrk6AgQWxhcm0g7Jqw7ISg7Iic7JyE66W8IOuGkuydtOuptCDtlbTqsrDrkJzri6QuIiwKICAg
ICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuz
tOuhnCDrs7jri6QuIEFsYXJtIGZsb29k64qUIOybkOyduCDsoJzqsbAsIO2VqeumrO2ZlCwgQ2hh
dHRlcmluZyDqsJzshKAsIOyDge2DnOq4sOuwmCBTdXBwcmVzc2lvbuqzvCDtmZTrqbTCt+ygiOyw
qCDqsJzshKDsnLzroZwg7KSE7J2464ukLiIsCiAgICAgICJncmFkaW5nX25vdGVzIjogIuuLteyV
iOydtCDtlbTri7kg7Jik64u17J2EIOyngeygkSDri6jsoJXtlZwg6rK97Jqw7JeQ66eMIOyggeya
qe2VmOupsCDri6jsiJwg64iE65297J2064KYIOyduOyaqSDrkqQg7KCV7KCV7J2AIGZhdGFs66Gc
IOuztOyngCDslYrripTri6QuIgogICAgfQogIF0sCiAgInNhZmVfZXhwcmVzc2lvbnMiOiBbCiAg
ICAiQWxhcm3qs7wgVHJpcOydgCDsl7Dqs4TrkKAg7IiYIOyeiOyngOunjCDrqqnsoIHqs7wg7Iuk
7ZaJ7KO87LK06rCAIOuLpOultOuLpC4iLAogICAgIuuqqOuToCBFdmVudOqwgCBBbGFybeyduCDq
soPsnYAg7JWE64uI64ukLiIsCiAgICAiQWNrbm93bGVkZ2XripQg7Jq07KCE7J6QIOyduOyngOul
vCDquLDroZ3tlZjrqbAg6rO17KCV7KGw6rG0IO2VtOygnOyZgCDrs4TqsJzsnbTri6QuIiwKICAg
ICJEZWFkYmFuZOyZgCBEZWxheeuKlCDrqqjrkZAgQ2hhdHRlcmluZ+ydhCDspITsnbwg7IiYIOye
iOycvOuCmCDqsJIg6riw67CY6rO8IOyLnOqwhCDquLDrsJjsnLzroZwg6rWs67aE65Cc64ukLiIs
CiAgICAiU2hlbHZpbmcg7KSR7JeQ64+EIEFsYXJtIOydtOugpeqzvCDsgqzsmqnquLDroZ3snYAg
7Jyg7KeA7ZWc64ukLiIsCiAgICAiU3VwcHJlc3Npb27snYAg7ISk6rOE65CcIOyatOyghOyDge2D
nCDsobDqsbTsl5Ag65Sw6528IOyekOuPmSDsoIHsmqntlaAg7IiYIOyeiOuLpC4iLAogICAgIkhp
Z2gtcGVyZm9ybWFuY2UgSE1J64+EIOydmOuvuOqwgCDrqoXtmZXtlZwg7KCc7ZWc65CcIOyDieyD
geydhCDsgqzsmqntlZzri6QuIiwKICAgICJUcmlwIOqwkuqzvCBBbGFybSDqsJLsnZgg7IOB64yA
7Iic7ISc64qUIOqzteyglSDsnITtl5jrsKntlqXqs7wg7J2R64u17Iuc6rCE7JeQIOuUsOudvCDs
oJXtlZzri6QuIiwKICAgICJJbnRlcmxvY2sgdmFsdWXripQg7Jew7IaNIOyImOy5mOqwgCDslYTr
i4jrnbwg7J207IKwIOyDge2DnCDrmJDripQg64W866as7KGw6rG07J28IOyImCDsnojri6QuIiwK
ICAgICJTT0Ug7KCV7ZmV64+E64qUIOyLnOqwhOuPmeq4sOyZgCDsnqXsuZggVGltZXN0YW1wIO2S
iOyniOyXkCDsnZjsobTtlZzri6QuIiwKICAgICJIaXN0b3JpYW7snYAgU09FIOu2hOyEneydhCDr
s7TsmYTtlaAg7IiYIOyeiOyngOunjCDtla3sg4Eg64yA7LK07ZWY7KeA64qUIOyViuuKlOuLpC4i
LAogICAgIkZpcnN0LW91dOqzvCBTT0Xrpbwg7ZWo6ruYIOyCrOyaqe2VmOuptCDstZzstIgg7JuQ
7J246rO8IOyghOyytCDsoITtjIzsiJzshJzrpbwg67mE6rWQ7ZWgIOyImCDsnojri6QuIiwKICAg
ICJBdWRpdCB0cmFpbOydgCDsgqzsmqnsnpAg7ZaJ7JyEIOy2lOyggeyXkCDspJHsoJDsnYQg65GU
64ukLiIsCiAgICAi67mE7IOB7KCI7LCo7JeQ7ISc64+EIOq2jO2VnCDtmZXrjIDsmYAg7IKs7ZuE
IEF1ZGl0IOq4sOuhnSDsobDqsbTsnYQg66qF7ZmV7Z6IIO2VtOyVvCDtlZzri6QuIiwKICAgICJB
bGFybSBwcmlvcml0eeuKlCDtmITsnqUg7LKg7ZWZ7JeQIOygleydmOuQnCDqsrDqs7zsmYAg7J2R
64u17Iuc6rCEIOq4sOykgOydhCDrlLDrpbjri6QuIiwKICAgICJTaGVsdmluZyDtl4jsmqnsi5zq
sITsnYAgQWxhcm0g7Yq57ISx6rO8IO2YhOyepSDsoJXssYXsl5Ag65Sw6528IOuLrOudvOyniCDs
iJgg7J6I64ukLiIsCiAgICAiRGlzcGxheSBoaWVyYXJjaHnsnZgg7IS467aAIExldmVsIOuqhey5
reydgCDsi5zsiqTthZzsl5Ag65Sw6528IOuLrOudvOuPhCDsg4HsnIQgT3ZlcnZpZXfsmYAg7IOB
7IS4IOynhOuLqOydmCDtnZDrpoTsnYAg7Jyg7KeA7ZWc64ukLiIsCiAgICAiU0NBREEg6rWs7ISx
7J2AIOykkeyVmeynkeykke2YlSwg67aE7IKw7ZiVIOuYkOuKlCDqsIDsg4HtmZQg6rWs7KGw6rCA
IOqwgOuKpe2VmOuLpC4iCiAgXSwKICAicmV2aXNpb25fbm90ZXMiOiBbCiAgICAiMjAyNi0wOC0w
NjogU1ctMDMg7Jq07KCE7KCV67O0IOq0gOumrCBvd25lcnNoaXDqs7wgU1ctMDIg7Iuk7ZaJ64W8
66asIOqyveqzhOulvCDtmZXsoJXtlojri6QuIiwKICAgICJBbGFybSBwaGlsb3NvcGh5LCByYXRp
b25hbGl6YXRpb24sIERlYWRiYW5kLCBEZWxheSwgU2hlbHZpbmcsIFN1cHByZXNzaW9uLCBTT0Xs
mYAgQXVkaXQgdHJhaWzsnYQg67aE66as65CcIEZhY3TroZwg6rWs7ISx7ZaI64ukLiIsCiAgICAi
U0lMIOyCsOyglSwgVi1Nb2RlbOqzvCDtlITroZzsoJ3tirggRkFUwrdTQVTripQg7J247KCRIFRv
cGlj7Jy866GcIOuEmOqyvOuLpC4iLAogICAgIjIwMjYtMDgtMDcgTExNIOydmOuvuCDqsJDsgqwg
7IiY66asOiAzMeqwnCBBbmNob3LsnZggcmVqZWN0ZWQg7ISk66qF7J2EIOq4sOuKpeuzhCDsi6Ts
oJwg67CY64yA6rCc64WQ7Jy866GcIOq1kOyytO2WiOuLpC4iCiAgXSwKICAidG9waWNfbGFiZWwi
OiAiU1ctMDMgSE1JwrdTQ0FEQcK3QWxhcm3Ct1NPRSIsCiAgImNvcmVfZmFjdHMiOiBbCiAgICAi
U1ctMDPripQgSE1JwrdTQ0FEQSDqtazsobAsIOqzoOyEseuKpSBITUksIEFsYXJtIOq0gOumrCwg
U2V0cG9pbnTCt0FsYXJtwrdUcmlwwrdJbnRlcmxvY2sg6rCSIOq0gOumrCwgU09FLCBBdWRpdCB0
cmFpbCwg7Jq07KCE7J6QIOq2jO2VnOqzvCDruYTsoJXsg4Hsg4Htmakg64yA7J2R7J2EIOyatOyg
hOygleuztCDqtIDrpqwg7LK06rOE66GcIOyXsOqysO2VnOuLpC4iLAogICAgIkhNSeuKlCDsmrTs
oITsnpDsmYAg7KCc7Ja07Iuc7Iqk7YWc7J2YIOyDge2YuOyekeyaqSDtmZTrqbTsnYQg7KCc6rO1
7ZWY6rOgLCBTQ0FEQeuKlCDsm5Dqsqkg6rCQ7IucwrfrjbDsnbTthLAg7IiY7KeRwrfrqoXroLnC
t+qyveuztMK37J2066ClIOq4sOuKpeydhCDshJzrsoQsIO2GteyLoOunnSwg7ZiE7J6lIOygnOyW
tOq4sOyZgCDsl7Dqs4TtlZjripQg7IOB7JyEIOqwkOyLnOyytOqzhOydtOuLpC4iLAogICAgIkhN
ScK3U0NBREEg6rWs7KGw64qUIOyEnOuyhOyZgCDrhKTtirjsm4ztgazsnZgg7J207KSR7ZmUIOyX
rOu2gOu/kCDslYTri4jrnbwg7Ya17IugIOuLqOygiCwgRmFpbG92ZXIsIOuNsOydtO2EsCDtkojs
p4gsIFN0YWxlIOyDge2DnCDrsI8g7J6s7Jew6rKwIO2bhCDrjbDsnbTthLAg7J287LmY7ISx7J2E
IOyatOyghOyekOyXkOqyjCDrqoXtmZXtnogg7KCE64us7ZW07JW8IO2VnOuLpC4iLAogICAgIkhp
Z2gtcGVyZm9ybWFuY2UgSE1J64qUIOygleyDgeyDge2DnOydmCDrtojtlYTsmpTtlZwg7J6l7Iud
7J2EIOykhOydtOqzoCDqs7XsoJXsg4Htg5wsIO2OuOywqCwg7LaU7IS47JmAIOu5hOygleyDgSDs
p5Xtm4Trpbwg67mg66W06rKMIOyduOyngO2VmOuPhOuhnSDsoJXrs7Qg67CA64+E7JmAIOyLnOqw
geyggSDsmrDshKDsiJzsnITrpbwg7ISk6rOE7ZWc64ukLiIsCiAgICAi7ZmU66m06rOE7Li17J2A
IOydvOuwmOyggeycvOuhnCBMZXZlbCAxIOqzteyglSDsoITssrQgT3ZlcnZpZXcsIExldmVsIDIg
VW5pdMK3QXJlYSwgTGV2ZWwgMyDsg4HshLgg7Jq07KCELCBMZXZlbCA0IOynhOuLqMK37KCV67mE
IOygleuztOuhnCDqtazshLHtlZjrqbAg7IOB7JyE7JeQ7IScIOydtOyDgSDsnITsuZjrpbwg7LC+
6rOgIO2VmOychOyXkOyEnCDsm5Dsnbjqs7wg7KGw7LmY66W8IO2ZleyduO2VmOuPhOuhnSDsl7Dq
srDtlZzri6QuIiwKICAgICLsg4nsg4HsnYAg7KCV7IOBIOyepeyLneuztOuLpCBBbGFybSwg67mE
7KCV7IOBLCDshKDtg53sg4Htg5zsmYAg7ZKI7KeI7KCA7ZWYIOuTsSDsoJztlZzrkJwg7J2Y66+4
7JeQIOydvOq0gOuQmOqyjCDsgqzsmqntlZjqs6AsIO2ZlOuptCDsnbTrj5kg7IucIOyEpOu5hCDs
nITsuZjCt+yatOyghOuqqOuTnMK37LaU7IS4wrfqtIDroKggQWxhcm3snZgg66el65297J20IOyc
oOyngOuQmOyWtOyVvCDtlZzri6QuIiwKICAgICJBbGFybeydgCDruYTsoJXsg4Eg7IOB7YOc66W8
IOyatOyghOyekOyXkOqyjCDslYzrpqzqs6Ag7KCV7ZW07KeEIOyLnOqwhCDslYjsl5Ag7YyQ64uo
IOuYkOuKlCDsobDsuZjrpbwg7JqU6rWs7ZWY64qUIOq4sOuKpeydtOupsCwg7KGw7LmY6rCAIO2V
hOyalO2VmOyngCDslYrsnYAg64uo7IicIEV2ZW50wrdTdGF0dXPCt05vdGlmaWNhdGlvbuqzvCDq
tazrtoTtlZzri6QuIiwKICAgICJBbGFybSBwaGlsb3NvcGh564qUIEFsYXJt7J2YIOuqqeyggSwg
7Jet7ZWgLCDsmrDshKDsiJzsnIQg6riw7KSALCDsg4Htg5ztkZztmIQsIOyKueyduOq2jO2VnCwg
U2hlbHZpbmfCt1N1cHByZXNzaW9uLCDshLHriqXsp4DtkZwsIOuzgOqyveq0gOumrOyZgCDso7zq
uLDsoIEg6rKA7YagIOybkOy5meydhCDsobDsp4Eg7LCo7JuQ7JeQ7IScIOygleydmO2VnCDsg4Hs
nIQg7KCV7LGF7J2064ukLiIsCiAgICAiQWxhcm0gcmF0aW9uYWxpemF0aW9u7J2AIOqwgSDtm4Tr
s7QgQWxhcm3sl5Ag64yA7ZW0IOybkOyduCwg6rKw6rO8LCDsmrTsoITsnpAg7KGw7LmYLCDtl4js
mqkg7J2R64u17Iuc6rCELCDsmrDshKDsiJzsnIQsIOyEpOygleqwkiwgRGVhZGJhbmQsIERlbGF5
LCBTaGVsdmluZyDtl4jsmqnsobDqsbTqs7wg66y47IScIOq3vOqxsOulvCDqsoDthqDtlZjsl6wg
7ZWE7JqU7ZWcIEFsYXJt66eMIOyKueyduO2VmOuKlCDtmZzrj5nsnbTri6QuIiwKICAgICJBbGFy
bSBwcmlvcml0eeuKlCDri6jsiJwg7Lih7KCV6rCSIO2BrOq4sOqwgCDslYTri4jrnbwg7KGw7LmY
7ZWY7KeAIOyViuyVmOydhCDrlYzsnZgg6rKw6rO8IOyLrOqwgeuPhOyZgCDsmrTsoITsnpDsl5Dq
sowg7ZeI7Jqp65CcIOydkeuLteyLnOqwhOydhCDtlajqu5gg7Y+J6rCA7ZWY7JesIOqysOygle2V
mOupsCwg7Jqw7ISg7Iic7JyE67OEIO2RnOyLnOyZgCDrjIDsnZHsoIjssKjqsIAg7J286rSA65CY
7Ja07JW8IO2VnOuLpC4iLAogICAgIkFsYXJt7J2YIFByb2Nlc3MgY29uZGl0aW9uLCBBY3RpdmXC
t1JldHVybi10by1ub3JtYWwg7IOB7YOc7JmAIEFja25vd2xlZGdlbWVudCDsg4Htg5zripQg67OE
6rCc7J2066mwLCDsmrTsoITsnpAgQWNrbm93bGVkZ2XripQg7J247KeAIOq4sOuhneydvCDrv5Ag
7JuQ7J24IOygnOqxsCDrmJDripQgQWxhcm0g7KGw6rG0IO2VtOygnOulvCDsnZjrr7jtlZjsp4Ag
7JWK64qU64ukLiIsCiAgICAiRGVhZGJhbmTripQgQWxhcm3snbQg67Cc7IOd7ZWcIOuSpCDsoJXs
g4Eg67O16reAIOyehOqzhOqwkuydhCDrsJzsg50g7J6E6rOE6rCS6rO8IOuLpOultOqyjCDrkZDr
ipQg6rCS7J2YIOydtOugpe2PreycvOuhnCwg6rK96rOEIOu2gOq3vCDrhbjsnbTspojsl5Ag7J2Y
7ZWcIOuwmOuztSDrsJzsg53qs7wg7ZW07KCc66W8IOykhOyduOuLpC4iLAogICAgIkFsYXJtIGRl
bGF564qUIOyhsOqxtOydtCDsnbzsoJUg7Iuc6rCEIOyXsOyGjSDsnKDsp4DrkKAg65WMIOuwnOyD
neyLnO2CpOqxsOuCmCDsoJXsg4Hsg4Htg5zqsIAg7J287KCVIOyLnOqwhCDsnKDsp4DrkKAg65WM
IO2VtOygnO2VmOuKlCDsi5zqsIQg7ZWE7YSw7J2066mwLCDsi6TsoJzroZwg7ZWE7JqU7ZWcIOyn
p+ydgCDsnZHri7XsnYQg6rCA66as7KeAIOyViuuPhOuhnSDqs7XsoJUg64+Z7Yq57ISx6rO8IO2X
iOyaqSDsnZHri7Xsi5zqsITsnYQg6rOg66Ck7ZWc64ukLiIsCiAgICAiU2hlbHZpbmfsnYAg6raM
7ZWcIOyeiOuKlCDsmrTsoITsnpDqsIAg7JWM66Ck7KeEIOyCrOycoOuhnCDtirnsoJUgQWxhcm3s
nYQg7KCc7ZWc7Iuc6rCEIOuPmeyViCBBY3RpdmUgZGlzcGxheeyXkOyEnCDsnoTsi5zroZwg7Iio
6riw64qUIOyatOyghO2WieychOydtOupsCwgQWxhcm0g7KCV7J2Y7JmAIOydtOugpeydgCDsnKDs
p4DtlZjqs6Ag7IKs7JygwrfsgqzsmqnsnpDCt+yLnOyekcK366eM66OM66W8IOq4sOuhne2VnOuL
pC4iLAogICAgIlN1cHByZXNzaW9u7J2AIOyEpOu5hOyDge2DnCwg7Jq07KCE66qo65OcIOuYkOuK
lCDrhbzrpqzsobDqsbTsg4Eg7J2Y66+46rCAIOyXhuuKlCBBbGFybeydhCDshKTqs4TrkJwg7KGw
6rG07JeQIOuUsOudvCDsnpDrj5nsnLzroZwg67Cc7IOd7ZWY7KeAIOyViuqyjCDtlZjqsbDrgpgg
7ZGc7Iuc64yA7IOB7JeQ7IScIOygnOyZuO2VmOuKlCDquLDriqXsnbTrqbAsIOyatOyghOyekCDs
noTsnZggU2hlbHZpbmfqs7wg6rWs67aE7ZWc64ukLiIsCiAgICAiQWxhcm0gZmxvb2TripQg7Ken
7J2AIOyLnOqwhOyXkCDrp47snYAgQWxhcm3snbQg7KeR7KSR65CY7Ja0IOyatOyghOyekOydmCDs
nbjsp4DCt+ynhOuLqMK37KGw7LmY66W8IOuwqe2VtO2VmOuKlCDsg4Htg5zsnbTqs6AsIENoYXR0
ZXJpbmfsnYAg6rCZ7J2AIEFsYXJt7J20IOuwmOuztSDrsJzsg53Ct+2VtOygnOuQmOuKlCDtmITs
g4HsnbTrr4DroZwg7JuQ7J24IOygnOqxsCwg7ZWp66as7ZmULCBEZWFkYmFuZMK3RGVsYXnsmYAg
7IOB7YOc6riw67CYIFN1cHByZXNzaW9u7Jy866GcIOqwnOyEoO2VnOuLpC4iLAogICAgIkFsYXJt
IOyEseuKpeydgCDsi5zqsITri7kg67Cc7IOd66WgLCBQZWFrIGFsYXJtIHJhdGUsIFN0YW5kaW5n
IGFsYXJtLCBDaGF0dGVyaW5nIGFsYXJtLCBGbG9vZCDqtazqsIQsIOyasOyEoOyInOychCDrtoTt
j6zsmYAgU2hlbHZpbmcg7IKs7Jqp7J2EIO2YhOyepSDquLDspIDsnLzroZwg7LaU7KCB7ZWY6rOg
IOuwmOuztSDsm5DsnbjsnYQg6rCc7ISg7ZW07JW8IO2VnOuLpC4iLAogICAgIuyatOyghCBTZXRw
b2ludCwgQWxhcm0gdmFsdWUsIFRyaXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl64qUIOuqqeyg
geqzvCDshozsnKDqtozsnbQg64uk66W066mwLCBBbGFybeydgCDsmrTsoITsnpAg7KGw7LmY66W8
IOy0ieq1rO2VmOqzoCBUcmlwwrdJbnRlcmxvY2vsnYAg7J6Q64+ZIOuztO2YuCDrmJDripQg64+Z
7J6R7KCc7JW97JeQIOyCrOyaqeuQmOuvgOuhnCDqsJnsnYAg6rCS7Jy866GcIOyehOydmCDthrXt
lantlZjsp4Ag7JWK64qU64ukLiIsCiAgICAiU2V0cG9pbnQgbGlzdOuKlCBUYWcsIOq4sOuKpSwg
6rCSLCDri6jsnIQsIOuwqe2WpSwgRGVhZGJhbmTCt0RlbGF5LCDsoIHsmqnrqqjrk5wsIOq3vOqx
sCwg7Iq57J247J6QLCDrs4Dqsr3snbTroKXqs7wg6rSA66CoIFRyaXDCt0ludGVybG9jayDssLjs
obDrpbwg6rSA66as7ZWY6rOgIOyYqOudvOyduCDrs4Dqsr3snYAg6raM7ZWcwrfqsoDthqDCt+q4
sOuhncK367O16rWs7KCI7LCo66W8IOqxsOyzkOyVvCDtlZzri6QuIiwKICAgICJBbGFybeydgCDs
mrTsoITsnpAg7YyQ64uo6rO8IOyhsOy5mOulvCDsp4Dsm5DtlZjripQg7KCV67O0IOq4sOuKpeyd
tOqzoCBUcmlw7J2AIOuztO2YuOyhsOqxtOyXkCDrlLDrpbgg7J6Q64+ZIOygleyngCwgSW50ZXJs
b2Nr7J2AIOychO2XmO2VmOqxsOuCmCDtl4jsmqnrkJjsp4Ag7JWK7J2AIOuPmeyekeydhCDquIjs
p4DCt+qwleygnO2VmOuKlCDrhbzrpqzsnbTrr4DroZwg7ZGc7Iuc7KCV67O07JmAIOyLpO2WieuF
vOumrOulvCDqtazrtoTtlZzri6QuIiwKICAgICJTT0XripQg7KCR7KCQwrfsg4Htg5zCt+uqheug
ucK367O07Zi464+Z7J6RIOuTseydmCDrs4DtmZQg7Iuc6rCBLCDsi6DtmLjsm5AsIOydtOyghOqw
ksK37IOI6rCS6rO8IO2SiOyniOydhCDqs7XthrUg7Iuc6rCE7LaV7JeQIOqzoO2VtOyDgeuPhOuh
nCDquLDroZ3tlZjsl6wg7IKs6rG07J2YIOyEoO2bhOq0gOqzhOyZgCDsm5DsnbjsoITtjIzrpbwg
67aE7ISd7ZWY64qUIOq4sOuKpeydtOuLpC4iLAogICAgIlNPReydmCDsnbjqs7zsiJzshJzrpbwg
7Iug66Kw7ZWY66Ck66m0IFBMQ8K3RENTwrdTQ0FEQcK367O07Zi47J6l7LmY7J2YIOyLnOqzhOul
vCDrj5nquLDtmZTtlZjqs6AgU291cmNlIHRpbWVzdGFtcCwg7Iuc6rCE7KCV7ZmV64+ELCDrtoTt
lbTriqUsIO2GteyLoOyngOyXsOqzvCBUaW1lIHF1YWxpdHnrpbwg7ZWo6ruYIOq0gOumrO2VtOyV
vCDtlZzri6QuIiwKICAgICJIaXN0b3JpYW7snYAg7KO86riwIOuYkOuKlCDrs4DtmZTquLDrsJjs
nLzroZwg6rO17KCV6rCSIOy2lOyEuOulvCDsnqXquLAg7KCA7J6l7ZWY64qUIOq4sOuKpeydtCDs
pJHsi6zsnbTqs6AgU09F64qUIOydtOyCsCDsnbTrsqTtirjsnZgg7KCV7ZmV7ZWcIOuwnOyDneyI
nOyEnOulvCDrtoTshJ3tlZjripQg6riw64ql7J20IOykkeyLrOydtOuvgOuhnCDtkZzrs7jso7zq
uLDsmYAgVGltZXN0YW1wIOy2nOyymOulvCDqtazrtoTtlZzri6QuIiwKICAgICJGaXJzdC1vdXTs
nYAg7ZWcIOyXsOyHhOyCrOqxtOyXkOyEnCDstZzstIjroZwg7Jyg7Zqo7ZW07KeEIOybkOyduOyd
hCBMYXRjaO2VmOyXrCDrs7TsobTtlZjripQg64W866as7J206rOgIFNPReuKlCDsoITssrQg7J20
67Kk7Yq4IOyInOyEnOulvCDquLDroZ3tlZjrr4DroZwsIEZpcnN0LW91dOydgCDruaDrpbgg7JuQ
7J247KeA7Iuc66W8IOygnOqzte2VmOqzoCBTT0XripQg7IOB7IS4IOqygOymneydhCDrs7TsmYTt
lZzri6QuIiwKICAgICJBdWRpdCB0cmFpbOydgCDsgqzsmqnsnpDqsIAg7IiY7ZaJ7ZWcIEFja25v
d2xlZGdlLCBTaGVsdmluZywgU3VwcHJlc3Npb24g7Iq57J24LCBTZXRwb2ludCDrs4Dqsr0sIExv
Z2luwrdMb2dvdXTqs7wg7ZmU66m0IOuqheugueyXkCDrjIDtlbQg7IKs7Jqp7J6QLCDsi5zqsIEs
IOuMgOyDgSwg7J207KCE6rCSwrfsg4jqsJIsIOyCrOycoOyZgCDqsrDqs7zrpbwg6riw66Gd7ZWc
64ukLiIsCiAgICAi7Jq07KCE7J6QIOq2jO2VnOydgCDsl63tlaDquLDrsJgg7LWc7IaM6raM7ZWc
LCDshKTruYTCt+q4sOuKpcK37Jq07KCE66qo65Oc67OEIOuylOychCwg7KSR7JqU7KGw7J6R7J2Y
IOyerO2ZleyduCDrmJDripQg7J207KSR7Iq57J24LCDshLjshZjqtIDrpqzsmYAgQXVkaXQgdHJh
aWzsnYQg7Ya17ZW0IO2GteygnO2VnOuLpC4iLAogICAgIkh1bWFuIGVycm9yIOuwqeyngOuKlCDt
mITsnqwgTW9kZcK37IaM7Jyg6raMwrdJbnRlcmxvY2sg7IKs7JygwrfrqoXroLnrjIDsg4HCt+yY
iOyDgeqysOqzvOulvCDrqoXtmZXtnogg7ZGc7Iuc7ZWY6rOgLCDspJHsmpTsobDsnpEg7ZmV7J24
LCDsnpjrqrvrkJwg64yA7IOBIOyEoO2DnSDrsKnsp4AsIENvbW1hbmTsmYAgRmVlZGJhY2sg67aE
66asLCDst6jshozCt+uzteq1rCDqsr3roZzrpbwg7KCc6rO17ZWY64qUIOuwqeyLneycvOuhnCDq
taztmITtlZzri6QuIiwKICAgICJCYWQsIFVuY2VydGFpbiwgU3RhbGUsIENvbW11bmljYXRpb24g
bG9zdOyZgCBNYW51YWwgc3Vic3RpdHV0aW9uIOqwmeydgCDrjbDsnbTthLAg7ZKI7KeI7J2AIOqw
kiDsnpDssrTsmYAg67OE64+EIOyDge2DnOuhnCDtkZzsi5ztlZjqs6AsIO2SiOyniOydtCDrgpjs
gZwg6rCS7J2EIOygleyDgSDstZzsi6DqsJLsspjrn7wg7KCc7Ja07YyQ64uo7J2064KYIOyatOyg
hOyekCDtjJDri6jsl5Ag7IKs7Jqp7ZWY7KeAIOyViuuPhOuhnSDtlZzri6QuIiwKICAgICJBYm5v
cm1hbCBzaXR1YXRpb24gbWFuYWdlbWVudOuKlCBPdmVydmlld+yXkOyEnCDsnbTsg4Eg7KeV7ZuE
66W8IOyhsOq4sOyXkCDrsJzqsqztlZjqs6AgQWxhcm3qs7wgVHJlbmTroZwg7KeE64uo7ZWY66mw
IOygiOywqOyZgCDqtoztlZzsl5Ag65Sw6528IOuMgOydke2VnCDrkqQg7KCV7IOB67O16rWs7JmA
IOyCrO2bhOu2hOyEneycvOuhnCDsnbTslrTsp4DripQgRGV0ZWN0LURpYWdub3NlLVJlc3BvbmQt
UmVjb3ZlciDtnZDrpoTsnbTri6QuIiwKICAgICJTVy0wM+uKlCBBbGFybcK3U2V0cG9pbnTCt1NP
RcK37ZmU66m0wrfqtoztlZwg65OxIOyatOyghOyekCDsoJXrs7TsmYAg6rSA66as7KCV7LGF7J2E
IOyGjOycoO2VmOqzoCwgSW50ZXJsb2NrwrdUcmlw7J2YIOyLpOygnCDrhbzrpqzqtazsobAsIOyD
ge2DnOyghOydtCwgTGF0Y2jCt1Jlc2V0IOuwjyBGYWlsLXNhZmUg64+Z7J6R7J2AIFNXLTAy66Gc
IOuEmOq4tOuLpC4iLAogICAgIlNXLTAz64qUIOyatOyghOygleuztOydmCDrgrTsmqnqs7wg7Jq0
7JiB6rSA66asIOybkOy5meydhCDshozsnKDtlZjqs6AsIOydvOuwmCDshoztlITtirjsm6jslrQg
Vi1Nb2RlbMK37LaU7KCB7ISxwrfsi5ztl5jssrTqs4TripQgU1ctMDQsIO2UhOuhnOygne2KuCDr
rLjshJwg7J2464+EwrdGQVTCt1NBVMK37Iuc7Jq07KCEIOygiOywqOuKlCBTVy0xMOycvOuhnCDr
hJjquLTri6QuIgogIF0KfQo=
PAYLOAD_SW03_03

    write_payload 'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/logic_check.json' 'ea925b4121be491825e1b041efa5f02405cb682e5a72e53267a922765b83e2c7' <<'PAYLOAD_SW03_04'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLmxvZ2ljX2NoZWNrLnYxIiwKICAidG9w
aWNfaWQiOiAiaG1pX3NjYWRhX2FsYXJtX3NldHBvaW50X3RyaXBfaW50ZXJsb2NrX3NvZV9vcGVy
YXRvcl9pbmZvcm1hdGlvbl9tYW5hZ2VtZW50IiwKICAidGl0bGUiOiAiSE1JwrdTQ0FEQcK3QWxh
cm3Ct1NldHBvaW50wrdUcmlwwrdJbnRlcmxvY2vCt1NPRSDrsI8g7Jq07KCE7KCV67O0IOq0gOum
rCIsCiAgImRldGVybWluaXN0aWNfY2hlY2tzIjogewogICAgImVuYWJsZWQiOiB0cnVlLAogICAg
InRvcGljX25hbWUiOiAiSE1JwrdTQ0FEQcK3QWxhcm3Ct1NldHBvaW50wrdUcmlwwrdJbnRlcmxv
Y2vCt1NPRSDrsI8g7Jq07KCE7KCV67O0IOq0gOumrCIsCiAgICAicXVlc3Rpb25fdHlwZSI6ICJQ
UklOQ0lQTEVfSU5URVJQUkVUQVRJT04iLAogICAgImRpZmZpY3VsdHlfcHJvZmlsZSI6ICJERVNJ
R05fRVZBTFVBVElPTiIsCiAgICAidG9waWNfYWxpYXNlcyI6IFsKICAgICAgIkhNSSBTQ0FEQSBh
bGFybSBtYW5hZ2VtZW50IFNPRSIsCiAgICAgICLqs6DshLHriqUgSE1JIOqyveuztCDtlanrpqzt
mZQgU09FIiwKICAgICAgIkhNSSBTQ0FEQSBBbGFybSBTZXRwb2ludCBUcmlwIEludGVybG9jayIs
CiAgICAgICLsmrTsoITsoJXrs7Qg6rK967O0IOyEpOygleqwkiDsnbTrsqTtirjsiJzshJwiLAog
ICAgICAiYWxhcm0gcGhpbG9zb3BoeSByYXRpb25hbGl6YXRpb24gcHJpb3JpdHkiLAogICAgICAi
6rK967O0IOyyoO2VmSDtlanrpqztmZQg7Jqw7ISg7Iic7JyEIiwKICAgICAgImFsYXJtIGRlYWRi
YW5kIGRlbGF5IHNoZWx2aW5nIHN1cHByZXNzaW9uIiwKICAgICAgIuqyveuztCDrjbDrk5zrsLTr
k5wg7KeA7JewIOyJmOu5mSDslrXsoJwiLAogICAgICAic2V0cG9pbnQgYWxhcm0gdHJpcCBpbnRl
cmxvY2sgdmFsdWUgbWFuYWdlbWVudCIsCiAgICAgICLshKTsoJXqsJIg6rK967O06rCSIO2KuOum
veqwkiDsnbjthLDroZ3qsJIg6rSA66asIiwKICAgICAgInNlcXVlbmNlIG9mIGV2ZW50cyBhdWRp
dCB0cmFpbCB0aW1lIHN5bmNocm9uaXphdGlvbiIsCiAgICAgICJTT0Ug6rCQ7IKs7LaU7KCBIOyL
nOqwgeuPmeq4sCIsCiAgICAgICJoaWdoIHBlcmZvcm1hbmNlIEhNSSBkaXNwbGF5IGhpZXJhcmNo
eSIsCiAgICAgICLqs6DshLHriqUgSE1JIO2ZlOuptOqzhOy4tSDsg4Htmansnbjsi50iLAogICAg
ICAib3BlcmF0b3IgYXV0aG9yaXR5IGh1bWFuIGVycm9yIHByZXZlbnRpb24iLAogICAgICAi7Jq0
7KCE7J6QIOq2jO2VnCDtnLTrqLzsl5Drn6wg67Cp7KeAIiwKICAgICAgImFsYXJtIGZsb29kIGNo
YXR0ZXJpbmcgc3RhbmRpbmcgYWxhcm0iLAogICAgICAi6rK967O07Y+t7KO8IOyxhO2EsOungSDs
g4Hsi5zqsr3rs7QiLAogICAgICAiYWJub3JtYWwgc2l0dWF0aW9uIG1hbmFnZW1lbnQgSE1JIGFs
YXJtIiwKICAgICAgIuu5hOygleyDgeyDge2ZqSDqtIDrpqwgU0NBREEg7Jq07KCE7KCV67O0Igog
ICAgXSwKICAgICJmYXRhbF9jaGVja3MiOiBbCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19m
YXRhbF9hbGxfZXZlbnRzX2FyZV9hbGFybXMiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIs
CiAgICAgICAgIm1lc3NhZ2UiOiAi66qo65OgIEV2ZW507JmAIFN0YXR1c+uKlCBBbGFybeycvOuh
nCDrp4zrk6TslrTslbwg7ZWc64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyg
gSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIEFsYXJt7J2AIOygle2V
tOynhCDsi5zqsIQg7JWI7JeQIOyatOyghOyekCDsobDsuZjqsIAg7ZWE7JqU7ZWcIOu5hOygleyD
gSDsg4Htg5zrp4wg64yA7IOB7Jy866GcIO2VmOupsCDri6jsiJwgRXZlbnTCt1N0YXR1c+yZgCDq
tazrtoTtlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkFsYXJt7J2AIOygle2VtOyn
hCDsi5zqsIQg7JWI7JeQIOyatOyghOyekCDsobDsuZjqsIAg7ZWE7JqU7ZWcIOu5hOygleyDgSDs
g4Htg5zrp4wg64yA7IOB7Jy866GcIO2VmOupsCDri6jsiJwgRXZlbnTCt1N0YXR1c+yZgCDqtazr
toTtlZzri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAsCiAgICAgICAg
Indyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/
66qo65OgXFwgRXZlbnTsmYBcXCBTdGF0dXPripRcXCBBbGFybeycvOuhnFxcIOunjOuTpOyWtOyV
vFxcIO2VnOuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAgICAgImV4YW1wbGVz
X29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIuuqqOuToCBFdmVudOyZgCBTdGF0dXPripQgQWxh
cm3snLzroZwg66eM65Ok7Ja07JW8IO2VnOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiYWZmZWN0
ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAg
ICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfYWxhcm1fZXF1YWxzX3RyaXBf
aW50ZXJsb2NrIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdl
IjogIkFsYXJtLCBUcmlw6rO8IEludGVybG9ja+ydgCDqsJnsnYAg6riw64ql7J2064ukLiIsCiAg
ICAgICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2b
hOuztOuhnCDrs7jri6QuIEFsYXJt7J2AIOyatOyghOyekCDsobDsuZjrpbwg7KeA7JuQ7ZWY64qU
IOygleuztCDquLDriqXsnbTqs6AgVHJpcMK3SW50ZXJsb2Nr7J2AIOyekOuPmSDrs7TtmLgg65iQ
64qUIOuPmeyekeygnOyVvSDrhbzrpqzsnbTri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjog
IkFsYXJt7J2AIOyatOyghOyekCDsobDsuZjrpbwg7KeA7JuQ7ZWY64qUIOygleuztCDquLDriqXs
nbTqs6AgVHJpcMK3SW50ZXJsb2Nr7J2AIOyekOuPmSDrs7TtmLgg65iQ64qUIOuPmeyekeygnOyV
vSDrhbzrpqzsnbTri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAsCiAg
ICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJd
XFxzKik/QWxhcm0sXFwgVHJpcOqzvFxcIEludGVybG9ja+ydgFxcIOqwmeydgFxcIOq4sOuKpeyd
tOuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAgICAgImV4YW1wbGVzX29yX3Bh
dHRlcm5zIjogWwogICAgICAgICAgIkFsYXJtLCBUcmlw6rO8IEludGVybG9ja+ydgCDqsJnsnYAg
6riw64ql7J2064ukLiIKICAgICAgICBdLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAg
ICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAg
ICAgICAiaWQiOiAic3cwM19mYXRhbF9hY2tfY2xlYXJzX2NvbmRpdGlvbiIsCiAgICAgICAgInNl
dmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICJBbGFybeydhCBBY2tub3dsZWRn
Ze2VmOuptCDqs7XsoJUg7JuQ7J246rO8IEFsYXJtIOyhsOqxtOydtCDtlbTsoJzrkJzri6QuIiwK
ICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg
7ZuE67O066GcIOuzuOuLpC4gQWNrbm93bGVkZ2XripQg7Jq07KCE7J6QIOyduOyngCDquLDroZ3s
nbTrqbAgUHJvY2VzcyBjb25kaXRpb27qs7wgQWN0aXZlIOyDge2DnOulvCDtlbTsoJztlZjsp4Ag
7JWK64qU64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBY2tub3dsZWRnZeuKlCDsmrTs
oITsnpAg7J247KeAIOq4sOuhneydtOupsCBQcm9jZXNzIGNvbmRpdGlvbuqzvCBBY3RpdmUg7IOB
7YOc66W8IO2VtOygnO2VmOyngCDslYrripTri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2Vp
bGluZyI6IDE1LjAsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0p
XlxccyooPzpbLSrigKJdXFxzKik/QWxhcm3snYRcXCBBY2tub3dsZWRnZe2VmOuptFxcIOqzteyg
lVxcIOybkOyduOqzvFxcIEFsYXJtXFwg7KGw6rG07J20XFwg7ZW07KCc65Cc64ukXFwuXFxzKlsu
IV0/XFxzKiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAg
ICAgICAgICAiQWxhcm3snYQgQWNrbm93bGVkZ2XtlZjrqbQg6rO17KCVIOybkOyduOqzvCBBbGFy
bSDsobDqsbTsnbQg7ZW07KCc65Cc64ukLiIKICAgICAgICBdLAogICAgICAgICJhZmZlY3RlZF9s
YXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0s
CiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9wcmlvcml0eV9ieV9wdl9vbmx5IiwK
ICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIkFsYXJtIOya
sOyEoOyInOychOuKlCDsuKHsoJXqsJLsnZgg7YGs6riw66eM7Jy866GcIOygle2VnOuLpC4iLAog
ICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDt
m4Trs7TroZwg67O464ukLiBBbGFybSDsmrDshKDsiJzsnITripQg6rKw6rO8IOyLrOqwgeuPhOyZ
gCDtl4jsmqkg7J2R64u17Iuc6rCE7J2EIO2VqOq7mCDtj4nqsIDtlZjsl6wg7KCV7ZWc64ukLiIs
CiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBbGFybSDsmrDshKDsiJzsnITripQg6rKw6rO8IOyL
rOqwgeuPhOyZgCDtl4jsmqkg7J2R64u17Iuc6rCE7J2EIO2VqOq7mCDtj4nqsIDtlZjsl6wg7KCV
7ZWc64ukLiIsCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wLAogICAgICAgICJ3
cm9uZ19wYXR0ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCiXVxccyopP0Fs
YXJtXFwg7Jqw7ISg7Iic7JyE64qUXFwg7Lih7KCV6rCS7J2YXFwg7YGs6riw66eM7Jy866GcXFwg
7KCV7ZWc64ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBsZXNf
b3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAiQWxhcm0g7Jqw7ISg7Iic7JyE64qUIOy4oeygleqw
kuydmCDtgazquLDrp4zsnLzroZwg7KCV7ZWc64ukLiIKICAgICAgICBdLAogICAgICAgICJhZmZl
Y3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAg
ICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9kZWFkYmFuZF9lcXVhbHNf
ZGVsYXkiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1lc3NhZ2UiOiAi
QWxhcm0gRGVhZGJhbmTsmYAgRGVsYXnripQg6rCZ7J2AIOq4sOuKpeydtOuLpC4iLAogICAgICAg
ICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7Tr
oZwg67O464ukLiBEZWFkYmFuZOuKlCDqsJLsnZgg67O16reAIOydtOugpe2PreydtOqzoCBEZWxh
eeuKlCDsobDqsbQg7KeA7IaN7Iuc6rCE7J2EIOydtOyaqe2VmOuKlCDsi5zqsIQg7ZWE7YSw7J20
64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJEZWFkYmFuZOuKlCDqsJLsnZgg67O16reA
IOydtOugpe2PreydtOqzoCBEZWxheeuKlCDsobDqsbQg7KeA7IaN7Iuc6rCE7J2EIOydtOyaqe2V
mOuKlCDsi5zqsIQg7ZWE7YSw7J2064ukLiIsCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmci
OiAxNS4wLAogICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5cXHMq
KD86Wy0q4oCiXVxccyopP0FsYXJtXFwgRGVhZGJhbmTsmYBcXCBEZWxheeuKlFxcIOqwmeydgFxc
IOq4sOuKpeydtOuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAgICAgImV4YW1w
bGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIkFsYXJtIERlYWRiYW5k7JmAIERlbGF564qU
IOqwmeydgCDquLDriqXsnbTri6QuIgogICAgICAgIF0sCiAgICAgICAgImFmZmVjdGVkX2xheWVy
cyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAg
ICAgewogICAgICAgICJpZCI6ICJzdzAzX2ZhdGFsX3NoZWx2aW5nX2RlbGV0ZXNfaGlzdG9yeSIs
CiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICJTaGVsdmlu
Z+2VmOuptCBBbGFybSDsoJXsnZjsmYAg7J2066Cl7J20IOyCreygnOuQnOuLpC4iLAogICAgICAg
ICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7Tr
oZwg67O464ukLiBTaGVsdmluZ+ydgCDsoJztlZzsi5zqsIQg64+Z7JWIIEFjdGl2ZSBkaXNwbGF5
7JeQ7IScIOyehOyLnOuhnCDsiKjquLDripQg6riw64ql7J2066mwIOygleydmOyZgCDsnbTroKXs
nYAg7Jyg7KeA7ZWc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTaGVsdmluZ+ydgCDs
oJztlZzsi5zqsIQg64+Z7JWIIEFjdGl2ZSBkaXNwbGF57JeQ7IScIOyehOyLnOuhnCDsiKjquLDr
ipQg6riw64ql7J2066mwIOygleydmOyZgCDsnbTroKXsnYAg7Jyg7KeA7ZWc64ukLiIsCiAgICAg
ICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wLAogICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6
IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCiXVxccyopP1NoZWx2aW5n7ZWY66m0XFwg
QWxhcm1cXCDsoJXsnZjsmYBcXCDsnbTroKXsnbRcXCDsgq3soJzrkJzri6RcXC5cXHMqWy4hXT9c
XHMqJCIKICAgICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAg
ICAgICJTaGVsdmluZ+2VmOuptCBBbGFybSDsoJXsnZjsmYAg7J2066Cl7J20IOyCreygnOuQnOuL
pC4iCiAgICAgICAgXSwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMi
LAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjog
InN3MDNfZmF0YWxfc3VwcHJlc3Npb25fZXF1YWxzX3NoZWx2aW5nIiwKICAgICAgICAic2V2ZXJp
dHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIlN1cHByZXNzaW9u6rO8IFNoZWx2aW5n
7J2AIOyatOyghOyekOqwgCDsnoTsnZjroZwgQWxhcm3snYQg7Iio6riw64qUIOuPmeydvCDquLDr
iqXsnbTri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zs
nqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gU3VwcHJlc3Npb27snYAg7ISk6rOE65CcIOyD
ge2DnMK364W866as7KGw6rG07JeQIOuUsOuluCDsnpDrj5kg7KCc7Jm47J206rOgIFNoZWx2aW5n
7J2AIOq2jO2VnCDsnojripQg7Jq07KCE7J6Q7J2YIOygnO2VnOyLnOqwhCDsnoTsi5wg7KGw7LmY
7J2064ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTdXBwcmVzc2lvbuydgCDshKTqs4Tr
kJwg7IOB7YOcwrfrhbzrpqzsobDqsbTsl5Ag65Sw66W4IOyekOuPmSDsoJzsmbjsnbTqs6AgU2hl
bHZpbmfsnYAg6raM7ZWcIOyeiOuKlCDsmrTsoITsnpDsnZgg7KCc7ZWc7Iuc6rCEIOyehOyLnCDs
obDsuZjsnbTri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAsCiAgICAg
ICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxz
Kik/U3VwcHJlc3Npb27qs7xcXCBTaGVsdmluZ+ydgFxcIOyatOyghOyekOqwgFxcIOyehOydmOuh
nFxcIEFsYXJt7J2EXFwg7Iio6riw64qUXFwg64+Z7J28XFwg6riw64ql7J2064ukXFwuXFxzKlsu
IV0/XFxzKiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAg
ICAgICAgICAiU3VwcHJlc3Npb27qs7wgU2hlbHZpbmfsnYAg7Jq07KCE7J6Q6rCAIOyehOydmOuh
nCBBbGFybeydhCDsiKjquLDripQg64+Z7J28IOq4sOuKpeydtOuLpC4iCiAgICAgICAgXSwKICAg
ICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAg
ICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfaW5kZWZp
bml0ZV9zaGVsdmluZyIsCiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVz
c2FnZSI6ICJBbGFybSBTaGVsdmluZ+ydgCDsgqzsnKDsmYAg66eM66OM7Iuc6rCEIOyXhuydtCDr
rLTquLDtlZwg7Jyg7KeA7ZW064+EIOuQnOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLr
qoXsi5zsoIEg67CY64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBTaGVsdmlu
Z+ydgCDsirnsnbjqtoztlZwsIOyCrOycoCwg7KCc7ZWc7Iuc6rCELCDtkZzsi5wsIOunjOujjOyZ
gCDrs7XqtaztmZXsnbjsnYQg6rSA66as7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJjb3JyZWN0
X3J1bGUiOiAiU2hlbHZpbmfsnYAg7Iq57J246raM7ZWcLCDsgqzsnKAsIOygnO2VnOyLnOqwhCwg
7ZGc7IucLCDrp4zro4zsmYAg67O16rWs7ZmV7J247J2EIOq0gOumrO2VtOyVvCDtlZzri6QuIiwK
ICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAsCiAgICAgICAgIndyb25nX3BhdHRl
cm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpbLSrigKJdXFxzKik/QWxhcm1cXCBTaGVs
dmluZ+ydgFxcIOyCrOycoOyZgFxcIOunjOujjOyLnOqwhFxcIOyXhuydtFxcIOustOq4sO2VnFxc
IOycoOyngO2VtOuPhFxcIOuQnOuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAg
ICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIkFsYXJtIFNoZWx2aW5n7J2A
IOyCrOycoOyZgCDrp4zro4zsi5zqsIQg7JeG7J20IOustOq4sO2VnCDsnKDsp4DtlbTrj4Qg65Cc
64ukLiIKICAgICAgICBdLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAi
QyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQi
OiAic3cwM19mYXRhbF92YWx1ZXNfaW50ZXJjaGFuZ2VhYmxlIiwKICAgICAgICAic2V2ZXJpdHki
OiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIuyatOyghCBTZXRwb2ludCwgQWxhcm0gdmFs
dWUsIFRyaXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl64qUIOyEnOuhnCDrsJTqvrjslrQg7IKs
7Jqp7ZW064+EIOuQnOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY
64yAIOyjvOyepeunjCBmYXRhbCDtm4Trs7TroZwg67O464ukLiDrhKQg6rCS7J2AIOuqqeyggeqz
vCDshozsnKDqtozsnbQg64uk66W066+A66GcIOq3vOqxsOyZgCDrs4Dqsr3qtIDrpqzrpbwg67aE
66as7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi64SkIOqwkuydgCDr
qqnsoIHqs7wg7IaM7Jyg6raM7J20IOuLpOultOuvgOuhnCDqt7zqsbDsmYAg67OA6rK96rSA66as
66W8IOu2hOumrO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6
IDE1LjAsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyoo
PzpbLSrigKJdXFxzKik/7Jq07KCEXFwgU2V0cG9pbnQsXFwgQWxhcm1cXCB2YWx1ZSxcXCBUcmlw
XFwgdmFsdWXsmYBcXCBJbnRlcmxvY2tcXCB2YWx1ZeuKlFxcIOyEnOuhnFxcIOuwlOq+uOyWtFxc
IOyCrOyaqe2VtOuPhFxcIOuQnOuLpFxcLlxccypbLiFdP1xccyokIgogICAgICAgIF0sCiAgICAg
ICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIuyatOyghCBTZXRwb2ludCwg
QWxhcm0gdmFsdWUsIFRyaXAgdmFsdWXsmYAgSW50ZXJsb2NrIHZhbHVl64qUIOyEnOuhnCDrsJTq
vrjslrQg7IKs7Jqp7ZW064+EIOuQnOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiYWZmZWN0ZWRf
bGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9
LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfc29lX3dpdGhvdXRfc3luYyIsCiAg
ICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAibWVzc2FnZSI6ICLsi5zqsIHrj5nq
uLDqsIAg7JeG7Ja064+EIFNPReydmCDsnbTrsqTtirgg7ISg7ZuE6rSA6rOE64qUIO2VreyDgSDs
oJXtmZXtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDs
o7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4gU09F7J2YIOyduOqzvOyInOyEnOulvCDs
i6DrorDtlZjroKTrqbQg6rO17Ya1IOyLnOqwhOuPmeq4sCwgVGltZXN0YW1wIOy2nOyymCwg7KCV
7ZmV64+E7JmAIFRpbWUgcXVhbGl0eeqwgCDtlYTsmpTtlZjri6QuIiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIlNPReydmCDsnbjqs7zsiJzshJzrpbwg7Iug66Kw7ZWY66Ck66m0IOqzte2GtSDs
i5zqsITrj5nquLAsIFRpbWVzdGFtcCDstpzsspgsIOygle2ZleuPhOyZgCBUaW1lIHF1YWxpdHnq
sIAg7ZWE7JqU7ZWY64ukLiIsCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wLAog
ICAgICAgICJ3cm9uZ19wYXR0ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCi
XVxccyopP+yLnOqwgeuPmeq4sOqwgFxcIOyXhuyWtOuPhFxcIFNPReydmFxcIOydtOuypO2KuFxc
IOyEoO2bhOq0gOqzhOuKlFxcIO2VreyDgVxcIOygle2Zle2VmOuLpFxcLlxccypbLiFdP1xccyok
IgogICAgICAgIF0sCiAgICAgICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAg
IuyLnOqwgeuPmeq4sOqwgCDsl4bslrTrj4QgU09F7J2YIOydtOuypO2KuCDshKDtm4TqtIDqs4Tr
ipQg7ZWt7IOBIOygle2Zle2VmOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiYWZmZWN0ZWRfbGF5
ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9LAog
ICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfaGlzdG9yaWFuX2VxdWFsc19zb2UiLAog
ICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1lc3NhZ2UiOiAiSGlzdG9yaWFu
IO2RnOuzuOyLnOqwhOunjOycvOuhnCBTT0XsmYAg64+Z7J287ZWcIOydtOuypO2KuCDsiJzshJzr
pbwg7ZWt7IOBIOyerO2YhO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9uIjog
IuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuztOuhnCDrs7jri6QuIEhpc3Rv
cmlhbiDstpTshLjsmYAgU09FIOydtOuypO2KuOyInOyEnOuKlCDtkZzrs7jso7zquLDsmYAgVGlt
ZXN0YW1wIOy2nOyymOqwgCDri6TrpbTrr4DroZwg64+Z7J287ZWY64uk6rOgIOuLqOygle2VoCDs
iJgg7JeG64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJIaXN0b3JpYW4g7LaU7IS47JmA
IFNPRSDsnbTrsqTtirjsiJzshJzripQg7ZGc67O47KO86riw7JmAIFRpbWVzdGFtcCDstpzsspjq
sIAg64uk66W066+A66GcIOuPmeydvO2VmOuLpOqzoCDri6jsoJXtlaAg7IiYIOyXhuuLpC4iLAog
ICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMCwKICAgICAgICAid3JvbmdfcGF0dGVy
bnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT9IaXN0b3JpYW5cXCDt
kZzrs7jsi5zqsITrp4zsnLzroZxcXCBTT0XsmYBcXCDrj5nsnbztlZxcXCDsnbTrsqTtirhcXCDs
iJzshJzrpbxcXCDtla3sg4FcXCDsnqztmITtlaBcXCDsiJhcXCDsnojri6RcXC5cXHMqWy4hXT9c
XHMqJCIKICAgICAgICBdLAogICAgICAgICJleGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAg
ICAgICJIaXN0b3JpYW4g7ZGc67O47Iuc6rCE66eM7Jy866GcIFNPReyZgCDrj5nsnbztlZwg7J20
67Kk7Yq4IOyInOyEnOulvCDtla3sg4Eg7J6s7ZiE7ZWgIOyImCDsnojri6QuIgogICAgICAgIF0s
CiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJE
IgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2ZhdGFsX2F1
ZGl0X2VxdWFsc19zb2UiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1l
c3NhZ2UiOiAiQXVkaXQgdHJhaWzqs7wgU09F64qUIOuPmeydvO2VnCDquLDroZ3snbTri6QuIiwK
ICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg
7ZuE67O066GcIOuzuOuLpC4gQXVkaXQgdHJhaWzsnYAg7IKs7Jqp7J6QIO2WieychOyZgCDrs4Dq
sr3snYQg6riw66Gd7ZWY6rOgIFNPReuKlCDqs7XsoJXCt+yEpOu5hCDsg4Htg5zrs4DtmZTsnZgg
7Iic7ISc66W8IOq4sOuhne2VnOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQXVkaXQg
dHJhaWzsnYAg7IKs7Jqp7J6QIO2WieychOyZgCDrs4Dqsr3snYQg6riw66Gd7ZWY6rOgIFNPReuK
lCDqs7XsoJXCt+yEpOu5hCDsg4Htg5zrs4DtmZTsnZgg7Iic7ISc66W8IOq4sOuhne2VnOuLpC4i
LAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMCwKICAgICAgICAid3JvbmdfcGF0
dGVybnMiOiBbCiAgICAgICAgICAiKD9pbSleXFxzKig/OlstKuKAol1cXHMqKT9BdWRpdFxcIHRy
YWls6rO8XFwgU09F64qUXFwg64+Z7J287ZWcXFwg6riw66Gd7J2064ukXFwuXFxzKlsuIV0/XFxz
KiQiCiAgICAgICAgXSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAg
ICAiQXVkaXQgdHJhaWzqs7wgU09F64qUIOuPmeydvO2VnCDquLDroZ3snbTri6QuIgogICAgICAg
IF0sCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAg
ICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2ZhdGFs
X2JyaWdodF9jb2xvcnMiLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgIm1l
c3NhZ2UiOiAiSGlnaC1wZXJmb3JtYW5jZSBITUnripQg67Cd7J2AIOyDieydhCDrp47snbQg7IKs
7Jqp7ZWg7IiY66GdIOyDge2ZqeyduOyLneydtCDsoovslYTsp4Tri6QuIiwKICAgICAgICAiZGVz
Y3JpcHRpb24iOiAi66qF7Iuc7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuz
uOuLpC4gSGlnaC1wZXJmb3JtYW5jZSBITUnripQg7IOJ7IOB7J2EIOygnO2VnOuQnCDruYTsoJXs
g4Eg7J2Y66+47JeQIOydvOq0gOuQmOqyjCDsgqzsmqntlZjsl6wg7Iuc6rCB7KCBIOyasOyEoOyI
nOychOulvCDrp4zrk6Dri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkhpZ2gtcGVyZm9y
bWFuY2UgSE1J64qUIOyDieyDgeydhCDsoJztlZzrkJwg67mE7KCV7IOBIOydmOuvuOyXkCDsnbzq
tIDrkJjqsowg7IKs7Jqp7ZWY7JesIOyLnOqwgeyggSDsmrDshKDsiJzsnITrpbwg66eM65Og64uk
LiIsCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wLAogICAgICAgICJ3cm9uZ19w
YXR0ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCiXVxccyopP0hpZ2hcXC1w
ZXJmb3JtYW5jZVxcIEhNSeuKlFxcIOuwneydgFxcIOyDieydhFxcIOunjuydtFxcIOyCrOyaqe2V
oOyImOuhnVxcIOyDge2ZqeyduOyLneydtFxcIOyii+yVhOynhOuLpFxcLlxccypbLiFdP1xccyok
IgogICAgICAgIF0sCiAgICAgICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAg
IkhpZ2gtcGVyZm9ybWFuY2UgSE1J64qUIOuwneydgCDsg4nsnYQg66eO7J20IOyCrOyaqe2VoOyI
mOuhnSDsg4Htmansnbjsi53snbQg7KKL7JWE7KeE64ukLiIKICAgICAgICBdLAogICAgICAgICJh
ZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBd
CiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF91bnJlc3RyaWN0ZWRf
YXV0aG9yaXR5IiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdl
IjogIuyatOyghOyekOyXkOqyjCDrqqjrk6AgU2V0cG9pbnTsmYAg67O07Zi46rSA66CoIOqwkuyd
hCDsoJztlZwg7JeG7J20IOuzgOqyve2VmOqyjCDtlbTslbwg7JWI7KCE7ZWY64ukLiIsCiAgICAg
ICAgImRlc2NyaXB0aW9uIjogIuuqheyLnOyggSDrsJjrjIAg7KO87J6l66eMIGZhdGFsIO2bhOuz
tOuhnCDrs7jri6QuIOykkeyalCDqsJLqs7wg7KGw7J6R7J2AIOyXre2VoOq4sOuwmCDstZzshozq
toztlZwsIOyKueyduCwg7ZmV7J246rO8IEF1ZGl0IHRyYWls66GcIO2GteygnO2VtOyVvCDtlZzr
i6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuykkeyalCDqsJLqs7wg7KGw7J6R7J2AIOyX
re2VoOq4sOuwmCDstZzshozqtoztlZwsIOyKueyduCwg7ZmV7J246rO8IEF1ZGl0IHRyYWls66Gc
IO2GteygnO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1
LjAsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpb
LSrigKJdXFxzKik/7Jq07KCE7J6Q7JeQ6rKMXFwg66qo65OgXFwgU2V0cG9pbnTsmYBcXCDrs7Tt
mLjqtIDroKhcXCDqsJLsnYRcXCDsoJztlZxcXCDsl4bsnbRcXCDrs4Dqsr3tlZjqsoxcXCDtlbTs
lbxcXCDslYjsoITtlZjri6RcXC5cXHMqWy4hXT9cXHMqJCIKICAgICAgICBdLAogICAgICAgICJl
eGFtcGxlc19vcl9wYXR0ZXJucyI6IFsKICAgICAgICAgICLsmrTsoITsnpDsl5Dqsowg66qo65Og
IFNldHBvaW507JmAIOuztO2YuOq0gOugqCDqsJLsnYQg7KCc7ZWcIOyXhuydtCDrs4Dqsr3tlZjq
sowg7ZW07JW8IOyViOyghO2VmOuLpC4iCiAgICAgICAgXSwKICAgICAgICAiYWZmZWN0ZWRfbGF5
ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9LAog
ICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfY29tbWFuZF9wcm92ZXNfYWN0aW9uIiwK
ICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIkhNSeyXkOyE
nCDrqoXroLnsnYQg7KCE7Iah7ZWY66m0IO2YhOyepeyEpOu5hCDrj5nsnpHsnbQg7JmE66OM65Cc
IOqyg+ycvOuhnCDtjJDri6jtlZzri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi66qF7Iuc
7KCBIOuwmOuMgCDso7zsnqXrp4wgZmF0YWwg7ZuE67O066GcIOuzuOuLpC4g66qF66C5IOyghOyG
oeqzvCDsi6TsoJwgRmVlZGJhY2vsnYQg67aE66as7ZWY6rOgIFRpbWVvdXTCt+u2iOydvOy5mMK3
7ZKI7KeI7IOB7YOc66W8IO2ZleyduO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9y
dWxlIjogIuuqheuguSDsoITshqHqs7wg7Iuk7KCcIEZlZWRiYWNr7J2EIOu2hOumrO2VmOqzoCBU
aW1lb3V0wrfrtojsnbzsuZjCt+2SiOyniOyDge2DnOulvCDtmZXsnbjtlbTslbwg7ZWc64ukLiIs
CiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wLAogICAgICAgICJ3cm9uZ19wYXR0
ZXJucyI6IFsKICAgICAgICAgICIoP2ltKV5cXHMqKD86Wy0q4oCiXVxccyopP0hNSeyXkOyEnFxc
IOuqheugueydhFxcIOyghOyGoe2VmOuptFxcIO2YhOyepeyEpOu5hFxcIOuPmeyekeydtFxcIOyZ
hOujjOuQnFxcIOqyg+ycvOuhnFxcIO2MkOuLqO2VnOuLpFxcLlxccypbLiFdP1xccyokIgogICAg
ICAgIF0sCiAgICAgICAgImV4YW1wbGVzX29yX3BhdHRlcm5zIjogWwogICAgICAgICAgIkhNSeyX
kOyEnCDrqoXroLnsnYQg7KCE7Iah7ZWY66m0IO2YhOyepeyEpOu5hCDrj5nsnpHsnbQg7JmE66OM
65CcIOqyg+ycvOuhnCDtjJDri6jtlZzri6QuIgogICAgICAgIF0sCiAgICAgICAgImFmZmVjdGVk
X2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0KICAgICAg
fSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2ZhdGFsX3JhaXNlX2FsbF9wcmlvcml0aWVz
IiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJtZXNzYWdlIjogIkFsYXJt
IGZsb29k64qUIOuqqOuToCBBbGFybSDsmrDshKDsiJzsnITrpbwg64aS7J2066m0IO2VtOqysOuQ
nOuLpC4iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLrqoXsi5zsoIEg67CY64yAIOyjvOyepeun
jCBmYXRhbCDtm4Trs7TroZwg67O464ukLiBBbGFybSBmbG9vZOuKlCDsm5Dsnbgg7KCc6rGwLCDt
lanrpqztmZQsIENoYXR0ZXJpbmcg6rCc7ISgLCDsg4Htg5zquLDrsJggU3VwcHJlc3Npb27qs7wg
7ZmU66m0wrfsoIjssKgg6rCc7ISg7Jy866GcIOykhOyduOuLpC4iLAogICAgICAgICJjb3JyZWN0
X3J1bGUiOiAiQWxhcm0gZmxvb2TripQg7JuQ7J24IOygnOqxsCwg7ZWp66as7ZmULCBDaGF0dGVy
aW5nIOqwnOyEoCwg7IOB7YOc6riw67CYIFN1cHByZXNzaW9u6rO8IO2ZlOuptMK37KCI7LCoIOqw
nOyEoOycvOuhnCDspITsnbjri6QuIiwKICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1
LjAsCiAgICAgICAgIndyb25nX3BhdHRlcm5zIjogWwogICAgICAgICAgIig/aW0pXlxccyooPzpb
LSrigKJdXFxzKik/QWxhcm1cXCBmbG9vZOuKlFxcIOuqqOuToFxcIEFsYXJtXFwg7Jqw7ISg7Iic
7JyE66W8XFwg64aS7J2066m0XFwg7ZW06rKw65Cc64ukXFwuXFxzKlsuIV0/XFxzKiQiCiAgICAg
ICAgXSwKICAgICAgICAiZXhhbXBsZXNfb3JfcGF0dGVybnMiOiBbCiAgICAgICAgICAiQWxhcm0g
Zmxvb2TripQg66qo65OgIEFsYXJtIOyasOyEoOyInOychOulvCDrhpLsnbTrqbQg7ZW06rKw65Cc
64ukLiIKICAgICAgICBdLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAi
QyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0KICAgIF0sCiAgICAibWFqb3JfY2hl
Y2tzIjogW10sCiAgICAicXVlc3Rpb25fdHlwZV9jaGVja3MiOiBbXSwKICAgICJuZXh0X3ByYWN0
aWNlX3BvaW50cyI6IFsKICAgICAgIkFsYXJtLCBFdmVudCwgVHJpcOqzvCBJbnRlcmxvY2vsnZgg
66qp7KCB6rO8IOyLpO2WieyjvOyytOulvCDruYTqtZDtlZzri6QuIiwKICAgICAgIkRlYWRiYW5k
LCBEZWxheSwgU2hlbHZpbmfqs7wgU3VwcHJlc3Npb27snZgg7KCB7Jqp7KGw6rG07J2EIO2RnOuh
nCDsoJXrpqztlZzri6QuIiwKICAgICAgIlNPRSwgSGlzdG9yaWFuLCBGaXJzdC1vdXTqs7wgQXVk
aXQgdHJhaWzsnZgg6riw66Gd64yA7IOB6rO8IOyLnOqwhO2SiOyniOydhCDqtazrtoTtlZzri6Qu
IiwKICAgICAgIlNldHBvaW50IGxpc3TsnZgg67OA6rK96raM7ZWcLCDqt7zqsbDsmYAgQXVkaXQg
7ZWt66qp7J2EIOyEpOqzhO2VnOuLpC4iLAogICAgICAiSGlnaC1wZXJmb3JtYW5jZSBITUkg7ZmU
66m06rOE7Li16rO8IOu5hOygleyDgeyDge2ZqSDrjIDsnZHtnZDrpoTsnYQg7Jew6rKw7ZWc64uk
LiIKICAgIF0sCiAgICAiZGVfY2xhaW1fdHJ1c3QiOiB7CiAgICAgICJmb3JtdWxhX2NsYWltcyI6
ICJtZWRpdW0iLAogICAgICAiZmllbGRfY2xhaW1zIjogIm1lZGl1bSIKICAgIH0KICB9LAogICJs
bG1fcHJvZmlsZSI6IHsKICAgICJkaXNwbGF5X25hbWUiOiAiSE1JwrdTQ0FEQcK3QWxhcm3Ct1Nl
dHBvaW50wrdUcmlwwrdJbnRlcmxvY2vCt1NPRSDrsI8g7Jq07KCE7KCV67O0IOq0gOumrCIsCiAg
ICAiZGlmZmljdWx0eSI6ICJERVNJR05fRVZBTFVBVElPTiIsCiAgICAiZW5hYmxlZCI6IHRydWUs
CiAgICAiY2FwX3BvbGljeSI6IHsKICAgICAgImZhdGFsX2RlZmF1bHRfY2VpbGluZyI6IDE1LjAs
CiAgICAgICJtYWpvcl9kZWZhdWx0X2NlaWxpbmciOiAxOC4wLAogICAgICAiZmF0YWxfcmVxdWly
ZXNfZXhwbGljaXRfY29udHJhZGljdGlvbiI6IHRydWUsCiAgICAgICJvbWlzc2lvbl9pc19ub3Rf
ZmF0YWwiOiB0cnVlCiAgICB9LAogICAgImNhbmRpZGF0ZV9leHRyYWN0aW9uIjogewogICAgICAi
dG9waWNfdGVybXMiOiBbCiAgICAgICAgIkhNSSBTQ0FEQSBhbGFybSBtYW5hZ2VtZW50IFNPRSIs
CiAgICAgICAgIuqzoOyEseuKpSBITUkg6rK967O0IO2VqeumrO2ZlCBTT0UiLAogICAgICAgICJI
TUkgU0NBREEgQWxhcm0gU2V0cG9pbnQgVHJpcCBJbnRlcmxvY2siLAogICAgICAgICLsmrTsoITs
oJXrs7Qg6rK967O0IOyEpOygleqwkiDsnbTrsqTtirjsiJzshJwiLAogICAgICAgICJhbGFybSBw
aGlsb3NvcGh5IHJhdGlvbmFsaXphdGlvbiBwcmlvcml0eSIsCiAgICAgICAgIuqyveuztCDssqDt
lZkg7ZWp66as7ZmUIOyasOyEoOyInOychCIsCiAgICAgICAgImFsYXJtIGRlYWRiYW5kIGRlbGF5
IHNoZWx2aW5nIHN1cHByZXNzaW9uIiwKICAgICAgICAi6rK967O0IOuNsOuTnOuwtOuTnCDsp4Ds
l7Ag7ImY67mZIOyWteygnCIsCiAgICAgICAgInNldHBvaW50IGFsYXJtIHRyaXAgaW50ZXJsb2Nr
IHZhbHVlIG1hbmFnZW1lbnQiLAogICAgICAgICLshKTsoJXqsJIg6rK967O06rCSIO2KuOumveqw
kiDsnbjthLDroZ3qsJIg6rSA66asIiwKICAgICAgICAic2VxdWVuY2Ugb2YgZXZlbnRzIGF1ZGl0
IHRyYWlsIHRpbWUgc3luY2hyb25pemF0aW9uIiwKICAgICAgICAiU09FIOqwkOyCrOy2lOyggSDs
i5zqsIHrj5nquLAiLAogICAgICAgICJoaWdoIHBlcmZvcm1hbmNlIEhNSSBkaXNwbGF5IGhpZXJh
cmNoeSIsCiAgICAgICAgIuqzoOyEseuKpSBITUkg7ZmU66m06rOE7Li1IOyDge2ZqeyduOyLnSIs
CiAgICAgICAgIm9wZXJhdG9yIGF1dGhvcml0eSBodW1hbiBlcnJvciBwcmV2ZW50aW9uIiwKICAg
ICAgICAi7Jq07KCE7J6QIOq2jO2VnCDtnLTrqLzsl5Drn6wg67Cp7KeAIiwKICAgICAgICAiYWxh
cm0gZmxvb2QgY2hhdHRlcmluZyBzdGFuZGluZyBhbGFybSIsCiAgICAgICAgIuqyveuztO2Preyj
vCDssYTthLDrp4Eg7IOB7Iuc6rK967O0IiwKICAgICAgICAiYWJub3JtYWwgc2l0dWF0aW9uIG1h
bmFnZW1lbnQgSE1JIGFsYXJtIiwKICAgICAgICAi67mE7KCV7IOB7IOB7ZmpIOq0gOumrCBTQ0FE
QSDsmrTsoITsoJXrs7QiCiAgICAgIF0sCiAgICAgICJrZXlfdGVybXMiOiBbCiAgICAgICAgImht
aSIsCiAgICAgICAgInNjYWRhIiwKICAgICAgICAic3VwZXJ2aXNvcnkgY29udHJvbCIsCiAgICAg
ICAgImRhdGEgYWNxdWlzaXRpb24iLAogICAgICAgICJoaWdoLXBlcmZvcm1hbmNlIGhtaSIsCiAg
ICAgICAgImRpc3BsYXkgaGllcmFyY2h5IiwKICAgICAgICAib3ZlcnZpZXcgZGlzcGxheSIsCiAg
ICAgICAgInNpdHVhdGlvbmFsIGF3YXJlbmVzcyIsCiAgICAgICAgImNvbG9yIGNvZGluZyIsCiAg
ICAgICAgIm5hdmlnYXRpb24gY29udGV4dCIsCiAgICAgICAgImFsYXJtIHBoaWxvc29waHkiLAog
ICAgICAgICJhbGFybSByYXRpb25hbGl6YXRpb24iLAogICAgICAgICJhbGFybSBwcmlvcml0eSIs
CiAgICAgICAgImNvbnNlcXVlbmNlIHNldmVyaXR5IiwKICAgICAgICAib3BlcmF0b3IgcmVzcG9u
c2UgdGltZSIsCiAgICAgICAgImFsYXJtIGFja25vd2xlZGdlbWVudCIsCiAgICAgICAgInJldHVy
biB0byBub3JtYWwiLAogICAgICAgICJkZWFkYmFuZCIsCiAgICAgICAgIm9uLWRlbGF5IiwKICAg
ICAgICAib2ZmLWRlbGF5IiwKICAgICAgICAic2hlbHZpbmciLAogICAgICAgICJzdXBwcmVzc2lv
biIsCiAgICAgICAgImFsYXJtIGZsb29kIiwKICAgICAgICAiY2hhdHRlcmluZyBhbGFybSIsCiAg
ICAgICAgInN0YW5kaW5nIGFsYXJtIiwKICAgICAgICAiYWxhcm0gcGVyZm9ybWFuY2Uga3BpIiwK
ICAgICAgICAic2V0cG9pbnQgbGlzdCIsCiAgICAgICAgImFsYXJtIHZhbHVlIiwKICAgICAgICAi
dHJpcCB2YWx1ZSIsCiAgICAgICAgImludGVybG9jayB2YWx1ZSIsCiAgICAgICAgInNlcXVlbmNl
IG9mIGV2ZW50cyIsCiAgICAgICAgInNvZSIsCiAgICAgICAgInNvdXJjZSB0aW1lc3RhbXAiLAog
ICAgICAgICJ0aW1lIHN5bmNocm9uaXphdGlvbiIsCiAgICAgICAgInRpbWUgcXVhbGl0eSIsCiAg
ICAgICAgImhpc3RvcmlhbiIsCiAgICAgICAgImZpcnN0LW91dCIsCiAgICAgICAgImF1ZGl0IHRy
YWlsIiwKICAgICAgICAib3BlcmF0b3IgYXV0aG9yaXR5IiwKICAgICAgICAicm9sZSBiYXNlZCBh
Y2Nlc3MiLAogICAgICAgICJsZWFzdCBwcml2aWxlZ2UiLAogICAgICAgICJodW1hbiBlcnJvciBw
cmV2ZW50aW9uIiwKICAgICAgICAiZGF0YSBxdWFsaXR5IiwKICAgICAgICAic3RhbGUgZGF0YSIs
CiAgICAgICAgImFibm9ybWFsIHNpdHVhdGlvbiBtYW5hZ2VtZW50IgogICAgICBdLAogICAgICAi
cmVxdWlyZWRfY29udGV4dF9ncm91cHMiOiBbCiAgICAgICAgWwogICAgICAgICAgImhtaSIsCiAg
ICAgICAgICAic2NhZGEiLAogICAgICAgICAgIuqzoOyEseuKpSBobWkiLAogICAgICAgICAgIu2Z
lOuptOqzhOy4tSIsCiAgICAgICAgICAi7IOB7Zmp7J247IudIgogICAgICAgIF0sCiAgICAgICAg
WwogICAgICAgICAgImFsYXJtIiwKICAgICAgICAgICLqsr3rs7QiLAogICAgICAgICAgInNldHBv
aW50IiwKICAgICAgICAgICJkZWFkYmFuZCIsCiAgICAgICAgICAic2hlbHZpbmciLAogICAgICAg
ICAgInN1cHByZXNzaW9uIgogICAgICAgIF0sCiAgICAgICAgWwogICAgICAgICAgInNvZSIsCiAg
ICAgICAgICAiYXVkaXQgdHJhaWwiLAogICAgICAgICAgIuyLnOqwgeuPmeq4sCIsCiAgICAgICAg
ICAi7Jq07KCE7J6QIOq2jO2VnCIsCiAgICAgICAgICAi67mE7KCV7IOB7IOB7ZmpIgogICAgICAg
IF0KICAgICAgXSwKICAgICAgImV4Y2x1ZGVfaWZfb25seSI6IFsKICAgICAgICAiU2VxdWVuY2Ug
c3RhdGUgdHJhbnNpdGlvbiB0cmlwIGxhdGNoIHJlc2V0IiwKICAgICAgICAi7Iuc7YCA7IqkIOyD
ge2DnOyghOydtCDsnbjthLDroZ0g7Yq466a9IOuFvOumrCIsCiAgICAgICAgIlYtTW9kZWwgcmVx
dWlyZW1lbnQgdHJhY2VhYmlsaXR5IHVuaXQgdGVzdCIsCiAgICAgICAgIuyGjO2UhO2KuOybqOyW
tCDsiJjrqoXso7zquLAg6rKA7KadIO2ZleyduCIsCiAgICAgICAgIkZBVCBTQVQgY29tbWlzc2lv
bmluZyBhY2NlcHRhbmNlIiwKICAgICAgICAi7ZSE66Gc7KCd7Yq4IOyLnOyatOyghCDsnbjsiJgi
LAogICAgICAgICJTSUwgUEZEYXZnIFBGSCBzYWZldHkgbGlmZWN5Y2xlIiwKICAgICAgICAiZmll
bGRidXMgZXRoZXJuZXQgcHJvdG9jb2wgY3liZXJzZWN1cml0eSIsCiAgICAgICAgIuqzte2GtSBS
b3V0ZXIg6rWs7ZiEIgogICAgICBdLAogICAgICAibWluaW11bV9kaXN0aW5jdF9ncm91cHMiOiAy
CiAgICB9LAogICAgInRydXRoX3NjaGVtYSI6IFsKICAgICAgewogICAgICAgICJpZCI6ICJzdzAz
X3Njb3BlX29wZXJhdG9yX2luZm9ybWF0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIlNX
LTAz64qUIEhNScK3U0NBREEg6rWs7KGwLCDqs6DshLHriqUgSE1JLCBBbGFybSDqtIDrpqwsIFNl
dHBvaW50wrdBbGFybcK3VHJpcMK3SW50ZXJsb2NrIOqwkiDqtIDrpqwsIFNPRSwgQXVkaXQgdHJh
aWwsIOyatOyghOyekCDqtoztlZzqs7wg67mE7KCV7IOB7IOB7ZmpIOuMgOydkeydhCDsmrTsoITs
oJXrs7Qg6rSA66asIOyytOqzhOuhnCDsl7DqsrDtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZf
b3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfaG1p
X3NjYWRhX2FyY2hpdGVjdHVyZSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJITUnripQg7Jq0
7KCE7J6Q7JmAIOygnOyWtOyLnOyKpO2FnOydmCDsg4HtmLjsnpHsmqkg7ZmU66m07J2EIOygnOqz
te2VmOqzoCwgU0NBREHripQg7JuQ6rKpIOqwkOyLnMK3642w7J207YSwIOyImOynkcK366qF66C5
wrfqsr3rs7TCt+ydtOugpSDquLDriqXsnYQg7ISc67KELCDthrXsi6Drp50sIO2YhOyepSDsoJzs
lrTquLDsmYAg7Jew6rOE7ZWY64qUIOyDgeychCDqsJDsi5zssrTqs4TsnbTri6QuIiwKICAgICAg
ICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDNfYXJjaGl0ZWN0dXJlX3JlZHVuZGFuY3lfcXVhbGl0eSIsCiAgICAgICAgImNvcnJl
Y3RfcnVsZSI6ICJITUnCt1NDQURBIOq1rOyhsOuKlCDshJzrsoTsmYAg64Sk7Yq47JuM7YGs7J2Y
IOydtOykke2ZlCDsl6zrtoDrv5Ag7JWE64uI6528IO2GteyLoCDri6jsoIgsIEZhaWxvdmVyLCDr
jbDsnbTthLAg7ZKI7KeILCBTdGFsZSDsg4Htg5wg67CPIOyerOyXsOqysCDtm4Qg642w7J207YSw
IOydvOy5mOyEseydhCDsmrTsoITsnpDsl5Dqsowg66qF7ZmV7Z6IIOyghOuLrO2VtOyVvCDtlZzr
i6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7
CiAgICAgICAgImlkIjogInN3MDNfaGlnaF9wZXJmb3JtYW5jZV9obWkiLAogICAgICAgICJjb3Jy
ZWN0X3J1bGUiOiAiSGlnaC1wZXJmb3JtYW5jZSBITUnripQg7KCV7IOB7IOB7YOc7J2YIOu2iO2V
hOyalO2VnCDsnqXsi53snYQg7KSE7J206rOgIOqzteygleyDge2DnCwg7Y647LCoLCDstpTshLjs
mYAg67mE7KCV7IOBIOynle2bhOulvCDruaDrpbTqsowg7J247KeA7ZWY64+E66GdIOygleuztCDr
sIDrj4TsmYAg7Iuc6rCB7KCBIOyasOyEoOyInOychOulvCDshKTqs4TtlZzri6QuIiwKICAgICAg
ICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDNfZGlzcGxheV9oaWVyYXJjaHkiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi7ZmU
66m06rOE7Li17J2AIOydvOuwmOyggeycvOuhnCBMZXZlbCAxIOqzteyglSDsoITssrQgT3ZlcnZp
ZXcsIExldmVsIDIgVW5pdMK3QXJlYSwgTGV2ZWwgMyDsg4HshLgg7Jq07KCELCBMZXZlbCA0IOyn
hOuLqMK37KCV67mEIOygleuztOuhnCDqtazshLHtlZjrqbAg7IOB7JyE7JeQ7IScIOydtOyDgSDs
nITsuZjrpbwg7LC+6rOgIO2VmOychOyXkOyEnCDsm5Dsnbjqs7wg7KGw7LmY66W8IO2ZleyduO2V
mOuPhOuhnSDsl7DqsrDtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxz
ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfY29sb3JfY29udGV4dF9uYXZp
Z2F0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIuyDieyDgeydgCDsoJXsg4Eg7J6l7Iud
67O064ukIEFsYXJtLCDruYTsoJXsg4EsIOyEoO2DneyDge2DnOyZgCDtkojsp4jsoIDtlZgg65Ox
IOygnO2VnOuQnCDsnZjrr7jsl5Ag7J286rSA65CY6rKMIOyCrOyaqe2VmOqzoCwg7ZmU66m0IOyd
tOuPmSDsi5wg7ISk67mEIOychOy5mMK37Jq07KCE66qo65OcwrfstpTshLjCt+q0gOugqCBBbGFy
beydmCDrp6Xrnb3snbQg7Jyg7KeA65CY7Ja07JW8IO2VnOuLpC4iLAogICAgICAgICJmYXRhbF9p
Zl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19h
bGFybV9kZWZpbml0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkFsYXJt7J2AIOu5hOyg
leyDgSDsg4Htg5zrpbwg7Jq07KCE7J6Q7JeQ6rKMIOyVjOumrOqzoCDsoJXtlbTsp4Qg7Iuc6rCE
IOyViOyXkCDtjJDri6gg65iQ64qUIOyhsOy5mOulvCDsmpTqtaztlZjripQg6riw64ql7J2066mw
LCDsobDsuZjqsIAg7ZWE7JqU7ZWY7KeAIOyViuydgCDri6jsiJwgRXZlbnTCt1N0YXR1c8K3Tm90
aWZpY2F0aW9u6rO8IOq1rOu2hO2VnOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6
IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2FsYXJtX3BoaWxvc29w
aHkiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQWxhcm0gcGhpbG9zb3BoeeuKlCBBbGFybeyd
mCDrqqnsoIEsIOyXre2VoCwg7Jqw7ISg7Iic7JyEIOq4sOykgCwg7IOB7YOc7ZGc7ZiELCDsirns
nbjqtoztlZwsIFNoZWx2aW5nwrdTdXBwcmVzc2lvbiwg7ISx64ql7KeA7ZGcLCDrs4Dqsr3qtIDr
pqzsmYAg7KO86riw7KCBIOqygO2GoCDsm5DsuZnsnYQg7KGw7KeBIOywqOybkOyXkOyEnCDsoJXs
nZjtlZwg7IOB7JyEIOygleyxheydtOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6
IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19hbGFybV9yYXRpb25h
bGl6YXRpb24iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQWxhcm0gcmF0aW9uYWxpemF0aW9u
7J2AIOqwgSDtm4Trs7QgQWxhcm3sl5Ag64yA7ZW0IOybkOyduCwg6rKw6rO8LCDsmrTsoITsnpAg
7KGw7LmYLCDtl4jsmqkg7J2R64u17Iuc6rCELCDsmrDshKDsiJzsnIQsIOyEpOygleqwkiwgRGVh
ZGJhbmQsIERlbGF5LCBTaGVsdmluZyDtl4jsmqnsobDqsbTqs7wg66y47IScIOq3vOqxsOulvCDq
soDthqDtlZjsl6wg7ZWE7JqU7ZWcIEFsYXJt66eMIOyKueyduO2VmOuKlCDtmZzrj5nsnbTri6Qu
IiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAg
ICAgICAgImlkIjogInN3MDNfYWxhcm1fcHJpb3JpdHkiLAogICAgICAgICJjb3JyZWN0X3J1bGUi
OiAiQWxhcm0gcHJpb3JpdHnripQg64uo7IicIOy4oeygleqwkiDtgazquLDqsIAg7JWE64uI6528
IOyhsOy5mO2VmOyngCDslYrslZjsnYQg65WM7J2YIOqysOqzvCDsi6zqsIHrj4TsmYAg7Jq07KCE
7J6Q7JeQ6rKMIO2XiOyaqeuQnCDsnZHri7Xsi5zqsITsnYQg7ZWo6ruYIO2PieqwgO2VmOyXrCDq
srDsoJXtlZjrqbAsIOyasOyEoOyInOychOuzhCDtkZzsi5zsmYAg64yA7J2R7KCI7LCo6rCAIOyd
vOq0gOuQmOyWtOyVvCDtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiB0cnVl
CiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19hbGFybV9zdGF0ZV9hY2tub3ds
ZWRnZW1lbnQiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQWxhcm3snZggUHJvY2VzcyBjb25k
aXRpb24sIEFjdGl2ZcK3UmV0dXJuLXRvLW5vcm1hbCDsg4Htg5zsmYAgQWNrbm93bGVkZ2VtZW50
IOyDge2DnOuKlCDrs4TqsJzsnbTrqbAsIOyatOyghOyekCBBY2tub3dsZWRnZeuKlCDsnbjsp4Ag
6riw66Gd7J28IOu/kCDsm5Dsnbgg7KCc6rGwIOuYkOuKlCBBbGFybSDsobDqsbQg7ZW07KCc66W8
IOydmOuvuO2VmOyngCDslYrripTri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiB0
cnVlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19hbGFybV9kZWFkYmFuZCIs
CiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJEZWFkYmFuZOuKlCBBbGFybeydtCDrsJzsg53tlZwg
65KkIOygleyDgSDrs7Xqt4Ag7J6E6rOE6rCS7J2EIOuwnOyDnSDsnoTqs4TqsJLqs7wg64uk66W0
6rKMIOuRkOuKlCDqsJLsnZgg7J2066Cl7Y+t7Jy866GcLCDqsr3qs4Qg67aA6re8IOuFuOydtOym
iOyXkCDsnZjtlZwg67CY67O1IOuwnOyDneqzvCDtlbTsoJzrpbwg7KSE7J2464ukLiIsCiAgICAg
ICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDNfYWxhcm1fZGVsYXkiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQWxhcm0gZGVs
YXnripQg7KGw6rG07J20IOydvOyglSDsi5zqsIQg7Jew7IaNIOycoOyngOuQoCDrlYwg67Cc7IOd
7Iuc7YKk6rGw64KYIOygleyDgeyDge2DnOqwgCDsnbzsoJUg7Iuc6rCEIOycoOyngOuQoCDrlYwg
7ZW07KCc7ZWY64qUIOyLnOqwhCDtlYTthLDsnbTrqbAsIOyLpOygnOuhnCDtlYTsmpTtlZwg7Ken
7J2AIOydkeuLteydhCDqsIDrpqzsp4Ag7JWK64+E66GdIOqzteyglSDrj5ntirnshLHqs7wg7ZeI
7JqpIOydkeuLteyLnOqwhOydhCDqs6DroKTtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bw
b3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfYWxhcm1f
c2hlbHZpbmciLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiU2hlbHZpbmfsnYAg6raM7ZWcIOye
iOuKlCDsmrTsoITsnpDqsIAg7JWM66Ck7KeEIOyCrOycoOuhnCDtirnsoJUgQWxhcm3snYQg7KCc
7ZWc7Iuc6rCEIOuPmeyViCBBY3RpdmUgZGlzcGxheeyXkOyEnCDsnoTsi5zroZwg7Iio6riw64qU
IOyatOyghO2WieychOydtOupsCwgQWxhcm0g7KCV7J2Y7JmAIOydtOugpeydgCDsnKDsp4DtlZjq
s6Ag7IKs7JygwrfsgqzsmqnsnpDCt+yLnOyekcK366eM66OM66W8IOq4sOuhne2VnOuLpC4iLAog
ICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAg
ICJpZCI6ICJzdzAzX2FsYXJtX3N1cHByZXNzaW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjog
IlN1cHByZXNzaW9u7J2AIOyEpOu5hOyDge2DnCwg7Jq07KCE66qo65OcIOuYkOuKlCDrhbzrpqzs
obDqsbTsg4Eg7J2Y66+46rCAIOyXhuuKlCBBbGFybeydhCDshKTqs4TrkJwg7KGw6rG07JeQIOuU
sOudvCDsnpDrj5nsnLzroZwg67Cc7IOd7ZWY7KeAIOyViuqyjCDtlZjqsbDrgpgg7ZGc7Iuc64yA
7IOB7JeQ7IScIOygnOyZuO2VmOuKlCDquLDriqXsnbTrqbAsIOyatOyghOyekCDsnoTsnZggU2hl
bHZpbmfqs7wg6rWs67aE7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1
ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfYWxhcm1fZmxvb2RfY2hhdHRl
cmluZyIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBbGFybSBmbG9vZOuKlCDsp6fsnYAg7Iuc
6rCE7JeQIOunjuydgCBBbGFybeydtCDsp5HspJHrkJjslrQg7Jq07KCE7J6Q7J2YIOyduOyngMK3
7KeE64uowrfsobDsuZjrpbwg67Cp7ZW07ZWY64qUIOyDge2DnOydtOqzoCwgQ2hhdHRlcmluZ+yd
gCDqsJnsnYAgQWxhcm3snbQg67CY67O1IOuwnOyDncK37ZW07KCc65CY64qUIO2YhOyDgeydtOuv
gOuhnCDsm5Dsnbgg7KCc6rGwLCDtlanrpqztmZQsIERlYWRiYW5kwrdEZWxheeyZgCDsg4Htg5zq
uLDrsJggU3VwcHJlc3Npb27snLzroZwg6rCc7ISg7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lm
X29wcG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2Fs
YXJtX3BlcmZvcm1hbmNlX2twaSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBbGFybSDshLHr
iqXsnYAg7Iuc6rCE64u5IOuwnOyDneuloCwgUGVhayBhbGFybSByYXRlLCBTdGFuZGluZyBhbGFy
bSwgQ2hhdHRlcmluZyBhbGFybSwgRmxvb2Qg6rWs6rCELCDsmrDshKDsiJzsnIQg67aE7Y+s7JmA
IFNoZWx2aW5nIOyCrOyaqeydhCDtmITsnqUg6riw7KSA7Jy866GcIOy2lOygge2VmOqzoCDrsJjr
s7Ug7JuQ7J247J2EIOqwnOyEoO2VtOyVvCDtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bw
b3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfc2V0cG9p
bnRfdmFsdWVfY2xhc3NlcyIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsmrTsoIQgU2V0cG9p
bnQsIEFsYXJtIHZhbHVlLCBUcmlwIHZhbHVl7JmAIEludGVybG9jayB2YWx1ZeuKlCDrqqnsoIHq
s7wg7IaM7Jyg6raM7J20IOuLpOultOupsCwgQWxhcm3snYAg7Jq07KCE7J6QIOyhsOy5mOulvCDs
tInqtaztlZjqs6AgVHJpcMK3SW50ZXJsb2Nr7J2AIOyekOuPmSDrs7TtmLgg65iQ64qUIOuPmeye
keygnOyVveyXkCDsgqzsmqnrkJjrr4DroZwg6rCZ7J2AIOqwkuycvOuhnCDsnoTsnZgg7Ya17ZWp
7ZWY7KeAIOyViuuKlOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IHRydWUKICAg
ICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX3NldHBvaW50X2dvdmVybmFuY2UiLAog
ICAgICAgICJjb3JyZWN0X3J1bGUiOiAiU2V0cG9pbnQgbGlzdOuKlCBUYWcsIOq4sOuKpSwg6rCS
LCDri6jsnIQsIOuwqe2WpSwgRGVhZGJhbmTCt0RlbGF5LCDsoIHsmqnrqqjrk5wsIOq3vOqxsCwg
7Iq57J247J6QLCDrs4Dqsr3snbTroKXqs7wg6rSA66CoIFRyaXDCt0ludGVybG9jayDssLjsobDr
pbwg6rSA66as7ZWY6rOgIOyYqOudvOyduCDrs4Dqsr3snYAg6raM7ZWcwrfqsoDthqDCt+q4sOuh
ncK367O16rWs7KCI7LCo66W8IOqxsOyzkOyVvCDtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZf
b3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfYWxh
cm1fdHJpcF9pbnRlcmxvY2tfYm91bmRhcnkiLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiQWxh
cm3snYAg7Jq07KCE7J6QIO2MkOuLqOqzvCDsobDsuZjrpbwg7KeA7JuQ7ZWY64qUIOygleuztCDq
uLDriqXsnbTqs6AgVHJpcOydgCDrs7TtmLjsobDqsbTsl5Ag65Sw66W4IOyekOuPmSDsoJXsp4As
IEludGVybG9ja+ydgCDsnITtl5jtlZjqsbDrgpgg7ZeI7Jqp65CY7KeAIOyViuydgCDrj5nsnpHs
nYQg6riI7KeAwrfqsJXsoJztlZjripQg64W866as7J2066+A66GcIO2RnOyLnOygleuztOyZgCDs
i6Ttlonrhbzrpqzrpbwg6rWs67aE7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRl
IjogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfc29lX2RlZmluaXRp
b24iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiU09F64qUIOygkeygkMK37IOB7YOcwrfrqoXr
oLnCt+uztO2YuOuPmeyekSDrk7HsnZgg67OA7ZmUIOyLnOqwgSwg7Iug7Zi47JuQLCDsnbTsoITq
sJLCt+yDiOqwkuqzvCDtkojsp4jsnYQg6rO17Ya1IOyLnOqwhOy2leyXkCDqs6DtlbTsg4Hrj4Tr
oZwg6riw66Gd7ZWY7JesIOyCrOqxtOydmCDshKDtm4TqtIDqs4TsmYAg7JuQ7J247KCE7YyM66W8
IOu2hOyEne2VmOuKlCDquLDriqXsnbTri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUi
OiB0cnVlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM190aW1lX3N5bmNfcmVz
b2x1dGlvbiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTT0XsnZgg7J246rO87Iic7ISc66W8
IOyLoOuisO2VmOugpOuptCBQTEPCt0RDU8K3U0NBREHCt+uztO2YuOyepey5mOydmCDsi5zqs4Tr
pbwg64+Z6riw7ZmU7ZWY6rOgIFNvdXJjZSB0aW1lc3RhbXAsIOyLnOqwhOygle2ZleuPhCwg67aE
7ZW064qlLCDthrXsi6Dsp4Dsl7Dqs7wgVGltZSBxdWFsaXR566W8IO2VqOq7mCDqtIDrpqztlbTs
lbwg7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9LAog
ICAgICB7CiAgICAgICAgImlkIjogInN3MDNfaGlzdG9yaWFuX3ZzX3NvZSIsCiAgICAgICAgImNv
cnJlY3RfcnVsZSI6ICJIaXN0b3JpYW7snYAg7KO86riwIOuYkOuKlCDrs4DtmZTquLDrsJjsnLzr
oZwg6rO17KCV6rCSIOy2lOyEuOulvCDsnqXquLAg7KCA7J6l7ZWY64qUIOq4sOuKpeydtCDspJHs
i6zsnbTqs6AgU09F64qUIOydtOyCsCDsnbTrsqTtirjsnZgg7KCV7ZmV7ZWcIOuwnOyDneyInOyE
nOulvCDrtoTshJ3tlZjripQg6riw64ql7J20IOykkeyLrOydtOuvgOuhnCDtkZzrs7jso7zquLDs
mYAgVGltZXN0YW1wIOy2nOyymOulvCDqtazrtoTtlZzri6QuIiwKICAgICAgICAiZmF0YWxfaWZf
b3Bwb3NpdGUiOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmly
c3Rfb3V0X3JlbGF0aW9uIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkZpcnN0LW91dOydgCDt
lZwg7Jew7IeE7IKs6rG07JeQ7IScIOy1nOy0iOuhnCDsnKDtmqjtlbTsp4Qg7JuQ7J247J2EIExh
dGNo7ZWY7JesIOuztOyhtO2VmOuKlCDrhbzrpqzsnbTqs6AgU09F64qUIOyghOyytCDsnbTrsqTt
irgg7Iic7ISc66W8IOq4sOuhne2VmOuvgOuhnCwgRmlyc3Qtb3V07J2AIOu5oOuluCDsm5Dsnbjs
p4Dsi5zrpbwg7KCc6rO17ZWY6rOgIFNPReuKlCDsg4HshLgg6rKA7Kad7J2EIOuztOyZhO2VnOuL
pC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsK
ICAgICAgICAiaWQiOiAic3cwM19hdWRpdF90cmFpbCIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6
ICJBdWRpdCB0cmFpbOydgCDsgqzsmqnsnpDqsIAg7IiY7ZaJ7ZWcIEFja25vd2xlZGdlLCBTaGVs
dmluZywgU3VwcHJlc3Npb24g7Iq57J24LCBTZXRwb2ludCDrs4Dqsr0sIExvZ2luwrdMb2dvdXTq
s7wg7ZmU66m0IOuqheugueyXkCDrjIDtlbQg7IKs7Jqp7J6QLCDsi5zqsIEsIOuMgOyDgSwg7J20
7KCE6rCSwrfsg4jqsJIsIOyCrOycoOyZgCDqsrDqs7zrpbwg6riw66Gd7ZWc64ukLiIsCiAgICAg
ICAgImZhdGFsX2lmX29wcG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJp
ZCI6ICJzdzAzX29wZXJhdG9yX2F1dGhvcml0eSIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLs
mrTsoITsnpAg6raM7ZWc7J2AIOyXre2VoOq4sOuwmCDstZzshozqtoztlZwsIOyEpOu5hMK36riw
64qlwrfsmrTsoITrqqjrk5zrs4Qg67KU7JyELCDspJHsmpTsobDsnpHsnZgg7J6s7ZmV7J24IOuY
kOuKlCDsnbTspJHsirnsnbgsIOyEuOyFmOq0gOumrOyZgCBBdWRpdCB0cmFpbOydhCDthrXtlbQg
7Ya17KCc7ZWc64ukLiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogdHJ1ZQogICAgICB9
LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfaHVtYW5fZXJyb3JfcHJldmVudGlvbiIsCiAg
ICAgICAgImNvcnJlY3RfcnVsZSI6ICJIdW1hbiBlcnJvciDrsKnsp4DripQg7ZiE7J6sIE1vZGXC
t+yGjOycoOq2jMK3SW50ZXJsb2NrIOyCrOycoMK366qF66C564yA7IOBwrfsmIjsg4HqsrDqs7zr
pbwg66qF7ZmV7Z6IIO2RnOyLnO2VmOqzoCwg7KSR7JqU7KGw7J6RIO2ZleyduCwg7J6Y66q765Cc
IOuMgOyDgSDshKDtg50g67Cp7KeALCBDb21tYW5k7JmAIEZlZWRiYWNrIOu2hOumrCwg7Leo7IaM
wrfrs7Xqtawg6rK966Gc66W8IOygnOqzte2VmOuKlCDrsKnsi53snLzroZwg6rWs7ZiE7ZWc64uk
LiIsCiAgICAgICAgImZhdGFsX2lmX29wcG9zaXRlIjogZmFsc2UKICAgICAgfSwKICAgICAgewog
ICAgICAgICJpZCI6ICJzdzAzX2RhdGFfcXVhbGl0eV9kaXNwbGF5IiwKICAgICAgICAiY29ycmVj
dF9ydWxlIjogIkJhZCwgVW5jZXJ0YWluLCBTdGFsZSwgQ29tbXVuaWNhdGlvbiBsb3N07JmAIE1h
bnVhbCBzdWJzdGl0dXRpb24g6rCZ7J2AIOuNsOydtO2EsCDtkojsp4jsnYAg6rCSIOyekOyytOyZ
gCDrs4Trj4Qg7IOB7YOc66GcIO2RnOyLnO2VmOqzoCwg7ZKI7KeI7J20IOuCmOyBnCDqsJLsnYQg
7KCV7IOBIOy1nOyLoOqwkuyymOufvCDsoJzslrTtjJDri6jsnbTrgpgg7Jq07KCE7J6QIO2MkOuL
qOyXkCDsgqzsmqntlZjsp4Ag7JWK64+E66GdIO2VnOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9v
cHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19hYm5v
cm1hbF9zaXR1YXRpb25fbWFuYWdlbWVudCIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBYm5v
cm1hbCBzaXR1YXRpb24gbWFuYWdlbWVudOuKlCBPdmVydmlld+yXkOyEnCDsnbTsg4Eg7KeV7ZuE
66W8IOyhsOq4sOyXkCDrsJzqsqztlZjqs6AgQWxhcm3qs7wgVHJlbmTroZwg7KeE64uo7ZWY66mw
IOygiOywqOyZgCDqtoztlZzsl5Ag65Sw6528IOuMgOydke2VnCDrkqQg7KCV7IOB67O16rWs7JmA
IOyCrO2bhOu2hOyEneycvOuhnCDsnbTslrTsp4DripQgRGV0ZWN0LURpYWdub3NlLVJlc3BvbmQt
UmVjb3ZlciDtnZDrpoTsnbTri6QuIiwKICAgICAgICAiZmF0YWxfaWZfb3Bwb3NpdGUiOiBmYWxz
ZQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfc3cwMl9ib3VuZGFyeSIsCiAg
ICAgICAgImNvcnJlY3RfcnVsZSI6ICJTVy0wM+uKlCBBbGFybcK3U2V0cG9pbnTCt1NPRcK37ZmU
66m0wrfqtoztlZwg65OxIOyatOyghOyekCDsoJXrs7TsmYAg6rSA66as7KCV7LGF7J2EIOyGjOyc
oO2VmOqzoCwgSW50ZXJsb2NrwrdUcmlw7J2YIOyLpOygnCDrhbzrpqzqtazsobAsIOyDge2DnOyg
hOydtCwgTGF0Y2jCt1Jlc2V0IOuwjyBGYWlsLXNhZmUg64+Z7J6R7J2AIFNXLTAy66GcIOuEmOq4
tOuLpC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0sCiAgICAg
IHsKICAgICAgICAiaWQiOiAic3cwM19zdzA0X3N3MTBfYm91bmRhcnkiLAogICAgICAgICJjb3Jy
ZWN0X3J1bGUiOiAiU1ctMDPripQg7Jq07KCE7KCV67O07J2YIOuCtOyaqeqzvCDsmrTsmIHqtIDr
pqwg7JuQ7LmZ7J2EIOyGjOycoO2VmOqzoCwg7J2867CYIOyGjO2UhO2KuOybqOyWtCBWLU1vZGVs
wrfstpTsoIHshLHCt+yLnO2XmOyytOqzhOuKlCBTVy0wNCwg7ZSE66Gc7KCd7Yq4IOusuOyEnCDs
nbjrj4TCt0ZBVMK3U0FUwrfsi5zsmrTsoIQg7KCI7LCo64qUIFNXLTEw7Jy866GcIOuEmOq4tOuL
pC4iLAogICAgICAgICJmYXRhbF9pZl9vcHBvc2l0ZSI6IGZhbHNlCiAgICAgIH0KICAgIF0sCiAg
ICAiZmF0YWxfY29uZGl0aW9ucyI6IFsKICAgICAgewogICAgICAgICJpZCI6ICJzdzAzX2ZhdGFs
X2FsbF9ldmVudHNfYXJlX2FsYXJtcyIsCiAgICAgICAgIndyb25nX2NsYWltIjogIuuqqOuToCBF
dmVudOyZgCBTdGF0dXPripQgQWxhcm3snLzroZwg66eM65Ok7Ja07JW8IO2VnOuLpC4iLAogICAg
ICAgICJjb3JyZWN0X3J1bGUiOiAiQWxhcm3snYAg7KCV7ZW07KeEIOyLnOqwhCDslYjsl5Ag7Jq0
7KCE7J6QIOyhsOy5mOqwgCDtlYTsmpTtlZwg67mE7KCV7IOBIOyDge2DnOunjCDrjIDsg4HsnLzr
oZwg7ZWY66mwIOuLqOyInCBFdmVudMK3U3RhdHVz7JmAIOq1rOu2hO2VnOuLpC4iLAogICAgICAg
ICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAg
ICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2Nl
aWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9h
bGFybV9lcXVhbHNfdHJpcF9pbnRlcmxvY2siLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICJBbGFy
bSwgVHJpcOqzvCBJbnRlcmxvY2vsnYAg6rCZ7J2AIOq4sOuKpeydtOuLpC4iLAogICAgICAgICJj
b3JyZWN0X3J1bGUiOiAiQWxhcm3snYAg7Jq07KCE7J6QIOyhsOy5mOulvCDsp4Dsm5DtlZjripQg
7KCV67O0IOq4sOuKpeydtOqzoCBUcmlwwrdJbnRlcmxvY2vsnYAg7J6Q64+ZIOuztO2YuCDrmJDr
ipQg64+Z7J6R7KCc7JW9IOuFvOumrOydtOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRh
bCIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAg
ICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAg
IH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9hY2tfY2xlYXJzX2NvbmRpdGlv
biIsCiAgICAgICAgIndyb25nX2NsYWltIjogIkFsYXJt7J2EIEFja25vd2xlZGdl7ZWY66m0IOqz
teyglSDsm5Dsnbjqs7wgQWxhcm0g7KGw6rG07J20IO2VtOygnOuQnOuLpC4iLAogICAgICAgICJj
b3JyZWN0X3J1bGUiOiAiQWNrbm93bGVkZ2XripQg7Jq07KCE7J6QIOyduOyngCDquLDroZ3snbTr
qbAgUHJvY2VzcyBjb25kaXRpb27qs7wgQWN0aXZlIOyDge2DnOulvCDtlbTsoJztlZjsp4Ag7JWK
64qU64ukLiIsCiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAiYWZmZWN0ZWRf
bGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAg
ICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJp
ZCI6ICJzdzAzX2ZhdGFsX3ByaW9yaXR5X2J5X3B2X29ubHkiLAogICAgICAgICJ3cm9uZ19jbGFp
bSI6ICJBbGFybSDsmrDshKDsiJzsnITripQg7Lih7KCV6rCS7J2YIO2BrOq4sOunjOycvOuhnCDs
oJXtlZzri6QuIiwKICAgICAgICAiY29ycmVjdF9ydWxlIjogIkFsYXJtIOyasOyEoOyInOychOuK
lCDqsrDqs7wg7Ius6rCB64+E7JmAIO2XiOyaqSDsnZHri7Xsi5zqsITsnYQg7ZWo6ruYIO2Pieqw
gO2VmOyXrCDsoJXtlZzri6QuIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAg
ICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAg
ICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7
CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfZGVhZGJhbmRfZXF1YWxzX2RlbGF5IiwKICAgICAg
ICAid3JvbmdfY2xhaW0iOiAiQWxhcm0gRGVhZGJhbmTsmYAgRGVsYXnripQg6rCZ7J2AIOq4sOuK
peydtOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiRGVhZGJhbmTripQg6rCS7J2YIOuz
teq3gCDsnbTroKXtj63snbTqs6AgRGVsYXnripQg7KGw6rG0IOyngOyGjeyLnOqwhOydhCDsnbTs
mqntlZjripQg7Iuc6rCEIO2VhO2EsOydtOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRh
bCIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAg
ICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAg
IH0sCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9zaGVsdmluZ19kZWxldGVzX2hp
c3RvcnkiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICJTaGVsdmluZ+2VmOuptCBBbGFybSDsoJXs
nZjsmYAg7J2066Cl7J20IOyCreygnOuQnOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAi
U2hlbHZpbmfsnYAg7KCc7ZWc7Iuc6rCEIOuPmeyViCBBY3RpdmUgZGlzcGxheeyXkOyEnCDsnoTs
i5zroZwg7Iio6riw64qUIOq4sOuKpeydtOupsCDsoJXsnZjsmYAg7J2066Cl7J2AIOycoOyngO2V
nOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgImFmZmVjdGVkX2xh
eWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAg
InJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAiaWQi
OiAic3cwM19mYXRhbF9zdXBwcmVzc2lvbl9lcXVhbHNfc2hlbHZpbmciLAogICAgICAgICJ3cm9u
Z19jbGFpbSI6ICJTdXBwcmVzc2lvbuqzvCBTaGVsdmluZ+ydgCDsmrTsoITsnpDqsIAg7J6E7J2Y
66GcIEFsYXJt7J2EIOyIqOq4sOuKlCDrj5nsnbwg6riw64ql7J2064ukLiIsCiAgICAgICAgImNv
cnJlY3RfcnVsZSI6ICJTdXBwcmVzc2lvbuydgCDshKTqs4TrkJwg7IOB7YOcwrfrhbzrpqzsobDq
sbTsl5Ag65Sw66W4IOyekOuPmSDsoJzsmbjsnbTqs6AgU2hlbHZpbmfsnYAg6raM7ZWcIOyeiOuK
lCDsmrTsoITsnpDsnZgg7KCc7ZWc7Iuc6rCEIOyehOyLnCDsobDsuZjsnbTri6QuIiwKICAgICAg
ICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAg
ICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9j
ZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxf
aW5kZWZpbml0ZV9zaGVsdmluZyIsCiAgICAgICAgIndyb25nX2NsYWltIjogIkFsYXJtIFNoZWx2
aW5n7J2AIOyCrOycoOyZgCDrp4zro4zsi5zqsIQg7JeG7J20IOustOq4sO2VnCDsnKDsp4DtlbTr
j4Qg65Cc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJTaGVsdmluZ+ydgCDsirnsnbjq
toztlZwsIOyCrOycoCwg7KCc7ZWc7Iuc6rCELCDtkZzsi5wsIOunjOujjOyZgCDrs7XqtaztmZXs
nbjsnYQg6rSA66as7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIs
CiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJE
IgogICAgICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0s
CiAgICAgIHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF92YWx1ZXNfaW50ZXJjaGFuZ2VhYmxl
IiwKICAgICAgICAid3JvbmdfY2xhaW0iOiAi7Jq07KCEIFNldHBvaW50LCBBbGFybSB2YWx1ZSwg
VHJpcCB2YWx1ZeyZgCBJbnRlcmxvY2sgdmFsdWXripQg7ISc66GcIOuwlOq+uOyWtCDsgqzsmqnt
lbTrj4Qg65Cc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLrhKQg6rCS7J2AIOuqqeyg
geqzvCDshozsnKDqtozsnbQg64uk66W066+A66GcIOq3vOqxsOyZgCDrs4Dqsr3qtIDrpqzrpbwg
67aE66as7ZW07JW8IO2VnOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAg
ICAgImFmZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAg
ICAgIF0sCiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAg
IHsKICAgICAgICAiaWQiOiAic3cwM19mYXRhbF9zb2Vfd2l0aG91dF9zeW5jIiwKICAgICAgICAi
d3JvbmdfY2xhaW0iOiAi7Iuc6rCB64+Z6riw6rCAIOyXhuyWtOuPhCBTT0XsnZgg7J2067Kk7Yq4
IOyEoO2bhOq0gOqzhOuKlCDtla3sg4Eg7KCV7ZmV7ZWY64ukLiIsCiAgICAgICAgImNvcnJlY3Rf
cnVsZSI6ICJTT0XsnZgg7J246rO87Iic7ISc66W8IOyLoOuisO2VmOugpOuptCDqs7XthrUg7Iuc
6rCE64+Z6riwLCBUaW1lc3RhbXAg7Lac7LKYLCDsoJXtmZXrj4TsmYAgVGltZSBxdWFsaXR56rCA
IO2VhOyalO2VmOuLpC4iLAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgImFm
ZmVjdGVkX2xheWVycyI6IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0s
CiAgICAgICAgInJlY29tbWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0sCiAgICAgIHsKICAg
ICAgICAiaWQiOiAic3cwM19mYXRhbF9oaXN0b3JpYW5fZXF1YWxzX3NvZSIsCiAgICAgICAgIndy
b25nX2NsYWltIjogIkhpc3RvcmlhbiDtkZzrs7jsi5zqsITrp4zsnLzroZwgU09F7JmAIOuPmeyd
vO2VnCDsnbTrsqTtirgg7Iic7ISc66W8IO2VreyDgSDsnqztmITtlaAg7IiYIOyeiOuLpC4iLAog
ICAgICAgICJjb3JyZWN0X3J1bGUiOiAiSGlzdG9yaWFuIOy2lOyEuOyZgCBTT0Ug7J2067Kk7Yq4
7Iic7ISc64qUIO2RnOuzuOyjvOq4sOyZgCBUaW1lc3RhbXAg7Lac7LKY6rCAIOuLpOultOuvgOuh
nCDrj5nsnbztlZjri6Tqs6Ag64uo7KCV7ZWgIOyImCDsl4bri6QuIiwKICAgICAgICAic2V2ZXJp
dHkiOiAiZmF0YWwiLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAgICAiQyIs
CiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAgICJyZWNvbW1lbmRlZF9jZWlsaW5nIjog
MTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfZmF0YWxfYXVkaXRfZXF1
YWxzX3NvZSIsCiAgICAgICAgIndyb25nX2NsYWltIjogIkF1ZGl0IHRyYWls6rO8IFNPReuKlCDr
j5nsnbztlZwg6riw66Gd7J2064ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBdWRpdCB0
cmFpbOydgCDsgqzsmqnsnpAg7ZaJ7JyE7JmAIOuzgOqyveydhCDquLDroZ3tlZjqs6AgU09F64qU
IOqzteyglcK37ISk67mEIOyDge2DnOuzgO2ZlOydmCDsiJzshJzrpbwg6riw66Gd7ZWc64ukLiIs
CiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjog
WwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAgICAicmVjb21t
ZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJpZCI6ICJzdzAz
X2ZhdGFsX2JyaWdodF9jb2xvcnMiLAogICAgICAgICJ3cm9uZ19jbGFpbSI6ICJIaWdoLXBlcmZv
cm1hbmNlIEhNSeuKlCDrsJ3snYAg7IOJ7J2EIOunjuydtCDsgqzsmqntlaDsiJjroZ0g7IOB7Zmp
7J247Iud7J20IOyii+yVhOynhOuLpC4iLAogICAgICAgICJjb3JyZWN0X3J1bGUiOiAiSGlnaC1w
ZXJmb3JtYW5jZSBITUnripQg7IOJ7IOB7J2EIOygnO2VnOuQnCDruYTsoJXsg4Eg7J2Y66+47JeQ
IOydvOq0gOuQmOqyjCDsgqzsmqntlZjsl6wg7Iuc6rCB7KCBIOyasOyEoOyInOychOulvCDrp4zr
k6Dri6QuIiwKICAgICAgICAic2V2ZXJpdHkiOiAiZmF0YWwiLAogICAgICAgICJhZmZlY3RlZF9s
YXllcnMiOiBbCiAgICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdLAogICAgICAg
ICJyZWNvbW1lbmRlZF9jZWlsaW5nIjogMTUuMAogICAgICB9LAogICAgICB7CiAgICAgICAgImlk
IjogInN3MDNfZmF0YWxfdW5yZXN0cmljdGVkX2F1dGhvcml0eSIsCiAgICAgICAgIndyb25nX2Ns
YWltIjogIuyatOyghOyekOyXkOqyjCDrqqjrk6AgU2V0cG9pbnTsmYAg67O07Zi46rSA66CoIOqw
kuydhCDsoJztlZwg7JeG7J20IOuzgOqyve2VmOqyjCDtlbTslbwg7JWI7KCE7ZWY64ukLiIsCiAg
ICAgICAgImNvcnJlY3RfcnVsZSI6ICLspJHsmpQg6rCS6rO8IOyhsOyekeydgCDsl63tlaDquLDr
sJgg7LWc7IaM6raM7ZWcLCDsirnsnbgsIO2ZleyduOqzvCBBdWRpdCB0cmFpbOuhnCDthrXsoJzt
lbTslbwg7ZWc64ukLiIsCiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAiYWZm
ZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwK
ICAgICAgICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAg
ICAgICJpZCI6ICJzdzAzX2ZhdGFsX2NvbW1hbmRfcHJvdmVzX2FjdGlvbiIsCiAgICAgICAgIndy
b25nX2NsYWltIjogIkhNSeyXkOyEnCDrqoXroLnsnYQg7KCE7Iah7ZWY66m0IO2YhOyepeyEpOu5
hCDrj5nsnpHsnbQg7JmE66OM65CcIOqyg+ycvOuhnCDtjJDri6jtlZzri6QuIiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIuuqheuguSDsoITshqHqs7wg7Iuk7KCcIEZlZWRiYWNr7J2EIOu2hOum
rO2VmOqzoCBUaW1lb3V0wrfrtojsnbzsuZjCt+2SiOyniOyDge2DnOulvCDtmZXsnbjtlbTslbwg
7ZWc64ukLiIsCiAgICAgICAgInNldmVyaXR5IjogImZhdGFsIiwKICAgICAgICAiYWZmZWN0ZWRf
bGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXSwKICAgICAg
ICAicmVjb21tZW5kZWRfY2VpbGluZyI6IDE1LjAKICAgICAgfSwKICAgICAgewogICAgICAgICJp
ZCI6ICJzdzAzX2ZhdGFsX3JhaXNlX2FsbF9wcmlvcml0aWVzIiwKICAgICAgICAid3JvbmdfY2xh
aW0iOiAiQWxhcm0gZmxvb2TripQg66qo65OgIEFsYXJtIOyasOyEoOyInOychOulvCDrhpLsnbTr
qbQg7ZW06rKw65Cc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJBbGFybSBmbG9vZOuK
lCDsm5Dsnbgg7KCc6rGwLCDtlanrpqztmZQsIENoYXR0ZXJpbmcg6rCc7ISgLCDsg4Htg5zquLDr
sJggU3VwcHJlc3Npb27qs7wg7ZmU66m0wrfsoIjssKgg6rCc7ISg7Jy866GcIOykhOyduOuLpC4i
LAogICAgICAgICJzZXZlcml0eSI6ICJmYXRhbCIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6
IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0sCiAgICAgICAgInJlY29t
bWVuZGVkX2NlaWxpbmciOiAxNS4wCiAgICAgIH0KICAgIF0sCiAgICAic2FmZV9jb25kaXRpb25z
IjogWwogICAgICAiQWxhcm3qs7wgVHJpcOydgCDsl7Dqs4TrkKAg7IiYIOyeiOyngOunjCDrqqns
oIHqs7wg7Iuk7ZaJ7KO87LK06rCAIOuLpOultOuLpC4iLAogICAgICAi66qo65OgIEV2ZW506rCA
IEFsYXJt7J24IOqyg+ydgCDslYTri4jri6QuIiwKICAgICAgIkFja25vd2xlZGdl64qUIOyatOyg
hOyekCDsnbjsp4Drpbwg6riw66Gd7ZWY66mwIOqzteygleyhsOqxtCDtlbTsoJzsmYAg67OE6rCc
7J2064ukLiIsCiAgICAgICJEZWFkYmFuZOyZgCBEZWxheeuKlCDrqqjrkZAgQ2hhdHRlcmluZ+yd
hCDspITsnbwg7IiYIOyeiOycvOuCmCDqsJIg6riw67CY6rO8IOyLnOqwhCDquLDrsJjsnLzroZwg
6rWs67aE65Cc64ukLiIsCiAgICAgICJTaGVsdmluZyDspJHsl5Drj4QgQWxhcm0g7J2066Cl6rO8
IOyCrOyaqeq4sOuhneydgCDsnKDsp4DtlZzri6QuIiwKICAgICAgIlN1cHByZXNzaW9u7J2AIOyE
pOqzhOuQnCDsmrTsoITsg4Htg5wg7KGw6rG07JeQIOuUsOudvCDsnpDrj5kg7KCB7Jqp7ZWgIOyI
mCDsnojri6QuIiwKICAgICAgIkhpZ2gtcGVyZm9ybWFuY2UgSE1J64+EIOydmOuvuOqwgCDrqoXt
mZXtlZwg7KCc7ZWc65CcIOyDieyDgeydhCDsgqzsmqntlZzri6QuIiwKICAgICAgIlRyaXAg6rCS
6rO8IEFsYXJtIOqwkuydmCDsg4HrjIDsiJzshJzripQg6rO17KCVIOychO2XmOuwqe2WpeqzvCDs
nZHri7Xsi5zqsITsl5Ag65Sw6528IOygle2VnOuLpC4iLAogICAgICAiSW50ZXJsb2NrIHZhbHVl
64qUIOyXsOyGjSDsiJjsuZjqsIAg7JWE64uI6528IOydtOyCsCDsg4Htg5wg65iQ64qUIOuFvOum
rOyhsOqxtOydvCDsiJgg7J6I64ukLiIsCiAgICAgICJTT0Ug7KCV7ZmV64+E64qUIOyLnOqwhOuP
meq4sOyZgCDsnqXsuZggVGltZXN0YW1wIO2SiOyniOyXkCDsnZjsobTtlZzri6QuIiwKICAgICAg
Ikhpc3RvcmlhbuydgCBTT0Ug67aE7ISd7J2EIOuztOyZhO2VoCDsiJgg7J6I7KeA66eMIO2VreyD
gSDrjIDssrTtlZjsp4DripQg7JWK64qU64ukLiIsCiAgICAgICJGaXJzdC1vdXTqs7wgU09F66W8
IO2VqOq7mCDsgqzsmqntlZjrqbQg7LWc7LSIIOybkOyduOqzvCDsoITssrQg7KCE7YyM7Iic7ISc
66W8IOu5hOq1kO2VoCDsiJgg7J6I64ukLiIsCiAgICAgICJBdWRpdCB0cmFpbOydgCDsgqzsmqns
npAg7ZaJ7JyEIOy2lOyggeyXkCDspJHsoJDsnYQg65GU64ukLiIsCiAgICAgICLruYTsg4HsoIjs
sKjsl5DshJzrj4Qg6raM7ZWcIO2ZleuMgOyZgCDsgqztm4QgQXVkaXQg6riw66GdIOyhsOqxtOyd
hCDrqoXtmZXtnogg7ZW07JW8IO2VnOuLpC4iLAogICAgICAiQWxhcm0gcHJpb3JpdHnripQg7ZiE
7J6lIOyyoO2VmeyXkCDsoJXsnZjrkJwg6rKw6rO87JmAIOydkeuLteyLnOqwhCDquLDspIDsnYQg
65Sw66W464ukLiIsCiAgICAgICJTaGVsdmluZyDtl4jsmqnsi5zqsITsnYAgQWxhcm0g7Yq57ISx
6rO8IO2YhOyepSDsoJXssYXsl5Ag65Sw6528IOuLrOudvOyniCDsiJgg7J6I64ukLiIsCiAgICAg
ICJEaXNwbGF5IGhpZXJhcmNoeeydmCDshLjrtoAgTGV2ZWwg66qF7Lmt7J2AIOyLnOyKpO2FnOyX
kCDrlLDrnbwg64us652864+EIOyDgeychCBPdmVydmlld+yZgCDsg4HshLgg7KeE64uo7J2YIO2d
kOumhOydgCDsnKDsp4DtlZzri6QuIiwKICAgICAgIlNDQURBIOq1rOyEseydgCDspJHslZnsp5Hs
pJHtmJUsIOu2hOyCsO2YlSDrmJDripQg6rCA7IOB7ZmUIOq1rOyhsOqwgCDqsIDriqXtlZjri6Qu
IgogICAgXSwKICAgICJtYWpvcl9jaGVja3MiOiBbCiAgICAgIHsKICAgICAgICAiaWQiOiAic3cw
M19tYWpvcl9hcmNoaXRlY3R1cmVfd2l0aG91dF9xdWFsaXR5IiwKICAgICAgICAic2V2ZXJpdHki
OiAibWFqb3IiLAogICAgICAgICJtZXNzYWdlIjogIkhNScK3U0NBREEg6rWs7KGw66W8IOuCmOyX
tO2WiOycvOuCmCDthrXsi6Dri6jsoIgsIEZhaWxvdmVyLCDrjbDsnbTthLAg7ZKI7KeI6rO8IFN0
YWxlIO2RnOyLnOqwgCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi6rWs
7KGwIOyEpOuqheyXkOuKlCDsmrTsoITsnpDqsIAg642w7J207YSwIOyLoOuisOyDge2DnOulvCDt
jJDri6jtlZjripQg6rK966Gc6rCAIO2PrO2VqOuQmOyWtOyVvCDtlZzri6QuIiwKICAgICAgICAi
Y29ycmVjdF9ydWxlIjogIuyEnOuyhMK37Ya17IugwrfsoJzslrTquLAg6rWs7KGw7JmAIO2VqOq7
mCBGYWlsb3Zlciwg7ZKI7KeILCBTdGFsZSDrsI8g7J6s7Jew6rKwIOydvOy5mOyEseydhCDsl7Dq
srDtlZzri6QuIiwKICAgICAgICAiY29uZGl0aW9uIjogIuusuO2VreydtCBITUnCt1NDQURBIOq1
rOyhsOyZgCDsi6DrorDshLHsnYQg7JqU6rWs7ZWY6rOgIO2SiOyniMK37J6l7JWg7ZGc7ZiE7J20
IOu2gOyhse2VnCDqsr3smrAiLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAgICAgICAg
ICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAi
aWQiOiAic3cwM19tYWpvcl9obWlfd2l0aG91dF9oaWVyYXJjaHkiLAogICAgICAgICJzZXZlcml0
eSI6ICJtYWpvciIsCiAgICAgICAgIm1lc3NhZ2UiOiAiSGlnaC1wZXJmb3JtYW5jZSBITUkg7JuQ
7LmZ7J2EIOyWuOq4ie2WiOycvOuCmCBPdmVydmlldywg7ZmU66m06rOE7Li1LCDstpTshLjsmYAg
66el6529IOycoOyngOqwgCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi
64uo7Iic7ZWcIOyDieyDgSDqt5zsuZnrp4zsnLzroZzripQg7IOB7Zmp7J247IudIOyEpOqzhOul
vCDshKTrqoXtlZjquLAg7Ja066C164ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJPdmVy
dmlld+yXkOyEnCDsnbTsg4HsnYQg7LC+6rOgIOyDgeyEuO2ZlOuptOyXkOyEnCDsm5Dsnbjqs7wg
7KGw7LmY66W8IO2ZleyduO2VmOuKlCDqs4TsuLXqs7wg66el65297J2EIOygnOyLnO2VnOuLpC4i
LAogICAgICAgICJjb25kaXRpb24iOiAi66y47ZWt7J20IOqzoOyEseuKpSBITUkg7ISk6rOE66W8
IOyalOq1rO2VmOqzoCDtmZTrqbTqs4TsuLXCt+yDge2ZqeyduOyLneydtCDrtoDsobHtlZwg6rK9
7JqwIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAg
ICAgIkQiCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfbWFq
b3JfcmF0aW9uYWxpemF0aW9uX21pc3NpbmdfcmVzcG9uc2UiLAogICAgICAgICJzZXZlcml0eSI6
ICJtYWpvciIsCiAgICAgICAgIm1lc3NhZ2UiOiAiQWxhcm0gcmF0aW9uYWxpemF0aW9u7JeQ7ISc
IOqysOqzvCwg7Jq07KCE7J6QIOyhsOy5mOyZgCDtl4jsmqkg7J2R64u17Iuc6rCE7J2YIOyXsOqy
sOydtCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAiQWxhcm0g7ZWE7JqU
7ISx6rO8IOyasOyEoOyInOychOuKlCDsmrTsoITsnpAg7KGw7LmYIOqwgOuKpeyEseyXkCDqt7zq
sbDtlbTslbwg7ZWc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLsm5Dsnbgt6rKw6rO8
LeyhsOy5mC3snZHri7Xsi5zqsIQt7Jqw7ISg7Iic7JyELeyEpOygleqwkuydhCDtlZjrgpjsnZgg
7Iq57J246re86rGw66GcIOyXsOqysO2VnOuLpC4iLAogICAgICAgICJjb25kaXRpb24iOiAi66y4
7ZWt7J20IEFsYXJtIHJhdGlvbmFsaXphdGlvbuydhCDsmpTqtaztlZjqs6Ag7KGw7LmYwrfsnZHr
i7Xsi5zqsITsnbQg67aA7KGx7ZWcIOqyveyasCIsCiAgICAgICAgImFmZmVjdGVkX2xheWVycyI6
IFsKICAgICAgICAgICJDIiwKICAgICAgICAgICJEIgogICAgICAgIF0KICAgICAgfSwKICAgICAg
ewogICAgICAgICJpZCI6ICJzdzAzX21ham9yX2FsYXJtX3RyZWF0bWVudF9jb25mdXNpb24iLAog
ICAgICAgICJzZXZlcml0eSI6ICJtYWpvciIsCiAgICAgICAgIm1lc3NhZ2UiOiAiRGVhZGJhbmQs
IERlbGF5LCBTaGVsdmluZ+qzvCBTdXBwcmVzc2lvbuydmCDrqqnsoIHqs7wg7KCB7Jqp7KGw6rG0
IOq1rOu2hOydtCDrtoDsobHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi64SkIOq4
sOuKpeydgCDqsJIg7J2066Cl7Y+tLCDsi5zqsITtlYTthLAsIOyatOyghOyekCDsnoTsi5zsobDs
uZgsIOyEpOqzhOyDgSDsnpDrj5nsoJzsmbjroZwg6rWs67aE65Cc64ukLiIsCiAgICAgICAgImNv
cnJlY3RfcnVsZSI6ICLqsIEg6riw64ql7J2YIFRyaWdnZXIsIOyggeyaqeyjvOyytCwg6riw6rCE
LCDsnbTroKXqs7wg67O16reA7KGw6rG07J2EIOu5hOq1kO2VnOuLpC4iLAogICAgICAgICJjb25k
aXRpb24iOiAi66y47ZWt7J20IG51aXNhbmNlIGFsYXJtIOqwnOyEoOydhCDsmpTqtaztlZjqs6Ag
66mU7Luk64uI7KaYIOq1rOu2hOydtCDrtoDsobHtlZwg6rK97JqwIiwKICAgICAgICAiYWZmZWN0
ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAg
ICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfbWFqb3Jfc2V0cG9pbnRfZ292ZXJuYW5j
ZSIsCiAgICAgICAgInNldmVyaXR5IjogIm1ham9yIiwKICAgICAgICAibWVzc2FnZSI6ICJTZXRw
b2ludMK3QWxhcm3Ct1RyaXDCt0ludGVybG9jayDqsJLsnYAg6rWs67aE7ZaI7Jy864KYIOq3vOqx
sCwg6raM7ZWcLCDrs4Dqsr3snbTroKXqs7wg67O16rWs7KCI7LCo6rCAIOu2gOyhse2VmOuLpC4i
LAogICAgICAgICJkZXNjcmlwdGlvbiI6ICLqsJIg6rSA66asIOusuOygnOuKlCDsiKvsnpDrqqnr
oZ3rs7Tri6Qg7IaM7Jyg6raM6rO8IOuzgOqyve2GteygnOqwgCDtlbXsi6zsnbTri6QuIiwKICAg
ICAgICAiY29ycmVjdF9ydWxlIjogIlRhZ8K364uo7JyEwrfrsKntlqXCt+q3vOqxsMK37Iq57J24
wrfrs4Dqsr3snbTroKXCt+yggeyaqeuqqOuTnMK367O16rWs66W8IFNldHBvaW50IGxpc3Tsl5Ag
7Jew6rKw7ZWc64ukLiIsCiAgICAgICAgImNvbmRpdGlvbiI6ICLrrLjtla3snbQg6rCSIOq0gOum
rOyZgCDrs4Dqsr3thrXsoJzrpbwg7JqU6rWs7ZWY6rOgIOqxsOuyhOuEjOyKpOqwgCDrtoDsobHt
lZwg6rK97JqwIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAog
ICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3
MDNfbWFqb3Jfc29lX3dpdGhvdXRfdGltZV9xdWFsaXR5IiwKICAgICAgICAic2V2ZXJpdHkiOiAi
bWFqb3IiLAogICAgICAgICJtZXNzYWdlIjogIlNPReulvCDsnbTrsqTtirgg66qp66Gd7Jy866Gc
66eMIOyEpOuqhe2VmOqzoCDsi5zqsIHrj5nquLAsIFNvdXJjZSB0aW1lc3RhbXAsIOu2hO2VtOuK
peqzvCBUaW1lIHF1YWxpdHnqsIAg67aA7KGx7ZWY64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9u
IjogIuyEoO2bhOq0gOqzhCDrtoTshJ3snZgg7Iug66Kw64+E64qUIOyLnOqwhOq4sOuwmCDtkojs
p4jsl5Ag7KKM7Jqw65Cc64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICLqs7XthrUg7Iuc
6rCBLCBUaW1lc3RhbXAg7JyE7LmYLCDsoJXtmZXrj4TCt+u2hO2VtOuKpcK37Ya17Iug7KeA7Jew
wrdUaW1lIHF1YWxpdHnrpbwg7KCc7Iuc7ZWc64ukLiIsCiAgICAgICAgImNvbmRpdGlvbiI6ICLr
rLjtla3snbQgU09FIOybkOyduOu2hOyEneydhCDsmpTqtaztlZjqs6Ag7Iuc6rCE7ZKI7KeIIOyE
pOuqheydtCDrtoDsobHtlZwg6rK97JqwIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwog
ICAgICAgICAgIkMiLAogICAgICAgICAgIkQiCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAg
ICAgICAgImlkIjogInN3MDNfbWFqb3JfYXV0aG9yaXR5X2F1ZGl0IiwKICAgICAgICAic2V2ZXJp
dHkiOiAibWFqb3IiLAogICAgICAgICJtZXNzYWdlIjogIuyatOyghOyekCDqtoztlZzsnYQg7Ja4
6riJ7ZaI7Jy864KYIOyXre2VoOq4sOuwmCDstZzshozqtoztlZwsIOykkeyalOyhsOyekSDtmZXs
nbjqs7wgQXVkaXQgdHJhaWzsnbQg67aA7KGx7ZWY64ukLiIsCiAgICAgICAgImRlc2NyaXB0aW9u
IjogIuq2jO2VnOydgCDsgqzsmqnsnpAg65Ox6riJ66eM7J20IOyVhOuLiOudvCDrjIDsg4HCt+q4
sOuKpcK366qo65OcwrfshLjshZjCt+uzgOqyveq4sOuhneycvOuhnCDthrXsoJztlZzri6QuIiwK
ICAgICAgICAiY29ycmVjdF9ydWxlIjogIuyXre2VoCwg67KU7JyELCDsnqztmZXsnbjCt+ydtOyk
keyKueyduCwg7IS47IWY6rO8IOyCrOyaqeyekCDtlonsnITquLDroZ3snYQg7Jew6rKw7ZWc64uk
LiIsCiAgICAgICAgImNvbmRpdGlvbiI6ICLrrLjtla3snbQg7Jq07KCE7J6QIOq2jO2VnOqzvCBI
dW1hbiBlcnJvciDrsKnsp4Drpbwg7JqU6rWs7ZWY6rOgIO2GteygnOqwgCDrtoDsobHtlZwg6rK9
7JqwIiwKICAgICAgICAiYWZmZWN0ZWRfbGF5ZXJzIjogWwogICAgICAgICAgIkMiLAogICAgICAg
ICAgIkQiCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgImlkIjogInN3MDNfbWFq
b3JfYWJub3JtYWxfbWFuYWdlbWVudCIsCiAgICAgICAgInNldmVyaXR5IjogIm1ham9yIiwKICAg
ICAgICAibWVzc2FnZSI6ICLruYTsoJXsg4Hsg4Htmakg64yA7J2R7JeQ7IScIERldGVjdC1EaWFn
bm9zZS1SZXNwb25kLVJlY292ZXIg7Z2Q66aE6rO8IEFsYXJtIGZsb29kIOuMgOyxheydtCDrtoDs
obHtlZjri6QuIiwKICAgICAgICAiZGVzY3JpcHRpb24iOiAi7ZGc7Iuc7JmAIOqyveuztOuKlCDr
sJzqsqzsl5DshJwg67O16rWs7JmAIOyCrO2bhOu2hOyEneq5jOyngCDsnbTslrTsoLjslbwg7ZWc
64ukLiIsCiAgICAgICAgImNvcnJlY3RfcnVsZSI6ICJPdmVydmlld8K3VHJlbmTCt0FsYXJtwrfs
oIjssKjCt+q2jO2VnMK367O16rWswrfsgqztm4QgS1BJ66W8IO2VmOuCmOydmCDrjIDsnZHtnZDr
poTsnLzroZwg7Jew6rKw7ZWc64ukLiIsCiAgICAgICAgImNvbmRpdGlvbiI6ICLrrLjtla3snbQg
QWJub3JtYWwgc2l0dWF0aW9uIG1hbmFnZW1lbnTrpbwg7JqU6rWs7ZWY6rOgIOuMgOydkcK367O1
6rWs6rCAIOu2gOyhse2VnCDqsr3smrAiLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiOiBbCiAg
ICAgICAgICAiQyIsCiAgICAgICAgICAiRCIKICAgICAgICBdCiAgICAgIH0KICAgIF0sCiAgICAi
ZmVlZGJhY2tfdGVtcGxhdGVzIjogewogICAgICAiZmF0YWwiOiAi7ZW17IusIOyatOyghOygleuz
tCDqtIDrpqwg7JuQ66as6rCAIOuwmOuMgOuhnCDshJzsiKDrkJjsl4jsirXri4jri6Q6IHttZXNz
YWdlfSIsCiAgICAgICJtYWpvciI6ICLshKTqs4TsobDqsbQg65iQ64qUIOq0gOumrO2GteygnOqw
gCDrtoDsobHtlanri4jri6Q6IHttZXNzYWdlfSIsCiAgICAgICJ3YXJuIjogIuusuO2VrSDrspTs
nIQg65iQ64qUIOuztOyhsOyhsOqxtOydtCDrtoDsobHtlanri4jri6Q6IHttZXNzYWdlfSIKICAg
IH0sCiAgICAibmV4dF9wcmFjdGljZV9wb2ludHMiOiBbCiAgICAgICJBbGFybSBsaWZlY3ljbGXq
s7wgQWNrbm93bGVkZ2XCt1JldHVybi10by1ub3JtYWwg7IOB7YOc66W8IOuPhOyLne2ZlO2VnOuL
pC4iLAogICAgICAiQWxhcm0gcmF0aW9uYWxpemF0aW9uIO2RnOyXkCDqsrDqs7wsIOyhsOy5mCwg
7J2R64u17Iuc6rCE6rO8IOyasOyEoOyInOychOulvCDsl7DqsrDtlZzri6QuIiwKICAgICAgIlNl
dHBvaW50wrdBbGFybcK3VHJpcMK3SW50ZXJsb2NrIOqwkuydmCDrqqnsoIHqs7wg67OA6rK96raM
7ZWc7J2EIOq1rOu2hO2VnOuLpC4iLAogICAgICAiU09FwrdIaXN0b3JpYW7Ct0F1ZGl0IHRyYWls
7J2YIOq4sOuhneuMgOyDgeqzvCDsi5zqsITquLDrsJjsnYQg67mE6rWQ7ZWc64ukLiIKICAgIF0s
CiAgICAiZmFsc2VfcG9zaXRpdmVfY2F1dGlvbnMiOiBbCiAgICAgICJBbGFybeydtCBUcmlw7J2E
IOycoOuwnO2VnOuLpOqzoCDtkZztmITtlbTrj4Qg65GQIOq4sOuKpeydhCDrj5nsnbzsi5ztlZjs
p4Ag7JWK7Jy866m0IGZhdGFs66GcIOuztOyngCDslYrripTri6QuIiwKICAgICAgIlNoZWx2aW5n
7J20IO2ZlOuptOqzvCDsnYztlqXsl5DshJwgQWxhcm3snYQg7Iio6ri064uk64qUIOyEpOuqheyd
gCDsnbTroKUg7IKt7KCcIOyjvOyepeqzvCDqtazrtoTtlZzri6QuIiwKICAgICAgIlN1cHByZXNz
aW9u7J20IO2KueyglSDsobDqsbTsl5DshJwgQWxhcm0g7IOd7ISx7J2EIOunieuKlOuLpOuKlCDs
hKTrqoXsnYAg7KCV7IOB7KCB7J24IOyEpOqzhOq4sOuKpeydvCDsiJgg7J6I64ukLiIsCiAgICAg
ICJEZWFkYmFuZOyZgCBEZWxheeqwgCDrqqjrkZAgQ2hhdHRlcmluZ+ydhCDspITsnbjri6Tqs6Ag
7ZW064+EIOqwmeydgCDrqZTsu6Tri4jsppjsnbTrnbzqs6Ag64uo7KCV7ZWY7KeAIOyViuycvOup
tCDtl4jsmqntlZzri6QuIiwKICAgICAgIkhpZ2gtcGVyZm9ybWFuY2UgSE1J6rCAIOyDieyDgeyd
hCDsgqzsmqntlZzri6Tqs6Ag7ZW064+EIOygnO2VnOyggcK37J286rSA65CcIOydmOuvuOudvOup
tCDsmKTrpZjqsIAg7JWE64uI64ukLiIsCiAgICAgICJBbGFybeqzvCBUcmlwIOqwkuydmCDsnbzr
sJjsoIHsnbgg7IOB64yA7Iic7ISc66W8IOygnOyLnO2VtOuPhCDqs7XsoJXrsKntlqXqs7wg6re8
6rGw66W8IO2VnOygle2VmOuptCDtl4jsmqntlZzri6QuIiwKICAgICAgIkhpc3RvcmlhbuydhCBT
T0Ug67aE7ISd7JeQIO2ZnOyaqe2VnOuLpOqzoCDtlbTrj4Qg7ZWt7IOBIOuPmeydvO2VmOuLpOqz
oCDri6jsoJXtlZjsp4Ag7JWK7Jy866m0IO2XiOyaqe2VnOuLpC4iLAogICAgICAiRmlyc3Qtb3V0
6rO8IFNPReulvCDtlajqu5gg7JuQ7J2467aE7ISd7JeQIOyCrOyaqe2VnOuLpOuKlCDshKTrqoXs
nYAgb3duZXJzaGlwIOy5qOuylOydtCDslYTri4jri6QuIiwKICAgICAgIuu5hOyDgeygiOywqOyX
kOyEnCDsnoTsi5wg6raM7ZWcIO2ZleuMgOulvCDshKTrqoXtlbTrj4Qg7Iq57J24wrfsi5zqsITs
oJztlZzCt+yCrO2bhOq4sOuhneydhCDtj6ztlajtlZjrqbQg7ZeI7Jqp7ZWc64ukLiIsCiAgICAg
ICJITUnCt1NDQURB7J2YIOq1rOyytOyggeyduCDshJzrsoTsiJjsmYAg7ZmU66m0IExldmVsIOuq
hey5reydgCDsi5zsiqTthZzrs4Qg7LCo7J2066W8IO2XiOyaqe2VnOuLpC4iCiAgICBdLAogICAg
Im91dHB1dF9jb250cmFjdCI6IHsKICAgICAgInJlcXVpcmVkX2ZpZWxkcyI6IFsKICAgICAgICAi
aWQiLAogICAgICAgICJzZXZlcml0eSIsCiAgICAgICAgIm1lc3NhZ2UiLAogICAgICAgICJjb3Jy
ZWN0X3J1bGUiLAogICAgICAgICJhZmZlY3RlZF9sYXllcnMiCiAgICAgIF0sCiAgICAgICJhbGxv
d2VkX3NldmVyaXR5IjogWwogICAgICAgICJmYXRhbCIsCiAgICAgICAgIm1ham9yIiwKICAgICAg
ICAid2FybiIsCiAgICAgICAgImluZm8iCiAgICAgIF0sCiAgICAgICJmYXRhbF9yZXF1aXJlc19k
aXJlY3Rfb3Bwb3NpdGVfY2xhaW0iOiB0cnVlLAogICAgICAiY2l0ZV9hbnN3ZXJfZXZpZGVuY2Ui
OiB0cnVlCiAgICB9CiAgfSwKICAicmV2aXNpb25fbm90ZXMiOiBbCiAgICAiMjAyNi0wOC0wNjog
7Jq07KCE7KCV67O0IOq0gOumrOyZgCBTVy0wMiDsi6TtlonrhbzrpqzsnZggb3duZXJzaGlwIOqy
veqzhOulvCDrsJjsmIHtlojri6QuIiwKICAgICJGYXRhbCDqsoDsgqzripQg7KeB7KCR7KCB7J24
IOuwmOuMgCDri6jsoJXrrLjsl5Drp4wg67CY7J2R7ZWY64+E66GdIGV4YWN0LWxpbmUg67O07KGw
7Yyo7YS07Jy866GcIOygnO2VnO2WiOuLpC4iLAogICAgIkFsYXJtIHRyZWF0bWVudCwgU09FIOyL
nOqwhO2SiOyniCwg6raM7ZWc6rO8IEF1ZGl07J2YIG1ham9yIOqygOyCrOulvCDstpTqsIDtlojr
i6QuIgogIF0sCiAgInRvcGljX2xhYmVsIjogIlNXLTAzIEhNScK3U0NBREHCt0FsYXJtwrdTT0Ui
Cn0K
PAYLOAD_SW03_04

    write_payload 'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/model_answer.json' '5d39a524114f60163721ec70af8249f20b6698d05a8bc97bc6f18f7d6198b01f' <<'PAYLOAD_SW03_05'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLm1vZGVsX2Fuc3dlci52MSIsCiAgInRv
cGljX2lkIjogImhtaV9zY2FkYV9hbGFybV9zZXRwb2ludF90cmlwX2ludGVybG9ja19zb2Vfb3Bl
cmF0b3JfaW5mb3JtYXRpb25fbWFuYWdlbWVudCIsCiAgInRpdGxlX2tvIjogIkhNScK3U0NBREHC
t0FsYXJtwrdTZXRwb2ludMK3VHJpcMK3SW50ZXJsb2NrwrdTT0Ug67CPIOyatOyghOygleuztCDq
tIDrpqwiLAogICJxdWVzdGlvbl90eXBlIjogIlBSSU5DSVBMRV9JTlRFUlBSRVRBVElPTiIsCiAg
ImV4cGVjdGVkX3F1ZXN0aW9uX3BhdHRlcm5zIjogWwogICAgewogICAgICAicGF0dGVybiI6ICJI
TUnsmYAgU0NBREHsnZgg6rWs7KGwLCDquLDriqUg67CPIOyLoOuisOyEsSDshKTqs4TquLDspIDs
nYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAgICJpbnRlbnQiOiAi6rCQ7Iuc6rWs7KGw7JmAIOya
tOyghOygleuztCDsi6DrorDshLEiLAogICAgICAicmVxdWlyZWRfYW5jaG9yX2lkcyI6IFsKICAg
ICAgICAic3cwM19obWlfc2NhZGFfYXJjaGl0ZWN0dXJlIiwKICAgICAgICAic3cwM19hcmNoaXRl
Y3R1cmVfcmVkdW5kYW5jeV9xdWFsaXR5IiwKICAgICAgICAic3cwM19kYXRhX3F1YWxpdHlfZGlz
cGxheSIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgInBhdHRlcm4iOiAiSGlnaC1wZXJmb3Jt
YW5jZSBITUnsnZgg7ISk6rOE7JuQ7LmZ6rO8IO2ZlOuptOqzhOy4teydhCDshKTrqoXtlZjsi5zs
mKQuIiwKICAgICAgImludGVudCI6ICLsg4Htmansnbjsi50g7KSR7IusIO2ZlOuptOyEpOqzhCIs
CiAgICAgICJyZXF1aXJlZF9hbmNob3JfaWRzIjogWwogICAgICAgICJzdzAzX2hpZ2hfcGVyZm9y
bWFuY2VfaG1pIiwKICAgICAgICAic3cwM19kaXNwbGF5X2hpZXJhcmNoeSIsCiAgICAgICAgInN3
MDNfY29sb3JfY29udGV4dF9uYXZpZ2F0aW9uIgogICAgICBdCiAgICB9LAogICAgewogICAgICAi
cGF0dGVybiI6ICJBbGFybSBwaGlsb3NvcGh57JmAIEFsYXJtIHJhdGlvbmFsaXphdGlvbuydmCDr
qqnsoIEg67CPIOygiOywqOulvCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICAgImludGVudCI6ICLq
sr3rs7TsoJXssYXqs7wg6rCc67OE6rK967O0IOyKueyduCIsCiAgICAgICJyZXF1aXJlZF9hbmNo
b3JfaWRzIjogWwogICAgICAgICJzdzAzX2FsYXJtX3BoaWxvc29waHkiLAogICAgICAgICJzdzAz
X2FsYXJtX3JhdGlvbmFsaXphdGlvbiIsCiAgICAgICAgInN3MDNfYWxhcm1fcHJpb3JpdHkiCiAg
ICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJwYXR0ZXJuIjogIkFsYXJtIHByaW9yaXR5LCBEZWFk
YmFuZOyZgCBEZWxheeydmCDshKDsoJXquLDspIDsnYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAg
ICJpbnRlbnQiOiAi6rK967O0IOyasOyEoOyInOychOyZgCBudWlzYW5jZSDsoIDqsJAiLAogICAg
ICAicmVxdWlyZWRfYW5jaG9yX2lkcyI6IFsKICAgICAgICAic3cwM19hbGFybV9wcmlvcml0eSIs
CiAgICAgICAgInN3MDNfYWxhcm1fZGVhZGJhbmQiLAogICAgICAgICJzdzAzX2FsYXJtX2RlbGF5
IgogICAgICBdCiAgICB9LAogICAgewogICAgICAicGF0dGVybiI6ICJBbGFybSBTaGVsdmluZ+qz
vCBTdXBwcmVzc2lvbuydmCDssKjsnbTsmYAg6rSA66as67Cp7JWI7J2EIOyEpOuqhe2VmOyLnOyY
pC4iLAogICAgICAiaW50ZW50IjogIuyehOyLnCDsiKjquYDqs7wg7IOB7YOc6riw67CYIOyekOuP
meygnOyZuCIsCiAgICAgICJyZXF1aXJlZF9hbmNob3JfaWRzIjogWwogICAgICAgICJzdzAzX2Fs
YXJtX3NoZWx2aW5nIiwKICAgICAgICAic3cwM19hbGFybV9zdXBwcmVzc2lvbiIsCiAgICAgICAg
InN3MDNfYXVkaXRfdHJhaWwiCiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJwYXR0ZXJuIjog
IlNldHBvaW50LCBBbGFybSB2YWx1ZSwgVHJpcCB2YWx1ZeyZgCBJbnRlcmxvY2sgdmFsdWXsnZgg
7LCo7J20IOuwjyDqtIDrpqzquLDspIDsnYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAgICJpbnRl
bnQiOiAi6rCS7J2YIOuqqeyggcK37IaM7Jyg6raMwrfrs4Dqsr3qtIDrpqwiLAogICAgICAicmVx
dWlyZWRfYW5jaG9yX2lkcyI6IFsKICAgICAgICAic3cwM19zZXRwb2ludF92YWx1ZV9jbGFzc2Vz
IiwKICAgICAgICAic3cwM19zZXRwb2ludF9nb3Zlcm5hbmNlIiwKICAgICAgICAic3cwM19hbGFy
bV90cmlwX2ludGVybG9ja19ib3VuZGFyeSIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgInBh
dHRlcm4iOiAiU09F7J2YIOybkOumrOyZgCDsi5zqsIHrj5nquLAsIEhpc3RvcmlhbiDrsI8gRmly
c3Qtb3V06rO87J2YIOq0gOqzhOulvCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICAgImludGVudCI6
ICLsnbTrsqTtirgg7ISg7ZuE6rSA6rOE7JmAIOybkOyduOu2hOyEnSIsCiAgICAgICJyZXF1aXJl
ZF9hbmNob3JfaWRzIjogWwogICAgICAgICJzdzAzX3NvZV9kZWZpbml0aW9uIiwKICAgICAgICAi
c3cwM190aW1lX3N5bmNfcmVzb2x1dGlvbiIsCiAgICAgICAgInN3MDNfaGlzdG9yaWFuX3ZzX3Nv
ZSIsCiAgICAgICAgInN3MDNfZmlyc3Rfb3V0X3JlbGF0aW9uIgogICAgICBdCiAgICB9LAogICAg
ewogICAgICAicGF0dGVybiI6ICLsmrTsoITsoJXrs7Qg7Iuc7Iqk7YWc7J2YIEF1ZGl0IHRyYWls
6rO8IOyatOyghOyekCDqtoztlZwg6rSA66as67Cp7JWI7J2EIOyEpOuqhe2VmOyLnOyYpC4iLAog
ICAgICAiaW50ZW50IjogIuyCrOyaqeyekCDtlonsnITsmYAg7KSR7JqU7KGw7J6RIO2GteygnCIs
CiAgICAgICJyZXF1aXJlZF9hbmNob3JfaWRzIjogWwogICAgICAgICJzdzAzX2F1ZGl0X3RyYWls
IiwKICAgICAgICAic3cwM19vcGVyYXRvcl9hdXRob3JpdHkiLAogICAgICAgICJzdzAzX2h1bWFu
X2Vycm9yX3ByZXZlbnRpb24iCiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJwYXR0ZXJuIjog
IkFsYXJtIGZsb29k7JmAIENoYXR0ZXJpbmfsnZgg66y47KCc7KCQIOuwjyDqsJzshKDrsKnslYjs
nYQg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAgICJpbnRlbnQiOiAi6rK967O06rO867aA7ZWYIOyn
hOuLqOqzvCDqsJzshKAiLAogICAgICAicmVxdWlyZWRfYW5jaG9yX2lkcyI6IFsKICAgICAgICAi
c3cwM19hbGFybV9mbG9vZF9jaGF0dGVyaW5nIiwKICAgICAgICAic3cwM19hbGFybV9wZXJmb3Jt
YW5jZV9rcGkiLAogICAgICAgICJzdzAzX2FsYXJtX3JhdGlvbmFsaXphdGlvbiIKICAgICAgXQog
ICAgfSwKICAgIHsKICAgICAgInBhdHRlcm4iOiAiSE1JwrdTQ0FEQeulvCDsnbTsmqntlZwgQWJu
b3JtYWwgc2l0dWF0aW9uIG1hbmFnZW1lbnQg67Cp7JWI7J2EIOyEpOuqhe2VmOyLnOyYpC4iLAog
ICAgICAiaW50ZW50IjogIuuwnOqyrMK37KeE64uowrfrjIDsnZHCt+uzteq1rCIsCiAgICAgICJy
ZXF1aXJlZF9hbmNob3JfaWRzIjogWwogICAgICAgICJzdzAzX2Fibm9ybWFsX3NpdHVhdGlvbl9t
YW5hZ2VtZW50IiwKICAgICAgICAic3cwM19oaWdoX3BlcmZvcm1hbmNlX2htaSIsCiAgICAgICAg
InN3MDNfYWxhcm1fc3RhdGVfYWNrbm93bGVkZ2VtZW50IiwKICAgICAgICAic3cwM19kYXRhX3F1
YWxpdHlfZGlzcGxheSIKICAgICAgXQogICAgfQogIF0sCiAgInJlY29tbWVuZGVkX291dGxpbmUi
OiBbCiAgICB7CiAgICAgICJzZWN0aW9uIjogIjEuIOuwsOqyveqzvCBTVy0wMyDshozsnKDrspTs
nIQiLAogICAgICAiaW50ZW50IjogIuyatOyghOygleuztCDqtIDrpqzsnZgg66qp7KCB6rO8IFNX
LTAywrdTVy0wNMK3U1ctMTAg6rK96rOE66W8IOygnOyLnO2VnOuLpC4iLAogICAgICAiYW5jaG9y
X3JlZnMiOiBbCiAgICAgICAgInN3MDNfc2NvcGVfb3BlcmF0b3JfaW5mb3JtYXRpb24iLAogICAg
ICAgICJzdzAzX3N3MDJfYm91bmRhcnkiLAogICAgICAgICJzdzAzX3N3MDRfc3cxMF9ib3VuZGFy
eSIKICAgICAgXQogICAgfSwKICAgIHsKICAgICAgInNlY3Rpb24iOiAiMi4gSE1JwrdTQ0FEQSDq
tazsobDsmYAg7KCV67O07Iug66Kw7ISxIiwKICAgICAgImludGVudCI6ICLqsJDsi5zqtazsobAs
IEZhaWxvdmVyLCDrjbDsnbTthLAg7ZKI7KeI6rO8IO2GteyLoOuLqOygiCDtkZzsi5zrpbwg7ISk
66qF7ZWc64ukLiIsCiAgICAgICJhbmNob3JfcmVmcyI6IFsKICAgICAgICAic3cwM19obWlfc2Nh
ZGFfYXJjaGl0ZWN0dXJlIiwKICAgICAgICAic3cwM19hcmNoaXRlY3R1cmVfcmVkdW5kYW5jeV9x
dWFsaXR5IiwKICAgICAgICAic3cwM19kYXRhX3F1YWxpdHlfZGlzcGxheSIKICAgICAgXQogICAg
fSwKICAgIHsKICAgICAgInNlY3Rpb24iOiAiMy4gSGlnaC1wZXJmb3JtYW5jZSBITUnsmYAg7ZmU
66m06rOE7Li1IiwKICAgICAgImludGVudCI6ICJPdmVydmlldywg7IOB7IS47ZmU66m0LCDstpTs
hLgsIOyDieyDgeqzvCDrp6Xrnb3snYQg7IOB7Zmp7J247IudIOq0gOygkOyXkOyEnCDsl7DqsrDt
lZzri6QuIiwKICAgICAgImFuY2hvcl9yZWZzIjogWwogICAgICAgICJzdzAzX2hpZ2hfcGVyZm9y
bWFuY2VfaG1pIiwKICAgICAgICAic3cwM19kaXNwbGF5X2hpZXJhcmNoeSIsCiAgICAgICAgInN3
MDNfY29sb3JfY29udGV4dF9uYXZpZ2F0aW9uIgogICAgICBdCiAgICB9LAogICAgewogICAgICAi
c2VjdGlvbiI6ICI0LiBBbGFybSDssqDtlZnCt+2VqeumrO2ZlMK37Jqw7ISg7Iic7JyEIiwKICAg
ICAgImludGVudCI6ICJBbGFybeydmCDsoJXsnZgsIOyDgeychOygleyxhSwg7JuQ7J24LeqysOqz
vC3sobDsuZgt7J2R64u17Iuc6rCE6rO8IOyasOyEoOyInOychOulvCDshKTrqoXtlZzri6QuIiwK
ICAgICAgImFuY2hvcl9yZWZzIjogWwogICAgICAgICJzdzAzX2FsYXJtX2RlZmluaXRpb24iLAog
ICAgICAgICJzdzAzX2FsYXJtX3BoaWxvc29waHkiLAogICAgICAgICJzdzAzX2FsYXJtX3JhdGlv
bmFsaXphdGlvbiIsCiAgICAgICAgInN3MDNfYWxhcm1fcHJpb3JpdHkiCiAgICAgIF0KICAgIH0s
CiAgICB7CiAgICAgICJzZWN0aW9uIjogIjUuIEFsYXJtIOyDge2DnOyZgCBOdWlzYW5jZSDqtIDr
pqwiLAogICAgICAiaW50ZW50IjogIkFjdGl2ZcK3QWNrbm93bGVkZ2XCt1JldHVybi10by1ub3Jt
YWzqs7wgRGVhZGJhbmQsIERlbGF5LCBTaGVsdmluZywgU3VwcHJlc3Npb27snYQg67mE6rWQ7ZWc
64ukLiIsCiAgICAgICJhbmNob3JfcmVmcyI6IFsKICAgICAgICAic3cwM19hbGFybV9zdGF0ZV9h
Y2tub3dsZWRnZW1lbnQiLAogICAgICAgICJzdzAzX2FsYXJtX2RlYWRiYW5kIiwKICAgICAgICAi
c3cwM19hbGFybV9kZWxheSIsCiAgICAgICAgInN3MDNfYWxhcm1fc2hlbHZpbmciLAogICAgICAg
ICJzdzAzX2FsYXJtX3N1cHByZXNzaW9uIgogICAgICBdCiAgICB9LAogICAgewogICAgICAic2Vj
dGlvbiI6ICI2LiBTZXRwb2ludMK3QWxhcm3Ct1RyaXDCt0ludGVybG9jayDqsJIg6rSA66asIiwK
ICAgICAgImludGVudCI6ICLqsJLsnZgg66qp7KCB6rO8IOyGjOycoOq2jCwgU2V0cG9pbnQgbGlz
dCwg6raM7ZWc6rO8IOuzgOqyveydtOugpeydhCDsoJzsi5ztlZzri6QuIiwKICAgICAgImFuY2hv
cl9yZWZzIjogWwogICAgICAgICJzdzAzX3NldHBvaW50X3ZhbHVlX2NsYXNzZXMiLAogICAgICAg
ICJzdzAzX3NldHBvaW50X2dvdmVybmFuY2UiLAogICAgICAgICJzdzAzX2FsYXJtX3RyaXBfaW50
ZXJsb2NrX2JvdW5kYXJ5IgogICAgICBdCiAgICB9LAogICAgewogICAgICAic2VjdGlvbiI6ICI3
LiBTT0XCt0hpc3RvcmlhbsK3Rmlyc3Qtb3V0wrdBdWRpdCB0cmFpbCIsCiAgICAgICJpbnRlbnQi
OiAi6riw66Gd64yA7IOBLCBUaW1lc3RhbXAsIOyLnOqwgeuPmeq4sCwg7ISg7ZuE6rSA6rOE7JmA
IOyCrOyaqeyekCDtlonsnITquLDroZ3snYQg6rWs67aE7ZWc64ukLiIsCiAgICAgICJhbmNob3Jf
cmVmcyI6IFsKICAgICAgICAic3cwM19zb2VfZGVmaW5pdGlvbiIsCiAgICAgICAgInN3MDNfdGlt
ZV9zeW5jX3Jlc29sdXRpb24iLAogICAgICAgICJzdzAzX2hpc3Rvcmlhbl92c19zb2UiLAogICAg
ICAgICJzdzAzX2ZpcnN0X291dF9yZWxhdGlvbiIsCiAgICAgICAgInN3MDNfYXVkaXRfdHJhaWwi
CiAgICAgIF0KICAgIH0sCiAgICB7CiAgICAgICJzZWN0aW9uIjogIjguIOq2jO2VnMK3SHVtYW4g
ZXJyb3LCt+u5hOygleyDgeyDge2ZqSDrjIDsnZEiLAogICAgICAiaW50ZW50IjogIuyXre2VoOq4
sOuwmCDqtoztlZwsIOuqheugucK3RmVlZGJhY2sg7ZmV7J246rO8IERldGVjdC1EaWFnbm9zZS1S
ZXNwb25kLVJlY292ZXIg7Z2Q66aE7J2EIOqysOuhoOycvOuhnCDsoJXrpqztlZzri6QuIiwKICAg
ICAgImFuY2hvcl9yZWZzIjogWwogICAgICAgICJzdzAzX29wZXJhdG9yX2F1dGhvcml0eSIsCiAg
ICAgICAgInN3MDNfaHVtYW5fZXJyb3JfcHJldmVudGlvbiIsCiAgICAgICAgInN3MDNfYWxhcm1f
Zmxvb2RfY2hhdHRlcmluZyIsCiAgICAgICAgInN3MDNfYWxhcm1fcGVyZm9ybWFuY2Vfa3BpIiwK
ICAgICAgICAic3cwM19hYm5vcm1hbF9zaXR1YXRpb25fbWFuYWdlbWVudCIKICAgICAgXQogICAg
fQogIF0sCiAgImhpZ2hfc2NvcmVfcG9pbnRzIjogWwogICAgIkFsYXJt7J2EIOyatOyghOyekCDs
obDsuZjqsIAg7ZWE7JqU7ZWcIOu5hOygleyDgSDsg4Htg5zroZwg7KCV7J2Y7ZWY6rOgIOuLqOyI
nCBFdmVudMK3U3RhdHVz7JmAIOq1rOu2hO2VnOuLpC4iLAogICAgIkhNSeyZgCBTQ0FEQeydmCDs
l63tlaDsnYQg7ZmU66m0IOyduO2EsO2OmOydtOyKpOyZgCDsg4HsnIQg6rCQ7IucwrfrjbDsnbTt
hLDsiJjsp5Eg6rWs7KGw66GcIOq1rOu2hO2VnOuLpC4iLAogICAgIkZhaWxvdmVyLCDthrXsi6Dr
i6jsoIgsIEJhZMK3U3RhbGUgcXVhbGl0eeyZgCDsnqzsl7DqsrAg7IOB7YOc66W8IOyatOyghOye
kCDsoJXrs7Tsi6DrorDshLHqs7wg7Jew6rKw7ZWc64ukLiIsCiAgICAiSGlnaC1wZXJmb3JtYW5j
ZSBITUnrpbwgT3ZlcnZpZXcsIO2ZlOuptOqzhOy4tSwg7LaU7IS4LCDsoJztlZzrkJwg7IOJ7IOB
6rO8IOunpeudvSDsnKDsp4DroZwg7ISk66qF7ZWc64ukLiIsCiAgICAiQWxhcm0gcGhpbG9zb3Bo
eeyZgCByYXRpb25hbGl6YXRpb27snYQg7IOB7JyE7KCV7LGF6rO8IOqwnOuzhCBBbGFybSDsirns
nbjtmZzrj5nsnLzroZwg6rWs67aE7ZWc64ukLiIsCiAgICAiQWxhcm0gcHJpb3JpdHnrpbwg6rKw
6rO8IOyLrOqwgeuPhOyZgCDtl4jsmqkg7J2R64u17Iuc6rCE7Jy866GcIOqysOygle2VnOuLpC4i
LAogICAgIkFja25vd2xlZGdl6rCAIOybkOyduCDsoJzqsbAg65iQ64qUIFJldHVybi10by1ub3Jt
YWzsnYQg7J2Y66+47ZWY7KeAIOyViuuKlOuLpOqzoCDshKTrqoXtlZzri6QuIiwKICAgICJEZWFk
YmFuZOyZgCBEZWxheeulvCDqsJIg6riw67CYIOydtOugpe2PreqzvCDsi5zqsIQg6riw67CYIO2V
hO2EsOuhnCDqtazrtoTtlZzri6QuIiwKICAgICJTaGVsdmluZ+qzvCBTdXBwcmVzc2lvbuydhCDs
oIHsmqnso7zssrQsIOyhsOqxtCwg7KCc7ZWc7Iuc6rCELCDsnbTroKXqs7wg67O16reA66GcIOu5
hOq1kO2VnOuLpC4iLAogICAgIkFsYXJtIGZsb29kLCBDaGF0dGVyaW5nLCBTdGFuZGluZyBhbGFy
beqzvCBLUEnrpbwg67CY67O16rCc7ISg7JeQIOyXsOqysO2VnOuLpC4iLAogICAgIlNldHBvaW50
wrdBbGFybcK3VHJpcMK3SW50ZXJsb2NrIOqwkuydhCDrqqnsoIHCt+yGjOycoOq2jMK367OA6rK9
6raM7ZWc7Jy866GcIOq1rOu2hO2VnOuLpC4iLAogICAgIlNldHBvaW50IGxpc3Tsl5Ag64uo7JyE
LCDrsKntlqUsIOyggeyaqeuqqOuTnCwg6re86rGwLCDsirnsnbjqs7wg67OA6rK97J2066Cl7J2E
IO2PrO2VqO2VnOuLpC4iLAogICAgIlNPReulvCBTb3VyY2UgdGltZXN0YW1wLCDsi5zqsIHrj5nq
uLAsIOu2hO2VtOuKpeqzvCBUaW1lIHF1YWxpdHnroZwg7ISk66qF7ZWc64ukLiIsCiAgICAiSGlz
dG9yaWFuLCBTT0UsIEZpcnN0LW91dOqzvCBBdWRpdCB0cmFpbOydmCDquLDroZ3rjIDsg4Hqs7wg
67aE7ISd66qp7KCB7J2EIOq1rOu2hO2VnOuLpC4iLAogICAgIuyatOyghOyekCDqtoztlZzsnYQg
7Jet7ZWg6riw67CYIOy1nOyGjOq2jO2VnCwg7KSR7JqU7KGw7J6RIO2ZleyduOqzvCBBdWRpdCB0
cmFpbOuhnCDthrXsoJztlZzri6QuIiwKICAgICJDb21tYW5k7JmAIEZlZWRiYWNr7J2EIOu2hOum
rO2VmOqzoCBNb2RlwrdJbnRlcmxvY2sg7IKs7Jygwrfrs7Xqtazqsr3roZzroZwgSHVtYW4gZXJy
b3Lrpbwg7KSE7J2464ukLiIsCiAgICAi67mE7KCV7IOB7IOB7Zmp7J2EIERldGVjdC1EaWFnbm9z
ZS1SZXNwb25kLVJlY292ZXIg7Z2Q66aE7Jy866GcIOyEpOuqhe2VnOuLpC4iLAogICAgIlNXLTAy
IOyLpO2WieuFvOumrCwgU1ctMDQgViZWLCBTVy0xMCDtlITroZzsoJ3tirgg7J247IiY7JmAIG93
bmVyc2hpcOydhCDrtoTrpqztlZzri6QuIgogIF0sCiAgImNvbW1vbl9taXNzaW5nX3BvaW50cyI6
IFsKICAgICJITUnsmYAgU0NBREHrpbwg6rCZ7J2AIOyepey5mOuqheycvOuhnOunjCDshKTrqoXt
laguIiwKICAgICLshJzrsoTCt+2GteyLoOq1rOyhsOulvCDshKTrqoXtlZjqs6Ag642w7J207YSw
IO2SiOyniOqzvCBGYWlsb3ZlciDtkZzsi5zrpbwg64iE65297ZWoLiIsCiAgICAiSGlnaC1wZXJm
b3JtYW5jZSBITUnrpbwg64uo7IicIOyDieyDgSDrs4Dqsr3snLzroZzrp4wg7ISk66qF7ZWoLiIs
CiAgICAi66qo65OgIEV2ZW5066W8IEFsYXJt7Jy866GcIOqwhOyjvO2VqC4iLAogICAgIkFsYXJt
IHBoaWxvc29waHnsmYAgcmF0aW9uYWxpemF0aW9u7J2YIOqzhOy4teq0gOqzhOulvCDriITrnb3t
laguIiwKICAgICLsmrDshKDsiJzsnITrpbwg7Lih7KCV6rCSIO2BrOq4sOuCmCDsnqXruYQg7KSR
7JqU64+EIO2VmOuCmOuhnOunjCDqsrDsoJXtlaguIiwKICAgICJBY2tub3dsZWRnZeyZgCBSZXR1
cm4tdG8tbm9ybWFs7J2EIO2YvOuPme2VqC4iLAogICAgIkRlYWRiYW5kLCBEZWxheSwgU2hlbHZp
bmfqs7wgU3VwcHJlc3Npb27snYQg6rCZ7J2AIG51aXNhbmNlIOuMgOyxheycvOuhnCDshKTrqoXt
laguIiwKICAgICJTaGVsdmluZ+ydmCDqtoztlZzCt+yCrOycoMK366eM66OMwrfsnbTroKXsnYQg
64iE65297ZWoLiIsCiAgICAiU2V0cG9pbnTCt0FsYXJtwrdUcmlwwrdJbnRlcmxvY2sg6rCS7J2Y
IOyGjOycoOq2jOqzvCDrs4Dqsr3thrXsoJzrpbwg64iE65297ZWoLiIsCiAgICAiU09F7JeQ7ISc
IOyLnOqwgeuPmeq4sCwgVGltZXN0YW1wIOy2nOyymOyZgCBUaW1lIHF1YWxpdHnrpbwg64iE6529
7ZWoLiIsCiAgICAiSGlzdG9yaWFuLCBTT0UsIEZpcnN0LW91dOqzvCBBdWRpdCB0cmFpbOydhCDq
sJnsnYAg7J2066Cl6riw64ql7Jy866GcIOyEpOuqhe2VqC4iLAogICAgIuyatOyghOyekCDqtozt
lZzsnYQgTG9naW4g65Ox6riJ66eM7Jy866GcIOyEpOuqhe2VmOqzoCDspJHsmpTsobDsnpEg7ZmV
7J246rO8IEF1ZGl066W8IOuIhOudve2VqC4iLAogICAgIkFsYXJtIGZsb29kIOuMgOyxheydhCDs
mrDshKDsiJzsnIQg7IOB7ZalIOuYkOuKlCBBbGFybSDstpTqsIDroZzrp4wg7KCc7Iuc7ZWoLiIs
CiAgICAiQ29tbWFuZCDsoITshqHrp4zsnLzroZwg7ZiE7J6l7ISk67mEIOuPmeyekeyZhOujjOul
vCDtjJDri6jtlaguIiwKICAgICJTVy0wMuydmCBUcmlwwrdJbnRlcmxvY2sg7IOB7YOc7KCE7J20
7JmAIFNXLTEw7J2YIEZBVMK3U0FU66W8IOuzuCBUb3BpYyDtlbXsi6zsnLzroZwg7ZmV7J6l7ZWo
LiIKICBdLAogICJyb3V0aW5nX2FsaWFzZXMiOiBbCiAgICAiSE1JIFNDQURBIGFsYXJtIG1hbmFn
ZW1lbnQgU09FIiwKICAgICLqs6DshLHriqUgSE1JIOqyveuztCDtlanrpqztmZQgU09FIiwKICAg
ICJITUkgU0NBREEgQWxhcm0gU2V0cG9pbnQgVHJpcCBJbnRlcmxvY2siLAogICAgIuyatOyghOyg
leuztCDqsr3rs7Qg7ISk7KCV6rCSIOydtOuypO2KuOyInOyEnCIsCiAgICAiYWxhcm0gcGhpbG9z
b3BoeSByYXRpb25hbGl6YXRpb24gcHJpb3JpdHkiLAogICAgIuqyveuztCDssqDtlZkg7ZWp66as
7ZmUIOyasOyEoOyInOychCIsCiAgICAiYWxhcm0gZGVhZGJhbmQgZGVsYXkgc2hlbHZpbmcgc3Vw
cHJlc3Npb24iLAogICAgIuqyveuztCDrjbDrk5zrsLTrk5wg7KeA7JewIOyJmOu5mSDslrXsoJwi
LAogICAgInNldHBvaW50IGFsYXJtIHRyaXAgaW50ZXJsb2NrIHZhbHVlIG1hbmFnZW1lbnQiLAog
ICAgIuyEpOygleqwkiDqsr3rs7TqsJIg7Yq466a96rCSIOyduO2EsOuhneqwkiDqtIDrpqwiLAog
ICAgInNlcXVlbmNlIG9mIGV2ZW50cyBhdWRpdCB0cmFpbCB0aW1lIHN5bmNocm9uaXphdGlvbiIs
CiAgICAiU09FIOqwkOyCrOy2lOyggSDsi5zqsIHrj5nquLAiLAogICAgImhpZ2ggcGVyZm9ybWFu
Y2UgSE1JIGRpc3BsYXkgaGllcmFyY2h5IiwKICAgICLqs6DshLHriqUgSE1JIO2ZlOuptOqzhOy4
tSDsg4Htmansnbjsi50iLAogICAgIm9wZXJhdG9yIGF1dGhvcml0eSBodW1hbiBlcnJvciBwcmV2
ZW50aW9uIiwKICAgICLsmrTsoITsnpAg6raM7ZWcIO2ctOuovOyXkOufrCDrsKnsp4AiLAogICAg
ImFsYXJtIGZsb29kIGNoYXR0ZXJpbmcgc3RhbmRpbmcgYWxhcm0iLAogICAgIuqyveuztO2Preyj
vCDssYTthLDrp4Eg7IOB7Iuc6rK967O0IiwKICAgICJhYm5vcm1hbCBzaXR1YXRpb24gbWFuYWdl
bWVudCBITUkgYWxhcm0iLAogICAgIuu5hOygleyDgeyDge2ZqSDqtIDrpqwgU0NBREEg7Jq07KCE
7KCV67O0IgogIF0sCiAgInJvdXRpbmdfZmllbGRfcG9pbnRzIjogWwogICAgImhtaSIsCiAgICAi
c2NhZGEiLAogICAgInN1cGVydmlzb3J5IGNvbnRyb2wiLAogICAgImRhdGEgYWNxdWlzaXRpb24i
LAogICAgImhpZ2gtcGVyZm9ybWFuY2UgaG1pIiwKICAgICJkaXNwbGF5IGhpZXJhcmNoeSIsCiAg
ICAib3ZlcnZpZXcgZGlzcGxheSIsCiAgICAic2l0dWF0aW9uYWwgYXdhcmVuZXNzIiwKICAgICJj
b2xvciBjb2RpbmciLAogICAgIm5hdmlnYXRpb24gY29udGV4dCIsCiAgICAiYWxhcm0gcGhpbG9z
b3BoeSIsCiAgICAiYWxhcm0gcmF0aW9uYWxpemF0aW9uIiwKICAgICJhbGFybSBwcmlvcml0eSIs
CiAgICAiY29uc2VxdWVuY2Ugc2V2ZXJpdHkiLAogICAgIm9wZXJhdG9yIHJlc3BvbnNlIHRpbWUi
LAogICAgImFsYXJtIGFja25vd2xlZGdlbWVudCIsCiAgICAicmV0dXJuIHRvIG5vcm1hbCIsCiAg
ICAiZGVhZGJhbmQiLAogICAgIm9uLWRlbGF5IiwKICAgICJvZmYtZGVsYXkiLAogICAgInNoZWx2
aW5nIiwKICAgICJzdXBwcmVzc2lvbiIsCiAgICAiYWxhcm0gZmxvb2QiLAogICAgImNoYXR0ZXJp
bmcgYWxhcm0iLAogICAgInN0YW5kaW5nIGFsYXJtIiwKICAgICJhbGFybSBwZXJmb3JtYW5jZSBr
cGkiLAogICAgInNldHBvaW50IGxpc3QiLAogICAgImFsYXJtIHZhbHVlIiwKICAgICJ0cmlwIHZh
bHVlIiwKICAgICJpbnRlcmxvY2sgdmFsdWUiLAogICAgInNlcXVlbmNlIG9mIGV2ZW50cyIsCiAg
ICAic29lIiwKICAgICJzb3VyY2UgdGltZXN0YW1wIiwKICAgICJ0aW1lIHN5bmNocm9uaXphdGlv
biIsCiAgICAidGltZSBxdWFsaXR5IiwKICAgICJoaXN0b3JpYW4iLAogICAgImZpcnN0LW91dCIs
CiAgICAiYXVkaXQgdHJhaWwiLAogICAgIm9wZXJhdG9yIGF1dGhvcml0eSIsCiAgICAicm9sZSBi
YXNlZCBhY2Nlc3MiLAogICAgImxlYXN0IHByaXZpbGVnZSIsCiAgICAiaHVtYW4gZXJyb3IgcHJl
dmVudGlvbiIsCiAgICAiZGF0YSBxdWFsaXR5IiwKICAgICJzdGFsZSBkYXRhIiwKICAgICJhYm5v
cm1hbCBzaXR1YXRpb24gbWFuYWdlbWVudCIKICBdLAogICJyZXZpc2lvbl9ub3RlcyI6IFsKICAg
ICIyMDI2LTA4LTA2OiDrjIDtkZwg66y47KCcIDEw6rCc7JmAIDjri6jqs4QgTW9kZWwgQW5zd2Vy
IOq1rOyhsOulvCDtmZXsoJXtlojri6QuIiwKICAgICJITUnCt1NDQURBLCBBbGFybSBsaWZlY3lj
bGUsIFNldHBvaW50IGdvdmVybmFuY2UsIFNPReyZgCDqtoztlZzsnYQg7ZWY64KY7J2YIOyatOyg
hOygleuztCDtnZDrpoTsnLzroZwg7Jew6rKw7ZaI64ukLiIsCiAgICAiU1ctMDIg7Iuk7ZaJ64W8
66as7JmAIFNXLTA0wrdTVy0xMCDsiJjtlonssrTqs4Trpbwg66qF7Iuc7KCB7Jy866GcIOu2hOum
rO2WiOuLpC4iCiAgXQp9Cg==
PAYLOAD_SW03_05

    write_payload 'rubrics/topic_packs/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management/topic_importance.json' '5d936639664912dca2c987d226adaea6180d0d78b033f3de1d3bf9698ef56eae' <<'PAYLOAD_SW03_06'
ewogICJzY2hlbWFfdmVyc2lvbiI6ICJ0b3BpY19wYWNrLnRvcGljX2ltcG9ydGFuY2UudjEiLAog
ICJ0b3BpY19pZCI6ICJobWlfc2NhZGFfYWxhcm1fc2V0cG9pbnRfdHJpcF9pbnRlcmxvY2tfc29l
X29wZXJhdG9yX2luZm9ybWF0aW9uX21hbmFnZW1lbnQiLAogICJkaWZmaWN1bHR5IjogIkRFU0lH
Tl9FVkFMVUFUSU9OIiwKICAic2VsZWN0aW9uX2ltcG9ydGFuY2UiOiAiQ09SRV9NVVNUX1BSRVBB
UkUiLAogICJxdWVzdGlvbl90eXBlIjogIlBSSU5DSVBMRV9JTlRFUlBSRVRBVElPTiIsCiAgImhp
Z2hfYmFuZF91bmxvY2tfY29uZGl0aW9ucyI6IFsKICAgICJITUnCt1NDQURBIOq1rOyhsOulvCDr
jbDsnbTthLAg7ZKI7KeILCBGYWlsb3ZlcuyZgCDsmrTsoITsnpAg7IOB7Zmp7J247Iud7Jy866Gc
IOyXsOqysO2VnOuLpC4iLAogICAgIkhpZ2gtcGVyZm9ybWFuY2UgSE1J7J2YIE92ZXJ2aWV3LCDt
mZTrqbTqs4TsuLUsIOy2lOyEuOyZgCDsoJztlZzrkJwg7IOJ7IOBIOybkOy5meydhCDshKTrqoXt
lZzri6QuIiwKICAgICJBbGFybSBwaGlsb3NvcGh57JmAIHJhdGlvbmFsaXphdGlvbuydhCDqtazr
toTtlZjqs6Ag6rKw6rO8wrfsobDsuZjCt+ydkeuLteyLnOqwhMK37Jqw7ISg7Iic7JyE66W8IOyX
sOqysO2VnOuLpC4iLAogICAgIkFja25vd2xlZGdlLCBSZXR1cm4tdG8tbm9ybWFsLCBEZWFkYmFu
ZCwgRGVsYXksIFNoZWx2aW5n6rO8IFN1cHByZXNzaW9u7J2EIOygle2Zle2eiCDqtazrtoTtlZzr
i6QuIiwKICAgICJTZXRwb2ludMK3QWxhcm3Ct1RyaXDCt0ludGVybG9jayDqsJLsnZgg66qp7KCB
LCDshozsnKDqtowsIOuzgOqyveq2jO2VnOqzvCDsnbTroKXsnYQg7KCc7Iuc7ZWc64ukLiIsCiAg
ICAiU09F7J2YIFNvdXJjZSB0aW1lc3RhbXAsIOyLnOqwgeuPmeq4sCwg67aE7ZW064ql6rO8IFRp
bWUgcXVhbGl0eeulvCDshKTrqoXtlZzri6QuIiwKICAgICJIaXN0b3JpYW4sIEZpcnN0LW91dCwg
U09F7JmAIEF1ZGl0IHRyYWls7J2YIOq4sOuhneuMgOyDgeqzvCDrtoTshJ3rqqnsoIHsnYQg67mE
6rWQ7ZWc64ukLiIsCiAgICAi7Jq07KCE7J6QIOq2jO2VnCwgSHVtYW4gZXJyb3Ig67Cp7KeA7JmA
IERldGVjdC1EaWFnbm9zZS1SZXNwb25kLVJlY292ZXIg7Z2Q66aE7J2EIOygnOyLnO2VnOuLpC4i
CiAgXSwKICAibm90ZSI6ICJITUnCt1NDQURB7JmAIEFsYXJtwrdTT0XripQg7KCc7Ja07Iuc7Iqk
7YWc7J2YIOyatOyghOyEsSwg67mE7KCV7IOB7IOB7ZmpIOuMgOydkeqzvCDsgqzqs6Dsm5Dsnbgg
67aE7ISd7J2EIOyXsOqysO2VmOuKlCDtlbXsi6wg67aE7JW87J2064ukLiDsmqnslrQg64KY7Je0
67O064ukIOygleuztOydmCDrqqnsoIEsIOyatOyghOyekCDsobDsuZgsIOyLnOqwhO2SiOyniCwg
6raM7ZWc6rO8IOydtOugpeq0gOumrOq5jOyngCDshKTrqoXtlbTslbwg6rOg65Od7KCQ7J20IOqw
gOuKpe2VmOuvgOuhnCDtlbXsi6wg7KSA67mEIFRvcGlj7Jy866GcIOu2hOulmO2VnOuLpC4iLAog
ICJyZXZpc2lvbl9ub3RlcyI6IFsKICAgICIyMDI2LTA4LTA2OiBkaWZmaWN1bHR5PURFU0lHTl9F
VkFMVUFUSU9OLCBzZWxlY3Rpb25faW1wb3J0YW5jZT1DT1JFX01VU1RfUFJFUEFSReuhnCDtmZXs
oJXtlojri6QuIiwKICAgICJxdWVzdGlvbl90eXBl7J2AIOyatOyghOygleuztCDquLDriqXsnZgg
7JuQ66aswrfruYTqtZDCt+yEpOqzhO2MkOuLqOydtCDspJHsi6zsnbTrr4DroZwgUFJJTkNJUExF
X0lOVEVSUFJFVEFUSU9O7Jy866GcIOyEpOygle2WiOuLpC4iCiAgXSwKICAidG9waWNfbGFiZWwi
OiAiU1ctMDMgSE1JwrdTQ0FEQcK3QWxhcm3Ct1NPRSIKfQo=
PAYLOAD_SW03_06

    write_payload 'scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py' '775c03be9399d6064d441f4acea5a5fe5d323e0315c733386fce67d5010519a5' <<'PAYLOAD_SW03_07'
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25z
CgppbXBvcnQganNvbgppbXBvcnQgcmUKaW1wb3J0IHVuaXR0ZXN0CmZyb20gcGF0aGxpYiBpbXBv
cnQgUGF0aAoKUk9PVCA9IFBhdGgoX19maWxlX18pLnJlc29sdmUoKS5wYXJlbnRzWzFdClRPUElD
X0lEID0gImhtaV9zY2FkYV9hbGFybV9zZXRwb2ludF90cmlwX2ludGVybG9ja19zb2Vfb3BlcmF0
b3JfaW5mb3JtYXRpb25fbWFuYWdlbWVudCIKUEFDSyA9IFJPT1QgLyAicnVicmljcyIgLyAidG9w
aWNfcGFja3MiIC8gVE9QSUNfSUQKU0hFRVQgPSBST09UIC8gImRvY3MiIC8gInRvcGljX3NoZWV0
cyIgLyBmIntUT1BJQ19JRH0ubWQiCgpFWFBFQ1RFRF9BTkNIT1JfQ09VTlQgPSAzMQpFWFBFQ1RF
RF9GQVRBTF9DT1VOVCA9IDE2CkVYUEVDVEVEX01BSk9SX0NPVU5UID0gOApFWFBFQ1RFRF9BTElB
U19DT1VOVCA9IDIwCkVYUEVDVEVEX0ZJRUxEX1BPSU5UX0NPVU5UID0gNDUKRVhQRUNURURfUEFU
VEVSTl9DT1VOVCA9IDEwCkVYUEVDVEVEX09VVExJTkVfQ09VTlQgPSA4CgpkZWYgbG9hZChuYW1l
OiBzdHIpIC0+IGRpY3Q6CiAgICByZXR1cm4ganNvbi5sb2FkcygoUEFDSyAvIG5hbWUpLnJlYWRf
dGV4dChlbmNvZGluZz0idXRmLTgiKSkKCkZBQ1QgPSBsb2FkKCJmYWN0X2FuY2hvci5qc29uIikK
TE9HSUMgPSBsb2FkKCJsb2dpY19jaGVjay5qc29uIikKTU9ERUwgPSBsb2FkKCJtb2RlbF9hbnN3
ZXIuanNvbiIpCklNUE9SVEFOQ0UgPSBsb2FkKCJ0b3BpY19pbXBvcnRhbmNlLmpzb24iKQoKY2xh
c3MgVG9waWNQYWNrU3RydWN0dXJlVGVzdHModW5pdHRlc3QuVGVzdENhc2UpOgogICAgZGVmIHRl
c3RfcmVxdWlyZWRfZmlsZXNfZXhpc3Qoc2VsZikgLT4gTm9uZToKICAgICAgICByZXF1aXJlZCA9
IFsKICAgICAgICAgICAgU0hFRVQsCiAgICAgICAgICAgIFBBQ0sgLyAiUkVBRE1FLm1kIiwKICAg
ICAgICAgICAgUEFDSyAvICJmYWN0X2FuY2hvci5qc29uIiwKICAgICAgICAgICAgUEFDSyAvICJs
b2dpY19jaGVjay5qc29uIiwKICAgICAgICAgICAgUEFDSyAvICJtb2RlbF9hbnN3ZXIuanNvbiIs
CiAgICAgICAgICAgIFBBQ0sgLyAidG9waWNfaW1wb3J0YW5jZS5qc29uIiwKICAgICAgICBdCiAg
ICAgICAgc2VsZi5hc3NlcnRUcnVlKGFsbChwYXRoLmlzX2ZpbGUoKSBmb3IgcGF0aCBpbiByZXF1
aXJlZCkpCgogICAgZGVmIHRlc3RfdG9waWNfaWRfYW5kX3NjaGVtYV9jb250cmFjdChzZWxmKSAt
PiBOb25lOgogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoRkFDVFsic2NoZW1hX3ZlcnNpb24iXSwg
InRvcGljX3BhY2suZmFjdF9hbmNob3IudjEiKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoTE9H
SUNbInNjaGVtYV92ZXJzaW9uIl0sICJ0b3BpY19wYWNrLmxvZ2ljX2NoZWNrLnYxIikKICAgICAg
ICBzZWxmLmFzc2VydEVxdWFsKE1PREVMWyJzY2hlbWFfdmVyc2lvbiJdLCAidG9waWNfcGFjay5t
b2RlbF9hbnN3ZXIudjEiKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoSU1QT1JUQU5DRVsic2No
ZW1hX3ZlcnNpb24iXSwgInRvcGljX3BhY2sudG9waWNfaW1wb3J0YW5jZS52MSIpCiAgICAgICAg
Zm9yIGRhdGEgaW4gKEZBQ1QsIExPR0lDLCBNT0RFTCwgSU1QT1JUQU5DRSk6CiAgICAgICAgICAg
IHNlbGYuYXNzZXJ0RXF1YWwoZGF0YVsidG9waWNfaWQiXSwgVE9QSUNfSUQpCgogICAgZGVmIHRl
c3RfYW5jaG9yX2NvdW50X2FuZF91bmlxdWVuZXNzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYW5j
aG9ycyA9IEZBQ1RbImFuY2hvcnMiXQogICAgICAgIGlkcyA9IFtpdGVtWyJhbmNob3JfaWQiXSBm
b3IgaXRlbSBpbiBhbmNob3JzXQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwobGVuKGFuY2hvcnMp
LCBFWFBFQ1RFRF9BTkNIT1JfQ09VTlQpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChsZW4oaWRz
KSwgbGVuKHNldChpZHMpKSkKICAgICAgICBzZWxmLmFzc2VydFRydWUoYWxsKGl0ZW1bImlkIl0g
PT0gaXRlbVsiYW5jaG9yX2lkIl0gZm9yIGl0ZW0gaW4gYW5jaG9ycykpCgogICAgZGVmIHRlc3Rf
cmVxdWlyZWRfc2VtYW50aWNfZ3JvdXBzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgaWRzID0ge2l0
ZW1bImFuY2hvcl9pZCJdIGZvciBpdGVtIGluIEZBQ1RbImFuY2hvcnMiXX0KICAgICAgICByZXF1
aXJlZCA9IHsKICAgICAgICAgICAgInN3MDNfaG1pX3NjYWRhX2FyY2hpdGVjdHVyZSIsCiAgICAg
ICAgICAgICJzdzAzX2hpZ2hfcGVyZm9ybWFuY2VfaG1pIiwKICAgICAgICAgICAgInN3MDNfYWxh
cm1fZGVmaW5pdGlvbiIsCiAgICAgICAgICAgICJzdzAzX2FsYXJtX3JhdGlvbmFsaXphdGlvbiIs
CiAgICAgICAgICAgICJzdzAzX2FsYXJtX3ByaW9yaXR5IiwKICAgICAgICAgICAgInN3MDNfYWxh
cm1fc3RhdGVfYWNrbm93bGVkZ2VtZW50IiwKICAgICAgICAgICAgInN3MDNfYWxhcm1fZGVhZGJh
bmQiLAogICAgICAgICAgICAic3cwM19hbGFybV9kZWxheSIsCiAgICAgICAgICAgICJzdzAzX2Fs
YXJtX3NoZWx2aW5nIiwKICAgICAgICAgICAgInN3MDNfYWxhcm1fc3VwcHJlc3Npb24iLAogICAg
ICAgICAgICAic3cwM19zZXRwb2ludF9nb3Zlcm5hbmNlIiwKICAgICAgICAgICAgInN3MDNfc29l
X2RlZmluaXRpb24iLAogICAgICAgICAgICAic3cwM190aW1lX3N5bmNfcmVzb2x1dGlvbiIsCiAg
ICAgICAgICAgICJzdzAzX2F1ZGl0X3RyYWlsIiwKICAgICAgICAgICAgInN3MDNfb3BlcmF0b3Jf
YXV0aG9yaXR5IiwKICAgICAgICAgICAgInN3MDNfYWJub3JtYWxfc2l0dWF0aW9uX21hbmFnZW1l
bnQiLAogICAgICAgICAgICAic3cwM19zdzAyX2JvdW5kYXJ5IiwKICAgICAgICAgICAgInN3MDNf
c3cwNF9zdzEwX2JvdW5kYXJ5IiwKICAgICAgICB9CiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKHJl
cXVpcmVkIDw9IGlkcykKCiAgICBkZWYgdGVzdF9mYXRhbF9jb3VudF9hbmRfc2hhcGUoc2VsZikg
LT4gTm9uZToKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihGQUNUWyJmYXRhbF93cm9uZ19j
bGFpbXMiXSksIEVYUEVDVEVEX0ZBVEFMX0NPVU5UKQogICAgICAgIGRldCA9IExPR0lDWyJkZXRl
cm1pbmlzdGljX2NoZWNrcyJdWyJmYXRhbF9jaGVja3MiXQogICAgICAgIGxsbSA9IExPR0lDWyJs
bG1fcHJvZmlsZSJdWyJmYXRhbF9jb25kaXRpb25zIl0KICAgICAgICBzZWxmLmFzc2VydEVxdWFs
KGxlbihkZXQpLCBFWFBFQ1RFRF9GQVRBTF9DT1VOVCkKICAgICAgICBzZWxmLmFzc2VydEVxdWFs
KGxlbihsbG0pLCBFWFBFQ1RFRF9GQVRBTF9DT1VOVCkKICAgICAgICBzZWxmLmFzc2VydFRydWUo
YWxsKGl0ZW1bInNldmVyaXR5Il0gPT0gImZhdGFsIiBmb3IgaXRlbSBpbiBkZXQpKQoKICAgIGRl
ZiB0ZXN0X2xvZ2ljX3Byb2ZpbGVfY29udHJhY3Qoc2VsZikgLT4gTm9uZToKICAgICAgICBwcm9m
aWxlID0gTE9HSUNbImxsbV9wcm9maWxlIl0KICAgICAgICBzZWxmLmFzc2VydFRydWUocHJvZmls
ZVsiZW5hYmxlZCJdKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwobGVuKHByb2ZpbGVbIm1ham9y
X2NoZWNrcyJdKSwgRVhQRUNURURfTUFKT1JfQ09VTlQpCiAgICAgICAgc2VsZi5hc3NlcnRHcmVh
dGVyRXF1YWwobGVuKHByb2ZpbGVbImZhbHNlX3Bvc2l0aXZlX2NhdXRpb25zIl0pLCAxMCkKICAg
ICAgICBzZWxmLmFzc2VydFRydWUocHJvZmlsZVsib3V0cHV0X2NvbnRyYWN0Il1bImZhdGFsX3Jl
cXVpcmVzX2RpcmVjdF9vcHBvc2l0ZV9jbGFpbSJdKQoKICAgIGRlZiB0ZXN0X21vZGVsX3JlZmVy
ZW5jZXNfYXJlX3ZhbGlkKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYW5jaG9yX2lkcyA9IHtpdGVt
WyJhbmNob3JfaWQiXSBmb3IgaXRlbSBpbiBGQUNUWyJhbmNob3JzIl19CiAgICAgICAgc2VsZi5h
c3NlcnRFcXVhbChsZW4oTU9ERUxbImV4cGVjdGVkX3F1ZXN0aW9uX3BhdHRlcm5zIl0pLCBFWFBF
Q1RFRF9QQVRURVJOX0NPVU5UKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwobGVuKE1PREVMWyJy
ZWNvbW1lbmRlZF9vdXRsaW5lIl0pLCBFWFBFQ1RFRF9PVVRMSU5FX0NPVU5UKQogICAgICAgIGZv
ciBwYXR0ZXJuIGluIE1PREVMWyJleHBlY3RlZF9xdWVzdGlvbl9wYXR0ZXJucyJdOgogICAgICAg
ICAgICBzZWxmLmFzc2VydFRydWUoc2V0KHBhdHRlcm5bInJlcXVpcmVkX2FuY2hvcl9pZHMiXSkg
PD0gYW5jaG9yX2lkcykKICAgICAgICBmb3Igc2VjdGlvbiBpbiBNT0RFTFsicmVjb21tZW5kZWRf
b3V0bGluZSJdOgogICAgICAgICAgICBzZWxmLmFzc2VydFRydWUoc2V0KHNlY3Rpb25bImFuY2hv
cl9yZWZzIl0pIDw9IGFuY2hvcl9pZHMpCgogICAgZGVmIHRlc3Rfcm91dGluZ19jb3VudHNfYW5k
X25vX2Jyb2FkX2FsaWFzKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYWxpYXNlcyA9IE1PREVMWyJy
b3V0aW5nX2FsaWFzZXMiXQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwobGVuKGFsaWFzZXMpLCBF
WFBFQ1RFRF9BTElBU19DT1VOVCkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihNT0RFTFsi
cm91dGluZ19maWVsZF9wb2ludHMiXSksIEVYUEVDVEVEX0ZJRUxEX1BPSU5UX0NPVU5UKQogICAg
ICAgIGZvcmJpZGRlbiA9IHsiSE1JIiwgIlNDQURBIiwgIkFsYXJtIiwgIlNPRSIsICJTZXRwb2lu
dCIsICLqsr3rs7QiLCAi7Jq07KCE7KCV67O0In0KICAgICAgICBzZWxmLmFzc2VydEZhbHNlKGZv
cmJpZGRlbiAmIHNldChhbGlhc2VzKSkKCiAgICBkZWYgdGVzdF9pbXBvcnRhbmNlX2NvbnRyYWN0
KHNlbGYpIC0+IE5vbmU6CiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChJTVBPUlRBTkNFWyJkaWZm
aWN1bHR5Il0sICJERVNJR05fRVZBTFVBVElPTiIpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChJ
TVBPUlRBTkNFWyJzZWxlY3Rpb25faW1wb3J0YW5jZSJdLCAiQ09SRV9NVVNUX1BSRVBBUkUiKQog
ICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoSU1QT1JUQU5DRVsicXVlc3Rpb25fdHlwZSJdLCAiUFJJ
TkNJUExFX0lOVEVSUFJFVEFUSU9OIikKICAgICAgICBzZWxmLmFzc2VydEdyZWF0ZXJFcXVhbChs
ZW4oSU1QT1JUQU5DRVsiaGlnaF9iYW5kX3VubG9ja19jb25kaXRpb25zIl0pLCA4KQoKICAgIGRl
ZiB0ZXN0X3Njb3BlX2JvdW5kYXJpZXNfYXJlX2V4cGxpY2l0KHNlbGYpIC0+IE5vbmU6CiAgICAg
ICAgdGV4dCA9ICJcbiIuam9pbihpdGVtWyJzdGF0ZW1lbnQiXSBmb3IgaXRlbSBpbiBGQUNUWyJh
bmNob3JzIl0pCiAgICAgICAgc2VsZi5hc3NlcnRJbigiU1ctMDIiLCB0ZXh0KQogICAgICAgIHNl
bGYuYXNzZXJ0SW4oIlNXLTA0IiwgdGV4dCkKICAgICAgICBzZWxmLmFzc2VydEluKCJTVy0xMCIs
IHRleHQpCiAgICAgICAgc2VsZi5hc3NlcnRJbigi7Iuk7KCcIOuFvOumrOq1rOyhsCIsIHRleHQp
CiAgICAgICAgc2VsZi5hc3NlcnRJbigiVi1Nb2RlbCIsIHRleHQpCiAgICAgICAgc2VsZi5hc3Nl
cnRJbigiRkFUIiwgdGV4dCkKCiAgICBkZWYgdGVzdF90ZXh0X2ZpbGVzX2hhdmVfY2xlYW5fd2hp
dGVzcGFjZShzZWxmKSAtPiBOb25lOgogICAgICAgIHBhdGhzID0gW1NIRUVULCBQQUNLIC8gIlJF
QURNRS5tZCIsICooUEFDSyAvIG5hbWUgZm9yIG5hbWUgaW4gKAogICAgICAgICAgICAiZmFjdF9h
bmNob3IuanNvbiIsICJsb2dpY19jaGVjay5qc29uIiwgIm1vZGVsX2Fuc3dlci5qc29uIiwgInRv
cGljX2ltcG9ydGFuY2UuanNvbiIKICAgICAgICApKV0KICAgICAgICBmb3IgcGF0aCBpbiBwYXRo
czoKICAgICAgICAgICAgdGV4dCA9IHBhdGgucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAg
ICAgICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZSh0ZXh0LmVuZHN3aXRoKCJcbiIpLCBwYXRoKQogICAg
ICAgICAgICBzZWxmLmFzc2VydEZhbHNlKGFueShsaW5lICE9IGxpbmUucnN0cmlwKCkgZm9yIGxp
bmUgaW4gdGV4dC5zcGxpdGxpbmVzKCkpLCBwYXRoKQoKY2xhc3MgQWxhcm1SZWxhdGlvbnNoaXBU
ZXN0cyh1bml0dGVzdC5UZXN0Q2FzZSk6CiAgICBkZWYgdGVzdF9oaWdoX2FsYXJtX2RlYWRiYW5k
X2RlbGF5X2xvZ2ljKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgZGVmIGFjdGl2ZShwdjogZmxvYXQs
IHNwOiBmbG9hdCwgaGVsZDogZmxvYXQsIG9uX2RlbGF5OiBmbG9hdCkgLT4gYm9vbDoKICAgICAg
ICAgICAgcmV0dXJuIHB2ID49IHNwIGFuZCBoZWxkID49IG9uX2RlbGF5CiAgICAgICAgZGVmIGNs
ZWFyKHB2OiBmbG9hdCwgc3A6IGZsb2F0LCBkZWFkYmFuZDogZmxvYXQsIGhlbGQ6IGZsb2F0LCBv
ZmZfZGVsYXk6IGZsb2F0KSAtPiBib29sOgogICAgICAgICAgICByZXR1cm4gcHYgPD0gc3AgLSBk
ZWFkYmFuZCBhbmQgaGVsZCA+PSBvZmZfZGVsYXkKICAgICAgICBzZWxmLmFzc2VydFRydWUoYWN0
aXZlKDEwMS4wLCAxMDAuMCwgMy4wLCAyLjApKQogICAgICAgIHNlbGYuYXNzZXJ0RmFsc2UoYWN0
aXZlKDEwMS4wLCAxMDAuMCwgMS4wLCAyLjApKQogICAgICAgIHNlbGYuYXNzZXJ0RmFsc2UoY2xl
YXIoOTkuMCwgMTAwLjAsIDIuMCwgMy4wLCAyLjApKQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShj
bGVhcig5OC4wLCAxMDAuMCwgMi4wLCAzLjAsIDIuMCkpCgogICAgZGVmIHRlc3RfYWNrbm93bGVk
Z2VfZG9lc19ub3RfY2xlYXJfY29uZGl0aW9uKHNlbGYpIC0+IE5vbmU6CiAgICAgICAgY29uZGl0
aW9uX2FjdGl2ZSA9IFRydWUKICAgICAgICBhY2tub3dsZWRnZWQgPSBUcnVlCiAgICAgICAgYWxh
cm1fYWN0aXZlID0gY29uZGl0aW9uX2FjdGl2ZQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShhY2tu
b3dsZWRnZWQpCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKGFsYXJtX2FjdGl2ZSkKCiAgICBkZWYg
dGVzdF9wcmlvcml0eV91c2VzX2NvbnNlcXVlbmNlX2FuZF90aW1lKHNlbGYpIC0+IE5vbmU6CiAg
ICAgICAgZGVmIHNjb3JlKHNldmVyaXR5OiBpbnQsIHVyZ2VuY3k6IGludCkgLT4gaW50OgogICAg
ICAgICAgICByZXR1cm4gc2V2ZXJpdHkgKiB1cmdlbmN5CiAgICAgICAgc2VsZi5hc3NlcnRHcmVh
dGVyKHNjb3JlKDQsIDQpLCBzY29yZSg0LCAxKSkKICAgICAgICBzZWxmLmFzc2VydEdyZWF0ZXIo
c2NvcmUoNCwgNCksIHNjb3JlKDEsIDQpKQoKICAgIGRlZiB0ZXN0X3NoZWx2aW5nX2FuZF9zdXBw
cmVzc2lvbl9hcmVfZGlzdGluY3Qoc2VsZikgLT4gTm9uZToKICAgICAgICBzaGVsdmluZyA9IHsi
YWN0b3IiOiAib3BlcmF0b3IiLCAidGVtcG9yYXJ5IjogVHJ1ZSwgImV4cGlyZXMiOiBUcnVlfQog
ICAgICAgIHN1cHByZXNzaW9uID0geyJhY3RvciI6ICJsb2dpYyIsICJ0ZW1wb3JhcnkiOiBGYWxz
ZSwgInN0YXRlX2NvbmRpdGlvbmVkIjogVHJ1ZX0KICAgICAgICBzZWxmLmFzc2VydE5vdEVxdWFs
KHNoZWx2aW5nWyJhY3RvciJdLCBzdXBwcmVzc2lvblsiYWN0b3IiXSkKICAgICAgICBzZWxmLmFz
c2VydFRydWUoc2hlbHZpbmdbImV4cGlyZXMiXSkKICAgICAgICBzZWxmLmFzc2VydFRydWUoc3Vw
cHJlc3Npb25bInN0YXRlX2NvbmRpdGlvbmVkIl0pCgogICAgZGVmIHRlc3Rfc29lX29yZGVyX3Jl
cXVpcmVzX2NvbW1vbl90aW1lYmFzZShzZWxmKSAtPiBOb25lOgogICAgICAgIGV2ZW50cyA9IFsK
ICAgICAgICAgICAgKCJQTENfQSIsIDEwMDAuMDAxLCAiVHJpcCIpLAogICAgICAgICAgICAoIlBM
Q19CIiwgMTAwMC4wMDQsICJWYWx2ZUNsb3NlZCIpLAogICAgICAgIF0KICAgICAgICBvcmRlcmVk
ID0gc29ydGVkKGV2ZW50cywga2V5PWxhbWJkYSBpdGVtOiBpdGVtWzFdKQogICAgICAgIHNlbGYu
YXNzZXJ0RXF1YWwoW2l0ZW1bMl0gZm9yIGl0ZW0gaW4gb3JkZXJlZF0sIFsiVHJpcCIsICJWYWx2
ZUNsb3NlZCJdKQoKICAgIGRlZiB0ZXN0X2NvbW1hbmRfYW5kX2ZlZWRiYWNrX2FyZV9kaXN0aW5j
dChzZWxmKSAtPiBOb25lOgogICAgICAgIGNvbW1hbmRfc2VudCA9IFRydWUKICAgICAgICBmZWVk
YmFja19vbiA9IEZhbHNlCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKGNvbW1hbmRfc2VudCkKICAg
ICAgICBzZWxmLmFzc2VydEZhbHNlKGZlZWRiYWNrX29uKQogICAgICAgIHNlbGYuYXNzZXJ0Tm90
RXF1YWwoY29tbWFuZF9zZW50LCBmZWVkYmFja19vbikKCmNsYXNzIERldGVybWluaXN0aWNGYXRh
bFBhdHRlcm5TYWZldHlUZXN0cyh1bml0dGVzdC5UZXN0Q2FzZSk6CiAgICBkZWYgdGVzdF9kaXJl
Y3Rfd3JvbmdfY2xhaW1zX21hdGNoX2RldGVybWluaXN0aWNfYWlkcyhzZWxmKSAtPiBOb25lOgog
ICAgICAgIGNoZWNrcyA9IExPR0lDWyJkZXRlcm1pbmlzdGljX2NoZWNrcyJdWyJmYXRhbF9jaGVj
a3MiXQogICAgICAgIGZvciBjaGVjayBpbiBjaGVja3M6CiAgICAgICAgICAgIHBhdHRlcm4gPSBy
ZS5jb21waWxlKGNoZWNrWyJ3cm9uZ19wYXR0ZXJucyJdWzBdKQogICAgICAgICAgICBzZWxmLmFz
c2VydFJlZ2V4KGNoZWNrWyJleGFtcGxlc19vcl9wYXR0ZXJucyJdWzBdLCBwYXR0ZXJuLCBjaGVj
a1siaWQiXSkKCiAgICBkZWYgdGVzdF9leHBsaWNpdF9jb3JyZWN0aW9uc19kb19ub3RfdHJpZ2dl
cl9wYXR0ZXJucyhzZWxmKSAtPiBOb25lOgogICAgICAgIGNoZWNrcyA9IExPR0lDWyJkZXRlcm1p
bmlzdGljX2NoZWNrcyJdWyJmYXRhbF9jaGVja3MiXQogICAgICAgIGNvcnJlY3Rpb25zID0gewog
ICAgICAgICAgICBpdGVtWyJpZCJdOiBpdGVtWyJjb3JyZWN0aW9uIl0gZm9yIGl0ZW0gaW4gRkFD
VFsiZmF0YWxfd3JvbmdfY2xhaW1zIl0KICAgICAgICB9CiAgICAgICAgZm9yIGNoZWNrIGluIGNo
ZWNrczoKICAgICAgICAgICAgcGF0dGVybiA9IHJlLmNvbXBpbGUoY2hlY2tbIndyb25nX3BhdHRl
cm5zIl1bMF0pCiAgICAgICAgICAgIHNlbnRlbmNlID0gZiLsmKTri7XsnYAgJ3tjaGVja1snbWVz
c2FnZSddfSfsnbTsp4Drp4wg7Iuk7KCc66Gc64qUIHtjb3JyZWN0aW9uc1tjaGVja1snaWQnXV19
IgogICAgICAgICAgICBzZWxmLmFzc2VydElzTm9uZShwYXR0ZXJuLnNlYXJjaChzZW50ZW5jZSks
IGNoZWNrWyJpZCJdKQoKICAgIGRlZiB0ZXN0X3BhdHRlcm5zX2RvX25vdF9tYXRjaF9vbWlzc2lv
bihzZWxmKSAtPiBOb25lOgogICAgICAgIHRleHQgPSAiQWxhcm0g6rSA66as7JeQ7ISc64qUIOya
tOyghOyekCDsobDsuZjsmYAg7J2R64u17Iuc6rCE7J2EIOqygO2GoO2VnOuLpC4iCiAgICAgICAg
Zm9yIGNoZWNrIGluIExPR0lDWyJkZXRlcm1pbmlzdGljX2NoZWNrcyJdWyJmYXRhbF9jaGVja3Mi
XToKICAgICAgICAgICAgc2VsZi5hc3NlcnRJc05vbmUocmUuY29tcGlsZShjaGVja1sid3Jvbmdf
cGF0dGVybnMiXVswXSkuc2VhcmNoKHRleHQpKQoKY2xhc3MgRm9jdXNlZFJvdXRpbmdCb3VuZGFy
eVRlc3RzKHVuaXR0ZXN0LlRlc3RDYXNlKToKICAgIGRlZiBfbWF0Y2hlZF9hbGlhc2VzKHNlbGYs
IHRleHQ6IHN0cikgLT4gbGlzdFtzdHJdOgogICAgICAgIGxvd2VyID0gdGV4dC5sb3dlcigpCiAg
ICAgICAgcmV0dXJuIFthbGlhcyBmb3IgYWxpYXMgaW4gTU9ERUxbInJvdXRpbmdfYWxpYXNlcyJd
IGlmIGFsaWFzLmxvd2VyKCkgaW4gbG93ZXJdCgogICAgZGVmIHRlc3RfcG9zaXRpdmVfY2FzZXNf
aGF2ZV9sb2NhbF9zaWduYWwoc2VsZikgLT4gTm9uZToKICAgICAgICBjYXNlcyA9IFsKICAgICAg
ICAgICAgIkhNSSBTQ0FEQSBhbGFybSBtYW5hZ2VtZW50IFNPReulvCDshKTrqoXtlZjsi5zsmKQu
IiwKICAgICAgICAgICAgImFsYXJtIGRlYWRiYW5kIGRlbGF5IHNoZWx2aW5nIHN1cHByZXNzaW9u
IOywqOydtOulvCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICAgICAgICAgInNlcXVlbmNlIG9mIGV2
ZW50cyBhdWRpdCB0cmFpbCB0aW1lIHN5bmNocm9uaXphdGlvbuydhCDshKTrqoXtlZjsi5zsmKQu
IiwKICAgICAgICAgICAgImhpZ2ggcGVyZm9ybWFuY2UgSE1JIGRpc3BsYXkgaGllcmFyY2h5IOyE
pOqzhOq4sOykgOydhCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICAgICBdCiAgICAgICAgZm9yIGNh
c2UgaW4gY2FzZXM6CiAgICAgICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShzZWxmLl9tYXRjaGVkX2Fs
aWFzZXMoY2FzZSksIGNhc2UpCgogICAgZGVmIHRlc3Rfc3cwMl9ib3VuZGFyeV9jYXNlc19kb19u
b3RfbWF0Y2hfY29tcG91bmRfYWxpYXMoc2VsZikgLT4gTm9uZToKICAgICAgICBjYXNlcyA9IFsK
ICAgICAgICAgICAgIlNlcXVlbmNlIHN0YXRlIHRyYW5zaXRpb24gdHJpcCBsYXRjaCByZXNldCBs
b2dpY+ydhCDshKTrqoXtlZjsi5zsmKQuIiwKICAgICAgICAgICAgIkludGVybG9ja+ydmCDsg4Ht
g5zsoITsnbTsmYAgRmFpbC1zYWZlIFJlc3RhcnTrpbwg7ISk66qF7ZWY7Iuc7JikLiIsCiAgICAg
ICAgXQogICAgICAgIGZvciBjYXNlIGluIGNhc2VzOgogICAgICAgICAgICBzZWxmLmFzc2VydEZh
bHNlKHNlbGYuX21hdGNoZWRfYWxpYXNlcyhjYXNlKSwgY2FzZSkKCiAgICBkZWYgdGVzdF9zdzA0
X2JvdW5kYXJ5X2Nhc2VzX2RvX25vdF9tYXRjaF9jb21wb3VuZF9hbGlhcyhzZWxmKSAtPiBOb25l
OgogICAgICAgIGNhc2VzID0gWwogICAgICAgICAgICAiVi1Nb2RlbCByZXF1aXJlbWVudCB0cmFj
ZWFiaWxpdHkgdW5pdCBpbnRlZ3JhdGlvbiB0ZXN066W8IOyEpOuqhe2VmOyLnOyYpC4iLAogICAg
ICAgICAgICAiU3RhdGljIGFuYWx5c2lz7JmAIHJlZ3Jlc3Npb24gdGVzdOulvCDshKTrqoXtlZjs
i5zsmKQuIiwKICAgICAgICBdCiAgICAgICAgZm9yIGNhc2UgaW4gY2FzZXM6CiAgICAgICAgICAg
IHNlbGYuYXNzZXJ0RmFsc2Uoc2VsZi5fbWF0Y2hlZF9hbGlhc2VzKGNhc2UpLCBjYXNlKQoKICAg
IGRlZiB0ZXN0X3N3MTBfYm91bmRhcnlfY2FzZXNfZG9fbm90X21hdGNoX2NvbXBvdW5kX2FsaWFz
KHNlbGYpIC0+IE5vbmU6CiAgICAgICAgY2FzZXMgPSBbCiAgICAgICAgICAgICJGQVQgU0FUIGNv
bW1pc3Npb25pbmcgYWNjZXB0YW5jZeyZgCBwdW5jaCBsaXN066W8IOyEpOuqhe2VmOyLnOyYpC4i
LAogICAgICAgICAgICAiVVJTIEZSUyBGRFPsmYAgc2l0ZSBpbnRlZ3JhdGlvbiB0ZXN066W8IOyE
pOuqhe2VmOyLnOyYpC4iLAogICAgICAgIF0KICAgICAgICBmb3IgY2FzZSBpbiBjYXNlczoKICAg
ICAgICAgICAgc2VsZi5hc3NlcnRGYWxzZShzZWxmLl9tYXRjaGVkX2FsaWFzZXMoY2FzZSksIGNh
c2UpCgpjbGFzcyBDb250ZW50UXVhbGl0eVRlc3RzKHVuaXR0ZXN0LlRlc3RDYXNlKToKICAgIGRl
ZiB0ZXN0X25vX3BsYWNlaG9sZGVyX21hcmtlcnMoc2VsZikgLT4gTm9uZToKICAgICAgICBmb3Ji
aWRkZW4gPSAoIlRPRE8iLCAic2NhZmZvbGQiLCAi67O06rCV7ZWY7IS47JqUIiwgIuyekeyEse2V
nOuLpCIpCiAgICAgICAgZm9yIG5hbWUgaW4gKCJSRUFETUUubWQiLCAiZmFjdF9hbmNob3IuanNv
biIsICJsb2dpY19jaGVjay5qc29uIiwgIm1vZGVsX2Fuc3dlci5qc29uIiwgInRvcGljX2ltcG9y
dGFuY2UuanNvbiIpOgogICAgICAgICAgICB0ZXh0ID0gKFBBQ0sgLyBuYW1lKS5yZWFkX3RleHQo
ZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgZm9yIHRva2VuIGluIGZvcmJpZGRlbjoKICAg
ICAgICAgICAgICAgIHNlbGYuYXNzZXJ0Tm90SW4odG9rZW4ubG93ZXIoKSwgdGV4dC5sb3dlcigp
LCBmIntuYW1lfTp7dG9rZW59IikKCiAgICBkZWYgdGVzdF9hbGFybV9ldmVudF9ib3VuZGFyeShz
ZWxmKSAtPiBOb25lOgogICAgICAgIGZhY3QgPSBuZXh0KGl0ZW0gZm9yIGl0ZW0gaW4gRkFDVFsi
YW5jaG9ycyJdIGlmIGl0ZW1bImFuY2hvcl9pZCJdID09ICJzdzAzX2FsYXJtX2RlZmluaXRpb24i
KQogICAgICAgIHNlbGYuYXNzZXJ0SW4oIuyatOyghOyekCIsIGZhY3RbInN0YXRlbWVudCJdKQog
ICAgICAgIHNlbGYuYXNzZXJ0SW4oIkV2ZW50IiwgZmFjdFsic3RhdGVtZW50Il0pCiAgICAgICAg
c2VsZi5hc3NlcnRJbigi6rWs67aEIiwgZmFjdFsic3RhdGVtZW50Il0pCgogICAgZGVmIHRlc3Rf
YXVkaXRfc29lX2JvdW5kYXJ5KHNlbGYpIC0+IE5vbmU6CiAgICAgICAgYXVkaXQgPSBuZXh0KGl0
ZW0gZm9yIGl0ZW0gaW4gRkFDVFsiYW5jaG9ycyJdIGlmIGl0ZW1bImFuY2hvcl9pZCJdID09ICJz
dzAzX2F1ZGl0X3RyYWlsIikKICAgICAgICBzb2UgPSBuZXh0KGl0ZW0gZm9yIGl0ZW0gaW4gRkFD
VFsiYW5jaG9ycyJdIGlmIGl0ZW1bImFuY2hvcl9pZCJdID09ICJzdzAzX3NvZV9kZWZpbml0aW9u
IikKICAgICAgICBzZWxmLmFzc2VydEluKCLsgqzsmqnsnpAiLCBhdWRpdFsic3RhdGVtZW50Il0p
CiAgICAgICAgc2VsZi5hc3NlcnRJbigi7IOB7YOcIiwgc29lWyJzdGF0ZW1lbnQiXSkKICAgICAg
ICBzZWxmLmFzc2VydE5vdEVxdWFsKGF1ZGl0WyJzdGF0ZW1lbnQiXSwgc29lWyJzdGF0ZW1lbnQi
XSkKCgpjbGFzcyBTZW1hbnRpY0F1ZGl0UmVwYWlyVGVzdHModW5pdHRlc3QuVGVzdENhc2UpOgog
ICAgZGVmIHRlc3RfYWxsX2FuY2hvcl9yZWplY3Rpb25zX2FyZV9zcGVjaWZpYyhzZWxmKSAtPiBO
b25lOgogICAgICAgIHJlamVjdGVkID0gW3R1cGxlKGl0ZW1bInJlamVjdGVkX2V4cGxhbmF0aW9u
cyJdKSBmb3IgaXRlbSBpbiBGQUNUWyJhbmNob3JzIl1dCiAgICAgICAgc2VsZi5hc3NlcnRFcXVh
bChsZW4ocmVqZWN0ZWQpLCAzMSkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGxlbihzZXQocmVq
ZWN0ZWQpKSwgMzEpCiAgICAgICAgZ2VuZXJpYyA9ICLshJzroZwg64uk66W4IOygleuztOq0gOum
rCDquLDriqXsnYQg6rCZ7J2AIOydmOuvuOuhnCDst6jquIntlZjqsbDrgpgg7KGw6rG0LCDqtozt
lZwsIOydtOugpeqzvCDsmrTsoITsnpAg7KGw7LmY66W8IOyDneuete2VnOuLpC4iCiAgICAgICAg
c2VsZi5hc3NlcnRGYWxzZShhbnkoZ2VuZXJpYyBpbiB2YWx1ZSBmb3IgdmFsdWVzIGluIHJlamVj
dGVkIGZvciB2YWx1ZSBpbiB2YWx1ZXMpKQoKICAgIGRlZiB0ZXN0X3JlamVjdGlvbnNfY292ZXJf
a2V5X2Z1bmN0aW9uX2JvdW5kYXJpZXMoc2VsZikgLT4gTm9uZToKICAgICAgICBieV9pZCA9IHtp
dGVtWyJpZCJdOiAiICIuam9pbihpdGVtWyJyZWplY3RlZF9leHBsYW5hdGlvbnMiXSkgZm9yIGl0
ZW0gaW4gRkFDVFsiYW5jaG9ycyJdfQogICAgICAgIHNlbGYuYXNzZXJ0SW4oIuuPmeydvCDsnqXs
uZgiLCBieV9pZFsic3cwM19obWlfc2NhZGFfYXJjaGl0ZWN0dXJlIl0pCiAgICAgICAgc2VsZi5h
c3NlcnRJbigi66qo65OgIEV2ZW50IiwgYnlfaWRbInN3MDNfYWxhcm1fZGVmaW5pdGlvbiJdKQog
ICAgICAgIHNlbGYuYXNzZXJ0SW4oIuqzteyglSDsm5Dsnbgg7KCc6rGwIiwgYnlfaWRbInN3MDNf
YWxhcm1fc3RhdGVfYWNrbm93bGVkZ2VtZW50Il0pCiAgICAgICAgc2VsZi5hc3NlcnRJbigiUFYg
7YGs6riwIiwgYnlfaWRbInN3MDNfYWxhcm1fcHJpb3JpdHkiXSkKICAgICAgICBzZWxmLmFzc2Vy
dEluKCLsi5zqsITsp4Dsl7AiLCBieV9pZFsic3cwM19hbGFybV9kZWFkYmFuZCJdKQogICAgICAg
IHNlbGYuYXNzZXJ0SW4oIuyehOydmCBTaGVsdmluZyIsIGJ5X2lkWyJzdzAzX2FsYXJtX3N1cHBy
ZXNzaW9uIl0pCiAgICAgICAgc2VsZi5hc3NlcnRJbigiSGlzdG9yaWFuIO2RnOuzuOqwkiIsIGJ5
X2lkWyJzdzAzX2hpc3Rvcmlhbl92c19zb2UiXSkKICAgICAgICBzZWxmLmFzc2VydEluKCLsgqzs
mqnsnpDCt+uMgOyDgSIsIGJ5X2lkWyJzdzAzX2F1ZGl0X3RyYWlsIl0pCgppZiBfX25hbWVfXyA9
PSAiX19tYWluX18iOgogICAgc3VpdGUgPSB1bml0dGVzdC5kZWZhdWx0VGVzdExvYWRlci5sb2Fk
VGVzdHNGcm9tTW9kdWxlKF9faW1wb3J0X18oX19uYW1lX18pKQogICAgY291bnQgPSBzdWl0ZS5j
b3VudFRlc3RDYXNlcygpCiAgICBwcmludChmIlNXMDNfRk9DVVNFRF9URVNUX0NPVU5UPXtjb3Vu
dH0iKQogICAgcmVzdWx0ID0gdW5pdHRlc3QuVGV4dFRlc3RSdW5uZXIodmVyYm9zaXR5PTIpLnJ1
bihzdWl0ZSkKICAgIHJhaXNlIFN5c3RlbUV4aXQoMCBpZiByZXN1bHQud2FzU3VjY2Vzc2Z1bCgp
IGVsc2UgMSkK
PAYLOAD_SW03_07

    if [ "$failure_count" -eq 0 ]; then
        for rel in "${JSON_PATHS[@]}"; do
            python3 -m json.tool "${payload_tmp}/${rel}" >/dev/null ||
                fail "TEMP_JSON_SYNTAX_FAILED:${rel}"
        done
    fi

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
    pass "existing complete SW-03 payload retained without rewrite"
fi

CURRENT_STAGE="SW03_TOPIC_LOCAL_VALIDATION"
NEXT_STAGE="SW03_OWNERSHIP_VALIDATION"
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
            "VALIDATE_SW03_TOPIC_QUALITY" \
            python3 scripts/validate_topic_pack_quality.py \
                --topic-id "$TOPIC_ID" \
                --strict-generic-aliases \
                --require-logic-check
    else
        fail "TOPIC_QUALITY_VALIDATOR_MISSING"
    fi
fi

CURRENT_STAGE="SW03_FOCUSED_REGRESSION"
NEXT_STAGE="SW03_OWNERSHIP_VALIDATION"
section "5. run SW-03 focused regression and source hygiene"

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "PY_COMPILE_SW03_FOCUSED_TEST" \
        python3 -m py_compile "$TEST_REL"
fi

if [ "$failure_count" -eq 0 ]; then
    focused_log="$(mktemp)"
    python3 "$TEST_REL" 2>&1 | tee "$focused_log"
    focused_rc=${PIPESTATUS[0]}
    printf 'STEP_RC=RUN_SW03_FOCUSED_TEST|%s\n' "$focused_rc"
    if [ "$focused_rc" -ne 0 ]; then
        fail "RUN_SW03_FOCUSED_TEST"
    elif ! grep -Fq 'SW03_FOCUSED_TEST_COUNT=27' "$focused_log"; then
        fail "SW03_FOCUSED_TEST_COUNT_CONTRACT_MISSING"
    else
        pass "SW-03 focused regressions passed: 27/27"
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
        "GIT_DIFF_CHECK_SW03_TARGETS" \
        git diff --check -- "${COMMIT_PATHS[@]}"
fi

CURRENT_STAGE="SW03_OWNERSHIP_VALIDATION"
NEXT_STAGE="SW03_LOCAL_COMMIT"
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
        pass "all changes are confined to immutable helper baseline and SW-03 commit paths"
    else
        fail "SW03_CHANGED_PATH_BOUNDARY_MISMATCH"
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
        pass "only the SW-03 focused test changes Python"
    else
        fail "PRODUCTION_OR_UNRELATED_PYTHON_CHANGED"
    fi
fi

if [ "$failure_count" -ne 0 ]; then
    CURRENT_STAGE="SW03_TOPIC_LOCAL_FAILED"
    NEXT_STAGE="SW03_MINIMAL_REPAIR"
    result_header "SW03_TOPIC_LOCAL_VALIDATION_FAILED"
    printf '%s\n' \
        "failure_count=${failure_count}" \
        "warning_count=${warning_count}" \
        "created_count=${created_count}" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_TOPIC=SW-03 minimal repair" \
        "LANE_PROGRESS=1/4"
    final_rc=1
    exit 1
fi

CURRENT_STAGE="SW03_LOCAL_COMMIT"
NEXT_STAGE="SW04_AUTHORING_PACKAGE"
section "7. stage and create one Topic-local SW-03 commit"

git add -- "${COMMIT_PATHS[@]}"
add_rc=$?
printf 'STEP_RC=GIT_ADD_SW03_TOPIC_ONLY|%s\n' "$add_rc"
[ "$add_rc" -eq 0 ] || fail "GIT_ADD_SW03_TOPIC_ONLY"

if [ "$failure_count" -eq 0 ]; then
    git diff --cached --name-only | LC_ALL=C sort -u > "$staged_file"
    printf '%s\n' "${COMMIT_PATHS[@]}" | LC_ALL=C sort -u > "$commit_files_file"

    printf 'STAGED_SW03_PATHS_BEGIN\n'
    cat "$staged_file"
    printf 'STAGED_SW03_PATHS_END\n'

    if cmp -s "$staged_file" "$commit_files_file"; then
        pass "Git index contains exactly one SW-03 Topic package and its Lane A script"
    else
        fail "SW03_STAGED_PATH_BOUNDARY_MISMATCH"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "GIT_CACHED_DIFF_CHECK_SW03" \
        git diff --cached --check -- "${COMMIT_PATHS[@]}"
fi

if [ "$failure_count" -eq 0 ]; then
    git commit -m "$COMMIT_SUBJECT"
    commit_rc=$?
    printf 'STEP_RC=GIT_COMMIT_SW03|%s\n' "$commit_rc"
    [ "$commit_rc" -eq 0 ] || fail "GIT_COMMIT_SW03"
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW03_TOPIC_LOCAL_COMMIT_FAILED"
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

CURRENT_STAGE="SW03_TOPIC_LOCAL_COMPLETE"
NEXT_STAGE="SW04_AUTHORING_PACKAGE"
LANE_PROGRESS="2/4"
section "8. summarize SW-03 Topic-local result"

printf '%s\n' \
    "SW03_ANCHOR_COUNT=31" \
    "SW03_FATAL_COUNT=16" \
    "SW03_LOGIC_FATAL_COUNT=16" \
    "SW03_LLM_MAJOR_COUNT=8" \
    "SW03_FALSE_POSITIVE_CAUTION_COUNT=10" \
    "SW03_ROUTING_ALIAS_COUNT=20" \
    "SW03_ROUTING_FIELD_POINT_COUNT=45" \
    "SW03_QUESTION_PATTERN_COUNT=10" \
    "SW03_OUTLINE_SECTION_COUNT=8" \
    "SW03_FOCUSED_TEST_COUNT=27" \
    "SW03_DIFFICULTY=DESIGN_EVALUATION" \
    "SW03_SELECTION_IMPORTANCE=CORE_MUST_PREPARE" \
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
    result_header "SW03_TOPIC_LOCAL_COMMIT_COMPLETE"
    printf '%s\n' \
        "LANE=${LANE}" \
        "SW_NUMBER=SW-03" \
        "TOPIC_ID=${TOPIC_ID}" \
        "COMMIT_HASH=${commit_hash}" \
        "COMMIT_SUBJECT=${commit_subject}" \
        "COMMITTED_FILES_BEGIN"
    cat "$commit_files_file"
    printf '%s\n' \
        "COMMITTED_FILES_END" \
        "VALIDATION_RESULT=JSON_SCHEMA_TOPIC_QUALITY_FOCUSED_TEST_PY_COMPILE_DIFF_CHECK_OWNERSHIP_PASS" \
        "NEXT_TOPIC=SW-04 instrumentation_control_software_lifecycle_v_model_traceability_verification_validation" \
        "LANE_PROGRESS=2/4" \
        "PUSH_EXECUTED=false"
    final_rc=0
else
    result_header "SW03_POST_COMMIT_AUDIT_FAILED"
    printf '%s\n' \
        "COMMIT_HASH=${commit_hash}" \
        "COMMIT_SUBJECT=${commit_subject}" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Run a post-commit minimal audit before SW-04"
    final_rc=1
fi

(return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
