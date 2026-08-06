#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

TOPIC_ID = 'control_software_project_engineering_documents_fat_sat_commissioning_acceptance'
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"
FILES = [PACK / "README.md", PACK / "fact_anchor.json", PACK / "logic_check.json", PACK / "model_answer.json", PACK / "topic_importance.json", SHEET, Path(__file__)]

def load(name: str):
    return json.loads((PACK / name).read_text(encoding="utf-8"))

class TopicPackStructureTests(unittest.TestCase):
    def setUp(self):
        self.fact=load("fact_anchor.json"); self.logic=load("logic_check.json"); self.model=load("model_answer.json"); self.imp=load("topic_importance.json")
    def test_required_files_exist(self):
        self.assertTrue(all(p.is_file() for p in FILES))
    def test_topic_id_and_schema_contract(self):
        for data in (self.fact,self.logic,self.model,self.imp): self.assertEqual(data["topic_id"], TOPIC_ID)
        self.assertEqual(self.fact["schema_version"],"topic_pack.fact_anchor.v1")
        self.assertEqual(self.logic["schema_version"],"topic_pack.logic_check.v1")
    def test_anchor_count_and_uniqueness(self):
        anchors=self.fact["anchors"]; self.assertEqual(len(anchors), 34); ids=[x["id"] for x in anchors]; self.assertEqual(len(ids),len(set(ids)))
    def test_importance_enum(self):
        self.assertTrue(all(x["importance"] in {"must","important","optional"} for x in self.fact["anchors"]))
    def test_fatal_count_and_shape(self):
        self.assertEqual(len(self.fact["fatal_wrong_claims"]),16); self.assertEqual(len(self.logic["deterministic_checks"]["fatal_checks"]),16); self.assertEqual(len(self.logic["llm_profile"]["fatal_conditions"]),16)
    def test_logic_profile_contract(self):
        profile=self.logic["llm_profile"]; self.assertTrue(profile["enabled"]); self.assertTrue(profile["cap_policy"]["fatal_requires_explicit_contradiction"]); self.assertTrue(profile["cap_policy"]["omission_is_not_fatal"]); self.assertEqual(len(profile["major_checks"]),8); self.assertEqual(len(profile["false_positive_cautions"]),10)
    def test_model_references_are_valid(self):
        ids={x["id"] for x in self.fact["anchors"]}; refs={r for s in self.model["recommended_outline"] for r in s["anchor_refs"]}; self.assertTrue(refs <= ids)
    def test_question_outline_counts(self):
        self.assertEqual(len(self.model["expected_question_patterns"]),10); self.assertEqual(len(self.model["recommended_outline"]),8)
    def test_routing_counts_and_no_broad_alias(self):
        self.assertEqual(len(self.model["routing_aliases"]),20); self.assertEqual(len(self.model["routing_field_points"]),45); self.assertTrue(all(len(x.split()) >= 3 for x in self.model["routing_aliases"]))
    def test_scope_boundaries_are_explicit(self):
        text=" ".join(x["statement"] for x in self.fact["anchors"]); self.assertIn("SW-04",text); self.assertIn("SW-02",text); self.assertIn("SW-03",text)
    def test_text_files_have_clean_whitespace(self):
        for path in FILES:
            data=path.read_bytes(); self.assertTrue(data.endswith(b"\n"), path)
            for i,line in enumerate(data.decode().splitlines(),1): self.assertEqual(line,line.rstrip(),f"{path}:{i}")

class DeterministicFatalPatternSafetyTests(unittest.TestCase):
    def setUp(self): self.logic=load("logic_check.json")
    def test_direct_wrong_claims_match_deterministic_aids(self):
        for item in self.logic["deterministic_checks"]["fatal_checks"]:
            self.assertTrue(any(re.search(p,item["message"]) for p in item["wrong_patterns"]),item["id"])
    def test_explicit_corrections_do_not_trigger_patterns(self):
        for item in self.logic["deterministic_checks"]["fatal_checks"]:
            answer=f'“{item["message"]}”라는 주장은 틀리며, {item["correct_rule"]}'
            self.assertFalse(any(re.search(p,answer) for p in item["wrong_patterns"]),item["id"])
    def test_patterns_do_not_match_omission(self):
        answer="프로젝트 문서와 시험단계를 일부만 설명했다."
        for item in self.logic["deterministic_checks"]["fatal_checks"]:
            self.assertFalse(any(re.search(p,answer) for p in item["wrong_patterns"]),item["id"])

