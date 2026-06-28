#!/usr/bin/env python3
import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from grading_agents import run_agent_pipeline
from llm_provider_settings import get_chat_provider, set_chat_provider, reset_chat_provider, provider_label

BASE_DIR = Path("/workspace/prof_eng_answer")
DATA_DIR = BASE_DIR / "data"
SESSIONS_DIR = DATA_DIR / "sessions"
LOG_DIR = BASE_DIR / "logs"
RUBRIC_FILE = BASE_DIR / "rubrics" / "default.json"
STATE_FILE = DATA_DIR / "state.json"
LOG_FILE = LOG_DIR / "prof_eng_answer.log"

TELEGRAM_TOKEN = (
    os.getenv("TELEGRAM_TOKEN")
    or os.getenv("TELEGRAM_BOT_TOKEN")
    or os.getenv("BOT_TOKEN")
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "hermes3:latest")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "900"))
AUTHORIZED_CHAT_ID = os.getenv("PROF_ENG_CHAT_ID", "").strip()


HELP_TEXT = """
기술사 답안 채점 MVP

사용 순서:

1) 새 세션 시작
/new

2) 답안지 사진 3장 업로드
가능하면 사진보다 파일로 업로드하세요.

3) Google OCR 텍스트 채점
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

기타 명령:
/status  현재 세션 상태
/rubric  현재 채점 기준 보기
/help    도움말
/provider 현재 LLM Provider 확인
/provider auto|gemini|clova|reset
""".strip()


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log(msg):
    ensure_dirs()
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state():
    ensure_dirs()
    if not STATE_FILE.exists():
        return {"last_update_id": 0, "chats": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"last_update_id": 0, "chats": {}}


def save_state(state):
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)


def tg_api(method, params=None):
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN 또는 TELEGRAM_BOT_TOKEN 환경변수가 없습니다.")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    data = None
    if params is not None:
        data = urllib.parse.urlencode(params).encode("utf-8")

    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_message(chat_id, text):
    text = text or ""
    max_len = 3900

    chunks = []
    while len(text) > max_len:
        cut = text.rfind("\n", 0, max_len)
        if cut < 1000:
            cut = max_len
        chunks.append(text[:cut])
        text = text[cut:].lstrip()
    chunks.append(text)

    for chunk in chunks:
        tg_api("sendMessage", {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": "true"
        })


def get_updates(offset):
    return tg_api("getUpdates", {
        "timeout": 30,
        "offset": offset,
        "allowed_updates": json.dumps(["message"], ensure_ascii=False)
    })


def get_file_path(file_id):
    res = tg_api("getFile", {"file_id": file_id})
    if not res.get("ok"):
        raise RuntimeError(f"getFile 실패: {res}")
    return res["result"]["file_path"]


def download_telegram_file(file_id, dest):
    file_path = get_file_path(file_id)
    url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def chat_allowed(chat_id):
    if not AUTHORIZED_CHAT_ID:
        return True
    return str(chat_id) == AUTHORIZED_CHAT_ID


