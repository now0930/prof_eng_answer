# Displacer식 레벨계의 부력·토크튜브와 계면·교정

`displacer_level_buoyancy_torque_tube_density_interface_calibration` — 사용자 검토 완료 선언에 따라 관리형 운영 Pack 승인 절차를 적용한다.

고정·현수된 Displacer의 액위 → 침수체적 → 부력·겉보기 무게 → 토크튜브 → 출력 사슬을 소유한다. 질문군은 (1) 측정원리와 Float 비교, (2) 밀도 오차와 액-액 계면, (3) wet/dry 교정과 설치·정비다. 각 문제의 `required_anchor_ids`만 필수이며 전체 7개 Anchor를 매 문제에 요구하지 않는다.

기본 관계는 균일 유체에서 `F_b = rho g V_sub`이다. 계면의 `F_b = g(rho_L V_L + rho_U V_U)`는 두 비혼합 액체와 전체 침수·일정 체적 조건을 붙여 설명한다. 설계 비중과 실제 비중이 다르면 힘·지시값이 달라질 수 있다. Wet 교정은 시험 유체의 비중과 침수량, Dry 교정은 등가 하중·추와 제조사 절차가 핵심이다.

Float의 액면 추종 위치 검출, DP의 정수압·Wet/Dry Leg, Radar·Ultrasonic·GWR의 시간측정은 이 Pack의 소유가 아니다. 답안에서의 비교는 허용하지만 해당 방식의 상세 정답 축으로 확대하지 않는다. 단순 누락·오답 인용·정정은 fatal이 아니며 신규 결정론적 fatal 규칙은 켜지 않았다.

근거는 [Chapter 20 후반부](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-20/) 20.4절과 [Fisher 249](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200100x012.pdf), [Fisher 2502](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200126x012.pdf), [Fisher 2500/2503](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d200124x012.pdf) 제조사 문서다. WordPress 원문은 보존하며 각 Fact는 질문에서 요구된 범위에만 적용한다.

사람 검토: 사용자 `now0930`이 후보 검토 완료를 2026-10-14에 명시했다. [Topic Sheet](../../../docs/topic_sheets/displacer_level_buoyancy_torque_tube_density_interface_calibration.md)와 네 source JSON을 관리형 승인 명령으로 기록한다. 자동 validator PASS는 별도의 사실 검증 주장으로 해석하지 않는다.
