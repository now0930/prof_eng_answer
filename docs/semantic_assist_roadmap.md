# 결정론적 채점의 미해결 의미 보완 로드맵

> 2026-10-19 한정 적용: 열전대·RTD의 원리·특성·정확도·개선 비교 문항은
> [교차 Topic 문항 계약](cross_topic_question_contract.md)으로 결정론적 관계를 먼저
> 판정하고, 남은 `PARTIAL`의 관련 답안 구절에만 점수 영향 없는 LLM 검토 제안을 허용한다.
> 최종 A/B/C/D/E 점수는 기존 결정론 엔진이 계산한다. 이는 이 비교 문항에
> 대한 제한된 코드 경로이며 운영 배포 또는 아래 전체 Topic 확대 Stage 5~8 완료를 뜻하지 않는다.

갱신: 2026-10-13. 사용자 승인: 세 경로의 점수 비교는 하지 않고 결정론적 해석이
부족한 부분에 LLM을 사용한다. 최종 점수는 기존 결정론적 정책이 계산한다.

## 전체 단계와 목표 달성 여부

완료는 구현과 해당 범위의 검증을 모두 마친 경우다. 부분 완료는 운영 연결까지
완료했다는 뜻이 아니다. 상태는 현재 checkout 기준이며 CI·배포를 뜻하지 않는다.

| 단계 | 목표 | 현재 근거 | 달성 여부 / 남은 일 |
|---|---|---|---|
| 0 기준선 | 기존 점수 계약·오류·coverage 확인 | Golden·replay 감사와 제한사항 기록 | 완료 |
| 1 공통 계약 | Fact·질문·주장 ID, snapshot, 권한 분리 | 입력 schema 및 계약 테스트 | 완료: 비활성 계약 범위 |
| 2 사실 지식 | 승인된 Fact와 출처·조건 연결 | 1,515 Fact / 82 Topic 등록, 전체 86 Master | 부분: 전체 연결·변경 영향 추적 |
| 3 문제 요구 | 답안과 독립된 요구·관련 Fact 확정 | compiler 및 모호성 보류 | 부분: 복합 요구·비교축·계산 실증 |
| 4 의미 보완 | 미해결 구절만 LLM에 전달하고 근거 제안 수신 | 실제 parser → 전용 queue → Gemini 비공개 호출과 재검토 파일럿 | 부분: 질문 범위 coverage와 제안의 독립 검증 대기; 모호한 scope는 호출 없이 보류 |
| 5 결정론 채점 연결 | 검증된 근거를 기존 요구 판정·점수 정책에 연결 | legacy Anchor ID에 대한 검토 근거의 shadow 투영 및 기존 점수 엔진 호출 테스트 | 부분: 운영 채점 연결 금지; 근거 승인·fatal/조건 전체 검증·핵심 미해결 보류 계약 대기 |
| 6 기능 평가 | 표현 다양성 수용·오인정 방지·실패 처리·재실행 검증 | SIL·V-Model 실제 제한 호출, Nyquist 무호출; 비공개 재실행과 의견 불일치 기록 | 부분: 세 사례의 완전 질문 범위와 독립 Fact/span 정답 라벨 대조 대기 |
| 7 확대 | 대표 3 → 10 → 전체 Topic | 지식 등록·출처 감사 수행 | 부분: 의미 보완 적용 coverage 확대 |
| 8 운영 | release·CI·설정·저장·복구 검증 | 기존 release 통과, 결정론적 실경로 세 사례 가동·비공개 품질 체크시트 저장 | 부분: 현재 브랜치 로컬 가동만 확인; 운영 봇 브랜치 통합·CI·배포 검증 대기 |

현재 위치: **Stage 4 비공개 실제 호출 파일럿 / Stage 5 shadow 점수 투영 / Stage 6 부분 실행**.
Stage 0~1 완료, Stage 2~8 부분 완료다. 운영 의미 보완을 활성화한 Topic은 아직 없다.