def new_session(chat_id, state):
    sid = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{chat_id}"
    session_dir = SESSIONS_DIR / sid
    (session_dir / "images").mkdir(parents=True, exist_ok=True)

    state["chats"][str(chat_id)] = {
        "active_session": sid,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }
    save_state(state)

    meta = {
        "session_id": sid,
        "chat_id": chat_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "images": [],
        "status": "created"
    }
    (session_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return sid


def get_active_session(chat_id, state):
    chat = state["chats"].get(str(chat_id)) or {}
    sid = chat.get("active_session")
    if not sid:
        sid = new_session(chat_id, state)
    return sid


def load_meta(sid):
    path = SESSIONS_DIR / sid / "meta.json"
    if not path.exists():
        return {"session_id": sid, "images": [], "status": "unknown"}
    return json.loads(path.read_text(encoding="utf-8"))


def save_meta(sid, meta):
    path = SESSIONS_DIR / sid / "meta.json"
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def save_incoming_image(message, chat_id, state):
    sid = get_active_session(chat_id, state)
    session_dir = SESSIONS_DIR / sid
    image_dir = session_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    file_id = None
    ext = ".jpg"

    if "photo" in message:
        photo = message["photo"][-1]
        file_id = photo["file_id"]
        ext = ".jpg"
    elif "document" in message:
        doc = message["document"]
        file_id = doc["file_id"]
        name = doc.get("file_name", "document")
        ext = Path(name).suffix or ".bin"
    else:
        return None

    idx = len(list(image_dir.glob("*"))) + 1
    dest = image_dir / f"page_{idx:02d}{ext}"
    download_telegram_file(file_id, dest)

    meta = load_meta(sid)
    meta.setdefault("images", []).append(str(dest))
    meta["status"] = "images_received"
    save_meta(sid, meta)

    return sid, dest, len(meta["images"])


def load_rubric():
    return json.loads(RUBRIC_FILE.read_text(encoding="utf-8"))


def build_prompt(raw_text, rubric, sid, image_count):
    return f"""
너는 기술사 논술형 답안 채점자다.

절대 규칙:
- OCR 텍스트에 없는 내용을 임의로 보완하지 마라.
- 점수는 항목별 배점 합산으로 산정하라.
- 장점과 감점 사유를 분리하라.
- 채점 기준이 부족하면 "임시 판단"이라고 표시하라.
- 결과는 반드시 JSON 하나만 출력하라.
- JSON 밖의 설명은 쓰지 마라.

세션 ID:
{sid}

첨부 이미지 수:
{image_count}
이미지는 원본 보관용이다. 채점은 사용자가 제공한 OCR 텍스트 기준으로 한다.

채점 기준:
{json.dumps(rubric, ensure_ascii=False, indent=2)}

사용자 입력:
{raw_text}

아래 JSON 형식으로만 답하라:
{{
  "session_id": "{sid}",
  "total_score": 0,
  "max_score": 25,
  "score_range": "예: 14~16",
  "grade_confidence": "high|medium|low",
  "one_line_summary": "한 줄 총평",
  "breakdown": [
    {{
      "item": "항목명",
      "score": 0,
      "max": 0,
      "reason": "점수 사유"
    }}
  ],
  "strengths": ["장점1", "장점2"],
  "weaknesses": ["약점1", "약점2"],
  "missing_keywords": ["누락 키워드1", "누락 키워드2"],
  "rewrite_advice": ["보완점1", "보완점2"],
  "model_answer_outline": ["모범 답안 목차1", "모범 답안 목차2"],
  "next_practice_focus": ["다음 연습 포인트1", "다음 연습 포인트2"]
}}
""".strip()


def call_ollama(prompt):
    url = OLLAMA_URL + "/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
            "num_predict": 4096
        },
        "messages": [
            {
                "role": "system",
                "content": "너는 기술사 답안 채점자다. 반드시 JSON만 출력한다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data.get("message", {}).get("content", "")


def extract_json(text):
    if not text:
        return None

    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            return None

    return None


def grade_answer(chat_id, raw_text, state):
    sid = get_active_session(chat_id, state)
    session_dir = SESSIONS_DIR / sid
    session_dir.mkdir(parents=True, exist_ok=True)

    meta = load_meta(sid)
    image_count = len(meta.get("images", []))
    rubric = load_rubric()

    (session_dir / "input.txt").write_text(raw_text, encoding="utf-8")

    raw_result, parsed = run_agent_pipeline(
        call_ollama_fn=call_ollama,
        raw_text=raw_text,
        rubric=rubric,
        sid=sid,
        image_count=image_count,
        session_dir=session_dir
    )

    if parsed:
        parsed["backend"] = "ollama"
        parsed["model"] = OLLAMA_MODEL
        (session_dir / "grade.json").write_text(
            json.dumps(parsed, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    meta["status"] = "graded"
    meta["graded_at"] = datetime.now().isoformat(timespec="seconds")
    meta["model"] = OLLAMA_MODEL
    meta["agent_pipeline"] = "2026-06-27-agent-v1"
    save_meta(sid, meta)

    return sid, raw_result, parsed



def normalize_grade_for_display(parsed):
    """
    phase2_layered_scoring_v1 결과가 기존 format_result에서 빈칸으로 표시되지 않도록
    summary/confidence/rater comment alias를 보강한다.
    """
    if not isinstance(parsed, dict):
        return parsed

    summary = (
        parsed.get("summary")
        or parsed.get("overall_comment")
        or parsed.get("overall_summary")
        or parsed.get("rater_summary")
        or parsed.get("comment")
        or ""
    )

    confidence = (
        parsed.get("confidence")
        or parsed.get("grade_confidence")
        or parsed.get("confidence_level")
        or "medium"
    )

    if not summary and parsed.get("version") == "phase2_layered_scoring_v1":
        total = parsed.get("total_score")
        max_score = parsed.get("max_score")
        volume = parsed.get("volume_evaluation") or {}
        level = volume.get("level", "unknown")
        summary = f"A/B/C/D/E 구조와 답안지 분량 정책을 적용해 {total}/{max_score}점으로 재산정했습니다. 분량 판단: {level}."

    parsed["summary"] = summary
    parsed["overall_comment"] = summary
    parsed["overall_summary"] = summary
    parsed["rater_summary"] = parsed.get("rater_summary") or summary
    parsed["comment"] = summary

    parsed["confidence"] = confidence
    parsed["grade_confidence"] = confidence
    parsed["confidence_level"] = confidence

    for r in parsed.get("rater_results", []):
        perspective = (
            r.get("perspective")
            or r.get("comment")
            or r.get("reason")
            or r.get("character")
            or ""
        )

        if not perspective:
            rid = r.get("rater_id")
            if rid == "professor":
                perspective = "개념, 용어, fact 설명의 정확성을 중심으로 본 평가입니다."
            elif rid == "professional_engineer":
                perspective = "문제점, fact, 대책의 현장 연결성을 중심으로 본 평가입니다."
            elif rid == "executive":
                perspective = "비용, 시간, 적용 가능성, 기존 설비 영향 등 현실성을 중심으로 본 평가입니다."

        r["perspective"] = perspective
        r["comment"] = perspective
        r["reason"] = perspective
        r["character"] = r.get("character") or perspective

    return parsed


def format_result(parsed, sid=None):
    """
    Telegram 표시용 채점 결과 포맷터.
    legacy grade와 phase2_layered_scoring_v1 grade를 모두 처리한다.
    """
    if not isinstance(parsed, dict):
        return "채점 결과 형식이 올바르지 않습니다."

    def yn(v):
        return "달성" if bool(v) else "미달"

    def pick(*values, default=""):
        for v in values:
            if v is not None and v != "":
                return v
        return default

    total = pick(parsed.get("total_score"), parsed.get("score"), default=0)
    max_score = pick(parsed.get("max_score"), parsed.get("total_points"), default=25)
    score_range = pick(parsed.get("score_range"), parsed.get("estimated_score_range"), default=f"{total}~{total}")

    confidence = pick(
        parsed.get("confidence"),
        parsed.get("grade_confidence"),
        parsed.get("confidence_level"),
        default="medium"
    )

    summary = pick(
        parsed.get("summary"),
        parsed.get("overall_comment"),
        parsed.get("overall_summary"),
        parsed.get("total_comment"),
        parsed.get("comment"),
        parsed.get("rater_summary"),
        default=""
    )

    if not summary and parsed.get("version") == "phase2_layered_scoring_v1":
        volume = parsed.get("volume_evaluation") or {}
        level = volume.get("level", "unknown")
        summary = f"A/B/C/D/E 구조와 답안지 분량 정책을 적용해 {total}/{max_score}점으로 재산정했습니다. 분량 판단: {level}."

    official = pick(parsed.get("official_pass_score"), default=round(float(max_score) * 0.60, 2))
    practical = pick(parsed.get("practical_target_score"), default=round(float(max_score) * 0.70, 2))
    high = pick(parsed.get("high_score_target"), default=round(float(max_score) * 0.80, 2))

    official_met = parsed.get("official_pass_met", float(total) >= float(official))
    practical_met = parsed.get("practical_target_met", float(total) >= float(practical))
    high_met = parsed.get("high_score_met", float(total) >= float(high))

    lines = []
    lines.append(f"채점 완료: {total}/{max_score:g}")
    lines.append(f"예상 점수대: {score_range}")
    lines.append(f"신뢰도: {confidence}")
    lines.append(f"공식 합격선: {official:g}점 ({yn(official_met)})")
    lines.append(f"실전 목표선: {practical:g}점 ({yn(practical_met)})")
    lines.append(f"고득점 기준: {high:g}점 ({yn(high_met)})")
    lines.append("")

    rater_summary = parsed.get("rater_summary")
    if rater_summary and rater_summary != summary:
        lines.append(f"3인 채점 요약: {rater_summary}")
        lines.append("")

    lines.append(f"총평: {summary}")
    lines.append("")

    rater_results = parsed.get("rater_results") or parsed.get("raters") or []
    if rater_results:
        lines.append("[3인 채점위원 점수]")
        for r in rater_results:
            name = pick(r.get("rater_name"), r.get("name"), r.get("id"), default="채점자")
            r_total = pick(r.get("total_score"), r.get("score"), default=total)
            r_max = pick(r.get("max_score"), default=max_score)

            r_official = pick(r.get("official_pass_score"), default=official)
            r_practical = pick(r.get("practical_target_score"), default=practical)
            r_high = pick(r.get("high_score_target"), default=high)

            r_official_met = r.get("official_pass_met", float(r_total) >= float(r_official))
            r_practical_met = r.get("practical_target_met", float(r_total) >= float(r_practical))
            r_high_met = r.get("high_score_met", float(r_total) >= float(r_high))

            perspective = pick(
                r.get("perspective"),
                r.get("comment"),
                r.get("reason"),
                r.get("character"),
                default=""
            )

            lines.append(f"- {name}: {r_total}/{float(r_max):g}")
            lines.append(f"  공식 {float(r_official):g}점: {yn(r_official_met)}")
            lines.append(f"  실전 {float(r_practical):g}점: {yn(r_practical_met)}")
            lines.append(f"  고득점 {float(r_high):g}점: {yn(r_high_met)}")
            if perspective:
                lines.append(f"  관점: {perspective}")
        lines.append("")

    breakdown = parsed.get("breakdown") or parsed.get("items") or []
    if breakdown:
        lines.append("[항목별 평균 점수]")
        for b in breakdown:
            item = pick(b.get("item"), b.get("name"), b.get("criterion"), default="항목")
            score = pick(b.get("score"), default=0)
            bmax = pick(b.get("max"), b.get("max_score"), b.get("points"), default="")
            reason = pick(b.get("reason"), b.get("comment"), default="")

            if bmax != "":
                try:
                    lines.append(f"- {item}: {score}/{float(bmax):g}")
                except Exception:
                    lines.append(f"- {item}: {score}/{bmax}")
            else:
                lines.append(f"- {item}: {score}")

            if reason:
                lines.append(f"  사유: {reason}")
        lines.append("")

    strengths = parsed.get("strengths") or []
    if strengths:
        lines.append("[장점]")
        for x in strengths:
            lines.append(f"- {x}")
        lines.append("")

    weaknesses = parsed.get("weaknesses") or []
    if weaknesses:
        lines.append("[약점]")
        for x in weaknesses:
            lines.append(f"- {x}")
        lines.append("")

    missing = parsed.get("missing_keywords") or parsed.get("missing_points") or []
    if missing:
        lines.append("[누락/보완 키워드]")
        for x in missing:
            lines.append(f"- {x}")
        lines.append("")

    advice = parsed.get("rewrite_advice") or parsed.get("improvement_advice") or []
    if advice:
        lines.append("[보완 방향]")
        for x in advice:
            lines.append(f"- {x}")
        lines.append("")

    focus = parsed.get("next_practice_focus") or []
    if focus:
        lines.append("[다음 연습 포인트]")
        for x in focus:
            lines.append(f"- {x}")

    return "\n".join(lines).strip()

def handle_text(message, chat_id, state):
    text = message.get("text", "")

    if text.startswith("/start") or text.startswith("/help"):
        send_message(chat_id, HELP_TEXT)
        return

    if text.startswith("/new"):
        sid = new_session(chat_id, state)
        send_message(chat_id, f"새 채점 세션을 만들었습니다.\n세션: {sid}\n\n사진 3장을 올리고, OCR 텍스트는 /grade 뒤에 붙여 보내세요.")
        return

    if text.startswith("/status"):
        sid = get_active_session(chat_id, state)
        meta = load_meta(sid)
        send_message(chat_id, f"현재 세션: {sid}\n상태: {meta.get('status')}\n이미지 수: {len(meta.get('images', []))}")
        return

    if text.startswith("/rubric"):
        rubric = load_rubric()
        send_message(chat_id, json.dumps(rubric, ensure_ascii=False, indent=2)[:3800])
        return


    if text.startswith("/provider"):
        raw = text[len("/provider"):].strip()

        if not raw:
            current = get_chat_provider(chat_id)
            send_message(
                chat_id,
                "현재 채점 LLM Provider: " + provider_label(current) + "\n\n"
                "사용 가능한 명령:\n"
                "/provider auto   - Gemini 우선, 실패 시 Clova fallback\n"
                "/provider gemini - Gemini만 사용\n"
                "/provider clova  - Clova만 사용\n"
                "/provider reset  - 기본값으로 초기화"
            )
            return

        value = raw.split()[0].strip().lower()

        if value in ("reset", "default"):
            current = reset_chat_provider(chat_id)
            send_message(
                chat_id,
                "LLM Provider 설정을 기본값으로 초기화했습니다.\n"
                "현재 Provider: " + provider_label(current)
            )
            return

        try:
            current = set_chat_provider(chat_id, value)
        except Exception:
            send_message(
                chat_id,
                "지원하지 않는 Provider입니다.\n"
                "사용 가능: auto, gemini, clova\n\n"
                "예:\n"
                "/provider auto\n"
                "/provider gemini\n"
                "/provider clova"
            )
            return

        send_message(
            chat_id,
            "LLM Provider를 변경했습니다.\n"
            "현재 Provider: " + provider_label(current)
        )
        return

    if text.startswith("/grade"):
        raw = text[len("/grade"):].strip()
        if not raw:
            send_message(chat_id, "사용법:\n/grade\n문제: ...\n배점: 25\n답안:\nGoogle OCR 텍스트...")
            return

        send_message(chat_id, f"채점을 시작합니다.\n채점 엔진: Gemini semantic grader + Python scoring rules\n보조 모델: {OLLAMA_MODEL}")
        sid, raw_result, parsed = grade_answer(chat_id, raw, state)
        send_message(chat_id, format_result(parsed, raw_result))
        send_message(chat_id, f"저장 위치: /workspace/prof_eng_answer/data/sessions/{sid}")
        return

    send_message(chat_id, "알 수 없는 명령입니다. /help 를 입력하세요.")


def handle_message(message, state):
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    if chat_id is None:
        return

    if not chat_allowed(chat_id):
        send_message(chat_id, "허용되지 않은 chat_id입니다.")
        return

    if "text" in message:
        handle_text(message, chat_id, state)
        return

    if "photo" in message or "document" in message:
        saved = save_incoming_image(message, chat_id, state)
        if saved:
            sid, dest, count = saved
            send_message(chat_id, f"파일 저장 완료: {dest.name}\n세션: {sid}\n현재 이미지 수: {count}")
        return


def main():
    ensure_dirs()

    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN 또는 TELEGRAM_BOT_TOKEN 환경변수가 없습니다.")

    log(f"bot started. ollama={OLLAMA_URL}, model={OLLAMA_MODEL}")

    state = load_state()

    while True:
        try:
            offset = int(state.get("last_update_id", 0)) + 1
            res = get_updates(offset)

            if not res.get("ok"):
                log(f"getUpdates failed: {res}")
                time.sleep(5)
                continue

            for update in res.get("result", []):
                state["last_update_id"] = update["update_id"]
                save_state(state)

                message = update.get("message")
                if message:
                    handle_message(message, state)

            save_state(state)

        except KeyboardInterrupt:
            log("bot stopped")
            break
        except Exception as e:
            log(f"ERROR: {repr(e)}")
            time.sleep(5)


if __name__ == "__main__":
    main()
