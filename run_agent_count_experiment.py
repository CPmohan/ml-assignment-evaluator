"""Run a nested, multi-reviewer comparison on one assignment PDF.

Each reviewer is an independent seeded Ollama evaluation request. Results for
N reviewers aggregate the first N reviewer outputs, so every larger group
contains the same baseline reviewers as the preceding group.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pymupdf
from dotenv import load_dotenv

from evaluation_core import evaluate_ml_assignment


ROOT = Path(__file__).resolve().parent
DEFAULT_PDF = ROOT / "data" / "assignments" / "AarathyU1A1- Linear Regression 1.pdf"
DEFAULT_RUBRIC = ROOT / "rubric.json"


def safe_stem(filename: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", Path(filename).stem).strip("_") or "assignment"


def aggregate_reviewers(reviewers: list[dict], rubric: dict) -> dict:
    """Build per-criterion majority scores and agreement from reviewer outputs."""
    criteria = []
    for rubric_item in rubric["criteria"]:
        criterion_id = rubric_item["id"]
        votes = []
        for reviewer in reviewers:
            match = next(
                (item for item in reviewer["criteria"] if item["criterion_id"] == criterion_id),
                None,
            )
            if match is not None and isinstance(match.get("score"), int):
                votes.append((reviewer["reviewer"], match))

        counts = Counter(item["score"] for _, item in votes)
        consensus_score = None
        selected = None
        if counts:
            highest_vote_count = max(counts.values())
            consensus_score = min(
                score for score, count in counts.items() if count == highest_vote_count
            )
            selected = next(item for _, item in votes if item["score"] == consensus_score)

        score_values = [item["score"] for _, item in votes]
        criteria.append({
            **(selected or {}),
            "criterion_id": criterion_id,
            "criterion_name": rubric_item["name"],
            "max_score": rubric_item["max_marks"],
            "score": consensus_score,
            "reviewer_scores": [
                {"reviewer": reviewer_id, "score": item["score"]}
                for reviewer_id, item in votes
            ],
            "agreement_votes": counts.get(consensus_score, 0) if consensus_score is not None else 0,
            "valid_votes": len(votes),
            "agreement_ratio": (
                counts.get(consensus_score, 0) / len(votes) if votes and consensus_score is not None else 0.0
            ),
            "score_range": [min(score_values), max(score_values)] if score_values else None,
        })

    all_scored = bool(criteria) and all(item["score"] is not None for item in criteria)
    total = sum(item["score"] for item in criteria) if all_scored else None
    max_total = sum(item["max_score"] for item in criteria)
    overall_agreement = (
        sum(item["agreement_ratio"] for item in criteria) / len(criteria)
        if criteria else 0.0
    )
    return {
        "agent_count": len(reviewers),
        "aggregation": "per-criterion mode; ties resolve to the lower score",
        "ai_provisional_total": total,
        "total_possible": max_total,
        "overall_criterion_agreement": overall_agreement,
        "criteria": criteria,
    }


def make_count_report(metadata: dict, reviewers: list[dict], rubric: dict) -> dict:
    aggregate = aggregate_reviewers(reviewers, rubric)
    return {
        "status": "AI suggestions — human review required",
        "experiment_id": metadata["experiment_id"],
        "assignment": metadata["assignment"],
        "assignment_sha256": metadata["assignment_sha256"],
        "rubric_version": rubric.get("rubric_version"),
        "model": metadata["model"],
        "temperature": metadata["temperature"],
        "reviewers": reviewers,
        **aggregate,
        "visual_review_required_pages": metadata["visual_review_required_pages"],
        "limitations": [
            "Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.",
            "Reviewer agreement is not evidence of correctness or human agreement.",
            "A human must verify cited evidence and image-only content against the original PDF.",
        ],
    }


def markdown_report(report: dict) -> str:
    lines = [
        f"# {report['agent_count']}-Reviewer Evaluation",
        "",
        f"- Assignment: `{report['assignment']}`",
        f"- Model: `{report['model']}`",
        f"- Seeded independent requests: {report['agent_count']}",
        f"- Aggregation: {report['aggregation']}",
        f"- AI provisional total: {report['ai_provisional_total']} / {report['total_possible']}",
        f"- Mean per-criterion reviewer agreement: {report['overall_criterion_agreement']:.1%}",
        "",
        "AI suggestions only; a human reviewer must verify every score against the PDF.",
        "",
        "| Criterion | Consensus | Reviewer scores | Agreement | Range |",
        "|---|---:|---|---:|---:|",
    ]
    for item in report["criteria"]:
        score = item["score"] if item["score"] is not None else "unscored"
        scores = ", ".join(
            f"{vote['reviewer']}: {vote['score']}" for vote in item["reviewer_scores"]
        ) or "none"
        score_range = "n/a" if item["score_range"] is None else "–".join(map(str, item["score_range"]))
        lines.append(
            f"| {item['criterion_id']} {item['criterion_name']} | {score}/{item['max_score']} "
            f"| {scores} | {item['agreement_ratio']:.0%} | {score_range} |"
        )
        lines.extend([
            "",
            f"**Decision:** {item.get('decision', 'Cannot Verify')}",
            f"**Feedback:** {item.get('feedback', '')}",
            f"**Limitations:** {item.get('limitations', '')}",
        ])
        for evidence in item.get("evidence", []):
            lines.append(f"- Evidence, page {evidence.get('page')}: {evidence.get('text', '')}")
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    return "\n".join(lines) + "\n"


def save_count_report(report: dict, output_dir: Path) -> tuple[Path, Path]:
    count = report["agent_count"]
    json_path = output_dir / f"agent_count_{count}.json"
    markdown_path = output_dir / f"agent_count_{count}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(markdown_report(report), encoding="utf-8")
    return json_path, markdown_path


def save_comparison(reports: list[dict], output_dir: Path) -> tuple[Path, Path]:
    csv_path = output_dir / "agent_count_comparison.csv"
    markdown_path = output_dir / "agent_count_comparison.md"
    criterion_ids = [item["criterion_id"] for item in reports[0]["criteria"]]
    fields = ["agent_count", "ai_provisional_total", "total_possible", "overall_criterion_agreement"]
    fields.extend(f"{criterion_id}_consensus" for criterion_id in criterion_ids)
    fields.extend(f"{criterion_id}_scores" for criterion_id in criterion_ids)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for report in reports:
            row = {
                "agent_count": report["agent_count"],
                "ai_provisional_total": report["ai_provisional_total"],
                "total_possible": report["total_possible"],
                "overall_criterion_agreement": report["overall_criterion_agreement"],
            }
            for criterion in report["criteria"]:
                row[f"{criterion['criterion_id']}_consensus"] = criterion["score"]
                row[f"{criterion['criterion_id']}_scores"] = ",".join(
                    str(vote["score"]) for vote in criterion["reviewer_scores"]
                )
            writer.writerow(row)

    lines = [
        "# Agent-Count Comparison",
        "",
        f"Assignment: `{reports[0]['assignment']}`",
        "",
        "Counts are nested: each row adds one seeded reviewer to the preceding row.",
        "Consensus is the per-criterion mode; tied modes resolve to the lower score.",
        "The 1-reviewer agreement value is 100% by definition and is not inter-reviewer agreement.",
        "",
        "| Reviewers | Provisional total | Mean criterion agreement | "
        + " | ".join(criterion_ids) + " |",
        "|---:|---:|---:|" + "---:|" * len(criterion_ids),
    ]
    for report in reports:
        scores = " | ".join(
            f"{item['score']}/{item['max_score']}" if item["score"] is not None else "unscored"
            for item in report["criteria"]
        )
        total = f"{report['ai_provisional_total']}/{report['total_possible']}" if report["ai_provisional_total"] is not None else "withheld"
        lines.append(
            f"| {report['agent_count']} | {total} | "
            f"{report['overall_criterion_agreement']:.1%} | {scores} |"
        )
    lines.extend([
        "",
        "The scores are provisional model outputs, not final grades. Reviewer agreement is internal model consistency, not human agreement.",
        "",
        "Files: one `agent_count_N.json` and one `agent_count_N.md` per reviewer count; raw per-reviewer responses are in `reviewers/`.",
    ])
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path, markdown_path


def load_assignment(pdf_path: Path) -> dict:
    with pymupdf.open(pdf_path) as document:
        pages = [
            {
                "page": number,
                "text": page.get_text("text").strip(),
                "image_count": len(page.get_images(full=True)),
            }
            for number, page in enumerate(document, start=1)
        ]
    if not any(page["text"] for page in pages):
        raise SystemExit("No selectable PDF text was found; OCR or visual extraction is required first.")
    return {"filename": pdf_path.name, "page_count": len(pages), "pages": pages}


def run_assignment(pdf_path: Path, rubric: dict, args: argparse.Namespace, output_dir: Path) -> dict:
    extracted = load_assignment(pdf_path)
    assignment_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    experiment_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reviewer_dir = output_dir / "reviewers"
    reviewer_dir.mkdir(parents=True, exist_ok=False)
    metadata = {
        "experiment_id": experiment_id,
        "assignment": pdf_path.name,
        "assignment_sha256": assignment_hash,
        "rubric_path": str(args.rubric),
        "rubric_version": rubric.get("rubric_version"),
        "model": os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct").strip(),
        "temperature": args.temperature,
        "first_seed": args.seed,
        "max_agents": args.max_agents,
        "status": "running",
        "visual_review_required_pages": [
            page["page"] for page in extracted["pages"]
            if len(page["text"]) < 40 or page.get("image_count", 0) > 0
        ],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "reviewers_completed": 0,
    }
    metadata_path = output_dir / "experiment.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    reviewer_results = []
    reports = []

    try:
        for reviewer_number in range(1, args.max_agents + 1):
            seed = args.seed + reviewer_number - 1
            print(
                f"{pdf_path.name}: reviewer {reviewer_number}/{args.max_agents} "
                f"(seed={seed}, model={metadata['model']})...",
                flush=True,
            )
            started = time.perf_counter()
            criteria = evaluate_ml_assignment(
                extracted, rubric, seed=seed, temperature=args.temperature
            )
            elapsed = time.perf_counter() - started
            reviewer = {
                "reviewer": reviewer_number,
                "seed": seed,
                "elapsed_seconds": round(elapsed, 3),
                "criteria": criteria,
            }
            reviewer_results.append(reviewer)
            (reviewer_dir / f"reviewer_{reviewer_number}.json").write_text(
                json.dumps(reviewer, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            metadata["reviewers_completed"] = reviewer_number
            metadata_path.write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            report = make_count_report(metadata, reviewer_results, rubric)
            json_path, markdown_path = save_count_report(report, output_dir)
            reports.append(report)
            print(
                f"Saved {pdf_path.name} {reviewer_number}-reviewer result: "
                f"{json_path.name}, {markdown_path.name}; total="
                f"{report['ai_provisional_total']}/{report['total_possible']}; "
                f"elapsed={elapsed:.1f}s",
                flush=True,
            )

        comparison_csv, comparison_md = save_comparison(reports, output_dir)
        metadata["status"] = "completed"
        metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        metadata["total_elapsed_seconds"] = round(
            sum(item["elapsed_seconds"] for item in reviewer_results), 3
        )
        metadata["comparison_csv"] = comparison_csv.name
        metadata["comparison_markdown"] = comparison_md.name
    except Exception as error:
        metadata["status"] = "failed"
        metadata["error"] = f"{type(error).__name__}: {error}"
        metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        raise
    finally:
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return {
        "assignment": pdf_path.name,
        "status": "completed",
        "agent_count_totals": ";".join(
            f"{report['agent_count']}:{report['ai_provisional_total']}"
            for report in reports
        ),
        "output_dir": str(output_dir),
        "comparison_markdown": str(output_dir / comparison_md.name),
        "error": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare 1..N independent Ollama reviewers across assignments."
    )
    parser.add_argument("pdf", nargs="?", type=Path, help="One PDF; omit for the assignment batch.")
    parser.add_argument("--input-dir", type=Path, default=ROOT / "data" / "assignments")
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--max-agents", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261017, help="Seed for reviewer 1; subsequent reviewers increment it.")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--limit", type=int, help="Limit batch PDFs for a smoke test.")
    args = parser.parse_args()

    rubric_path = args.rubric.expanduser().resolve()
    if not 1 <= args.max_agents <= 20:
        raise SystemExit("--max-agents must be between 1 and 20.")
    if not 0.0 <= args.temperature <= 2.0:
        raise SystemExit("--temperature must be between 0 and 2.")
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1.")

    load_dotenv(ROOT / ".env")
    if os.getenv("EVALUATOR_PROVIDER", "ollama").strip().lower() != "ollama":
        raise SystemExit("This experiment requires EVALUATOR_PROVIDER=ollama.")
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    batch_mode = args.pdf is None
    if batch_mode:
        input_dir = args.input_dir.expanduser().resolve()
        pdf_paths = sorted(input_dir.glob("*.pdf"))
        if args.limit is not None:
            pdf_paths = pdf_paths[:args.limit]
        if not pdf_paths:
            raise SystemExit(f"No PDF assignments found in {input_dir}")
    else:
        pdf_path = args.pdf.expanduser().resolve()
        if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
            raise SystemExit(f"PDF not found or not a PDF: {pdf_path}")
        pdf_paths = [pdf_path]

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_root = args.output_dir.expanduser().resolve() if args.output_dir else None
    if batch_mode and output_root is None:
        output_root = ROOT / "outputs" / "ai_evaluation" / "agent_count_experiment" / f"batch_{stamp}"
    rows = []
    for pdf_path in pdf_paths:
        assignment_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        if batch_mode:
            output_dir = output_root / f"{safe_stem(pdf_path.name)}_{assignment_hash[:8]}"
        elif output_root is not None:
            output_dir = output_root
        else:
            output_dir = (
                ROOT / "outputs" / "ai_evaluation" / "agent_count_experiment"
                / f"{safe_stem(pdf_path.name)}_{assignment_hash[:12]}_{stamp}"
            )
        output_dir.mkdir(parents=True, exist_ok=False)
        try:
            rows.append(run_assignment(pdf_path, rubric, args, output_dir))
        except Exception as error:
            rows.append({
                "assignment": pdf_path.name,
                "status": "failed",
                "agent_count_totals": "",
                "output_dir": str(output_dir),
                "comparison_markdown": "",
                "error": f"{type(error).__name__}: {error}",
            })
            print(f"Failed {pdf_path.name}: {error}", flush=True)
            if not batch_mode:
                raise

    if batch_mode:
        output_root.mkdir(parents=True, exist_ok=True)
        summary_path = output_root / "batch_summary.csv"
        fields = ["assignment", "status", "agent_count_totals", "output_dir", "comparison_markdown", "error"]
        with summary_path.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        completed = sum(row["status"] == "completed" for row in rows)
        print(f"\nBatch complete: {completed}/{len(pdf_paths)} assignments", flush=True)
        print(f"Batch summary: {summary_path}", flush=True)
    else:
        print(f"\nComplete comparison: {rows[0]['comparison_markdown']}", flush=True)


if __name__ == "__main__":
    main()