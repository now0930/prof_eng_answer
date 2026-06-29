# Operation Runbook

## 1. 목적

이 문서는 `prof_eng_answer` Telegram 채점 Bot의 운영 점검, 재시작, 장애 대응 절차를 정리한다.

현재 운영 기준은 다음과 같다.

| 항목 | 기준 |
|---|---|
| Repository | `~/hermes/workspace/prof_eng_answer` |
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 최종 출력 정리 위치 | `send_message()` boundary |
| 수동 nohup 실행 | 사용하지 않음 |

## 2. 빠른 상태 점검

    cd ~/hermes

    docker compose ps prof-eng-answer-bot
    docker logs --tail=120 prof_eng_answer_bot

정상 기준:

    prof_eng_answer_bot   Up

Telegram에서 `/grade` 요청 시 다음 흐름이 보여야 한다.

    채점을 시작합니다.
    채점 완료: .../25
    [Question Type Coverage]

## 3. Git 최신 상태 확인

    cd ~/hermes/workspace/prof_eng_answer

    git fetch origin main

    echo "[local HEAD]"
    git rev-parse --short HEAD

    echo "[origin/main]"
    git rev-parse --short origin/main

    echo
    git status --short
    git log --oneline --decorate -5

정상 기준:

    local HEAD == origin/main
    git status --short 출력 없음

## 4. Bot 재시작

일반 재시작:

    cd ~/hermes

    docker compose restart prof-eng-answer-bot

    sleep 5

    docker compose ps prof-eng-answer-bot
    docker logs --tail=80 prof_eng_answer_bot

완전 재기동:

    cd ~/hermes

    docker compose stop prof-eng-answer-bot

    sleep 3

    docker compose up -d prof-eng-answer-bot

    sleep 8

    docker compose ps prof-eng-answer-bot
    docker logs --tail=120 prof_eng_answer_bot

다음 상황에서는 완전 재기동을 권장한다.

- `bot.py` 실행 흐름을 수정한 경우
- formatter 또는 `send_message()` 경계를 수정한 경우
- Telegram 응답이 이전 코드처럼 보이는 경우
- polling 충돌이 의심되는 경우

## 5. 중복 polling 확인

Telegram Bot은 같은 token으로 여러 프로세스가 polling하면 응답이 충돌할 수 있다.

    cd ~/hermes

    echo "[containers]"
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Command}}' \
      | grep -E 'prof|hermes|bot|agent' || true

    echo
    echo "[host python bot processes]"
    ps -ef \
      | grep -E 'prof_eng|run_prof_eng_bot|bot.py|telegram' \
      | grep -v grep || true

    echo
    echo "[prof_eng_answer_bot processes]"
    docker exec prof_eng_answer_bot bash -lc '
    ps -ef | grep -E "python|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
    '

    echo
    echo "[hermes_agent processes]"
    docker exec hermes_agent bash -lc '
    ps -ef | grep -E "prof_eng|bot.py|run_prof_eng_bot|telegram" | grep -v grep || true
    ' 2>/dev/null || true

정상 기준:

    prof_eng_answer_bot 내부에 python -u bot.py 1개
    hermes_agent 내부에는 prof_eng_answer bot.py 없음
    host에서 보이는 python -u bot.py는 컨테이너 프로세스일 수 있음

주의사항:

- `hermes_agent` 내부에서 `nohup python bot.py &`를 실행하지 않는다.
- `telegram_bot_prod` 같은 다른 Bot 컨테이너가 같은 Telegram token을 쓰는지 확인한다.
- 같은 token을 쓰는 프로세스가 둘 이상이면 Telegram 응답이 꼬일 수 있다.

## 6. 실행 명령 확인

    cd ~/hermes

    docker inspect prof_eng_answer_bot \
      --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'

    docker compose config | sed -n '/prof-eng-answer-bot:/,/^[^ ]/p'

정상 기준:

    prof_eng_answer_bot이 bot.py를 실행
    수동 nohup 실행 없음

