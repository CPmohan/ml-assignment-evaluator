# 3-Reviewer Evaluation

- Assignment: `Jayasree _Solution- Coding Assignment U1A1 - Linear Regression (3).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 4 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions: sample count (414), input variables (6), target variable (house price of unit area), and meaning of each input variable. All responses are student-generated and match expected evidence.
**Limitations:** None; all text is extractable and directly addresses the rubric criteria without reliance on external sources or placeholders. No visual elements are referenced
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable? House price of unit area 4. What does each of the input columns 
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2, 3: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1-X4 vs Y are not present or verifiable in text; only list of plots is mentioned without plot evidence. Selected predictor (X2) is stated with explanation, but no visual plot support exists to validate the reasoning. Does
**Limitations:** No scatter plots or visual evidence present; text extraction omits plot images. A reviewer must visually confirm the scatter plots to verify the analysis and pl
- Evidence, page 2: 1) X1- Transaction Date V/s House price 2) X2- House age V/s House price 3) X3 distance to the nearest MRT station V/s House price 4) X4 number of convenience stores V/s Houseprice
| Q3 Number of samples | 0/1 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, but no code or output showing the count is provided. The prompt requires student's own code or calculation with output. Without code or output, the evidence is missing.
**Limitations:** No code or output is provided to verify the 414 sample count. The value is stated but not supported by student-generated computation or execution result.
- Evidence, page 4: 2. Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio of 70:30 is clearly stated and matches the expected evidence. No code is required as the ratio is reported directly. The assignment does not prescribe a specific ratio, so this is valid.
**Limitations:** None; the split ratio is explicitly stated and verifiable in text.
- Evidence, page 4: Train to Test split = 70:30
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** No computed values for MAE, MSE, or MAPE are provided. No code or output showing the metrics is present. The student references a sample link but does not report any actual computed values.
**Limitations:** No metrics values or supporting output are present in text. A visual plot or output page would be needed to verify computation, but none are provided.
- Evidence, page 5: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE) . (for MAPE - pls refer to the sample here - https://scikit-learn.org/stale

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
