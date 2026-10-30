# Topic 내부 소유 경계

이 문서는 engineering Fact Registry에서 분리한 저장소 내부 라우팅·소유권 계약이다. 외부 기술 사실이나 답안 채점 근거로 사용하지 않는다. 실제 경계는 해당 Topic Pack/Topic Sheet가 소유하며, 변경 시 함께 재검토한다.

| 이전 Fact ID | 소유 경계 | 확인 위치 |
| --- | --- | --- |
| `repository_cavitation_topic_noise_and_material_handoff_contract` | cavitation/flashing Pack은 현상·대책을 소유하고, 상세 소음 예측은 `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`, 재료·극한 서비스 상세는 `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`가 소유한다. | `docs/topic_sheets/control_valve_cavitation_flashing_choked_flow_damage_prevention.md`의 Topic 9/14 handoff 및 각 Pack README |
| `pressure_sensor_pack_and_dp_level_pack_scope_boundary` | 압력 센서 원리·정압 영향·zero/span·impulse-line 문제와 정수압 액위 변환·밀도 보상·wet/dry leg·remote-seal head 문제를 별도 Pack으로 소유한다. 이는 DP 전송기의 액위 사용을 부정하지 않는다. | `rubrics/topic_packs/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error/fact_anchor.json`의 `dp_level_boundary`, `rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json` |

두 이전 ID는 2026-10-29 재검증에서 Fact Registry에서 제외했다. 내용은 보존했지만 Registry의 `verified` 건수나 Fact-to-Anchor 투영에 포함되지 않는다.
