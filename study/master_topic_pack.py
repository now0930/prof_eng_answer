"""Contracts for additive Master Topic Pack records.

The current Topic Pack remains the grading authority. This module validates
the versioned envelope and will expose read-only projections in later stages.
"""

from __future__ import annotations

from datetime import datetime
import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = "master-topic-pack-v1"
SOURCE_KEYS = {
    "fact_anchor",
    "logic_check",
    "model_answer",
    "topic_importance",
    "question_demand_axes",
}
_REQUIRED_SOURCE_KEYS = SOURCE_KEYS - {"question_demand_axes"}
_SOURCE_TYPES = {
    "wordpress_post",
    "wordpress_page",
    "pdf",
    "image",
    "overleaf",
    "html",
    "other",
}
_VERIFICATION_STATUSES = {"unverified", "verified", "stale", "unavailable"}


class MasterTopicPackError(ValueError):
    """Raised when a Master Topic Pack violates its schema contract."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise MasterTopicPackError(message)


def _valid_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    parts = value.split("/")
    return not value.startswith("/") and all(part not in {"", ".", ".."} for part in parts)


def _valid_uri(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _valid_topic_id(value: Any) -> bool:
    return isinstance(value, str) and len(value) >= 8 and re.fullmatch(
        r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", value
    ) is not None


def _validate_source_reference(source: Any, index: int) -> None:
    prefix = f"sources[{index}]"
    _expect(isinstance(source, dict), f"{prefix} must be an object")
    required = {
        "source_id", "source_type", "wordpress_url", "title", "version",
        "page", "section", "updated_at", "verification_status",
    }
    allowed = required | {"source_url", "training_scope", "content_sha256"}
    _expect(required <= set(source) <= allowed, f"{prefix} fields do not match the source reference contract")
    _expect(isinstance(source["source_id"], str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]*", source["source_id"]) is not None, f"{prefix}.source_id is invalid")
    _expect(source["source_type"] in _SOURCE_TYPES, f"{prefix}.source_type is invalid")
    _expect(isinstance(source["title"], str) and bool(source["title"].strip()), f"{prefix}.title is required")
    _expect(isinstance(source["version"], (str, int)) and not isinstance(source["version"], bool), f"{prefix}.version is invalid")
    _expect(source["page"] is None or isinstance(source["page"], (str, int)), f"{prefix}.page is invalid")
    _expect(source["section"] is None or isinstance(source["section"], str), f"{prefix}.section is invalid")
    _expect(source["verification_status"] in _VERIFICATION_STATUSES, f"{prefix}.verification_status is invalid")
    if "content_sha256" in source:
        _expect(
            isinstance(source["content_sha256"], str)
            and re.fullmatch(r"[0-9a-fA-F]{64}", source["content_sha256"]) is not None,
            f"{prefix}.content_sha256 is invalid",
        )
    url = source["wordpress_url"]
    _expect(url is None or _valid_uri(url), f"{prefix}.wordpress_url must be an HTTP(S) URL or null")
    source_url = source.get("source_url", url)
    _expect(source_url is None or _valid_uri(source_url), f"{prefix}.source_url must be an HTTP(S) URL or null")
    if source["source_type"] in {"wordpress_post", "wordpress_page"}:
        _expect(_valid_uri(url), f"{prefix}.wordpress_url is required for WordPress sources")
    updated_at = source["updated_at"]
    _expect(updated_at is None or isinstance(updated_at, str), f"{prefix}.updated_at is invalid")
    if updated_at is not None:
        try:
            parsed = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise MasterTopicPackError(f"{prefix}.updated_at must be ISO-8601") from exc
        _expect(parsed.tzinfo is not None, f"{prefix}.updated_at must include a timezone")
    scope = source.get("training_scope")
    if scope is not None:
        _expect(isinstance(scope, dict), f"{prefix}.training_scope must be an object")
        _expect(
            set(scope) in (
                {"mode", "reason"},
                {"mode", "reason", "page_ranges"},
                {"mode", "reason", "text_ranges"},
            ),
            f"{prefix}.training_scope fields are invalid",
        )
        _expect(scope.get("mode") in {"include", "exclude", "pages", "text_ranges"}, f"{prefix}.training_scope.mode is invalid")
        _expect(isinstance(scope.get("reason"), str) and bool(scope["reason"].strip()), f"{prefix}.training_scope.reason is required")
        if scope["mode"] == "pages":
            ranges = scope.get("page_ranges")
            _expect(isinstance(ranges, list) and bool(ranges), f"{prefix}.training_scope.page_ranges are required")
            for page_range in ranges:
                _expect(
                    isinstance(page_range, dict)
                    and set(page_range) == {"start", "end"}
                    and type(page_range["start"]) is int
                    and type(page_range["end"]) is int
                    and 1 <= page_range["start"] <= page_range["end"],
                    f"{prefix}.training_scope page range is invalid",
                )
        else:
            _expect("page_ranges" not in scope, f"{prefix}.training_scope.page_ranges require mode=pages")
        if scope["mode"] == "text_ranges":
            ranges = scope.get("text_ranges")
            _expect(isinstance(ranges, list) and bool(ranges), f"{prefix}.training_scope.text_ranges are required")
            for text_range in ranges:
                _expect(
                    isinstance(text_range, dict)
                    and set(text_range) == {"start_marker", "end_marker"}
                    and isinstance(text_range["start_marker"], str)
                    and bool(text_range["start_marker"].strip())
                    and isinstance(text_range["end_marker"], str)
                    and bool(text_range["end_marker"].strip()),
                    f"{prefix}.training_scope text range is invalid",
                )
        else:
            _expect("text_ranges" not in scope, f"{prefix}.training_scope.text_ranges require mode=text_ranges")


def validate_source_reference(source: Any) -> dict[str, Any]:
    """Validate a standalone WordPress/knowledge-source reference."""
    _validate_source_reference(source, 0)
    return source


def validate_master_topic_pack(value: Any) -> dict[str, Any]:
    """Validate and return a Master Topic Pack mapping without mutating it."""
    _expect(isinstance(value, dict), "Master Topic Pack must be an object")
    required = {
        "schema_version", "topic_id", "title_ko", "revision", "legacy_topic_pack",
        "projections", "sources", "source_update_policy",
    }
    optional = {"$schema", "learning_materials", "learning_synthesis"}
    allowed = required | optional
    _expect(required <= set(value) and set(value) <= allowed, "Master Topic Pack fields do not match the contract")
    _expect(value["schema_version"] == SCHEMA_VERSION, "unsupported Master Topic Pack schema_version")
    topic_id = value["topic_id"]
    _expect(_valid_topic_id(topic_id), "topic_id is invalid")
    _expect(isinstance(value["title_ko"], str) and bool(value["title_ko"].strip()), "title_ko is required")
    _expect(isinstance(value["revision"], int) and not isinstance(value["revision"], bool) and value["revision"] >= 1, "revision must be a positive integer")
    if "learning_synthesis" in value:
        from .learning_synthesis import validate_reference, SynthesisError
        try:
            validate_reference(value["learning_synthesis"])
        except SynthesisError as exc:
            raise MasterTopicPackError(str(exc)) from exc
    if "learning_materials" in value:
        material_paths = value["learning_materials"]
        _expect(
            isinstance(material_paths, list)
            and all(_valid_relative_path(path) and path.endswith(".json") for path in material_paths)
            and len(material_paths) == len(set(material_paths)),
            "learning_materials must contain unique safe JSON paths",
        )

    legacy = value["legacy_topic_pack"]
    _expect(isinstance(legacy, dict) and set(legacy) == {"source_root", "source_files"}, "legacy_topic_pack fields are invalid")
    _expect(_valid_relative_path(legacy["source_root"]), "legacy source_root must be a safe relative path")
    files = legacy["source_files"]
    _expect(isinstance(files, dict) and _REQUIRED_SOURCE_KEYS <= set(files) <= SOURCE_KEYS, "legacy source_files are incomplete or contain unknown keys")
    _expect(all(_valid_relative_path(path) for path in files.values()), "legacy source file paths must be safe relative paths")

    projections = value["projections"]
    _expect(isinstance(projections, dict) and set(projections) == {"grading", "training", "diagnosis"}, "all three projections are required")
    grading = projections["grading"]
    _expect(isinstance(grading, dict) and set(grading) == {"projection_id", "authority", "source_keys"}, "grading projection fields are invalid")
    _expect(grading["projection_id"] == "grading-projection-v1" and grading["authority"] == "existing_topic_pack", "grading projection must preserve existing grading authority")
    _expect(isinstance(grading["source_keys"], list) and len(grading["source_keys"]) >= 4 and len(set(grading["source_keys"])) == len(grading["source_keys"]), "grading source_keys are invalid")
    _expect(set(grading["source_keys"]) <= set(files), "grading projection references a missing legacy source")

    training = projections["training"]
    _expect(isinstance(training, dict) and set(training) == {"projection_id", "content_sources", "daily_target"}, "training projection fields are invalid")
    _expect(training["projection_id"] == "training-projection-v1", "unsupported training projection")
    _expect(isinstance(training["content_sources"], list) and len(training["content_sources"]) > 0, "training content_sources are required")
    _expect(set(training["content_sources"]) <= set(files), "training projection references a missing legacy source")
    _expect(isinstance(training["daily_target"], int) and not isinstance(training["daily_target"], bool) and training["daily_target"] >= 1, "daily_target must be positive")

    diagnosis = projections["diagnosis"]
    _expect(isinstance(diagnosis, dict) and set(diagnosis) == {"projection_id", "content_sources", "dimensions"}, "diagnosis projection fields are invalid")
    _expect(diagnosis["projection_id"] == "diagnosis-projection-v1", "unsupported diagnosis projection")
    _expect(isinstance(diagnosis["content_sources"], list) and len(diagnosis["content_sources"]) > 0, "diagnosis content_sources are required")
    _expect(set(diagnosis["content_sources"]) <= set(files), "diagnosis projection references a missing legacy source")
    valid_dimensions = {"format", "content", "reasoning", "application", "verification"}
    _expect(isinstance(diagnosis["dimensions"], list) and len(diagnosis["dimensions"]) >= 2 and set(diagnosis["dimensions"]) <= valid_dimensions, "diagnosis dimensions are invalid")

    _expect(isinstance(value["sources"], list), "sources must be an array")
    source_ids: set[str] = set()
    for index, source in enumerate(value["sources"]):
        _validate_source_reference(source, index)
        _expect(source["source_id"] not in source_ids, "source_id values must be unique within a Topic")
        source_ids.add(source["source_id"])

    policy = value["source_update_policy"]
    _expect(policy == {"mode": "proposal_only", "approval_required": True}, "source updates must require approval")
    return value


def load_legacy_topic_sources(repository_root: str | Path, master: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Load referenced legacy Topic Pack files and verify their ownership."""
    validate_master_topic_pack(master)
    root = Path(repository_root).resolve()
    files = master["legacy_topic_pack"]["source_files"]
    sources: dict[str, dict[str, Any]] = {}
    for key, relative_path in files.items():
        path = (root / relative_path).resolve()
        _expect(path.is_relative_to(root), f"legacy source escapes repository root: {relative_path}")
        _expect(path.is_file(), f"legacy source does not exist: {relative_path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MasterTopicPackError(f"could not read legacy source: {relative_path}") from exc
        _expect(isinstance(payload, dict), f"legacy source must contain a JSON object: {relative_path}")
        _expect(payload.get("topic_id") == master["topic_id"], f"legacy source topic_id mismatch: {relative_path}")
        sources[key] = payload
    return sources


def project_grading(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Return a read-only projection over existing grading source artifacts."""
    sources = load_legacy_topic_sources(repository_root, master)
    projection = master["projections"]["grading"]
    selected = {
        key: copy.deepcopy(sources[key])
        for key in projection["source_keys"]
    }
    return {
        "projection_id": projection["projection_id"],
        "authority": projection["authority"],
        "topic_id": master["topic_id"],
        "sources": selected,
    }


def grading_compatibility_payload(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Expose the source-key mapping expected by legacy grading adapters."""
    return project_grading(repository_root, master)["sources"]


def load_master_topic_pack(path: str | Path) -> dict[str, Any]:
    """Read and validate one versioned Master record."""
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MasterTopicPackError(f"could not read Master Topic Pack: {path}") from exc
    return validate_master_topic_pack(value)


def _as_list(value: Any) -> list[Any]:
    return copy.deepcopy(value) if isinstance(value, list) else []


def _first_list(payload: dict[str, Any], *keys: str) -> list[Any]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return copy.deepcopy(value)
    return []


def project_training(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Build a learner-facing content view without generating or grading answers."""
    sources = load_legacy_topic_sources(repository_root, master)
    config = master["projections"]["training"]
    sources = {key: sources[key] for key in config["content_sources"]}
    fact_anchor = sources.get("fact_anchor", {})
    model_answer = sources.get("model_answer", {})
    topic_importance = sources.get("topic_importance", {})
    raw_source_materials = _load_linked_wordpress_materials(repository_root, master)
    source_materials, excluded_source_references = _apply_training_source_scopes(
        raw_source_materials, master["sources"]
    )
    learning_materials = _load_curated_learning_materials(repository_root, master, source_materials)
    from .learning_synthesis import synthesis_for_training
    synthesis = synthesis_for_training(repository_root, master, raw_source_materials, learning_materials)
    return {
        **({"learning_synthesis": synthesis} if synthesis is not None else {}),
        "projection_id": config["projection_id"],
        "topic_id": master["topic_id"],
        "title_ko": master["title_ko"],
        "daily_target": config["daily_target"],
        "source_references": copy.deepcopy(master["sources"]),
        # WordPress HTML and first-party PDF/image extraction stay as
        # provenance-bearing study material, separate from Grading sources.
        "source_materials": source_materials,
        "excluded_source_references": excluded_source_references,
        "curated_learning_materials": copy.deepcopy(learning_materials),
        "source_review_annotations": _load_source_review_annotations(repository_root, master, source_materials),
        "question_examples": _first_list(model_answer, "question_examples"),
        "question_patterns": _first_list(model_answer, "expected_question_patterns", "question_patterns"),
        "recommended_outline": _first_list(model_answer, "recommended_outline", "expected_structure"),
        "fact_anchors": _first_list(fact_anchor, "anchors", "core_facts"),
        "high_score_points": _first_list(model_answer, "high_score_points", "high_score_features"),
        "common_missing_points": _first_list(model_answer, "common_missing_points"),
        "high_band_unlock_conditions": _as_list(topic_importance.get("high_band_unlock_conditions")),
    }


def _apply_training_source_scopes(source_materials, source_references):
    """Apply score-neutral source-use scope to learner-visible raw materials.

    Raw material hashes/evidence are validated before this projection. The
    original Master references are retained, while excluded or out-of-scope
    text is omitted only from the Training View.
    """
    references = {row["source_id"]: row for row in source_references}
    included = []
    excluded = []
    seen_sources = set()
    for material in source_materials:
        reference = references[material["source_id"]]
        seen_sources.add(material["source_id"])
        scope = reference.get("training_scope", {"mode": "include", "reason": "legacy default: include linked source"})
        mode = scope["mode"]
        if mode == "exclude":
            excluded.append({**copy.deepcopy(reference), "exclusion_reason": scope["reason"]})
            continue
        projected = copy.deepcopy(material)
        if mode == "pages":
            if material["source_type"] != "pdf":
                excluded.append({**copy.deepcopy(reference), "exclusion_reason": "page-scoped Training material is supported only for PDF sources"})
                continue
            selected_text = _select_pdf_pages(material["text"], scope["page_ranges"])
            if selected_text is None:
                excluded.append({**copy.deepcopy(reference), "exclusion_reason": "PDF page markers did not permit safe scope extraction"})
                continue
            projected["text"] = selected_text
            projected["training_text_sha256"] = hashlib.sha256(selected_text.encode("utf-8")).hexdigest()
            projected["training_scope"] = copy.deepcopy(scope)
        elif mode == "text_ranges":
            selected_text = _select_text_ranges(material["text"], scope["text_ranges"])
            if selected_text is None:
                excluded.append({**copy.deepcopy(reference), "exclusion_reason": "Text range markers were missing, duplicated, or out of order"})
                continue
            projected["text"] = selected_text
            projected["training_text_sha256"] = hashlib.sha256(selected_text.encode("utf-8")).hexdigest()
            projected["training_scope"] = copy.deepcopy(scope)
        included.append(projected)
    for source_id, reference in references.items():
        if source_id in seen_sources:
            continue
        scope = reference.get("training_scope")
        if scope and scope["mode"] == "exclude":
            excluded.append({**copy.deepcopy(reference), "exclusion_reason": scope["reason"]})
        elif scope and scope["mode"] in {"pages", "text_ranges"}:
            excluded.append({**copy.deepcopy(reference), "exclusion_reason": "scoped source text is unavailable for safe projection"})
    return included, excluded


def _select_pdf_pages(text, page_ranges):
    """Select exact [Page N] blocks; fail closed when page boundaries are absent."""
    matches = list(re.finditer(r"(?m)^\[Page\s+(\d+)\]\s*", text))
    if not matches:
        return None
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        page_number = int(match.group(1))
        if any(item["start"] <= page_number <= item["end"] for item in page_ranges):
            blocks.append(text[match.start():end].strip())
    return "\n\n".join(blocks) if blocks else None


def _select_text_ranges(text, text_ranges):
    """Select uniquely delimited text blocks; ambiguous boundaries fail closed."""
    selected = []
    previous_end = -1
    for item in text_ranges:
        start_marker, end_marker = item["start_marker"], item["end_marker"]
        if text.count(start_marker) != 1 or text.count(end_marker) != 1:
            return None
        start = text.find(start_marker)
        end = text.find(end_marker)
        if start < previous_end or end <= start:
            return None
        selected.append(text[start:end].strip())
        previous_end = end + len(end_marker)
    return "\n\n".join(selected) if selected else None


def _load_curated_learning_materials(
    repository_root: str | Path,
    master: dict[str, Any],
    source_materials: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Load score-neutral curated material pinned to linked source text."""
    root = Path(repository_root).resolve()
    linked = {
        item["source_id"]: item
        for item in master["sources"]
        if item["source_type"] in {"wordpress_post", "wordpress_page"}
    }
    raw_by_id = {item["source_id"]: item for item in source_materials}
    result: list[dict[str, Any]] = []
    material_ids: set[str] = set()
    for relative_path in master.get("learning_materials", []):
        path = (root / relative_path).resolve()
        _expect(path.is_relative_to(root), "learning material path escapes repository root")
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MasterTopicPackError(f"could not read curated learning material: {relative_path}") from exc
        _expect(isinstance(pack, dict), "learning material pack must be an object")
        _expect(pack.get("schema_version") == "topic-learning-material-v1", "unsupported learning material schema")
        _expect(pack.get("topic_id") == master["topic_id"], "learning material topic_id mismatch")
        items = pack.get("materials")
        _expect(isinstance(items, list), "learning material materials must be an array")
        for item in items:
            _expect(isinstance(item, dict), "learning material item must be an object")
            required = {
                "material_id", "material_type", "title", "review_status", "source",
                "learning_objective", "assumptions", "steps", "result", "self_check",
                "diagnostic_cues", "score_effect",
            }
            _expect(set(item) == required, "learning material item fields are invalid")
            material_id = item["material_id"]
            _expect(isinstance(material_id, str) and re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", material_id) is not None, "material_id is invalid")
            _expect(material_id not in material_ids, "duplicate curated learning material ID")
            material_ids.add(material_id)
            _expect(item["material_type"] in {"worked_example", "study_note"}, "learning material type is invalid")
            _expect(item["review_status"] in {"llm_reviewed_human_pending", "human_verified"}, "learning material review status is invalid")
            _expect(item["score_effect"] == "none", "learning material must have no score effect")
            for field in ("title", "learning_objective", "result"):
                _expect(isinstance(item[field], str) and bool(item[field].strip()), f"learning material {field} is required")
            for field in ("assumptions", "steps", "self_check", "diagnostic_cues"):
                _expect(isinstance(item[field], list) and len(item[field]) > 0, f"learning material {field} must be non-empty")
            _expect(all(isinstance(value, str) and value.strip() for value in item["assumptions"] + item["steps"] + item["diagnostic_cues"]), "learning material text lists must contain non-empty strings")
            evidence = item["source"]
            _expect(
                isinstance(evidence, dict)
                and set(evidence) == {"source_id", "source_url", "source_version", "source_content_sha256", "locator", "excerpt"},
                "learning material source evidence fields are invalid",
            )
            source = linked.get(evidence["source_id"])
            _expect(source is not None, "learning material source is not linked to this Topic")
            scope = source.get("training_scope", {"mode": "include"})
            _expect(scope["mode"] == "include", "curated material source is excluded from Training scope")
            _expect(evidence["source_url"] == source["wordpress_url"], "learning material source URL mismatch")
            _expect(evidence["source_version"] == source["version"], "learning material source version mismatch")
            raw_source = raw_by_id.get(evidence["source_id"])
            bundle = root / "data" / "wordpress_topic_packs" / f"{master['topic_id']}.json"
            _expect(
                raw_source is not None or not bundle.is_file(),
                "curated material source text is missing from the private bundle",
            )
            if raw_source is not None:
                _expect(evidence["source_content_sha256"] == raw_source["content_sha256"], "learning material source text hash mismatch")
            _expect(isinstance(evidence["locator"], str) and bool(evidence["locator"].strip()), "learning material source locator is required")
            _expect(isinstance(evidence["excerpt"], str) and bool(evidence["excerpt"].strip()), "learning material evidence excerpt is required")
            if raw_source is not None:
                _expect(evidence["excerpt"] in raw_source["text"], "learning material evidence excerpt is not in the linked source")
            checks = item["self_check"]
            _expect(
                all(isinstance(check, dict) and set(check) == {"question", "answer"}
                    and isinstance(check["question"], str) and check["question"].strip()
                    and isinstance(check["answer"], str) and check["answer"].strip()
                    for check in checks),
                "learning material self_check entries are invalid",
            )
            projected = copy.deepcopy(item)
            projected["source_text_state"] = "verified_against_bundle" if raw_source is not None else "private_bundle_unavailable"
            result.append(projected)
    return result


def _load_linked_wordpress_materials(
    repository_root: str | Path, master: dict[str, Any]
) -> list[dict[str, Any]]:
    """Expose only extracted WordPress text already linked to this Topic.

    Source text is unverified input, not canonical facts. The projection
    preserves the original text and its hash so a learner/reviewer can inspect
    the source; it never feeds the Grading Projection.
    """
    root = Path(repository_root).resolve()
    bundle = (root / "data" / "wordpress_topic_packs" / f"{master['topic_id']}.json").resolve()
    _expect(bundle.is_relative_to(root), "WordPress Topic Pack path escapes repository root")
    if not bundle.is_file():
        return []
    try:
        payload = json.loads(bundle.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MasterTopicPackError(f"could not read WordPress Topic Pack: {bundle}") from exc
    _expect(isinstance(payload, dict), "WordPress Topic Pack must be an object")
    _expect(payload.get("topic_id") == master["topic_id"], "WordPress Topic Pack topic_id mismatch")
    _expect(payload.get("private") is True, "WordPress Topic Pack must remain private")
    linked = {source["source_id"]: source for source in master["sources"]}
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    rows = payload.get("sources")
    _expect(isinstance(rows, list), "WordPress Topic Pack sources must be an array")
    for item in rows:
        if not isinstance(item, dict) or item.get("source_id") not in linked:
            continue
        source_id = item["source_id"]
        _expect(source_id not in seen, "duplicate WordPress source ID in Topic Pack")
        seen.add(source_id)
        reference = linked[source_id]
        _expect(
            item.get("source_type") == reference["source_type"],
            "WordPress source type does not match Master reference",
        )
        if reference["source_type"] in {"pdf", "image"} and (
            item.get("version") != reference["version"]
            or item.get("source_url", item.get("wordpress_url"))
            != reference.get("source_url", reference["wordpress_url"])
        ):
            # Changed attachments are source-update proposals, not approved
            # learning material. Exclude them until the Master is updated.
            continue
        _expect(item.get("topic_id", master["topic_id"]) == master["topic_id"], "WordPress source topic_id mismatch")
        _expect(item.get("wordpress_url") == reference["wordpress_url"], "WordPress source URL does not match Master reference")
        _expect(item.get("version") == reference["version"], "WordPress source version does not match Master reference")
        _expect(
            item.get("source_url", item.get("wordpress_url"))
            == reference.get("source_url", reference["wordpress_url"]),
            "WordPress exact source URL does not match Master reference",
        )
        if reference["source_type"] in {"pdf", "image"}:
            article_host = urlparse(reference["wordpress_url"]).hostname
            asset_url = urlparse(item.get("source_url", ""))
            _expect(
                asset_url.scheme in {"http", "https"}
                and asset_url.hostname == article_host
                and "/wp-content/uploads/" in asset_url.path,
                "WordPress PDF/image must be a first-party uploaded asset",
            )
        text = item.get("extracted_text")
        if item.get("extraction_status") != "extracted" or not isinstance(text, str) or not text.strip():
            continue
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        declared_digest = item.get("extracted_text_sha256")
        _expect(declared_digest == digest, "WordPress extracted text hash mismatch")
        extraction_methods = {
            "wordpress_post": {"wordpress_wxr_html", "wordpress_rest_html"},
            "wordpress_page": {"wordpress_wxr_html", "wordpress_rest_html"},
            "pdf": {"pdftotext", "pdftotext+tesseract_ocr", "tesseract_ocr", "llm_ocr"},
            "image": {"tesseract_ocr", "llm_ocr"},
            "html": {"wordpress_wxr_html", "wordpress_rest_html", "html_text"},
        }
        _expect(
            item.get("extraction_method") in extraction_methods.get(reference["source_type"], set()),
            "unsupported WordPress text extraction method for source type",
        )
        result.append({
            "source_id": source_id,
            "source_type": reference["source_type"],
            "wordpress_url": reference["wordpress_url"],
            "source_url": item.get("source_url", reference.get("source_url", reference["wordpress_url"])),
            "title": reference["title"],
            "version": reference["version"],
            "updated_at": reference["updated_at"],
            "extraction_method": item["extraction_method"],
            "content_sha256": digest,
            "verification_status": reference["verification_status"],
            "content_trust": payload.get("content_trust", "untrusted_source_text"),
            "text": text,
        })
    return result


def _load_source_review_annotations(repository_root, master, source_materials):
    """Keep unresolved editorial comments separate from source text and facts."""
    root = Path(repository_root).resolve()
    path = (root / "study/source_review_annotations" / f"{master['topic_id']}.json").resolve()
    _expect(path.is_relative_to(root), "annotation path escapes repository root")
    if not path.is_file():
        return []
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MasterTopicPackError("could not read source review annotations") from exc
    _expect(isinstance(pack, dict) and set(pack) == {"schema_version", "topic_id", "annotations"}, "annotation pack fields are invalid")
    _expect(pack["schema_version"] == "source-review-annotations-v1" and pack["topic_id"] == master["topic_id"], "annotation pack identity mismatch")
    _expect(isinstance(pack["annotations"], list), "annotations must be an array")
    references = {row["source_id"]: row for row in master["sources"]}
    materials = {row["source_id"]: row for row in source_materials}
    result, seen = [], set()
    for note in pack["annotations"]:
        fields = {"annotation_id", "source_id", "source_version", "source_text_sha256", "locator", "quote", "review_note", "status", "decision", "score_effect"}
        _expect(isinstance(note, dict) and set(note) == fields, "annotation fields are invalid")
        for key in fields - {"decision"}:
            _expect(isinstance(note[key], str) and bool(note[key].strip()), f"annotation {key} is required")
        _expect(note["annotation_id"] not in seen, "duplicate annotation ID")
        seen.add(note["annotation_id"])
        _expect(note["status"] == "pending_review" and note["decision"] is None and note["score_effect"] == "none", "annotations must remain undecided and score-neutral")
        _expect(re.fullmatch(r"[a-f0-9]{64}", note["source_text_sha256"]) is not None, "invalid annotation text hash")
        reference = references.get(note["source_id"])
        _expect(reference is not None, "annotation source is not linked to Master")
        material = materials.get(note["source_id"])
        state = "text_unavailable"
        if reference["version"] != note["source_version"]:
            state = "stale"
        elif material is not None:
            state = "matching" if material["content_sha256"] == note["source_text_sha256"] else "stale"
            if state == "matching":
                _expect(note["quote"] in material["text"], "annotation quote does not match source text")
        result.append({**copy.deepcopy(note), "source_url": reference.get("source_url", reference["wordpress_url"]), "source_state": state})
    return result


def project_diagnosis(repository_root: str | Path, master: dict[str, Any]) -> dict[str, Any]:
    """Expose structured diagnosis inputs without scoring or changing grader output."""
    sources = load_legacy_topic_sources(repository_root, master)
    config = master["projections"]["diagnosis"]
    sources = {key: sources[key] for key in config["content_sources"]}
    fact_anchor = sources.get("fact_anchor", {})
    logic_check = sources.get("logic_check", {})
    model_answer = sources.get("model_answer", {})
    source_materials = _load_linked_wordpress_materials(repository_root, master)
    learning_materials = _load_curated_learning_materials(repository_root, master, source_materials)
    from .learning_feedback import navigation_view
    navigation = navigation_view(repository_root, master, source_materials, learning_materials)
    return {
        **({"learning_navigation": navigation} if navigation is not None else {}),
        "projection_id": config["projection_id"],
        "topic_id": master["topic_id"],
        "title_ko": master["title_ko"],
        "dimensions": list(config["dimensions"]),
        "source_review_annotations": _load_source_review_annotations(repository_root, master, source_materials),
        "source_references": copy.deepcopy(master["sources"]),
        "fact_anchors": _first_list(fact_anchor, "anchors", "core_facts"),
        "fatal_wrong_claims": _first_list(fact_anchor, "fatal_wrong_claims"),
        "deterministic_checks": _first_list(logic_check, "deterministic_checks"),
        "diagnostic_guidance": copy.deepcopy(logic_check.get("llm_profile", {}))
        if isinstance(logic_check.get("llm_profile"), dict) else {},
        "common_missing_points": _first_list(model_answer, "common_missing_points"),
        "recommended_materials": [
            {
                "material_id": item["material_id"],
                "material_type": item["material_type"],
                "title": item["title"],
                "review_status": item["review_status"],
                "source_id": item["source"]["source_id"],
                "source_url": item["source"]["source_url"],
            }
            for item in learning_materials
        ],
        "score_effect": "none",
    }
