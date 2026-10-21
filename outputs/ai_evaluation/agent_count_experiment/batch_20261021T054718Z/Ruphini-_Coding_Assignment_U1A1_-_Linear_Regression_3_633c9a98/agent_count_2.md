# 2-Reviewer Evaluation

- Assignment: `Ruphini- Coding Assignment U1A1 - Linear Regression (3).pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 2
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 5 / 10
- Mean per-criterion reviewer agreement: 100.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions: sample count (414), input variables (6), target variable (Y), and meaning of inputs. All responses are student-generated and match expected evidence.
**Limitations:** None. Text extraction fully captures all required elements from page 1 without visual gaps or omissions. No embedded images present to require visual review. No
- Evidence, page 1: No: of samples: 414, No: of input Variables: 6, Y= house price of unit area is the output variable, Each of the input variable is an independent variable on which the output变量 Y is
| Q2 Scatter-plot analysis and predictor selection | 2/4 | 1: 2, 2: 2 | 100% | 2–2 |

**Decision:** Partially Satisfied
**Feedback:** Student identifies X3 as best predictor with a valid explanation of negative correlation. However, no scatter plots are visible or extractable on pages 2–4, so plot evidence is missing. No visual proof of X1–X4 vs Y plots exists to support 
**Limitations:** No scatter plots visible or extractable. Page 2 and 3 are blank or contain only text without plots. Visual evidence of scatter plots is absent, so plot analysis
- Evidence, page 3: The X3 variable – "distance to the nearest MRT station" is better in predicting the variable as the distance decreases the target variable y "house price of unit area" increases. 
| Q3 Number of samples | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student correctly states that X.shape gives sample count and references code. Though no output is shown, the explanation implies the code computes 414 samples. The prompt does not require output, only code or calculation. The student's text
**Limitations:** No actual output showing 414 is visible. However, the student's explanation and context imply correct computation. The absence of output does not invalidate the
- Evidence, page 4: X.shape returns the number of rows in the feature matrix X, which corresponds to the total number of samples in the dataset. From the code:
| Q4 Train/test split | 1/1 | 1: 1, 2: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Clearly states a train/test split ratio (1:2 or 33.3%:66.7%) and supports it with text. No code is shown, but the ratio is explicitly reported and valid. The assignment does not prescribe a ratio, so this is acceptable.
**Limitations:** No code or output showing the split is visible. However, the ratio is clearly stated and meets the rubric requirement for reported split. Visual confirmation of
- Evidence, page 5: The train test split ratio is: Test ration: 33.333% (1/3) Train Ratio: 66.666%(2/3)
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student mentions MAE, MSE, and MAPE but provides no code or output showing computed values. No screenshot or result is visible. The rubric requires code/output supporting the metrics, which is missing.
**Limitations:** No code or output for MAE, MSE, or MAPE is visible. The student references a sample link but does not include actual computed results. Visual evidence is absent
- Evidence, page 5: Evaluate the linear regression model by computing the MAE, MSE and Mean Absolute Percentage Error (MAPE) .

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
