#!/usr/bin/env python3
"""Repeat score-neutral D/E shadow evaluation of one reviewed calibration case.

Only redacted metrics are printed. This command does not write a grade, session,
Topic Pack or answer copy. Ollama calls are opt-in via --provider ollama.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.qualitative.de_benchmark import _source_text, build_manifest
from grading.qualitative.provider_transport import (
    RESPONSE_SCHEMA,
    ModelOutputEmpty,
    ModelOutputTruncated,
    ProviderHTTPError,
    argon_call as _argon_call,
    provider_input as _provider_input,
    resolved_response as _resolved_response,
)
from grading.qualitative.repeatability import measure_repeated_shadow
from grading.qualitative.shadow_input import project_deterministic_shadow_input
from grading.scoring.deterministic_primary_grader import grade_deterministically


def _ollama_call(url: str, model: str, temperature: float, max_output_tokens: int = 4096,
                 context_tokens: int = 16384):
    endpoint = url.rstrip("/") + "/api/chat"
    def call(prompt: str) -> str:
        provider_prompt, by_id = _provider_input(prompt)
        payload = json.dumps({"model": model, "messages": [{"role": "user", "content": provider_prompt}],
                              "stream": False, "format": RESPONSE_SCHEMA, "think": False,
                              "options": {"temperature": temperature, "num_predict": max_output_tokens,
                                          "num_ctx": context_tokens}},
                             ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(endpoint, data=payload,
                                         headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.load(response)
        if body.get("done_reason") == "length":
            raise ModelOutputTruncated()
        content = body["message"].get("content", "")
        if not content.strip():
            raise ModelOutputEmpty()
        proposal = json.loads(content)
        return _resolved_response(proposal, by_id)
    return call


def _gemini_call(model: str, api_key: str, temperature: float, max_output_tokens: int = 4096):
    if not api_key:
        raise ValueError("missing_gemini_api_key")
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def call(prompt: str) -> str:
        provider_prompt, by_id = _provider_input(prompt)
        payload = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": provider_prompt}]}],
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_output_tokens,
                                 "responseMimeType": "application/json"},
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
        candidate = body["candidates"][0]
        if candidate.get("finishReason") == "MAX_TOKENS":
            raise ModelOutputTruncated()
        content = "".join(part.get("text", "") for part in candidate["content"]["parts"]
                          if isinstance(part, dict) and not part.get("thought"))
        if not content.strip():
            raise ModelOutputEmpty()
        return _resolved_response(json.loads(content), by_id)

    return call


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--provider", choices=("none", "ollama", "gemini", "argon"), default="none")
    parser.add_argument("--model", default="")
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    parser.add_argument("--context-tokens", type=int, default=16384)
    args = parser.parse_args()
    if not 512 <= args.max_output_tokens <= 8192:
        parser.error("--max-output-tokens must be between 512 and 8192")
    if not 4096 <= args.context_tokens <= 65536:
        parser.error("--context-tokens must be between 4096 and 65536")
    manifest = build_manifest(ROOT)
    cases = [row for row in manifest["cases"] if row["case_id"] == args.case_id]
    if len(cases) != 1:
        parser.error("case_id is not in the 25-case reviewed worklist")
    callback = None
    if args.provider == "ollama":
        url = os.getenv("OLLAMA_URL", "")
        args.model = args.model or os.getenv("OLLAMA_MODEL", "")
        if not url or not args.model:
            parser.error("OLLAMA_URL and --model/OLLAMA_MODEL are required")
        callback = _ollama_call(url, args.model, args.temperature,
                                args.max_output_tokens, args.context_tokens)
    elif args.provider == "gemini":
        args.model = args.model or os.getenv("GEMINI_MODEL", "")
        if not args.model or not os.getenv("GEMINI_API_KEY", ""):
            parser.error("GEMINI_MODEL and GEMINI_API_KEY are required")
        callback = _gemini_call(args.model, os.environ["GEMINI_API_KEY"],
                                args.temperature, args.max_output_tokens)
    elif args.provider == "argon":
        args.model = "gemini-4-argon"
        if not os.getenv("GEMINI_API_KEY", ""):
            parser.error("GEMINI_API_KEY is required")
        callback = _argon_call(os.environ["GEMINI_API_KEY"])
    question, answer = _source_text(ROOT, cases[0])
    try:
        grade = grade_deterministically(question_text=question, answer_text=answer)
        abc_result, topic_context = project_deterministic_shadow_input(grade)
        metadata = {"provider": args.provider, "model_id": args.model or "unconfigured",
                    "prompt_version": "qualitative_de_shadow_v3_examples"}
        if args.provider != "argon":
            metadata["temperature"] = args.temperature
        report = measure_repeated_shadow(
            question, answer, abc_result, topic_context, callback,
            metadata,
            runs=args.runs,
        )
    except Exception as error:
        # Exception messages may include private answer fragments.
        print(json.dumps({"case_id": args.case_id, "measurement_status": "INCOMPLETE",
                          "error_type": type(error).__name__}, ensure_ascii=False))
        return 1
    report.update({"case_id": args.case_id,
                   "question_sha256": cases[0]["question_sha256"],
                   "answer_sha256": cases[0]["answer_sha256"],
                   "deterministic_topic_ids": topic_context["topic_ids"]})
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0 if report["measurement_status"] == "MEASURED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
