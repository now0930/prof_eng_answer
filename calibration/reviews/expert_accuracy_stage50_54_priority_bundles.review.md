# Stage50~54 우선위험 5개 묶음 Golden 검토 기록

- 범위: Nyquist, Lead/Lag, LQR, HIPPS, PLC·DCS·SCADA 대표 핵심 관계
- 구성: Topic별 normal 1건, adverse 1건, fatal mutation 1건(총 15건)
- 근거: 승인 Topic Pack의 fact/fatal 기준과 additive machine contract
- 판정권: canonical evidence와 deterministic contract만 사용하며 LLM verdict 권한은 0
- 검토 방식: 사용자가 5개 묶음을 승인 대기 없이 끝까지 진행하도록 명시적으로 위임

정상 사례는 핵심 관계를 충족하고, adverse 사례는 일부 요구를 의도적으로 누락한다.
fatal 사례는 임계점, 보상기 목적, Q/R 역할, HIPPS/PSV 기능, PLC/DCS 역할을
반전한다. 특정 전체 문장을 탐지하지 않고 subject-predicate-object 관계 충돌로 판정한다.
