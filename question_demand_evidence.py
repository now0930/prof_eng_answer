from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import math
import re
import unicodedata

QUESTION_DEMAND_EVIDENCE_VERSION = "QUESTION_DEMAND_EVIDENCE_V1"
QUESTION_DEMAND_EVIDENCE_FILENAME = "question_demand_evidence_shadow.json"

QUESTION_DEMAND_ANCHOR_MAPPING_DIR = "question_demand_evidence_maps"


def _load_explicit_demand_anchor_mapping(
    repo_dir: Path,
    demands: list[dict[str, Any]],
    routing: dict[str, Any],
) -> dict[str, Any] | None:
    mapping_dir = (
        repo_dir
        / "calibration"
        / QUESTION_DEMAND_ANCHOR_MAPPING_DIR
    )

    if not mapping_dir.exists():
        return None

    expected_topics = list(
        routing["primary_topic_ids"]
    )
    expected_demands = [
        {
            "demand_id": row["demand_id"],
            "text": row["text"],
        }
        for row in demands
    ]

    matches: list[dict[str, Any]] = []

    for path in sorted(
        mapping_dir.glob("*.json")
    ):
        payload = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        if not isinstance(payload, dict):
            continue

        if payload.get("version") != (
            "QUESTION_DEMAND_ANCHOR_MAPPING_V1"
        ):
            continue

        if payload.get(
            "primary_topic_ids"
        ) != expected_topics:
            continue

        raw_demands = payload.get(
            "demands"
        )

        if not isinstance(
            raw_demands,
            list,
        ):
            continue

        identity = [
            {
                "demand_id": str(
                    row.get("demand_id")
                    or ""
                ).strip(),
                "text": str(
                    row.get("text")
                    or ""
                ).strip(),
            }
            for row in raw_demands
            if isinstance(row, dict)
        ]

        if identity != expected_demands:
            continue

        matches.append(
            {
                "path": path,
                "payload": payload,
            }
        )

    if len(matches) > 1:
        raise ValueError(
            "multiple exact Question Demand "
            "anchor mappings matched"
        )

    if not matches:
        return None

    return matches[0]

_STOP_TOKENS = {
    "대해", "대한", "설명", "설명하시오", "설명하시요", "제시", "기준",
    "및", "와", "과", "의", "를", "을", "이", "가", "은", "는",
    "으로", "에서", "것",
    "for", "and", "the", "of", "to", "a", "an", "in", "on",
    "with", "by",
}

_TEXT_KEYS = (
    "anchor",
    "text",
    "fact",
    "statement",
    "description",
    "claim",
    "name",
    "title",
    "requirement",
    "summary",
    "criterion",
)


def _walk(value: Any, path: str = "$", depth: int = 0):
    if depth > 30:
        return
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}", depth + 1)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]", depth + 1)


def _normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).lower()
    text = re.sub(r"[^0-9a-zA-Z가-힣_+\-/]+", " ", text)
    return " ".join(text.split())


def _tokens(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(
            r"[0-9a-zA-Z가-힣_+\-/]+",
            _normalize_text(value),
        )
        if len(token) >= 2 and token not in _STOP_TOKENS
    }


def _anchor_id(anchor: Any, fallback_index: int) -> str:
    if isinstance(anchor, dict):
        for key in ("anchor_id", "id", "key", "code"):
            value = anchor.get(key)
            if isinstance(value, (str, int)):
                text = str(value).strip()
                if text:
                    return text
    return f"A{fallback_index + 1}"


def _best_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""

    for key in _TEXT_KEYS:
        item = value.get(key)
        if isinstance(item, str) and item.strip():
            return item.strip()

    candidates: list[tuple[int, int, str]] = []
    for path, item in _walk(value):
        if not isinstance(item, str):
            continue
        text = item.strip()
        if len(text) < 4:
            continue
        leaf = path.rsplit(".", 1)[-1].lower()
        priority = 0 if any(
            key == leaf or key in leaf
            for key in _TEXT_KEYS
        ) else 1
        candidates.append((priority, -len(text), text))

    if not candidates:
        return ""
    candidates.sort()
    return candidates[0][2]


