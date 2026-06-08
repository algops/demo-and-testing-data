# LEGAL — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `legislation` | Legislation | name, number, type, effective_date, area_of_law, status, key_sections, last_amendment |
| `court_decision` | CourtDecision | court, case_number, decision_date, legal_area, key_holding, cited_legislation, relevance_score, internal_note |
| `contract` | Contract | title, type, matter_id, client, counterparty, execution_date, status, value_czk, governing_law, template_used, deviations_from_template, language |
| `template` | Template | title, code, type, version, author, last_updated, language, jurisdiction, status, known_issues |
| `legal_opinion` | LegalOpinion | title, id, matter_id, author, date, area_of_law, confidentiality, status, cited_decisions_count, cited_legislation_count |
| `counterparty` | Counterparty | name, id, type, sector, aml_status, aml_last_check, engagement_since, key_contact, conflict_check_complete, revenue_tier |
| `matter` | Matter | id, title, type, client_id, lead_partner, team_members, status, opened_date, closed_date, area_of_law, fee_arrangement, total_billed_czk, wip_czk |
| `internal_guideline` | InternalGuideline | title, code, category, version, approved_by, effective_date, next_review_date, status |
| `legal_area` | LegalArea | name, code, parent_area, team_lead, headcount |
| `person` | Person | name, role, seniority, legal_area, bar_number, joined_date, hourly_rate_czk, utilization_target_pct, languages |
| `ddproject` | DDProject | id, matter_id, type, target_company, status, total_documents, reviewed_documents, red_flags_count, report_status |
