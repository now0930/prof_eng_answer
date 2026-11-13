# WordPress full-catalog Topic retrieval

> **사람용 핵심:** 전체 WordPress 카탈로그 검색·증분 캐시 절차입니다. 소스 원문과 생성 결과는 비공개 저장 경계를 지킵니다.
>
> **AI·개발자:** [구현 및 데이터 경계](ai_implementation_reference.md) · [WordPress/View 계약](wordpress_topic_pack_view_contract.md). 개인 원문·OCR·DB를 공개하지 않습니다.


## Purpose and boundary

Relationship semantics, partial-contribution criteria, review statuses, and
application boundaries are defined in
[the WordPress–Topic Pack linking policy](wordpress_topic_pack_linking_policy.md).

`scripts/match_wordpress_posts_to_topic_packs.py` ranks WordPress articles
against every existing `rubrics/topic_packs/*/README.md` and selected authored
Topic source JSON. It reads the WordPress catalog with SQLite `mode=ro`.
First-party extracted PDF/image text can add candidate Topics, but is ranked
separately from the post body because attachments may be unrelated or OCR may
be wrong.

The output is a retrieval shortlist, **not a semantic link decision**.
`retrieval_score`, `body_rank`, `asset_rank`, and `matched_terms` are not
probabilities. A reviewer must read the post evidence and candidate README
ownership boundaries. A retrieval miss is not evidence that a new Topic Pack
is required.

## Run

```bash
python3 scripts/match_wordpress_posts_to_topic_packs.py \
  --output reports/wordpress_topic_retrieval_YYYYMMDD.json
```

The output path must not already exist. By default the command scans every
post and Topic Pack, returns up to 12 candidates per post, and stores the
ranking cache at `data/wordpress_topic_match_cache.sqlite3`. The cache is local
runtime state and is git-ignored.

To run a subset:

```bash
python3 scripts/match_wordpress_posts_to_topic_packs.py \
  --post-id 123 --post-id 456 \
  --output reports/wordpress_topic_retrieval_subset_YYYYMMDD.json
```

## Incremental cache behavior

Each cached row is keyed by:

- post ID and a digest of post title, excerpt, tags, body version, and extracted
  first-party asset text;
- a digest of every indexed Topic README and selected authored source JSON;
- retrieval schema version and candidate count.

An edited article invalidates only its cached result. A changed Topic source or
retrieval schema invalidates results against the old index. An unchanged repeat
run reuses cached candidate rankings. Use a new output filename for each run;
never overwrite an earlier review artifact.

## Review and application

Review candidates in post groups, not as independent lexical rows. Preserve
existing approved mappings. For each proposed additional link, record source
locators, at least two independent direct technical facts when available, the
Topic README scope and ownership check, and any OCR/factual concerns.

Only direct, high-confidence semantic matches can be recommended for approval.
Keep ambiguous, sparse-source, or fact-conflicted cases for review. Record
likely coverage gaps separately from ordinary rejected candidates. The
retrieval report and LLM recommendations do not change `topic_links`, Master
Topic Packs, or any Grading/Training projection. Apply mappings only through
the separately reviewed link-decision workflow.

## Validation

Run the focused tests with:

```bash
python3 scripts/test_match_wordpress_posts_to_topic_packs.py
```

The test covers candidate ranking, preservation of existing links in the
shortlist, reuse of a cached result, and invalidation after the post body
changes. Production runs should also record source/database hashes and confirm
the catalog and Topic Pack files were not modified by retrieval.