def _demand_id(demand: dict[str, Any], index: int) -> str:
    for key in ("demand_id", "id"):
        value = demand.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return f"D{index + 1}"


def _demand_text(demand: dict[str, Any]) -> str:
    for key in (
        "text",
        "demand",
        "description",
        "requirement",
        "statement",
    ):
        value = demand.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    string_values = [
        str(value).strip()
        for value in demand.values()
        if isinstance(value, str)
        and len(value.strip()) >= 20
        and not re.fullmatch(r"D\d+", value.strip())
    ]

    if not string_values:
        return ""
    return max(string_values, key=len)


def _extract_demands(payload: Any) -> list[dict[str, Any]]:
    candidates: list[list[dict[str, Any]]] = []

    for path, value in _walk(payload):
        leaf = path.rsplit(".", 1)[-1].lower()
        if leaf != "demands":
            continue
        if not isinstance(value, list) or not value:
            continue
        if not all(isinstance(row, dict) for row in value):
            continue
        candidates.append(value)

    if len(candidates) != 1:
        raise ValueError(
            "canonical Question Demand demands path must resolve uniquely"
        )

    rows: list[dict[str, Any]] = []
    for index, demand in enumerate(candidates[0]):
        demand_id = _demand_id(demand, index)
        text = _demand_text(demand)

        if not text:
            raise ValueError(f"{demand_id}: demand text unresolved")

        rows.append(
            {
                "demand_id": demand_id,
                "text": text,
            }
        )

    return rows


def _question_demand_cache_path(
    repo_dir: Path,
    question_text: str,
) -> Path:
    import question_demand_shadow as qds

    key = qds.question_demand_cache_key(question_text)

    if isinstance(key, Path):
        filename = key.name
    else:
        filename = Path(str(key)).name

    if not filename.endswith(".json"):
        filename = f"{filename}.json"

    return (
        repo_dir
        / "calibration"
        / "question_demand_contracts"
        / filename
    )


def _load_canonical_demands(
    repo_dir: Path,
    question_text: str,
) -> tuple[Path, list[dict[str, Any]]]:
    path = _question_demand_cache_path(repo_dir, question_text)

    if not path.exists():
        raise FileNotFoundError(
            f"canonical Question Demand missing: {path}"
        )

    payload = json.loads(path.read_text(encoding="utf-8"))
    return path, _extract_demands(payload)


def _load_routing(session_dir: Path) -> dict[str, Any]:
    path = session_dir / "semantic_router_shadow.json"

    if not path.exists():
        raise FileNotFoundError(
            f"semantic router artifact missing: {path}"
        )

    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise ValueError("semantic router artifact root must be object")

    mode = str(payload.get("routing_mode") or "").strip().upper()

    if mode not in {"SINGLE_TOPIC", "MULTI_TOPIC"}:
        raise ValueError(f"unsupported shadow routing mode: {mode}")

    topic_ids: list[str] = []
    for value in payload.get("primary_topic_ids") or []:
        if not isinstance(value, str):
            continue
        topic_id = value.strip()
        if topic_id and topic_id not in topic_ids:
            topic_ids.append(topic_id)

    if mode == "SINGLE_TOPIC" and len(topic_ids) != 1:
        raise ValueError("SINGLE_TOPIC must contain one primary topic")

    if mode == "MULTI_TOPIC" and len(topic_ids) < 2:
        raise ValueError("MULTI_TOPIC must contain >=2 primary topics")

    demand_map: dict[str, list[str]] = {}
    mappings = payload.get("demand_mappings")

    if isinstance(mappings, list):
        for row in mappings:
            if not isinstance(row, dict):
                continue

            demand_id = str(row.get("demand_id") or "").strip()
            topic_id = str(row.get("topic_id") or "").strip()

            if demand_id and topic_id in topic_ids:
                demand_map.setdefault(demand_id, [])
                if topic_id not in demand_map[demand_id]:
                    demand_map[demand_id].append(topic_id)

    return {
        "path": path,
        "routing_mode": mode,
        "primary_topic_ids": topic_ids,
        "demand_topic_map": demand_map,
    }


