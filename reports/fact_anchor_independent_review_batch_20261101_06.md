# Fact Anchor source verification batch 06 — Hydrostatic DP level and optical ranging

Reviewed on 2026-11-01. Pre-existing verified count: 119/1,290. Newly checked 16 claims. Cumulative 135/1,290. Remaining 1,155. Outcome of this batch: 14 conditional KEEP, 2 REVISE, 0 falsehood rejections.

Primary original inspected:
- Yokogawa Electric, **Model EJ210 and EJ220 Flange Mounted Differential Pressure Transmitter**, User's Manual IM 01C20C01-01E, **9th edition June 2006**, §7.4, printed pp. 7-5–7-6, web PDF https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf (PDF page indices 24–25 visually examined).
- Hamamatsu Photonics, **Measuring distance with light**, April 2, 2015, sections Active triangulation and Direct time of flight, Eqs. 3–4 and 6–7, figures 4 and 8, https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Baumer, **Ultrasonic sensors – function**, §Measuring range / Distance measurement, https://www.baumer.com/pl/en/service-support/function-principle/ultrasonic-sensors---function/a/Know-how_Function_Ultrasonic-sensors

**Citation metadata discrepancy:** the 10 current Registry verification_refs citing this Yokogawa PDF incorrectly call it Y/11, Y/12, Y/13, Y/14 and Y/15 Series. The actual cover says EJ210/EJ220, IM 01C20C01-01E, 9th edition (June 2006). This is an evidence-citation correction to apply in canonical Registry separately under normal protected source and validation procedure; it does not imply the correctly limited static-head formulas are false.

## Claim-to-source decisions

