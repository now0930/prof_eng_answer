# prof_eng_answer

**산업계측제어기술사 논술 답안을 채점하고 복습하는 개인 학습 도구**입니다.
Telegram으로 답안을 제출하고, 확정 점수와 부족한 지식을 확인한 뒤 필요한 주제를 복습합니다.

## 공부하는 순서

1. ChatGPT에 **25점형 문제 1개**를 요청하고, 힌트 없이 직접 답안을 씁니다.
2. Telegram에서 `/grade`를 입력하고 문제와 답안을 보냅니다.
3. 마지막 줄에 **`끝.`**을 보내 채점을 실행합니다.
4. 확정 결과를 확인한 다음 ChatGPT 모범답안과 비교합니다.
5. `/review <topic_id 또는 주제명>`으로 복습하고, `/review done <topic_id>`로 완료를 기록합니다.

```text
/grade
문제: 계측 시스템의 신뢰성을 높이는 방법을 설명하시오.
답안:
1. 신뢰성 개념 ...
2. 설계·유지관리 방법 ...
끝.
```

| 명령 | 기능 |
| --- | --- |
| `/grade` | 문제·답안을 모으고 `끝.`을 받으면 채점 |
| `/review 주제` | 해당 주제의 학습자료와 이전 피드백 보기 |
| `/review done 주제ID` | 복습 완료 기록 |
| `/new` | 새 세션 생성 |
| `/help` | 다른 명령 확인 |

복습은 날짜별 자동 출제가 아니라 **사용자가 선택**합니다. AI 모범답안과 복습 안내는 확정 점수를 바꾸지 않습니다.

## 자료의 역할

```text
Topic Pack 원본 → 생성된 채점 자료 → Telegram 채점 → 확정 결과
WordPress 원문/OCR → 승인된 출처 연결 → 학습 View → 복습 이력
```

- **Topic Pack** (`rubrics/topic_packs/`): 검토·승인 대상인 채점 기준 원본.
- **생성 자료** (`rubrics/generated/`): 운영용 채점 bank 5개와 주제 목록 1개. 직접 수정하지 않습니다.
- **Master** (`master_topic_packs/`): 주제와 출처·학습 View의 연결 정보. 채점기의 직접 입력은 아닙니다.
- **WordPress·OCR**: 비공개 학습 참고자료. 자동으로 정답·감점 규칙이 되지 않습니다.
- **학습 DB**: 문제·시도·확정 점수·요약 진단·복습 상태. 원본 답안은 비공개 세션에 별도 보존합니다.

배점은 **A 3 / B 6 / C 8 / D 6 / E 2 = 25점**입니다. 실제 채점 엔진은 실행 설정을 따릅니다.
`DETERMINISTIC_GRADING_PRIMARY`는 활성화와 권한 확인이 필요한 선택 경로이며, 저장소의 `.env.example` 기본값은 `false`입니다.

## 개발용 실행

Python 3.11과 필요한 서비스·인증정보를 준비한 뒤 저장소 루트에서 실행합니다.

```bash
cp .env.example .env
# .env에 본인 설정을 입력
set -a
. ./.env
set +a
export PROF_ENG_BASE_DIR="$PWD"
python3 bot.py
```

`.env`를 복사만 하면 환경변수는 자동 적용되지 않습니다. 이 명령은 실제 Telegram polling을 시작하므로 **운영 봇과 중복 실행하지 마세요.**
서버 운영·배포는 [운영 절차](docs/operation_runbook.md)를 따릅니다. 배포용 코드 검증은 전체 오프라인 pytest이며, 유료 정확도 진단은 필수가 아닙니다.

```bash
python3 -B scripts/release_candidate.py validate
```

## 문서

| 목적 | 문서 |
| --- | --- |
| 구조와 채점 흐름 | [시스템 구조](docs/system_architecture.md), [채점 구조](docs/grading_architecture.md) |
| 문제·채점·복습 | [학습 루프](docs/answer_review_loop_policy.md), [학습 계층](docs/learning_layer.md) |
| Topic Pack 작성·승인 | [Topic Pack 절차](docs/topic_pack_workflow.md), [Fact 정책](docs/fact_anchor_eligibility_policy.md) |
| **WordPress URL 추가·변경** | **[반복 운영 정책](docs/wordpress_url_continuous_workflow.md)**, [AI 실행 계약](docs/wordpress_url_continuous_ai_runbook.md) |
| 공개·비공개 자료·백업 | [데이터/보고서 안내](docs/data_reports_inventory.md), [비공개 백업](docs/private_runtime_backup.md) |
| **AI/Codex의 파일·함수·계약 확인** | **[AI·개발자용 구현 참조](docs/ai_implementation_reference.md)** |
| 기타 문서 | [문서 인덱스](docs/README.md) |

개인 답안·세션·WordPress OCR 원문·운영 DB·로그·실제 `.env`는 공개 GitHub에 올리지 않습니다.
