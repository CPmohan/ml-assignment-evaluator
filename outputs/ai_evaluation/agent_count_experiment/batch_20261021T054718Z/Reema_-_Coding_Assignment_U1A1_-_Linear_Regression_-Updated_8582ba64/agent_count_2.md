# 2-Reviewer Evaluation

- Assignment: `Reema - Coding Assignment U1A1 - Linear Regression -Updated.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 5 / 10
- Mean per-criterion reviewer agreement: 90.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are answered correctly: sample count (414), input variables (6), target variable (Y), and meaning (features of dataset). No copied text; answer is student-generated.
**Limitations:** No visual plots or code snippets provided on page 2; extraction may miss full variable meanings, but text implies understanding of input features as dataset 're
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable (target outcome)? Y,House price 4. What does each of the input柱s 
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Cannot Verify
**Feedback:** Student references a '2nd Picture' but no image is present or extractable. No scatter plots or visual evidence shown. Explanation is given but lacks plot support; cannot verify plot-based reasoning.
**Limitations:** Embedded image placeholder present on page 2; text extraction omits visual plots; no actual plot or labeling visible in text.
- Evidence, page 2: Ans: 2nd Picture-Because typically, the variable where the data points are more tightly clustered around a line is better for prediction.
| Q3 Number of samples | 0/1 | 1: 0, 2: 1 | 50% | 0–1 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples. While code snippet is missing, the answer matches expected output. No code shown, but value is correctly stated and matches dataset size; rubric requires output, not just answer.
**Limitations:** No code or output screenshot present; student answer is correct but unsupported by visible code execution.
- Evidence, page 3: Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Train/test split ratio (80:20) is clearly stated and matches common practice. No code shown, but ratio is explicitly reported and meets rubric requirement for stated ratio.
**Limitations:** No code snippet or output visible; however, ratio is correctly stated and meets criteria without needing code output.
- Evidence, page 3: 20% Test,80 % Train.
| Q5 Regression model evaluation | 3/3 | 1: 3, 2: 3 | 100% | 3–3 |

**Decision:** Satisfied
**Feedback:** Student computes and reports MAE, MSE, and MAPE for multiple combinations. Values are specific and not copied; metrics are correctly identified and reported with numerical outputs.
**Limitations:** No code or output screenshot provided; however, values are listed and match evaluation metrics; student work shows computation.
- Evidence, page 4: MAE: 6.0647... MAPE: 0.2115... MAPE: 0.2937...

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
