# Topic Sheet: 개수로 위어·플룸의 수위–유량 환산과 적용

## Topic metadata

- topic_id: `open_channel_weir_flume_head_discharge_submergence_selection`
- question_type: `PRINCIPLE_INTERPRETATION`
- difficulty: `FIELD_APPLICATION`
- status: `draft / human_review_required`

## Scope and ownership

이 Topic은 자유수면이 있는 개수로에서 위어(weir)와 플룸(flume)의 수위–유량 관계, 적용조건, 수몰 영향과 설치·검증 판단을 소유한다. 밀폐 배관의 차압·전자기·초음파·용적식 계측은 `flow_measurement_meter_principles_velocity_selection`이 소유한다. 블로그의 종합 비교표는 두 Topic을 구분하는 참고 자료일 뿐 독립 Fact Anchor가 아니다.

## Candidate core facts

- 개수로의 수두(head)는 측정 기준점과 지정된 상류 수위의 차이이며, 유량은 구조물 형상과 수두에 따른 교정/표준 관계로 환산한다. 임의 위치의 수위를 같은 H로 쓰지 않는다.
- 날카로운 모서리의 직사각형 위어에서 자유 월류·적용 범위 등 조건이 충족되면 대표적인 수두 지수는 `Q ∝ H^(3/2)`이다. 계수는 폭·형상·접근유속·수축·방류계수 등 조건에 따른다.
- V-notch 위어의 대표적인 자유 월류 관계는 `Q ∝ H^(5/2)`이며, notch 각도와 방류계수·설치조건을 포함한 계수에 종속된다. 이 지수를 모든 위어에 적용하지 않는다.
- 플룸의 `Q=K H^n`은 해당 플룸 형식의 교정 관계이다. K와 n을 플룸 종류에 무관한 보편 상수로 취급하지 않는다.
- 하류 수위 상승으로 구조물이 수몰되면 자유흐름 교정식을 그대로 적용할 수 없다. 해당 형식의 하류수위·잠김률 보정 또는 재선정이 필요하다.
- 위어·플룸 비교는 유량범위, 수두 손실, 침전물/부유물, 설치 공간, 접근 흐름, 유지보수와 교정 기준을 연결해 수행한다.

위 항목은 블로그 HTML을 기반으로 한 검토 후보이며 운영 채점용으로 승인하지 않았다. 외부 교재 PDF/OCR은 이번 범위에 포함하지 않는다.

## Representative exam-style questions

1. 직사각형 위어와 V-notch 위어의 수두–유량 관계와 적용조건을 비교하시오.
2. 개수로 유량 측정에서 위어와 플룸을 비교하고, 수몰 흐름이 유량 환산에 미치는 영향 및 대응을 설명하시오.
3. 위어/플룸 계측의 수위 측정 위치·설치조건·교정자료 검증 절차를 설명하시오.

## Answer and error boundaries

수두의 기준과 자유/수몰 흐름을 먼저 정의하고, 구조물별 관계식의 지수와 계수의 의미를 구분한 뒤 현장 적용을 판단한다. 단순히 `Q=K H^n`만 적거나 지수를 모든 구조물의 보편 법칙으로 일반화하면 안 된다. 누락과 명시적 오답은 구별한다.

## Source

- [Lessons In Industrial Instrumentation, Chapter 22, 1](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-22-1/) — WordPress post `9774`, HTML modified `2026-10-26T14:37:41Z`, section 6. HTML 본문을 원문으로 보존하며 Fact 후보만 별도로 기술했다.
- [USGS 위어 유량표](https://pubs.usgs.gov/wri/1992/4028/report.pdf) — 직사각형과 삼각 노치 위어의 형식별 수두 지수와 계수 범위 검토용.
- [USGS Parshall flume 지침](https://pubs.usgs.gov/twri/twri3-a14/pdf/twri_3-A14_a.pdf) — 수몰에 따른 자유흐름 유량 보정 검토용.

## Current runtime diagnosis

이 후보가 승인된 운영 Pack에 없으므로 위어·플룸 합성 문항은 현재 유공압 Topic으로 잘못 연결된다. 이 결과를 정답 채점으로 사용하지 않는다. 상세 재현과 배관 유량 Pack의 별도 보강 후보는 [Chapter 22 시험·보강 제안](../topic_pack_proposals/chapter22_flow_test_and_upgrade.md)을 따른다.
