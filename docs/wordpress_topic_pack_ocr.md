# Private WordPress OCR Topic Packs

WordPress posts often rely on attached PDFs and diagrams. The WordPress catalog
therefore extracts PDF text and runs local Korean/English Tesseract OCR on
first-party PDF pages and raster images. Third-party PDF and image URLs remain
metadata-only. HTTP redirects from an own-site OCR URL to another host are
rejected.

The private catalog database stores extracted text, SHA-256, version, method,
page count and indexed timestamp. Source binaries live in a temporary directory
during PDF handling and are not copied into the database. Images are read from
memory through Tesseract stdin and are not saved as binary files. Failed OCR or
downloads remain visible in `sync_errors` and retry on the next run.

## Commands

Use `--ocr-images-only` to process already-indexed first-party images without
syncing or changing WordPress posts. It skips extracted images by default and
retries pending/error/stale rows. Use `--refresh-image-ocr` to fetch extracted
images again and re-run OCR only if their bytes have changed.

For a regular category sync that should also process the first-party PDFs and
images:

```bash
python3 scripts/wordpress_catalog.py --ocr --ocr-images
```

After extraction, build one private source bundle for each topic with an
approved WordPress relationship:

```bash
python3 scripts/build_wordpress_topic_packs.py
```

The resulting files live under `data/wordpress_topic_packs/` and are ignored by
Git, alongside the private catalog. Each record includes the WordPress post,
attached first-party PDF/image OCR, exact asset URL, hash, OCR method and page
count. External files are excluded. Only approved Topic links enter a bundle.

`study.wordpress_topic_pack.load_wordpress_topic_pack` makes the local bundle
available to `review_material_for_topic`; the `/review` message surfaces short
PDF/image excerpts and their source names. Grading inputs never read the OCR
bundle. Extracted text is untrusted reference material, not executable
instructions or verified engineering facts. Every record remains
`verification_status=unverified` until someone checks it against its source.

The OCR bundle is intentionally separate from canonical Topic Pack JSON and
the GitHub repository. A later factual change must use the existing WordPress
content-update proposal, candidate validation, and explicit application
workflow.

## Restore private body text after a GitHub clone

GitHub contains Master source references, **not** the WordPress article/OCR
body or the catalog database. A new checkout therefore has no source text until
the private bundles are copied from an existing checkout or secure backup.
Run this in the **new** checkout, pointing at the old private bundle directory:

```bash
python3 scripts/sync_private_wordpress_topic_packs.py \
  --source-directory /path/to/old-checkout/data/wordpress_topic_packs \
  --topic-id rtd_temperature_sensor_principle_pt100_wiring_compensation \
  --topic-id thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization \
  --topic-id thermocouple_temperature_sensor_seebeck_reference_junction_compensation
```

The command checks each source ID, URL, type, version and body SHA-256 against
the target Master before copying. It refuses changed bundles rather than
overwriting existing private material. Destination files are Git-ignored with
private permissions. `--verify-only` checks compatibility without writing.
Repeat after approving a newer WordPress source version in Master. The catalog
database is not required to *read* restored bundles; keep it in a separate
private backup if catalog rebuild/OCR is needed. Never commit either the
database or these bundles.
