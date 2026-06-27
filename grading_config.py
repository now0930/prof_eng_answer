import json
from pathlib import Path
from datetime import datetime


def read_json(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_active_config(base_dir=None):
    base = Path(base_dir) if base_dir else Path(__file__).resolve().parent
    profile_path = base / "rubrics" / "active_profile.json"

    if not profile_path.exists():
        raise FileNotFoundError(f"active profile not found: {profile_path}")

    profile = read_json(profile_path)

    scoring_model_path = base / profile["scoring_model"]
    subject_rubric_path = base / profile["subject_rubric"]
    rater_profile_path = base / profile["rater_profile"]
    legacy_rubric_path = base / profile.get("legacy_rubric", "rubrics/default.json")

    config = {
        "loaded_at": datetime.now().isoformat(timespec="seconds"),
        "base_dir": str(base),
        "profile_path": str(profile_path),
        "profile": profile,
        "paths": {
            "scoring_model": str(scoring_model_path),
            "subject_rubric": str(subject_rubric_path),
            "rater_profile": str(rater_profile_path),
            "legacy_rubric": str(legacy_rubric_path)
        },
        "scoring_model": read_json(scoring_model_path),
        "subject_rubric": read_json(subject_rubric_path),
        "rater_profile": read_json(rater_profile_path),
        "legacy_rubric": read_json(legacy_rubric_path) if legacy_rubric_path.exists() else None
    }

    validate_active_config(config)
    return config


def validate_active_config(config):
    scoring = config["scoring_model"]

    layers = scoring.get("layers", [])
    total = float(scoring.get("total_points", 0))
    layer_sum = sum(float(x.get("points", 0)) for x in layers)

    if abs(layer_sum - total) > 0.0001:
        raise ValueError(f"scoring layer sum mismatch: {layer_sum} != {total}")

    weights = scoring.get("rater_weights_by_layer", {})
    for layer in layers:
        layer_id = layer.get("id")
        if layer_id not in weights:
            raise ValueError(f"missing rater weights for layer {layer_id}")
        s = sum(float(v) for v in weights[layer_id].values())
        if abs(s - 1.0) > 0.0001:
            raise ValueError(f"rater weight sum mismatch for {layer_id}: {s}")

    if "answer_sheet_volume_policy" not in scoring:
        raise ValueError("missing answer_sheet_volume_policy in scoring_model")

    raters = config["rater_profile"].get("raters", [])
    rater_ids = {r.get("id") for r in raters}
    for layer_id, layer_weights in weights.items():
        for rater_id in layer_weights:
            if rater_id not in rater_ids:
                raise ValueError(f"rater weight references unknown rater: {rater_id}")

    return True


def save_active_config_snapshots(session_dir, config):
    session = Path(session_dir)
    session.mkdir(parents=True, exist_ok=True)

    write_json(session / "active_profile_snapshot.json", config["profile"])
    write_json(session / "scoring_model_snapshot.json", config["scoring_model"])
    write_json(session / "subject_rubric_snapshot.json", config["subject_rubric"])
    write_json(session / "layered_rater_snapshot.json", config["rater_profile"])

    return {
        "active_profile_snapshot": str(session / "active_profile_snapshot.json"),
        "scoring_model_snapshot": str(session / "scoring_model_snapshot.json"),
        "subject_rubric_snapshot": str(session / "subject_rubric_snapshot.json"),
        "layered_rater_snapshot": str(session / "layered_rater_snapshot.json")
    }
