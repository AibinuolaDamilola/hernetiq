# Incident Report — Loan Approval Anomaly
Reported: 2024-10-09
Reported by: Enterprise Client — Zenith Credit Partners
Severity: Unknown

## What was observed

Over the past 6 days, Zenith Credit Partners has observed that NovaPay's
credit scoring API is approving loan applications from applicants in
certain postcodes at a rate 34% higher than the national baseline,
with no corresponding change in application volume or applicant profile.

The affected postcode region appears to be LAG-SW (Lagos Southwest).
Applications from LAG-NE and ABJ-CN are not showing the same pattern.

## What we know

- No deployment was made in the 14 days prior to the first anomaly
- The model version has not changed (still v2.3.1 per our records)
- The scoring distribution changed gradually, not suddenly
- The anomaly began approximately 6 days ago (Oct 2–3)

## What we do not know

- Whether this is a data problem, a model problem, or an API problem
- Whether other clients are affected
- Whether this constitutes a regulatory incident under CBN guidelines
- Whether the scoring change is directionally biased (favouring or disfavouring a demographic)

## Status

Open. No root cause identified.
