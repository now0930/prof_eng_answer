#!/usr/bin/env bash
set -u
set -o pipefail

OVERALL_STAGE="SOFTWARE_TOPIC_PACK_PARALLELIZATION"
CURRENT_STAGE="CHECKPOINT_PUSH_AND_WORKTREE_SETUP"
NEXT_STAGE="START_LANE_A_B_C"
REPO_DIR="/home/now0930/hermes/workspace/prof_eng_answer"
REMOTE="origin"
BASE_BRANCH="main"
COMMIT_MESSAGE="chore: checkpoint software topic pack parallel lanes"

LANE_A_BRANCH="software/lane-a-control-lifecycle"
LANE_B_BRANCH="software/lane-b-network-security"
LANE_C_BRANCH="software/lane-c-safety-data-ai"

LANE_A_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_a"
LANE_B_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_b"
LANE_C_DIR="/home/now0930/hermes/workspace/prof_eng_answer_sw_lane_c"

final_rc=0

section() {
  local number="$1"
  local title="$2"
  printf '\n===== %s. %s =====\n' "$number" "$title"
  printf 'OVERALL_STAGE=%s\n' "$OVERALL_STAGE"
  printf 'CURRENT_STAGE=%s\n' "$CURRENT_STAGE"
  printf 'NEXT_STAGE=%s\n' "$NEXT_STAGE"
}

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  final_rc=1
}

require_clean_command() {
  command -v "$1" >/dev/null 2>&1 || {
    fail "required command not found: $1"
    return 1
  }
}

