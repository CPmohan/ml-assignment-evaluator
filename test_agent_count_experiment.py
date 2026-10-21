import unittest

from run_agent_count_experiment import aggregate_reviewers


class AgentCountAggregationTest(unittest.TestCase):
    def setUp(self):
        self.rubric = {
            "criteria": [
                {"id": "Q1", "name": "Dataset understanding", "max_marks": 1},
                {"id": "Q2", "name": "Analysis", "max_marks": 4},
            ]
        }

    def test_majority_score_and_agreement_are_reported(self):
        reviewers = [
            {"reviewer": 1, "criteria": [
                {"criterion_id": "Q1", "score": 1},
                {"criterion_id": "Q2", "score": 2},
            ]},
            {"reviewer": 2, "criteria": [
                {"criterion_id": "Q1", "score": 1},
                {"criterion_id": "Q2", "score": 3},
            ]},
            {"reviewer": 3, "criteria": [
                {"criterion_id": "Q1", "score": 0},
                {"criterion_id": "Q2", "score": 2},
            ]},
        ]

        report = aggregate_reviewers(reviewers, self.rubric)

        self.assertEqual(report["agent_count"], 3)
        self.assertEqual(report["criteria"][0]["score"], 1)
        self.assertEqual(report["criteria"][0]["agreement_votes"], 2)
        self.assertEqual(report["criteria"][1]["score"], 2)
        self.assertEqual(report["ai_provisional_total"], 3)

    def test_tied_scores_resolve_to_lower_score(self):
        reviewers = [
            {"reviewer": 1, "criteria": [{"criterion_id": "Q1", "score": 0}]},
            {"reviewer": 2, "criteria": [{"criterion_id": "Q1", "score": 1}]},
        ]

        report = aggregate_reviewers(reviewers, self.rubric)

        self.assertEqual(report["criteria"][0]["score"], 0)
        self.assertIsNone(report["ai_provisional_total"])


if __name__ == "__main__":
    unittest.main()