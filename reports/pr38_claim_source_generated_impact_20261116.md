# PR #38 · Claim 정리 및 Source→Generated 채점 영향 정적 감사 (2026-11-16)

> **작업 결론:** 48개 후보의 현재 Source는 **단문 표현 적용 18 / HOLD 30**이다. 18개에만 `sentence_compatibility`가 명시되어 기존 `expected`와 첫 허용 설명을 유지한다. 이 보고서는 실제 원격 HEAD와 파일·구현 경로의 **정적 검사**이지 전체 pytest/Release Validation 실행이나 새 Fact 승인 기록이 아니다.

## 감사 기준

- 기준 source HEAD: `63de8a7aec2132ff00ea21455eef52d46ff83d57` (보류 ID별 별도 보고서는 [30건 검토 JSON](pr38_pending_30_evidence_gate_review_20261116.json)).
- 원문 및 score-canonical: `calibration/fact_anchor_simplification_review_20261114.json`의 각 `previous_statement`. 단문화 역사적 `simplified_statement` 필드와 실제 표시용 소스의 짧은 첫 문장은 별개임.
- 실제 Source: 7개 `rubrics/topic_packs/<topic_id>/fact_anchor.json`의 Anchor, `expected`, 첫 `accepted_explanations`, `claim`, `description`, `core_facts`.
- 런타임 호환성: `grading/evidence/fact_anchor_compatibility.py`의 `scoring_anchor_view` 및 `scoring_topic_view`; Claim 관계 우선순위: `grading/evidence/fact_claim_adapter.py` (검증 Registry → 구조화 Machine Contract → unstructured 진단).

## 18개 적용 항목 원본 불변조건

- 단문 표시가 원본 **정확한 첫 완결 문장**인 Anchor: **18/18**.
- `expected == previous_statement` 유지: **18/18**.
- 첫 `accepted_explanations` == 기존 이전 전체 문장: **18/18**.
- 기존 `claim` 별칭이 있는 경우 표시문과 동일: **16개**; 나머지 **2개**는 원래 해당 필드가 없으므로 불일치로 오해 금지.
- 기존 `description` 필드가 있는 경우 표시문과 동일: **16개**; 나머지 **2개**는 원래 미정의.
- `core_facts` 표시문 mirror: **16개**; **2개**는 해당 Topic에서 `core_facts` 배열 자체가 없으므로 18개 모두를 강제 보충해서는 안 됨.

| 적용 Fact ID | Topic 약칭 | 원본·첫 설명 유지 | Claim/description | core_facts |
|---|---|---|---|---|
| `relative_humidity_definition` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `absolute_humidity_definition` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `dew_point_definition` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `frost_point_distinction` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `pressure_dew_point_effect` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `capacitive_polymer_principle` | 습도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `diaphragm_deflection_principle` | 압력 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `diaphragm_sensor_vs_seal` | 압력 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `dp_transmitter_two_port_principle` | 압력 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `counting_window_speed_equation` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `period_measurement_low_speed` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `quadrature_direction_principle` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `inductive_proximity_principle` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `gear_tooth_speed_equation` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `tachogenerator_voltage_speed_principle` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `digital_tachometer_instrument_boundary` | 회전속도 | 유지 | 현재 단문과 일치 | 단문 mirror |
| `thermocouple_law_of_intermediate_metals` | 열전대 | 유지 | 둘 다 원래 없음 | 해당 Topic 목록 없음 |
| `thermocouple_thermowell_installation_dynamic_error` | 열전대 | 유지 | 둘 다 원래 없음 | 해당 Topic 목록 없음 |

## 보류 30개 판단과 다음 Gate

- [30건 ID별 원문·공식 근거·조건·차단 사유](pr38_pending_30_evidence_gate_review_20261116.json)에 정확한 30개 Topic/Anchor/후보와 기존 HOLD 사유를 분리 기록했다. **30개 전체** source/score 변경·신규 승인 0. 이전 출처 보고서에만 근거가 있는 경우 새로 직접 확인했다고 주장하지 않는다.
- 기존 첫 허용 설명이 과거 전체 문장과 일치하지 않는 HOLD는 **12건**. 현재 `sentence_compatibility` v1은 첫 허용 설명과 `expected`가 정확히 같을 것을 요구하므로, 이 조건을 삭제하거나 설명 순서를 임의 변경해 후보를 적용해서는 안 된다.
- 기존 채점 제외 유지: `fsrm_markov_complexity` (scoring exclusion: noncore_detail), `low_humidity_dew_point_selection` (unresolved-source hold: vendor-specific). **자동 해제 금지**.
- `encoder_frequency_limit_selection`은 18개 단문화에 속하지 않는다. 이전에 승인 검토한 정밀 교정 소스를 계속 사용하고, PPR 채널 Hz와 x4 이벤트 count/s를 섞는 구 단문화 후보를 적용하지 않는다.
- 구조/기술 조건이 명확한 `sw10_fat_sat_relation`, `sw10_loop_test`, `feedback_disturbance_noise_paths`는 공식 기관 자료가 원리의 범위를 뒷받침하나, **기존 허용 설명·질문 범위·D/E 축·라우팅**이 보호되는 호환 설계와 실제 테스트를 먼저 요구한다.
- `feedback_steady_state_error_final_value`는 `sE(s)`의 극점과 최종값 존재 조건을 유지해야 하며, `thermocouple_reference_junction_compensation`은 원문의 단순 부정형 첫 문장만 표시하는 축약이 오히려 공학적 설명을 손상한다.

