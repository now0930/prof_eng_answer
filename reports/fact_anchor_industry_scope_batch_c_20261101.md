# Fact Anchor 기술사 보편원리·물리식 대조 — Batch C (2026-11-01)

## 범위, 판정 규약
- 기준: `codex/essay-boundary-calibration-20261028` Registry 1,520행, 현행 Queue 1,290행. 이 문서는 Batch A/B와 **중복 없는 추가 71개 Fact ID**를 다룬다.
- `GENERAL_KEEP`은 물리식·측정원리·산업적 선택기준이 해당 기술적 조건과 함께 일관된다는 **채점 적합 후보**다. 모든 인용 표준 원문 전체를 대조했다는 의미가 아니며 Registry `verified` 재승인이 아니다.
- `GENERALIZE_PRODUCT_CASE`는 모델별 문구를 공학 원리로 치환할 권고, `REMOVE_PRODUCT_NUMERIC`은 제품 숫자를 **범용 필수 정답에서 배제**할 권고, `HOLD_MIXED_CLAIM`은 조합된 주장을 분리·추가 확인할 때까지 새 채점승격 보류.
- 이 Batch의 분류: GENERAL_KEEP 63건; GENERALIZE_PRODUCT_CASE 5건; REMOVE_PRODUCT_NUMERIC 2건; HOLD_MIXED_CLAIM 1건. **삭제·승인·generated 변경 0건**. 제조사 링크가 있다는 이유만으로 일반원리를 인증하지 않는다.

## 개별 판단 기록

