# ML Assignment Evaluator

A local Streamlit application for uploading PDF assignments, extracting page text, locating rubric-related evidence, and optionally generating local Ollama score suggestions. Every AI score is provisional and requires a human reviewer. Image-only pages, plots, code screenshots, and extracted-text gaps must be checked against the original PDF.

## Run it on Windows

1. Open PowerShell in this project folder.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the upload app:

   ```powershell
   python -m streamlit run app.py
   ```

5. Upload one or more PDFs. The default `rubric.json` follows the U1A1 Linear Regression assignment's 1/4/1/1/3 mark allocation. Click **Evaluate this ML assignment** to run criterion-focused AI reviewers. Download the JSON or Markdown evaluation. Reviewer-approved marks are saved under `outputs/graded` and added to `data/human_marks.csv`.

The rubric checks dataset understanding, plots and predictor selection, sample-count code/output, the student's chosen train/test split, and MAE/MSE/MAPE. The assignment does not require an 80:20 split.

For one PDF without the browser interface, run:

```powershell
.\.venv\Scripts\python.exe crewai_evaluate_assignment.py "data/assignments/your_submission.pdf"
```

This writes a provisional, criterion-level JSON evaluation under `outputs/ai_evaluation`.

## Enable AI suggestions

Install and start [Ollama](https://ollama.com), then install the configured local model:

```powershell
ollama pull qwen3:4b-instruct
```

Copy `.env.example` to `.env` if it is not already present, then restart Streamlit. The app reads `OLLAMA_MODEL` from `.env`; no cloud API key is needed. The default context size is 8192 tokens and the evaluator may take several minutes per submission on CPU.

## Prepare the current assignment collection

The repository currently contains 28 PDFs under `data/assignments`. To extract page text and produce evidence maps for that folder, run:

```powershell
.\.venv\Scripts\python.exe process_dataset.py
```

This writes page-level JSON and `outputs/dataset/submission_inventory.csv`. Evidence preparation is not grading and does not create marks. The application supports new uploaded submissions independently of this batch folder.

## Human–AI comparison

Enter one row per reviewed criterion in `data/human_marks.csv` with columns:

```text
assignment,criterion_id,human_score,ai_score
```

Use reviewer-confirmed human scores and the corresponding AI suggestion. Then run:

```powershell
.\.venv\Scripts\python.exe performance_analysis.py
```

The script reports MAE, exact agreement, signed error, variance difference, Pearson correlation, and quadratic weighted kappa when enough paired rows exist. With no paired data, it reports that metrics cannot be calculated.

## Agent-count experiment

To compare one through four independent reviews for all PDFs in `data/assignments`, run:

```powershell
\.venv\Scripts\python.exe run_agent_count_experiment.py --max-agents 4
```

The batch runs sequentially, saving each reviewer's checkpoint and per-assignment results under a timestamped folder in `outputs/ai_evaluation/agent_count_experiment/`; `batch_summary.csv` records all assignments and failures. Use `--limit 1` for a smoke test or pass a PDF path to run only that assignment. `--max-agents` accepts 1 through 20; `--seed` and `--temperature` can be set for reproducibility. Each count uses the first N seeded requests (nested groups); per-criterion mode is the consensus, with tied scores resolved downward. Criterion feedback explains why the score is justified, what is correct or missing, and a rubric-linked next step.

Here, an "agent" means an independent request to the same Ollama model, not a separate model process or a different specialist. Agreement measures model consistency only. All scores are provisional, and visual evidence must be checked by a human against the original PDF.

## Project files

- `app.py`: upload interface and optional local Ollama suggestions.
- `evaluation_core.py`: ML rubric prompts, local Ollama request, and score checks.
- `crewai_evaluate_assignment.py`: command-line evaluator for one PDF.
- `rubric.json`: default five-criterion, ten-mark U1A1 rubric.
- `organize_sections.py`: page-linked evidence detection.
- `process_dataset.py`: batch extraction/evidence preparation for the included PDFs.
- `performance_analysis.py`: agreement metrics from paired human/AI marks.
- `outputs/`: generated review and analysis artifacts.

`performance_analysis.py` computes MAE, Pearson correlation, AI-minus-human variance difference, Cohen's kappa, and quadratic weighted kappa from complete paired rows in `data/human_marks.csv`. That CSV must contain reviewer-verified human scores as well as AI scores; the metrics remain unavailable while it is empty.

The system is an evaluation aid, not an autonomous final grader. Scores should not be reported as human grades or as validated AI–human agreement unless those reviews and paired score records actually exist.
