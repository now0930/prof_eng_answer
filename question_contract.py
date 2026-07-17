from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


QUESTION_CONTRACT_VERSION = (
    "question_contract_v1"
)
QUESTION_CONTRACT_FILENAME = (
    "question_contract.json"
)

_CONFIRMATION_STATUSES = {
    "pending",
    "auto_confirmed",
    "manual_confirmed",
}


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def _hash_json(value: Any) -> str:
    return _sha256_text(
        _canonical_json(value)
    )


def _read_json(path: Path) -> Any:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def _write_json_atomic(
    path: Path,
    value: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    temporary.replace(path)


def _question_type_id(
    evaluation: Any,
) -> str:
    if not isinstance(evaluation, dict):
        return ""

    direct = (
        evaluation.get("question_type")
        or evaluation.get("type")
        or evaluation.get("lens")
    )

    if isinstance(direct, str):
        direct = direct.strip()

        if direct:
            return direct

    primary = evaluation.get(
        "primary_type"
    )

    if isinstance(primary, dict):
        value = str(
            primary.get("id")
            or ""
        ).strip()

        if value:
            return value

    return ""


def _model_answer_topic_id(
    reference: Any,
) -> str:
    if not isinstance(reference, dict):
        return ""

    primary = reference.get(
        "primary_reference"
    )

    if isinstance(primary, dict):
        value = str(
            primary.get("topic_id")
            or ""
        ).strip()

        if value:
            return value

    candidates = (
        reference.get("candidates")
        or []
    )

    if isinstance(candidates, list):
        for candidate in candidates:
            if not isinstance(
                candidate,
                dict,
            ):
                continue

            answer = (
                candidate.get("answer")
                or candidate.get(
                    "reference"
                )
                or {}
            )

            if not isinstance(
                answer,
                dict,
            ):
                continue

            value = str(
                answer.get("topic_id")
                or ""
            ).strip()

            if value:
                return value

    return ""


def _rubric_snapshot_hash(
    snapshot_path: str | Path,
) -> str:
    path = Path(snapshot_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Rubric snapshot not found: "
            f"{path}"
        )

    value = _read_json(path)

    return _hash_json(value)


def _deterministic_classification(
    *,
    confidence: str,
    status: str,
    locked: bool,
    source: str,
    matched_rules: list[Any],
) -> bool:
    if confidence != "high":
        return False

    if status != "locked":
        return False

    if locked is not True:
        return False

    lowered_source = source.lower()

    if any(
        token in lowered_source
        for token in [
            "fallback",
            "semantic",
            "llm",
            "provisional",
        ]
    ):
        return False

    if "deterministic" in lowered_source:
        return True

    if lowered_source in {
        "rule",
        "rules",
        "router",
        "question_type_router",
    }:
        return True

    return bool(matched_rules)


def _contract_payload(
    contract: dict[str, Any],
) -> dict[str, Any]:
    payload = copy.deepcopy(contract)
    payload.pop(
        "contract_hash",
        None,
    )

    return payload


def _with_contract_hash(
    contract: dict[str, Any],
) -> dict[str, Any]:
    output = copy.deepcopy(contract)
    output["contract_hash"] = (
        _hash_json(
            _contract_payload(output)
        )
    )

    return output


def build_question_contract(
    *,
    grading_identity: dict[str, Any],
    question_type_evaluation: dict[str, Any],
    fact_evaluation: dict[str, Any],
    model_answer_reference: dict[str, Any],
    rubric_snapshot_path: str | Path,
    subject_rubric: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = (
        grading_identity
        if isinstance(
            grading_identity,
            dict,
        )
        else {}
    )
    qtype = (
        question_type_evaluation
        if isinstance(
            question_type_evaluation,
            dict,
        )
        else {}
    )
    fact_eval = (
        fact_evaluation
        if isinstance(
            fact_evaluation,
            dict,
        )
        else {}
    )
    model_ref = (
        model_answer_reference
        if isinstance(
            model_answer_reference,
            dict,
        )
        else {}
    )
    rubric = (
        subject_rubric
        if isinstance(
            subject_rubric,
            dict,
        )
        else {}
    )

    normalization_version = str(
        identity.get(
            "normalization_version"
        )
        or ""
    ).strip()
    question_hash = str(
        identity.get("question_hash")
        or ""
    ).strip()
    submission_hash = str(
        identity.get("submission_hash")
        or ""
    ).strip()

    question_type = (
        _question_type_id(qtype)
    )

    confidence = str(
        qtype.get("confidence")
        or "low"
    ).strip().lower()
    locked = bool(
        qtype.get(
            "question_type_locked"
        )
    )
    status = str(
        qtype.get("status")
        or (
            "locked"
            if locked
            else "provisional"
        )
    ).strip().lower()
    source = str(
        qtype.get("source")
        or "unknown"
    ).strip()

    matched_rules = (
        qtype.get("matched_rules")
        or []
    )

    if not isinstance(
        matched_rules,
        list,
    ):
        matched_rules = []

    warning = str(
        qtype.get("warning")
        or ""
    ).strip()

    fact_topic_id = str(
        fact_eval.get("topic_id")
        or ""
    ).strip()
    model_topic_id = (
        _model_answer_topic_id(
            model_ref
        )
    )

    canonical_topic_id = (
        model_topic_id
        or fact_topic_id
    )

    auto_confirmed = (
        _deterministic_classification(
            confidence=confidence,
            status=status,
            locked=locked,
            source=source,
            matched_rules=matched_rules,
        )
    )

    confirmation = {
        "required": not auto_confirmed,
        "status": (
            "auto_confirmed"
            if auto_confirmed
            else "pending"
        ),
        "actor": (
            "deterministic_router"
            if auto_confirmed
            else None
        ),
        "method": (
            "automatic"
            if auto_confirmed
            else None
        ),
        "confirmed_at": None,
        "audit": [],
    }

    contract = {
        "version": (
            QUESTION_CONTRACT_VERSION
        ),
        "revision": 1,
        "immutable_identity": {
            "normalization_version": (
                normalization_version
            ),
            "question_hash": (
                question_hash
            ),
            "submission_hash": (
                submission_hash
            ),
        },
        "lens": question_type,
        "question_type": {
            "id": question_type,
            "confidence": confidence,
            "status": status,
            "locked": locked,
            "source": source,
            "matched_rules": copy.deepcopy(
                matched_rules
            ),
            "warning": warning,
        },
        "routing": {
            "fact_topic_id": (
                fact_topic_id
                or None
            ),
            "model_answer_topic_id": (
                model_topic_id
                or None
            ),
            "canonical_topic_id": (
                canonical_topic_id
                or None
            ),
        },
        "rubric": {
            "snapshot_hash": (
                _rubric_snapshot_hash(
                    rubric_snapshot_path
                )
            ),
            "name": rubric.get("name"),
            "version": rubric.get(
                "version"
            ),
            "question_type_profile": (
                rubric.get(
                    "question_type_profile"
                )
            ),
            "fact_anchor_bank": (
                rubric.get(
                    "fact_anchor_bank"
                )
            ),
            "model_answer_bank": (
                rubric.get(
                    "model_answer_bank"
                )
            ),
        },
        "confirmation": confirmation,
    }

    contract = _with_contract_hash(
        contract
    )

    validate_question_contract(
        contract
    )

    return contract


def validate_question_contract(
    contract: Any,
) -> dict[str, Any]:
    if not isinstance(contract, dict):
        raise TypeError(
            "Question contract must be a dict"
        )

    if (
        contract.get("version")
        != QUESTION_CONTRACT_VERSION
    ):
        raise ValueError(
            "Unsupported question contract version"
        )

    revision = contract.get("revision")

    if (
        isinstance(revision, bool)
        or not isinstance(revision, int)
        or revision < 1
    ):
        raise ValueError(
            "revision must be a positive integer"
        )

    identity = contract.get(
        "immutable_identity"
    )

    if not isinstance(identity, dict):
        raise ValueError(
            "immutable_identity must be a dict"
        )

    for key in [
        "normalization_version",
        "question_hash",
        "submission_hash",
    ]:
        value = str(
            identity.get(key)
            or ""
        ).strip()

        if not value:
            raise ValueError(
                f"immutable_identity.{key} "
                "is required"
            )

    lens = str(
        contract.get("lens")
        or ""
    ).strip()

    if not lens:
        raise ValueError(
            "lens is required"
        )

    question_type = contract.get(
        "question_type"
    )

    if not isinstance(
        question_type,
        dict,
    ):
        raise ValueError(
            "question_type must be a dict"
        )

    if (
        str(
            question_type.get("id")
            or ""
        ).strip()
        != lens
    ):
        raise ValueError(
            "lens and question_type.id "
            "must match"
        )

    confidence = str(
        question_type.get("confidence")
        or ""
    ).strip()

    if not confidence:
        raise ValueError(
            "question_type.confidence "
            "is required"
        )

    status = str(
        question_type.get("status")
        or ""
    ).strip()

    if not status:
        raise ValueError(
            "question_type.status is required"
        )

    source = str(
        question_type.get("source")
        or ""
    ).strip()

    if not source:
        raise ValueError(
            "question_type.source is required"
        )

    routing = contract.get("routing")

    if not isinstance(routing, dict):
        raise ValueError(
            "routing must be a dict"
        )

    rubric = contract.get("rubric")

    if not isinstance(rubric, dict):
        raise ValueError(
            "rubric must be a dict"
        )

    snapshot_hash = str(
        rubric.get("snapshot_hash")
        or ""
    ).strip()

    if len(snapshot_hash) != 64:
        raise ValueError(
            "rubric.snapshot_hash must be "
            "a SHA-256 hex digest"
        )

    confirmation = contract.get(
        "confirmation"
    )

    if not isinstance(
        confirmation,
        dict,
    ):
        raise ValueError(
            "confirmation must be a dict"
        )

    confirmation_status = str(
        confirmation.get("status")
        or ""
    ).strip()

    if (
        confirmation_status
        not in _CONFIRMATION_STATUSES
    ):
        raise ValueError(
            "Unsupported confirmation status"
        )

    required = confirmation.get(
        "required"
    )

    if not isinstance(required, bool):
        raise ValueError(
            "confirmation.required must "
            "be boolean"
        )

    if (
        confirmation_status == "pending"
        and required is not True
    ):
        raise ValueError(
            "Pending confirmation must "
            "remain required"
        )

    if (
        confirmation_status
        in {
            "auto_confirmed",
            "manual_confirmed",
        }
        and required is not False
    ):
        raise ValueError(
            "Confirmed contract cannot "
            "remain required"
        )

    audit = confirmation.get("audit")

    if not isinstance(audit, list):
        raise ValueError(
            "confirmation.audit must be a list"
        )

    contract_hash = str(
        contract.get("contract_hash")
        or ""
    ).strip()

    expected_hash = _hash_json(
        _contract_payload(contract)
    )

    if contract_hash != expected_hash:
        raise ValueError(
            "Question contract hash mismatch"
        )

    return contract


def persist_question_contract(
    session_dir: str | Path,
    contract: dict[str, Any],
) -> Path:
    validated = (
        validate_question_contract(
            contract
        )
    )

    path = (
        Path(session_dir)
        / QUESTION_CONTRACT_FILENAME
    )

    _write_json_atomic(
        path,
        validated,
    )

    return path


def load_question_contract(
    session_dir: str | Path,
) -> dict[str, Any]:
    path = (
        Path(session_dir)
        / QUESTION_CONTRACT_FILENAME
    )

    contract = _read_json(path)

    return validate_question_contract(
        contract
    )


def apply_question_contract_to_question_type(
    evaluation: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    validate_question_contract(
        contract
    )

    output = (
        copy.deepcopy(evaluation)
        if isinstance(evaluation, dict)
        else {}
    )

    qtype = contract["question_type"]
    question_type = qtype["id"]

    primary = output.get(
        "primary_type"
    )

    if not isinstance(primary, dict):
        primary = {}

    primary = copy.deepcopy(primary)
    primary["id"] = question_type

    output["primary_type"] = primary
    output["question_type"] = (
        question_type
    )
    output["confidence"] = qtype[
        "confidence"
    ]
    output["status"] = qtype["status"]
    output["question_type_locked"] = (
        qtype["locked"]
    )
    output["source"] = qtype["source"]
    output["matched_rules"] = (
        copy.deepcopy(
            qtype["matched_rules"]
        )
    )

    warning = qtype.get("warning")

    if warning:
        output["warning"] = warning
    else:
        output.pop("warning", None)

    return output


def apply_question_contract_to_fact_evaluation(
    evaluation: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    validate_question_contract(
        contract
    )

    output = (
        copy.deepcopy(evaluation)
        if isinstance(evaluation, dict)
        else {}
    )

    topic_id = (
        contract["routing"].get(
            "canonical_topic_id"
        )
        or contract["routing"].get(
            "fact_topic_id"
        )
    )

    if topic_id:
        output["topic_id"] = topic_id

    return output


def apply_question_contract_to_model_reference(
    reference: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    validate_question_contract(
        contract
    )

    output = (
        copy.deepcopy(reference)
        if isinstance(reference, dict)
        else {}
    )

    topic_id = (
        contract["routing"].get(
            "canonical_topic_id"
        )
    )

    if not topic_id:
        return output

    primary = output.get(
        "primary_reference"
    )

    if isinstance(primary, dict):
        primary = copy.deepcopy(primary)
        primary["topic_id"] = topic_id
        output["primary_reference"] = (
            primary
        )

    return output


def confirm_question_contract(
    contract: dict[str, Any],
    *,
    question_type: str,
    actor: str,
    method: str = "manual",
    confirmed_at: str | None = None,
) -> dict[str, Any]:
    validated = (
        validate_question_contract(
            contract
        )
    )

    requested_type = str(
        question_type
        or ""
    ).strip()
    actor_value = str(
        actor
        or ""
    ).strip()
    method_value = str(
        method
        or ""
    ).strip()

    if not requested_type:
        raise ValueError(
            "question_type is required"
        )

    if not actor_value:
        raise ValueError(
            "actor is required"
        )

    if not method_value:
        raise ValueError(
            "method is required"
        )

    timestamp = (
        str(confirmed_at).strip()
        if confirmed_at is not None
        else datetime.now(
            timezone.utc
        ).isoformat()
    )

    if not timestamp:
        raise ValueError(
            "confirmed_at is required"
        )

    output = copy.deepcopy(
        validated
    )
    previous_hash = output[
        "contract_hash"
    ]
    previous_identity = copy.deepcopy(
        output["immutable_identity"]
    )

    before = {
        "lens": output["lens"],
        "question_type": copy.deepcopy(
            output["question_type"]
        ),
        "confirmation_status": (
            output["confirmation"][
                "status"
            ]
        ),
    }

    output["revision"] += 1
    output["lens"] = requested_type
    output["question_type"]["id"] = (
        requested_type
    )

    confirmation = output[
        "confirmation"
    ]
    audit = confirmation.get("audit")

    if not isinstance(audit, list):
        audit = []

    confirmation["required"] = False
    confirmation["status"] = (
        "manual_confirmed"
    )
    confirmation["actor"] = actor_value
    confirmation["method"] = method_value
    confirmation["confirmed_at"] = (
        timestamp
    )

    after = {
        "lens": requested_type,
        "question_type": copy.deepcopy(
            output["question_type"]
        ),
        "confirmation_status": (
            "manual_confirmed"
        ),
    }

    audit.append(
        {
            "event": (
                "manual_question_type_"
                "confirmation"
            ),
            "actor": actor_value,
            "method": method_value,
            "confirmed_at": timestamp,
            "previous_contract_hash": (
                previous_hash
            ),
            "before": before,
            "after": after,
        }
    )

    confirmation["audit"] = audit

    if (
        output["immutable_identity"]
        != previous_identity
    ):
        raise RuntimeError(
            "Manual confirmation changed "
            "immutable identity"
        )

    output = _with_contract_hash(
        output
    )

    validate_question_contract(
        output
    )

    return output
