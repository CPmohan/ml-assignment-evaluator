"""Create a first-pass, provisional grading report for Arya only.

No score is inferred from extracted text, OCR, evidence_role, or a missing
evidence field. A score can appear only from an explicit human-review record.
"""

from pathlib import Path
import json


RUBRIC_PATH = Path("provisional_10_mark_rubric.json")
EVIDENCE_REPORT_PATH = Path(
    "outputs/mentor_review_sample/"
    "AryaR_AM_En_P2GEO23002_Assignment1_prototype_report.json"
)
OUTPUT_DIR = Path("outputs/mentor_review_sample")
EXPECTED_ASSIGNMENT = "AryaR_AM_En_P2GEO23002_Assignment1.pdf"


def load_json_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in: {path}")
    return data


def approved_score(
    evidence: list[dict],
    maximum_marks: int | float | None,
) -> int | float | None:
    """Return only an explicitly reviewer-supplied, verified score."""
    if maximum_marks is None:
        return None

    reviewed_items = [
        item
        for item in evidence
        if isinstance(item, dict)
        and "reviewer_provisional_score" in item
    ]

    if len(reviewed_items) != 1:
        return None

    reviewed_item = reviewed_items[0]
    score = reviewed_item["reviewer_provisional_score"]

    if not reviewed_item.get("human_verified", False):
        return None

    if reviewed_item.get("is_ocr", False) and not reviewed_item.get(
        "visual_verification_complete", False
    ):
        return None

    # bool is a subclass of int in Python, but is never a valid mark.
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return None

    if score < 0 or score > maximum_marks:
        return None

    return score


def criterion_reason(
    evidence: list[dict],
    score: int | float | None,
) -> str:
    if not evidence:
        return (
            "Needs manual review: no matching captured evidence was found. "
            "This does not establish that the student omitted the requirement; "
            "it may be present in an image or screenshot."
        )

    # A non-null score can only come from explicit human verification, and
    # OCR evidence can reach this branch only after visual verification.
    if score is not None:
        return "Provisional score recorded from explicit human-verified evidence."

    if any(
        isinstance(item, dict) and item.get("is_ocr", False)
        for item in evidence
    ):
        return (
            "Needs manual review: OCR-derived evidence requires visual "
            "verification before it may support a provisional score."
        )

    return (
        "Needs manual review: no explicit human-reviewed score is present. "
        "'student_response_or_context' is a heuristic, not proof of an answer."
    )


def report_evidence_by_criterion(evidence_report: dict) -> dict[str, list[dict]]:
    evidence_by_name = {}

    for item in evidence_report.get("criteria", []):
        if not isinstance(item, dict):
            continue

        criterion_name = item.get("criterion")
        evidence = item.get("evidence", [])

        if isinstance(criterion_name, str) and isinstance(evidence, list):
            evidence_by_name[criterion_name] = evidence

    return evidence_by_name


def build_grading_report(evidence_report: dict, rubric: dict) -> dict:
    assignment_filename = evidence_report.get("assignment_filename")
    if assignment_filename != EXPECTED_ASSIGNMENT:
        raise ValueError(
            "This prototype is restricted to Arya's assignment only: "
            f"{EXPECTED_ASSIGNMENT}"
        )

    evidence_by_name = report_evidence_by_criterion(evidence_report)
    criteria = []

    for rubric_item in rubric.get("criteria", []):
        if not isinstance(rubric_item, dict):
            continue

        criterion_name = rubric_item.get("criterion")
        maximum_marks = rubric_item.get("max_marks")

        if not isinstance(criterion_name, str):
            continue

        evidence = evidence_by_name.get(criterion_name, [])
        score = approved_score(evidence, maximum_marks)

        criteria.append({
            "criterion": criterion_name,
            "maximum_marks": maximum_marks,
            "provisional_awarded_marks": score,
            "evidence": evidence,
            "reasoning": criterion_reason(evidence, score),
            "review_status": (
                "Provisionally scored after human verification"
                if score is not None
                else "Needs manual review"
            ),
            "manual_review_required": score is None,
        })

    unscored_items = []
    for item in evidence_report.get("unscored_items", []):
        if not isinstance(item, dict):
            continue

        unscored_items.append({
            "criterion": item.get("criterion"),
            "maximum_marks": None,
            "provisional_awarded_marks": None,
            "evidence": item.get("evidence", []),
            "reasoning": (
                "Unscored: the assignment instructions do not state a "
                "mark allocation for this item."
            ),
            "review_status": "Unscored",
            "manual_review_required": True,
        })

    all_scores_available = bool(criteria) and all(
        item["provisional_awarded_marks"] is not None
        for item in criteria
    )

    return {
        "label": "first-pass grading prototype / provisional / not mentor-approved",
        "assignment_filename": assignment_filename,
        "rubric_source": str(RUBRIC_PATH),
        "evidence_report_source": str(EVIDENCE_REPORT_PATH),
        "criteria": criteria,
        "unscored_items": unscored_items,
        "provisional_total": (
            sum(item["provisional_awarded_marks"] for item in criteria)
            if all_scores_available
            else None
        ),
        "total_status": (
            "All criteria have justified provisional scores"
            if all_scores_available
            else "Provisional total unavailable—manual review required"
        ),
        "safeguards": [
            "No marks are inferred from extracted text.",
            "OCR evidence and OCR-derived numbers require visual verification.",
            "'student_response_or_context' is not proof of an answer.",
            "Missing captured evidence is not treated as student omission.",
        ],
    }


def write_markdown(report: dict, output_path: Path) -> None:
    lines = [
        "# First-Pass Grading Prototype",
        "",
        "**Provisional / not mentor-approved.**",
        "",
        f"Assignment: `{report['assignment_filename']}`",
    ]

    for criterion in report["criteria"] + report["unscored_items"]:
        lines.extend([
            "",
            f"## {criterion['criterion']}",
            "",
            f"Maximum marks: {criterion['maximum_marks']}",
            f"Provisional awarded marks: "
            f"{criterion['provisional_awarded_marks']}",
            f"Review status: {criterion['review_status']}",
            f"Reasoning: {criterion['reasoning']}",
            "",
            "Evidence:",
        ])

        if not criterion["evidence"]:
            lines.append("- No matching captured evidence.")
            continue

        for item in criterion["evidence"]:
            if not isinstance(item, dict):
                continue

            lines.extend([
                "",
                f"- Page {item.get('page')} | source: {item.get('source')} "
                f"| visual verification needed: "
                f"{item.get('needs_visual_verification')}",
                "```text",
                item.get("snippet", ""),
                "```",
            ])

    lines.extend([
        "",
        "## Total",
        "",
        f"Provisional total: {report['provisional_total']}",
        report["total_status"],
    ])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rubric = load_json_object(RUBRIC_PATH)
    evidence_report = load_json_object(EVIDENCE_REPORT_PATH)
    report = build_grading_report(evidence_report, rubric)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / (
        "AryaR_AM_En_P2GEO23002_Assignment1_first_pass_grading.json"
    )
    markdown_path = OUTPUT_DIR / (
        "AryaR_AM_En_P2GEO23002_Assignment1_first_pass_grading.md"
    )

    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(report, markdown_path)
    print(f"Created Arya-only first-pass grading report: {markdown_path}")


if __name__ == "__main__":
    main()
