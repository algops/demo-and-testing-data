# LEGAL — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `legislation`
- `name` — string
- `number` — number
- `type` — string
- `effective_date` — date
- `area_of_law` — string
- `status` — string
- `key_sections` — string
- `last_amendment` — string

## `court_decision`
- `court` — string
- `case_number` — string
- `decision_date` — date
- `legal_area` — string
- `key_holding` — string
- `cited_legislation` — string
- `relevance_score` — number
- `internal_note` — string

## `contract`
- `title` — string
- `type` — string
- `matter_id` — string
- `client` — string
- `counterparty` — string
- `execution_date` — date
- `status` — string
- `value_czk` — number
- `governing_law` — string
- `template_used` — string
- `deviations_from_template` — string
- `language` — string

## `template`
- `title` — string
- `code` — string
- `type` — string
- `version` — string
- `author` — string
- `last_updated` — date
- `language` — string
- `jurisdiction` — string
- `status` — string
- `known_issues` — string

## `legal_opinion`
- `title` — string
- `id` — string
- `matter_id` — string
- `author` — string
- `date` — date
- `area_of_law` — string
- `confidentiality` — string
- `status` — string
- `cited_decisions_count` — number
- `cited_legislation_count` — number

## `counterparty`
- `name` — string
- `id` — string
- `type` — string
- `sector` — string
- `aml_status` — string
- `aml_last_check` — string
- `engagement_since` — string
- `key_contact` — string
- `conflict_check_complete` — boolean
- `revenue_tier` — string

## `matter`
- `id` — string
- `title` — string
- `type` — string
- `client_id` — string
- `lead_partner` — string
- `team_members` — string
- `status` — string
- `opened_date` — date
- `closed_date` — date
- `area_of_law` — string
- `fee_arrangement` — string
- `total_billed_czk` — number
- `wip_czk` — number

## `internal_guideline`
- `title` — string
- `code` — string
- `category` — string
- `version` — string
- `approved_by` — string
- `effective_date` — date
- `next_review_date` — date
- `status` — string

## `legal_area`
- `name` — string
- `code` — string
- `parent_area` — string
- `team_lead` — string
- `headcount` — number

## `person`
- `name` — string
- `role` — string
- `seniority` — string
- `legal_area` — string
- `bar_number` — string
- `joined_date` — date
- `hourly_rate_czk` — number
- `utilization_target_pct` — number
- `languages` — string

## `ddproject`
- `id` — string
- `matter_id` — string
- `type` — string
- `target_company` — string
- `status` — string
- `total_documents` — string
- `reviewed_documents` — string
- `red_flags_count` — number
- `report_status` — string
