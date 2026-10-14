# Displacer식 레벨계: 부력, 토크튜브, 밀도·계면 및 교정

## 1. Topic metadata

- topic_id: `displacer_level_buoyancy_torque_tube_density_interface_calibration`
- question_type: `PRINCIPLE_INTERPRETATION`
- difficulty: `FIELD_APPLICATION`
- 상태: `candidate / human_review_required` (승인 전 운영 `topic_packs/` 밖에서 보관)

## 2. Scope and ownership

고정된 displacer에 작용하는 부력 변화가 토크튜브의 비틀림으로 전달되어 레벨·계면·밀도 신호가 되는 문제군을 소유한다. 자유롭게 액면을 따라 이동하는 Float의 위치 검출은 Float 후보가, 정수압과 탱크 압력 보상은 차압식 레벨 Pack이 소유한다. 자유공간 Radar·초음파·GWR의 왕복시간 원리도 이 Pack의 필수 답안이 아니다.

## 3. Core correct facts

- 잠긴 체적 `V_sub`에 작용하는 부력은 균일한 액체·중력장이라는 조건에서 `F_b = rho * g * V_sub`이다. 액위 상승으로 침수체적이 증가하면 겉보기 무게가 줄고 토크튜브의 비틀림이 달라진다.
- Displacer는 보통 지지·현수되어 자유 Float처럼 액면 위치를 그대로 따라가지 않는다. 레벨 변화 → 침수체적/부력 변화 → 토크튜브 토크·각도 변화 → 전송기 또는 제어기 출력의 측정 사슬을 구별한다.
- 설계 비중과 실제 밀도가 달라지면 같은 침수 깊이에서도 부력이 바뀌므로 레벨 지시 오차 또는 재교정 필요가 생길 수 있다. 유체 밀도·온도·운전범위·토크튜브 정격을 확인한다.
- 두 비혼합 액체의 계면 측정에서는 하부·상부 액체의 밀도 차와 각각의 침수체적이 신호를 정한다. 전체 displacer가 두 액체에 잠기고 액체 밀도가 일정한 모델이면 `F_b = g(rho_L V_L + rho_U V_U)`이며 `V_L + V_U`는 일정하다. 이것은 계면 위치와 밀도 차가 토크에 미치는 관계를 설명하는 조건부 모델이다.
- Wet calibration은 실제 또는 동등한 비중의 시험 유체를 사용하여 작동 범위를 확인한다. 다른 시험액을 사용하면 설계 비중에 따른 침수량 환산이 필요하다. Dry calibration은 제조사 절차에 따른 등가 하중·추를 써서 부력 변화를 모사하며 실제 운전 유체 조건 검증과 구분한다.
- Caged/externally mounted 구조와 cageless/in-vessel 구조의 설치·격리·정비 접근성을 구별한다. 구조별 공정 연결, 압력·온도 정격과 오염·침전·마찰/부착 영향을 확인한다.

## 4. Acceptable expressions

- 액위가 오르면 잠긴 길이가 늘고 apparent weight가 줄어 토크튜브 입력이 변한다.
- Archimedes 원리, 밀도×중력가속도×배제체적의 동등한 식을 인정한다.
- 계면 검출은 두 액체 비중차에 의존한다고 설명해도 된다.
- 실제 액체 교정과 추를 이용한 모의 교정의 기능 차이를 인정한다.

## 5. Fatal wrong claims

단순 누락은 fatal이 아니다. 고정 displacer가 초음파 echo 시간을 측정한다거나, 액체 밀도가 바뀌어도 동일 잠김 부력이 항상 일정하다는 명시적 원리 반전을 검토 후보로 둔다. 이 초안은 신규 결정론적 fatal regex를 활성화하지 않는다.

## 6. Warn-level weak claims

부력만 쓰고 토크튜브·출력 전달을 빠뜨림; 계면 문제에서 두 액체 밀도차를 빠뜨림; 교정 문제에서 유체 비중과 wet/dry 조건을 구별하지 않음. 각 누락은 질문에 그 축이 직접 요구된 경우에만 적용한다.

## 7. False positive cautions

오답 인용·부정·정정은 오답 주장으로 취급하지 않는다. 단위와 변수 정의가 일치하는 동등식을 인정한다. 모든 displacer가 항상 완전 침수되거나 모든 장치가 동일한 방향의 출력이라고 가정하지 않는다. 압력 영향은 압력에 따른 유체 밀도 변화·기계 정격·차압을 분리한다.

## 8. Expected question patterns

- Displacer식 액면계의 부력·토크튜브 측정원리와 Float식과의 차이를 설명하시오. → `displacer_buoyancy`, `displacer_signal_chain`, `displacer_float_boundary`
- Displacer식 액면계의 밀도 변화에 따른 오차와 액-액 계면 측정 조건을 설명하시오. → `displacer_buoyancy`, `displacer_density_error`, `displacer_interface_density_difference`
- Displacer식 액면계의 wet/dry 교정 방법과 설치·유지보수 시 유의점을 설명하시오. → `displacer_signal_chain`, `displacer_wet_dry_calibration`, `displacer_installation_maintenance`

## 9–12. JSON authoring

`fact_anchor.json`은 위 원자 Fact와 원문 절·제조사 문서를 근거로 한다. `model_answer.json`은 질문마다 필요한 anchor만 required로 지정한다. `logic_check.json`의 자동 검출은 비활성화하고 의미 판단 후보·정상 문맥만 남긴다. `topic_importance.json`은 FIELD_APPLICATION/NORMAL이며 난이도가 점수를 직접 변경하지 않는다.

## 13. Cross-topic handoff

- Float: 액면 추종 위치·가이드·테이프 → 기존 Float 후보.
- DP: `Delta P = rho g h` 및 wet/dry leg → 기존 차압식 레벨 Pack.
- GWR/Radar/Ultrasonic: echo·TDR → 해당 기존 Pack 또는 후보.

## 14. Human review checklist

- [ ] 출처의 실제 절과 수식·조건·정격·교정 문구 확인
- [ ] 질문별 anchor 범위와 인접 Topic 소유권 확인
- [ ] README와 4개 source JSON의 의미 검토
- [ ] `add-topic`으로 관리형 경로를 다시 만들고 검토된 source를 옮긴 뒤 `approve-topic --reviewer` 수행

## Source references

- [개인 WordPress Chapter 20 후반부](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-20/) — 20.4절 Displacer/Torque Tube/Calibration; 원문이며 자동 사실 승격 아님.
- [Emerson Fisher 249 Cageless Sensor manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200100x012.pdf) — 변위기·토크튜브 측정 사슬과 설치 조건.
- [Emerson Fisher 2502 Controllers manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200126x012.pdf) — wet/dry 및 비중 교정 절차.
- [Emerson Fisher 2500/2503 Controllers manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200124x012.pdf) — 계면·비중 차 조건.
