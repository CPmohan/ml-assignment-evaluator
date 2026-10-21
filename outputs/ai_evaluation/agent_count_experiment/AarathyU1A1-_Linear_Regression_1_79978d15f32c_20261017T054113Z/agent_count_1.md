# 1-Reviewer Evaluation

- Assignment: `AarathyU1A1- Linear Regression 1.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 1
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 6 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** All four dataset questions are correctly answered with clear, student-generated responses.
**Limitations:** None detected in text extraction or content coverage. Full meaning of input variables is provided in the response text.
- Evidence, page 2: 414, 6, Y house price of unit area, Column 1- X1 transaction date, Column 2- X2 house age, Column 3- X3 distance to the nearest MRT station, Column 4- X4 number of convenience stor
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** The student identifies X2 as better, but no scatter plots or visual evidence are present in the text; plot analysis cannot be verified.
**Limitations:** No scatter plots or visual evidence present in text; reviewer must visually confirm plot evidence on embedded_images>0 pages.
- Evidence, page 2: Using the scatter plots between each of the input features (X1-X4) and the output (Y), which input variable, do you think, is better in predicting the output / target variable ?
| Q3 Number of samples | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The student references code to count samples, though the actual code is missing; the answer '414' matches expected output.
**Limitations:** No visible code output; however, the stated result matches the expected sample count.
- Evidence, page 6: 2. Write code to find out how many samples are there in total in this dataset?  
| Q4 Train/test split | 1/1 | 1: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** The train/test split ratio is clearly stated and consistent across all input variables.
**Limitations:** None detected; ratio is explicitly stated and matches student work.
- Evidence, page 6: Train test split ratio : Train- 70% Test -30%
| Q5 Regression model evaluation | 1/3 | 1: 1 | 100% | 1–1 |

**Decision:** Partially Satisfied
**Feedback:** The student lists MAE, MSE, and MAPE for each X1-X4, but no actual computed values or supporting code/output are provided.
**Limitations:** No computed values or code output for MAE, MSE, or MAPE; values are not verified in text.
- Evidence, page 9: MAE, MSE and MAPE for X1

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
