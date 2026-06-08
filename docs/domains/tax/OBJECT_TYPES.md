# TAX — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `tax_law` | TaxLaw | name, number, type, area, effective_date, key_sections, last_amendment, status |
| `accounting_standard` | AccountingStandard | name, code, issuing_body, scope, version, status |
| `tax_form` | TaxForm | name, form_number, tax_type, filing_frequency, deadline_rule, electronic_only, system_used |
| `account` | Account | number, name, class, group, type, tax_relevance, standard_reference |
| `tax_rate` | TaxRate | type, rate_pct, applicable_to, effective_from, effective_to, conditions, law_reference |
| `legal_entity` | LegalEntity | name, id, ico, dic, legal_form, sector, size_category, audit_required, consolidation, accounting_system, fiscal_year, ifrs, engagement_since, responsible_partner, fee_monthly_czk |
| `engagement` | Engagement | id, client_id, type, period, status, responsible_person, fee_czk, deadline, filed_date, notes |
| `internal_procedure` | InternalProcedure | title, code, category, version, owner, last_updated, status, known_gaps |
| `deadline` | Deadline | name, type, base_date_rule, offset_days, extension_possible, extension_condition, penalty_czk, applies_to |
| `tax_ruling` | TaxRuling | id, topic, issuing_authority, date, binding, area, superseded_by, practical_impact |
| `tax_treaty` | TaxTreaty | countries, treaty_number, effective_date, withholding_rates, applicable_articles |
| `tax_control` | TaxControl | id, client_id, tax_type, period_under_review, authority, status, findings_amount_czk, contested |
