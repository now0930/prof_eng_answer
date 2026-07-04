#!/usr/bin/env python3
"""
Gemini client for topic-pack review.

This module is intentionally separate from grading providers. It is used for
rubric/topic authoring review only, so changing topic review settings does not
change runtime grading behavior.

Environment fallback order:

  API KEY:
    TOPIC_REVIEW_GEMINI_API_KEY
    GEMINI_API_KEY
    GOOGLE_API_KEY
    GOOGLE_GENERATIVE_AI_API_KEY

  MODEL:
    TOPIC_REVIEW_GEMINI_MODEL
    GEMINI_MODEL
    gemini-2.5-flash

  TIMEOUT:
    TOPIC_REVIEW_GEMINI_TIMEOUT
    GEMINI_TIMEOUT
    180
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TopicReviewLLMSettings:
    provider: str
    model: str
    timeout: int
    temperature: float
    max_output_tokens: int
    response_mime_type: str


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _api_key() -> str:
    return (
        os.getenv("TOPIC_REVIEW_GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
        or ""
    ).strip()


def get_topic_review_llm_settings(
    *,
    model: str | None = None,
    timeout: int | None = None,
    temperature: float | None = None,
    max_output_tokens: int | None = None,
) -> TopicReviewLLMSettings:
    resolved_model = (
        model
        or os.getenv("TOPIC_REVIEW_GEMINI_MODEL")
        or os.getenv("GEMINI_MODEL")
        or "gemini-2.5-flash"
    ).strip()

    resolved_timeout = (
        timeout
        if timeout is not None
        else _int_env("TOPIC_REVIEW_GEMINI_TIMEOUT", _int_env("GEMINI_TIMEOUT", 180))
    )

    resolved_temperature = (
        temperature
        if temperature is not None
        else _float_env("TOPIC_REVIEW_GEMINI_TEMPERATURE", 0.1)
    )

    resolved_max_output_tokens = (
        max_output_tokens
        if max_output_tokens is not None
        else _int_env("TOPIC_REVIEW_GEMINI_MAX_OUTPUT_TOKENS", 8192)
    )

    return TopicReviewLLMSettings(
        provider="gemini",
        model=resolved_model,
        timeout=resolved_timeout,
        temperature=resolved_temperature,
        max_output_tokens=resolved_max_output_tokens,
        response_mime_type="application/json",
    )


def gemini_generate(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
    timeout: int | None = None,
    temperature: float | None = None,
    max_output_tokens: int | None = None,
) -> dict[str, Any]:
    api_key = _api_key()
    if not api_key:
        raise RuntimeError(
            "TOPIC_REVIEW_GEMINI_API_KEY/GEMINI_API_KEY/GOOGLE_API_KEY/"
            "GOOGLE_GENERATIVE_AI_API_KEY is empty"
        )

    settings = get_topic_review_llm_settings(
        model=model,
        timeout=timeout,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    model_part = urllib.parse.quote(settings.model, safe="")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_part}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    )

    payload = {
        "systemInstruction": {
            "parts": [
                {
                    "text": system_prompt,
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_prompt,
                    }
                ],
            }
        ],
        "generationConfig": {
            "temperature": settings.temperature,
            "maxOutputTokens": settings.max_output_tokens,
            "responseMimeType": settings.response_mime_type,
        },
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=settings.timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini HTTPError {exc.code}: {detail[:4000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Gemini connection failed: {exc}") from exc

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini returned invalid JSON envelope: {body[:4000]}") from exc

    content = _extract_gemini_text(data)

    return {
        "provider": settings.provider,
        "model": settings.model,
        "timeout": settings.timeout,
        "temperature": settings.temperature,
        "max_output_tokens": settings.max_output_tokens,
        "response_mime_type": settings.response_mime_type,
        "content": content,
        "raw_response": data,
    }


def _extract_gemini_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return ""

    first = candidates[0]
    if not isinstance(first, dict):
        return ""

    content = first.get("content")
    if not isinstance(content, dict):
        return ""

    parts = content.get("parts")
    if not isinstance(parts, list):
        return ""

    texts: list[str] = []
    for part in parts:
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            texts.append(part["text"])

    return "\n".join(texts).strip()


def extract_json_object(text: str) -> tuple[dict[str, Any] | None, str | None]:
    stripped = text.strip()

    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    candidates = [stripped]

    first = stripped.find("{")
    last = stripped.rfind("}")
    if first >= 0 and last > first:
        candidates.append(stripped[first : last + 1])

    last_error = "no JSON object found"
    for candidate in candidates:
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = str(exc)
            continue

        if isinstance(data, dict):
            return data, None

        last_error = "parsed JSON is not an object"

    return None, last_error
