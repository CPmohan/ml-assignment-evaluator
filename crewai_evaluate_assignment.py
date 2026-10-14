"""Evaluate any U1A1 Linear Regression PDF from the command line.

Usage: python crewai_evaluate_assignment.py path/to/submission.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pymupdf
from dotenv import load_dotenv

from evaluation_core import evaluate_ml_assignment


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate an ML assignment PDF with the U1A1 rubric.")
    parser.add_argument("pdf", type=Path, help="Path to one assignment PDF")
    parser.add_argument("--rubric", type=Path, default=ROOT / "rubric.json", help="Rubric JSON (defaults to project rubric)")
    args = parser.parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise SystemExit("This evaluator currently accepts PDF assignments.")

    load_dotenv(ROOT / ".env")
    rubric = json.loads(args.rubric.read_text(encoding="utf-8"))
    with pymupdf.open(pdf_path) as document:
        pages = [{"page": number, "text": page.get_text("text").strip()}
                 for number, page in enumerate(document, start=1)]
    if not any(page["text"] for page in pages):
        raise SystemExit("No selectable PDF text was found. OCR is not enabled; review or OCR this PDF first.")

    extracted = {"filename": pdf_path.name, "page_count": len(pages), "pages": pages}
    results = evaluate_ml_assignment(extracted, rubric)
    possible = sum(item["max_marks"] for item in rubric["criteria"])
    available = [item["score"] for item in results]
    total = sum(available) if all(score is not None for score in available) else None
    report = {
        "status": "AI rubric suggestions — human review required",
        "assignment": pdf_path.name,
        "rubric_version": rubric.get("rubric_version"),
        "criteria_count": len(results),
        "score_coverage": sum(score is not None for score in available),
        "ai_provisional_total": total,
        "total_possible": possible,
        "criteria": results,
        "visual_review_required_pages": [page["page"] for page in pages if len(page["text"]) < 40],
    }

    content_id = hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:12]
    output_dir = ROOT / "outputs" / "ai_evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{pdf_path.stem}_{content_id}_cli.json"
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Assignment: {pdf_path.name}")
    for item in results:
        print(f"{item['criterion_id']} {item['criterion_name']}: {item['score']}/{item['max_score']} — {item.get('decision')}")
    print(f"AI-proposed total: {total}/{possible}" if total is not None else "Total withheld: one or more criteria could not be scored reliably.")
    print(f"Saved provisional evaluation: {output_path}")
    print("A human reviewer must verify the source PDF and approve all marks.")


if __name__ == "__main__":
    main()
