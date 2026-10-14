import unittest

from grade_one_assignment import (
    EVIDENCE_REPORT_PATH,
    RUBRIC_PATH,
    approved_score,
    build_grading_report,
    criterion_reason,
    load_json_object,
)


class GradingRulesTest(unittest.TestCase):
    def test_unconfirmed_text_evidence_cannot_receive_a_score(self):
        evidence = [{
            "source": "text_layer",
            "is_ocr": False,
            "evidence_role": "student_response_or_context",
            "answer_confirmation": "not_confirmed",
        }]

        self.assertIsNone(approved_score(evidence, 1))

    def test_ocr_evidence_requires_visual_verification(self):
        evidence = [{
            "source": "ocr",
            "is_ocr": True,
            "human_verified": True,
            "visual_verification_complete": False,
            "reviewer_provisional_score": 1,
        }]

        self.assertIsNone(approved_score(evidence, 1))

    def test_verified_text_evidence_accepts_valid_score(self):
        evidence = [{
            "source": "text_layer",
            "is_ocr": False,
            "human_verified": True,
            "reviewer_provisional_score": 1,
        }]

        self.assertEqual(approved_score(evidence, 1), 1)

    def test_verified_ocr_evidence_accepts_valid_score(self):
        evidence = [{
            "source": "ocr",
            "is_ocr": True,
            "human_verified": True,
            "visual_verification_complete": True,
            "reviewer_provisional_score": 2,
        }]

        score = approved_score(evidence, 3)
        self.assertEqual(score, 2)
        self.assertEqual(
            criterion_reason(evidence, score),
            "Provisional score recorded from explicit human-verified evidence.",
        )

    def test_boolean_values_are_not_valid_scores(self):
        evidence = [{
            "source": "text_layer",
            "is_ocr": False,
            "human_verified": True,
            "reviewer_provisional_score": True,
        }]

        self.assertIsNone(approved_score(evidence, 1))

    def test_actual_arya_report_and_rubric_load_without_schema_error(self):
        rubric = load_json_object(RUBRIC_PATH)
        evidence_report = load_json_object(EVIDENCE_REPORT_PATH)

        report = build_grading_report(evidence_report, rubric)

        self.assertEqual(
            report["assignment_filename"],
            "AryaR_AM_En_P2GEO23002_Assignment1.pdf",
        )
        self.assertEqual(len(report["criteria"]), 5)
        self.assertTrue(
            all(
                item["provisional_awarded_marks"] is None
                for item in report["criteria"]
            )
        )
        self.assertEqual(len(report["unscored_items"]), 1)
        self.assertIsNone(report["provisional_total"])
        self.assertEqual(
            report["total_status"],
            "Provisional total unavailable—manual review required",
        )


if __name__ == "__main__":
    unittest.main()
