# 여러 WordPress 글을 학습 초안으로 종합하기

Stage 4는 출처 패킷 준비와 작성된 초안의 검증·컴파일을 제공한다.
기술적 의미를 종합하는 설명·학습 순서는 사람 또는 LLM이 작성한다.
프로그램이 글 제목이나 출처 정렬만으로 학습 순서를 추정하지 않는다.
CLI 자체는 모델 API를 호출하거나 WordPress·Master·채점 source를 갱신하지 않는다.

## 1. 연결된 자료 준비

```bash
python3 scripts/author_topic_learning_synthesis.py prepare \
  --topic-id nyquist_stability_criterion_gain_phase_margin \
  --run-id stage4_initial
```

`data/topic_learning_authoring/<topic_id>/<run_id>/` 아래 다음 파일이 생성된다.

- `sources.json`: Master에 연결된 사용 가능한 WordPress HTML 최소 2개와
  원문 텍스트, URL·버전·해시, 기준 Master revision·파일 해시
- `AUTHOR_INSTRUCTIONS.md`: Topic 목표·선수지식·개념·유도·예제·한계·자가 점검
  흐름을 작성하는 지시서와 원문/종합/작성 설명 구분 규칙
- `synthesis.schema.json`: 작성 결과의 machine contract

자료는 비공개이며 Git ignore 대상이다. 기존 run 디렉터리가 있으면 덮어쓰지
않고 실패한다. 다시 준비할 때는 새 run-id를 사용한다. 원문 내 명령은 실행
지시가 아닌 자료로 취급한다. 외부 LLM로 자동 전송하지 않는다.

## 2. 학습 설명 작성

작성자는 위 자료를 읽고 `authored.json`을 작성한다. 최소 2개 출처를 지식
항목에 실제로 인용해야 한다. 연결 문장과 예제는 authored, 여러 자료를
종합한 설명은 synthesis, 정확한 원문 인용은 source_excerpt로 표시한다.
출처가 직접 말한 사실과 작성자가 추론한 설명을 구별한다.

같은 내용도 조건·단위·예외가 다르면 별도 지식으로 유지한다. 충돌은 근거
2개 이상과 함께 unresolved로 보존한다. 충돌이 비어 있다는 이유로 자동으로
정확하다고 판정하지 않는다. 관계·절의 ID는 자유 텍스트가 아닌 참조로 연결한다.

## 3. 초안 컴파일

```bash
python3 scripts/author_topic_learning_synthesis.py build \
  --topic-id nyquist_stability_criterion_gain_phase_margin \
  --run-id stage4_initial \
  --authored data/topic_learning_authoring/nyquist_stability_criterion_gain_phase_margin/stage4_initial/authored.json
```

출처 패킷을 현재 Master와 다시 비교한다. 원문·연결·버전이 달라졌거나
패킷이 편집됐으면 중단한다. 각 인용문은 실제 원문 부분 문자열이어야 하며
URL·버전·해시도 일치해야 한다. 신규 초안은 revision=1, 개정은 패킷의 지정
revision을 사용한다. 매핑은 기본적으로 비워 두며 8~9절 계약으로 작성한다.
개정 제한과 재승인은 7절을 따른다.

정확히 같은 지식 필드만 합쳐 근거 목록을 보존하고 ID 참조를 다시 연결한다.
원문 충돌에 연결된 항목은 자동 병합하지 않는다. 병합 후 선수관계 순환이나
불량 참조가 생기면 실패한다. 의미 유사성에 의한 병합은 작성자가 판단한다.

`candidate/`에 draft.json, report.json, authored.json을 저장한다. 최초 작성본을
보존하며 병합 ID와 입력·출력 해시를 보고한다. 모든 검토 상태는 draft로
재설정한다. 사람이 승인했다는 입력 문자열만으로 승인 상태를 유지하지 않는다.
이 결과는 구조·근거 확인을 통과한 초안이며 기술적 정확성 승인 자료가 아니다.

## 현재 검증 상태

