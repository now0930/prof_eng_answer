# 산업계측제어기술사 2027~2030 `IC-2027-W-5-2` Dynamic Review Lane 운영 규칙

## 1. 목적

`IC-2027-W-5-2`의 공식 범위는 **계측제어 관련 동향**이며 관련 법령, 기술기준 등을 포함한다.

이 범위는 시간이 지나면서 내용과 유효성이 변한다. 따라서 정적 Topic Pack으로 고정하지 않고 `DYNAMIC_REVIEW_LANE`에서 시점별 evidence를 검증한다.

이 문서는 Dynamic Review Lane의 운영 계약이다. 특정 시점의 최신 동향 자체를 저장하는 snapshot 문서가 아니다.

## 2. 현재 상태와 Architecture boundary

- criterion: `IC-2027-W-5-2`
- 현재 static coverage: **GAP**
- selection importance: **HIGH**
- static PRIMARY owner: `0`
- static SECONDARY owner: `0`
- static Topic Pack 생성: **금지**
- generated rubric rebuild: **불필요**
- Question Type 확장: **금지**
- Dynamic Review Lane 운영문서 또는 snapshot 생성만으로 coverage를 `COVERED`로 승격하지 않는다.

`Official Category ≠ Topic Pack ≠ Question Type ≠ Dynamic Review Snapshot`을 유지한다.

Dynamic Review Snapshot은 최신성 evidence다. Topic Pack의 영구 지식 ownership을 대체하지 않는다.

## 3. Review scope

매 review는 다음 4개 source bucket을 모두 확인한다.

1. **공식 출제기준**
   - `IC-2027-W-5-2` 문구와 적용 기간
   - 공식 출제기준의 개정·정정·후속 공지
2. **법령·규제·기술기준**
   - 계측제어 설계·설치·운영·검사·안전·보안에 직접 영향을 주는 법령, 고시, 기술기준
   - 제정, 개정, 시행일, 폐지, 경과조치
3. **표준**
   - 계측제어 관련 표준의 edition, amendment, corrigendum, active/replaced/withdrawn 상태
   - 시험 답안에 영향을 주는 적용 범위 또는 요구사항 변화
4. **계측제어 산업 동향**
   - 계측, 제어, OT/IT, 산업통신, 기능안전, 산업보안, AI/로봇/스마트팩토리 등 출제기준과 직접 연결되는 변화
   - 단순 제품 출시나 마케팅 자료는 그 자체로 시험 동향 evidence가 아니다.

## 4. Review cadence와 trigger

### 4.1 정기 review

- 최소 **매 calendar month 1회** 성공한 review snapshot을 만든다.
- 마지막 성공 review의 `verified_as_of`로부터 **45일을 초과하면 STALE**로 본다.
- STALE 상태에서는 기존 snapshot을 최신 근거처럼 사용하지 않는다.

### 4.2 시험 전 freshness gate

- 시험 일정이 확정된 경우 시험일 기준 **14일 이내**에 성공한 review가 있어야 한다.
- 14일 이내 성공 review가 없으면 시험 직전 최종 review를 수행한다.
- 시험 전 review는 월간 review를 대체할 수 있다.

### 4.3 Event-triggered review

다음 사건이 확인되면 월간 cadence를 기다리지 않고 review한다.

- 공식 출제기준 개정 또는 정정
- 관련 법령·고시·기술기준의 제정, 개정, 시행 또는 폐지
- 관련 표준의 새 edition, amendment, corrigendum, replacement 또는 withdrawal
- 시험 답안의 기술적 판단을 바꿀 수 있는 중대한 계측제어 산업 변화

## 5. Source authority hierarchy

### Tier 1 — Normative / authoritative

법적·표준·출제기준 사실은 원칙적으로 Tier 1에서 확정한다.

- 공식 시험 시행기관의 출제기준·공지
- 정부·규제기관의 법령·고시·기술기준 원문
- 표준 발행기관의 공식 edition/status 정보
- 해당 기관의 공식 개정·시행·폐지 공지

Tier 1과 다른 source가 충돌하면 Tier 1을 우선한다.

### Tier 2 — Official explanatory

- 정부·규제기관·공공기관의 해설, FAQ, 가이드, 보도자료
- 표준 발행기관의 공식 해설·technical bulletin
- 공신력 있는 공공 연구기관의 기술 보고서

Tier 2는 Tier 1의 의미를 보조한다. 법적 의무나 표준 requirement를 Tier 2만으로 새로 확정하지 않는다.

### Tier 3 — Industry evidence

