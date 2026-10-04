#!/usr/bin/env bash
set -Eeuo pipefail

# 기본은 읽기 전용 미리보기. 삭제하지 않고, 명시적 격리 모드에서만
# 오래된 tmp_pack_* 파일을 사용자가 지정한 다른 파일시스템으로 이동한다.
readonly GIT_DIR=/home/now0930/.git
readonly REPO_ROOT=/home/now0930/chatgpt_project
readonly PACK_DIR="$GIT_DIR/objects/pack"
readonly MIN_AGE_DEFAULT=48
readonly SAFETY_MARGIN=$((5 * 1024 * 1024 * 1024))

mode=dry-run
destination=
min_age=$MIN_AGE_DEFAULT
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
usage() {
  cat <<'EOF'
Usage:
  scripts/clean_home_git_tmp_packs.sh [--older-than-hours N]
  scripts/clean_home_git_tmp_packs.sh --quarantine EXISTING_DEST [--older-than-hours N]

기본은 읽기 전용입니다. 48시간 이상 지난 tmp_pack_* 일반 파일만 대상으로
표시합니다. --quarantine은 지정한 다른 파일시스템으로 이동하며 삭제하지 않습니다.
대상 Git 디렉터리는 /home/now0930/.git으로 고정되어 있습니다.
EOF
}

while (($#)); do
  case "$1" in
    --quarantine)
      (($# >= 2)) || fail '--quarantine에 대상 경로가 필요합니다'
      mode=quarantine; destination=$2; shift 2 ;;
    --older-than-hours)
      (($# >= 2)) || fail '--older-than-hours에 정수가 필요합니다'
      [[ $2 =~ ^[0-9]+$ ]] || fail '시간은 정수여야 합니다'
      min_age=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; fail "알 수 없는 옵션: $1" ;;
  esac
done

((min_age >= 24)) || fail '최소 경과 시간은 24시간입니다'
[[ -d $GIT_DIR && ! -L $GIT_DIR && -d $PACK_DIR && ! -L $PACK_DIR ]] \
  || fail '예상한 Git/pack 디렉터리가 없거나 심볼릭 링크입니다'
resolved_root=$(env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR \
  git --git-dir="$GIT_DIR" --work-tree="$REPO_ROOT" rev-parse --show-toplevel 2>/dev/null) \
  || fail '예상한 Git worktree를 확인할 수 없습니다'
[[ $(realpath -e -- "$resolved_root") == $(realpath -e -- "$REPO_ROOT") ]] \
  || fail 'Git 디렉터리가 예상 저장소와 일치하지 않습니다'

if [[ $mode == quarantine ]]; then
  [[ -d $destination && -w $destination ]] || fail '격리 경로는 존재하며 쓰기 가능해야 합니다'
  destination=$(realpath -e -- "$destination")
  [[ $destination != "$GIT_DIR"* && $destination != "$PACK_DIR"* ]] \
    || fail '격리 경로는 Git 디렉터리 바깥이어야 합니다'
fi

mapfile -d '' candidates < <(
  find "$PACK_DIR" -mindepth 1 -maxdepth 1 -type f -name 'tmp_pack_*' \
    -mmin "+$((min_age * 60))" -print0
)
((${#candidates[@]})) || { printf '%s시간보다 오래된 대상 파일이 없습니다.\n' "$min_age"; exit 0; }

total=0
for file in "${candidates[@]}"; do
  [[ -f $file && ! -L $file ]] || fail "일반 파일이 아닙니다: $file"
  size=$(stat -c '%s' -- "$file")
  total=$((total + size))
  printf '%s  %s bytes\n' "$file" "$size"
done
printf '대상 %d개, 총 %.2f GiB, 모드=%s\n' \
  "${#candidates[@]}" "$(awk -v n="$total" 'BEGIN {print n/1024/1024/1024}')" "$mode"
[[ $mode == quarantine ]] || exit 0

command -v flock >/dev/null || fail 'flock가 필요합니다'
command -v lsof >/dev/null || fail 'lsof가 필요합니다'
exec 9>/tmp/clean_home_git_tmp_packs.lock
flock -n 9 || fail '다른 정리 스크립트가 실행 중입니다'
for proc in git git-pack-objects git-index-pack git-repack; do
  pgrep -x "$proc" >/dev/null && fail "Git 프로세스가 실행 중입니다: $proc"
done
for lock in "$GIT_DIR/gc.pid" "$GIT_DIR/index.lock" "$GIT_DIR/packed-refs.lock"; do
  [[ ! -e $lock ]] || fail "Git 잠금 파일이 있습니다: $lock"
done
if find "$PACK_DIR" -maxdepth 1 -type f -name '*.lock' -print -quit | grep -q .; then
  fail 'pack 잠금 파일이 있습니다'
fi

[[ $(stat -c '%d' -- "$PACK_DIR") != "$(stat -c '%d' -- "$destination")" ]] \
  || fail '격리 경로는 다른 파일시스템이어야 합니다'
available=$(df -B1 --output=avail -- "$destination" | tail -n 1 | tr -d ' ')
((available >= total + SAFETY_MARGIN)) || fail '대상 디스크에 파일 용량과 5GiB 여유 공간이 필요합니다'
for file in "${candidates[@]}"; do
  [[ -f $file && ! -L $file ]] || fail "검증 중 대상 파일이 바뀌었습니다: $file"
  if lsof -t -- "$file" >/dev/null 2>&1; then fail "프로세스가 사용 중인 파일입니다: $file"; fi
done

for file in "${candidates[@]}"; do
  mv --no-clobber -- "$file" "$destination/"
  [[ ! -e $file ]] || fail "이동 여부를 확인하세요: $file"
done
printf '%d개 파일을 격리했습니다. 삭제된 파일은 없습니다. 경로: %s\n' \
  "${#candidates[@]}" "$destination"
