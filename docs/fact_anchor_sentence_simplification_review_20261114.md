# Fact Anchor 단일 기술명제 문장 정리 — 2026-11-14 배치 감사

> **현재 상태: SOURCE DRAFT / REVIEW REQUIRED / TESTS NOT RUN ON NEW HEAD.**
> 이 문서는 [Issue #39](https://github.com/now0930/prof_eng_answer/issues/39)의
> C영역 작업 증거이다. 사용자의 단문 정리 요청을 이행하되, **문장 형식 개선과
> 독립 기술적 검증·채점 승격·배포를 분리**한다.
> [Draft PR #38](https://github.com/now0930/prof_eng_answer/pull/38) 및
> `feat/claim-alignment-verification-20261114` 브랜치에서만 작업했다.

## 2026-11-14 3차 배치 — 압력·회전속도·열전대 (구현, 테스트 실행 전)

- 추가 **26개 단문**을 원천 `fact_anchor.json`에 초안으로 반영:
  **압력계측 7개**, **회전속도·엔코더 11개**, **열전대·냉접점 보상 8개**.
  이전 22개와 합산한 현재 **단문 수정 누계는 48개**이며 새 HEAD에
  대한 pytest·rubric source hash·generated 동기화는 아직 **미확인**이다.
- pressure:
  `bourdon_forms_application`, `diaphragm_deflection_principle`,
  `diaphragm_sensor_vs_seal`, `piezoresistive_static_capability`,
  `dp_transmitter_two_port_principle`,
  `ambient_environment_hazardous_selection`,
  `accuracy_total_performance_terms`.
- rotation:
  `pulse_frequency_speed_equation`, `counting_window_speed_equation`,
  `period_measurement_low_speed`, `quadrature_direction_principle`,
  `index_z_channel_role`, `absolute_encoder_principle`,
  `encoder_frequency_limit_selection`, `inductive_proximity_principle`,
  `gear_tooth_speed_equation`, `tachogenerator_voltage_speed_principle`,
  `digital_tachometer_instrument_boundary`.
- thermocouple:
  `thermocouple_temperature_measurement_chain`,
  `thermocouple_seebeck_effect_dissimilar_conductors`,
  `thermocouple_measures_temperature_difference`,
  `thermocouple_reference_junction_compensation`,
  `thermocouple_law_of_intermediate_metals`,
  `thermocouple_law_of_intermediate_temperatures`,
  `thermocouple_nonlinearity_reference_tables_polynomial_conversion`,
  `thermocouple_thermowell_installation_dynamic_error`.
- **구체적 안전 경계:** `n=60f/N_eff`,
  `n=60m/(N_eff·Δt)`, `n=60/(N_eff·T_c)`, `n=60f/Z`,
  `E(T1,T3)=E(T1,T2)+E(T2,T3)` 수식을 보존하고 N_eff 해석·
  계수방식·센서 응답한계·등온 접점·열전대 형식별 기준을 단문에 남겼다.
  기존 상세 표현은 `accepted_explanations`에 보관했다.
- **정적 원천 필드 비교:** 압력·회전속도 두 Topic의 원본 대비
  변경 Anchor 18건을 확인하고 **ID·Anchor 개수·importance·keywords·
  core_terms·source_basis·rejected_explanations·grading_notes가
  바뀌지 않았음**을 확인했다. 열전대 8건과 전체 회귀시험은
  뒤이어 재검증이 필요하다.
- **의도적 HOLD:** 압력기준 3종 정의, 다중 식/독립 조건,
  엔코더 제조사별 허용하중·장착오차, 열전대 종류별 분위기·보호관
  적용과 보상도선 및 교정 불확도 등은 짧은 한 문장으로 덮지 않았다.
  해당 Fact는 별도 개별 검토·필요시 독립 Anchor 분리 대상으로 유지한다.
- `tests/test_fact_anchor_simplification_batch.py`의
  **단일 문장/원문 보존/최소 조건·수식 검사 대상을 48건으로 확대**했다.
  테스트를 추가한 사실만 확인되었으며 `PASS`는 주장하지 않는다.
- **관리형 Displacer 4건은 여전히 미적용**이며 사용자 서명/승인 기록
  재작성 없이 검토 대기한다. `score_admission=DISABLED`, PR Draft 유지.

---

## 2026-11-14 4차 배치 — 48건 이전 원문 대조와 Source–Generated 영향 분석

**이 단계는 신규 단문 개수 증가가 아니라 정합성 보강이다.**

- 마지막 검증된 코드 커밋 `09e4b1c7`의 Topic Pack 원천과 현재
  작업 브랜치의 7개 Topic을 직접 대조하여 **48개 문장 변경**을 확인했다.
  이전 statement는 **48/48건 모두 `accepted_explanations`에 보존**되었다.
  해당 Anchor의 ID·importance·keywords·core_terms·source_basis·
  rejected_explanations·grading_notes·weight에서 예상하지 못한 차이는 **0건**.
  이 검사는 구조/보존 검증이며 기술적 정답 검증은 아니다.
- 최초 신뢰도 Anchor 3건은 짧아진 statement를
  `accepted_explanations`에 중복 기재하지 않았는데, 기존 신규 테스트가
  그것까지 요구하고 있었다. **원천을 테스트에 맞춰 임의 수정하지 않고**
  `calibration/fact_anchor_simplification_review_20261114.json`에
  48개 before/after 문장을 고정하고, 테스트가 **이전 원문의
  보존**을 검증하도록 고쳤다. 새 테스트의 PASS 여부는 아직 미확인.
- 열전대 Seebeck Anchor의 `열전도체` 표현을 의미가 더 분명한
  `열전소자`로 교정하고 snapshot을 함께 수정했다.
  해당 단문안도 독립 기술 검토 전까지 `PENDING_TECHNICAL_REVIEW`다.
- 승인받은 관리형 Displacer Topic은 기존 Git blob
  `23ae898870b6dd2e1e71f3ead09038688ba6fc3a`를
  Git blob SHA-1로 검사하는 회귀를 추가했다. 관리형 원천/사용자
  승인 메타데이터를 다시 쓰지 않는다.
- `rubrics/generated/fact_anchors.generated.json`의 Git blob
  `5bb598eebe293915236cd485660921dbe4fc64f2`는
  **원천 변경 전(`09e4b1c7`)과 현재 HEAD에서 동일**하다.
  `topic_pack_manifest.generated.json`의 Git blob도
  `6941dc2e9f7bf9cc5664115ce5a99ac3b51757ee`로 동일하다.
  **즉 원천 단문 수정 후 생성물의 재빌드는 아직 이루어지지 않았다.**
  이는 모든 Anchor의 runtime content 영향이 0이라는 뜻이 아니다.
- `scripts/build_generated_rubrics.py`의 `build_fact_anchors`는
  source `expected/fact/statement`를 기준으로 generated Anchor와
  **라우팅 `triggers`까지 합성한다**. 추후 정식 재생성 시
  Fact 문구 및 Topic routing 후보가 변경될 수 있으므로,
  **source match와 routing equivalence를 별도 평가**해야 한다.
- 새 `scripts/audit_fact_anchor_sentence_sync.py`는 48건에 대해
  `GENERATED_WORDING_MATCHES_SOURCE`,
  `GENERATED_WORDING_MATCHES_PREVIOUS`,
  `GENERATED_WORDING_OTHER`, `GENERATED_ANCHOR_MISSING`
  네 상태를 **읽기 전용** 집계한다. 다음 실행에서 개인 답안·가점 없이
  생성물의 실제 건별 상태를 얻는다. 현재는 script **작성만 완료**했고
  새 코드 실행 결과는 아직 없다.

### 실행 전 품질 확인 순서

```bash
python3 -B -m pytest -q \
  tests/test_fact_anchor_sentence_view.py \
  tests/test_fact_anchor_simplification_batch.py \
  tests/test_fact_anchor_sentence_sync_audit.py

python3 -B scripts/audit_fact_anchor_sentence_sync.py --summary-only
python3 -B scripts/rubric_manager.py validate-all
python3 -B scripts/release_candidate.py validate
```

`build-generated-rubrics`는 기술 내용 검토와 재생성 영향 검토 후
승인 workflow에 따라 수행하며, 이 항목만을 이유로 자동 병합/배포하지 않는다.
새 HEAD의 focused 및 전체 pytest와 Fact별 전문 검토는 **미완료**.

---

## 1. 기준과 규모

- 전체 **89개** `rubrics/topic_packs/*/fact_anchor.json` 파일을 GitHub에서
  읽어 구조를 조사했다. 현재 목록은 **약 2,096개 Anchor**이다.
- 마침표·문장 종결부호 중심의 초기 휴리스틱에서는 여러 문장으로 작성된
  항목이 **약 454건** 관찰됐다. 이미 단문으로 개정된 이전 3건을 포함한
  시점의 스캔이며, **이후 19건을 수정했기 때문에 같은 기준의 잠정 잔여는
  약 435건**이다. 본 수치는 독립 기술명제 개수나 확정 분리 대상 건수가 아니다.
- 한 문장 안에도 서로 다른 공학 명제가 들어갈 수 있다. 단순 분량·마침표
  개수만으로 승인된 사실을 잘라서 독립 Anchor로 자동 승격하지 않는다.

## 2. 원천에서 단문 정리한 22건 (검증 전)

각 Topic의 `fact_anchor.json`에서 대상 `statement`를 간결한 공학 명제
**한 문장**으로 수정했다. 스키마상 있는 `expected`, `claim`,
`description`은 일치시키고 기존 원문 설명은 `accepted_explanations`에
유지했다. **ID, owner Topic, required, importance, weight, keywords,
source_basis 및 승인 Registry를 수정하지 않았다.**

| Topic | 원천 단문 수정 | Anchor IDs |
| --- | ---: | --- |
| 기능안전 신뢰도 (선행 배치) | 3 | `fsrm_markov_state_transition`, `fsrm_markov_complexity`, `fsrm_model_assumption_documentation` |
| FAT/SAT·Loop Test | 2 | `sw10_fat_sat_relation`, `sw10_loop_test` |
| 습도 계측 | 12 | `relative_humidity_definition`, `rh_temperature_dependence`, `absolute_humidity_definition`, `dew_point_definition`, `frost_point_distinction`, `pressure_dew_point_effect`, `capacitive_polymer_principle`, `resistive_humidity_principle`, `psychrometric_wet_dry_bulb`, `condensation_sensor_temperature_error`, `low_humidity_dew_point_selection`, `selection_environment_process` |
| 피드백 민감도·정상상태오차 | 5 | `feedback_sensitivity_functions`, `feedback_parameter_sensitivity`, `feedback_disturbance_noise_paths`, `feedback_steady_state_error_final_value`, `feedback_integral_action_tradeoff` |
| **합계** | **22** | 원본의 추가 조건·적용범위는 개별 기술 검토 대상 |

예를 들어 다음의 단문 원칙을 적용했다.

- `relative_humidity_definition`:
  **상대습도 RH[%]는 같은 온도의 실제 수증기 분압 P_w와 포화수증기압
  P_ws(T)의 비율로, RH=100·P_w/P_ws(T)이다.**
- `feedback_steady_state_error_final_value`:
  **정상상태 오차는 sE(s)의 모든 극이 개방 좌반평면에 있고 최종값이
  존재할 때 e_ss=lim[s→0]sE(s)로 계산한다.**
- `sw10_fat_sat_relation`:
  **FAT와 SAT는 시험 장소와 설치·통합 검증 조건이 다르므로, 승인된
  시험계획에서 둘 다 요구하면 FAT 합격으로 현장 SAT를 대체하지 않는다.**

**주의:** 상세 설명을 `accepted_explanations`로 보존한 것은 손실 방지이지,
문장 변경이 기술적으로 검증되었거나 기존 runtime 은행이 동기화되었다는
의미가 아니다. source-hash/generated 계약, 기술 리뷰, 회귀 검증이 필요하다.

## 3. 관리형 Topic 4건 — 원천 변경 보류·별도 재승인 필요

`displacer_level_buoyancy_torque_tube_density_interface_calibration`은
`topic_status.json`에 **`approved / review_method=human /
reviewer=now0930`와 승인 source hash**가 있다.

따라서 단문안을 잠시 작성했으나, 승인 기록을 우회할 수 없어
**원천 JSON을 정확히 이전 버전으로 되돌렸다**.
이하 네 문장은 **재승인 검토 후보**이며 현재 승인된 Fact Anchor가 아니다.

| Anchor ID | 재승인 제안 단문 |
| --- | --- |
| `displacer_buoyancy` | 균일한 액체에서 displacer의 부력 F_b=ρgV_sub는 액위에 따른 침수체적 V_sub에 비례한다. |
| `displacer_signal_chain` | 지지된 displacer의 부력 변화는 토크튜브의 비틀림·각도로 변환되어 전송기 또는 제어기 출력에 반영되며, 출력 방향은 장치 구성에 따른다. |
| `displacer_interface_density_difference` | 비혼합 두 액체에 완전히 잠긴 displacer의 부력은 F_b=g(ρ_LV_L+ρ_UV_U)이며, 전체 침수체적이 일정하면 계면변화에 대한 부력 감도는 밀도차에 비례한다. |
| `displacer_wet_dry_calibration` | Displacer의 습식 교정은 시험액 비중에 따른 침수량을 환산하고 건식 교정은 제조사 절차의 등가하중으로 부력을 모사하되, 실제 운전 유체 검증과 구별한다. |

완료 조건: 출처·계측 조건·공식 단위·표현 검토 →
기존 `rubric_manager.py approve-topic` 검토·source-hash 갱신 경로 →
focused/통합 검증 → 생성물 동기화.
**사용자 명의 human 승인 기록을 AI가 임의로 재작성하지 않는다.**

## 4. 보류할 복합 Anchor 유형

- **표준 판/규정 범위·제품 경계가 긴 경우:** OT 보안, 제어밸브 제조사
  특정 규격, 산업안전, 위험장소 선정. 문장을 짧게 만들어 조건을 없애면
  표준에서 보장하지 않는 범위까지 일반화될 수 있다.
- **독립 명제 여러 개가 혼합된 경우:** 시스템 형별 오차상수,
  감쇠비별 극점, 압력·밀도·배관 구성별 DP 레벨 식.
  한 문장으로 묶기보다 독립 Fact 분리·중복 Owner 검토가 필요하다.
- **사용 조건이 불가결한 경우:** 최종값 정리 극점 조건, 계면 부력의 전체
  침수·밀도 조건, 유량계 설치/제어밸브 cavitation·flashing 구분.
  필수 조건 삭제는 단문 정리가 아니라 Fact 오류이므로 HOLD.
- **기술적 근거 부족·중복 항목:** 기존 scoring exclusion/verified status를
  변경하지 않고 관련 #33/#35 및 본 Issue #39에서 검토 후보로 관리한다.

## 5. 코드/검증 경계

- `grading/evidence/fact_anchor_sentence_view.py`: 원래 source의 `statement`를
  읽는 score-neutral projection. 복합문은 자동 수정하지 않고 HOLD.
- `scripts/audit_fact_anchor_sentences.py`: 전체 Topic/Anchor의
  단문·복합문 현황을 **읽기만 하는** 감사 도구.
- `tests/test_fact_anchor_sentence_view.py` 및
  `tests/test_fact_anchor_simplification_batch.py`: 파일/ID/핵심 조건/
  기존 상세 설명 보존·관리형 Topic 승인 경계에 관한 focused 회귀를 **작성**.
- **미실행:** 새 HEAD 대상 focused pytest, 전체
  `python3 -B scripts/release_candidate.py validate`,
  `python3 scripts/rubric_manager.py validate-all`, source-hash 비교,
  generated bank 정식 재빌드. GitHub Actions 과거 PASS는 해당 최신 HEAD
  검증에 전용하지 않는다.
- Source 변경 전후 점수·잘못된 사실 인정·Fatal/WRONG·중복 가점이
  기존 정책과 일치하는지 확인하기 전, 머지/실운영 배포/자동 점수 인정은 금지.

## 6. 다음 배치 우선순위

1. 단문 개정 **22건**의 원문 대조·근거/조건 검토 후 위험 항목 수정·원복.
2. legacy Topic source-hash와 generated 은행의 정식 통합 동기화.
3. 별도로 관리형 Displacer **4건**의 reviewer 재승인 및 적용.
4. 복합문 다수 Topic의 원자성 분류: 산업 OT 사이버보안,
   최종요소 SIL, DP 레벨계, 제어밸브 정비·시험·표준, 유속·회전계측.
5. 신규 HEAD에서 focused+전체 pytest, Topic validation 결과 기록 후
   Issue #39의 C5/C7/C8·D2/D3을 **실제 증거로만** 완료 처리.
