# Agent-Count Comparison

Assignment: `S Devika - Coding Assignment U1A1 - Linear Regression A1.pdf`

Counts are nested: each row adds one seeded reviewer to the preceding row.
Consensus is the per-criterion mode; tied modes resolve to the lower score.
The 1-reviewer agreement value is 100% by definition and is not inter-reviewer agreement.

| Reviewers | Provisional total | Mean criterion agreement | Q1 | Q2 | Q3 | Q4 | Q5 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2/10 | 100.0% | 1/1 | 0/4 | 0/1 | 1/1 | 0/3 |
| 2 | 2/10 | 90.0% | 1/1 | 0/4 | 0/1 | 1/1 | 0/3 |
| 3 | 2/10 | 93.3% | 1/1 | 0/4 | 0/1 | 1/1 | 0/3 |
| 4 | 2/10 | 90.0% | 1/1 | 0/4 | 0/1 | 1/1 | 0/3 |

The scores are provisional model outputs, not final grades. Reviewer agreement is internal model consistency, not human agreement.

Files: one `agent_count_N.json` and one `agent_count_N.md` per reviewer count; raw per-reviewer responses are in `reviewers/`.