합성 자료 기반 작성·중복 통합·조건 차이 보존·충돌 보존·위조 인용 거부·
기준 자료 변경 거부·쓰기 격리 테스트를 추가했다. Nyquist Topic의 실제 연결
자료 2개로 prepare를 실행했다. 실제 자료의 authored.json 작성과 Topic별
의미 검토는 Stage 7 대표 Topic 검증에서 진행한다.

아래 최초 연결 미리보기·적용 기능을 제공한다. 기존 연결의 개정은 7절을 따른다.

## 4. 검토 템플릿과 미리보기

```bash
python3 scripts/author_topic_learning_synthesis.py review-template \
  --topic-id nyquist_stability_criterion_gain_phase_margin --run-id stage4_initial
python3 scripts/author_topic_learning_synthesis.py preview \
  --topic-id nyquist_stability_criterion_gain_phase_margin --run-id stage4_initial \
  --decision data/topic_learning_authoring/nyquist_stability_criterion_gain_phase_margin/stage4_initial/decision.template.json
```

`decision.template.json`은 pending 적용 결정과 항목별 draft 검토로 시작한다.
별도 파일로 복사해 검토 결과를 작성한다. 계약은
`schemas/learning_synthesis_decision.schema.json`에 정의한다.

- application: `decision`(pending/approve/reject), `actor`, `actor_type=human/llm`, `decided_at`
- reviews: 각 knowledge/relations/conflicts/learning_path의 `target`, `status`,
  `actor`, `actor_type`(human/llm), `decided_at`, `note`
- human_verified에는 human 검토자, llm_reviewed_human_pending에는 llm 검토자가 필요하다.
- 모든 항목을 포함해야 하며 draft는 검토자·시각을 null로 둔다.
- 후보 해시와 기준 Master 해시는 템플릿에서 보존한다. 내용 수정 시 후보를 다시 만든다.

미리보기는 파일을 쓰지 않는다. 현재 출처 패킷으로 후보를 재생성하고 저장된
후보·보고서·검토 해시를 대조한다. 적용 승인과 표시 가능한 학습 절이 모두
있어야 can_apply=true다. 연결 승인과 기술적 정답 승인은 구별한다.
학습 절에 LLM 검토만 있으면 화면도 사람 검토 대기임을 계속 표시한다.

## 5. 명시적 최초 적용

검토를 마친 `decision.reviewed.json`이 있다고 가정한 명령이다. 이 문서의
예시는 실행된 승인 기록이 아니다.

```bash
python3 scripts/author_topic_learning_synthesis.py apply \
  --topic-id nyquist_stability_criterion_gain_phase_margin --run-id stage4_initial \
  --decision data/topic_learning_authoring/nyquist_stability_criterion_gain_phase_margin/stage4_initial/decision.reviewed.json \
  --applied-by operator-name
```

적용은 Linux flock으로 동일 Topic의 이 도구 실행을 직렬화하고, immutable
자료·검토 기록·원래 Master 바이트를 비공개 디렉터리에 먼저 저장한다. 마지막에
Master를 원자적으로 교체한다. 기존 Grading payload 동일성을 적용 전에 검사한다.
직전 source/Master가 변경되면 중단한다. 개정은 새 run에서 기존 참조를 고정한다.

쓰기 오류가 교체 전에 나면 원래 Master는 그대로 유지된다. 준비된 자료와
backup은 남을 수 있다. audit의 `receipt.json`은 prepared 상태이며 실제 적용
여부는 현재 Master와 `master.after.json`의 바이트 일치로 판단한다. 다른 편집
도구는 이 lock을 사용하지 않을 수 있으므로 적용 중 동시 수동 편집은 피한다.
이 절차는 운영체제 파일 교체의 원자성을 이용하며 다중 파일의 전원 장애까지
포함한 트랜잭션 DB 보장을 제공하지 않는다.

검토자 이름은 운영자의 명시적 기록이며 로그인 인증·서명 검증 기능은 아니다.
자동 도구는 실제 인간 검토 없이 actor_type=human을 채우면 안 된다.

## 6. LLM 승인과 사람 검토 분리

