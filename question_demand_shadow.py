from __future__ import annotations

import os
from typing import Any, Callable


QUESTION_DEMAND_SHADOW_VERSION = "question_demand_shadow_v1"
QUESTION_DEMAND_SHADOW_FILE = "question_demand_shadow.json"
DEFAULT_MAX_DEMANDS = 12


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    return str(raw).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def question_demand_shadow_enabled() -> bool:
    # Safe rollout: Stage 2 introduces the shadow path without changing
    # production routing unless the operator explicitly enables it.
    return _env_flag(
        "QUESTION_DEMAND_SHADOW_ENABLED",
        default=False,
    )


def build_question_demand_prompt(
    question_text: str,
    *,
    max_demands: int = DEFAULT_MAX_DEMANDS,
) -> str:
    question = str(question_text or "").strip()

    return f"""
You are a question-demand decomposition engine for the
Korean Professional Engineer examination.

Analyze ONLY the examination question below.
Do not use or infer anything from a student's answer.
Do not select a Topic, topic_id, rubric, score, or model answer.
Do not add technical facts that the question itself does not ask for.

Split the question into the smallest independently gradable
explicit demands while preserving:
- requested action: explain, compare, calculate, design, propose, etc.
- named target or technology
- conditions, constraints, comparison axes, and requested application context

Rules:
1. Keep only explicit or necessarily implied task demands.
2. Do not create duplicate demands.
3. Do not turn expected answer content into a new demand.
4. Return at most {int(max_demands)} demands.
5. Return JSON only. No markdown.

Required JSON shape:
{{
  "demands": [
    {{"id": "D1", "text": "요구사항"}},
    {{"id": "D2", "text": "요구사항"}}
  ]
}}

Question:
{question}
""".strip()


def _normalize_demands(
    payload: Any,
    *,
    max_demands: int = DEFAULT_MAX_DEMANDS,
) -> list[dict[str, str]]:
    if not isinstance(payload, dict):
        raise ValueError("LLM demand result root must be an object")

    raw_demands = payload.get("demands")
    if not isinstance(raw_demands, list):
        raise ValueError("LLM demand result must contain a demands list")

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()

    for item in raw_demands:
        if not isinstance(item, dict):
            continue

        text = str(item.get("text") or "").strip()
        if not text:
            continue

        collapsed = " ".join(text.split())
        dedupe_key = collapsed.casefold()

        if dedupe_key in seen:
            continue

        seen.add(dedupe_key)
        normalized.append(
            {
                "id": f"D{len(normalized) + 1}",
                "text": collapsed,
            }
        )

        if len(normalized) >= int(max_demands):
            break

    if not normalized:
        raise ValueError("LLM demand result contained no usable demand")

    return normalized


def _base_result(
    *,
    enabled: bool,
    status: str,
    ok: bool,
    demands: list[dict[str, str]] | None = None,
    error: str = "",
) -> dict[str, Any]:
    normalized = demands or []

    return {
        "version": QUESTION_DEMAND_SHADOW_VERSION,
        "shadow": True,
        "enabled": bool(enabled),
        "status": str(status),
        "ok": bool(ok),
        "mode": "question_demand_decomposition_only",
        "demands": normalized,
        "demand_count": len(normalized),
        "error": str(error or ""),
        "routing_effect": "none",
        "score_effect": "none",
        "student_answer_used": False,
        "topic_selection_performed": False,
    }


def extract_question_demands(
    question_text: str,
    *,
    llm_call: Callable[[str], Any] | None = None,
    max_demands: int = DEFAULT_MAX_DEMANDS,
    enabled: bool | None = None,
) -> dict[str, Any]:
    question = str(question_text or "").strip()

    if enabled is None:
        enabled = question_demand_shadow_enabled()

    if not enabled:
        return _base_result(
            enabled=False,
            status="disabled",
            ok=False,
            error="QUESTION_DEMAND_SHADOW_ENABLED is not enabled",
        )

    if not question:
        return _base_result(
            enabled=True,
            status="skipped",
            ok=False,
            error="question text is empty",
        )

    prompt = build_question_demand_prompt(
        question,
        max_demands=max_demands,
    )

    if llm_call is None:
        # Reuse the already-tested deterministic Ollama JSON transport.
        # Import lazily so disabled shadow mode has zero LLM dependency.
        from logic_llm_verifier import _call_ollama_json

        llm_call = _call_ollama_json

    try:
        payload = llm_call(prompt)
        demands = _normalize_demands(
            payload,
            max_demands=max_demands,
        )
    except Exception as exc:
        return _base_result(
            enabled=True,
            status="fallback",
            ok=False,
            error=f"question demand shadow failed: {exc!r}",
        )

    result = _base_result(
        enabled=True,
        status="ok",
        ok=True,
        demands=demands,
    )
    result["engine"] = "ollama_json_via_logic_llm_verifier"
    return result
