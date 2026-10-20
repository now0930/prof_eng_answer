"""Shared evidence-ID transport for bounded D/E model proposals."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .evidence_options import build_evidence_options, resolve_evidence_id


_CRITERION_SCHEMA = {
    "type": "object",
    "properties": {
        "criterion_id": {"type": "string", "enum": ["D1", "D2", "D3", "E1", "E2"]},
        "score": {"type": "number", "minimum": 0, "maximum": 2},
        "reason": {"type": "string"}, "topic_id": {"type": "string"},
        "evidence_id": {"type": ["string", "null"]},
    },
    "required": ["criterion_id", "score", "reason", "topic_id", "evidence_id"],
    "additionalProperties": False,
}
_QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "question_id": {"type": "string"}, "question": {"type": "string"},
        "topic_id": {"type": "string"}, "reason": {"type": "string"},
        "expected_elements": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "evidence_id": {"type": "string"},
    },
    "required": ["question_id", "question", "topic_id", "reason",
                 "expected_elements", "evidence_id"],
    "additionalProperties": False,
}
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "criteria": {"type": "array", "items": _CRITERION_SCHEMA, "minItems": 5, "maxItems": 5},
        "interview_questions": {"type": "array", "items": _QUESTION_SCHEMA, "maxItems": 3},
        "abc_observations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["criteria", "interview_questions", "abc_observations"],
    "additionalProperties": False,
}


class ModelOutputTruncated(RuntimeError):
    """The provider exhausted output tokens before completing JSON."""


class ModelOutputEmpty(RuntimeError):
    """The provider returned no JSON content."""


class ModelOutputIncomplete(RuntimeError):
    """An interaction did not complete; partial output is never a grade."""


class ProviderHTTPError(RuntimeError):
    """Expose HTTP status only, never a credential-bearing provider body."""

    def __init__(self, status: int):
        super().__init__(f"provider_http_{status}")


def provider_input(prompt: str) -> tuple[str, dict]:
    prompt_data = json.loads(prompt)
    options = build_evidence_options(prompt_data["answer"], prompt_data["requirements"])
    by_id = {item["evidence_id"]: item for item in options}
    prompt_data["instruction"] += (
        " 각 양수 점수와 면접 질문은 evidence_options의 evidence_id 하나를 선택하세요. "
        "0점은 evidence_id=null입니다. 원문 인용이나 위치를 새로 쓰지 마세요. "
        "서로 다른 양수 점수에는 서로 다른 evidence_id를 사용하세요. "
        "각 reason은 선택한 evidence_id의 인용문이 직접 뒷받침하는 내용만 설명하세요. "
        "인용문에 없는 절차·조건·지식을 다른 문장에서 추측해 보태지 마세요. "
        "가점에 쓸 서로 다른 근거가 부족하면 해당 항목은 0점으로 두세요."
    )
    prompt_data["schema"] = RESPONSE_SCHEMA
    prompt_data["evidence_options"] = [
        {key: item[key] for key in ("evidence_id", "quote", "topic_ids")}
        for item in options
    ]
    return json.dumps(prompt_data, ensure_ascii=False, separators=(",", ":")), by_id


def resolved_response(proposal: dict, by_id: dict) -> str:
    if isinstance(proposal, dict):
        if isinstance(proposal.get("criteria"), list):
            proposal["criteria"] = [resolve_evidence_id(
                row, by_id, zero_score=row.get("score") == 0) for row in proposal["criteria"]]
        if isinstance(proposal.get("interview_questions"), list):
            proposal["interview_questions"] = [resolve_evidence_id(row, by_id)
                                               for row in proposal["interview_questions"]]
    return json.dumps(proposal, ensure_ascii=False)


def argon_call(api_key: str):
    """Call Gemini 4 Argon Interactions API with structured, bounded output."""
    if not api_key:
        raise ValueError("missing_gemini_api_key")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/interactions"

    def call(prompt: str) -> str:
        provider_prompt, by_id = provider_input(prompt)
        payload = json.dumps({
            "model": "gemini-4-argon",
            "input": provider_prompt,
            "generation_config": {"max_output_tokens": 32768, "thinking_level": "medium"},
            "response_format": {"type": "text", "mime_type": "application/json",
                                "schema": RESPONSE_SCHEMA},
        }, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            endpoint, data=payload,
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                body = json.load(response)
        except urllib.error.HTTPError as error:
            raise ProviderHTTPError(error.code) from None
        if body.get("status") != "completed":
            raise ModelOutputIncomplete()
        content = "".join(
            item.get("text", "")
            for step in body.get("steps", []) if step.get("type") == "model_output"
            for item in step.get("content", []) if item.get("type") == "text"
        )
        if not content.strip():
            raise ModelOutputEmpty()
        return resolved_response(json.loads(content), by_id)

    return call
