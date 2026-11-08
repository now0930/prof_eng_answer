"""Credential isolation for opt-in, live *validation* work.

Production Telegram grading keeps GEMINI_API_KEY/CLOVA_API_KEY unchanged.
Validation never silently falls back to those production credentials.
No secret values should be logged or persisted.
"""
from __future__ import annotations

import os
from typing import Mapping


PRODUCTION_CREDENTIAL_KEYS = (
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_GENERATIVE_AI_API_KEY",
    "CLOVA_API_KEY",
    "CLOVA_APIGW_API_KEY",
)
VALIDATION_CREDENTIAL_KEYS = (
    "VALIDATION_GEMINI_API_KEY",
    "VALIDATION_CLOVA_API_KEY",
    "VALIDATION_CLOVA_APIGW_API_KEY",
)


class ValidationCredentialError(ValueError):
    """Validation is missing explicit authorization or isolated credentials."""


def _source(environ: Mapping[str, str] | None) -> Mapping[str, str]:
    return os.environ if environ is None else environ


def live_validation_enabled(environ: Mapping[str, str] | None = None) -> bool:
    return _source(environ).get("VALIDATION_LIVE_API", "0").strip() == "1"


def require_validation_key(
    provider: str, environ: Mapping[str, str] | None = None
) -> str:
    """Require opt-in and an independent credential; never use grader keys."""
    env = _source(environ)
    if not live_validation_enabled(env):
        raise ValidationCredentialError("validation_live_api_disabled")
    names = {
        "gemini": "VALIDATION_GEMINI_API_KEY",
        "clova": "VALIDATION_CLOVA_API_KEY",
    }
    if provider not in names:
        raise ValidationCredentialError("unsupported_validation_provider")
    key = str(env.get(names[provider]) or "").strip()
    if not key:
        raise ValidationCredentialError(f"missing_{names[provider].lower()}")
    if any(key == str(env.get(name) or "").strip() for name in PRODUCTION_CREDENTIAL_KEYS):
        raise ValidationCredentialError("validation_credential_reuses_production_key")
    return key


def validation_provider_environment(
    environ: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Map only dedicated validation keys to legacy provider transports.

    The ordinary production variable names are deliberately cleared first,
    including alias/fallback keys. Disabled mode is offline even if the
    process inherited production and validation secrets.
    """
    source = _source(environ)
    output = dict(source)
    for name in PRODUCTION_CREDENTIAL_KEYS:
        output.pop(name, None)
    output["VALIDATION_CREDENTIAL_CONTEXT"] = "isolated"
    if not live_validation_enabled(source):
        return output
    if source.get("VALIDATION_GEMINI_API_KEY"):
        output["GEMINI_API_KEY"] = require_validation_key("gemini", source)
    if source.get("VALIDATION_CLOVA_API_KEY"):
        output["CLOVA_API_KEY"] = require_validation_key("clova", source)
    legacy = str(source.get("VALIDATION_CLOVA_APIGW_API_KEY") or "").strip()
    if legacy:
        if not source.get("VALIDATION_CLOVA_API_KEY"):
            raise ValidationCredentialError("validation_clova_legacy_without_primary")
        if any(legacy == str(source.get(name) or "").strip()
               for name in PRODUCTION_CREDENTIAL_KEYS):
            raise ValidationCredentialError("validation_credential_reuses_production_key")
        output["CLOVA_APIGW_API_KEY"] = legacy
    return output
