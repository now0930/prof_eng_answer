# Logic Check JSON Profile 운영 README

이 문서는 산업계측제어기술사 답안 채점기에서 **표, 도면, 수식, 비교 구조**를 어떻게 `Model Answer`, `Fact Anchor`, `Logic Check`에 반영할지 정의한다.

현재 채점기는 다음 원칙으로 운영한다.

```text
Model Answer = 고득점 답안의 구조와 서술 방향
Fact Anchor  = 정답 요소 coverage 평가
Logic Check  = 핵심 이론 오류, 반대 주장, fatal cap 판단
```

Logic Check는 주제별 이론을 Python 코드에 하드코딩하지 않고, 다음 JSON 문서로 관리한다.

```text
rubrics/logic_check_profiles/industrial_instrumentation_control.json
```

---

## 1. 기본 원칙

### 1.1 세 자료의 역할 분리

| 구분 | 목적 | 넣어야 할 내용 | 넣지 말아야 할 내용 |
|---|---|---|---|
| Model Answer | 수험생이 따라 쓸 고득점 답안 구조 | 정답 표, 정답 도면, 실무 판단, 결론 | 오답 패턴 중심의 경고문 |
| Fact Anchor | 정답 요소가 포함되었는지 coverage 평가 | 핵심 용어, 수식, 비교축, 실무 연결 요소 | fatal 조건, 오답 문장 |
| Logic Check Profile | 정답과 직접 충돌하는 핵심 이론 오류 검출 | fatal 조건, safe 조건, candidate 추출 규칙 | 모든 정답 내용을 장황하게 반복 |

같은 표와 도면이라도 목적에 따라 다르게 반영한다.

```text
모범답안은 정답을 가르친다.
Fact Anchor는 정답 요소가 있는지 본다.
Logic Check는 정답과 직접 충돌하는 오답을 잡는다.
```

---

## 2. 표를 어떻게 해석할 것인가

답안의 표는 단순 문자열이 아니라 **열 제목과 행 값을 연결한 주장 묶음**으로 해석한다.

예를 들어 다음 표가 있다고 하자.

```text
+-----------+-------------------+-------------------+-------------------+
|   구분    |    Under damp     |   Critical damp   |     over damp     |
+-----------+-------------------+-------------------+-------------------+
|   zeta    |      ζ < 0.7      |       ζ = 0.7     |    0.7 ≤ ζ < 1    |
+-----------+-------------------+-------------------+-------------------+
|   Step    |     완만 응답      |       진동        |     overshot      |
+-----------+-------------------+-------------------+-------------------+
|   장점    |    정확한 제어    |       진동        |     빠른 제어     |
+-----------+-------------------+-------------------+-------------------+
|   단점    |     늦은 속도     |       있음        |     충돌 위험     |
+-----------+-------------------+-------------------+-------------------+
```

채점기는 이 표를 다음 claim으로 해석해야 한다.

```text
Under damp    => ζ < 0.7
Critical damp => ζ = 0.7
Over damp     => 0.7 <= ζ < 1

Critical damp => 진동 있음
Over damp     => overshoot / 빠른 제어 / 충돌 위험
```

이는 단순 누락이 아니라 표준 정의와 직접 충돌하는 핵심 이론 오류다.

---

## 3. 표를 Model Answer에 반영하는 방법

Model Answer에는 잘못된 표를 넣지 않는다. 반드시 **정답 비교표**로 반영한다.

예시:

| 구분 | 무감쇠 | 부족감쇠 | 임계감쇠 | 과감쇠 | 불안정 |
|---|---|---|---|---|---|
| 감쇠비 ζ | ζ=0 | 0<ζ<1 | ζ=1 | ζ>1 | ζ<0 또는 RHP 극점 |
| 극점 | ±jωn | -σ±jωd | -ωn 중근 | 서로 다른 음의 실근 | 우반평면 극점 |
| 오버슈트 | 지속 진동 | 존재 | 없음 | 없음 | 발산 |
| 정착시간 | 정착 안 됨 | Ts≈4/(ζωn) | 오버슈트 없는 최속 수렴 | 느린 수렴 | 정착 안 됨 |
| Step 응답 | 영구 진동 | 감쇠진동 수렴 | 무진동 최속 수렴 | 무진동 지연 수렴 | 발산 |
| 현장 판단 | 사용 부적합 | 속응성 요구 시 사용 | 오버슈트 금지 공정 | 안정성 우선 공정 | 설계 불가 |

