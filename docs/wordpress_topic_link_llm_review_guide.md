# LLM-Assisted WordPress–Topic Link Review

## Purpose

Use this procedure to recommend whether WordPress posts are relevant to
existing Topic Packs. The model is a reviewer aid only. A recommendation is
not an approved link and must not update the catalog, a Master Topic Pack, a
Topic Pack, or any learning/grading View.

Input is the CSV created by:

```bash
python3 scripts/wordpress_catalog.py \
  --export-topic-link-review reports/wordpress_topic_link_manual_review_YYYYMMDD.csv
```

The export contains one row per existing approved or pending link candidate,
and one row per post with no active link. A post may therefore occur on several
rows. Preserve every row and its order-independent identity (`post_id`,
`link_status`, `candidate_topic_id`).

## Hard boundaries

- Do not edit the input CSV. Write a separate output file and refuse to
  overwrite an existing output.
- Do not run commands that approve/reject a Topic link, approve a source
  proposal, prepare/apply a content candidate, or modify the database or
  canonical files.
- Do not create Topic Packs, alter Topic IDs, routing, grading rules, or Master
  content. Review only relationships to the existing 82 Topic Packs.
- Treat `lexical_score` and `matched_terms` as retrieval hints, not proof.
  Shared generic words or a title-only overlap are not sufficient evidence.
- Do not fetch or OCR external PDF URLs. OCR scope is limited to PDFs on
  `now0930.pe.kr` and its subdomains. External PDFs are metadata-only.
- If the supplied post excerpt and available Topic Pack material do not give
  enough evidence, choose human review; do not guess.

## What to inspect

For each row, consider the post title, URL, excerpt, tags, and attached asset
metadata. If more context is needed, read the already-collected post body from
the local catalog (`posts.content_text`, or `sources.extracted_text` for
`source_id=wp-post:<post_id>`) using read-only access. Do not sync or download
new material. Open the existing Topic Pack named by `candidate_topic_id` and
check its README and relevant source JSON (especially fact anchors, logic
checks, question patterns, and model-answer scope). For an unmatched post,
search all existing Topic Pack IDs/titles and inspect the most plausible pack
before recommending a new link. Do not infer fit from the candidate title
alone.

Assess whether the post's main technical subject falls within the Topic Pack's
defined scope. Distinguish a central topic from a passing mention, an adjacent
engineering subject, exam-writing advice, a general article, or unrelated
attachment metadata. When several rows share a `post_id`, compare the
candidates together and recommend multiple links only when the post materially
covers each Topic.

## Recommendation fields

Copy every input column unchanged and append these columns:

- `llm_recommendation`: one of `recommend_approve`, `recommend_reject`,
  `recommend_link`, `retain_approved`, `unmatched`, `manual_review`.
- `llm_confidence`: `high`, `medium`, or `low`.
- `llm_topic_id`: the existing candidate Topic ID for an approval/link
  recommendation; otherwise blank. Never invent an ID.
- `llm_evidence`: concise evidence from the post and the specific Topic Pack
  scope. State the filenames/section or anchor IDs inspected; distinguish
  direct evidence from inference.
- `llm_notes`: ambiguity, conflicting candidates, missing source text, or the
  reason a human decision is needed.

Apply these rules:

| Input row | Recommendation rule |
| --- | --- |
| `link_status=approved` | `retain_approved`; do not reopen or alter it. |
| `link_status=pending_review` | `recommend_approve` only for a direct, well-supported subject match; `recommend_reject` when evidence clearly shows it is out of scope; otherwise `manual_review`. |
| `link_status=unmatched` | `recommend_link` only when one existing Topic Pack has a direct, high-confidence fit; otherwise `unmatched` or `manual_review`. |

Use `high` only when the post's main subject and Topic Pack scope agree on
specific technical content and there is no material ambiguity. Use `medium`
or `low` for adjacent, sparse, OCR-dependent, or conflicting evidence; these
must not result in an automated catalog change. `recommend_reject` means the
candidate link appears wrong; it does not authorize rejection.

## Output and validation

Save a new UTF-8 CSV, for example:
`reports/wordpress_topic_link_manual_review_YYYYMMDD_llm.csv`. Keep all input
columns and rows unchanged, including the blank human fields
`review_action`, `review_topic_id`, and `reviewer_notes`. Do not put an LLM
recommendation into those human-decision fields.

Before returning the result, verify:

1. Input and output row counts match and every `(post_id, link_status,
   candidate_topic_id)` key is preserved exactly once.
2. All approved rows are `retain_approved` and no non-approved row is marked
   `retain_approved`.
3. Every `llm_topic_id` exists in `rubrics/topic_packs/` and agrees with the
   row's candidate unless the row is `unmatched` and the recommendation is
   `recommend_link`.
4. No `manual_review`, `unmatched`, or low-confidence item is represented as
   approved.
5. No project database or canonical file changed during the review.

Run the deterministic contract check before handing back the file:

```bash
python3 scripts/validate_wordpress_topic_link_review.py \
  --source reports/wordpress_topic_link_manual_review_YYYYMMDD.csv \
  --review reports/wordpress_topic_link_manual_review_YYYYMMDD_llm.csv
```

A passing check confirms row/field integrity and recommendation shape; it does
not confirm the semantic correctness of recommendations or authorize applying
them.

Return the output path and a short count of each recommendation/confidence.
The owner makes the final decision and applies accepted mappings one at a time
with the existing `--review-topic-link POST_ID TOPIC_ID approve|reject`
command. No LLM output is imported automatically.

## Explicitly delegated resolution

If the owner separately delegates final relationship decisions to an agent,
that agent may resolve links after checking the stored post and Topic scope.
The CSV remains recommendation data; a `high` label alone is not approval.
Record the delegation, CSV hashes, decisions, reasons and deferred row keys in
a separate resolution report. Pass the real agent identity and review evidence
to `review_topic_link(..., reviewed_by=..., evidence=...)`; do not impersonate
a human reviewer. Resolved decisions are preserved on retries, and a failed
proposal-queue write rolls back the link decision.

Source-reference approval records provenance only. Keep references unverified
until their technical content and locators have been checked. Content changes
still follow the separate Topic-content proposal contract. Defer ambiguous
recommendations with reasons rather than treating the remainder as rejected.
