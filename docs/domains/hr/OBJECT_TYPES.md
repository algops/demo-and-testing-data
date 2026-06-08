# HR — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `policy` | Policy | title, code, category, version, effective_date, next_review_date, owner, status, applies_to, known_issues, language |
| `process` | Process | name, code, category, owner, sla_days, approval_chain, system, digitalization_pct, known_bottleneck |
| `benefit` | Benefit | name, type, provider, monthly_value, eligibility, enrollment_period, taxable, utilization_pct, applies_to, status |
| `role` | Role | title, code, department, level, band, reports_to, headcount, location, shift_work |
| `department` | Department | name, code, head, headcount, budget_center, location, interim_head |
| `training` | Training | name, code, type, mandatory, frequency, duration_hours, provider, certification, evidence_system, compliance_rate_pct |
| `document` | Document | title, code, type, template_available, location, format, required_for, retention_years, status |
| `system` | System | name, type, vendor, url, admin_contact, go_live_date, module_status, data_completeness |
| `leave_type` | LeaveType | name, code, days_per_year, carryover_allowed, carryover_max_months, approval_required, documentation_needed, applies_to, system |
| `legal_requirement` | LegalRequirement | name, law_reference, requirement_type, frequency, deadline, penalty, responsible, compliance_status |
| `compensation_band` | CompensationBand | band, label, min_base_czk, max_base_czk, variable_pct_max, typical_roles, auto_policy, benefits_tier |
| `grievance_case` | GrievanceCase | id, type, filed_date, filed_by_role, status, severity, resolution, days_to_resolve |
| `performance_review` | PerformanceReview | cycle, status, completion_rate_pct, avg_rating, applies_to, system |
