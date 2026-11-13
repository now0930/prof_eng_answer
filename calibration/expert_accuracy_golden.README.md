# Expert Accuracy Golden Set

> **사람용 핵심:** Golden Set은 전문가 정확도·오답 안전성 점검을 위한 표본이며, 현재 배포 필수 정확도 Gate가 아닙니다. AI reviewer는 사람 검토로 표기하지 않습니다.
>
> **AI·개발자:** [코드·권한 참조](../docs/ai_implementation_reference.md). 변경 전 최신 정책과 실제 코드 경로를 확인하세요.


- `draft`는 개발용이며 공식 정확도에서 제외한다.
- 전문가 검토 후 `reviewed`, 근거를 기록한 조정 완료 후 `adjudicated`로 표시한다.
- AI가 source-grounded adjudication을 수행한 경우 reviewer에 AI임을 명시하고 조정 근거를 별도 기록한다. 이를 인간 전문가 검토로 표기하지 않는다.
- Golden label과 모델 prediction은 분리한다.
- 실행: `python scripts/measure_expert_accuracy.py --predictions predictions.jsonl`
- 개발 중 draft 포함: `--include-draft`
- CI에서 평가 건수를 강제하려면 `--require-cases`를 사용한다.
- 선택적 정확도 감사 기준: `docs/accuracy_release_gate.md` (배포 필수 아님)
- 현재 48건은 모두 `reviewed`이며 31개 주제와 4개 Question Type을 포함한다.
- `python3 scripts/audit_golden_risk_coverage.py`로 Topic별 normal/adverse/fatal
  lane 공백을 위험도 순으로 확인한다.
- 정확도·오류 재현율·점수 MAE 기준 미달 시 **해당 선택적 감사**는 `HOLD`다. 현재 배포용 코드는 전체 오프라인 pytest로 검증한다.
