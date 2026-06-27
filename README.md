# prof_eng_answer

기술사 답안지 채점 MVP.

## 역할 구조

- Telegram: 입출력 창구
- Google/휴대폰: OCR 담당
- Python: 진행 관리자
- Hermes: 채점자

## 사용법

1. Telegram에서 새 세션 시작

/new

2. 답안지 사진 3장 업로드

가능하면 Telegram에서 사진이 아니라 파일로 업로드한다.
사진은 채점용이 아니라 원본 보관용이다.

3. Google OCR 텍스트 채점

/grade
문제: ○○○에 대해 설명하시오.
배점: 25
답안:
1. 서론
...
2. 본론
...
3. 결론
...

## 기타 명령

/status
현재 세션 상태 확인

/rubric
현재 기본 채점 기준 보기

/help
도움말 보기

## 실행

컨테이너 안에서 실행:

docker exec -it hermes_agent bash
cd /workspace/prof_eng_answer
python bot.py

백그라운드 실행:

docker exec -d hermes_agent bash -lc 'cd /workspace/prof_eng_answer && nohup python bot.py >> logs/prof_eng_answer.log 2>&1 &'

## 로그 확인

tail -f ~/hermes/workspace/prof_eng_answer/logs/prof_eng_answer.log

## 세션 저장 위치

data/sessions/
