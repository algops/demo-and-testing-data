# ESG — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `regulation` | Regulation | name, abbreviation, jurisdiction, effective_date, scope, enforcement_body, status, transposition_law |
| `standard` | Standard | name, code, issuing_body, version, category, mandatory, adoption_status |
| `disclosure_requirement` | DisclosureRequirement | code, standard, title, mandatory_for_all, subject_to_materiality, datapoints_count |
| `metric` | Metric | name, unit, category, disclosure_requirement, data_source, frequency, data_quality_score, methodology |
| `policy` | Policy | title, code, version, owner_department, approval_date, next_review_date, status, scope, related_esrs |
| `report` | Report | title, type, reporting_period, status, author, assurance_level, assurance_provider, publication_date, format |
| `economic_activity` | EconomicActivity | nace_code, name, taxonomy_eligible, taxonomy_aligned, revenue_share_pct, capex_share_pct, opex_share_pct, sc_criteria_met, dnsh_status |
| `supplier` | Supplier | name, id, tier, country, sector, risk_score, last_assessment_date, assessment_status, spend_annual_czk, critical |
| `risk` | Risk | name, category, subcategory, severity, likelihood, mitigation_status, risk_owner, last_reviewed |
| `target` | Target | name, category, baseline_year, baseline_value, target_year, target_value, current_value, status, sbti_validated |
| `data_source` | DataSource | name, type, system, owner_department, refresh_frequency, data_quality_rating, coverage_pct, known_gaps |
| `material_topic` | MaterialTopic | name, category, impact_score, financial_score, material, stakeholder_relevance |
| `audit_finding` | AuditFinding | id, type, severity, metric_affected, description, status, remediation_deadline |
