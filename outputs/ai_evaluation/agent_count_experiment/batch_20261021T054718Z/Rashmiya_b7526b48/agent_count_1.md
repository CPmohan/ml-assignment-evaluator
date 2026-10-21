# 1-Reviewer Evaluation

- Assignment: `Rashmiya.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 4 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are answered correctly: sample count (414), input variables (6), target (Y), and meaning of inputs. No copied text; answer is student-generated.
**Limitations:** None. Text is fully extractable and directly addresses all expected evidence points on page 1. No visual elements needed for this criterion. 1 mark awarded as a
- Evidence, page 1: 1. How many samples are there? Ans: 414 2. How many input variables are there? Ans: 6 3. Which column is the output variable? Ans: Y(House price of unit area) 4. What does each of 
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0 | 100% | 0–0 |

**Decision:** Cannot Verify
**Feedback:** Scatter plots for X1-X4 vs Y are referenced but no actual plots or visual evidence is present on page 2–4. The student mentions analysis but no plot evidence exists to verify the plots or the explanation. Cannot verify predictor selection.
**Limitations:** Pages 2–4 contain embedded_images>0 but no actual scatter plot images are visible or extractable. Visual confirmation required to verify scatter plot evidence.
- Evidence, page 2: 1. Understanding the dataset [4 marks] There are many input variables in this dataset. Use only X1 to X4 as input variables, and y as the output variable. Using the scatter plots
| Q3 Number of samples | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student states 414 samples, and while code is not shown, the answer matches the expected output. The prompt does not require code output, only the count. Answer is correct and directly stated.
**Limitations:** No code or output is visible on page 5. However, the stated result (414) is correct and matches the expected value. No need for code output as per rubric.
- Evidence, page 5: 2. Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student clearly states a train/test split ratio (70:30) and provides a clear explanation. This meets the rubric requirement for a reported ratio with no prescribed value.
**Limitations:** No code or output is visible, but the stated ratio is sufficient per rubric. The assignment does not require a specific ratio, so 70:30 is valid.
- Evidence, page 5: The train test split ratio is 70:30. (70% training model and 30% testing set).
| Q5 Regression model evaluation | 1/3 | 1: 1 | 100% | 1–1 |

**Decision:** Partially Satisfied
**Feedback:** The student mentions computing MAE, MSE, and MAPE, but no code or output showing the actual values is present. Values are not reported or verified. Only the request is made, not the computed results.
**Limitations:** No code or output for MAE, MSE, or MAPE is visible. The student did not provide computed values, so metrics cannot be verified.
- Evidence, page 5: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE).

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
