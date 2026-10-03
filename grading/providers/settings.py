#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, Any


VALID_PROVIDERS = {"auto", "gemini", "clova"}

PROVIDER_ALIASES = {
    "auto": "auto",
    "fallback": "auto",
    "default": "auto",

    "gemini": "gemini",
    "google": "gemini",

    "clova": "clova",
    "naver": "clova",
    "naver-clova": "clova",
    "naver_clova": "clova",
}


def _settings_path() -> Path:
    return Path(os.getenv(
        "LLM_PROVIDER_SETTINGS_FILE",
        "data/user_settings/llm_provider_settings.json"
    ))


def normalize_provider(value: str) -> str:
    v = str(value or "").strip().lower()
    provider = PROVIDER_ALIASES.get(v)

    if provider not in VALID_PROVIDERS:
        raise ValueError(f"invalid provider: {value}")

    return provider


def get_default_provider() -> str:
    try:
        return normalize_provider(os.getenv("LLM_PROVIDER", "auto"))
    except Exception:
        return "auto"


def _load() -> Dict[str, Any]:
    path = _settings_path()

    if not path.exists():
        return {
            "schema_version": "llm_provider_settings_v1",
            "chat_providers": {}
        }

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "schema_version": "llm_provider_settings_v1",
            "chat_providers": {}
        }


def _save(data: Dict[str, Any]) -> None:
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def get_chat_provider(chat_id) -> str:
    data = _load()
    chat_key = str(chat_id)
    provider = data.get("chat_providers", {}).get(chat_key)

    if provider:
        try:
            return normalize_provider(provider)
        except Exception:
            pass

    return get_default_provider()


def set_chat_provider(chat_id, provider: str) -> str:
    provider = normalize_provider(provider)

    data = _load()
    data.setdefault("schema_version", "llm_provider_settings_v1")
    data.setdefault("chat_providers", {})
    data["chat_providers"][str(chat_id)] = provider

    _save(data)
    return provider


def reset_chat_provider(chat_id) -> str:
    data = _load()
    data.setdefault("chat_providers", {})
    data["chat_providers"].pop(str(chat_id), None)
    _save(data)

    return get_default_provider()


def provider_label(provider: str) -> str:
    provider = normalize_provider(provider)

    labels = {
        "auto": "자동 선택(auto: Gemini 우선, 실패 시 Clova fallback)",
        "gemini": "Gemini",
        "clova": "Naver CLOVA"
    }

    return labels.get(provider, provider)
