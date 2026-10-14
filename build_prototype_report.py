"""Create one mentor-reviewable, evidence-only prototype report.

This script does not grade assignments. It converts organized evidence into a
provisional review report and withholds marks until a human verifies evidence.
"""

from pathlib import Path
import json


RUBRIC_PATH = Path("provisional_10_mark_rubric.json")
ORGANIZED_DIR = Path("outputs/organized")
REPORT_DIR = Path("outputs/mentor_review_sample")
SAMPLE_FILE = ORGANIZED_DIR / "AryaR_AM_En_P2GEO23002_Assignment1.json"


def select_evidence(items: list[dict], limit: int = 4) -> list[dict]:
    """Keep exact evidence records, prioritizing page order without correction."""
    records = [item for item in items if isinstance(item, dict)]
    return sorted(records, key=lambda item: (item.get("page", 0), item.get("source", "")))[:limit]


def criterion_record(
    criterion: dict,
    evidence: list[dict],
    *,
    unscored: bool = False,
) -> dict:
    has_ocr = any(item.get("is_ocr") for item in evidence)

    if unscored:
        reason = "Unscored: the assignment instructions do not state a mark allocation."
    elif not evidence:
        reason = (
            "Needs manual review: no matching captured evidence was found. "
            "This does not establish that the student omitted the requirement; "
            "it may be in an image or screenshot."
        )
    elif has_ocr:
        reason = (
            "Needs manual review: OCR-derived evidence requires visual "
            "verification before it can support a score."
        )
    else:
        reason = (
            "Needs manual review: captured text is evidence for review, not "
            "confirmation that the requirement was completed or correct."
        )

    return {
        "criterion": criterion["criterion"],
        "maximum_marks": criterion.get("max_marks"),
        "evidence": evidence,
        "provisional_score": None,
        "score_status": "Unscored" if unscored else "Needs manual review",
        "reason_and_uncertainty": reason,
        "manual_review_required": True,
    }


def build_report(organized: dict, rubric: dict) -> dict:
    metrics = organized.get("metrics", {})
    metric_evidence = []
    if isinstance(metrics, dict):
        for metric_name in ("MAE", "MSE", "MAPE"):
            metric_evidence.extend(metrics.get(metric_name, []))

    evidence_by_id = {
        "section_a": select_evidence(organized.get("section_a", [])),
        "scatter_analysis": select_evidence(organized.get("scatter_analysis", [])),
        "sample_count": select_evidence(organized.get("sample_count", [])),
        "train_test_split": select_evidence(organized.get("train_test_split", [])),
        "metrics": select_evidence(metric_evidence),
        "reflection": select_evidence(organized.get("reflection", [])),
    }

    criteria = [
        criterion_record(criterion, evidence_by_id[criterion["id"]])
        for criterion in rubric.get("criteria", [])
    ]
    unscored = [
        criterion_record(
            criterion,
            evidence_by_id[criterion["id"]],
            unscored=True,
        )
        for criterion in rubric.get("unscored_items", [])
    ]

    return {
        "label": "prototype / provisional rubric / not mentor-approved",
        "assignment_filename": organized.get("filename"),
        "rubric_source": str(RUBRIC_PATH),
        "criteria": criteria,
        "unscored_items": unscored,
        "provisional_total": None,
        "total_status": "Needs manual review",
        "total_reason": (
            "No total is calculated because captured and OCR evidence has not "
            "been confirmed by human review."
        ),
        "evidence_gaps": organized.get("evidence_gaps", []),
        "ocr_review_items": organized.get("uncertain_ocr_evidence", []),
    }


def write_markdown(report: dict, output_path: Path) -> None:
    lines = [
        "# Prototype Assignment Review",
        "",
        "**Prototype / provisional rubric / not mentor-approved.**",
        "",
        f"Assignment: `{report['assignment_filename']}`",
        "",
        "No marks or total have been assigned automatically. Every criterion "
        "requires human review before a score is recorded.",
    ]

    for item in report["criteria"] + report["unscored_items"]:
        lines.extend([
            "",
            f"## {item['criterion']}",
            "",
            f"Maximum marks: {item['maximum_marks']}",
            f"Status: {item['score_status']}",
            f"Provisional score: {item['provisional_score']}",
            f"Reason: {item['reason_and_uncertainty']}",
        ])

        if item["evidence"]:
            lines.append("")
            lines.append("Evidence for review:")
            for evidence in item["evidence"]:
                lines.extend([
                    "",
                    f"- Page {evidence.get('page')} | source: {evidence.get('source')} "
                    f"| visual verification: {evidence.get('needs_visual_verification')}",
                    "```text",
                    evidence.get("snippet", ""),
                    "```",
                ])

    lines.extend([
        "",
        "## Total",
        "",
        f"Provisional total: {report['provisional_total']}",
        f"Status: {report['total_status']}",
        report["total_reason"],
    ])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not SAMPLE_FILE.is_file():
        raise FileNotFoundError(f"Organized sample not found: {SAMPLE_FILE}")

    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    organized = json.loads(SAMPLE_FILE.read_text(encoding="utf-8"))
    report = build_report(organized, rubric)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"{SAMPLE_FILE.stem}_prototype_report.json"
    markdown_path = REPORT_DIR / f"{SAMPLE_FILE.stem}_prototype_report.md"

    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(report, markdown_path)
    print(f"Created prototype report: {markdown_path}")
    print("Assignment reports created=1; no automatic marks or total assigned.")


if __name__ == "__main__":
    main()
