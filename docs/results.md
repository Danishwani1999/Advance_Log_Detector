# Evaluation results

Synthetic test set: 10,000 log lines, 335 injected problems
(made by scripts/generate_logs.py, seed 42).

| Method | Flagged | Precision | Recall | F1 |
|---|---|---|---|---|
| v1: Isolation Forest fitted on each batch (contamination 0.2) | 1068 | 0.31 | 1.00 | 0.48 |
| Baseline rule: level is ERROR or CRITICAL | 508 | 0.62 | 0.93 | 0.74 |
