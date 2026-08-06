#!/usr/bin/env bash

set -uo pipefail

OVERALL_STAGE="SOFTWARE_TOPIC_PACK_PARALLEL_EXPANSION"
LANE="SOFTWARE_LLM_LANE_A"
LANE_BRANCH="software/lane-a-control-lifecycle"
REMOTE="origin"
REPO_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_a"
CURRENT_TOPIC="SW-02 control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
CURRENT_STAGE="LANE_A_READ_ONLY_WORKTREE_CHECK"
NEXT_STAGE="SW02_COMMIT_STATUS_DETECTION"
LANE_PROGRESS="0/4"
COMMIT_SUBJECT="feat(topic-pack): add SW-02 control logic topic"

TOPIC_ID="control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
TOPIC_DIR="rubrics/topic_packs/$TOPIC_ID"
SHEET_PATH="docs/topic_sheets/$TOPIC_ID.md"
TEST_PATH="scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py"
SCRIPT_NAME="20260806_sw02_lane_a_author_commit_topic_pack.sh"

TARGET_PATHS=(
    "docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md"
    "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md"
    "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json"
    "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json"
    "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json"
    "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json"
    "scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py"
)
JSON_PATHS=(
    "$TOPIC_DIR/fact_anchor.json"
    "$TOPIC_DIR/logic_check.json"
    "$TOPIC_DIR/model_answer.json"
    "$TOPIC_DIR/topic_importance.json"
)

declare -A EXPECTED_SHA256=(
    ["docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md"]="f93c707e8d43cf0714547f3080fa308da0d491874b1d2fb3c56fae0e5a5a7cf1"
    ["rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md"]="496b1adf8a8f3c68877dd654dd8402a4f13ea409dfd5592e4b4d8e358d155d32"
    ["rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json"]="c528ee538dc911e2693a466ee6bc7f41cbd7acea876cc5c8959e2b8f383f04a1"
    ["rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json"]="9d2317dbd82a8c553daadf737c77409ab2ee7f3cb8587d523116b3ba0ea0347f"
    ["rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json"]="5daefe4095b905bca7e311f6d9ab5e5bf8b600263acbd32fc00cd9cdfc11a32c"
    ["rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json"]="3b8a3fd6a05cf53d0d12917154c31c266faa9e3ce5ecfee0afcb392974096190"
    ["scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py"]="2a4ce107a9dce88e2f38ccdc543e2371737ffb0fadd8479009516d25e0cabd2f"
)


failure_count=0
warning_count=0
final_rc=0
created_count=0
AUTHORING_REQUIRED=true
REUSE_EXISTING_PAYLOAD=false
SW02_ALREADY_COMMITTED=false
SW02_COMMIT_HASH=""
SW02_COMMIT_SUBJECT=""
SCRIPT_ABS=""
SCRIPT_REL=""
python_cache_dir="${TMPDIR:-/tmp}/sw02_pycache.$$"
export PYTHONPYCACHEPREFIX="$python_cache_dir"
export PYTHONDONTWRITEBYTECODE=1
changed_paths_file=""
allowed_paths_file=""
baseline_unrelated_paths_file=""
baseline_unrelated_manifest_file=""
post_changed_paths_file=""
post_unrelated_paths_file=""
post_unrelated_manifest_file=""
staged_paths_file=""
commit_files_file=""

section_header() {
    printf '\n===== %s =====\n' "$1"
    printf 'OVERALL_STAGE=%s\n' "$OVERALL_STAGE"
    printf 'LANE=%s\n' "$LANE"
    printf 'LANE_BRANCH=%s\n' "$LANE_BRANCH"
    printf 'CURRENT_TOPIC=%s\n' "$CURRENT_TOPIC"
    printf 'CURRENT_STAGE=%s\n' "$CURRENT_STAGE"
    printf 'NEXT_STAGE=%s\n' "$NEXT_STAGE"
    printf 'LANE_PROGRESS=%s\n' "$LANE_PROGRESS"
}

result_header() {
    printf '\n--- RESULT: %s ---\n' "$1"
    printf 'OVERALL_STAGE=%s\n' "$OVERALL_STAGE"
    printf 'LANE=%s\n' "$LANE"
    printf 'LANE_BRANCH=%s\n' "$LANE_BRANCH"
    printf 'CURRENT_TOPIC=%s\n' "$CURRENT_TOPIC"
    printf 'CURRENT_STAGE=%s\n' "$CURRENT_STAGE"
    printf 'NEXT_STAGE=%s\n' "$NEXT_STAGE"
    printf 'LANE_PROGRESS=%s\n' "$LANE_PROGRESS"
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
    final_rc=1
    printf 'FAIL: %s\n' "$1"
}

run_step() {
    step_name="$1"
    shift
    printf '\n--- %s ---\n' "$step_name"
    "$@"
    step_rc=$?
    printf 'STEP_RC=%s|%s\n' "$step_name" "$step_rc"
    if [ "$step_rc" -ne 0 ]; then
        fail "$step_name"
    fi
    return 0
}

collect_repository_paths() {
    {
        git diff --name-only 2>/dev/null || true
        git diff --cached --name-only 2>/dev/null || true
        git ls-files --others --exclude-standard 2>/dev/null || true
    } | awk 'NF > 0 { print }' | LC_ALL=C sort -u
}

