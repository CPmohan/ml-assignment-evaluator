# 3-Reviewer Evaluation

- Assignment: `S Devika - Coding Assignment U1A1 - Linear Regression A1.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 3
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 2 / 10
- Mean per-criterion reviewer agreement: 93.3%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target (Y), and meaning of each input variable. No copied text or placeholders.
**Limitations:** None. Text extraction fully captures all required responses on page 1. No visual elements needed for this criterion. All answers are explicitly stated and verid
- Evidence, page 1: 1. How many samples are there? 414
2. How many input variables are there? 6
3. Which column is the output variable? Y= house price of unit area
4. What does each of the input cols?
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0, 2: 2, 3: 0 | 67% | 0–2 |

**Decision:** Not Satisfied
**Feedback:** Only a selected predictor is given without scatter plot evidence. The rubric requires scatter plots for X1-X4 vs Y and a plot-based explanation. No plot or visual evidence is present in text or image pages.
**Limitations:** No scatter plots or visual evidence present in text. A reviewer must visually confirm if plots exist on embedded_images>0 pages, which are not provided or cited
- Evidence, page 2: The input variable X3 (the distance to the Nearest MRT Station) is better in predicting the output / target variable (house price of unit area)
| Q3 Number of samples | 0/1 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** The student states 414 samples. However, no actual code or output is provided to show how the count was computed. The rubric requires code or calculation showing 414. This is missing.
**Limitations:** No code or output is present to verify the 414 sample count. The student only states the number without supporting computation.
- Evidence, page 2: 2. Write code to find out how many samples are there in total in dataset? 
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The train/test split ratio (80:20) is clearly stated and matches expected evidence. No code is required as the ratio is reported. The assignment does not prescribe a ratio, so this is valid.
**Limitations:** None. The split ratio is explicitly stated and verifiable from text.
- Evidence, page 3: 80:20 Split: approximately 80% of the data is assigned to the training set, while the remaining 20% forms the test set.
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** The student mentions computing MAE, MSE, and MAPE but provides no actual values or supporting code/output. The rubric requires computed values with supporting evidence.
**Limitations:** No computed metrics or output shown. The student only references the computation without values or code.
- Evidence, page 3: 4. Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE).

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
