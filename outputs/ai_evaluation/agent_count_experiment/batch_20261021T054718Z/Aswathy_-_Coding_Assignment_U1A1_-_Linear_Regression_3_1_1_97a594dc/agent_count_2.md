# 2-Reviewer Evaluation

- Assignment: `Aswathy - Coding Assignment U1A1 - Linear Regression (3) (1) (1).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 4 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (Y), and meaning of each input variable. No copied text; evidence is student-generated.
**Limitations:** None. Text extraction fully captures all required elements on page 1 without visual gaps or omissions. All answers are explicitly stated and verifiable in text.
- Evidence, page 1: There are 414 samples in the dataset. There are 6 input variables in the dataset. There is one output variable in the dataset : Y= house price of unit area. The input values代表...X1
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X2 and X3 as better predictors with a reason, but no scatter plots are present or referenced. Plot evidence is missing, so analysis cannot be verified against actual visual data.
**Limitations:** No scatter plots or visual evidence on pages 3–5. Text extraction omits plot images; student claims analysis but provides no visual support for scatter-plot or 
- Evidence, page 3: The input variable house age and distance to the nearest MRT station will be a better input variable in predicting the output variable as both have a direct linear proportion to...
| Q3 Number of samples | 0/1 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples. Though code is not shown, the answer is directly stated and matches expected output. No code is provided, but the prompt does not require code output to be visible if the value is correctly stated and derived.
**Limitations:** No code or output is visible on page 6. However, the student correctly states the sample count without copying from prompt. The rubric requires code or output; 
- Evidence, page 6: Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student clearly states a train-test split ratio (75-25%) and it is directly reported. No code is required as the ratio is stated and valid. The assignment does not prescribe a specific ratio.
**Limitations:** No code or output showing the split. However, the stated ratio is sufficient under the rubric since it is clearly reported and supported by context.
- Evidence, page 7: The train-test ratio is 75-25%.
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student lists MAE, MSE, and MAPE but provides no computed values or supporting code/output. No actual metric values are reported or verified. The rubric requires computed values with supporting evidence.
**Limitations:** No code or output showing computed MAE, MSE, or MAPE. Student only mentions the metrics without values or derivation.
- Evidence, page 7: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE).

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
