# D/E Argon shadow exploratory audit — 2026-10-20

## Boundary

Only three publicly tracked, reviewed calibration fixtures were sent to the
Google Gemini API with the user's explicit approval. No private answer session,
WordPress database or Telegram message was sent. `gemini-4-argon` was used via
the Interactions API. This was an exploratory shadow test, not a release of D/E
score authority. The final 25-point grade, A/B/C, `WRONG` and fatal policies
were unchanged. Raw answers and credentials are not included here.

## Observations

| Public case ID | Purpose | Valid runs | D proposals | E proposals | Within-case dispersion |
| --- | --- | ---: | --- | --- | --- |
| `qtype_qg-cs-high-01` | high-quality comparison | 2/2 | 6, 6 | 2, 2 | 0 |
| `qtype_qg-cs-low-01` | low-quality comparison | 2/2 | 2, 2 | 0, 0 | 0 |
| `mcdc_vmodel_sil_issue1` | answer with verified technical errors | 2/2 | 3, 3 | 0, 0 | 0 |

All six proposals passed literal-quote, Topic-scope, positive-evidence and
non-duplication validation. The model separated the high- and low-quality
cases and did not grant E credit to the error case. This does **not** establish
agreement with an independent expert D/E label. On one additional inspection
of the error case, positive D1–D3 reasons were tied to partial, literal answer
excerpts; E1–E2 were zero. That is a narrow reason audit, not a proof that the
proposed points are the only defensible expert scores.

Earlier local `qwen3.5:9b` and `glm-4.7-flash` trials remained `UNEVALUATED`
because they reused an evidence ID for multiple positive criteria. Increasing
Ollama context size fixed premature truncation but did not justify relaxing
the duplicate-credit guard. The Argon prompt excludes short bare headings
from evidence options and requires each reason to be supported by its selected
excerpt.

## Decision and next evidence

**Shadow evaluation: technically callable and provisionally promising.**
**Final-score authority: NO-GO.** Three cases, two repetitions each and one
manual reason inspection are insufficient to establish cross-topic accuracy,
calibration or acceptable failure rate. Before score promotion, compare a
pre-declared broader sample against independently reviewed D1–E2 labels,
including wrong-answer and terse-answer edge cases, and define the exact
fallback and final-score ceiling policy. Do not treat structural validity or
zero within-case dispersion as semantic truth.

## Subsequent operational decision

After this exploratory report, the user authorized bounded use of Argon D/E
in the final grade and ongoing operational review. The adapter is opt-in;
accepted D/E proposals stay under deterministic requirement ceilings, while
A/B/C, fatal findings and verdict policy are unchanged. Provider or validation
failure falls back to deterministic D/E. This operational choice does not
retroactively turn the six shadow runs into independent expert labels. Score
disputes and provider failures should be recorded in private quality check
sheets, then reviewed against expert criteria before prompt or policy changes.

## 2026-11-13 운영 후속 이슈 — `duplicate_positive_evidence` (OPEN)

2026-10-20의 공개 calibration 6회 유효 판정은 **과거의 제한된 shadow 실험 결과**이다. 2026-11-13의 별도 비공개 실사용 답안에서는 선택된 `gemini-4-argon` D/E 제안이 **근거 중복 검증**에 실패했다. 실사용 성능 또는 전체 유효율을 기존 6회만으로 추정하지 않는다.

확인된 비공개 `grade.json` 진단 필드: `mode=argon`, `status=FALLBACK`, `provider_calls=1`, `reason_code=duplicate_positive_evidence`, `score_effect=none`, `llm_score_authority=none`. 결정론적 D=0, E=1로 최종 11/25가 유지됐다. `provider_calls=1`만으로 HTTP 성공을 단정하지 않지만, 근거 중복 검증에 도달했다는 점에서 단순 API 미설정/429 문제로 설명할 증거는 없다.

이는 과거 qwen evidence ID 중복 이슈와 **동일 검증 경계에서 발생한 Gemini 실사용 사례**다. 중복 근거 방지 정책을 없애서 점수를 높이는 것이 해결책은 아니다. 후보 근거가 부족한지, 모델이 중복 ID를 선택했는지, A/B/C가 지원 span을 과도하게 좁혔는지 분리 진단하고, 필요한 경우 **1회 제한 재시도 + 전부 재검증**을 평가한다.

**세부 작업·안전 경계·완료 조건:** [D/E qualitative shadow contract — 2026-11-13 운영 보완](../docs/qualitative_de_shadow.md#2026-11-13-운영-보완-항목--gemini-de-근거-중복에-따른-fallback). 비공개 세션 원문·세션 경로·API 키를 본 보고서로 옮기지 않는다. 본 추가 기록은 코드 수정 또는 재평가 완료 선언이 아니다.

