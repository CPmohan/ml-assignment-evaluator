# PDF Extraction Quality Report

Generated from the eight source PDFs and their matching JSON files in `outputs/extracted/`.

| PDF | Pages | Extracted characters | Pages that may need OCR |
| --- | ---: | ---: | --- |
| AryaR_AM_En_P2GEO23002_Assignment1.pdf | 5 | 3,829 | None flagged |
| Bincy - Coding Assignment U1A1 - Linear Regression Bincy Babu.pdf | 4 | 2,555 | None flagged |
| BUDHISAGAR_AMENP2WNA23004.pdf | 5 | 2,131 | 2 (44 characters) |
| Goutham _Coding_Assignment_U1A1_Linear_Regression_GowthamIyer.pdf | 8 | 5,221 | None flagged |
| Harsha - Coding Assignment U1A1 - Linear Regression (3) 2.pdf | 6 | 2,511 | 4 (8 characters); 6 (67 characters) |
| Megha.pdf | 7 | 3,737 | 3 (48 characters) |
| Namitha - Coding Assignment U1A1 - Linear Regression_Namitha.pdf | 10 | 3,411 | 3 (11 characters); 4 (11 characters); 7 (95 characters); 8 (11 characters); 9 (11 characters) |
| Sreevisal_ML - Coding Assignment U1A1 - Linear Regression.pdf | 5 | 3,422 | None flagged |

## Method and cautions

`extract_pdfs.py` uses PyMuPDF's text layer (`page.get_text("text")`). A page with fewer than 100 non-whitespace extracted characters is flagged as an OCR candidate. This is a triage threshold, not proof that a page is unreadable: pages may contain plots, code screenshots, or other visual evidence.

All eight expected JSON files are present and have non-empty full text. No extra JSON files were found in `outputs/extracted/`.

## Rubric status

`rubric.json` is **provisional** (`rubric_version: "0.1-provisional"`) and explicitly states that it is a research rubric rather than an official advisor rubric. This report makes no judgments, marks, or experimental claims.
