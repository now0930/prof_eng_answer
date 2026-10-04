"""Generic grading contracts shared by the grading engine.

This module contains no topic-pack vocabulary, fact anchors, model answers,
or topic-specific extractors. It defines only generic states and pure
normalization helpers. Production pipeline ownership is wired in later stages.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, TypeVar


GENERIC_GRADING_CONTRACT_VERSION = "stage23.generic_grading_contract.v1"
SCORING_POLICY_VERSION = "stage23.generic_scoring_policy.v1"


class DemandState(str, Enum):
    CORRECT = "CORRECT"
    PARTIAL = "PARTIAL"
    WRONG = "WRONG"
    MISSING = "MISSING"


class ClaimRelationType(str, Enum):
    DEFINITION = "DEFINITION"
    CLASSIFICATION = "CLASSIFICATION"
    PURPOSE = "PURPOSE"
    MAPPING = "MAPPING"
    CAUSE_EFFECT = "CAUSE_EFFECT"
    CONDITION = "CONDITION"
    SEQUENCE = "SEQUENCE"
    METRIC_SCOPE = "METRIC_SCOPE"
    COMPONENT = "COMPONENT"
    EQUIVALENCE = "EQUIVALENCE"


class AlignmentStatus(str, Enum):
    ALIGNED = "ALIGNED"
    PARTIAL = "PARTIAL"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceTrustTier(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    VERIFIED_STRUCTURED = "VERIFIED_STRUCTURED"
    SEMANTIC_INFERRED = "SEMANTIC_INFERRED"
    UNSUPPORTED = "UNSUPPORTED"


class DERequirementClass(str, Enum):
    MANDATORY = "MANDATORY"
    OPTIONAL_BONUS = "OPTIONAL_BONUS"
    NO_PENALTY = "NO_PENALTY"


EnumT = TypeVar("EnumT", bound=Enum)


def _coerce_enum(enum_type: type[EnumT], value: Any, default: EnumT) -> EnumT:
    if isinstance(value, enum_type):
        return value
    normalized = str(value or "").strip().upper()
    for member in enum_type:
        if normalized == str(member.value).upper():
            return member
    return default


def normalize_demand_state(value: Any) -> DemandState:
    return _coerce_enum(DemandState, value, DemandState.MISSING)


def normalize_relation_type(value: Any) -> ClaimRelationType:
    return _coerce_enum(ClaimRelationType, value, ClaimRelationType.EQUIVALENCE)


def normalize_alignment_status(value: Any) -> AlignmentStatus:
    return _coerce_enum(AlignmentStatus, value, AlignmentStatus.UNSUPPORTED)


def normalize_evidence_trust_tier(value: Any) -> EvidenceTrustTier:
    return _coerce_enum(EvidenceTrustTier, value, EvidenceTrustTier.UNSUPPORTED)


def normalize_de_requirement_class(value: Any) -> DERequirementClass:
    return _coerce_enum(DERequirementClass, value, DERequirementClass.NO_PENALTY)


@dataclass(frozen=True)
class DemandAssessment:
    demand_id: str
    status: DemandState
    mentioned: bool = False
    evidence: str = ""
    rationale: str = ""

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DemandAssessment":
        demand_id = str(value.get("demand_id") or value.get("criterion") or value.get("id") or "").strip()
        status = normalize_demand_state(value.get("status"))
        mentioned_raw = value.get("mentioned")
        mentioned = bool(mentioned_raw) if mentioned_raw is not None else status is not DemandState.MISSING
        return cls(
            demand_id=demand_id,
            status=status,
            mentioned=mentioned,
            evidence=str(value.get("evidence") or "").strip(),
            rationale=str(value.get("rationale") or "").strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = self.status.value
        return result


@dataclass(frozen=True)
class ClaimRelationAssessment:
    claim_id: str
    relation_type: ClaimRelationType
    alignment_status: AlignmentStatus
    evidence_trust_tier: EvidenceTrustTier
    source_claim: str = ""
    target_claim: str = ""
    evidence: str = ""

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ClaimRelationAssessment":
        return cls(
            claim_id=str(value.get("claim_id") or value.get("id") or "").strip(),
            relation_type=normalize_relation_type(value.get("relation_type")),
            alignment_status=normalize_alignment_status(value.get("alignment_status") or value.get("status")),
            evidence_trust_tier=normalize_evidence_trust_tier(value.get("evidence_trust_tier") or value.get("trust_tier")),
            source_claim=str(value.get("source_claim") or "").strip(),
            target_claim=str(value.get("target_claim") or "").strip(),
            evidence=str(value.get("evidence") or "").strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["relation_type"] = self.relation_type.value
        result["alignment_status"] = self.alignment_status.value
        result["evidence_trust_tier"] = self.evidence_trust_tier.value
        return result


def demand_correctness_credit(status: DemandState | str) -> float:
    normalized = normalize_demand_state(status)
    if normalized is DemandState.CORRECT:
        return 1.0
    if normalized is DemandState.PARTIAL:
        return 0.5
    return 0.0


def demand_matrix_summary(rows: Iterable[DemandAssessment | Mapping[str, Any]]) -> dict[str, Any]:
    normalized_rows: list[DemandAssessment] = []
    for row in rows:
        if isinstance(row, DemandAssessment):
            normalized_rows.append(row)
        elif isinstance(row, Mapping):
            normalized_rows.append(DemandAssessment.from_mapping(row))

    counts = {state.value: 0 for state in DemandState}
    mentioned_count = 0
    correctness_credit = 0.0
    for row in normalized_rows:
        counts[row.status.value] += 1
        if row.mentioned:
            mentioned_count += 1
        correctness_credit += demand_correctness_credit(row.status)

    total = len(normalized_rows)
    mention_ratio = round(mentioned_count / total, 4) if total else None
    correctness_ratio = round(correctness_credit / total, 4) if total else None
    full_correct_coverage = bool(
        total
        and counts[DemandState.CORRECT.value] == total
        and counts[DemandState.WRONG.value] == 0
        and counts[DemandState.MISSING.value] == 0
    )
    return {
        "contract_version": GENERIC_GRADING_CONTRACT_VERSION,
        "rows": [row.to_dict() for row in normalized_rows],
        "total": total,
        "mentioned_count": mentioned_count,
        "mention_coverage_ratio": mention_ratio,
        "mention_coverage_percent": round(mention_ratio * 100.0, 1) if mention_ratio is not None else None,
        "correctness_credit": round(correctness_credit, 2),
        "correctness_coverage_ratio": correctness_ratio,
        "correctness_coverage_percent": round(correctness_ratio * 100.0, 1) if correctness_ratio is not None else None,
        "state_counts": counts,
        "correct_count": counts[DemandState.CORRECT.value],
        "partial_count": counts[DemandState.PARTIAL.value],
        "wrong_count": counts[DemandState.WRONG.value],
        "missing_count": counts[DemandState.MISSING.value],
        "full_correct_coverage": full_correct_coverage,
    }


def evidence_credit_weight(trust_tier: EvidenceTrustTier | str, alignment_status: AlignmentStatus | str) -> float:
    tier = normalize_evidence_trust_tier(trust_tier)
    alignment = normalize_alignment_status(alignment_status)
    if alignment in {AlignmentStatus.CONTRADICTED, AlignmentStatus.UNSUPPORTED, AlignmentStatus.NOT_APPLICABLE}:
        return 0.0
    if tier is EvidenceTrustTier.UNSUPPORTED:
        return 0.0
    trust_weight = {
        EvidenceTrustTier.DETERMINISTIC: 1.0,
        EvidenceTrustTier.VERIFIED_STRUCTURED: 1.0,
        EvidenceTrustTier.SEMANTIC_INFERRED: 0.5,
        EvidenceTrustTier.UNSUPPORTED: 0.0,
    }[tier]
    alignment_weight = 1.0 if alignment is AlignmentStatus.ALIGNED else 0.5
    return round(trust_weight * alignment_weight, 2)


def classify_de_requirement(*, explicitly_requested: bool, mandatory_when_requested: bool = True, bonus_only: bool = False) -> DERequirementClass:
    if not explicitly_requested:
        return DERequirementClass.NO_PENALTY
    if bonus_only or not mandatory_when_requested:
        return DERequirementClass.OPTIONAL_BONUS
    return DERequirementClass.MANDATORY


def de_penalty_allowed(requirement_class: DERequirementClass | str) -> bool:
    return normalize_de_requirement_class(requirement_class) is DERequirementClass.MANDATORY


def structured_consistency_issues(*, demand_summary: Mapping[str, Any] | None, narrative_flags: Mapping[str, Any] | None) -> list[str]:
    demand_summary = demand_summary or {}
    narrative_flags = narrative_flags or {}
    wrong_count = int(demand_summary.get("wrong_count") or 0)
    missing_count = int(demand_summary.get("missing_count") or 0)
    full_correct = bool(demand_summary.get("full_correct_coverage"))
    issues: list[str] = []
    if wrong_count and narrative_flags.get("claims_exact_fact"):
        issues.append("EXACT_FACT_WITH_WRONG_DEMAND")
    if wrong_count and narrative_flags.get("claims_zero_wrong"):
        issues.append("ZERO_WRONG_WITH_WRONG_DEMAND")
    if (wrong_count or missing_count) and narrative_flags.get("claims_full_coverage"):
        issues.append("FULL_COVERAGE_WITH_NONCORRECT_DEMAND")
    if narrative_flags.get("claims_full_coverage") and not full_correct:
        issues.append("NARRATIVE_FULL_COVERAGE_NOT_STRUCTURED_FULL")
    return issues


def contract_snapshot() -> dict[str, Any]:
    return {
        "schema_version": GENERIC_GRADING_CONTRACT_VERSION,
        "scoring_policy_version": SCORING_POLICY_VERSION,
        "demand_states": [item.value for item in DemandState],
        "claim_relation_types": [item.value for item in ClaimRelationType],
        "alignment_states": [item.value for item in AlignmentStatus],
        "evidence_trust_tiers": [item.value for item in EvidenceTrustTier],
        "de_requirement_classes": [item.value for item in DERequirementClass],
    }