Model Answer에는 다음 설명을 함께 넣는다.

```text
ζ≈0.707은 부족감쇠 영역 안에서 속도와 안정성의 실무적 타협점으로 사용할 수 있으나, 임계감쇠의 정의는 아니다. 임계감쇠는 ζ=1이며, 과감쇠는 ζ>1이다.
```

---

## 4. 표를 Fact Anchor에 반영하는 방법

Fact Anchor에는 오답 패턴이 아니라 정답 요소를 넣는다.

예시:

```json
{
  "id": "second_order_damping_regions",
  "core_terms": [
    "ζ=0 무감쇠",
    "0<ζ<1 부족감쇠",
    "ζ=1 임계감쇠",
    "ζ>1 과감쇠",
    "오버슈트",
    "정착시간",
    "좌반면 극점"
  ],
  "expected_points": [
    "감쇠비 ζ에 따라 무감쇠, 부족감쇠, 임계감쇠, 과감쇠로 구분한다.",
    "부족감쇠는 0<ζ<1이며 오버슈트와 감쇠진동을 동반하되 안정 수렴한다.",
    "임계감쇠는 ζ=1이며 오버슈트 없이 가장 빠르게 수렴한다.",
    "과감쇠는 ζ>1이며 오버슈트는 없지만 응답이 느리다."
  ]
}
```

Fact Anchor는 다음 질문에 답해야 한다.

```text
학생이 정답 요소를 충분히 썼는가?
```

다음 질문은 Logic Check가 담당한다.

```text
학생이 정답과 반대되는 주장을 했는가?
```

---

## 5. 표를 Logic Check Profile에 반영하는 방법

Logic Check Profile에는 표의 오답 claim을 fatal 조건으로 넣는다.

예시:

```json
{
  "fatal_conditions": [
    "명시적으로 부족감쇠를 ζ<0.7로 제한하면 fatal이다.",
    "명시적으로 임계감쇠를 ζ=0.7 또는 ζ=0.707로 정의하면 fatal이다.",
    "명시적으로 과감쇠를 0.7≤ζ<1로 정의하면 fatal이다.",
    "임계감쇠를 진동 또는 오버슈트 응답으로 설명하면 fatal이다.",
    "과감쇠를 오버슈트, 빠른 제어, 충돌 위험 응답으로 설명하면 fatal이다."
  ],
  "safe_conditions": [
    "ζ≈0.707 언급 자체는 fatal이 아니다.",
    "ζ≈0.707을 부족감쇠 영역의 실무적 튜닝점, 최적 타협점, 45도 극점으로 설명하면 정상이다.",
    "ζ=1 임계감쇠와 ζ≈0.707 실무 타협점을 명확히 구분하면 fatal이 아니다."
  ]
}
```

candidate extractor는 표 전체를 완벽히 파싱하려 하지 않는다. 대신 핵심 후보만 만든다.

```json
{
  "kind": "structured_damping_region_table",
  "text": "Under damp => ζ < 0.7 | Critical damp => ζ = 0.7 | Over damp => 0.7 <= ζ < 1"
}
```

LLM verifier는 이 candidate를 보고 정답 스키마와 직접 충돌하는지 판단한다.

---

## 6. 도면을 어떻게 해석할 것인가

S-평면 도면은 고득점 요소가 될 수 있지만, 각도 기준과 삼각함수 관계를 잘못 쓰면 핵심 이론 오류가 된다.

예시 도면:

```text
             ^ Im
             |
    * . . . .|  ωd
     \       |
      \      |
       \ θ   |
        \    |
----+--------+-------------> Re
   -σ        O
```

정답 관계는 다음과 같다.

```text
s = -σ ± jωd
σ = ζωn
ωd = ωn√(1-ζ²)
ωn = √(σ² + ωd²)
```

θ를 **음의 실수축과 극점 벡터가 이루는 각도**로 정의하면 다음이 성립한다.

```text
cosθ = σ/ωn = ζ
sinθ = ωd/ωn = √(1-ζ²)
```

