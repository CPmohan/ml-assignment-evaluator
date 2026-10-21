# 3-Reviewer Evaluation

- Assignment: `Megha.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 4 / 10
- Mean per-criterion reviewer agreement: 86.7%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (Y), and meaning of inputs. No prompt text copied; student work directly addresses each point.
**Limitations:** None. Text is fully extractable and directly answers all required elements of dataset understanding on page 1. No visual evidence needed for this criterion as a
- Evidence, page 1: There are 414 samples. There are 6 input variables. Y house price of unit area is output variable. Input columns are the independent variables on which the output/target variable依赖
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2, 3: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1-X4 vs Y are referenced but not shown. Selected predictor (X3) is identified with a plot explanation, but no actual scatter plot evidence is visible. Plot evidence is missing, so full 4 marks not awarded.
**Limitations:** Pages 3-4 contain only labels for input features, no actual scatter plots. Visual confirmation required to verify plot existence and trend description. Cannot v
- Evidence, page 2: Input feature 1, Input feature 2, Input feature 3, Input feature 4
| Q3 Number of samples | 0/1 | 1: 1, 2: 0, 3: 0 | 67% | 0–1 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, and the code is implied in the context. Though code is not shown, the correct sample count is stated and matches the expected output. No code is visible, but the answer is correct and directly stated.
**Limitations:** No code or output is visible on page 5. The student's response does not include actual code or output to count samples. Cannot verify code execution.
- Evidence, page 5: Write code to find out how many samples are there in total in this dataset? 
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student clearly states a train/test split ratio of 8:2, which is supported by the text. No code is provided, but the ratio is explicitly stated and valid under the rubric. The assignment does not require a specific ratio.
**Limitations:** No code or output showing the split is present. However, the stated ratio is sufficient per rubric, which allows any valid split.
- Evidence, page 5: Train test split ratio - 8:2
| Q5 Regression model evaluation | 0/3 | 1: 1, 2: 0, 3: 0 | 67% | 0–1 |

**Decision:** Not Satisfied
**Feedback:** Student mentions MAE, MSE, and MAPE but provides no computed values or supporting code/output. Values are not reported or verified. No evidence of actual model evaluation metrics.
**Limitations:** No code or output for MAE, MSE, or MAPE is visible. The mention of metrics is insufficient without computed values or supporting output.
- Evidence, page 5: MAE, MSE, MAPE of linear regression model for input variable 3 (distance to the nearest MRT station)

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
