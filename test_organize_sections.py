import json
from pathlib import Path
import unittest
from unittest.mock import patch

from organize_sections import (
    INPUT_DIR,
    OCR_MARKER,
    find_matches,
    organize_file,
    split_page_sources,
)


class OrganizeSectionsUnitTest(unittest.TestCase):
    def test_preserves_source_without_ocr_marker(self):
        page = {
            "page": 1,
            "source": "custom_source",
            "text": "A page with regular extracted text.",
        }

        segments = split_page_sources(page)

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["source"], "custom_source")
        self.assertFalse(segments[0]["is_ocr"])
        self.assertEqual(segments[0]["text"], page["text"])

    def test_evidence_never_confirms_an_answer(self):
        text_layer_page = {
            "page": 1,
            "source": "text_layer",
            "text": "Answer: the dataset has 414 samples.",
        }
        ocr_page = {
            "page": 2,
            "source": "text_layer+ocr",
            "text": (
                "Page 2\n"
                f"{OCR_MARKER}\n"
                "Answer: the dataset has 414 samples."
            ),
        }

        segments = (
            split_page_sources(text_layer_page)
            + split_page_sources(ocr_page)
        )
        evidence_items = find_matches(
            segments,
            [r"\bsamples\b"],
            "sample_count",
        )

        self.assertTrue(evidence_items)
        self.assertEqual(
            {item["source"] for item in evidence_items},
            {"text_layer", "ocr"},
        )
        self.assertTrue(
            all(
                item["answer_confirmation"] == "not_confirmed"
                for item in evidence_items
            )
        )

    def test_organize_file_never_confirms_generated_evidence(self):
        merged_data = {
            "filename": "temporary-assignment.pdf",
            "pages": [
                {
                    "page": 1,
                    "source": "text_layer",
                    "text": (
                        "Section A\n"
                        "Answer: the dataset has 414 samples.\n"
                        "I chose a 70:30 train-test split."
                    ),
                },
                {
                    "page": 2,
                    "source": "text_layer+ocr",
                    "text": (
                        "Page 2\n"
                        f"{OCR_MARKER}\n"
                        "Scatter plot: I think X3 is a better predictor.\n"
                        "MAE: 10.2"
                    ),
                },
            ],
        }

        # Model a temporary merged JSON file in memory. This keeps the test
        # independent of restricted temporary-directory permissions.
        temporary_file = Path("temporary-merged.json")
        with patch.object(Path, "read_text", return_value=json.dumps(merged_data)):
            result = organize_file(temporary_file)

        evidence_items = []
        for field_name in (
            "section_a",
            "scatter_analysis",
            "sample_count",
            "train_test_split",
            "reflection",
            "uncertain_ocr_evidence",
        ):
            evidence_items.extend(result[field_name])

        for metric_items in result["metrics"].values():
            evidence_items.extend(metric_items)

        self.assertTrue(evidence_items)
        self.assertTrue(
            all(
                item["answer_confirmation"] == "not_confirmed"
                for item in evidence_items
            )
        )


class NamithaMergedOcrTest(unittest.TestCase):
    def test_namitha_ocr_metric_evidence_is_page_linked_and_unverified(self):
        matches = list(INPUT_DIR.glob("Namitha*.json"))
        self.assertEqual(len(matches), 1, "Expected one Namitha merged JSON file")

        merged_file = matches[0]
        merged_data = json.loads(merged_file.read_text(encoding="utf-8"))
        result = organize_file(merged_file)

        ocr_text_by_page = {}
        for page in merged_data.get("pages", []):
            if not isinstance(page, dict):
                continue

            page_text = page.get("text", "")
            if isinstance(page_text, str) and OCR_MARKER in page_text:
                _, ocr_text = page_text.split(OCR_MARKER, maxsplit=1)
                ocr_text_by_page[page.get("page")] = ocr_text

        ocr_metric_items = [
            item
            for metric_items in result["metrics"].values()
            for item in metric_items
            if item["source"] == "ocr"
        ]

        self.assertTrue(ocr_metric_items)
        self.assertTrue(
            any(item["page"] in {7, 8, 9} for item in ocr_metric_items)
        )
        self.assertTrue(
            all(
                item["needs_visual_verification"]
                for item in ocr_metric_items
            )
        )

        for item in ocr_metric_items:
            self.assertIn(item["page"], ocr_text_by_page)
            self.assertIn(item["snippet"], ocr_text_by_page[item["page"]])


if __name__ == "__main__":
    unittest.main()
