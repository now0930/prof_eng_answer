"""Public View boundaries preserve legacy contracts and independent loading."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study import topic_views
from study.master_topic_pack import project_grading, project_training, project_diagnosis
from test_master_topic_pack_schema import _valid_record
from test_training_diagnosis_projections import _write_sources


class TopicViewsTest(unittest.TestCase):
    def test_public_views_match_existing_contracts_and_are_isolated(self):
        master = _valid_record()
        before = copy.deepcopy(master)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_sources(root, master)
            for view, legacy in (
                (topic_views.grading_view, project_grading),
                (topic_views.training_view, project_training),
                (topic_views.feedback_view, project_diagnosis),
            ):
                expected = legacy(root, master)
                result = view(root, master)
                self.assertEqual(result, expected)
                result.clear()
                self.assertEqual(view(root, master), expected)
            self.assertEqual(master, before)
            feedback = topic_views.feedback_view(root, master)
            self.assertEqual(feedback['score_effect'], 'none')
            self.assertEqual(feedback['projection_id'], 'diagnosis-projection-v1')

    def test_grading_does_not_load_learning_or_feedback(self):
        master = _valid_record()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write_sources(root, master)
            with patch.object(topic_views, 'project_training', side_effect=ValueError('unavailable')), \
                 patch.object(topic_views, 'project_diagnosis', side_effect=ValueError('unavailable')):
                self.assertEqual(topic_views.grading_view(root, master), project_grading(root, master))


if __name__ == '__main__':
    unittest.main()
