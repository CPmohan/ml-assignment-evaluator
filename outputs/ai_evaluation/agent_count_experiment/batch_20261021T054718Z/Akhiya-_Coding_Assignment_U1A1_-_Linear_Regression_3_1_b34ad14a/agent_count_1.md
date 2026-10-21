# 1-Reviewer Evaluation

- Assignment: `Akhiya- Coding Assignment U1A1 - Linear Regression (3) (1).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 4 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered with clear, student-generated responses. Sample count, input variables, target, and variable meanings are fully addressed in the text.
**Limitations:** None; all evidence is text-extractable and fully present.
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable (target outcome)? Y house price of unit area 4. What does each of
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X3 as predictor and references scatter plot clustering, but no actual scatter plots are provided or visible. Plot evidence is missing, so explanation lacks grounding in visual data.
**Limitations:** No scatter plots present; visual evidence omitted despite claim of plot-based analysis.
- Evidence, page 2: X3 would be the best input variable for predicting Y house price of unit area as the clustering we can observe from the given scatter plot.
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, but no code or output showing the count is provided. Evidence of code/output is missing; thus, cannot verify the computation.
**Limitations:** No code or output shown for sample count; student response lacks computational evidence.
- Evidence, page 3: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** 70:30 split is clearly stated and matches expected format. No code is required as ratio is sufficient per rubric; student response is valid and complete.
**Limitations:** None; ratio is explicitly stated and meets rubric criteria.
- Evidence, page 4: What is the train test split ratio that you have chosen ? 70:30
| Q5 Regression model evaluation | 0/3 | 1: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student mentions computing MAE, MSE, and MAPE but provides no code, output, or values. No evidence of actual computation or results is present.
**Limitations:** No computed metrics or supporting output; values are not shown or verifiable.
- Evidence, page 4: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE)

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