따라서 이 기준에서는 다음이 정답이다.

```text
ζ = cosθ
```

반대로 θ를 **허수축 기준 각도**로 정의한 경우에는 `ζ=sinθ` 표현이 가능하다. 따라서 Logic Check는 `sinθ` 자체를 무조건 fatal로 보면 안 되고, **각도 기준축과 함께 판단**해야 한다.

---

## 7. 도면을 Model Answer에 반영하는 방법

Model Answer에는 도면과 함께 기준축을 명확히 써야 한다.

예시 문장:

```text
S-평면에서 부족감쇠 영역의 극점은 s=-σ±jωd로 표현되며, σ는 감쇠 속도, ωd는 감쇠진동수를 의미한다. 원점에서 극점까지의 거리는 고유진동수 ωn이고, θ를 음의 실수축과 극점 벡터가 이루는 각도로 정의하면 cosθ=σ/ωn=ζ, sinθ=ωd/ωn=√(1-ζ²)가 된다. 따라서 ζ가 클수록 극점은 음의 실수축에 가까워져 진동성과 오버슈트가 감소하고, ζ가 작을수록 허수축에 가까워져 진동성이 커진다. θ=45°인 경우는 ζ=cos45°≈0.707로, 부족감쇠 영역 내의 실무적 속도·안정성 타협점으로 볼 수 있으나 임계감쇠는 아니다.
```

Model Answer에는 다음 표를 함께 넣을 수 있다.

| 항목 | 관계 |
|---|---|
| 극점 | s=-σ±jωd |
| 감쇠율 | σ=ζωn |
| 감쇠진동수 | ωd=ωn√(1-ζ²) |
| 고유진동수 | ωn=√(σ²+ωd²) |
| 음의 실수축 기준 각도 θ | ζ=cosθ |
| θ=45° 특수점 | ζ≈0.707, 부족감쇠 영역의 실무적 타협점 |

---

## 8. 도면을 Fact Anchor에 반영하는 방법

Fact Anchor에는 도면 자체보다 관계식을 넣는다.

예시:

```json
{
  "id": "second_order_s_plane_geometry",
  "core_terms": [
    "S-평면",
    "s=-σ±jωd",
    "σ=ζωn",
    "ωd=ωn√(1-ζ²)",
    "ωn=√(σ²+ωd²)",
    "ζ=cosθ"
  ],
  "expected_points": [
    "부족감쇠 극점은 S-평면 좌반면 복소근 s=-σ±jωd로 표현된다.",
    "σ는 감쇠율로 σ=ζωn이며 응답 엔벨로프 감쇠 속도를 결정한다.",
    "ωd는 감쇠진동수로 ωd=ωn√(1-ζ²)이다.",
    "θ를 음의 실수축 기준 각도로 정의하면 ζ=cosθ이다.",
    "θ=45°는 ζ≈0.707인 특수한 부족감쇠 튜닝점이지 임계감쇠 정의가 아니다."
  ]
}
```

---

## 9. 도면을 Logic Check Profile에 반영하는 방법

Logic Check에는 각도 기준과 sin/cos 관계 충돌을 넣는다.

예시:

```json
{
  "truth_schema": [
    "부족감쇠 극점은 s=-σ±jωd로 표현된다.",
    "σ=ζωn이다.",
    "ωd=ωn√(1-ζ²)이다.",
    "ωn=√(σ²+ωd²)이다.",
    "θ를 음의 실수축 기준으로 정의하면 ζ=cosθ이다.",
    "θ를 허수축 기준으로 정의하면 ζ=sinθ로 표현할 수 있다.",
    "θ=45°는 ζ≈0.707인 특수한 부족감쇠 튜닝점이지 임계감쇠 정의가 아니다."
  ],
  "fatal_conditions": [
    "θ를 음의 실수축 기준으로 정의하고 sinθ=σ/ωn=ζ라고 쓰면 fatal이다.",
    "음의 실수축 기준 θ에서 ζ=sinθ라고 주장하면 fatal이다.",
    "θ=45° 또는 ζ≈0.707을 임계감쇠 정의로 사용하면 fatal이다."
  ],
  "safe_conditions": [
    "θ=45°를 ζ≈0.707의 특수 사례로 설명하는 것은 정상이다.",
    "θ=45°를 부족감쇠 영역의 실무적 타협점으로 설명하면 정상이다.",
    "θ를 음의 실수축 기준으로 정의하고 ζ=cosθ라고 설명하면 정상이다.",
    "θ를 허수축 기준으로 정의한 경우 ζ=sinθ라고 설명할 수 있다."
  ]
}
```

