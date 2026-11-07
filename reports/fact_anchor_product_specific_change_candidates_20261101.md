# 제품 고유 Fact의 채점 제거·치환 실행 후보 — 2026-11-01

## 원칙
Fact는 **참**이더라도 기술사 **보편적 필수 답안**이 아닐 수 있다. 다음은 Registry와 실제 Topic Pack `fact_anchor.json`을 함께 비교해 확인한 11개 사례의 적용 계획이다. 제품별 사양을 독립적으로 확인하지 않은 경우 **제품 사실 재승인은 하지 않는다**.

**주의:** 이 문서는 삭제 실행 결과가 아니다. 1,520 Fact Registry, Topic Pack, 채점, generated에 실제 mutation은 아직 0건. 삭제 시 source-hash·approval·CLI rebuild·전체 release gate를 통과하지 못하면 반영하지 않는다.

## Pack에 일반원리 표현이 이미 있으므로 Registry 제품 사례 제거가 유력한 4건

| Fact ID / Pack Anchor | Pack 중요도 | 조치 후보 | 근거 |
|---|---|---|---|
| `fisher_multiport_selector_well_test_routing_scope` / `multiport_selector_flow_routing` | important | Registry의 8-inlet/1 test/7 production 제품 사양 **제거 후보**. Pack에는 이미 Multiport의 유로 선택·전환·격리라는 일반원리가 있음 | 제품 포트 수는 제품/질문별로 달라 보편 정답 아님 |
| `fisher_v500_eccentric_plug_cam_action_and_erosive_service_scope` / `eccentric_plug_noncontact_rotation` | important | V500 제품별 적용·사양 Fact는 범용 Registry에서 제외 후보. Pack의 편심 회전·접촉 감소 일반원리는 유지 | 모델 고유 침식성 유체 허용성은 전체 eccentric plug로 확대 금지 |
| `dp_level_wet_leg_zero_elevation` / 동일 ID | core | Registry의 Yokogawa LRV=-23.73 kPa **사례 수치 제외**. Pack의 LP wet-leg 수두와 음의 LRV 원리는 이미 일반화되어 유지 | 정수압식의 적용 조건은 일반 사실, 교정값은 개별 설치 예시 |
| `ultrasonic_installation_alignment_nozzle_and_obstruction_controls` / `ultrasonic_mounting_nozzle_obstruction_error` | core | Registry의 Rosemount 3100 노즐 돌출 5 mm **제조사 수치 제외**. Pack의 노즐·정렬·장애물과 허위에코 원리는 유지 | 모든 초음파 센서에 동일 5 mm 규칙 없음 |

위 4건은 **Pack 원문이 이미 범용인 것**을 확인했다. 실제 삭제 전에 해당 Registry Fact를 참조하는 Machine Contract·Logic·tests·Model Answer 검색이 필요하다. 제품별 질문 대비 자료는 보조 문서에 남길 수 있다.

## Pack 자체가 제품명·구체수치를 Core/Important로 소유하여 동시 수정이 필요한 7건

| Fact ID → Pack Anchor | Pack 중요도 | 보편 Fact로 바꿀 방향 |
|---|---|---|
| `fisher_2625_volume_booster_one_to_one_pressure_following` → `booster_pressure_follower_boundary` | core | Volume Booster는 공급/배기 유량을 확대하고 액추에이터 응답을 보조한다. Pilot/output pressure ratio와 deadband는 선정 모델로 확인. 2625 1:1은 예시만 |
| `fisher_handbook_reports_direction_specific_valve_response_time` → `opening_closing_response_asymmetry` | important | 같은 valve라도 열기/닫기 방향의 구동력·마찰·공기공급/배기 경로가 달라 step 응답이 비대칭일 수 있다. Valve A의 Td/T63 수치 암기 제외 |
| `dvc6200_sis_relay_capacity_and_tubing_requirements_are_variant_specific` → `pneumatic_supply_tubing_spool_capacity` | core | Actuator 응답시간은 요구 공기량, Supply/Exhaust capacity와 Tube 유동저항에 의존. 3/8 in, High-Cv port 제품 수치 제외 |
| `dvc6200_sis_tuning_response_adjustment_is_assembly_specific` → `positioner_gain_speed_stability_tradeoff` | core | Positioner tuning은 응답속도/오버슈트/안정성 tradeoff와 실제 조립체 확인이 핵심. C~M 튜닝 코드 제외 |
| `fisher_vbl_booster_bypass_separates_large_and_small_signal_operation` → `volume_booster_flow_capacity_feedback_condition` | core | Booster의 빠른 공급/배기와 소신호 정밀제어·안정성 상충을 설명. 개별 VBL bypass 조정 절차는 제품 문맥으로 한정 |
| `fisher_positioner_feedback_and_actuator_linkage_lost_motion_are_distinct` → `positioner_cannot_remove_mechanical_backlash` | important | Positioner feedback tuning은 기계적 Linkage 유격을 물리적으로 제거하지 못함. 3660/1052 부품 링크 구조 암기 제외 |
| `actuator_bench_set_is_spring_adjustment_not_positioner_signal_travel_calibration` → `bench_set_calibration_boundary` | important | Bench set의 Spring preload와 Positioner signal-to-travel calibration 차이를 일반원리로 유지; Fisher 657 절차는 예시 |

## 별도 보류

- `rosemount_5408_upper_null_zone_suppresses_measurement_and_api2350_cat3_independence` → `radar_upper_null_zone_overfill_coordination` (optional): 장치의 가까운 측정 제외구간과 API 2350 Category 3 Overfill 독립성은 주제·적용범위가 다르다. **한 Fact로 새 검증 승인 금지**. 분리 후 5408 제품 매뉴얼과 API 2350 실제 조항을 각각 대조.

## 적용 순서와 Gate
1. 위 Registry 항목에 대한 참조 검색, Topic·Machine Contract·Model Answer·Logic·Golden 영향 명세. 제품 관련 시험 문항이 별도로 존재하는지도 확인.
2. **Pack이 이미 일반화된 4건**은 범용 Registry에서 제품 사례를 빼되 일반원리 대체 Fact 존재·상태를 확인. 그 외 7건은 Pack 문장·accepted_explanations·Model Answer·Logic을 함께 일반화.
3. 제품 상세 문구는 주제 README나 별도 예시자료에 출처·제품/버전을 명시해 둘 수 있으나 필수 채점 Fact로 강제하지 않는다.
4. 등록된 승인 hash와 source_refs를 정식 절차로 갱신. 생성물은 **CLI로만 재생성**. Focused tests, Golden mutations, `validate-topic-pack-release --all`, `validate-all`, `PROMOTE_GENERATED=0 scripts/validate_release.sh` 확인. 실패 시 미승격.
5. 서로 다른 Topic은 **단계별 커밋**. 사용자 미커밋 README 및 `docs/operational_quality_checksheet.md` 보존. 운영 checkout/컨테이너 작업과 분리.

검증 출처 예: [Fisher DVC6200 SIS 매뉴얼](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc6200-sis-digital-valve-controller-en.pdf), [Fisher 2625 제품 개요](https://www.emerson.kr/ko/final-control/products/fisher-2625), [NI RTD 메트롤로지](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-temperature-with-thermocouples-rtds-and-thermistors.html), [Endress+Hauser Radar 측정](https://www.endress.com/en/support-overview/learning-center/radar-level-measurement-explained). 제품 기술자료는 그 제품의 정확한 사양만 뒷받침하며 업계 보편 의무가 아니다.
