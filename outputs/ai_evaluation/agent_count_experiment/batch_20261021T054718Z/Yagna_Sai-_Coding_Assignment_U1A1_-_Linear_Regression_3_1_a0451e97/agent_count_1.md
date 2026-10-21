# 1-Reviewer Evaluation

- Assignment: `Yagna Sai- Coding Assignment U1A1 - Linear Regression (3) (1).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 2 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions: sample count (414), input variables (6), target variable (Y), and meaning of input variables (features of real estate). No copied text; directly from student work.
**Limitations:** None; all answers are explicitly stated in text and match expected evidence without visual dependency. Text extraction is complete and verifiable here. 1 mark: 
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable? Y house price of unit area 4. What does each of the inputcolumns
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Only asks about scatter plots and predictor selection without any actual scatter plot evidence or explanation. No plot or reasoning provided in text or images; missing plot evidence and explanation as required by rubric.
**Limitations:** No scatter plots or visual evidence present in text; page 3-4 are blank or unextractable. Reviewer must visually confirm if plots exist and if explanation is in
- Evidence, page 2: Using the scatter plots between each of the input features (X1-X4) and the output (Y), which input variable, do you think, is better in predicting the output / target variable ?
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Partially Satisfied
**Feedback:** States 414 samples but no code or output showing the count. The answer is correct but lacks supporting code or output as required by rubric. Cannot verify computation from student work.
**Limitations:** No code or output shown in text; student only states the number without demonstrating how it was computed. Visual confirmation needed for code execution.
- Evidence, page 5: 2. Write code to find out how many samples are there in total in this dataset? 
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Clearly states a train/test split ratio (80:20) without prescribing a required ratio. The ratio is reported and matches expected evidence; no code is needed as ratio is stated directly.
**Limitations:** No code shown, but the ratio is clearly stated and sufficient per rubric. Rubric allows any split; 80:20 is valid.
- Evidence, page 6: I have selected an 80:20 split ratio for the train and test sets.
| Q5 Regression model evaluation | 0/3 | 1: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** States evaluation is performed but provides no computed values or supporting code/output for MAE, MSE, or MAPE. No values reported or verified in text or images; missing metric computation as required.
**Limitations:** No MAE, MSE, or MAPE values or code output visible in text; visual confirmation needed for computed metrics. Cannot verify any of the three metrics.
- Evidence, page 6: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE) .

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