## 7. 컨테이너 내부 코드 확인

    cd ~/hermes

    docker exec prof_eng_answer_bot bash -lc '
    cd /workspace/prof_eng_answer 2>/dev/null || cd /app 2>/dev/null || exit 1

    pwd

    echo
    echo "[git]"
    git log --oneline --decorate -5 2>/dev/null || true
    git status --short 2>/dev/null || true

    echo
    echo "[bot structure]"
    grep -nE "send boundary legacy GENERAL|final Telegram legacy GENERAL cleanup wrapper|_cleanup_legacy_general_text_for_send|def send_message|if __name__|main\(|while True" bot.py | sed -n "1,220p"
    '

정상 기준:

    send boundary legacy GENERAL cleanup v1 있음
    _cleanup_legacy_general_text_for_send 있음
    def send_message 내부에서 cleanup 호출함
    main()보다 위에 cleanup이 있음
    final Telegram legacy GENERAL cleanup wrapper 없음

예상 형태:

    110:# === send boundary legacy GENERAL cleanup v1 ===
    111:def _cleanup_legacy_general_text_for_send(text):
    150:def send_message(chat_id, text):
    151:    text = _cleanup_legacy_general_text_for_send(text)
    886:def main():
    896:    while True:
    924:if __name__ == "__main__":
    925:    main()

## 8. bot.py 실행 흐름 주의

운영 시 `bot.py`는 다음처럼 실행된다.

    python -u bot.py

파일 내부에서는 다음 코드가 실행된다.

    if __name__ == "__main__":
        main()

`main()` 안에는 polling loop가 있다.

    while True:
        ...

따라서 `if __name__ == "__main__": main()` 아래에 append한 wrapper는 실행되지 않는다.

문제가 되었던 구조:

    if __name__ == "__main__":
        main()

    # 이 아래 cleanup wrapper는 실행형 bot.py에서 실행되지 않음
    def format_result(...):
        ...

올바른 구조:

    send_message() 내부에서 최종 출력 cleanup
    또는 main()보다 위에서 함수 정의

현재 legacy `GENERAL(일반 설명형)` 문구는 `send_message()` boundary에서 정리한다.

## 9. send boundary cleanup 단독 테스트

    cd ~/hermes/workspace/prof_eng_answer

    python3 - <<'PY'
    import bot

    sample = """[보완 방향]
    - C항목 보완: 일반 설명형 유형에서는 '문제 요구에 맞는 핵심 fact, 적용 범위, 한계, 실무 의미를 설명했는가'를 충족하도록 답안을 전개하세요.
    """

    cleaned = bot._cleanup_legacy_general_text_for_send(sample)

    print(cleaned)
    print("legacy remains:", "일반 설명형 유형에서는" in cleaned)
    print("replacement exists:", "문제 유형 lens에 맞는 핵심 fact" in cleaned)

    assert "일반 설명형 유형에서는" not in cleaned
    assert "문제 유형 lens에 맞는 핵심 fact" in cleaned
    PY

정상 기준:

    legacy remains: False
    replacement exists: True

## 10. 대표 smoke test

Telegram에서 다음을 보낸다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 확인:

