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

## topic_id

```text
second_order_lag_response_by_damping_ratio
```