write_path_manifest() {
    manifest_paths_file="$1"
    manifest_output_file="$2"
    python3 - "$manifest_paths_file" "$manifest_output_file" <<'PY_MANIFEST'
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

paths_file = Path(sys.argv[1])
output_file = Path(sys.argv[2])
paths = [line for line in paths_file.read_text(encoding="utf-8").splitlines() if line]

def run(*args: str) -> str:
    completed = subprocess.run(
        args,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout

records = []
for rel in paths:
    path = Path(rel)
    try:
        st = path.lstat()
    except FileNotFoundError:
        worktree_kind = "missing"
        worktree_digest = ""
        worktree_mode = ""
    else:
        worktree_mode = oct(stat.S_IMODE(st.st_mode))
        if path.is_symlink():
            worktree_kind = "symlink"
            worktree_digest = hashlib.sha256(os.readlink(path).encode("utf-8")).hexdigest()
        elif path.is_file():
            worktree_kind = "file"
            worktree_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            worktree_kind = "directory"
            worktree_digest = ""
        else:
            worktree_kind = "other"
            worktree_digest = ""

    records.append(
        {
            "path": rel,
            "status": run(
                "git",
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                rel,
            ),
            "index": run("git", "ls-files", "-s", "--", rel),
            "worktree_kind": worktree_kind,
            "worktree_mode": worktree_mode,
            "worktree_sha256": worktree_digest,
        }
    )

output_file.write_text(
    "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records)
    + ("\n" if records else ""),
    encoding="utf-8",
)
PY_MANIFEST
}

cleanup_temp_files() {
    rm -f -- \
        "${changed_paths_file:-}" \
        "${allowed_paths_file:-}" \
        "${baseline_unrelated_paths_file:-}" \
        "${baseline_unrelated_manifest_file:-}" \
        "${post_changed_paths_file:-}" \
        "${post_unrelated_paths_file:-}" \
        "${post_unrelated_manifest_file:-}" \
        "${staged_paths_file:-}" \
        "${commit_files_file:-}" 2>/dev/null || true
    rm -rf -- "${python_cache_dir:-}" 2>/dev/null || true
}

trap cleanup_temp_files EXIT

CURRENT_STAGE="LANE_A_READ_ONLY_WORKTREE_CHECK"
NEXT_STAGE="SW02_COMMIT_STATUS_DETECTION"
section_header "0. verify dedicated Lane A worktree before modification"

printf '%s\n' \
    "REPO_DIR=$REPO_DIR" \
    "EXPECTED_BRANCH=$LANE_BRANCH" \
    "REMOTE=$REMOTE" \
    "MAIN_FALLBACK_ALLOWED=false" \
    "GENERATED_REBUILD=false" \
    "FULL_VALIDATE_ALL=false" \
    "EXTERNAL_LLM_VALIDATION=false" \
    "TOPIC_LOCAL_COMMIT=true" \
    "TOPIC_LOCAL_PUSH=false"

invocation_pwd="$(pwd -P 2>/dev/null || true)"
SCRIPT_ABS="$(realpath "${BASH_SOURCE[0]}" 2>/dev/null || true)"
script_dir="$(dirname "$SCRIPT_ABS" 2>/dev/null || true)"
script_repo_dir="$(realpath "$script_dir/.." 2>/dev/null || true)"

printf '%s\n' \
    "INVOCATION_ABSOLUTE_PATH=${invocation_pwd:-UNKNOWN}" \
    "SCRIPT_ABSOLUTE_PATH=${SCRIPT_ABS:-UNKNOWN}" \
    "SCRIPT_DERIVED_REPO_DIR=${script_repo_dir:-UNKNOWN}"

if [ ! -d "$REPO_DIR" ]; then
    fail "LANE_A_REPO_DIR_NOT_FOUND: $REPO_DIR"
fi

case "$SCRIPT_ABS" in
    "$REPO_DIR"/gemini_script/*.sh)
        SCRIPT_REL="${SCRIPT_ABS#"$REPO_DIR"/}"
        pass "script is located in Lane A gemini_script"
        ;;
    *)
        fail "SCRIPT_LOCATION_MISMATCH: copy script under $REPO_DIR/gemini_script before execution"
        ;;
esac

if [ "$script_repo_dir" != "$REPO_DIR" ]; then
    fail "SCRIPT_DERIVED_REPO_MISMATCH: expected=$REPO_DIR actual=${script_repo_dir:-UNKNOWN}"
fi

if [ "$failure_count" -eq 0 ] && [ ! -f "$REPO_DIR/.git" ]; then
    fail "NOT_A_LINKED_GIT_WORKTREE: expected .git file at $REPO_DIR/.git"
fi

if [ "$failure_count" -eq 0 ]; then
    if ! cd "$REPO_DIR"; then
        fail "CANNOT_ENTER_LANE_A_REPO_DIR: $REPO_DIR"
    fi
fi

current_pwd="$(pwd -P 2>/dev/null || true)"
printf 'CURRENT_ABSOLUTE_PATH=%s\n' "${current_pwd:-UNKNOWN}"

if [ "$failure_count" -eq 0 ] && [ "$current_pwd" != "$REPO_DIR" ]; then
    fail "WORKTREE_PATH_MISMATCH_AFTER_NORMALIZATION: expected=$REPO_DIR actual=${current_pwd:-UNKNOWN}"
fi

if [ "$failure_count" -eq 0 ]; then
    repo_toplevel="$(git rev-parse --show-toplevel 2>/dev/null || true)"
    inside_worktree="$(git rev-parse --is-inside-work-tree 2>/dev/null || true)"
    current_branch="$(git branch --show-current 2>/dev/null || true)"
    git_dir="$(git rev-parse --path-format=absolute --git-dir 2>/dev/null || true)"
    common_dir="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"

    printf '%s\n' \
        "GIT_TOPLEVEL=$repo_toplevel" \
        "GIT_INSIDE_WORKTREE=$inside_worktree" \
        "GIT_BRANCH=$current_branch" \
        "GIT_DIR=$git_dir" \
        "GIT_COMMON_DIR=$common_dir"

    if [ "$repo_toplevel" != "$REPO_DIR" ]; then
        fail "GIT_TOPLEVEL_MISMATCH: expected=$REPO_DIR actual=$repo_toplevel"
    fi
    if [ "$inside_worktree" != "true" ]; then
        fail "NOT_INSIDE_GIT_WORKTREE"
    fi
    if [ "$current_branch" != "$LANE_BRANCH" ]; then
        fail "LANE_BRANCH_MISMATCH: expected=$LANE_BRANCH actual=$current_branch"
    fi
    if [ -z "$git_dir" ] || [ -z "$common_dir" ] || [ "$git_dir" = "$common_dir" ]; then
        fail "WORKTREE_IS_NOT_LINKED_TO_COMMON_GIT_DIR"
    fi

    if ! git worktree list --porcelain |
        awk -v expected_worktree="$REPO_DIR" \
            -v expected_branch="refs/heads/$LANE_BRANCH" '
            $1 == "worktree" {
                current_worktree = substr($0, index($0, " ") + 1)
                next
            }
            $1 == "branch" {
                current_branch = $2
                if (current_worktree == expected_worktree && current_branch == expected_branch) {
                    found = 1
                }
                next
            }
            END { exit(found ? 0 : 1) }
        '
    then
        fail "WORKTREE_LIST_CONTRACT_MISMATCH"
    fi

    if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
        fail "REMOTE_NOT_CONFIGURED: $REMOTE"
    fi
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "READ_ONLY_CONTRACT_REJECTED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Correct worktree path, branch, or script location and rerun"
    (return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
    exit $?
fi

pass "dedicated Lane A linked-worktree contract verified"

CURRENT_STAGE="SW02_COMMIT_STATUS_DETECTION"
NEXT_STAGE="SW02_AUTHOR_OR_SKIP"
section_header "1. detect whether SW-02 is already normally committed"

head_presence_count=0
working_presence_count=0
last_commit_hashes=""

for path in "${TARGET_PATHS[@]}"; do
    if git cat-file -e "HEAD:$path" 2>/dev/null; then
        head_presence_count=$((head_presence_count + 1))
        last_hash="$(git log -1 --format='%H' -- "$path" 2>/dev/null || true)"
        last_commit_hashes="${last_commit_hashes}${last_hash}"$'\n'
    fi
    if [ -e "$path" ] || [ -L "$path" ]; then
        working_presence_count=$((working_presence_count + 1))
    fi
done

printf '%s\n' \
    "SW02_HEAD_PATH_COUNT=$head_presence_count/${#TARGET_PATHS[@]}" \
    "SW02_WORKTREE_PATH_COUNT=$working_presence_count/${#TARGET_PATHS[@]}"

if [ "$head_presence_count" -eq "${#TARGET_PATHS[@]}" ]; then
    unique_hashes="$(
        printf '%s' "$last_commit_hashes" |
        awk 'NF > 0 { print }' |
        LC_ALL=C sort -u
    )"
    unique_hash_count="$(
        printf '%s\n' "$unique_hashes" |
        awk 'NF > 0 { count++ } END { print count + 0 }'
    )"

    if [ "$unique_hash_count" -ne 1 ]; then
        fail "SW02_FILES_NOT_OWNED_BY_ONE_TOPIC_COMMIT"
    else
        SW02_COMMIT_HASH="$(printf '%s\n' "$unique_hashes" | awk 'NF > 0 { print; exit }')"
        SW02_COMMIT_SUBJECT="$(git show -s --format='%s' "$SW02_COMMIT_HASH" 2>/dev/null || true)"
        target_status="$(git status --porcelain=v1 -- "${TARGET_PATHS[@]}")"

        printf '%s\n' \
            "SW02_EXISTING_COMMIT_HASH=$SW02_COMMIT_HASH" \
            "SW02_EXISTING_COMMIT_SUBJECT=$SW02_COMMIT_SUBJECT"

        if [ -n "$target_status" ]; then
            printf 'SW02_TARGET_STATUS_BEGIN\n%s\nSW02_TARGET_STATUS_END\n' "$target_status"
            fail "SW02_COMMITTED_FILES_HAVE_UNCOMMITTED_CHANGES"
        elif [ "$SW02_COMMIT_SUBJECT" != "$COMMIT_SUBJECT" ]; then
            fail "SW02_COMMIT_SUBJECT_MISMATCH: expected=$COMMIT_SUBJECT actual=$SW02_COMMIT_SUBJECT"
        else
            SW02_ALREADY_COMMITTED=true
            AUTHORING_REQUIRED=false
            LANE_PROGRESS="1/4"
            CURRENT_STAGE="SW02_ALREADY_COMMITTED"
            NEXT_STAGE="SW03_AUTHORING_PACKAGE"
            pass "SW-02 already committed normally; authoring will not be repeated"
        fi
    fi
elif [ "$head_presence_count" -ne 0 ]; then
    fail "PARTIAL_SW02_PATHS_ALREADY_TRACKED_IN_HEAD"
fi

if [ "$failure_count" -eq 0 ] && [ "$AUTHORING_REQUIRED" = true ]; then
    changed_paths_file="$(mktemp)"
    allowed_paths_file="$(mktemp)"
    collect_repository_paths > "$changed_paths_file"
    {
        printf '%s\n' "${TARGET_PATHS[@]}"
        printf '%s\n' "$SCRIPT_REL"
    } | LC_ALL=C sort -u > "$allowed_paths_file"

    printf 'CURRENT_CHANGED_PATHS_BEGIN\n'
    cat "$changed_paths_file"
    printf 'CURRENT_CHANGED_PATHS_END\n'

    baseline_unrelated_paths_file="$(mktemp)"
    baseline_unrelated_manifest_file="$(mktemp)"
    comm -23 "$changed_paths_file" "$allowed_paths_file" > "$baseline_unrelated_paths_file"

    if [ -s "$baseline_unrelated_paths_file" ]; then
        invalid_baseline_paths="$(
            awk '$0 !~ /^gemini_script\/[^/]+\.sh$/ { print }' \
                "$baseline_unrelated_paths_file"
        )"
        if [ -n "$invalid_baseline_paths" ]; then
            printf '%s\n' "$invalid_baseline_paths" | sed 's/^/INVALID_BASELINE_CHANGE=/'
            fail "PREEXISTING_CHANGE_OUTSIDE_LANE_A_GEMINI_SCRIPT"
        else
            while IFS= read -r preserved_path; do
                printf 'PRESERVED_BASELINE_CHANGE=%s\n' "$preserved_path"
            done < "$baseline_unrelated_paths_file"
            write_path_manifest "$baseline_unrelated_paths_file" "$baseline_unrelated_manifest_file"
            pass "pre-existing Lane A gemini scripts captured as immutable baseline"
        fi
    else
        : > "$baseline_unrelated_manifest_file"
        pass "no pre-existing non-SW02 Lane A changes require preservation"
    fi

    if [ "$working_presence_count" -eq 0 ]; then
        REUSE_EXISTING_PAYLOAD=false
        pass "SW-02 is absent and will be authored"
    elif [ "$working_presence_count" -eq "${#TARGET_PATHS[@]}" ]; then
        REUSE_EXISTING_PAYLOAD=true
        pass "complete uncommitted SW-02 payload found; exact payload will be verified and reused"
    else
        fail "PARTIAL_UNCOMMITTED_SW02_PAYLOAD_FOUND"
    fi
fi

if [ "$failure_count" -ne 0 ]; then
    result_header "SW02_STATUS_DETECTION_FAILED"
    printf '%s\n' \
        "FILES_MODIFIED_BY_SCRIPT=false" \
        "COMMIT_CREATED=false" \
        "PUSH_EXECUTED=false" \
        "NEXT_ACTION=Repair Lane A worktree state without touching main or other lanes"
    (return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
    exit $?
fi

if [ "$SW02_ALREADY_COMMITTED" = true ]; then
    result_header "SW02_SKIP_CONFIRMED"
    printf '%s\n' \
        "LANE=$LANE" \
        "SW_NUMBER=SW-02" \
        "TOPIC_ID=$TOPIC_ID" \
        "COMMIT_HASH=$SW02_COMMIT_HASH" \
        "COMMIT_SUBJECT=$SW02_COMMIT_SUBJECT" \
        "VALIDATION_RESULT=EXISTING_TOPIC_COMMIT_AND_CLEAN_TARGETS_CONFIRMED" \
        "NEXT_TOPIC=SW-03 hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management" \
        "LANE_PROGRESS=$LANE_PROGRESS" \
        "PUSH_EXECUTED=false"
    (return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
    exit $?
fi

CURRENT_STAGE="SW02_SOURCE_AUTHORING"
NEXT_STAGE="SW02_TOPIC_LOCAL_VALIDATION"
section_header "2. create or reuse complete SW-02 Topic Authoring Package"

if [ "$REUSE_EXISTING_PAYLOAD" = false ] && [ "$failure_count" -eq 0 ]; then

if [ "$failure_count" -eq 0 ]; then
    mkdir -p --         "docs/topic_sheets"         "$TOPIC_DIR"         "scripts"
    mkdir_rc=$?
    printf 'STEP_RC=CREATE_TARGET_DIRECTORIES|%s\n' "$mkdir_rc"
    if [ "$mkdir_rc" -ne 0 ]; then
        fail "CREATE_TARGET_DIRECTORIES"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md" <<'EOF_SW02_TOPIC_SHEET_8D4F'
# SW-02 Topic Sheet

## 0. Topic identity

- Topic ID: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
- 한글 주제: 제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe
- Lane: `SOFTWARE_LLM_LANE_A`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`

## 1. 출제 의도

산업 계측제어 소프트웨어는 단순히 조건문을 연결하는 프로그램이 아니다. 실제 설비는 기동 전 조건, 운전 중 금지조건, 보호정지, 수동조작, 통신고장과 재기동 상황을 동시에 처리해야 한다. 따라서 답안은 Sequence, 상태전이, Interlock, Permissive와 Trip의 의미를 구분하고, 정상경로와 실패·복구경로를 함께 제시해야 한다.

## 2. 포함 범위

1. Sequence control
2. Step과 State
3. State transition과 Transition guard
4. Entry action, 지속동작, Exit action
5. Permissive
6. Interlock
7. Trip과 Trip latch
8. 정상 Shutdown과 보호 Shutdown
9. Cause & Effect
10. M-out-of-N Voting
11. First-out
12. Bypass와 Override
13. Fail-safe와 Safe state
14. Watchdog와 Heartbeat
15. Bad quality와 stale data
16. Command arbitration
17. Abnormal transition prevention
18. Restart와 Recovery

## 3. 제외 범위

### 3.1 SW-03으로 넘기는 범위

- HMI·SCADA architecture
- High-performance HMI
- Alarm philosophy와 rationalization
- Priority, Deadband, Delay
- Shelving과 Suppression
- Setpoint·Alarm·Trip·Interlock value list 관리
- SOE 화면·보고서
- Audit trail
- Operator authority와 Display hierarchy

SW-02는 Alarm 또는 SOE에 나타날 실제 논리 이벤트의 발생조건을 다룬다. 표시방식과 운영정보 관리는 SW-03이 담당한다.

### 3.2 SW-05로 넘기는 범위

- SIL 산정
- PFDavg와 PFH
- 안전수명주기
- 체계적 고장
- 독립성
- Safety V&V
- SIS 안전 SW 적격성

SW-02는 일반 운전논리와 보호동작 메커니즘만 담당한다.

## 4. Ownership 판단표

| 논점 | SW-02 소유 | 인접 Topic 소유 |
|---|---|---|
| Interlock 동작조건과 출력 강제 | O |  |
| Trip 상태전이와 Latch·Reset | O |  |
| First-out 최초 원인 선정 | O |  |
| SOE 화면 표시와 검색 |  | SW-03 |
| Alarm priority·Shelving |  | SW-03 |
| Operator 권한과 Audit trail |  | SW-03 |
| Voting 논리의 동작 메커니즘 | O |  |
| Voting 구조의 SIL 충족성 |  | SW-05 |
| Fail-safe 상태전환 | O |  |
| Safety lifecycle와 독립성 |  | SW-05 |

## 5. 핵심 개념

### 5.1 Sequence control

Sequence는 공정을 여러 Step 또는 State로 분할한다. 각 상태에는 다음 항목이 필요하다.

- 진입조건
- 실행출력
- 유지조건
- 완료 피드백
- 최대 허용시간
- 실패상태
- 복구 또는 안전정지 경로

Timer만 만료되었다고 실제 설비가 움직였다고 판단해서는 안 된다.

### 5.2 상태전이

```text
S(k+1) = delta[S(k), U(k), P(k), I(k), T(k), F(k)]
```

- `S(k)`: 현재 State
- `U(k)`: 운전명령
- `P(k)`: Permissive
- `I(k)`: Interlock·Inhibit
- `T(k)`: Trip
- `F(k)`: 설비 Feedback와 Timer

다음 상태는 동일한 입력에서 동일하게 결정되어야 한다. 허용되지 않은 전이는 Illegal state로 처리한다.

### 5.3 Transition guard

```text
E_transition
= Command
AND Permissive_All
AND Feedback_OK
AND NOT Trip
AND NOT Inhibit
```

전이조건은 명령만으로 구성하지 않는다. 실제 설비상태와 보호조건을 함께 확인해야 한다.

### 5.4 Permissive

Permissive는 기동 또는 특정 전이를 시작하기 위한 사전 허가조건이다.

예:

- 윤활유 압력 정상
- 냉각수 유량 정상
- 흡입밸브 위치 확인
- Downstream 설비 준비완료

보통 필수조건을 AND로 묶는다.

### 5.5 Interlock

Interlock은 위험한 조합을 금지하거나 출력을 강제하는 운전 제약이다.

예:

- Pump 운전 중 흡입밸브 Close 금지
- 두 방향 Contactor 동시 투입 금지
- 고온 시 Heater 출력 차단
- 설비 이동 중 Door open 금지

Alarm은 운전자에게 정보를 주지만 Interlock은 실제 동작을 제한한다.

### 5.6 Trip

Trip은 보호조건 성립 시 정상 Sequence보다 우선하여 설비를 미리 정한 정지상태로 이행시킨다.

일반적인 Trip 처리:

1. 원인 검출
2. Trip Event Set
3. Trip Latch 유지
4. 보호출력 실행
5. First-out 저장
6. 원인 제거 확인
7. Safe condition 확인
8. 권한 있는 Reset
9. Restart 조건 재평가

### 5.7 Shutdown

정상 Shutdown은 공정을 순차적으로 정리할 수 있다. Trip은 위험을 제한하기 위해 정상 Sequence를 중단하고 우선동작한다. 두 동작은 목적과 시간특성이 다르다.

### 5.8 Cause & Effect

Cause & Effect는 원인과 결과를 표 또는 행렬로 연결한다.

| Cause | Alarm | Interlock | Trip | Final action |
|---|---:|---:|---:|---|
| Low suction pressure | O | Start inhibit | Delay trip | Pump stop |
| High-high temperature | O | Heater cut | Immediate trip | Valve safe state |
| Communication loss | O | Mode inhibit | Conditional | Hold or stop |

Cause & Effect는 설계의도 기준문서이다. 상세 상태전이, Timer, Latch, Reset, 우선순위와 Scan 동작은 별도 논리사양이 필요하다.

### 5.9 Voting

```text
Trip_vote = 1 if sum(x_i) >= M
```

예를 들어 2oo3은 3개 채널 중 2개 이상이 Trip일 때 동작한다.

검토 항목:

- 채널 독립성
- 공통원인
- Bad quality 처리
- 불일치 Alarm
- Bypass 중 Voting 변환
- 채널 복구조건

Voting은 채널 수만 늘린다고 항상 좋아지지 않는다.

### 5.10 First-out

```text
First_Out = arg min(t_i)
```

연쇄적으로 여러 Trip 신호가 발생할 때 가장 먼저 발생한 유효 원인을 보존한다. 최종 잔류신호나 Alarm 우선순위가 아니다.

### 5.11 Bypass와 Override

| 구분 | Bypass | Override |
|---|---|---|
| 목적 | 입력 또는 보호경로 우회 | 정상 명령보다 우선하는 강제명령 |
| 주요 위험 | 보호기능 감소 | 예상하지 못한 출력 강제 |
| 필수 통제 | 승인, 표시, 시간제한, 대체조치 | 권한, 범위, 우선순위, 해제조건 |
| 복구 | 원상복귀와 기능확인 | 강제 해제와 정상 소유권 반환 |

### 5.12 Fail-safe

Fail-safe는 고장 시 위험을 최소화하는 상태와 동작이다.

가능한 Safe state:

- Fail-close
- Fail-open
- Fail-last 또는 Hold
- Controlled stop
- 단계적 Depressurization
- 제한운전

모든 설비가 Fail-close인 것은 아니다.

### 5.13 Watchdog

```text
Watchdog_Expired
= Current_Time - Last_Heartbeat > Timeout
```

Watchdog 대상:

- PLC Task
- Controller redundancy
- Remote I/O
- Network connection
- Smart device heartbeat

Timeout 후에는 단순 Alarm뿐 아니라 Hold, Controlled stop 또는 Safe action 정책이 필요하다.

### 5.14 Trip latch와 Reset

```text
Q_trip(k+1)
= Trip_Event
OR [Q_trip(k) AND NOT Reset_Valid]
```

```text
Reset_Valid
= Cause_Clear
AND Safe_Condition
AND Authorized
AND Reset_Edge
```

원인이 남아 있는 상태에서 Reset을 허용해서는 안 된다.

### 5.15 이상전이 방지

- Allowed transition matrix
- Mutual exclusion
- One-hot state
- Transition-in-progress lock
- Timeout
- Feedback discrepancy
- Debounce와 Hysteresis
- Illegal-state fallback
- 단일 출력 소유자
- Trip 우선순위

### 5.16 Scan, Edge와 Memory

PLC Scan에서는 Level과 Edge를 구분한다.

- Level: 조건이 참인 동안 계속 참
- Rising edge: False에서 True로 변한 1회 이벤트
- One-shot: 한 Scan 또는 한 실행주기만 참
- Latch: Reset 전까지 상태 유지

Set과 Reset이 동시에 성립할 가능성이 있으면 우선순위를 명시한다.

### 5.17 Command arbitration

권장 우선순위 예:

```text
Trip or Emergency action
> Safety-critical Interlock
> Controlled shutdown
> Maintenance Override
> Manual command
> Automatic Sequence command
```

실제 우선순위는 프로젝트 요구사항으로 확정한다. 한 출력은 한 시점에 하나의 논리 소유자만 가져야 한다.

### 5.18 Restart와 Recovery

Restart 시 확인사항:

1. Cold start와 Warm restart 구분
2. 출력 초기화 정책
3. 실제 밸브·모터·접점 상태 재수집
4. 메모리 State와 현장상태 비교
5. State reconciliation
6. Trip latch 보존
7. Permissive 재확인
8. 자동재개 또는 운영자 승인 결정
9. 부분정전과 통신복구 시나리오 검증

## 6. 대표 오답과 판정

| 대표 오답 | 판정 | 정정 |
|---|---|---|
| Permissive와 Trip은 같다 | Fatal | 사전 허가와 보호정지를 구분 |
| Interlock은 Alarm만 발생 | Fatal | 금지 또는 강제동작 수행 |
| Trip 원인이 없어지면 즉시 Auto reset | Fatal | Latch와 Reset valid 필요 |
| 모든 Fail-safe는 Fail-close | Fatal | 공정별 Safe state |
| Voting은 채널이 많을수록 항상 안전 | Fatal | 독립성·공통원인 검토 |
| Timer 만료가 실제 완료 피드백 | Fatal | 실제 Feedback 확인 |
| Restart 시 이전 Step 그대로 복원 | Fatal | State reconciliation |
| Bypass 승인과 시간제한 누락 | Major | 관리통제 추가 |
| First-out 누락 | Warn 또는 Major | 문항 요구 시 최초 원인 보존 설명 |
| HMI 화면과 Alarm priority 위주 답안 | Scope drift | SW-03으로 이동 |
| SIL 계산 위주 답안 | Scope drift | SW-05로 이동 |

## 7. False positive 기준

1. 문항이 Alarm 관리 중심이면 SW-03이다.
2. 문항이 SIL 산정 중심이면 SW-05이다.
3. 특정 밸브의 Fail-close 사례는 허용한다.
4. 비위험 설비의 조건부 Auto restart는 허용할 수 있다.
5. Cause & Effect를 중요 설계문서라고 한 것은 정답이다.
6. Bypass가 필요할 수 있다는 설명 자체는 정답이다.
7. First-out과 SOE를 함께 설명해도 소유범위를 구분하면 정답이다.
8. 단순 누락은 Fatal이 아니다.

## 8. Model Answer 예시 구조

### 8.1 배경

공정 자동화는 정상운전뿐 아니라 기동 전 조건, 운전 중 금지조건, 고장 시 보호정지와 복구를 일관되게 처리해야 한다. 이를 위해 Sequence, 상태전이, Interlock, Permissive와 Trip을 계층적으로 설계한다.

### 8.2 핵심 내용

Sequence는 State와 Transition으로 구성한다. 전이는 명령, Permissive, 정상 Feedback, `NOT Trip`, `NOT Inhibit`가 모두 성립할 때 허용한다. Permissive는 사전 허가조건이다. Interlock은 위험한 조합을 금지하거나 출력을 강제한다. Trip은 보호조건 발생 시 정상 Sequence보다 우선하여 정지상태로 이행한다.

Cause & Effect는 원인과 결과의 설계 의도를 제시한다. Voting은 M-out-of-N 구조로 판정하되 독립성과 공통원인을 검토한다. First-out은 연쇄 Trip의 최초 원인을 보존한다. Bypass와 Override는 목적이 다르므로 권한, 표시, 시간제한과 해제조건을 분리한다.

Fail-safe는 공정별 Safe state로 정의한다. Watchdog, Bad quality와 stale data는 Hold, Controlled stop, Trip 또는 Degraded mode로 연결한다. Restart 시에는 실제 상태를 재수집하고 State reconciliation과 Permissive 재확인을 수행한다.

### 8.3 결론

고득점 답안은 용어 나열이 아니라 조건, 우선순위, 출력, 피드백, 실패와 복구를 상태전이로 연결해야 한다. 또한 HMI·Alarm 관리는 SW-03, SIL과 안전수명주기는 SW-05로 구분해야 한다.

## 9. Topic Importance

이 Topic은 PLC·DCS 응용, Cause & Effect, 시운전, 트러블슈팅과 안전정지 문제의 공통 기반이다. 실무 적용성이 높고 다양한 문제와 결합되므로 `CORE_MUST_PREPARE`로 분류한다.

## 10. Routing alias

- `제어논리 Sequence Interlock Permissive Trip`
- `시퀀스 상태전이 인터록 퍼미시브 트립`
- `Sequence control state transition interlock permissive trip`
- `운전 제어논리와 상태전이`
- `Interlock Permissive Trip 차이`
- `인터록 퍼미시브 트립 차이`
- `Cause & Effect Voting First-out`
- `원인 결과표 Voting First-out`
- `Bypass Override 제어논리`
- `바이패스 오버라이드 명령 우선순위`
- `Fail-safe Watchdog Restart Recovery`
- `Fail safe watchdog 재기동 복구논리`
- `Sequence abnormal transition prevention`
- `시퀀스 이상전이 방지`
- `Trip latch reset logic`
- `트립 래치 리셋 조건`
- `Manual Auto Local Remote command arbitration`
- `수동 자동 로컬 리모트 명령 중재`
- `PLC sequence feedback timeout one-shot latch`
- `상태전이표 mutual exclusion illegal state recovery`

## 11. Focused regression cases

### Positive routing cases

1. Sequence 상태전이와 Interlock·Trip 설계
2. Permissive와 Trip 차이
3. Cause & Effect, Voting과 First-out
4. Bypass·Override 및 명령 우선순위
5. Watchdog와 Restart recovery
6. Feedback Timeout과 Illegal state 방지

### Negative boundary cases

1. Alarm priority, Deadband, Shelving과 Suppression
2. High-performance HMI와 Display hierarchy
3. SOE 보고서와 Operator audit trail
4. SIL 산정, PFDavg와 PFH
5. Safety lifecycle, independence와 Safety V&V
6. PLC·DCS architecture와 redundancy만 묻는 문제

## 12. Source JSON 설계

- `fact_anchor.json`: Anchor 28개, Fatal 16개
- `logic_check.json`: 명시적 반대 주장용 deterministic fatal, LLM major·warn 및 false-positive 기준
- `model_answer.json`: 대표 질문 10개, 8단계 Outline, compound routing alias
- `topic_importance.json`: DESIGN_EVALUATION, CORE_MUST_PREPARE

## 13. Topic-local 검증

- JSON 문법
- Topic Pack quality/schema
- focused unittest
- trailing whitespace와 EOF
- 변경 파일 ownership
- generated 및 공통 Python 불변

## 14. Topic-local 커밋과 통합 단계 이관

Topic-local 검증이 성공하면 SW-02 파일과 SW-02 전용 실행 스크립트만 별도 로컬 커밋한다. Topic 작업 중에는 원격 push를 수행하지 않는다.

다음은 최종 main 통합 단계로 넘긴다.

- generated rebuild
- cross-topic duplicate 검사
- 전체 Router 회귀
- validate-all
- release validation
- container smoke
- main commit
- main push
EOF_SW02_TOPIC_SHEET_8D4F
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: docs/topic_sheets/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe.md"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md" <<'EOF_SW02_README_7C2A'
# 제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe

## Topic identity

- SW 번호: `SW-02`
- Topic ID: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
- Lane: `SOFTWARE_LLM_LANE_A`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`

## 1. 목적

이 Topic Pack은 PLC·DCS 기반 운전 제어논리를 단순 키워드가 아니라 상태와 조건의 관계로 평가한다. 핵심은 Sequence를 Step 나열로 설명하는 데 있지 않다. 현재 상태, 전이조건, 출력동작, 피드백 확인, Timeout, 보호 우선순위와 복구경로를 하나의 결정론적 논리로 연결해야 한다.

## 2. 포함 범위

- Sequence control과 Step·State 모델
- State transition, Transition guard, Entry·Exit action
- Permissive, Interlock, Trip, Shutdown
- Cause & Effect
- M-out-of-N Voting과 First-out
- Bypass와 Override
- Fail-safe와 Safe state
- Watchdog, Heartbeat, Bad quality와 stale data
- Trip latch와 Reset valid
- Manual·Auto, Local·Remote 명령 우선순위
- Timeout, Feedback confirmation, Debounce, Hysteresis
- Restart, Recovery, State reconciliation
- Abnormal transition prevention과 Degraded mode

## 3. 제외 범위

다음은 SW-02의 핵심 채점범위가 아니다.

- HMI 화면계층, High-performance HMI
- Alarm philosophy, rationalization, priority, Deadband, Delay, Shelving, Suppression
- Setpoint list, Alarm value, Trip value, Interlock value 관리
- SOE 화면·보고서 운영, Audit trail, Operator authority
- SIL 산정, PFDavg, PFH
- 안전수명주기, 체계적 고장 통제, 독립성
- Safety V&V와 안전 SW 적격성

## 4. Ownership 경계

### SW-03과의 경계

SW-02는 Interlock·Trip·Sequence의 실제 동작논리와 상태전이를 소유한다. SW-03은 그 결과를 운전자에게 전달하는 HMI·SCADA, Alarm 관리, Setpoint, SOE, Audit trail과 권한을 소유한다.

First-out은 최초 원인을 선정하는 메커니즘까지 SW-02이다. First-out 또는 SOE를 화면에 표시하고 검색·보고하는 운영기능은 SW-03이다.

### SW-05와의 경계

SW-02는 Fail-safe, Trip, Voting과 Bypass의 운전논리 메커니즘을 다룬다. SW-05는 해당 기능의 SIL 산정, 안전수명주기, 독립성, 체계적 고장 통제와 Safety V&V를 다룬다. 모든 Interlock을 SIS로 간주하지 않는다.

## 5. 핵심 논리 관계

### 5.1 상태전이

```text
S(k+1) = delta(S(k), Command, Permissive, Interlock, Trip, Feedback, Timer)
```

동일한 현재 상태와 입력에는 동일한 다음 상태가 결정되어야 한다.

### 5.2 전이 허가

```text
Transition_Enable
= Command
AND Permissive_All
AND Feedback_OK
AND NOT Trip
AND NOT Inhibit
```

여기서 `Permissive_All = p1 AND p2 AND ... AND pn`이다.

### 5.3 Voting

```text
Trip_vote = 1, when sum(x_i) >= M for N channels
```

`M-out-of-N` 숫자만으로 성능이 보장되지 않는다. 채널 독립성, 공통원인, 진단과 불일치 처리가 필요하다.

### 5.4 Trip latch

```text
Trip_Latched(k+1)
= Trip_Event
OR [Trip_Latched(k) AND NOT Reset_Valid]
```

Set-dominant가 기본이다. `Reset_Valid`는 원인 제거, 안전조건, 권한과 Reset edge를 모두 확인해야 한다.

### 5.5 First-out

```text
First_Out = arg min(t_i), for valid initiating causes
```

후속 연쇄신호가 아니라 최초의 유효 원인을 고정한다.

### 5.6 Watchdog

```text
Watchdog_Expired = Current_Time - Last_Heartbeat > Timeout
```

Timeout 후 동작은 Hold, Controlled stop, Safe action 또는 제한운전 중 공정에 적합한 정책으로 정한다.

## 6. 대표 출제문제

1. Sequence control의 상태전이, 단계완료 조건 및 비정상 전이 방지방법을 설명하시오.
2. Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.
3. 공정 Shutdown 논리와 Cause & Effect 작성 시 고려사항을 설명하시오.
4. 2oo3 Voting과 First-out 논리의 원리 및 설계 유의사항을 설명하시오.
5. Bypass와 Override의 차이, 위험요인 및 관리방안을 설명하시오.
6. Fail-safe와 Watchdog의 개념을 설명하고 고장 시 제어논리를 제시하시오.
7. 제어시스템 Restart 및 Recovery 논리의 설계기준을 설명하시오.
8. PLC Sequence에서 Timer, Feedback, Edge 및 Latch 적용 시 주의사항을 설명하시오.
9. Manual·Auto, Local·Remote 운전모드의 명령 우선순위와 보호논리를 설명하시오.
10. 상태전이표를 이용한 이상전이 방지 및 복구방안을 설명하시오.

## 7. 대표 Fatal 오류

- Permissive와 Trip을 같은 기능으로 설명
- Interlock을 Alarm 표시만 하는 기능으로 설명
- Trip 원인 소멸 즉시 무조건 Auto reset
- Bypass를 승인·표시·시간제한 없이 유지
- Fail-safe를 모든 설비의 Fail-close로 일반화
- Voting 채널을 늘리면 항상 안전하다고 설명
- First-out을 마지막 신호 또는 Alarm 우선순위로 설명
- Watchdog를 표시기능으로만 설명
- Restart 시 이전 출력과 Step을 조건 확인 없이 복원
- Cause & Effect만으로 실행논리가 완성된다고 설명
- Timer 만료를 설비 완료 피드백으로 대체
- Override와 Bypass를 같은 기능으로 설명
- 정상 Shutdown과 Trip을 동일시
- 모든 Interlock을 SIS·SIL 기능으로 간주
- Manual mode에서 보호 Interlock과 Trip을 전부 무효화
- Bad quality와 stale data를 정상 신호로 간주

## 8. Warn 또는 Major 수준 부족사항

- State와 Step은 언급했으나 진입·완료·실패·복구 조건이 없음
- Permissive·Interlock·Trip의 시점과 우선순위 비교가 없음
- Trip latch와 Reset valid가 없음
- Feedback confirmation과 Timeout의 역할을 구분하지 않음
- Bypass·Override의 권한과 복구통제가 없음
- Restart 상태 일치화가 없음
- Bad quality와 통신복구 정책이 없음
- HMI·Alarm 또는 SIL 설명으로 주제가 이동함

## 9. False positive 방지

- `Trip` 또는 `Interlock` 단어 하나만으로 이 Topic을 선택하지 않는다.
- Alarm priority·Shelving·SOE 표시가 중심이면 SW-03이다.
- SIL·PFDavg·Safety lifecycle이 중심이면 SW-05이다.
- 특정 설비의 Fail-close 사례는 허용한다. 모든 설비에 대한 절대 주장일 때만 Fatal이다.
- 위험이 낮은 보조설비의 조건부 Auto reset도 상태검증과 설계근거가 있으면 허용한다.
- Bypass를 정비수단으로 언급한 것 자체는 오류가 아니다. 관리통제 유무를 평가한다.

## 10. Model Answer 권장 구조

1. 배경과 제어논리 계층
2. Sequence와 상태전이 모델
3. Permissive·Interlock·Trip·Shutdown 비교
4. Cause & Effect·Voting·First-out
5. Bypass·Override·명령 우선순위
6. Fail-safe·Watchdog·신호품질
7. 이상전이 방지와 Scan 기반 구현
8. Restart·Recovery와 현장 적용 결론

## 11. Focused regression 계약

Focused test는 다음을 확인한다.

- source JSON 4개의 Topic ID와 schema
- Anchor 28개와 Fatal 16개의 유일성
- Model Answer의 모든 Anchor reference 유효성
- SW-03·SW-05 ownership 경계 존재
- broad alias인 `PLC`, `SCADA`, `Alarm`, `Trip`, `Interlock`, `SIS` 단독 사용 금지
- 상태전이, Voting, Trip latch, Watchdog, Restart 논리 회귀
- generated bank와 공통 Router를 변경하지 않았는지 ownership 검사

## 12. Topic-local 완료 기준

- Topic Sheet 생성
- README와 source JSON 4개 생성
- focused test 생성 및 통과
- JSON 문법 검증 통과
- Topic Pack quality/schema 검증 통과
- git diff whitespace 검증 통과
- 새 변경경로가 SW-02 허용경로와 정확히 일치
- generated, 공통 Python, 기존 Topic 불변
- SW-02 Topic-local 로컬 커밋 생성
- 원격 push 미실행
EOF_SW02_README_7C2A
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/README.md"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json" <<'EOF_SW02_FACT_ANCHOR_4E91'
{
  "schema_version": "topic_pack.fact_anchor.v1",
  "topic_id": "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
  "title_ko": "제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe",
  "question_type_hint": "PRINCIPLE_INTERPRETATION",
  "anchors": [
    {
      "id": "sw02_scope_operational_logic",
      "anchor_id": "sw02_scope_operational_logic",
      "statement": "SW-02는 운전 제어논리의 동작 메커니즘을 다루며 Sequence, 상태전이, Interlock, Permissive, Trip, Shutdown, Cause & Effect, Voting, First-out, Bypass, Override, Fail-safe, Watchdog 및 Restart·Recovery를 하나의 운전 논리 체계로 연결한다.",
      "importance": "must",
      "keywords": [
        "운전 제어논리",
        "Sequence",
        "상태전이",
        "Interlock",
        "Permissive",
        "Trip",
        "Fail-safe"
      ],
      "core_terms": [
        "운전 제어논리",
        "상태전이",
        "보호동작",
        "복구"
      ],
      "accepted_explanations": [
        "SW-02는 운전 제어논리의 동작 메커니즘을 다루며 Sequence, 상태전이, Interlock, Permissive, Trip, Shutdown, Cause & Effect, Voting, First-out, Bypass, Override, Fail-safe, Watchdog 및 Restart·Recovery를 하나의 운전 논리 체계로 연결한다.",
        "운전 제어논리, 상태전이, 보호동작, 복구의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "SW-02의 핵심을 HMI Alarm 운영이나 SIL 산정으로 확장하거나 Sequence·보호동작·복구를 서로 같은 기능으로 설명한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_sequence_definition",
      "anchor_id": "sw02_sequence_definition",
      "statement": "Sequence control은 공정을 여러 Step 또는 State로 나누고, 각 단계의 진입조건·실행동작·완료조건·시간제한·실패처리를 정의하여 정해진 순서로 운전하는 제어방식이다.",
      "importance": "must",
      "keywords": [
        "Sequence control",
        "Step",
        "State",
        "진입조건",
        "완료조건",
        "시간제한",
        "실패처리"
      ],
      "core_terms": [
        "Sequence control",
        "Step",
        "완료조건",
        "실패처리"
      ],
      "accepted_explanations": [
        "Sequence control은 공정을 여러 Step 또는 State로 나누고, 각 단계의 진입조건·실행동작·완료조건·시간제한·실패처리를 정의하여 정해진 순서로 운전하는 제어방식이다.",
        "Sequence control, Step, 완료조건, 실패처리의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Sequence를 Timer와 출력의 순서 나열로만 정의하고 Step의 진입조건·완료조건·실패처리를 두지 않는다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_state_transition_model",
      "anchor_id": "sw02_state_transition_model",
      "statement": "상태전이는 현재 상태와 명령, Permissive, Interlock, Trip, 설비 피드백 및 시간조건을 입력으로 다음 상태를 결정하는 함수로 표현할 수 있으며, 동일 입력에서 결정론적 결과가 나와야 한다.",
      "importance": "must",
      "keywords": [
        "상태전이",
        "현재 상태",
        "다음 상태",
        "결정론",
        "명령",
        "피드백",
        "시간조건"
      ],
      "core_terms": [
        "상태전이",
        "결정론",
        "현재 상태",
        "다음 상태"
      ],
      "accepted_explanations": [
        "상태전이는 현재 상태와 명령, Permissive, Interlock, Trip, 설비 피드백 및 시간조건을 입력으로 다음 상태를 결정하는 함수로 표현할 수 있으며, 동일 입력에서 결정론적 결과가 나와야 한다.",
        "상태전이, 결정론, 현재 상태, 다음 상태의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "현재 상태를 고려하지 않거나 동일한 상태와 입력에서 임의로 다른 다음 상태가 허용된다고 설명한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_transition_guard",
      "anchor_id": "sw02_transition_guard",
      "statement": "Transition guard는 상태변화를 허용하는 논리조건이다. 기동·명령 기반 전이의 대표식은 Command AND 모든 필수 Permissive AND 필요한 선행 Feedback AND NOT Trip AND NOT Inhibit로 나타낼 수 있다. 자동 진행, 시간 유지 완료 또는 공정조건 도달 전이는 Command 없이 성립할 수 있으며, Feedback은 전이의 선행조건 또는 동작 완료 확인조건으로 구분한다.",
      "importance": "must",
      "keywords": [
        "Transition guard",
        "Command",
        "Permissive",
        "Feedback",
        "Trip",
        "Inhibit",
        "AND"
      ],
      "core_terms": [
        "Transition guard",
        "Permissive",
        "Trip",
        "피드백"
      ],
      "accepted_explanations": [
        "Transition guard는 상태변화를 허용하는 논리조건이다. 기동·명령 기반 전이의 대표식은 Command AND 모든 필수 Permissive AND 필요한 선행 Feedback AND NOT Trip AND NOT Inhibit로 나타낼 수 있다. 자동 진행, 시간 유지 완료 또는 공정조건 도달 전이는 Command 없이 성립할 수 있으며, Feedback은 전이의 선행조건 또는 동작 완료 확인조건으로 구분한다.",
        "기동 전이의 선행조건과 동작 완료 후 확인조건을 구분하고, Command가 없는 자동 전이도 별도로 설명한다."
      ],
      "rejected_explanations": [
        "모든 전이에 Command가 반드시 필요하다고 일반화하거나 기동·명령 기반 전이에서 필수 Permissive와 Trip 차단조건을 무시한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_state_entry_exit_actions",
      "anchor_id": "sw02_state_entry_exit_actions",
      "statement": "각 State에는 Entry action, 지속 동작, Exit action을 구분하여 정의해야 하며, 출력은 상태와 전이 이벤트의 소유관계를 명확히 하여 중복 명령과 잔류 출력을 방지한다.",
      "importance": "important",
      "keywords": [
        "Entry action",
        "Exit action",
        "State action",
        "출력 소유권",
        "잔류 출력",
        "중복 명령"
      ],
      "core_terms": [
        "Entry action",
        "Exit action",
        "출력 소유권"
      ],
      "accepted_explanations": [
        "각 State에는 Entry action, 지속 동작, Exit action을 구분하여 정의해야 하며, 출력은 상태와 전이 이벤트의 소유관계를 명확히 하여 중복 명령과 잔류 출력을 방지한다.",
        "Entry action, Exit action, 출력 소유권의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Entry·지속·Exit 동작의 소유권을 구분하지 않고 여러 State가 같은 출력을 동시에 지배해도 된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_permissive_definition",
      "anchor_id": "sw02_permissive_definition",
      "statement": "Permissive는 기동 또는 특정 전이를 시작하기 전에 만족해야 하는 사전 허가조건이며, 보통 모든 필수 조건의 AND 논리로 구성한다.",
      "importance": "must",
      "keywords": [
        "Permissive",
        "기동조건",
        "사전조건",
        "허가조건",
        "AND logic"
      ],
      "core_terms": [
        "Permissive",
        "사전 허가조건",
        "AND"
      ],
      "accepted_explanations": [
        "Permissive는 기동 또는 특정 전이를 시작하기 전에 만족해야 하는 사전 허가조건이며, 보통 모든 필수 조건의 AND 논리로 구성한다.",
        "Permissive, 사전 허가조건, AND의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Permissive를 운전 중 강제정지인 Trip과 동일시하거나 필수 허가조건 중 일부만 만족해도 기동할 수 있다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_interlock_definition",
      "anchor_id": "sw02_interlock_definition",
      "statement": "Interlock은 위험하거나 비정상적인 조합을 방지하기 위해 동작을 금지하거나 운전 중 특정 출력을 강제하는 제약논리이며, 단순 Alarm 표시와 구분된다.",
      "importance": "must",
      "keywords": [
        "Interlock",
        "금지조건",
        "강제동작",
        "비정상 조합",
        "Alarm 구분"
      ],
      "core_terms": [
        "Interlock",
        "금지",
        "강제동작",
        "Alarm"
      ],
      "accepted_explanations": [
        "Interlock은 위험하거나 비정상적인 조합을 방지하기 위해 동작을 금지하거나 운전 중 특정 출력을 강제하는 제약논리이며, 단순 Alarm 표시와 구분된다.",
        "Interlock, 금지, 강제동작, Alarm의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Interlock을 표시용 Alarm으로만 보거나 허용되지 않은 동작을 차단·강제하지 않는다고 설명한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_trip_definition",
      "anchor_id": "sw02_trip_definition",
      "statement": "Trip은 보호조건이 성립할 때 정상 Sequence보다 우선하여 설비 또는 공정을 미리 정한 정지상태로 이행시키는 강제 보호동작이며, 위험도와 공정특성에 따라 Latch와 수동 Reset을 적용한다.",
      "importance": "must",
      "keywords": [
        "Trip",
        "보호조건",
        "우선순위",
        "강제 정지",
        "Latch",
        "Reset"
      ],
      "core_terms": [
        "Trip",
        "강제 보호동작",
        "Latch",
        "Reset"
      ],
      "accepted_explanations": [
        "Trip은 보호조건이 성립할 때 정상 Sequence보다 우선하여 설비 또는 공정을 미리 정한 정지상태로 이행시키는 강제 보호동작이며, 위험도와 공정특성에 따라 Latch와 수동 Reset을 적용한다.",
        "Trip, 강제 보호동작, Latch, Reset의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Trip을 정상 Sequence와 같은 우선순위의 일반 정지명령으로 보거나 모든 Trip이 무조건 자동 Reset된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_shutdown_classes",
      "anchor_id": "sw02_shutdown_classes",
      "statement": "Shutdown은 정상정지, 공정정지, 비상정지 등 목적과 속도에 따라 구분하며, 정상정지는 순차적 감속·배출·정리 절차를 따를 수 있지만 Trip은 보호목적의 우선 동작으로 설계한다.",
      "importance": "important",
      "keywords": [
        "Shutdown",
        "정상정지",
        "공정정지",
        "비상정지",
        "순차정지",
        "Trip"
      ],
      "core_terms": [
        "정상정지",
        "Trip",
        "Shutdown"
      ],
      "accepted_explanations": [
        "Shutdown은 정상정지, 공정정지, 비상정지 등 목적과 속도에 따라 구분하며, 정상정지는 순차적 감속·배출·정리 절차를 따를 수 있지만 Trip은 보호목적의 우선 동작으로 설계한다.",
        "정상정지, Trip, Shutdown의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "정상 Shutdown과 보호 Trip의 목적·우선순위·동작절차가 완전히 같다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_cause_effect",
      "anchor_id": "sw02_cause_effect",
      "statement": "Cause & Effect는 원인신호와 요구되는 결과동작을 행렬 또는 표로 연결하여 Interlock·Trip·Alarm·Shutdown의 설계 의도를 명확히 하지만, 세부 상태전이·타이머·Reset·우선순위까지 포함한 실행논리 자체를 자동으로 대체하지는 않는다.",
      "importance": "must",
      "keywords": [
        "Cause & Effect",
        "원인",
        "결과동작",
        "행렬",
        "설계 의도",
        "실행논리"
      ],
      "core_terms": [
        "Cause & Effect",
        "원인-결과",
        "실행논리"
      ],
      "accepted_explanations": [
        "Cause & Effect는 원인신호와 요구되는 결과동작을 행렬 또는 표로 연결하여 Interlock·Trip·Alarm·Shutdown의 설계 의도를 명확히 하지만, 세부 상태전이·타이머·Reset·우선순위까지 포함한 실행논리 자체를 자동으로 대체하지는 않는다.",
        "Cause & Effect, 원인-결과, 실행논리의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Cause & Effect 표만으로 상태전이·Timer·Reset·우선순위의 구현과 검증이 모두 완료된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_voting_logic",
      "anchor_id": "sw02_voting_logic",
      "statement": "Voting logic은 N개 입력 중 M개 이상이 Trip 조건일 때 동작하는 M-out-of-N 구조이며, 채널 독립성·공통원인·진단·불일치 처리와 함께 설계해야 한다.",
      "importance": "must",
      "keywords": [
        "Voting",
        "M-out-of-N",
        "2oo3",
        "채널 독립성",
        "공통원인",
        "불일치"
      ],
      "core_terms": [
        "Voting",
        "M-out-of-N",
        "채널 독립성"
      ],
      "accepted_explanations": [
        "Voting logic은 N개 입력 중 M개 이상이 Trip 조건일 때 동작하는 M-out-of-N 구조이며, 채널 독립성·공통원인·진단·불일치 처리와 함께 설계해야 한다.",
        "Voting, M-out-of-N, 채널 독립성의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "M-out-of-N 채널 수만 늘리면 독립성·공통원인·진단과 무관하게 항상 안전해진다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_first_out",
      "anchor_id": "sw02_first_out",
      "statement": "First-out은 연쇄 Trip에서 가장 먼저 발생한 유효 원인을 시간순으로 고정하여 후속 결과신호와 구분하는 기능이며, 원인진단과 복구 판단에 사용한다.",
      "importance": "must",
      "keywords": [
        "First-out",
        "최초 원인",
        "연쇄 Trip",
        "시간순",
        "원인진단"
      ],
      "core_terms": [
        "First-out",
        "최초 원인",
        "연쇄"
      ],
      "accepted_explanations": [
        "First-out은 연쇄 Trip에서 가장 먼저 발생한 유효 원인을 시간순으로 고정하여 후속 결과신호와 구분하는 기능이며, 원인진단과 복구 판단에 사용한다.",
        "First-out, 최초 원인, 연쇄의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "마지막에 남은 Trip 신호나 가장 높은 Alarm priority를 최초 원인으로 저장한다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_bypass",
      "anchor_id": "sw02_bypass",
      "statement": "Bypass는 특정 입력 또는 보호경로를 제한된 조건과 기간 동안 우회하는 관리된 기능이며, 승인·표시·시간제한·대체조치·복구확인을 포함해야 한다.",
      "importance": "must",
      "keywords": [
        "Bypass",
        "우회",
        "승인",
        "표시",
        "시간제한",
        "대체조치",
        "복구확인"
      ],
      "core_terms": [
        "Bypass",
        "시간제한",
        "대체조치",
        "복구"
      ],
      "accepted_explanations": [
        "Bypass는 특정 입력 또는 보호경로를 제한된 조건과 기간 동안 우회하는 관리된 기능이며, 승인·표시·시간제한·대체조치·복구확인을 포함해야 한다.",
        "Bypass, 시간제한, 대체조치, 복구의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "승인·표시·기간·대체조치·복구확인 없이 입력 또는 보호경로를 계속 우회해도 된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_override",
      "anchor_id": "sw02_override",
      "statement": "Override는 정상 명령 또는 자동출력보다 우선하는 강제 명령으로, Bypass와 목적이 다르며 권한·우선순위·범위·해제조건을 명확히 해야 한다.",
      "importance": "must",
      "keywords": [
        "Override",
        "강제 명령",
        "우선순위",
        "권한",
        "해제조건",
        "Bypass 구분"
      ],
      "core_terms": [
        "Override",
        "강제 명령",
        "우선순위"
      ],
      "accepted_explanations": [
        "Override는 정상 명령 또는 자동출력보다 우선하는 강제 명령으로, Bypass와 목적이 다르며 권한·우선순위·범위·해제조건을 명확히 해야 한다.",
        "Override, 강제 명령, 우선순위의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Override를 입력·보호경로를 우회하는 Bypass와 동일시하거나 우선순위와 해제조건 없이 강제명령해도 된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_fail_safe",
      "anchor_id": "sw02_fail_safe",
      "statement": "Fail-safe는 전원·공기·통신·제어기 또는 신호 고장 시 위험을 최소화하는 사전 정의 상태와 동작을 말하며, 항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라 공정 위험분석과 최종요소 특성에 따라 정한다.",
      "importance": "must",
      "keywords": [
        "Fail-safe",
        "Safe state",
        "Fail-close",
        "Fail-open",
        "De-energize",
        "위험 최소화"
      ],
      "core_terms": [
        "Fail-safe",
        "Safe state",
        "공정 위험"
      ],
      "accepted_explanations": [
        "Fail-safe는 전원·공기·통신·제어기 또는 신호 고장 시 위험을 최소화하는 사전 정의 상태와 동작을 말하며, 항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라 공정 위험분석과 최종요소 특성에 따라 정한다.",
        "Fail-safe, Safe state, 공정 위험의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "모든 최종요소를 항상 Fail-close 또는 De-energize 상태로 만들어야 한다고 일반화한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_watchdog",
      "anchor_id": "sw02_watchdog",
      "statement": "Watchdog는 제어기 Task, 통신, 원격 I/O 또는 장치의 정상 갱신을 감시하고 정해진 시간 내 Heartbeat가 없으면 진단상태를 만들고 사전 정의된 Hold, Controlled stop 또는 Safe action으로 전환한다.",
      "importance": "must",
      "keywords": [
        "Watchdog",
        "Heartbeat",
        "Timeout",
        "Hold",
        "Controlled stop",
        "Safe action"
      ],
      "core_terms": [
        "Watchdog",
        "Heartbeat",
        "Timeout",
        "Safe action"
      ],
      "accepted_explanations": [
        "Watchdog는 제어기 Task, 통신, 원격 I/O 또는 장치의 정상 갱신을 감시하고 정해진 시간 내 Heartbeat가 없으면 진단상태를 만들고 사전 정의된 Hold, Controlled stop 또는 Safe action으로 전환한다.",
        "Watchdog, Heartbeat, Timeout, Safe action의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "운전·보호에 필요한 제어기 Task나 필수 통신의 Heartbeat 상실을 표시만 하고 사전 정의 대응동작은 필요 없다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_feedback_confirmation_timeout",
      "anchor_id": "sw02_feedback_confirmation_timeout",
      "statement": "Sequence는 명령 출력만으로 단계완료를 판단하지 않고 위치·압력·속도·접점 등 독립적인 설비 피드백과 Timeout을 사용하여 성공, 지연, 고착, 센서불일치를 구분한다.",
      "importance": "must",
      "keywords": [
        "Feedback confirmation",
        "Timeout",
        "설비 피드백",
        "고착",
        "센서불일치",
        "단계완료"
      ],
      "core_terms": [
        "피드백 확인",
        "Timeout",
        "단계완료"
      ],
      "accepted_explanations": [
        "Sequence는 명령 출력만으로 단계완료를 판단하지 않고 위치·압력·속도·접점 등 독립적인 설비 피드백과 Timeout을 사용하여 성공, 지연, 고착, 센서불일치를 구분한다.",
        "피드백 확인, Timeout, 단계완료의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "밸브 개폐·모터 기동·위치이동처럼 물리적 동작 확인이 필요한 Step에서 Command 출력이나 Timer 만료만으로 완료를 선언한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_trip_latch_reset",
      "anchor_id": "sw02_trip_latch_reset",
      "statement": "Trip Latch는 원인이 순간적으로 사라져도 보호상태를 유지하며, Reset은 원인 제거, 안전조건 재확인, 조작권한 및 Reset edge가 모두 유효할 때만 허용해야 한다.",
      "importance": "must",
      "keywords": [
        "Trip latch",
        "Reset",
        "원인 제거",
        "안전조건",
        "권한",
        "Reset edge"
      ],
      "core_terms": [
        "Trip latch",
        "Reset 조건",
        "원인 제거"
      ],
      "accepted_explanations": [
        "Trip Latch는 원인이 순간적으로 사라져도 보호상태를 유지하며, Reset은 원인 제거, 안전조건 재확인, 조작권한 및 Reset edge가 모두 유효할 때만 허용해야 한다.",
        "Trip latch, Reset 조건, 원인 제거의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "원인이 순간적으로 사라지면 안전조건·권한·Reset edge 확인 없이 Latch를 해제하고 재기동한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_abnormal_transition_prevention",
      "anchor_id": "sw02_abnormal_transition_prevention",
      "statement": "비정상 전이 방지는 허용 전이표, Mutual exclusion, One-hot state, 전이 중 재명령 차단, Timeout, Debounce, 입력 품질검사 및 Illegal-state recovery를 조합하여 구현한다.",
      "importance": "must",
      "keywords": [
        "허용 전이표",
        "Mutual exclusion",
        "One-hot",
        "Illegal state",
        "Debounce",
        "Timeout"
      ],
      "core_terms": [
        "허용 전이표",
        "Mutual exclusion",
        "Illegal state"
      ],
      "accepted_explanations": [
        "비정상 전이 방지는 허용 전이표, Mutual exclusion, One-hot state, 전이 중 재명령 차단, Timeout, Debounce, 입력 품질검사 및 Illegal-state recovery를 조합하여 구현한다.",
        "허용 전이표, Mutual exclusion, Illegal state의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "허용되지 않은 상태조합·중복상태·전이 중 재명령·불량입력을 정상 전이로 처리하고 Illegal-state recovery를 두지 않는다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_command_arbitration",
      "anchor_id": "sw02_command_arbitration",
      "statement": "Local·Remote, Manual·Auto, Sequence·Operator, Normal·Trip 명령이 경쟁할 때는 명시적인 명령 우선순위와 단일 출력 소유자를 정하고, 보호동작은 정상 운전명령보다 우선하도록 한다.",
      "importance": "must",
      "keywords": [
        "Command arbitration",
        "Local Remote",
        "Manual Auto",
        "Priority",
        "Output owner",
        "Trip priority"
      ],
      "core_terms": [
        "명령 우선순위",
        "출력 소유자",
        "Trip 우선"
      ],
      "accepted_explanations": [
        "Local·Remote, Manual·Auto, Sequence·Operator, Normal·Trip 명령이 경쟁할 때는 명시적인 명령 우선순위와 단일 출력 소유자를 정하고, 보호동작은 정상 운전명령보다 우선하도록 한다.",
        "명령 우선순위, 출력 소유자, Trip 우선의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Local·Remote, Manual·Auto와 Trip 명령의 우선순위·단일 출력 소유자를 정의하지 않아 여러 명령이 동시에 출력을 지배해도 된다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_signal_quality",
      "anchor_id": "sw02_signal_quality",
      "statement": "Bad quality, stale data, 통신단절 또는 비현실값을 정상 신호로 간주해서는 안 되며, 입력별 대체값·Hold·Trip·Degraded mode 정책을 명시해야 한다.",
      "importance": "must",
      "keywords": [
        "Bad quality",
        "Stale data",
        "통신단절",
        "대체값",
        "Hold",
        "Degraded mode"
      ],
      "core_terms": [
        "신호 품질",
        "Stale data",
        "Degraded mode"
      ],
      "accepted_explanations": [
        "Bad quality, stale data, 통신단절 또는 비현실값을 정상 신호로 간주해서는 안 되며, 입력별 대체값·Hold·Trip·Degraded mode 정책을 명시해야 한다.",
        "신호 품질, Stale data, Degraded mode의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Bad·Stale·통신단절 값을 최신 정상값으로 간주하고 입력 품질별 대응정책을 두지 않는다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_restart_recovery",
      "anchor_id": "sw02_restart_recovery",
      "statement": "Restart와 Recovery는 Cold start, Warm restart, 통신복구 및 부분정전 시나리오를 구분하고, 실제 설비상태를 재수집한 뒤 State reconciliation, Permissive 재확인, Latch 보존 및 운영자 승인 여부에 따라 재개한다.",
      "importance": "must",
      "keywords": [
        "Restart",
        "Recovery",
        "Cold start",
        "Warm restart",
        "State reconciliation",
        "Latch 보존"
      ],
      "core_terms": [
        "Restart",
        "State reconciliation",
        "Permissive 재확인"
      ],
      "accepted_explanations": [
        "Restart와 Recovery는 Cold start, Warm restart, 통신복구 및 부분정전 시나리오를 구분하고, 실제 설비상태를 재수집한 뒤 State reconciliation, Permissive 재확인, Latch 보존 및 운영자 승인 여부에 따라 재개한다.",
        "Restart, State reconciliation, Permissive 재확인의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "전원·통신 복구 즉시 실제 설비상태와 Permissive를 확인하지 않고 이전 Step과 출력을 그대로 복원한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_degraded_mode",
      "anchor_id": "sw02_degraded_mode",
      "statement": "Degraded mode는 일부 기능 또는 신호가 상실된 상태에서 허용되는 제한운전 범위와 금지동작, 감시강화, 종료조건을 정의한 운전상태이며 무조건적인 계속운전을 의미하지 않는다.",
      "importance": "important",
      "keywords": [
        "Degraded mode",
        "제한운전",
        "금지동작",
        "감시강화",
        "종료조건"
      ],
      "core_terms": [
        "Degraded mode",
        "제한운전",
        "종료조건"
      ],
      "accepted_explanations": [
        "Degraded mode는 일부 기능 또는 신호가 상실된 상태에서 허용되는 제한운전 범위와 금지동작, 감시강화, 종료조건을 정의한 운전상태이며 무조건적인 계속운전을 의미하지 않는다.",
        "Degraded mode, 제한운전, 종료조건의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Degraded mode를 제한범위·금지동작·감시강화·종료조건이 없는 무조건 계속운전으로 정의한다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_scan_edge_memory",
      "anchor_id": "sw02_scan_edge_memory",
      "statement": "PLC/DCS의 Scan 기반 논리는 Level 신호와 Edge 이벤트, One-shot, Memory/Latch를 구분해야 하며, 한 Scan 내 Set·Reset 순서와 출력 갱신순서가 의도한 우선순위를 보장해야 한다.",
      "importance": "important",
      "keywords": [
        "Scan",
        "Edge",
        "One-shot",
        "Memory",
        "Set Reset priority",
        "Output update"
      ],
      "core_terms": [
        "Scan",
        "Edge",
        "Set Reset 우선순위"
      ],
      "accepted_explanations": [
        "PLC/DCS의 Scan 기반 논리는 Level 신호와 Edge 이벤트, One-shot, Memory/Latch를 구분해야 하며, 한 Scan 내 Set·Reset 순서와 출력 갱신순서가 의도한 우선순위를 보장해야 한다.",
        "Scan, Edge, Set Reset 우선순위의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Level·Edge·One-shot·Latch와 Set·Reset 실행순서가 Scan 결과와 우선순위에 영향을 주지 않는다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_debounce_hysteresis",
      "anchor_id": "sw02_debounce_hysteresis",
      "statement": "접점 Chattering과 임계값 진동은 Debounce, On-delay·Off-delay, Hysteresis 및 지속시간 조건으로 억제하되, 보호응답 지연과 놓침 위험을 함께 검토해야 한다.",
      "importance": "important",
      "keywords": [
        "Debounce",
        "Chattering",
        "On-delay",
        "Off-delay",
        "Hysteresis",
        "응답지연"
      ],
      "core_terms": [
        "Debounce",
        "Hysteresis",
        "응답지연"
      ],
      "accepted_explanations": [
        "접점 Chattering과 임계값 진동은 Debounce, On-delay·Off-delay, Hysteresis 및 지속시간 조건으로 억제하되, 보호응답 지연과 놓침 위험을 함께 검토해야 한다.",
        "Debounce, Hysteresis, 응답지연의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Debounce·Delay·Hysteresis를 무조건 크게 하면 보호성능이 향상되고 응답지연이나 사건 놓침 위험은 없다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_manual_mode_boundary",
      "anchor_id": "sw02_manual_mode_boundary",
      "statement": "Manual mode는 정상 자동 Sequence를 우회할 수 있지만 필수 보호 Interlock과 Trip까지 자동으로 무효화하는 모드가 아니며, 수동조작 가능 범위와 금지조건을 별도로 정의해야 한다.",
      "importance": "must",
      "keywords": [
        "Manual mode",
        "자동 Sequence",
        "보호 Interlock",
        "Trip",
        "수동조작 범위"
      ],
      "core_terms": [
        "Manual mode",
        "보호 Interlock",
        "금지조건"
      ],
      "accepted_explanations": [
        "Manual mode는 정상 자동 Sequence를 우회할 수 있지만 필수 보호 Interlock과 Trip까지 자동으로 무효화하는 모드가 아니며, 수동조작 가능 범위와 금지조건을 별도로 정의해야 한다.",
        "Manual mode, 보호 Interlock, 금지조건의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Manual mode가 필수 보호 Interlock과 Trip을 자동으로 모두 무효화한다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_sw03_boundary",
      "anchor_id": "sw02_sw03_boundary",
      "statement": "SW-03은 HMI·SCADA 화면, Alarm 우선순위·Deadband·Delay·Shelving·Suppression, Setpoint list, SOE 표시, Audit trail 및 Operator authority를 소유하고, SW-02는 그 정보가 발생하는 실제 Interlock·Trip·Sequence 상태전이 논리를 소유한다.",
      "importance": "important",
      "keywords": [
        "SW-03 boundary",
        "HMI",
        "SCADA",
        "Alarm management",
        "SOE",
        "Operator authority"
      ],
      "core_terms": [
        "SW-03",
        "운전정보",
        "논리 소유권"
      ],
      "accepted_explanations": [
        "SW-03은 HMI·SCADA 화면, Alarm 우선순위·Deadband·Delay·Shelving·Suppression, Setpoint list, SOE 표시, Audit trail 및 Operator authority를 소유하고, SW-02는 그 정보가 발생하는 실제 Interlock·Trip·Sequence 상태전이 논리를 소유한다.",
        "SW-03, 운전정보, 논리 소유권의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "Alarm philosophy·Shelving·SOE 표시 운영을 SW-02 실행논리 자체로 소유하거나 실제 Interlock·Trip 상태전이를 SW-03에 넘긴다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    },
    {
      "id": "sw02_sw05_boundary",
      "anchor_id": "sw02_sw05_boundary",
      "statement": "SW-05는 SIL 산정, 안전수명주기, 체계적 고장 통제, 독립성 및 Safety V&V를 소유하고, SW-02는 SIL 등급 산정이 아닌 운전논리의 상태전이와 보호동작 메커니즘만 소유한다.",
      "importance": "important",
      "keywords": [
        "SW-05 boundary",
        "SIL",
        "안전수명주기",
        "독립성",
        "Safety V&V",
        "운전논리"
      ],
      "core_terms": [
        "SW-05",
        "SIL 산정 제외",
        "운전논리"
      ],
      "accepted_explanations": [
        "SW-05는 SIL 산정, 안전수명주기, 체계적 고장 통제, 독립성 및 Safety V&V를 소유하고, SW-02는 SIL 등급 산정이 아닌 운전논리의 상태전이와 보호동작 메커니즘만 소유한다.",
        "SW-05, SIL 산정 제외, 운전논리의 관계를 원인-조건-동작-복구 순서로 설명한다."
      ],
      "rejected_explanations": [
        "일반 운전논리 설명만으로 SIL 산정·Safety lifecycle·독립성·Safety V&V까지 충족했다고 본다."
      ],
      "grading_notes": "직접적인 반대 주장은 fatal 후보이며, 단순 누락은 문항 요구범위에 따라 major 또는 warn으로 평가한다.",
      "source_basis": "일반 산업 제어공학 및 운전 제어논리 설계 원칙"
    }
  ],
  "fatal_wrong_claims": [
    {
      "id": "sw02_fatal_permissive_equals_trip",
      "claim": "Permissive와 Trip은 같은 논리이다.",
      "wrong_claim": "Permissive와 Trip은 같은 논리이다.",
      "correction": "Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
      "correct_rule": "Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Permissive와 Trip은 같은 논리이다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_interlock_alarm_only",
      "claim": "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다.",
      "wrong_claim": "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다.",
      "correction": "Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
      "correct_rule": "Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_trip_unconditional_auto_reset",
      "claim": "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다.",
      "wrong_claim": "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다.",
      "correction": "Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
      "correct_rule": "Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_bypass_unmanaged",
      "claim": "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다.",
      "wrong_claim": "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다.",
      "correction": "Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
      "correct_rule": "Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D",
        "E"
      ],
      "message": "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_fail_safe_always_close",
      "claim": "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다.",
      "wrong_claim": "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다.",
      "correction": "안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
      "correct_rule": "안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. 안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_voting_always_safer",
      "claim": "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다.",
      "wrong_claim": "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다.",
      "correction": "Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
      "correct_rule": "Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_first_out_last_cause",
      "claim": "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다.",
      "wrong_claim": "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다.",
      "correction": "First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
      "correct_rule": "First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_watchdog_monitor_only",
      "claim": "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다.",
      "wrong_claim": "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다.",
      "correction": "제어기 Task, 필수 통신, 원격 I/O와 보호 관련 경로의 Watchdog Timeout은 위험분석에 따라 Hold, Controlled stop 또는 Safe action에 연결한다. 비중요 Historian, 상태수집과 진단 경로는 공정위험에 직접 영향을 주지 않는 경우 Alarm-only 처리를 적용할 수 있다.",
      "correct_rule": "제어기 Task, 필수 통신, 원격 I/O 등 운전·보호에 필요한 Watchdog Timeout은 진단과 함께 Hold, Controlled stop 또는 Safe action으로 연결한다. 비중요 Historian·상태수집·진단경로는 위험분석에 따라 Alarm-only 처리가 가능하다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. 제어기 Task, 필수 통신, 원격 I/O와 보호 관련 경로의 Watchdog Timeout은 위험분석에 따라 Hold, Controlled stop 또는 Safe action에 연결한다. 비중요 Historian, 상태수집과 진단 경로는 공정위험에 직접 영향을 주지 않는 경우 Alarm-only 처리를 적용할 수 있다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_restart_blind_resume",
      "claim": "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다.",
      "wrong_claim": "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다.",
      "correction": "Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
      "correct_rule": "Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_cause_effect_is_executable_complete",
      "claim": "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다.",
      "wrong_claim": "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다.",
      "correction": "Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
      "correct_rule": "Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_timer_is_feedback",
      "claim": "밸브 개폐, 모터 기동, 위치이동처럼 물리적 동작 확인이 필요한 Step도 Timer가 만료되면 실제 설비 Feedback과 관계없이 완료로 판단해도 된다.",
      "wrong_claim": "밸브 개폐·모터 기동·위치이동처럼 물리적 동작 확인이 필요한 Step도 Timer가 만료되면 실제 설비 Feedback과 관계없이 완료로 판단해도 된다.",
      "correction": "물리적 동작 완료는 필요한 설비 Feedback으로 확인한다. 다만 Purge 유지시간, 안정화 대기, 혼합시간처럼 시간 자체가 공정 요구조건인 Step은 Timer 만료를 정상 완료조건으로 사용할 수 있다.",
      "correct_rule": "물리적 동작 확인이 필요한 Step에서 Timer는 최대 허용시간 또는 지연조건일 뿐이며 완료는 필요한 설비 Feedback으로 확인한다. 반면 Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Timer가 만료되면 실제 설비 피드백과 관계없이 Step 완료로 판단해도 된다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. 물리적 동작 확인이 필요한 Step은 필요한 설비 Feedback으로 완료를 확인한다. 다만 Purge 유지시간, 안정화 대기, 혼합시간처럼 시간 자체가 공정 요구조건인 Step은 Timer 만료를 정상 완료조건으로 사용할 수 있다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_override_equals_bypass",
      "claim": "Override와 Bypass는 완전히 같은 기능이다.",
      "wrong_claim": "Override와 Bypass는 완전히 같은 기능이다.",
      "correction": "Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
      "correct_rule": "Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Override와 Bypass는 완전히 같은 기능이다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_shutdown_equals_trip",
      "claim": "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다.",
      "wrong_claim": "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다.",
      "correction": "정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
      "correct_rule": "정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. 정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_all_interlocks_are_sis",
      "claim": "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다.",
      "wrong_claim": "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다.",
      "correction": "운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
      "correct_rule": "운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. 운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_manual_disables_protection",
      "claim": "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다.",
      "wrong_claim": "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다.",
      "correction": "Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
      "correct_rule": "Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    },
    {
      "id": "sw02_fatal_bad_signal_is_healthy",
      "claim": "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다.",
      "wrong_claim": "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다.",
      "correction": "Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
      "correct_rule": "Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
      "severity": "fatal",
      "affected_layers": [
        "C",
        "D"
      ],
      "message": "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다.",
      "description": "핵심 운전논리의 의미를 반대로 설명한 오류이다. Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
      "grading_notes": "문맥상 명시적 주장일 때만 fatal로 판정하고, 단순 미언급은 fatal로 판정하지 않는다."
    }
  ],
  "safe_expressions": [
    "Permissive는 기동 또는 전이를 허가하는 사전조건이고 Trip은 보호조건 성립 시 강제정지를 요구하는 동작이다.",
    "Interlock은 운전 중 위험한 조합을 금지하거나 출력을 강제할 수 있으며 Alarm은 운전자 정보 제공 기능이다.",
    "Trip의 Latch와 Reset 방식은 위험도와 공정 요구에 따라 정하되 원인 제거와 안전조건 확인이 우선이다.",
    "Fail-safe 상태는 설비마다 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 다를 수 있다.",
    "De-energize-to-trip은 흔한 구현 원칙이지만 모든 설비의 유일한 안전상태는 아니다.",
    "Voting은 채널 독립성, 공통원인, 진단과 불일치 처리까지 함께 검토해야 한다.",
    "First-out은 연쇄 Trip에서 최초 원인을 보존한다.",
    "Bypass는 유지보수에 필요할 수 있으나 승인, 표시, 제한시간과 복구확인이 필요하다.",
    "Override는 강제 명령이고 Bypass는 보호경로 우회이므로 목적과 권한을 구분한다.",
    "Watchdog Timeout 시 Hold 또는 안전동작은 공정 위험과 복구전략에 따라 선택한다.",
    "Restart 후 자동재개가 가능한 비위험 설비도 있으나 상태 일치와 Permissive 검증이 선행되어야 한다.",
    "Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
    "Manual mode에서도 필수 보호논리는 유지해야 한다.",
    "Cause & Effect는 논리 설계의 기준문서이며 상세 상태전이와 구현검증이 추가로 필요하다.",
    "운전 Interlock이 모두 SIS인 것은 아니며 SIL 산정은 별도 안전수명주기 범위이다.",
    "Alarm Deadband, Shelving, SOE 표시와 Operator authority는 SW-03의 주 소유범위이다.",
    "SW-02는 SOE에 표시될 이벤트의 실제 발생논리와 First-out 메커니즘을 다루되 화면·Alarm 관리정책은 SW-03에 넘긴다.",
    "SIL 산정, 체계적 고장, 독립성 및 Safety V&V는 SW-05로 넘긴다.",
    "비중요 Historian·상태수집·진단경로의 Watchdog는 위험분석에 따라 Alarm-only로 처리할 수 있다."
  ],
  "revision_notes": [
    "2026-08-06: SOFTWARE_LLM_LANE_A SW-02 source Topic Pack 최초 작성.",
    "SW-03의 HMI·Alarm·SOE·권한과 SW-05의 SIL·안전수명주기·Safety V&V를 ownership 경계로 분리했다.",
    "generated bank, 공통 Router, 기존 Topic Pack은 변경하지 않는다.",
    "2026-08-07 LLM 의미 감사 수리: Anchor별 rejected 설명, 조건부 Transition guard, Timer·Watchdog false-positive 경계를 반영했다."
  ],
  "topic_label": "SW-02 제어논리·Sequence·Interlock·Trip",
  "core_facts": [
    "SW-02는 운전 제어논리의 동작 메커니즘을 다루며 Sequence, 상태전이, Interlock, Permissive, Trip, Shutdown, Cause & Effect, Voting, First-out, Bypass, Override, Fail-safe, Watchdog 및 Restart·Recovery를 하나의 운전 논리 체계로 연결한다.",
    "Sequence control은 공정을 여러 Step 또는 State로 나누고, 각 단계의 진입조건·실행동작·완료조건·시간제한·실패처리를 정의하여 정해진 순서로 운전하는 제어방식이다.",
    "상태전이는 현재 상태와 명령, Permissive, Interlock, Trip, 설비 피드백 및 시간조건을 입력으로 다음 상태를 결정하는 함수로 표현할 수 있으며, 동일 입력에서 결정론적 결과가 나와야 한다.",
    "Transition guard는 상태변화를 허용하는 논리조건이다. 기동·명령 기반 전이의 대표식은 Command AND 모든 필수 Permissive AND 필요한 선행 Feedback AND NOT Trip AND NOT Inhibit로 나타낼 수 있다. 자동 진행, 시간 유지 완료 또는 공정조건 도달 전이는 Command 없이 성립할 수 있으며, Feedback은 전이의 선행조건 또는 동작 완료 확인조건으로 구분한다.",
    "각 State에는 Entry action, 지속 동작, Exit action을 구분하여 정의해야 하며, 출력은 상태와 전이 이벤트의 소유관계를 명확히 하여 중복 명령과 잔류 출력을 방지한다.",
    "Permissive는 기동 또는 특정 전이를 시작하기 전에 만족해야 하는 사전 허가조건이며, 보통 모든 필수 조건의 AND 논리로 구성한다.",
    "Interlock은 위험하거나 비정상적인 조합을 방지하기 위해 동작을 금지하거나 운전 중 특정 출력을 강제하는 제약논리이며, 단순 Alarm 표시와 구분된다.",
    "Trip은 보호조건이 성립할 때 정상 Sequence보다 우선하여 설비 또는 공정을 미리 정한 정지상태로 이행시키는 강제 보호동작이며, 위험도와 공정특성에 따라 Latch와 수동 Reset을 적용한다.",
    "Shutdown은 정상정지, 공정정지, 비상정지 등 목적과 속도에 따라 구분하며, 정상정지는 순차적 감속·배출·정리 절차를 따를 수 있지만 Trip은 보호목적의 우선 동작으로 설계한다.",
    "Cause & Effect는 원인신호와 요구되는 결과동작을 행렬 또는 표로 연결하여 Interlock·Trip·Alarm·Shutdown의 설계 의도를 명확히 하지만, 세부 상태전이·타이머·Reset·우선순위까지 포함한 실행논리 자체를 자동으로 대체하지는 않는다.",
    "Voting logic은 N개 입력 중 M개 이상이 Trip 조건일 때 동작하는 M-out-of-N 구조이며, 채널 독립성·공통원인·진단·불일치 처리와 함께 설계해야 한다.",
    "First-out은 연쇄 Trip에서 가장 먼저 발생한 유효 원인을 시간순으로 고정하여 후속 결과신호와 구분하는 기능이며, 원인진단과 복구 판단에 사용한다.",
    "Bypass는 특정 입력 또는 보호경로를 제한된 조건과 기간 동안 우회하는 관리된 기능이며, 승인·표시·시간제한·대체조치·복구확인을 포함해야 한다.",
    "Override는 정상 명령 또는 자동출력보다 우선하는 강제 명령으로, Bypass와 목적이 다르며 권한·우선순위·범위·해제조건을 명확히 해야 한다.",
    "Fail-safe는 전원·공기·통신·제어기 또는 신호 고장 시 위험을 최소화하는 사전 정의 상태와 동작을 말하며, 항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라 공정 위험분석과 최종요소 특성에 따라 정한다.",
    "Watchdog는 제어기 Task, 통신, 원격 I/O 또는 장치의 정상 갱신을 감시하고 정해진 시간 내 Heartbeat가 없으면 진단상태를 만들고 사전 정의된 Hold, Controlled stop 또는 Safe action으로 전환한다.",
    "Sequence는 명령 출력만으로 단계완료를 판단하지 않고 위치·압력·속도·접점 등 독립적인 설비 피드백과 Timeout을 사용하여 성공, 지연, 고착, 센서불일치를 구분한다.",
    "Trip Latch는 원인이 순간적으로 사라져도 보호상태를 유지하며, Reset은 원인 제거, 안전조건 재확인, 조작권한 및 Reset edge가 모두 유효할 때만 허용해야 한다.",
    "비정상 전이 방지는 허용 전이표, Mutual exclusion, One-hot state, 전이 중 재명령 차단, Timeout, Debounce, 입력 품질검사 및 Illegal-state recovery를 조합하여 구현한다.",
    "Local·Remote, Manual·Auto, Sequence·Operator, Normal·Trip 명령이 경쟁할 때는 명시적인 명령 우선순위와 단일 출력 소유자를 정하고, 보호동작은 정상 운전명령보다 우선하도록 한다.",
    "Bad quality, stale data, 통신단절 또는 비현실값을 정상 신호로 간주해서는 안 되며, 입력별 대체값·Hold·Trip·Degraded mode 정책을 명시해야 한다.",
    "Restart와 Recovery는 Cold start, Warm restart, 통신복구 및 부분정전 시나리오를 구분하고, 실제 설비상태를 재수집한 뒤 State reconciliation, Permissive 재확인, Latch 보존 및 운영자 승인 여부에 따라 재개한다.",
    "Degraded mode는 일부 기능 또는 신호가 상실된 상태에서 허용되는 제한운전 범위와 금지동작, 감시강화, 종료조건을 정의한 운전상태이며 무조건적인 계속운전을 의미하지 않는다.",
    "PLC/DCS의 Scan 기반 논리는 Level 신호와 Edge 이벤트, One-shot, Memory/Latch를 구분해야 하며, 한 Scan 내 Set·Reset 순서와 출력 갱신순서가 의도한 우선순위를 보장해야 한다.",
    "접점 Chattering과 임계값 진동은 Debounce, On-delay·Off-delay, Hysteresis 및 지속시간 조건으로 억제하되, 보호응답 지연과 놓침 위험을 함께 검토해야 한다.",
    "Manual mode는 정상 자동 Sequence를 우회할 수 있지만 필수 보호 Interlock과 Trip까지 자동으로 무효화하는 모드가 아니며, 수동조작 가능 범위와 금지조건을 별도로 정의해야 한다.",
    "SW-03은 HMI·SCADA 화면, Alarm 우선순위·Deadband·Delay·Shelving·Suppression, Setpoint list, SOE 표시, Audit trail 및 Operator authority를 소유하고, SW-02는 그 정보가 발생하는 실제 Interlock·Trip·Sequence 상태전이 논리를 소유한다.",
    "SW-05는 SIL 산정, 안전수명주기, 체계적 고장 통제, 독립성 및 Safety V&V를 소유하고, SW-02는 SIL 등급 산정이 아닌 운전논리의 상태전이와 보호동작 메커니즘만 소유한다."
  ]
}
EOF_SW02_FACT_ANCHOR_4E91
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json" <<'EOF_SW02_LOGIC_CHECK_5B37'
{
  "schema_version": "topic_pack.logic_check.v1",
  "topic_id": "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
  "title": "제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe",
  "deterministic_checks": {
    "enabled": true,
    "topic_name": "제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe",
    "question_type": "PRINCIPLE_INTERPRETATION",
    "difficulty_profile": "DESIGN_EVALUATION",
    "topic_aliases": [
      "제어논리 Sequence Interlock Permissive Trip",
      "시퀀스 상태전이 인터록 퍼미시브 트립",
      "Sequence control state transition interlock permissive trip",
      "운전 제어논리와 상태전이",
      "Interlock Permissive Trip 차이",
      "인터록 퍼미시브 트립 차이",
      "Cause & Effect Voting First-out",
      "원인 결과표 Voting First-out",
      "Bypass Override 제어논리",
      "바이패스 오버라이드 명령 우선순위",
      "Fail-safe Watchdog Restart Recovery",
      "Fail safe watchdog 재기동 복구논리",
      "Sequence abnormal transition prevention",
      "시퀀스 이상전이 방지",
      "Trip latch reset logic",
      "트립 래치 리셋 조건",
      "Manual Auto Local Remote command arbitration",
      "수동 자동 로컬 리모트 명령 중재",
      "PLC sequence feedback timeout one-shot latch",
      "상태전이표 mutual exclusion illegal state recovery"
    ],
    "fatal_checks": [
      {
        "id": "sw02_fatal_permissive_equals_trip",
        "severity": "fatal",
        "message": "Permissive와 Trip은 같은 논리이다.",
        "description": "명시적 반대 주장만 검출한다. Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
        "correct_rule": "Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Permissive와\\ Trip은\\ 같은\\ 논리이다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Permissive와 Trip은 같은 논리이다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_interlock_alarm_only",
        "severity": "fatal",
        "message": "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다.",
        "description": "명시적 반대 주장만 검출한다. Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
        "correct_rule": "Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Interlock은\\ Alarm만\\ 발생시키며\\ 동작을\\ 차단하거나\\ 강제하지\\ 않는다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_trip_unconditional_auto_reset",
        "severity": "fatal",
        "message": "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다.",
        "description": "명시적 반대 주장만 검출한다. Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
        "correct_rule": "Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Trip\\ 원인이\\ 사라지면\\ 즉시\\ 자동\\ Reset하여\\ 운전을\\ 재개해야\\ 한다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_bypass_unmanaged",
        "severity": "fatal",
        "message": "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다.",
        "description": "명시적 반대 주장만 검출한다. Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
        "correct_rule": "Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Bypass는\\ 점검\\ 편의를\\ 위해\\ 승인이나\\ 시간제한\\ 없이\\ 계속\\ 유지해도\\ 된다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다."
        ],
        "affected_layers": [
          "C",
          "D",
          "E"
        ]
      },
      {
        "id": "sw02_fatal_fail_safe_always_close",
        "severity": "fatal",
        "message": "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다.",
        "description": "명시적 반대 주장만 검출한다. 안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
        "correct_rule": "안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Fail\\-safe는\\ 모든\\ 설비를\\ 무조건\\ Fail\\-close\\ 또는\\ De\\-energize로\\ 만드는\\ 것이다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_voting_always_safer",
        "severity": "fatal",
        "message": "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다.",
        "description": "명시적 반대 주장만 검출한다. Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
        "correct_rule": "Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Voting\\ 채널\\ 수를\\ 늘리면\\ 독립성이나\\ 공통원인과\\ 관계없이\\ 항상\\ 더\\ 안전해진다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_first_out_last_cause",
        "severity": "fatal",
        "message": "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다.",
        "description": "명시적 반대 주장만 검출한다. First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
        "correct_rule": "First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?First\\-out은\\ 마지막에\\ 남은\\ Trip\\ 신호\\ 또는\\ 가장\\ 우선순위가\\ 높은\\ Alarm을\\ 기록한다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_watchdog_monitor_only",
        "severity": "fatal",
        "message": "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다.",
        "description": "명시적 반대 주장만 검출한다. 제어기 Task, 필수 통신, 원격 I/O 등 운전·보호에 필요한 Watchdog Timeout은 진단과 함께 Hold, Controlled stop 또는 Safe action으로 연결한다. 비중요 Historian·상태수집·진단경로는 위험분석에 따라 Alarm-only 처리가 가능하다.",
        "correct_rule": "제어기 Task, 필수 통신, 원격 I/O 등 운전·보호에 필요한 Watchdog Timeout은 진단과 함께 Hold, Controlled stop 또는 Safe action으로 연결한다. 비중요 Historian·상태수집·진단경로는 위험분석에 따라 Alarm-only 처리가 가능하다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Watchdog는\\ 상태를\\ 표시만\\ 하며\\ 제어동작과\\ 연결할\\ 필요가\\ 없다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_restart_blind_resume",
        "severity": "fatal",
        "message": "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다.",
        "description": "명시적 반대 주장만 검출한다. Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
        "correct_rule": "Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?전원이나\\ 통신이\\ 복구되면\\ 이전\\ 출력과\\ Sequence\\ Step을\\ 조건\\ 확인\\ 없이\\ 그대로\\ 복원해야\\ 한다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_cause_effect_is_executable_complete",
        "severity": "fatal",
        "message": "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다.",
        "description": "명시적 반대 주장만 검출한다. Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
        "correct_rule": "Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Cause\\ \\&\\ Effect\\ 표만\\ 작성하면\\ 상태전이,\\ Timer,\\ Reset,\\ 우선순위를\\ 포함한\\ 실행논리가\\ 완성된다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_timer_is_feedback",
        "severity": "fatal",
        "message": "밸브 개폐·모터 기동·위치이동처럼 물리적 동작 확인이 필요한 Step도 Timer가 만료되면 실제 설비 Feedback과 관계없이 완료로 판단해도 된다.",
        "description": "명시적 반대 주장만 검출한다. 물리적 동작 확인이 필요한 Step에서 Timer는 최대 허용시간 또는 지연조건일 뿐이며 완료는 필요한 설비 Feedback으로 확인한다. 반면 Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
        "correct_rule": "물리적 동작 확인이 필요한 Step에서 Timer는 최대 허용시간 또는 지연조건일 뿐이며 완료는 필요한 설비 Feedback으로 확인한다. 반면 Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?밸브\\ 개폐·모터\\ 기동·위치이동처럼\\ 물리적\\ 동작\\ 확인이\\ 필요한\\ Step도\\ Timer가\\ 만료되면\\ 실제\\ 설비\\ Feedback과\\ 관계없이\\ 완료로\\ 판단해도\\ 된다\\.\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "밸브 개폐·모터 기동·위치이동처럼 물리적 동작 확인이 필요한 Step도 Timer가 만료되면 실제 설비 Feedback과 관계없이 완료로 판단해도 된다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_override_equals_bypass",
        "severity": "fatal",
        "message": "Override와 Bypass는 완전히 같은 기능이다.",
        "description": "명시적 반대 주장만 검출한다. Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
        "correct_rule": "Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Override와\\ Bypass는\\ 완전히\\ 같은\\ 기능이다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Override와 Bypass는 완전히 같은 기능이다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_shutdown_equals_trip",
        "severity": "fatal",
        "message": "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다.",
        "description": "명시적 반대 주장만 검출한다. 정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
        "correct_rule": "정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?정상\\ Shutdown과\\ Trip은\\ 목적,\\ 우선순위,\\ 동작속도가\\ 모두\\ 같다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_all_interlocks_are_sis",
        "severity": "fatal",
        "message": "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다.",
        "description": "명시적 반대 주장만 검출한다. 운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
        "correct_rule": "운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?모든\\ Interlock은\\ 자동으로\\ SIS이며\\ SIL\\ 등급을\\ 가진다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_manual_disables_protection",
        "severity": "fatal",
        "message": "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다.",
        "description": "명시적 반대 주장만 검출한다. Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
        "correct_rule": "Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?Manual\\ mode에서는\\ 보호\\ Interlock과\\ Trip을\\ 모두\\ 무효화해도\\ 된다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_fatal_bad_signal_is_healthy",
        "severity": "fatal",
        "message": "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다.",
        "description": "명시적 반대 주장만 검출한다. Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
        "correct_rule": "Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
        "recommended_ceiling": 15.0,
        "wrong_patterns": [
          "(?im)^\\s*(?:[-*•]\\s*)?통신단절이나\\ Bad\\ quality\\ 입력은\\ 마지막\\ 값이\\ 남아\\ 있으므로\\ 정상\\ 신호로\\ 간주한다\\s*[.!]?\\s*$"
        ],
        "examples_or_patterns": [
          "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다."
        ],
        "affected_layers": [
          "C",
          "D"
        ]
      }
    ],
    "major_checks": [],
    "question_type_checks": [],
    "next_practice_points": [
      "Permissive·Interlock·Trip을 목적, 성립시점, 출력동작, Latch와 Reset으로 비교표 작성.",
      "State transition 식과 허용 전이표를 이용해 정상·실패·복구 경로를 함께 작성.",
      "2oo3 Voting, First-out, Bad quality와 Bypass 시나리오를 Cause & Effect에 연결.",
      "Watchdog Timeout과 통신복구 시 Hold·Controlled stop·재기동 조건을 설계.",
      "Cold/Warm restart 시 실제 설비상태와 메모리 상태를 일치시키는 절차 작성."
    ],
    "de_claim_trust": {
      "formula_claims": "논리식은 변수 정의와 우선순위, Latch·Reset 조건 및 실제 피드백 위치가 일치할 때 신뢰한다.",
      "field_claims": "Fail-safe, Bypass, Auto restart 주장은 공정 위험, 권한, 표시, 제한조건과 복구검증이 함께 있을 때 신뢰한다."
    }
  },
  "llm_profile": {
    "display_name": "SW-02 운전 제어논리와 상태전이 평가",
    "difficulty": "DESIGN_EVALUATION",
    "enabled": true,
    "cap_policy": {
      "fatal_default_ceiling": 15.0,
      "major_default_ceiling": 19.0,
      "fatal_requires_explicit_contradiction": true,
      "omission_is_not_fatal": true
    },
    "candidate_extraction": {
      "topic_terms": [
        "제어논리 Sequence Interlock Permissive Trip",
        "시퀀스 상태전이 인터록 퍼미시브 트립",
        "Sequence control state transition interlock permissive trip",
        "운전 제어논리와 상태전이",
        "Interlock Permissive Trip 차이",
        "인터록 퍼미시브 트립 차이",
        "Cause & Effect Voting First-out",
        "원인 결과표 Voting First-out",
        "Bypass Override 제어논리",
        "바이패스 오버라이드 명령 우선순위",
        "Fail-safe Watchdog Restart Recovery",
        "Fail safe watchdog 재기동 복구논리",
        "Sequence abnormal transition prevention",
        "시퀀스 이상전이 방지",
        "Trip latch reset logic",
        "트립 래치 리셋 조건",
        "Manual Auto Local Remote command arbitration",
        "수동 자동 로컬 리모트 명령 중재",
        "PLC sequence feedback timeout one-shot latch",
        "상태전이표 mutual exclusion illegal state recovery"
      ],
      "key_terms": [
        "sequence control",
        "step",
        "state",
        "state transition",
        "transition guard",
        "entry action",
        "exit action",
        "permissive",
        "interlock",
        "trip",
        "shutdown",
        "cause and effect",
        "cause & effect",
        "voting",
        "m-out-of-n",
        "2oo3",
        "first-out",
        "bypass",
        "override",
        "fail-safe",
        "safe state",
        "watchdog",
        "heartbeat",
        "timeout",
        "restart",
        "recovery",
        "state reconciliation",
        "abnormal transition",
        "mutual exclusion",
        "one-hot",
        "illegal state",
        "command arbitration",
        "manual auto",
        "local remote",
        "feedback confirmation",
        "trip latch",
        "reset condition",
        "bad quality",
        "stale data",
        "degraded mode",
        "debounce",
        "hysteresis",
        "one-shot",
        "scan"
      ],
      "required_context_groups": [
        [
          "sequence",
          "시퀀스",
          "state transition",
          "상태전이"
        ],
        [
          "interlock",
          "인터록",
          "permissive",
          "퍼미시브",
          "trip",
          "트립"
        ],
        [
          "fail-safe",
          "watchdog",
          "restart",
          "recovery",
          "bypass",
          "override"
        ]
      ],
      "exclude_if_only": [
        "HMI 화면 구성",
        "Alarm priority",
        "Alarm shelving",
        "SOE display",
        "SIL calculation",
        "PFDavg",
        "PFH",
        "Safety lifecycle",
        "Safety V&V"
      ],
      "minimum_distinct_groups": 2
    },
    "truth_schema": [
      {
        "id": "sw02_scope_operational_logic",
        "correct_rule": "SW-02는 운전 제어논리의 동작 메커니즘을 다루며 Sequence, 상태전이, Interlock, Permissive, Trip, Shutdown, Cause & Effect, Voting, First-out, Bypass, Override, Fail-safe, Watchdog 및 Restart·Recovery를 하나의 운전 논리 체계로 연결한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_sequence_definition",
        "correct_rule": "Sequence control은 공정을 여러 Step 또는 State로 나누고, 각 단계의 진입조건·실행동작·완료조건·시간제한·실패처리를 정의하여 정해진 순서로 운전하는 제어방식이다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_state_transition_model",
        "correct_rule": "상태전이는 현재 상태와 명령, Permissive, Interlock, Trip, 설비 피드백 및 시간조건을 입력으로 다음 상태를 결정하는 함수로 표현할 수 있으며, 동일 입력에서 결정론적 결과가 나와야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_transition_guard",
        "correct_rule": "Transition guard는 상태변화를 허용하는 논리조건이다. 기동·명령 기반 전이의 대표식은 Command AND 모든 필수 Permissive AND 필요한 선행 Feedback AND NOT Trip AND NOT Inhibit로 나타낼 수 있다. 자동 진행, 시간 유지 완료 또는 공정조건 도달 전이는 Command 없이 성립할 수 있으며, Feedback은 전이의 선행조건 또는 동작 완료 확인조건으로 구분한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_state_entry_exit_actions",
        "correct_rule": "각 State에는 Entry action, 지속 동작, Exit action을 구분하여 정의해야 하며, 출력은 상태와 전이 이벤트의 소유관계를 명확히 하여 중복 명령과 잔류 출력을 방지한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_permissive_definition",
        "correct_rule": "Permissive는 기동 또는 특정 전이를 시작하기 전에 만족해야 하는 사전 허가조건이며, 보통 모든 필수 조건의 AND 논리로 구성한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_interlock_definition",
        "correct_rule": "Interlock은 위험하거나 비정상적인 조합을 방지하기 위해 동작을 금지하거나 운전 중 특정 출력을 강제하는 제약논리이며, 단순 Alarm 표시와 구분된다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_trip_definition",
        "correct_rule": "Trip은 보호조건이 성립할 때 정상 Sequence보다 우선하여 설비 또는 공정을 미리 정한 정지상태로 이행시키는 강제 보호동작이며, 위험도와 공정특성에 따라 Latch와 수동 Reset을 적용한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_shutdown_classes",
        "correct_rule": "Shutdown은 정상정지, 공정정지, 비상정지 등 목적과 속도에 따라 구분하며, 정상정지는 순차적 감속·배출·정리 절차를 따를 수 있지만 Trip은 보호목적의 우선 동작으로 설계한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_cause_effect",
        "correct_rule": "Cause & Effect는 원인신호와 요구되는 결과동작을 행렬 또는 표로 연결하여 Interlock·Trip·Alarm·Shutdown의 설계 의도를 명확히 하지만, 세부 상태전이·타이머·Reset·우선순위까지 포함한 실행논리 자체를 자동으로 대체하지는 않는다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_voting_logic",
        "correct_rule": "Voting logic은 N개 입력 중 M개 이상이 Trip 조건일 때 동작하는 M-out-of-N 구조이며, 채널 독립성·공통원인·진단·불일치 처리와 함께 설계해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_first_out",
        "correct_rule": "First-out은 연쇄 Trip에서 가장 먼저 발생한 유효 원인을 시간순으로 고정하여 후속 결과신호와 구분하는 기능이며, 원인진단과 복구 판단에 사용한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_bypass",
        "correct_rule": "Bypass는 특정 입력 또는 보호경로를 제한된 조건과 기간 동안 우회하는 관리된 기능이며, 승인·표시·시간제한·대체조치·복구확인을 포함해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_override",
        "correct_rule": "Override는 정상 명령 또는 자동출력보다 우선하는 강제 명령으로, Bypass와 목적이 다르며 권한·우선순위·범위·해제조건을 명확히 해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_fail_safe",
        "correct_rule": "Fail-safe는 전원·공기·통신·제어기 또는 신호 고장 시 위험을 최소화하는 사전 정의 상태와 동작을 말하며, 항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라 공정 위험분석과 최종요소 특성에 따라 정한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_watchdog",
        "correct_rule": "Watchdog는 제어기 Task, 통신, 원격 I/O 또는 장치의 정상 갱신을 감시하고 정해진 시간 내 Heartbeat가 없으면 진단상태를 만들고 사전 정의된 Hold, Controlled stop 또는 Safe action으로 전환한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_feedback_confirmation_timeout",
        "correct_rule": "Sequence는 명령 출력만으로 단계완료를 판단하지 않고 위치·압력·속도·접점 등 독립적인 설비 피드백과 Timeout을 사용하여 성공, 지연, 고착, 센서불일치를 구분한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_trip_latch_reset",
        "correct_rule": "Trip Latch는 원인이 순간적으로 사라져도 보호상태를 유지하며, Reset은 원인 제거, 안전조건 재확인, 조작권한 및 Reset edge가 모두 유효할 때만 허용해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_abnormal_transition_prevention",
        "correct_rule": "비정상 전이 방지는 허용 전이표, Mutual exclusion, One-hot state, 전이 중 재명령 차단, Timeout, Debounce, 입력 품질검사 및 Illegal-state recovery를 조합하여 구현한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_command_arbitration",
        "correct_rule": "Local·Remote, Manual·Auto, Sequence·Operator, Normal·Trip 명령이 경쟁할 때는 명시적인 명령 우선순위와 단일 출력 소유자를 정하고, 보호동작은 정상 운전명령보다 우선하도록 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_signal_quality",
        "correct_rule": "Bad quality, stale data, 통신단절 또는 비현실값을 정상 신호로 간주해서는 안 되며, 입력별 대체값·Hold·Trip·Degraded mode 정책을 명시해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_restart_recovery",
        "correct_rule": "Restart와 Recovery는 Cold start, Warm restart, 통신복구 및 부분정전 시나리오를 구분하고, 실제 설비상태를 재수집한 뒤 State reconciliation, Permissive 재확인, Latch 보존 및 운영자 승인 여부에 따라 재개한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_degraded_mode",
        "correct_rule": "Degraded mode는 일부 기능 또는 신호가 상실된 상태에서 허용되는 제한운전 범위와 금지동작, 감시강화, 종료조건을 정의한 운전상태이며 무조건적인 계속운전을 의미하지 않는다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_scan_edge_memory",
        "correct_rule": "PLC/DCS의 Scan 기반 논리는 Level 신호와 Edge 이벤트, One-shot, Memory/Latch를 구분해야 하며, 한 Scan 내 Set·Reset 순서와 출력 갱신순서가 의도한 우선순위를 보장해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_debounce_hysteresis",
        "correct_rule": "접점 Chattering과 임계값 진동은 Debounce, On-delay·Off-delay, Hysteresis 및 지속시간 조건으로 억제하되, 보호응답 지연과 놓침 위험을 함께 검토해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_manual_mode_boundary",
        "correct_rule": "Manual mode는 정상 자동 Sequence를 우회할 수 있지만 필수 보호 Interlock과 Trip까지 자동으로 무효화하는 모드가 아니며, 수동조작 가능 범위와 금지조건을 별도로 정의해야 한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_sw03_boundary",
        "correct_rule": "SW-03은 HMI·SCADA 화면, Alarm 우선순위·Deadband·Delay·Shelving·Suppression, Setpoint list, SOE 표시, Audit trail 및 Operator authority를 소유하고, SW-02는 그 정보가 발생하는 실제 Interlock·Trip·Sequence 상태전이 논리를 소유한다.",
        "fatal_if_opposite": false
      },
      {
        "id": "sw02_sw05_boundary",
        "correct_rule": "SW-05는 SIL 산정, 안전수명주기, 체계적 고장 통제, 독립성 및 Safety V&V를 소유하고, SW-02는 SIL 등급 산정이 아닌 운전논리의 상태전이와 보호동작 메커니즘만 소유한다.",
        "fatal_if_opposite": false
      }
    ],
    "fatal_conditions": [
      {
        "id": "sw02_fatal_permissive_equals_trip",
        "wrong_claim": "Permissive와 Trip은 같은 논리이다.",
        "correct_rule": "Permissive는 기동·전이 전의 허가조건이고 Trip은 운전 중 보호조건에 의한 강제정지 동작이다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_interlock_alarm_only",
        "wrong_claim": "Interlock은 Alarm만 발생시키며 동작을 차단하거나 강제하지 않는다.",
        "correct_rule": "Interlock은 금지 또는 강제동작을 수행하는 제약논리이며 Alarm 표시는 별도 운전정보 기능이다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_trip_unconditional_auto_reset",
        "wrong_claim": "Trip 원인이 사라지면 즉시 자동 Reset하여 운전을 재개해야 한다.",
        "correct_rule": "Latch 적용 Trip은 원인 제거와 안전조건·권한 확인 후 Reset해야 하며 자동복귀 여부는 위험도와 설계에 따라 제한한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_bypass_unmanaged",
        "wrong_claim": "Bypass는 점검 편의를 위해 승인이나 시간제한 없이 계속 유지해도 된다.",
        "correct_rule": "Bypass는 승인, 표시, 제한시간, 대체조치와 복구확인이 필요한 관리 기능이다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D",
          "E"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_fail_safe_always_close",
        "wrong_claim": "Fail-safe는 모든 설비를 무조건 Fail-close 또는 De-energize로 만드는 것이다.",
        "correct_rule": "안전상태는 공정 위험과 최종요소 기능에 따라 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 정한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_voting_always_safer",
        "wrong_claim": "Voting 채널 수를 늘리면 독립성이나 공통원인과 관계없이 항상 더 안전해진다.",
        "correct_rule": "Voting 성능은 M-out-of-N 구조, 채널 독립성, 공통원인, 진단과 불일치 처리에 좌우된다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_first_out_last_cause",
        "wrong_claim": "First-out은 마지막에 남은 Trip 신호 또는 가장 우선순위가 높은 Alarm을 기록한다.",
        "correct_rule": "First-out은 연쇄 결과 이전에 최초로 발생한 유효 원인을 시간순으로 고정한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_watchdog_monitor_only",
        "wrong_claim": "Watchdog는 상태를 표시만 하며 제어동작과 연결할 필요가 없다.",
        "correct_rule": "제어기 Task, 필수 통신, 원격 I/O 등 운전·보호에 필요한 Watchdog Timeout은 진단과 함께 Hold, Controlled stop 또는 Safe action으로 연결한다. 비중요 Historian·상태수집·진단경로는 위험분석에 따라 Alarm-only 처리가 가능하다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_restart_blind_resume",
        "wrong_claim": "전원이나 통신이 복구되면 이전 출력과 Sequence Step을 조건 확인 없이 그대로 복원해야 한다.",
        "correct_rule": "Restart는 실제 설비상태 재수집, 상태 일치화, Permissive 확인, Latch 보존과 승인 조건을 거쳐야 한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_cause_effect_is_executable_complete",
        "wrong_claim": "Cause & Effect 표만 작성하면 상태전이, Timer, Reset, 우선순위를 포함한 실행논리가 완성된다.",
        "correct_rule": "Cause & Effect는 설계 의도를 표현하지만 상세 Sequence와 상태전이 사양 및 실행논리 검증이 별도로 필요하다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_timer_is_feedback",
        "wrong_claim": "밸브 개폐·모터 기동·위치이동처럼 물리적 동작 확인이 필요한 Step도 Timer가 만료되면 실제 설비 Feedback과 관계없이 완료로 판단해도 된다.",
        "correct_rule": "물리적 동작 확인이 필요한 Step에서 Timer는 최대 허용시간 또는 지연조건일 뿐이며 완료는 필요한 설비 Feedback으로 확인한다. 반면 Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_override_equals_bypass",
        "wrong_claim": "Override와 Bypass는 완전히 같은 기능이다.",
        "correct_rule": "Override는 명령 우선 강제이고 Bypass는 입력 또는 보호경로 우회이므로 목적과 통제가 다르다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_shutdown_equals_trip",
        "wrong_claim": "정상 Shutdown과 Trip은 목적, 우선순위, 동작속도가 모두 같다.",
        "correct_rule": "정상정지는 순차 운전절차이고 Trip은 보호목적의 우선 강제동작으로 구분한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_all_interlocks_are_sis",
        "wrong_claim": "모든 Interlock은 자동으로 SIS이며 SIL 등급을 가진다.",
        "correct_rule": "운전 Interlock과 안전기능은 구분해야 하며 SIL·안전수명주기 판단은 SW-05 범위의 별도 분석이 필요하다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_manual_disables_protection",
        "wrong_claim": "Manual mode에서는 보호 Interlock과 Trip을 모두 무효화해도 된다.",
        "correct_rule": "Manual mode에서도 필수 보호논리는 유지하고 허용 가능한 수동조작 범위를 제한해야 한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      },
      {
        "id": "sw02_fatal_bad_signal_is_healthy",
        "wrong_claim": "통신단절이나 Bad quality 입력은 마지막 값이 남아 있으므로 정상 신호로 간주한다.",
        "correct_rule": "Bad quality와 stale data는 별도 상태로 처리하고 Hold, 대체값, Degraded mode 또는 Trip 정책을 적용한다.",
        "severity": "fatal",
        "affected_layers": [
          "C",
          "D"
        ],
        "recommended_ceiling": 15.0
      }
    ],
    "safe_conditions": [
      "Permissive는 기동 또는 전이를 허가하는 사전조건이고 Trip은 보호조건 성립 시 강제정지를 요구하는 동작이다.",
      "Interlock은 운전 중 위험한 조합을 금지하거나 출력을 강제할 수 있으며 Alarm은 운전자 정보 제공 기능이다.",
      "Trip의 Latch와 Reset 방식은 위험도와 공정 요구에 따라 정하되 원인 제거와 안전조건 확인이 우선이다.",
      "Fail-safe 상태는 설비마다 Fail-close, Fail-open, Hold 또는 Controlled stop 등으로 다를 수 있다.",
      "De-energize-to-trip은 흔한 구현 원칙이지만 모든 설비의 유일한 안전상태는 아니다.",
      "Voting은 채널 독립성, 공통원인, 진단과 불일치 처리까지 함께 검토해야 한다.",
      "First-out은 연쇄 Trip에서 최초 원인을 보존한다.",
      "Bypass는 유지보수에 필요할 수 있으나 승인, 표시, 제한시간과 복구확인이 필요하다.",
      "Override는 강제 명령이고 Bypass는 보호경로 우회이므로 목적과 권한을 구분한다.",
      "Watchdog Timeout 시 Hold 또는 안전동작은 공정 위험과 복구전략에 따라 선택한다.",
      "Restart 후 자동재개가 가능한 비위험 설비도 있으나 상태 일치와 Permissive 검증이 선행되어야 한다.",
      "Purge 유지시간·안정화 대기·혼합시간처럼 시간 자체가 요구조건인 Step은 Timer 완료를 정상 완료조건으로 사용할 수 있다.",
      "Manual mode에서도 필수 보호논리는 유지해야 한다.",
      "Cause & Effect는 논리 설계의 기준문서이며 상세 상태전이와 구현검증이 추가로 필요하다.",
      "운전 Interlock이 모두 SIS인 것은 아니며 SIL 산정은 별도 안전수명주기 범위이다.",
      "Alarm Deadband, Shelving, SOE 표시와 Operator authority는 SW-03의 주 소유범위이다.",
      "SW-02는 SOE에 표시될 이벤트의 실제 발생논리와 First-out 메커니즘을 다루되 화면·Alarm 관리정책은 SW-03에 넘긴다.",
      "SIL 산정, 체계적 고장, 독립성 및 Safety V&V는 SW-05로 넘긴다.",
      "비중요 Historian·상태수집·진단경로의 Watchdog는 위험분석에 따라 Alarm-only로 처리할 수 있다."
    ],
    "major_checks": [
      {
        "id": "sw02_major_terms_without_relationship",
        "severity": "major",
        "message": "Sequence·Permissive·Interlock·Trip 용어를 나열했으나 사전허가, 운전제약, 보호정지의 관계가 부족하다.",
        "description": "문항이 세 논리의 차이를 요구할 때 목적·동작시점·우선순위를 연결해야 한다.",
        "correct_rule": "Permissive=전이 전 허가, Interlock=금지·강제 제약, Trip=보호 우선 정지로 비교한다.",
        "condition": "문항이 Interlock·Permissive·Trip 비교를 요구하고 관계 설명이 부족한 경우",
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_major_no_transition_failure_path",
        "severity": "major",
        "message": "정상 Sequence만 설명하고 Timeout, 실패처리 또는 Illegal-state recovery가 없다.",
        "description": "상태전이는 정상 경로와 실패·복구 경로를 함께 정의해야 한다.",
        "correct_rule": "완료 피드백, Timeout, 실패상태와 복구조건을 포함한다.",
        "condition": "문항이 Sequence 설계를 요구하는 경우",
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_major_no_latch_reset",
        "severity": "major",
        "message": "Trip 동작은 설명했으나 Latch와 Reset 유효조건이 부족하다.",
        "description": "순간 원인 소멸에 따른 재기동을 방지하는 복구논리가 필요하다.",
        "correct_rule": "원인 제거, 안전조건, 권한, Reset edge를 제시한다.",
        "condition": "Trip 또는 Shutdown 설계 문항인 경우",
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_major_no_bypass_governance",
        "severity": "major",
        "message": "Bypass 또는 Override를 언급했으나 승인·표시·기간·대체조치·해제조건이 부족하다.",
        "description": "우회와 강제명령은 운전 리스크를 증가시키므로 관리통제가 필요하다.",
        "correct_rule": "권한, 상태표시, 시간제한, 대체조치, 해제와 복구확인을 제시한다.",
        "condition": "Bypass 또는 Override 문항인 경우",
        "affected_layers": [
          "C",
          "D",
          "E"
        ]
      },
      {
        "id": "sw02_major_no_restart_reconciliation",
        "severity": "major",
        "message": "Restart를 언급했으나 실제 설비상태 재수집과 State reconciliation이 부족하다.",
        "description": "메모리 상태와 현장 상태 불일치가 이상동작을 유발할 수 있다.",
        "correct_rule": "Cold/Warm restart를 구분하고 상태 재수집, Permissive, Latch와 승인조건을 확인한다.",
        "condition": "Restart 또는 Recovery 문항인 경우",
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_major_no_signal_quality_policy",
        "severity": "major",
        "message": "Watchdog 또는 통신고장을 언급했으나 Bad quality와 stale data 처리정책이 부족하다.",
        "description": "마지막 값 유지와 정상신호는 구분되어야 한다.",
        "correct_rule": "Hold, 대체값, Degraded mode, Controlled stop 또는 Trip 정책을 정의한다.",
        "condition": "Watchdog·통신·신호고장 문항인 경우",
        "affected_layers": [
          "C",
          "D"
        ]
      },
      {
        "id": "sw02_major_sw03_scope_drift",
        "severity": "warn",
        "message": "실제 제어논리보다 HMI 화면, Alarm 철학, Shelving 또는 SOE 표시 운영에 답안이 치우쳤다.",
        "description": "운전정보 관리는 SW-03이 주 소유한다.",
        "correct_rule": "SW-02에서는 Alarm이 발생하는 실제 상태전이·Interlock·Trip 논리를 중심으로 쓴다.",
        "condition": "질문의 핵심이 운전 제어논리인 경우",
        "affected_layers": [
          "C"
        ]
      },
      {
        "id": "sw02_major_sw05_scope_drift",
        "severity": "warn",
        "message": "상태전이 메커니즘보다 SIL 산정, 안전수명주기 또는 Safety V&V에 답안이 치우쳤다.",
        "description": "해당 항목은 SW-05가 주 소유한다.",
        "correct_rule": "SW-02에서는 운전논리 동작과 Fail-safe·Trip 메커니즘만 다룬다.",
        "condition": "질문의 핵심이 일반 운전 제어논리인 경우",
        "affected_layers": [
          "C"
        ]
      }
    ],
    "feedback_templates": {
      "fatal": "핵심 제어논리의 의미가 반대로 서술되었습니다: {message}",
      "major": "설계조건 또는 복구경로가 부족합니다: {message}",
      "warn": "문항 소유범위 또는 보조조건이 부족합니다: {message}"
    },
    "next_practice_points": [
      "전이조건 E=Command∧Permissive_all∧Feedback_ok∧¬Trip∧¬Inhibit를 변수 정의와 함께 제시한다.",
      "Trip latch의 Set-dominant 식과 Reset_valid 조건을 제시한다.",
      "Voting의 M-out-of-N 식과 First-out 시간선정을 구분한다.",
      "Restart 상태 일치화와 이상전이 방지표를 하나의 사례로 연습한다."
    ],
    "false_positive_cautions": [
      "Trip 또는 Interlock 단어가 있다는 이유만으로 SW-02를 적용하지 말고 Sequence·상태전이·보호동작 맥락의 공존을 확인한다.",
      "Alarm 값, Deadband, Delay, Shelving, Suppression, HMI hierarchy, SOE 표시와 Operator authority가 핵심이면 SW-03으로 넘긴다.",
      "SIL 산정, PFDavg, PFH, 안전수명주기, 독립성, 체계적 고장, Safety V&V가 핵심이면 SW-05로 넘긴다.",
      "Fail-safe가 Fail-close 사례로 설명되더라도 모든 설비에 대한 절대 주장인지 문맥을 확인한다.",
      "비위험 보조설비의 조건부 Auto reset 또는 Auto restart 사례는 위험분석과 상태검증 조건을 명시하면 fatal로 보지 않는다.",
      "Bypass를 유지보수 절차로 언급한 것 자체는 오류가 아니며 승인·표시·제한·복구 통제가 있는지 평가한다.",
      "Cause & Effect를 핵심 설계문서라고 한 표현은 안전하며 실행논리를 완전히 대체한다고 단정할 때만 오류다.",
      "Voting을 신뢰도 향상 수단으로 설명한 것 자체는 안전하며 독립성·공통원인을 무시한 절대 주장을 구분한다.",
      "First-out과 SOE를 함께 설명할 수 있으나 최초 원인 선정 메커니즘은 SW-02, 표시·기록 운영은 SW-03 소유다.",
      "Manual mode에서 일부 자동 Sequence를 우회하는 것은 가능하지만 보호 Interlock과 Trip까지 전부 무효화한다고 단정할 때만 fatal이다.",
      "Purge 유지시간, 안정화 대기, 혼합시간처럼 시간 자체가 공정 요구조건인 Step은 Timer 완료를 정상 완료조건으로 인정한다.",
      "비중요 Historian·상태수집·진단경로의 Watchdog는 위험분석상 제어동작이 필요 없으면 Alarm-only로 처리할 수 있다."
    ],
    "output_contract": {
      "required_fields": [
        "id",
        "severity",
        "message",
        "correct_rule",
        "affected_layers"
      ],
      "allowed_severity": [
        "fatal",
        "major",
        "warn",
        "info"
      ],
      "fatal_requires_direct_opposite_claim": true,
      "cite_answer_evidence": true
    }
  },
  "revision_notes": [
    "2026-08-06: 16개 명시적 fatal 오개념과 문항별 major/warn 기준을 작성했다.",
    "결정론적 fatal은 직접적인 반대 주장만 검출하도록 복합 정규식을 사용했다.",
    "SW-03 및 SW-05 범위 이동은 false positive caution과 warn으로 처리한다.",
    "2026-08-07 LLM 의미 감사 수리: Timer·Watchdog 조건부 정상표현과 Transition guard 범위를 명확히 했다."
  ],
  "topic_label": "SW-02 제어논리·Sequence·Interlock·Trip"
}
EOF_SW02_LOGIC_CHECK_5B37
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/logic_check.json"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json" <<'EOF_SW02_MODEL_ANSWER_3A68'
{
  "schema_version": "topic_pack.model_answer.v1",
  "topic_id": "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
  "title_ko": "제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe",
  "question_type": "PRINCIPLE_INTERPRETATION",
  "expected_question_patterns": [
    {
      "pattern": "Sequence control의 상태전이, 단계완료 조건 및 비정상 전이 방지방법을 설명하시오.",
      "intent": "Sequence와 상태전이 설계",
      "required_anchor_ids": [
        "sw02_sequence_definition",
        "sw02_state_transition_model",
        "sw02_transition_guard",
        "sw02_feedback_confirmation_timeout",
        "sw02_abnormal_transition_prevention"
      ]
    },
    {
      "pattern": "Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.",
      "intent": "세 논리의 목적과 동작 차이",
      "required_anchor_ids": [
        "sw02_permissive_definition",
        "sw02_interlock_definition",
        "sw02_trip_definition",
        "sw02_trip_latch_reset"
      ]
    },
    {
      "pattern": "공정 Shutdown 논리와 Cause & Effect 작성 시 고려사항을 설명하시오.",
      "intent": "정상정지와 보호정지 및 원인-결과 문서",
      "required_anchor_ids": [
        "sw02_shutdown_classes",
        "sw02_cause_effect",
        "sw02_command_arbitration"
      ]
    },
    {
      "pattern": "2oo3 Voting과 First-out 논리의 원리 및 설계 유의사항을 설명하시오.",
      "intent": "다중 입력 판정과 최초 원인 보존",
      "required_anchor_ids": [
        "sw02_voting_logic",
        "sw02_first_out",
        "sw02_signal_quality"
      ]
    },
    {
      "pattern": "Bypass와 Override의 차이, 위험요인 및 관리방안을 설명하시오.",
      "intent": "우회와 강제명령의 구분",
      "required_anchor_ids": [
        "sw02_bypass",
        "sw02_override",
        "sw02_command_arbitration"
      ]
    },
    {
      "pattern": "Fail-safe와 Watchdog의 개념을 설명하고 고장 시 제어논리를 제시하시오.",
      "intent": "고장 검출과 안전상태 전환",
      "required_anchor_ids": [
        "sw02_fail_safe",
        "sw02_watchdog",
        "sw02_signal_quality",
        "sw02_degraded_mode"
      ]
    },
    {
      "pattern": "제어시스템 Restart 및 Recovery 논리의 설계기준을 설명하시오.",
      "intent": "재기동과 상태 일치화",
      "required_anchor_ids": [
        "sw02_restart_recovery",
        "sw02_trip_latch_reset",
        "sw02_signal_quality",
        "sw02_command_arbitration"
      ]
    },
    {
      "pattern": "PLC Sequence에서 Timer, Feedback, Edge 및 Latch 적용 시 주의사항을 설명하시오.",
      "intent": "Scan 기반 구현 상세",
      "required_anchor_ids": [
        "sw02_feedback_confirmation_timeout",
        "sw02_scan_edge_memory",
        "sw02_debounce_hysteresis",
        "sw02_trip_latch_reset"
      ]
    },
    {
      "pattern": "Manual·Auto, Local·Remote 운전모드의 명령 우선순위와 보호논리를 설명하시오.",
      "intent": "모드와 명령 중재",
      "required_anchor_ids": [
        "sw02_command_arbitration",
        "sw02_manual_mode_boundary",
        "sw02_interlock_definition",
        "sw02_trip_definition"
      ]
    },
    {
      "pattern": "제어논리에서 상태전이표를 이용한 이상전이 방지 및 복구방안을 설명하시오.",
      "intent": "Illegal state 방지와 복구",
      "required_anchor_ids": [
        "sw02_state_transition_model",
        "sw02_abnormal_transition_prevention",
        "sw02_restart_recovery",
        "sw02_degraded_mode"
      ]
    }
  ],
  "recommended_outline": [
    {
      "section": "1. 배경과 제어논리 계층",
      "intent": "운전요구를 Sequence, 상태전이, 제약논리와 보호동작으로 구조화하고 SW-02의 소유범위를 제시한다.",
      "anchor_refs": [
        "sw02_scope_operational_logic",
        "sw02_sw03_boundary",
        "sw02_sw05_boundary"
      ]
    },
    {
      "section": "2. Sequence와 상태전이 모델",
      "intent": "Step·State, Entry/Exit action, 전이조건과 결정론적 다음 상태를 설명한다.",
      "anchor_refs": [
        "sw02_sequence_definition",
        "sw02_state_transition_model",
        "sw02_transition_guard",
        "sw02_state_entry_exit_actions"
      ]
    },
    {
      "section": "3. Permissive·Interlock·Trip·Shutdown",
      "intent": "기동 허가, 운전 제약, 보호정지와 정상정지의 목적·우선순위·Reset 차이를 비교한다.",
      "anchor_refs": [
        "sw02_permissive_definition",
        "sw02_interlock_definition",
        "sw02_trip_definition",
        "sw02_shutdown_classes",
        "sw02_trip_latch_reset"
      ]
    },
    {
      "section": "4. Cause & Effect·Voting·First-out",
      "intent": "원인-결과 설계문서, M-out-of-N 판정과 최초 원인 보존 메커니즘을 연결한다.",
      "anchor_refs": [
        "sw02_cause_effect",
        "sw02_voting_logic",
        "sw02_first_out"
      ]
    },
    {
      "section": "5. Bypass·Override·명령 우선순위",
      "intent": "우회와 강제명령을 구분하고 Local/Remote, Manual/Auto 및 Trip 우선순위를 제시한다.",
      "anchor_refs": [
        "sw02_bypass",
        "sw02_override",
        "sw02_command_arbitration",
        "sw02_manual_mode_boundary"
      ]
    },
    {
      "section": "6. Fail-safe·Watchdog·신호품질",
      "intent": "고장 검출, 안전상태, Bad quality와 제한운전 정책을 설명한다.",
      "anchor_refs": [
        "sw02_fail_safe",
        "sw02_watchdog",
        "sw02_signal_quality",
        "sw02_degraded_mode"
      ]
    },
    {
      "section": "7. 이상전이 방지와 구현 상세",
      "intent": "피드백 확인, Timeout, 전이표, Mutual exclusion, Scan·Edge·Latch와 Debounce를 설명한다.",
      "anchor_refs": [
        "sw02_feedback_confirmation_timeout",
        "sw02_abnormal_transition_prevention",
        "sw02_scan_edge_memory",
        "sw02_debounce_hysteresis"
      ]
    },
    {
      "section": "8. Restart·Recovery와 현장 적용 결론",
      "intent": "상태 일치화, Latch 보존, 재기동 승인과 시험 시나리오를 통해 안전하고 복구 가능한 논리설계를 정리한다.",
      "anchor_refs": [
        "sw02_restart_recovery",
        "sw02_trip_latch_reset",
        "sw02_signal_quality",
        "sw02_command_arbitration"
      ]
    }
  ],
  "high_score_points": [
    "Sequence를 Step 나열이 아니라 State, 진입조건, 동작, 완료조건, Timeout과 실패처리로 구조화한다.",
    "Permissive, Interlock, Trip을 사전 허가·운전 제약·보호 강제정지로 구분한다.",
    "정상 Shutdown과 Trip의 목적, 우선순위와 동작속도 차이를 설명한다.",
    "상태전이식을 제시하고 Command, Permissive, Feedback, Trip과 Inhibit의 논리관계를 설명한다.",
    "Trip Latch와 Reset valid 조건을 원인 제거, 안전조건, 권한과 Reset edge로 제시한다.",
    "Cause & Effect가 설계 의도 문서이며 상세 실행논리를 완전히 대체하지 않는다고 설명한다.",
    "Voting을 M-out-of-N 식과 채널 독립성·공통원인·진단·불일치 처리로 연결한다.",
    "First-out을 최초 유효 원인 보존과 연쇄 결과 구분으로 설명한다.",
    "Bypass와 Override의 목적을 구분하고 승인, 시간제한, 표시, 대체조치와 해제를 제시한다.",
    "Fail-safe를 공정별 Safe state로 정의하고 Fail-close 절대론을 피한다.",
    "Watchdog와 Bad quality를 Hold, Controlled stop, Trip 또는 Degraded mode 정책으로 연결한다.",
    "명령 출력과 실제 설비 피드백을 구분하고 Timeout과 고착·불일치 진단을 포함한다.",
    "허용 전이표, Mutual exclusion, One-hot, Edge, Latch, Debounce로 이상전이를 방지한다.",
    "Restart 시 실제 상태 재수집, State reconciliation, Permissive 재확인과 Latch 보존을 설명한다.",
    "SW-03과 SW-05의 소유범위를 명확히 구분하여 Alarm 관리나 SIL 산정으로 범위를 확장하지 않는다.",
    "비용과 구현 난이도뿐 아니라 운전성, 유지보수, 기존 설비 I/O와 시험 가능성을 고려한다."
  ],
  "common_missing_points": [
    "Sequence를 단순 순서도나 Timer 나열로만 설명하고 상태·완료조건·실패처리를 누락함.",
    "Permissive, Interlock, Trip을 같은 의미로 사용함.",
    "Trip의 Latch와 Reset 조건을 설명하지 않음.",
    "정상 Shutdown과 보호 Trip의 차이를 누락함.",
    "Cause & Effect를 실행 프로그램과 동일시함.",
    "Voting 숫자만 제시하고 채널 독립성·공통원인·불일치 처리를 누락함.",
    "First-out을 Alarm 우선순위 또는 마지막 잔류신호와 혼동함.",
    "Bypass와 Override의 승인, 표시, 시간제한과 복구확인을 누락함.",
    "Fail-safe를 모든 밸브 Fail-close로 일반화함.",
    "Watchdog를 단순 상태감시로만 설명하고 Timeout 후 동작을 누락함.",
    "Restart 시 이전 Step과 출력을 그대로 복원한다고 설명함.",
    "Manual mode에서 보호논리 유지와 명령 우선순위를 누락함.",
    "Bad quality와 stale data 처리정책을 누락함.",
    "SW-03의 Alarm·SOE 운영정보와 SW-05의 SIL·Safety V&V를 본 Topic의 핵심으로 확장함."
  ],
  "routing_aliases": [
    "제어논리 Sequence Interlock Permissive Trip",
    "시퀀스 상태전이 인터록 퍼미시브 트립",
    "Sequence control state transition interlock permissive trip",
    "운전 제어논리와 상태전이",
    "Interlock Permissive Trip 차이",
    "인터록 퍼미시브 트립 차이",
    "Cause & Effect Voting First-out",
    "원인 결과표 Voting First-out",
    "Bypass Override 제어논리",
    "바이패스 오버라이드 명령 우선순위",
    "Fail-safe Watchdog Restart Recovery",
    "Fail safe watchdog 재기동 복구논리",
    "Sequence abnormal transition prevention",
    "시퀀스 이상전이 방지",
    "Trip latch reset logic",
    "트립 래치 리셋 조건",
    "Manual Auto Local Remote command arbitration",
    "수동 자동 로컬 리모트 명령 중재",
    "PLC sequence feedback timeout one-shot latch",
    "상태전이표 mutual exclusion illegal state recovery"
  ],
  "routing_field_points": [
    "sequence control",
    "step",
    "state",
    "state transition",
    "transition guard",
    "entry action",
    "exit action",
    "permissive",
    "interlock",
    "trip",
    "shutdown",
    "cause and effect",
    "cause & effect",
    "voting",
    "m-out-of-n",
    "2oo3",
    "first-out",
    "bypass",
    "override",
    "fail-safe",
    "safe state",
    "watchdog",
    "heartbeat",
    "timeout",
    "restart",
    "recovery",
    "state reconciliation",
    "abnormal transition",
    "mutual exclusion",
    "one-hot",
    "illegal state",
    "command arbitration",
    "manual auto",
    "local remote",
    "feedback confirmation",
    "trip latch",
    "reset condition",
    "bad quality",
    "stale data",
    "degraded mode",
    "debounce",
    "hysteresis",
    "one-shot",
    "scan"
  ],
  "revision_notes": [
    "2026-08-06: SW-02 대표 출제문제 10개와 8단계 Model Answer 구조를 작성했다.",
    "단독 broad alias인 PLC, SCADA, Alarm, Trip, Interlock, SIS는 routing_aliases에서 제외했다.",
    "SW-03 및 SW-05 경계 질문은 보조 범위로만 포함했다."
  ]
}
EOF_SW02_MODEL_ANSWER_3A68
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json" <<'EOF_SW02_IMPORTANCE_1F24'
{
  "schema_version": "topic_pack.topic_importance.v1",
  "topic_id": "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
  "difficulty": "DESIGN_EVALUATION",
  "selection_importance": "CORE_MUST_PREPARE",
  "question_type": "PRINCIPLE_INTERPRETATION",
  "high_band_unlock_conditions": [
    "Sequence를 State, 진입조건, 동작, 완료 피드백, Timeout과 실패·복구 경로로 설명한다.",
    "Permissive, Interlock, Trip 및 정상 Shutdown을 목적·시점·우선순위·Latch·Reset 기준으로 구분한다.",
    "상태전이 논리식 또는 허용 전이표를 제시하고 이상전이 방지조건을 설명한다.",
    "Cause & Effect, M-out-of-N Voting과 First-out의 역할과 한계를 구분한다.",
    "Bypass와 Override의 권한, 표시, 제한시간, 대체조치 및 복구확인을 제시한다.",
    "Fail-safe를 공정별 Safe state로 정의하고 Watchdog·Bad quality·Degraded mode를 연결한다.",
    "Restart 시 실제 설비상태 재수집, State reconciliation, Permissive 재확인과 Latch 보존을 설명한다.",
    "SW-03의 운전정보 관리와 SW-05의 SIL·안전수명주기를 ownership 경계로 명확히 분리한다."
  ],
  "note": "Sequence와 Interlock·Permissive·Trip은 PLC·DCS 응용문제, Cause & Effect, 시운전 및 이상상황 대응의 공통 기반이다. 단순 용어 암기가 아니라 상태전이, 우선순위, 피드백 확인, Fail-safe와 복구까지 연결해야 고득점이 가능하므로 핵심 준비 Topic으로 분류한다.",
  "revision_notes": [
    "2026-08-06: difficulty=DESIGN_EVALUATION, selection_importance=CORE_MUST_PREPARE로 확정했다.",
    "question_type은 개념과 동작 메커니즘 비교가 중심이므로 PRINCIPLE_INTERPRETATION으로 설정했다."
  ],
  "topic_label": "SW-02 제어논리·Sequence·Interlock·Trip"
}
EOF_SW02_IMPORTANCE_1F24
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json"
    else
        created_count=$((created_count + 1))
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    cat > "scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py" <<'EOF_SW02_FOCUSED_TEST_9C53'
#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

JSON_FILES = [
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
]
BROAD_ALIASES = {
    "plc", "dcs", "scada", "hmi", "alarm", "trip", "interlock",
    "permissive", "sis", "sil", "sequence", "watchdog", "bypass",
}
SW03_MARKERS = {
    "alarm philosophy", "alarm rationalization", "alarm priority",
    "deadband", "shelving", "suppression", "display hierarchy",
    "operator authority",
}
SW05_MARKERS = {
    "pfdavg", "pfh", "safety lifecycle", "systematic failure",
    "safety v&v", "sil calculation",
}


def load_json(name: str) -> dict[str, Any]:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def permissive_all(values: list[bool]) -> bool:
    return all(values)


def transition_enable(
    command: bool,
    permissives: list[bool],
    feedback_ok: bool,
    trip: bool,
    inhibit: bool,
) -> bool:
    return (
        command
        and permissive_all(permissives)
        and feedback_ok
        and not trip
        and not inhibit
    )


def vote_moo_n(values: list[bool], m: int) -> bool:
    if not values or m < 1 or m > len(values):
        raise ValueError("invalid M-out-of-N configuration")
    return sum(bool(value) for value in values) >= m


def trip_latch(previous: bool, event: bool, reset_valid: bool) -> bool:
    return event or (previous and not reset_valid)


def watchdog_expired(now: float, last_heartbeat: float, timeout: float) -> bool:
    if timeout <= 0 or now < last_heartbeat:
        raise ValueError("invalid watchdog time")
    return now - last_heartbeat > timeout


def local_topic_score(text: str, aliases: list[str], field_points: list[str]) -> int:
    norm = normalize(text)
    alias_hits = sum(1 for alias in aliases if normalize(alias) in norm)
    field_hits = sum(1 for term in field_points if normalize(term) in norm)
    return alias_hits * 5 + min(field_hits, 12)


class TopicPackStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")
        cls.model = load_json("model_answer.json")
        cls.importance = load_json("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = SHEET.read_text(encoding="utf-8")

    def test_required_files_exist(self) -> None:
        self.assertTrue(SHEET.is_file())
        self.assertTrue((PACK / "README.md").is_file())
        for name in JSON_FILES:
            self.assertTrue((PACK / name).is_file(), name)

    def test_topic_id_and_schema_contract(self) -> None:
        expected_schema = {
            "fact_anchor.json": "topic_pack.fact_anchor.v1",
            "logic_check.json": "topic_pack.logic_check.v1",
            "model_answer.json": "topic_pack.model_answer.v1",
            "topic_importance.json": "topic_pack.topic_importance.v1",
        }
        for name, schema in expected_schema.items():
            data = load_json(name)
            self.assertEqual(data["topic_id"], TOPIC_ID, name)
            self.assertEqual(data["schema_version"], schema, name)

    def test_anchor_count_and_uniqueness(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(len(anchors), 28)
        anchor_ids = [item["anchor_id"] for item in anchors]
        self.assertEqual(len(anchor_ids), len(set(anchor_ids)))
        for item in anchors:
            self.assertEqual(item["id"], item["anchor_id"])
            self.assertIn(item["importance"], {"must", "important", "optional"})
            self.assertTrue(item["statement"].strip())
            self.assertTrue(item["core_terms"])

    def test_fatal_count_and_shape(self) -> None:
        fatals = self.fact["fatal_wrong_claims"]
        self.assertEqual(len(fatals), 16)
        ids = [item["id"] for item in fatals]
        self.assertEqual(len(ids), len(set(ids)))
        for item in fatals:
            self.assertEqual(item["severity"], "fatal")
            self.assertTrue(item["wrong_claim"])
            self.assertTrue(item["correct_rule"])
            self.assertTrue(item["affected_layers"])

    def test_model_references_are_valid(self) -> None:
        anchor_ids = {item["anchor_id"] for item in self.fact["anchors"]}
        self.assertEqual(len(self.model["expected_question_patterns"]), 10)
        self.assertEqual(len(self.model["recommended_outline"]), 8)
        for pattern in self.model["expected_question_patterns"]:
            self.assertTrue(pattern["pattern"].strip())
            self.assertTrue(set(pattern["required_anchor_ids"]) <= anchor_ids)
        for section in self.model["recommended_outline"]:
            self.assertTrue(set(section["anchor_refs"]) <= anchor_ids)

    def test_importance_contract(self) -> None:
        self.assertEqual(self.importance["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.importance["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertGreaterEqual(
            len(self.importance["high_band_unlock_conditions"]),
            8,
        )

    def test_logic_profile_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        llm = self.logic["llm_profile"]
        self.assertTrue(deterministic["enabled"])
        self.assertEqual(len(deterministic["fatal_checks"]), 16)
        self.assertEqual(len(llm["fatal_conditions"]), 16)
        self.assertGreaterEqual(len(llm["major_checks"]), 8)
        self.assertGreaterEqual(len(llm["false_positive_cautions"]), 8)
        for check in deterministic["fatal_checks"]:
            self.assertTrue(check["wrong_patterns"])
            self.assertEqual(check["severity"], "fatal")

    def test_sw03_and_sw05_boundaries_are_explicit(self) -> None:
        combined = normalize(
            json.dumps(self.fact, ensure_ascii=False)
            + json.dumps(self.logic, ensure_ascii=False)
            + self.readme
            + self.sheet
        )
        for marker in [
            "sw-03", "alarm philosophy", "soe", "operator authority",
            "sw-05", "sil 산정", "안전수명주기", "safety v&v",
        ]:
            self.assertIn(normalize(marker), combined)

    def test_no_broad_routing_alias(self) -> None:
        aliases = {normalize(value) for value in self.model["routing_aliases"]}
        self.assertTrue(aliases)
        self.assertFalse(aliases & BROAD_ALIASES)

    def test_scope_does_not_claim_sw03_or_sw05_ownership(self) -> None:
        scope_anchor = next(
            item for item in self.fact["anchors"]
            if item["anchor_id"] == "sw02_scope_operational_logic"
        )
        scope = normalize(scope_anchor["statement"])
        for marker in SW03_MARKERS | SW05_MARKERS:
            self.assertNotIn(marker, scope)

    def test_required_semantic_groups(self) -> None:
        combined = normalize(
            json.dumps(self.fact, ensure_ascii=False)
            + json.dumps(self.model, ensure_ascii=False)
        )
        groups = {
            "state": ["sequence", "state transition", "상태전이", "transition guard"],
            "protection": ["permissive", "interlock", "trip", "shutdown"],
            "diagnosis": ["voting", "first-out", "watchdog", "bad quality"],
            "governance": ["bypass", "override", "command arbitration"],
            "recovery": ["restart", "recovery", "state reconciliation"],
        }
        for group, markers in groups.items():
            with self.subTest(group=group):
                self.assertGreaterEqual(
                    sum(normalize(marker) in combined for marker in markers),
                    3,
                )

    def test_text_files_have_clean_whitespace(self) -> None:
        paths = [SHEET, PACK / "README.md"] + [PACK / name for name in JSON_FILES]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"), path)
            for line_number, line in enumerate(text.splitlines(), start=1):
                self.assertEqual(line, line.rstrip(), f"{path}:{line_number}")


class DeterministicFatalPatternSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")

    def test_direct_wrong_claims_match_deterministic_aids(self) -> None:
        checks = {
            item["id"]: item
            for item in self.logic["deterministic_checks"]["fatal_checks"]
        }
        for fatal in self.fact["fatal_wrong_claims"]:
            with self.subTest(fatal=fatal["id"]):
                patterns = checks[fatal["id"]]["wrong_patterns"]
                self.assertTrue(
                    any(
                        re.search(
                            pattern,
                            fatal["wrong_claim"],
                            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
                        )
                        for pattern in patterns
                    )
                )

    def test_explicit_corrections_do_not_trigger_patterns(self) -> None:
        corrections = [
            "Permissive와 Trip은 같은 개념이 아니며 시작 허가와 강제 정지로 구분한다.",
            "Interlock은 Alarm만을 의미하지 않고 동작 금지 또는 강제 전이를 수행한다.",
            "Trip 원인이 사라져도 즉시 자동 Reset하면 안 된다.",
            "Bypass에는 승인, 표시와 시간제한이 반드시 필요하다.",
            "Fail-safe는 항상 Close가 아니라 공정별 안전상태로 정한다.",
            "Voting을 적용하면 항상 안전성이 증가하는 것은 아니다.",
            "First-out은 마지막 원인이 아니라 최초 성립 원인을 보존한다.",
            "Watchdog은 감시 표시만 하는 것이 아니라 Timeout 시 안전 동작을 수행한다.",
            "Restart 시 조건 확인 없이 이전 Step을 그대로 재개하면 안 된다.",
            "Cause & Effect 표는 실행논리 프로그램을 완성하거나 대체하지 않는다.",
            "Timer 만료만으로 실제 Feedback을 대신할 수 없다.",
            "Override와 Bypass는 동일하지 않다.",
            "정상 Shutdown과 Trip은 같은 개념이 아니다.",
            "모든 Interlock가 자동으로 SIS 또는 SIL 기능이 되는 것은 아니다.",
            "Manual 모드에서도 보호 Interlock와 Trip을 모두 해제하면 안 된다.",
            "Bad quality 신호를 정상으로 간주하면 안 된다.",
        ]
        checks = self.logic["deterministic_checks"]["fatal_checks"]
        for correction in corrections:
            with self.subTest(correction=correction):
                hits = [
                    check["id"]
                    for check in checks
                    if any(
                        re.search(
                            pattern,
                            correction,
                            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
                        )
                        for pattern in check["wrong_patterns"]
                    )
                ]
                self.assertEqual(hits, [])


class LogicRelationshipTests(unittest.TestCase):
    def test_transition_requires_all_guards(self) -> None:
        self.assertTrue(
            transition_enable(True, [True, True], True, False, False)
        )
        self.assertFalse(
            transition_enable(True, [True, False], True, False, False)
        )
        self.assertFalse(
            transition_enable(True, [True, True], True, True, False)
        )
        self.assertFalse(
            transition_enable(True, [True, True], True, False, True)
        )

    def test_voting_logic(self) -> None:
        self.assertTrue(vote_moo_n([True, True, False], 2))
        self.assertFalse(vote_moo_n([True, False, False], 2))
        with self.assertRaises(ValueError):
            vote_moo_n([True, False], 3)

    def test_trip_latch_is_set_dominant(self) -> None:
        self.assertTrue(trip_latch(False, True, True))
        self.assertTrue(trip_latch(True, False, False))
        self.assertFalse(trip_latch(True, False, True))
        self.assertFalse(trip_latch(False, False, False))

    def test_watchdog_timeout_boundary(self) -> None:
        self.assertFalse(watchdog_expired(10.0, 5.0, 5.0))
        self.assertTrue(watchdog_expired(10.01, 5.0, 5.0))
        with self.assertRaises(ValueError):
            watchdog_expired(4.0, 5.0, 1.0)


class FocusedRoutingBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        model = load_json("model_answer.json")
        cls.aliases = model["routing_aliases"]
        cls.fields = model["routing_field_points"]

    def test_positive_cases_have_local_signal(self) -> None:
        samples = [
            "Sequence control의 state transition과 permissive, interlock, trip 우선순위를 설명하시오.",
            "Cause & Effect와 2oo3 voting, first-out 로직을 설계하시오.",
            "Bypass와 override의 차이 및 manual auto command arbitration을 설명하시오.",
            "Watchdog timeout과 restart recovery의 state reconciliation을 설명하시오.",
            "PLC sequence에서 feedback confirmation, trip latch와 abnormal transition을 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertGreaterEqual(
                    local_topic_score(sample, self.aliases, self.fields),
                    4,
                )

    def test_sw03_boundary_cases_do_not_match_compound_alias(self) -> None:
        samples = [
            "Alarm philosophy, priority, deadband, delay, shelving과 suppression을 설명하시오.",
            "High-performance HMI display hierarchy와 operator authority를 설명하시오.",
            "SCADA SOE report와 audit trail 관리방안을 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                alias_hits = sum(
                    normalize(alias) in normalize(sample)
                    for alias in self.aliases
                )
                self.assertEqual(alias_hits, 0)

    def test_sw05_boundary_cases_do_not_match_compound_alias(self) -> None:
        samples = [
            "SIL 산정과 PFDavg, PFH 계산방법을 설명하시오.",
            "Safety lifecycle, systematic failure, independence와 Safety V&V를 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                alias_hits = sum(
                    normalize(alias) in normalize(sample)
                    for alias in self.aliases
                )
                self.assertEqual(alias_hits, 0)


class SemanticAuditRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")
        cls.anchors = {item["id"]: item for item in cls.fact["anchors"]}
        cls.fatals = {item["id"]: item for item in cls.fact["fatal_wrong_claims"]}

    def test_rejected_explanations_are_anchor_specific(self) -> None:
        rejected = [tuple(item["rejected_explanations"]) for item in self.fact["anchors"]]
        self.assertEqual(len(rejected), 28)
        self.assertEqual(len(set(rejected)), 28)
        generic = "용어를 서로 같은 의미로 취급하거나 보호동작의 조건·우선순위·복구를 생략한다."
        self.assertFalse(any(generic in value for values in rejected for value in values))

    def test_transition_guard_is_representative_not_universal(self) -> None:
        text = self.anchors["sw02_transition_guard"]["statement"]
        self.assertIn("기동·명령 기반 전이의 대표식", text)
        self.assertIn("Command 없이", text)
        self.assertIn("선행조건 또는 동작 완료 확인조건", text)

    def test_timer_fatal_is_limited_to_physical_action_steps(self) -> None:
        fatal = self.fatals["sw02_fatal_timer_is_feedback"]
        for field in ("claim", "wrong_claim"):
            self.assertIn("물리적 동작 확인이 필요한 Step", fatal[field])
            self.assertIn("실제 설비 Feedback", fatal[field])
        for field in ("correction", "correct_rule", "description"):
            self.assertIn("Purge 유지시간", fatal[field])
            self.assertIn("시간 자체가", fatal[field])
            self.assertIn("정상 완료조건", fatal[field])
        self.assertNotEqual(fatal["claim"], "Timer가 만료되면 실제 설비 피드백과 관계없이 Step 완료로 판단해도 된다.")

    def test_timer_and_noncritical_watchdog_safe_boundaries(self) -> None:
        cautions = " ".join(self.logic["llm_profile"]["false_positive_cautions"])
        self.assertIn("혼합시간", cautions)
        self.assertIn("Historian", cautions)
        self.assertIn("Alarm-only", cautions)
        fatal = self.fatals["sw02_fatal_watchdog_monitor_only"]
        for field in ("correction", "correct_rule", "description"):
            self.assertIn("제어기 Task", fatal[field])
            self.assertIn("필수 통신", fatal[field])
            self.assertIn("원격 I/O", fatal[field])
            self.assertIn("Historian", fatal[field])
            self.assertIn("Alarm-only", fatal[field])
        self.assertNotIn("연결해야 한다.", fatal["description"].split("비중요 Historian", 1)[-1])

    def test_fail_safe_negated_absolute_remains_unchanged(self) -> None:
        text = self.anchors["sw02_fail_safe"]["statement"]
        self.assertIn("항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
EOF_SW02_FOCUSED_TEST_9C53
    write_rc=$?
    printf 'WRITE_RC=%s|%s\n' "scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py" "$write_rc"
    if [ "$write_rc" -ne 0 ]; then
        fail "WRITE_FAILED: scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py"
    else
        created_count=$((created_count + 1))
    fi
fi


else
    pass "existing complete SW-02 payload retained without rewrite"
fi


CURRENT_STAGE="SW02_TOPIC_LOCAL_VALIDATION"
NEXT_STAGE="SW02_OWNERSHIP_VALIDATION"
section_header "2A. verify exact embedded source payload hashes"

if [ "$failure_count" -eq 0 ]; then
    for path in "${TARGET_PATHS[@]}"; do
        actual_sha="$(sha256sum "$path" | awk '{print $1}')"
        expected_sha="${EXPECTED_SHA256[$path]}"
        printf 'PAYLOAD_SHA256=%s|%s\n' "$path" "$actual_sha"
        if [ "$actual_sha" = "$expected_sha" ]; then
            pass "payload hash matches: $path"
        else
            fail "PAYLOAD_HASH_MISMATCH: $path"
        fi
    done
fi

section_header "3. validate JSON syntax and production Topic Pack schema"

if [ "$failure_count" -eq 0 ]; then
    for path in "${JSON_PATHS[@]}"; do
        printf '\n--- JSON_SYNTAX:%s ---\n' "$path"
        python3 -m json.tool "$path" >/dev/null
        json_rc=$?
        printf 'STEP_RC=JSON_SYNTAX:%s|%s\n' "$path" "$json_rc"
        if [ "$json_rc" -ne 0 ]; then
            fail "JSON_SYNTAX:$path"
        fi
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
anchor_ids = validator.validate_fact_anchor(
    pack_dir,
    topic_id,
    global_anchor_ids,
)
validator.validate_model_answer(pack_dir, topic_id, anchor_ids)
validator.validate_topic_importance(pack_dir, topic_id)
validator.validate_logic_check(pack_dir, topic_id)

print("TOPIC_LOCAL_SCHEMA_VALID=true")
print(f"TOPIC_LOCAL_ANCHOR_COUNT={len(anchor_ids)}")
PY_SCHEMA
    schema_rc=$?
    printf 'STEP_RC=TOPIC_LOCAL_PRODUCTION_SCHEMA_VALIDATION|%s\n' "$schema_rc"
    if [ "$schema_rc" -ne 0 ]; then
        fail "TOPIC_LOCAL_PRODUCTION_SCHEMA_VALIDATION"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    if [ -f "scripts/validate_topic_pack_quality.py" ]; then
        run_step \
            "VALIDATE_SW02_TOPIC_QUALITY" \
            python3 scripts/validate_topic_pack_quality.py \
                --topic-id "$TOPIC_ID" \
                --strict-generic-aliases \
                --require-logic-check
    else
        fail "TOPIC_QUALITY_VALIDATOR_MISSING"
    fi
fi

section_header "4. run SW-02 focused regressions and whitespace checks"

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "PY_COMPILE_SW02_FOCUSED_TEST" \
        python3 -m py_compile "$TEST_PATH"
fi

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "RUN_SW02_FOCUSED_TEST" \
        python3 "$TEST_PATH"
fi

if [ "$failure_count" -eq 0 ]; then
    printf '\n--- TOPIC_LOCAL_WHITESPACE_VALIDATION ---\n'
    python3 - "${TARGET_PATHS[@]}" <<'PY_WHITESPACE'
from __future__ import annotations

import sys
from pathlib import Path

errors: list[str] = []
for raw in sys.argv[1:]:
    path = Path(raw)
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        errors.append(f"{path}: missing final newline")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            errors.append(f"{path}:{line_number}: trailing whitespace")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("TOPIC_LOCAL_WHITESPACE_VALID=true")
PY_WHITESPACE
    whitespace_rc=$?
    printf 'STEP_RC=TOPIC_LOCAL_WHITESPACE_VALIDATION|%s\n' "$whitespace_rc"
    if [ "$whitespace_rc" -ne 0 ]; then
        fail "TOPIC_LOCAL_WHITESPACE_VALIDATION"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    run_step \
        "GIT_DIFF_CHECK_SW02_TARGETS" \
        git diff --check -- "${TARGET_PATHS[@]}"
fi


CURRENT_STAGE="SW02_OWNERSHIP_VALIDATION"
NEXT_STAGE="SW02_LOCAL_COMMIT"
section_header "5. verify strict Lane A and SW-02 ownership boundary"

if [ "$failure_count" -eq 0 ]; then
    collect_repository_paths > "$changed_paths_file"

    {
        printf '%s\n' "${TARGET_PATHS[@]}"
        printf '%s\n' "$SCRIPT_REL"
    } | LC_ALL=C sort -u > "$allowed_paths_file"

    printf 'ALLOWED_SW02_CHANGED_PATHS_BEGIN\n'
    cat "$allowed_paths_file"
    printf 'ALLOWED_SW02_CHANGED_PATHS_END\n'
    printf 'ACTUAL_CHANGED_PATHS_BEGIN\n'
    cat "$changed_paths_file"
    printf 'ACTUAL_CHANGED_PATHS_END\n'

    current_unrelated_paths_file="$(mktemp)"
    current_unrelated_manifest_file="$(mktemp)"
    comm -23 "$changed_paths_file" "$allowed_paths_file" > "$current_unrelated_paths_file"
    write_path_manifest "$current_unrelated_paths_file" "$current_unrelated_manifest_file"

    if ! cmp -s "$baseline_unrelated_paths_file" "$current_unrelated_paths_file"; then
        printf 'BASELINE_UNRELATED_PATHS_BEGIN\n'
        cat "$baseline_unrelated_paths_file"
        printf 'BASELINE_UNRELATED_PATHS_END\n'
        printf 'CURRENT_UNRELATED_PATHS_BEGIN\n'
        cat "$current_unrelated_paths_file"
        printf 'CURRENT_UNRELATED_PATHS_END\n'
        fail "SW02_OWNERSHIP_CHANGE_SET_DIFFERS_FROM_BASELINE"
    elif ! cmp -s "$baseline_unrelated_manifest_file" "$current_unrelated_manifest_file"; then
        printf 'CURRENT_BASELINE_MANIFEST_DIFF_BEGIN\n'
        diff -u "$baseline_unrelated_manifest_file" "$current_unrelated_manifest_file" || true
        printf 'CURRENT_BASELINE_MANIFEST_DIFF_END\n'
        fail "SW02_OWNERSHIP_BASELINE_CONTENT_CHANGED"
    else
        pass "all newly introduced changes are confined to SW-02 and its Lane A script"
    fi
    rm -f -- "$current_unrelated_paths_file" "$current_unrelated_manifest_file"

    for path in "${TARGET_PATHS[@]}"; do
        if ! grep -Fxq "$path" "$changed_paths_file"; then
            fail "SW02_REQUIRED_PATH_NOT_CHANGED_OR_ADDED: $path"
        fi
    done

    generated_changes="$(grep '^rubrics/generated/' "$changed_paths_file" 2>/dev/null || true)"
    if [ -n "$generated_changes" ]; then
        printf '%s\n' "$generated_changes" | sed 's/^/UNEXPECTED_GENERATED_CHANGE=/'
        fail "GENERATED_BANK_CHANGED"
    else
        pass "rubrics/generated remains unchanged"
    fi

    production_python_changes="$(
        awk '
            /\.py$/ {
                if ($0 != "'"$TEST_PATH"'") print
            }
        ' "$changed_paths_file"
    )"
    if [ -n "$production_python_changes" ]; then
        printf '%s\n' "$production_python_changes" | sed 's/^/UNEXPECTED_PYTHON_CHANGE=/'
        fail "PRODUCTION_OR_UNRELATED_PYTHON_CHANGED"
    else
        pass "only the SW-02 focused test changes Python"
    fi

    run_step \
        "GIT_DIFF_CHECK_SW02_COMMIT_PATHS" \
        git diff --check -- "${TARGET_PATHS[@]}" "$SCRIPT_REL"
fi

CURRENT_STAGE="SW02_LOCAL_COMMIT"
NEXT_STAGE="SW03_AUTHORING_PACKAGE"
section_header "6. create one Topic-local SW-02 commit"

if [ "$failure_count" -eq 0 ]; then
    git add -- "${TARGET_PATHS[@]}" "$SCRIPT_REL"
    add_rc=$?
    printf 'STEP_RC=GIT_ADD_SW02_TOPIC_ONLY|%s\n' "$add_rc"
    if [ "$add_rc" -ne 0 ]; then
        fail "GIT_ADD_SW02_TOPIC_ONLY"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    staged_paths_file="$(mktemp)"
    git diff --cached --name-only | LC_ALL=C sort -u > "$staged_paths_file"

    printf 'STAGED_SW02_PATHS_BEGIN\n'
    cat "$staged_paths_file"
    printf 'STAGED_SW02_PATHS_END\n'

    unexpected_staged="$(
        comm -23 "$staged_paths_file" "$allowed_paths_file"
    )"
    if [ -n "$unexpected_staged" ]; then
        printf '%s\n' "$unexpected_staged" | sed 's/^/UNEXPECTED_STAGED_PATH=/'
        fail "UNRELATED_PATH_STAGED_FOR_SW02_COMMIT"
    fi

    for path in "${TARGET_PATHS[@]}"; do
        if ! grep -Fxq "$path" "$staged_paths_file"; then
            fail "REQUIRED_SW02_PATH_NOT_STAGED: $path"
        fi
    done

    run_step \
        "GIT_CACHED_DIFF_CHECK_SW02" \
        git diff --cached --check
fi

if [ "$failure_count" -eq 0 ]; then
    git commit -m "$COMMIT_SUBJECT"
    commit_rc=$?
    printf 'STEP_RC=GIT_COMMIT_SW02|%s\n' "$commit_rc"
    if [ "$commit_rc" -ne 0 ]; then
        fail "GIT_COMMIT_SW02"
    fi
fi

if [ "$failure_count" -eq 0 ]; then
    SW02_COMMIT_HASH="$(git rev-parse HEAD)"
    SW02_COMMIT_SUBJECT="$(git show -s --format='%s' HEAD)"
    commit_files_file="$(mktemp)"
    git diff-tree --no-commit-id --name-only -r HEAD | LC_ALL=C sort -u > "$commit_files_file"

    if [ "$SW02_COMMIT_SUBJECT" != "$COMMIT_SUBJECT" ]; then
        fail "CREATED_COMMIT_SUBJECT_MISMATCH"
    fi

    unexpected_commit_files="$(
        comm -23 "$commit_files_file" "$allowed_paths_file"
    )"
    if [ -n "$unexpected_commit_files" ]; then
        printf '%s\n' "$unexpected_commit_files" | sed 's/^/UNEXPECTED_COMMITTED_FILE=/'
        fail "CREATED_COMMIT_CONTAINS_NON_SW02_FILES"
    fi

    for path in "${TARGET_PATHS[@]}"; do
        if ! grep -Fxq "$path" "$commit_files_file"; then
            fail "CREATED_COMMIT_MISSING_SW02_FILE: $path"
        fi
    done

    target_post_commit_status="$(git status --porcelain=v1 -- "${TARGET_PATHS[@]}" "$SCRIPT_REL")"
    if [ -n "$target_post_commit_status" ]; then
        printf 'SW02_POST_COMMIT_TARGET_STATUS_BEGIN\n%s\nSW02_POST_COMMIT_TARGET_STATUS_END\n' "$target_post_commit_status"
        fail "SW02_TARGETS_NOT_CLEAN_AFTER_TOPIC_COMMIT"
    else
        pass "SW-02 Topic files and Lane A authoring script are clean after commit"
    fi

    post_changed_paths_file="$(mktemp)"
    post_unrelated_paths_file="$(mktemp)"
    post_unrelated_manifest_file="$(mktemp)"
    collect_repository_paths > "$post_changed_paths_file"
    comm -23 "$post_changed_paths_file" "$allowed_paths_file" > "$post_unrelated_paths_file"
    write_path_manifest "$post_unrelated_paths_file" "$post_unrelated_manifest_file"

    if ! cmp -s "$baseline_unrelated_paths_file" "$post_unrelated_paths_file"; then
        printf 'BASELINE_UNRELATED_PATHS_BEGIN\n'
        cat "$baseline_unrelated_paths_file"
        printf 'BASELINE_UNRELATED_PATHS_END\n'
        printf 'POST_COMMIT_UNRELATED_PATHS_BEGIN\n'
        cat "$post_unrelated_paths_file"
        printf 'POST_COMMIT_UNRELATED_PATHS_END\n'
        fail "PREEXISTING_LANE_A_CHANGE_SET_WAS_NOT_PRESERVED"
    elif ! cmp -s "$baseline_unrelated_manifest_file" "$post_unrelated_manifest_file"; then
        printf 'PREEXISTING_CHANGE_MANIFEST_DIFF_BEGIN\n'
        diff -u "$baseline_unrelated_manifest_file" "$post_unrelated_manifest_file" || true
        printf 'PREEXISTING_CHANGE_MANIFEST_DIFF_END\n'
        fail "PREEXISTING_LANE_A_CHANGE_CONTENT_WAS_NOT_PRESERVED"
    elif [ -s "$post_unrelated_paths_file" ]; then
        while IFS= read -r preserved_path; do
            printf 'PRESERVED_POST_COMMIT_CHANGE=%s\n' "$preserved_path"
        done < "$post_unrelated_paths_file"
        pass "pre-existing non-SW02 Lane A changes remain byte-identical after commit"
    else
        pass "Lane A worktree contains no unrelated changes after SW-02 commit"
    fi
fi

CURRENT_STAGE="SW02_TOPIC_LOCAL_COMPLETE"
NEXT_STAGE="SW03_AUTHORING_PACKAGE"
if [ "$failure_count" -eq 0 ]; then
    LANE_PROGRESS="1/4"
fi
section_header "7. summarize SW-02 Topic-local result"

if [ "$failure_count" -eq 0 ]; then
    python3 - "$TOPIC_DIR" <<'PY_SUMMARY'
from __future__ import annotations

import json
import sys
from pathlib import Path

pack = Path(sys.argv[1])
fact = json.loads((pack / "fact_anchor.json").read_text(encoding="utf-8"))
logic = json.loads((pack / "logic_check.json").read_text(encoding="utf-8"))
model = json.loads((pack / "model_answer.json").read_text(encoding="utf-8"))
importance = json.loads((pack / "topic_importance.json").read_text(encoding="utf-8"))

print(f"SW02_ANCHOR_COUNT={len(fact['anchors'])}")
print(f"SW02_FATAL_COUNT={len(fact['fatal_wrong_claims'])}")
print(f"SW02_LOGIC_FATAL_COUNT={len(logic['deterministic_checks']['fatal_checks'])}")
print(f"SW02_LLM_MAJOR_COUNT={len(logic['llm_profile']['major_checks'])}")
print(f"SW02_FALSE_POSITIVE_CAUTION_COUNT={len(logic['llm_profile']['false_positive_cautions'])}")
print(f"SW02_ROUTING_ALIAS_COUNT={len(model['routing_aliases'])}")
print(f"SW02_ROUTING_FIELD_POINT_COUNT={len(model['routing_field_points'])}")
print(f"SW02_QUESTION_PATTERN_COUNT={len(model['expected_question_patterns'])}")
print(f"SW02_OUTLINE_SECTION_COUNT={len(model['recommended_outline'])}")
print(f"SW02_DIFFICULTY={importance['difficulty']}")
print(f"SW02_SELECTION_IMPORTANCE={importance['selection_importance']}")
PY_SUMMARY
    summary_rc=$?
    printf 'STEP_RC=SW02_SOURCE_SUMMARY|%s\n' "$summary_rc"
    if [ "$summary_rc" -ne 0 ]; then
        fail "SW02_SOURCE_SUMMARY"
    fi
fi

printf '%s\n' \
    "failure_count=$failure_count" \
    "warning_count=$warning_count" \
    "created_count=$created_count" \
    "CHATGPT_SEMANTIC_REVIEW=completed_before_script" \
    "EXTERNAL_LLM_VALIDATION_EXECUTED=false" \
    "GENERATED_REBUILD_EXECUTED=false" \
    "VALIDATE_ALL_EXECUTED=false" \
    "RELEASE_PROMOTION_EXECUTED=false" \
    "PUSH_EXECUTED=false"

if [ "$failure_count" -eq 0 ]; then
    result_header "SW02_TOPIC_LOCAL_COMMIT_COMPLETE"
    printf '%s\n' \
        "LANE=$LANE" \
        "SW_NUMBER=SW-02" \
        "TOPIC_ID=$TOPIC_ID" \
        "COMMIT_HASH=$SW02_COMMIT_HASH" \
        "COMMIT_SUBJECT=$SW02_COMMIT_SUBJECT" \
        "COMMITTED_FILES_BEGIN"
    cat "$commit_files_file"
    printf '%s\n' \
        "COMMITTED_FILES_END" \
        "VALIDATION_RESULT=JSON_SCHEMA_FOCUSED_TEST_PY_COMPILE_DIFF_CHECK_OWNERSHIP_PASS" \
        "NEXT_TOPIC=SW-03 hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management" \
        "LANE_PROGRESS=$LANE_PROGRESS" \
        "PUSH_EXECUTED=false"
else
    result_header "SW02_TOPIC_LOCAL_COMMIT_FAILED"
    printf '%s\n' \
        "VALIDATION_RESULT=FAILED" \
        "NEXT_TOPIC=SW-02 minimal repair" \
        "LANE_PROGRESS=$LANE_PROGRESS" \
        "PUSH_EXECUTED=false"
fi

(return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
