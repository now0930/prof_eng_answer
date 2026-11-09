"""Fail-closed API call and token budgets for explicit live validation runs.

Only aggregate counters and provider/model names are persisted. Prompts, answers,
headers, credentials, response bodies, and case text are never written here.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sqlite3
import threading
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import uuid


class ValidationBudgetExceeded(RuntimeError):
    """A live validation request would exceed its explicit budget."""


def _positive_int(name: str) -> int:
    raw = str(os.getenv(name, "")).strip()
    if not raw or not raw.isdecimal() or int(raw) <= 0:
        raise ValidationBudgetExceeded(f"invalid_or_missing_{name.lower()}")
    return int(raw)


def _db_path() -> Path:
    raw = str(os.getenv("VALIDATION_API_BUDGET_DB", "")).strip()
    if not raw:
        raise ValidationBudgetExceeded("validation_api_budget_db_missing")
    path = Path(raw).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect(path: Path | None = None) -> sqlite3.Connection:
    database_path = path or _db_path()
    connection = sqlite3.connect(database_path, timeout=30, isolation_level=None)
    try:
        database_path.chmod(0o600)
    except OSError:
        connection.close()
        raise ValidationBudgetExceeded("validation_budget_permissions_invalid") from None
    connection.execute("PRAGMA busy_timeout=30000")
    connection.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            grades INTEGER NOT NULL DEFAULT 0,
            http_calls INTEGER NOT NULL DEFAULT 0,
            actual_tokens INTEGER NOT NULL DEFAULT 0,
            reserved_tokens INTEGER NOT NULL DEFAULT 0,
            input_tokens INTEGER NOT NULL DEFAULT 0,
            output_tokens INTEGER NOT NULL DEFAULT 0,
            thought_tokens INTEGER NOT NULL DEFAULT 0,
            usage_unknown_calls INTEGER NOT NULL DEFAULT 0,
            over_budget INTEGER NOT NULL DEFAULT 0
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            http_calls INTEGER NOT NULL DEFAULT 0,
            actual_tokens INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(provider, model)
        )
    """)
    connection.execute("INSERT OR IGNORE INTO budget(id) VALUES (1)")
    return connection


def enabled() -> bool:
    return bool(str(os.getenv("VALIDATION_API_BUDGET_DB", "")).strip())