## 실행 흐름과 계약

1. 질문 compiler가 요구와 관련 Fact를 확정한다. 답안 때문에 요구가 달라지면 안 된다.
2. 기존 parser가 확인한 근거를 보존한다. 단어 일치만으로 의미를 확정하지 않는다.
3. 기존 `canonical_claim_extractor`의 `unresolved_spans`를 승인된 질문 요구와 연결한다.
   한 요구에 유일하게 연결되는 문장만 `requirement_id`, `fact_ids`, `source_span`,
   `reason`으로 표현한다. 요구가 모호하거나 질문 범위가 해결되지 않은 문장은 보류한다.
4. 호출부는 해당 구절과 질문·승인 Fact만 LLM에 보낸다. 기본 설정은 꺼짐이며
   미해결 항목이 없으면 호출하지 않는다.
5. LLM은 Fact별 `supported/partial/contradicted/unknown`, 원문 인용, 이유,
   누락 조건을 반환한다. 이것은 해석 제안이며 점수·fatal·합격 판정은 금지한다.
6. 현재 구현은 범위·인용·조건 ID·응답 완전성을 확인하고 `pending_verification`으로
   보관한다. 이후 기존 공학 불변식 위반, 명시적 부정·인용·거절 문장에 대한 잘못된
   `supported` 제안을 차단한다. 통과는 의미의 참·거짓을 증명하지 않는다.
7. 선택적으로 두 번째 LLM이 첫 제안을 보지 않고 원문·Fact를 다시 읽는다. 결과가
   다르거나 응답이 잘못되면 미해결이다. 두 해석이 같아도 `semantic_agreement`일 뿐
   독립적인 참 증명이나 채점 승인으로 표기하지 않는다. 수식·차원·극성·조건을 충분히
   증명할 수 없는 제안은 누락·오답 대신 `UNRESOLVED`로 유지한다.
8. 검증된 근거만 점수 adapter로 전달한다. 핵심 요구 미해결 시 최종 확정을 보류하는
   출력·저장 계약을 함께 구현한 뒤 운영 연결한다.

API 실패나 잘못된 응답은 해당 항목만 미해결로 남긴다. 이미 확인한 결정론 근거를
수정하지 않는다. 상충하는 여러 구절의 결합 판정은 후속 검증기에서 처리해야 한다.

## 재실행과 저장

요청 hash에는 질문, 전체 답안 hash, 발췌 구간, 요구 ID, 관련 Fact 전체 snapshot,
모델·prompt·parser·verifier·정책 버전이 포함된다. 같은 요청의 구조 검증된 제안은
재사용하며 cache를 읽을 때도 검증한다. cache 적중은 의미 검증 완료를 뜻하지 않는다.

현재 cache는 호출자가 제공하는 메모리 mapping 또는 저장소 밖 권한 0600의 비공개
SQLite mapping이다. 다만 검증된 근거의 revision, 재해석 이력은 미구현이다.
실제 운영 연결 전 구현한다. 고정된 검증 근거의
점수 재현과 새로운 LLM 호출의 해석 변동은 별도로 기록한다.

## 순차 후속 작업과 수용 기준

