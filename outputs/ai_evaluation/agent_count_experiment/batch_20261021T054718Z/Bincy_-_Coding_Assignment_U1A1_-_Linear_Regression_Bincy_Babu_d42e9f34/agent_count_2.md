# 2-Reviewer Evaluation

- Assignment: `Bincy - Coding Assignment U1A1 - Linear Regression Bincy Babu.pdf`
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
**Feedback:** Correctly identifies input variables and their meanings; all four dataset questions answered accurately in student text.
**Limitations:** None, as meanings are fully stated in text.
- Evidence, page 1: Column 2 (X1): Transaction Date  Column 3 (X2): House Age  Column 4 (X3): Distance to the nearest MRT Station  Column 5 (X4): Number of convenience stores  Column 6 (X5): Latitude 
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Provides a selection and explanation, but no scatter plots are visible or referenced in text or images; plot evidence missing, so analysis cannot be verified.
**Limitations:** No scatter plots or visual evidence present; text extraction omits plot content; reviewer must visually confirm plot evidence on page 1 or 2.
- Evidence, page 1: X3(distance to the nearest MRT station) has a clear trend with the output variable (house price of unit area), so X3 is better in predicting the output variable.
| Q3 Number of samples | 0/1 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Satisfied
**Feedback:** Student states 414 samples, but no code or output is shown; prompt requires student's own code/output to count samples; missing evidence for 414 count via code/output.
**Limitations:** No code or output shown; student only states answer without supporting computation.
- Evidence, page 2: Write code to find out how many samples are there in total in this dataset?
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Clearly states 80-20 split ratio; supported by text; no code required as ratio is stated and valid; rubric allows any ratio.
**Limitations:** None; ratio is explicitly stated and valid.
- Evidence, page 2: Train test split ratio is 80-20. (Test size=0.2)
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** No MAE, MSE, or MAPE values or code shown; student references performance but provides no computed metrics or outputs; values not computed or verified.
**Limitations:** No metrics or code output visible; student only lists input combinations without performance values.
- Evidence, page 3: Performance measures for different input combinations

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
