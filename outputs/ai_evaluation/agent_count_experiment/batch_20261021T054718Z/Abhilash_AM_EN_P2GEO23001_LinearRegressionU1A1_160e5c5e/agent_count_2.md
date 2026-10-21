# 2-Reviewer Evaluation

- Assignment: `Abhilash_AM.EN.P2GEO23001_LinearRegressionU1A1.pdf`
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
**Feedback:** All four dataset questions are answered correctly: sample count (414), input variables (6), target variable (Y), and meaning of each input variable. No copied text; answers match expected evidence.
**Limitations:** None. Text extraction fully captures all required responses on page 1. No visual elements present to affect verifiability. All answers are explicitly stated in 
- Evidence, page 1: 1. How many samples are there? Answer: 414
2. How many input variables are there? Answer: 6
3. Which column is the output variable (target outcome)? Answer: Y house price of unit面积
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X3 as predictor and gives a reason based on correlation, but no scatter plots or visual evidence is provided. Plot evidence is missing, so explanation lacks grounding in plot data as required by rubric.
**Limitations:** No scatter plots or visual evidence present on any page. Text extraction omits plot images; student's reasoning is not supported by actual plot data. A reviewer
- Evidence, page 1: Answer: X3 (distance to the nearest MRT station). Because it shows stronger correlation with the target variable compared to the other input variables.
| Q3 Number of samples | 0/1 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples in answer to question 1, but no code or output is provided. The rubric requires code or calculation showing 414. Without code or output, this evidence is missing.
**Limitations:** No code or output is present in the submission. The answer '414' is stated but not backed by student-written code or execution result.
- Evidence, page 2: 2. Write code to find out how many samples are there in total in this dataset? [1 mark]
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student clearly states a train/test split ratio (1/4 or 25%-75%) and provides it in text. No code is required; the ratio is explicitly reported and valid under rubric.
**Limitations:** None. The split ratio is clearly stated and matches expected format. No visual or code evidence needed as per rubric.
- Evidence, page 2: 3. What is the train test split ratio you have chosen? [1 Mark] Answer: 1/4 (25% - 75%)
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** No MAE, MSE, or MAPE values are reported or supported by code/output. The question is raised but no metrics are computed or presented. Rubric requires computed values with supporting evidence.
**Limitations:** No code, output, or computed values for MAE, MSE, or MAPE are present. Text extraction omits any numerical results or model evaluation output.
- Evidence, page 3: 4. Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE). [3 marks]

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
