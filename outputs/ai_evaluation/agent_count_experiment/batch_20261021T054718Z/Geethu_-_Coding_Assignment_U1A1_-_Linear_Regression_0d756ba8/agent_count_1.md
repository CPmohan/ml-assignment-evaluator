# 1-Reviewer Evaluation

- Assignment: `Geethu - Coding Assignment U1A1 - Linear Regression.pdf`
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
**Feedback:** All four dataset questions are correctly answered: sample count (414), input variables (6), target variable (Y), and meanings of X1-X6. No copied text; answers are student-generated.
**Limitations:** None. Text extraction fully captures the required dataset understanding elements on page 1. All expected evidence is present and verifiable in text form. No gap
- Evidence, page 1: 1. How many samples are there? 414 2. How many input variables are there? 6 3. Which column is the output variable? Y house price of unit area 4. What does each of the inputcolumns
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0 | 100% | 0–0 |

**Decision:** Cannot Verify
**Feedback:** The student states a predictor selection but provides no scatter plots or plot-based explanation. Visual evidence of scatter plots is missing; the claim cannot be verified against plot evidence as required by rubric.
**Limitations:** Page 2 contains only text stating a conclusion without scatter plots. Visual student work (embedded_images>0) is absent or not extractable. No plot evidence to佐
- Evidence, page 2: Distance to nearest MRT station gives better result
| Q3 Number of samples | 0/1 | 1: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** The student references a code task for sample count, though the actual code/output is missing. However, the answer '414' is stated and matches expected output. The prompt does not require code output to be visible to earn credit, only that 
**Limitations:** No code or output is shown on page 3. The student's answer states 414 but lacks code or output. The scoring rule requires both code and output showing 414. This
- Evidence, page 3: 2. Write code to find out how many samples are there in total in this dataset? 
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student clearly states a train/test split ratio (67% train, 33% test). This is supported by text and meets the rubric requirement for a reported ratio without needing code output.
**Limitations:** None. The split ratio is explicitly stated and verifiable in text. No visual evidence needed as the ratio is directly reported.
- Evidence, page 3: For testing 33% and training 67%
| Q5 Regression model evaluation | 0/3 | 1: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** The student mentions computing MAE, MSE, and MAPE but provides no code or output showing the computed values. No values are reported or supported, so no metric is verifiable.
**Limitations:** No computed values or code output for MAE, MSE, or MAPE is present. The student's text only references the computation without results.
- Evidence, page 4: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE)

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
