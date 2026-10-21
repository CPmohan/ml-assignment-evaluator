# 1-Reviewer Evaluation

- Assignment: `Harsha - Coding Assignment U1A1 - Linear Regression (3) 2.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 8 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions with accurate values and meanings; no copied text; fully satisfies rubric criteria for dataset understanding.
**Limitations:** none
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable? 8th 4. What does each input column mean? X1=transaction date, X2
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Provides a selection (X3) and explanation based on plot evidence, but no actual scatter plots are present in text or images; explanation is plausible but not verifiable from student work; missing plot evidence prevents full mark.
**Limitations:** No scatter plot images or outputs visible in text; cannot verify plot evidence; explanation is inferred.
- Evidence, page 1: X3 : The input variable that has a closer clustering of data points around a straight line, indicating a stronger linear relationship between the input and output variables, is更好
| Q3 Number of samples | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, and the code is implied in the context; though code is not shown, the output is stated and matches expected value; satisfies rubric with correct sample count and output.
**Limitations:** No explicit code or output shown; relies on inference; however, the stated result matches expected output and is correctly reported.
- Evidence, page 2: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Clearly states a train/test split ratio (80:20) and it is supported by text; no requirement for specific ratio; satisfies rubric criteria.
**Limitations:** none
- Evidence, page 2: Train-test split ratio chosen as 80-20
| Q5 Regression model evaluation | 3/3 | 1: 3 | 100% | 3–3 |

**Decision:** Satisfied
**Feedback:** Student computes and reports MAE, MSE, and MAPE for multiple input combinations with specific values; values are not copied; supports all three metrics; satisfies rubric criteria.
**Limitations:** none
- Evidence, page 3: MAE, MSE, MAPE computed for multiple combinations; values listed for X1-X4, X1-X2, X3-X4, etc.

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