def reserve_grade() -> None:
    if not enabled():
        return
    maximum = _positive_int("VALIDATION_MAX_LIVE_GRADES")
    connection = _connect()
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT grades FROM budget WHERE id=1").fetchone()
        if row[0] >= maximum:
            raise ValidationBudgetExceeded("validation_grade_budget_exceeded")
        connection.execute("UPDATE budget SET grades=grades+1 WHERE id=1")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def reserve_http(provider: str, model: str) -> None:
    maximum = _positive_int("VALIDATION_MAX_HTTP_CALLS")
    connection = _connect()
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT http_calls FROM budget WHERE id=1").fetchone()
        if row[0] >= maximum:
            raise ValidationBudgetExceeded("validation_http_call_budget_exceeded")
        connection.execute("UPDATE budget SET http_calls=http_calls+1 WHERE id=1")
        connection.execute("""
            INSERT INTO providers(provider, model, http_calls)
            VALUES (?, ?, 1)
            ON CONFLICT(provider, model) DO UPDATE SET http_calls=http_calls+1
        """, (provider, model))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def reserve_tokens(token_count: int) -> str:
    if isinstance(token_count, bool) or not isinstance(token_count, int) or token_count < 0:
        raise ValidationBudgetExceeded("invalid_provider_token_count")
    maximum = _positive_int("VALIDATION_MAX_TOTAL_TOKENS")
    connection = _connect()
    reservation_id = uuid.uuid4().hex
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT actual_tokens, reserved_tokens FROM budget WHERE id=1"
        ).fetchone()
        if row[0] + row[1] + token_count > maximum:
            raise ValidationBudgetExceeded("validation_token_budget_exceeded_before_request")
        connection.execute(
            "UPDATE budget SET reserved_tokens=reserved_tokens+? WHERE id=1",
            (token_count,),
        )
        connection.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                reserved_tokens INTEGER NOT NULL,
                settled INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.execute(
            "INSERT INTO reservations(reservation_id, provider, model, reserved_tokens) VALUES (?, ?, ?, ?)",
            (reservation_id, "gemini", "unknown", token_count),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return reservation_id


def reserve_generation_request(provider: str, model: str, token_count: int) -> str:
    """Atomically reserve one generation HTTP attempt and its token ceiling."""
    if isinstance(token_count, bool) or not isinstance(token_count, int) or token_count < 0:
        raise ValidationBudgetExceeded("invalid_provider_token_count")
    max_http = _positive_int("VALIDATION_MAX_HTTP_CALLS")
    max_tokens = _positive_int("VALIDATION_MAX_TOTAL_TOKENS")
    connection = _connect()
    reservation_id = uuid.uuid4().hex
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT http_calls,actual_tokens,reserved_tokens FROM budget WHERE id=1"
        ).fetchone()
        if row[0] >= max_http:
            raise ValidationBudgetExceeded("validation_http_call_budget_exceeded")
        if row[1] + row[2] + token_count > max_tokens:
            raise ValidationBudgetExceeded("validation_token_budget_exceeded_before_request")
        connection.execute("""
            UPDATE budget SET http_calls=http_calls+1,reserved_tokens=reserved_tokens+?
            WHERE id=1
        """, (token_count,))
        connection.execute("""
            INSERT INTO providers(provider,model,http_calls) VALUES (?,?,1)
            ON CONFLICT(provider,model) DO UPDATE SET http_calls=http_calls+1
        """, (provider, model))
        connection.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                reserved_tokens INTEGER NOT NULL,
                settled INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.execute(
            "INSERT INTO reservations(reservation_id,provider,model,reserved_tokens) VALUES (?,?,?,?)",
            (reservation_id, provider, model, token_count),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return reservation_id


def update_reservation_identity(reservation_id: str, provider: str, model: str) -> None:
    connection = _connect()
    try:
        connection.execute(
            "UPDATE reservations SET provider=?, model=? WHERE reservation_id=?",
            (provider, model, reservation_id),
        )
    finally:
        connection.close()


def _usage(payload: Any) -> dict[str, int] | None:
    if not isinstance(payload, dict):
        return None
    usage = payload.get("usageMetadata") or payload.get("usage")
    if not isinstance(usage, dict):
        return None
    aliases = {
        "input": ("promptTokenCount", "total_input_tokens", "input_tokens", "prompt_tokens"),
        "output": ("candidatesTokenCount", "total_output_tokens", "output_tokens", "completion_tokens"),
        "thought": ("thoughtsTokenCount", "total_thought_tokens", "thought_tokens"),
        "total": ("totalTokenCount", "total_tokens", "totalTokens"),
    }
    result: dict[str, int] = {}
    for target, names in aliases.items():
        for name in names:
            value = usage.get(name)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                result[target] = value
                break
    if "total" not in result:
        parts = result.get("input", 0) + result.get("output", 0) + result.get("thought", 0)
        if parts:
            result["total"] = parts
    return result if "total" in result else None


def settle_tokens(reservation_id: str, provider: str, model: str, payload: Any) -> None:
    usage = _usage(payload)
    connection = _connect()
    try:
        connection.execute("BEGIN IMMEDIATE")
        reservation = connection.execute(
            "SELECT reserved_tokens, settled FROM reservations WHERE reservation_id=?",
            (reservation_id,),
        ).fetchone()
        if not reservation or reservation[1]:
            connection.commit()
            return
        reserved = reservation[0]
        if usage is None:
            # Retain the full reservation when the provider omits usage. This is
            # conservative and avoids fabricating token counts.
            connection.execute("UPDATE budget SET usage_unknown_calls=usage_unknown_calls+1 WHERE id=1")
            connection.execute("UPDATE reservations SET settled=1 WHERE reservation_id=?", (reservation_id,))
            connection.commit()
            return
        actual = usage["total"]
        connection.execute("""
            UPDATE budget SET reserved_tokens=reserved_tokens-?, actual_tokens=actual_tokens+?,
                input_tokens=input_tokens+?, output_tokens=output_tokens+?,
                thought_tokens=thought_tokens+?, over_budget=CASE
                    WHEN actual_tokens + ? + (reserved_tokens - ?) > ? THEN 1 ELSE over_budget END
            WHERE id=1
        """, (
            reserved, actual, usage.get("input", 0), usage.get("output", 0),
            usage.get("thought", 0), actual, reserved,
            _positive_int("VALIDATION_MAX_TOTAL_TOKENS"),
        ))
        connection.execute("""
            UPDATE providers SET actual_tokens=actual_tokens+?
            WHERE provider=? AND model=?
        """, (actual, provider, model))
        connection.execute("UPDATE reservations SET settled=1 WHERE reservation_id=?", (reservation_id,))
        connection.commit()
        if actual > reserved:
            raise ValidationBudgetExceeded("provider_usage_exceeded_reserved_token_budget")
        if actual + _totals()["reserved_tokens"] > _positive_int("VALIDATION_MAX_TOTAL_TOKENS"):
            raise ValidationBudgetExceeded("validation_token_budget_exceeded_after_response")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _totals(path: Path | None = None) -> dict[str, int]:
    connection = _connect(path)
    try:
        row = connection.execute("""
            SELECT grades,http_calls,actual_tokens,reserved_tokens,input_tokens,
                output_tokens,thought_tokens,usage_unknown_calls,over_budget FROM budget WHERE id=1
        """).fetchone()
        keys = ("grades", "http_calls", "actual_tokens", "reserved_tokens", "input_tokens",
                "output_tokens", "thought_tokens", "usage_unknown_calls", "over_budget")
        return dict(zip(keys, row))
    finally:
        connection.close()


def summary(
    *,
    db_path: Path | None = None,
    max_live_grades: int | None = None,
    max_http_calls: int | None = None,
    max_total_tokens: int | None = None,
) -> dict[str, Any]:
    totals = _totals(db_path)
    connection = _connect(db_path)
    try:
        providers = [
            {"provider": row[0], "model": row[1], "http_calls": row[2], "reported_tokens": row[3]}
            for row in connection.execute(
                "SELECT provider,model,http_calls,actual_tokens FROM providers ORDER BY provider,model"
            )
        ]
    finally:
        connection.close()
    return {
        "schema_version": "validation_api_usage_v1",
        "budgets": {
            "max_live_grades": max_live_grades or _positive_int("VALIDATION_MAX_LIVE_GRADES"),
            "max_http_calls": max_http_calls or _positive_int("VALIDATION_MAX_HTTP_CALLS"),
            "max_total_tokens": max_total_tokens or _positive_int("VALIDATION_MAX_TOTAL_TOKENS"),
        },
        "totals": totals,
        "providers": providers,
        "token_usage_source": "provider_response_metadata_only",
        "case_text_or_credentials_persisted": False,
    }


def _request_parts(request: Any) -> tuple[str, bytes, dict[str, str]]:
    if isinstance(request, urllib.request.Request):
        url = request.full_url
        data = request.data or b""
        headers = {str(k).lower(): str(v) for k, v in request.header_items()}
    else:
        url, data, headers = str(request), b"", {}
    return url, data, headers


def _provider(url: str) -> str | None:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    if host == "generativelanguage.googleapis.com":
        return "gemini"
    if "clovastudio" in host or host.endswith("ntruss.com"):
        return "clova"
    return None


def _model(url: str, body: dict[str, Any]) -> str:
    match = re.search(r"/models/([^/:]+)", urllib.parse.urlsplit(url).path)
    return str(body.get("model") or (match.group(1) if match else "unknown"))


def _count_request_body(body: dict[str, Any], path: str) -> dict[str, Any]:
    if "/interactions" in path:
        value = body.get("input", "")
        if isinstance(value, str):
            contents: Any = [{"role": "user", "parts": [{"text": value}]}]
        elif isinstance(value, list):
            contents = value
        else:
            contents = [{"role": "user", "parts": [{"text": json.dumps(value, ensure_ascii=False)}]}]
        result: dict[str, Any] = {"contents": contents}
        if isinstance(body.get("tools"), list):
            result["tools"] = body["tools"]
        return result
    contents = body.get("contents")
    if not isinstance(contents, list):
        raise ValidationBudgetExceeded("validation_request_input_not_meterable")
    return {key: body[key] for key in ("contents", "systemInstruction", "tools", "toolConfig", "cachedContent") if key in body}


def _max_output_tokens(body: dict[str, Any]) -> int:
    configs = (body.get("generation_config"), body.get("generationConfig"))
    for config in configs:
        if isinstance(config, dict):
            value = config.get("max_output_tokens", config.get("maxOutputTokens"))
            if isinstance(value, int) and not isinstance(value, bool) and value > 0:
                return value
    raise ValidationBudgetExceeded("validation_request_output_limit_missing")


def _count_input_tokens(original_urlopen, request, provider: str, model: str, body: dict[str, Any], raw_url: str) -> int:
    if provider != "gemini":
        raise ValidationBudgetExceeded("provider_input_token_preflight_unsupported")
    path = urllib.parse.urlsplit(raw_url).path
    count_body = _count_request_body(body, path)
    _, _, headers = _request_parts(request)
    api_key = headers.get("x-goog-api-key") or headers.get("x-goog-api_key")
    if not api_key:
        raise ValidationBudgetExceeded("validation_provider_key_header_missing")
    parsed = urllib.parse.urlsplit(raw_url)
    count_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, f"/v1beta/models/{model}:countTokens", "", ""))
    count_payload = json.dumps(count_body, ensure_ascii=False).encode("utf-8")
    count_request = urllib.request.Request(
        count_url, data=count_payload,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key}, method="POST",
    )
    reserve_http("gemini", f"{model}:countTokens")
    try:
        response = original_urlopen(count_request, timeout=30)
        with response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        # Do not expose request/response bodies or credentials.
        raise ValidationBudgetExceeded("validation_token_count_preflight_failed") from None
    count = payload.get("totalTokens") if isinstance(payload, dict) else None
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ValidationBudgetExceeded("validation_token_count_missing")
    return count


