# 1-Reviewer Evaluation

- Assignment: `Jisha ML.pdf`
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
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (y), and meaning of input variables. No copied text; answers are student-generated.
**Limitations:** None; all text is extractable and directly addresses the required elements in the student response on page 1.
- Evidence, page 1: 1. How many samples are there? << 414 >> 2. How many input variables are there? << 6 >> 3. Which column is the output variable? << y house price of unit area >> 4. What does eachof
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Scatter plots for X1-X4 vs Y are present and visualized. A predictor (distance to MRT) is selected with a plot-based explanation. However, the explanation lacks depth or statistical grounding; full marks require a more rigorous analysis.
**Limitations:** No visual plots are provided in text; the explanation is inferred from text but not verified against actual plot images. A reviewer must visually confirm the 't
- Evidence, page 2: plt.scatter(x1,y,color='red') ... plt.scatter(x4,y) ... Distance to the nearest MRT station: This can better predict the model because most of the samples are clustered together in
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Cannot Verify
**Feedback:** The student states '414' but no code or output showing the sample count computation is present. The evidence is missing; the value is stated without supporting code or output.
**Limitations:** No code or output is visible on page 4 for sample count computation; the student's answer is text-only and lacks executable evidence.
- Evidence, page 4: 2. Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student clearly states a train/test split ratio (70:30) and provides it in a section with no ambiguity. This meets the rubric requirement for a reported split ratio.
**Limitations:** None; the ratio is explicitly stated and verifiable in text.
- Evidence, page 5: The train test split ratio selected is 70:30
| Q5 Regression model evaluation | 0/3 | 1: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** The student mentions MAE, MSE, and MAPE but provides no computed values or supporting code/output. The metrics are referenced without actual computation or results.
**Limitations:** No code or output showing MAE, MSE, or MAPE values is present; the student only references the metrics without computing or reporting them.
- Evidence, page 5: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE)

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