### 1. `dp_level_hydrostatic_pressure_principle` — KEEP_BOUNDED
- Original Registry statement: 정지 유체의 압력수두는 밀도와 높이에 의존하며, 밀도가 일정한 액주에서는 ΔP=ρgΔh이다. 따라서 차압식 레벨은 밀도가 일정하다는 가정 없이 높이만 직접 측정하지 않는다.
- Source locator: Yokogawa §7.4 p7-5. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Hydrostatic head is measured from liquid specific gravity multiplied by height with constant-density assumption.
- Conditions: static_or_hydrostatic_column; density_constant_for_linear_equation
### 2. `dp_level_open_tank_equation` — KEEP_BOUNDED
- Original Registry statement: 개방탱크의 DP 범위 계산은 액주수두와 설치 기준고도를 반영하며, 송신기 고도 차이에 따라 LRV에 zero suppression 또는 elevation이 생길 수 있다.
- Source locator: Yokogawa §7.4(1) p7-5. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Open tank high/low port and hydrostatic LRV/span with positive zero suppression are shown, including transmitter height.
- Conditions: low_pressure_side_vented_to_atmosphere; actual_tap_and_transmitter_elevations_used
### 3. `dp_level_closed_tank_vapor_pressure_cancellation` — KEEP_BOUNDED
- Original Registry statement: 밀폐탱크에서 탱크 기상압을 고압측과 저압측에 공통으로 전달하는 구성에서는 공통 기상압이 DP 계산에서 상쇄되며, dry-leg 범위는 개방탱크와 같은 방식으로 산정할 수 있다.
- Source locator: Yokogawa §7.4(2) p7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Top vapor pressure shared at both ports cancels for dry leg; dry low-pressure line must stay gas-filled.
- Conditions: same_vapor_pressure_reaches_both_sides; dry_leg_remains_gas_filled_without_liquid_head
### 4. `dp_level_wet_leg_reference_head` — KEEP_BOUNDED
- Original Registry statement: 밀폐탱크 wet-leg 구성에서는 저압측 기준액의 액주수두가 측정 DP에서 차감된다. 정수 기준과 동일한 단위계에서 LRV 항은 고압측 최소 액주수두에서 저압측 wet-leg 기준수두를 뺀 값이다.
- Source locator: Yokogawa §7.4(3) p7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Wet leg LRV is y*GL - d*GS, with high-side liquid and reference-head terms correctly signed.
- Conditions: reference_leg_filled_to_defined_height; reference_liquid_density_and_geometry_known
### 5. `dp_level_reference_elevation_and_span` — KEEP_BOUNDED
- Original Registry statement: 차압 범위의 LRV와 URV는 0%·100%의 가변 액주수두뿐 아니라 설치고도와 impulse-line 고정수두를 부호를 포함해 반영한다. 같은 밀도·고정배치에서 Span은 가변 레벨 구간에 따른 압력차이다.
- Source locator: Yokogawa §7.4(1,3) pp7-5–7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Both LRV/URV depend on fixed head and variable level; span equals variable level span when fixed heads constant.
- Conditions: actual_geometry_and_fluid_densities_used; lrv_and_urv_evaluated_at_defined_level_endpoints
### 6. `dp_level_dry_leg_configuration` — KEEP_BOUNDED
- Original Registry statement: 밀폐탱크 dry-leg 방식은 저압측 impulse line을 기상부에 연결해 기상압을 전달하며, 저압측 도압관의 액체수두가 무시될 만큼 기상 상태를 유지해야 범위 계산에서 추가 액주항을 생략할 수 있다.
- Source locator: Yokogawa §5.2.2 & §7.4(2) p7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Dry reference leg transmits vapor pressure to low side; liquid accumulation invalidates nominal dry-leg reference.
- Conditions: low_side_line_remains_gas_filled; liquid_condensate_head_negligible
### 7. `dp_level_dry_leg_condensation_error` — KEEP_BOUNDED
- Original Registry statement: 정상적으로 고압측−저압측을 측정하는 DP 구성에서 dry-leg 저압측에 응축액 액주가 생기면 저압측 압력이 증가하여 측정 DP가 감소한다. 액주 크기와 탭 구성에 따라 레벨 지시오차가 생길 수 있다.
- Source locator: Yokogawa §7.4(2) & §7.5 p7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Manual says condensation can cause measurement error; for high-minus-low DP, positive condensate head on low leg mathematically lowers measured DP.
- Conditions: condensate_forms_positive_liquid_head_on_low_side; transmitter_differential_is_high_side_minus_low_side
### 8. `dp_level_zero_suppression_and_elevation` — KEEP_BOUNDED
- Original Registry statement: LRV가 양수인 DP range는 zero suppression, LRV가 음수인 DP range는 zero elevation으로 부른다. 이는 트랜스미터 자체의 물리적 설치 위치가 아니라 0% 공정조건에서 계산된 입력값의 부호에 관한 명칭이다.
- Source locator: Yokogawa §7.4(1,3) pp7-5–7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Positive LRV shown as suppression, negative as elevation, tied to calibration zero reference rather than physical instrument placement alone.
- Conditions: lrv_referenced_to_transmitter_differential_input_zero
### 9. `dp_level_density_compensation` — KEEP_BOUNDED
- Original Registry statement: 설치 고정수두를 제거하고 실제 액주 차압을 ΔP=ρ_actual·g·h_actual로 두면, 교정밀도 ρ_cal로 환산한 지시높이는 h_ind=ΔP/(ρ_cal·g)=(ρ_actual/ρ_cal)h_actual이다. 따라서 실제 밀도가 교정밀도보다 큰 조건에서는 지시높이가 실제높이보다 크게 계산된다.
- Source locator: Yokogawa §7.4 p7-5. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Direct derivation using DP=rho*g*h and calibrated rho gives h_ind/h_actual = rho_actual/rho_cal when fixed heads have been removed.
- Conditions: fixed_heads_compensated; uniform_density_over_measured_column; calibrated_density_used_for_conversion
### 10. `dp_level_process_temperature_density_error` — KEEP_BOUNDED
- Original Registry statement: 동일한 액주 높이에서도 운전밀도 변화는 정수압 차압을 바꾸므로, 교정 시 가정한 밀도와 운전밀도가 다르면 레벨 환산값에 오차가 생긴다. 따라서 범위 산정·밀도보정에는 해당 운전조건의 대표 밀도를 사용해야 한다.
- Source locator: Yokogawa §7.4 pp7-5–7-6. Primary: https://web-material3.yokogawa.com/IM01C20C01-01EN_009.pdf
- Comparison: Manual explicitly assumes constant fluid specific gravities GL and GS, so different actual density produces converted level error.
- Conditions: liquid_column_height_fixed; density_changes_between_calibration_and_operation
### 11. `active_triangulation_distance_uncertainty_depends_on_geometry` — KEEP_BOUNDED
- Original Registry statement: For active laser triangulation under the far-field approximation d >> f, the geometric mapping is d ≈ f b/u, where b is the baseline, f the imaging lens focal length, and u the detector spot coordinate. Propagating spot-coordinate uncertainty δu gives δd ≈ d² δu/(f b). For fixed distance and δu, a longer baseline or focal length reduces this modelled distance uncertainty, while uncertainty grows quadratically with distance. This idealized geometry is not a product performance specification.
- Source locator: Hamamatsu Active triangulation eq3–4. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Comparison: Explicit far-field d=f*b/u and uncertainty d^2*delta(u)/(f*b), with longer baseline reducing idealized coordinate-propagation uncertainty.
- Conditions: far_field_approximation_requires_distance_much_greater_than_focal_length; formula_is_for_idealized_active_triangulation_geometry; detector_spot_coordinate_uncertainty_is_delta_u; not_a_vendor_product_performance_specification
### 12. `direct_tof_target_surface_changes_return_pulse_amplitude` — KEEP_BOUNDED
- Original Registry statement: For the direct-ToF pulse receiver described by Hamamatsu, with a given telescope aperture, received return-light amount depends on target distance and reflection characteristics including color, orientation, and surface smoothness. At a fixed distance, these target characteristics can therefore change the received return-pulse amplitude. This is a configuration-specific signal-amplitude statement, not a universal SNR or uncertainty formula for all optical sensors.
- Source locator: Hamamatsu Direct ToF fig8 discussion. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Comparison: Returned-light pulse amplitude changes with object color/orientation/roughness and distance for fixed receiver aperture.
- Conditions: applies_to_the_hamamatsu_direct_tof_receiver_example_with_fixed_telescope_aperture; target_color_orientation_and_surface_smoothness_are_listed_as_reflection_characteristics; no_universal_snr_or_measurement_uncertainty_formula_is_claimed
### 13. `active_triangulation_shadowing_occultation_and_baseline_tradeoff` — KEEP_BOUNDED
- Original Registry statement: In active triangulation, shadowing occurs when the projector light cannot reach a target point, while occultation occurs when reflected light from that point cannot reach the camera/receiver. Reducing the baseline can reduce occultation, but the cited geometry incurs increased distance uncertainty. These are line-of-sight and geometry effects in the described triangulation setup.
- Source locator: Hamamatsu Active triangulation fig4. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Comparison: Separates target-to-camera occlusion from laser-to-target shadowing, and the baseline versus uncertainty tradeoff.
- Conditions: shadowing_blocks_projector_to_target_path; occultation_blocks_target_to_receiver_path; baseline_reduction_can_reduce_occultation_but_increases_distance_uncertainty_in_the_cited_setup; not_a_claim_about_all_optical_sensor_installation_errors
### 14. `direct_tof_timing_uncertainty_propagates_to_distance_uncertainty` — KEEP_BOUNDED
- Original Registry statement: For the described pulsed direct-ToF round-trip model in a medium of refractive index n, distance is d=ct/(2n) and timing uncertainty δt gives approximate range uncertainty δd≈cδt/(2n). The source identifies detector jitter, pulse rise-time variation, electrical noise, and threshold-crossing levels as contributors to timing variation in its example. Propagation speed alone therefore does not guarantee high ranging accuracy.
- Source locator: Hamamatsu Direct ToF eq6–7 and fig8. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Comparison: Explicit d=ct/(2n) and delta(d)=c*delta(t)/(2n), including timing jitter, rise time, electronic noise and threshold.
- Conditions: uses_round_trip_time_and_medium_refractive_index_n; uncertainty_relation_is_approximate_for_the_described_model; listed_timing_variations_are_from_the_hamamatsu_detection_example; no_universal_product_accuracy_or_resolution_is_claimed
### 15. `hamamatsu_direct_tof_uses_wavelength_centered_filter_for_background` — REVISE_REQUIRED
- Original Registry statement: In Hamamatsu’s described pulsed direct-ToF receiver, band-pass filters centered on the transmitted wavelength λ0 are used to reduce background light. This verifies a filter implementation example, not a universal requirement or the only ambient-light mitigation for optical sensors.
- Source locator: Hamamatsu Direct ToF before eq6. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html
- Comparison: The source confirms bandpass filters in the author's particular design, but that manufacturer implementation detail is too narrow for general-exam core Fact scoring.
- Conditions: specific_to_the_described_direct_tof_setup; filter_centered_on_transmitted_wavelength_lambda0; not_a_universal_filter_requirement_for_all_optical_sensors
- Proposed corrected wording (not promoted): Optical background-light suppression may employ wavelength-selective filtering centered on the transmitter band when suitable; method and design requirements depend on the application. The Hamamatsu example remains explanatory context, not an obligatory answer element.
### 16. `optical_vs_ultrasonic_tof_comparison` — REVISE_REQUIRED
- Original Registry statement: 반사형 Direct optical ToF는 왕복 광 비행시간 t와 매질 굴절률 n으로 d=ct/(2n)을 계산하고, 초음파 pulse-echo는 왕복 음향시간 t와 음속 c_s로 d=c_s·t/2를 계산한다. 따라서 두 방식 모두 왕복시간에서 편도거리를 얻지만 전파속도와 반환 신호(광반사/음향 에코)가 다르다. 탱크 ullage의 기체 경로에서는 음속이 기체 종류·온도·증기압의 영향을 받는다. 이는 비교 개요이며 초음파 보상·설치·에코 진단의 상세는 초음파 Topic 소유 범위다.
- Source locator: Hamamatsu eq6 and Baumer Distance measurement formula. Primary: https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html; corroboration: https://www.baumer.com/pl/en/service-support/function-principle/ultrasonic-sensors---function/a/Know-how_Function_Ultrasonic-sensors
- Comparison: Hamamatsu verifies optical round-trip d=ct/(2n); Baumer independently verifies ultrasonic d=t*c_s/2. The original further gas-composition/vapor-pressure and Topic-ownership assertions were not verified from these two source sections.
- Conditions: optical_equation_applies_to_reflected_direct_tof_with_medium_refractive_index_n; ultrasonic_equation_applies_to_reflected_pulse_echo_with_sound_speed_along_path; tank_ullage_gas_sound_speed_conditions_are_limited_to_gas_type_temperature_and_vapor_pressure; detailed_ultrasonic_compensation_and_installation_are_owned_by_adjacent_ultrasonic_topic
- Proposed corrected wording (not promoted): Reflected direct optical ToF and pulse-echo ultrasound both use half of a round-trip propagation time; propagation speeds differ (light in medium c/n, sound c_s). Specific gas temperature/composition/vapor effects and repository ownership should be separate claims.
## Safeguards

- Previously excluded 276 remain excluded; source-revision holds increased from 40 to 42, without silently converting revised statements to accepted core anchors.
- The 1,155 still unreviewed claims have no independent approval from this batch; historical Registry verified status alone is not evidence of a fresh source comparison.
- No generated rubric rebuild, complete unit test, CI or release gate is claimed. The canonical Registry and Topic Packs were not modified; metadata repair remains outstanding.
