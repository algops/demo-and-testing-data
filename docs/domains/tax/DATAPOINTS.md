# TAX — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `tax_law`
- `name` — string
- `number` — number
- `type` — string
- `area` — string
- `effective_date` — date
- `key_sections` — string
- `last_amendment` — string
- `status` — string

## `accounting_standard`
- `name` — string
- `code` — string
- `issuing_body` — string
- `scope` — string
- `version` — string
- `status` — string

## `tax_form`
- `name` — string
- `form_number` — string
- `tax_type` — string
- `filing_frequency` — string
- `deadline_rule` — string
- `electronic_only` — boolean
- `system_used` — string

## `account`
- `number` — number
- `name` — string
- `class` — string
- `group` — string
- `type` — string
- `tax_relevance` — string
- `standard_reference` — string

## `tax_rate`
- `type` — string
- `rate_pct` — number
- `applicable_to` — string
- `effective_from` — date
- `effective_to` — date
- `conditions` — string
- `law_reference` — string

## `legal_entity`
- `name` — string
- `id` — string
- `ico` — string
- `dic` — string
- `legal_form` — string
- `sector` — string
- `size_category` — string
- `audit_required` — boolean
- `consolidation` — string
- `accounting_system` — string
- `fiscal_year` — number
- `ifrs` — string
- `engagement_since` — string
- `responsible_partner` — string
- `fee_monthly_czk` — number

## `engagement`
- `id` — string
- `client_id` — string
- `type` — string
- `period` — string
- `status` — string
- `responsible_person` — string
- `fee_czk` — number
- `deadline` — string
- `filed_date` — date
- `notes` — string

## `internal_procedure`
- `title` — string
- `code` — string
- `category` — string
- `version` — string
- `owner` — string
- `last_updated` — date
- `status` — string
- `known_gaps` — string

## `deadline`
- `name` — string
- `type` — string
- `base_date_rule` — date
- `offset_days` — number
- `extension_possible` — boolean
- `extension_condition` — string
- `penalty_czk` — number
- `applies_to` — string

## `tax_ruling`
- `id` — string
- `topic` — string
- `issuing_authority` — string
- `date` — date
- `binding` — boolean
- `area` — string
- `superseded_by` — string
- `practical_impact` — string

## `tax_treaty`
- `countries` — string
- `treaty_number` — string
- `effective_date` — date
- `withholding_rates` — string
- `applicable_articles` — string

## `tax_control`
- `id` — string
- `client_id` — string
- `tax_type` — string
- `period_under_review` — string
- `authority` — string
- `status` — string
- `findings_amount_czk` — number
- `contested` — boolean