| 번호 | Fact ID | 판정 | 기술 내용과 적용·배제 조건 |
|---:|---|---|---|
| 1 | `displacer_buoyancy_equals_displaced_liquid_weight` | `GENERAL_KEEP` | 침수 체적과 액체 밀도로 부력을 계산: Fb=ρgVsub |
| 2 | `displacer_density_change_can_bias_level_indication` | `GENERAL_KEEP` | 동일 침수체적에 대해 부력은 밀도에 비례, 지시 편향 발생 가능 |
| 3 | `displacer_force_sensing_differs_from_free_float_position_sensing` | `GENERAL_KEEP` | 현수형 displacer는 지지력 변화, float는 액면 추종 위치 검출 |
| 4 | `fisher_displacer_installation_and_maintenance_require_configuration_checks` | `GENERALIZE_PRODUCT_CASE` | 격리·부착·마찰·접근성은 범용 선정 관점; Fisher 설치 상세는 예시 |
| 5 | `fully_submerged_interface_displacer_force_depends_on_density_difference` | `GENERAL_KEEP` | 층별 체적 배분에 대한 Fb=g(ρL VL+ρU VU); 계면 감도는 밀도차에 비례 |
| 6 | `fisher_displacer_wet_and_dry_calibration_require_density_or_weight_compensation` | `GENERALIZE_PRODUCT_CASE` | Wet/Dry 등가 부력·하중 보상 개념 유지; 제조사 교정 순서·사양은 제외 |
| 7 | `dp_level_hydrostatic_pressure_principle` | `GENERAL_KEEP` | 정수압 ΔP=ρgΔh는 일정 밀도 조건이 핵심 |
| 8 | `dp_level_open_tank_equation` | `GENERAL_KEEP` | 탭·송신기 설치고도/정수두를 LRV 계산에 반영 |
| 9 | `dp_level_closed_tank_vapor_pressure_cancellation` | `GENERAL_KEEP` | 공통 기상압이 두 포트에 동일하게 전달되면 차압에서 상쇄 |
| 10 | `dp_level_wet_leg_reference_head` | `GENERAL_KEEP` | LP wet-leg 고정 수두는 HP-LP 측정 차압에서 감산 |
| 11 | `dp_level_wet_leg_zero_elevation` | `REMOVE_PRODUCT_NUMERIC` | 특정 Yokogawa 사례의 -23.73kPa 값은 범용 Fact가 아님; 음의 LRV 조건만 유지 |
| 12 | `dp_level_reference_elevation_and_span` | `GENERAL_KEEP` | LRV/URV는 고정수두와 가변수두의 부호·고도 기준을 반영 |
| 13 | `dp_level_dry_leg_configuration` | `GENERAL_KEEP` | LP 기상측 도압관이 dry 상태여야 액주 추가항을 무시 가능 |
| 14 | `dp_level_dry_leg_condensation_error` | `GENERAL_KEEP` | LP 도압관 응축 수두 증가→HP−LP 감소(명시된 포트 배치) |
| 15 | `dp_level_zero_suppression_and_elevation` | `GENERAL_KEEP` | LRV 양/음으로 zero suppression/elevation 용어 구별(정의된 범위 기준) |
| 16 | `dp_level_density_compensation` | `GENERAL_KEEP` | 같은 수두의 실제/교정 밀도 비가 환산 높이를 편향 |
| 17 | `dp_level_interface_density_difference` | `GENERAL_KEEP` | 두 액체 계면 DP 감도는 두 층의 밀도차에 비례 |
| 18 | `dp_level_process_temperature_density_error` | `GENERAL_KEEP` | 온도→밀도 변화→수두-레벨 환산 오차의 인과 |
| 19 | `dp_level_remote_seal_pressure_transfer_architecture_and_limits` | `GENERAL_KEEP` | 격리막·충전액으로 압력을 전달; 온도·정격·응답 영향은 구성별 |
| 20 | `rosemount_1159_capillary_length_increases_response_time` | `GENERALIZE_PRODUCT_CASE` | Capillary 길이·체적과 응답/온도오차의 상충관계만 유지; 1159의 세부 영향은 별도 |
| 21 | `remote_seal_signed_fill_fluid_static_head` | `GENERAL_KEEP` | 정수 충전액 두수와 부호를 고도 기준에 맞게 적용 |
| 22 | `rosemount_remote_seal_temperature_effect_mechanisms_scoped` | `GENERALIZE_PRODUCT_CASE` | 충전액 열팽창·밀도 변화는 일반 오차기전; Rosemount 특정 설계치는 제외 |
| 23 | `flow_volumetric_rate_area_integral` | `GENERAL_KEEP` | Q=∫v_n dA=A v평균, 국소속도와 단면평균 구별 |
| 24 | `flow_dp_primary_element_conditions` | `GENERAL_KEEP` | 유로 수축 ΔP의 유량 환산은 형상·Re·유체 물성·계수 조건 |
| 25 | `flow_pitot_local_velocity` | `GENERAL_KEEP` | 정체압-정압 속도수두는 국소 유속, 전체 유량엔 면적 평균 필요 |
| 26 | `flow_variable_area_meter` | `GENERAL_KEEP` | 부자력·유체력·중력의 평형 위치에서 테이퍼 유로면적 이용 |
| 27 | `flow_positive_displacement_meter` | `GENERAL_KEEP` | 정해진 계량실 부피의 반복 계수로 누적체적/유량 계산 |
| 28 | `flow_meter_principle_taxonomy` | `GENERAL_KEEP` | 터빈/와류/전자기식은 회전·와류주파수·유도전압으로 구분 |
| 29 | `flow_ultrasonic_transit_doppler` | `GENERAL_KEEP` | 상하류 전파시간차와 산란체 Doppler 주파수 이동을 구분 |
| 30 | `flow_coriolis_thermal_mass` | `GENERAL_KEEP` | 진동관 Coriolis 위상/비틀림과 열전달 기반 질량유량 원리 구분 |
| 31 | `flow_meter_selection_tradeoffs` | `GENERAL_KEEP` | 유체/유량범위/정확도/설치조건을 함께 고려; 모든 환경 공통 최적계기 없음 |
| 32 | `flow_process_condition_maintenance` | `GENERAL_KEEP` | 기포·고형물·맥동·오염 영향은 계측 원리별로 다름 |
| 33 | `rtd_excitation_voltage_measurement` | `GENERAL_KEEP` | 전류 I와 저항 양단전압 V에서 R=V/I(센서 여기) |
| 34 | `rtd_self_heating_thermal_error` | `GENERAL_KEEP` | P=I²R에 의한 자기발열·매질온도와의 차이 |
| 35 | `rtd_two_wire_lead_resistance_error` | `GENERAL_KEEP` | 2선식 Rmeas=RRTD+RL1+RL2; 금속 RTD 양의 기울기 구간에서 과대온도 |
| 36 | `rtd_three_wire_bridge_compensation_assumptions` | `GENERAL_KEEP` | 3선식 리드선 균형 가정이 깨지면 잔류 오차 |
| 37 | `rtd_four_wire_kelvin_measurement` | `GENERAL_KEEP` | Force/Sense 분리, 고입력 임피던스 전압측정으로 리드저항 오차 억제 |
| 38 | `rtd_measurement_chain_passive_sensor` | `GENERAL_KEEP` | 센서는 수동 저항 소자; 여기-전압-저항-온도 환산 체인 |
| 39 | `rtd_metal_resistance_temperature_principle` | `GENERAL_KEEP` | 금속의 저항 온도의존성과 백금의 안정성 |
| 40 | `rtd_transmitter_connection_signal_conditioning` | `GENERAL_KEEP` | 여기·보상·선형화·절연 기능의 유무는 장치 구성별로 검증 |
| 41 | `rtd_wiring_method_selection_tradeoff` | `GENERAL_KEEP` | 정확도/케이블/비용과 2·3·4선 보상 수준의 상충관계 |
| 42 | `rtd_channel_fault_checks_are_topology_and_device_dependent` | `GENERAL_KEEP` | 단선·단락·절연·누설은 실제 입력회로/진단지원에 맞춰 검사 |
| 43 | `rtd_calibration_uncertainty_depends_on_reference_bath_readout_and_sensor_application_effects` | `GENERAL_KEEP` | 소급 가능한 기준온도계·열원 균일성·리드·자기발열의 불확도 예산 고려 |
| 44 | `ultrasonic_echo_distance_uses_round_trip_time_over_two` | `GENERAL_KEEP` | 왕복시간 t를 편도 거리로 환산하면 d=ct/2 |
| 45 | `ultrasonic_distance_conversion_uses_medium_sound_speed` | `GENERAL_KEEP` | 음속은 전파매질에 의존; 가스 조성·온도 가정 필요 |
| 46 | `ultrasonic_air_temperature_changes_uncompensated_range` | `GENERAL_KEEP` | 온도 변화에 따른 음속 변화가 무보상 거리오차 초래 |
| 47 | `ultrasonic_pulse_echo_measures_emission_to_echo_return_time` | `GENERAL_KEEP` | 송신에서 반향 검출까지의 시간에서 거리 추정 |
| 48 | `ultrasonic_nearby_sensor_crosstalk_risk` | `GENERAL_KEEP` | 복수 센서의 오인 반향 가능; 설치/동기화는 모델별 |
| 49 | `ultrasonic_target_geometry_surface_affects_echo_detection` | `GENERAL_KEEP` | 표면 기울기·크기·반사율은 echo 수신 강도/방향에 영향 |
| 50 | `ultrasonic_level_is_bottom_reference_minus_surface_distance` | `GENERAL_KEEP` | 레벨=탱크의 기준 높이-측정 거리(고도 기준/offset 정의) |
| 51 | `ultrasonic_installation_alignment_nozzle_and_obstruction_controls` | `REMOVE_PRODUCT_NUMERIC` | Rosemount 3100의 5mm 노즐 돌출량은 모델 고유 설치조건; 정렬·장애물 회피만 유지 |
| 52 | `rosemount_5408_upper_null_zone_suppresses_measurement_and_api2350_cat3_independence` | `HOLD_MIXED_CLAIM` | 5408의 UNZ와 API 2350 Cat3 독립성 문구는 서로 다른 기술주제; 분리·1차 조항 검증 전 채점 제외 |
| 53 | `magnetrol_706_single_rod_installation_and_nozzle_reflection_effects` | `GENERALIZE_PRODUCT_CASE` | 노즐 임피던스 불연속·근접 금속 반사의 일반원리만 유지; 706 probe별 단정 제외 |
| 54 | `radar_level_from_empty_distance_minus_measured_distance` | `GENERAL_KEEP` | D를 탱크 기준점에서 정의하면 L=E−D(실제 기준고도 필요) |
| 55 | `radar_microwave_surface_echo_is_electromagnetic` | `GENERAL_KEEP` | Radar는 전자기파 반사 측정이며 초음파가 아님 |
| 56 | `radar_fmcw_sweep_slope_definition` | `GENERAL_KEEP` | 이상적 선형 FMCW sweep의 기울기 S=B/Ts |
| 57 | `radar_fmcw_beat_frequency_to_distance_relation` | `GENERAL_KEEP` | 정지 표적·선형 chirp·동일 경로 조건에서 fb=Sτ, D=vfb/(2S) |
| 58 | `gwr_tdr_pulse_propagation_and_surface_reflection` | `GENERAL_KEEP` | Probe를 따른 고주파 펄스와 유전율 불연속 반향 시간 |
| 59 | `radar_pulse_tof_distance_and_gas_phase_velocity` | `GENERAL_KEEP` | D=vgτ/2, 일반 대기에서 vg≈c이지만 특정 증기에서는 보정 |
| 60 | `fmcw_range_resolution_accuracy_and_fft_bin_distinction` | `GENERAL_KEEP` | 이상적 거리 분해능 ΔR≈vg/(2B)와 단일목표 정확도는 구분 |
| 61 | `radar_beam_footprint_and_obstruction_echo` | `GENERAL_KEEP` | 거리·빔각에 따른 footprint 증가, 탱크 내부물체 다중반향 가능 |
| 62 | `transmission_line_reflection_coefficient` | `GENERAL_KEEP` | Γ=(ZL−Z0)/(ZL+Z0); 정합·개방·단락 경계 확인 |
| 63 | `transmission_line_reflection_waveform_effects` | `GENERAL_KEEP` | 입사파+반사파 중첩으로 overshoot/ringing·오검출 가능 |
| 64 | `transmission_line_termination_and_topology` | `GENERAL_KEEP` | 임피던스 정합 종단과 분기 최소화로 반사 감소; 기준은 물리계층별 |
| 65 | `transmission_line_waveform_diagnostic_procedure` | `GENERAL_KEEP` | 케이블/종단/분기의 파형 점검은 현장 절차; 특정 probe 방법 일반화 금지 |
| 66 | `pressure_reference_categories_and_differential_ports` | `GENERAL_KEEP` | 절대·게이지·차압의 기준압 정의 구분 |
| 67 | `bourdon_tube_oval_to_circular_elastic_motion` | `GENERAL_KEEP` | 타원 단면 Bourdon tube의 압력 탄성변형과 자유단 이동 |
| 68 | `differential_pressure_transmitter_two_port_sensing` | `GENERAL_KEEP` | HP−LP 차압 측정; 이상적 동일압 입력은 ΔP=0 |
| 69 | `piezoresistive_pressure_sensor_bridge_readout` | `GENERAL_KEEP` | 압력에 의한 저항 변화를 Wheatstone bridge로 읽는 기전 |
| 70 | `piezoresistive_vs_piezoelectric_static_pressure_response` | `GENERAL_KEEP` | 저항형은 정압 검출 가능; 전하 출력 압전형은 장기 정압 유지에 제약 |
| 71 | `pressure_range_overpressure_and_burst_limits_are_distinct_product_ratings` | `GENERAL_KEEP` | 측정범위/작동압/내과압/파열압은 다른 사양값이며 혼동 금지 |

