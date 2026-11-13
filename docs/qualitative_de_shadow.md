# D/E qualitative shadow contract

> **사람용 핵심:** D/E 보조 모델은 근거를 제한적으로 제안하고 프로그램이 검증합니다. A/B/C의 확정 오류·점수 권한을 모델에 이전하지 않습니다.
>
> **AI·개발자:** [코드·데이터 권한 참조](ai_implementation_reference.md) · [프로젝트 정책](../AGENTS.md). 과거 실행 기록과 현재 필수 Gate를 혼동하지 않습니다.


`GRADING_DIRECTION_CONTRACT.md` governs bounded D/E score authority. This
shadow evaluator remains score-neutral by itself; the explicit opt-in adapter
may use a validated proposal to replace D/E in the final 25-point grade.

## Inputs and authority

`grading.qualitative.de_shadow.evaluate_qualitative_de(question, answer,
abc_result, topic_context, llm_call=None, model_metadata=None)` accepts an
already completed deterministic A/B/C breakdown, requirement rows with literal
answer spans, routed Topic IDs and optional verified Fact excerpts. The LLM
receives these as context; answer text is untrusted data. The LLM response is a
proposal, never an authority over A/B/C, `WRONG` or fatal findings. Only
validated D/E proposals can change the deterministically recomputed total.

## Output

Each `criteria` row has `criterion_id`, `score`, `reason`, `topic_id`, `quote`,
`start`, `end`. D1 (technical choice), D2 (grounds and conditions), D3
(alternatives, limitations and trade-offs) each have a 0–2 proposed range.
E1 (specific technical follow-up question) and E2 (answer-grounded ability to
explain it) each have a 0–1 proposed range. Interview questions (up to three)
carry a program-generated stable ID, quoted answer span, Topic ID, question,
reason and expected explanation elements. They remain review candidates, not
Master facts.

The evaluator returns either `SHADOW_VALIDATED` (structurally validated but
`semantic_truth_verified=false`) or `UNEVALUATED` with a reason code.
`score_effect=none` in both cases. No `total_score` is emitted. If unavailable
or invalid, D/E is **not** 0; it is unassessed. `model_metadata`, `input_hash`,
`request_hash`, and provider-call count support repeated evaluation audits
without publishing answer text.

When `QUALITATIVE_DE_MODE=argon` enables the bounded production adapter, the
Telegram `/provider` choice is also passed to this D/E call: `/provider clova`
uses CLOVA Studio (`CLOVA_API_KEY`, `CLOVA_MODEL`, and the CLOVA endpoint
settings), while `/provider gemini` uses Gemini 4 Argon. `/provider auto`
preserves the historical Gemini Argon choice for D/E; its CLOVA fallback
behavior applies to the separate semantic-grading route, not this D/E route.
The selected provider and model are recorded in the private grade artifact.
Provider choice does not change A/B/C ownership, D/E limits, quote/evidence
validation, Fatal handling, or program-owned score ceilings. The production
qualification gate remains explicitly Argon-qualified and does not treat a
CLOVA run as Argon qualification evidence.

The prompt also includes four **synthetic, topic-neutral scoring examples**
(`grading/qualitative/prompt_examples.py`): a partially supported choice,
a generic conclusion without evidence, a claim already marked `WRONG` by
A/B/C, and a fully supported choice with distinct grounds. The illustrative
0–2/0–1 scores calibrate the scale; they are not model
answers, live Topic facts, or expert labels. Current-question A/B/C and literal
answer evidence take precedence. The example version is included in the hashed
request, so later policy changes remain auditable. No example can authorize an
LLM to change the deterministic result or the final score.

`project_deterministic_shadow_input` forms the shadow scope from the owner
Topic IDs of already established requirement rows. It does **not** pass all
router candidates to D/E: a router candidate unrelated to the question must
not become a qualitative credit source. The current adapter supplies no
additional `verified_facts`; the deterministic requirement judgments and
their cited spans are the only technical-evidence boundary in this run.

For a reviewed calibration case, `scripts/run_qualitative_de_repeatability.py`
rebuilds the deterministic input and repeats the shadow evaluation. Its stdout
contains hashes, status counts, proposed-score dispersion and model metadata,
but no answer or answer quotation. A provider-free dry run intentionally exits
2 with `INCOMPLETE`, not a fabricated zero score. Live Ollama use is opt-in:

