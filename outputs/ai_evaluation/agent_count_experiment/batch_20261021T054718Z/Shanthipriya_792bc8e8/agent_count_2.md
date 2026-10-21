# 2-Reviewer Evaluation

- Assignment: `Shanthipriya.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 3 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions with specific values and meanings. No copied text. Full rubric criterion met.
**Limitations:** None, all text is present and verifiable in student work.
- Evidence, page 1: There are 414 samples in the dataset. There are 6 input variables. Output variable is Y house price of unit area. X1 – transaction, X2- house age, X3- distance from nearest MRT, X4
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** States predictor selection (X1, X4) and gives reasoning based on plot evidence, but no actual scatter plots are visible or referenced. Missing visual proof of scatter plots for X1-X4 vs Y.
**Limitations:** No scatter plots or visual evidence present; text extraction omits plot content. Reviewer must visually confirm plots on page 2 or 4.
- Evidence, page 4: In the dataset we could say X1 and X4 can predict the output well because in the linear regression fitting we could say that X1 and X4 have more data in the line.
| Q3 Number of samples | 0/1 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student writes code request but no actual code or output showing 414 samples. No evidence of execution or output. Does not satisfy rubric requirement of code and output showing 414.
**Limitations:** No code or output provided on page 5. Missing execution evidence. Cannot verify sample count from student work.
- Evidence, page 5: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 0/1 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Partially Satisfied
**Feedback:** Ratio is asked but not stated or supported by code/output. No reported split ratio or evidence. Missing required code or output for split ratio.
**Limitations:** No train/test split code or reported ratio visible. Cannot verify split from text or image.
- Evidence, page 5: What is the train test split ratio that you have chosen ?
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** No code or output showing MAE, MSE, or MAPE values. Student only states general interpretation without computed metrics or supporting results. No evidence of actual computation.
**Limitations:** No computed metrics or output visible. Cannot verify values or code for MAE, MSE, or MAPE.
- Evidence, page 5: Evaluate the linear regression model by computing the MAE, MSE and MAPE

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
