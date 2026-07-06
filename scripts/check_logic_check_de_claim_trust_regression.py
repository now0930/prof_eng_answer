#!/usr/bin/env python3
import sys
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from logic_check_evaluator import evaluate_logic_checks

CASES = {
    "normal_second_order": """
2차 시스템의 표준형은 G(s)=wn^2/(s^2+2*zeta*wn*s+wn^2)로 표현한다.
극점은 s=-zeta*wn ± j*wd 이고, 감쇠진동수는 wd=wn*sqrt(1-zeta^2)이다.
zeta가 1이면 임계감쇠이며, 오버슈트 없이 빠르게 목표값에 접근한다.
0<zeta<1은 과소감쇠로 진동과 오버슈트가 발생할 수 있다.
zeta>1은 과대감쇠로 오버슈트 없이 느리게 수렴한다.
비교축은 극점 위치, 오버슈트, 피크시간, 정착시간, 현장 선정 기준으로 둘 수 있다.
따라서 오버슈트가 위험한 공정에서는 감쇠비와 고유진동수를 고려해 안정 여유를 확보한다.
""",
    "fatal_second_order": """
2차 시스템에서 zeta=1은 과대감쇠이다.
임계감쇠와 과대감쇠는 동일하며 둘 다 중근을 가진다.
따라서 오버슈트가 위험한 모든 공정에서는 zeta=1을 과대감쇠 기준으로 설계하면 된다.
""",
    "keyword_only": """
2차 시스템은 PID, MPC, Smith Predictor, Digital Twin, AI, TSN, EtherCAT을 적용한다.
현장에서는 최신 기술을 적용하면 품질이 좋아지고 유지보수가 쉬워진다.
""",
}

errors = []

for name, answer in CASES.items():
    # Regression must be deterministic in CI.
    # Do not depend on Ollama or any external LLM verifier.
    with patch(
        "logic_llm_verifier.verify_logic_with_llm",
        return_value={
            "fatal_error_detected": False,
            "mode": "mocked",
            "findings": [],
        },
    ), patch(
        "logic_llm_verifier._call_ollama_json",
        return_value=None,
    ):
        result = evaluate_logic_checks(answer_text=answer, grade={})

    if not result.get("applicable"):
        errors.append(f"{name}: logic check not applicable")
        continue

    trust = result.get("de_claim_trust_evaluation") or {}

    if trust.get("score_effect") != "none":
        errors.append(f"{name}: de_claim_trust score_effect is not none")

    for finding in result.get("findings", []):
        layers = finding.get("affected_layers", [])
        if "D" in layers or "E" in layers:
            errors.append(
                f"{name}: D/E remains in affected_layers: "
                f"{finding.get('id')} {layers}"
            )

    if name == "normal_second_order":
        if result.get("fatal_error_detected"):
            errors.append(f"{name}: unexpected fatal")

        if trust.get("status") not in {"trusted", "trusted_with_notes"}:
            errors.append(
                f"{name}: expected trusted/trusted_with_notes, "
                f"got {trust.get('status')}"
            )

        finding_ids = [str(f.get("id")) for f in result.get("findings", [])]
        if "missing_damped_frequency_relation" in finding_ids:
            errors.append(f"{name}: ASCII damped frequency relation was not recognized")

    if name == "fatal_second_order":
        if not result.get("fatal_error_detected"):
            errors.append(f"{name}: expected fatal")

        if trust.get("status") != "limited":
            errors.append(
                f"{name}: trust status should be limited, got {trust.get('status')}"
            )

        ceiling = (result.get("score_policy") or {}).get("recommended_ceiling")
        if ceiling is not None and ceiling != 10.0:
            errors.append(
                f"{name}: unexpected recommended_ceiling {ceiling}"
            )

    if name == "keyword_only":
        if result.get("fatal_error_detected"):
            errors.append(f"{name}: unexpected fatal")

        if trust.get("status") == "trusted":
            errors.append(f"{name}: keyword-only answer must not be fully trusted")

        if trust.get("status") not in {"not_invalidated", "trusted_with_notes"}:
            errors.append(
                f"{name}: unexpected trust status {trust.get('status')}"
            )

        finding_ids = [str(f.get("id")) for f in result.get("findings", [])]
        forbidden_fragments = [
            "advanced_tradeoff",
            "field_application",
            "coherence_defense",
            "d_e_feedback",
        ]

        for frag in forbidden_fragments:
            if any(frag in fid for fid in finding_ids):
                errors.append(f"{name}: forbidden D/E finding generated: {frag}")

if errors:
    print("INVALID")
    for err in errors:
        print(f"- {err}")
    raise SystemExit(1)

print("VALID: Logic Check D/E claim trust regression")