```bash
OLLAMA_URL=http://ollama:11434 OLLAMA_MODEL=<installed-model> \
  python3 -B scripts/run_qualitative_de_repeatability.py \
  --case-id qtype_qg-cs-high-01 --provider ollama --runs 3
```

Run this only in an authorized environment for transferring the calibration
question and answer to the selected model. Repeated structural acceptance is
**not** expert agreement; all reports retain `acceptance_status=REVIEW_REQUIRED`.
For approved, publicly tracked calibration fixtures only, Gemini 4 Argon can
be exercised with `--provider argon` and `GEMINI_API_KEY` set in the process
environment. The adapter uses the Interactions API with structured JSON,
medium thinking and a 32,768-token ceiling. It never reads private sessions
or credentials from disk itself. The caller must separately decide which
fixture and credential source are authorized. See
`reports/qualitative_de_argon_shadow_audit_20261020.md` for the first
score-neutral quality observations.
The local Ollama adapter now supplies literal, uniquely located evidence
options and asks the model to select IDs. The program converts IDs back to
exact quotations and offsets before the original validator runs. It rejects
unknown IDs, unrelated Topic IDs, WRONG-overlapping spans, duplicate positive
credit and truncated model output. This has not yet produced a passing live
repeatability result; see `reports/grading_direction_operational_decision.md`.

## Program validation and known limits

The validator rejects score overflow, unapproved Topic IDs, missing or altered
literal quote/spans, positive evidence overlapping `WRONG`, positive evidence
without a deterministic supported Fact span, exact duplicate positive evidence,
malformed schema, and LLM attempts to set a final/ABC score. It does not prove
that a semantically plausible interpretation is technically true or that all
expressions of judgment were recalled; expert D/E labels and repeated live
model runs are required before operational promotion.

The optional `shadow_storage` module writes only to an explicitly supplied
private path with exclusive creation and 0600 permissions. Its learning and
diagnosis projections are `candidate`/score-neutral; they cannot update Master
Topic Packs or review history automatically. These are staging envelopes, **not**
the existing `training_projection.schema.json` or
`diagnosis_projection.schema.json` views; a reviewed adapter is needed before a
trainer or diagnoser consumes them.

## Operational promotion

`QUALITATIVE_DE_MODE=argon` enables the bounded adapter. The default `off`
keeps deterministic D/E. Validated proposals replace only D/E; existing
requirement ceilings, fatal caps and verdict rules still apply. An invalid or
unavailable proposal triggers a disclosed `FALLBACK` to deterministic D/E.
The shadow evaluator's own `score_effect=none` and
`semantic_truth_verified=false` remain accurate: its output is structurally
accepted, not expert-verified. Operational disputes go to the private quality
check sheet for later review.

## 2026-11-13 운영 보완 항목 — Gemini D/E 근거 중복에 따른 fallback

**상태: OPEN / 문서화 완료 · 원인 분류 완료 · 수정·회귀·운영 검증 미완료.** 아래 기록은 2026-11-13 실제 PID 제어기 기술사 답안의 **비공개** Telegram 세션에서 관찰한 현상이다. 답안 원문, 세션 경로·식별자, API 키, 요청/응답 전문은 공개 저장소에 복사하지 않는다.

| 관측 필드 | 확인된 값 | 해석 한계 |
| --- | --- | --- |
| `qualitative_de_evaluation.mode` | `argon` | D/E opt-in 경로에 진입 |
| `status` / `reason_code` | `FALLBACK` / `duplicate_positive_evidence` | 중복된 양수 점수의 인용 구간을 검증기가 거부 |
| `provider` / `model_id` | `argon` / `gemini-4-argon` | 선택된 모델 |
| `provider_calls` | `1` | 호출 **시도** 기록; 단독으로 HTTP 성공을 증명하지 않음 |
| `score_effect` / `llm_score_authority` | `none` / `none` | Gemini 제안은 최종 점수에 미반영 |
| 최종 D/E 및 총점 | 결정론적 D=0/6, E=1/2, 총점 11/25 | Gemini가 D=0을 판정했다는 뜻이 아님 |
| A/B/C 판정 요약 | `PARTIAL` 1건, `SATISFIED` 0건 | 근거 후보가 제한됐을 가능성. 실제 후보 개수와 span 연결은 별도 분석 필요 |

