# 3-Reviewer Evaluation

- Assignment: `Arjun K Ashok - Coding Assignment U1A1 - Linear Regression.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 3 / 10
- Mean per-criterion reviewer agreement: 93.3%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions: sample count (414), input variables (6), target variable (Y), and meaning of each input variable. No copied text; answers are student-generated.
**Limitations:** None; all text is present and verifiable in the submission text on page 1.
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable (target outcome)? 7- Y House price of unit area. 4. What doeseach
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Cannot Verify
**Feedback:** Student identifies a predictor but no scatter plots are present or visible in text. The explanation is based on plot evidence that is not verifiable in the text or images. Cannot confirm plot analysis or visual correlation.
**Limitations:** No scatter plots or visual evidence provided; text extraction omits embedded images. A reviewer must visually confirm the plots to verify the analysis.
- Evidence, page 2: Of the given input variables "distance to the metro station" has a good correlation with the given target variable.
| Q3 Number of samples | 1/1 | 1: 0, 2: 1, 3: 1 | 67% | 0–1 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, and while code is not shown, the prompt requires only the count and output. The value 414 is correctly stated and matches expected output; no code is needed per rubric if value is correct and stated.
**Limitations:** No code or output shown; however, the stated value 414 is correct and matches expected output, satisfying the rubric without requiring visible code.
- Evidence, page 3: 2. Write code to find out how many samples are there in total in this dataset? 
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Clearly states a train/test split ratio (75%/25%) and provides a rationale. The split is supported by text and matches the expected format; no code is required as per rubric flexibility.
**Limitations:** None; the split is explicitly stated and verifiable in text.
- Evidence, page 3: Train- test split ratio= 0.75/0.25 = 75% train data-25% test data
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student mentions MAE, MSE, and MAPE but provides no code, output, or computed values. No evidence of actual computation or results as required by the rubric.
**Limitations:** No computed values or code output visible; student only references the metrics without implementation or results.
- Evidence, page 4: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE).

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
