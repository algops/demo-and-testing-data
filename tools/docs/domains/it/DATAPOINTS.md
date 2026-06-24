# IT — Datapoints

Fields from propozice `attributes[]`; edge via `defines_schema`.

## `adr`
- `author` — string
- `category` — string
- `date` — date
- `id` — string
- `linked_incidents` — string
- `status` — string
- `superseded_by` — string
- `title` — string

## `api`
- `auth_method` — string
- `base_url` — string
- `breaking_changes` — string
- `consumer_count` — number
- `docs_url` — string
- `name` — string
- `protocol` — string
- `rate_limit` — string
- `status` — string
- `version` — string

## `database`
- `backup_policy` — string
- `engine` — string
- `hosting` — string
- `name` — string
- `owner_service` — string
- `shared` — string
- `size_gb` — number
- `version` — string

## `dependency`
- `current_version` — string
- `cve_count` — number
- `cve_critical` — number
- `ecosystem` — string
- `last_updated` — date
- `latest_version` — string
- `license` — string
- `name` — string

## `environment`
- `access_control` — string
- `auto_deploy` — boolean
- `cloud_provider` — string
- `name` — string
- `region` — string
- `type` — string
- `url` — string

## `feature_flag`
- `created_date` — date
- `description` — string
- `name` — string
- `owner` — string
- `service` — string
- `stale` — boolean
- `status` — string

## `guideline`
- `category` — string
- `code` — string
- `compliance_status` — string
- `last_updated` — date
- `owner` — string
- `title` — string
- `version` — string

## `incident`
- `detected_at` — date
- `id` — string
- `on_call_person` — string
- `rca_status` — string
- `resolved_at` — date
- `root_cause_category` — string
- `severity` — string
- `status` — string
- `title` — string
- `ttd_minutes` — number
- `ttr_minutes` — number

## `pipeline`
- `avg_duration_min` — number
- `last_failure_reason` — string
- `name` — string
- `platform` — string
- `stages` — string
- `success_rate_pct` — number
- `trigger` — string
- `type` — string

## `runbook`
- `author` — string
- `last_updated` — date
- `linked_alerts` — string
- `service` — string
- `status` — string
- `title` — string

## `service`
- `created_date` — date
- `description` — string
- `framework` — string
- `language` — string
- `last_deploy_date` — date
- `lines_of_code` — number
- `name` — string
- `repo_url` — string
- `status` — string
- `team_owner` — string
- `test_coverage_pct` — number
- `tier` — number
- `type` — string

## `slo`
- `current_value` — string
- `error_budget_remaining_pct` — number
- `metric` — string
- `name` — string
- `service` — string
- `target` — string
- `window` — string

## `team`
- `domain` — string
- `lead` — string
- `member_count` — number
- `name` — string
- `on_call_schedule` — string
- `slack_channel` — string

## `tech_debt`
- `blocked_by` — string
- `category` — string
- `created_date` — date
- `estimated_effort_days` — number
- `id` — string
- `impact` — string
- `priority` — string
- `status` — string
- `title` — string
