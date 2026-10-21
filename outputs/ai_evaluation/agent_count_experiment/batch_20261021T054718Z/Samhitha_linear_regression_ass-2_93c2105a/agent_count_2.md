# 2-Reviewer Evaluation

- Assignment: `Samhitha linear regression ass-2.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 5 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly states sample count (414), number of input variables (6), target variable (Y), and meaning of each input variable. All four expected elements are present in student text.
**Limitations:** None; all dataset elements are clearly stated in text without reliance on images or external outputs. No visual evidence needed for this criterion. 1 mark fully
- Evidence, page 1: From csv file we get no. of samples = 414. From Csv file we observe the are 8 variables and input variables = 6. X1 transaction date, X2 house age, X3 distance to the nearest MRT, 
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1, X2, X3, X4 vs Y are referenced but only output labels are shown; no visual plots are present or verifiable. Selected predictor is implied but not explained with plot evidence. Missing explanation grounded in plot data.
**Limitations:** Pages 4–6 contain only output labels, no actual scatter plots. Visual evidence of plots is missing or not extractable. Cannot verify plot-based explanation.
- Evidence, page 4: FOR X1 AND Y: Output:
| Q3 Number of samples | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student explicitly states 414 samples in text and includes it in code context. Output is shown in plain text, matching expected value. Code is not shown but the result is correctly reported.
**Limitations:** No code snippet provided, but the stated result matches the expected output. Does not require code execution to verify; value is correctly reported.
- Evidence, page 7: There are 414 samples and 8 variables in dataset
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (70:30) is clearly stated and matches expected format. No code is required as ratio is explicitly reported. Ratio is valid and supported by text.
**Limitations:** No code shown, but the split ratio is clearly stated and valid. Does not require visual output to verify.
- Evidence, page 7: Train split ratio: 70 Test split ratio: 30
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student mentions computing MAE, MSE, and MAPE but provides no code, output, or values. No evidence of computed metrics. Values are not reported or verified.
**Limitations:** No code or output for MAE, MSE, or MAPE is present. Cannot verify any metric values. Student only states the task, not the results.
- Evidence, page 8: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE).

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
