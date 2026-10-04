# WordPress Topic Link 결정 적용 절차

## 목적

확정 후보와 후속 검토 대상을 분리하고, 나중에 사람이 검토한 결과를 안정적으로 적용하기 위한 절차다.

## 결정 템플릿

`reports/wordpress_topic_link_manual_review_20261005_decision_template.csv`

이 파일은 179개 후보를 모두 포함한다.

- `suggested_decision=approve`: 현재 직접 근거가 확인된 13건
- `suggested_decision=defer`: 나머지 166건
- `final_decision`: 사람이 최종 입력하는 값
- `final_topic_id`: 승인 시 후보 Topic ID와 일치해야 함
- `reviewed_by`, `reviewed_at`, `final_evidence`: 최종 결정 증적

## 입력 규칙

`final_decision`은 `approve`, `reject`, `defer` 중 하나만 허용한다.

- `approve`: 본문과 Topic 범위를 다시 확인한 경우
- `reject`: 후보 Topic과 명백히 무관한 경우
- `defer`: 근거 부족·범위 경계·추가 OCR/사람 판단이 필요한 경우

`approve`가 아니면 `final_topic_id`는 공란으로 둔다. `approve`이면 원본 `candidate_topic_id`와 정확히 같아야 한다. 모든 결정에는 `reviewed_by`, `reviewed_at`, `final_evidence`를 기록한다.

## 적용 순서

1. 결정 템플릿을 복사해 작업본을 만든다. 원본 템플릿은 수정하지 않는다.
2. 사람이 `final_decision`과 증적 열을 입력한다.
3. 별도 검증기로 행 수, 후보 키, Topic ID, 결정값, 증적을 검증한다.
4. 검증 결과를 먼저 dry-run으로 확인한다.
5. 승인된 행만 기존 `wordpress_catalog.py --review-topic-link POST_ID TOPIC_ID approve` 명령으로 한 건씩 적용한다.
6. 적용 후 pending/approved 개수와 source proposal을 확인한다.

`defer` 행은 어떠한 DB 변경도 일으키지 않는다. CSV 권고만으로 자동 적용하지 않는다.

## 보호 원칙

- 원본 WordPress DB와 Master Topic Pack은 템플릿 편집 중 변경하지 않는다.
- `final_decision`이 없는 행은 적용하지 않는다.
- 자동 승인 일괄 명령을 만들지 않는다.
- 적용 전후 DB 무결성과 Golden/release gate를 확인한다.
