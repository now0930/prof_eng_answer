# prof_eng_answer

산업계측제어기술사 논술 답안을 Telegram으로 받아 채점하고, 확정된 결과를 학습·복습에 연결하는 프로젝트입니다. 채점은 기존 A/B/C/D/E 25점 계약과 결정론적 primary 판정이 기준입니다.

## 큰 구조

```text
Topic Pack source ──생성──► generated bank ──► 기존 Grader ──► 확정 채점 결과
       │                                                   │
       └──► Master Topic Pack의 승인된 참조 ──► Training / Diagnosis View
                         ▲                         │             │
WordPress 글·HTML·자사 PDF·이미지 ──출처·검토·승인──┘             │
                                                 /review 학습    └──► 피드백
                                                       └──► 별도 학습 이력·Review Queue
```

Master는 Topic의 식별자·버전·출처와 View 계약을 관리합니다. **운영 Grader는 Master나 Grading View를 거치지 않고 generated bank를 직접 읽습니다.** Grading View는 기존 Topic Pack과의 호환성을 확인하는 읽기 전용 projection이며 새 채점 엔진이 아닙니다. Training View는 학습자료를, Diagnosis/Feedback View는 확정 점수 이후의 안내를 제공합니다. 두 View 모두 점수·판정을 바꾸지 않습니다.

WordPress는 원문과 출처의 원천입니다. HTML·OCR·검토 주석을 연결했다고 채점 기준이 되지는 않습니다. 채점 기준 변경은 별도 제안·사실 검토·승인 및 Topic Pack 검증을 거칩니다. 개인 답안, WordPress 원문 DB/OCR 본문, 인증정보는 공개 저장소에 올리지 않습니다.

계층별 실제 소비 경로와 승인 경계는 [시스템 구조](docs/system_architecture.md)에 정리했습니다.

## 사용과 실행

Python 3.11 환경에서 저장소 루트 기준:

```bash
cp .env.example .env
# .env에 필요한 Telegram 및 provider 설정 입력
python3 bot.py
```

Compose 예제를 사용할 때는 `docker-compose.example.yml`을 환경에 맞게 확인하세요. 실제 운영 배포·재시작은 [운영 절차](docs/operation_runbook.md)를 따릅니다. GitHub `main` 병합만으로 운영 서버의 checkout이나 실행 중인 봇이 자동 갱신되는 것은 아닙니다.

Telegram에서 `/grade`로 문제와 답안을 제출하고, `/review <topic_id 또는 주제명>`으로 복습할 주제를 직접 지정합니다. `/review`는 날짜별 자동 추천 명령이 아닙니다. 저장된 시도·진단·복습 상태는 Topic Pack과 별도 사용자 데이터입니다.

## 소스와 검증

| 경로 | 책임 |
|---|---|
| `rubrics/topic_packs/<topic_id>/` | 승인·검증 대상인 채점용 source |
| `rubrics/generated/` | source로부터 만든 운영 bank 6개; 직접 수정 금지 |
| `master_topic_packs/` | Topic 식별자·참조·세 View의 계약 |
| `study/` | Training·Diagnosis View, 이력과 Review Queue |
| `grading/`, `grading_agents.py`, `bot.py` | 채점·결과 확정·Telegram 연동 |
| `docs/` | 구조, 작성·승인 절차, 운영 지침 |

현재 커밋의 generated manifest에는 Topic 86개가 있습니다. 이들은 공식 기출문항 목록이 아니라 출제 가능성을 기준으로 구성한 지식 단위입니다. 개수와 내용은 고정된 약속이 아니므로 현재 source와 manifest를 확인하세요.

새 managed Topic은 `rubric_manager.py add-topic`으로 초안을 만들고 사람 검토 후 `rubric_manager.py approve-topic`으로 승인합니다. 기존 Topic 수정도 [작성·승인 절차](docs/topic_pack_workflow.md)를 따르고 생성물을 공식 builder로 갱신합니다. 재생성 결과와 커밋된 bank가 같은지는 작업 트리를 바꾸지 않는 검사로 확인할 수 있습니다.

```bash
python3 -B scripts/check_generated_rubrics_freshness.py
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

CI는 release 회귀, generated 재생성 일치, 작업 트리의 의도치 않은 변경을 검사합니다. 별도 opt-in 재현성 검사와 실제 운영 배포 확인은 이 CI 통과만으로 완료됐다고 간주하지 않습니다.

## 상세 문서

- [문서 길잡이](docs/README.md) · [시스템 구조와 권한](docs/system_architecture.md)
- [채점 아키텍처](docs/grading_architecture.md) · [Topic Pack 구조](docs/topic_pack_architecture.md)
- [Master/View 계약](docs/master_view_architecture.md) · [WordPress와 View 계약](docs/wordpress_topic_pack_view_contract.md)
- [학습 계층](docs/learning_layer.md) · [Topic 학습 구성](docs/topic_learning_synthesis_contract.md)
- [Topic Pack 작성·승인 절차](docs/topic_pack_workflow.md) · [운영 절차](docs/operation_runbook.md)