## Source→Generated→실제 채점 관계

```text
Topic Pack canonical source
  ├─ statement: 짧은 첫 문장 (18개 표시용)
  ├─ claim/description: 존재하면 짧은 표현과 동기화
  ├─ sentence_compatibility: 원문 SHA-256 (18개)
  └─ expected / accepted_explanations[0]: 과거 전체 문장
                  │
                  ▼
  scoring_anchor_view / scoring_topic_view
  · 정확한 opt-in marker가 있을 때 원문 전체 표현으로 채점 문맥 복원
  · core_facts는 해당 Topic에 배열이 존재하는 경우만 연결
                  │
                  ├─ Fact evidence/required-anchor/질문 scope/라우팅/D·E axis
                  └─ Claim Alignment: Registry verified relation → machine relation
                       └─ OFF/SHADOW 진단 경로, score_effect=none
```

**중요:** Source `claim` 별칭을 가독성 정리하거나 새 Claim으로 쪼개는 행위는 현재 이미 운영 승격된 Registry 관계와 동일하다는 증거가 아니다. Canonical Claim Extractor는 실제 문제·답안과 Machine Contract를 사용하며, `fact_claim_adapter`는 검증 Registry 관계를 우선한다. 따라서 source 단문 18개를 신규 점수 항목 18개로 바꾸거나 Verified Registry/Logic/Golden을 자동 변경하는 것은 금지한다.

### 변경이 발생할 수 있는 영향 경로와 필요한 검증

| 경로 | 현재 확인 | 실제 실행할 게이트 |
|---|---|---|
| Display `statement` vs scoring `expected` | 18개 필드 관계 정적 일치 | read-only audit, compat negative tests |
| 원본 첫 허용 답안 / lexical evidence | 기존 18개 첫 허용 설명 보존 | Fact evidence adapter 동일 정답·조건누락·거부 반례 |
| Generated bank six files | 이번 report-only commit에서 실제 source/builder 미변경 | 정식 Builder freshness, topic manifest SHA, routing triggers |
| 질문 scope 및 cross-topic | `scoring_topic_view` 보정 경로 존재 | synthetic 질문·hybrid/multi-topic owner 비교 |
| D/E canonical axes | baseline 중복 축 위험 보고서 존재, compat 대응 구현 | 축 ID·텍스트·중복/제외/가중치 패리티 |
| Claim alignment Fact→Answer→Logic | verified Registry 우선, machine relation은 진단 | OFF/SHADOW score/verdict 동등, forged/rejection/fatal tests |
| S7 optional 연구 | 기존 보고서에서 정답 독립 라벨 부족, 점수 권한 없음 | 별도 연구 평가만 가능; 새 필수 Gate 아님 |

## 실제 검증 이력과 현 HEAD 제한

- [2026-11-16 인계서](pr38_chatgpt_handoff_20261116.md): **로컬 검증 커밋 `5adbc9bbba15aa1b39b4ab902f34396fc3401825`**에서 전체 오프라인 pytest **1,793 passed, 2 skipped, 0 failed** 및 `VALIDATION=PASS`; Topic 전체 통합, Generated six freshness, focused pytest 50 passed. 이것은 인계서가 주장하는 **과거 로컬 기록**이며 현재 GitHub SHA에서 독립 실행한 결과가 아니다.
- 078f750a 기준 Git tree와 검증된 로컬 5adbc9의 동등성은 인계서 기록이며, 이번에는 변경 파일과 기존 generated blob SHA를 추가 확인한다. 새 코드는 수정하지 않았고 보고서만 추가했다.
- 이번 GitHub 연결에는 원격 Actions `workflow_dispatch` 실행기와 원격 Python/pytest 수행기가 없다. 최신 SHA에 대한 전체 pytest 출력/manifest/exit code를 생성하지 않았으므로 **현 HEAD Release PASS를 주장하지 않는다**.

## 안전한 다음 작업 순서 (별도 clean checkout)

1. 30개 중 2개 제외·조건부/호환 차단을 유지하면서 기존 `sentence_compatibility`의 정확한 첫 문장·accepted 설명 제약을 만족하는 한정 항목만 재검토. 문장 1개라도 canonical이 변경되면 generated·focused/전체 pytest의 새로운 근거 필요.
2. `grading/evidence/fact_anchor_compatibility.py` + tests의 invalid marker/fallback owner, exact evidence span, D/E axis, Claim off/shadow 패리티를 실제 실행하고 실패 원인별로 해결. **검증 없이 호환 계약을 느슨하게 하지 않음**.
3. 단문 적용 원본과 같은 Topic/Fact ID의 검증 Registry·Machine Contract에 중복 Claim이 있는지 정확한 관계/소유권으로 확인. 중복은 report-only 후보로 제안하고 검증·승인 전 삭제/합병 금지.
4. `python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated`; `python3 -B scripts/check_generated_rubrics_freshness.py`; 관련 focused pytest; clean worktree에서 `python3 -B scripts/release_candidate.py validate`. 모든 결과를 **실제 실행 SHA/exit code/pass/fail/skip/manifest**와 연결.
5. 필수 Gate 통과 전 PR #38 Draft, Issue #39 open, main 미병합, 봇 미배포, 기존 작업 폴더/비공개 데이터 미수정.

**이 보고서 자체의 score_effect: none / runtime change: none / test execution: NOT_RUN.**

