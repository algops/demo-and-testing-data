# ESG — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `regulation`
- `name` — string
- `abbreviation` — string
- `jurisdiction` — string
- `effective_date` — date
- `scope` — string
- `enforcement_body` — string
- `status` — string
- `transposition_law` — string

## `standard`
- `name` — string
- `code` — string
- `issuing_body` — string
- `version` — string
- `category` — string
- `mandatory` — boolean
- `adoption_status` — string

## `disclosure_requirement`
- `code` — string
- `standard` — string
- `title` — string
- `mandatory_for_all` — boolean
- `subject_to_materiality` — boolean
- `datapoints_count` — number

## `metric`
- `name` — string
- `unit` — string
- `category` — string
- `disclosure_requirement` — string
- `data_source` — string
- `frequency` — string
- `data_quality_score` — number
- `methodology` — string

## `policy`
- `title` — string
- `code` — string
- `version` — string
- `owner_department` — string
- `approval_date` — date
- `next_review_date` — date
- `status` — string
- `scope` — string
- `related_esrs` — string

## `report`
- `title` — string
- `type` — string
- `reporting_period` — string
- `status` — string
- `author` — string
- `assurance_level` — string
- `assurance_provider` — string
- `publication_date` — date
- `format` — string

## `economic_activity`
- `nace_code` — string
- `name` — string
- `taxonomy_eligible` — boolean
- `taxonomy_aligned` — string
- `revenue_share_pct` — number
- `capex_share_pct` — number
- `opex_share_pct` — number
- `sc_criteria_met` — boolean
- `dnsh_status` — string

## `supplier`
- `name` — string
- `id` — string
- `tier` — number
- `country` — string
- `sector` — string
- `risk_score` — string
- `last_assessment_date` — date
- `assessment_status` — string
- `spend_annual_czk` — number
- `critical` — boolean

## `risk`
- `name` — string
- `category` — string
- `subcategory` — string
- `severity` — string
- `likelihood` — string
- `mitigation_status` — string
- `risk_owner` — string
- `last_reviewed` — string

## `target`
- `name` — string
- `category` — string
- `baseline_year` — number
- `baseline_value` — string
- `target_year` — number
- `target_value` — string
- `current_value` — string
- `status` — string
- `sbti_validated` — boolean

## `data_source`
- `name` — string
- `type` — string
- `system` — string
- `owner_department` — string
- `refresh_frequency` — string
- `data_quality_rating` — string
- `coverage_pct` — number
- `known_gaps` — string

## `material_topic`
- `name` — string
- `category` — string
- `impact_score` — number
- `financial_score` — number
- `material` — boolean
- `stakeholder_relevance` — string

## `audit_finding`
- `id` — string
- `type` — string
- `severity` — string
- `metric_affected` — string
- `description` — string
- `status` — string
- `remediation_deadline` — string
