#!/usr/bin/env bash
set -Eeuo pipefail

cd /workspace/prof_eng_answer
mkdir -p logs

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${BOT_TOKEN:-}" ]; then
  export TELEGRAM_BOT_TOKEN="${BOT_TOKEN}"
fi

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_TOKEN:-}" ]; then
  export TELEGRAM_BOT_TOKEN="${TELEGRAM_TOKEN}"
fi

if [ -z "${BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_BOT_TOKEN:-}" ]; then
  export BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
fi

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] && [ -z "${BOT_TOKEN:-}" ]; then
  echo "[$(date -Is)] ERROR: Telegram bot token is not set. Set TELEGRAM_BOT_TOKEN or BOT_TOKEN in .env" >> logs/prof_eng_answer.log
  exit 1
fi

echo "[$(date -Is)] prof_eng_answer_bot service started" >> logs/prof_eng_answer.log
echo "[$(date -Is)] cwd=$(pwd)" >> logs/prof_eng_answer.log
echo "[$(date -Is)] DIFFICULTY_CEILING_MODE=${DIFFICULTY_CEILING_MODE:-}" >> logs/prof_eng_answer.log

exec python -u bot.py >> logs/prof_eng_answer.log 2>&1
