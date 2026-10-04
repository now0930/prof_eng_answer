# WordPress–Topic 링크 확정 후보 우선 정책

## 운영 원칙

현재 단계에서는 확실한 직접 근거가 있는 링크만 `confirmed_candidate`로 관리한다. 근거가 부족한 링크는 거절하지 않고 `deferred`로 보류한다.

`deferred`는 잘못된 링크라는 뜻이 아니다. 게시글 전문, 자사 OCR, Topic ownership boundary 또는 추가 원문을 사람이 확인한 뒤 후속 결정한다.

## 현재 확정 후보 기준

- 게시글 중심 기술 내용이 Topic 핵심 범위와 직접 일치
- 본문에서 Topic 고유 개념과 절차·수식·장치 원리가 확인됨
- 단순 제목·태그·어휘 점수에 의존하지 않음
- 인접 Topic 또는 상위 개념으로의 확장이 없음
- 본문에 직접 부정·제외 문구가 없음

현재 확정 후보는 13건이며, 나머지 166건은 `deferred`이다.

## 금지 사항

- `deferred`를 자동 reject 또는 approved로 변환하지 않는다.
- 확정 후보를 DB, Master, Topic Pack에 반영하기 전 사람의 최종 승인을 받는다.
- 새로운 WordPress 수집·외부 PDF OCR·추정 근거를 사용하지 않는다.
- Grader, routing, scoring contract를 변경하지 않는다.

## 후속 검토 시 필요한 것

- 자사 게시글 본문과 OCR 위치 확인
- Topic README 및 ownership boundary 재확인
- 독립적인 기술 근거 2개 이상 기록
- 부정·제외 표현 확인
- 확정·보류·거절 사유를 별도 기록

## 산출물

`reports/wordpress_topic_link_manual_review_20261005_confirmed_only.csv`를 기준 목록으로 사용한다.

- `confirmed_candidate`: 현재 확실한 후보
- `deferred`: 후속 검토 대상

이 파일은 검토용 projection이며 실제 카탈로그 상태를 변경하지 않는다.
