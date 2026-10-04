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
URL·버전·해시도 일치해야 한다. revision=1의 신규 초안만 지원하며 채점 연결은
비워 둔다. 기존 종합 문서의 갱신·승인은 후속 적용 경로에서 담당한다.

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

후속 구현으로 아래 최초 연결 미리보기·적용 기능을 제공한다. 기존 연결의
교체/개정은 아직 지원하지 않는다.

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

- application: `decision`(pending/approve/reject), `actor`, `actor_type=human`, `decided_at`
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
직전 source/Master가 변경되면 중단하며 기존 synthesis가 있으면 덮어쓰지 않는다.

쓰기 오류가 교체 전에 나면 원래 Master는 그대로 유지된다. 준비된 자료와
backup은 남을 수 있다. audit의 `receipt.json`은 prepared 상태이며 실제 적용
여부는 현재 Master와 `master.after.json`의 바이트 일치로 판단한다. 다른 편집
도구는 이 lock을 사용하지 않을 수 있으므로 적용 중 동시 수동 편집은 피한다.
이 절차는 운영체제 파일 교체의 원자성을 이용하며 다중 파일의 전원 장애까지
포함한 트랜잭션 DB 보장을 제공하지 않는다.

검토자 이름은 운영자의 명시적 기록이며 로그인 인증·서명 검증 기능은 아니다.
자동 도구는 실제 인간 검토 없이 actor_type=human을 채우면 안 된다.
