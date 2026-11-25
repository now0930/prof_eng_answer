# Fact Anchor Registry 승인 검토 통합 목록 — 17건

이 문서는 PR #46의 5건과 그 후속 PR #47의 12건을 하나의 승인 검토 묶음으로 정리한다. **17건은 모두 제안이며 현재 승인된 변경이 아니다.** Registry, 승인/Promotion Ledger, source hash, exclusion overlay 및 점수 권한은 이 문서 작성 과정에서 수정하지 않았다. 457건 분류 및 원문 기록은 별도 보존한다.

각 Registry 행은 현재 `approved/verified` 상태의 기존 기록이다. 아래 “제안”은 기존 행을 바꾸려면 다시 검토할 정확한 문장이지, 현재 정본 또는 승인 상태를 자동으로 덮어쓰라는 지시가 아니다. 기술적 출처 확인과 Topic Pack 승인 및 채점 적격성은 별도다.

## 승인 전 요약

- PR #46: 5개 기존 Registry fact의 문장/범위를 더 정밀하게 제안한다. 모두 현재 exclusion overlay에서 제외되지 않지만, Registry 문장 변경 자체가 채점 승인이나 점수 효력을 부여하지 않는다.
- PR #47: 12개 기존 fact의 문장 또는 범위 재검토. 현재 9개는 exclusion overlay에 있고 3개는 제외되어 있지 않다.
- PR #47의 source guard: 5개는 기존 Promotion Ledger의 Topic 전체 hash 고정, 1개는 managed Topic source hash, 2개는 canonical/Registry exact-contract, 나머지 4개는 #47에서 정본이 바뀌어 Registry 문안과 재대조가 필요하다.
- 승인 후 최소 범위는 기존 Registry row 및 검토 provenance다. Topic Pack 문구나 승인 hash를 바꿔야 할 경우 공식 Topic workflow/validator를 사용하고, 필요 Generated 6개는 official builder로 재생성한다. hash나 Ledger를 수동 편집하지 않는다.
- 예상 점수 효과: Registry-only review/update는 `score_effect=none`. 채점 제외 상태를 변경하지 않는다. 정본 문구 변경은 별도 표적 회귀에서 확인되어야 한다.

## 1. encoder_frequency_limit_selection

- **PR / Topic / Anchor ID / Registry ID:** #46 / `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `encoder_frequency_limit_selection` / `encoder_speed_and_decode_rate_must_fit_frequency_limits`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** Encoder와 receiving counter/PLC의 최대 output/input frequency를 확인한다. 최고 속도 n[rpm]에서 채널당 pulse/rev P_ch이면 물리 pulse frequency f_ch=n·P_ch/60 [Hz], 유효 count/rev N_eff이면 decoded count rate=n·N_eff/60 [count/s]이다. 동일 회전속도에서 물리 PPR 증가에 따라 pulse frequency가 증가하며 decoding 배율 변경은 count rate를 바꾼다. 각 장치 사양의 단위와 조건에 맞춰 선정한다.
- **기존 Registry statement:** For an incremental encoder with N_eff decoded counts per revolution at n rpm, the count-event rate is f=n·N_eff/60 counts/s. Encoder output electronics and the receiving counter/input each have finite frequency or pulse-width limits; the selected maximum speed and decode mode must remain within both applicable limits. Increasing decoded counts/revolution increases event rate at the same shaft speed.
- **최종 승인 검토 문장(제안):** 증분형 엔코더가 `n` rpm으로 회전하고 PPR이 채널의 회전당 신호 주기 수를 뜻할 때, 채널 출력 주파수는 `n·PPR/60` Hz이고 수신기의 유효 계수율은 `n·N_eff/60` count/s이다. 최대 회전속도와 선택한 복호 모드에서 엔코더 출력 한계, 수신기 입력 주파수·펄스폭 한계, 사양에 명시된 내부 계수 처리 한계를 각각 확인한다.
- **출처 및 적용범위:** [Rockwell 1746-UM002B, counting relationship and input frequency](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1746-um002_-en-p.pdf); [Rockwell 1756-UM007E, x1/x4 and minimum pulse width](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1756-um007_-en-p.pdf). PPR 정의는 제조사별 단위를 확인하고 모듈별 수치 한계는 해당 모델에만 적용한다.
- **정본 상태:** PR #46에서 이미 수정됨; 이번 문서는 Registry 승인만 제안
- **Ledger/hash 영향:** PR #46의 우선순위 Anchor 문구는 이미 수정됨. 104개 Ledger 중 이 Anchor의 직접 항목 없음. Registry 승인/출처 기록은 기존 승인 절차로 갱신하고 source hash를 수동 조작하지 않는다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `encoder_speed_and_decode_rate_must_fit_frequency_limits` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 2. gear_tooth_speed_equation