path_has_sensitive_name() {
  local path="$1"
  case "$path" in
    *.pem|*.key|*.p12|*.pfx|*.jks|*.keystore|*.env|*/.env|*/.env.*|*secret*|*token*|*credential*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

create_or_reuse_lane() {
  local lane_name="$1"
  local branch="$2"
  local dir="$3"
  local base_commit="$4"

  printf '\n--- %s ---\n' "$lane_name"
  printf 'lane_branch=%s\n' "$branch"
  printf 'lane_dir=%s\n' "$dir"

  if git show-ref --verify --quiet "refs/heads/$branch"; then
    local branch_commit
    branch_commit="$(git rev-parse "$branch")"
    if [ "$branch_commit" != "$base_commit" ]; then
      fail "$branch already exists at $branch_commit, expected $base_commit"
      return 1
    fi
  fi

  if git ls-remote --exit-code --heads "$REMOTE" "$branch" >/dev/null 2>&1; then
    local remote_commit
    remote_commit="$(git ls-remote "$REMOTE" "refs/heads/$branch" | awk '{print $1}')"
    if [ "$remote_commit" != "$base_commit" ]; then
      fail "$REMOTE/$branch already exists at $remote_commit, expected $base_commit"
      return 1
    fi
  fi

  if [ -e "$dir" ]; then
    if ! git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      fail "$dir exists but is not a Git worktree"
      return 1
    fi

    local actual_branch actual_commit
    actual_branch="$(git -C "$dir" branch --show-current)"
    actual_commit="$(git -C "$dir" rev-parse HEAD)"

    if [ "$actual_branch" != "$branch" ]; then
      fail "$dir uses branch $actual_branch, expected $branch"
      return 1
    fi
    if [ "$actual_commit" != "$base_commit" ]; then
      fail "$dir is at $actual_commit, expected $base_commit"
      return 1
    fi

    printf 'worktree_status=REUSED\n'
  else
    if git show-ref --verify --quiet "refs/heads/$branch"; then
      git worktree add "$dir" "$branch" || {
        fail "failed to add existing branch worktree: $branch"
        return 1
      }
    else
      git worktree add -b "$branch" "$dir" "$base_commit" || {
        fail "failed to create worktree: $branch"
        return 1
      }
    fi
    printf 'worktree_status=CREATED\n'
  fi

  mkdir -p "$dir/gemini_script"

  git -C "$dir" status --short
  if [ -n "$(git -C "$dir" status --porcelain)" ]; then
    fail "$lane_name worktree is not clean"
    return 1
  fi

  git -C "$dir" push -u "$REMOTE" "$branch" || {
    fail "failed to push lane branch: $branch"
    return 1
  }

  printf 'lane_head=%s\n' "$(git -C "$dir" rev-parse HEAD)"
  printf 'lane_remote=%s/%s\n' "$REMOTE" "$branch"
  printf 'lane_status=READY\n'
}

section 0 "contract"
printf 'REPO_DIR=%s\n' "$REPO_DIR"
printf 'BASE_BRANCH=%s\n' "$BASE_BRANCH"
printf 'REMOTE=%s\n' "$REMOTE"
printf 'POLICY=current state checkpoint commit and push, then isolated lane worktrees\n'
printf 'POLICY=no force push\n'
printf 'POLICY=abort on divergent or pre-existing nonmatching lane branches\n'

require_clean_command git || final_rc=1
require_clean_command python3 || final_rc=1

if [ "$final_rc" -ne 0 ]; then
  (return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
fi

section 1 "verify repository and main branch"
if [ ! -d "$REPO_DIR/.git" ]; then
  fail "repository not found: $REPO_DIR"
else
  cd "$REPO_DIR" || fail "cannot enter repository"
fi

if [ "$final_rc" -eq 0 ]; then
  current_branch="$(git branch --show-current)"
  printf 'current_branch=%s\n' "$current_branch"
  if [ "$current_branch" != "$BASE_BRANCH" ]; then
    fail "run this script from $BASE_BRANCH, current branch is $current_branch"
  fi

  git remote get-url "$REMOTE" >/dev/null 2>&1 || fail "remote not found: $REMOTE"
  git status --short
fi

section 2 "fetch and verify synchronization boundary"
if [ "$final_rc" -eq 0 ]; then
  git fetch "$REMOTE" "$BASE_BRANCH" || fail "git fetch failed"
fi

if [ "$final_rc" -eq 0 ]; then
  local_head="$(git rev-parse HEAD)"
  remote_head="$(git rev-parse "$REMOTE/$BASE_BRANCH")"
  merge_base="$(git merge-base HEAD "$REMOTE/$BASE_BRANCH")"

  printf 'local_head=%s\n' "$local_head"
  printf 'remote_head=%s\n' "$remote_head"
  printf 'merge_base=%s\n' "$merge_base"

  if [ "$merge_base" != "$remote_head" ]; then
    fail "local $BASE_BRANCH is behind or diverged from $REMOTE/$BASE_BRANCH; reconcile manually before checkpointing"
  fi
fi

section 3 "inspect current changes and safety guards"
if [ "$final_rc" -eq 0 ]; then
  git diff --check || fail "git diff --check failed"
fi

if [ "$final_rc" -eq 0 ]; then
  mapfile -t changed_paths < <(
    {
      git diff --name-only
      git diff --cached --name-only
      git ls-files --others --exclude-standard
    } | sed '/^$/d' | sort -u
  )

  printf 'changed_path_count=%s\n' "${#changed_paths[@]}"
  printf '%s\n' "${changed_paths[@]}"

  for path in "${changed_paths[@]}"; do
    if path_has_sensitive_name "$path"; then
      fail "sensitive-looking path detected; review manually: $path"
    fi

    if [ -f "$path" ]; then
      size_bytes="$(wc -c < "$path")"
      if [ "$size_bytes" -gt 26214400 ]; then
        fail "file larger than 25 MiB detected; review manually: $path ($size_bytes bytes)"
      fi
    fi
  done
fi

section 4 "compile changed Python files"
if [ "$final_rc" -eq 0 ]; then
  mapfile -t changed_python < <(
    {
      git diff --name-only -- '*.py'
      git diff --cached --name-only -- '*.py'
      git ls-files --others --exclude-standard -- '*.py'
    } | sed '/^$/d' | sort -u
  )

  if [ "${#changed_python[@]}" -eq 0 ]; then
    printf 'changed_python=NONE\n'
  else
    printf 'changed_python_count=%s\n' "${#changed_python[@]}"
    for py_file in "${changed_python[@]}"; do
      [ -f "$py_file" ] || continue
      printf 'py_compile=%s\n' "$py_file"
      python3 -m py_compile "$py_file" || fail "py_compile failed: $py_file"
    done
  fi
fi

section 5 "checkpoint current state"
if [ "$final_rc" -eq 0 ]; then
  if [ -n "$(git status --porcelain)" ]; then
    git add -A || fail "git add failed"
  else
    printf 'checkpoint_commit=SKIPPED_CLEAN_TREE\n'
  fi
fi

if [ "$final_rc" -eq 0 ] && [ -n "$(git diff --cached --name-only)" ]; then
  printf 'staged_files:\n'
  git diff --cached --name-status
  git commit -m "$COMMIT_MESSAGE" || fail "checkpoint commit failed"
elif [ "$final_rc" -eq 0 ]; then
  printf 'checkpoint_commit=NO_NEW_COMMIT\n'
fi

section 6 "push main checkpoint"
if [ "$final_rc" -eq 0 ]; then
  git push "$REMOTE" "$BASE_BRANCH" || fail "push of $BASE_BRANCH failed"
fi

if [ "$final_rc" -eq 0 ]; then
  base_commit="$(git rev-parse HEAD)"
  remote_after_push="$(git rev-parse "$REMOTE/$BASE_BRANCH")"
  printf 'base_commit=%s\n' "$base_commit"
  printf 'remote_after_push=%s\n' "$remote_after_push"
  if [ "$base_commit" != "$remote_after_push" ]; then
    fail "local and remote main do not match after push"
  fi
fi

section 7 "create and push isolated lane worktrees"
if [ "$final_rc" -eq 0 ]; then
  create_or_reuse_lane "SOFTWARE_LLM_LANE_A" "$LANE_A_BRANCH" "$LANE_A_DIR" "$base_commit" || final_rc=1
fi
if [ "$final_rc" -eq 0 ]; then
  create_or_reuse_lane "SOFTWARE_LLM_LANE_B" "$LANE_B_BRANCH" "$LANE_B_DIR" "$base_commit" || final_rc=1
fi
if [ "$final_rc" -eq 0 ]; then
  create_or_reuse_lane "SOFTWARE_LLM_LANE_C" "$LANE_C_BRANCH" "$LANE_C_DIR" "$base_commit" || final_rc=1
fi

section 8 "final verification"
if [ "$final_rc" -eq 0 ]; then
  git worktree list
  printf '\nmain_status:\n'
  git -C "$REPO_DIR" status --short
  printf '\nlane_a_status:\n'
  git -C "$LANE_A_DIR" status --short
  printf '\nlane_b_status:\n'
  git -C "$LANE_B_DIR" status --short
  printf '\nlane_c_status:\n'
  git -C "$LANE_C_DIR" status --short

  if [ -n "$(git -C "$REPO_DIR" status --porcelain)" ]; then
    fail "main is not clean after checkpoint"
  fi
  if [ -n "$(git -C "$LANE_A_DIR" status --porcelain)" ]; then
    fail "lane A is not clean"
  fi
  if [ -n "$(git -C "$LANE_B_DIR" status --porcelain)" ]; then
    fail "lane B is not clean"
  fi
  if [ -n "$(git -C "$LANE_C_DIR" status --porcelain)" ]; then
    fail "lane C is not clean"
  fi
fi

section 9 "lane assignments"
if [ "$final_rc" -eq 0 ]; then
  cat <<EOF
MAIN
  path:   $REPO_DIR
  branch: $BASE_BRANCH
  role:   integration only after all lanes complete

LANE A
  path:   $LANE_A_DIR
  branch: $LANE_A_BRANCH
  topics: SW-02, SW-03, SW-04, SW-10

LANE B
  path:   $LANE_B_DIR
  branch: $LANE_B_BRANCH
  topics: SW-06, SW-07, SW-08, SW-09

LANE C
  path:   $LANE_C_DIR
  branch: $LANE_C_BRANCH
  topics: SW-05, SW-11, SW-12, SW-13

Each lane:
  - modifies only its assigned source Topic Packs, Topic Sheets, and focused tests
  - commits each completed Topic separately on its own branch
  - does not push during Topic-by-Topic work
  - pushes its own branch once after all four assigned Topics pass lane validation
  - never modifies rubrics/generated/** in parallel
  - never merges or cherry-picks another lane
  - never pushes main
EOF
  printf 'PASS: CHECKPOINT PUSH AND THREE WORKTREES READY\n'
else
  printf 'FAIL: SETUP INCOMPLETE\n'
fi

(return "$final_rc" 2>/dev/null) || [ "$final_rc" -eq 0 ]
