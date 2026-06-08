# IT — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `service`
- `name` — string
- `type` — string
- `language` — string
- `framework` — string
- `team_owner` — string
- `status` — string
- `repo_url` — string
- `description` — string
- `created_date` — date
- `last_deploy_date` — date
- `test_coverage_pct` — number
- `lines_of_code` — number
- `tier` — number

## `api`
- `name` — string
- `version` — string
- `protocol` — string
- `base_url` — string
- `auth_method` — string
- `status` — string
- `docs_url` — string
- `consumer_count` — number
- `rate_limit` — string
- `breaking_changes` — string

## `database`
- `name` — string
- `engine` — string
- `version` — string
- `hosting` — string
- `size_gb` — number
- `backup_policy` — string
- `shared` — string
- `owner_service` — string

## `pipeline`
- `name` — string
- `type` — string
- `trigger` — string
- `platform` — string
- `stages` — string
- `avg_duration_min` — number
- `success_rate_pct` — number
- `last_failure_reason` — string

## `team`
- `name` — string
- `lead` — string
- `member_count` — number
- `domain` — string
- `slack_channel` — string
- `on_call_schedule` — string

## `adr`
- `id` — string
- `title` — string
- `status` — string
- `date` — date
- `author` — string
- `category` — string
- `superseded_by` — string
- `linked_incidents` — string

## `guideline`
- `title` — string
- `code` — string
- `category` — string
- `version` — string
- `last_updated` — date
- `owner` — string
- `compliance_status` — string

## `dependency`
- `name` — string
- `ecosystem` — string
- `current_version` — string
- `latest_version` — string
- `license` — string
- `cve_count` — number
- `cve_critical` — number
- `last_updated` — date

## `environment`
- `name` — string
- `type` — string
- `cloud_provider` — string
- `region` — string
- `url` — string
- `auto_deploy` — boolean
- `access_control` — string

## `incident`
- `id` — string
- `title` — string
- `severity` — string
- `status` — string
- `detected_at` — date
- `resolved_at` — date
- `ttd_minutes` — number
- `ttr_minutes` — number
- `rca_status` — string
- `root_cause_category` — string
- `on_call_person` — string

## `tech_debt`
- `id` — string
- `title` — string
- `category` — string
- `priority` — string
- `estimated_effort_days` — number
- `impact` — string
- `created_date` — date
- `status` — string
- `blocked_by` — string

## `slo`
- `name` — string
- `service` — string
- `metric` — string
- `target` — string
- `current_value` — string
- `error_budget_remaining_pct` — number
- `window` — string

## `runbook`
- `title` — string
- `service` — string
- `last_updated` — date
- `author` — string
- `status` — string
- `linked_alerts` — string

## `feature_flag`
- `name` — string
- `service` — string
- `status` — string
- `created_date` — date
- `owner` — string
- `description` — string
- `stale` — boolean
