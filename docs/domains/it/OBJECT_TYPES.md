# IT — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `service` | Service | name, type, language, framework, team_owner, status, repo_url, description, created_date, last_deploy_date, test_coverage_pct, lines_of_code, tier |
| `api` | API | name, version, protocol, base_url, auth_method, status, docs_url, consumer_count, rate_limit, breaking_changes |
| `database` | Database | name, engine, version, hosting, size_gb, backup_policy, shared, owner_service |
| `pipeline` | Pipeline | name, type, trigger, platform, stages, avg_duration_min, success_rate_pct, last_failure_reason |
| `team` | Team | name, lead, member_count, domain, slack_channel, on_call_schedule |
| `adr` | ADR | id, title, status, date, author, category, superseded_by, linked_incidents |
| `guideline` | Guideline | title, code, category, version, last_updated, owner, compliance_status |
| `dependency` | Dependency | name, ecosystem, current_version, latest_version, license, cve_count, cve_critical, last_updated |
| `environment` | Environment | name, type, cloud_provider, region, url, auto_deploy, access_control |
| `incident` | Incident | id, title, severity, status, detected_at, resolved_at, ttd_minutes, ttr_minutes, rca_status, root_cause_category, on_call_person |
| `tech_debt` | TechDebt | id, title, category, priority, estimated_effort_days, impact, created_date, status, blocked_by |
| `slo` | SLO | name, service, metric, target, current_value, error_budget_remaining_pct, window |
| `runbook` | Runbook | title, service, last_updated, author, status, linked_alerts |
| `feature_flag` | FeatureFlag | name, service, status, created_date, owner, description, stale |
