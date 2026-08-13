from __future__ import annotations
import ast
from copy import deepcopy
from pathlib import Path
import grading_agents as ga
LAYER_MAX={"A":3.0,"B":6.0,"C":8.0,"D":6.0,"E":2.0}
def vector(rows):
    out={}
    for row in rows:
        if not isinstance(row,dict): continue
        lid=str(row.get("layer_id") or row.get("layer") or row.get("id") or "").upper()
        if lid in LAYER_MAX: out[lid]=float(row["score"])
    assert set(out)==set(LAYER_MAX),out
    return out
model={"total_points":25.0,"layers":[{"id":lid,"name":lid,"points":mx} for lid,mx in LAYER_MAX.items()]}
base=ga._phase2_layer_scores("sentinel",deepcopy(model)); base_v=vector(base)
helper=ga._phase3_apply_question_demand_evidence_to_layer_scores
probes=((0,0,0,0.0),(0.5,0.25,0.25,2.0),(1,1,0.5,5.0),(1,1,1,6.0))
for covered,verified,mean,expected in probes:
    evidence={"summary":{"covered_ratio":covered,"verified_ratio":verified,"mean_demand_level":mean,"linked_ratio":0.123}}
    v=vector(helper(deepcopy(base),evidence)); assert abs(v["B"]-expected)<=1e-12,(evidence,v)
    for lid in ("A","C","D","E"): assert abs(v[lid]-base_v[lid])<=1e-12
fact=ga._phase3_apply_fact_anchor_to_layer_scores(deepcopy(base),{"c_score":6.25,"c_score_detail":{"accuracy":1.25,"core_concept":1.50,"problem_link":2.50,"compactness":1.00}})
fv=vector(fact); assert abs(fv["C"]-6.25)<=1e-12
fallback=ga._phase3_apply_fact_anchor_to_layer_scores(deepcopy(base),{"c_score_detail":{"accuracy":1.25,"core_concept":1.50,"problem_link":2.00,"compactness":0.50}})
assert abs(vector(fallback)["C"]-5.25)<=1e-12
conn=ga._phase3_apply_connection_to_layer_scores(deepcopy(fact),{"score":999.0}); assert vector(conn)==fv
source=Path(ga.__file__).read_text(encoding="utf-8"); tree=ast.parse(source)
owner=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=="_phase2_postprocess_grade")
def call_name(call):
    if isinstance(call.func,ast.Name): return call.func.id
    if isinstance(call.func,ast.Attribute): return call.func.attr
    return ""
phase8=[]; qd=[]; caps=[]
for node in ast.walk(owner):
    if not isinstance(node,ast.Call): continue
    name=call_name(node)
    if name=="_phase8_apply_originality_to_layer_scores": phase8.append(node.lineno)
    if name=="_phase3_apply_question_demand_evidence_to_layer_scores": qd.append(node.lineno)
    if "cap" in name.lower(): caps.append(node.lineno)
assert len(phase8)==1 and len(qd)==1
down=[x for x in caps if x>qd[0]]; assert down and phase8[0]<qd[0]<min(down)
for marker in ("QUESTION_DEMAND_B_COMPLETENESS_NATIVE_V2","QTYPE_FACT_C_NATIVE_SCORE_V2","QUESTION_DEMAND_B_TERMINAL_OWNER_GUARDED_V3"): assert marker in source
print("QUESTION_DEMAND_B_SCORE_CONNECTION_V2_FOCUSED_TEST=PASS")
print("B_FORMULA=2*(covered_ratio+verified_ratio+mean_demand_level)")
print("FACT_C_NATIVE_SCORE=YES")
print("CONNECTION_NOOP_PRESERVED=YES")
print("TERMINAL_OWNER_ORDER_PRESERVED=YES")


# PHASE8_CONSTRAINT_ONLY_OWNER_CONTRACT_V2_FOCUSED
_semantic_s6d2 = [
    {"id": "A", "score": 2.5},
    {"id": "B", "score": 3.0},
    {"id": "C", "score": 6.0},
    {"id": "D", "score": 4.5},
    {"id": "E", "score": 1.5},
]
_phase8_s6d2 = [
    {"id": "A", "score": 2.8},
    {"id": "B", "score": 1.0},
    {"id": "C", "score": 5.0},
    {"id": "D", "score": 5.0},
    {"id": "E", "score": 1.2},
]
_out_s6d2 = ga._phase8_apply_constraint_only_to_semantic_layers(
    _semantic_s6d2,
    _phase8_s6d2,
)

def _vec_s6d2(rows):
    return {
        str(r.get("id") or r.get("layer_id") or r.get("layer")).upper(): float(r["score"])
        for r in rows
        if isinstance(r, dict)
    }

_v_s6d2 = _vec_s6d2(_out_s6d2)
assert _v_s6d2 == {
    "A": 2.5,
    "B": 1.0,
    "C": 5.0,
    "D": 4.5,
    "E": 1.2,
}, _v_s6d2

_source_s6d2 = Path(ga.__file__).read_text(encoding="utf-8")
_tree_s6d2 = ast.parse(_source_s6d2)
_owner_s6d2 = next(
    n for n in _tree_s6d2.body
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    and n.name == "_phase2_postprocess_grade"
)

def _call_name_s6d2(call):
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return ""

