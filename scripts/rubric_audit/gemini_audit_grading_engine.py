import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "data" / "audits"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise SystemExit("GEMINI_API_KEY 환경변수가 없습니다. docker 컨테이너 안에서 실행하거나 .env를 확인하세요.")

FILES_TO_REVIEW = [
    "rubrics/active_profile.json",
    "rubrics/scoring_model/default.json",
    "rubrics/subjects/industrial_instrumentation_control.json",
    "rubrics/raters/layered_default.json",
    "grading_config.py",
    "grading_agents.py",
    "bot.py",
]

def read_text(rel, max_chars=45000):
    path = ROOT / rel
    if not path.exists():
        return f"[MISSING] {rel}"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[:max_chars] + f"\n\n...[TRUNCATED {len(text) - max_chars} chars]..."
    return text

def latest_session():
    base = ROOT / "data" / "sessions"
    if not base.exists():
        return None
    dirs = [p for p in base.iterdir() if p.is_dir()]
    if not dirs:
        return None
    return max(dirs, key=lambda p: p.stat().st_mtime)

def read_latest_artifacts():
    s = latest_session()
    if not s:
        return {"latest_session": None}

    artifacts = {"latest_session": str(s.relative_to(ROOT))}
    for name in [
        "grade.json",
        "volume_evaluation.json",
        "answer_page_evaluation.json",
        "fact_anchor_evaluation.json",
        "connection_evaluation.json",
        "interview_followup.json",
        "rater_weighted_evaluation.json",
        "input.txt",
    ]:
        p = s / name
        if p.exists():
            artifacts[name] = p.read_text(encoding="utf-8", errors="replace")[:30000]
        else:
            artifacts[name] = "[MISSING]"
    return artifacts

source_bundle = {}
for rel in FILES_TO_REVIEW:
    source_bundle[rel] = read_text(rel)

latest = read_latest_artifacts()

prompt = f"""
너는 기술사 답안 채점 시스템을 검토하는 독립 감사자다.

목표:
- 현재 구현이 사용자의 의도에 맞는지 평가한다.
- 코드 수정은 하지 말고, 구조·채점 철학·실행 결과·위험요소를 평가한다.
- 특히 아래 기준을 엄격히 본다.

사용자의 채점 철학:
1. 기술사 25점 문항은 답안지 약 3쪽 수준의 전개를 평균 답안량으로 본다.
2. 짧은 텍스트 답안은 고득점으로 평가하면 안 된다.
3. 키워드만 있다고 높은 점수를 주면 안 된다.
4. 문제 의도 파악 → 문제 요구 파악 → fact 기반 설명 → 현장 적용·제언 → 연결성/면접 방어 가능성이 필요하다.
5. fact만 맞으면 한계가 있고, 현장 적용·제언과 기술사적 판단이 있어야 고득점 가능하다.
6. 교수·기술사·기업 임원 3인 채점 관점은 달라야 한다.
7. C항목은 단순 키워드가 아니라 문제별 Fact Anchor로 평가해야 한다.
8. 사진 3장과 OCR 텍스트가 함께 들어올 때는 답안지 쪽수와 OCR 품질을 함께 판단해야 한다.

현재 구현 단계:
- active_profile 연결
- A/B/C/D/E layer scoring
- answer sheet volume cap
- fact anchor scoring
- connection evaluation
- interview follow-up
- rater weighted scoring
- Telegram format_result 보정

검토해야 할 산출물:
- 코드와 설정 파일
- 최신 grade.json
- fact_anchor_evaluation.json
- connection_evaluation.json
- rater_weighted_evaluation.json
- volume_evaluation.json

아래 형식으로 한국어로 답하라.

1. 총평
2. 현재 구현이 사용자의 채점 철학을 얼마나 반영했는지: 0~100점
3. 잘 된 부분
4. 위험하거나 부정확한 부분
5. 채점 점수가 과대/과소평가될 가능성
6. Gemini가 보기에 반드시 고쳐야 할 부분 TOP 5
7. 다음 단계 우선순위
8. 이 시스템을 실제 답안지 사진 3장 + OCR에 적용하기 전에 필요한 검증 테스트
9. 최종 결론: 계속 진행 / 보류 / 재설계 중 하나

중요:
- 단순 칭찬하지 말고 비판적으로 평가하라.
- 코드가 휴리스틱 중심이면 그 한계를 지적하라.
- 기술사 답안 채점이라는 맥락에서 평가하라.
- 근거는 제공된 파일 내용과 최신 결과에 기반하라.

[FILES]
{json.dumps(source_bundle, ensure_ascii=False, indent=2)}

[LATEST_SESSION_ARTIFACTS]
{json.dumps(latest, ensure_ascii=False, indent=2)}
"""

payload = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 8192
    }
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    method="POST"
)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_path = AUDIT_DIR / f"gemini_audit_raw_{ts}.json"
md_path = AUDIT_DIR / f"gemini_audit_{ts}.md"

try:
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")
    raise SystemExit(f"Gemini HTTPError {e.code}\n{body}")
except Exception as e:
    raise SystemExit(f"Gemini request failed: {e!r}")

raw_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

text_parts = []
for cand in data.get("candidates", []):
    content = cand.get("content", {})
    for part in content.get("parts", []):
        if "text" in part:
            text_parts.append(part["text"])

answer = "\n\n".join(text_parts).strip()
if not answer:
    answer = json.dumps(data, ensure_ascii=False, indent=2)

md_path.write_text(answer, encoding="utf-8")

print("Gemini audit complete")
print("model:", MODEL)
print("raw:", raw_path)
print("report:", md_path)
print()
print(answer[:5000])
