# Stage49 FSRM 위험 기반 Golden 검토 기록

- 검토 범위: PFDavg/PFH demand mode 선택, quantity dimension, 직접 비교 오류
- 근거: 기존 승인 Topic Pack의 machine contract와 global quantity/dimension ontology
- 구성: 정상 1건, 부분 1건, fatal mutation 1건
- 금지: 특정 운영 답안 전체 문자열 탐지, LLM verdict, Topic별 점수 hardcoding
- 판정: owner가 위임한 기존 Golden review 절차에 따라 세 사례를 reviewed로 편입

정상 사례는 저수요-PFDavg와 고수요·연속수요-PFH 관계 및 차원을 모두 설명한다.
부분 사례는 저수요-PFDavg만 설명하고 PFH 요구축을 명시적으로 누락한다. Fatal 사례는
demand mode를 서로 바꾸고 rate와 dimensionless probability를 직접 대소 비교한다.
