# 4-Reviewer Evaluation

- Assignment: `Namitha - Coding Assignment U1A1 - Linear Regression_Namitha.pdf`
- Model: `qwen3:4b-instruct`
- Seeded independent requests: 4
- Aggregation: per-criterion mode; ties resolve to the lower score
- AI provisional total: 3 / 10
- Mean per-criterion reviewer agreement: 90.0%

AI suggestions only; a human reviewer must verify every score against the PDF.

| Criterion | Consensus | Reviewer scores | Agreement | Range |
|---|---:|---|---:|---:|
| Q1 Dataset understanding | 1/1 | 1: 1, 2: 1, 3: 1, 4: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Correctly answers all four dataset questions: sample count (414), input variables (6), target variable (Y), and meanings of X1-X6. No copied text; directly from student work.
**Limitations:** None; all answers are explicitly stated in text and match expected evidence without visual dependency. Text extraction is complete and verifiable here. 0 visual
- Evidence, page 1: 1. How many samples are there? 414
2. How many input variables are there? 6
3. Which column is the output variable (target outcome)? Y (house price of unit area)
4. What does each 
| Q2 Scatter-plot analysis and predictor selection | 0/4 | 1: 0, 2: 0, 3: 0, 4: 0 | 100% | 0–0 |

**Decision:** Not Satisfied
**Feedback:** Student mentions scatter plots in question but provides no actual scatter plot evidence or explanation based on plot data. No visual or textual description of plot results or reasoning. Missing plot evidence violates rubric requirement.
**Limitations:** No scatter plots or plot analysis visible in text; student references plots but does not describe or justify selection based on visual evidence.
- Evidence, page 2: Using the scatter plots between each of the input features (X1-X4) and the output (Y), which input variable, do you think, is better in predicting the output / target variable ?
| Q3 Number of samples | 1/1 | 1: 0, 2: 1, 3: 1, 4: 1 | 75% | 0–1 |

**Decision:** Satisfied
**Feedback:** Student references a code snippet and output in the prompt, though the actual code/output is not visible. However, the answer states '414' which matches expected sample count and is directly stated in the response. The student's own answer,
**Limitations:** No actual code or output is visible in the text. But the stated sample count (414) is correct and explicitly provided in the student's text, satisfying the rubr
- Evidence, page 5: Write code to find out how many samples are there in total in this dataset? [1 mark]
<< insert the screenshot of the code snippet and its output from google colab >>
| Q4 Train/test split | 1/1 | 1: 1, 2: 1, 3: 1, 4: 1 | 100% | 1–1 |

**Decision:** Satisfied
**Feedback:** Student clearly states a train/test split ratio (70:30) and references code, satisfying the rubric. Ratio is valid and not prescribed, so not incorrect. Evidence is present in text.
**Limitations:** No actual code snippet shown; only a reference to code is given. However, the ratio is stated and contextually supported. Does not require full code to be valid
- Evidence, page 6: Train test split is in the 70:30 ratio. Please find below the code snippet for distance from MRT station:
| Q5 Regression model evaluation | 0/3 | 1: 0, 2: 0, 3: 0, 4: 3 | 75% | 0–3 |

**Decision:** Not Satisfied
**Feedback:** Student claims low values for MAE, MSE, MAPE for X4, but provides no computed values or supporting code/output. Values are not verified or derived from model predictions. No evidence of actual metric computation.
**Limitations:** No actual MAE, MSE, or MAPE values or code output shown. Student states result without supporting computation or output.
- Evidence, page 7: Distance to the nearest MRT station is having the lowest MAE,MSE and MAPE values

## Limitations

- Each reviewer is a separate seeded request to the same Ollama model, not a separate model process.
- Reviewer agreement is not evidence of correctness or human agreement.
- A human must verify cited evidence and image-only content against the original PDF.
