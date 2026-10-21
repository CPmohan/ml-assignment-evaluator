# 3-Reviewer Evaluation

- Assignment: `Sreevisal_ML - Coding Assignment U1A1 - Linear Regression.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 3 / 10
- Mean per-criterion reviewer agreement: 93.3%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target (Y), and meanings of X1-X4. No prompt text copied; student work directly addresses each element.
**Limitations:** None, as all dataset elements are clearly stated in text.
- Evidence, page 1: 1. How many samples are there? 414 samples 2. How many input variables are there? 6 input variables 3. Which column is the output variable? Y house price of unit area 4. What does每
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2, 3: 0 | 67% | 0–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X3 (distance to MRT) as better predictor with plot-based reasoning, but no scatter plots are present. Visual evidence missing; explanation lacks plot support per rubric.
**Limitations:** No scatter plots visible; text extraction omits image content. Reviewer must visually confirm plot evidence on page 2.
- Evidence, page 2: I think Distance to the Nearest MRT station and Housing Price shows more linearity and clustering. Also points are close to linear regression line
| Q3 Number of samples | 0/1 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, but no code or output is provided. Evidence of code/output is missing; cannot verify count via student work. Score awarded 0 per rubric rule requiring code/output showing 414.
**Limitations:** No code or output shown; student only states the number without supporting computation.
- Evidence, page 3: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 0/1 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student does not state a train/test ratio or provide code. No ratio or evidence of split is present; rubric requires clear statement and code/output.
**Limitations:** No ratio or code provided; student response is blank or incomplete.
- Evidence, page 3: What is the train test split ratio that you have chosen ?
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** No code or output for MAE, MSE, or MAPE is provided. Student only references a sample link, not computed values. No metrics reported or supported.
**Limitations:** No computed metrics or output shown; student work lacks execution evidence.
- Evidence, page 4: Evaluate the linear regression model by computing the MAE, MSE and MAPE

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
