# 문제 요구사항의 비활성 compiler

`grading/routing/fact_question_compiler.py`는 문제 원문과 승인 Fact snapshot,
원문 span이 검증된 `question_requirement` 후보만 읽는다. 답안은 입력으로 받지 않으므로
답안 표현이나 점수를 보고 문제 요구를 변경할 수 없다. 출력은 Stage 1의
`question_contract`이며 채점기에는 아직 연결되지 않는다.

현재는 개념·적용 조건이 정확히 맞는 승인 Fact가 유일하고, 사전에 제공한 승인
개념 별칭이 문제 원문에 나타나며, 규칙 parser가 만든 `define` 또는 `explain`
행위일 때만 `resolved`다. 별칭 사전이 없거나 의미 해석기 후보이면 보류한다.
승인 Fact가 없으면 `knowledge_gap`, 여러
Fact가 맞거나 비교·계산·설계·평가·적용 행위이면 `ambiguous`로 보류한다. 이는
미등록 질문을 억지로 기존 모범답안에 맞추지 않기 위한 보수적 초기 규칙이다.
`ambiguous`가 곧 수험생 오답이라는 뜻은 아니다.

완료되지 않은 부분: 행위별 세부 축(비교 대상 쌍, 계산 입력·단위, 설계 제약),
복합 Topic의 fact group·허용 대안, 승인 Fact가 실제로 채워진 대표 3개 Topic의
독립 질문 평가. 이 부분이 검증되기 전에는 운영 점수에 사용하지 않는다.

합성 fixture 검증: `python3 -m pytest -q tests/test_fact_question_compiler.py`.
