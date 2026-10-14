"""Organize merged assignment evidence without grading or modifying sources."""

from pathlib import Path
import json
import re


INPUT_DIR = Path("outputs/merged")
OUTPUT_DIR = Path("outputs/organized")
OCR_MARKER = "[OCR TEXT]"

SECTION_PATTERNS = {
    "section_a": [
        r"\bsection\s*a\b",
        r"how\s+many\s+samples",
        r"input\s+variables",
        r"target\s+outcome",
        r"input\s+columns?\s+mean",
    ],
    "scatter_analysis": [
        r"scatter\s*plot",
        r"better\s+(?:in\s+)?predicting",
        r"better\s+predictor",
        r"clear\s+trend",
        r"regression\s+line",
    ],
    "reflection": [
        r"three\s+new\s+things",
        r"what.*learned",
        r"\blearned\b",
    ],
}

METRIC_PATTERNS = {
    "MAE": r"\bMAE\b|mean\s+absolute\s+error",
    "MSE": r"\bMSE\b|mean\s+squared\s+error",
    "MAPE": r"\bMAPE\b|mean\s+absolute\s+percentage\s+error",
}

INSTRUCTION_SIGNALS = [
    r"\bhow\s+many\b",
    r"\bwhat\s+(?:is|are)\b",
    r"\bwhich\b",
    r"\bwrite\s+code\b",
    r"\bevaluate\b",
    r"\byou\s+(?:need|should|have)\b",
    r"\bfor\s+each\b",
]

RESPONSE_SIGNALS = [
    r"\bans(?:wer)?\s*[:=]",
    r"\bi\s+(?:think|chose|learned)\b",
    r"\bmy\b",
    r"\bprint\s*\(",
    r"\bMAE\s+[-+]?\d",
    r"\bMSE\s+[-+]?\d",
    r"\bMAPE\s+[-+]?\d",
]


def split_page_sources(page: dict) -> list[dict]:
    """Separate text-layer and appended OCR content without changing it."""
    text = page.get("text", "")
    if not isinstance(text, str):
        return []

    page_number = page.get("page")
    if OCR_MARKER not in text:
        return [{
            "page": page_number,
            "source": page.get("source", "text_layer"),
            "is_ocr": False,
            "text": text,
        }]

    text_layer, ocr_text = text.split(OCR_MARKER, maxsplit=1)
    return [
        {
            "page": page_number,
            "source": "text_layer",
            "is_ocr": False,
            "text": text_layer,
        },
        {
            "page": page_number,
            "source": "ocr",
            "is_ocr": True,
            "text": ocr_text,
        },
    ]


def role_for_context(context: str) -> str:
    """Return a cautious detection label, never a conclusion about an answer.

    ``student_response_or_context`` is not confirmation that text is a student
    answer and must not be used to grade or score work.
    """
    has_instruction = any(
        re.search(pattern, context, flags=re.IGNORECASE)
        for pattern in INSTRUCTION_SIGNALS
    )
    has_response = any(
        re.search(pattern, context, flags=re.IGNORECASE)
        for pattern in RESPONSE_SIGNALS
    )

    if has_instruction and not has_response:
        return "possibly_instruction"
    return "student_response_or_context"


def make_evidence(
    segment: dict,
    match: re.Match,
    label: str,
    before: int = 180,
    after: int = 500,
) -> dict:
    """Create page-linked evidence while preserving the selected text exactly."""
    text = segment["text"]
    start = max(0, match.start() - before)
    end = min(len(text), match.end() + after)
    snippet = text[start:end]

    return {
        "label": label,
        "page": segment["page"],
        "source": segment["source"],
        "is_ocr": segment["is_ocr"],
        "needs_visual_verification": segment["is_ocr"],
        "evidence_role": role_for_context(snippet),
        "answer_confirmation": "not_confirmed",
        "snippet": snippet,
    }


def find_matches(
    segments: list[dict], patterns: list[str], label: str
) -> list[dict]:
    results = []

    for segment in segments:
        for pattern in patterns:
            for match in re.finditer(pattern, segment["text"], re.IGNORECASE):
                item = make_evidence(segment, match, label)
                item["matched_pattern"] = pattern
                results.append(item)

    return results


def find_sample_count(segments: list[dict]) -> list[dict]:
    results = []

    for segment in segments:
        for match in re.finditer(
            r"\b(\d+)\s+samples\b", segment["text"], re.IGNORECASE
        ):
            item = make_evidence(segment, match, "sample_count")
            item["value"] = match.group(1)
            item["uncertain"] = (
                item["evidence_role"] == "possibly_instruction"
            )
            results.append(item)

    return results


def find_train_test_split(segments: list[dict]) -> list[dict]:
    results = []
    ratio_pattern = r"\b\d{1,2}\s*[:/-]\s*\d{1,2}\b"
    context_pattern = r"train.?test|training|testing|split|test\s+size"

    for segment in segments:
        text = segment["text"]

        for match in re.finditer(ratio_pattern, text, re.IGNORECASE):
            start = max(0, match.start() - 160)
            end = min(len(text), match.end() + 160)
            nearby_context = text[start:end]

            if not re.search(context_pattern, nearby_context, re.IGNORECASE):
                continue

            item = make_evidence(segment, match, "train_test_split")
            item["value"] = match.group(0)
            item["uncertain"] = (
                item["evidence_role"] == "possibly_instruction"
            )
            results.append(item)

    return results


