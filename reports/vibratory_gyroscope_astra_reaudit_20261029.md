# 진동 자이로 Topic Pack 재검토·수정 이력 — 2026-10-29

검토자: Astra (`gpt-6-astra`), 사용자 위임에 따른 AI 검토. 사람 승인으로 표시하지 않는다.

## 범위와 근거

- 관리형 Pack `vibratory_gyroscope_coriolis_angular_rate_sensing`의 README, Topic Sheet, 네 source JSON, Master 참조, 승인 metadata를 점검했다.
- WordPress post 8253의 저장된 최신 HTML 버전(2026-10-28T13:00:39Z, SHA-256 `360461342211e20c6b06083caa5d691c85ca2f19ffe3161cddec2b287574c764`)과 기존 [원문 검토 기록](vibratory_gyroscope_astra_followup_20261028.md)을 대조했다. 이번 감사 중 WordPress 실시간 재접속은 실패했으므로 원문의 현 시점 불변성을 주장하지 않는다.
- [Analog Devices의 진동 자이로 설명](https://www.analog.com/en/resources/analog-dialogue/articles/imems-angular-rate-sensing-gyroscope.html)을 독립 기술 근거로 사용했다.

## 형식 검토

JSON 구조, Topic ID, Anchor 참조, 관리형 승인·source hash 계약은 유효하다. `source_sheet_hash`와 `reviewed_sheet_hash`는 생성/승인 시점이 달라 정상적으로 다르다. Master의 `verification_status=unverified`는 원문 전체 검증 상태이므로 선택된 Fact의 승인 사실과 혼동해 바꾸지 않았다.

## 내용 검토와 수정 이력

| 항목 | 기존 문제 | 반영한 수정 |
| --- | --- | --- |
| 원시 신호와 출력 | 구동 반주기의 원시 감지 응답 반전이 최종 각속도 출력 반전으로 읽힐 수 있었다. | Anchor 04·대표 질문·답안 흐름에 원시 코리올리 힘의 반전과 일정 각속도의 복조 후 출력 유지를 구분했다. 감지 변위의 가능한 위상 지연도 명시했다. |
| 질문 범위 | 유량계·축 RPM 비교가 기본 결론·고득점 조건처럼 보였다. | 비교는 질문이 요구할 때만 적용하도록 제한했다. |
| 검출 방식 | 변위 검출을 모든 진동 자이로의 배타적 방식처럼 읽을 수 있었다. | 대표적인 변위 검출과 힘 재평형 피드백 방식을 구분했다. |
| 출처 범위 | 일부 문서가 HTML 1절만 명시해 최신 Master의 1~2절과 어긋났다. | README와 source JSON 설명을 1~2절로 맞췄다. |

`2|Ω||v|sinθ`, 직교 시 `2m|Ω||v(t)|`, `v(t)≠0`인 순간의 역산식, RPM과 rad/s의 환산 가능성, 자이로와 유량계의 소유 범위는 유지했다. 좌표계가 없는 부호·좌우 차이를 자동 fatal 처리하지 않는 정책도 유지했다.

## 판정

위 수정 후 형식과 내용은 이 Pack의 출제 범위에 적합하다. 새로운 점수 항목이나 자동 fatal 규칙은 추가하지 않는다. 실제 WordPress 원문이 다시 바뀌면 source-update proposal 경로로 재검토한다.
