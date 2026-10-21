# 1-Reviewer Evaluation

- Assignment: `Asha_ML_Assignment1_ Coding Assignment U1A1_Linear Regression 1.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 6 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (Column 8), and meaning of each input variable. No prompt text copied.
**Limitations:** None, all text is present and verifiable in the submission.
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable? Column 8 (Y house price of unit area) 4. What does each input柱s?
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Selected predictor (X3) and explanation are provided, but no scatter plots are shown or referenced. Plot evidence is missing, so analysis cannot be verified against actual visual data.
**Limitations:** No scatter plots visible or referenced in text; visual confirmation required for plot evidence on page 2.
- Evidence, page 2: The input variable "X3 - Distance to the nearest MRT Station" is better in predicting the target variable. As X3 increases, Y tends to decrease (negatively correlated scatter plot)
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** The student states 414 samples, but no code or output is shown. The rubric requires code or calculation with output showing 414. This evidence is missing, so score is 0.
**Limitations:** No code or output provided for sample count; student only states the number without supporting computation.
- Evidence, page 3: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (80:20) is clearly stated and matches expected format. No code is required as ratio is stated, and assignment does not prescribe a specific ratio.
**Limitations:** None; ratio is explicitly stated and verifiable in text.
- Evidence, page 3: ● Here the train-test ratio is 80:20. ● 80% of the data is used for training and remaining 20% is used for testing
| Q5 Regression model evaluation | 2/3 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** MAE, MSE, and MAPE are reported with values and a comparison table. However, no code or output supports the computed values. Values are not verified as computed from model predictions.
**Limitations:** No code or output showing computation of metrics; values are listed but not backed by execution.
- Evidence, page 5: Model 3 gives the lowest errors MAE: 5.31, MSE: 53.5, MAPE: 0.17

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
