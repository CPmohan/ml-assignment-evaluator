"""Prepare evidence-only reports for every PDF in data/assignments."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pymupdf

from organize_sections import organize_file


ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / "data" / "assignments"
OUT_DIR = ROOT / "outputs" / "dataset"
HUMAN_CSV = ROOT / "data" / "human_marks.csv"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDF submissions found in {PDF_DIR}")

    summary = []
    for pdf in pdfs:
        try:
            with pymupdf.open(pdf) as document:
                pages = [{"page": i, "text": page.get_text("text").strip(),
                          "image_count": len(page.get_images(full=True))}
                         for i, page in enumerate(document, start=1)]
            extracted = {"filename": pdf.name, "page_count": len(pages), "pages": pages,
                         "text": "\n\n".join(page["text"] for page in pages)}
            low_text = [p["page"] for p in pages if len(p["text"]) < 40]
            image_pages = [p["page"] for p in pages if p["image_count"]]
            raw_path = OUT_DIR / f"{pdf.stem}.extracted.json"
            raw_path.write_text(json.dumps(extracted, ensure_ascii=False, indent=2), encoding="utf-8")
            evidence_path = OUT_DIR / f"{pdf.stem}.evidence.json"
            evidence_path.write_text(json.dumps(organize_file(raw_path), ensure_ascii=False, indent=2), encoding="utf-8")
            summary.append({"filename": pdf.name, "pages": len(pages),
                            "extracted_characters": len(extracted["text"]),
                            "low_text_pages": ";".join(map(str, low_text)),
                            "image_pages": ";".join(map(str, image_pages)),
                            "status": "Evidence prepared; no score assigned"})
            print(f"Prepared evidence: {pdf.name} ({len(pages)} pages)")
        except Exception as error:
            summary.append({"filename": pdf.name, "pages": "", "extracted_characters": "",
                            "low_text_pages": "", "image_pages": "", "status": f"Failed: {error}"})
            print(f"Failed: {pdf.name}: {error}")

    summary_csv = OUT_DIR / "submission_inventory.csv"
    with summary_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filename", "pages", "extracted_characters", "low_text_pages", "image_pages", "status"])
        writer.writeheader()
        writer.writerows(summary)
    (OUT_DIR / "dataset_summary.json").write_text(json.dumps({
        "submission_count": len(pdfs),
        "evidence_prepared": sum(row["status"].startswith("Evidence prepared") for row in summary),
        "ai_scores_generated": 0,
        "human_scores_available": 0,
        "human_marks_csv": str(HUMAN_CSV.relative_to(ROOT)),
        "note": "An input PDF count is not an evaluation count. Scores require AI runs and human verification.",
    }, indent=2), encoding="utf-8")
    print(f"\nSubmissions found: {len(pdfs)}")
    print(f"Evidence prepared: {sum(row['status'].startswith('Evidence prepared') for row in summary)}")
    print("Scores assigned: 0 (evidence preparation is not grading)")
    print(f"Inventory: {summary_csv}")


if __name__ == "__main__":
    main()
