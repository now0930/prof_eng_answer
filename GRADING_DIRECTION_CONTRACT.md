# Grading direction contract — bounded D/E qualitative scoring

> **사람용 핵심:** D/E 정성 평가는 근거를 제한적으로 제안할 뿐 A/B/C의 확정 판정권을 갖지 않습니다. 해당 Argon 경로는 명시적 opt-in입니다.
>
> **AI·개발자:** [코드·권한 참조](docs/ai_implementation_reference.md). 변경 전 최신 정책과 실제 코드 경로를 확인하세요.


Status: opt-in operational mode (`QUALITATIVE_DE_MODE=argon`), 2026-10-20.

## Purpose and authority

The 25-point rubric remains A 3, B 6, C 8, D 6, E 2. A/B/C and the
`SATISFIED`/`PARTIAL`/`WRONG`/`MISSING` requirement decisions belong to the
deterministic engine, approved Master Topic Pack and Engineering Ontology.
The LLM may propose only D1–D3 and E1–E2 qualitative evidence and at most
three interview questions. The program validates the proposal. An LLM cannot
change A/B/C, a verified error, a fatal finding or a Topic Pack. Only validated
D/E proposals may change the final total within existing deterministic ceilings.

## Scope

Allowed now: shadow evaluation and private persistence, plus an explicit opt-in
Argon adapter that replaces only validated D/E scores. The default mode still
uses legacy deterministic D/E. The user separately authorized transfer of
operational questions, answers and A/B/C evidence to Argon on 2026-10-20.

Forbidden: modifying generated banks or Topic Packs, silently changing score
ceilings, altering A/B/C or deterministic error findings, treating a model
proposal as verified semantic truth, or publishing answers/sessions/credentials.
An unresolved proposal is not zero: use and disclose deterministic D/E fallback.

## Failure and uncertainty

For a provider failure, malformed JSON, bad quote/span, wrong-topic evidence,
contradiction with deterministic `WRONG`, duplicate positive credit, or uncertain
meaning, the shadow result is `UNEVALUATED` with reason codes. The scoring
adapter then uses the existing deterministic D/E. Static checks prove only shape and literal
provenance, not the truth of a technical interpretation.

## Release and transition

Before deployment, run focused regressions, the full offline pytest suite,
and applicable rubric/source validation. Accuracy and stability qualification
are optional diagnostics, not deployment requirements. The Argon shadow report establishes structural acceptance, not
expert-label agreement. Monitor operational check sheets and review disputed
grades. Interview questions never auto-promote to Master facts.
