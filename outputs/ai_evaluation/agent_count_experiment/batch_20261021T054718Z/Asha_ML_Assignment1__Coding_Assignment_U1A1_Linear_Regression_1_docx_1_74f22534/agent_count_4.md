# 4-Reviewer Evaluation

- Assignment: `Asha_ML_Assignment1_ Coding Assignment U1A1_Linear Regression 1.docx (1).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 4
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 6 / 10
- Mean per-criterion reviewer agreement: 95.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1, 4: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions answered correctly: sample count (414), input variables (6), target variable (Column 8), and meaning of each input variable. No prompt text copied.
**Limitations:** None, all text is present and verifiable in student work.
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable (target outcome)? Column 8 (Y house price of unit area) 4. What d
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2, 3: 2, 4: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X3 as predictor and gives a plot-based explanation, but no scatter plots are visible. Plot evidence missing, so analysis cannot be verified.
**Limitations:** No scatter plots present; visual confirmation required to verify plot evidence for X1-X4 vs Y.
- Evidence, page 2: The input variable "X3 - Distance to the nearest MRT Station" is better in predicting the target variable. As X3 - Distance to the nearest MRT Station increases , the Y-house price
| Q3 Number of samples | 0/1 | 1: 0, 2: 0, 3: 0, 4: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, but no code or output showing the count is provided. The prompt requires student's own code or output; absence of code means no evidence of computation.
**Limitations:** No code or output showing sample count computation; student only states result without supporting code.
- Evidence, page 3: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1, 4: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (80:20) is clearly stated and matches expected format. No code required as ratio is reported and contextually valid.
**Limitations:** None; ratio is explicitly stated and verifiable in text.
- Evidence, page 3: Here the train-test ratio is 80:20. 80% of the data is used for training and remaining 20% is used for testing
| Q5 Regression model evaluation | 2/3 | 1: 2, 2: 2, 3: 1, 4: 2 | 75% | 1–2 |

**Decision:** Partially Satisfied
**Feedback:** Student reports MAE, MSE, MAPE values and includes a comparison table, but no code or output supporting these metrics is shown. Values are not tied to model predictions or computation evidence.
**Limitations:** No code or output showing computation of MAE/MSE/MAPE; values are listed without verification of source.
- Evidence, page 5: Model 3 gives the lowest errors MAE: 5.31, MSE: 53.5, MAPE: 0.17

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
