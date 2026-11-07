# Canonical optical and software structural-coverage source checks — 2026-11-01

Original source statements retrieved from project canonical Topic Packs; independently compared with OMRON original technical documentation and MathWorks original reference documentation (R2026b). Reviewer GPT-6, AI, 2026-11-01. Not a human or release approval. No generated bank changed.

11 direct matches are KEEP_BOUNDED with limitations; 3 other IDs remain NOT_PERFORMED because missing direct evidence for all canonical clauses. No general scoring claim is authorized by the 3 holds.

## 1. optical_direct_tof_round_trip_distance_equation

- Canonical: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `optical_direct_tof_distance_equation`
- Statement: 같은 센서 위치에서 방사·수광하는 반사형 Direct ToF의 이상적 거리관계는 d=c·Δt/2이며, c는 광의 전파속도이고 2는 송신과 반사의 왕복경로를 보정한다.
- Publisher original: https://www.omron.com/global/en/technology/omrontechnics/vol53/007.html
- Specific locator: Sec.2.1 TOF direct, d=c*t/2
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Monostatic reflected light d=cΔt/2 from round-trip flight; account for medium refractive index and delay calibration.

## 2. indirect_tof_uses_modulated_light_phase_delay

- Canonical: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `optical_indirect_tof_phase_principle`
- Statement: Indirect ToF는 변조된 광의 송신신호와 수신신호 사이 위상지연을 측정해 왕복 전파지연을 추정하며, 단일 변조주파수의 대표식은 d=c·φ/(4πf_m) 형태로 표현할 수 있다.
- Publisher original: https://www.omron.com/global/en/technology/omrontechnics/vol53/007.html
- Specific locator: Sec.2.2 phase difference indirect time of flight
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Phase range equation for sinusoidal modulation φ in radians; distance wraps every c/(2f_m) without extra modulation/frequency disambiguation; c is speed in path medium.

## 3. through_beam_photoelectric_sensing_uses_opposed_emitter_receiver

- Canonical: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `photoelectric_through_beam_mode`
- Statement: 투과형 광전센서는 발광기와 수광기를 서로 마주보게 배치하고 대상이 광로를 차단할 때 수광량 변화로 존재를 검출하므로 긴 검출거리와 높은 광학 여유를 얻기 쉽다.
- Publisher original: https://www.ia.omron.com/support/guide/43/introduction.html
- Specific locator: Through-beam Sensors: emitter and receiver opposite, beam interruption
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Separate emitter and receiver detect obscuration of optical path; long ranges are potential, model/ambient/target limitations apply.

## 4. diffuse_photoelectric_sensing_uses_target_scattered_light

- Canonical: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `photoelectric_diffuse_reflective_mode`
- Statement: 확산반사형 광전센서는 센서에서 방사한 광이 대상 표면에서 산란되어 되돌아오는 수광량을 이용하므로 대상의 반사율·색상·표면각도와 배경의 영향을 더 크게 받을 수 있다.
- Publisher original: https://www.ia.omron.com/support/guide/43/introduction.html
- Specific locator: Diffuse Reflective Sensors, sensing methods and reflectivity limitations
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Returned target-reflected light causes detection, influenced by surface, color, alignment and background. Not absolute distance without calibrated geometry.

## 5. diffuse_photoelectric_intensity_and_distance_setting_principle_boundary

- Canonical: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `photoelectric_intensity_boundary`
- Statement: 확산반사형 광전센서의 수광량 기반 검출에서는 대상 표면의 색과 매끄러움에 따라 반사광량, 동작 안정성과 sensing distance가 달라질 수 있으므로, 수광량만으로 장치 독립적인 절대거리를 정할 수 없다. 별도의 distance-setting 센서는 반사 spot 위치 또는 분할 수광소자 간 광량 차를 이용할 수 있어 두 방식을 구분한다.
- Publisher original: https://www.ia.omron.com/support/guide/43/introduction.html
- Specific locator: Diffuse-reflective versus distance-settable sensor overview
- Decision: **HOLD_NEEDS_DISTANCE_SETTING_MECHANISM_SOURCE**
- Claim/evidence mapping, exclusions and limits: Source supports qualitative distinction and intensity sensitivity, but detailed split-receiver spot geometry is not clearly established in this particular primary page.

## 6. statement_coverage_executes_each_executable_statement_only

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_statement_coverage`
- Statement: Statement Coverage는 실행 가능한 각 문장 또는 구문이 최소 한 번 실행되었는지를 평가하지만 Decision 내부 조건의 독립 영향은 보장하지 않는다.
- Publisher original: https://www.mathworks.com/help/slcoverage/ug/types-of-code-coverage.html
- Specific locator: Statement Coverage paragraphs
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Executing each executable statement once does not establish independent decision condition effects or requirements correctness.

## 7. condition_coverage_exercises_each_condition_outcome_not_decision_effect

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_condition_coverage`
- Statement: Condition Coverage는 각 원자 조건이 True와 False를 모두 취했는지를 확인하지만 그 변화가 Decision 결과를 바꾸었다는 독립 영향 증거는 아니다.
- Publisher original: https://www.mathworks.com/help/slcoverage/ug/types-of-code-coverage.html
- Specific locator: Condition Coverage definition
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Atomic conditions true and false are tested, but they need not independently affect decision output.

