# 차압식 레벨계의 원리, 밀도 보정, Dry/Wet Leg, Remote Seal 및 설치 오차

## 1. Topic 계약

- Topic ID: `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Theory Depth: `THEORY_CORE`
- Preparation Priority: `CORE_MUST_PREPARE`
- Grading Mode: `LLM_ONLY`
- Deterministic Checks: `disabled`

## 2. 기본 원리

\[
P_2-P_1=\int_{z_1}^{z_2}ho g\,dz
\]

밀도가 일정하면 다음과 같다.

\[
\Delta P=ho gh
\]

차압식 레벨계는 높이만 직접 측정하지 않는다.
밀도와 높이의 곱인 압력수두를 측정한다.

## 3. Open Tank

\[
\Delta P=ho_pgh
\]

저압측은 대기에 개방한다.
동일한 대기압은 양측에서 상쇄된다.

## 4. Closed Tank

\[
P_H=P_v+ho_pgh
\]

\[
P_L=P_v
\]

\[
\Delta P=(P_v+ho_pgh)-P_v=ho_pgh
\]

## 5. Dry Leg와 Wet Leg

### 5.1. Dry Leg

저압측 도압관을 기체 또는 증기상태로 유지한다.
응축수는 저압측 가변수두를 만든다.
측정차압과 지시레벨을 감소시킨다.

### 5.2. Wet Leg

\[
\Delta P=ho_pgh-ho_wgH_w
\]

0%에서도 음의 차압이 생길 수 있다.
따라서 Zero Elevation을 적용한다.

## 6. 밀도오차

\[
h_{ind}
=rac{\Delta P}{ho_{cal}g}
=rac{ho_{actual}}{ho_{cal}}
 h_{actual}
\]

실제밀도가 교정밀도보다 크면 레벨을 높게 지시한다.

## 7. Zero Suppression과 Elevation

- Zero Suppression: `LRV > 0`
- Zero Elevation: `LRV < 0`

설치 위치가 아니라 0% 입력차압의 부호로 구분한다.

## 8. Remote Diaphragm Seal

압력전달 경로는 다음과 같다.

`공정압력 → 격리막 → 충전액 → 모세관 → 차압셀`

충전액 수두는 다음과 같다.

\[
P_f=ho_fg\Delta z
\]

주요 오차요인은 다음과 같다.

- 충전액 밀도와 체적 변화
- 격리막 강성
- 모세관 길이와 내경
- 모세관 온도
- 충전액 점도
- 양측 모세관 비대칭

## 9. 계면 측정

\[
\Delta P=C+g[ho_LH+(ho_H-ho_L)h_i]
\]

\[
rac{d\Delta P}{dh_i}=g(ho_H-ho_L)
\]

밀도차가 작으면 계면 span이 감소한다.
전체 액주높이와 상부 액체층 조건이 필요하다.

## 10. 주요 현장 오차

- 도압관 막힘·누설·기포
- 액봉 손실
- 응축과 동결
- Heat Tracing 비대칭
- 트랜스미터 설치높이
- Remote Seal 온도오차
- 높은 정압과 한쪽 포트 과압
- 탱크 형상에 따른 체적 비선형

## 11. 교정 원칙

1. 0% 차압을 계산하여 LRV로 설정한다.
2. 100% 차압을 계산하여 URV로 설정한다.
3. `Span = URV - LRV`를 확인한다.
4. 실제 운전밀도와 기준액 밀도를 사용한다.
5. 모든 설치수두와 충전액 수두를 포함한다.

## 12. 선정 비교

차압식은 기존 압력탭과 계면 측정에 유리하다.
밀도와 도압관 상태에 영향을 받는다.

자유공간 Radar는 공정액 밀도 변화의 직접 영향이 작다.
유전율, 노즐, 에코와 불감영역을 검토한다.

GWR은 좁은 공간과 계면 측정에 유리할 수 있다.
프로브 부착물, 기계하중과 상부매질 조건을 검토한다.

## 13. 기술사 답안 권장 위계

1. 배경 및 측정원리
2. Open/Closed Tank와 Dry/Wet Leg
3. LRV·URV·Span과 영점 이동
4. 밀도·온도·설치 오차
5. Remote Seal과 계면 측정
6. 개선대책과 방식 선정

## 14. Logic Check 정책

Fatal은 명시적인 핵심 이론 반대 주장에만 적용한다.

- 밀도와 무관하다는 주장
- 밀폐탱크 기상부 압력이 항상 더해진다는 주장
- Wet Leg 저압측 수두의 부호 반전
- 계면 감도가 밀도차와 무관하다는 주장

Fatal의 직접 점수 영향은 B/C에 한정한다.
D/E 점수는 직접 변경하지 않는다.
관련 현장 주장 claim trust만 제한한다.

## 15. Fact verification references

- Emerson differential-pressure level guidance
- Yokogawa differential-pressure level application notes
- Endress+Hauser Deltabar guidance
- WIKA diaphragm-seal system guidance
- ISA hydrostatic-level and impulse-piping practices
