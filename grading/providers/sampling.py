from __future__ import annotations

import hashlib
import json
from typing import Any


SAMPLING_CONTRACT_VERSION = (
    "score_affecting_llm_sampling_v1"
)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def build_llm_request_contract(
    *,
    provider: str,
    model: str,
    prompt: str,
    requested_sampling: dict[str, Any],
    applied_sampling: dict[str, Any],
    unsupported_settings: list[str] | None = None,
) -> dict[str, Any]:
    prompt_hash = _sha256_text(
        str(prompt or "")
    )

    requested = dict(
        requested_sampling or {}
    )
    applied = dict(
        applied_sampling or {}
    )

    unsupported = sorted(
        {
            str(item).strip()
            for item in (
                unsupported_settings or []
            )
            if str(item).strip()
        }
    )

    identity = {
        "version": SAMPLING_CONTRACT_VERSION,
        "provider": str(
            provider or ""
        ).strip().lower(),
        "model": str(
            model or ""
        ).strip(),
        "prompt_hash": prompt_hash,
        "applied_sampling": applied,
    }

    return {
        **identity,
        "request_hash": _sha256_text(
            _canonical_json(identity)
        ),
        "requested_sampling": requested,
        "unsupported_settings": unsupported,
    }
