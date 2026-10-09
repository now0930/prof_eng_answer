"""Public synthetic reproduction of the compact V-model/HFT regression.

This is not a recovered private session. It models the two explicit wrong table
relations and seven coverage rows required by the original regression assertions.
"""
import copy


def synthetic_session():
    text = '''문제: 제어 소프트웨어의 단위·통합·시스템 시험과 SIL 검증을 설명하시오.
답안: V-model에서 설계와 시험을 대응시키고 추적성을 관리한다.
비교 항목 (비교축)단위 시험통합 시험시스템 시험
검증 대상 / 도구단일 모듈 / xUnit, MISRA인터페이스 / Stub, S/W HIL전체 SIS / HIL 시뮬레이터
SIL 대응 요소Random IntegrityArch. Constraints (HFT 0,1,2)Systematic Integrity
Architectural Constraints: HFT(1oo2, 2oo3) 이중화 검증, HIL 시뮬레이션 기반 검증.
SIL은 Safety Integrity Level이다.
'''
    criteria = ['background_need','classification_axis','structure_features',
                'comparison_axis','pros_cons_limits','application_conditions','selection_judgement']
    rows = [dict(criterion=key, status='present', evidence='개발 절차와 시험을 설명') for key in criteria]
    rows[5]['evidence'] = '통합시험을 HFT에 대응시킴'
    grade = dict(
        topic_id='instrumentation_control_software_lifecycle_v_model_traceability_verification_validation',
        logic_check_topic_id='instrumentation_control_software_lifecycle_v_model_traceability_verification_validation',
        total_score=15.25, final_total_score=15.25, max_score=25,
        question_type='COMPARISON_SELECTION',
        summary='요구사항을 충실히 다루고 구조적으로 잘 서술하였다.',
        overall_comment='요구사항을 충실히 다루고 구조적으로 잘 서술하였다.',
        question_type_coverage={'sub_criteria_coverage':copy.deepcopy(rows)},
        question_type_coverage_summary={'criteria_status_rows':copy.deepcopy(rows)},
    )
    return text, grade