candidate extractor에는 다음 rule을 둘 수 있다.

```json
{
  "kind": "angle_relation_context",
  "type": "nearby_regex",
  "regex": "(S-?평면|s\\s*=\\s*-?σ|ωd|ωn|θ|45°|45\\^?\\\\circ|sin|cos|실수축|허수축|real\\s*axis|imaginary\\s*axis)"
}
```

---

## 10. Logic Check JSON Profile 작성 규칙

Logic Check Profile은 다음 파일에 둔다.

```text
rubrics/logic_check_profiles/industrial_instrumentation_control.json
```

profile 하나는 다음 구조를 가진다.

```json
{
  "topic_id": "second_order_lag_response_by_damping_ratio",
  "display_name": "2차 표준형 시스템 감쇠비별 응답 특성",
  "difficulty": "THEORY_CORE",
  "cap_policy": {
    "fatal_recommended_ceiling": 10.0,
    "fatal_confidence_threshold": 0.75
  },
  "candidate_extraction": {
    "max_candidates": 12,
    "nearby_window": 1,
    "rules": []
  },
  "truth_schema": [],
  "fatal_conditions": [],
  "safe_conditions": []
}
```

작성 원칙:

```text
truth_schema:
- 정답 기준을 쓴다.
- 모범답안 전체를 복사하지 않는다.

fatal_conditions:
- 정답과 직접 충돌하는 주장만 쓴다.
- 단순 누락, 설명 부족, 표현 애매함은 fatal로 쓰지 않는다.

safe_conditions:
- 오탐 방지 기준을 쓴다.
- 특히 ζ≈0.707처럼 좋은 답안과 나쁜 답안 양쪽에 등장하는 표현은 safe 조건을 반드시 둔다.

candidate_extraction:
- 모든 문장을 파싱하려 하지 않는다.
- LLM verifier가 판단할 핵심 evidence 후보만 뽑는다.
```

---

## 11. 평가 흐름

현재 Logic Check 흐름은 다음과 같다.

```text
1. grading_agents.py
   - 기본 Gemini semantic grading 수행

2. logic_check_evaluator.py
   - 대상 topic_id 확인
   - THEORY_CORE 여부 확인
   - logic_llm_verifier 호출

3. logic_llm_verifier.py
   - JSON profile 로드
   - candidate evidence 추출
   - LLM verifier prompt 생성
   - LLM 결과 JSON 파싱
   - confidence guardrail 적용
   - fatal finding이면 recommended_ceiling=10

4. difficulty_score_ceiling.py
   - logic_check_evaluation.fatal_error_detected 확인
   - THEORY_CORE fatal이면 최종 점수 cap 적용

5. bot.py
   - Logic Check 결과를 사용자에게 표시
   - fatal이면 ceiling 전 점수와 최종 점수를 구분해 출력
```

---

## 12. 표와 도면 반영 체크리스트

새로운 표나 도면을 반영할 때는 아래 순서로 처리한다.

```text
1. 이 표/도면이 정답 구조인가, 오답 패턴인가 구분한다.
2. 정답 구조이면 Model Answer에 반영한다.
3. 핵심 용어와 관계식은 Fact Anchor에 반영한다.
4. 정답과 직접 충돌하는 패턴은 Logic Check fatal_conditions에 넣는다.
5. 오탐 가능성이 있는 표현은 safe_conditions에 넣는다.
6. candidate_extraction에는 LLM이 판단할 최소 evidence만 뽑도록 rule을 넣는다.
7. 좋은 답안과 나쁜 답안 regression test를 각각 만든다.
```

---

## 13. 2차 감쇠비 문항의 대표 regression case

### 좋은 답안

```text
ζ=0은 무감쇠, 0<ζ<1은 부족감쇠, ζ=1은 임계감쇠, ζ>1은 과감쇠이다.
ζ=0.707은 극점이 실수축과 θ=45도를 이룰 때이며 cos45≈0.707이다.
이는 진동을 허용하는 부족감쇠 영역 내의 실무적 최적 타협점이다.
```

