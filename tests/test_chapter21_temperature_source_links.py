"""Chapter 21 is one source shared by three question-owned temperature Topics."""

from pathlib import Path

from study.master_topic_pack import load_master_topic_pack, project_grading, project_training


ROOT = Path(__file__).resolve().parents[1]
POST_ID = "wp-post:9752"
PDF_ID = "wpurl:45da0d33af7b299e7b7651542abcda7c"
TOPIC_MARKERS = {
    "rtd_temperature_sensor_principle_pt100_wiring_compensation": (
        "RTD (Resistance Temperature Detector)", "21.4 열전대 (Thermocouples)"
    ),
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization": (
        "서미스터 (Thermistor)", "RTD (Resistance Temperature Detector)"
    ),
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation": (
        "21.4 열전대 (Thermocouples)", "원문 필기 검토 사항"
    ),
}


def test_chapter21_source_is_scoped_per_existing_topic_without_grading_promotion():
    versions = set()
    for topic_id, markers in TOPIC_MARKERS.items():
        master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{topic_id}.json")
        references = {source["source_id"]: source for source in master["sources"]}
        post, pdf = references[POST_ID], references[PDF_ID]
        versions.add(post["version"])
        assert post["wordpress_url"] == "https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-21/"
        assert post["verification_status"] == pdf["verification_status"] == "unverified"
        assert post["training_scope"]["mode"] == "text_ranges"
        assert post["training_scope"]["text_ranges"] == [
            {"start_marker": markers[0], "end_marker": markers[1]}
        ]
        assert pdf["training_scope"]["mode"] == "exclude"
        training = project_training(ROOT, master)
        assert POST_ID in {source["source_id"] for source in training["source_references"]}
        assert PDF_ID in {source["source_id"] for source in training["source_references"]}
        assert PDF_ID not in {source["source_id"] for source in training["source_materials"]}
        assert project_grading(ROOT, master)["authority"] == "existing_topic_pack"
    assert len(versions) == 1