| 순서 | 작업 | 완료 기준 | 현재 |
|---|---|---|---|
| A | 요구·미해결·LLM 응답 계약 | 범위 밖 Fact/인용 위조/점수 필드 거부 | 완료: 연결부 단위 범위 |
| B | 규칙 parser → 미해결 queue → provider | 해결된 항목 호출 0, 실제 미해결만 전달 | 부분 완료: 기존 컨테이너 Gemini 키를 밖으로 꺼내지 않는 비공개 파일럿; Topic 전체 coverage 대기 |
| C | 의미·수식·조건 검증 | 잘못된 SIL 곱셈식을 올바른 비율 Fact로 승격하지 않음, 부정·부분 조건 보존 | 부분 완료: 공학 불변식·부정·인용 차단 및 원 제안 없는 재검토·불일치 보류; 자동 의미 승인 기준·조건 독립 검증 대기 |
| D | 검증 근거 → 기존 채점 adapter | 같은 근거는 같은 점수, 핵심 미해결 최종 확정 보류 | 부분: 승인 Fact의 legacy Anchor shadow 투영, WRONG/fatal·다중 Fact 미완성 차단; 운영 연결 대기 |
| E | 비공개 저장·실제 3사례 E2E | 입력·버전·근거 이력 및 실패 후 재실행 확인 | 부분: 권한 0600 SQLite/결과, 세 사례 파일럿; 기준 라벨·완전 범위 대기 |
| F | 10개·전체 Topic 확대와 운영 | 범위별 결과, release/CI/복구 검증 | 대기 |

초기 계약 테스트는 provider 대역을 사용했다. 아래의 별도 비공개 파일럿에서는 실제
Gemini 연결을 확인했지만 의미 정확도와 전체 Stage 6 완료로 표현하지 않는다.
과거 3경로 점수 차이는 이번 수용 기준이 아니다.

## 이번 구현의 검증 결과

- 관련 pytest: **53 passed**, 실패·skip 없음.
- `python3 scripts/rubric_manager.py validate-all`: **ALL VALID**.
- `PROMOTE_GENERATED=0 bash scripts/validate_release.sh`: **exit 0**.
- `git diff --check`: 통과.
- 실제 provider 호출·운영 배포·CI는 이번 작업에서 실행하지 않았다.
- 상세 로그는 공개 커밋 밖 `/tmp/semantic_assist_release_20261013.log` 및
  `/tmp/semantic_assist_validate_all_20261013.log`에 저장했다.

release 통과는 기존 회귀 조건의 충족이다. 위 표의 의미 검증·점수 연결·운영 적용
미완료 항목을 완료로 바꾸지 않는다.

2026-10-13 후속: [실제 parser 연결](../grading/evidence/fact_unresolved_queue.py)을 추가했다.
질문 요구가 유일하게 확정된 문장만 전송하고, 잘못된 SIL 곱셈식과 명시적 부정·인용을
`supported`로 승격하지 않도록 1차 차단했다. 이 차단은 false positive를 줄이는
방어 계층이며, 통과한 제안도 독립 의미 검증 전까지 점수에 반영되지 않는다.
후속 집중 pytest **45 passed**, `rubric_manager.py validate-all` **ALL VALID**,
`PROMOTE_GENERATED=0 scripts/validate_release.sh` **exit 0**였다. release의 Topic content
audit은 86 Topic / 86 Master / 749 question patterns / 2,073 anchors PASS였다.
전용 10회 재현성 검사는 opt-in이라 SKIP됐고, CI·배포는 수행하지 않았다.
상세 로그: `/tmp/semantic_assist_stage_b_release_20261013.log`,
`/tmp/semantic_assist_stage_b_validate_all_20261013.log` (비공개 작업 환경).

2026-10-13 재검토 단계: [의미 재검토 계약](../grading/evidence/fact_semantic_review.py)은
첫 LLM의 해석·이유를 전달하지 않고 동일 원문과 승인 Fact를 재평가한다. 일치,
불일치, 형식 실패, 알려진 수식 오류를 별도 상태로 기록한다. 일치는 확률적 신호이므로
`independently_verified=false`, `score_effect=none`을 유지한다. 실제 사실 검증과
기존 A/B/C/D/E 입력 연결은 다음 단계다.
재검토 후 관련 pytest **58 passed**, `rubric_manager.py validate-all` **ALL VALID**,
`PROMOTE_GENERATED=0 scripts/validate_release.sh` **exit 0**였다. 전용 10회 재현성
검사는 opt-in으로 SKIP됐다. 상세 로그는 비공개 작업 환경의
`/tmp/semantic_assist_stage_c_release_20261013.log`와
`/tmp/semantic_assist_stage_c_validate_all_20261013.log`에 있다.

