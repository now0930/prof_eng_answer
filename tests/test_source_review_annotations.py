"""Regression for approved source identity and undecided editorial notes."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
from test_master_topic_pack_schema import _valid_record
from test_training_diagnosis_projections import _write_sources
from study.master_topic_pack import MasterTopicPackError, project_training, project_diagnosis, project_grading
from study.learning_runtime import feedback_from_view


class SourceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.master = _valid_record()
        self.ref = self.master["sources"][0]
        self.ref["source_url"] = self.ref["wordpress_url"]
        _write_sources(self.root, self.master)
        self.text = "Original handwritten wording: Critical System."
        self.digest = hashlib.sha256(self.text.encode()).hexdigest()
        self.row = {
            "source_id": self.ref["source_id"], "source_type": self.ref["source_type"], "version": self.ref["version"],
            "wordpress_url": self.ref["wordpress_url"], "source_url": self.ref["source_url"],
            "extraction_status": "extracted", "extraction_method": "wordpress_wxr_html",
            "extracted_text": self.text, "extracted_text_sha256": self.digest,
        }
        self.bundle_path = self.root / "data/wordpress_topic_packs" / f"{self.master['topic_id']}.json"
        self.bundle_path.parent.mkdir(parents=True)
        self.write_bundle()
        self.note = {
            "annotation_id": "terminology_review", "source_id": self.ref["source_id"],
            "source_version": self.ref["version"], "source_text_sha256": self.digest,
            "locator": "section 10", "quote": "Critical System",
            "review_note": "미확정 의견: 문맥 검토 필요. 원문 보존.",
            "status": "pending_review", "decision": None, "score_effect": "none",
        }
        self.note_path = self.root / "study/source_review_annotations" / f"{self.master['topic_id']}.json"
        self.note_path.parent.mkdir(parents=True)
        self.write_note()

    def write_bundle(self):
        self.bundle_path.write_text(json.dumps({"topic_id": self.master["topic_id"], "private": True, "sources": [self.row]}))

    def write_note(self):
        self.note_path.write_text(json.dumps({"schema_version": "source-review-annotations-v1", "topic_id": self.master["topic_id"], "annotations": [self.note]}))

    def test_new_text_with_valid_checksum_cannot_impersonate_approved_version(self):
        self.row.update(version="new-unapproved", extracted_text="new text", extracted_text_sha256=hashlib.sha256(b"new text").hexdigest())
        self.write_bundle()
        for view in (project_training, project_diagnosis):
            with self.assertRaisesRegex(MasterTopicPackError, "source version"):
                view(self.root, self.master)
        del self.row["version"]
        self.write_bundle()
        with self.assertRaisesRegex(MasterTopicPackError, "source version"):
            project_training(self.root, self.master)

    def test_exact_source_url_must_match_even_when_parent_matches(self):
        self.row["source_url"] = "https://example.org/different/"
        self.write_bundle()
        with self.assertRaisesRegex(MasterTopicPackError, "exact source URL"):
            project_training(self.root, self.master)

    def test_notes_reach_feedback_without_modifying_original_or_grade(self):
        before_bytes = self.bundle_path.read_bytes()
        before_master = copy.deepcopy(self.master)
        before_grading = project_grading(self.root, self.master)
        training = project_training(self.root, self.master)
        diagnosis = project_diagnosis(self.root, self.master)
        grade = {"topic_id": self.master["topic_id"], "final_total_score": 17.0}
        before_grade = copy.deepcopy(grade)
        feedback = feedback_from_view(grade, diagnosis)
        self.assertEqual(training["source_materials"][0]["text"], self.text)
        self.assertEqual(training["source_review_annotations"], feedback["source_review_annotations"])
        self.assertEqual(feedback["source_review_annotations"][0]["source_state"], "matching")
        self.assertIsNone(feedback["source_review_annotations"][0]["decision"])
        feedback["source_review_annotations"][0]["review_note"] = "local mutation"
        self.assertEqual(self.bundle_path.read_bytes(), before_bytes)
        self.assertEqual(self.master, before_master)
        self.assertEqual(grade, before_grade)
        self.assertEqual(project_grading(self.root, self.master), before_grading)
        self.assertNotEqual(diagnosis["source_review_annotations"][0]["review_note"], "local mutation")

    def test_old_annotations_are_preserved_and_marked_stale(self):
        for key, value in [("source_version", "older"), ("source_text_sha256", "0" * 64)]:
            original = self.note[key]
            self.note[key] = value
            self.write_note()
            note = project_training(self.root, self.master)["source_review_annotations"][0]
            self.assertEqual(note["source_state"], "stale")
            self.assertEqual(note["quote"], "Critical System")
            self.note[key] = original

    def test_missing_private_text_is_not_marked_matching(self):
        self.bundle_path.unlink()
        note = project_training(self.root, self.master)["source_review_annotations"][0]
        self.assertEqual(note["source_state"], "text_unavailable")

    def test_fabricated_excerpt_is_rejected(self):
        self.note["quote"] = "not in this source"
        self.write_note()
        with self.assertRaisesRegex(MasterTopicPackError, "quote"):
            project_training(self.root, self.master)


if __name__ == "__main__":
    unittest.main()