def _load_topic_assets(
    repo_dir: Path,
    topic_id: str,
) -> dict[str, Any]:
    root = repo_dir / "rubrics" / "topic_packs" / topic_id
    fact_path = root / "fact_anchor.json"
    model_path = root / "model_answer.json"

    if not fact_path.exists():
        raise FileNotFoundError(f"fact_anchor.json missing: {fact_path}")

    if not model_path.exists():
        raise FileNotFoundError(f"model_answer.json missing: {model_path}")

    fact_payload = json.loads(fact_path.read_text(encoding="utf-8"))
    model_payload = json.loads(model_path.read_text(encoding="utf-8"))

    anchors = fact_payload.get("anchors")
    if not isinstance(anchors, list):
        raise ValueError(f"{topic_id}: anchors missing")

    anchor_rows: list[dict[str, Any]] = []

    for index, anchor in enumerate(anchors):
        anchor_rows.append(
            {
                "anchor_id": _anchor_id(anchor, index),
                "text": _best_text(anchor),
            }
        )

    patterns: list[dict[str, Any]] = []

    for field in ("expected_question_patterns", "recommended_outline"):
        value = model_payload.get(field)

        if not isinstance(value, list):
            continue

        for index, item in enumerate(value):
            item_text = _best_text(item)
            refs: list[str] = []

            if isinstance(item, dict):
                for key, ref_value in item.items():
                    if "anchor" not in key.lower():
                        continue

                    if isinstance(ref_value, (str, int)):
                        ref = str(ref_value).strip()
                        if ref:
                            refs.append(ref)

                    elif isinstance(ref_value, list):
                        for ref_item in ref_value:
                            if not isinstance(ref_item, (str, int)):
                                continue
                            ref = str(ref_item).strip()
                            if ref:
                                refs.append(ref)

            patterns.append(
                {
                    "source_field": field,
                    "index": index,
                    "text": item_text,
                    "anchor_refs": list(dict.fromkeys(refs)),
                }
            )

    return {
        "topic_id": topic_id,
        "anchors": anchor_rows,
        "patterns": patterns,
    }


def _rank_pattern_links(
    demand_text: str,
    topic_assets: dict[str, Any],
) -> dict[str, Any]:
    demand_tokens = _tokens(demand_text)

    ranked: list[dict[str, Any]] = []

    for row in topic_assets["patterns"]:
        shared = sorted(demand_tokens & _tokens(row["text"]))
        ranked.append({**row, "shared_tokens": shared})

    max_shared = max(
        [len(row["shared_tokens"]) for row in ranked] or [0]
    )

    best_patterns = [
        row
        for row in ranked
        if max_shared > 0
        and len(row["shared_tokens"]) == max_shared
    ]

    linked_refs: list[str] = []
    for row in best_patterns:
        for ref in row["anchor_refs"]:
            if ref not in linked_refs:
                linked_refs.append(ref)

    if linked_refs:
        return {
            "method": "model_pattern_anchor_refs",
            "max_shared_tokens": max_shared,
            "anchor_ids": linked_refs,
        }

    anchor_ranked: list[dict[str, Any]] = []

    for anchor in topic_assets["anchors"]:
        shared = sorted(demand_tokens & _tokens(anchor["text"]))
        anchor_ranked.append(
            {
                "anchor_id": anchor["anchor_id"],
                "shared_tokens": shared,
            }
        )

    max_anchor_shared = max(
        [len(row["shared_tokens"]) for row in anchor_ranked] or [0]
    )

    anchor_ids = [
        row["anchor_id"]
        for row in anchor_ranked
        if max_anchor_shared > 0
        and len(row["shared_tokens"]) == max_anchor_shared
    ]

    return {
        "method": (
            "max_token_overlap_anchors"
            if anchor_ids
            else "unlinked"
        ),
        "max_shared_tokens": max_anchor_shared,
        "anchor_ids": anchor_ids,
    }


def _result_anchor_id(row: Any) -> str:
    if not isinstance(row, dict):
        return ""

    for path, value in _walk(row):
        leaf = path.rsplit(".", 1)[-1].lower()

        if leaf not in {"anchor_id", "id"}:
            continue

        if isinstance(value, (str, int)):
            text = str(value).strip()
            if text:
                return text

    return ""