- **PR / Topic / Anchor ID / Registry ID:** #46 / `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `gear_tooth_speed_equation` / `rotation_speed_tooth_event_frequency_relation`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 평균 event frequency f에 대해 n = 60f/Z이다. 실제 missing-tooth, multiple-edge counting 또는 target pattern에서는 전체 회전 평균에 회전당 유효 event 수 Z_eff를 적용한다. 비등간격 event의 국부 period로 속도를 계산할 때는 실제 각도 간격을 반영한다.
- **기존 Registry statement:** If there are Z effective target events per revolution and each event produces one counted pulse, pulse frequency f in hertz and rotational speed n in rpm satisfy n = 60f/Z. Z must reflect the actual counted events per revolution, including edge multiplication or missing-tooth patterns as applicable.
- **최종 승인 검토 문장(제안):** 한 회전 또는 정수 회전에서 측정한 이벤트 평균 주파수가 `f` Hz이고 회전당 유효 이벤트 수가 `Z`이면 평균 회전속도는 `60f/Z` rpm이다. 결손치를 포함한 두 검출 에지 사이의 구간 평균 회전속도는 실제 회전각을 경과 시간으로 나누어 환산한다.
- **출처 및 적용범위:** [MathWorks toothed-wheel/missing-tooth engineering example](https://blogs.mathworks.com/simulink/2018/11/07/internal-combustion-engine-ignition-control-example-part-1/). `n=60f/Z` and local `60Δθ/(2πΔt)` are dimensional/kinematic derivations; the gap sample uses actual edge-to-edge angular spacing, not nominal pitch.
- **정본 상태:** PR #46에서 이미 수정됨; 이번 문서는 Registry 승인만 제안
- **Ledger/hash 영향:** PR #46 우선순위 Anchor 문구 수정 반영. 104개 Ledger에서 직접 항목 없음. Registry 승인 및 출처 기록은 공식 절차로 갱신한다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `rotation_speed_tooth_event_frequency_relation` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 3. incremental_encoder_principle

- **PR / Topic / Anchor ID / Registry ID:** #46 / `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `incremental_encoder_principle` / `incremental_encoder_reports_displacement_relative_to_reference`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** Incremental rotary encoder는 optical 또는 magnetic pattern의 회전에 따라 pulse train을 발생시키며 기준점에서 누적한 pulse 수 또는 주파수로 상대 위치와 속도를 계산한다. Encoder 자체는 절대위치를 직접 부호화하지 않는다. 전원 차단 중 미계측 축 이동은 저장된 count만으로 복원할 수 없으므로 count 연속성, homing 또는 별도 절대위치 확인이 필요하다.
- **기존 Registry statement:** An incremental encoder represents shaft movement as pulses/count transitions relative to a reference; an external counter/controller accumulates those transitions to obtain relative position and can derive speed from pulse timing. Unless the accumulated count is retained through power loss or re-established by a reference/homing procedure, an incremental output alone does not identify the shaft's absolute position after restart.
- **최종 승인 검토 문장(제안):** 증분형 엔코더의 펄스를 기준 위치부터 누적하면 상대 변위를 구할 수 있다. 전원 차단 동안 계측하지 못한 이동은 저장 계수값으로 복원할 수 없으며, 위치를 복구하려면 계수의 연속성을 확인하거나 원점 복귀 등으로 기준을 다시 확립해야 한다.
- **출처 및 적용범위:** [Rockwell Sensor Technology and Application Basics, Incremental Encoders](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/c117-rm001_-en-p.pdf); [Rockwell Kinetix 300 homing methods](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/2097-um001_-en-p.pdf). The cited homing procedure is product-specific; the general limitation is unobserved movement without retained/verified continuity.
- **정본 상태:** PR #46에서 이미 수정됨; 이번 문서는 Registry 승인만 제안
- **Ledger/hash 영향:** PR #46 우선순위 Anchor 문구 수정 반영. 104개 Ledger에서 직접 항목 없음. Registry 승인/출처 기록만 기존 절차로 검토한다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `incremental_encoder_reports_displacement_relative_to_reference` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 4. thermocouple_measures_temperature_difference

- **PR / Topic / Anchor ID / Registry ID:** #46 / `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_measures_temperature_difference` / `thermocouple_measures_temperature_difference`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** 열전대 전압은 측정접점 온도만의 함수가 아니다. 균질한 열전대에서 열기전력 E(Th,Tc)=E0(Th)−E0(Tc)는 재료 조합과 측정접점·기준접점의 두 온도에 의존하며, Seebeck 계수가 온도에 따라 변하므로 같은 온도차라도 열기전력이 다를 수 있다. 측정접점 온도를 구하려면 기준접점 온도(또는 알려진 기준조건)와 해당 열전대의 유효 온도-열기전력 변환관계를 이용한다. 온도차 측정이라는 일반적인 설명은 ΔT만의 함수라는 단정과 구분한다.
- **기존 Registry statement:** 열전대 전압은 측정접점과 기준접점의 온도차에 대응하므로, 절대 측정접점 온도를 구하려면 기준접점 온도를 알아야 한다.
- **최종 승인 검토 문장(제안):** 균질한 열전대 재료쌍과 지정 극성에서 측정접점과 기준접점의 온도를 각각 `T_m`, `T_r`로 하면, 순 열기전력은 해당 형식의 기준함수 차 `E(T_m) − E(T_r)`이다. 기준접점 온도가 고정된 경우 해당 형식의 유효 범위에서 온도차로 전압 변화를 설명할 수 있다.
- **출처 및 적용범위:** [NIST Monograph 175, thermocouple reference functions](https://www.nist.gov/publications/temperature-electromotive-force-reference-functions-and-tables-letter-designated); [NBS Handbook 121, law of intermediate temperatures](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook121.pdf). Use the thermocouple type-specific reference function, reference-junction condition and valid temperature range; a fixed ΔT is not a universal voltage equivalence.
- **정본 상태:** PR #46에서 이미 수정됨; 이번 문서는 Registry 승인만 제안
- **Ledger/hash 영향:** PR #46 우선순위 Anchor 문구 수정 반영. 104개 Ledger에서 직접 항목 없음. Registry 승인 및 source reference의 기존 흐름을 따른다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `thermocouple_measures_temperature_difference` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 5. imperfect_test_residual_risk

- **PR / Topic / Anchor ID / Registry ID:** #46 / `final_control_element_sil_sis_esd_valve_partial_stroke_test` / `imperfect_test_residual_risk` / `partial_testing_leaves_unrevealed_failure_modes_for_full_proof_test`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** Imperfect proof test 후에도 검출되지 않는 dangerous failure가 남을 수 있다. Residual failure rate와 untested failure modes를 명시하고 실제 검출·복구 가능한 시험, 교체 또는 overhaul/mission time까지의 risk contribution을 평가한다. Full proof test도 coverage 100%를 자동으로 보장하지 않는다.
- **기존 Registry statement:** Imperfect proof test 후에도 검출되지 않는 dangerous failure가 남는다. Residual failure rate와 untested failure modes를 명시하고 다음 full test까지의 risk contribution을 평가한다.
- **최종 승인 검토 문장(제안):** 부분시험에서 드러나지 않는 위험고장은 해당 시험의 주기로 제거된 것으로 계산할 수 없다. 각 잔여 고장모드에 대해 실제 검출 후 복구할 수 있는 시험 또는 해당 모드를 제거하는 교체까지의 노출을 모델에 반영한다. 그런 조치가 정의되지 않은 운용구간에는 해당 모드의 위험 기여를 계속 반영한다.
- **출처 및 적용범위:** [HSE OG54 Appendix 1 §§35–43](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf); [HSE OG54 Appendix 3, partial proof example](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf); [ISA-TR96.05.02-2022 preview](https://www.isa.org/getmedia/0fdf7b91-86c4-42e6-9cbe-2f42449204c6/ISA-TR96-05-02-2022-Preview.pdf). A full-test interval applies only to failure modes the test can reveal and address; do not assume test-name coverage or repair.
- **정본 상태:** PR #46에서 이미 수정됨; 이번 문서는 Registry 승인만 제안
- **Ledger/hash 영향:** PR #46 우선순위 Anchor 문구 수정 반영. 104개 Ledger에서 직접 항목 없음. 공식 Registry 재검토 대상.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `partial_testing_leaves_unrevealed_failure_modes_for_full_proof_test` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/final_control_element_sil_sis_esd_valve_partial_stroke_test/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 6. dp_level_wet_leg_zero_elevation

- **PR / Topic / Anchor ID / Registry ID:** #47 / `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` / `dp_level_wet_leg_zero_elevation` / `dp_level_wet_leg_zero_elevation`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** Wet Leg에서는 0% 레벨에서도 저압측 기준수두 때문에 음의 차압이 발생할 수 있다. 따라서 LRV가 0보다 작은 Zero Elevation 교정을 적용한다.
- **기존 Registry statement:** Wet-leg 구성의 0% 차압은 계기 및 탭 고도와 기준액 수두에 따라 음수가 될 수 있다. Yokogawa 매뉴얼의 예에서는 LRV가 −23.73 kPa이므로 해당 배치에 zero elevation이 적용된다.
- **최종 승인 검토 문장(제안):** Wet leg의 0% 레벨에서 LRV는 실제 설치 조건의 고압측 압력에서 저압측 압력을 뺀 값이다. 일정 밀도에서 공정액의 양의 수두가 `ρ_p·g·h_min`, 저압측 기준액 수두가 `ρ_w·g·H_w`이면 `LRV=ρ_p·g·h_min−ρ_w·g·H_w+C`이다. `C`는 두 수두에 포함되지 않은 설치 오프셋의 부호 있는 합이다. 계산한 LRV가 음수일 때 zero elevation을 적용한다.
- **출처 및 적용범위:** [Yokogawa IM 01C20C01-01E §7.4(3), p. 7-6](https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf), including the stated −23.73 kPa worked example. Formula/generalization is hydrostatic head balance for the installed H/L legs; negative LRV is possible, not universal.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** PINNED_TOPIC_HASH: 해당 Topic `fact_anchor.json` 전체가 기존 keep-bounded Promotion Ledger 해시에 고정. Owner 승인 및 공식 재검증 없이 파일/hash를 갱신하지 않는다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `dp_level_wet_leg_zero_elevation` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 7. sw09_software_firmware_integrity

- **PR / Topic / Anchor ID / Registry ID:** #47 / `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_software_firmware_integrity` / `nist_80082r3_ot_software_firmware_authenticity_checks`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** NIST SP 800-82 Rev. 3은 vendor-provided OT software·firmware의 authenticity 확인을 위해 serial/checksum/certificate/signature 같은 식별정보를 기록·추적하고, 자동 code-authentication이 없으면 hash, reputable source, vendor version confirmation 또는 offline/test 환경으로 수동 확인하는 방법을 제시한다.
- **기존 Registry statement:** NIST SP 800-82 Rev. 3은 vendor-provided OT software·firmware의 authenticity 확인을 위해 serial/checksum/certificate/signature 같은 식별정보를 기록·추적하고, 자동 code-authentication이 없으면 hash, reputable source, vendor version confirmation 또는 offline/test 환경으로 수동 확인하는 방법을 제시한다.
- **최종 승인 검토 문장(제안):** OT 소프트웨어·펌웨어는 신뢰할 수 있는 배포 경로와 버전을 확인하고, 신뢰된 공급자가 제공한 서명·인증서 또는 검증 기준 해시를 적용 가능한 방식으로 대조한다. 격리 시험은 호환성과 기능을 확인하는 데 사용할 수 있다. 진위와 무결성은 배포 출처 및 검증값의 신뢰성으로 별도 확인한다.
- **출처 및 적용범위:** [NIST SP 800-82 Rev. 3 §6.1.5, pp. 96–97; Appendix F SI-7(15), pp. 293–294](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf). Apply verification methods appropriate to availability; offline/test execution is functional compatibility evidence, not by itself proof of authenticity.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** EXACT_REGISTRY_CONTRACT: 기존 Registry와 정본 일치 회귀 조건에 걸림. Canonical 문안 승인 전 Registry만 바꾸거나 assertion을 우회하지 않는다.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `nist_80082r3_ot_software_firmware_authenticity_checks` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 8. hazard_scenario_boundary

- **PR / Topic / Anchor ID / Registry ID:** #47 / `sil_target_determination_risk_reduction_and_lifecycle` / `hazard_scenario_boundary` / `sil_hazard_scenario_boundary`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** 목표 SIL은 initiating event, 운전조건, consequence endpoint와 필요한 safe state가 명확한 위험 시나리오별로 결정한다. 서로 다른 원인이나 결과를 한 빈도로 뭉치지 않는다.
- **기존 Registry statement:** 목표 SIL은 initiating event, 운전조건, consequence endpoint와 필요한 safe state가 명확한 위험 시나리오별로 결정한다. 서로 다른 원인이나 결과를 한 빈도로 뭉치지 않는다.
- **최종 승인 검토 문장(제안):** 목표 SIL 검토에서는 개시사건, 운전조건, 결과와 요구 안전상태를 시나리오별로 정의한다. 같은 위험 결과 및 SIF에 기여하는 시나리오 빈도를 집계할 때에는 공통 조건, 종속성과 중복 산입을 확인한다.
- **출처 및 적용범위:** [AIChE/CCPS LOPA Data](https://ccps.aiche.org/resources/tools/lopa), one cause–consequence pair per scenario; [HSE Functional Safety Inspection Guide, Appendix 4](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf). Scenario-boundary guidance does not imply a blanket ban on aggregating comparable frequencies; dependence and double counting require explicit risk-model review.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** PINNED_TOPIC_HASH: SIL Topic `fact_anchor.json` 전체 해시가 Promotion Ledger에 고정. Existing ledger/topic source hash는 owner-authorized workflow 외 수정 금지.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `sil_hazard_scenario_boundary` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/sil_target_determination_risk_reduction_and_lifecycle/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 9. dp_level_hydrostatic_pressure_principle

- **PR / Topic / Anchor ID / Registry ID:** #47 / `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` / `dp_level_hydrostatic_pressure_principle` / `dp_level_hydrostatic_pressure_principle`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** 정지 유체의 두 점 사이 압력차는 ΔP=∫ρg·dz이며, 밀도가 일정하면 ΔP=ρgΔh이다. 차압식 레벨계는 높이만이 아니라 밀도와 높이의 곱인 압력수두를 측정한다.
- **기존 Registry statement:** 정지 유체의 압력수두는 밀도와 높이에 의존하며, 밀도가 일정한 액주에서는 ΔP=ρgΔh이다. 따라서 차압식 레벨은 밀도가 일정하다는 가정 없이 높이만 직접 측정하지 않는다.
- **최종 승인 검토 문장(제안):** 정지 유체에서 위쪽을 양의 `z`로 잡으면 `dP/dz=−ρg`이다. 아래점과 위점의 압력차 `P_b−P_t`는 두 높이 사이의 `ρg` 적분이며, 밀도가 일정하면 `ρgΔh`이다. 전송기의 지시 부호는 실제 H/L 연결과 각 측의 수두를 기준으로 판단한다.
- **출처 및 적용범위:** [Yokogawa IM 01C20C01-01E §7.4, pp. 7-5–7-6](https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf), specific-gravity/head span calculation; differential equation and sign convention are hydrostatic derivation under the stated coordinate convention.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** PINNED_TOPIC_HASH: 같은 DP Topic 전체 `fact_anchor.json` 해시가 Ledger에 고정. Owner-authorized update required.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `dp_level_hydrostatic_pressure_principle` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 10. om_asset_register_system_boundary

- **PR / Topic / Anchor ID / Registry ID:** #47 / `control_system_operations_maintenance_calibration_inspection_spares_kpi` / `om_asset_register_system_boundary` / `iso14224_equipment_id_function_location_and_reliability_taxonomy`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** ISO 14224의 석유·천연가스·석유화학 분야 신뢰성·정비 데이터 체계에서는 장비 식별번호가 장비 기능과 물리적 위치를 식별하며, 장비 taxonomy와 신뢰성 평가에 관련된 장비 속성을 수집한다. 이 표준은 모든 계측자산에 적용되는 완전한 asset-register 필드 목록을 정하지 않는다.
- **기존 Registry statement:** Within ISO 14224:2016's petroleum, natural gas and petrochemical scope, equipment identification numbers identify equipment function and physical location; reliability/maintenance data include equipment taxonomy and relevant equipment attributes. The standard excludes complete equipment data sheets and additional on-service data an operator may separately consider useful, so it does not define a universal complete instrumentation asset-register schema.
- **최종 승인 검토 문장(제안):** ISO 14224의 석유·천연가스·석유화학 설비 맥락에서 장비 태그는 기능과 물리적 위치를 식별하는 데 쓰고, 제조 일련번호는 개별 장비와 교체 이력을 식별하는 데 쓴다. 신뢰성·정비 데이터 항목은 해당 분류체계와 분석 목적에 맞춰 정한다.
- **출처 및 적용범위:** [ISO 14224:2016 §§3.91–3.92 and official scope](https://www.iso.org/standard/64076.html). Applies to petroleum, petrochemical and natural-gas industries; not a universal complete instrumentation asset-register schema.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** PINNED_TOPIC_HASH: 해당 Topic `fact_anchor.json` source is covered by prior ledger. Existing hash guard remains; approval must use formal review/update flow.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `iso14224_equipment_id_function_location_and_reliability_taxonomy` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/control_system_operations_maintenance_calibration_inspection_spares_kpi/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 11. manifold_isolation_sequence

- **PR / Topic / Anchor ID / Registry ID:** #47 / `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation` / `manifold_isolation_sequence` / `rosemount_2051_three_valve_zero_check_isolation_side_sequence`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** Rosemount 2051 3-valve manifold의 zeroing 예에서는 LP isolation을 먼저 닫고 center equalizing valve를 열어 양측 압력을 equalize한다. 이 구성은 별도 bleed valve가 없으므로 equalizer를 bleed로 표현하거나 이 절차를 일반적인 depressurization 절차로 확대하지 않는다.
- **기존 Registry statement:** Rosemount 2051 3-valve manifold의 zeroing 예에서는 LP isolation을 먼저 닫고 center equalizing valve를 열어 양측 압력을 equalize한다. 이 구성은 별도 bleed valve가 없으므로 equalizer를 bleed로 표현하거나 이 절차를 일반적인 depressurization 절차로 확대하지 않는다.
- **최종 승인 검토 문장(제안):** Rosemount 2051의 해당 3밸브 매니폴드 영점 확인 절차에서 차단 밸브 두 개와 평형 밸브 한 개를 구분한다. 해당 구성의 전송기에 별도로 설치된 drain/vent는 매니폴드의 평형 밸브와 다른 기능이다. 영점 확인과 감압에는 설치 구성에 맞는 제조사 및 현장 승인 절차를 적용한다.
- **출처 및 적용범위:** [Emerson/Rosemount 2051 Reference Manual 00809-0100-4101 §2.8.4, Table 2-7, pp. 32–33](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-00809-0100-4101.pdf). Product/configuration-specific zeroing sequence; does not authorize generic depressurization or equate an equalizer with a bleed valve.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** MANAGED_SOURCE_HASH: managed Topic `topic_status.json` approved_source_hash and source sheet hash protect this content; use the formal topic approval workflow.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `rosemount_2051_three_valve_zero_check_isolation_side_sequence` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 12. production_schedule_adherence_delivery_kpi

- **PR / Topic / Anchor ID / Registry ID:** #47 / `instrumentation_production_management_planning_quality_cost_resources` / `production_schedule_adherence_delivery_kpi` / `production_schedule_kpi_defines_freeze_period_and_completion_basis`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** 생산 일정 준수·완료 KPI를 사용할 때에는 기준계획의 freeze 시점, 측정기간, 완료 판정, numerator와 denominator를 문서화해야 한다. ISO 22400은 KPI를 공식과 구성요소·시간특성으로 기술하며, SAP Schedule Attainment는 일정기간과 freeze 시점의 planned work를 기준으로 비교하는 구현 예를 제공한다. 지연 원인 분류는 현장의 데이터와 개선 목적에 맞춰 별도로 정의한다.
- **기존 Registry statement:** A production schedule adherence/attainment KPI needs an explicit planned-schedule snapshot or freeze point, measurement period, completion rule, and numerator/denominator so that the reported value has a reproducible meaning. ISO 22400 describes manufacturing KPIs with formulas, elements, time behaviour and units; SAP documentation provides one schedule-attainment implementation based on work planned at schedule freeze and completed as planned. Cause categories for lateness are organization-specific rather than a universal required taxonomy.
- **최종 승인 검토 문장(제안):** 생산 일정 준수·완료 KPI는 기준계획의 버전, 측정기간, 완료 판정, 분자와 분모를 정의한다. 계획 동결 시점을 사용하는 KPI에서는 동결 기준을 명시한다. ISO 22400의 KPI 기술 방식과 SAP의 Schedule Attainment 구현 예는 각각의 적용 범위에서 참고한다.
- **출처 및 적용범위:** [ISO 22400-2:2014 §4, KPI description structure](https://www.iso.org/obp/ui/?_escaped_fragment_=iso%253Astd%253A54497%253Aen); [SAP Key Information for Tracking Schedule Execution](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/8308e6d301d54584a33cd04a9861bc52/9a3262c243ef4c649eaeed4e63bf510f.html). Freeze point is a SAP/selected KPI implementation basis, not mandatory for every schedule metric.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** EXACT_REGISTRY_CONTRACT: canonical/Registry exact-statement contract is tested. Formal approval must update both under the approved process; no manual hash change.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `production_schedule_kpi_defines_freeze_period_and_completion_basis` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/instrumentation_production_management_planning_quality_cost_resources/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 13. tolerable_risk_alarp

- **PR / Topic / Anchor ID / Registry ID:** #47 / `sil_target_determination_risk_reduction_and_lifecycle` / `tolerable_risk_alarp` / `sil_tolerable_risk_alarp`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** 허용 가능한 사건빈도 또는 위험 기준은 조직이 승인한 개인·사회적 위험 기준과 consequence category에 따라 정한다. ALARP에서는 관련 good practice와 추가 위험저감조치를 우선 검토하고, 조치를 시행하지 않을 때는 비용·시간 등의 희생이 얻는 위험감소에 비해 현저히 불균형하다는 근거를 제시한다.
- **기존 Registry statement:** 허용 가능한 사건빈도 또는 위험 기준은 조직이 승인한 개인·사회적 위험 기준과 consequence category에 따라 정한다. ALARP에서는 관련 good practice와 추가 위험저감조치를 우선 검토하고, 조치를 시행하지 않을 때는 비용·시간 등의 희생이 얻는 위험감소에 비해 현저히 불균형하다는 근거를 제시한다.
- **최종 승인 검토 문장(제안):** 위험 허용 기준은 적용 법령·규제 및 승인된 위험 기준과 결과 범주에 따라 정한다. 영국 ALARP 문맥에서는 관련 모범 관행과 추가 위험저감조치를 검토하며, 조치를 합리적으로 실행할 수 없다고 판단할 때에는 필요한 희생이 안전상 이익에 비해 현저히 불균형한지 검토한다.
- **출처 및 적용범위:** [UK HSE ALARP at a glance](https://www.hse.gov.uk/enforce/expert/alarpglance.htm); [UK HSE Functional Safety Inspection Guide, Appendix 4](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf). ALARP/gross-disproportion wording is jurisdiction-scoped to the UK legal/practice context; risk criteria otherwise follow applicable jurisdiction/approved organization criteria.
- **정본 상태:** PR #47에서 원문 정본은 그대로 둠; Registry/정본 승인 연결 대기
- **Ledger/hash 영향:** PINNED_TOPIC_HASH: SIL Topic `fact_anchor.json` whole-file hash is in the existing Promotion Ledger. Formal owner review required.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `sil_tolerable_risk_alarp` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/sil_target_determination_risk_reduction_and_lifecycle/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 14. digital_twin_definition

- **PR / Topic / Anchor ID / Registry ID:** #47 / `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control` / `digital_twin_definition` / `iso_23247_manufacturing_digital_twin_is_fit_for_purpose_and_synchronized`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** ISO 23247-1:2021의 제조용 digital twin은 관측 가능한 제조 요소의 목적에 적합한 디지털 표현이며, 해당 요소와 그 표현 사이의 동기화를 포함한다. 구체적인 동기화 방식과 주기는 용도에 따라 정한다.
- **기존 Registry statement:** ISO 23247의 제조 맥락에서 digital twin instance는 observable manufacturing element의 fit-for-purpose digital representation이며 physical element와 digital representation 간 synchronization을 제공한다. 이는 제조 분야 표준의 정의다. NIST는 여러 분야에서 단일 통일 digital-twin 정의가 없다고 설명하므로, 이 정의와 목적·수명주기 요소를 모든 분야의 보편 요건으로 확대하지 않는다.
- **최종 승인 검토 문장(제안):** ISO 23247-1:2021의 제조용 digital twin은 관측 가능한 제조 요소의 목적에 적합한 디지털 표현이며, 해당 요소와 그 표현 사이의 동기화를 포함한다. 구체적인 동기화 방식과 주기는 용도에 따라 정한다.
- **출처 및 적용범위:** [ISO 23247-1:2021 official scope](https://www.iso.org/standard/75066.html); [ISO Smart Manufacturing White Paper, Annex A](https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100459.pdf). Manufacturing framework only; synchronization is at an appropriate, use-dependent rate. Do not generalize as a single cross-industry definition.
- **정본 상태:** PR #47 정본 수정 반영됨; Registry 재대조 미승인
- **Ledger/hash 영향:** PR #47 canonical source changed; no exact row in bounded-promotion ledger. Registry statement/provenance amendment remains unapproved; current score overlay is not excluded.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `iso_23247_manufacturing_digital_twin_is_fit_for_purpose_and_synchronized` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 15. half_bridge_sensitivity_compensation

- **PR / Topic / Anchor ID / Registry ID:** #47 / `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error` / `half_bridge_sensitivity_compensation` / `half_bridge_sensitivity_compensation`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** 두 활성 게이지가 같은 크기의 반대 변형을 받아 출력이 합산되도록 결선하면, 작은 변형에서 한 활성 게이지를 쓰는 회로보다 감도가 높다. 활성 게이지 하나와 무변형 보상 게이지는 온도 영향 상쇄에 쓰이며 두 활성 게이지의 감도 증가를 만들지 않는다. 회로 명칭은 배치와 제조사 분류를 확인한다.
- **기존 Registry statement:** Half bridge는 두 개의 게이지를 사용한다. 두 활성 게이지를 출력이 합산되도록 배치하면 Quarter bridge보다 감도가 높아지고, 활성·더미 구성은 주로 온도보상을 제공한다.
- **최종 승인 검토 문장(제안):** 두 활성 게이지가 같은 크기의 반대 변형을 받아 출력이 합산되도록 결선하면, 작은 변형에서 한 활성 게이지를 쓰는 회로보다 감도가 높다. 활성 게이지 하나와 무변형 보상 게이지는 온도 영향 상쇄에 쓰이며 두 활성 게이지의 감도 증가를 만들지 않는다. 회로 명칭은 배치와 제조사 분류를 확인한다.
- **출처 및 적용범위:** [Micro-Measurements, Introduction to Strain Gage Measurements](https://docs.micro-measurements.com/?id=13752), half-bridge/dummy-gage arrangements; [NI SCXI-1520 manual, Ch. 4 Fig. 4-4](https://download.ni.com/support/manuals/372583e.pdf), which classifies one active/one dummy wiring as a quarter-bridge type; sensitivity comparison is first-order Wheatstone-bridge derivation for the stated wiring.
- **정본 상태:** PR #47 정본 수정 반영됨; Registry 재대조 미승인
- **Ledger/hash 영향:** PR #47 canonical source changed; existing source file has no direct bounded-promotion ledger row. Registry amendment not approved; currently excluded from scoring.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `half_bridge_sensitivity_compensation` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 16. resistive_sensor_ac_measurement

- **PR / Topic / Anchor ID / Registry ID:** #47 / `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `resistive_sensor_ac_measurement` / `some_resistive_humidity_sensors_require_ac_excitation`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `false`
- **현재 Anchor 정본:** 저항식 습도 센서의 여자 방식은 소자 사양에 따른다. HDK는 HIS-08V가 포함된 HIS-08 계열 저항식 소자에 AC 구동을 지정하고 DC 인가를 제한한다. 구동 파형·주파수와 판독 회로는 해당 제품 지침을 확인한다.
- **기존 Registry statement:** Some resistive humidity elements use AC excitation to avoid polarization. The HDK HIS-08V polymer sensor documentation specifies AC drive and warns that DC voltage can change sensor characteristics and lead to failure; excitation waveform, frequency, voltage, and readout circuit must follow the specific product instructions.
- **최종 승인 검토 문장(제안):** 저항식 습도 센서의 여자 방식은 소자 사양에 따른다. HDK는 HIS-08V가 포함된 HIS-08 계열 저항식 소자에 AC 구동을 지정하고 DC 인가를 제한한다. 구동 파형·주파수와 판독 회로는 해당 제품 지침을 확인한다.
- **출처 및 적용범위:** [HDK KRH1901003 §§3-3, 4, pp. 3–4](https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf), model/family-specific AC drive and DC warning; [TI Precision Analog Seminar, pp. 2-44–2-45](https://www.ti.com/lit/pdf/slyp160) says most resistive humidity sensors use AC to prevent polarization. Do not state all resistive sensors require AC or assert a general mechanism from a product source alone.
- **정본 상태:** PR #47 정본 수정 반영됨; Registry 재대조 미승인
- **Ledger/hash 영향:** PR #47 canonical source updated; no direct ledger row. Registry row amendment remains pending; current scoring exclusion is false, so any source wording change requires targeted score regression.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `some_resistive_humidity_sensors_require_ac_excitation` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/humidity_measurement_capacitive_resistive_dew_point_selection_compensation/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 17. pst_not_full_proof_test

- **PR / Topic / Anchor ID / Registry ID:** #47 / `final_control_element_sil_sis_esd_valve_partial_stroke_test` / `pst_not_full_proof_test` / `partial_stroke_exercise_is_not_full_proof_test`
- **현재 Registry 검토상태:** `approved/verified` (기존 상태; 이 제안의 재승인을 뜻하지 않음)
- **현재 scoring exclusion:** `true`
- **현재 Anchor 정본:** 부분행정시험은 실제 시험 자극으로 검출할 수 있는 고장모드에 한해 시험범위를 인정한다. 완전 행정, 요구 격리 및 시트 누설 검증은 SRS가 요구하는 성능과 고장모드를 해당 시험 절차가 실제로 확인하는 경우에만 인정한다.
- **기존 Registry statement:** Actuator exercise or partial-stroke action can reveal some failures or degradation and improve diagnostic coverage, but HSE distinguishes it from proof testing; partial tests do not test every dangerous failure mode.
- **최종 승인 검토 문장(제안):** 부분행정시험은 실제 시험 자극으로 검출할 수 있는 고장모드에 한해 시험범위를 인정한다. 완전 행정, 요구 격리 및 시트 누설 검증은 SRS가 요구하는 성능과 고장모드를 해당 시험 절차가 실제로 확인하는 경우에만 인정한다.
- **출처 및 적용범위:** [HSE OG54 Appendix 1 §§35–43](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf) and [Appendix 3](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf). Test credit depends on detectable failure modes and actual procedure; neither a PST label nor full stroke alone proves every required isolation/leakage criterion.
- **정본 상태:** PR #47 정본 수정 반영됨; Registry 재대조 미승인
- **Ledger/hash 영향:** PR #47 canonical source updated. Registry row and existing review record remain unchanged; current exclusion overlay true.
- **승인 후 최소 파일 경로:** `grading/evidence/approved_fact_registry.json`의 `partial_stroke_exercise_is_not_full_proof_test` 행과 검토 provenance. 관련 소유 정본은 `rubrics/topic_packs/final_control_element_sil_sis_esd_valve_partial_stroke_test/fact_anchor.json`; Source Sheet/README는 기존 workflow가 요구하는 경우에만 함께 갱신. 공식 approval/review ledger는 승인 tool을 통해 기록하고 수동 hash 수정 금지. Generated 영향이 있으면 공식 builder로 6개 bank 재생성 후 freshness 검사.
- **예상 기존 채점 영향:** Registry 승인만으로 점수를 바꾸지 않는다 (`score_effect=none`). 기존 exclusion을 그대로 둔다. exclusion이 false인 항목도 이 제안만으로 점수/상태가 변하지 않아야 하며, 정본 source를 추가 수정하는 경우 143개 baseline 및 해당 Topic 집중 재생이 필수다.

## 승인자가 확인할 순서

1. 각 출처가 해당 주장 전체를 지지하는지, 제조사·표준·관할 범위가 문장에 남아 있는지 확인한다.
2. 제안 문장이 Registry의 기존 관계/조건을 변경하는지, 단지 설명을 명료화하는지 구분한다. 특히 계산 도출은 공식 원문 인용과 별도로 도출 가정·단위를 승인 기록에 남긴다.
3. `score_excluded=true` 항목은 제외 상태 그대로 승인할 수 있다. 승인 결과를 scoring admission 승격으로 취급하지 않는다.
4. source hash/managed Topic 제약이 있는 항목은 owner-authorized official flow로만 변경하고, 기존 source hash나 ledger record를 수동 overwrite하지 않는다.
5. 채점 변화가 관측되면 Registry 승인으로 정당화하지 말고 해당 source change의 점수 근거와 기존/신규 답안 영향을 별도 검증한다.

## 현재 상태

**PENDING_OWNER_REVIEW — 0/17 newly approved.** 현재 PR #46과 #47은 Draft다. 이 목록은 승인 패킷이며 승인 기록을 대신하지 않는다.