## 8. decision_coverage_exercises_decision_true_and_false_not_condition_effect

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_decision_coverage`
- Statement: Decision 또는 Branch Coverage는 각 Decision 결과가 True와 False를 모두 취했는지를 확인하지만 개별 조건이 결과를 실제로 좌우했는지는 입증하지 못한다.
- Publisher original: https://www.mathworks.com/help/slcoverage/ug/types-of-code-coverage.html
- Specific locator: Decision Coverage definition
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Each Boolean decision true and false is executed; individual-condition influence not proven.

## 9. mcdc_structural_criterion_targets_independent_condition_effect

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_purpose`
- Statement: MC/DC는 복합 Boolean Decision에서 각 원자 조건이 다른 조건의 영향과 구분되어 Decision 결과에 독립적으로 영향을 미치는지를 입증하는 구조적 커버리지 기준이다.
- Publisher original: https://www.mathworks.com/help/matlab-test/ug/types-of-code-coverage-for-matlab-source-code.html
- Specific locator: MC/DC criteria section
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Each condition independently flips decision output; structural coverage is one element of V&V, not proof of safety requirement satisfaction.

## 10. mcdc_independence_pair_changes_decision_via_target_effect

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_independent_effect_pair`
- Statement: 조건 하나의 독립 영향 Test Pair는 대상 조건의 값 변화가 Decision 결과를 변화시키고 나머지 조건은 고정되거나 그 Pair에서 결과에 영향을 줄 수 없도록 마스킹되어야 한다.
- Publisher original: https://www.mathworks.com/help/matlab-test/ug/types-of-code-coverage-for-matlab-source-code.html
- Specific locator: MC/DC example X||(Y&&Z), test pairs
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: A pair demonstrates target condition's effect and opposite decision results, with other conditions fixed or masked.

## 11. mcdc_masking_allows_non_target_changes_when_effect_masked

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_masking`
- Statement: Masking MC/DC는 다른 조건도 값이 달라질 수 있으나 Boolean 마스킹으로 그 조건들이 Decision 결과에 영향을 줄 수 없음을 보인 상태에서 대상 조건의 독립 영향을 입증한다.
- Publisher original: https://www.mathworks.com/help/slcoverage/ref/mcdcmode.html
- Specific locator: MCDC mode masking vs unique cause
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: Masking allows other conditions to vary only if their effect on decision is masked; not equivalent to arbitrary non-target changes.

## 12. mcdc_inactive_boolean_branch_masks_other_condition_effect

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_masked_inactive_condition`
- Statement: OR 식에서 이미 True인 조건이나 AND 식에서 이미 False인 조건은 다른 조건의 영향을 마스킹하므로 독립 영향 Pair 선정 시 각 조건의 활성 상태를 확인해야 한다.
- Publisher original: https://www.mathworks.com/help/matlab-test/ug/types-of-code-coverage-for-matlab-source-code.html
- Specific locator: MCDC example X||(Y&&Z) explanation
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping, exclusions and limits: For OR, true input masks others; for AND, false input masks others, in corresponding combinational Boolean semantics.

## 13. mcdc_condition_coupling_can_invalidate_unique_cause_pairs

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_coupled_conditions`
- Statement: 동일 변수나 논리적으로 종속된 조건이 한 Decision에 반복되면 조건을 독립적으로 변화시킬 수 없어 Unique-cause MC/DC가 불가능할 수 있으므로 식의 재구성 또는 Masking 근거가 필요하다.
- Publisher original: https://www.mathworks.com/help/slcoverage/ref/mcdcmode.html
- Specific locator: Unique-Cause MCDC requires other inputs fixed
- Decision: **HOLD_NEEDS_DEPENDENCE_COUNTEREXAMPLE**
- Claim/evidence mapping, exclusions and limits: The source defines unique cause, but does not itself specifically address repeated correlated conditions and their infeasible independently varied pairs.

## 14. mcdc_mcc_exercises_all_condition_combinations

- Canonical: `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` / `mcdc_multiple_condition_coverage`
- Statement: Multiple Condition Coverage는 가능한 조건 조합을 폭넓게 시험하는 기준이며 조합 수가 지수적으로 증가하므로 MC/DC와 목적·비용을 구분해야 한다.
- Publisher original: https://www.mathworks.com/help/matlab-test/ug/types-of-code-coverage-for-matlab-source-code.html
- Specific locator: MC/DC contrasts with all combinations
- Decision: **HOLD_MCC_SCOPE_PRIMARY_NOT_EXPLICIT**
- Claim/evidence mapping, exclusions and limits: Source confirms MC/DC can reduce tests versus combinations but does not clearly define formal Multiple Condition Coverage scope for all feasible combinations.


`KEEP_BOUNDED` remains subject to scoring-eligibility, original exclusion overlays, and independent-revision holds. No CI/focused test run occurred.