def _result_level(row: Any) -> float:
    if not isinstance(row, dict):
        return 0.0

    for key in ("level", "anchor_level"):
        value = row.get(key)

        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(float(value))
        ):
            return max(0.0, min(1.0, float(value)))

    return 0.0


def _result_has_evidence(row: Any) -> bool:
    if not isinstance(row, dict):
        return False

    for path, value in _walk(row):
        leaf = path.rsplit(".", 1)[-1].lower()

        if not any(
            token in leaf
            for token in ("evidence", "excerpt", "matched_text")
        ):
            continue

        if isinstance(value, str) and value.strip():
            return True

    return False


def _build_fact_result_index(
    fact_evaluation: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    anchors = fact_evaluation.get("anchors")

    if not isinstance(anchors, list):
        raise ValueError("fact_evaluation.anchors missing")

    result: dict[str, dict[str, Any]] = {}

    for row in anchors:
        anchor_id = _result_anchor_id(row)

        if not anchor_id:
            continue

        result[anchor_id] = {
            "level": _result_level(row),
            "has_evidence": _result_has_evidence(row),
            "text": _best_text(row),
        }

    return result


def build_question_demand_evidence_shadow(
    *,
    question_text: str,
    fact_evaluation: dict[str, Any],
    session_dir: str | Path,
    repo_dir: str | Path | None = None,
) -> dict[str, Any]:
    repo = (
        Path(repo_dir)
        if repo_dir is not None
        else Path(__file__).resolve().parent
    )
    session = Path(session_dir)

    canonical_path, demands = _load_canonical_demands(
        repo,
        question_text,
    )
    routing = _load_routing(session)

    topic_assets = {
        topic_id: _load_topic_assets(repo, topic_id)
        for topic_id in routing["primary_topic_ids"]
    }

    fact_index = _build_fact_result_index(fact_evaluation)

    explicit_match = _load_explicit_demand_anchor_mapping(
        repo,
        demands,
        routing,
    )

    explicit_rows: dict[str, dict[str, Any]] = {}

    if explicit_match is not None:
        explicit_rows = {
            str(row.get("demand_id") or "").strip(): row
            for row in explicit_match["payload"]["demands"]
            if isinstance(row, dict)
        }

    demand_rows: list[dict[str, Any]] = []

    for demand in demands:
        demand_id = demand["demand_id"]

        explicit_row = explicit_rows.get(
            demand_id
        )

        linked_anchor_ids: list[str] = []
        linkage: list[dict[str, Any]] = []

        if explicit_row is not None:
            demand_topic_ids = list(
                explicit_row.get("topic_ids")
                or []
            )

            if not demand_topic_ids:
                raise ValueError(
                    f"{demand_id}: explicit topic owner missing"
                )

            if any(
                topic_id
                not in routing["primary_topic_ids"]
                for topic_id in demand_topic_ids
            ):
                raise ValueError(
                    f"{demand_id}: explicit topic owner "
                    "outside routed topic set"
                )

            explicit_anchor_ids = list(
                explicit_row.get("anchor_ids")
                or []
            )

            for topic_id in demand_topic_ids:
                valid_ids = {
                    row["anchor_id"]
                    for row in topic_assets[
                        topic_id
                    ]["anchors"]
                }

                anchor_ids = [
                    anchor_id
                    for anchor_id in explicit_anchor_ids
                    if anchor_id in valid_ids
                ]

                invalid_ids = [
                    anchor_id
                    for anchor_id in explicit_anchor_ids
                    if anchor_id not in valid_ids
                ]

                if invalid_ids:
                    raise ValueError(
                        f"{demand_id}: explicit anchors "
                        f"outside topic {topic_id}: "
                        f"{invalid_ids}"
                    )

                for anchor_id in anchor_ids:
                    if anchor_id not in linked_anchor_ids:
                        linked_anchor_ids.append(anchor_id)

                linkage.append(
                    {
                        "topic_id": topic_id,
                        "method": (
                            "explicit_semantic_mapping_v1"
                        ),
                        "max_shared_tokens": None,
                        "anchor_ids": anchor_ids,
                    }
                )

        else:
            if routing["routing_mode"] == "SINGLE_TOPIC":
                demand_topic_ids = list(
                    routing["primary_topic_ids"]
                )
            else:
                demand_topic_ids = list(
                    routing[
                        "demand_topic_map"
                    ].get(
                        demand_id,
                        [],
                    )
                )

            for topic_id in demand_topic_ids:
                link = _rank_pattern_links(
                    demand["text"],
                    topic_assets[topic_id],
                )

                valid_ids = {
                    row["anchor_id"]
                    for row in topic_assets[
                        topic_id
                    ]["anchors"]
                }

                anchor_ids = [
                    anchor_id
                    for anchor_id in link[
                        "anchor_ids"
                    ]
                    if anchor_id in valid_ids
                ]

                for anchor_id in anchor_ids:
                    if anchor_id not in linked_anchor_ids:
                        linked_anchor_ids.append(anchor_id)

                linkage.append(
                    {
                        "topic_id": topic_id,
                        "method": link["method"],
                        "max_shared_tokens": (
                            link[
                                "max_shared_tokens"
                            ]
                        ),
                        "anchor_ids": anchor_ids,
                    }
                )

        observed = [
            {
                "anchor_id": anchor_id,
                **fact_index[anchor_id],
            }
            for anchor_id in linked_anchor_ids
            if anchor_id in fact_index
        ]

        levels = [
            fact_index.get(
                anchor_id,
                {
                    "level": 0.0,
                },
            )["level"]
            for anchor_id in linked_anchor_ids
        ]

        demand_level = (
            sum(levels) / len(levels)
            if levels
            else 0.0
        )

        covered = any(
            level > 0.0
            for level in levels
        )

        verified = any(
            row["level"] > 0.0
            and row["has_evidence"]
            for row in observed
        )

        demand_rows.append(
            {
                "demand_id": demand_id,
                "text": demand["text"],
                "required": True,
                "topic_ids": demand_topic_ids,
                "linkage": linkage,
                "linked_anchor_ids": linked_anchor_ids,
                "linked_anchor_count": len(linked_anchor_ids),
                "observed_anchor_count": len(observed),
                "covered": covered,
                "verified": verified,
                "level": round(demand_level, 6),
                "observed_anchors": observed,
            }
        )

    total = len(demand_rows)
    linked_count = sum(
        1 for row in demand_rows if row["linked_anchor_count"] > 0
    )
    covered_count = sum(
        1 for row in demand_rows if row["covered"]
    )
    verified_count = sum(
        1 for row in demand_rows if row["verified"]
    )
    mean_level = (
        sum(row["level"] for row in demand_rows) / total
        if total
        else 0.0
    )

    return {
        "version": QUESTION_DEMAND_EVIDENCE_VERSION,
        "status": "shadow_only",
        "score_effect": "none",
        "question_demand_source": str(canonical_path),
        "routing_source": str(routing["path"]),
        "routing_mode": routing["routing_mode"],
        "primary_topic_ids": routing["primary_topic_ids"],
        "explicit_mapping": (
            str(explicit_match["path"])
            if explicit_match is not None
            else None
        ),
        "level_aggregation": (
            "mean_linked_anchor_levels"
        ),
        "demand_count": total,
        "demands": demand_rows,
        "summary": {
            "linked_ratio": round(
                linked_count / total if total else 0.0,
                6,
            ),
            "covered_ratio": round(
                covered_count / total if total else 0.0,
                6,
            ),
            "verified_ratio": round(
                verified_count / total if total else 0.0,
                6,
            ),
            "mean_demand_level": round(mean_level, 6),
        },
    }


def write_question_demand_evidence_shadow(
    *,
    question_text: str,
    fact_evaluation: dict[str, Any],
    session_dir: str | Path,
    repo_dir: str | Path | None = None,
) -> dict[str, Any]:
    payload = build_question_demand_evidence_shadow(
        question_text=question_text,
        fact_evaluation=fact_evaluation,
        session_dir=session_dir,
        repo_dir=repo_dir,
    )

    path = Path(session_dir) / QUESTION_DEMAND_EVIDENCE_FILENAME

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return payload
