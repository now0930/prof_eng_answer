#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from gemini_grader import gemini_semantic_grade as _gemini_semantic_grade
from clova_grader import clova_semantic_grade as _clova_semantic_grade
from llm_provider_settings import get_chat_provider, get_default_provider, normalize_provider


def _settings_path() -> Path:
    return Path(os.getenv(
        "LLM_PROVIDER_SETTINGS_FILE",
        "data/user_settings/llm_provider_settings.json"
    ))


def _provider_from_saved_single_chat() -> Optional[str]:
    """
    grading_agents.py에서 chat_id를 넘기지 않는 경우를 위한 보완.
    현재는 1인/1방 운영이므로 저장된 chat provider가 하나뿐이면 그 값을 사용한다.
    """
    path = _settings_path()
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        providers = data.get("chat_providers", {})
        if isinstance(providers, dict) and len(providers) == 1:
            return normalize_provider(next(iter(providers.values())))
    except Exception:
        return None

    return None


def _extract_chat_id(args, kwargs) -> Optional[str]:
    for key in ("chat_id", "telegram_chat_id", "tg_chat_id"):
        if kwargs.get(key):
            return str(kwargs.get(key))

    # dict 형태 인자가 있으면 chat_id를 찾아본다.
    for item in list(args) + list(kwargs.values()):
        if isinstance(item, dict):
            for key in ("chat_id", "telegram_chat_id", "tg_chat_id"):
                if item.get(key):
                    return str(item.get(key))

    return None


def _select_provider(args, kwargs) -> str:
    explicit = kwargs.pop("llm_provider", None) or kwargs.pop("provider", None)
    if explicit:
        return normalize_provider(explicit)

    chat_id = _extract_chat_id(args, kwargs)
    if chat_id:
        return get_chat_provider(chat_id)

    saved = _provider_from_saved_single_chat()
    if saved:
        return saved

    return get_default_provider()


def _is_success(result: Any) -> bool:
    if not isinstance(result, dict):
        return False

    if result.get("ok") is False:
        return False

    if result.get("error"):
        return False

    return True


def _tag(result: Any, provider: str) -> Any:
    if isinstance(result, dict):
        result.setdefault("llm_provider", provider)
    return result


def provider_semantic_grade(*args, **kwargs) -> Dict[str, Any]:
    provider = _select_provider(args, kwargs)

    if provider == "gemini":
        try:
            return _tag(_gemini_semantic_grade(*args, **kwargs), "gemini")
        except Exception as e:
            return {
                "ok": False,
                "llm_provider": "gemini",
                "error": str(e),
            }

    if provider == "clova":
        return _tag(_clova_semantic_grade(*args, **kwargs), "clova")

    # auto: Gemini 우선, 실패 시 CLOVA fallback
    try:
        gemini_result = _tag(_gemini_semantic_grade(*args, **kwargs), "gemini")
        if _is_success(gemini_result):
            return gemini_result

        clova_result = _tag(_clova_semantic_grade(*args, **kwargs), "clova")
        if isinstance(clova_result, dict):
            clova_result.setdefault("fallback_from", "gemini")
            clova_result.setdefault("gemini_error", gemini_result.get("error") if isinstance(gemini_result, dict) else None)
        return clova_result

    except Exception as e:
        clova_result = _tag(_clova_semantic_grade(*args, **kwargs), "clova")
        if isinstance(clova_result, dict):
            clova_result.setdefault("fallback_from", "gemini_exception")
            clova_result.setdefault("gemini_error", str(e))
        return clova_result
