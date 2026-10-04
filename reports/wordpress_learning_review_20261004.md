# WordPress learning content: review required

Status: resumed following the user's annotation-only instruction; editorial decisions remain pending.
Inspected HEAD: `7ffc247`.

## Subsequent user decision

사용자 지시: 블로그 원문을 보존하고 주석만 남긴다. 기술 내용의 수정 여부는
사용자와 다른 LLM이 나중에 판단한다. 아래의 기존 교정 제안은 채택된 결정이 아니다.
미확정 주석 3건은 `study/source_review_annotations/second_order_lag_response_by_damping_ratio.json`
에 저장한다. 원문·채점 기준은 수정하지 않는다. 별도 프로그램 결함인 출처 버전과
정확한 URL 불일치는 로더에서 차단하고 격리된 회귀시험으로 검증한다.

## 1. Reproduced source-version mismatch

Location: `study/master_topic_pack.py`, `_load_linked_wordpress_materials`.

The loader validates source ID, parent URL and the extracted text's own hash,
but does not compare the bundle's version with the approved Master reference.
Its output takes `version` from the Master and `text` from the bundle. A fresh
catalog/bundle can therefore expose changed text under an older approved version.

Read-only mocked reproduction (no catalog or Master files changed):

- Master approved version: `2026-10-03`.
- Bundle version: `NEW_UNAPPROVED_VERSION`.
- Bundle text: `CHANGED_TEXT_WITHOUT_MASTER_APPROVAL`, with its correct SHA-256.
- Result: changed text accepted; emitted version remained `2026-10-03`.

The text checksum proves only internal bundle consistency. It does not prove
that the approved source revision supplied that text.

Recommended correction: check bundle version and exact source URL against the
Master reference before exposing text; preserve honest provenance; cover stale
and matching versions with isolated regression fixtures. Define how unavailable
or stale supplemental material is reported without losing existing learning
content. Re-run the learning integration and required release checks before push.

## 2. OCR terminology requiring editorial review

Source: `wp-post:7176`, “2차 시스템 과도 응답”.
URL: https://now0930.pe.kr/wordpress/2%ec%b0%a8-%ec%8b%9c%ec%8a%a4%ed%85%9c-%ea%b3%bc%eb%8f%84-%ec%9d%91%eb%8b%b5/
Topic: `second_order_lag_response_by_damping_ratio`.
Source version: `32a5dfd164ef1fa9b69fc57fbd0400f4db6b0025cc5adc8e06012b274599ad34`.
Extracted-text SHA-256: `27925feb9e8182d403e51ad38b2fc4162ca4fcab3f09ac3e92a661fdfbe4793b`.

- Section 3 explicitly reports that the handwriting labels ωd “Undamped natural
  freq”, while the HTML limits its adopted description to the pole's imaginary
  component. This is an acknowledged source annotation, not an assertion that
  the HTML silently adopts the incorrect label.
- Sections 10 and 13 preserve “Critical System” for imaginary-axis poles.
  A study summary should distinguish marginal stability from critical damping.
- The closing note explicitly leaves the unclear transfer-function numerator
  unspecified. It must not be reconstructed as though it were legible OCR.

Existing Topic anchors already distinguish the damped frequency ωd from ωn,
critical damping at ζ=1, and undamped imaginary poles at ζ=0. For the standard
complex-pole case, the quadratic gives
`s = -ζωn ± jωn√(1-ζ²)` and hence `ωd = ωn√(1-ζ²)`.

Recommended handling: preserve the WordPress/OCR source, state these distinctions
explicitly in any derived study aid, and retain the numerator as unknown. Do not
promote the transcribed terminology into a new grading fact.

## Scope at the initial stop

No new Topic content, database changes, source approvals, commits or pushes were
performed during this review. This report is the only workspace change. The
reproduction establishes a loader defect; it does not establish that any actual
stored source pair is currently mismatched.

## Implementation verification after resuming

- Three comments are exposed separately in Training, Diagnosis and feedback,
  all with `pending_review`, null decision and no score effect.
- Original text remains unchanged. Source changes mark old comments stale;
  absent private source text is explicitly reported as unavailable.
- Source versions and exact URLs must match Master before text is exposed.
- Six isolated annotation/provenance regression tests passed. Existing
  learning projection, integration, source contract and runtime tests passed.
- All three real-source comments matched their pinned text hash and quote.
- Master validation passed for 49 records; the complete non-promote
  `scripts/validate_release.sh` and Topic Pack `--all` release validation passed.
  Live smoke and opt-in reproducibility runs were disabled.
- The current catalog bundles showed zero linked WordPress version/URL
  mismatches. The regression reproduces a potential update failure, not evidence
  of an existing mislabeled production article.
