# LLM Provider

이 문서는 `prof_eng_answer`의 LLM provider 구조를 설명한다. 채점 점수 구조는 `grading_architecture.md`를 우선한다.

## 1. Provider 구성

| 구성 | 역할 |
|---|---|
| Ollama local model | 1차 보조 분석과 legacy pipeline 입력 |
| Gemini | primary semantic grader |
| Naver CLOVA | fallback 또는 직접 지정 semantic grader |
| Python rules | LLM 결과를 최종 점수와 출력으로 후처리 |

운영 기준:

```text
LLM_PROVIDER=auto
LLM_PRIMARY=gemini
LLM_FALLBACK=clova
```

## 2. Telegram 명령

```text
/provider
/provider auto
/provider gemini
/provider clova
/provider reset
```

의미:

| 명령 | 의미 |
|---|---|
| `/provider` | 현재 chat의 provider 설정 확인 |
| `/provider auto` | primary 우선, 실패 시 fallback |
| `/provider gemini` | Gemini만 사용 |
| `/provider clova` | CLOVA만 사용 |
| `/provider reset` | 기본값으로 초기화 |

## 3. 환경변수

| 변수 | 의미 |
|---|---|
| `OLLAMA_URL` | Ollama API URL |
| `OLLAMA_MODEL` | 로컬 보조 모델 |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini 모델명 |
| `CLOVA_API_KEY` | Naver CLOVA API key |
| `CLOVA_MODEL` | CLOVA 모델명 |
| `CLOVA_HOST` | CLOVA endpoint host |
| `CLOVA_ENDPOINT` | CLOVA endpoint path |
| `LLM_PROVIDER` | `auto`, `gemini`, `clova` |
| `LLM_PRIMARY` | auto 모드 primary |
| `LLM_FALLBACK` | auto 모드 fallback |

민감 정보는 `.env`에만 둔다. Git에는 commit하지 않는다.

## 4. Provider와 최종 점수의 관계

LLM provider는 의미 평가와 보완 문구를 제공한다. 최종 점수는 다음 후처리를 거친다.

```text
semantic grader result
→ A/B/C/D/E Python scoring
→ Fact Anchor / Model Answer Bank 보강
→ Question Type coverage
→ Difficulty ceiling
→ Telegram display normalization
```

따라서 provider가 바뀌어도 Python rule이 score cap, score_range, ceiling, fallback, 출력 정합성을 보정한다.

## 5. JSON parsing fallback

LLM은 가끔 다음 형태의 malformed JSON을 반환할 수 있다.

- code fence 포함
- JSON object 앞뒤 설명문 포함
- 닫는 `]` 또는 `}` 누락
- LaTeX `\omega`, `\zeta`, `\frac` 같은 backslash 포함

`grading_agents.py`의 parser는 가능한 범위에서 이를 복구한다. 그래도 실패하면 legacy 1차 분석은 fallback될 수 있으나, phase2 semantic/Python scoring이 최종 grade를 다시 구성할 수 있다.

로그에서 확인할 문구:

```text
[agent] 모델 분석 JSON 파싱에 실패하여 fallback 채점을 적용합니다.
[agent] Gemini semantic grader applied.
[agent] phase2 layered scoring applied: ...
```

위와 같이 뒤에서 phase2가 적용되면 최종 사용자 출력은 phase2 결과를 기준으로 본다.

## 6. Provider 점검

Telegram:

```text
/provider
```

로그:

```bash
cd ~/hermes
docker logs --tail=120 prof_eng_answer_bot | grep -E 'Provider|Gemini|CLOVA|semantic grader|fallback' || true
```

## 7. 관련 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | `/provider` 명령 처리, `call_ollama()`, Telegram 출력 |
| `llm_provider_settings.py` | chat별 provider 설정 |
| `llm_provider_router.py` | provider routing |
| `gemini_grader.py` | Gemini semantic grader |
| `clova_grader.py` | CLOVA semantic grader |
| `grading_agents.py` | provider 결과를 phase2 pipeline에 결합 |
