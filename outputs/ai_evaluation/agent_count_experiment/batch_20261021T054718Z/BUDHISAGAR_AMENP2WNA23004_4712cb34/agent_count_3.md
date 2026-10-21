# 3-Reviewer Evaluation

- Assignment: `BUDHISAGAR_AMENP2WNA23004.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 3 / 10
- Mean per-criterion reviewer agreement: 86.7%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 0/1 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Missing meaning of each input variable; 'independent' is insufficient. Rubric requires detailed meaning per variable, not generic statement.
**Limitations:** No visual evidence of input variable meanings; text extraction omits detailed descriptions of X1-X4 variables in the dataset context. Cannot verify meaning from
- Evidence, page 1: 1. How many samples are there? Sol: 414 samples 2. How many input variables are there? Sol: 6 input variables 3. Which column is the output variable (target outcome)? Sol: Y is the
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2, 3: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1-X4 vs Y are present in visual evidence; however, no explanation based on plot trends is provided. Selection of multiple predictors without justification fails to meet rubric requirement.
**Limitations:** Visual plots exist but no textual explanation of which predictor is better based on plot patterns; reviewer must verify plot trends.
- Evidence, page 2: For X1 and Y
For X2 and Y
For X3 and Y
For X4 and Y
| Q3 Number of samples | 0/1 | 1: 0, 2: 0, 3: 1 | 67% | 0–1 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples in text; however, no code or output is shown. Rubric requires code and output showing 414. Without visible code/output, score is zero.
**Limitations:** No visible code or output on page 4 to confirm 414 samples; student's text alone does not satisfy evidence rule.
- Evidence, page 4: 2. Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (70:30) is clearly stated and matches expected format. No code is provided, but rubric does not require code if ratio is reported.
**Limitations:** No visible code or output for split; however, stated ratio is sufficient per rubric as long as it is reported.
- Evidence, page 4: Here I have choosen 70-30 train test split ratio.
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 1 | 67% | 0–1 |

**Decision:** Not Satisfied
**Feedback:** No code or output showing computed MAE, MSE, or MAPE. Student references a sample link but provides no actual values or results. No evidence of computed metrics.
**Limitations:** No visual output or code for MAE, MSE, or MAPE; extraction omits values despite request in text.
- Evidence, page 4: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE) .

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