기대:

```text
mode=pass 또는 warn
fatal=false
recommended_ceiling=null
```

### 나쁜 답안

```text
Under damp => ζ < 0.7
Critical damp => ζ = 0.7
Over damp => 0.7 <= ζ < 1
```

기대:

```text
mode=fatal
fatal=true
recommended_ceiling=10.0
```

### 나쁜 S-평면 답안

```text
θ는 음의 실수축과 극점이 이루는 각도이며 sinθ=σ/ωn=ζ이다.
```

기대:

```text
mode=fatal
fatal=true
recommended_ceiling=10.0
```

---

## 14. 테스트 명령

```bash
python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_score_ceiling.py \
  logic_check_evaluator.py \
  logic_llm_verifier.py

python3 -m json.tool rubrics/logic_check_profiles/industrial_instrumentation_control.json >/tmp/logic_profile_check.json

python3 scripts/validate_logic_check_bank.py
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
```

좋은 답안/나쁜 답안 단독 검증:

```bash
OLLAMA_URL=http://localhost:11434 python3 - <<'PY'
import json
from logic_llm_verifier import verify_second_order_logic_with_llm

cases = {
    "good": r"""
ζ=0은 무감쇠, 0<ζ<1은 부족감쇠, ζ=1은 임계감쇠, ζ>1은 과감쇠이다.
ζ=0.707은 극점이 실수축과 θ=45도를 이룰 때이며 cos45≈0.707이다.
이는 진동을 허용하는 부족감쇠 영역 내의 실무적 최적 타협점이다.
""",
    "bad_table": r"""
구분 Under damp Critical damp over damp
zeta ζ < 0.7 ζ = 0.7 0.7 ≤ ζ < 1
""",
    "bad_angle": r"""
S-평면상 사이각 θ는 음의 실수축과 극점이 이루는 각도이며 sinθ = σ/ωn = ζ
"""
}

for name, answer in cases.items():
    r = verify_second_order_logic_with_llm(answer)
    print("==", name, "==")
    print(json.dumps({
        "mode": r["mode"],
        "fatal": r["fatal_error_detected"],
        "recommended_ceiling": r["recommended_ceiling"],
        "findings": [(x.get("severity"), x.get("message")) for x in r["findings"]]
    }, ensure_ascii=False, indent=2))
PY
```

---

## 15. 운영 원칙

Logic Check를 추가할 때는 다음 원칙을 지킨다.

```text
1. 주제 지식은 Python 코드에 하드코딩하지 않는다.
2. 주제 지식은 JSON profile에 둔다.
3. Python은 JSON profile을 읽고 candidate evidence만 추출한다.
4. LLM은 candidate evidence와 truth_schema를 비교한다.
5. fatal은 정답과 직접 충돌할 때만 적용한다.
6. LLM 실패 또는 confidence 부족 시 fatal을 적용하지 않는다.
7. 좋은 답안에 자주 나오는 표현은 반드시 safe_conditions에 등록한다.
8. 표와 도면은 문자열이 아니라 claim 구조로 해석한다.
9. 단순 누락은 major/minor, 핵심 반대 주장은 fatal이다.
10. THEORY_CORE fatal은 최종 점수 cap을 적용한다.
```

---

## 16. 현재 2차 감쇠비 문항 정리

현재 문항에서 가장 중요한 구분은 다음이다.

```text
정답:
ζ=0       → 무감쇠
0<ζ<1     → 부족감쇠
ζ=1       → 임계감쇠
ζ>1       → 과감쇠
ζ≈0.707   → 부족감쇠 영역의 실무적 타협점

fatal:
ζ<0.7       → 부족감쇠라고 제한
ζ=0.7       → 임계감쇠라고 정의
0.7≤ζ<1     → 과감쇠라고 정의
음의 실수축 기준 θ에서 sinθ=ζ라고 주장
ζ≈0.707을 임계감쇠 정의로 사용
```

이 원칙을 유지하면, 좋은 답안의 `ζ=0.707`은 살리고, 잘못된 표와 도면은 정확히 fatal 처리할 수 있다.
