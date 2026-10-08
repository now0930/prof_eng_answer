# GitHub `main` 기준 Anchor 감사 인벤토리 정합 (2026-10-08)

## 정합 결과

감사 기준은 이 커밋의 GitHub `main`에서 분기한 source inventory다. `rubrics/topic_packs/*/fact_anchor.json`을 다시 집계해 **86개 Topic Pack, 2,073개 Anchor**를 기준으로 삼았다. 과거 작업 브랜치의 87개 Pack / 2,068개 Anchor 총계는 최신 기준이 아니므로 더 이상 현재 인벤토리로 사용하지 않는다.

| 감사 등록부 구성 | Anchor 수 | 처리 |
| --- | ---: | --- |
| 기존 배치 보고서에서 현재 Topic·Anchor·statement가 일치하는 기록 | 2,026 | 기존 세부 판정과 근거를 유지하고 최신 기준의 등록부로 이관 |
| 최신 `main`에 이미 있는 보고서에서 추가로 확인되는 현재 Anchor | 11 | 기존 2,026건과 겹치지 않는 기록만 추가 |
| 이번 비교에서 남은 차이 감사 | 36 | 아래 표에서 사실 대조 완료 |
| **최신 인벤토리 전체** | **2,073** | **2,073/2,073 등록** |

위 세 구간은 중복을 제거한 수치다. 판정의 세부 근거는 이 문서가 참조하는 기존 배치 보고서와 아래의 36개 항목 기록에 있다. `확인`은 명시한 범위에서 일반 원리·식과 모순을 찾지 못했다는 뜻이며, 특정 설비의 적합성이나 표준 인증을 보증하지 않는다. `적용조건`은 실제 기종·설치·유체·운전점에 종속되는 경계를 기록한다.

### 이전 기록과 달라진 항목

- 이전 작업 브랜치에만 있던 **29개 Anchor**는 최신 `main` 인벤토리에 없으므로 이번 등록부에서 제외했다. 이는 자동 삭제나 Topic의 유효성 판정이 아니라 inventory 차이다.
- 기존 기록 중 현재 Anchor와 statement가 일치하는 항목만 유효한 기존 감사로 이관했다. 최신 `main`의 변경된 statement는 이전 판정만으로 승인된 것으로 간주하지 않는다.
- 아래 36개는 최신 인벤토리에서 기존 유효 등록이 없는 항목이므로 이번에 직접 대조했다. 그중 `sw04_hil`은 약어 충돌을 피하도록 source 문장을 수정했다.

## 최신 main 차이 36개: Anchor별 판정

