"""Upload and evaluate machine-learning assignment PDFs against a rubric."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pymupdf
import streamlit as st
from dotenv import load_dotenv

from evaluation_core import evaluate_ml_assignment
from organize_sections import organize_file


ROOT = Path(__file__).resolve().parent
DEFAULT_RUBRIC = ROOT / "rubric.json"
load_dotenv(ROOT / ".env")
def extract_pdf(upload) -> dict:
    """Extract selectable text and flag pages likely to need visual review."""
    pages = []
    with pymupdf.open(stream=upload.getvalue(), filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()
            pages.append({
                "page": page_number,
                "text": text,
                "image_count": len(page.get_images(full=True)),
            })
    return {
        "filename": Path(upload.name).name,
        "page_count": len(pages),
        "pages": pages,
        "text": "\n\n".join(page["text"] for page in pages),
        "low_text_pages": [page["page"] for page in pages if len(page["text"]) < 40],
        "image_pages": [page["page"] for page in pages if page["image_count"]],
    }


def make_evidence_map(extracted: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix="ml_assignment_review_") as temp_dir:
        source = Path(temp_dir) / "submission.json"
        source.write_text(json.dumps(extracted, ensure_ascii=False), encoding="utf-8")
        evidence = organize_file(source)
    return {
        **evidence,
        "filename": extracted["filename"],
        "page_count": extracted["page_count"],
        "low_text_pages": extracted["low_text_pages"],
        "image_pages": extracted["image_pages"],
    }


def update_totals(report: dict, rubric: dict) -> None:
    criteria = rubric["criteria"]
    human_scores = report.get("reviewer_scores")
    if human_scores:
        report["reviewer_total"] = sum(human_scores.values())
        report["reviewer_total_possible"] = sum(item["max_marks"] for item in criteria)
    suggestions = {item["criterion_id"]: item.get("score")
                   for item in report.get("ai_suggestions", [])}
    valid = [suggestions.get(item["id"]) for item in criteria]
    report["ai_score_coverage"] = sum(score is not None for score in valid)
    report["ai_total_possible"] = sum(item["max_marks"] for item in criteria)
    report["ai_provisional_total"] = sum(valid) if valid and all(score is not None for score in valid) else None


def safe_stem(filename: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", Path(filename).stem).strip("_") or "submission"


def report_markdown(report: dict) -> str:
    lines = [
        "# ML Assignment Evaluation", "", f"Assignment: `{report['assignment']}`",
        f"Status: **{report['status']}**", "",
        f"AI provisional total: {report.get('ai_provisional_total')} / {report.get('ai_total_possible')}"
        if report.get("ai_suggestions") else "AI score: not generated.",
        f"Reviewer total: {report.get('reviewer_total')} / {report.get('reviewer_total_possible')}"
        if report.get("reviewer_scores") else "Reviewer marks: not recorded.",
        "",
        "AI scores are suggestions until a reviewer checks the original submission.",
    ]
    for item in report.get("ai_suggestions", []):
        lines.extend(["", f"## {item['criterion_id']} — {item['criterion_name']}", "",
                      f"Score: {item.get('score')} / {item['max_score']} ({item.get('decision')})",
                      f"Feedback: {item.get('feedback', '')}",
                      f"Limitations: {item.get('limitations', '')}"])
        for evidence in item.get("evidence", []):
            lines.append(f"- Page {evidence.get('page')}: {evidence.get('text', '')}")
    if report.get("low_text_pages") or report.get("image_pages"):
        lines.extend(["", "## Visual review required", "",
                      f"Low-text pages: {report.get('low_text_pages', [])}",
                      f"Pages containing images: {report.get('image_pages', [])}"])
    return "\n".join(lines) + "\n"


def persist_ai_report(report: dict, upload_key: str) -> tuple[Path, Path]:
    out_dir = ROOT / "outputs" / "ai_evaluation"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{safe_stem(report['assignment'])}_{upload_key}"
    json_path, md_path = out_dir / f"{stem}.json", out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(report_markdown(report), encoding="utf-8")
    return json_path, md_path


def persist_reviewer_scores(report: dict, rubric: dict, upload_key: str) -> Path:
    out_dir = ROOT / "outputs" / "graded"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{safe_stem(report['assignment'])}_{upload_key}_reviewed"
    json_path = out_dir / f"{stem}.json"
    report["reviewer_saved_at"] = datetime.now(timezone.utc).isoformat()
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / f"{stem}.md").write_text(report_markdown(report), encoding="utf-8")

    csv_path = ROOT / "data" / "human_marks.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    assignment_id = f"{report['assignment']}::{upload_key}"
    existing = []
    if csv_path.exists() and csv_path.stat().st_size:
        with csv_path.open(newline="", encoding="utf-8-sig") as handle:
            existing = list(csv.DictReader(handle))
    existing = [row for row in existing if row.get("assignment") != assignment_id]
    ai_scores = {item["criterion_id"]: item.get("score")
                 for item in report.get("ai_suggestions", [])}
    for criterion in rubric["criteria"]:
        criterion_id = criterion["id"]
        existing.append({
            "assignment": assignment_id,
            "criterion_id": criterion_id,
            "human_score": report["reviewer_scores"][criterion_id],
            "ai_score": ai_scores.get(criterion_id, ""),
        })
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["assignment", "criterion_id", "human_score", "ai_score"])
        writer.writeheader()
        writer.writerows(existing)
    return json_path


def validate_rubric(rubric: object) -> tuple[bool, str]:
    if not isinstance(rubric, dict) or not isinstance(rubric.get("criteria"), list) or not rubric["criteria"]:
        return False, "Rubric JSON must be an object with a non-empty criteria list."
    ids = set()
    for item in rubric["criteria"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("name"), str):
            return False, "Every criterion must have string id and name fields."
        if item["id"] in ids:
            return False, f"Duplicate criterion id: {item['id']}"
        ids.add(item["id"])
        maximum = item.get("max_marks")
        if isinstance(maximum, bool) or not isinstance(maximum, (int, float)) or maximum <= 0:
            return False, f"Criterion {item['id']} needs a positive numeric max_marks."
        if not float(maximum).is_integer():
            return False, f"Criterion {item['id']} must use whole-number marks in this app."
    return True, ""


st.set_page_config(page_title="ML Assignment Evaluator", page_icon="📋", layout="wide")
st.title("ML Assignment Evaluator")
st.caption("Upload a machine-learning assignment PDF for a criterion-by-criterion rubric evaluation.")

with st.sidebar:
    st.header("Evaluation rubric")
    rubric_upload = st.file_uploader("Upload rubric JSON (optional)", type=["json"])
    try:
        rubric = (json.loads(rubric_upload.getvalue().decode("utf-8")) if rubric_upload
                  else json.loads(DEFAULT_RUBRIC.read_text(encoding="utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        st.error(f"Could not read the rubric: {error}")
        st.stop()
    valid_rubric, rubric_error = validate_rubric(rubric)
    if not valid_rubric:
        st.error(rubric_error)
        st.stop()
    total_marks = sum(item["max_marks"] for item in rubric["criteria"])
    st.write(f"{len(rubric['criteria'])} criteria · {total_marks:g} total marks")
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct")
    ai_mode = st.checkbox("Enable local Ollama rubric scoring", value=True)
    if ai_mode:
        st.caption(f"Local AI scoring uses Ollama model `{ollama_model}`. Start Ollama before evaluating.")
    st.caption("AI marks remain provisional until a human checks the PDF and approves them.")

uploads = st.file_uploader("Upload ML assignment PDF(s)", type=["pdf"], accept_multiple_files=True)
if uploads:
    for upload_index, upload in enumerate(uploads):
        upload_key = hashlib.sha256(upload.getvalue()).hexdigest()[:12]
        state_key = f"ml_eval_{upload_index}_{upload_key}"
        with st.expander(upload.name, expanded=True):
            try:
                with st.spinner("Extracting pages and preparing ML rubric evidence…"):
                    extracted = extract_pdf(upload)
                    evidence_map = make_evidence_map(extracted)
            except Exception as error:
                st.error(f"Could not read this PDF: {error}")
                continue

            st.write(f"Pages: {extracted['page_count']} · Extracted characters: {len(extracted['text']):,}")
            review_pages = sorted(set(extracted["low_text_pages"] + extracted["image_pages"]))
            if review_pages:
                st.warning(
                    "Visually check these pages for plots, tables, code screenshots, or scans: "
                    + ", ".join(map(str, review_pages))
                )
            with st.expander("Show page text and detected evidence"):
                for page in extracted["pages"]:
                    st.markdown(f"**Page {page['page']}**")
                    st.text(page["text"][:5000] or "No selectable text; inspect the original page.")
                for criterion in rubric["criteria"]:
                    st.markdown(f"**{criterion['id']} · {criterion['name']}**")
                    st.write(", ".join(criterion.get("expected_evidence", [])) or "Use the scoring rule in the rubric.")

            report = {
                "assignment": upload.name,
                "rubric_version": rubric.get("rubric_version", "custom"),
                "total_marks": total_marks,
                "page_count": extracted["page_count"],
                "low_text_pages": extracted["low_text_pages"],
                "image_pages": extracted["image_pages"],
                "evidence_map": evidence_map,
                "ai_suggestions": [],
                "reviewer_scores": None,
                "status": "Evidence extracted; not scored yet",
            }
            report.update(st.session_state.get(state_key, {}))

            if ai_mode and st.button("Evaluate this ML assignment", key=f"evaluate_{upload_key}"):
                try:
                    with st.spinner("Running one rubric-focused evaluator per criterion…"):
                        report["ai_suggestions"] = evaluate_ml_assignment(extracted, rubric)
                    report["status"] = "AI rubric suggestions generated — reviewer approval required"
                    report["evaluated_at"] = datetime.now(timezone.utc).isoformat()
                    update_totals(report, rubric)
                    ai_json, ai_md = persist_ai_report(report, upload_key)
                    st.session_state[state_key] = report
                    st.success(f"AI review saved to {ai_json.relative_to(ROOT)} and {ai_md.relative_to(ROOT)}")
                except Exception as error:
                    st.error(f"ML evaluation failed: {error}")

            if report.get("ai_suggestions"):
                st.subheader("ML rubric evaluation — provisional")
                update_totals(report, rubric)
                for result in report["ai_suggestions"]:
                    st.markdown(
                        f"**{result['criterion_id']} · {result['criterion_name']}:** "
                        f"{result.get('score')} / {result['max_score']} — {result.get('decision')}"
                    )
                    st.write(result.get("feedback", ""))
                    if result.get("limitations"):
                        st.caption("Review limitation: " + result["limitations"])
                    for item in result.get("evidence", []):
                        st.write(f"Evidence · page {item.get('page')}: {item.get('text', '')}")
                if report["ai_provisional_total"] is None:
                    st.info(
                        f"AI score coverage: {report['ai_score_coverage']} of {len(rubric['criteria'])} criteria. "
                        "A total is withheld until every criterion has a valid score."
                    )
                else:
                    st.info(
                        f"AI-proposed total: {report['ai_provisional_total']} / {report['ai_total_possible']} "
                        "— verify each criterion before using this grade."
                    )

            st.subheader("Reviewer scoring")
            reviewer_scores = {}
            for criterion in rubric["criteria"]:
                choice = st.selectbox(
                    f"{criterion['id']} · {criterion['name']} (maximum {criterion['max_marks']:g})",
                    ["Not reviewed", *map(str, range(int(criterion["max_marks"]) + 1))],
                    key=f"score_{upload_key}_{criterion['id']}",
                )
                if choice != "Not reviewed":
                    reviewer_scores[criterion["id"]] = int(choice)
            visual_check = True
            if review_pages:
                visual_check = st.checkbox(
                    "I checked the flagged pages in the original PDF before saving marks.",
                    key=f"visual_{upload_key}",
                )
            if st.button("Save reviewer marks and evaluation", key=f"save_{upload_key}"):
                if len(reviewer_scores) != len(rubric["criteria"]):
                    st.error("Enter a reviewer score for every criterion.")
                elif not visual_check:
                    st.error("Check the flagged pages before recording final marks.")
                else:
                    report["reviewer_scores"] = reviewer_scores
                    report["status"] = "Reviewer-entered marks saved"
                    update_totals(report, rubric)
                    final_path = persist_reviewer_scores(report, rubric, upload_key)
                    st.session_state[state_key] = report
                    st.success(f"Saved reviewer evaluation to {final_path.relative_to(ROOT)} and data/human_marks.csv")

            if report.get("reviewer_scores"):
                st.write(f"Reviewer total: {report.get('reviewer_total')} / {report.get('reviewer_total_possible')}")
            json_bytes = json.dumps(report, ensure_ascii=False, indent=2)
            st.download_button(
                "Download evaluation JSON", json_bytes,
                file_name=f"{safe_stem(upload.name)}_evaluation.json",
                mime="application/json", key=f"download_json_{upload_key}",
            )
            st.download_button(
                "Download evaluation report", report_markdown(report),
                file_name=f"{safe_stem(upload.name)}_evaluation.md",
                mime="text/markdown", key=f"download_md_{upload_key}",
            )
