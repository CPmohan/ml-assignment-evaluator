# 2-Reviewer Evaluation

- Assignment: `Goutham _Coding_Assignment_U1A1_Linear_Regression_GowthamIyer.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 6 / 10
- Mean per-criterion reviewer agreement: 90.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are answered correctly: sample count (414), input variables (6), target variable (Y), and meaning of each input variable as per table. No copied text; full response in student text.
**Limitations:** None; all expected evidence is present and verifiable in text.
- Evidence, page 1: There are 414 samples. There are 6 input variables. The output variable is "Y house price of unit area", column "H" in the dataset. Meaning of input columns is described in table.
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student provides a selection (X3) and explanation based on scatter plot evidence. However, no actual scatter plots are visible in text or image; plot evidence is missing, so full 4 marks not awarded. Explanation is sound but lacks visual佐证.
**Limitations:** No scatter plots visible in text; image pages referenced but not accessible. Cannot verify plot evidence for X1-X4 vs Y.
- Evidence, page 2: The X3 input variable is better in predicting output since scatter plot shows clear negative correlation. Number of convenience stores comes next. Other inputs show no clear trend.
| Q3 Number of samples | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student provides code and output showing 414 samples. Matches expected value and is derived from own code. Full credit for correct computation and output.
**Limitations:** None; output is explicitly stated and matched to code in student work.
- Evidence, page 5: Screenshot of code snippet to find total number of samples, output shows 414.
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (2/3 and 1/3) is clearly stated and supported by code snippet screenshot. Ratio is valid and not prescribed, so correct. Full credit awarded.
**Limitations:** None; ratio and code are present and verifiable.
- Evidence, page 6: I have chosen train set of ratio 2/3 and test set of ratio 1/3.
| Q5 Regression model evaluation | 1/3 | 1: 1, 2: 3 | 50% | 1–3 |

**Decision:** Partially Satisfied
**Feedback:** Student reports MAE, MSE, and MAPE and includes code/output. However, no actual values are provided in text; values are missing from output. Cannot verify computed metrics. One point per metric only if values are present and computed. Since
**Limitations:** No values for MAE, MSE, or MAPE are visible in text; output values omitted. Cannot verify computed metrics.
- Evidence, page 7: Screenshot of code snippet for evaluating model using MAE, MSE, and MAPE and its output.

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