| Topic Pack | Anchor ID | 판정 | 대조 결과·적용 경계 |
| --- | --- | --- | --- |
| `flow_measurement_meter_principles_velocity_selection` | `flow_volumetric_rate_area_integral` | 확인 | 체적유량은 단면 법선속도의 면적 적분이며 평균 법선속도를 쓰면 `Q=A·v̄_n`. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_mass_rate_density_relation` | 확인 | 질량유량 적분식과 `ṁ=ρQ` 단순화는 밀도 균일 조건을 구분한다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_dp_primary_element_conditions` | 적용조건 | 차압 primary element와 유량의 관계는 유체·형상·β·방출계수·압축성/팽창·Re 및 적용 표준 조건에 따른다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_pitot_local_velocity` | 적용조건 | Pitot 차압은 측정 위치의 속도 추정치다. 비압축·저속 단순식의 전제와 단면 평균을 위한 traverse/profile 필요성을 구분한다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_variable_area_meter` | 적용조건 | float의 힘 평형·유효 유로면적으로 유량을 지시한다. 설치방향 및 유체/교정 조건은 기종에 종속된다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_positive_displacement_meter` | 확인 | 일정 체적을 포획·이송하는 반복량/응답으로 유량을 산출하는 원리로 확인했다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_meter_principle_taxonomy` | 확인 | 터빈 회전, 와류 shedding, 도전성 유체의 전자기 유도 등 원리 분류가 타당하다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_ultrasonic_transit_doppler` | 확인 | Transit-time은 전파시간 차, Doppler는 반사체에 의한 주파수 이동을 이용한다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_coriolis_thermal_mass` | 확인 | 진동관의 Coriolis 응답은 질량유량, 열식은 유동에 따른 열전달 응답을 이용한다. 구현별 성능 차이는 별도다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_meter_selection_tradeoffs` | 적용조건 | 선택 인자는 유체·범위·정확도·응답·압력손실·설치·출력·정비 등이며 가중치는 공정 요구에 따른다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_profile_installation_error` | 적용조건 | 유동 프로파일·선회·상류 교란의 영향은 계측 원리와 설치 구성에 따라 달라진다. 모든 유량계에 같은 오차를 가정하지 않는다. |
| `flow_measurement_meter_principles_velocity_selection` | `flow_process_condition_maintenance` | 적용조건 | 기포·고형물·오염·마모·물성 변화·맥동·교정 상태의 영향은 계기 방식과 공정 조건별로 확인한다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_01` | 확인 | 유압은 액체, 공압은 기체 작동유체로 동력을 전달·제어한다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_02` | 적용조건 | pump/source, reservoir·conditioning, control valve, actuator, piping·return은 일반 유압 경로의 구성 예이며 회로·장비에 따라 달라진다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_03` | 확인 | 이상적인 기본 관계에서 힘은 압력×유효면적, 유량은 면적×속도, 유압동력은 일관된 단위계에서 `pQ`로 연결된다. 실제 압력강하·효율은 손실을 추가한다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_04` | 확인 | 방향제어·압력제어·유량제어 밸브의 회로 기능 구분이 타당하며 복합 기능 밸브는 별도다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_05` | 적용조건 | accumulator의 에너지 저장·방출과 보조유량·압력유지·비상·맥동 용도는 회로 설계 및 안전 요건에 따라 적용한다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_06` | 적용조건 | 유공압 선정의 힘·속도·응답·압축성·누설·효율·환경·정비 비교축은 타당하나 우선순위는 부하와 설계 요구에 종속된다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_07` | 적용조건 | 공압 filter/regulator는 통상적 conditioning 구성이다. lubricator·건조/수분 제거는 downstream 품질·장치 요구에 따라 선택하며 무조건 설치하지 않는다. |
| `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection` | `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection_anchor_08` | 적용조건 | 전기 명령을 유압 pilot/main stage 제어로 연결하는 설명은 일반 원리다. servo/proportional valve 내부 단계는 제품 설계별로 다르다. |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | `sw04_hil` | 수정 | HIL은 실제 제어기/실제 I/O와 실시간 plant model의 폐루프 시험이다. `SIL`이 Safety Integrity Level과 충돌하므로 software-in-the-loop를 `SiL`로 표기하고 구별 문장을 source에 반영했다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_01` | 확인 | 전력반도체 스위칭으로 전력 형태·크기를 변환·제어한다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_02` | 확인 | AC–DC, DC–DC, DC–AC, AC–AC 명칭은 변환단의 입력·출력 형태를 기준으로 한다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_03` | 적용조건 | 전력반도체의 gate 제어·turn-on/off 능력은 소자 종류별로 다르며 구동·부하·commutation·스위칭 조건이 동작에 영향을 준다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_04` | 적용조건 | PWM의 시간비 제어가 출력 평균/기본파에 미치는 관계는 converter topology와 운전 조건을 전제로 한다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_05` | 적용조건 | 유도전동기 V/f는 주파수와 전압을 함께 조정해 자속을 유지하려는 scalar 접근이다. 저속·고속·부하 토크 범위는 보정과 drive 한계에 따른다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_06` | 적용조건 | d-q 자속/토크 분리제어 설명이 타당하며 성능은 자속각 추정·전류제어·모터 파라미터 등 구현에 종속된다. |
| `power_electronics_converters_motor_drive_control` | `power_electronics_converters_motor_drive_control_anchor_07` | 적용조건 | 손실·열·고조파·역률·보호·EMC·절연·회생·정비는 선정 검토축이며 프로젝트별로 중요도·한계값을 정한다. |
| `second_order_lag_response_by_damping_ratio` | `so2_pole_response_relationship` | 확인 | 표준 2차 특성식의 복소근(under-damped) 식과 실근(over-damped) 식을 구분한 표현이 타당하다. `|s|=ω_n`은 복소근 범위에서만 적용한다. |
| `second_order_lag_response_by_damping_ratio` | `so2_zero_negative_damping` | 확인 | `ζ=0`, `ω_n>0`의 단순 허수극점은 자유응답 지속진동을 만든다. 이를 BIBO 안정으로 오해하지 않도록 공진 입력의 비유계 응답 경계를 명시한다. |
| `second_order_lag_response_by_damping_ratio` | `so2_negative_damping_instability` | 확인 | 표준 2차계에서 `ζ<0`, `ω_n>0`이면 극점 실수부가 양수여서 자연응답이 성장한다. |
| `second_order_system_modeling_electromechanical_analogy` | `second_order_system_modeling_electromechanical_analogy_anchor_01` | 확인 | 선형 질량–스프링–댐퍼의 운동방정식 `mẍ+Dẋ+kx=f(t)`와 계수 의미를 대조했다. |
| `second_order_system_modeling_electromechanical_analogy` | `second_order_system_modeling_electromechanical_analogy_anchor_02` | 확인 | 직렬 RLC의 전하 방정식 `Lq¨+Rq˙+q/C=E(t)`는 KVL 및 소자식으로 확인된다. |
| `second_order_system_modeling_electromechanical_analogy` | `second_order_system_modeling_electromechanical_analogy_anchor_03` | 적용조건 | `force–voltage` 대응 `f↔E, m↔L, D↔R, k↔1/C, x↔q`는 일관된 한 가지 analogy다. force–current analogy도 있으므로 대응 convention을 밝혀야 한다. |
| `second_order_system_modeling_electromechanical_analogy` | `second_order_system_modeling_electromechanical_analogy_anchor_04` | 확인 | 유사성은 각 계의 지배 미분방정식 형태와 변수 대응을 비교한다는 뜻으로 확인된다. 물리 도메인 자체가 동일하다는 주장은 아니다. |
| `second_order_system_modeling_electromechanical_analogy` | `second_order_system_modeling_electromechanical_analogy_anchor_05` | 확인 | `Lq¨`의 차원은 henry·coulomb/s² = volt로, 식의 전압 차원과 일치한다. |

## 대조 근거

- 유량 원리: [Endress+Hauser 유량 측정 원리 자료][flow-basics], [Coriolis 원리][coriolis], [초음파 transit-time/Doppler][ultrasonic]. 제조사 자료는 원리 대조에만 사용하며 제품별 성능을 일반화하지 않았다.
- 유공압: [Bosch Rexroth 유압 기초 교육범위][hydraulics], [Festo 공압 conditioning 기술자료][airprep]. 이는 구성·용도 확인 근거이며 특정 회로/제품의 선정승인이 아니다.
- HIL/SiL: [MathWorks HIL·SiL 구분][hil]. `sw04_hil`의 약어 수정은 이 정의 혼동을 방지하기 위한 표기 개선이다.
- 전력변환·전동기 구동: [ABB Direct Torque Control 기술 가이드][abb-dtc]. PWM 및 V/f 설명은 drive 기술 가이드의 구현 범위에서 대조했다.
- 2차계: [University of Washington 1·2차 시스템 강의][uw-second], [MIT 기계–전기 analogy 자료][mit-analogy], [Feynman Lectures 질량–스프링과 RLC analogy][feynman]. analogy는 linear lumped model과 명시한 force–voltage convention에 한정했다.

[flow-basics]: https://www.my.endress.com/_storage/asset/1267924/storage/master/file/5074019/download/Day%25201%2520Flow.pdf
[coriolis]: https://www.casc.endress.com/en/support-overview/learning-center/flow-measuring-principle-coriolis
[ultrasonic]: https://www.us.endress.com/en/support-overview/learning-center/flow-measuring-principle-ultrasonic-methods
[hydraulics]: https://www.boschrexroth.com/en/pl/academy/training/technical-training/fundamentals-of-hydrostatic-power-transmission-systems-of-machines-and-devices/
[airprep]: https://www.festo.com/media/cms/media/editorial/downloads/en/WhitePaper_Airprep_MS_en.pdf
[hil]: https://www.mathworks.com/discovery/hardware-in-the-loop-hil.html
[abb-dtc]: https://library.e.abb.com/public/3dc7259dcd684a55841165ddefe7eb3f/Technical_guide_No_1_3AFE58056685_RevD_EN.pdf
[uw-second]: https://faculty.washington.edu/chx/teaching/fbintro/lec06-first-and-second-order-systems/
[mit-analogy]: https://www.web.mit.edu/viz/EM/visualizations/coursenotes/modules/guide11.pdf
[feynman]: https://www.feynmanlectures.caltech.edu/I_25.html