## 2026-10-13 비공개 실제 호출 파일럿과 남은 승인 경계

`scripts/prepare_semantic_assist_pilot.py`는 Golden의 세 문제에서 답안을 보지 않고
작은 질문 구절과 승인 Fact ID를 지정한다. 이는 **시험용 잠정 범위**이며 질문 전체의
요구를 확정한 계약이 아니다. `scripts/run_semantic_assist_private.py`는 기존 컨테이너
내 API 키로만 요청을 보내고, 입력·응답·cache를 저장소 밖 권한 0600 파일에 저장한다.
기본 호출 상한은 사례당 미해결 구절 3개이며 각 구절은 별도 재검토가 가능하다.
출력의 `score_effect=none`, `final_grade_allowed=false`는 고정이다.

최신 동일 코드 경로에서 사례당 최대 2개 구절을 보낸 결과는 다음과 같다.

| 사례 | parser 미해결 | 질문 Fact에 유일하게 연결 | 전송 / 독립 재검토 | 상태 |
|---|---:|---:|---:|---|
| SIL | 12 | 4 | 2 / 2 | 1개 해석 일치, 1개 불일치; 8개 범위 보류, 2개 상한 이월 |
| V-Model | 11 | 2 | 2 / 2 | 2개 해석 불일치; 9개 범위 보류 |
| Nyquist | 0 | 0 | 0 / 0 | 이미 규칙 parser가 미해결로 분류하지 않아 무호출 |

이는 **provider/비공개 cache/보류 동작의 파일럿**이지 Fact 의미 정확도나 채점 점수
평가가 아니다. 두 모델 출력의 일치는 독립적인 참 증명이 아니고, 오류 응답은 보류로
남는다. 실제 점수 입력 전에는 (1) 질문 전체 요구와 Fact 범위의 독립 확정,
(2) 답안 원문 span의 사람 또는 별도 결정론 검증, (3) 조건·극성·수식·다중 Fact Anchor
완결성 검사, (4) 미해결 핵심 요구의 최종 점수 보류, (5) 별도 holdout 회귀가 필요하다.
현재 생산 채점 경로에는 연결하지 않았으며 승인 Fact registry와 generated bank도
이 파일럿 때문에 수정하지 않았다. 세 사례의 원문·모델 응답·SQLite cache는
공개 저장소에 넣지 않는다.

이 변경 범위의 집중 pytest는 **57 passed**, `rubric_manager.py validate-all`은
**ALL VALID**, `PROMOTE_GENERATED=0 scripts/validate_release.sh`는 **exit 0**,
`validate-topic-pack-release --all`은 **PASS**였다. 릴리스의 전체 Topic content
audit은 86 Topic / 86 Master / 749 question patterns / 2,073 anchors PASS였다.
전용 10회 재현성 검사는 opt-in으로 SKIP됐으며 운영 배포·CI 확인은 수행하지 않았다.
상세 로그는 공개 저장소 밖 `/tmp/semantic_assist_final_release_20261013.log`,
`/tmp/semantic_assist_final_validate_all_20261013.log`,
`/tmp/semantic_assist_final_topic_release_20261013.log`에 있다.

이후 [운영 품질 체크시트](operational_quality_checksheet.md)를 결정론적 실제 세션 저장
경로에 추가하고 승인된 과거 사례 3건을 가동했다. 세 사례 모두 전문가 승인 점수 범위와
차이가 나 `benchmark_conflict`로 기록했다. 차이만으로 채점기 결함이나 라벨 결함을
확정하지 않는다. 운영 봇은 다른 checkout을 쓰므로 이 변경이 실서비스에 배포된 것은
아니다. Topic별 사실 수정은 체크시트 분류·재시험 후 순차 진행한다.
