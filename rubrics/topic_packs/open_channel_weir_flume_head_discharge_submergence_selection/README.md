# 개수로 위어·플룸의 수위-유량 환산과 적용

## Topic ID

`open_channel_weir_flume_head_discharge_submergence_selection`

## Question type

`PRINCIPLE_INTERPRETATION`

## 작성 상태

WordPress Chapter 22-1의 개수로 부분을 별도 출제 단위로 분리했다.
운영 반영 상태는 `topic_status.json`의 승인 해시와 release gate 결과를 따른다.

## 소유 범위

자유수면 개수로의 위어·플룸에서 기준 수두와 유량 교정 관계, 자유/수몰 흐름,
설치·선정·검증을 다룬다. 밀폐 배관 유량계는
`flow_measurement_meter_principles_velocity_selection`이 소유한다.

## 핵심 관계와 조건

- 대표적 sharp-crested 직사각형 위어의 자유 월류에서는 조건부로
  `Q∝H^(3/2)`이다. 폭·방류계수·접근유속·수축 조건을 확인한다.
- 대표적 V-notch 위어의 자유 월류에서는 조건부로 `Q∝H^(5/2)`이다.
  노치 각도·방류계수·수위 기준을 확인한다.
- 플룸의 `Q=K H^n`은 형식별 교정식이다. 하류 수몰 시 해당 형식의
  잠김률·하류수위 보정 없이 자유흐름식을 그대로 사용하지 않는다.
- 단순 관계식 누락은 fatal이 아니다. 서로 다른 위어의 지수를 명시적으로
  뒤바꾸거나 모든 플룸의 K·n을 같은 상수라 하는 주장은 오답 후보이다.

## 대표 질문

1. 직사각형 위어와 V-notch 위어의 수두–유량 관계 및 적용조건을 비교하시오.
2. 두 위어의 수두–유량 관계를 비교하고 플룸의 수몰 영향을 설명하시오.
3. 위어와 플룸의 선정 조건, 수두손실 및 유지관리 차이를 설명하시오.

## 검토 자료

- [WordPress Chapter 22-1](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-22-1/)의 HTML 6절. 외부 교재 PDF/OCR은 채점 근거에서 제외했다.
- [USGS 위어 유량표](https://pubs.usgs.gov/wri/1992/4028/report.pdf), [USGS 플룸 수몰 보정 지침](https://pubs.usgs.gov/twri/twri3-a14/pdf/twri_3-A14_a.pdf).
- 상세 경계와 사람 검토 항목은 `docs/topic_sheets/open_channel_weir_flume_head_discharge_submergence_selection.md`를 따른다.
