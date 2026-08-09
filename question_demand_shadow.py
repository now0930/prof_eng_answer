from __future__ import annotations
import hashlib
import json
import tempfile
from pathlib import Path


import os
from typing import Any, Callable


QUESTION_DEMAND_SHADOW_VERSION = "question_demand_shadow_v1"
QUESTION_DEMAND_SHADOW_FILE = "question_demand_shadow.json"
DEFAULT_MAX_DEMANDS = 12
QUESTION_DEMAND_CACHE_VERSION = "question_demand_authoritative_cache_v1"
QUESTION_DEMAND_PROMPT_CONTRACT_VERSION = "question_demand_prompt_v1"
QUESTION_DEMAND_CANONICAL_DIR = Path(__file__).resolve().parent / "calibration" / "question_demand_contracts"
QUESTION_DEMAND_RUNTIME_CACHE_DIR = Path(__file__).resolve().parent / "data" / "question_contract_cache" / "question_demand"


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



def _question_demand_question_sha256(question_text: str) -> str:
    question = str(question_text or "").strip()
    return hashlib.sha256(question.encode("utf-8")).hexdigest()


def question_demand_cache_key(
    question_text: str,
    *,
    max_demands: int = DEFAULT_MAX_DEMANDS,
) -> str:
    identity = {
        "cache_version": QUESTION_DEMAND_CACHE_VERSION,
        "prompt_contract_version": QUESTION_DEMAND_PROMPT_CONTRACT_VERSION,
        "question_sha256": _question_demand_question_sha256(question_text),
        "max_demands": int(max_demands),
    }
    encoded = json.dumps(
        identity,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _question_demand_cache_path(
    cache_dir: str | Path,
    cache_key: str,
) -> Path:
    return Path(cache_dir) / f"{cache_key}.json"


def _read_question_demand_cache_entry(
    cache_path: Path,
    *,
    question_text: str,
    max_demands: int,
    allowed_confirmation_statuses: set[str],
) -> dict[str, Any] | None:
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return None

        expected_key = question_demand_cache_key(
            question_text,
            max_demands=max_demands,
        )
        expected_qsha = _question_demand_question_sha256(question_text)

        if payload.get("cache_version") != QUESTION_DEMAND_CACHE_VERSION:
            return None
        if (
            payload.get("prompt_contract_version")
            != QUESTION_DEMAND_PROMPT_CONTRACT_VERSION
        ):
            return None
        if payload.get("cache_key") != expected_key:
            return None
        if payload.get("question_sha256") != expected_qsha:
            return None
        if int(payload.get("max_demands", -1)) != int(max_demands):
            return None

        confirmation_status = str(
            payload.get("confirmation_status") or ""
        )
        if confirmation_status not in allowed_confirmation_statuses:
            return None

        demands = _normalize_demands(
            {"demands": payload.get("demands")},
            max_demands=max_demands,
        )
        return {
            "cache_key": expected_key,
            "confirmation_status": confirmation_status,
            "demands": demands,
            "source": str(payload.get("source") or ""),
        }
    except Exception:
        return None


def _load_question_demand_authoritative_cache(
    question_text: str,
    *,
    max_demands: int,
) -> dict[str, Any] | None:
    cache_key = question_demand_cache_key(
        question_text,
        max_demands=max_demands,
    )

    canonical_path = _question_demand_cache_path(
        QUESTION_DEMAND_CANONICAL_DIR,
        cache_key,
    )
    canonical = _read_question_demand_cache_entry(
        canonical_path,
        question_text=question_text,
        max_demands=max_demands,
        allowed_confirmation_statuses={"confirmed"},
    )
    if canonical is not None:
        canonical["cache_source"] = "confirmed_canonical"
        canonical["cache_path"] = str(canonical_path)
        return canonical

    runtime_path = _question_demand_cache_path(
        QUESTION_DEMAND_RUNTIME_CACHE_DIR,
        cache_key,
    )
    runtime = _read_question_demand_cache_entry(
        runtime_path,
        question_text=question_text,
        max_demands=max_demands,
        allowed_confirmation_statuses={"pending", "confirmed"},
    )
    if runtime is not None:
        runtime["cache_source"] = "runtime_cache"
        runtime["cache_path"] = str(runtime_path)
        return runtime

    return None


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_name = ""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            tmp_name = handle.name
            json.dump(
                payload,
                handle,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            handle.write("\n")
            handle.flush()

        Path(tmp_name).replace(path)
    finally:
        if tmp_name:
            tmp_path = Path(tmp_name)
            if tmp_path.exists():
                tmp_path.unlink()


def _write_pending_question_demand_cache(
    question_text: str,
    demands: list[dict[str, str]],
    *,
    max_demands: int,
) -> dict[str, Any]:
    cache_key = question_demand_cache_key(
        question_text,
        max_demands=max_demands,
    )
    cache_path = _question_demand_cache_path(
        QUESTION_DEMAND_RUNTIME_CACHE_DIR,
        cache_key,
    )

    entry = {
        "cache_version": QUESTION_DEMAND_CACHE_VERSION,
        "prompt_contract_version": QUESTION_DEMAND_PROMPT_CONTRACT_VERSION,
        "cache_key": cache_key,
        "question_sha256": _question_demand_question_sha256(question_text),
        "max_demands": int(max_demands),
        "confirmation_status": "pending",
        "source": "first_successful_question_demand_llm_result",
        "demands": demands,
    }
    try:
        _write_json_atomic(cache_path, entry)
    except OSError as exc:
        return {
            "cache_key": cache_key,
            "cache_source": "runtime_cache_write_failed",
            "cache_path": str(cache_path),
            "confirmation_status": "pending_unpersisted",
            "cache_write_status": "failed",
            "cache_write_error": f"{type(exc).__name__}: {exc}",
        }

    return {
        "cache_key": cache_key,
        "cache_source": "runtime_cache_write",
        "cache_path": str(cache_path),
        "confirmation_status": "pending",
        "cache_write_status": "written",
        "cache_write_error": "",
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

    cached = _load_question_demand_authoritative_cache(
        question,
        max_demands=max_demands,
    )
    if cached is not None:
        result = _base_result(
            enabled=True,
            status="ok",
            ok=True,
            demands=cached["demands"],
        )
        result["engine"] = "question_demand_authoritative_cache"
        result["cache_key"] = cached["cache_key"]
        result["cache_source"] = cached["cache_source"]
        result["cache_path"] = cached["cache_path"]
        result["confirmation_status"] = cached["confirmation_status"]
        return result

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
    cache_metadata = _write_pending_question_demand_cache(
        question,
        demands,
        max_demands=max_demands,
    )
    result.update(cache_metadata)
    result["engine"] = "ollama_json_via_logic_llm_verifier"
    return result
