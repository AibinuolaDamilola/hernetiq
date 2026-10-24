# Incident Report — Fraud Model Regression
Reported: 2024-10-08
Reported by: Internal risk team
Severity: Unknown

## What was observed

Transactions that were flagged and blocked by the fraud detection model
three weeks ago are now passing through without flags. The transaction
profiles are identical to previously blocked ones.

Examples from audit log:
- TXN-88445 (Oct 3) — PASS — matches previously blocked TXN-87201
- TXN-88512 (Oct 4) — PASS — matches previously blocked TXN-87290
- TXN-88601 (Oct 5) — PASS — matches previously blocked TXN-87311
- TXN-88701 (Oct 6) — PASS — matches previously blocked TXN-87402

## What we know

- The fraud model shares the same fine-tuning pipeline as the credit model
- No deliberate changes were made to fraud detection thresholds
- The regression began approximately 7 days ago (around Oct 1)
- The fine-tuning pipeline ran on Oct 1 (see audit log: pipeline_run events)

## What we do not know

- Whether the fine-tuning pipeline affected the fraud model weights
- Whether the data sources used in the Oct 1 pipeline run are responsible
- Whether this is related to the loan approval anomaly (Incident 001)

## Status

Open. No root cause identified.
