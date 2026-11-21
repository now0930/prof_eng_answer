# S7 B7 — 14개 Nonformula Fact 유형 분류 및 4개 문장 단서 Pilot (2026-11-17)

**상태: 구현 커밋됨, 새 HEAD GitHub Actions 전수 검증 전.** 대상은 PR #38의 Draft 브랜치뿐이며 프로덕션 채점, Ontology, Fact Registry, Machine Contract, Topic Pack을 변경하지 않는다.

## 실제 근거

Actions [#43984387892](https://github.com/now0930/prof_eng_answer/actions/runs/43984387892), HEAD `491175040629844b5613bb4073e2e2c667a8f5d0` 의 다섯 Artifact를 확인했다.

- 47 Golden + 1 정책 abstention, Alias gap 179 projection / 고유 Fact 119, `ID_NOT_FOUND=179`.
- 119개 Source Fact는 승인·검증된 Registry 관계를 가지지만 **새 Parser Alias 승인 0건, 119개 모두 HOLD**.
- 기존 20 작성자 정합 초안의 canonical `EXACT_RELATION=0` 및 20개 반례의 `EXACT_RELATION=0`.
- 수식 Shadow: 정상 표면 수식 6/6, 반례 역방향 6/6.
- Source-borrowed ID Bridge: Relation ID 후보 6/20, 비수식 인식 미지원 14/20. Registry ID의 대여만으로 답안 관계를 독립 추출한 것은 아니다.

## 14개 원본 Registry Fact의 검토 유형

| 연구용 그룹 | 건수 | Legacy Fact ID | 분석 방향 |
|---|---:|---|---|
| `DEFINITION_OR_CONSTRUCTION` | 5 | effective_unbalanced_area, sw06_baseline_approved_reference, deadband_definition_direction_reversal, single_port_globe_throttling_structure, rtd_four_wire_kelvin_measurement | 정의·구조·배선의 필수 요소, 범위/예외 |
| `CONDITIONAL_DEPENDENCY` | 3 | safe_state_process_hazard_basis, residual_frequency_before_sif, thermocouple_measures_temperature_difference | 공정 위험, 독립 IPL, 기준 접점 등 성립 조건 |
| `TREND_OR_TIME_BASIS` | 2 | rh_temperature_dependence, radar_pulse_time_of_flight | 변화 방향, 왕복/편도 시간 구별 |
| `MAPPING_OR_TRACEABILITY` | 2 | sw04_v_model_definition, nyquist_contour_and_mapping | 사상의 정의역/공역 및 단계 추적 |
| `POLE_ZERO_SCOPE_COUNT` | 2 | closed_loop_rhp_poles_count, open_loop_rhp_poles_count | 극점과 영점, 개루프/폐루프, 중복도 |

이 분류는 **검토 우선순위를 위한 연구자 분류**이지 새로운 공식 Ontology나 전문 검증 판정이 아니다. Source Review의 원문 Registry Subject/Predicate/Object 및 Condition ID를 변경하지 않는다.

## 1차 제한적 텍스트 Pilot: 4개 작성자 초안 쌍

| Fact | 정합 초안에서 관찰할 문자 단서 | 반례에서 관찰할 문자 단서 |
|---|---|---|
| single_port_globe_throttling_structure | Single-port globe + 시트링 한 개 + 선형 이동 | 시트링 두 개 |
| rtd_four_wire_kelvin_measurement | 4선식 Kelvin RTD + 전류/전압 검출 경로 분리 + 고입력 임피던스 + 오차 감소 | 2선식도 4선식처럼 별도 검출선 없이 보상된다는 주장 |
| rh_temperature_dependence | 수증기 분압 일정 + 온도 증가 + 상대습도 감소 | 같은 조건에서 상대습도 증가 |
| radar_pulse_time_of_flight | FMR56/FMR57 펄스 레이더 + 왕복 + `D=ct/2` | `D=ct` |

분리된 코드 `grading/evidence/s7_nonformula_surface_triage.py`는 각 원본 검증 관계의 Owner, Source ID, Predicate 및 HOLD 상태를 조회한다. Legacy Fact ID에 대응되는 **아주 좁은 문자 단서만** 판별하며 새 Predicate/Subject/Object ID를 추가하거나 답안에서 의미적 관계를 완성하지 않는다.

4개 Pilot 이외 **10개는 `NOT_PROBED`**로 명시한다. 부정 또는 인용/거부 문맥, 상반된 수식·문장 단서, 소유 주제 누락 등은 `UNRESOLVED` 또는 `HOLD`로 처리한다. 작성자 초안 8문장의 관찰 결과를 정답 판정, 정밀도·재현율·정확도, 산업 표준 검증 또는 채점 적격성으로 간주해서는 안 된다.

## 실패 차단 기준

- Source Review `119 HOLD`, `score_admission=DISABLED`; Bridge `6/20` 및 비수식 `14/20`.
- Source Review와 Bridge Artifact의 `execution_commit_sha` 및 `inventory_execution_sha`가 같은 새 Git SHA여야 함.
- 14개 Topic/Fact/Predicate/Source 검증 상태 및 부정/상반 문장 시험 중 불일치 시 **해당 연구 단계 HOLD**, 등가 Alias 자동 생성 금지.
- 원문 답안은 별도 Artifact에 저장하지 않음. 요약 ID와 문자 단서 상태만 보고.
- 예상 연구 출력 `nonformula_fact_count=14`, `pilot_fact_count=4`, `unprobed_nonformula_fact_count=10`; 초안 기준 정합 표면 단서 4건/상반 단서 4건. **실제 CI 전에는 숫자 성공을 주장하지 않는다.**
- 기존 `EXACT_RELATION` 결과와 운영 점수/WRONG/Fatal/Ceiling 불변; `B7/D2/D3 OPEN`, PR Draft, main 미병합.

## 실행 및 다음 과제

수동 [validation workflow](https://github.com/now0930/prof_eng_answer/actions/workflows/validation.yml)에서 기존 브랜치 선택 후, `run_s7_experiment=OFF`, `run_s7_alias_diagnostics=ON`으로 실행한다. 기존 다섯 Artifact와 추가 `s7-nonformula-surface-triage`를 따로 확인한다.

그다음 **독립 전문가가 구분한** 정합/반례/조건 누락 문장과 문맥 부정 사례를 확보한 후에야 답안에서 Subject·Predicate·Object 및 조건을 추출하는 실제 의미 판별기를 평가할 수 있다. 이번 결과를 채점 기준으로 자동 승격하지 않는다.
