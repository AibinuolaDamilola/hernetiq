# NovaPay AI Governance Policy
**Version:** 1.0
**Owner:** CTO Office
**Effective date:** 2024-03-01
**Review cycle:** Annual

---

## 1. Purpose

This policy establishes NovaPay's approach to the responsible development, deployment, and ongoing management of AI systems used in our products and operations. It applies to all machine learning models and automated decision systems that affect customer outcomes.

---

## 2. Scope

This policy covers:

- Credit scoring models used to evaluate loan applications
- Fraud detection models used to flag or block transactions
- Any future AI system that makes or assists in financial decisions affecting NovaPay customers or enterprise clients

---

## 3. AI System Inventory

NovaPay maintains an internal register of AI systems in production. Each system is documented with:

- Model name and current version
- Business function and decision type (fully automated / assisted / advisory)
- Input features and output schema
- Owning team and technical contact

The register is maintained in `system-architecture.md` and updated when new systems are introduced or existing systems are substantially changed.

---

## 4. Data Governance

### 4.1 Training data sources

All training data sources used in production model pipelines must be listed in `model/training_data_manifest.json`. Sources are categorised as internal, partner bureau, or external.

Internal and partner bureau sources are subject to schema validation and hash verification before ingestion. External sources require documented approval before being added to the manifest.

### 4.2 Data quality

Data pipelines include quality checks prior to model training. Schema violations in internal and partner sources will fail the pipeline run.

### 4.3 Data retention

Training datasets are retained for a minimum of 12 months to support model audits and regulatory enquiries.

---

## 5. Model Development

### 5.1 Model documentation

Each production model must have a model card documenting intended use, training data sources, key performance metrics, and known limitations. Model cards are maintained in `model/`.

### 5.2 Model evaluation

Models are evaluated on a held-out test set prior to deployment. Evaluation results are recorded in the model card.

### 5.3 Model versioning

Model versions are tracked in the engineering system. Version identifiers are logged in the production audit trail.

---

## 6. Deployment

### 6.1 Deployment process

Production model deployments are managed through the engineering pipeline. Deployments are logged to the centralised audit trail with the triggering event and version identifiers.

### 6.2 Rollback capability

The previous model version is retained in the model artifact store to support rollback in the event of a production incident. Rollback is initiated by the engineering team.

---

## 7. Monitoring and Incident Response

### 7.1 Performance monitoring

Production models are monitored for latency and availability. Significant anomalies in model outputs reported by enterprise clients are reviewed by the engineering and risk teams.

### 7.2 Incident documentation

Anomalies or incidents involving model behaviour are documented in `/incidents/` and assigned to a responsible owner for investigation.

---

## 8. Multi-Tenant Data Isolation

NovaPay serves multiple enterprise clients whose data must be strictly isolated. API access controls ensure that authenticated clients can access only their own data. Tenant isolation is enforced at the API layer via JWT-based authentication.

---

## 9. Regulatory Alignment

NovaPay operates under Central Bank of Nigeria (CBN) guidelines for credit operations. AI-assisted credit decisions comply with applicable consumer protection and fair lending regulations. This policy will be updated as the regulatory landscape evolves, including in response to applicable frameworks from NIST and international AI governance standards.

---

## 10. Policy Review

This policy is reviewed annually or following a material AI system incident. Changes are approved by the CTO and logged in version control.

---

*Version 1.0 approved: Adaeze Okonkwo, CTO*
