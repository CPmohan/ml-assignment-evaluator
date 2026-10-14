"""Generate provisional rubric evaluations for all prepared submissions.

This script consumes the text extracted by ``process_dataset.py``.  It never
writes final student marks: each result is an AI suggestion that must be
checked against the original PDF, especially where plots or screenshots are
present.

Usage:
    python grade_dataset.py
    python grade_dataset.py --limit 1          # connection/model smoke test
    python grade_dataset.py --force            # re-evaluate existing reports
"""

from __future__ import annotations

import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from evaluation_core import evaluate_ml_assignment_batch


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "outputs" / "dataset"
DEFAULT_OUTPUT = ROOT / "outputs" / "ai_evaluation" / "batch"


def read_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def safe_stem(filename: str) -> str:
    """Use the extracted filename's stem, which matches the evidence files."""
    return Path(filename).stem


def report_path(output_dir: Path, extracted: dict) -> Path:
    return output_dir / f"{safe_stem(extracted['filename'])}.evaluation.json"


def make_report(extracted: dict, rubric: dict) -> dict:
    results = evaluate_ml_assignment_batch(extracted, rubric)
    scores = [item.get("score") for item in results]
    possible = sum(item["max_marks"] for item in rubric["criteria"])
    all_scored = len(scores) == len(rubric["criteria"]) and all(
        score is not None for score in scores
    )
    low_text_pages = [
        page.get("page") for page in extracted.get("pages", [])
        if len(str(page.get("text", "")).strip()) < 40
    ]
    return {
        "status": "AI rubric suggestions generated — human review required",
        "assignment": extracted["filename"],
        "rubric_version": rubric.get("rubric_version", "unknown"),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "total_possible": possible,
        "score_coverage": sum(score is not None for score in scores),
        "ai_provisional_total": sum(scores) if all_scored else None,
        "criteria": results,
        "visual_review_required_pages": low_text_pages,
        "safeguards": [
            "These are AI suggestions, not final grades.",
            "A reviewer must check cited evidence in the original PDF.",
            "Plots, screenshots, and image-only pages require visual verification.",
        ],
    }


def write_summary(rows: list[dict], output_dir: Path) -> Path:
    path = output_dir / "grading_summary.csv"
    fields = [
        "assignment", "status", "ai_provisional_total", "total_possible",
        "score_coverage", "visual_review_pages", "report", "error",
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create provisional AI rubric evaluations for prepared submissions."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--rubric", type=Path, default=ROOT / "rubric.json")
    parser.add_argument("--limit", type=int, help="Evaluate only the first N submissions.")
    parser.add_argument(
        "--workers", type=int, default=2,
        help="Concurrent model requests (default: 2; use 1 for strictly sequential grading).",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing evaluation reports.")
    parser.add_argument(
        "--retry-unscored", action="store_true",
        help="Re-evaluate only reports whose existing score coverage is incomplete.",
    )
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    load_dotenv(ROOT / ".env")
    rubric = read_object(args.rubric)
    files = sorted(args.input_dir.glob("*.extracted.json"))
    if args.limit:
        files = files[:args.limit]
    if not files:
        raise SystemExit(f"No extracted submissions found in {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary: list[dict] = []
    pending: list[Path] = []
    for input_path in files:
        try:
            extracted = read_object(input_path)
            target = report_path(args.output_dir, extracted)
            if target.exists():
                existing = read_object(target)
                complete = existing.get("score_coverage") == len(rubric["criteria"])
                if args.retry_unscored and not complete:
                    pending.append(input_path)
                    continue
                if args.force:
                    pending.append(input_path)
                    continue
                summary.append({
                    "assignment": extracted["filename"], "status": "Skipped (already evaluated)",
                    "ai_provisional_total": existing.get("ai_provisional_total"),
                    "total_possible": existing.get("total_possible"),
                    "score_coverage": existing.get("score_coverage"),
                    "visual_review_pages": ";".join(map(str, existing.get("visual_review_required_pages", []))),
                    "report": str(target.relative_to(ROOT)), "error": "",
                })
                print(f"Skipped: {extracted['filename']}")
                continue
        except Exception as error:
            filename = input_path.name.removesuffix(".extracted.json")
            summary.append({
                "assignment": filename, "status": "Failed", "ai_provisional_total": "",
                "total_possible": "", "score_coverage": "", "visual_review_pages": "",
                "report": "", "error": str(error),
            })
            print(f"  Failed: {error}")
        else:
            pending.append(input_path)

    def grade_file(input_path: Path) -> dict:
        extracted = read_object(input_path)
        target = report_path(args.output_dir, extracted)
        report = make_report(extracted, rubric)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "assignment": extracted["filename"], "status": report["status"],
            "ai_provisional_total": report["ai_provisional_total"],
            "total_possible": report["total_possible"],
            "score_coverage": report["score_coverage"],
            "visual_review_pages": ";".join(map(str, report["visual_review_required_pages"])),
            "report": str(target.relative_to(ROOT)), "error": "",
        }

    if pending:
        print(f"Evaluating {len(pending)} submission(s) with {args.workers} concurrent request(s).")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(grade_file, path): path for path in pending}
            for number, future in enumerate(as_completed(futures), start=1):
                source = futures[future]
                try:
                    row = future.result()
                    print(
                        f"[{number}/{len(pending)}] {row['assignment']}: "
                        f"{row['ai_provisional_total']}/{row['total_possible']}"
                    )
                except Exception as error:
                    row = {
                        "assignment": source.name.removesuffix(".extracted.json"),
                        "status": "Failed", "ai_provisional_total": "", "total_possible": "",
                        "score_coverage": "", "visual_review_pages": "", "report": "",
                        "error": str(error),
                    }
                    print(f"[{number}/{len(pending)}] Failed: {source.name}: {error}")
                summary.append(row)

    summary_path = write_summary(summary, args.output_dir)
    completed = sum(row["status"].startswith("AI rubric") for row in summary)
    failed = sum(row["status"] == "Failed" for row in summary)
    print(f"\nCompleted: {completed}; failed: {failed}; summary: {summary_path}")
    print("All totals are provisional and require human approval before use.")


if __name__ == "__main__":
    main()