- 전문 협회·학회·산업 컨소시엄 자료
- 제조사·솔루션 공급자의 first-party technical document
- 공개된 산업 적용사례와 기술 release

산업 동향을 `EXAM_CORE` 또는 `EXAM_SUPPORT`로 올리려면 다음 중 하나를 만족한다.

1. Tier 1 또는 Tier 2 source가 직접 뒷받침한다.
2. 서로 독립적인 Tier 3 source 2개 이상이 같은 변화를 뒷받침한다.

단일 vendor의 마케팅 claim은 `WATCH` 이상으로 승격하지 않는다.

### Tier 4 — Discovery only

뉴스, 블로그, 커뮤니티, 검색 결과 등 secondary source는 discovery에 사용할 수 있다.

Tier 4만으로 법령·표준·출제기준 사실을 확정하지 않는다. 중요한 claim은 Tier 1~3으로 역추적한다.

## 6. As-of와 freshness 규칙

각 snapshot은 최소 다음 시간을 구분해 기록한다.

- `reviewed_at`: review를 실제 수행한 시각
- `verified_as_of`: mandatory source bucket을 모두 성공적으로 확인한 기준일
- `next_due`: 다음 정기 review 만료 기준
- source별 `published_or_effective_date`
- source별 `checked_at`

`verified_as_of`는 확인하지 못한 source를 추정해서 앞으로 당기지 않는다.

마지막 성공 `verified_as_of` 이후 45일이 지나면 snapshot 상태는 `STALE`이다.

법령·표준은 publication date만으로 최신성을 판단하지 않는다. 시행일, edition, amendment, replacement, withdrawal 상태를 함께 확인한다.

## 7. Review 절차

1. 직전 성공 snapshot을 찾는다.
2. 공식 출제기준을 확인한다.
3. 관련 법령·고시·기술기준을 확인한다.
4. 관련 표준의 edition/status를 확인한다.
5. 계측제어 산업 동향을 scan한다.
6. source register에 확인 근거를 기록한다.
7. 직전 snapshot과 비교하여 change class를 부여한다.
8. exam relevance gate를 적용한다.
9. 시험 답안에 실제 영향을 주는 delta만 exam-use summary에 반영한다.
10. snapshot을 새 파일로 보존한다.
11. mandatory source 확인 실패가 있으면 `INCOMPLETE`로 종료하고 성공 review로 간주하지 않는다.

## 8. Change classification

각 변화는 다음 중 하나로 분류한다.

- `NO_CHANGE`
  - mandatory source를 모두 확인했으나 시험에 영향을 주는 변화가 없음
- `EDITORIAL`
  - 문구·링크·정정 등 의미 또는 시험 답안을 바꾸지 않는 변화
- `MATERIAL`
  - 법적 요구, 기술기준, 표준 edition/status, 적용 범위 또는 시험 답안의 핵심 설명을 바꾸는 변화
- `URGENT`
  - 즉시 반영하지 않으면 법령·안전·보안·기술기준 측면에서 잘못된 답안을 만들 가능성이 큰 변화

`URGENT`는 `MATERIAL`보다 우선 처리한다.

## 9. Exam relevance gate

각 candidate change는 다음 중 하나로 판정한다.

- `EXAM_CORE`
  - `IC-2027-W-5-2`에 직접 해당하며 답안 핵심에 포함할 가치가 있음
- `EXAM_SUPPORT`
  - 직접 핵심은 아니지만 비교, 적용조건, 현장 대책, 표준/법령 근거로 유용함
- `WATCH`
  - 관련성은 있으나 성숙도·근거·범용성이 부족하여 현 시점 답안 핵심으로 사용하지 않음
- `OUT_OF_SCOPE`
  - 공식 criterion과 직접 연결되지 않음

`EXAM_CORE`와 `EXAM_SUPPORT`만 exam-use summary에 들어간다.

다음은 원칙적으로 `WATCH` 또는 `OUT_OF_SCOPE`다.

- 단일 vendor 제품 출시
- 검증되지 않은 성능 claim
- 계측제어 적용성이 불명확한 일반 IT 뉴스
- 단기 주가·시장점유율·투자 이슈
- 시험 답안의 기술 판단을 바꾸지 않는 홍보성 발표

## 10. Snapshot 저장 규칙

snapshot은 다음 경로에 append-only로 저장한다.

`docs/exam_scope/dynamic_reviews/ic_2027_w_5_2/YYYY-MM-DD.md`

같은 날 추가 review가 필요하면 `YYYY-MM-DD-r2.md`, `YYYY-MM-DD-r3.md` 순으로 새 파일을 만든다.

