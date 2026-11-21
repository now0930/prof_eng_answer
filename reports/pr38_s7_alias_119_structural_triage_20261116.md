# PR #38 · S7 B7 / Alias 119개 고유 Fact 구조적 위험 분류 (2026-11-16)

> **상태: STRUCTURAL_TRIAGE_COMPLETE / REGISTRY_SOURCE_JOIN_NOT_RUN / TECHNICAL_REVIEW_HOLD.** 아래 항목은 실제 179-row Artifact를 분석한 수치이고, Alias/Fact 기술적 승인이 아니다.

## 검증 입력과 기준

- 이전 실제 검증: [Actions #43841253718](https://github.com/now0930/prof_eng_answer/actions/runs/43841253718) @ `0f556d5a1903dedca0b16ab8f98fe6fbd0c87f49`; `1,805 passed, 2 skipped, VALIDATION=PASS`; `REPRODUCED_BASELINE`, S7 47 graded/1 expected abstention/score_admission=DISABLED.
- 실제 입력 Artifact: `s7-alias-inventory` (artifact id 14215165770), `s7_alias_inventory.json`, 179 projections. **고유 `(owner_topic_id,fact_id)` 119개, 60개는 다른 Golden에 재투영.**
- 원인 분할: `ID_NOT_FOUND=179`; `EMPTY_ALIAS=0`, `INVALID_ALIAS_FORMAT=0`, `UNSUPPORTED_RELATION=0`, `OTHER=0`; 누락 유일 ID Subject 112 / Predicate 106 / Object 117. 이는 실제 source/loader 기준 **구조적 ID 부재**, 기술적 의미 판정은 별도다.
- 범위: **27개 Topic**, 39개 Golden에서 누락이 발견됨. 179개 투영 가운데 조건 있는 것은 177개, 고유 Fact 119개 중 조건 있는 것은 **117개**, 조건 없는 것은 **2개**.

## 개별 Fact 119개의 구조적 위험 태그

**각 Tag는 중복 가능하며 119개의 승인/거부 판정 합계가 아니다.**

| Tag | 고유 Fact | 검사 내용 |
|---|---:|---|
| `ID_NOT_DEFINED_IN_PARSER_ONTOLOGY` | 119 | Registry relation이 사용하는 ID를 현재 해당 Ontology namespace/loader에서 찾지 못함 |
| `CONDITIONS_MUST_BE_ASSERTED_NOT_GUESSED` | 117 | Golden에서 조건·가정·예외를 판단하지 않고 Alias만 추가하면 오인정 |
| `COMPOUND_PREDICATE_MAY_HIDE_MULTIPLE_CLAIMS` | 39 | Predicate ID 자체에 복합 동작/범위가 들어 있는지 수동 확인 필요 |
| `BROAD_PREDICATE_FALSE_POSITIVE_RISK` | 18 | `is`, `equals`, `has`, `maps` 등 짧고 범용적인 관계 표현 확장 위험 |
| `FORMULA_OR_DIRECTION_CONSTRAINT_RISK` | 11 | 등식·계수 방향·매핑, 집계, 한계 등의 수학적/방향적 조건 검증 필요 |

### 우선 검토할 경계 사례

- 조건 없는 단 2개도 자동 승인 대상이 아니다. `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation / sw04_v_model_definition`의 `maps`는 일반적인 설명상의 대응과 검증 추적성을 혼동할 수 있다. `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration / piezoelectric_direct_inverse_effect_distinction`도 정/역압전의 방향성이 뒤바뀌면 오인정 위험.
- `sil_target_determination_risk_reduction_and_lifecycle / required_rrf_relation`, `nyquist_stability_criterion_gain_phase_margin / argument_principle_pnz_relation` 등의 `equals`는 산술식·부호·위상/안정도 정의가 중요한 관계이며 일상어 `같다`만으로 인정하면 안 된다.
- SIF/FAT/SAT/PLC 시험과 안전·보안 관계의 조건식은 공식 기술 표준/해당 버전, 범위, 입력 답안의 명시 조건을 같이 판정해야 한다.

## 새 읽기 전용 source-evidence 단계 (현재 HEAD에서 아직 검증 안 됨)

- `scripts/review_s7_alias_registry_sources.py`: **기존 47 Golden 재생이 만든 179행 ID-only inventory**를 승인 Registry `approved_fact_registry.json`에 **`source_fact_id + owner/topic + legacy Anchor + 완전한 canonical relation`**으로 1:1 결합한다. 하나라도 불일치하면 `SOURCE_JOIN_HOLD`와 exit 2 (부분 성공으로 인정하지 않음).
- 각 119개 고유 Fact에 대해 승인된 source statement, 승인/verified 상태, revision, 원본 verification_refs(출처·판본·locator), source_refs, 조건, 중복된 Golden 사례, 오인식 위험 태그를 함께 저장. **Golden 답안 원문은 저장하지 않는다.**
- 모든 후보의 `candidate_alias`와 `candidate_wording`은 `null`, `review_decision`은 `HOLD`. Source Fact의 `verified`는 신규 어휘가 승인됐다는 뜻이 아니다. `score_admission=DISABLED` 유지.
- `tests/test_s7_alias_registry_source_review.py`에 중복 Fact, 불일치 relation, 다른 owner, 비승인 Fact, 출처 부재, 기준선 실패 등 fail-closed 테스트 추가. **새 HEAD에 대한 실제 pytest 결과는 없음.**
- GitHub `validation` 수동 실행 시 기존 `run_s7_alias_diagnostics=true`를 선택하면 이전 `s7-alias-inventory` 외에 `s7-alias-source-review` JSON Artifact를 업로드하도록 구성. 모든 테스트가 정상 통과해야 선택 실험까지 진행됨.

## 다음 검증·판정 게이트

1. 새 HEAD에서 Actions `validation` 전체 pytest PASS 확인, S7 `REPRODUCED_BASELINE` 재현 확인, 두 Artifact의 179/119/0 불일치 검증.
2. `s7-alias-source-review.json`의 **119개 source verification_refs와 실제 출처 원문**을 개별 비교하고 ID 의미·기존 Ontology 충돌·공학적 제약·대체 Predicate 여부를 확인.
3. 각 후보에 `ACCEPT/REVISE/REJECT/HOLD`, 제안된 한국어·영어 문구, 서술관계의 정/역 방향, 조건, FP 반례, 출처 페이지를 **개별 검토 후에만** 기입. 무근거·포괄적 Alias를 일괄 생성하지 않는다.
4. 안전하게 승인된 **소수** 변경만 별도 commit 후 focused tests + full offline pytest + source/Generated 정합성 + 동일 Golden S7 비교. 실제 TP/FP/FN/false-positive를 독립 평가하기 전 `literal candidate` 증가만으로 정확도 개선 주장 금지.

**보호 정책:** 원본 Registry·Topic Pack·Generated·점수/합격·Fatal/WRONG·Ceiling·SUPPORTED 상태 불변. PR Draft/Issue OPEN, main 미병합, 운영 배포/서비스 재시작 없음. 연구 실험의 선택 step 실패는 연구 FAIL로 명시하며 전체 offline pytest PASS와 혼동하지 않는다.