2026-10-05 사용자 정책 변경: 확실한 학습 콘텐츠는 LLM이 승인하고 불확실한
항목만 사람에게 넘긴다. 이전 절의 사람 승인 전용 제한을 학습 최초 연결에 한해
확장한다. 기존 decision-v1에 상태를 추가했으며 기존 결정 파일은 유효하다.

| 상태 | 의미 | 학습 노출 |
| --- | --- | --- |
| llm_verified | LLM이 근거와 적용 범위를 검토하여 승인 | 가능, LLM 승인 표시 |
| human_verified | 실제 사람이 검토 | 가능, 사람 승인 표시 |
| human_review_required | 불확실·근거 부족 | 해당 지식 및 의존 절 보류 |
| llm_reviewed_human_pending | 이전 계약의 검토 대기 | 기존 표시 유지; 신규 LLM 적용 전 재분류 필요 |
| draft / rejected | 미검토 / 거절 | 보류 |

LLM 승인 판단에는 원문 대조, 수식·단위·적용 조건, 예외 및 관련 계산 검토를
사용하고 note에 근거를 기록한다. 단순 confidence 점수나 schema 통과는 사실
확정의 근거가 아니다. validator는 이 판단의 진실성까지 증명하지 않는다.

application.actor_type=llm으로 최초 연결할 수 있다. 학습 경로 자체는 검토
완료여야 하며, legacy pending 항목을 모두 분류하고 표시 가능한 절이 있어야
한다. human_review_required 항목은 주석과 함께 보존되고 preview의
human_review_targets에 표시된다. 선행 항목이 보류되면 의존 절도 노출하지 않는다.
충돌의 resolved 승격은 기존 사람 검토 조건을 유지한다.

LLM 승인은 채점 기준 변경, grading_links 사람 승인, 신규 채점용 Topic의
approve-topic을 대체하지 않는다. 블로그 원문은 수정하지 않으며 모든 적용은
기존 해시 검증·Grading 동일성 확인·원본 백업·감사 기록 절차를 사용한다.
기존 synthesis의 개정은 아래 제한된 절차를 따른다.

### 최초 LLM 적용 결과

Nyquist Master revision 25에 2개 WordPress 글을 종합한 학습 문서를 연결했다.
S0~S4는 LLM 승인, K5/S5의 안정 경계 표현은 사람 검토 대상으로 보류했다.
실제 Training View의 5절 노출·6절 보류와 적용 전후 Grading 동일성을 확인했다.
승인 결정·원본 Master 백업·종합 문서는 비공개 data 경로에 보관한다.
공개 checkout에는 원문을 포함하지 않으며 비공개 파일이 없으면 기존 계약대로
학습 종합 자료 unavailable로 표시하고 기존 View로 동작한다.

## 7. 학습 문서 개정·재승인

실제 Topic 내용 검토는 보류하고 합성 자료로 검증한 구조다. 기존 prepare/build/
review-template/preview/apply 명령을 **새 run-id**로 실행한다. 이전 run은 보존한다.

1. prepare는 현재 Master 해시와 이전 synthesis의 경로·revision·해시를 고정한다.
2. 이전 파일의 해시·문서 identity를 검사하고 target_synthesis_revision=이전+1을 제공한다.
3. 작성자는 현재 sources.json을 기준으로 새 문서를 작성한다. 원문을 수정하지 않는다.
4. build는 revision을 확인하고 모든 검토를 draft로 초기화한다. 과거 승인은 승계하지 않는다.
5. 새 후보의 항목별 검토·승인 후 preview/apply한다. Grading 동일성은 계속 강제한다.
6. 새 immutable 문서와 감사 백업을 먼저 저장하고 Master 참조만 원자적으로 교체한다.
   이전 문서는 삭제하지 않는다. 구버전 진단 링크는 기존 revision 검사로 구별된다.

출처가 준비 이후 바뀌면 재준비해야 한다. 이 경로는 WordPress 수집이나 Master
source reference 변경을 대신하지 않는다. 기존 파일이 없거나 변조됐으면 차단한다.
기존 grading_links가 있으면 아래 매핑 이관 계약을 적용한다. 실제 사용자 콘텐츠의
개정·승인은 이번 구조 구현 과정에서 수행하지 않는다.

