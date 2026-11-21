# S7 B7 — 마지막 5개 Fact 검토 목록 및 독립 전문가 판정 절차 (2026-11-17)

**상태:** PR #38 Draft의 연구 전용 변경. 신규 HEAD의 전체 pytest와 신규 8번째 Artifact는 아직 GitHub Actions에서 검증되지 않았다.

## 1. 이전 검증 기준선

[Actions #43994135463](https://github.com/now0930/prof_eng_answer/actions/runs/43994135463), HEAD `50d072526399f0cb561b86fd919b4470680bc8a5`, `1910 passed, 2 skipped`, `VALIDATION=PASS`; 연구용 Artifact 7개. 현재까지 Registry Fact 119개는 Alias 제안 상태 **HOLD**, 179개 누락 projection은 `ID_NOT_FOUND`. 20개 작성자 초안 쌍은 정합 초안 20건/반례 20건 모두 canonical `EXACT_RELATION=0`이므로 실제 Claim 파서의 일반 성능을 증명하지 않는다. 앞선 6개 수식, 4개 제한적 비수식, 5개 조건·범위 시험은 작성자 문구를 보고 표면 단서만 구별했다. 조건 증명은 0건이다.

**이번 단계는 14개 비수식 Fact 중 9개 표면 단서 검사를 이미 완료한 상태에서 남아 있는 5개를 독립 검토 대상으로 등록한다. 새로운 키워드 추출 성공 수치로 인식률을 부풀리지 않는다.**

## 2. Source Review의 Registry Fact별 대상

[Actions #43994135463]의 `s7-alias-source-review`를 직접 대조하여 다음 구조화된 관계와 조건을 고정한다. 승인·검증된 원본 관계와 **답안의 조건 충족 여부**는 별개이다.

| Legacy Fact ID | 검토 초점 | Registry Source Fact | 소스 조건 ID |
|---|---|---|---|
| `effective_unbalanced_area` | 실제 압력 기하에 따른 실효 면적과 공칭 시트 면적의 혼동 | `control_valve_effective_unbalance_area_definition` | `configuration_specific`, `defined_for_actual_pressure_geometry` |
| `sw06_baseline_approved_reference` | 공식 승인 또는 합의된 시점의 기준선과 단순 최신 파일의 혼동 | `configuration_baseline_is_approved_point_in_time_reference` | `configuration_information_is_identified`, `formal_approval_or_agreement` |
| `deadband_definition_direction_reversal` | 방향 반전 후 출력 변화가 없는 입력 구간과 시간 지연을 구별 | `control_valve_deadband_is_reversal_input_interval_without_observed_output_change` | `input_direction_reversal_is_part_of_definition`, `magnitude_is_assembly_and_test_condition_specific`, `output_change_is_not_observable_over_deadband_interval` |
| `sw04_v_model_definition` | V-Model의 설계/시험 단계 대응 및 추적성 요건 구별 | `v_model_design_test_mapping` | 없음 |
| `nyquist_contour_and_mapping` | s-평면의 우반평면 경로와 `L(s)` 사상 결과 구별 | `nyquist_contour_and_mapping` | `rhp_stability_analysis` |

합계 5개 Fact, 기존 소스 조건 ID 8개. V-Model 작성자 초안에 포함된 '추적 가능하게 연결' 표현은 소스 Registry의 관계 ID `v_model maps design_and_test_stages`만으로는 모든 별도 추적성 요구사항을 확정할 수 없다. 독립 검토자가 원문 근거와 범위를 따로 판단해야 한다. 이 부분을 일반적 표준 요구사항으로 자동 추가하지 않는다.

## 3. 구현한 두 단계

### A. CI가 실행할 메타데이터 전용 검토 대기 목록

- `grading/evidence/s7_remaining_five_expert_queue.py`: 기존 source-review, 14-Fact triage, 5-Fact condition/scope shadow, 20쌍 작성자 초안을 동일 HEAD에서 결합. Fact/Topic/Source/Subject/Predicate/Object/조건 ID를 고정하고 기존 5건의 `NOT_PROBED` 여부를 확인한다.
- `scripts/evaluate_s7_remaining_five_expert_queue.py`: 검증되지 않은 Registry/승격/교차 HEAD/점수 개입/조건 변경 시 거부하고 리포지토리 외부의 새로운 JSON 파일만 만든다.
- `tests/test_s7_remaining_five_expert_queue.py`: 대상 5건·조건 8개, 상태 HOLD, 개인정보 없는 출력, 소스 관계 변조, 혼합 실행, 승인 우회 등 다수 방어 시험.
- `.github/workflows/validation.yml`: 수동 workflow에서 `run_s7_alias_diagnostics=ON`일 때 비게이트 `s7-remaining-five-expert-queue` Artifact만 추가. 이 파일에는 원문 답안·원문 소스 문장·검토자 라벨은 들어가지 않는다.

예상 상태: `FIVE_UNPROBED_FACTS_QUEUED_FOR_INDEPENDENT_REVIEW`, `queued_fact_count=5`, `authored_draft_answer_count=10`, `source_condition_ids_total=8`, `independently_labeled_answer_count=0`, `score_admission=DISABLED`.

### B. 사람에게만 제공할 비공개 검토 패킷

- `grading/evidence/s7_independent_expert_packet.py` 및 `scripts/prepare_s7_private_expert_review_packet.py`는 **CI에서 실행하지 않는다**.
- 실존하는 5개 소스 문장, 원본 Registry 관계 ID/조건 ID, 출처 정보를 포함한다. 10개 작성자 초안은 새 무작위 review-item ID로 섞어 제공하고, 어떤 것이 작성자 정상/반례인지는 패킷에서 빼고 **별도의 private sealed-map 파일**에만 저장한다.
- 검토자 파일에는 판정 결과가 미리 쓰여 있지 않다. 검토자가 각 문장의 관계·부정·범위·조건 명시 여부 및 판단 근거를 작성하며, 독립 작성 정합 패러프레이즈/잘못된 관계/누락 조건/인용 또는 상충 문장도 별도로 작성한다.
- 단순히 기존 작성자 초안의 방향을 숨긴 것이므로 **검토자를 실제 배정하거나 검토를 마쳤다는 뜻이 아니며**, 외부 독립 검토 정답 데이터가 생성된 것도 아니다.
- 원문 텍스트가 포함된 reviewer-packet, sealed-map, 향후 실제 판정은 private filesystem에만 둔다. GitHub Artifact·Issue·PR에는 절대 업로드하지 않는다.

로컬 작업 예시(신규 CI가 끝난 뒤 같은 HEAD의 Artifact JSON을 추출해야 함):

```bash
python3 -B scripts/prepare_s7_private_expert_review_packet.py \
  --source-review /private/s7_alias_source_review.json \
  --review-queue /private/s7_remaining_five_expert_queue.json \
  --reviewer-packet /private/s7_review_packet_expertA.json \
  --sealed-map /private/s7_review_sealed_expertA.json
```

서로 다른 검토자 2명에게 각자의 패킷을 제공하고, 원래 작성자 기대값 없이 독립 판정을 받는 절차를 권고한다. 판정 항목은 (1) 관계·필수 조건 모두 명시, (2) 관계는 맞지만 조건 누락, (3) 상반된 관계, (4) 판정 불가/범위 밖. 이때 Source Review의 원본 관계와 표준 출처만 근거로 사용할 수 있다. 불일치는 전문가 합의 또는 보류로 해소하고, 합의를 결과의 독립성·정확도 입증과 혼동하지 않는다.

검토 완료 후에도 별도 버전의 독립 라벨, 새로운 전문가 작성 도전 사례, 분리된 평가 집합 및 false-positive 분석이 없으면 B7/D2/D3를 닫거나 `EXACT_RELATION` 성능을 주장하지 않는다.

## 4. 새 CI 검증 및 고정 정책

[validation.yml](https://github.com/now0930/prof_eng_answer/actions/workflows/validation.yml) 수동 실행 시 브랜치 `feat/claim-alignment-verification-20261114`, `run_s7_experiment=OFF`, `run_s7_alias_diagnostics=ON`. 실행 후 전체 pytest, `VALIDATION`, 기존 연구 Artifact 7개, 추가 8번째 `s7-remaining-five-expert-queue`의 실제 JSON을 개별 확인해야 한다. 비게이트 작업이 실패하면 workflow 전체 SUCCESS로 덮어쓰지 않는다.

**절대 불변:** Registry, Ontology, Topic Pack, Machine Contract, 정규 Claim 파서/채점기, 실제 점수 및 Goldens 변경 없음. 119 HOLD, `score_admission=DISABLED`, B7/D2/D3 OPEN, PR #38 Draft. Alias 자동 승인, main 병합 및 배포 금지.