**직접 원인:** `grading/qualitative/de_shadow.py`의 `_validate_proposal()`은 양수 점수를 받는 D1/D2/D3/E1/E2의 동일한 `(start, end)` 구간 재사용을 `duplicate_positive_evidence`로 거부한다. `grading/qualitative/provider_transport.py`는 evidence ID를 실제 답안 span으로 변환한다. 이 경우 구조 검증 단계까지 도달했으므로, 이번 실패를 API 키·과금·429·모델 미지원 등 전송 실패로 단정하지 않는다. **근거 검증 실패는 실제 답안의 기술적 품질 평가와 분리**한다.

### 보완 작업 (실행 전 승인·검증 필요)

1. **P0 — 원인·상태 관측성:** `reason_code`, `provider_calls`, 제안 검증 단계, 중복 `criterion_id` 조합, 중복 `evidence_id` 또는 span의 **비식별 해시/개수**만 비공개 진단에 기록한다. HTTP 실패와 응답 스키마/근거 검증 실패를 구별한다. 원문 인용, 토큰, API 키 및 요청·응답 전문을 공용 로그·Telegram에 노출하지 않는다. Telegram은 필요 시 `D/E 미반영(근거 중복; 결정론적 기준 적용)`처럼 정확하고 짧은 상태만 표시한다.
2. **P1 — 후보 부족/중복 원인 분리:** 동일 비공개 사례에서 `build_evidence_options()`가 제시한 후보 수·서로 다른 supported span 수·D1~E2의 선택 ID·중복 지점을 조사한다. 후보가 실제로 적다면 중복을 피하도록 *다른 문장을 억지 생성*하지 말고 해당 기준에 0점을 제안할 수 있게 한다. `PARTIAL` 하나만 인정한 A/B/C requirement 매핑이 답안의 여러 기술적 판단을 누락했는지도 **독립 진단**하되, Gemini를 이용해 A/B/C를 승격하지 않는다.
3. **P1 — 제한적 재시도 설계:** 중복 ID가 원인일 때만, 이미 제공한 유효한 evidence ID 목록과 중복 금지 설명을 이용해 **최대 1회** D/E 제안 재시도를 검토한다. 재시도 결과도 같은 quote/Topic/WRONG/supported span/중복·E1 질문 검증을 통과해야 한다. 유효 후보가 부족하면 `FALLBACK`; 0점을 성공인 것처럼 강제하지 않는다. 비용·타임아웃·재시도 횟수는 명시적으로 기록한다.
4. **P2 — 중복 근거 정책의 의미 검토:** 한 문장이 여러 관점의 판단 근거일 수 있지만, **동일한 증거를 중복 가점한 것**과 구별하는 독립 전문가 사례가 먼저 필요하다. 전문가 합의 없이 `duplicate_positive_evidence` guard를 삭제하거나, 인용 구간을 기계적으로 분할하여 가점을 늘리지 않는다.
5. **P2 — 성능·채점 타당성 검증:** 동일 답안의 D/E 구조 검증 통과 여부와 전문가 D1~E2 라벨의 부합 여부를 **별도 지표**로 기록한다. 일반적 정상·부분·오류·짧은 답안·복합 Topic 사례를 포함하고, 재시도 전후 비용·지연·유효 제안율·부당 가점률을 비교한다. 11/25를 변경하는 목적의 회귀가 아니라 정확한 근거와 평가 권한을 검증하는 것이다.

### 변경 및 완료 판정 경계

- A/B/C 결정론적 권한, Fatal/WRONG, 최종 점수 상한과 기존 fallback은 **변경 금지**. 모델 응답이 무효면 D/E는 모델의 0점이 아니라 결정론적 D/E를 사용한다.
- 검증 대상: `tests/test_qualitative_de_shadow.py`, `tests/test_qualitative_de_evidence_options.py`, `tests/test_qualitative_de_provider_transport.py`, `tests/test_qualitative_de_authority.py`와 기존 score ceiling/replay 테스트. 중복 ID, 유효 ID 부족, 재시도 성공/실패, 잘못된 Topic·WRONG 인용, 민감정보 비노출, A/B/C·Fatal 불변 조건을 포함한다.
- 이 문서는 **개선사항 등록**이며 코드 수정·API 재호출·재채점·운영 배포·pytest 실행 완료를 의미하지 않는다. 후속 구현은 별도 변경 커밋과 검증 결과가 있어야 `DONE`으로 전환한다.

