# 근거 보강 후속 검토: 5개 Anchor (2026-10-08)

이 문서는 GitHub `main` 기준 감사에서 근거 보강 대상으로 남았던 다섯 Anchor의 후속 사실 대조와 source JSON 수정 내용을 기록한다. 각 Anchor의 기존 출처는 주장 전체를 뒷받침하지 못하거나, 조건부인 모델 선택을 보편 규칙처럼 표현하고 있었다. 수정은 source Topic Pack JSON에 반영했으며 generated bank는 release rebuild 단계에서만 갱신한다.

## 판정 요약

| Topic Pack / Anchor | 판정 | 보강·수정 내용 | 남긴 경계 |
| --- | --- | --- | --- |
| `sil_target_determination_risk_reduction_and_lifecycle` / `method_selection` | 보강·정정 | HSE 자료에 근거해 LOPA를 시나리오별 반정량 분석으로, risk graph를 더 단순한 방법으로 설명했다. 해당 HSE 자료의 범위에서는 risk graph가 screening 또는 독립 평가로 쓰일 수 있다. QRA는 정량 위험평가 대안으로 언급하고, 방법 선택을 지침·시나리오 복잡도·자료 품질에 종속시켰다. | calibrated risk graph/safety-layer matrix에 대해 보편적으로 적용되는 분류·보정 규칙은 확인하지 못해 단정 문구를 제거했다. HSE 예시를 모든 업종에 일반화하지 않는다. |
| 같은 Topic / `cyber_ai_safety_boundary` | 보강·경계 명확화 | OT 보안은 safety·reliability 제약을 고려해야 하고, 사이버 위협의 SIS/SIF 영향은 기능안전 검토와 연계한다는 내용을 HSE/NIST 근거와 연결했다. | AI 생성 코드 사용 시 추적성·형상관리·독립 검토/시험·배포 승인은 안전한 적용 권고로 적었다. 이를 IEC 61511의 AI 전용 직접 요구라고 표현하지 않았다. |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_markov_state_transition` | 정정 | Markov 모델의 일반 요소를 상태와 전이확률/전이율로 표현하고, 상태 집합은 모델 경계·목적에 따라 정한다고 수정했다. 시간불변/시간변화 전이율 모두 가능하다고 제한했다. | 운전·고장·검출·수리·proof-test·bypass·degraded 상태는 SIS 모델에서 필요할 때 선택하는 예시이며 모든 모델의 고정 목록이 아니다. |
| 같은 Topic / `fsrm_model_assumption_documentation` | 적용조건 보강 | 결과를 재현할 수 있도록 모델 경계·수요모드와 실제 적용한 자료·가정을 기록하도록 수정했다. 고장자료/환경, 진단·시험·수리, CCF, bypass/override, 근사와 제외조건은 해당 모델에 관련될 때 기록한다. | 모델에 적용되지 않은 항목은 무조건 계산요소로 요구하지 않고 미모델링/제외를 밝혀 범위를 설명한다. |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_exercise_metrics` | 정정 | CISA exercise 자료의 역할·기획·피드백·사후 개선계획 및 NIST incident response의 탐지·대응·복구 개선을 근거로 훈련 목적을 정리했다. | MTTD·containment time·복구지표는 조직이 선택할 수 있는 지표로 한정했다. 시작 이벤트, 종료/containment 기준, 시간기록 출처와 모집단을 사전 정의해야 비교 가능하며, 보편적인 MTTC 시작점을 가정하지 않는다. |

## 근거 자료

- HSE, [Functional Safety Inspection Guide](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf): LOPA의 반정량 성격, scenario frequency, IPL 및 허용빈도 관련 설명.
- HSE, [Inspection of Loss of Containment](https://www.hse.gov.uk/offshore/assets/docs/inspection-of-loss-of-containment.pdf): risk graph와 LOPA의 방법 비교 및 해당 산업 문맥에서의 사용 범위.
- HSE, [LOPA: Practical Application and Pitfalls](https://training.hse.gov.uk/courses/lopa-practical-application-and-pitfalls): LOPA 적용 범위·복잡도와 QRA 대안을 함께 고려하는 교육 지침.
- HSE, [Functional Safety](https://www.hse.gov.uk/eci/functional.htm) 및 [Cyber Security](https://www.hse.gov.uk/eci/cyber-security.htm): 기능안전 관리와 주요위험 설비의 산업제어/안전시스템 사이버보안 문맥.
- NIST, [SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): OT 보안이 성능·신뢰성·안전 요구를 고려해야 한다는 범위.
- NIST, [Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf): secure development practices 및 generative-AI profile 안내. 본 보고서는 이를 IEC 기능안전 요구로 대체하거나 등치하지 않는다.
- NASA, [Reliability Modeling Method, CR-188288](https://ntrs.nasa.gov/api/citations/19940028356/downloads/19940028356.pdf), §2.4: discrete-state Markov reliability model, 상태의 구성, state-dependent/time-varying transition rate 선택 및 모델 가정 사례.
- NASA NTRS, [A non-homogeneous Markov model for phased-mission reliability analysis](https://ntrs.nasa.gov/citations/19900039580): 일반적 제약과 시간·상태 의존 전이 모델 확장의 구분.
- HSE, [SIS Proof Testing Requirements](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf) 및 [Implementing SIS Proof Testing](https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf): 진단 coverage, proof-test interval, 관측 고장자료, 수리/시험 가정과 설계 가정 대비 모니터링.
- CISA, [Cybersecurity Tabletop Exercise Package](https://www.cisa.gov/resources-tools/resources/ctep-package-documents): 훈련 역할, planner/facilitator 자료, 피드백과 AAR/improvement-plan 도구.
- NIST, [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final): incident 대응 활동을 준비하고 탐지·대응·복구의 효과를 개선하는 위험관리 지침.
- NIST CSRC, [Mean Time to Detect glossary](https://csrc.nist.gov/glossary/term/mean_time_to_detect): MTTD 용어 설명. MTTC의 시작점/종료점을 표준화하는 근거로 사용하지 않았다.

## 검증 경계

이 작업은 다섯 Anchor의 기술 주장·허용 표현·source basis를 보강한 것이다. 산업별 규정 준수, 특정 SIF의 SIL 달성, 위험그래프 보정값, MTTC의 보편 정의 또는 안전 관련 AI 코드의 인증을 보증하지 않는다. Source JSON 수정과 별도로 generated bank rebuild 및 전체 release gate를 통과해야 integration 준비가 완료된다.
