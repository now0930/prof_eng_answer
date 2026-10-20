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
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.qualitative.de_benchmark import _source_text, build_manifest
from grading.qualitative.evidence_options import build_evidence_options, resolve_evidence_id
from grading.qualitative.repeatability import measure_repeated_shadow
from grading.qualitative.shadow_input import project_deterministic_shadow_input
from grading.scoring.deterministic_primary_grader import grade_deterministically


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


def _ollama_call(url: str, model: str, temperature: float):
    endpoint = url.rstrip("/") + "/api/chat"
    def call(prompt: str) -> str:
        prompt_data = json.loads(prompt)
        options = build_evidence_options(prompt_data["answer"], prompt_data["requirements"])
        by_id = {item["evidence_id"]: item for item in options}
        prompt_data["instruction"] += (
            " 각 양수 점수와 면접 질문은 evidence_options의 evidence_id 하나를 선택하세요. "
            "0점은 evidence_id=null입니다. 원문 인용이나 위치를 새로 쓰지 마세요. "
            "서로 다른 양수 점수에는 서로 다른 evidence_id를 사용하세요."
        )
        prompt_data["schema"] = RESPONSE_SCHEMA
        prompt_data["evidence_options"] = [
            {key: item[key] for key in ("evidence_id", "quote", "topic_ids")}
            for item in options
        ]
        provider_prompt = json.dumps(prompt_data, ensure_ascii=False, separators=(",", ":"))
        payload = json.dumps({"model": model, "messages": [{"role": "user", "content": provider_prompt}],
                              "stream": False, "format": RESPONSE_SCHEMA, "think": False,
                              "options": {"temperature": temperature, "num_predict": 2048}},
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
        if isinstance(proposal, dict):
            if isinstance(proposal.get("criteria"), list):
                proposal["criteria"] = [resolve_evidence_id(
                    row, by_id, zero_score=row.get("score") == 0) for row in proposal["criteria"]]
            if isinstance(proposal.get("interview_questions"), list):
                proposal["interview_questions"] = [resolve_evidence_id(row, by_id)
                                                   for row in proposal["interview_questions"]]
        return json.dumps(proposal, ensure_ascii=False)
    return call


class ModelOutputTruncated(RuntimeError):
    """The provider exhausted output tokens before completing its JSON."""


class ModelOutputEmpty(RuntimeError):
    """The provider returned no JSON content."""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--provider", choices=("none", "ollama"), default="none")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", ""))
    parser.add_argument("--temperature", type=float, default=0)
    args = parser.parse_args()
    manifest = build_manifest(ROOT)
    cases = [row for row in manifest["cases"] if row["case_id"] == args.case_id]
    if len(cases) != 1:
        parser.error("case_id is not in the 25-case reviewed worklist")
    callback = None
    if args.provider == "ollama":
        url = os.getenv("OLLAMA_URL", "")
        if not url or not args.model:
            parser.error("OLLAMA_URL and --model/OLLAMA_MODEL are required")
        callback = _ollama_call(url, args.model, args.temperature)
    question, answer = _source_text(ROOT, cases[0])
    try:
        grade = grade_deterministically(question_text=question, answer_text=answer)
        abc_result, topic_context = project_deterministic_shadow_input(grade)
        report = measure_repeated_shadow(
            question, answer, abc_result, topic_context, callback,
            {"provider": args.provider, "model_id": args.model or "unconfigured",
             "temperature": args.temperature, "prompt_version": "qualitative_de_shadow_v2"},
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