def find_metrics(segments: list[dict]) -> dict:
    """Find metrics; parse values only when on the same source line."""
    metrics = {"MAE": [], "MSE": [], "MAPE": []}
    number = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?%?"

    for metric, pattern in METRIC_PATTERNS.items():
        for segment in segments:
            text = segment["text"]

            for match in re.finditer(pattern, text, re.IGNORECASE):
                item = make_evidence(segment, match, metric, before=100, after=350)

                line_start = text.rfind("\n", 0, match.start()) + 1
                line_end = text.find("\n", match.end())
                if line_end == -1:
                    line_end = len(text)

                line = text[line_start:line_end]
                item["line_or_table_context"] = line

                match_end_in_line = match.end() - line_start
                text_after_metric = line[match_end_in_line:]
                value_match = re.match(
                    rf"(?:\s*[:=]\s*|\s+)({number})(?![\w.])",
                    text_after_metric,
                    re.IGNORECASE,
                )

                if value_match:
                    item["value"] = value_match.group(1)
                    item["needs_review"] = item["is_ocr"]
                else:
                    item["value"] = None
                    item["needs_review"] = True

                if item["evidence_role"] == "possibly_instruction":
                    item["needs_review"] = True

                metrics[metric].append(item)

    return metrics


def collect_uncertain_ocr_evidence(
    section_fields: dict, metrics: dict
) -> list[dict]:
    """Collect all OCR-derived evidence because it requires visual review."""
    items = []

    for evidence_items in section_fields.values():
        items.extend(
            {
                **item,
                "reason": "OCR-derived evidence requires visual verification.",
            }
            for item in evidence_items
            if item["is_ocr"]
        )

    for metric_items in metrics.values():
        items.extend(
            {
                **item,
                "reason": (
                    "OCR-derived metric evidence requires visual verification; "
                    "the displayed value may be unclear."
                ),
            }
            for item in metric_items
            if item["is_ocr"]
        )

    return items


def build_evidence_gaps(section_fields: dict, metrics: dict) -> list[str]:
    """Describe missing captured evidence without inferring student omission."""
    gaps = []

    for field_name, items in section_fields.items():
        if not items:
            gaps.append(
                f"No captured text matched {field_name}. This does not show "
                "that the student omitted it; it may be in an image or screenshot."
            )

    for metric, items in metrics.items():
        explicit_values = [
            item for item in items
            if item["value"] is not None
            and item["evidence_role"] != "possibly_instruction"
        ]
        if not explicit_values:
            gaps.append(
                f"No explicit {metric} value was confidently linked to captured "
                "text. It may be in an image or require visual OCR review."
            )

    return gaps


def organize_file(json_file: Path) -> dict:
    """Organize one merged JSON file without modifying the source file."""
    data = json.loads(json_file.read_text(encoding="utf-8"))
    pages = data.get("pages", [])

    segments = []
    if isinstance(pages, list):
        for page in pages:
            if isinstance(page, dict):
                segments.extend(split_page_sources(page))

    section_fields = {
        "section_a": find_matches(
            segments, SECTION_PATTERNS["section_a"], "section_a"
        ),
        "scatter_analysis": find_matches(
            segments, SECTION_PATTERNS["scatter_analysis"], "scatter_analysis"
        ),
        "sample_count": find_sample_count(segments),
        "train_test_split": find_train_test_split(segments),
        "reflection": find_matches(
            segments, SECTION_PATTERNS["reflection"], "reflection"
        ),
    }
    metrics = find_metrics(segments)

    return {
        "filename": data.get("filename", json_file.name),
        **section_fields,
        "metrics": metrics,
        "evidence_gaps": build_evidence_gaps(section_fields, metrics),
        "uncertain_ocr_evidence": collect_uncertain_ocr_evidence(
            section_fields, metrics
        ),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_files = sorted(INPUT_DIR.glob("*.json"))

    if not json_files:
        print(f"No merged JSON files found in: {INPUT_DIR.resolve()}")
        return

    processed = 0
    failed = 0

    for json_file in json_files:
        try:
            result = organize_file(json_file)
            output_path = OUTPUT_DIR / json_file.name
            output_path.write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            processed += 1
            print(
                f"{result['filename']}: "
                f"metric references="
                f"{sum(len(items) for items in result['metrics'].values())}, "
                f"OCR review items="
                f"{len(result['uncertain_ocr_evidence'])}"
            )
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
            failed += 1
            print(f"{json_file.name}: skipped ({error})")

    print(
        f"Organized files saved to: {OUTPUT_DIR.resolve()} "
        f"(processed={processed}, failed={failed})"
    )


if __name__ == "__main__":
    main()
