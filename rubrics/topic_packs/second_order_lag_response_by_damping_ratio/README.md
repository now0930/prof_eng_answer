# second_order_lag_response_by_damping_ratio

## 목적

감쇠비에 따른 2차 지연시스템 응답 특성을 topic 단위로 분리한 첫 번째 topic pack이다.

## 구성

- `fact_anchor.json`: 사실 기반 핵심 anchor
- `model_answer.json`: 모범 답안 구조와 고득점 포인트
- `logic_check.json`: deterministic check와 LLM profile을 함께 관리하는 topic 단위 source
- `topic_importance.json`: 난이도와 시험 전략 정보

## 현재 상태

- 기존 종합 bank를 대체하지 않는다.
- grader에 직접 연결하지 않는다.
- `scripts/validate_topic_packs.py`로 standalone 검증한다.
- 검증 안정화 후 generated bank 또는 기존 bank 통합을 검토한다.

## 문항 범위 경계

5개 예상문항에는 각각 독립 intent/example 및 required Anchor 집합을 둔다. 전체 감쇠 구간(ζ<0, ζ=0 포함)을 요구하는 Pattern 1과 극점-감쇠비 관계를 묻는 Pattern 4에서만 ζ=0·ζ<0 Anchor를 합격 필수(`pass_required`)로 한다. 부족·임계·과대감쇠 비교나 응답지표 영향만 묻는 문항에 해당 내용을 전역 필수로 요구하지 않는다. 고득점·누락 판단도 해당 문항에서 요구한 범위로 제한한다.

## topic_id

```text
second_order_lag_response_by_damping_ratio
```
