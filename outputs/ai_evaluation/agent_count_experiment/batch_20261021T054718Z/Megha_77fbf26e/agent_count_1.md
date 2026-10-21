# 1-Reviewer Evaluation

- Assignment: `Megha.pdf`
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
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (Y), and meaning of inputs. No prompt text copied; student work directly addresses each point.
**Limitations:** None. Text is fully extractable and directly answers all required elements of dataset understanding on page 1. No visual evidence needed for this criterion as a
- Evidence, page 1: There are 414 samples. There are 6 input variables. Y house price of unit area is output variable. Input columns are the independent variables on which the output/target variable依赖
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1-X4 vs Y are referenced but not shown. Selected predictor (X3) is identified with a plot explanation, but no actual scatter plot evidence is visible. Plot evidence is missing, so full 4 marks not awarded.
**Limitations:** Pages 3-4 contain only labels for input features, no actual scatter plots. Visual confirmation required to verify plot existence and trend description. Cannot v
- Evidence, page 2: Input feature 1, Input feature 2, Input feature 3, Input feature 4
| Q3 Number of samples | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student states 414 samples, and the code section is present on page 5, though code is missing. However, the stated sample count matches the expected output and is directly in student text. The absence of code does not negate the stated 
**Limitations:** No actual code or output is visible on page 5. The student's statement of 414 is correct, but without code or output, the evidence is incomplete. Still, the rub
- Evidence, page 5: Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student clearly states a train/test split ratio of 8:2, which is supported by the text. No code is provided, but the ratio is explicitly stated and valid under the rubric. The assignment does not require a specific ratio.
**Limitations:** No code or output showing the split is present. However, the stated ratio is sufficient per rubric, which allows any valid split.
- Evidence, page 5: Train test split ratio - 8:2
| Q5 Regression model evaluation | 1/3 | 1: 1 | 100% | 1–1 |

**Decision:** Partially Satisfied
**Feedback:** The student identifies MAE, MSE, and MAPE as computed, but no actual values or code/output are shown. The metrics are mentioned, but without supporting computation or output, the values cannot be verified. Only one point per metric is valid
**Limitations:** No code or numerical output for MAE, MSE, or MAPE is visible. The student mentions the metrics but does not provide computed values or supporting output.
- Evidence, page 5: MAE, MSE, MAPE of linear regression model for input variable 3 (distance to the nearest MRT station)

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
