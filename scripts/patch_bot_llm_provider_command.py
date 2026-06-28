#!/usr/bin/env python3
from pathlib import Path
import re


path = Path("bot.py")

if not path.exists():
    raise SystemExit("bot.py not found")

s = path.read_text(encoding="utf-8")

# 1. CommandHandler import 보강
if "from telegram.ext import CommandHandler" not in s and "CommandHandler" not in s.split("\n", 40)[0:]:
    s = "from telegram.ext import CommandHandler\n" + s
elif "CommandHandler" not in s:
    s = "from telegram.ext import CommandHandler\n" + s

# 2. provider settings import 추가
provider_import = (
    "from llm_provider_settings import "
    "get_chat_provider, set_chat_provider, reset_chat_provider, provider_label"
)

if provider_import not in s:
    s = provider_import + "\n" + s

# 3. provider command 함수 추가
marker = "# PHASE19_LLM_PROVIDER_SELECTION"

block = r'''

# PHASE19_LLM_PROVIDER_SELECTION
async def provider_command(update, context):
    """Telegram command: /provider [auto|gemini|clova|reset]"""
    chat = getattr(update, "effective_chat", None)
    message = getattr(update, "message", None)

    if chat is None or message is None:
        return

    chat_id = chat.id
    args = getattr(context, "args", []) or []

    if not args:
        current = get_chat_provider(chat_id)
        text = (
            "현재 채점 LLM Provider: " + provider_label(current) + "\n\n"
            "사용 가능한 명령:\n"
            "/provider auto   - Gemini 우선, 실패 시 Clova fallback\n"
            "/provider gemini - Gemini만 사용\n"
            "/provider clova  - Clova만 사용\n"
            "/provider reset  - 기본값으로 초기화"
        )
        await message.reply_text(text)
        return

    value = str(args[0]).strip().lower()

    if value in ("reset", "default"):
        current = reset_chat_provider(chat_id)
        await message.reply_text(
            "LLM Provider 설정을 기본값으로 초기화했습니다.\n"
            "현재 Provider: " + provider_label(current)
        )
        return

    try:
        current = set_chat_provider(chat_id, value)
    except Exception:
        await message.reply_text(
            "지원하지 않는 Provider입니다.\n"
            "사용 가능: auto, gemini, clova\n\n"
            "예:\n"
            "/provider auto\n"
            "/provider gemini\n"
            "/provider clova"
        )
        return

    await message.reply_text(
        "LLM Provider를 변경했습니다.\n"
        "현재 Provider: " + provider_label(current)
    )
'''

if marker not in s:
    # main 함수 앞에 넣는 것을 우선 시도
    m = re.search(r"^def\s+main\s*\(", s, flags=re.M)
    if m:
        s = s[:m.start()] + block + "\n\n" + s[m.start():]
    else:
        s = s.rstrip() + block + "\n"

# 4. handler 등록
if 'CommandHandler("provider", provider_command)' not in s and "CommandHandler('provider', provider_command)" not in s:
    # 기존 add_handler 호출을 찾아서 같은 application 변수에 등록
    m = re.search(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)\.add_handler\(", s, flags=re.M)

    if not m:
        path.write_text(s, encoding="utf-8")
        raise SystemExit(
            "provider_command 함수는 추가했지만 add_handler 위치를 자동으로 찾지 못했습니다. "
            "bot.py에서 application.add_handler(CommandHandler(\"provider\", provider_command))를 직접 추가하세요."
        )

    indent = m.group(1)
    app_var = m.group(2)
    insert = f'{indent}{app_var}.add_handler(CommandHandler("provider", provider_command))\n'
    s = s[:m.start()] + insert + s[m.start():]

path.write_text(s, encoding="utf-8")
print("bot.py provider command patched")
