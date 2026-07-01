#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
OUT_CSV = ROOT / "reports/fact_anchor_final_support_resolution_applied.csv"

# old_term -> new noun phrase
RESOLUTIONS = {
    "정상·최소·최대 유량에서 밸브 개도 범위를 검토해야 함":
        "정상·최소·최대 유량별 밸브 개도 범위 검토",

    "평가 대상과 baseline 조건을 명확히 설정한다":
        "평가 대상·baseline 조건 설정",

    "교정 결과는 설비 신뢰성, 품질 감사, 계측기 이력 관리와 연결된다":
        "교정 결과와 설비 신뢰성·품질 감사·이력 관리",

    "상승·하강 교정으로 선형성, 반복성, 히스테리시스 확인고 쓴다":
        "상승·하강 교정과 선형성·반복성·히스테리시스 확인",

    "인버터 일반론으로 확장하지 않고 전원 인덕턴스가 있는 정류기 현상으로 한정한다":
        "전원 인덕턴스가 있는 정류기 현상 한정",

    "전압 파형만으로 판단하지 말고 입력 전류, 소자 전류, 부하 전류를 함께 측정한다":
        "전압·입력 전류·소자 전류·부하 전류 동시 측정",

    "변압기 누설 인덕턴스, 긴 배선, 큰 부하 전류는 중첩각을 증가시킬 수 있다":
        "변압기 누설 인덕턴스·긴 배선·큰 부하 전류",

    "전원 품질 문제가 있는 경우 전류 왜곡과 정류기 커뮤테이션 현상을 함께 분석한다":
        "전류 왜곡과 정류기 커뮤테이션 현상 동시 분석",

    "전압 파형만 보지 말고 전류 파형을 함께 측정해야 한다는 실무 해석을 포함한다":
        "전압 파형·전류 파형 동시 측정 실무 해석",

    "신뢰도, 정비도, 가용도의 정의를 서로 구분한다":
        "신뢰도·정비도·가용도 정의 구분",

    "방폭, 재질, 접속, 출력 신호, 기존 시스템 호환성까지 포함한다":
        "방폭·재질·접속·출력 신호·시스템 호환성",

    "형상과 삽입 길이를 응답성, 강도, 대표성으로 비교한다":
        "형상·삽입 길이와 응답성·강도·대표성 비교",

    "GWR을 일반 비접촉식 radar와 구분한다":
        "GWR과 일반 비접촉식 radar 구분",

    "거품, 증기, 유전율, 점도, 부식성, 방폭 조건을 선정 기준으로 사용한다":
        "거품·증기·유전율·점도·부식성·방폭 조건",

    "유지보수, 기존 nozzle, wiring, 비용까지 판단한다":
        "유지보수·기존 nozzle·wiring·비용 판단",

    "표준 2차 전달함수를 정확히 쓴다":
        "표준 2차 전달함수",

    "ζ=1 임계감쇠를 공진 조건처럼 오해하지 않는다":
        "ζ=1 임계감쇠와 공진 조건 구분",

    "시간응답 overshoot와 주파수응답 resonance를 명확히 구분한다":
        "시간응답 overshoot와 주파수응답 resonance 구분",

    "SIL을 단순 중요도 등급이 아니라 위험저감 성능으로 해석한다":
        "SIL의 위험저감 성능 해석",

    "직관거리, beta ratio, 유량계수, 보상 조건을 함께 언급한다":
        "직관거리·beta ratio·유량계수·보상 조건",

    "오리피스의 경제성과 압력손실, 유지보수 한계를 균형 있게 쓴다":
        "오리피스 경제성·압력손실·유지보수 한계",

    "프로토콜별 장단점과 적용 위치를 구체적으로 비교한다":
        "프로토콜별 장단점·적용 위치 비교",

    "무선 통신은 별도 적용 조건과 보안·신뢰성 검토가 필요함을 구분한다":
        "무선 통신 적용 조건·보안·신뢰성 검토",

    "실시간성, 결정성, 노이즈, 이중화, 보안을 함께 평가한다":
        "실시간성·결정성·노이즈·이중화·보안 평가",

    "Remote I/O의 배선 절감 장점과 통신 의존 리스크를 함께 쓴다":
        "Remote I/O 배선 절감 장점과 통신 의존 리스크",
}

def load_topics(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ["topics", "fact_anchors", "items", "data"]:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        if "topic_id" in data and "anchors" in data:
            return [data]
    raise SystemExit("ERROR: unsupported fact anchor json structure")

def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    data = json.loads(FACT_PATH.read_text(encoding="utf-8"))
    topics = load_topics(data)

    applied = []

    for topic in topics:
        topic_id = str(topic.get("topic_id", "")).strip()
        anchors = topic.get("anchors", [])
        if not isinstance(anchors, list):
            continue

        for anchor in anchors:
            if not isinstance(anchor, dict):
                continue

            anchor_id = str(anchor.get("id", "")).strip()
            terms = anchor.get("support_terms", [])
            if not isinstance(terms, list):
                continue

            new_terms = []
            seen = set()

            for raw in terms:
                old = str(raw).strip()
                new = RESOLUTIONS.get(old, old)

                if new in seen:
                    applied.append({
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                        "old_term": old,
                        "new_term": new,
                        "action": "dedupe_after_rewrite",
                    })
                    continue

                seen.add(new)
                new_terms.append(new)

                if old != new:
                    applied.append({
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                        "old_term": old,
                        "new_term": new,
                        "action": "rewrite",
                    })

            anchor["support_terms"] = new_terms

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["topic_id", "anchor_id", "old_term", "new_term", "action"],
        )
        writer.writeheader()
        writer.writerows(applied)

    print("resolution patterns:", len(RESOLUTIONS))
    print("applied:", len(applied))
    print("wrote:", OUT_CSV)

    for r in applied[:120]:
        print(f"- {r['action']} | {r['topic_id']} / {r['anchor_id']} :: {r['old_term']} -> {r['new_term']}")

    if args.write:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.fact_anchors.before_final_support_resolution.{ts}.json"
        shutil.copy2(FACT_PATH, backup)
        save_json(FACT_PATH, data)
        print("backup:", backup)
        print("written:", FACT_PATH)
    else:
        print("DRY RUN only. Re-run with --write to apply.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
