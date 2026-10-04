import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from study.review_presentation import source_review_lines


class ReviewPresentationTest(unittest.TestCase):
    def test_html_source_and_pending_notes_preserve_input(self):
        training = {
            "source_materials": [{"title": "HTML", "text": "원문 " * 200,
                                  "source_url": "https://example.com/post"}],
            "source_review_annotations": [dict(status="pending_review", score_effect="none",
                source_state=state, quote="인용", locator="1절", review_note="미확정 의견")
                for state in ("matching", "stale", "text_unavailable")],
        }
        before = copy.deepcopy(training)
        output = "\n".join(source_review_lines(training))
        self.assertIn("채점 기준 아님", output)
        self.assertIn("이전 원문 기준", output)
        self.assertIn("주석 1건 추가", output)
        self.assertLess(len(output), 1200)
        self.assertEqual(training, before)

    def test_no_raw_bundle_fallback(self):
        self.assertEqual(source_review_lines({"wordpress_topic_pack": {
            "sources": [{"extracted_text": "unlinked raw text"}]}}), [])
        self.assertEqual(source_review_lines({"source_materials": None,
                                             "source_review_annotations": None}), [])

    def test_unavailable_and_unapproved_comments(self):
        output = "\n".join(source_review_lines({"source_review_annotations": [
            dict(status="pending_review", score_effect="none", source_state="text_unavailable"),
            dict(status="approved", score_effect="none", review_note="DO NOT DISPLAY"),
        ]}))
        self.assertIn("원문 확인 불가", output)
        self.assertNotIn("DO NOT DISPLAY", output)


if __name__ == "__main__":
    unittest.main()
