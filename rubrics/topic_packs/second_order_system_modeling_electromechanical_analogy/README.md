# 2차 시스템 모델링과 전기계·기계계 유사성

## 상태

사용자가 핵심 식·대응, 차원 확인의 학습상 중요도, 별도 Topic 경계, 분류값 및 라우팅 후보를 검토해 승인했다. 다만 이 승인은 Topic 내용 제안에 대한 것으로, 운영 채점 규칙 및 공식 Topic 승격 승인은 아니다. `topic_status.json`은 `draft / human_review_required`로 유지하며 운영 채점에는 사용하지 않는다.

## 범위

- 질량-스프링-댐퍼계와 직렬 RLC계의 2차 지배방정식 비교
- 출처가 사용하는 Force–Voltage analogy의 변수·계수 대응
- 대응표의 모델링 의미 및 출처에서 제시한 차원 확인

`L q¨` 항의 차원 확인은 선택적 보충이 아니라 이 Topic의 핵심 학습 항목이다.

감쇠비별 시간응답은 `second_order_lag_response_by_damping_ratio`, 공진·주파수응답은 `second_order_system_resonance_frequency_response`의 소유 범위로 둔다. 이 초안은 두 Topic의 내용을 복제하거나 대신하지 않는다.

## WordPress 출처

- 게시물: [136회 2교시 2번](https://now0930.pe.kr/wordpress/136%ed%9a%8c-2%ea%b5%90%ec%8b%9c-2%eb%b2%88/)
- 첨부: `fourier_Transform-2.pdf`, 2쪽, WordPress source ID `wpurl:6114b4c1b43d6bdc546cf98765cecdf7`
- PDF 버전: `2026-04-20T13:01:22`
- p.1: 질량-스프링-댐퍼식, 직렬 RLC식, Force–Voltage 대응
- p.2: `L q¨` 항의 차원 확인
- p.2의 무감쇠 고유진동수 설명은 기존 공진 Topic 소유로 이 Pack의 학습·채점 범위에는 포함하지 않는다.

## 초안에서 추출한 핵심 주장

1. 기계계 식: `m x¨ + D x˙ + kx = f(t)`.
2. 출처의 직렬 RLC 식: `L q¨ + R q˙ + (1/C)q = E(t)`.
3. 출처의 Force–Voltage 대응: `f↔E`, `m↔L`, `D↔R`, `k↔1/C`, `x↔q`, `x˙↔q˙`.
4. 위 대응은 출처가 선택한 모델 간 수학적 대응표로 기록하며, 물리량 자체가 동일하다는 주장으로 확대하지 않는다.
5. 출처는 `L q¨` 항의 차원을 전압으로 확인한다. 기호·단위·가정은 원 PDF와 대조 검토해야 한다.

## 검토 범위와 제한

- 사실 앵커는 출처의 추출 내용을 표현하며, 독립적인 기술 승인이나 정답 완전성을 뜻하지 않는다.
- 결정론적 fatal/major 채점 규칙은 비워 둔다. 이 초안으로 감점, 점수 상향, fatal 판정을 추가하지 않는다.
- question pattern, 라우팅 키워드, 난이도·선택 중요도는 모두 제안값이며 기존 Topic routing 권한을 덮어쓰지 않는다.
- 검토 전에는 생성 bank/manifest에 반영하지 않고 운영 grader에서 참조하지 않는다.

## 남은 승인·운영 작업

- [x] PDF의 원문 수식 및 직렬 회로 가정 검토 — 사용자 승인
- [x] Force–Voltage 대응 검토 — 사용자 승인
- [x] `L q¨` 차원 확인을 핵심 학습으로 지정 — 사용자 승인
- [x] 기존 응답·공진 Topic과 별도 소유 경계 지정 — 사용자 승인
- [x] question patterns / aliases / importance 후보 대표성 검토 — 사용자 승인
- [ ] 채점 fatal/major 규칙을 추가할지와 점수 영향을 별도 검증
- [ ] 공식 승인·생성 bank 반영은 해당 검증 이후 수행