class ProjectRelationshipTests(unittest.TestCase):
    def setUp(self): self.fact=load("fact_anchor.json"); self.by={x["id"]:x["statement"] for x in self.fact["anchors"]}
    def test_document_hierarchy(self):
        text=self.by["sw10_document_hierarchy_traceability"]; self.assertRegex(text,r"URS→FRS→FDS→SDS→시험명세→시험결과"); self.assertIn("양방향",text)
    def test_fat_sat_distinct(self):
        self.assertIn("통제",self.by["sw10_fat"]); self.assertIn("현장",self.by["sw10_sat"]); self.assertIn("생략",self.by["sw10_fat_sat_relation"])
    def test_loop_is_end_to_end(self):
        text=self.by["sw10_loop_test"]
        self.assertIn("현장 입력 또는 출력 종단",text)
        self.assertIn("폐루프 제어 Loop",text)
        self.assertIn("최종요소가 없는 정보·감시 Loop",text)
        self.assertIn("종단 간",text)
    def test_site_integration_has_handshake_time(self):
        text=self.by["sw10_site_integration_test"]; self.assertIn("Handshake",text); self.assertIn("시간동기",text); self.assertIn("장애복구",text)
    def test_commissioning_sequence_has_safety(self):
        text=self.by["sw10_commissioning"]; self.assertIn("안전조건",text); self.assertIn("단계별 기동",text); self.assertIn("부하시험",text)
    def test_performance_has_quantitative_contract(self):
        text=self.by["sw10_performance_test"]; self.assertIn("조건",text); self.assertIn("기간",text); self.assertIn("허용기준",text)
    def test_acceptance_is_not_installation(self):
        text=self.by["sw10_acceptance"]; self.assertIn("시험",text); self.assertIn("문서",text); self.assertIn("Punch",text)
    def test_punch_closure_loop(self):
        text=self.by["sw10_change_punch_closure"]; self.assertIn("영향분석",text); self.assertIn("회귀시험",text); self.assertIn("Closure".lower(),text.lower())
    def test_asbuilt_matches_actual(self):
        text=self.by["sw10_as_built_handover"]; self.assertIn("실제 상태",text); self.assertIn("백업",text); self.assertIn("교육",text)

class FocusedRoutingBoundaryTests(unittest.TestCase):
    def setUp(self): self.model=load("model_answer.json"); self.aliases=[x.lower() for x in self.model["routing_aliases"]]
    def signal(self,text):
        words={w.lower() for a in self.aliases for w in re.findall(r"[A-Za-z0-9가-힣]+",a) if len(w)>1}; return sum(1 for w in words if w in text.lower())
    def test_positive_cases_have_local_signal(self):
        for text in ["FAT SAT loop test commissioning acceptance", "URS FRS FDS SDS 제어 프로젝트", "Punch As-built Handover 성능시험"]: self.assertGreaterEqual(self.signal(text),3)
    def test_sw04_boundary_case_is_not_compound_alias(self):
        text="V-Model unit test integration test RTM static analysis".lower(); self.assertFalse(any(a in text for a in self.aliases))
    def test_sw02_boundary_case_is_not_compound_alias(self):
        text="Sequence state transition trip latch reset fail-safe".lower(); self.assertFalse(any(a in text for a in self.aliases))
    def test_sw03_boundary_case_is_not_compound_alias(self):
        text="alarm philosophy shelving suppression SOE operator display".lower(); self.assertFalse(any(a in text for a in self.aliases))

class ContentQualityTests(unittest.TestCase):
    def test_no_placeholder_markers(self):
        for path in FILES[:-1]:
            text=path.read_text(encoding="utf-8").lower(); self.assertNotIn("to"+"do",text); self.assertNotIn("scaf"+"fold",text); self.assertNotIn("보강하세요",text)
    def test_alarm_interlock_document_boundary(self):
        text=load("fact_anchor.json")["core_facts"]; joined=" ".join(text); self.assertIn("SW-03",joined); self.assertIn("SW-02",joined)


class SemanticAuditRepairTests(unittest.TestCase):
    def setUp(self):
        self.fact = load("fact_anchor.json")
        self.logic = load("logic_check.json")
        self.by = {item["id"]: item for item in self.fact["anchors"]}

    def test_anchor_explanations_are_stage_specific(self):
        accepted = [tuple(item["accepted_explanations"]) for item in self.fact["anchors"]]
        rejected = [tuple(item["rejected_explanations"]) for item in self.fact["anchors"]]
        self.assertEqual(len(set(accepted)), 34)
        self.assertEqual(len(set(rejected)), 34)
        joined = " ".join(value for item in self.fact["anchors"] for value in item["rejected_explanations"])
        self.assertNotIn("다른 단계나 문서와 동일한 것으로 간주하거나 승인·시험 증적 없이 완료로 처리한다", joined)

    def test_definition_anchors_do_not_require_test_evidence(self):
        feasibility = " ".join(self.by["sw10_feasibility"]["accepted_explanations"])
        scope = " ".join(self.by["sw10_scope_baseline"]["accepted_explanations"])
        self.assertIn("아직 FAT·SAT 증적을 요구하지 않고", feasibility)
        self.assertIn("포함·제외범위", scope)

    def test_loop_test_protects_monitoring_loop_boundary(self):
        text = self.by["sw10_loop_test"]["statement"]
        self.assertIn("최종요소가 없는 정보·감시 Loop", text)
        self.assertIn("해당 입력 종단", text)
        cautions = " ".join(self.logic["llm_profile"]["false_positive_cautions"])
        self.assertIn("정보·감시 Loop", cautions)

    def test_distributed_approved_documents_are_allowed(self):
        for anchor_id in ("sw10_alarm_list", "sw10_interlock_list", "sw10_cause_effect"):
            text = self.by[anchor_id]["statement"]
            self.assertIn("식별자로 연결된 승인 문서", text)
        self.assertIn("추적성", " ".join(self.by["sw10_interlock_list"]["accepted_explanations"]))

if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    count=suite.countTestCases(); print(f"SW10_FOCUSED_TEST_COUNT={count}")
    if count != 33: raise SystemExit(f"expected 33, got {count}")
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