## 판단 근거와 검증 경계

- **부력/밀도/계면:** Archimedes 원리 `Fb=ρgV`, 2층 계면의 층별 합산으로 대조한다. Float와 displacer 계측량을 구분. 설치·시험은 실제 기종에 따름.
- **정수압/DP:** 기준방향을 HP−LP로 고정하고 `ΔP=ρgh`를 유도. Wet leg/dry leg와 응축은 **액주가 어느 포트에 포함되는지**로 검산한다. LRV 부호와 전송기 높이 조건을 분리한다. 특정 제조사 −23.73 kPa 교정 사례는 필수 암기사항 아님.
- **유량:** `Q=∫v·n dA=A v평균`이 기본이다. 피토관은 국소속도·평균속도 구분. 유량계별 감지 물리량을 구분하고 각 운전 조건을 추가한다.
- **RTD:** `R=V/I`, `P=I²R`. 2선식 리드가 측정저항에 합산; 3선식은 리드 균형과 회로구조, 4선식은 독립 Kelvin sense가 조건이다.
- **초음파:** `d=ct/2`는 반향 왕복시간과 음속의 정의가 맞을 때. 반사·온도·장애물 문제를 설명한다. Rosemount 3100 노즐 돌출 **5mm**는 개별 모델 사양이므로 범용 채점에서 제외.
- **레이더:** `L=E−D`, 이상적 선형 FMCW `D=v_g f_b/(2S)`, `S=B/T_s`. 파형·매질·정지 대상의 조건 필수. FMCW 분해능과 단일표적 정확도 구분. Rosemount 5408 Null Zone와 API2350 위험성 분류를 합친 주장은 토픽을 분리한 뒤 재검증한다.
- **전송선:** `Γ=(ZL−Z0)/(ZL+Z0)`, 정합이면 Γ=0. 통신선 신호 반사와 전송선 정합은 일반 공학 관계. 제품별 종단 저항은 별개.
- **압력:** 기준압 정의/격막/탄성 요소/저항형과 전하형 센서 차이를 적용조건과 함께 유지.
- 위 범주에서 명시된 일반 식들은 물리 모델 자체로 재현 가능하나, *모델별 오류 수치·허용차·세부 설치 절차*는 독립 규격·제조사 근거 없이는 범용 Fact로 인증하지 않는다.