## 8. 기존 평가 매핑 이관

prepare는 해시가 고정된 이전 문서의 grading_links를 previous_grading_links로
제공한다. 새 문서는 모든 기존 link_id를 유지해야 한다. 누락은 거부하며,
새 ID는 9절의 명시적으로 준비된 canonical target이 있을 때만 허용한다.
기존 ID의 target/knowledge_ids/section_ids 변경은 허용하지만 현재 canonical의
해시·record ID와 문서 참조 검증을 통과해야 한다. 지식 중복 병합 시 참조도 갱신한다.

build report와 preview의 mapping_changes는 ID별 unchanged/modified 및 before/
after를 제공한다. unchanged도 학습 본문이 달라질 수 있으므로 승인을 승계하지
않고 draft로 초기화한다. 모든 grading_links 항목이 review-template에 포함된다.

- 유지·변경 후 사용: 별도 사람 검토로 human_verified, 검토 근거 필수.
- 사용 중단: 사람의 rejected 결정과 사유를 기록한다. 물리적으로 삭제하지 않는다.
- 불확실: human_review_required로 보존하고 Feedback 추천에서 제외한다.
- 미검토: draft로 보존하고 Feedback 추천에서 제외한다.

LLM의 학습 본문 승인만으로 매핑을 활성화하거나 사용 중단하지 않는다. 매핑을
보류한 채 검증된 학습 절만 반영할 수 있다. 기존 Feedback 소비자의 사람 승인
검사와 canonical provenance 확인은 그대로다. 기존 매핑 참조는 보류·중단 시에도
유효해야 하며, 대상 ID가 없어졌을 때 자동 추측으로 이관하지 않는다.

이는 진단→학습 절 안내의 개정 계약이다. 채점 기준이나 배점을 수정하지 않으며
최초 매핑 생성·새 매핑 ID 추가는 아래 CLI 절차를 따른다.

## 9. 새 요구사항→학습 절 매핑 작성

실제 콘텐츠는 보류하고 합성 fixture로 검증한 인터페이스다.

```bash
python3 scripts/author_topic_learning_synthesis.py prepare \
  --topic-id <topic_id> --run-id <new_run> --include-mapping-targets
python3 scripts/author_topic_learning_synthesis.py add-mapping \
  --topic-id <topic_id> --run-id <new_run> --authored <authored.json> \
  --link-id <new_link_id> --requirement-id <canonical_requirement_id> \
  --knowledge-id <knowledge_id> --section-id <section_id>
```

sources.json의 mapping_targets는 현재 Master가 참조하는 question_demand_axes의
requirement_id, requirement_text, source_file, 파일 해시를 제공한다. 해당 파일이
없으면 빈 목록이며 이름·문장 유사도로 ID를 추측하지 않는다. 중복 ID·잘못된
Topic·빈 요구사항은 거부한다. 기존 prepare의 기본 동작은 유지된다.

add-mapping은 정확한 ID를 선택해 authored.mapping.json을 별도로 저장한다.
입력은 수정하지 않고 기존 출력이 있으면 덮어쓰지 않는다. knowledge-id와
section-id는 반복 지정할 수 있으며 선택한 절에 해당 지식이 실제 연결되어야
한다. 여러 매핑은 이 파일의 grading_links에 추가하거나 새 run에서 작성한다.
직접 편집해도 같은 canonical target·참조·build 검증을 적용한다.

이후 build의 --authored에 authored.mapping.json을 지정하고 기존 review-template,
preview, apply 절차를 따른다. 신규 매핑은 mapping_changes에서 added로 표시되며
모든 승인은 draft로 초기화된다. 별도 사람이 human_verified로 검토하기 전에는
Feedback에서 사용하지 않는다. 학습 콘텐츠의 LLM 승인과 채점 규칙은 변경하지 않는다.

준비 후 canonical 파일이 바뀌면 packet 재비교에서 차단하고 새 run을 요구한다.
지원하는 신규 매핑은 현재 Feedback 소비자가 사용하는 question_demand_axes에
한정한다. 다른 canonical 종류의 기존 매핑 이관은 앞 절의 기존 계약을 유지한다.
