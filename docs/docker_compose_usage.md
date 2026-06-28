# Docker Compose 사용 예시

이 문서는 prof_eng_answer 프로젝트를 다른 환경에서 받을 때 Docker Compose로 실행하는 방법을 설명한다.

실제 운영 환경의 docker-compose.yml은 사용자마다 경로, Docker network, Ollama 위치, API key 설정이 다를 수 있으므로 GitHub에는 docker-compose.example.yml만 포함한다.

---

## 1. 기본 사용 순서

아래 흐름으로 사용한다.

    git clone https://github.com/now0930/prof_eng_answer.git
    cd prof_eng_answer

    cp docker-compose.example.yml docker-compose.yml
    cp .env.example .env

    vim .env
    docker compose up -d

---

## 2. .env 설정

.env에는 실제 key와 모델 정보를 입력한다.

예시:

    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_MODEL=gemini-3.1-flash-lite

    OLLAMA_URL=http://ollama:11434
    OLLAMA_MODEL=

    TELEGRAM_BOT_TOKEN=your_telegram_bot_token

.env는 민감정보를 포함하므로 Git에 커밋하지 않는다.

---

## 3. Ollama 연결 방식

### Ollama가 같은 Docker network에 있는 경우

OLLAMA_URL은 다음처럼 둔다.

    OLLAMA_URL=http://ollama:11434

이 경우 ai_net 네트워크가 필요하다.

    docker network create ai_net

이미 존재하면 생성하지 않아도 된다.

### Ollama가 host에서 실행 중인 경우

환경에 따라 아래처럼 바꿀 수 있다.

    OLLAMA_URL=http://host.docker.internal:11434

Linux에서 이 방식을 쓰려면 docker-compose.yml에 다음 설정이 필요할 수 있다.

    extra_hosts:
      - "host.docker.internal:host-gateway"

---

## 4. 실행

    docker compose up -d
    docker ps
    docker logs -f prof_eng_answer_bot

---

## 5. 중지

    docker compose down

---

## 6. 주의사항

- 실제 운영용 docker-compose.yml은 사용자 환경에 맞게 수정한다.
- GitHub에는 docker-compose.example.yml만 커밋한다.
- .env, logs/, data/sessions/, backups/, hermes_home/은 커밋하지 않는다.
- Telegram token, Gemini API key 등 민감정보는 절대 README나 코드에 직접 쓰지 않는다.
