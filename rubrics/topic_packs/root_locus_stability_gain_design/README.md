# 근궤적법에 의한 안정도 해석과 제어기 이득 설계

## Topic 계약

- Topic ID: `root_locus_stability_gain_design`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: LLM-only semantic verification
- deterministic check: disabled
- candidate rules: empty
- Fact Anchor: 14개
- fatal wrong claim: 8개
- 예상 문항: 5개 (각 문항 intent/example 및 평가범위 개별 정의)
- 필수 Anchor 추적: 14/14 pattern union, 14/14 answer-outline union

## 대표 문제

> 근궤적법의 원리와 작성 규칙을 설명하고, 이득 변화에 따른 폐루프 안정성과 제어기 이득 설계 방법을 설명하시오.

## 핵심 원리

- 폐루프 특성방정식: `1+KG(s)H(s)=0`
- 각도조건: `∠G(s)H(s)=(2q+1)180°`
- 크기조건: `K|G(s)H(s)|=1`
- 설계 이득: `K=1/|G(s)H(s)|`

근궤적은 개루프 극점 자체의 이동이 아니라 이득 변화에 따른 폐루프 극점의 이동이다.

## 필수 작도 규칙

- 가지는 개루프 극점에서 시작한다.
- 유한 개루프 영점 또는 무한대 영점으로 끝난다.
- 오른쪽 실수 극점과 영점 총수가 홀수인 실수축 구간만 근궤적이다.
- 점근선 수는 `n-m`이다.
- 점근선 각도는 `θ_a=(2q+1)180°/(n-m)`이다.
- 점근선 중심은 `σ_a=(Σp_i-Σz_i)/(n-m)`이다.
- 이탈점 후보는 `dK(s)/ds=0`으로 구한 후 유효성을 확인한다.
- 허수축 교차점은 안정 경계다.

## 과도응답 설계

- `s=-ζω_n±jω_n√(1-ζ²)`
- `T_s≈4/(ζω_n)`
- `M_p=e^[-πζ/√(1-ζ²)]`
- `ω_d=ω_n√(1-ζ²)`

목표점이 기존 근궤적 위에 없으면 lead, lag, lead-lag 또는 PID 보상기를 적용한다.

## 현장 적용

모델 오차, 시간지연, 운전점 변화, actuator 포화, deadband, 센서 노이즈와 디지털 샘플링을 검토한다.

이 디렉터리는 generated Rubric Bank의 source of truth다.

## 패턴·라우팅 경계 메모

문항별 채점 조건은 원리·작도(P1), 안정 이득 범위(P2), 작도량 계산(P3), 과도응답 설계(P4), 보상기 적용(P5)로 구분한다. 각 문항이 직접 요구하지 않는 다른 패턴 계산은 누락 감점의 보편 요건으로 적용하지 않는다. `lead compensator`와 `lag compensator` alias는 Lead-lag owner와의 교차 충돌이 있으나 기존 routing authority를 변경하지 않고 owner audit 대상으로 남긴다.