- 채점을 시작합니다 메시지가 온다.
- 채점 완료 메시지가 온다.
- `[Question Type Coverage]`가 출력된다.
- 문제 유형 lens가 `적용·평가형(IMPLEMENTATION_EVALUATION)`로 표시된다.
- `[보완 방향]`에 `C항목 보완: 일반 설명형 유형에서는 ...` 문구가 없어야 한다.
- 대신 `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나와야 한다.

## 11. Provider 점검

Telegram에서 provider 확인:

    /provider

Provider 변경:

    /provider auto
    /provider gemini
    /provider clova
    /provider reset

운영 권장값:

    LLM_PROVIDER=auto
    LLM_PRIMARY=gemini
    LLM_FALLBACK=clova

## 12. 환경변수 점검

환경변수는 상위 `.env`에서 관리한다.

    ~/hermes/.env

민감 정보는 출력하지 않는다.

확인할 항목:

- `TELEGRAM_BOT_TOKEN` 또는 `BOT_TOKEN` 존재 여부
- `GEMINI_API_KEY` 존재 여부
- `CLOVA_API_KEY` 존재 여부
- `LLM_PROVIDER`
- `LLM_PRIMARY`
- `LLM_FALLBACK`
- `DIFFICULTY_CEILING_MODE`
- `QUESTION_TYPE_COVERAGE_SCORE_MODE`

민감 정보 값을 직접 로그에 남기지 않는다.

## 13. 코드 검증

    cd ~/hermes/workspace/prof_eng_answer

    python3 -m py_compile \
      bot.py \
      grading_agents.py \
      gemini_grader.py \
      clova_grader.py \
      difficulty_strategy.py \
      difficulty_output_adapter.py \
      difficulty_score_ceiling.py \
      question_type_taxonomy.py \
      question_type_coverage_adapter.py \
      question_type_coverage_score_adjuster.py \
      semantic_question_type_prompt.py \
      semantic_question_type_postprocess.py \
      scripts/validate_model_answer_bank.py

Rubric 전체 검증:

    python3 scripts/rubric_manager.py validate-all

정상 기준:

    ALL VALID

## 14. 문서 정합성 점검

README가 참조하는 docs 파일이 실제 존재하는지 확인한다.

    cd ~/hermes/workspace/prof_eng_answer

    echo "[README referenced docs]"
    grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u

    echo
    echo "[missing referenced docs]"
    for f in $(grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u); do
      [ -f "$f" ] || echo "MISSING: $f"
    done

    echo
    echo "[docs files]"
    find docs -maxdepth 1 -type f -name '*.md' | sort

정상 기준:

    MISSING 출력 없음

Markdown fence 균형 검사:

    cd ~/hermes/workspace/prof_eng_answer

    python3 - <<'PY'
    from pathlib import Path
    import re

    bad = False
    for p in [Path("README.md")] + sorted(Path("docs").glob("*.md")):
        s = p.read_text(encoding="utf-8")
        ticks = len(re.findall(r"^```", s, flags=re.MULTILINE))
        tildes = len(re.findall(r"^~~~", s, flags=re.MULTILINE))
        print(f"{p}: backtick_fences={ticks}, tilde_fences={tildes}")
        if ticks % 2 != 0:
            print(f"  ERROR: unbalanced backtick fences in {p}")
            bad = True
        if tildes:
            print(f"  WARN: remaining tilde fences in {p}")
    raise SystemExit(1 if bad else 0)
    PY

정상 기준:

    backtick_fences 짝수
    tilde_fences 0

이 문서는 4칸 들여쓰기 코드블록을 사용하므로 `operation_runbook.md` 자체에는 backtick fence가 없어도 정상이다.

## 15. 문서 변경 반영

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

    git add docs/operation_runbook.md
    git commit -m "Add operation runbook for grading bot operations"
    git push origin main

문서만 바꾼 경우 컨테이너 재시작은 필수는 아니다.

## 16. Rollback

최근 commit만 되돌릴 때:

    cd ~/hermes/workspace/prof_eng_answer

    git log --oneline --decorate -5
    git revert HEAD
    git push origin main

로컬 변경만 버릴 때:

    cd ~/hermes/workspace/prof_eng_answer

    git status --short
    git restore docs/operation_runbook.md

특정 백업 파일을 복원할 때:

    cd ~/hermes/workspace/prof_eng_answer

    ls -lt backups | head
    cp backups/<backup-file> docs/operation_runbook.md

## 17. 자주 보는 증상과 원인

| 증상 | 가능 원인 | 조치 |
|---|---|---|
| Telegram 응답이 오지 않음 | Bot down, token 문제, polling 충돌 | `docker logs`, 중복 polling 확인 |
| 예전 문구가 계속 나옴 | live 프로세스가 이전 코드 import 상태 | 완전 재기동 |
| `import bot` 테스트는 정상인데 Telegram은 비정상 | wrapper가 `main()` 아래 있어 실행되지 않음 | send boundary cleanup으로 이동 |
| `GENERAL(일반 설명형)` 문구 출력 | legacy 문구 cleanup 누락 | `send_message()` boundary 확인 |
| 점수 편차가 큼 | semantic grader 특성, 짧은 답안 | cap rule, prompt, temperature 점검 |
| `MISSING` docs 출력 | README 참조와 docs 파일 불일치 | docs 파일 생성 또는 README 수정 |