class _UsageResponse:
    def __init__(self, response, reservation_id: str, provider: str, model: str):
        self._response = response
        self._reservation_id = reservation_id
        self._provider = provider
        self._model = model
        self._buffer = bytearray()
        self._settled = False

    def __getattr__(self, name):
        return getattr(self._response, name)

    def __enter__(self):
        self._response.__enter__()
        return self

    def __exit__(self, *args):
        return self._response.__exit__(*args)

    def read(self, size=-1):
        data = self._response.read(size)
        self._buffer.extend(data or b"")
        if not self._settled and (size is None or size < 0 or not data):
            self._settled = True
            try:
                payload = json.loads(self._buffer.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = None
            settle_tokens(self._reservation_id, self._provider, self._model, payload)
        return data


_install_lock = threading.Lock()


def install_http_meter() -> None:
    """Count every paid provider HTTP attempt and meter token use in response."""
    if not enabled():
        return
    with _install_lock:
        if getattr(urllib.request.urlopen, "_validation_api_meter", False) is True:
            return
        original_urlopen = urllib.request.urlopen

        def metered_urlopen(request, *args, **kwargs):
            raw_url, raw_body, _ = _request_parts(request)
            provider = _provider(raw_url)
            if provider is None:
                return original_urlopen(request, *args, **kwargs)
            # No provider token-count contract is available for this direct
            # CLOVA transport. Fail before sending anything rather than record
            # an invented input-token total.
            if provider == "clova":
                raise ValidationBudgetExceeded("clova_input_token_preflight_unsupported")
            path = urllib.parse.urlsplit(raw_url).path
            if provider == "gemini" and ":countTokens" in raw_url:
                reserve_http(provider, "countTokens")
                return original_urlopen(request, *args, **kwargs)
            if provider == "gemini" and not (":generateContent" in raw_url or path.endswith("/interactions")):
                # Reject before transport because this endpoint's token bounds
                # are not auditable through the implemented contract.
                raise ValidationBudgetExceeded("validation_provider_endpoint_not_meterable")
            body: dict[str, Any] = {}
            if raw_body:
                try:
                    body = json.loads(raw_body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise ValidationBudgetExceeded("validation_request_not_meterable") from None
            model = _model(raw_url, body)
            reservation_id = ""
            if provider == "gemini":
                input_tokens = _count_input_tokens(original_urlopen, request, provider, model, body, raw_url)
                output_cap = _max_output_tokens(body)
                reservation_id = reserve_generation_request(
                    provider, model, input_tokens + output_cap,
                )
            response = original_urlopen(request, *args, **kwargs)
            if reservation_id:
                return _UsageResponse(response, reservation_id, provider, model)
            return response

        metered_urlopen._validation_api_meter = True
        urllib.request.urlopen = metered_urlopen


def write_summary(path: Path, **kwargs) -> dict[str, Any]:
    data = summary(**kwargs)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return data
