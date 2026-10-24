# NovaPay System Architecture

## Component Overview

```
[Enterprise Client (e.g. Zenith Credit Partners)]
        |
        | HTTPS — REST API
        v
[API Gateway / Rate Limiter]
        |
        v
[Auth Middleware] ← JWT validation
        |
        v
[Credit Scoring Service]     [Fraud Detection Service]
        |                            |
        v                            v
[Credit Model v2.3.1]       [Fraud Model v1.8.2]
        |                            |
        +----------+-----------------+
                   |
                   v
         [Fine-Tuning Pipeline]
                   |
                   v
        [Training Data Sources]
         - Internal transaction data
         - Partner bureau data
         - External data feeds
```

## Key Services

### Credit Scoring Service
- Input: loan application (applicant profile, postcode, transaction history)
- Output: approval score (0–100), decision (APPROVE / DECLINE / REVIEW)
- Model version: v2.3.1
- Serving: FastAPI, deployed on GCP Cloud Run

### Fraud Detection Service
- Input: transaction event (amount, merchant, device fingerprint)
- Output: risk score, flag (PASS / FLAG / BLOCK)
- Model version: v1.8.2
- Serving: FastAPI, deployed on GCP Cloud Run

### Fine-Tuning Pipeline
- Scheduler: Airflow (weekly cadence)
- Data sources: see `model/training_data_manifest.json`
- Last run: 2024-10-01 (run-20241001-0901, see audit log)

### API Layer
- Auth: JWT-based
- Multi-tenant: yes (enterprise clients isolated by tenant_id)
- Rate limiting: configured (see `api/rate_limiter.py`)

## Infrastructure
- Cloud: GCP
- Database: Cloud SQL (PostgreSQL)
- Storage: GCS buckets per environment (dev / staging / prod)
- CI/CD: GitHub Actions → Cloud Run

## Known gaps (as of last engineering review)
- Staging environment not fully mirroring prod
- Alerting on model drift not yet configured
- Audit log retention policy not enforced