### 근거 자료 (공개 접근 범위 / 제품 문서 = 사례)
- ABB: https://new.abb.com/products/measurement-products/level/a-dozen-ways-to-measure-fluid-level — displacer buoyancy and float distinction
- Control.com: https://control.com/textbook/continuous-level-measurement/displacement/ — two-liquid displacer buoyancy derivation
- USGS: https://www.usgs.gov/water-science-school/science/how-streamflow-measured — flow area-times-average velocity
- USACE: https://www.publications.usace.army.mil/Portals/76/Publications/EngineerManuals/EM_200-1-19.pdf — pitot local stagnation/static pressure method
- NI: https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-temperature-with-thermocouples-rtds-and-thermistors.html — RTD 2/3/4 wires and excitation
- Analog Devices: https://www.analog.com/en/resources/analog-dialogue/articles/a-precision-temperature-measurement-solution-with-high-emc-performance-using-an-rtd.html — RTD Kelvin/matched leads
- Endress+Hauser: https://www.endress.com/en/support-overview/learning-center/radar-level-measurement-explained — radar TOF L=E-D; FMCW sweep
- Endress+Hauser GWR: https://www.ca.endress.com/en/field-instruments-overview/level-measurement/Guided-radar-level-measurement — guided pulse and dielectric reflection
- Tektronix: https://www.tek.com/en/documents/fact-sheet/tdr-impedance-measurements-foundation-signal-integrity — reflection coefficient and matched load
- Previous source pack: grading/evidence/approved_fact_registry.json — Full official/documentation references per row; not all independently re-read in this batch

## 후속 적용 시 반드시 지킬 사항
- 이 검토는 보고서 단독 commit이며 실제 Registry/Pack/Model Answer/Logic/Generated 변경이 아니다. 채점 규약이나 수험생 점수에 영향을 주지 않는다.
- 삭제 후보를 적용하려면 `legacy_anchor_id`에 연결된 Pack core/important 및 `accepted_explanations`, 질문 요구축, 모범답안, Logic Check, Golden fixtures와 맞물린 일반원리 대체를 확인할 것.
- 변경 시 generated를 CLI로 재구성하고 release all + validate-all + 관련 pytest + diff/check 수행 후 **Topic 단위 커밋**. 검증 실패면 승격 금지. 기존 로컬 README와 `docs/operational_quality_checksheet.md` 미커밋 변경, 별도 운영 checkout과 컨테이너는 보존.
- 2026-10-30 최초 스냅샷의 2 제거/5 유지/1,265 미확인, 현행 Registry의 1,520행과 현행 Queue 1,290행은 이 Chat 보고서로 소급 갱신하지 않는다.
