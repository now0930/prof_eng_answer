# 제어밸브 시트 누설, 차단 등급, 패킹 및 비산배출


## 1. Topic 정보

- Topic ID: `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions`
- Primary: `COMPARE_SELECTION`
- Secondary: `DIAGNOSIS_ACTION`
- Tertiary: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Importance: `CORE_MUST_PREPARE`

## 2. Leakage Path 구분

Internal through-seat leakage는 inlet에서 outlet으로 이동한다.
External leakage는 packing·joint에서 atmosphere로 방출된다.
두 leakage의 시험과 acceptance를 분리한다.

## 3. Shutoff Class

Class는 지정된 test procedure의 허용 누설 계약이다.
Medium, pressure, direction, temperature, duration와 unit를 함께 명시한다.
Field operating leakage를 자동 보증하지 않는다.

## 4. Soft Seat와 Metal Seat

| 항목 | Soft Seat | Metal Seat |
|---|---|---|
| Tightness | 낮은 leakage에 유리 가능 | Surface·load 조건에 의존 |
| Temperature | Polymer 한계 확인 | 상대적으로 넓을 수 있음 |
| Wear | Extrusion·damage 검토 | Galling·erosion 검토 |
| 적용 | Clean·compatible service | Harsh·high-temperature service |

## 5. Seat Load

부족: contact stress 부족과 shutoff leakage 증가.
과다: deformation, galling, wear와 actuator demand 증가.
Actuator sizing은 Topic 1 경계를 따른다.

## 6. Pressure Direction

Pressure-assisted sealing과 pressure-unbalanced force를 구분한다.
Normal과 reverse-pressure shutoff를 별도 평가한다.

## 7. Leakage Ratio

$$R_L=\frac{Q_{\mathrm{leak}}}{Q_{\mathrm{ref}}}$$
$$P_{\mathrm{allow}}=100\frac{Q_{\mathrm{leak}}}{Q_{\mathrm{allow}}}$$
Reference와 allowable은 양수이고 medium·condition을 맞춘다.

## 8. Normalized Leakage

$$Q_n=\frac{Q_{\mathrm{leak}}}{S_{\mathrm{basis}}}$$
Nominal size, port, seat diameter 등 governing basis를 명시한다.

## 9. Mass와 Gas Reference Conversion

$$\dot m=\rho Q$$
$$Q_{\mathrm{ref}}=Q_{\mathrm{test}}\left(\frac{P_{\mathrm{test}}}{P_{\mathrm{ref}}}\right)\left(\frac{T_{\mathrm{ref}}}{T_{\mathrm{test}}}\right)$$
Absolute pressure와 absolute temperature를 사용한다.

## 10. Bubble Count

$$Q_b=\frac{N_bV_b}{\Delta t}$$
Bubble volume, duration와 gas condition을 확인한다.

## 11. Seat Leakage 원인

- Damage·erosion·wire drawing·galling
- Foreign material·scale·polymerization
- Thermal distortion·differential expansion
- Stem bending·guide wear·misalignment
- Surface finish·hardness·coating

## 12. Balanced Trim

Unbalanced force는 줄지만 balance-seal과 clearance leakage path가 추가될 수 있다.
구조 mechanics는 Topic 10이 소유한다.

## 13. Packing Leakage

Sliding stem과 rotary shaft의 motion과 wear mode를 구분한다.
Material, ring arrangement, box dimension와 surface finish를 확인한다.

## 14. Packing Compression

$$\varepsilon_p=\frac{h_0-h}{h_0}$$
$$\sigma_g=\frac{F_g}{A_g}$$
Compression 증가 시 leakage와 friction의 trade-off를 검토한다.

## 15. Live-Loaded Packing

Spring element로 consolidation·relaxation을 보상한다.
Spring range, installed compression와 corrosion inspection이 필요하다.

## 16. Bellows Seal

Stem leakage 격리에 유리하다.
Pressure, temperature, cycle life와 fatigue limitation을 확인한다.
Backup packing을 함께 정의한다.

## 17. Low-Emission Qualification

Qualification은 지정된 pressure·temperature·cycle 시험의 결과이다.
Field installation과 maintenance 성능을 자동 보증하지 않는다.

## 18. Fugitive Emission

Source와 monitoring point를 구분한다.
Background와 instrument condition을 기록한다.
Sniffing·screening과 bagging·quantification을 구분한다.

## 19. Concentration과 Mass Rate

Concentration은 특정 위치의 species fraction이다.
Mass-emission rate는 flow와 species mass를 포함한다.

## 20. As-Found와 As-Left

같은 medium, pressure, temperature, method와 stabilization에서 비교한다.
Repair 효과와 remaining risk를 기록한다.

## 21. Leakage Trend

$$\Delta Q=Q_{\mathrm{current}}-Q_{\mathrm{baseline}}$$
$$\Delta Q_{\%}=100\frac{Q_{\mathrm{current}}-Q_{\mathrm{baseline}}}{|Q_{\mathrm{baseline}}|}$$
$$\dot Q=\frac{Q_2-Q_1}{t_2-t_1}$$

## 22. Uncertainty-Aware Acceptance

$$Q_{\mathrm{meas}}+U\le Q_{\mathrm{allow}}$$
Detection limit 이하를 정확한 zero leakage로 표현하지 않는다.

## 23. False Pass·False Fail

Stabilization, background, drift, range와 detection limit를 확인한다.
Borderline result는 repeat test와 uncertainty review를 수행한다.

## 24. Lifecycle Workflow

Specification → selection → shop test → installation → commissioning → monitoring → maintenance → as-left

## 25. Topic 경계

- Topic 1: Actuator thrust·seat load sizing
- Topic 3: Packing friction·stiction·dynamic response
- Topic 8: Cavitation·flashing damage physics
- Topic 10: Balanced trim·balance-seal mechanics
- Topic 11: Positioner·I/P calibration
- Topic 12: Valve signature·predictive diagnostics
- Topic 14: Severe-service·cryogenic·high-temperature package
- Topic 15: SIS·ESD·PST·proof test
- Topic 16: Full package selection·lifecycle economics

## 26. 대표 오답

- Shutoff class가 모든 field condition의 leakage를 보증한다.
- Soft seat는 항상 zero leakage이다.
- Seat load는 클수록 항상 좋다.
- Gas와 liquid leakage 숫자를 직접 비교한다.
- Bubble volume은 universal constant이다.
- Packing을 계속 조이면 항상 해결된다.
- Live-loaded packing은 maintenance-free이다.
- Bellows seal이 모든 external leakage를 제거한다.
- Concentration은 mass-emission rate와 같다.
- PST가 shutoff class와 proof test를 자동 증명한다.

## 27. 고득점 답안 기준

1. Internal과 external leakage를 구분한다.
2. Class와 test condition을 하나의 계약으로 설명한다.
3. Soft·metal seat trade-off를 설명한다.
4. Seat load 부족·과다와 pressure direction을 설명한다.
5. Volumetric·mass·bubble와 reference conversion을 구분한다.
6. Seat damage·contamination·thermal 원인을 구분한다.
7. Packing compression과 leakage-friction trade-off를 설명한다.
8. Live-loaded·low-emission packing과 bellows limitation을 설명한다.
9. As-found·as-left, detection limit와 uncertainty를 포함한다.
10. Topic 1·3·8·10·11·12·14·15·16 경계를 명시한다.
