"""JSON-only Gemini transport for score-neutral Fact interpretation requests."""
from __future__ import annotations

import json
import os
import io
import re
import subprocess
import urllib.error
import urllib.request


class SemanticProviderError(RuntimeError):
    """Safe, content-free provider failure for private answer handling."""


class GeminiSemanticProvider:
    def __init__(self, *, model: str, api_key: str | None = None,
                 timeout: float = 90.0, urlopen=None):
        if not isinstance(model, str) or not model.strip() or "/" in model or ":" in model:
            raise ValueError("invalid model name")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("invalid provider timeout")
        self.model = model
        self._api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY", "")
        self.timeout = timeout
        self._urlopen = urlopen or urllib.request.urlopen

    def __call__(self, request: dict) -> dict:
        if not self._api_key:
            raise SemanticProviderError("missing_api_key")
        if not isinstance(request, dict) or request.get("schema_version") not in {
            "unresolved-semantic-assist-v1", "semantic-review-v1",
        }:
            raise SemanticProviderError("unsupported_request")
        if request["schema_version"] == "unresolved-semantic-assist-v1":
            payload = {
                "question": request["question"], "excerpt": request["excerpt"],
                "facts": [{"fact_id": fact["fact_id"], "statement": fact["statement"],
                           "relation": fact["relation"]} for fact in request["facts"]],
            }
        else:
            fact = request["fact"]
            payload = {
                "question": request["question"], "excerpt": request["excerpt"],
                "fact": {"fact_id": fact["fact_id"], "statement": fact["statement"],
                         "relation": fact["relation"]},
            }
        prompt = request["instruction"] + "\n\nINPUT_JSON_DATA:\n" + json.dumps(
            payload, ensure_ascii=False, sort_keys=True,
        )
        body = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": 8192,
                                 "responseMimeType": "application/json"},
        }, ensure_ascii=False).encode("utf-8")
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self.model}:generateContent")
        http_request = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json", "x-goog-api-key": self._api_key},
        )
        try:
            with self._urlopen(http_request, timeout=self.timeout) as response:
                outer = json.load(response)
            parts = outer["candidates"][0]["content"]["parts"]
            raw = "".join(part.get("text", "") for part in parts if not part.get("thought"))
            result = json.loads(raw)
            if not isinstance(result, dict):
                raise ValueError("provider response is not an object")
            return result
        except urllib.error.HTTPError as error:
            raise SemanticProviderError(f"http_{error.code}") from None
        except SemanticProviderError:
            raise
        except Exception as error:
            # No provider message: it may contain credentials or private text.
            raise SemanticProviderError(type(error).__name__) from None


_DOCKER_WORKER = r'''
import json, os, sys, urllib.request, urllib.error
payload = json.load(sys.stdin)
key = os.environ.get("GEMINI_API_KEY")
if not key:
    print(json.dumps({"ok": False, "error_type": "missing_api_key"})); sys.exit(2)
req = urllib.request.Request(payload["url"],
    data=json.dumps(payload["body"]).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-goog-api-key": key})
try:
    with urllib.request.urlopen(req, timeout=payload["timeout"]) as response:
        result = json.load(response)
    print(json.dumps({"ok": True, "response": result}, ensure_ascii=False))
except urllib.error.HTTPError as error:
    print(json.dumps({"ok": False, "error_type": "http_error", "status": error.code})); sys.exit(2)
except Exception as error:
    print(json.dumps({"ok": False, "error_type": type(error).__name__})); sys.exit(2)
'''


def docker_urlopen(container: str):
    """Keep API credentials inside an existing, authorized provider container."""
    if not isinstance(container, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", container):
        raise ValueError("invalid container name")

    class _Response:
        def __init__(self, data):
            self._data = io.BytesIO(data)
        def __enter__(self):
            return self._data
        def __exit__(self, *_):
            self._data.close()

    def call(http_request, *, timeout):
        try:
            payload = {"url": http_request.full_url,
                       "body": json.loads(http_request.data), "timeout": timeout}
            result = subprocess.run(
                ["docker", "exec", "-i", container, "python3", "-c", _DOCKER_WORKER],
                input=json.dumps(payload, ensure_ascii=False), text=True,
                capture_output=True, timeout=timeout + 15, check=False,
            )
            reply = json.loads(result.stdout)
            if result.returncode or reply.get("ok") is not True:
                raise SemanticProviderError(
                    f"container_{reply.get('error_type', 'request_failed')}"
                    + (f"_{reply['status']}" if "status" in reply else "")
                )
            return _Response(json.dumps(reply["response"], ensure_ascii=False).encode())
        except SemanticProviderError:
            raise
        except Exception as error:
            raise SemanticProviderError(type(error).__name__) from None
    return call