_order_s6d2 = {}
for _node_s6d2 in ast.walk(_owner_s6d2):
    if isinstance(_node_s6d2, ast.Call):
        _name_s6d2 = _call_name_s6d2(_node_s6d2)
        if _name_s6d2 in {
            "_phase6_apply_gemini_layer_scores",
            "_phase8_apply_originality_to_layer_scores",
            "_phase8_apply_constraint_only_to_semantic_layers",
            "_phase3_apply_question_demand_evidence_to_layer_scores",
        }:
            _order_s6d2.setdefault(_name_s6d2, []).append(_node_s6d2.lineno)

for _name_s6d2, _vals_s6d2 in _order_s6d2.items():
    assert len(_vals_s6d2) == 1, (_name_s6d2, _vals_s6d2)

assert (
    _order_s6d2["_phase6_apply_gemini_layer_scores"][0]
    < _order_s6d2["_phase8_apply_originality_to_layer_scores"][0]
    < _order_s6d2["_phase8_apply_constraint_only_to_semantic_layers"][0]
    < _order_s6d2["_phase3_apply_question_demand_evidence_to_layer_scores"][0]
), _order_s6d2

assert _source_s6d2.count("QTYPE_PHASE8_CONSTRAINT_ONLY_V1") == 1
assert _source_s6d2.count("QTYPE_PHASE6_SEMANTIC_SNAPSHOT_V1") == 1
print("PHASE8_CONSTRAINT_ONLY_OWNER_CONTRACT_V2_FOCUSED=PASS")

# STAGE8B_NATIVE_OUTPUT_SYNC_INTEGRATION_FOCUSED_V1
_qd_s8b = {
    "demands": [
        {"demand_id": "D1", "demand_text": "원리", "native_state": 3},
        {"demand_id": "D2", "demand_text": "적용", "native_state": 2},
    ]
}
_grade_s8b = {
    "breakdown": [
        {"layer_id": "A", "score": 2.0},
        {"layer_id": "B", "score": 1.0},
        {"layer_id": "C", "score": 1.0, "native_fact_projection_v1": {"score": 7.0}},
        {"layer_id": "D", "score": 4.0},
        {"layer_id": "E", "score": 1.5},
    ],
    "layer_scores": [
        {"layer_id": "A", "score": 2.0},
        {"layer_id": "B", "score": 1.0},
        {"layer_id": "C", "score": 1.0},
        {"layer_id": "D", "score": 4.0},
        {"layer_id": "E", "score": 1.5},
    ],
    "rater_weighted_evaluation": {
        "weighted_layers": [
            {"layer_id": "A", "score": 2.0},
            {"layer_id": "B", "score": 1.0},
            {"layer_id": "C", "score": 1.0},
            {"layer_id": "D", "score": 4.0},
            {"layer_id": "E", "score": 1.5},
        ],
        "total_score": 0.0,
    },
    "total_score": 0.0,
    "score": 0.0,
}
_applied_s8b = ga._stage7_apply_native_qd_projection_to_grade_output(_grade_s8b, _qd_s8b)
assert _applied_s8b is _grade_s8b
assert abs(_applied_s8b["coverage"] - 100.0) <= 1e-12
assert abs(_applied_s8b["native_question_demand_projection_v1"]["score"] - 5.0) <= 1e-12
_final_s8b = [
    {"layer_id": "A", "score": 2.0},
    {"layer_id": "B", "score": 5.0, "native_question_demand_projection_v1": {"score": 5.0}},
    {"layer_id": "C", "score": 7.0, "native_fact_projection_v1": {"score": 7.0}},
    {"layer_id": "D", "score": 4.0},
    {"layer_id": "E", "score": 1.5},
]
_synced_s8b = ga._stage7_sync_terminal_bc_from_final_layer_scores(_applied_s8b, _final_s8b)
assert _synced_s8b is _grade_s8b
assert vector(_synced_s8b["breakdown"])["B"] == 5.0
assert vector(_synced_s8b["breakdown"])["C"] == 7.0
assert vector(_synced_s8b["layer_scores"])["B"] == 5.0
assert vector(_synced_s8b["layer_scores"])["C"] == 7.0
assert _synced_s8b["total_score"] == 19.5
assert _synced_s8b["score"] == 19.5
_source_s8b = Path(ga.__file__).read_text(encoding="utf-8")
_tree_s8b = ast.parse(_source_s8b)
_owner_s8b = next(n for n in _tree_s8b.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "_phase2_postprocess_grade")
_apply_lines_s8b = []
_sync_lines_s8b = []
_write_lines_s8b = []
for _node_s8b in ast.walk(_owner_s8b):
    if not isinstance(_node_s8b, ast.Call):
        continue
    _name_s8b = call_name(_node_s8b)
    if _name_s8b == "_stage7_apply_native_qd_projection_to_grade_output":
        _apply_lines_s8b.append(_node_s8b.lineno)
    elif _name_s8b == "_stage7_sync_terminal_bc_from_final_layer_scores":
        _sync_lines_s8b.append(_node_s8b.lineno)
    elif _name_s8b == "_phase2_json_write" and _node_s8b.args and "grade.json" in ast.unparse(_node_s8b.args[0]):
        _write_lines_s8b.append(_node_s8b.lineno)
assert len(_apply_lines_s8b) == len(_sync_lines_s8b) == len(_write_lines_s8b) == 1
assert _apply_lines_s8b[0] < _sync_lines_s8b[0] < _write_lines_s8b[0]
assert _source_s8b.count("STAGE8_FINAL_NATIVE_BC_PERSISTENCE_V1") == 1
print("STAGE8B_NATIVE_OUTPUT_SYNC_INTEGRATION_FOCUSED_V1=PASS")
