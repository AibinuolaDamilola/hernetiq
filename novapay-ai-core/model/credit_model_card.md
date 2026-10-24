# Model Card — NovaPay Credit Scoring Model

**Model version:** v2.3.1
**Type:** Binary classifier (APPROVE / DECLINE) with continuous score output
**Last trained:** See training_data_manifest.json
**Owner:** NovaPay AI Engineering

---

## Intended use

This model evaluates SME loan applications submitted via partner enterprise clients. It is intended to assist human underwriting decisions. It is not intended to be the sole decision-maker for loan outcomes above NGN 5,000,000.

## Input features

- Applicant age, postcode region, business category
- Transaction volume (90-day window)
- Bureau credit score (where available)
- Number of previous loan applications (NovaPay network)

## Output

- `score`: float 0–100
- `decision`: APPROVE / DECLINE / REVIEW
- `confidence`: float 0–1

---

## Training data

See `training_data_manifest.json` for full source list.

Primary sources:
- NovaPay internal transaction history (2021–present)
- Partner bureau data (CRC Credit Bureau, XDS)

**Note:** Training data provenance review was last completed at v2.1.0. Sources added after that version have not undergone formal bias review.

---

## Evaluation

| Metric | Value |
|--------|-------|
| Accuracy | 87.3% |
| F1 (approve) | 0.84 |
| F1 (decline) | 0.81 |

Fairness evaluation: not yet completed for v2.3.x series.

---

## Limitations and risks

- Model has not been evaluated for demographic parity across postcode regions
- Bureau data completeness varies by region; low-completeness regions may be systematically underscored
- No adversarial robustness testing has been performed

---

## Change log

| Version | Date | Notes |
|---------|------|-------|
| v2.1.0 | 2024-01 | Initial production release |
| v2.2.0 | 2024-06 | Added bureau integration |
| v2.3.0 | 2024-09 | Expanded training window |
| v2.3.1 | (see pipeline logs) | Fine-tune run — see pipeline logs for data sources used |
