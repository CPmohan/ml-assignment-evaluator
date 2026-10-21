# 1-Reviewer Evaluation

- Assignment: `AarathyU1A1- Linear Regression 1.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 5 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target (Y), and meaning of each input variable. No copied text; direct student response.
**Limitations:** None. Text extraction fully captures all required elements on page 2. No visual components needed for this criterion. 1 mark awarded as per rubric rule for all 
- Evidence, page 2: 414, 6, Y house price of unit area, Column 1- X1 transaction date, Column 2- X2 house age, Column 3- X3 distance to the nearest MRT station, Column 4- X4 number of convenience stor
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X2 as better predictor but provides no scatter plot evidence. Rubric requires plot analysis and explanation grounded in plots. No visual evidence present to verify scatter plots or plot-based reasoning.
**Limitations:** Page 5 contains only text stating X2 is better; no scatter plots or visual evidence are present. Cannot verify plot analysis or explanation. 4 marks not awarded
- Evidence, page 2: Using the scatter plots between each of the input features (X1-X4) and the output (Y), which input variable, do you think, is better in predicting the output / target variable ?
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student writes code to find sample count, though code is missing. However, the answer '414' is stated and matches expected output. Rubric requires student's own code or calculation showing 414. The response satisfies this criterion as per '
**Limitations:** No code is visible on page 6. The answer '414' is stated but code is missing. Cannot verify code output. Score 0 for this criterion.
- Evidence, page 6: 2. Write code to find out how many samples are there in total in this dataset?  
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student clearly states train/test split ratio (70:30) and includes it in the response. No code is required; ratio is stated and consistent across multiple pages. Rubric allows any valid ratio. 1 mark awarded.
**Limitations:** No code or output showing the split. However, the stated ratio is sufficient per rubric. No visual evidence needed.
- Evidence, page 6: Train test split ratio : Train- 70% Test -30%
| Q5 Regression model evaluation | 1/3 | 1: 1 | 100% | 1–1 |

**Decision:** Partially Satisfied
**Feedback:** Student lists MAE, MSE, and MAPE for each X1–X4, but no actual computed values or supporting code/output are provided. Rubric requires computed metrics with supporting evidence. Values are not present or verifiable. Only 1 mark awarded for 
**Limitations:** No actual computed values or code output for MAE, MSE, or MAPE. Values are listed without computation or verification. Cannot verify any metric values.
- Evidence, page 9: MAE, MSE and MAPE for X1

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
