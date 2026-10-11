# MC/DC 적용범위 Anchor 근거 재검토 (2026-10-12)

## 판정 요약

다음 두 Anchor는 현재 문구 전체를 입증하는 근거가 확인되지 않아 Fact registry의 `verified`로 승격하지 않았다.

| Topic | Anchor | 판정 | 이유 |
|---|---|---|---|
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | `mcdc_industrial_application_boundary` | 조건부 근거, 미승격 | FAA 자료는 DO-178C의 항공 소프트웨어 개발보증 범위를 명시하고, IEC 61508-3은 안전관련 소프트웨어에 적용하면서 기법을 요구 systematic capability에 따라 등급화한다. 이는 산업별 기준을 적용해야 한다는 제한은 지지하지만, 해당 Anchor의 `언어`와 `Functional Safety Plan`이 모든 산업에서 직접적인 MC/DC 적용결정 인자라고 일반화하는 근거는 부족하다. |
| 같은 Topic | `mcdc_safety_plc_boundary` | 사례 근거, 미승격 | Rockwell ControlLogix 문서는 응용프로그램을 명세에 맞춰 시험하고, 입력 범위/경계/오류값 및 센서·액추에이터를 포함한 전체 응용 검증을 수행하도록 설명한다. IEC 61511-1 공식 preview도 공정분야 SIS의 application programming을 다루고, embedded/system software와 application program의 표준 경계를 구분한다. 하지만 공개된 preview와 제조사 사례만으로 모든 Safety PLC의 SRS 추적 의무, 입력조합 시험 범위, 내부 Firmware MC/DC의 인증범위/Safety Manual별 처리까지 일반화할 수는 없다. |

## 확인한 출처

- FAA, [AC 20-115D — Airborne Software Development Assurance](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032046): 항공 시스템/장비 소프트웨어의 감항 인증을 위한 허용 가능한 수단과 DO-178C 인정을 설명한다. 산업용 PLC/HMI 일반 요구사항의 근거로 확대하지 않는다.
- IEC, [IEC 61508-3:2010 — Software requirements](https://webstore.iec.ch/en/publication/5517): 안전관련 시스템의 소프트웨어 및 개발·구성 지원도구, 소프트웨어 안전수명주기, 요구 systematic capability에 맞춘 기법의 적용 범위를 설명한다. 요약 페이지는 특정 MC/DC 수치나 모든 산업 PLC의 의무를 규정하지 않는다.
- IEC, [IEC 61511-1:2016 official preview](https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTExLTF7ZWQyLjB9Yi5wZGY%3D): 공개 preview의 적용범위 및 관계도는 공정분야 application programming과 embedded/system software를 구분하고 IEC 61508-3의 적용 경계를 제시한다. 공개 부분만으로 내부 firmware의 MC/DC 재수행 조건이나 특정 Safety PLC 인증의 세부 경계를 입증하지는 않는다.
- Rockwell Automation, [ControlLogix 5590 — Validate the Project](https://www.rockwellautomation.com/en-se/docs/technical/logix5000/_online/1756-um900/controllogix-5590-controller-user-manual-ditamap/validate-the-project.html): 응용 명세를 확인할 시험사례 문서화, 범위/경계/유효하지 않은 입력값 시험, 현장장치 및 전체 안전 응용의 검증, 변경 영향분석을 설명한다. 이는 제품별 응용 검증 사례이며 전 산업 제품의 인증조건을 대체하지 않는다.
- Rockwell Automation, [Logix SIS — Application Development and Testing](https://www.rockwellautomation.com/en-us/docs/technical/logix5000/_online/1756-rm015/logix-sis-safety-reference-manual-ditamap/safety-applications/application-development-and-testing.html): 안전 응용프로그램의 기능 명세, 로직 검토 및 응용 검증을 설명한다.

## 다음 조치

정확한 적용성을 확정하려면 대상 산업 표준 및 실제 Safety PLC 제조사의 인증서·Safety Manual을 특정해야 한다. 따라서 현 단계에서는 두 Anchor를 미검증으로 유지한다. 표현을 좁혀 FAA 항공 MC/DC와 IEC 61508의 체계적 capability/응용검증을 각각 구분하면 이후 Fact로 승격할 수 있으나, 현재 저장소에는 그러한 좁은 문구가 반영되지 않았다. IEC 61511-1 공개 preview를 추가 대조했으나, 이는 표준 간 software 경계를 보강할 뿐 `firmware MC/DC` 재수행 조건을 제공하지 않아 승격 근거로 사용하지 않았다.
