# HR — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `policy`
- `title` — string
- `code` — string
- `category` — string
- `version` — string
- `effective_date` — date
- `next_review_date` — date
- `owner` — string
- `status` — string
- `applies_to` — string
- `known_issues` — string
- `language` — string

## `process`
- `name` — string
- `code` — string
- `category` — string
- `owner` — string
- `sla_days` — number
- `approval_chain` — string
- `system` — string
- `digitalization_pct` — number
- `known_bottleneck` — string

## `benefit`
- `name` — string
- `type` — string
- `provider` — string
- `monthly_value` — string
- `eligibility` — string
- `enrollment_period` — string
- `taxable` — boolean
- `utilization_pct` — number
- `applies_to` — string
- `status` — string

## `role`
- `title` — string
- `code` — string
- `department` — string
- `level` — string
- `band` — string
- `reports_to` — string
- `headcount` — number
- `location` — string
- `shift_work` — boolean

## `department`
- `name` — string
- `code` — string
- `head` — string
- `headcount` — number
- `budget_center` — string
- `location` — string
- `interim_head` — string

## `training`
- `name` — string
- `code` — string
- `type` — string
- `mandatory` — boolean
- `frequency` — string
- `duration_hours` — number
- `provider` — string
- `certification` — string
- `evidence_system` — string
- `compliance_rate_pct` — number

## `document`
- `title` — string
- `code` — string
- `type` — string
- `template_available` — boolean
- `location` — string
- `format` — string
- `required_for` — string
- `retention_years` — number
- `status` — string

## `system`
- `name` — string
- `type` — string
- `vendor` — string
- `url` — string
- `admin_contact` — string
- `go_live_date` — date
- `module_status` — string
- `data_completeness` — string

## `leave_type`
- `name` — string
- `code` — string
- `days_per_year` — number
- `carryover_allowed` — boolean
- `carryover_max_months` — number
- `approval_required` — boolean
- `documentation_needed` — string
- `applies_to` — string
- `system` — string

## `legal_requirement`
- `name` — string
- `law_reference` — string
- `requirement_type` — string
- `frequency` — string
- `deadline` — date
- `penalty` — string
- `responsible` — string
- `compliance_status` — string

## `compensation_band`
- `band` — string
- `label` — string
- `min_base_czk` — number
- `max_base_czk` — number
- `variable_pct_max` — number
- `typical_roles` — string
- `auto_policy` — boolean
- `benefits_tier` — string

## `grievance_case`
- `id` — string
- `type` — string
- `filed_date` — date
- `filed_by_role` — string
- `status` — string
- `severity` — string
- `resolution` — string
- `days_to_resolve` — number

## `performance_review`
- `cycle` — string
- `status` — string
- `completion_rate_pct` — number
- `avg_rating` — number
- `applies_to` — string
- `system` — string