과거 snapshot을 최신 내용으로 덮어쓰지 않는다.

오타 또는 metadata 오류를 수정해야 하면 수정 이유를 snapshot 안에 `correction_note`로 남긴다.

별도 `latest.md` 포인터를 두지 않는다. 파일명의 날짜와 `verified_as_of`를 기준으로 가장 최근 성공 snapshot을 찾는다.

## 11. Snapshot 필수 schema

각 snapshot은 최소 다음 구조를 가진다.

```text
criterion: IC-2027-W-5-2
review_status: COMPLETE | INCOMPLETE
reviewed_at: ISO-8601
verified_as_of: YYYY-MM-DD | UNVERIFIED
next_due: YYYY-MM-DD
freshness: CURRENT | STALE
previous_snapshot: path | NONE
overall_change: NO_CHANGE | EDITORIAL | MATERIAL | URGENT
```

### Source register

| bucket | tier | issuer | document | edition/status | published/effective | checked_at | source_ref | result |
|---|---|---|---|---|---|---|---|---|

### Change register

| change_class | exam_relevance | domain | change summary | exam impact | action |
|---|---|---|---|---|---|

### Exam-use summary

`EXAM_CORE`와 `EXAM_SUPPORT` 변화만 짧게 정리한다.

### Excluded / WATCH

검토했지만 답안 핵심에 넣지 않은 항목과 이유를 남긴다.

## 12. NO_CHANGE와 failure 처리

### 성공했지만 변화가 없는 경우

mandatory source bucket을 모두 확인했다면 변화가 없어도 snapshot을 만든다.

- `review_status: COMPLETE`
- `overall_change: NO_CHANGE`
- `verified_as_of`를 실제 확인일로 갱신
- source register에 확인한 근거를 남김

`NO_CHANGE`도 Dynamic Review Lane의 유효한 evidence다.

### source 확인 실패가 있는 경우

mandatory source bucket 중 하나라도 필요한 확인을 완료하지 못하면 다음과 같이 처리한다.

- `review_status: INCOMPLETE`
- `verified_as_of: UNVERIFIED`
- `overall_change`를 `NO_CHANGE`로 기록하지 않음
- 실패 source와 원인을 기록
- 직전 성공 snapshot을 마지막 verified evidence로 유지
- 45일 freshness 한계는 직전 성공 `verified_as_of` 기준으로 계속 계산

접속 실패나 검색 실패를 "변경 없음"으로 해석하지 않는다.

## 13. Coverage와 grading 경계

Dynamic Review Lane 운영문서 또는 snapshot이 존재한다는 이유만으로 다음을 수행하지 않는다.

- `IC-2027-W-5-2`를 static `COVERED`로 승격
- PRIMARY/SECONDARY static owner 부여
- Topic Pack 생성
- generated rubric rebuild
- Question Type 추가
- production grading logic 변경

Dynamic snapshot을 실제 grading runtime에 주입하려면 별도 설계·검증·commit이 필요하다.

현재 단계의 목적은 **최신성 evidence의 수집·검증·보존 규칙을 확정하는 것**이다.

## 14. 운영 체크리스트

review 완료 전 다음을 모두 확인한다.

- [ ] 공식 출제기준 확인
- [ ] 법령·고시·기술기준 확인
- [ ] 관련 표준 edition/status 확인
- [ ] 계측제어 산업 동향 scan
- [ ] source authority tier 기록
- [ ] reviewed_at / verified_as_of / next_due 기록
- [ ] 직전 snapshot 대비 change classification
- [ ] exam relevance gate 적용
- [ ] EXAM_CORE / EXAM_SUPPORT만 exam-use summary에 반영
- [ ] WATCH / OUT_OF_SCOPE 제외 이유 기록
- [ ] 실패 source가 있으면 INCOMPLETE 처리
- [ ] static Topic / coverage / Question Type 경계 확인
- [ ] 새 dated snapshot으로 archive

## 15. 완료 정의

Dynamic Review Lane의 "운영 가능" 상태는 다음을 의미한다.

1. 본 운영 규칙 문서가 repository에 존재한다.
2. review cadence와 freshness 규칙이 정의되어 있다.
3. source authority hierarchy가 정의되어 있다.
4. change classification과 exam relevance gate가 정의되어 있다.
5. snapshot schema, no-change 처리, failure 처리, archive 규칙이 정의되어 있다.
6. static Topic Pack과 coverage status를 자동 변경하지 않는 경계가 유지된다.

이는 `IC-2027-W-5-2`의 static coverage를 `COVERED`로 만드는 완료조건이 아니다.
