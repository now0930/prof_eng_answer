from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_llm_verifier import (
    _authoritative_structured_findings,
    load_logic_check_profile,
)


SIL_TOPIC = "sil_target_determination_risk_reduction_and_lifecycle"
MCDC_TOPIC = (
    "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
)


def _rule_ids(answer: str, topic_id: str) -> set[str]:
    profile = load_logic_check_profile(topic_id)
    return {
        str(row["rule_id"])
        for row in _authoritative_structured_findings(answer, profile, 10.0)
    }


def test_sil_issue1_concept_errors_are_detected_deterministically() -> None:
    answer = """
    PFH는 High Demand로 고장 즉시 고장을 확인할 수 있고,
    PFD는 Low Demand로 고장 후 점검 주기까지 고장 여부를 알 수 없다.
    PST 등 자동화된 점검 프로그램으로 MTTR을 축소한다.
    인증 수준보다 짧게 점검할 이유는 없다.
    """
    assert _rule_ids(answer, SIL_TOPIC) == {
        "fatal_demand_mode_by_fault_detection",
        "fatal_pst_replaces_full_test_or_reduces_mttr",
        "fatal_certificate_interval_as_operating_minimum",
    }


def test_sil_corrected_claims_do_not_trigger_structured_rules() -> None:
    answer = """
    Demand mode는 요구빈도와 연속작동 여부로 구분한다.
    PST는 일부 고장만 검출하며 full proof test를 대체하지 않고 MTTR은
    실제 수리절차로 별도 산정한다. 인증서 주기는 적용 가정일 뿐이며
    현장 자료와 PFDavg 계산으로 시험주기를 정한다.
    """
    assert not _rule_ids(answer, SIL_TOPIC)


def test_unqualified_sil_mcdc_universal_rule_is_detected() -> None:
    answer = "Systematic Integrity는 SIL 3/4의 MC/DC 100%로 검증한다."
    assert _rule_ids(answer, MCDC_TOPIC) == {"sil_four_universal_rule"}


def test_qualified_mcdc_requirement_does_not_trigger_universal_rule() -> None:
    answer = (
        "SIL 3/4의 MC/DC 100% 적용은 일률적인 규칙이 아니며, "
        "적용 표준과 자체 개발 코드 범위 및 Safety Plan에 따라 결정한다."
    )
    assert not _rule_ids(answer, MCDC_TOPIC)


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"AUTHORITATIVE_STRUCTURED_SAFETY_RULE_TESTS={len(tests)}_PASS")
