# Quantitative Risk & Business Impact Analysis

**HIPAA Checklist Project**  
Craig Weinstein  
2025-08-14

---

## Quantitative Risk Analysis

| Risk                        | Probability | Impact ($) | SLE ($) | ARO | EMV ($) | ALE ($) |
|-----------------------------|-------------|------------|---------|-----|---------|---------|
| Ransomware Attack           | 0.10        | 50,000     | 50,000  | 0.2 | 5,000   | 10,000  |
| Data Breach (PHI Exposure)  | 0.05        | 200,000    | 200,000 | 0.1 | 10,000  | 20,000  |

- **EMV (Expected Monetary Value) = Probability × Impact**
- **ALE (Annualized Loss Expectancy) = SLE × ARO**
- Example: For ransomware, EMV = 0.10 × $50,000 = $5,000; ALE = $50,000 × 0.2 = $10,000

*This section quantifies risk using standard financial metrics for decision-making.*

---

## Business Impact Analysis (BIA)

| Asset/Process         | RTO (hrs) | RPO (hrs) | MTD (hrs) | Financial Impact ($/hr) | Dependencies                |
|-----------------------|-----------|-----------|-----------|-------------------------|-----------------------------|
| PHI Database          | 4         | 1         | 24        | 5,000                   | App server, backup system   |
| Checklist App         | 8         | 2         | 48        | 2,000                   | PHI DB, user auth service   |

- **RTO (Recovery Time Objective):** Maximum time to restore after disruption
- **RPO (Recovery Point Objective):** Max data loss in hours
- **MTD (Maximum Tolerable Downtime):** Max tolerable downtime
- **Financial Impact:** Estimated cost per hour of downtime

### Dependency Mapping
- PHI Database depends on backup system and app server.
- Checklist App depends on PHI DB and user authentication.

*This section details the business impact and dependencies of critical assets.*

---

## Evaluation Criteria & Stakeholder Approval

- **Multi-criteria risk scoring model:**
  - Financial (weight: 40%)
  - Operational (weight: 25%)
  - Compliance (weight: 20%)
  - Reputation (weight: 15%)
- **Measurement scales:** 1 (Low) to 5 (High) for each factor
- **Scoring rationale:** Weighted sum of factor scores determines risk priority

| Risk                        | Financial | Operational | Compliance | Reputation | Weighted Score |
|-----------------------------|-----------|-------------|------------|------------|----------------|
| Ransomware Attack           | 5         | 4           | 4          | 5          | 4.45           |
| Data Breach (PHI Exposure)  | 5         | 5           | 5          | 5          | 5.00           |

- **Stakeholder Approval:**
  - Criteria and results reviewed and approved by: Craig Weinstein, 2025-08-14

*This section documents the evaluation criteria and formal approval for risk scoring.*

---

*Prepared for executive/academic review. For questions or further details, contact the project security lead.*
